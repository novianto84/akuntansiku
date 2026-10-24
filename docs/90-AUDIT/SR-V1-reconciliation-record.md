# SR V1 Documentation Reconciliation Record

**Record type:** Canonical traceability/audit record; not a new business decision or implementation specification  
**Status:** MATERIALIZED — FINAL AUDIT IN PROGRESS  
**Date:** 2026-09-25  
**Authority:** Explicit Human decisions and documentation-reconciliation instruction in the 2026-09-25 approval thread.  
**Decision IDs:** Existing BD-SR-001…005, BD-SR-010, BD-SR-011, and BD-SRWO-001 retained; no new decision ID created.  
**Implementation:** NO CODE / NO SCHEMA / NO MIGRATION / NO API IMPLEMENTATION / NO UI IMPLEMENTATION.

## Human decision → reconciliation

The final Human decision establishes SR V1 status `OPEN → CLOSED`; WO creation leaves the SR `OPEN`; SR and WO remain distinct and linked by the existing source-reference relationship; WO DRAFT is separate from official Related WO, visible only under existing permissions, continuable only by its creator, and not duplicable as another active draft; the official Related WO appears when WO is `OPEN`; `CREATE_WO` authority remains unchanged; V1 `CLOSE_SR` is Manager + Admin, with possible future configurability separate; historical `CONVERT_SR` data/labels are unchanged; no Source field/value set is invented.

## Canonical documentation materialized

| File | Reconciliation scope |
|---|---|
| `DECISION_REGISTER.md` | Synced existing SR decision summaries to the amended sources; no new decision/gate or identifier. |
| `docs/10-DECISIONS/BD-SR-001-sr-lifecycle-v1.md` | Replaced prior intermediate/conversion lifecycle with OPEN/CLOSED; SR remains OPEN after WO creation; relationship and DRAFT distinctions documented. |
| `docs/10-DECISIONS/BD-SR-002-sr-closure-reason-v1.md` | Closure-reason rule tied to OPEN → CLOSED only; WO creation does not close SR. |
| `docs/10-DECISIONS/BD-SR-004-sr-retention-visibility-v1.md` | OPEN remains editable; only CLOSED is terminal/immutable. |
| `docs/10-DECISIONS/BD-SR-005-sr-minimal-permission-matrix-v1.md` | V1 Close SR Admin + Manager only; other roles denied; CREATE_WO unchanged; future configuration separate; historic identifier note retained. |
| `docs/10-DECISIONS/BD-SR-010-sr-minimal-form-v1.md` | Editable values and closure behavior aligned to OPEN/CLOSED; no Source field added. |
| `docs/10-DECISIONS/BD-SR-011-create-wo-from-sr-v1.md` | Ordinary CREATE_WO with SR reference; preserves official-WO atomicity/duplicate/failure/lineage/audit rules; adds approved active-DRAFT routing/creator-only behavior without an SR transition. |
| `docs/10-DECISIONS/BD-SRWO-001-sr-to-wo-v1.md` | UI terminology clarified as Create WO; optional source reference and existing Manager CREATE_WO/ASSIGN_WO remain unchanged. |
| `docs/30-ARCHITECTURE/AB-01-service-execution-architecture-baseline.md` | SR lifecycle, SR→WO boundary, audit family, and invariant descriptions reconciled. |
| `docs/30-ARCHITECTURE/TA-01-technical-architecture-specification.md` | WO command/state and atomic uniqueness descriptions reconciled; no mechanism choice or implementation. |
| `docs/40-SPECIFICATION/IS-02-technical-decomposition.md` | SR state/transaction/duplicate/authorization/audit references reconciled. |
| `docs/40-SPECIFICATION/IS-04-api-service-contract.md` | Contract descriptions for follow-up, Close SR, Create WO, atomicity/duplicate expectations reconciled; no API implemented. |
| `docs/40-SPECIFICATION/IS-07-audit-history-correction.md` | SR-origin WO audit event no longer implies an SR status change. |

## Preserved boundaries

- CD-11 WO lifecycle and original draft creator ownership remain unchanged.
- Existing `CREATE_WO` authority, WO lifecycle, JOB formation guards, official-WO at-most-one V1 scope, atomic uniqueness requirement, failure handling, lineage, and append-only audit remain unchanged except removal of the superseded SR status transition.
- BD-SR-003's separate SR-content/no-auto-JOB rule is unchanged.
- Sales quotation/order `CONVERTED` terminology in CD-05/IS-01 and other unrelated business domains is unchanged.
- Historical `CONVERT_SR` logs/data were not inspected, rewritten, renamed, or migrated.
- No source field, enum, or value set was introduced.
- Existing repository `.gitignore`, `opencode.json`, and other worktree state were not modified by this reconciliation.

## Scope-limited finding not modified

`docs/30-ARCHITECTURE/AB-01-service-execution-architecture-baseline.md` has an internal status-label discrepancy: its header identifies the baseline as APPROVED / CANONICAL while its closing line calls it a DRAFT. This reconciliation updates only SR-relevant technical content in that document; the unrelated document-level approval/status wording was not resolved or changed because the available sources do not authorize selecting one label over the other. The explicit Human SR decisions and the SR decision sources govern this reconciliation; the metadata discrepancy is separately flagged for governance/document-owner review and does not change the resolved SR V1 business/UI decisions.

## Traceability and provenance limits

The Human approval thread is the authority for these amendments; no new BD identifier is created. The source decision files were untracked in the available Git worktree before reconciliation, so Git history is unavailable; the previous source texts were read directly. Historical audit/database records were not inspected. The table records the observed pre-change and final read-back hashes for every canonical source changed. The independent final read-only UI audit returned PASS with no in-scope defects; the AB-01 metadata inconsistency above remains an explicit out-of-scope item.

| Canonical file | Pre-change SHA-256 | Final read-back SHA-256 |
|---|---|---|
| `DECISION_REGISTER.md` | `0506c5a9fe6c84904c9c0c781b7ea5c645c3d08935e6bf74c30490a82d5002e7` | `5430c4a26afe31206ad205191d5f261d598cf54423e4c2251417241f19812807` |
| `BD-SR-001-sr-lifecycle-v1.md` | `701f300e2797b8ffbc86aea71ef2a4e2ae0322ad4f6e9635c7e9b53e3663211d` | `96cc250506c0224de2cfd46745236fc3982c8f84e1366ee265e3bd981be826d7` |
| `BD-SR-002-sr-closure-reason-v1.md` | `aa0c695113a7ac8f8ee65293b919d1216c448a040c300b3fcba92bc96748881d` | `ab8e905ff879faf96b058adbca9945935f590ebfd4bf2757e47cd13f301a4270` |
| `BD-SR-004-sr-retention-visibility-v1.md` | `133be2c0cf6c6b9b5a78149132ab8e891bcee1381b7bb032b92f09fffd47826d` | `c3180be4391f4780d7560a461c5ab94d72b40442a6737f6ddbc3a7e5ebc4f02c` |
| `BD-SR-005-sr-minimal-permission-matrix-v1.md` | `ff9d35ab797771e9764ce2f1a17e59273f71cf5f2ce2e1ac8102b21edcd71003` | `930da14bd6d52dd0ad35108dedf6291d953234a35f0d7f01e5332112d311374c` |
| `BD-SR-010-sr-minimal-form-v1.md` | `ac3af4fe04d0be26b6bd51f5bd37f7254af56f3061bd8ea99a43e9758cc0234d` | `b7255e9a266522bc34e6661ef9b932a830f05cca9e004e0d67dea92e1cf8f38e` |
| `BD-SR-011-create-wo-from-sr-v1.md` | `6b648de9ecfaa47b0d43a51451a457b3959e705d0cc8c5b8c3e2059226fd5ef3` | `64f3b44daa7ad6c49bbba712a04ae176902d23840be55e744bb99ddef5f137e9` |
| `BD-SRWO-001-sr-to-wo-v1.md` | `bf9845fa6906f8e777b7a8a3b83e5c82a5935cf25ad552471b5ce546e9d69632` | `60b8fb2ae3682f5a27648bcaa1aae325e56fb23dcfdc9e9f90fd3753bf7bfa0e` |
| `AB-01-service-execution-architecture-baseline.md` | `5bcff40a9c7953db4b50ad1965709ba4c012e78d31aaefd28b9b09f923eb1539` | `7a31f64e2fc18c675f0afee61228ffcaf9238914a1094c255d2af5db0af765a1` |
| `TA-01-technical-architecture-specification.md` | `6f985a6b5be2aa5cfa79aabdf2fe4cdfc36cb117e6414cb9c14f36accea34410` | `42ddcd9295761d49227a7eb5c62d7a4c4881af1f2f084fffb176f2e8727a75ac` |
| `IS-02-technical-decomposition.md` | `70cb9b504bd2a1993675c9ec46a360241df515cde581bb516844909fbc815586` | `da4824c6d837eeb208b48b3d23feb5181a9b20513e87be37a2a86c8633264d70` |
| `IS-04-api-service-contract.md` | `4e7ac197f03571df4a69303607df5f05794c03917e47bb943a3d4d9d04fa2463` | `fd7ba8dd3ddd194ef714cd934e2299764fb2d8953f687d9da1f3c06aa0087172` |
| `IS-07-audit-history-correction.md` | `e9e69c44a990e42cb26e1bbba63f620a5e7571da1293fef1810058ffe4bd5aa3` | `e3545be2a706481fc9b4beea3f0a1cd522c4104a399f63546ff4643d8759a2c0` |
