# HBA DECISION RECORD — Rasionalisasi status IS-01/IS-02, C-1/C-2/C-3/C-5, dan portal pelanggan (2026-10-07)

```text
Record ID:      HBA-DECISIONS-08
Date:           2026-10-07
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decisions as stated by HBA in group chat 2026-10-07
Classification: Audit record. NOT a canonical specification document.
Implementation: None in this record. Edits to IS-01/IS-02 status headers are documentation
                reconciliations performed under explicit HBA authorization in the same session.
```

---

## Decisions (verbatim intent)

1. **C-1 residual — 3 kunjungan lama COMPLETED tanpa jam masuk/keluar**: HBA states there is
   no real data yet, so these old visits **can be ignored**; if the artifact exists only because
   of legacy data, mark them. Normative reading (applied under §2.1 interpretation rule since the
   decision is conditional on facts):
   - Deferred business decision: the legacy-visit handling remains **DEFERRED until first real
     data** — do not invent legacy-migration behavior now. If such data actually appears, mark it
     (HBA-prescribed action), do not silently reinterpret. **LOCK so no further per-visit
     decision is needed.**

2. **C-2 + C-5**: HBA **authorizes building the general event store (C-2)** and the
   **acknowledge no-op fix (C-5)**. **LOCK.**

3. **C-3**: HBA **re-affirms full corrective fix authorization** (initially authorized
   HBA-DECISIONS-07). **LOCK.**

4. **IS-01 and IS-02**: HBA **acknowledges and accepts both specifications** and authorizes the
   status-header edits. **LOCK — recorded as ACCEPTED by HBA 2026-10-07.** Implementation still
   requires separate authorization.

5. **Portal (IS-06)**: Portal **must NOT display prices**. Login/signup **Google-only**.
   Embedded-vs-separate serving: HBA asks for **pros and cons** — no decision yet; provide
   comparison, HBA decides. Publication mechanism: still OPEN (architecture/mechanism).

## Applied edits (authorized documentation reconciliation)

- `docs/40-SPECIFICATION/IS-01-domain-data-model-specification.md` — status header updated to
  ACKNOWLEDGED & ACCEPTED by HBA (2026-10-07, per this record).
- `docs/40-SPECIFICATION/IS-02-service-execution-specification.md` — status header updated to
  ACKNOWLEDGED & ACCEPTED by HBA (2026-10-07, per this record).
- Portal price/login decisions to be materialized in IS-06 as a separate scoped edit.

## Not decided by this record

- IS-06 embedded-vs-separate serving (pros/cons presented; HBA decision pending).
- IS-06 publication/serving mechanism (architecture/mechanism OPEN).
- Remaining deferred/clarification items already on the board (index cleanup details, old WV-1
  superseded items, etc.).

*End of decision record.*
