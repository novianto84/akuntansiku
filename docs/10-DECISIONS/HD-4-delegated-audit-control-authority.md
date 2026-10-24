# HD-4 — Delegated Audit Control Authority (Governed Worker Delegation)

```text
Decision ID: HD-4
Title: Delegated Audit Control Authority — governed delegation envelope (§4) + audit result contract (§12)
Mode: Governance Documentation — materialization of an already-decided control set
Status: CANONICAL (recorded, not created) — materialized 2026-09-26
Authority: HUMAN BUSINESS AUTHORITY — materialization decision D-1 (2026-09-26)
Canonical location: docs/10-DECISIONS/ — location decision D-2 (2026-09-26), resolves SD-8
Implementation Authorization: NO
```

> This record materializes the delegation/audit control set already decided by the Human Business
> Authority and already enforced on the governed execution path, so that a future auditor can trace the
> enforcement duty to an authoritative governance record instead of to execution-layer worker
> definitions. It documents; it creates no control, no role, no permission, and no implementation
> authority. Nothing in it reinterprets HD-4, expands its authority, or invents a control.

---

## 1. Scope

1.1 **In scope (the governed boundary).** Delegations reaching the governed execution path — i.e. an
invocation of `.opencode/bin/opencode-governed` dispatching the native Task tool to a governed worker.
Two control planes apply there: the **delegation envelope** (§2) and the **audit result contract** (§3).

1.2 **Which workers the result contract binds.** `mitrasp-auditor` and `mitrasp-falsifier` (the governed
audit workers), plus any delegation whose envelope declares `output_schema: HD-4 §12`. The
`mitrasp-programmer` result contract is not defined by HD-4.

1.3 **Out of scope (expressly).** CRM business rules, CRM schema, API, UI, migrations; the business
lifecycles in `CD-11`; the LOCKED role model; and ordinary, non-governed delegations. HD-4 imposes no
envelope template on trivial or non-governed tasks: `AI_OPERATING_RULES.md` §10A (*"sufficient context,
minimum necessary process"*; do not require rigid templates for trivial tasks) remains in force for
those, and no conflict exists because the envelope is a control on the *governed audit* boundary only.

1.4 **Relationship to existing canonical rules.** This record operationalizes, for the governed audit
boundary: `AI_GOVERNANCE_CANONICAL.md` §1.2/§1.4 (one AI Manager; independent auditor judgement) and
§8 (audit invocation/enforcement is a governance concern, not a reason for another management role);
`AI_OPERATING_RULES.md` §1 (authority model), §10A (delegation context), §10B (reconciliation of
specialist output — findings are reconciled, never auto-accepted), §14 (auditability).

---

## 2. Delegation envelope — the twelve required controls (HD-4 §4)

A governed delegation carries **exactly one envelope** with all twelve controls. A missing control makes
the delegation invalid: the governed enforcement boundary rejects it **before any worker executes**, and
a worker that nevertheless receives such a delegation must refuse and STOP.

| # | Control | Enforced handling |
|---|---|---|
| 1 | `worker_identity` | present; must equal the dispatched worker identity; the worker definition must exist |
| 2 | `task_id` | present; recorded in every ledger entry |
| 3 | `parent_execution_id` | present; links the delegation to its parent execution |
| 4 | `target_scope` | present (the artifact/area the delegation may read) |
| 5 | `allowed_actions` | present; the worker's *granted* capability set is separately bound by its definition permissions |
| 6 | `prohibited_actions` | present; the runtime permission denies apply in addition |
| 7 | `authorization_state` | present and non-empty |
| 8 | `evidence_requirement` | present (the contract's alternative spelling `evidence_requirements` is accepted and the spelling seen is recorded — documentation alignment remains an open item) |
| 9 | `output_schema` | present; it is also the trigger for the §3 result gate |
| 10 | `no_subdelegation` | must be `TRUE` — a governed delegation may not sub-delegate |
| 11 | `remediation_authority` | must be `FALSE` — an audit delegation carries no remediation authority |
| 12 | `dispatch_authority` | must be `FALSE` — an audit delegation carries no dispatch authority |

**RC-1 (exactly-one-definition rule, adopted 2026-09-26).** A delegation that defines any required control
more than once is rejected: a governed delegation carries exactly one effective definition of each
required control. A duplicated control is treated as an attempt to widen the envelope, not as a
harmless repetition.

**Verbatim-passing duty (HBA decision D-3, 2026-09-26).**

> The Manager must pass the delegation envelope verbatim as authored. The Manager must not silently add,
> complete, repair, infer, or substitute missing delegation controls before the governed enforcement
> boundary.

A missing required control must remain missing and must therefore be rejected by the governed enforcement
boundary. **Envelope hash-binding (issuance, publication, comparison, hash-bound acceptance, or any
Hermes-side envelope plumbing) is NOT AUTHORIZED.** It remains a separate future decision.

---

## 3. Audit result contract (HD-4 §12)

A governed audit result is **exactly one JSON object** carrying the 13 top-level fields, each entry of
`findings[]` carrying all 15 fields, and `execution_status` drawn from one fixed vocabulary.

```text
Top-level (13): worker_identity, task_id, parent_execution_id, execution_status, scope,
                authorization_state, started_at, completed_at, findings[], evidence[],
                limitations[], undeclared_scope[], prohibited_action_attempts[]
execution_status: COMPLETED | COMPLETED_WITH_LIMITATIONS | STOP | FAILURE | INVALID_OUTPUT
findings[] (15): finding_id, severity, claim, canonical_source, conflict_type, evidence, impact,
                 recommended_action, remediation_authority_required, prohibited_action_attempted,
                 finding_status, required_human_decision, timestamp, scope_checked, applies_to
```

**Mandatory properties.** The four array fields are always arrays (empty is valid, absent is not). A
missing required field is **malformed**; an explicit `null` is valid where the schema permits it, and the
gap must be recorded in `limitations[]`. A worker may not be required to guess a value.

**RC-3 (machine-enforced completeness, adopted 2026-09-26).** Required finding/output schema is enforced
by the governed path; malformed output cannot become a successful governed result. A non-conformant
result is replaced by `FAILURE / INVALID_OUTPUT`, the raw result is preserved as evidence, and **no field
is filled in, repaired or normalised** by any party.

---

## 4. Enforcement points and evidence

| Point | Mechanism | Evidence |
|---|---|---|
| Envelope admission | gate hook on the Task tool, `tool.execute.before` — refusal blocks the worker from ever starting | append-only ledger `ENVELOPE_ACCEPTED` / `ENVELOPE_REJECTED` with the controls seen/missing, the violated invariants, `execution_proceeded: false` and the reason list |
| Result admission | gate hook `tool.execute.after` — non-conformant results replaced, raw preserved | ledger `RESULT_ACCEPTED` / `RESULT_INVALID_OUTPUT`; raw results under `.opencode/ledger/raw/` |
| Identity / no-fallback | launcher guard: explicit agent required, `mode: primary` required, definition must exist, executed identity verified against the requested one; fail-closed heartbeat (no gate initialisation ⇒ invocation refused, classified UNGOVERNED) | ledger `LAUNCHER_*` records |
| Worker-side duty (defence in depth) | the worker definitions state the same duties; a worker that receives a defective envelope refuses and STOPs | worker definitions; worker results |
| Read-only hashing | in-process `governed_sha256` (no shell, workspace-bounded, secret-path-refusing) | ledger `HASH_PRIMITIVE_USED` |

**Ledger.** Enforcement is recorded in an append-only JSONL ledger outside the product code; enforcement
claims are read from it, never from prose.

---

## 5. What this record does NOT do

- It creates no control, role, permission, status, lifecycle, business rule, or approval.
- It grants no implementation authorization: coding, schema, migration, API, UI, MCP and deployment
  remain **NOT AUTHORIZED**.
- It does not amend `CD-01`…`CD-11`, any `BD-*` decision, `AI_GOVERNANCE_CANONICAL.md`,
  `AI_OPERATING_RULES.md`, `ARCHITECTURE_LOCK.md`, or `BRIDGE_CONTRACT.md`.
- It does not alter the enforcement behaviour of the governed path; the behaviour was implemented and
  verified in the G1.2/G1-D phases and is recorded as found.
- It does not close `RR-1` (raw `opencode run` path) or `RR-4` (live exercise of the `governed_sha256`
  refusal path); both remain OPEN.
- It does not finalize `BRIDGE_CONTRACT.md`; that acceptance remains PENDING.

---

## 6. Provenance

| Item | Source |
|---|---|
| Control set decided | Human Business Authority directives of 2026-09-26 (governance-control remediation and revalidation authorizations), recorded in `docs/90-AUDIT/G1-D-ACCEPTANCE-AND-CONTROL-ADOPTION-RECORD.md` (decision items D-1…D-6) |
| Control set as enforced (verified by direct extraction) | `.opencode/plugin/mitrasp-governance-gate.js` sha256 `46849812003b833e9c170f97e8a5e1d10e126103c8e9a3325947d5f906356cf8` (19,401 B) — `REQUIRED_CONTROLS` (12), `SCHEMA_FIELDS` (13), `FINDING_CORE` (15), `VALID_STATUS` (5) |
| Entry-point / identity policy holder | `.opencode/bin/opencode-governed` sha256 `52fa5c2c365dc8d6f84b7b6d91bcc339a38e7cb61fc2ba4a4b59903628434092` (6,096 B) |
| Execution-layer citations (this materialization) | `.opencode/agent/mitrasp-auditor.md` sha256 `c08fba0cf85fe836dbf520a9011cd8e3c263c32a5ea0ad3b24df73a1fb3699fd` (6,323 B) · `.opencode/agent/mitrasp-falsifier.md` sha256 `b1448cf64903bf6ce3c7b87e5857f81a321b3bfb5efa0fdffeda5fe6ee4b26d3` (6,445 B) · `.opencode/agent/mitrasp-manager.md` sha256 `9920b6144cb7b9c3db871c3cf572c6d8aee900951b06041860d9b749474f7900` (6,712 B) |
| Verification evidence | `.opencode/ledger/governance-gate.jsonl` (99 records at materialization time) + preserved raw results; phase evidence in the G1/G1.1/G1.2/G1-D execution records |
| All digests above | obtained programmatically from the files at materialization time (no digest in this record was typed from memory) |

**Related status.** `HD-1`: its canonical location is decided by D-2 (`docs/10-DECISIONS/`), but no HD-1
record is materialized by this execution — that materialization was not authorized here, and its
substance currently exists only in `AI_GOVERNANCE_CANONICAL.md` and the decision history; it is reported
as an OPEN item, not reconstructed. `SD-8` is resolved by D-2 (location). `RC-1`/`RC-3` adoption is
recorded in `docs/90-AUDIT/G1-D-ACCEPTANCE-AND-CONTROL-ADOPTION-RECORD.md`. The SD-3 traceability
artifact (`HD-4-CONTROL-TRACEABILITY.md`, PROPOSED, non-canonical) is **not** rewritten by this round; its
three "NOT IMPLEMENTED" rows (duplicate-control detection, full 15-field finding check, second governed
worker) are superseded by RC-1, RC-3 and the second audit worker respectively.

*End of HD-4.*
