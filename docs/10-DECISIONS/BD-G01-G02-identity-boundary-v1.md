# BD-G01-G02 — Identity Boundary: Requester ↔ Contact/PIC ↔ Company ↔ Verified PIC (PROPOSAL)

```text
Decision ID: BD-G01-G02
Title: Identity Boundary for Unverified Requesters + Individual Customers
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — BA DECISION G-01/G-02 Identity Boundary LOCK V1, 2026-09-23)
Implementation Authorization: NO
```

> BA-approved identity boundary for G-01/G-02. Investigation closed. O-10 unblocked
> (see BD-SR-010). Historical documents are untouched. G-02 external verification/
> access stays FUTURE (see §9 below). Requester is a domain concept on SR, never an
> automatic database entity (see §3 below).

> Investigation proposal for gaps G-01/G-02 found during O-10 finalization. Changes
> nothing canonical. Must not be registered as LOCKED before BA approval. O-10 stays
> NOT LOCKED until the identity boundary is resolved:
> **O-10 can be locked only after BA resolves the identity boundary.**

---

## 1. Findings (from canonical docs)

- F-01. Contact/PIC is a separate entity, Company-child 1-N, identity-level, usable
  across roles (CD-03 §Contact; Consequences). No UNVERIFIED/intake state exists; no
  company-less Contact exists.
- F-02. Access chain is Google Identity → Contact/PIC → Verified PIC Link → Company,
  per-company VERIFIED/PENDING/REVOKED, no cross-company grant; link entity separate
  from Contact; applicant ≠ approver; Manager/Admin approval establishes the link;
  PENDING is entered via PIC registration application (LOCKED human decision;
  TADR-13 §§Dependencies, Security).
- F-03. The chain's entry anchor is an authenticated Google Identity. A phoned-in /
  walk-in intake requester has no anchor and therefore cannot occupy any position in
  the chain until they authenticate and apply. No canonical bypass exists.
- F-04. Company is the single identity root (CD-03). No individual-customer identity
  model exists anywhere. BA-validated company-less individuals are therefore a genuine
  architectural gap (G-02), not a reading dispute.
- F-05. No document contradicts another on these points. No real conflict found.
- F-06. Audit principles already cover what history preservation needs (actor, server
  timestamp, action, object, reason, before/after; link lifecycle events are first-class
  audit events — TADR-13 §Audit; CD-11 §28): point-in-time status is derivable from
  event ordering provided verification/promotion is recorded as events on a stable
  identity pointer — no snapshot mechanism required.

## 2. Existing architecture (textual)

```text
Google Identity
      ↓  (external auth; sign-up alone grants nothing)
Contact/PIC ── under exactly one Company (1-N, CD-03)
      ↓  (separate link entity, TADR-13)
Verified PIC Link [VERIFIED / PENDING / REVOKED] per Company
      ↓  (SOLE basis of Company-level access)
Company  (+ Units, histories, COMPANY_SCOPE portal)
```

Requester's current position: **outside the graph** — an intake-time name/claim with
no canonical home. That is G-01.

## 3. G-01 analysis — Pertanyaan A (Joko claims PT XYZ, unknown, unverified)

- Joko MAY be Requester and MAY be recorded in SR — as intake data (name + channel +
  claimed company as plain claimed context).
- `Company = PT XYZ` as a **relationship must stay NULL** until verification. Writing
  the claim into the Company association would be semantically indistinguishable from
  membership ("Joko adalah Contact PT XYZ") — the Claim ≠ Relationship violation.
- No Company Detail, no unit views, no history, no Verified PIC Link flows from the
  claim. Link only via the standard path: authenticate → PIC application (PENDING) →
  Manager/Admin approval (applicant ≠ approver) → VERIFIED.
- Governing line: **claimed context vs verified relationship** — the first lives in
  SR intake data, the second lives only in Contact + Link.

## 4. G-02 analysis — individual customer (Andi, no Company)

- Andi MAY be Requester; the SR is valid with Company = NULL (BA-locked concept,
  O-10 revised §6).
- Andi's identity has no canonical home (F-04): not a Contact (needs a Company
  parent), not linkable (Link is per-company). Storing Andi as a Contact under a
  fabricated/company-by-default record is prohibited (no fake Company — O-10 §6).
- External access for Andi has no mechanism: COMPANY_SCOPE is per-company by locked
  definition. Two options: (A) verify identity without Company (new concept —
  architectural change, needs BA + access-model amendment); (B) no external access
  for company-less individuals in V1 (they remain UNVERIFIED requesters, fully
  servable through the internal SR → WO flow, history preserved).
- WO for Andi MUST be possible (BA requirement): WO formation depends on internal
  authorization (O-06), never on requester verification — satisfiable today.

## 5. Scenario matrix

| Case | Requester | Company | Verification | External Access | SR | WO |
|---|---|---|---|---|---|---|
| A existing verified PIC | Budi (VERIFIED Contact) | PT XYZ (relationship) | VERIFIED | Existing governance (no SR exposure V1) | Valid; Created By = recorder | Normal governance |
| B new person claiming Company | Joko (UNVERIFIED intake) | NULL relationship; "PT XYZ" as claimed context only | UNVERIFIED | None | Valid; follow-up yes | Only after separate authorization |
| C individual | Andi (UNVERIFIED intake) | NULL | UNVERIFIED (no path in V1 — G-02) | None in V1 | Valid | Possible via internal authority |
| D technician source | Technician (internal) | Known/unknown | N/A (internal role) | Internal role | Valid | Governance (requester status grants nothing) |
| E manager instruction | Customer person (any state) | As known/NULL | Any | Not relevant | Valid; Created By = instructed user | Governance |
| F UNVERIFIED → VERIFIED | Same identity pointer, state changes by event | Relationship established at verification | Transition via Manager approval + evidence | Governance applies only after VERIFIED | History preserved (events ordered, nothing rewritten) | Normal |
| G UNVERIFIED tries access | Joko | Claimed PT XYZ | UNVERIFIED | DENIED (claims are not credentials) | No external access | No authority |
| H non-representative | Whoever reported | Any | FAILED/UNVERIFIED | DENIED | Request remains valid | Separate authorization required |
| I duplicate discovered (Joko = existing Contact) | Link, never duplicate | — | Manager manual link | — | History untouched | — |

## 6. Architecture options

**Option A — intake-scoped requester + link-at-verification (RECOMMENDED).**
Requester = SR-scoped intake data (name, channel, claimed-company-as-text). No Contact
created at intake (no accidental membership). Verification travels only the existing
chain; if no Contact exists, the Manager creates/links it as part of the governed
verification action. Promotion = Manager-recorded link between the SR requester entry
and the Contact (new link event, never an edit of history). Dedup = human Manager
check at promotion time (search-then-link); never automatic; old records never deleted.

**Option B — extend Contact with UNVERIFIED/intake state (± NULL/claimed Company).**
Rejected: rewrites CD-03 parentage semantics; a Contact row carrying "PT XYZ" reads as
membership to every consumer (reports, history, future access code) regardless of a
state flag; Company-NULL contacts fracture the identity-root model; every access
consumer must learn the new flag or risk leakage. Larger blast radius for zero V1 gain.

**Option C — per-channel/external requester registry.** Rejected outright: recreates
the per-channel entities BA already prohibited and duplicates Contact under a new name.

## 7. Impact matrix

| Area | Option A (recommended) | Option B | Option C |
|---|---|---|---|
| Domain clarity | Requester/Contact/Link/Company stay distinct (§21 principle intact) | Blurs Contact into intake staging | Duplicates identity domain |
| Duplicate prevention | Human link-time check + never-delete; no silent dupes | Flag-dependent; dupes hide behind state | Registry↔Contact sync problem created |
| Security | Claims confer nothing; access only via existing chain | Membership-looking rows exist pre-verification (leakage surface) | Second identity store to guard |
| Audit/history | Events ordered on stable pointer; §13 satisfied | State rewrites risk history ambiguity | Cross-store lineage required |
| Individual customer | Servable now (NULL company, UNVERIFIED); access deferred cleanly | Still needs NULL-company Contact (same gap, worse) | Same gap, new store |
| Company claim | Text context, zero semantics | Relationship-looking row | Text context, zero semantics |
| External access | Unchanged chain | Chain must learn new state | Second chain or bridge |
| Database complexity | Intake columns on SR + link event (minimal) | Contact state machine + nullable parent + claimed field | New entity + sync |
| Migration risk | Negligible | Existing Contact consumers affected | New store migration |
| V1 implementation impact | Smallest: intake fields + Manager link action | Medium: model + consumer changes | Largest |

## 8. Risks (largest per option)

- A: intake-name collision (two "Joko"s) — mitigated by channel/contact detail on the
  entry + human dedup at link time; residual risk accepted, no auto-merge ever.
- B: accidental Company membership read-off (reports/access treating UNVERIFIED rows
  as members); impersonation via claimed-company rows; history ambiguity on state flips.
- C: registry drift, sync bugs, and a second access-governance surface.

Cross-cutting risks (all options, controlled by LOCKED rules): impersonation and false
claims (no access flows from claims); self-verification/self-approval (applicant ≠
approver, TADR-13); privilege escalation via verification (verification grants access
only, never WO authority); history rewriting (prohibited; §13 test must hold).

## 9. Recommendation (NOT a lock)

Adopt **Option A**: (1) Requester stays SR-scoped intake data; Company relationship
NULL until verification; claims recorded as text context only. (2) Verification only
through the existing chain (authenticate → apply PENDING → Manager/Admin approval →
VERIFIED link); Manager creates/links Contact where missing as part of that action.
(3) Promotion = new link event; dedup human-only; never delete; never auto-merge.
(4) G-02 V1: company-less individuals servable end-to-end as UNVERIFIED requesters
with no external access; identity-without-Company verification deferred as an explicit
architecture question. Rationale: only option with zero canonical-model changes,
smallest V1 footprint, clean COMPANY_SCOPE preservation, and §13 history test passing.

## 10. BA Decision Required

**Mandatory (O-10 cannot lock without these):**
1. Approve/reject Option A (intake-scoped requester + link-at-verification), including
   the rule "Company relationship NULL until verification; claims as text only".
2. Approve/reject G-02 V1 posture: individuals servable without Company and without
   external access, with identity-without-Company verification deferred.
3. Approve promotion mechanics: Manager human action, manual dedup, no auto-merge,
   no deletion, verification-as-event history.

**Deferrable:** Company-record-for-individual design; dedup tooling/search UX;
external access for individuals; V2 channel identity.

**Already canonical (no decision needed):** the chain and its states; applicant ≠
approver; claims confer nothing; verification grants access only, never WO authority;
history preservation principles.

*End of proposal. O-10 stays NOT LOCKED. O-10 can be locked only after BA resolves
the identity boundary.*

---

## BA Lock record (2026-09-23 — LOCKED V1, supersedes PROPOSED status above)

BA approved Option A (intake-scoped requester + link-at-verification) with the
following locked additions, all consistent with the investigation (§§1–10 verified
conflict-free against O-01…O-07, CD-03, CD-11, Verified PIC governance):

1. **Requester ≠ new entity automatically.** Requester is a domain concept /
   information on SR, not an automatic `requesters` table, identity registry,
   generic person/contact entity, EAV, or JSON store. Dedicated data structures, if
   ever needed, are a separate technical design proposal — never auto-locked here.
2. **Company field rules (V1):** existing verified relationship → Company filled per
   that relationship; new/unverified claim → relationship NULL, claim in intake
   narrative only (BD-SR-003 boundary); individual → NULL. No fake Company for any
   reason (avoiding NULL, Contact parentage, access model, or storing claims).
3. **O-10 consequence:** Requester REQUIRED; Company OPTIONAL/NULL-valid; create guard
   `Requester AND (Need OR Scope)`, Company not required (see BD-SR-010).
4. **O-05 consequence:** none — requester status grants zero authorization; matrix
   unchanged.
5. **WO consequence:** none — individual SR/NULL-company WO permitted under existing
   governance; requester verification is not a universal WO prerequisite.
6. **G-02 FUTURE (NOT LOCKED):** how a company-less individual may be verified and/or
   gain external access safely — V2 or later. No individual portal, individual
   Verified Link, new access scope, or new identity root in V1.
7. V2 multi-channel note stays FUTURE / NOT LOCKED; nothing in this lock activates
   any channel.

*End of BA lock record. BD-G01-G02 is LOCKED — V1.*
