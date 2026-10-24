# G1-D ACCEPTANCE AND CONTROL ADOPTION RECORD

**Status:** GOVERNANCE / AUDIT RECORD — **recorded, not created.** This file records Human Business
Authority decisions already taken; it adds no business rule, no permission, no role, no control and no
implementation authority of its own.

**Recorded:** 2026-09-26 (WIB) · **Decision source:** Human Business Authority message
"G1-D ACCEPTANCE & GOVERNANCE DECISIONS" (2026-09-26), answering
`G1-D-HBA-DECISION-PACKAGE.md` (items D-1 … D-6).
**Materialized records in this round:** `docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md`
(D-1, D-2) · this record (D-2 record, D-3, D-4, D-5, D-6).
**Implementation Authorization: NO** — coding, schema, migration, API, UI, MCP and deployment remain
unauthorized.

---

## 1. Decisions recorded

| Item | Decision | Recorded effect |
|---|---|---|
| **D-1** | **APPROVED** — HD-4 and its applicable control decisions are materialized into canonical governance documentation | `docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md` (§4 envelope controls, §12 result contract). Materialization is documentation/governance work only: no reinterpretation, no authority expansion, no invented control, no change to demonstrated enforcement behaviour, no change to CRM rules, `CD-11`, architecture or implementation authorization |
| **D-2** | **APPROVED** — canonical location for HD-1 / HD-4 decision records is `docs/10-DECISIONS/` | **SD-8 resolved.** No folder was created, no tree restructured, no unrelated document moved |
| **D-3** | **APPROVED — OPTION (A) ONLY** — verbatim-passing policy | Policy text in §2 below; clause added to the governed Manager definition; **hash-binding NOT AUTHORIZED** in any form |
| **D-4** | **ADOPTED** — RC-1 and RC-3 as standing controls within the G1-D demonstrated scope | §3 below; no expansion beyond the demonstrated scope, no architecture redesign |
| **D-5** | **ACCEPT** — `G1-D VERIFIED WITH DECLARED FRESHNESS LIMITATIONS` | §4 below, including the mandatory qualification and the two limitations, verbatim and visibly |
| **D-6** | **APPROVED WITH STRICT SCOPE LIMITATION** — `mitrasp-falsifier` as standing second audit worker | §5 below, including the explicit no-authority list |

---

## 2. D-3 — Delegation-envelope authorship policy (recorded verbatim)

> The Manager must pass the delegation envelope verbatim as authored. The Manager must not silently add,
> complete, repair, infer, or substitute missing delegation controls before the governed enforcement
> boundary.

A missing required control must remain missing and must therefore be rejected by the governed enforcement
boundary. This closes the governance-policy gap identified as **RF-G1D-01** at the policy level.

**Hash-binding is NOT AUTHORIZED.** No envelope hash issuance, hash publication, hash comparison,
hash-bound acceptance, Hermes-side envelope plumbing, or any other D-3 option (c) implementation is
authorized. It remains a separate future decision and authorization item.

*Execution-layer record:* the policy clause was added to `.opencode/agent/mitrasp-manager.md`
(see §7). The policy is a duty on the Manager; it is stated as a duty, not as a demonstrated machine
control, and it does not replace the envelope validation at the governed boundary.

---

## 3. D-4 — Adopted controls (RC-1, RC-3)

**RC-1 — exactly-one-definition rule.** Duplicate envelope-control definitions are rejected; a governed
delegation carries exactly one effective definition of each required control.

**RC-3 — machine-enforced schema completeness.** The required finding/output schema is machine-enforced;
missing required fields are malformed; `null` is valid where the schema permits it; malformed output
cannot become a successful governed result.

Adoption scope is exactly the scope demonstrated in the G1-D phase (live rejection of a duplicated
control; live admission of results carrying the full finding schema; deterministic batteries over the
same module). These controls are not expanded beyond that scope, and the control architecture is not
redesigned as part of this adoption. Both controls are documented in
`docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md` §2/§3.

---

## 4. D-5 — G1-D acceptance, and the mandatory qualification

**Accepted phase verdict:**

```text
G1-D VERIFIED WITH DECLARED FRESHNESS LIMITATIONS
```

The verdict is **not** downgraded to UNVERIFIED solely because the two limitations exist, and the
limitations are **not** erased, minimized or described as equivalent to fresh live evidence.

**Mandatory qualification — two criteria do not have fresh same-phase live negative-event evidence:**

1. **Malformed-worker/output rejection direction.** The rejection of a malformed worker/output artifact
   was **not** freshly demonstrated live during G1-D. Five malformation vectors were submitted on the
   real path and both governed workers refused each of them, returning schema-conformant results; the
   rejection direction therefore relies on **current deterministic module evidence** (the battery over
   the same module file) plus a **prior live rejection on the same code path** (previous phase).
2. **Fail-closed behaviour.** The fail-closed guard was **not** deliberately re-broken in this phase,
   because the destructive probe was not authorized. Its freshness therefore rests on unchanged guard
   code plus its earlier verification.

**Recorded constraints on the interpretation of this acceptance:**

- Do **not** claim those two negative events were freshly demonstrated live during G1-D.
- The deterministic battery is **regression protection, not a substitute for fresh live evidence**.
- If future changes affect the relevant control path, the earlier evidence must be revalidated as
  appropriate.

*Evidence basis:* `AUTONOMOUS-AUDIT-G1-D-REPORT.md` §4/§9 and `AUTONOMOUS-AUDIT-G1-D-EVIDENCE.md` §4/§5
(non-canonical bridge workspace; historical phase records, not rewritten by this round).

---

## 5. D-6 — Standing role of `mitrasp-falsifier` (strict scope limitation)

Approved as the standing second audit worker **for**: independent audit perspective; falsification-oriented
review; conflict testing; evidence challenge; independent audit reasoning.

It is **NOT** a second Manager and **NOT** an authority center. It has **NO**: approval authority; closure
authority; dispatch authority; remediation authority; implementation authority; governance-authority
promotion; subdelegation authority; self-escalation authority. It remains a governed worker, and
`task: deny` / equivalent no-subdelegation enforcement must remain intact. Its standing purpose is
**audit independence only**.

*Execution-layer record:* the scope limitation is stated in the worker definition's canonical-citation
block (see §7); its permission block remains `edit: deny`, `bash: deny`, `task: deny`.

---

## 6. Execution boundary applied, and what was deliberately not implemented

**Performed under this decision (execution boundary items 1–9):** HD-4 materialized (§1 D-1); the
location decision recorded (§1 D-2); traceable citations added to the execution-layer definitions (§7);
the D-3 policy recorded (§2) and added to the Manager definition; RC-1/RC-3 adoption recorded (§3); the
G1-D acceptance recorded with the verdict line and the two limitations (§4); the scoped standing role of
`mitrasp-falsifier` recorded (§5); register rows updated (§8).

**Deliberately NOT implemented (prohibited actions, and items outside the boundary):**

- hash-binding (issuance, publication, comparison, acceptance, plumbing) — **NOT AUTHORIZED**;
- no CRM application code, schema, migration, API, or production UI was touched;
- MCP was not enabled, contacted, or reconfigured;
- no deployment;
- no unrelated remediation;
- no governance-folder restructuring (no `docs/60/70/80-GOVERNANCE/` created);
- no historical G1 / G1.1 / G1.2 / G1-D evidence was rewritten, and no prior finding was deleted or
  altered; no historical verdict was altered;
- no fresh evidence was manufactured and no regression evidence was converted into live-event evidence;
- `RR-1` and `RR-4` were **not** closed; `BRIDGE_CONTRACT.md` final acceptance was **not** inferred;
- no PROPOSED material was silently promoted to LOCKED beyond the decisions stated above.

---

## 7. Change set (execution-layer citations) and digests

All digests below were obtained **programmatically** from the files in this round.

| File | Change | Digest (sha256) |
|---|---|---|
| `docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md` | **created** — canonical HD-4 authority record (D-1, D-2) | `2545ae87ddbe99f4cb155b3805d7f07aa9e17be3bda87747f94749cae5cdb4c7` (159 lines, 11,186 B) |
| `.opencode/agent/mitrasp-auditor.md` | citation added to the canonical HD-4 record | `c08fba0cf85fe836dbf520a9011cd8e3c263c32a5ea0ad3b24df73a1fb3699fd` (6,323 B) — was `535ee9ff7b77c290299a289b4c3e86446e392fd3e1394c5c07f5909beab340bd` |
| `.opencode/agent/mitrasp-falsifier.md` | citation + D-6 scope limitation stated | `b1448cf64903bf6ce3c7b87e5857f81a321b3bfb5efa0fdffeda5fe6ee4b26d3` (6,445 B) — was `f6c960840e88b19e5cf7df5f64beb5fdf31148ff922adad7f82c2d78c636b424` |
| `.opencode/agent/mitrasp-manager.md` | D-3 verbatim-passing clause + canonical citations | `9920b6144cb7b9c3db871c3cf572c6d8aee900951b06041860d9b749474f7900` (6,712 B) — was `1e48095157d8a99921b6fe7d11eceee439970ba8fa8d2f19ac9da98a3e596b62` |
| `.opencode/plugin/mitrasp-governance-gate.js` | **unchanged** (no behaviour change authorized or made) | `46849812003b833e9c170f97e8a5e1d10e126103c8e9a3325947d5f906356cf8` (19,401 B) |
| `.opencode/bin/opencode-governed` | **unchanged** | `52fa5c2c365dc8d6f84b7b6d91bcc339a38e7cb61fc2ba4a4b59903628434092` (6,096 B) |
| `DECISION_REGISTER.md` | rows added (§8) | see the register's own updated state |

**Files intentionally unchanged:** every `CD-*` and `BD-*` decision file; `CD-11` and both appendices;
`AI_GOVERNANCE_CANONICAL.md`; `AI_OPERATING_RULES.md`; `AI_CONTEXT_INDEX.md`; `ARCHITECTURE_LOCK.md`;
`BRIDGE_CONTRACT.md`; `opencode.json`; `docs/90-AUDIT/00-INDEX.md` and the materialization registers
(stage records — not refreshed); all historical G1/G1.1/G1.2/G1-D artifacts; the ledger; all CRM
application files.

---

## 8. Register and index

`DECISION_REGISTER.md` gained: a row for `HD-4` (canonical source = the new decision record; note that the
materialization records an already-decided control set and authorizes no implementation), and a row for
this acceptance record under the "recorded, not created" convention, carrying the D-5 verdict line and the
explicit statement that the acceptance implies no CRM/schema/API/migration/UI/MCP implementation
authorization, no autonomous remediation, no Bridge Contract final acceptance and no hash-binding
authorization.

`docs/90-AUDIT/00-INDEX.md` was **not** refreshed: it declares itself a materialization-stage record
(2026-09-18) listing that stage's canonical files, and refreshing a stage record destroys audit evidence;
the precedent in this family is that new audit records are added as new files. Recorded here so the
omission is deliberate, not an oversight.

---

## 9. Remaining OPEN / PENDING items (preserved, not closed)

| Item | Status |
|---|---|
| `RR-1` — whether the raw `opencode run` path may still be used | **OPEN** (not closed) |
| `RR-4` — live exercise of the `governed_sha256` refusal path | **OPEN** (no claim that it was demonstrated) |
| `BRIDGE_CONTRACT.md` — final acceptance | **PENDING** (not inferred from G1-D acceptance) |
| `RC-01` … `RC-06` — residual design-package items | **PROPOSED / UNTOUCHED** |
| Envelope hash-binding | **NOT AUTHORIZED** (future decision item) |
| `HD-1` record materialization | **OPEN** — location decided (D-2); the record itself was not authorized in this round and is not reconstructed |
| `RF-G1D-01` upstream envelope completion | **policy gap closed at policy level (D-3)**; machine enforcement is not authorized |
| `RF-G1D-02` … `RF-G1D-09` (G1-D residual findings) | **reported, not remediated** (remediation not authorized) |
| MCP | **unchanged** — no server enabled, contacted or reconfigured; `opencode.json` unmodified |

## 10. Provenance statement

For every artifact changed above, the record preserves: what existed before (previous digest), what this
HBA decision authorizes, what changed, why, which decision item authorized it, the evidence reference, and
the resulting digest. No digest in this record was typed from memory; each was read from the file. This
record itself creates no decision, rule or authority — it is a faithful record of decisions taken by the
Human Business Authority, and where it is silent, existing canonical governance remains in force.

*End of G1-D acceptance and control adoption record.*
