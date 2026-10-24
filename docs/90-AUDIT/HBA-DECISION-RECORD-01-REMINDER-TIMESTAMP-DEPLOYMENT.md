# HBA DECISION RECORD — REMINDER, TIMESTAMP, DEPLOYMENT

```text
Record ID:      HBA-DEC-RECORD-01
Date:           2026-10-01
Recorded by:    Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decisions as stated by HBA in session 2026-10-01
Classification: Audit record. NOT a canonical specification document.
Implementation: NO code / schema / migration / deployment change made by this record.
```

> This record captures three HBA decisions exactly as stated. It does **not**
> materialize them into canonical documents (DECISION_REGISTER, CD-11, IS-00 §14,
> IS-01, IS-02, IS-10). Those updates are a separate, explicitly-authorized step.

---

## DECISION 1 — REMINDER / AUTOMATION POLICY

**HBA decision: DEFERRED to a future version. Manual-only remains for V1.**

### What HBA stated

- The rule is not yet designed ("kita belum buat rulenya").
- It must be possible to add it later.
- Intended future direction (illustrative, NOT locked):
  - For **maintenance** work, an automatic reminder appears on the **Sales dashboard**,
    signalling that a customer follow-up is due.
  - It does **NOT** auto-create a Work Order.
  - **Any** Sales user may pick up the reminder.
  - Sales then records the follow-up outcome: either close it with a reason, or
    create a new WO.
  - This is **for recording only**.
- To be built in a future version.

### Effect on current state

| Aspect | State after this decision |
|---|---|
| Manual reminder (Admin/Manager/Sales) | Unchanged — remains the V1 baseline, already implemented |
| Automatic reminder generation | Remains DISABLED in V1 |
| Reminder/automation policy question | Remains open, but now **deferred by HBA** rather than merely unresolved |

### Is later addition possible without rework?

**Yes.** Verified in code:

- `app/reporting/reminder.py` carries an explicit `AUTOMATIC_REMINDERS_ENABLED = False`
  constant with a documented disabled reason, plus a stated rule that the module
  builds no scheduler and no interval field.
- The reminder record (`E-55`) and its authority model already exist and are
  workspace-scoped.
- Adding automatic generation later is **additive**: a scheduler/trigger plus a
  dashboard surface. No existing reminder behaviour, table, or authority needs to
  be redefined.

### Not decided by this record

Intervals, trigger conditions, escalation, notification channel, and the
"any Sales may claim" pooling model are **direction notes only**. They are not
locked and not canonical.

---

## DECISION 2 — WO TIMESTAMP AUTHORITY

**HBA decision: DECIDED. The WO creation timestamp is authoritative. No retroactive
event-time convention is required.**

### What HBA stated

- The scenario of a WO being recorded long after the work occurred **does not exist
  in this operation** ("Tidak ada cerita seperti itu").
- A WO is created **before** the technician works; or, if the technician happens to
  be on site, they create the WO there and then.
- The WO is therefore created **instantly at that moment**.
- The recorded creation time is correct and presents no problem.
- The basis is simply **when the WO was created**.

### Effect on current state

| Aspect | State after this decision |
|---|---|
| Authoritative time | WO **creation time** (`created_at`) |
| Dual capture (event-time + record-time) | **Not required** by business need |
| Emergency retroactive convention | **Not required** — the scenario it would govern does not occur |
| Current implementation | Already conforms — `work_orders` carries `created_at` |

### Verified implementation fact

The schema carries a single creation timestamp. No `event_time` / `record_time` /
`occurred_at` / `reported_at` / retroactive columns exist anywhere in `app/`.
The implementation therefore already matches this decision — **no code change is
implied**.

### Governance note

This is a **business decision by HBA**. It resolves the substance of the open item
"emergency retroactive timestamp convention". Formal closure of that register entry
is a **separate authorized documentation step** and is not performed by this record.

---

## DECISION 3 — DEPLOYMENT OPERATIONAL CONTEXT

**HBA decision: DEFERRED to a future version. V1 target is the NUC. Prepare the
security option now so a future version does not require major rework.**

### What HBA stated

- This version will run on the **NUC**.
- Accessible **locally and online**.
- A subdomain `crm.benshi.my.id` is intended — feasibility questioned.
- Security intent for the future:
  - **Backend** reachable **only** via local network or Tailscale.
  - **General application** usable from anywhere.
  - **Admin** users reachable **only** via Tailscale / local.
- Record only; belongs to the next version, so V1 scope does not widen.
- However, the option may be **prepared now** to avoid a large overhaul later.

### Feasibility finding — `crm.benshi.my.id`

**YES — technically possible, and low effort.** Verified on this host:

| Fact | Verified value |
|---|---|
| Host | `anto-NUC7i3BNHXF` |
| LAN address | `192.168.30.12` |
| Tailscale address | `100.72.199.61` |
| DNS nameservers for `benshi.my.id` | `hunts.ns.cloudflare.com`, `molly.ns.cloudflare.com` (Cloudflare-managed) |
| Cloudflare Tunnel | Running — tunnel `home`, ID `a4fb6a23-5057-4d1c-8a56-0dfd742e1cdd`, service `cloudflared.service` |
| Existing tunnel hostnames | `ha.`, `opencode.`, `n8n.`, `hermes.`, `p4997fddf.` |
| Reverse proxy (nginx/caddy/traefik) | None installed |
| Cloudflare Access | Not currently applied to any hostname |

Because DNS is already Cloudflare-managed and the tunnel is already running,
publishing `crm.benshi.my.id` requires only a DNS route plus one ingress entry —
the same pattern already used for the four existing hostnames. No new
infrastructure is needed.

### Preparation option — recommended shape (design only, not implemented)

The stated security intent is achievable **without Cloudflare Access at all**, by
never exposing the backend through the tunnel:

| Layer | Measure | Satisfies |
|---|---|---|
| 1. Listener separation | Application listens on one port; admin/backend listens on a **different** port bound to `127.0.0.1` and the Tailscale address only | Backend unreachable from the internet regardless of app bugs |
| 2. Tunnel ingress | Only the **application** port is published in the tunnel ingress; the admin port is **absent** from ingress | Admin simply not routable from outside |
| 3. Optional edge control | If admin must be reachable online, protect it with Cloudflare Access instead of relying on network position | Defence in depth |

The key architectural point for "prepare now": **design the app as two separately
bound listeners from the start**, so the split is a configuration change later
rather than a restructuring.

### Not decided by this record

Hosting topology, database product, runtime, backup policy, monitoring, and the
Accurate 5 integration boundary remain **open**. This record does not select them.

---

## WHAT THIS RECORD DOES NOT DO

- Does not modify any canonical document.
- Does not create or modify a business rule beyond the HBA statements above.
- Does not create a new decision identifier, role, actor, lifecycle state, or SLA.
- Does not write code, schema, migration, or deployment configuration.
- Does not close any register entry formally.
- Does not authorize implementation of the deferred items.

---

## WHAT REQUIRES FURTHER HBA AUTHORIZATION

| Item | Nature |
|---|---|
| Materializing Decision 2 into `DECISION_REGISTER.md` and the affected IS documents | Canonical documentation change |
| Formally closing the retroactive-timestamp register entry | Canonical documentation change |
| Assigning formal identifiers to the deferred items (if HBA wants them) | Governance decision |
| Implementing the reminder direction | Future-version build authorization |
| Deploying to the NUC / publishing `crm.benshi.my.id` | Deployment authorization |
| Preparing the two-listener security split in code | Build authorization |

---

## EVIDENCE BASIS

All technical facts in this record were verified directly on the host on 2026-10-01:

- `hostname`, `hostname -I`, `tailscale status`, `tailscale ip -4`
- `cat ~/.cloudflared/config.yml`, `cloudflared tunnel list`
- `systemctl --user list-units` (cloudflared service active/running)
- `ss -tlnp` (no reverse proxy listening)
- `dig +short NS benshi.my.id`, `dig +short crm.benshi.my.id` (no record yet)
- `docker ps` (no CRM container; CRM not yet deployed)
- Source inspection of `app/reporting/reminder.py`, `app/wo/emergency.py`,
  `app/migrations/migrate.py` (timestamp columns)

---

*End of record. Decisions are HBA's; this document only records them.*
