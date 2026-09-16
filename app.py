"""
Aplikasi Akuntansi ala Accurate Online (Modular Monolith, Python stdlib only)
===========================================================================
Cara jalan:  python app.py   -> buka http://localhost:8000
DB: SQLite database.db (dibuat otomatis + seed COA 5-digit, gudang, barang contoh)
Engine inti: Double-Entry (setiap jurnal wajib Debit == Kredit), auto-posting
  - Sales Invoice   -> Dr Piutang / Cr Penjualan (+PPN) + Dr HPP / Cr Persediaan
  - Purchase Invoice-> Dr Persediaan (+PPN Masukan) / Cr Utang Usaha
  - Payment         -> Dr Kas/Bank / Cr Piutang  ATAU  Dr Utang / Cr Kas
  - Inventory       -> Moving Average, stok = SUM(in)-SUM(out)
"""
import json, sqlite3, os, datetime, secrets, hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))
# Prioritas DB: env AKUNTANSIKU_DB (Docker/NUC) -> database.db lokal
DB = os.environ.get("AKUNTANSIKU_DB") or os.path.join(BASE, "database.db")
if not os.path.isabs(DB):
    DB = os.path.join(BASE, DB)
PORT = int(os.environ.get("PORT", "8000"))
PUBLIC = os.path.join(BASE, "public")

# ---------------- DB ----------------
def conn(timeout=30.0):
    c = sqlite3.connect(DB, timeout=timeout, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    try: c.execute("PRAGMA journal_mode=WAL")
    except Exception: pass
    try: c.execute("PRAGMA busy_timeout=30000")
    except Exception: pass
    return c

def rp_int(n):
    """Kebijakan Rupiah integer: bulatkan ke Rp 1 (tanpa sen)."""
    try: return int(round(float(n or 0)))
    except Exception: return 0

SCHEMA = """
CREATE TABLE IF NOT EXISTS chart_of_accounts(
 id INTEGER PRIMARY KEY AUTOINCREMENT, account_code TEXT UNIQUE NOT NULL,
 account_name TEXT NOT NULL, account_type TEXT NOT NULL,
 parent_account_id INTEGER NULL, is_active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS warehouses(
 id INTEGER PRIMARY KEY AUTOINCREMENT, warehouse_code TEXT UNIQUE NOT NULL,
 warehouse_name TEXT NOT NULL, address TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS items(
 id INTEGER PRIMARY KEY AUTOINCREMENT, item_code TEXT UNIQUE NOT NULL,
 item_name TEXT NOT NULL, item_type TEXT NOT NULL DEFAULT 'INVENTORY',
 base_unit TEXT NOT NULL DEFAULT 'PCS',
 inventory_account_id INTEGER NULL, sales_account_id INTEGER NOT NULL,
 cogs_account_id INTEGER NULL, purchase_price REAL DEFAULT 0,
 sales_price REAL DEFAULT 0, avg_cost REAL DEFAULT 0);
CREATE TABLE IF NOT EXISTS customers(
 id INTEGER PRIMARY KEY AUTOINCREMENT, customer_code TEXT UNIQUE NOT NULL,
 customer_name TEXT NOT NULL, email TEXT DEFAULT '',
 receivable_account_id INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS vendors(
 id INTEGER PRIMARY KEY AUTOINCREMENT, vendor_code TEXT UNIQUE NOT NULL,
 vendor_name TEXT NOT NULL, email TEXT DEFAULT '',
 payable_account_id INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS journal_entries(
 id INTEGER PRIMARY KEY AUTOINCREMENT, journal_number TEXT UNIQUE NOT NULL,
 transaction_date TEXT NOT NULL, reference_type TEXT DEFAULT 'MANUAL',
 reference_id INTEGER NULL, description TEXT DEFAULT '',
 status TEXT DEFAULT 'POSTED');
CREATE TABLE IF NOT EXISTS journal_entry_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, journal_entry_id INTEGER NOT NULL REFERENCES journal_entries(id) ON DELETE CASCADE,
 account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id), debit REAL DEFAULT 0, credit REAL DEFAULT 0, memo TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS inventory_transactions(
 id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER NOT NULL REFERENCES items(id),
 warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 transaction_date TEXT NOT NULL, reference_type TEXT DEFAULT '',
 reference_id INTEGER NULL, qty_in REAL DEFAULT 0, qty_out REAL DEFAULT 0,
 cogs_unit_price REAL NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS sales_invoices(
 id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_number TEXT UNIQUE NOT NULL,
 transaction_date TEXT NOT NULL, due_date TEXT NOT NULL, customer_id INTEGER NOT NULL REFERENCES customers(id),
 subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0, total_amount REAL NOT NULL,
 status TEXT DEFAULT 'UNPAID', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS sales_invoice_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, sales_invoice_id INTEGER NOT NULL REFERENCES sales_invoices(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, discount_amount REAL DEFAULT 0, line_total REAL NOT NULL);
CREATE TABLE IF NOT EXISTS purchase_invoices(
 id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_number TEXT UNIQUE NOT NULL,
 transaction_date TEXT NOT NULL, due_date TEXT NOT NULL, vendor_id INTEGER NOT NULL REFERENCES vendors(id),
 subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0, total_amount REAL NOT NULL,
 status TEXT DEFAULT 'UNPAID', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS purchase_invoice_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, purchase_invoice_id INTEGER NOT NULL REFERENCES purchase_invoices(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, line_total REAL NOT NULL);
CREATE TABLE IF NOT EXISTS payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT, payment_number TEXT UNIQUE NOT NULL,
 transaction_date TEXT NOT NULL, kind TEXT NOT NULL,
 contact_id INTEGER NOT NULL, cash_account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id),
 amount REAL NOT NULL, note TEXT DEFAULT '', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS payment_allocations(
 id INTEGER PRIMARY KEY AUTOINCREMENT, payment_id INTEGER NOT NULL REFERENCES payments(id) ON DELETE CASCADE,
 invoice_type TEXT NOT NULL, invoice_id INTEGER NOT NULL, amount REAL NOT NULL);
CREATE TABLE IF NOT EXISTS sales_returns(
 id INTEGER PRIMARY KEY AUTOINCREMENT, return_number TEXT UNIQUE NOT NULL,
 sales_invoice_id INTEGER NOT NULL REFERENCES sales_invoices(id),
 transaction_date TEXT NOT NULL, subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0,
 total_amount REAL NOT NULL, journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS sales_return_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, sales_return_id INTEGER NOT NULL REFERENCES sales_returns(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, line_total REAL NOT NULL);
CREATE TABLE IF NOT EXISTS purchase_returns(
 id INTEGER PRIMARY KEY AUTOINCREMENT, return_number TEXT UNIQUE NOT NULL,
 purchase_invoice_id INTEGER NOT NULL REFERENCES purchase_invoices(id),
 transaction_date TEXT NOT NULL, subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0,
 total_amount REAL NOT NULL, journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS purchase_return_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, purchase_return_id INTEGER NOT NULL REFERENCES purchase_returns(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, line_total REAL NOT NULL);
CREATE TABLE IF NOT EXISTS fixed_assets(
 id INTEGER PRIMARY KEY AUTOINCREMENT, asset_code TEXT UNIQUE NOT NULL, asset_name TEXT NOT NULL,
 purchase_date TEXT NOT NULL, cost REAL NOT NULL, useful_months INTEGER NOT NULL DEFAULT 48,
 method TEXT DEFAULT 'STRAIGHT', accum_depr REAL DEFAULT 0, asset_account_id INTEGER NULL,
 depr_expense_account_id INTEGER NULL, accum_account_id INTEGER NULL);
CREATE TABLE IF NOT EXISTS webhooks(
 id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT NOT NULL, url TEXT NOT NULL, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS webhook_logs(
 id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT NOT NULL, payload TEXT DEFAULT '', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
 password_hash TEXT NOT NULL, salt TEXT NOT NULL, full_name TEXT NOT NULL,
 role TEXT NOT NULL DEFAULT 'KASIR', is_active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS sessions(
 token TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 created_at TEXT NOT NULL, expires_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS activity_logs(
 id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NULL, username TEXT DEFAULT '',
 action TEXT NOT NULL, detail TEXT DEFAULT '', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS item_units(
 id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
 unit_code TEXT NOT NULL, conversion REAL NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS salespersons(
 id INTEGER PRIMARY KEY AUTOINCREMENT, sp_code TEXT UNIQUE NOT NULL, sp_name TEXT NOT NULL,
 commission_pct REAL DEFAULT 0, monthly_target REAL DEFAULT 0, is_active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS sales_tradeins(
 id INTEGER PRIMARY KEY AUTOINCREMENT, sales_invoice_id INTEGER NOT NULL REFERENCES sales_invoices(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, agreed_value REAL NOT NULL, note TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS payroll_records(
 id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_date TEXT NOT NULL, employee_name TEXT NOT NULL,
 gross REAL NOT NULL, pph21 REAL DEFAULT 0, net REAL NOT NULL,
 journal_entry_id INTEGER NULL REFERENCES journal_entries(id), created_by TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS branches(
 id INTEGER PRIMARY KEY AUTOINCREMENT, branch_code TEXT UNIQUE NOT NULL,
 branch_name TEXT NOT NULL, address TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS bank_statements(
 id INTEGER PRIMARY KEY AUTOINCREMENT, bank_account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id),
 transaction_date TEXT NOT NULL, description TEXT DEFAULT '', amount REAL NOT NULL,
 direction TEXT NOT NULL, status TEXT DEFAULT 'UNMATCHED',
 matched_line_id INTEGER NULL REFERENCES journal_entry_lines(id));
CREATE TABLE IF NOT EXISTS employees(
 id INTEGER PRIMARY KEY AUTOINCREMENT, emp_code TEXT UNIQUE NOT NULL, full_name TEXT NOT NULL,
 position TEXT DEFAULT '', base_salary REAL DEFAULT 0, leave_quota REAL DEFAULT 12, is_active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS attendances(
 id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
 att_date TEXT NOT NULL, check_in TEXT NULL, check_out TEXT NULL,
 lat REAL NULL, lng REAL NULL, note TEXT DEFAULT '',
 UNIQUE(employee_id, att_date));
CREATE TABLE IF NOT EXISTS leaves(
 id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
 date_from TEXT NOT NULL, date_to TEXT NOT NULL, days REAL NOT NULL,
 reason TEXT DEFAULT '', status TEXT DEFAULT 'PENDING', decided_by TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS inventory_layers(
 id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
 warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 transaction_date TEXT NOT NULL, reference_type TEXT DEFAULT '', reference_id INTEGER NULL,
 qty_in REAL NOT NULL DEFAULT 0, qty_remaining REAL NOT NULL DEFAULT 0, unit_cost REAL NOT NULL DEFAULT 0);
-- Uang muka (DP): terima/bayar dulu, dialokasikan ke invoice kemudian
CREATE TABLE IF NOT EXISTS sales_dps(
 id INTEGER PRIMARY KEY AUTOINCREMENT, dp_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 customer_id INTEGER NOT NULL REFERENCES customers(id), sales_order_id INTEGER NULL REFERENCES sales_orders(id),
 amount REAL NOT NULL, allocated REAL DEFAULT 0, cash_account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id),
 status TEXT DEFAULT 'OPEN', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS sales_dp_allocations(
 id INTEGER PRIMARY KEY AUTOINCREMENT, dp_id INTEGER NOT NULL REFERENCES sales_dps(id) ON DELETE CASCADE,
 invoice_id INTEGER NOT NULL REFERENCES sales_invoices(id), amount REAL NOT NULL);
CREATE TABLE IF NOT EXISTS purchase_dps(
 id INTEGER PRIMARY KEY AUTOINCREMENT, dp_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 vendor_id INTEGER NOT NULL REFERENCES vendors(id), purchase_order_id INTEGER NULL REFERENCES purchase_orders(id),
 amount REAL NOT NULL, allocated REAL DEFAULT 0, cash_account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id),
 status TEXT DEFAULT 'OPEN', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS purchase_dp_allocations(
 id INTEGER PRIMARY KEY AUTOINCREMENT, dp_id INTEGER NOT NULL REFERENCES purchase_dps(id) ON DELETE CASCADE,
 invoice_id INTEGER NOT NULL REFERENCES purchase_invoices(id), amount REAL NOT NULL);
-- Giro: terima (AR) / keluar (AP), status POSTED -> CAIR / TOLAK
CREATE TABLE IF NOT EXISTS giros(
 id INTEGER PRIMARY KEY AUTOINCREMENT, giro_number TEXT UNIQUE NOT NULL, kind TEXT NOT NULL,
 contact_id INTEGER NOT NULL, giro_no TEXT DEFAULT '', bank_name TEXT DEFAULT '',
 issue_date TEXT NOT NULL, due_date TEXT NOT NULL, amount REAL NOT NULL,
 status TEXT DEFAULT 'POSTED', journal_entry_id INTEGER NULL REFERENCES journal_entries(id),
 clear_journal_id INTEGER NULL REFERENCES journal_entries(id), note TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS giro_allocations(
 id INTEGER PRIMARY KEY AUTOINCREMENT, giro_id INTEGER NOT NULL REFERENCES giros(id) ON DELETE CASCADE,
 invoice_type TEXT NOT NULL, invoice_id INTEGER NOT NULL, amount REAL NOT NULL);
CREATE TABLE IF NOT EXISTS period_locks(
 year TEXT PRIMARY KEY, locked_by TEXT DEFAULT '', locked_at TEXT NOT NULL);
-- Tahap2: master tarif pajak + approval workflow maker-checker
CREATE TABLE IF NOT EXISTS taxes(
 id INTEGER PRIMARY KEY AUTOINCREMENT, tax_code TEXT UNIQUE NOT NULL, tax_name TEXT NOT NULL,
 rate REAL NOT NULL DEFAULT 11, masukan_account_id INTEGER NULL REFERENCES chart_of_accounts(id),
 keluaran_account_id INTEGER NULL REFERENCES chart_of_accounts(id), is_active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS approvals(
 id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, ref_type TEXT NOT NULL, ref_id INTEGER NOT NULL,
 amount INTEGER DEFAULT 0, requested_by TEXT DEFAULT '', status TEXT DEFAULT 'PENDING',
 decided_by TEXT DEFAULT '', created_at TEXT NOT NULL, decided_at TEXT DEFAULT '');
-- Rantai dokumen penjualan: Quotation -> Order -> Delivery -> Invoice (non-posting kecuali DO & SI)
CREATE TABLE IF NOT EXISTS sales_quotations(
 id INTEGER PRIMARY KEY AUTOINCREMENT, quotation_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 customer_id INTEGER NOT NULL REFERENCES customers(id), subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0,
 total_amount REAL NOT NULL, status TEXT DEFAULT 'OPEN', notes TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS sales_quotation_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, quotation_id INTEGER NOT NULL REFERENCES sales_quotations(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, discount_pct REAL DEFAULT 0, discount_pct2 REAL DEFAULT 0,
 discount_amount REAL DEFAULT 0, line_total REAL NOT NULL, description TEXT DEFAULT '',
 unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1);
CREATE TABLE IF NOT EXISTS sales_orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT, order_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 customer_id INTEGER NOT NULL REFERENCES customers(id), quotation_id INTEGER NULL REFERENCES sales_quotations(id),
 subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0, total_amount REAL NOT NULL, status TEXT DEFAULT 'OPEN', notes TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS sales_order_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, sales_order_id INTEGER NOT NULL REFERENCES sales_orders(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, discount_pct REAL DEFAULT 0, discount_pct2 REAL DEFAULT 0,
 discount_amount REAL DEFAULT 0, line_total REAL NOT NULL, description TEXT DEFAULT '',
 unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1);
CREATE TABLE IF NOT EXISTS delivery_orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT, delivery_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 sales_order_id INTEGER NULL REFERENCES sales_orders(id), customer_id INTEGER NOT NULL REFERENCES customers(id),
 status TEXT DEFAULT 'POSTED', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS delivery_order_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, delivery_order_id INTEGER NOT NULL REFERENCES delivery_orders(id) ON DELETE CASCADE,
 sales_order_line_id INTEGER NULL REFERENCES sales_order_lines(id),
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, cogs_total REAL DEFAULT 0, invoiced_qty REAL DEFAULT 0,
 unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1);
-- Rantai dokumen pembelian: Requisition -> Order -> Receive -> Invoice
CREATE TABLE IF NOT EXISTS purchase_requisitions(
 id INTEGER PRIMARY KEY AUTOINCREMENT, requisition_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 vendor_id INTEGER NULL REFERENCES vendors(id), requester TEXT DEFAULT '', status TEXT DEFAULT 'OPEN', notes TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS purchase_requisition_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, requisition_id INTEGER NOT NULL REFERENCES purchase_requisitions(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), quantity REAL NOT NULL, est_price REAL DEFAULT 0,
 unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1);
CREATE TABLE IF NOT EXISTS purchase_orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT, order_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 vendor_id INTEGER NOT NULL REFERENCES vendors(id), requisition_id INTEGER NULL REFERENCES purchase_requisitions(id),
 subtotal REAL NOT NULL, tax_amount REAL DEFAULT 0, total_amount REAL NOT NULL, status TEXT DEFAULT 'OPEN', notes TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS purchase_order_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, purchase_order_id INTEGER NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, line_total REAL NOT NULL,
 unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1);
CREATE TABLE IF NOT EXISTS receive_items(
 id INTEGER PRIMARY KEY AUTOINCREMENT, receive_number TEXT UNIQUE NOT NULL, transaction_date TEXT NOT NULL,
 purchase_order_id INTEGER NULL REFERENCES purchase_orders(id), vendor_id INTEGER NOT NULL REFERENCES vendors(id),
 subtotal REAL NOT NULL, status TEXT DEFAULT 'POSTED', journal_entry_id INTEGER NULL REFERENCES journal_entries(id));
CREATE TABLE IF NOT EXISTS receive_item_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT, receive_id INTEGER NOT NULL REFERENCES receive_items(id) ON DELETE CASCADE,
 purchase_order_line_id INTEGER NULL REFERENCES purchase_order_lines(id),
 item_id INTEGER NOT NULL REFERENCES items(id), warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
 quantity REAL NOT NULL, unit_price REAL NOT NULL, line_total REAL NOT NULL, billed_qty REAL DEFAULT 0,
 unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1);
"""

def init_db():
    first = not os.path.exists(DB)
    c = conn(); c.executescript(SCHEMA); c.commit()
    for sql in [
        "ALTER TABLE vendors ADD COLUMN credit_limit REAL DEFAULT 0",        "ALTER TABLE sales_invoice_lines ADD COLUMN unit_code TEXT DEFAULT ''",
        "ALTER TABLE sales_invoice_lines ADD COLUMN unit_qty REAL DEFAULT 0",
        "ALTER TABLE sales_invoice_lines ADD COLUMN unit_conv REAL DEFAULT 1",
        "ALTER TABLE purchase_invoice_lines ADD COLUMN unit_code TEXT DEFAULT ''",
        "ALTER TABLE purchase_invoice_lines ADD COLUMN unit_qty REAL DEFAULT 0",
        "ALTER TABLE purchase_invoice_lines ADD COLUMN unit_conv REAL DEFAULT 1",
        "ALTER TABLE sales_invoices ADD COLUMN salesperson_id INTEGER NULL",
        "ALTER TABLE sales_invoices ADD COLUMN commission_amount REAL DEFAULT 0",
        "ALTER TABLE sales_invoices ADD COLUMN commission_journal_id INTEGER NULL",
        "ALTER TABLE warehouses ADD COLUMN branch_id INTEGER NULL",
        "ALTER TABLE items ADD COLUMN cost_method TEXT DEFAULT 'AVERAGE'",
        "ALTER TABLE sales_invoice_lines ADD COLUMN sales_order_line_id INTEGER NULL",
        "ALTER TABLE sales_invoices ADD COLUMN sales_order_id INTEGER NULL",
        "ALTER TABLE sales_invoices ADD COLUMN delivery_order_id INTEGER NULL",
        "ALTER TABLE purchase_invoice_lines ADD COLUMN purchase_order_line_id INTEGER NULL",
        "ALTER TABLE purchase_invoices ADD COLUMN purchase_order_id INTEGER NULL",
        "ALTER TABLE purchase_invoices ADD COLUMN receive_item_id INTEGER NULL",
        "ALTER TABLE purchase_invoice_lines ADD COLUMN receive_line_id INTEGER NULL",
        "ALTER TABLE customers ADD COLUMN credit_limit REAL DEFAULT 0",
        "ALTER TABLE customers ADD COLUMN terms TEXT DEFAULT ''",
        "ALTER TABLE customers ADD COLUMN term_days INTEGER DEFAULT 0",
        "ALTER TABLE sales_invoices ADD COLUMN tax_rate REAL DEFAULT 11",
        "ALTER TABLE purchase_invoices ADD COLUMN tax_rate REAL DEFAULT 11",
        "ALTER TABLE sales_quotations ADD COLUMN tax_rate REAL DEFAULT 11",
        "ALTER TABLE sales_orders ADD COLUMN tax_rate REAL DEFAULT 11",
        "ALTER TABLE purchase_orders ADD COLUMN tax_rate REAL DEFAULT 11",
    ]:
        try: c.execute(sql)
        except Exception: pass
    c.commit()
    for tbl in ("sales_quotation_lines","sales_order_lines","delivery_order_lines","sales_invoice_lines",
                "purchase_requisition_lines","purchase_order_lines","receive_item_lines","purchase_invoice_lines",
                "sales_return_lines","purchase_return_lines"):
        try: c.execute(f"ALTER TABLE {tbl} ADD COLUMN description TEXT DEFAULT ''")
        except Exception: pass
    c.commit()
    # Lepas warehouse_id dari baris Penawaran & Pesanan (sesuai Accurate: gudang dipilih saat kirim/faktur)
    for tbl, fk, fkcol in (("sales_quotation_lines","sales_quotations","quotation_id"),
                           ("sales_order_lines","sales_orders","sales_order_id")):
        cols = [r[1] for r in c.execute(f"PRAGMA table_info({tbl})").fetchall()]
        if "warehouse_id" in cols:
            c.execute("PRAGMA foreign_keys=OFF")
            c.execute(f"""CREATE TABLE {tbl}_new(
             id INTEGER PRIMARY KEY AUTOINCREMENT, {fkcol} INTEGER NOT NULL REFERENCES {fk}(id) ON DELETE CASCADE,
             item_id INTEGER NOT NULL REFERENCES items(id),
             quantity REAL NOT NULL, unit_price REAL NOT NULL, discount_pct REAL DEFAULT 0, discount_pct2 REAL DEFAULT 0,
             discount_amount REAL DEFAULT 0, line_total REAL NOT NULL, description TEXT DEFAULT '',
             unit_code TEXT DEFAULT '', unit_qty REAL DEFAULT 0, unit_conv REAL DEFAULT 1)""")
            descsel = ",description" if "description" in cols else ",''"
            c.execute(f"""INSERT INTO {tbl}_new(id,{fkcol},item_id,quantity,unit_price,discount_pct,discount_pct2,
             discount_amount,line_total{descsel},unit_code,unit_qty,unit_conv)
             SELECT id,{fkcol},item_id,quantity,unit_price,discount_pct,discount_pct2,
             discount_amount,line_total{descsel},unit_code,unit_qty,unit_conv FROM {tbl}""")
            c.execute(f"DROP TABLE {tbl}")
            c.execute(f"ALTER TABLE {tbl}_new RENAME TO {tbl}")
            c.execute("PRAGMA foreign_keys=ON")
    c.commit()
    for code, name, typ in [("64002","Beban Komisi Penjualan","EXPENSE"),("23002","Utang Komisi","LIABILITY"),("22002","Utang PPh 21","LIABILITY"),("13002","Barang Dalam Perjalanan","ASSET"),("21201","Uang Muka Penjualan","LIABILITY"),("12002","Uang Muka Pembelian","ASSET"),("12003","Giro Diterima","ASSET"),("21301","Giro Diterbitkan","LIABILITY"),("32002","Ikhtisar Laba/Rugi","EQUITY")]:
        c.execute("INSERT OR IGNORE INTO chart_of_accounts(account_code,account_name,account_type) VALUES(?,?,?)",(code,name,typ))
    c.commit()
    # Tahap2: seed master tarif pajak
    try:
        ppn_in = acct(c,"14001"); ppn_out = acct(c,"22001")
        c.execute("INSERT OR IGNORE INTO taxes(tax_code,tax_name,rate,masukan_account_id,keluaran_account_id) VALUES('PPN11','PPN 11%',11,?,?)",(ppn_in,ppn_out))
        c.execute("INSERT OR IGNORE INTO taxes(tax_code,tax_name,rate) VALUES('PPN0','PPN 0% (ekspor/bebas)',0)")
        c.execute("INSERT OR IGNORE INTO taxes(tax_code,tax_name,rate) VALUES('NONPPN','Non-PPN',0)")
    except Exception: pass
    c.commit()
    c.execute("INSERT OR IGNORE INTO branches(branch_code,branch_name,address) VALUES('PUSAT','Kantor Pusat','Jakarta')")
    pus = c.execute("SELECT id FROM branches WHERE branch_code='PUSAT'").fetchone()["id"]
    c.execute("UPDATE warehouses SET branch_id=? WHERE branch_id IS NULL", (pus,))
    c.commit()
    c.execute("INSERT OR IGNORE INTO employees(emp_code,full_name,position,base_salary) VALUES('EMP-001','Andi','Operator',5000000)")
    c.commit()
    # --- Tahap1: dukung lock bulanan YYYY-MM (kompatibel lock tahunan lama) ---
    try: c.execute("ALTER TABLE period_locks ADD COLUMN period TEXT")
    except Exception: pass
    try: c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_period_locks_period ON period_locks(period) WHERE period IS NOT NULL")
    except Exception: pass
    try: c.execute("CREATE TABLE IF NOT EXISTS doc_sequences(seq_key TEXT PRIMARY KEY, last_no INTEGER DEFAULT 0)")
    except Exception: pass
    c.commit()
    # --- Tahap1: bulatkan semua nominal uang ke Rp integer (tanpa sen) ---
    try:
        money_tables = {
            "items": ["purchase_price","sales_price","avg_cost"],
            "sales_invoices": ["subtotal","tax_amount","total_amount","commission_amount"],
            "sales_invoice_lines": ["unit_price","discount_amount","line_total"],
            "purchase_invoices": ["subtotal","tax_amount","total_amount"],
            "purchase_invoice_lines": ["unit_price","line_total"],
            "payments": ["amount"], "payment_allocations": ["amount"],
            "sales_returns": ["subtotal","tax_amount","total_amount"],
            "purchase_returns": ["subtotal","tax_amount","total_amount"],
            "journal_entry_lines": ["debit","credit"],
            "sales_dps": ["amount","allocated"], "sales_dp_allocations": ["amount"],
            "purchase_dps": ["amount","allocated"], "purchase_dp_allocations": ["amount"],
            "giros": ["amount"], "giro_allocations": ["amount"],
            "payroll_records": ["gross","pph21","net"],
            "fixed_assets": ["cost","accum_depr"],
            "bank_statements": ["amount"],
            "inventory_transactions": ["cogs_unit_price"],
            "inventory_layers": ["unit_cost"],
        }
        for tbl, cols in money_tables.items():
            try:
                existing = {r[1] for r in c.execute(f"PRAGMA table_info({tbl})").fetchall()}
            except Exception: continue
            for col in cols:
                if col in existing:
                    try: c.execute(f"UPDATE {tbl} SET {col}=CAST(ROUND({col}) AS INTEGER) WHERE {col} IS NOT NULL")
                    except Exception: pass
        c.commit()
    except Exception: pass
    if first or c.execute("SELECT COUNT(*) n FROM chart_of_accounts").fetchone()["n"] == 0:
        seed(c)
    c.close()

def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100000).hex()

def make_user(c, username, password, full_name, role):
    salt = secrets.token_hex(8)
    c.execute("INSERT OR IGNORE INTO users(username,password_hash,salt,full_name,role) VALUES(?,?,?,?,?)",
        (username, hash_pw(password, salt), salt, full_name, role))

def acct(c, code):
    r = c.execute("SELECT id FROM chart_of_accounts WHERE account_code=?", (code,)).fetchone()
    return r["id"] if r else None

def seed(c):
    coa = [
        ("11001","Kas","ASSET"),("11002","Bank BCA","ASSET"),
        ("12001","Piutang Usaha","ASSET"),("13001","Persediaan Barang","ASSET"),
        ("14001","PPN Masukan","ASSET"),
        ("15001","Peralatan","ASSET"),("15002","Akum. Penyusutan Peralatan","ASSET"),
        ("21001","Utang Usaha","LIABILITY"),("22001","Utang PPN Keluaran","LIABILITY"),
        ("23001","Utang Gaji","LIABILITY"),
        ("31001","Modal","EQUITY"),("32001","Laba Ditahan","EQUITY"),
        ("41001","Penjualan Produk","REVENUE"),("42001","Pendapatan Jasa","REVENUE"),
        ("51001","Harga Pokok Penjualan","COGS"),
        ("61001","Beban Gaji","EXPENSE"),("62001","Beban Listrik","EXPENSE"),
        ("63001","Beban Sewa","EXPENSE"),("64001","Beban Penyusutan","EXPENSE"),
        ("71001","Pendapatan Lain-lain","REVENUE"),("72001","Beban Lain-lain","EXPENSE"),
        ("81001","Beban Pajak Penghasilan","EXPENSE"),
    ]
    for code, name, typ in coa:
        c.execute("INSERT OR IGNORE INTO chart_of_accounts(account_code,account_name,account_type) VALUES(?,?,?)", (code, name, typ))
    c.execute("INSERT OR IGNORE INTO warehouses(warehouse_code,warehouse_name,address) VALUES('GUD-01','Gudang Utama','Jakarta'),('GUD-02','Gudang Cabang','Bandung')")
    inv, sales, cogs = acct(c,"13001"), acct(c,"41001"), acct(c,"51001")
    jasa = acct(c,"42001")
    c.execute("INSERT OR IGNORE INTO items(item_code,item_name,item_type,base_unit,inventory_account_id,sales_account_id,cogs_account_id,purchase_price,sales_price,avg_cost) VALUES(?,?,?,?,?,?,?,?,?,?)",
        ("BRG-001","Laptop 14in","INVENTORY","PCS",inv,sales,cogs,8000000,10500000,8000000))
    c.execute("INSERT OR IGNORE INTO items(item_code,item_name,item_type,base_unit,inventory_account_id,sales_account_id,cogs_account_id,purchase_price,sales_price,avg_cost) VALUES(?,?,?,?,?,?,?,?,?,?)",
        ("BRG-002","Mouse Wireless","INVENTORY","PCS",inv,sales,cogs,120000,180000,120000))
    c.execute("INSERT OR IGNORE INTO items(item_code,item_name,item_type,base_unit,sales_account_id,sales_price) VALUES('JASA-001','Jasa Service','SERVICE',?,?,?)",
        ("JAM", jasa, 150000))
    piut = acct(c,"12001"); ut = acct(c,"21001")
    c.execute("INSERT OR IGNORE INTO customers(customer_code,customer_name,email,receivable_account_id) VALUES('CUST-001','PT Maju Jaya','halo@maju.id',?)", (piut,))
    c.execute("INSERT OR IGNORE INTO vendors(vendor_code,vendor_name,email,payable_account_id) VALUES('VEND-001','PT Supplier Abadi','po@supplier.id',?)", (ut,))
    make_user(c, "admin", "admin123", "Administrator", "ADMIN")
    make_user(c, "manager", "manager123", "Manajer", "MANAGER")
    make_user(c, "kasir", "kasir123", "Kasir", "KASIR")
    m = c.execute("SELECT id FROM items WHERE item_code='BRG-002'").fetchone()
    if m:
        c.execute("INSERT OR IGNORE INTO item_units(item_id,unit_code,conversion) VALUES(?,?,1)", (m["id"], "PCS"))
        if c.execute("SELECT COUNT(*) n FROM item_units WHERE item_id=? AND unit_code='BOX'", (m["id"],)).fetchone()["n"]==0:
            c.execute("INSERT INTO item_units(item_id,unit_code,conversion) VALUES(?, 'BOX', 10)", (m["id"],))
    c.commit()
    c.commit()
    # stok awal 10 laptop + 50 mouse via transaksi + jurnal penyesuaian modal
    w = c.execute("SELECT id FROM warehouses LIMIT 1").fetchone()["id"]
    today = datetime.date.today().isoformat()
    for code, qty, cost in (("BRG-001",10,8000000),("BRG-002",50,120000)):
        it = c.execute("SELECT id FROM items WHERE item_code=?",(code,)).fetchone()["id"]
        c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?)",
            (it,w,today,"OPENING",qty,cost))
    jn = "JE-OPEN-001"
    c.execute("INSERT OR IGNORE INTO journal_entries(journal_number,transaction_date,reference_type,description) VALUES(?,?,?,?)",
        (jn,today,"OPENING","Saldo awal persediaan vs modal"))
    jid = c.execute("SELECT id FROM journal_entries WHERE journal_number=?",(jn,)).fetchone()["id"]
    if c.execute("SELECT COUNT(*) n FROM journal_entry_lines WHERE journal_entry_id=?",(jid,)).fetchone()["n"]==0:
        total = 10*8000000+50*120000
        c.execute("INSERT INTO journal_entry_lines(journal_entry_id,account_id,debit,credit,memo) VALUES(?,?,?,0,'Saldo awal')",(jid,acct(c,"13001"),total))
        c.execute("INSERT INTO journal_entry_lines(journal_entry_id,account_id,debit,credit,memo) VALUES(?,?,0,?,'Saldo awal')",(jid,acct(c,"31001"),total))
    c.commit()

# ---------------- helpers ----------------
def q(c, sql, args=()):
    return [dict(r) for r in c.execute(sql, args).fetchall()]

def rp(n):
    return "Rp {:,.0f}".format(n or 0).replace(",", ".")

def next_no(c, prefix, table, col):
    """Nomor dokumen atomic anti-duplikat via tabel doc_sequences.
    Fallback ke COUNT bila tabel belum ada (kompatibel DB lama)."""
    day = datetime.date.today().strftime('%Y%m%d')
    key = f"{prefix}-{day}"
    try:
        c.execute("CREATE TABLE IF NOT EXISTS doc_sequences(seq_key TEXT PRIMARY KEY, last_no INTEGER DEFAULT 0)")
        # atomic increment dalam satu statement
        c.execute("INSERT OR IGNORE INTO doc_sequences(seq_key,last_no) VALUES(?,0)", (key,))
        c.execute("UPDATE doc_sequences SET last_no=last_no+1 WHERE seq_key=?", (key,))
        n = c.execute("SELECT last_no FROM doc_sequences WHERE seq_key=?", (key,)).fetchone()[0]
        # pastikan tidak tabrakan dengan data lama (COUNT-based)
        try:
            cnt = c.execute(f"SELECT COUNT(*) n FROM {table}").fetchone()["n"]+1
            if cnt > n:
                n = cnt
                c.execute("UPDATE doc_sequences SET last_no=? WHERE seq_key=?", (n, key))
        except Exception: pass
        return f"{prefix}-{day}-{n:04d}"
    except Exception:
        n = c.execute(f"SELECT COUNT(*) n FROM {table}").fetchone()["n"]+1
        return f"{prefix}-{day}-{n:04d}"

def post_journal(c, number, date, ref_type, ref_id, desc, lines):
    """lines: [(account_id, debit, credit, memo)] — validasi balance, return journal_id.
    Kebijakan Rp integer: semua D/K dibulatkan ke rupiah bulat."""
    lines = [(a, rp_int(d), rp_int(k), m) for a, d, k, m in lines]
    td = sum(l[1] for l in lines); tc = sum(l[2] for l in lines)
    if abs(td-tc) > 0 or td <= 0:
        raise ValueError(f"Jurnal tidak seimbang (D={td} K={tc})")
    cur = c.execute("INSERT INTO journal_entries(journal_number,transaction_date,reference_type,reference_id,description) VALUES(?,?,?,?,?)",
        (number,date,ref_type,ref_id,desc))
    jid = cur.lastrowid
    for a,d,k,m in lines:
        c.execute("INSERT INTO journal_entry_lines(journal_entry_id,account_id,debit,credit,memo) VALUES(?,?,?,?,?)",(jid,a,d,k,m or ""))
    return jid

def stock_of(c, item_id, warehouse_id=None):
    sql = "SELECT COALESCE(SUM(qty_in),0)-COALESCE(SUM(qty_out),0) s FROM inventory_transactions WHERE item_id=?"
    args=[item_id]
    if warehouse_id:
        sql += " AND warehouse_id=?"; args.append(warehouse_id)
    return c.execute(sql,args).fetchone()["s"] or 0

def is_fifo(c, item_id):
    try:
        r = c.execute("SELECT cost_method FROM items WHERE id=?", (item_id,)).fetchone()
        return (r["cost_method"] or "AVERAGE") == "FIFO"
    except Exception:
        return False

def add_layer(c, item_id, warehouse_id, date, ref_type, ref_id, qty, unit_cost):
    c.execute("""INSERT INTO inventory_layers(item_id,warehouse_id,transaction_date,reference_type,reference_id,
        qty_in,qty_remaining,unit_cost) VALUES(?,?,?,?,?,?,?,?)""",
        (item_id,warehouse_id,date,ref_type,ref_id,qty,qty,unit_cost))

def fifo_stock(c, item_id, warehouse_id):
    r = c.execute("SELECT COALESCE(SUM(qty_remaining),0) s FROM inventory_layers WHERE item_id=? AND warehouse_id=?",
        (item_id,warehouse_id)).fetchone()
    return r["s"] or 0

def consume_fifo(c, item_id, warehouse_id, date, ref_type, ref_id, qty):
    """Ambil stok FIFO (lapisan tertua dulu). Return total HPP. Raise jika kurang."""
    if fifo_stock(c,item_id,warehouse_id) < qty-0.005:
        code = c.execute("SELECT item_code FROM items WHERE id=?", (item_id,)).fetchone()["item_code"]
        raise ValueError(f"Stok FIFO {code} kurang (sisa {fifo_stock(c,item_id,warehouse_id)})")
    left = qty; total = 0
    for lay in q(c,"""SELECT * FROM inventory_layers WHERE item_id=? AND warehouse_id=? AND qty_remaining>0.005
        ORDER BY transaction_date,id""",(item_id,warehouse_id)):
        if left <= 0.005: break
        take = min(lay["qty_remaining"], left)
        c.execute("UPDATE inventory_layers SET qty_remaining=qty_remaining-? WHERE id=?",(take,lay["id"]))
        total += take*lay["unit_cost"]; left -= take
    return rp_int(total)

def stock_value(c, item_id, warehouse_id):
    """Nilai persediaan: FIFO pakai sisa layer, Average pakai avg_cost. Rp integer."""
    if is_fifo(c, item_id):
        r = c.execute("SELECT COALESCE(SUM(qty_remaining*unit_cost),0) s FROM inventory_layers WHERE item_id=? AND warehouse_id=?",
            (item_id,warehouse_id)).fetchone()
        return rp_int(r["s"] or 0)
    it = c.execute("SELECT avg_cost FROM items WHERE id=?", (item_id,)).fetchone()
    return rp_int(stock_of(c,item_id,warehouse_id)*(it["avg_cost"] or 0))

def rebuild_fifo(c, item_id):
    """Bangun ulang layer FIFO dari stok saat ini @ avg_cost (dipakai saat ganti metode)."""
    it = c.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    c.execute("DELETE FROM inventory_layers WHERE item_id=?", (item_id,))
    if (it["cost_method"] or "AVERAGE")=="FIFO":
        for w in q(c,"SELECT id FROM warehouses"):
            s = stock_of(c,item_id,w["id"])
            if s > 0.005:
                add_layer(c,item_id,w["id"],datetime.date.today().isoformat(),"REBUILD",None,s,it["avg_cost"] or 0)

def calc_line(c, l, wh_default=None):
    """Hitung baris dokumen: dukung satuan + multi-diskon. Rp integer bulat."""
    it = c.execute("SELECT * FROM items WHERE id=?", (l["item_id"],)).fetchone()
    if not it: raise ValueError("Barang tidak valid")
    qty=float(l["qty"]); price=rp_int(l["price"])
    conv = float(l.get("unit_conv",1)) or 1
    ucode = l.get("unit_code", it["base_unit"])
    base = round(qty*conv,2)
    gross = rp_int(qty*price)
    d1 = rp_int(gross*float(l.get("discount_pct",0))/100)
    d2 = rp_int((gross-d1)*float(l.get("discount_pct2",0))/100)
    disc = rp_int(d1+d2+float(l.get("discount",0)))
    return {"it":it,"qty":qty,"price":price,"conv":conv,"ucode":ucode,"uqty":qty,
        "base":base,"gross":gross,"disc":disc,"lt":rp_int(gross-disc),"p1":float(l.get("discount_pct",0)),"p2":float(l.get("discount_pct2",0)),
        "desc":l.get("description",""),
        "wh":int(l.get("warehouse_id") or wh_default or 0)}

def ship_out(c, it, warehouse_id, date, ref_type, ref_id, base):
    """Keluarkan stok + return (cost_total, unit_cost). FIFO consume / Average pakai avg."""
    if it["item_type"]=="INVENTORY":
        if stock_of(c,it["id"],warehouse_id) < base-0.005:
            raise ValueError(f"Stok {it['item_code']} kurang (sisa {stock_of(c,it['id'],warehouse_id)} {it['base_unit']})")
        if is_fifo(c,it["id"]):
            h = consume_fifo(c,it["id"],warehouse_id,date,ref_type,ref_id,base)
            unit = rp_int(h/base) if base else 0
        else:
            unit = rp_int(it["avg_cost"] or 0); h = rp_int(unit*base)
        c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
            (it["id"],warehouse_id,date,ref_type,ref_id,base,unit))
        return h, unit
    return 0, 0

def receive_in(c, it, warehouse_id, date, ref_type, ref_id, base, unit_cost):
    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
        (it["id"],warehouse_id,date,ref_type,ref_id,base,unit_cost))
    if it["item_type"]=="INVENTORY" and is_fifo(c,it["id"]):
        add_layer(c,it["id"],warehouse_id,date,ref_type,ref_id,base,unit_cost)

def so_fulfill(c, so_line_id):
    """Kembalikan {ordered, delivered, invoiced} satu baris SO."""
    sol = c.execute("SELECT quantity FROM sales_order_lines WHERE id=?", (so_line_id,)).fetchone()
    dlv = c.execute("SELECT COALESCE(SUM(quantity),0) s FROM delivery_order_lines dl JOIN delivery_orders d ON d.id=dl.delivery_order_id WHERE dl.sales_order_line_id=? AND d.status='POSTED'", (so_line_id,)).fetchone()["s"] or 0
    direct = c.execute("SELECT COALESCE(SUM(quantity),0) s FROM sales_invoice_lines WHERE sales_order_line_id=? AND sales_invoice_id IN (SELECT id FROM sales_invoices WHERE status!='VOID')", (so_line_id,)).fetchone()["s"] or 0
    invd = c.execute("SELECT COALESCE(SUM(invoiced_qty),0) s FROM delivery_order_lines WHERE sales_order_line_id=?", (so_line_id,)).fetchone()["s"] or 0
    return {"ordered":sol["quantity"],"delivered":round(dlv+direct,2),"invoiced":round(invd+direct,2)}

def po_fulfill(c, pol_id):
    pol = c.execute("SELECT quantity FROM purchase_order_lines WHERE id=?", (pol_id,)).fetchone()
    rcv = c.execute("SELECT COALESCE(SUM(quantity),0) s FROM receive_item_lines rl JOIN receive_items r ON r.id=rl.receive_id WHERE rl.purchase_order_line_id=? AND r.status='POSTED'", (pol_id,)).fetchone()["s"] or 0
    direct = c.execute("SELECT COALESCE(SUM(quantity),0) s FROM purchase_invoice_lines WHERE purchase_order_line_id=? AND purchase_invoice_id IN (SELECT id FROM purchase_invoices WHERE status!='VOID')", (pol_id,)).fetchone()["s"] or 0
    billed_ri = c.execute("SELECT COALESCE(SUM(billed_qty),0) s FROM receive_item_lines WHERE purchase_order_line_id=?", (pol_id,)).fetchone()["s"] or 0
    return {"ordered":pol["quantity"],"received":round(rcv+direct,2),"billed":round(billed_ri+direct,2)}

def refresh_doc_status(c, kind, doc_id):
    """Update status OPEN/PARTIAL/CLOSED berdasar fulfillment. kind: SQ,SO,PR,PO."""
    if kind=="SO":
        lines = q(c,"SELECT id FROM sales_order_lines WHERE sales_order_id=?", (doc_id,))
        if not lines: return
        st = [so_fulfill(c,l["id"]) for l in lines]
        done = sum(1 for s in st if s["delivered"] >= s["ordered"]-0.005)
        anyx = sum(1 for s in st if s["delivered"] > 0.005)
        cur = "CLOSED" if done==len(st) else ("PARTIAL" if anyx else "OPEN")
        if c.execute("SELECT status FROM sales_orders WHERE id=?", (doc_id,)).fetchone()["status"]!="CLOSED" or cur=="CLOSED":
            if cur=="CLOSED" or c.execute("SELECT status FROM sales_orders WHERE id=?", (doc_id,)).fetchone()["status"] in ("OPEN","PARTIAL"):
                c.execute("UPDATE sales_orders SET status=? WHERE id=?", (cur,doc_id))
    elif kind=="PO":
        lines = q(c,"SELECT id FROM purchase_order_lines WHERE purchase_order_id=?", (doc_id,))
        if not lines: return
        st = [po_fulfill(c,l["id"]) for l in lines]
        done = sum(1 for s in st if s["received"] >= s["ordered"]-0.005)
        anyx = sum(1 for s in st if s["received"] > 0.005)
        cur = "CLOSED" if done==len(st) else ("PARTIAL" if anyx else "OPEN")
        curst = c.execute("SELECT status FROM purchase_orders WHERE id=?", (doc_id,)).fetchone()["status"]
        if cur=="CLOSED" or curst in ("OPEN","PARTIAL"):
            c.execute("UPDATE purchase_orders SET status=? WHERE id=?", (cur,doc_id))

def fire_webhook(c, event, payload):
    try:
        c.execute("INSERT INTO webhook_logs(event,payload,created_at) VALUES(?,?,?)",
            (event, json.dumps(payload)[:2000], datetime.datetime.now().isoformat()))
    except Exception: pass

def paid_of(c, invoice_type, invoice_id):
    r = c.execute("SELECT COALESCE(SUM(amount),0) s FROM payment_allocations WHERE invoice_type=? AND invoice_id=?",
        (invoice_type, invoice_id)).fetchone()
    return r["s"] or 0

def returned_of(c, invoice_type, invoice_id):
    if invoice_type=="AR":
        r = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM sales_returns WHERE sales_invoice_id=?", (invoice_id,)).fetchone()
    else:
        r = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM purchase_returns WHERE purchase_invoice_id=?", (invoice_id,)).fetchone()
    return r["s"] or 0

def outstanding_of(c, invoice_type, invoice_id, total):
    out = total - paid_of(c, invoice_type, invoice_id) - returned_of(c, invoice_type, invoice_id)
    if invoice_type=="AR":
        r = c.execute("SELECT COALESCE(SUM(agreed_value),0) s FROM sales_tradeins WHERE sales_invoice_id=?", (invoice_id,)).fetchone()
        out -= r["s"] or 0
        r = c.execute("SELECT COALESCE(SUM(amount),0) s FROM sales_dp_allocations WHERE invoice_id=?", (invoice_id,)).fetchone()
        out -= r["s"] or 0
        r = c.execute("""SELECT COALESCE(SUM(a.amount),0) s FROM giro_allocations a JOIN giros g ON g.id=a.giro_id
            WHERE a.invoice_type='AR' AND a.invoice_id=? AND g.status IN ('POSTED','CAIR')""", (invoice_id,)).fetchone()
        out -= r["s"] or 0
    else:
        r = c.execute("SELECT COALESCE(SUM(amount),0) s FROM purchase_dp_allocations WHERE invoice_id=?", (invoice_id,)).fetchone()
        out -= r["s"] or 0
        r = c.execute("""SELECT COALESCE(SUM(a.amount),0) s FROM giro_allocations a JOIN giros g ON g.id=a.giro_id
            WHERE a.invoice_type='AP' AND a.invoice_id=? AND g.status IN ('POSTED','CAIR')""", (invoice_id,)).fetchone()
        out -= r["s"] or 0
    return rp_int(out)

def check_lock(c, date_str):
    """Blokir periode terkunci. Dukung bulanan YYYY-MM dan legacy tahunan YYYY."""
    ds = (date_str or "")[:7]
    # bulanan: YYYY-MM
    if len(ds) >= 7 and ds[4] == "-" and ds[:4].isdigit() and ds[5:7].isdigit():
        try:
            cols = [r[1] for r in c.execute("PRAGMA table_info(period_locks)").fetchall()]
            if "period" in cols:
                if c.execute("SELECT COUNT(*) n FROM period_locks WHERE period=?", (ds[:7],)).fetchone()["n"]:
                    raise ValueError(f"Periode {ds[:7]} sudah dikunci (tutup buku). Gunakan tanggal periode berjalan.")
        except ValueError: raise
        except Exception: pass
    y = (date_str or "")[:4]
    if len(y)==4 and y.isdigit() and c.execute("SELECT COUNT(*) n FROM period_locks WHERE year=?", (y,)).fetchone()["n"]:
        raise ValueError(f"Periode {y} sudah dikunci (tutup buku). Gunakan tanggal periode berjalan.")

def refresh_dp(c, kind, dp_id):
    tbl = "sales_dps" if kind=="AR" else "purchase_dps"
    r = c.execute(f"SELECT d.amount,COALESCE(SUM(a.amount),0) al FROM {tbl} d LEFT JOIN {'sales' if kind=='AR' else 'purchase'}_dp_allocations a ON a.dp_id=d.id WHERE d.id=? GROUP BY d.id", (dp_id,)).fetchone()
    al = rp_int(r["al"] or 0)
    amt = rp_int(r["amount"] or 0)
    st = "CLOSED" if al >= amt else ("PARTIAL" if al > 0 else "OPEN")
    c.execute(f"UPDATE {tbl} SET allocated=?,status=? WHERE id=?", (al,st,dp_id))
    return st

def returned_qty(c, rtype, inv_id, item_id):
    """Qty barang yg sudah diretur. rtype: 'SALES' / 'PURCHASE'."""
    if rtype=="SALES":
        r = c.execute("SELECT COALESCE(SUM(l.quantity),0) s FROM sales_return_lines l JOIN sales_returns r ON r.id=l.sales_return_id WHERE r.sales_invoice_id=? AND l.item_id=?", (inv_id, item_id)).fetchone()
    else:
        r = c.execute("SELECT COALESCE(SUM(l.quantity),0) s FROM purchase_return_lines l JOIN purchase_returns r ON r.id=l.purchase_return_id WHERE r.purchase_invoice_id=? AND l.item_id=?", (inv_id, item_id)).fetchone()
    return r["s"] or 0

def refresh_status(c, invoice_type, invoice_id):
    tbl = "sales_invoices" if invoice_type=="AR" else "purchase_invoices"
    total = rp_int(c.execute(f"SELECT total_amount FROM {tbl} WHERE id=?", (invoice_id,)).fetchone()["total_amount"])
    out = outstanding_of(c, invoice_type, invoice_id, total)
    settled = total-out
    st = "PAID" if out <= 0 else ("PARTIAL" if settled > 0 else "UNPAID")
    c.execute(f"UPDATE {tbl} SET status=? WHERE id=?", (st, invoice_id))
    return st

def auth_user(c, handler):
    h = handler.headers.get("Authorization", "")
    tok = h[7:] if h.startswith("Bearer ") else ""
    if not tok:
        qs = parse_qs(urlparse(handler.path).query)
        tok = qs.get("token", [""])[0]
    if not tok: return None
    return c.execute("SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token=? AND s.expires_at>? AND u.is_active=1",
        (tok, datetime.datetime.now().isoformat())).fetchone()

def need(user, *roles):
    if not user: raise PermissionError("Belum login")
    if user["role"] not in roles: raise PermissionError(f"Akses ditolak untuk peran {user['role']}")

def reverse_journal(c, orig_id, number, date, desc):
    """Jurnal pembalik: mirror D<->K dari jurnal asli. Return id jurnal baru."""
    orig = c.execute("SELECT * FROM journal_entries WHERE id=?", (orig_id,)).fetchone()
    if not orig: raise ValueError("Jurnal asli tidak ditemukan")
    lines = q(c, "SELECT account_id,debit,credit,memo FROM journal_entry_lines WHERE journal_entry_id=?", (orig_id,))
    if not lines: raise ValueError("Jurnal asli kosong")
    return post_journal(c, number, date, "REVERSAL", orig_id, desc,
        [(l["account_id"], l["credit"], l["debit"], "Reversal: "+(l["memo"] or "")) for l in lines])

# ---------------- HTTP ----------------
class H(BaseHTTPRequestHandler):
    server_version = "AccurateClone/1.0"
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        if code==200 and getattr(self, "_alog", None):
            try:
                lc = conn()
                lc.execute("INSERT INTO activity_logs(user_id,username,action,detail,created_at) VALUES(?,?,?,?,?)",
                    (self._alog[0], self._alog[1], self._alog[2], self._alog[3], datetime.datetime.now().isoformat()))
                lc.commit(); lc.close()
            except Exception: pass
            self._alog = None
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def _body(self):
        try: return json.loads(self.rfile.read(int(self.headers.get("Content-Length",0) or 0)).decode() or "{}")
        except Exception: return {}
    def do_GET(self):
        p = urlparse(self.path); path = p.path; qs = parse_qs(p.query)
        if path in ("/", "/index.html"):
            return self.serve_static("index.html")
        if path == "/app.js": return self.serve_static("app.js")
        if path == "/styles.css": return self.serve_static("styles.css")
        if not path.startswith("/api"):
            return self.serve_static("index.html")
        c = conn()
        try:
            me = auth_user(c, self)
            if not me: return self._json({"error":"Belum login"},401)
            if path in ("/api/reports/trial-balance","/api/reports/profit-loss","/api/reports/balance-sheet","/api/reports/cash-flow"):
                need(me,"ADMIN","MANAGER")
            if path=="/api/users": need(me,"ADMIN")
            if path=="/api/activity": need(me,"ADMIN","MANAGER")
            if path=="/api/me": return self._json({"id":me["id"],"username":me["username"],"full_name":me["full_name"],"role":me["role"]})
            if path=="/api/users": return self._json(q(c,"SELECT id,username,full_name,role,is_active FROM users ORDER BY id"))
            if path=="/api/activity": return self._json(q(c,"SELECT * FROM activity_logs ORDER BY id DESC LIMIT 200"))
            if path=="/api/coa": return self._json(q(c,"SELECT * FROM chart_of_accounts ORDER BY account_code"))
            if path=="/api/warehouses": return self._json(q(c,"SELECT * FROM warehouses"))
            if path=="/api/items":
                rows = q(c,"SELECT * FROM items ORDER BY item_code")
                for r in rows:
                    r["stock"] = stock_of(c, r["id"])
                    r["units"] = q(c,"SELECT unit_code,conversion FROM item_units WHERE item_id=?",(r["id"],)) or [{"unit_code":r["base_unit"],"conversion":1}]
                return self._json(rows)
                return self._json(rows)
            if path=="/api/customers": return self._json(q(c,"SELECT * FROM customers"))
            if path=="/api/vendors": return self._json(q(c,"SELECT * FROM vendors"))
            if path=="/api/journals":
                rows = q(c,"SELECT * FROM journal_entries ORDER BY id DESC LIMIT 200")
                for r in rows: r["lines"] = q(c,"SELECT l.*,a.account_code,a.account_name FROM journal_entry_lines l JOIN chart_of_accounts a ON a.id=l.account_id WHERE journal_entry_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/ledger":
                aid = qs.get("account_id",[""])[0]
                sql = "SELECT e.transaction_date,e.journal_number,e.description,l.debit,l.credit FROM journal_entry_lines l JOIN journal_entries e ON e.id=l.journal_entry_id WHERE e.status='POSTED'"
                args=[]
                if aid: sql+=" AND l.account_id=?"; args.append(aid)
                sql+=" ORDER BY e.transaction_date,e.id"
                return self._json(q(c,sql,args))
            if path=="/api/sales":
                rows = q(c,"SELECT s.*,cu.customer_name,sp.sp_name AS salesperson FROM sales_invoices s JOIN customers cu ON cu.id=s.customer_id LEFT JOIN salespersons sp ON sp.id=s.salesperson_id ORDER BY s.id DESC LIMIT 200")
                for r in rows:
                    r["lines"] = q(c,"SELECT l.*,i.item_name FROM sales_invoice_lines l JOIN items i ON i.id=l.item_id WHERE sales_invoice_id=?",(r["id"],))
                    r["paid"] = paid_of(c,"AR",r["id"]); r["returned"] = returned_of(c,"AR",r["id"]); r["outstanding"] = outstanding_of(c,"AR",r["id"],r["total_amount"])
                    tr = q(c,"SELECT t.*,i.item_code FROM sales_tradeins t JOIN items i ON i.id=t.item_id WHERE t.sales_invoice_id=?",(r["id"],))
                    r["tradeins"] = tr; r["tradein_total"] = round(sum(t["agreed_value"] for t in tr),2)
                return self._json(rows)
            if path=="/api/salespersons": return self._json(q(c,"SELECT * FROM salespersons ORDER BY sp_name"))
            if path=="/api/targets":
                need(me,"ADMIN","MANAGER")
                month = qs.get("month",[datetime.date.today().strftime("%Y-%m")])[0]
                out=[]
                for sp in q(c,"SELECT * FROM salespersons WHERE is_active=1"):
                    agg = c.execute("SELECT COALESCE(SUM(total_amount),0) realisasi, COALESCE(SUM(commission_amount),0) komisi, COUNT(*) n FROM sales_invoices WHERE salesperson_id=? AND status!='VOID' AND substr(transaction_date,1,7)=?",(sp["id"],month)).fetchone()
                    tgt = sp["monthly_target"] or 0
                    out.append({"sp_name":sp["sp_name"],"commission_pct":sp["commission_pct"],"target":tgt,
                        "realisasi":agg["realisasi"],"transaksi":agg["n"],"komisi":agg["komisi"],
                        "pencapaian":round(agg["realisasi"]/tgt*100,1) if tgt else 0})
                return self._json({"month":month,"rows":out})
            if path=="/api/payroll":
                need(me,"ADMIN","MANAGER")
                return self._json(q(c,"SELECT * FROM payroll_records ORDER BY id DESC LIMIT 100"))
            if path=="/api/purchases":
                rows = q(c,"SELECT s.*,v.vendor_name FROM purchase_invoices s JOIN vendors v ON v.id=s.vendor_id ORDER BY s.id DESC LIMIT 200")
                for r in rows:
                    r["lines"] = q(c,"SELECT l.*,i.item_name FROM purchase_invoice_lines l JOIN items i ON i.id=l.item_id WHERE purchase_invoice_id=?",(r["id"],))
                    r["paid"] = paid_of(c,"AP",r["id"]); r["returned"] = returned_of(c,"AP",r["id"]); r["outstanding"] = outstanding_of(c,"AP",r["id"],r["total_amount"])
                return self._json(rows)
            if path=="/api/aging":
                typ = qs.get("type",["AR"])[0]
                today = datetime.date.today()
                if typ == "AP":
                    rows = q(c,"SELECT s.id,s.invoice_number,s.transaction_date,s.due_date,s.total_amount,s.status,v.vendor_name AS contact FROM purchase_invoices s JOIN vendors v ON v.id=s.vendor_id WHERE s.status NOT IN ('VOID','PAID') ORDER BY s.due_date")
                    for r in rows:
                        r["paid"] = paid_of(c,"AP",r["id"]); r["returned"] = returned_of(c,"AP",r["id"]); r["outstanding"] = outstanding_of(c,"AP",r["id"],r["total_amount"])
                else:
                    rows = q(c,"SELECT s.id,s.invoice_number,s.transaction_date,s.due_date,s.total_amount,s.status,cu.customer_name AS contact FROM sales_invoices s JOIN customers cu ON cu.id=s.customer_id WHERE s.status NOT IN ('VOID','PAID') ORDER BY s.due_date")
                    for r in rows:
                        r["paid"] = paid_of(c,"AR",r["id"]); r["returned"] = returned_of(c,"AR",r["id"]); r["outstanding"] = outstanding_of(c,"AR",r["id"],r["total_amount"])
                for r in rows:
                    try: dd = (today - datetime.date.fromisoformat(r["due_date"])).days
                    except Exception: dd = 0
                    r["days_overdue"] = max(dd, 0)
                    r["bucket"] = "Lancar" if r["days_overdue"]==0 else ("1-30 hari" if r["days_overdue"]<=30 else ("31-60 hari" if r["days_overdue"]<=60 else ">60 hari"))
                rows = [r for r in rows if r["outstanding"] > 0.005]
                return self._json(rows)
            if path=="/api/payments": return self._json(q(c,"SELECT * FROM payments ORDER BY id DESC LIMIT 200"))
            if path=="/api/taxes": return self._json(q(c,"SELECT * FROM taxes WHERE is_active=1 ORDER BY rate DESC, tax_code"))
            if path=="/api/approvals":
                need(me,"ADMIN","MANAGER","FINANCE")
                return self._json(q(c,"SELECT * FROM approvals ORDER BY id DESC LIMIT 200"))
            if path=="/api/sales-dp":
                rows = q(c,"SELECT d.*,cu.customer_name FROM sales_dps d JOIN customers cu ON cu.id=d.customer_id ORDER BY d.id DESC LIMIT 100")
                for r in rows: r["allocs"] = q(c,"SELECT a.*,s.invoice_number FROM sales_dp_allocations a JOIN sales_invoices s ON s.id=a.invoice_id WHERE a.dp_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/purchase-dp":
                rows = q(c,"SELECT d.*,v.vendor_name FROM purchase_dps d JOIN vendors v ON v.id=d.vendor_id ORDER BY d.id DESC LIMIT 100")
                for r in rows: r["allocs"] = q(c,"SELECT a.*,s.invoice_number FROM purchase_dp_allocations a JOIN purchase_invoices s ON s.id=a.invoice_id WHERE a.dp_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/giros":
                rows = q(c,"SELECT * FROM giros ORDER BY id DESC LIMIT 200")
                for r in rows:
                    nm = c.execute("SELECT customer_name FROM customers WHERE id=?",(r["contact_id"],)).fetchone() if r["kind"]=="AR" else c.execute("SELECT vendor_name FROM vendors WHERE id=?",(r["contact_id"],)).fetchone()
                    r["contact_name"] = (nm[0] if nm else "?")
                    r["allocs"] = q(c,"SELECT * FROM giro_allocations WHERE giro_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/period-locks":
                need(me,"ADMIN","MANAGER")
                return self._json(q(c,"SELECT * FROM period_locks ORDER BY year DESC"))
            if path=="/api/returns":
                typ = qs.get("type",["SALES"])[0]
                if typ=="PURCHASE":
                    return self._json(q(c,"SELECT r.*,s.invoice_number FROM purchase_returns r JOIN purchase_invoices s ON s.id=r.purchase_invoice_id ORDER BY r.id DESC LIMIT 100"))
                return self._json(q(c,"SELECT r.*,s.invoice_number FROM sales_returns r JOIN sales_invoices s ON s.id=r.sales_invoice_id ORDER BY r.id DESC LIMIT 100"))
            if path=="/api/branches":
                return self._json(q(c,"SELECT b.*, (SELECT COUNT(*) FROM warehouses w WHERE w.branch_id=b.id) n_wh FROM branches b ORDER BY b.branch_code"))
            if path=="/api/quotations":
                rows = q(c,"SELECT s.*,cu.customer_name FROM sales_quotations s JOIN customers cu ON cu.id=s.customer_id ORDER BY s.id DESC LIMIT 200")
                for r in rows: r["lines"] = q(c,"SELECT l.*,i.item_name FROM sales_quotation_lines l JOIN items i ON i.id=l.item_id WHERE quotation_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/sales-orders":
                rows = q(c,"SELECT s.*,cu.customer_name FROM sales_orders s JOIN customers cu ON cu.id=s.customer_id ORDER BY s.id DESC LIMIT 200")
                for r in rows:
                    r["lines"] = q(c,"SELECT l.*,i.item_name FROM sales_order_lines l JOIN items i ON i.id=l.item_id WHERE sales_order_id=?",(r["id"],))
                    for l in r["lines"]: l.update(so_fulfill(c,l["id"]))
                return self._json(rows)
            if path=="/api/deliveries":
                rows = q(c,"SELECT d.*,cu.customer_name FROM delivery_orders d JOIN customers cu ON cu.id=d.customer_id ORDER BY d.id DESC LIMIT 200")
                for r in rows: r["lines"] = q(c,"SELECT l.*,i.item_name FROM delivery_order_lines l JOIN items i ON i.id=l.item_id WHERE delivery_order_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/requisitions":
                rows = q(c,"SELECT r.*,v.vendor_name FROM purchase_requisitions r LEFT JOIN vendors v ON v.id=r.vendor_id ORDER BY r.id DESC LIMIT 200")
                for r in rows: r["lines"] = q(c,"SELECT l.*,i.item_name FROM purchase_requisition_lines l JOIN items i ON i.id=l.item_id WHERE requisition_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/purchase-orders":
                rows = q(c,"SELECT s.*,v.vendor_name FROM purchase_orders s JOIN vendors v ON v.id=s.vendor_id ORDER BY s.id DESC LIMIT 200")
                for r in rows:
                    r["lines"] = q(c,"SELECT l.*,i.item_name FROM purchase_order_lines l JOIN items i ON i.id=l.item_id WHERE purchase_order_id=?",(r["id"],))
                    for l in r["lines"]: l.update(po_fulfill(c,l["id"]))
                return self._json(rows)
            if path=="/api/receives":
                rows = q(c,"SELECT r.*,v.vendor_name FROM receive_items r JOIN vendors v ON v.id=r.vendor_id ORDER BY r.id DESC LIMIT 200")
                for r in rows: r["lines"] = q(c,"SELECT l.*,i.item_name FROM receive_item_lines l JOIN items i ON i.id=l.item_id WHERE receive_id=?",(r["id"],))
                return self._json(rows)
            if path=="/api/employees":
                return self._json(q(c,"SELECT * FROM employees ORDER BY full_name"))
            if path=="/api/attendance":
                month = qs.get("month",[datetime.date.today().strftime("%Y-%m")])[0]
                need(me,"ADMIN","MANAGER")
                return self._json(q(c,"""SELECT a.*,e.full_name FROM attendances a JOIN employees e ON e.id=a.employee_id
                    WHERE substr(a.att_date,1,7)=? ORDER BY a.att_date DESC""",(month,)))
            if path=="/api/attendance/summary":
                need(me,"ADMIN","MANAGER")
                month = qs.get("month",[datetime.date.today().strftime("%Y-%m")])[0]
                y, m = int(month[:4]), int(month[7:] if len(month)>7 else month[5:])
                import calendar
                workdays = sum(1 for d in range(1, calendar.monthrange(y,m)[1]+1) if datetime.date(y,m,d).weekday()<6)
                out=[]
                for e in q(c,"SELECT * FROM employees WHERE is_active=1"):
                    rows = q(c,"SELECT * FROM attendances WHERE employee_id=? AND substr(att_date,1,7)=?",(e["id"],month))
                    hadir = sum(1 for r in rows if r["check_in"])
                    telat = sum(1 for r in rows if r["check_in"] and r["check_in"]>"08:00:00")
                    cuti = c.execute("SELECT COALESCE(SUM(days),0) s FROM leaves WHERE employee_id=? AND status='APPROVED' AND substr(date_from,1,7)=?",(e["id"],month)).fetchone()["s"] or 0
                    out.append({"employee":e["full_name"],"hadir":hadir,"telat":telat,"cuti":cuti,
                        "alpa":max(workdays-hadir-int(cuti),0),"workdays":workdays})
                return self._json({"month":month,"rows":out})
            if path=="/api/leaves":
                rows = q(c,"""SELECT l.*,e.full_name FROM leaves l JOIN employees e ON e.id=l.employee_id
                    ORDER BY l.id DESC LIMIT 100""")
                return self._json(rows)
            if path=="/api/reports/ppn":
                need(me,"ADMIN","MANAGER")
                month = qs.get("month",[datetime.date.today().strftime("%Y-%m")])[0]
                def ppn_sum(code, debit_side):
                    r = c.execute("""SELECT COALESCE(SUM(l.debit),0) d, COALESCE(SUM(l.credit),0) k
                        FROM journal_entry_lines l JOIN journal_entries e ON e.id=l.journal_entry_id
                        JOIN chart_of_accounts a ON a.id=l.account_id
                        WHERE e.status='POSTED' AND a.account_code=? AND substr(e.transaction_date,1,7)=?""",
                        (code,month)).fetchone()
                    return rp_int((r["d"]-r["k"]) if debit_side else (r["k"]-r["d"]))
                keluaran = ppn_sum("22001", False)
                masukan = ppn_sum("14001", True)
                selisih = rp_int(keluaran-masukan)
                detail = q(c,"""SELECT e.transaction_date,e.journal_number,e.description,a.account_code,l.debit,l.credit
                    FROM journal_entry_lines l JOIN journal_entries e ON e.id=l.journal_entry_id
                    JOIN chart_of_accounts a ON a.id=l.account_id
                    WHERE e.status='POSTED' AND a.account_code IN ('22001','14001') AND substr(e.transaction_date,1,7)=?
                    ORDER BY e.transaction_date,e.id""",(month,))
                return self._json({"month":month,"keluaran":keluaran,"masukan":masukan,"selisih":selisih,
                    "status":"KURANG BAYAR (utang)" if selisih>0 else ("LEBIH BAYAR" if selisih<0 else "NIHIL"),
                    "detail":detail})
            if path=="/api/reorder":
                since = (datetime.date.today()-datetime.timedelta(days=30)).isoformat()
                out=[]
                for it in q(c,"SELECT * FROM items WHERE item_type='INVENTORY' ORDER BY item_code"):
                    sold = c.execute("""SELECT COALESCE(SUM(qty_out),0) s FROM inventory_transactions
                        WHERE item_id=? AND reference_type='SALES_INVOICE' AND transaction_date>=?""",(it["id"],since)).fetchone()["s"] or 0
                    back = c.execute("""SELECT COALESCE(SUM(qty_in),0) s FROM inventory_transactions
                        WHERE item_id=? AND reference_type IN ('SALES_RETURN','SALES_VOID') AND transaction_date>=?""",(it["id"],since)).fetchone()["s"] or 0
                    net = max(sold-back,0); daily = round(net/30,2)
                    stock = stock_of(c,it["id"])
                    cover = round(stock/daily,1) if daily>0 else 999
                    need_qty = max(round(daily*10-stock,2),0)
                    out.append({"item_code":it["item_code"],"item_name":it["item_name"],"stock":stock,
                        "terjual_30h":net,"rata_hari":daily,"tahan_hari":cover,
                        "saran_order":need_qty,
                        "status":"SEGERA ORDER" if cover<=7 else ("WASPADA" if cover<=14 else "AMAN")})
                out.sort(key=lambda r: (r["tahan_hari"]))
                return self._json(out)
            if path=="/api/reports/branch":
                need(me,"ADMIN","MANAGER")
                month = qs.get("month",[datetime.date.today().strftime("%Y-%m")])[0]
                out=[]
                for br in q(c,"SELECT * FROM branches ORDER BY branch_code"):
                    omzet = c.execute("""SELECT COALESCE(SUM(l.line_total),0) s FROM sales_invoice_lines l
                        JOIN sales_invoices s ON s.id=l.sales_invoice_id JOIN warehouses w ON w.id=l.warehouse_id
                        WHERE w.branch_id=? AND s.status!='VOID' AND substr(s.transaction_date,1,7)=?""",(br["id"],month)).fetchone()["s"]
                    beli = c.execute("""SELECT COALESCE(SUM(l.line_total),0) s FROM purchase_invoice_lines l
                        JOIN purchase_invoices s ON s.id=l.purchase_invoice_id JOIN warehouses w ON w.id=l.warehouse_id
                        WHERE w.branch_id=? AND s.status!='VOID' AND substr(s.transaction_date,1,7)=?""",(br["id"],month)).fetchone()["s"]
                    stok_val = 0
                    for it in q(c,"SELECT id FROM items WHERE item_type='INVENTORY'"):
                        for w in q(c,"SELECT id FROM warehouses WHERE branch_id=?",(br["id"],)):
                            stok_val += stock_value(c,it["id"],w["id"])
                    out.append({"branch":br["branch_code"]+" - "+br["branch_name"],"omzet":omzet,"pembelian":beli,"stok":round(stok_val,2)})
                return self._json({"month":month,"rows":out})
            if path=="/api/reconcile":
                aid = qs.get("account_id",[""])[0]
                filt = "AND s.bank_account_id=?" if aid else ""
                args = [aid] if aid else []
                stmts = q(c,f"""SELECT s.*, a.account_code, a.account_name,
                    e.journal_number AS matched_journal FROM bank_statements s
                    JOIN chart_of_accounts a ON a.id=s.bank_account_id
                    LEFT JOIN journal_entry_lines l ON l.id=s.matched_line_id
                    LEFT JOIN journal_entries e ON e.id=l.journal_entry_id
                    WHERE 1=1 {filt} ORDER BY s.transaction_date, s.id""", args)
                sysfilt = "AND a.id=?" if aid else ""
                sysargs = [aid] if aid else []
                syslines = q(c,f"""SELECT l.id AS line_id, l.debit, l.credit, a.account_code, e.journal_number, e.transaction_date, e.description
                    FROM journal_entry_lines l JOIN journal_entries e ON e.id=l.journal_entry_id
                    JOIN chart_of_accounts a ON a.id=l.account_id
                    WHERE e.status='POSTED' AND a.account_code LIKE '110%' AND (l.debit>0.005 OR l.credit>0.005)
                    AND l.id NOT IN (SELECT matched_line_id FROM bank_statements WHERE matched_line_id IS NOT NULL)
                    {sysfilt} ORDER BY e.transaction_date DESC LIMIT 100""", sysargs)
                return self._json({"statements":stmts,"unmatched_system":syslines})
            if path=="/api/stock":
                rows = q(c,"SELECT * FROM items ORDER BY item_code")
                out=[]
                for it in rows:
                    for w in q(c,"SELECT * FROM warehouses"):
                        s = stock_of(c,it["id"],w["id"])
                        out.append({"item_code":it["item_code"],"item_name":it["item_name"],"warehouse":w["warehouse_name"],
                            "stock":s,"avg_cost":it["avg_cost"],"method":it["cost_method"] if "cost_method" in it.keys() else "AVERAGE",
                            "value":stock_value(c,it["id"],w["id"])})
                return self._json(out)
            if path=="/api/stock-card":
                iid = qs.get("item_id",[""])[0]
                return self._json(q(c,"SELECT t.*,i.item_name,w.warehouse_name FROM inventory_transactions t JOIN items i ON i.id=t.item_id JOIN warehouses w ON w.id=t.warehouse_id WHERE (?='' OR t.item_id=?) ORDER BY t.transaction_date,t.id",(iid,iid)))
            if path=="/api/assets": return self._json(q(c,"SELECT * FROM fixed_assets"))
            if path=="/api/webhooks": return self._json({"webhooks":q(c,"SELECT * FROM webhooks"),"logs":q(c,"SELECT * FROM webhook_logs ORDER BY id DESC LIMIT 50")})
            if path=="/api/reports/trial-balance":
                rows = q(c,"SELECT a.account_code,a.account_name,a.account_type,COALESCE(SUM(l.debit),0) d,COALESCE(SUM(l.credit),0) k FROM chart_of_accounts a LEFT JOIN journal_entry_lines l ON l.account_id=a.id LEFT JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED' GROUP BY a.id ORDER BY a.account_code")
                return self._json(rows)
            if path=="/api/reports/profit-loss":
                rows = q(c,"SELECT a.account_code,a.account_name,a.account_type,COALESCE(SUM(l.credit),0)-COALESCE(SUM(l.debit),0) net_rev,COALESCE(SUM(l.debit),0)-COALESCE(SUM(l.credit),0) net_exp FROM chart_of_accounts a LEFT JOIN journal_entry_lines l ON l.account_id=a.id LEFT JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED' WHERE a.account_type IN ('REVENUE','COGS','EXPENSE') GROUP BY a.id ORDER BY a.account_code")
                rev = sum(r["net_rev"] for r in rows if r["account_type"]=="REVENUE")
                exp = sum(r["net_exp"] for r in rows if r["account_type"] in ("COGS","EXPENSE"))
                return self._json({"lines":rows,"revenue":rev,"expense":exp,"net":rev-exp})
            if path=="/api/reports/balance-sheet":
                rows = q(c,"SELECT a.account_code,a.account_name,a.account_type,COALESCE(SUM(l.debit),0)-COALESCE(SUM(l.credit),0) net_db,COALESCE(SUM(l.credit),0)-COALESCE(SUM(l.debit),0) net_cr FROM chart_of_accounts a LEFT JOIN journal_entry_lines l ON l.account_id=a.id LEFT JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED' WHERE a.account_type IN ('ASSET','LIABILITY','EQUITY') GROUP BY a.id ORDER BY a.account_code")
                pl = q(c,"SELECT COALESCE(SUM(CASE WHEN a.account_type='REVENUE' THEN l.credit-l.debit ELSE 0 END),0)-COALESCE(SUM(CASE WHEN a.account_type IN ('COGS','EXPENSE') THEN l.debit-l.credit ELSE 0 END),0) net FROM journal_entry_lines l JOIN chart_of_accounts a ON a.id=l.account_id JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED'")[0]["net"] or 0
                return self._json({"lines":rows,"net_income":pl})
            if path=="/api/reports/cash-flow":
                # Arus kas dari mutasi akun 110xx pada jurnal POSTED.
                # Klasifikasi per jurnal berdasar akun lawan: 15xxx/aset tetap->investasi, 3xxxx->pendanaan, sisanya operasi.
                journals = q(c,"SELECT id,journal_number,transaction_date,description FROM journal_entries WHERE status='POSTED' ORDER BY transaction_date,id")
                cats = {"operasi":{"in":0,"out":0},"investasi":{"in":0,"out":0},"pendanaan":{"in":0,"out":0}}
                detail=[]
                for j in journals:
                    lines = q(c,"SELECT l.debit,l.credit,a.account_code,a.account_name FROM journal_entry_lines l JOIN chart_of_accounts a ON a.id=l.account_id WHERE l.journal_entry_id=?",(j["id"],))
                    cash = [l for l in lines if l["account_code"].startswith("110")]
                    if not cash: continue
                    others = [l["account_code"] for l in lines if not l["account_code"].startswith("110")]
                    if any(o.startswith("15") for o in others): cat="investasi"
                    elif any(o.startswith("31") or o.startswith("32") for o in others): cat="pendanaan"
                    else: cat="operasi"
                    ci = sum(l["debit"] for l in cash); co = sum(l["credit"] for l in cash)
                    cats[cat]["in"]+=ci; cats[cat]["out"]+=co
                    detail.append({"tanggal":j["transaction_date"],"jurnal":j["journal_number"],"keterangan":j["description"],"kategori":cat,"masuk":ci,"keluar":co})
                net = {k: round(v["in"]-v["out"],2) for k,v in cats.items()}
                return self._json({"summary":[{"kategori":k,"masuk":round(v["in"],2),"keluar":round(v["out"],2),"net":net[k]} for k,v in cats.items()],
                    "net_total": round(sum(net.values()),2), "detail":detail})
            if path=="/api/dashboard":
                omzet = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM sales_invoices WHERE status!='VOID'").fetchone()["s"]
                hut = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM purchase_invoices WHERE status!='VOID'").fetchone()["s"]
                piut = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM sales_invoices WHERE status IN ('UNPAID','PARTIAL')").fetchone()["s"]
                kas = c.execute("SELECT COALESCE(SUM(CASE WHEN a.account_code LIKE '110%' THEN l.debit-l.credit ELSE 0 END),0) s FROM journal_entry_lines l JOIN chart_of_accounts a ON a.id=l.account_id JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED'").fetchone()["s"]
                low = []
                for r in c.execute("SELECT id,item_code,item_name FROM items").fetchall():
                    if stock_of(c, r["id"]) < 5:
                        low.append({"item_code": r["item_code"], "item_name": r["item_name"]})
                open_so = c.execute("SELECT COUNT(*) n FROM sales_orders WHERE status IN ('OPEN','PARTIAL')").fetchone()["n"]
                open_po = c.execute("SELECT COUNT(*) n FROM purchase_orders WHERE status IN ('OPEN','PARTIAL')").fetchone()["n"]
                return self._json({"omzet":omzet,"pembelian":hut,"piutang_outstanding":piut,"kas_bank":kas,"stok_menipis":low,
                    "open_so":open_so,"open_po":open_po,
                    "forecast":"Rata-rata 3 invoice terakhir diproyeksikan: kas +%.0f%%/bln (lihat modul Laporan > Forecast)" % 8})
            if path=="/api/forecast":
                rows = q(c,"SELECT total_amount FROM sales_invoices WHERE status!='VOID' ORDER BY id DESC LIMIT 3")
                avg = sum(r["total_amount"] for r in rows)/len(rows) if rows else 0
                return self._json([{"bulan":f"+{i} bln","proyeksi_kas_masuk":rp_int(avg*(1+0.08*i))} for i in range(1,4)])
            if path=="/api/dashboard/monthly":
                out=[]
                t = datetime.date.today()
                for i in range(5,-1,-1):
                    yy, mm = t.year, t.month-i
                    while mm<1: mm+=12; yy-=1
                    key = f"{yy:04d}-{mm:02d}"
                    om = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM sales_invoices WHERE status!='VOID' AND substr(transaction_date,1,7)=?",(key,)).fetchone()["s"]
                    be = c.execute("SELECT COALESCE(SUM(total_amount),0) s FROM purchase_invoices WHERE status!='VOID' AND substr(transaction_date,1,7)=?",(key,)).fetchone()["s"]
                    out.append({"bulan":key,"omzet":om,"pembelian":be})
                return self._json(out)
            if path=="/api/backup":
                need(me,"ADMIN")
                with open(DB,"rb") as f: blob=f.read()
                self.send_response(200)
                self.send_header("Content-Type","application/octet-stream")
                self.send_header("Content-Disposition",'attachment; filename="backup-akuntansi.db"')
                self.send_header("Content-Length",str(len(blob)))
                self.end_headers(); self.wfile.write(blob)
                return
            return self._json({"error":"not found"},404)
        except PermissionError as e: return self._json({"error":str(e)},403)
        except Exception as e: return self._json({"error":str(e)},500)
        finally: c.close()

    def do_POST(self):
        p = urlparse(self.path); path = p.path; b = self._body(); c = conn()
        try:
            if path=="/api/login":
                u = c.execute("SELECT * FROM users WHERE username=? AND is_active=1",(b.get("username",""),)).fetchone()
                if not u or u["password_hash"] != hash_pw(b.get("password",""), u["salt"]):
                    return self._json({"error":"Username/password salah"},401)
                tok = secrets.token_hex(24)
                exp = (datetime.datetime.now()+datetime.timedelta(hours=12)).isoformat()
                c.execute("INSERT INTO sessions(token,user_id,created_at,expires_at) VALUES(?,?,?,?)",
                    (tok,u["id"],datetime.datetime.now().isoformat(),exp))
                c.commit()
                self._alog = (u["id"], u["username"], "login", "Login berhasil")
                # Tahap1: paksa ganti password default bawaan
                must_change = False
                try:
                    defaults = {"admin":"admin123","manager":"manager123","kasir":"kasir123"}
                    if u["username"] in defaults and b.get("password","") == defaults[u["username"]]:
                        must_change = True
                except Exception: pass
                return self._json({"ok":True,"token":tok,"role":u["role"],"full_name":u["full_name"],"expires_at":exp,"must_change_password":must_change})
            if path=="/api/logout":
                me = auth_user(c, self)
                if me: c.execute("DELETE FROM sessions WHERE token=?",(self.headers.get("Authorization","")[7:],)); c.commit()
                return self._json({"ok":True})
            if path=="/api/change-password":
                me = auth_user(c, self)
                if not me: return self._json({"error":"Belum login"},401)
                if me["password_hash"] != hash_pw(b.get("old",""), me["salt"]):
                    return self._json({"error":"Password lama salah"},400)
                if len(b.get("new","")) < 6: return self._json({"error":"Password baru min. 6 karakter"},400)
                salt = secrets.token_hex(8)
                c.execute("UPDATE users SET password_hash=?,salt=? WHERE id=?",(hash_pw(b["new"],salt),salt,me["id"]))
                h = self.headers.get("Authorization",""); tok = h[7:] if h.startswith("Bearer ") else ""
                c.execute("DELETE FROM sessions WHERE user_id=? AND token!=?",(me["id"],tok))
                c.commit()
                self._alog = (me["id"], me["username"], "change-password", "Ganti password")
                return self._json({"ok":True})
            me = auth_user(c, self)
            if not me: return self._json({"error":"Belum login"},401)
            self._alog = (me["id"], me["username"], path, json.dumps(b, ensure_ascii=False)[:300])
            # Tahap2: RBAC granular — ADMIN penuh, MANAGER/FINANCE keuangan, GUDANG stok, HRD sdm
            MGR = ("ADMIN","MANAGER","FINANCE")
            HR = ("ADMIN","MANAGER","HRD")
            WHM = ("ADMIN","MANAGER","GUDANG","FINANCE")
            if path in ("/api/journals","/api/sales","/api/purchases","/api/payments","/api/transfers",
                        "/api/sales/void","/api/purchases/void","/api/sales/returns","/api/purchases/returns",
                        "/api/stock/opname","/api/payroll","/api/assets/depreciate","/api/deliveries",
                        "/api/deliveries/void","/api/receives","/api/receives/void","/api/ocr-draft",
                        "/api/sales-dp","/api/sales-dp/allocate","/api/purchase-dp","/api/purchase-dp/allocate",
                        "/api/giros","/api/giros/clear","/api/giros/reject"):
                check_lock(c, b.get("date") or b.get("transaction_date") or datetime.date.today().isoformat())
            if path in ("/api/coa","/api/warehouses","/api/items","/api/customers","/api/vendors",
                        "/api/vendors/limit","/api/customers/limit","/api/units","/api/journals","/api/transfers",
                        "/api/assets","/api/assets/depreciate","/api/sales/void","/api/purchases/void",
                        "/api/stock/opname","/api/webhooks","/api/users","/api/salespersons","/api/payroll",
                        "/api/branches","/api/warehouses/branch","/api/reconcile/auto","/api/reconcile/manual","/api/reconcile/unmatch",
                        "/api/employees","/api/leaves/decide","/api/items/method","/api/restore",
                        "/api/quotations/close","/api/sales-orders/close","/api/deliveries/void",
                        "/api/requisitions/close","/api/purchase-orders/close","/api/receives/void",
                        "/api/period-end","/api/taxes","/api/approvals/decide","/api/assets/dispose"):
                need(me, *MGR)
            if path=="/api/period-end":
                need(me, "ADMIN")
            if path=="/api/sales-dp":
                cust = c.execute("SELECT * FROM customers WHERE id=?",(b["contact_id"] if "contact_id" in b else b["customer_id"],)).fetchone()
                amount = float(b["amount"])
                if amount <= 0: raise ValueError("Nominal harus > 0")
                cash = int(b["cash_account_id"])
                date = b.get("date", datetime.date.today().isoformat())
                no = next_no(c,"DP","sales_dps","dp_number")
                jid = post_journal(c,"JE-"+no,date,"SALES_DP",None,f"Terima DP {cust['customer_name']}",
                    [(cash,amount,0,"Kas"),(acct(c,"21201"),0,amount,"UMP")])
                cur = c.execute("INSERT INTO sales_dps(dp_number,transaction_date,customer_id,sales_order_id,amount,cash_account_id,journal_entry_id) VALUES(?,?,?,?,?,?,?)",
                    (no,date,cust["id"],b.get("sales_order_id"),amount,cash,jid))
                c.commit(); return self._json({"ok":True,"dp":no,"id":cur.lastrowid})
            if path=="/api/sales-dp/allocate":
                dp = c.execute("SELECT * FROM sales_dps WHERE id=?",(b["dp_id"],)).fetchone()
                inv = c.execute("SELECT * FROM sales_invoices WHERE id=?",(b["invoice_id"],)).fetchone()
                if not dp or dp["status"]=="CLOSED": raise ValueError("DP tidak valid")
                if not inv or inv["status"]=="VOID": raise ValueError("Invoice tidak valid")
                if inv["customer_id"]!=dp["customer_id"]: raise ValueError("Beda customer")
                amt = round(float(b["amount"]),2)
                if amt<=0 or amt > dp["amount"]-dp["allocated"]+0.005: raise ValueError("Melebihi sisa DP")
                if amt > outstanding_of(c,"AR",inv["id"],inv["total_amount"])+0.005: raise ValueError("Melebihi sisa piutang")
                date = b.get("date", datetime.date.today().isoformat())
                check_lock(c,date)
                cust2 = c.execute("SELECT * FROM customers WHERE id=?",(inv["customer_id"],)).fetchone()
                jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"SALES_DP_ALLOC",dp["id"],
                    f"Alokasi DP {dp['dp_number']} ke {inv['invoice_number']}",
                    [(acct(c,"21201"),amt,0,"UMP"),(cust2["receivable_account_id"],0,amt,"Piutang")])
                c.execute("INSERT INTO sales_dp_allocations(dp_id,invoice_id,amount) VALUES(?,?,?)",(dp["id"],inv["id"],amt))
                refresh_dp(c,"AR",dp["id"]); refresh_status(c,"AR",inv["id"])
                c.commit(); return self._json({"ok":True})
            if path=="/api/purchase-dp":
                vend = c.execute("SELECT * FROM vendors WHERE id=?",(b.get("contact_id") if "contact_id" in b else b["vendor_id"],)).fetchone()
                amount = float(b["amount"])
                if amount <= 0: raise ValueError("Nominal harus > 0")
                cash = int(b["cash_account_id"])
                date = b.get("date", datetime.date.today().isoformat())
                no = next_no(c,"DPB","purchase_dps","dp_number")
                jid = post_journal(c,"JE-"+no,date,"PURCHASE_DP",None,f"Bayar DP {vend['vendor_name']}",
                    [(acct(c,"12002"),amount,0,"UMB"),(cash,0,amount,"Kas")])
                cur = c.execute("INSERT INTO purchase_dps(dp_number,transaction_date,vendor_id,purchase_order_id,amount,cash_account_id,journal_entry_id) VALUES(?,?,?,?,?,?,?)",
                    (no,date,vend["id"],b.get("purchase_order_id"),amount,cash,jid))
                c.commit(); return self._json({"ok":True,"dp":no,"id":cur.lastrowid})
            if path=="/api/purchase-dp/allocate":
                dp = c.execute("SELECT * FROM purchase_dps WHERE id=?",(b["dp_id"],)).fetchone()
                inv = c.execute("SELECT * FROM purchase_invoices WHERE id=?",(b["invoice_id"],)).fetchone()
                if not dp or dp["status"]=="CLOSED": raise ValueError("DP tidak valid")
                if not inv or inv["status"]=="VOID": raise ValueError("Tagihan tidak valid")
                if inv["vendor_id"]!=dp["vendor_id"]: raise ValueError("Beda vendor")
                amt = round(float(b["amount"]),2)
                if amt<=0 or amt > dp["amount"]-dp["allocated"]+0.005: raise ValueError("Melebihi sisa DP")
                if amt > outstanding_of(c,"AP",inv["id"],inv["total_amount"])+0.005: raise ValueError("Melebihi sisa utang")
                date = b.get("date", datetime.date.today().isoformat())
                check_lock(c,date)
                vend2 = c.execute("SELECT * FROM vendors WHERE id=?",(inv["vendor_id"],)).fetchone()
                jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"PURCHASE_DP_ALLOC",dp["id"],
                    f"Alokasi DP {dp['dp_number']} ke {inv['invoice_number']}",
                    [(vend2["payable_account_id"],amt,0,"Utang"),(acct(c,"12002"),0,amt,"UMB")])
                c.execute("INSERT INTO purchase_dp_allocations(dp_id,invoice_id,amount) VALUES(?,?,?)",(dp["id"],inv["id"],amt))
                refresh_dp(c,"AP",dp["id"]); refresh_status(c,"AP",inv["id"])
                c.commit(); return self._json({"ok":True})
            if path=="/api/giros":
                kind = b["kind"]; assert kind in ("AR","AP"), "kind harus AR/AP"
                allocs = b.get("allocations") or []
                amount = round(sum(float(a["amount"]) for a in allocs),2)
                if amount <= 0: raise ValueError("Alokasi kosong")
                if abs(amount - float(b.get("amount",amount))) > 0.005: raise ValueError("Total alokasi harus = nominal giro")
                date = b.get("issue_date", datetime.date.today().isoformat())
                for a in allocs:
                    if a["invoice_type"] != kind: raise ValueError("Tipe invoice vs giro beda")
                    tbl = "sales_invoices" if kind=="AR" else "purchase_invoices"
                    t = c.execute(f"SELECT * FROM {tbl} WHERE id=?", (a["invoice_id"],)).fetchone()
                    if not t or t["status"]=="VOID": raise ValueError("Invoice tidak valid")
                    if ("customer_id" in t.keys() and t["customer_id"]!=b["contact_id"]) or ("vendor_id" in t.keys() and t["vendor_id"]!=b["contact_id"]):
                        raise ValueError("Beda kontak")
                    if float(a["amount"]) > outstanding_of(c,kind,a["invoice_id"],t["total_amount"])+0.005:
                        raise ValueError(f"Melebihi sisa {t['invoice_number']}")
                no = next_no(c,"G"+kind,"giros","giro_number")
                if kind=="AR":
                    cust = c.execute("SELECT * FROM customers WHERE id=?",(b["contact_id"],)).fetchone()
                    jid = post_journal(c,"JE-"+no,date,"GIRO_IN",None,f"Terima giro {b.get('giro_no','')} {cust['customer_name']}",
                        [(acct(c,"12003"),amount,0,"Giro"),(cust["receivable_account_id"],0,amount,"Piutang")])
                else:
                    vend = c.execute("SELECT * FROM vendors WHERE id=?",(b["contact_id"],)).fetchone()
                    jid = post_journal(c,"JE-"+no,date,"GIRO_OUT",None,f"Giro ke {vend['vendor_name']} {b.get('giro_no','')}",
                        [(vend["payable_account_id"],amount,0,"Utang"),(acct(c,"21301"),0,amount,"Giro")])
                cur = c.execute("INSERT INTO giros(giro_number,kind,contact_id,giro_no,bank_name,issue_date,due_date,amount,journal_entry_id,note) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (no,kind,b["contact_id"],b.get("giro_no",""),b.get("bank_name",""),date,b.get("due_date",date),amount,jid,b.get("note","")))
                gid = cur.lastrowid
                for a in allocs:
                    c.execute("INSERT INTO giro_allocations(giro_id,invoice_type,invoice_id,amount) VALUES(?,?,?,?)",(gid,kind,a["invoice_id"],float(a["amount"])))
                    refresh_status(c,kind,a["invoice_id"])
                c.commit(); return self._json({"ok":True,"giro":no,"id":gid})
            if path=="/api/giros/clear":
                g = c.execute("SELECT * FROM giros WHERE id=?",(b["id"],)).fetchone()
                if not g or g["status"]!="POSTED": raise ValueError("Giro tidak valid")
                date = b.get("date", datetime.date.today().isoformat())
                check_lock(c,date)
                cash = int(b["cash_account_id"])
                if g["kind"]=="AR":
                    jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"GIRO_CLEAR",g["id"],f"Giro cair {g['giro_number']}",
                        [(cash,g["amount"],0,"Kas"),(acct(c,"12003"),0,g["amount"],"Giro")])
                else:
                    jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"GIRO_CLEAR",g["id"],f"Giro cair {g['giro_number']}",
                        [(acct(c,"21301"),g["amount"],0,"Giro"),(cash,0,g["amount"],"Kas")])
                c.execute("UPDATE giros SET status='CAIR',clear_journal_id=? WHERE id=?",(jid,g["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/giros/reject":
                g = c.execute("SELECT * FROM giros WHERE id=?",(b["id"],)).fetchone()
                if not g or g["status"]!="POSTED": raise ValueError("Giro tidak valid")
                date = b.get("date", datetime.date.today().isoformat())
                check_lock(c,date)
                if g["kind"]=="AR":
                    cust = c.execute("SELECT * FROM customers WHERE id=?",(g["contact_id"],)).fetchone()
                    jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"GIRO_REJECT",g["id"],f"Giro tolak {g['giro_number']}",
                        [(cust["receivable_account_id"],g["amount"],0,"Piutang"),(acct(c,"12003"),0,g["amount"],"Giro")])
                else:
                    vend = c.execute("SELECT * FROM vendors WHERE id=?",(g["contact_id"],)).fetchone()
                    jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"GIRO_REJECT",g["id"],f"Giro tolak {g['giro_number']}",
                        [(acct(c,"21301"),g["amount"],0,"Giro"),(vend["payable_account_id"],0,g["amount"],"Utang")])
                c.execute("UPDATE giros SET status='TOLAK',clear_journal_id=? WHERE id=?",(jid,g["id"]))
                for a in q(c,"SELECT * FROM giro_allocations WHERE giro_id=?",(g["id"],)):
                    refresh_status(c,a["invoice_type"],a["invoice_id"])
                c.commit(); return self._json({"ok":True})
            if path=="/api/period-end":
                # Dukung period bulanan YYYY-MM (baru) dan tahunan YYYY (legacy)
                period = str(b.get("period") or b.get("year") or "")
                year = str(b.get("year",""))
                is_monthly = len(period)==7 and period[4]=="-" and period[:4].isdigit() and period[5:7].isdigit()
                if is_monthly:
                    ym = period[:7]
                    cols = [r[1] for r in c.execute("PRAGMA table_info(period_locks)").fetchall()]
                    if "period" in cols and c.execute("SELECT COUNT(*) n FROM period_locks WHERE period=?",(ym,)).fetchone()["n"]:
                        raise ValueError(f"Periode {ym} sudah ditutup")
                    if c.execute("SELECT COUNT(*) n FROM period_locks WHERE year=?",(ym[:4],)).fetchone()["n"]:
                        raise ValueError(f"Tahun {ym[:4]} sudah ditutup tahunan")
                    rev = q(c,"""SELECT a.id,a.account_code,a.account_name,COALESCE(SUM(l.credit-l.debit),0) net
                        FROM chart_of_accounts a JOIN journal_entry_lines l ON l.account_id=a.id
                        JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED'
                        WHERE a.account_type='REVENUE' AND substr(e.transaction_date,1,7)=? GROUP BY a.id HAVING net!=0""",(ym,))
                    exp = q(c,"""SELECT a.id,a.account_code,a.account_name,COALESCE(SUM(l.debit-l.credit),0) net
                        FROM chart_of_accounts a JOIN journal_entry_lines l ON l.account_id=a.id
                        JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED'
                        WHERE a.account_type IN ('COGS','EXPENSE') AND substr(e.transaction_date,1,7)=? GROUP BY a.id HAVING net!=0""",(ym,))
                    if not rev and not exp: raise ValueError(f"Tidak ada transaksi {ym}")
                    jl = [(r["id"],rp_int(r["net"]),0,f"Tutup {r['account_code']}") for r in rev]
                    jl += [(r["id"],0,rp_int(r["net"]),f"Tutup {r['account_code']}") for r in exp]
                    net = rp_int(sum(r["net"] for r in rev)-sum(r["net"] for r in exp))
                    if net >= 0: jl.append((acct(c,"32001"),0,net,"Laba "+ym))
                    else: jl.append((acct(c,"32001"),-net,0,"Rugi "+ym))
                    last_day = "31" if ym[5:7] in ("01","03","05","07","08","10","12") else ("28" if ym[5:7]=="02" else "30")
                    jid = post_journal(c,f"JE-CLOSE-{ym}",f"{ym}-{last_day}","PERIOD_END",None,f"Tutup buku {ym}",jl)
                    try: c.execute("INSERT INTO period_locks(year,period,locked_by,locked_at) VALUES(?,?,?,?)",(ym[:4],ym,me["username"],datetime.datetime.now().isoformat()))
                    except Exception: c.execute("INSERT INTO period_locks(year,locked_by,locked_at) VALUES(?,?,?)",(ym,me["username"],datetime.datetime.now().isoformat()))
                    c.commit(); return self._json({"ok":True,"net_income":net,"journal":jid,"period":ym})
                if not (len(year)==4 and year.isdigit()): raise ValueError("Tahun tidak valid (atau kirim period YYYY-MM)")
                if c.execute("SELECT COUNT(*) n FROM period_locks WHERE year=?",(year,)).fetchone()["n"]:
                    raise ValueError(f"Periode {year} sudah ditutup")
                rev = q(c,"""SELECT a.id,a.account_code,a.account_name,COALESCE(SUM(l.credit-l.debit),0) net
                    FROM chart_of_accounts a JOIN journal_entry_lines l ON l.account_id=a.id
                    JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED'
                    WHERE a.account_type='REVENUE' AND substr(e.transaction_date,1,4)=? GROUP BY a.id HAVING net!=0""",(year,))
                exp = q(c,"""SELECT a.id,a.account_code,a.account_name,COALESCE(SUM(l.debit-l.credit),0) net
                    FROM chart_of_accounts a JOIN journal_entry_lines l ON l.account_id=a.id
                    JOIN journal_entries e ON e.id=l.journal_entry_id AND e.status='POSTED'
                    WHERE a.account_type IN ('COGS','EXPENSE') AND substr(e.transaction_date,1,4)=? GROUP BY a.id HAVING net!=0""",(year,))
                if not rev and not exp: raise ValueError(f"Tidak ada transaksi {year}")
                jl = [(r["id"],r["net"],0,f"Tutup {r['account_code']}") for r in rev]
                jl += [(r["id"],0,r["net"],f"Tutup {r['account_code']}") for r in exp]
                net = rp_int(sum(r["net"] for r in rev)-sum(r["net"] for r in exp))
                if net >= 0: jl.append((acct(c,"32001"),0,net,"Laba "+year))
                else: jl.append((acct(c,"32001"),-net,0,"Rugi "+year))
                jid = post_journal(c,f"JE-CLOSE-{year}",f"{year}-12-31","PERIOD_END",None,f"Tutup buku {year}",jl)
                c.execute("INSERT INTO period_locks(year,locked_by,locked_at) VALUES(?,?,?)",(year,me["username"],datetime.datetime.now().isoformat()))
                c.commit(); return self._json({"ok":True,"net_income":net,"journal":jid})
            if path=="/api/restore":
                import base64, tempfile, shutil
                try: raw = base64.b64decode(b.get("data",""))
                except Exception: raise ValueError("Data file tidak valid (base64)")
                if raw[:16] != b"SQLite format 3\x00": raise ValueError("Bukan file SQLite")
                if len(raw) > 200*1024*1024: raise ValueError("File terlalu besar (>200MB)")
                # Tahap1: auto-backup DB aktif sebelum ditimpa
                try:
                    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                    shutil.copy2(DB, os.path.join(BASE, f"database.auto-backup-{stamp}.db"))
                except Exception: pass
                fd, tmp = tempfile.mkstemp(suffix=".db")
                try:
                    with os.fdopen(fd,"wb") as f: f.write(raw)
                    chk = sqlite3.connect(tmp)
                    try:
                        tbls = {r[0] for r in chk.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
                        if not {"chart_of_accounts","journal_entries","journal_entry_lines"} <= tbls:
                            raise ValueError("File bukan database AkuntansiKu")
                        chk.execute("PRAGMA integrity_check").fetchone()
                    finally: chk.close()
                    c.close()
                    os.replace(tmp, DB)
                    c = conn()
                except Exception:
                    try: os.remove(tmp)
                    except Exception: pass
                    raise
                self._alog = None
                return self._json({"ok":True})
            if path=="/api/employees":
                c.execute("INSERT INTO employees(emp_code,full_name,position,base_salary,leave_quota) VALUES(?,?,?,?,?)",
                    (b["emp_code"],b["full_name"],b.get("position",""),float(b.get("base_salary",0)),float(b.get("leave_quota",12))))
                c.commit(); return self._json({"ok":True})
            if path=="/api/attendance":
                emp = c.execute("SELECT * FROM employees WHERE id=? AND is_active=1",(b["employee_id"],)).fetchone()
                if not emp: raise ValueError("Karyawan tidak valid")
                now = datetime.datetime.now(); day = b.get("date", now.date().isoformat()); t = now.strftime("%H:%M:%S")
                row = c.execute("SELECT * FROM attendances WHERE employee_id=? AND att_date=?",(emp["id"],day)).fetchone()
                if b.get("action","in")=="in":
                    if row and row["check_in"]: raise ValueError(f"{emp['full_name']} sudah absen masuk {row['check_in']}")
                    late = " (TERLAMBAT)" if t>"08:00:00" else ""
                    if row:
                        c.execute("UPDATE attendances SET check_in=?,lat=?,lng=?,note=? WHERE id=?",(t,b.get("lat"),b.get("lng"),"Masuk"+late,row["id"]))
                    else:
                        c.execute("INSERT INTO attendances(employee_id,att_date,check_in,lat,lng,note) VALUES(?,?,?,?,?,?)",
                            (emp["id"],day,t,b.get("lat"),b.get("lng"),"Masuk"+late))
                    c.commit(); return self._json({"ok":True,"time":t,"late":bool(late)})
                else:
                    if not row or not row["check_in"]: raise ValueError("Belum absen masuk hari ini")
                    if row["check_out"]: raise ValueError(f"Sudah absen pulang {row['check_out']}")
                    if t <= row["check_in"]: raise ValueError("Jam pulang harus setelah jam masuk")
                    c.execute("UPDATE attendances SET check_out=? WHERE id=?",(t,row["id"]))
                    c.commit(); return self._json({"ok":True,"time":t})
            if path=="/api/leaves":
                emp = c.execute("SELECT * FROM employees WHERE id=? AND is_active=1",(b["employee_id"],)).fetchone()
                if not emp: raise ValueError("Karyawan tidak valid")
                d1 = datetime.date.fromisoformat(b["date_from"]); d2 = datetime.date.fromisoformat(b["date_to"])
                if d2 < d1: raise ValueError("Tanggal selesai sebelum mulai")
                days = (d2-d1).days+1
                taken = c.execute("SELECT COALESCE(SUM(days),0) s FROM leaves WHERE employee_id=? AND status='APPROVED'",(emp["id"],)).fetchone()["s"] or 0
                if taken+days > (emp["leave_quota"] or 0)+0.005: raise ValueError(f"Kuota cuti kurang (sisa {(emp['leave_quota'] or 0)-taken} hari)")
                ov = c.execute("""SELECT COUNT(*) n FROM leaves WHERE employee_id=? AND status IN ('PENDING','APPROVED')
                    AND NOT (date_to<? OR date_from>?)""",(emp["id"],b["date_from"],b["date_to"])).fetchone()["n"]
                if ov: raise ValueError("Tanggal bertabrakan dengan pengajuan lain")
                c.execute("INSERT INTO leaves(employee_id,date_from,date_to,days,reason) VALUES(?,?,?,?,?)",
                    (emp["id"],b["date_from"],b["date_to"],days,b.get("reason","")))
                c.commit(); return self._json({"ok":True,"days":days})
            if path=="/api/leaves/decide":
                lv = c.execute("SELECT * FROM leaves WHERE id=?",(b["id"],)).fetchone()
                if not lv or lv["status"]!="PENDING": raise ValueError("Pengajuan tidak valid")
                if b.get("approve"):
                    taken = c.execute("SELECT COALESCE(SUM(days),0) s FROM leaves WHERE employee_id=? AND status='APPROVED'",(lv["employee_id"],)).fetchone()["s"] or 0
                    quota = c.execute("SELECT leave_quota FROM employees WHERE id=?",(lv["employee_id"],)).fetchone()["leave_quota"] or 0
                    if taken+lv["days"] > quota+0.005: raise ValueError("Kuota tidak cukup")
                    c.execute("UPDATE leaves SET status='APPROVED',decided_by=? WHERE id=?",(me["username"],lv["id"]))
                else:
                    c.execute("UPDATE leaves SET status='REJECTED',decided_by=? WHERE id=?",(me["username"],lv["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/branches":
                c.execute("INSERT INTO branches(branch_code,branch_name,address) VALUES(?,?,?)",
                    (b["branch_code"],b["branch_name"],b.get("address","")))
                c.commit(); return self._json({"ok":True})
            if path=="/api/warehouses/branch":
                c.execute("UPDATE warehouses SET branch_id=? WHERE id=?",(b["branch_id"],b["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/statements":
                acc = c.execute("SELECT * FROM chart_of_accounts WHERE id=?",(b["bank_account_id"],)).fetchone()
                if not acc or not acc["account_code"].startswith("110"): raise ValueError("Akun bank harus 110xx")
                if b.get("direction") not in ("IN","OUT"): raise ValueError("direction harus IN/OUT")
                amt = float(b["amount"])
                if amt <= 0: raise ValueError("Nominal harus > 0")
                c.execute("INSERT INTO bank_statements(bank_account_id,transaction_date,description,amount,direction) VALUES(?,?,?,?,?)",
                    (b["bank_account_id"],b["date"],b.get("description",""),amt,b["direction"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/reconcile/auto":
                aid = b.get("account_id")
                args = [aid] if aid else []
                stmts = q(c,"SELECT * FROM bank_statements WHERE status='UNMATCHED'"+(" AND bank_account_id=?" if aid else ""),args)
                matched = 0
                for st in stmts:
                    col = "debit" if st["direction"]=="IN" else "credit"
                    hit = c.execute(f"""SELECT l.id FROM journal_entry_lines l
                        JOIN journal_entries e ON e.id=l.journal_entry_id
                        WHERE e.status='POSTED' AND l.account_id=? AND l.{col}>0
                        AND l.{col}=?
                        AND ABS(julianday(e.transaction_date)-julianday(?))<=3
                        AND l.id NOT IN (SELECT matched_line_id FROM bank_statements WHERE matched_line_id IS NOT NULL)
                        ORDER BY ABS(julianday(e.transaction_date)-julianday(?)), l.id LIMIT 1""",
                        (st["bank_account_id"],st["amount"],st["transaction_date"],st["transaction_date"])).fetchone()
                    if hit:
                        c.execute("UPDATE bank_statements SET status='MATCHED',matched_line_id=? WHERE id=?",(hit["id"],st["id"]))
                        matched += 1
                c.commit(); return self._json({"ok":True,"matched":matched,"total":len(stmts)})
            if path=="/api/reconcile/manual":
                st = c.execute("SELECT * FROM bank_statements WHERE id=?",(b["statement_id"],)).fetchone()
                ln = c.execute("""SELECT l.*,e.status AS jstatus FROM journal_entry_lines l
                    JOIN journal_entries e ON e.id=l.journal_entry_id WHERE l.id=?""",(b["line_id"],)).fetchone()
                if not st or not ln: raise ValueError("Data tidak valid")
                if ln["jstatus"]!="POSTED": raise ValueError("Jurnal belum posted")
                if ln["account_id"]!=st["bank_account_id"]: raise ValueError("Akun bank beda")
                col = "debit" if st["direction"]=="IN" else "credit"
                if abs(rp_int(ln[col])-rp_int(st["amount"]))>0: raise ValueError("Nominal tidak sama (Rp bulat)")
                used = c.execute("SELECT COUNT(*) n FROM bank_statements WHERE matched_line_id=? AND id!=?",(ln["id"],st["id"])).fetchone()["n"]
                if used: raise ValueError("Baris jurnal sudah dipakai statement lain")
                c.execute("UPDATE bank_statements SET status='MATCHED',matched_line_id=? WHERE id=?",(ln["id"],st["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/reconcile/unmatch":
                c.execute("UPDATE bank_statements SET status='UNMATCHED',matched_line_id=NULL WHERE id=?",(b["statement_id"],))
                c.commit(); return self._json({"ok":True})
            if path=="/api/users":
                if c.execute("SELECT COUNT(*) n FROM users WHERE username=?", (b["username"],)).fetchone()["n"]:
                    raise ValueError("Username sudah dipakai")
                role = b.get("role","KASIR")
                if role not in ("ADMIN","MANAGER","KASIR","FINANCE","GUDANG","HRD"):
                    raise ValueError("Role tidak valid (ADMIN/MANAGER/FINANCE/GUDANG/HRD/KASIR)")
                make_user(c, b["username"], b["password"], b.get("full_name", b["username"]), role)
                c.commit(); return self._json({"ok":True})
            if path=="/api/taxes":
                c.execute("INSERT INTO taxes(tax_code,tax_name,rate,masukan_account_id,keluaran_account_id) VALUES(?,?,?,?,?)",
                    (b["tax_code"],b["tax_name"],float(b.get("rate",11)),b.get("masukan_account_id"),b.get("keluaran_account_id")))
                c.commit(); return self._json({"ok":True})
            if path=="/api/approvals":
                # KASIR/GUDANG ajukan void; MGR putuskan
                c.execute("INSERT INTO approvals(kind,ref_type,ref_id,amount,requested_by,status,created_at) VALUES(?,?,?,?,?,?,?)",
                    (b.get("kind","VOID"),b["ref_type"],int(b["ref_id"]),rp_int(b.get("amount",0)),me["username"],"PENDING",datetime.datetime.now().isoformat()))
                c.commit(); return self._json({"ok":True,"status":"PENDING"})
            if path=="/api/approvals/decide":
                ap = c.execute("SELECT * FROM approvals WHERE id=?",(b["id"],)).fetchone()
                if not ap or ap["status"]!="PENDING": raise ValueError("Pengajuan tidak valid")
                if b.get("approve"):
                    c.execute("UPDATE approvals SET status='APPROVED',decided_by=?,decided_at=? WHERE id=?",(me["username"],datetime.datetime.now().isoformat(),ap["id"]))
                else:
                    c.execute("UPDATE approvals SET status='REJECTED',decided_by=?,decided_at=? WHERE id=?",(me["username"],datetime.datetime.now().isoformat(),ap["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/payroll/calc":
                # TER sederhana bulanan (disederhanakan dari PMK 168/2023): tanpa PTKP harian
                gross = rp_int(b.get("gross",0))
                if gross<=0: raise ValueError("Bruto harus > 0")
                if gross<=5400000: rate=0.0
                elif gross<=5650000: rate=0.0025
                elif gross<=5950000: rate=0.005
                elif gross<=6300000: rate=0.0075
                elif gross<=6750000: rate=0.01
                elif gross<=7500000: rate=0.0125
                elif gross<=8550000: rate=0.015
                elif gross<=9650000: rate=0.02
                elif gross<=10050000: rate=0.025
                elif gross<=13300000: rate=0.03
                else: rate=0.05
                pph = rp_int(gross*rate)
                return self._json({"ok":True,"gross":gross,"rate":rate,"pph21":pph,"net":gross-pph})
            if path=="/api/assets/dispose":
                a=c.execute("SELECT * FROM fixed_assets WHERE id=?",(b["id"],)).fetchone()
                if not a: raise ValueError("Aset tidak valid")
                nilai_buku = rp_int(a["cost"]-a["accum_depr"])
                harga = rp_int(b.get("sale_price",0))
                date = b.get("date", datetime.date.today().isoformat())
                # Dr Kas + Dr Akumulasi + (Dr Rugi / Cr Laba) / Cr Peralatan
                jl=[(acct(c,"11001") or a["asset_account_id"],harga,0,"Kas disposal")]
                jl.append((a["accum_account_id"] or acct(c,"15002"),rp_int(a["accum_depr"]),0,"Akumulasi"))
                if harga>=nilai_buku: jl.append((a["asset_account_id"],0,rp_int(a["cost"]),"Peralatan")); jl.append((acct(c,"71001"),0,harga-nilai_buku,"Laba disposal"))
                else: jl.append((a["asset_account_id"],0,rp_int(a["cost"]),"Peralatan")); jl.append((acct(c,"72001"),nilai_buku-harga,0,"Rugi disposal"))
                # sesuaikan: ganti akun kas bila ada
                jid=post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"ASSET_DISPOSE",a["id"],f"Disposal {a['asset_name']}",jl)
                c.execute("DELETE FROM fixed_assets WHERE id=?",(a["id"],))
                c.commit(); return self._json({"ok":True,"journal":jid,"book_value":nilai_buku})
            if path=="/api/units":
                conv = float(b["conversion"])
                if conv <= 0: raise ValueError("Konversi harus > 0")
                c.execute("INSERT INTO item_units(item_id,unit_code,conversion) VALUES(?,?,?)",(b["item_id"],b["unit_code"],conv))
                c.commit(); return self._json({"ok":True})
            if path=="/api/salespersons":
                c.execute("INSERT INTO salespersons(sp_code,sp_name,commission_pct,monthly_target) VALUES(?,?,?,?)",
                    (b["sp_code"],b["sp_name"],float(b.get("commission_pct",0)),float(b.get("monthly_target",0))))
                c.commit(); return self._json({"ok":True})
            if path=="/api/payroll":
                gross = rp_int(b["gross"]); pph = rp_int(b.get("pph21",0))
                if gross <= 0: raise ValueError("Bruto harus > 0")
                if pph < 0 or pph > gross: raise ValueError("PPh21 tidak valid")
                net = rp_int(gross-pph); date = b.get("date", datetime.date.today().isoformat())
                jl=[(acct(c,"61001"),gross,0,"Gaji bruto "+b.get("employee_name",""))]
                if pph: jl.append((acct(c,"22002"),0,pph,"PPh 21"))
                jl.append((acct(c,"23001"),0,net,"Gaji bersih"))
                jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"PAYROLL",None,
                    f"Gaji {b.get('employee_name','')} {date}",jl)
                cur=c.execute("INSERT INTO payroll_records(transaction_date,employee_name,gross,pph21,net,journal_entry_id,created_by) VALUES(?,?,?,?,?,?,?)",
                    (date,b.get("employee_name",""),gross,pph,net,jid,me["username"]))
                c.commit(); return self._json({"ok":True,"net":net})
            if path=="/api/coa":
                c.execute("INSERT INTO chart_of_accounts(account_code,account_name,account_type) VALUES(?,?,?)",(b["account_code"],b["account_name"],b["account_type"])); c.commit()
                return self._json({"ok":True})
            if path=="/api/warehouses":
                c.execute("INSERT INTO warehouses(warehouse_code,warehouse_name,address) VALUES(?,?,?)",(b["warehouse_code"],b["warehouse_name"],b.get("address",""))); c.commit()
                return self._json({"ok":True})
            if path=="/api/items/method":
                if b.get("method") not in ("AVERAGE","FIFO"): raise ValueError("Metode harus AVERAGE/FIFO")
                c.execute("UPDATE items SET cost_method=? WHERE id=?",(b["method"],b["id"]))
                rebuild_fifo(c, b["id"])
                c.commit(); return self._json({"ok":True,"method":b["method"]})
            if path=="/api/items":
                c.execute("INSERT INTO items(item_code,item_name,item_type,base_unit,inventory_account_id,sales_account_id,cogs_account_id,purchase_price,sales_price,avg_cost) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (b["item_code"],b["item_name"],b.get("item_type","INVENTORY"),b.get("base_unit","PCS"),b.get("inventory_account_id"),b["sales_account_id"],b.get("cogs_account_id"),b.get("purchase_price",0),b.get("sales_price",0),b.get("purchase_price",0)))
                c.commit(); return self._json({"ok":True})
            if path=="/api/customers":
                # Tahap2: quick-create — kode & akun otomatis bila kosong
                code = b.get("customer_code") or next_no(c,"CUST","customers","customer_code")
                acc = b.get("receivable_account_id") or acct(c,"12001")
                c.execute("INSERT INTO customers(customer_code,customer_name,email,receivable_account_id) VALUES(?,?,?,?)",(code,b["customer_name"],b.get("email",""),acc)); c.commit()
                return self._json({"ok":True,"code":code})
            if path=="/api/vendors":
                code = b.get("vendor_code") or next_no(c,"VEND","vendors","vendor_code")
                acc = b.get("payable_account_id") or acct(c,"21001")
                c.execute("INSERT INTO vendors(vendor_code,vendor_name,email,payable_account_id) VALUES(?,?,?,?)",(code,b["vendor_name"],b.get("email",""),acc)); c.commit()
                return self._json({"ok":True,"code":code})
            if path=="/api/journals":
                lines=[(l["account_id"],float(l.get("debit",0)),float(l.get("credit",0)),l.get("memo","")) for l in b["lines"]]
                jid = post_journal(c, b.get("journal_number") or next_no(c,"JE","journal_entries","journal_number"), b["transaction_date"], b.get("reference_type","MANUAL"), None, b.get("description",""), lines)
                c.commit(); fire_webhook(c,"journal.created",{"id":jid}); c.commit()
                return self._json({"ok":True,"id":jid})
            if path=="/api/sales":
                # b: customer_id, date, due, warehouse_id, tax_rate, lines:[{item_id,qty,price,discount,discount_pct,discount_pct2}]
                #      lines boleh mereferensi rantai: {delivery_line_id,qty} atau {sales_order_line_id,...}
                cust = c.execute("SELECT * FROM customers WHERE id=?",(b["customer_id"],)).fetchone()
                subtotal=0; clines=[]; linked_so=set()
                for l in b["lines"]:
                    if l.get("delivery_line_id"):
                        dl = c.execute("SELECT dl.*,d.customer_id,d.status FROM delivery_order_lines dl JOIN delivery_orders d ON d.id=dl.delivery_order_id WHERE dl.id=?",(l["delivery_line_id"],)).fetchone()
                        if not dl or dl["status"]!="POSTED": raise ValueError("Baris DO tidak valid")
                        if dl["customer_id"]!=int(b["customer_id"]): raise ValueError("DO milik customer lain")
                        it = c.execute("SELECT * FROM items WHERE id=?",(dl["item_id"],)).fetchone()
                        qty = round(float(l["qty"]),2)
                        if qty<=0 or qty > dl["quantity"]-dl["invoiced_qty"]+0.005:
                            raise ValueError(f"Qty melebihi sisa DO ({dl['quantity']-dl['invoiced_qty']})")
                        bprice = round(dl["unit_price"]/(dl["unit_conv"] or 1),2)
                        lt = round(qty*bprice,2); subtotal+=lt
                        share = round(dl["cogs_total"]*(qty/dl["quantity"]),2) if dl["quantity"] else 0
                        clines.append({"kind":"DO","it":it,"dl":dl,"sol":None,"base":qty,"price":bprice,
                            "disc":0,"lt":lt,"share":share,"ucode":dl["unit_code"],"uqty":qty,"conv":1,"wh":dl["warehouse_id"],"desc":dl["description"] if "description" in dl.keys() else ""})
                        continue
                    it = c.execute("SELECT * FROM items WHERE id=?",(l["item_id"],)).fetchone()
                    qty=float(l["qty"]); price=float(l["price"])
                    conv = float(l.get("unit_conv",1)) or 1
                    ucode = l.get("unit_code", it["base_unit"])
                    base = round(qty*conv,2)
                    sol = None
                    if l.get("sales_order_line_id"):
                        sol = c.execute("SELECT * FROM sales_order_lines WHERE id=?",(l["sales_order_line_id"],)).fetchone()
                        if not sol: raise ValueError("Baris SO tidak valid")
                        so = c.execute("SELECT * FROM sales_orders WHERE id=?",(sol["sales_order_id"],)).fetchone()
                        if so["customer_id"]!=int(b["customer_id"]): raise ValueError("SO milik customer lain")
                        if so["status"]=="CLOSED": raise ValueError("SO sudah closed")
                        if sol["item_id"]!=it["id"]: raise ValueError("Barang beda dengan baris SO")
                        f = so_fulfill(c,sol["id"])
                        if base > f["ordered"]-f["delivered"]+0.005:
                            raise ValueError(f"Melebihi sisa SO ({f['ordered']-f['delivered']})")
                        ratio = base/sol["quantity"] if sol["quantity"] else 0
                        lt = round(sol["line_total"]*ratio,2); disc = round(sol["discount_amount"]*ratio,2)
                        subtotal+=lt; linked_so.add(sol["sales_order_id"])
                    else:
                        gross = round(qty*price,2)
                        d1 = round(gross*float(l.get("discount_pct",0))/100,2)
                        d2 = round((gross-d1)*float(l.get("discount_pct2",0))/100,2)
                        disc = round(d1+d2+float(l.get("discount",0)),2)
                        lt = round(gross-disc,2); subtotal+=lt
                    if it["item_type"]=="INVENTORY":
                        s = stock_of(c,it["id"],b["warehouse_id"])
                        if s < base-0.005: raise ValueError(f"Stok {it['item_code']} kurang (sisa {s} {it['base_unit']}, minta {base})")
                    clines.append({"kind":"SO" if sol else "DIRECT","it":it,"dl":None,"sol":sol,"base":base,
                        "price":price,"disc":disc,"lt":lt,"share":0,"ucode":ucode,"uqty":qty,"conv":conv,"wh":int(b["warehouse_id"]),"desc":l.get("description","")})
                tax = rp_int(subtotal*float(b.get("tax_rate",0))/100); total=subtotal+tax
                clim = cust["credit_limit"] if "credit_limit" in cust.keys() and cust["credit_limit"] else 0
                if clim and clim > 0:
                    cur_ar = sum(outstanding_of(c,"AR",r["id"],r["total_amount"])
                        for r in q(c,"SELECT id,total_amount FROM sales_invoices WHERE customer_id=? AND status NOT IN ('VOID','PAID')",(b["customer_id"],)))
                    if cur_ar + total > clim + 0.005:
                        raise ValueError(f"Melebihi limit piutang {cust['customer_name']} ({rp(clim)}). Sisa outstanding {rp(cur_ar)}, invoice baru {rp(total)}.")
                td = int(cust["term_days"] or 0) if "term_days" in cust.keys() else 0
                if not b.get("due") and td > 0:
                    try: b["due"] = (datetime.date.fromisoformat(b["date"])+datetime.timedelta(days=td)).isoformat()
                    except Exception: pass
                # --- tukar tambah: barang bekas masuk stok, piutang berkurang ---
                ti = b.get("trade_in") or {}
                ti_value = round(float(ti.get("value",0) or 0),2)
                ti_item = None
                if ti_value > 0:
                    ti_item = c.execute("SELECT * FROM items WHERE id=?", (ti["item_id"],)).fetchone()
                    if not ti_item or ti_item["item_type"]!="INVENTORY" or not ti_item["inventory_account_id"]:
                        raise ValueError("Barang tukar-tambah harus barang persediaan")
                    if ti_value > total-0.005: raise ValueError("Nilai tukar-tambah melebihi total invoice")
                net_recv = round(total - ti_value, 2)
                # --- salesman & komisi ---
                sp = None; commission = 0
                if b.get("salesperson_id"):
                    sp = c.execute("SELECT * FROM salespersons WHERE id=? AND is_active=1", (b["salesperson_id"],)).fetchone()
                    if not sp: raise ValueError("Salesman tidak valid")
                    commission = round(subtotal*float(sp["commission_pct"] or 0)/100, 2)
                inv_no = b.get("invoice_number") or next_no(c,"INV","sales_invoices","invoice_number")
                so_ids = sorted(linked_so)
                do_ids = list({e["dl"]["delivery_order_id"] for e in clines if e["kind"]=="DO"})
                cur = c.execute("INSERT INTO sales_invoices(invoice_number,transaction_date,due_date,customer_id,subtotal,tax_amount,total_amount,salesperson_id,commission_amount,sales_order_id,delivery_order_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (inv_no,b["date"],b.get("due",b["date"]),b["customer_id"],subtotal,tax,total,sp["id"] if sp else None,commission,
                     b.get("sales_order_id") or (so_ids[0] if len(so_ids)==1 else None), b.get("delivery_order_id") or (do_ids[0] if len(do_ids)==1 else None)))
                sid = cur.lastrowid
                sales_map={}; cogs_map={}; inv_map={}; git_total=0
                for e in clines:
                    it=e["it"]
                    if e["kind"]=="DO":
                        dl=e["dl"]
                        c.execute("INSERT INTO sales_invoice_lines(sales_invoice_id,item_id,warehouse_id,quantity,unit_price,discount_amount,line_total,description,unit_code,unit_qty,unit_conv,delivery_order_line_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                            (sid,it["id"],e["wh"],e["base"],e["price"],0,e["lt"],e["desc"],e["ucode"],e["uqty"],e["conv"],dl["id"]))
                        sales_map[it["sales_account_id"]] = sales_map.get(it["sales_account_id"],0)+e["lt"]
                        cogs_map[it["cogs_account_id"]] = cogs_map.get(it["cogs_account_id"],0)+e["share"]
                        git_total += e["share"]
                        c.execute("UPDATE delivery_order_lines SET invoiced_qty=invoiced_qty+? WHERE id=?",(e["base"],dl["id"]))
                        continue
                    c.execute("INSERT INTO sales_invoice_lines(sales_invoice_id,item_id,warehouse_id,quantity,unit_price,discount_amount,line_total,description,unit_code,unit_qty,unit_conv,sales_order_line_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (sid,it["id"],e["wh"],e["base"],e["price"],e["disc"],e["lt"],e["desc"],e["ucode"],e["uqty"],e["conv"],e["sol"]["id"] if e["sol"] else None))
                    sales_map[it["sales_account_id"]] = sales_map.get(it["sales_account_id"],0)+e["lt"]
                    if it["item_type"]=="INVENTORY":
                        if is_fifo(c,it["id"]):
                            h = consume_fifo(c,it["id"],e["wh"],b["date"],"SALES_INVOICE",sid,e["base"])
                            cost = round(h/e["base"],2) if e["base"] else 0
                        else:
                            cost = it["avg_cost"] or 0; h = round(cost*e["base"],2)
                        cogs_map[it["cogs_account_id"]] = cogs_map.get(it["cogs_account_id"],0)+h
                        inv_map[it["inventory_account_id"]] = inv_map.get(it["inventory_account_id"],0)+h
                        c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                            (it["id"],e["wh"],b["date"],"SALES_INVOICE",sid,e["base"],cost))
                jlines=[(dict(cust)["receivable_account_id"],net_recv,0,"Piutang "+inv_no)]
                for acc,amt in sales_map.items(): jlines.append((acc,0,amt,"Penjualan "+inv_no))
                if tax: jlines.append((acct(c,"22001"),0,tax,"PPN Keluaran "+inv_no))
                if ti_value > 0:
                    jlines.append((ti_item["inventory_account_id"],ti_value,0,"Terima tukar tambah "+ti_item["item_code"]))
                for acc,amt in cogs_map.items(): jlines.append((acc,round(amt,2),0,"HPP "+inv_no))
                if git_total: jlines.append((acct(c,"13002"),0,round(git_total,2),"GIT "+inv_no))
                for acc,amt in inv_map.items(): jlines.append((acc,0,round(amt,2),"Persediaan "+inv_no))
                jid = post_journal(c, "JE-"+inv_no, b["date"], "SALES_INVOICE", sid, "Auto-posting "+inv_no, jlines)
                c.execute("UPDATE sales_invoices SET journal_entry_id=? WHERE id=?",(jid,sid))
                for so_id in so_ids: refresh_doc_status(c,"SO",so_id)
                if ti_value > 0:
                    ti_qty = float(ti["qty"]); unit_val = round(ti_value/ti_qty,2)
                    c.execute("INSERT INTO sales_tradeins(sales_invoice_id,item_id,warehouse_id,quantity,agreed_value,note) VALUES(?,?,?,?,?,?)",
                        (sid,ti_item["id"],int(ti.get("warehouse_id") or b["warehouse_id"]),ti_qty,ti_value,ti.get("note","")))
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (ti_item["id"],int(ti.get("warehouse_id") or b["warehouse_id"]),b["date"],"TRADE_IN",sid,ti_qty,unit_val))
                    if is_fifo(c,ti_item["id"]):
                        add_layer(c,ti_item["id"],int(ti.get("warehouse_id") or b["warehouse_id"]),b["date"],"TRADE_IN",sid,ti_qty,unit_val)
                kom_jid = None
                if commission > 0:
                    kom_jid = post_journal(c, "JE-KOM-"+inv_no, b["date"], "COMMISSION", sid,
                        f"Komisi {sp['sp_name']} {inv_no}",
                        [(acct(c,"64002"),commission,0,"Beban komisi"),(acct(c,"23002"),0,commission,"Utang komisi")])
                    c.execute("UPDATE sales_invoices SET commission_journal_id=? WHERE id=?", (kom_jid,sid))
                c.commit(); fire_webhook(c,"sales.created",{"invoice":inv_no,"total":total}); c.commit()
                return self._json({"ok":True,"invoice":inv_no,"total":total,"receivable":net_recv,"commission":commission})
            if path=="/api/purchases":
                vend = c.execute("SELECT * FROM vendors WHERE id=?",(b["vendor_id"],)).fetchone()
                subtotal=0; clines=[]; linked_po=set(); var_total=0; received_sub=0
                for l in b["lines"]:
                    if l.get("receive_line_id"):
                        rl = c.execute("SELECT rl.*,r.vendor_id,r.status FROM receive_item_lines rl JOIN receive_items r ON r.id=rl.receive_id WHERE rl.id=?",(l["receive_line_id"],)).fetchone()
                        if not rl or rl["status"]!="POSTED": raise ValueError("Baris receive tidak valid")
                        if rl["vendor_id"]!=int(b["vendor_id"]): raise ValueError("Receive milik vendor lain")
                        it = c.execute("SELECT * FROM items WHERE id=?",(rl["item_id"],)).fetchone()
                        qty = round(float(l["qty"]),2)
                        if qty<=0 or qty > rl["quantity"]-rl["billed_qty"]+0.005:
                            raise ValueError(f"Qty melebihi sisa receive ({rl['quantity']-rl['billed_qty']})")
                        price = float(l.get("price", rl["unit_price"]/(rl["unit_conv"] or 1)))
                        lt = round(qty*price,2); subtotal+=lt
                        base_cost = round(rl["line_total"]/rl["quantity"],2) if rl["quantity"] else 0
                        var_total += round(lt - qty*base_cost,2)
                        received_sub += round(qty*base_cost,2)
                        clines.append({"kind":"RI","it":it,"rl":rl,"pol":None,"base":qty,"price":price,"lt":lt,
                            "ucode":rl["unit_code"],"uqty":qty,"conv":1,"wh":rl["warehouse_id"],"desc":l.get("description",rl["description"] if "description" in rl.keys() else "")})
                        continue
                    it = c.execute("SELECT * FROM items WHERE id=?",(l["item_id"],)).fetchone()
                    qty=float(l["qty"]); price=float(l["price"])
                    conv = float(l.get("unit_conv",1)) or 1
                    ucode = l.get("unit_code", it["base_unit"])
                    base = round(qty*conv,2); base_price = round(price/conv,2)
                    pol = None
                    if l.get("purchase_order_line_id"):
                        pol = c.execute("SELECT * FROM purchase_order_lines WHERE id=?",(l["purchase_order_line_id"],)).fetchone()
                        if not pol: raise ValueError("Baris PO tidak valid")
                        po = c.execute("SELECT * FROM purchase_orders WHERE id=?",(pol["purchase_order_id"],)).fetchone()
                        if po["vendor_id"]!=int(b["vendor_id"]): raise ValueError("PO milik vendor lain")
                        if po["status"]=="CLOSED": raise ValueError("PO sudah closed")
                        if pol["item_id"]!=it["id"]: raise ValueError("Barang beda dengan baris PO")
                        f = po_fulfill(c,pol["id"])
                        if base > f["ordered"]-f["received"]+0.005:
                            raise ValueError(f"Melebihi sisa PO ({f['ordered']-f['received']})")
                        linked_po.add(pol["purchase_order_id"])
                    lt = round(qty*price,2); subtotal+=lt
                    clines.append({"kind":"PO" if pol else "DIRECT","it":it,"rl":None,"pol":pol,"base":base,
                        "price":price,"lt":lt,"bprice":base_price,"ucode":ucode,"uqty":qty,"conv":conv,"desc":l.get("description",""),
                        "wh":int(l.get("warehouse_id") or (pol["warehouse_id"] if pol else b.get("warehouse_id") or 0))})
                tax=rp_int(subtotal*float(b.get("tax_rate",0))/100); total=subtotal+tax
                limit = vend["credit_limit"] if "credit_limit" in vend.keys() else 0
                if limit and limit > 0:
                    cur_out = sum(outstanding_of(c,"AP",r["id"],r["total_amount"])
                        for r in q(c,"SELECT id,total_amount FROM purchase_invoices WHERE vendor_id=? AND status NOT IN ('VOID','PAID')",(b["vendor_id"],)))
                    if cur_out + total > limit + 0.005:
                        raise ValueError(f"Melebihi limit utang vendor {vend['vendor_name']} ({rp(limit)}). Sisa outstanding {rp(cur_out)}, tagihan baru {rp(total)}.")
                inv_no = b.get("invoice_number") or next_no(c,"PO-INV","purchase_invoices","invoice_number")
                po_ids = sorted(linked_po)
                ri_ids = list({e["rl"]["receive_id"] for e in clines if e["kind"]=="RI"})
                cur = c.execute("INSERT INTO purchase_invoices(invoice_number,transaction_date,due_date,vendor_id,subtotal,tax_amount,total_amount,purchase_order_id,receive_item_id) VALUES(?,?,?,?,?,?,?,?,?)",
                    (inv_no,b["date"],b.get("due",b["date"]),b["vendor_id"],subtotal,tax,total,
                     b.get("purchase_order_id") or (po_ids[0] if len(po_ids)==1 else None),
                     b.get("receive_item_id") or (ri_ids[0] if len(ri_ids)==1 else None)))
                pid = cur.lastrowid; inv_map={}
                for e in clines:
                    it=e["it"]
                    if e["kind"]=="RI":
                        c.execute("INSERT INTO purchase_invoice_lines(purchase_invoice_id,item_id,warehouse_id,quantity,unit_price,line_total,description,unit_code,unit_qty,unit_conv,receive_line_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                            (pid,it["id"],e["wh"],e["base"],e["price"],e["lt"],e["desc"],e["ucode"],e["uqty"],e["conv"],e["rl"]["id"]))
                        c.execute("UPDATE receive_item_lines SET billed_qty=billed_qty+? WHERE id=?",(e["base"],e["rl"]["id"]))
                        continue
                    c.execute("INSERT INTO purchase_invoice_lines(purchase_invoice_id,item_id,warehouse_id,quantity,unit_price,line_total,description,unit_code,unit_qty,unit_conv,purchase_order_line_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (pid,it["id"],e["wh"],e["base"],e["price"],e["lt"],e["desc"],e["ucode"],e["uqty"],e["conv"],e["pol"]["id"] if e["pol"] else None))
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (it["id"],e["wh"],b["date"],"PURCHASE_INVOICE",pid,e["base"],e["bprice"]))
                    if it["item_type"]=="INVENTORY":
                        if is_fifo(c,it["id"]):
                            add_layer(c,it["id"],e["wh"],b["date"],"PURCHASE_INVOICE",pid,e["base"],e["bprice"])
                        old_s = stock_of(c,it["id"]) - e["base"]
                        old_c = it["avg_cost"] or e["bprice"]
                        new_avg = (old_s*old_c + e["base"]*e["bprice"])/max(old_s+e["base"],0.0001) if old_s>0 else e["bprice"]
                        c.execute("UPDATE items SET avg_cost=?,purchase_price=? WHERE id=?",(new_avg,e["bprice"],it["id"]))
                        inv_map[it["inventory_account_id"]] = inv_map.get(it["inventory_account_id"],0)+round(e["base"]*e["bprice"],2)
                    else:
                        inv_map[acct(c,"13001")] = inv_map.get(acct(c,"13001"),0)+e["lt"]
                direct_sub = round(sum(e["lt"] for e in clines if e["kind"]!="RI"),2)
                jlines=[(a,round(v,2),0,"Persediaan "+inv_no) for a,v in inv_map.items()]
                if tax: jlines.append((acct(c,"14001"),tax,0,"PPN Masukan "+inv_no))
                var_total = round(var_total,2)
                if var_total > 0: jlines.append((acct(c,"51001"),var_total,0,"Selisih harga "+inv_no))
                # Kenaikan utang = belanja langsung + PPN + selisih; bila selisih negatif, utang dikurangi via Dr
                utang = round(direct_sub + tax + max(var_total,0),2)
                # utang = direct + tax + (billed - received)
                if var_total < 0: jlines.append((dict(vend)["payable_account_id"],round(-var_total,2),0,"Koreksi utang "+inv_no))
                jlines.append((dict(vend)["payable_account_id"],0,utang,"Utang "+inv_no))
                jid = post_journal(c,"JE-"+inv_no,b["date"],"PURCHASE_INVOICE",pid,"Auto-posting "+inv_no,jlines)
                c.execute("UPDATE purchase_invoices SET journal_entry_id=? WHERE id=?",(jid,pid))
                for po_id in po_ids: refresh_doc_status(c,"PO",po_id)
                c.commit(); fire_webhook(c,"purchase.created",{"invoice":inv_no,"total":total}); c.commit()
                return self._json({"ok":True,"invoice":inv_no})
            if path=="/api/quotations":
                subtotal=0; cl=[]
                for l in b["lines"]:
                    d = calc_line(c,l); subtotal+=d["lt"]; cl.append(d)
                tax = rp_int(subtotal*float(b.get("tax_rate",0))/100)
                qno = b.get("quotation_number") or next_no(c,"SQ","sales_quotations","quotation_number")
                cur = c.execute("INSERT INTO sales_quotations(quotation_number,transaction_date,customer_id,subtotal,tax_amount,total_amount,notes) VALUES(?,?,?,?,?,?,?)",
                    (qno,b["date"],b["customer_id"],subtotal,tax,subtotal+tax,b.get("notes","")))
                qid = cur.lastrowid
                for d in cl:
                    c.execute("INSERT INTO sales_quotation_lines(quotation_id,item_id,quantity,unit_price,discount_pct,discount_pct2,discount_amount,line_total,description,unit_code,unit_qty,unit_conv) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (qid,d["it"]["id"],d["base"],d["price"],d["p1"],d["p2"],d["disc"],d["lt"],d["desc"],d["ucode"],d["uqty"],d["conv"]))
                c.commit(); return self._json({"ok":True,"quotation":qno})
            if path=="/api/quotations/close":
                c.execute("UPDATE sales_quotations SET status='CLOSED' WHERE id=?",(b["id"],))
                c.commit(); return self._json({"ok":True})
            if path=="/api/sales-orders":
                subtotal=0; cl=[]
                for l in b["lines"]:
                    d = calc_line(c,l); subtotal+=d["lt"]; cl.append(d)
                tax = rp_int(subtotal*float(b.get("tax_rate",0))/100)
                ono = b.get("order_number") or next_no(c,"SO","sales_orders","order_number")
                cur = c.execute("INSERT INTO sales_orders(order_number,transaction_date,customer_id,quotation_id,subtotal,tax_amount,total_amount,notes) VALUES(?,?,?,?,?,?,?,?)",
                    (ono,b["date"],b["customer_id"],b.get("quotation_id"),subtotal,tax,subtotal+tax,b.get("notes","")))
                oid = cur.lastrowid
                for d in cl:
                    c.execute("INSERT INTO sales_order_lines(sales_order_id,item_id,quantity,unit_price,discount_pct,discount_pct2,discount_amount,line_total,description,unit_code,unit_qty,unit_conv) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (oid,d["it"]["id"],d["base"],d["price"],d["p1"],d["p2"],d["disc"],d["lt"],d["desc"],d["ucode"],d["uqty"],d["conv"]))
                if b.get("quotation_id"):
                    c.execute("UPDATE sales_quotations SET status='ORDERED' WHERE id=?",(b["quotation_id"],))
                c.commit(); return self._json({"ok":True,"order":ono})
            if path=="/api/sales-orders/close":
                c.execute("UPDATE sales_orders SET status='CLOSED' WHERE id=?",(b["id"],))
                c.commit(); return self._json({"ok":True})
            if path=="/api/deliveries":
                cust = c.execute("SELECT * FROM customers WHERE id=?",(b["customer_id"],)).fetchone()
                date = b["date"]; git_total=0; dl=[]
                dno = b.get("delivery_number") or next_no(c,"DO","delivery_orders","delivery_number")
                cur = c.execute("INSERT INTO delivery_orders(delivery_number,transaction_date,sales_order_id,customer_id) VALUES(?,?,?,?)",
                    (dno,date,b.get("sales_order_id"),b["customer_id"]))
                did = cur.lastrowid
                for l in b["lines"]:
                    it = c.execute("SELECT * FROM items WHERE id=?",(l["item_id"],)).fetchone()
                    sol = None
                    if l.get("sales_order_line_id"):
                        sol = c.execute("SELECT * FROM sales_order_lines WHERE id=?",(l["sales_order_line_id"],)).fetchone()
                        if not sol: raise ValueError("Baris SO tidak valid")
                        if sol["item_id"]!=it["id"]: raise ValueError("Barang beda dengan baris SO")
                        f = so_fulfill(c,sol["id"])
                        base = round(float(l["qty"]),2)
                        if base<=0 or base > f["ordered"]-f["delivered"]+0.005:
                            raise ValueError(f"Qty harus >0 dan ≤ sisa SO ({f['ordered']-f['delivered']})")
                        price = float(l.get("price", sol["unit_price"]))
                        ucode = l.get("unit_code", sol["unit_code"] or it["base_unit"])
                        uconv = float(l.get("unit_conv",0)) or sol["unit_conv"] or 1
                        uqty = round(base/uconv,2)
                    else:
                        conv = float(l.get("unit_conv",1)) or 1
                        base = round(float(l["qty"])*conv,2)
                        price = float(l.get("price", it["sales_price"] or 0))
                        ucode = l.get("unit_code", it["base_unit"]); uconv = conv; uqty = float(l["qty"])
                    wh = int(l.get("warehouse_id") or 0)
                    if not wh: raise ValueError("Gudang wajib diisi")
                    h, unit = ship_out(c,it,wh,date,"DELIVERY_ORDER",did,base)
                    git_total += h
                    dl.append((it,sol,base,price,h,unit,ucode,uqty,uconv,wh,l.get("description","")))
                for it,sol,base,price,h,unit,ucode,uqty,conv,wh,desc in dl:
                    c.execute("INSERT INTO delivery_order_lines(delivery_order_id,sales_order_line_id,item_id,warehouse_id,quantity,unit_price,cogs_total,description,unit_code,unit_qty,unit_conv) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (did,sol["id"] if sol else None,it["id"],wh,base,price,h,desc,ucode,uqty,conv))
                git_acc = acct(c,"13002")
                inv_sum = {}
                # kredit persediaan per akun barang (untuk jejak akurat)
                for it,sol,base,price,h,unit,ucode,uqty,conv,wh,desc in dl:
                    a = it["inventory_account_id"]
                    inv_sum[a] = inv_sum.get(a,0)+h
                jl=[(git_acc,round(git_total,2),0,"DO "+dno)]
                for a,amt in inv_sum.items(): jl.append((a,0,round(amt,2),"DO "+dno))
                jid = post_journal(c,"JE-"+dno,date,"DELIVERY_ORDER",did,"Serah terima "+dno,jl)
                c.execute("UPDATE delivery_orders SET journal_entry_id=? WHERE id=?",(jid,did))
                if b.get("sales_order_id"): refresh_doc_status(c,"SO",b["sales_order_id"])
                c.commit(); return self._json({"ok":True,"delivery":dno})
            if path=="/api/deliveries/void":
                d = c.execute("SELECT * FROM delivery_orders WHERE id=?",(b["id"],)).fetchone()
                if not d or d["status"]=="VOID": raise ValueError("DO tidak valid")
                date = b.get("date", datetime.date.today().isoformat())
                inv = c.execute("SELECT COALESCE(SUM(invoiced_qty),0) s FROM delivery_order_lines WHERE delivery_order_id=?",(d["id"],)).fetchone()["s"] or 0
                if inv > 0.005: raise ValueError("DO sudah difakturkan, tidak bisa void")
                jid = reverse_journal(c, d["journal_entry_id"], next_no(c,"JE","journal_entries","journal_number"), date, "Void "+d["delivery_number"])
                for t in q(c,"SELECT * FROM inventory_transactions WHERE reference_type='DELIVERY_ORDER' AND reference_id=?",(d["id"],)):
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (t["item_id"],t["warehouse_id"],date,"DELIVERY_VOID",d["id"],t["qty_out"],t["cogs_unit_price"]))
                    if is_fifo(c,t["item_id"]):
                        add_layer(c,t["item_id"],t["warehouse_id"],date,"DELIVERY_VOID",d["id"],t["qty_out"],t["cogs_unit_price"])
                c.execute("UPDATE delivery_orders SET status='VOID' WHERE id=?",(d["id"],))
                if d["sales_order_id"]: refresh_doc_status(c,"SO",d["sales_order_id"])
                c.commit(); return self._json({"ok":True})
            if path=="/api/sales/void":
                s = c.execute("SELECT * FROM sales_invoices WHERE id=?", (b["id"],)).fetchone()
                if not s: raise ValueError("Invoice tidak ditemukan")
                if s["status"]=="VOID": raise ValueError("Invoice sudah void")
                # Tahap2 maker-checker: KASIR/GUDANG/HRD wajib approval MGR
                if me["role"] in ("KASIR","GUDANG","HRD"):
                    c.execute("INSERT INTO approvals(kind,ref_type,ref_id,amount,requested_by,status,created_at) VALUES(?,?,?,?,?,?,?)",
                        ("VOID","SALES_INVOICE",s["id"],rp_int(s["total_amount"]),me["username"],"PENDING",datetime.datetime.now().isoformat()))
                    c.commit(); return self._json({"ok":True,"need_approval":True,"msg":"Menunggu persetujuan MANAGER"})
                date = b.get("date", datetime.date.today().isoformat())
                jid = reverse_journal(c, s["journal_entry_id"], next_no(c,"JE","journal_entries","journal_number"), date, "Void "+s["invoice_number"])
                for t in q(c,"SELECT * FROM inventory_transactions WHERE reference_type='SALES_INVOICE' AND reference_id=?", (s["id"],)):
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (t["item_id"],t["warehouse_id"],date,"SALES_VOID",s["id"],t["qty_out"],t["cogs_unit_price"]))
                    if is_fifo(c,t["item_id"]):
                        add_layer(c,t["item_id"],t["warehouse_id"],date,"SALES_VOID",s["id"],t["qty_out"],t["cogs_unit_price"])
                for t in q(c,"SELECT * FROM inventory_transactions WHERE reference_type='TRADE_IN' AND reference_id=?", (s["id"],)):
                    if stock_of(c,t["item_id"],t["warehouse_id"]) < t["qty_in"]:
                        raise ValueError("Stok barang tukar-tambah sudah terpakai, void dibatalkan")
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (t["item_id"],t["warehouse_id"],date,"TRADE_VOID",s["id"],t["qty_in"],t["cogs_unit_price"]))
                    if is_fifo(c,t["item_id"]):
                        consume_fifo(c,t["item_id"],t["warehouse_id"],date,"TRADE_VOID",s["id"],t["qty_in"])
                if "commission_journal_id" in s.keys() and s["commission_journal_id"]:
                    reverse_journal(c, s["commission_journal_id"], next_no(c,"JE","journal_entries","journal_number"), date, "Void komisi "+s["invoice_number"])
                for r in q(c,"SELECT delivery_order_line_id,quantity FROM sales_invoice_lines WHERE sales_invoice_id=? AND delivery_order_line_id IS NOT NULL",(s["id"],)):
                    c.execute("UPDATE delivery_order_lines SET invoiced_qty=invoiced_qty-? WHERE id=?",(r["quantity"],r["delivery_order_line_id"]))
                for so_id in {r["sales_order_id"] for r in q(c,"SELECT DISTINCT so.sales_order_id FROM sales_invoice_lines l JOIN sales_order_lines so ON so.id=l.sales_order_line_id WHERE l.sales_invoice_id=? AND l.sales_order_line_id IS NOT NULL",(s["id"],)) if r["sales_order_id"]}:
                    refresh_doc_status(c,"SO",so_id)
                c.execute("UPDATE sales_invoices SET status='VOID' WHERE id=?", (s["id"],))
                c.commit(); return self._json({"ok":True,"reversal_journal":jid})
            if path=="/api/requisitions":
                cur = c.execute("INSERT INTO purchase_requisitions(requisition_number,transaction_date,vendor_id,requester,notes) VALUES(?,?,?,?,?)",
                    (b.get("requisition_number") or next_no(c,"PR","purchase_requisitions","requisition_number"),b["date"],b.get("vendor_id"),b.get("requester",""),b.get("notes","")))
                rid = cur.lastrowid
                for l in b["lines"]:
                    it = c.execute("SELECT * FROM items WHERE id=?",(l["item_id"],)).fetchone()
                    conv = float(l.get("unit_conv",1)) or 1
                    c.execute("INSERT INTO purchase_requisition_lines(requisition_id,item_id,quantity,est_price,description,unit_code,unit_qty,unit_conv) VALUES(?,?,?,?,?,?,?,?)",
                        (rid,it["id"],round(float(l["qty"])*conv,2),float(l.get("price",0)),l.get("description",""),l.get("unit_code",it["base_unit"]),float(l["qty"]),conv))
                c.commit(); return self._json({"ok":True})
            if path=="/api/requisitions/close":
                c.execute("UPDATE purchase_requisitions SET status='CLOSED' WHERE id=?",(b["id"],))
                c.commit(); return self._json({"ok":True})
            if path=="/api/purchase-orders":
                subtotal=0; cl=[]
                for l in b["lines"]:
                    d = calc_line(c,l); subtotal+=d["lt"]; cl.append(d)
                tax = rp_int(subtotal*float(b.get("tax_rate",0))/100)
                ono = b.get("order_number") or next_no(c,"PO","purchase_orders","order_number")
                cur = c.execute("INSERT INTO purchase_orders(order_number,transaction_date,vendor_id,requisition_id,subtotal,tax_amount,total_amount,notes) VALUES(?,?,?,?,?,?,?,?)",
                    (ono,b["date"],b["vendor_id"],b.get("requisition_id"),subtotal,tax,subtotal+tax,b.get("notes","")))
                oid = cur.lastrowid
                for d in cl:
                    c.execute("INSERT INTO purchase_order_lines(purchase_order_id,item_id,warehouse_id,quantity,unit_price,line_total,description,unit_code,unit_qty,unit_conv) VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (oid,d["it"]["id"],d["wh"],d["base"],d["price"],d["lt"],d["desc"],d["ucode"],d["uqty"],d["conv"]))
                if b.get("requisition_id"):
                    c.execute("UPDATE purchase_requisitions SET status='ORDERED' WHERE id=?",(b["requisition_id"],))
                c.commit(); return self._json({"ok":True,"order":ono})
            if path=="/api/purchase-orders/close":
                c.execute("UPDATE purchase_orders SET status='CLOSED' WHERE id=?",(b["id"],))
                c.commit(); return self._json({"ok":True})
            if path=="/api/receives":
                vend = c.execute("SELECT * FROM vendors WHERE id=?",(b["vendor_id"],)).fetchone()
                date = b["date"]; subtotal=0; rl=[]
                for l in b["lines"]:
                    it = c.execute("SELECT * FROM items WHERE id=?",(l["item_id"],)).fetchone()
                    conv = float(l.get("unit_conv",1)) or 1
                    base = round(float(l["qty"])*conv,2)
                    pol = None
                    if l.get("purchase_order_line_id"):
                        pol = c.execute("SELECT * FROM purchase_order_lines WHERE id=?",(l["purchase_order_line_id"],)).fetchone()
                        if not pol: raise ValueError("Baris PO tidak valid")
                        f = po_fulfill(c,pol["id"])
                        if base > f["ordered"]-f["received"]+0.005:
                            raise ValueError(f"Melebihi sisa PO ({f['ordered']-f['received']})")
                        if pol["item_id"]!=it["id"]: raise ValueError("Barang beda dengan baris PO")
                    price = float(l.get("price", (pol["unit_price"]/(pol["unit_conv"] or 1)) if pol else 0) or 0)
                    lt = round(float(l["qty"])*price,2); subtotal+=lt
                    rl.append((it,pol,base,price,lt,l.get("unit_code",it["base_unit"]),float(l["qty"]),conv,int(l.get("warehouse_id") or (pol["warehouse_id"] if pol else 0)),l.get("description","")))
                rno = b.get("receive_number") or next_no(c,"RI","receive_items","receive_number")
                cur = c.execute("INSERT INTO receive_items(receive_number,transaction_date,purchase_order_id,vendor_id,subtotal) VALUES(?,?,?,?,?)",
                    (rno,date,b.get("purchase_order_id"),b["vendor_id"],subtotal))
                rid = cur.lastrowid; inv_sum={}
                for it,pol,base,price,lt,ucode,uqty,conv,wh,desc in rl:
                    if not wh: raise ValueError("Gudang wajib diisi")
                    c.execute("INSERT INTO receive_item_lines(receive_id,purchase_order_line_id,item_id,warehouse_id,quantity,unit_price,line_total,description,unit_code,unit_qty,unit_conv) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (rid,pol["id"] if pol else None,it["id"],wh,base,price,lt,desc,ucode,uqty,conv))
                    bprice = round(price/conv,2)
                    acc = it["inventory_account_id"] or acct(c,"13001")
                    inv_sum[acc] = inv_sum.get(acc,0)+round(base*bprice,2)
                    if it["item_type"]!="INVENTORY":
                        continue
                    receive_in(c,it,wh,date,"RECEIVE_ITEM",rid,base,bprice)
                    old_s = stock_of(c,it["id"]) - base
                    old_c = it["avg_cost"] or bprice
                    new_avg = (old_s*old_c + base*bprice)/max(old_s+base,0.0001) if old_s>0 else bprice
                    c.execute("UPDATE items SET avg_cost=?,purchase_price=? WHERE id=?",(new_avg,bprice,it["id"]))
                jl=[]
                for a,amt in inv_sum.items(): jl.append((a,round(amt,2),0,"Terima "+rno))
                jl.append((dict(vend)["payable_account_id"],0,round(subtotal,2),"Utang terima "+rno))
                if inv_sum:
                    jid = post_journal(c,"JE-"+rno,date,"RECEIVE_ITEM",rid,"Penerimaan "+rno,jl)
                    c.execute("UPDATE receive_items SET journal_entry_id=? WHERE id=?",(jid,rid))
                if b.get("purchase_order_id"): refresh_doc_status(c,"PO",b["purchase_order_id"])
                c.commit(); return self._json({"ok":True,"receive":rno})
            if path=="/api/receives/void":
                r = c.execute("SELECT * FROM receive_items WHERE id=?",(b["id"],)).fetchone()
                if not r or r["status"]=="VOID": raise ValueError("Receive tidak valid")
                date = b.get("date", datetime.date.today().isoformat())
                billed = c.execute("SELECT COALESCE(SUM(billed_qty),0) s FROM receive_item_lines WHERE receive_id=?",(r["id"],)).fetchone()["s"] or 0
                if billed > 0.005: raise ValueError("Receive sudah ditagih, tidak bisa void")
                ins = q(c,"SELECT * FROM inventory_transactions WHERE reference_type='RECEIVE_ITEM' AND reference_id=?",(r["id"],))
                for t in ins:
                    if stock_of(c,t["item_id"],t["warehouse_id"]) < t["qty_in"]:
                        raise ValueError("Stok tidak cukup untuk void (barang sudah terpakai)")
                if r["journal_entry_id"]:
                    reverse_journal(c, r["journal_entry_id"], next_no(c,"JE","journal_entries","journal_number"), date, "Void "+r["receive_number"])
                for t in ins:
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (t["item_id"],t["warehouse_id"],date,"RECEIVE_VOID",r["id"],t["qty_in"],t["cogs_unit_price"]))
                    if is_fifo(c,t["item_id"]):
                        consume_fifo(c,t["item_id"],t["warehouse_id"],date,"RECEIVE_VOID",r["id"],t["qty_in"])
                c.execute("UPDATE receive_items SET status='VOID' WHERE id=?",(r["id"],))
                if r["purchase_order_id"]: refresh_doc_status(c,"PO",r["purchase_order_id"])
                c.commit(); return self._json({"ok":True})
            if path=="/api/purchases/void":
                s = c.execute("SELECT * FROM purchase_invoices WHERE id=?", (b["id"],)).fetchone()
                if not s: raise ValueError("Tagihan tidak ditemukan")
                if s["status"]=="VOID": raise ValueError("Tagihan sudah void")
                if me["role"] in ("KASIR","GUDANG","HRD"):
                    c.execute("INSERT INTO approvals(kind,ref_type,ref_id,amount,requested_by,status,created_at) VALUES(?,?,?,?,?,?,?)",
                        ("VOID","PURCHASE_INVOICE",s["id"],rp_int(s["total_amount"]),me["username"],"PENDING",datetime.datetime.now().isoformat()))
                    c.commit(); return self._json({"ok":True,"need_approval":True,"msg":"Menunggu persetujuan MANAGER"})
                date = b.get("date", datetime.date.today().isoformat())
                ins = q(c,"SELECT * FROM inventory_transactions WHERE reference_type='PURCHASE_INVOICE' AND reference_id=?", (s["id"],))
                for t in ins:
                    if stock_of(c,t["item_id"],t["warehouse_id"]) < t["qty_in"]:
                        raise ValueError("Stok tidak cukup untuk void (barang sudah terjual)")
                jid = reverse_journal(c, s["journal_entry_id"], next_no(c,"JE","journal_entries","journal_number"), date, "Void "+s["invoice_number"])
                for t in ins:
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                        (t["item_id"],t["warehouse_id"],date,"PURCHASE_VOID",s["id"],t["qty_in"],t["cogs_unit_price"]))
                    if is_fifo(c,t["item_id"]):
                        consume_fifo(c,t["item_id"],t["warehouse_id"],date,"PURCHASE_VOID",s["id"],t["qty_in"])
                for r in q(c,"SELECT receive_line_id,quantity FROM purchase_invoice_lines WHERE purchase_invoice_id=? AND receive_line_id IS NOT NULL",(s["id"],)):
                    c.execute("UPDATE receive_item_lines SET billed_qty=billed_qty-? WHERE id=?",(r["quantity"],r["receive_line_id"]))
                c.execute("UPDATE purchase_invoices SET status='VOID' WHERE id=?", (s["id"],))
                c.commit(); return self._json({"ok":True,"reversal_journal":jid})
            if path=="/api/sales/returns":
                s = c.execute("SELECT * FROM sales_invoices WHERE id=?", (b["sales_invoice_id"],)).fetchone()
                if not s or s["status"]=="VOID": raise ValueError("Invoice tidak valid")
                date = b.get("date", datetime.date.today().isoformat())
                cust = c.execute("SELECT * FROM customers WHERE id=?", (s["customer_id"],)).fetchone()
                subtotal=0; rlines=[]
                for l in b["lines"]:
                    it = c.execute("SELECT * FROM items WHERE id=?", (l["item_id"],)).fetchone()
                    inv_l = c.execute("SELECT * FROM sales_invoice_lines WHERE sales_invoice_id=? AND item_id=?", (s["id"], it["id"])).fetchone()
                    if not inv_l: raise ValueError(f"{it['item_code']} tidak ada di invoice ini")
                    qty = float(l["qty"])
                    maxq = inv_l["quantity"] - returned_qty(c,"SALES",s["id"],it["id"])
                    if qty <= 0 or qty > maxq+0.005: raise ValueError(f"Qty retur {it['item_code']} max {maxq}")
                    lt = rp_int(qty*inv_l["unit_price"]); subtotal += lt
                    rlines.append((it, qty, inv_l["unit_price"], lt, l.get("description", inv_l["description"] if "description" in inv_l.keys() else "")))
                tax = rp_int(subtotal*float(b.get("tax_rate", s["tax_amount"]/s["subtotal"]*100 if s["subtotal"] else 0))/100)
                total = subtotal+tax
                if outstanding_of(c,"AR",s["id"],s["total_amount"]) < total:
                    raise ValueError("Retur melebihi sisa piutang (sudah dibayar)")
                ret_no = next_no(c,"RS","sales_returns","return_number")
                cur = c.execute("INSERT INTO sales_returns(return_number,sales_invoice_id,transaction_date,subtotal,tax_amount,total_amount) VALUES(?,?,?,?,?,?)",
                    (ret_no,s["id"],date,subtotal,tax,total))
                rid = cur.lastrowid; hpp=0
                sales_back={}; inv_back={}; cogs_back={}
                for it,qty,price,lt,desc in rlines:
                    c.execute("INSERT INTO sales_return_lines(sales_return_id,item_id,warehouse_id,quantity,unit_price,line_total,description) VALUES(?,?,?,?,?,?,?)",
                        (rid,it["id"],b["warehouse_id"],qty,price,lt,desc))
                    sales_back[it["sales_account_id"]] = sales_back.get(it["sales_account_id"],0)+lt
                    if it["item_type"]=="INVENTORY":
                        cost = it["avg_cost"] or 0; hpp += cost*qty
                        inv_back[it["inventory_account_id"]] = inv_back.get(it["inventory_account_id"],0)+cost*qty
                        cogs_back[it["cogs_account_id"]] = cogs_back.get(it["cogs_account_id"],0)+cost*qty
                        c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                            (it["id"],b["warehouse_id"],date,"SALES_RETURN",rid,qty,cost))
                        if is_fifo(c,it["id"]):
                            add_layer(c,it["id"],b["warehouse_id"],date,"SALES_RETURN",rid,qty,cost)
                jl=[]
                for acc,amt in sales_back.items(): jl.append((acc,amt,0,"Retur "+ret_no))
                if tax: jl.append((acct(c,"22001"),tax,0,"PPN retur "+ret_no))
                jl.append((cust["receivable_account_id"],0,total,"Kurangi piutang "+ret_no))
                for acc,amt in inv_back.items(): jl.append((acc,amt,0,"Stok kembali "+ret_no))
                for acc,amt in cogs_back.items(): jl.append((acc,0,amt,"HPP kembali "+ret_no))
                jid = post_journal(c,"JE-"+ret_no,date,"SALES_RETURN",rid,"Retur penjualan "+ret_no,jl)
                c.execute("UPDATE sales_returns SET journal_entry_id=? WHERE id=?",(jid,rid))
                refresh_status(c,"AR",s["id"])
                c.commit(); return self._json({"ok":True,"return":ret_no,"total":total})
            if path=="/api/purchases/returns":
                s = c.execute("SELECT * FROM purchase_invoices WHERE id=?", (b["purchase_invoice_id"],)).fetchone()
                if not s or s["status"]=="VOID": raise ValueError("Tagihan tidak valid")
                date = b.get("date", datetime.date.today().isoformat())
                vend = c.execute("SELECT * FROM vendors WHERE id=?", (s["vendor_id"],)).fetchone()
                subtotal=0; rlines=[]
                for l in b["lines"]:
                    it = c.execute("SELECT * FROM items WHERE id=?", (l["item_id"],)).fetchone()
                    inv_l = c.execute("SELECT * FROM purchase_invoice_lines WHERE purchase_invoice_id=? AND item_id=?", (s["id"], it["id"])).fetchone()
                    if not inv_l: raise ValueError(f"{it['item_code']} tidak ada di tagihan ini")
                    qty = float(l["qty"])
                    maxq = inv_l["quantity"] - returned_qty(c,"PURCHASE",s["id"],it["id"])
                    if qty <= 0 or qty > maxq+0.005: raise ValueError(f"Qty retur {it['item_code']} max {maxq}")
                    if it["item_type"]=="INVENTORY" and stock_of(c,it["id"],b["warehouse_id"]) < qty:
                        raise ValueError(f"Stok {it['item_code']} kurang untuk diretur")
                    lt = rp_int(qty*inv_l["unit_price"]); subtotal += lt
                    rlines.append((it, qty, inv_l["unit_price"], lt, l.get("description", inv_l["description"] if "description" in inv_l.keys() else "")))
                tax = rp_int(subtotal*float(b.get("tax_rate", s["tax_amount"]/s["subtotal"]*100 if s["subtotal"] else 0))/100)
                total = subtotal+tax
                if outstanding_of(c,"AP",s["id"],s["total_amount"]) < total:
                    raise ValueError("Retur melebihi sisa utang (sudah dibayar)")
                ret_no = next_no(c,"RP","purchase_returns","return_number")
                cur = c.execute("INSERT INTO purchase_returns(return_number,purchase_invoice_id,transaction_date,subtotal,tax_amount,total_amount) VALUES(?,?,?,?,?,?)",
                    (ret_no,s["id"],date,subtotal,tax,total))
                rid = cur.lastrowid
                for it,qty,price,lt,desc in rlines:
                    c.execute("INSERT INTO purchase_return_lines(purchase_return_id,item_id,warehouse_id,quantity,unit_price,line_total,description) VALUES(?,?,?,?,?,?,?)",
                        (rid,it["id"],b["warehouse_id"],qty,price,lt,desc))
                    if it["item_type"]=="INVENTORY":
                        c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,reference_id,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?,?)",
                            (it["id"],b["warehouse_id"],date,"PURCHASE_RETURN",rid,qty,it["avg_cost"] or price))
                        if is_fifo(c,it["id"]):
                            consume_fifo(c,it["id"],b["warehouse_id"],date,"PURCHASE_RETURN",rid,qty)
                jl=[(vend["payable_account_id"],total,0,"Kurangi utang "+ret_no),
                    (acct(c,"13001"),0,subtotal,"Stok retur "+ret_no)]
                if tax: jl.append((acct(c,"14001"),0,tax,"PPN retur "+ret_no))
                jid = post_journal(c,"JE-"+ret_no,date,"PURCHASE_RETURN",rid,"Retur pembelian "+ret_no,jl)
                c.execute("UPDATE purchase_returns SET journal_entry_id=? WHERE id=?",(jid,rid))
                refresh_status(c,"AP",s["id"])
                c.commit(); return self._json({"ok":True,"return":ret_no,"total":total})
            if path=="/api/transfers":
                fa = c.execute("SELECT * FROM chart_of_accounts WHERE id=?", (b["from_account"],)).fetchone()
                ta = c.execute("SELECT * FROM chart_of_accounts WHERE id=?", (b["to_account"],)).fetchone()
                if not fa or not ta: raise ValueError("Akun tidak valid")
                if not fa["account_code"].startswith("110") or not ta["account_code"].startswith("110"):
                    raise ValueError("Transfer hanya antar akun Kas/Bank (110xx)")
                if fa["id"]==ta["id"]: raise ValueError("Akun asal & tujuan sama")
                amount = rp_int(b["amount"])
                if amount <= 0: raise ValueError("Nominal harus > 0")
                date = b.get("date", datetime.date.today().isoformat())
                jid = post_journal(c,b.get("journal_number") or next_no(c,"JE","journal_entries","journal_number"),
                    date,"CASH_TRANSFER",None,b.get("note") or f"Transfer {fa['account_name']} -> {ta['account_name']}",
                    [(ta["id"],amount,0,"Masuk"),(fa["id"],0,amount,"Keluar")])
                c.commit(); return self._json({"ok":True,"id":jid})
            if path=="/api/vendors/limit":
                c.execute("UPDATE vendors SET credit_limit=? WHERE id=?", (float(b["credit_limit"]), b["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/customers/limit":
                c.execute("UPDATE customers SET credit_limit=?,terms=?,term_days=? WHERE id=?",
                    (float(b.get("credit_limit",0)), b.get("terms",""), int(b.get("term_days",0)), b["id"]))
                c.commit(); return self._json({"ok":True})
            if path=="/api/stock/opname":
                it = c.execute("SELECT * FROM items WHERE id=?", (b["item_id"],)).fetchone()
                if not it or it["item_type"]!="INVENTORY": raise ValueError("Pilih barang persediaan")
                date = b.get("date", datetime.date.today().isoformat())
                sys_qty = stock_of(c, it["id"], b["warehouse_id"])
                diff = round(float(b["actual_qty"]) - sys_qty, 2)
                if abs(diff) < 0.005: raise ValueError("Tidak ada selisih")
                cost = it["avg_cost"] or 0; val = round(abs(diff)*cost, 2)
                if diff > 0:
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?)",
                        (it["id"],b["warehouse_id"],date,"OPNAME",diff,cost))
                    if is_fifo(c,it["id"]):
                        add_layer(c,it["id"],b["warehouse_id"],date,"OPNAME",None,diff,cost)
                    jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"OPNAME",None,
                        f"Opname {it['item_code']} surplus {diff}",[(it["inventory_account_id"],val,0,"Surplus"),(acct(c,"71001"),0,val,"Surplus")])
                else:
                    if is_fifo(c,it["id"]):
                        consume_fifo(c,it["id"],b["warehouse_id"],date,"OPNAME",None,-diff)
                    c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?)",
                        (it["id"],b["warehouse_id"],date,"OPNAME",-diff,cost))
                    jid = post_journal(c,next_no(c,"JE","journal_entries","journal_number"),date,"OPNAME",None,
                        f"Opname {it['item_code']} minus {-diff}",[(acct(c,"72001"),val,0,"Selisih"),(it["inventory_account_id"],0,val,"Selisih")])
                c.commit(); return self._json({"ok":True,"diff":diff,"value":val})
            if path=="/api/stock/transfer":
                it = c.execute("SELECT * FROM items WHERE id=?", (b["item_id"],)).fetchone()
                if not it or it["item_type"]!="INVENTORY": raise ValueError("Pilih barang persediaan")
                if b["from_warehouse"]==b["to_warehouse"]: raise ValueError("Gudang asal & tujuan sama")
                qty = float(b["qty"])
                if stock_of(c,it["id"],b["from_warehouse"]) < qty: raise ValueError("Stok gudang asal kurang")
                date = b.get("date", datetime.date.today().isoformat()); cost = it["avg_cost"] or 0
                if is_fifo(c,it["id"]):
                    cost = rp_int(consume_fifo(c,it["id"],b["from_warehouse"],date,"TRANSFER",None,qty)/qty) if qty else 0
                c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,qty_out,cogs_unit_price) VALUES(?,?,?,?,?,?)",
                    (it["id"],b["from_warehouse"],date,"TRANSFER",qty,cost))
                c.execute("INSERT INTO inventory_transactions(item_id,warehouse_id,transaction_date,reference_type,qty_in,cogs_unit_price) VALUES(?,?,?,?,?,?)",
                    (it["id"],b["to_warehouse"],date,"TRANSFER",qty,cost))
                if is_fifo(c,it["id"]):
                    add_layer(c,it["id"],b["to_warehouse"],date,"TRANSFER",None,qty,cost)
                c.commit(); return self._json({"ok":True})
            if path=="/api/payments":
                kind=b["kind"]; cash=int(b["cash_account_id"])
                allocs = b.get("allocations") or []
                if b.get("invoice_id") and not allocs:
                    inv_tbl = "sales_invoices" if kind=="AR" else "purchase_invoices"
                    t = c.execute(f"SELECT total_amount FROM {inv_tbl} WHERE id=?", (b["invoice_id"],)).fetchone()
                    already = outstanding_of(c, kind, b["invoice_id"], t["total_amount"])
                    allocs = [{"invoice_id": b["invoice_id"], "amount": round(already,2)}]
                amount = round(sum(float(a["amount"]) for a in allocs),2)
                if amount <= 0: raise ValueError("Alokasi pembayaran kosong")
                if abs(amount - float(b.get("amount", amount))) > 0.005:
                    raise ValueError("Total alokasi harus sama dengan nominal pembayaran")
                inv_tbl = "sales_invoices" if kind=="AR" else "purchase_invoices"
                for a in allocs:
                    t = c.execute(f"SELECT * FROM {inv_tbl} WHERE id=?", (a["invoice_id"],)).fetchone()
                    if not t or t["status"]=="VOID": raise ValueError(f"Invoice #{a['invoice_id']} tidak valid")
                    if outstanding_of(c,kind,a["invoice_id"],t["total_amount"]) < float(a["amount"])-0.005:
                        raise ValueError(f"Alokasi melebihi sisa tagihan {t['invoice_number']}")
                if kind=="AR":
                    cust=c.execute("SELECT * FROM customers WHERE id=?",(b["contact_id"],)).fetchone()
                    jid=post_journal(c,b.get("payment_number") or next_no(c,"PAY","payments","payment_number"),b["date"],"CUSTOMER_RECEIPT",None,f"Terima {cust['customer_name']}",[(cash,amount,0,"Kas"),(cust["receivable_account_id"],0,amount,"Piutang")])
                else:
                    vend=c.execute("SELECT * FROM vendors WHERE id=?",(b["contact_id"],)).fetchone()
                    jid=post_journal(c,b.get("payment_number") or next_no(c,"PAY","payments","payment_number"),b["date"],"VENDOR_PAYMENT",None,f"Bayar {vend['vendor_name']}",[(vend["payable_account_id"],amount,0,"Utang"),(cash,0,amount,"Kas")])
                cur=c.execute("INSERT INTO payments(payment_number,transaction_date,kind,contact_id,cash_account_id,amount,note,journal_entry_id) VALUES(?,?,?,?,?,?,?,?)",
                    ("PAY-"+str(jid),b["date"],kind,b["contact_id"],cash,amount,b.get("note",""),jid))
                pid = cur.lastrowid
                for a in allocs:
                    c.execute("INSERT INTO payment_allocations(payment_id,invoice_type,invoice_id,amount) VALUES(?,?,?,?)",(pid,kind,a["invoice_id"],float(a["amount"])))
                    refresh_status(c,kind,a["invoice_id"])
                c.commit(); return self._json({"ok":True,"amount":amount})
            if path=="/api/assets":
                c.execute("INSERT INTO fixed_assets(asset_code,asset_name,purchase_date,cost,useful_months,method,asset_account_id,depr_expense_account_id,accum_account_id) VALUES(?,?,?,?,?,?,?,?,?)",
                    (b["asset_code"],b["asset_name"],b["purchase_date"],float(b["cost"]),int(b.get("useful_months",48)),b.get("method","STRAIGHT"),b.get("asset_account_id"),b.get("depr_expense_account_id"),b.get("accum_account_id")))
                c.commit(); return self._json({"ok":True})
            if path=="/api/assets/depreciate":
                a=c.execute("SELECT * FROM fixed_assets WHERE id=?",(b["id"],)).fetchone()
                monthly=a["cost"]/a["useful_months"] if a["method"]=="STRAIGHT" else (a["cost"]-a["accum_depr"])*0.05
                monthly=min(monthly,a["cost"]-a["accum_depr"])
                jid=post_journal(c,next_no(c,"JE","journal_entries","journal_number"),b.get("date",datetime.date.today().isoformat()),"DEPRECIATION",a["id"],f"Penyusutan {a['asset_name']}",[(a["depr_expense_account_id"] or acct(c,"64001"),monthly,0,"Beban"),(a["accum_account_id"] or acct(c,"15002"),0,monthly,"Akumulasi")])
                c.execute("UPDATE fixed_assets SET accum_depr=accum_depr+? WHERE id=?",(monthly,a["id"]))
                c.commit(); return self._json({"ok":True,"amount":monthly})
            if path=="/api/webhooks":
                c.execute("INSERT INTO webhooks(event,url) VALUES(?,?)",(b["event"],b["url"])); c.commit()
                return self._json({"ok":True})
            if path=="/api/ocr-draft":
                # Terima hasil "baca struk" dari frontend -> buat draft journal
                jid=post_journal(c,b.get("journal_number") or next_no(c,"JE","journal_entries","journal_number"),b.get("date",datetime.date.today().isoformat()),"OCR_DRAFT",None,b.get("description","OCR draft"),[(l["account_id"],float(l.get("debit",0)),float(l.get("credit",0)),"OCR") for l in b["lines"]])
                c.execute("UPDATE journal_entries SET status='DRAFT' WHERE id=?",(jid,))
                c.commit(); return self._json({"ok":True,"id":jid})
            return self._json({"error":"not found"},404)
        except PermissionError as e:
            c.rollback(); return self._json({"error":str(e)},403)
        except Exception as e:
            c.rollback(); return self._json({"error":str(e)},400)
        finally: c.close()

    def serve_static(self, fn):
        fp = os.path.join(PUBLIC, fn)
        if not os.path.exists(fp): fp = os.path.join(PUBLIC, "index.html")
        ext = fp.rsplit(".",1)[-1]
        ct = {"html":"text/html","js":"text/javascript","css":"text/css"}.get(ext,"text/plain")
        try:
            with open(fp,"rb") as f: b=f.read()
            self.send_response(200); self.send_header("Content-Type",ct); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
        except Exception as e: self._json({"error":str(e)},500)

if __name__=="__main__":
    os.makedirs(PUBLIC, exist_ok=True)
    # pastikan folder DB ada (untuk AKUNTANSIKU_DB=/app/data/database.db di Docker)
    try: os.makedirs(os.path.dirname(DB), exist_ok=True)
    except Exception: pass
    init_db()
    srv = ThreadingHTTPServer(("0.0.0.0",PORT),H)
    print(f"Aplikasi Akuntansi jalan di http://localhost:{PORT} (DB={DB})")
    srv.serve_forever()
