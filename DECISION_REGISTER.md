# Decision Register

**Status:** TRACEABILITY REGISTER / AUTHORITY INDEX

This register records current decision-document status and known Human Decision Gates. Listing a gate does not create a business decision, assign a business rule, or approve a technical solution.

> **Amendment note - status freshness (2026-09-26, amendment by Hermes).**
> The rows in this register record the status of each item **as of the date named in that row**; a row is not
> rewritten when a later acceptance event occurs. One later event is therefore NOT reflected in the rows below:
> the Bridge Contract final acceptance, state **`ACCEPTED WITH EXPLICIT RESIDUALS`**, whose address of record is the
> acceptance receipt (sha256 begins `27fe1db7`). Later revision-identity clarifications for that contract are
> addressed by the contract's own addenda and are deliberately NOT restated here. **To read current status, use the
> acceptance receipt and the contract's own header - not this register's historical rows.** This note is additive:
> no existing row, wording, or historical record is modified by it, and it creates no business decision, rule,
> permission or status.

> **Amendment note — Manager operating summary (`SOUL.md`) revision (2026-10-02, amendment by Hermes).**
> Under explicit Human Business Authority decision **D-7** (2026-10-02), the Manager agent's operating
> summary (`SOUL.md`, held outside this repository in the Manager profile home) was revised. The revision:
> (a) records `SOUL.md` as a **non-canonical operational summary**, with the canonical documents
> remaining authoritative wherever they differ; (b) states the AI modes as **READ / PROPOSE / IMPLEMENT**
> and clarifies that **APPROVE belongs to the Human**, not to AI; (c) replaces rule text duplicated from
> the canonical documents with concise pointers to the canonical section numbers. Address of record for
> the revised summary: Manager profile home `SOUL.md`; pointer added at `AI_CONTEXT_INDEX.md` §3.
> This note is **additive**: it modifies no existing row, creates no business decision, rule, role,
> permission, or status, and authorizes no implementation. Traceability: Human Decision **D-7** (2026-10-02)
> -> `SOUL.md` revision -> this note.

> **Amendment note — HBA-DECISIONS-30/31/32/34 dan addendum kanon (2026-10-24, catatan oleh Hermes).**
> Perintah HBA **"segera kanonin kan. dan eksekusikan"** (chat 2026-10-24) menutup empat pertanyaan
> terbuka HBA-DECISIONS-30: diskusi boleh dibaca semua pihak internal; panggilan pekerja cukup di dalam
> aplikasi dan semua pihak internal berhak memanggil; hanya Manager/Admin yang menandai berkas boleh
> tampil di portal pelanggan; dan rujukan SPK/Invoice/Project cukup **satu kolom**. Peran **Admin diisi
> akun** yang dikaitkan dengan akun Google `noviantodj@gmail.com`. Addendum kanon yang bersangkutan:
> `IS-01` (diskusi internal, rujukan dokumen unit, penyerahan unit, penanda terbitan), `IS-03` v1.5
> (hak baca internal, panggilan, penanda terbitan, pengisian peran Admin), `IS-05` v1.2 (penanda terbitan
> artefak tingkat Unit + bingkai WO setara Visit), `IS-06` v1.4 (berkas unit yang boleh tampil dan tiga
> hal penyerahan yang tidak dicantumkan), `IS-07` v1.2 (diskusi bukan audit; transisi penanda diobservasi
> audit), `IS-08` v1.2 (empat permukaan detail Unit + Kotak Masuk). Rekaman audit: HBA-DECISIONS-30,
> -31, -32, -33, -34. Catatan ini **aditif**: tidak mengubah baris mana pun di bawah, tidak membuat
> keputusan bisnis, peran, izin, atau status baru di luar rekaman HBA di atas.

## Current Decision Documents

| Decision | Status | Canonical source | Traceability note |
|---|---|---|---|
| CD-01 | FINAL / LOCKED | `docs/10-DECISIONS/CD-01-business-scope.md` | Current business scope and boundary authority |
| CD-02 | DEFERRED / UNVERIFIED | No current canonical document present | Must not be reconstructed |
| CD-03 | LOCKED | `docs/10-DECISIONS/CD-03-business-master.md` | Current canonical decision |
| CD-04 | LOCKED | `docs/10-DECISIONS/CD-04-operational-acquisition-price.md` | Current canonical decision |
| CD-05 | LOCKED | `docs/10-DECISIONS/CD-05-sales-transaction-quotation.md` | Current canonical decision |
| CD-06 | LOCKED | `docs/10-DECISIONS/CD-06-vendor-offer-price.md` | Current canonical decision |
| CD-07 | LOCKED | `docs/10-DECISIONS/CD-07-multi-workspace.md` | Current canonical decision |
| CD-08 | LOCKED | `docs/10-DECISIONS/CD-08-data-ownership.md` | Current canonical decision |
| CD-09 | LOCKED | `docs/10-DECISIONS/CD-09-purchasing-transaction-boundary.md` | Current canonical decision |
| CD-10 | LOCKED | `docs/10-DECISIONS/CD-10-inventory-operational-boundary.md` | Current canonical decision |
| CD-11 | SIGNED-OFF / LOCKED / CLOSED | `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md` | Signed-off canonical baseline (BA SIGN-OFF, CD11-001…CD11-029); operative terminology appendix: `docs/10-DECISIONS/CD-11-Appendix-A-job-scope-terminology.md` (does not alter historical content) |
| BD-WORKTYPE-001 Rev.A | APPROVED / CANONICAL (minimum-cardinality wording partially superseded, see BD-WORKMODEL-001 C-01) | `docs/10-DECISIONS/BD-WORKTYPE-001-job-scope-canonicalization.md` | JOB / SCOPE canonicalization (BA APPROVAL 2026-09-23); operative minimum for official WO now 1..N per BD-WORKMODEL-001; remainder in full force; implementation NOT authorized |
| BD-WORKMODEL-001 | APPROVED / CANONICAL | `docs/10-DECISIONS/BD-WORKMODEL-001-work-model-definitions.md` | Work Model definitions (SERVICE / INSPEKSI / EMERGENCY TROUBLESHOOT) + JOB minimum 1..N (DRAFT exempt) + Visit/continuation + ON HOLD + Minor Job + Junior/Senior boundary (BA DECISION 2026-09-23); operative CD-11 appendix: `docs/10-DECISIONS/CD-11-Appendix-B-work-model-continuation.md`; implementation NOT authorized |
| BD-SRWO-001 | LOCKED — V1 | `docs/10-DECISIONS/BD-SRWO-001-sr-to-wo-v1.md` | SR→WO V1 scope: O-06 Manager default CREATE_WO + ASSIGN_WO unchanged; O-07 optional WO.source_sr_id (NULL = direct WO); one-WO-per-SR as V1 scope limit only; UI entry label Create WO (not a special business action); source SR remains OPEN; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| BD-SR-001 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-001-sr-lifecycle-v1.md` | SR Lifecycle V1 (O-01), reconciled to final Human decision: OPEN → CLOSED only; WO reference/creation leaves SR OPEN; no HAS_WO, CONVERTED, or REALIZED SR status; no reopen; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| BD-SR-002 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-002-sr-closure-reason-v1.md` | SR Closure Reason V1 (O-02): DUPLICATE / WITHDRAWN / DECLINED / OTHER (keterangan mandatory only for OTHER); mandatory on OPEN → CLOSED; immutable; WO creation leaves SR OPEN and requires no closure reason; audit follows existing pattern; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| BD-SR-003 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-003-sr-content-boundary-v1.md` | SR Content Boundary V1 (O-03): 8 content definitions; SR-context vs WO-establishes boundary; no SR JOB or auto-JOB creation / new entity; unchanged; implementation NOT authorized |
| BD-SR-004 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-004-sr-retention-visibility-v1.md` | SR Retention/Visibility V1 (O-04): no special retention; internal visibility by assignment/relevance; zero external exposure; no visibility field; editable while OPEN, immutable only after CLOSED; no delete; no reopen; WO creation leaves SR OPEN; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| BD-SR-005 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-005-sr-minimal-permission-matrix-v1.md` | SR Minimal Permission Matrix V1 (O-05), reconciled: CLOSE_SR Admin + Manager only; future configurability is a separate Configuration Panel concern; existing CREATE_WO authorities unchanged; other roles have no CLOSE_SR; historical CONVERT_SR data unchanged; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| BD-G01-G02 | LOCKED — V1 | `docs/10-DECISIONS/BD-G01-G02-identity-boundary-v1.md` | Identity Boundary V1: Option A intake-scoped requester + link-at-verification; Claim ≠ Relationship; Contact/PIC model unchanged (CD-03); requester ≠ new entity; governed verification/promotion, no auto-merge/delete, history preserved; individual valid, NULL company, no V1 external access (future question deferred); implementation NOT authorized |
| BD-SR-010 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-010-sr-minimal-form-v1.md` | SR Minimal Form V1 (O-10): field table; Requester REQUIRED + (Need OR Scope) + Company OPTIONAL; lifecycle OPEN/CLOSED; edit while OPEN, read-only after CLOSED; WO creation leaves SR OPEN; Source field/value set is not defined; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| BD-SR-011 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-011-create-wo-from-sr-v1.md` | O-11, reconciled: ordinary CREATE_WO with optional SR reference; SR remains OPEN; WO formation + lineage/audit atomic; no auto-JOB; preserve max-one official WO duplicate guard; active DRAFT routes to existing draft, creator-only continuation; official Related WO at OPEN; implementation NOT authorized; see `docs/90-AUDIT/SR-V1-reconciliation-record.md` |
| **HD-4** | **CANONICAL (recorded, not created) — materialized 2026-09-26** | `docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md` (sha256 `2545ae87ddbe99f4cb155b3805d7f07aa9e17be3bda87747f94749cae5cdb4c7`) | Delegated audit control authority: the twelve-control governed delegation envelope (HD-4 §4) + the audit result contract (HD-4 §12) + the RC-1 exactly-one-definition rule + the RC-3 schema-completeness control + the D-3 verbatim-passing duty. Materialized by explicit HUMAN BUSINESS AUTHORITY decision **D-1** (2026-09-26) in `docs/10-DECISIONS/` (**D-2**, which resolves **SD-8**). Documentation only: this row, and the record it points to, create no control, rule, role or permission, reinterpret nothing, expand no authority, and change no demonstrated enforcement behaviour. This is the governance-control record for governed worker delegation — it is not a CRM business decision. **Implementation NOT authorized.** Related: `docs/90-AUDIT/G1-D-ACCEPTANCE-AND-CONTROL-ADOPTION-RECORD.md` |

## Pending Human Decision Gates

The following are known decision gates. Four are now DECIDED by explicit HUMAN decision (recorded, not created, here — three LOCKED human decisions plus the customer publication model, HBA D-01A = RETAIN); the remainder are pending/unregistered and have no invented BD identifier. Listing a gate does not create a business decision, assign a business rule, or approve a technical solution. Formal CD documentation of the three LOCKED decisions is pending.

### WP-11 Specification Gaps (F-20 through F-24)

Tracked for traceability — these originated from the WP-11 independent second-opinion review and were resolved via HBA decisions recorded in `WP-11_HBA_DECISION_PACKAGE_F20-F24.md` and `HBA-DECISIONS-05.md` / `HBA-DECISIONS-06.md`. The package itself is NON-CANONICAL / DECISION PREPARATION ONLY.

| Gate | Register status | Canonical support | Note |
|---|---|---|---|
| F-20 — Pending Revision Abandonment | **RECORDED** — HBA decision (2026-10-03), clarified 2026-10-05 | `HBA-DECISIONS-05` §1; WP-11 package §2 | DRAFT-based lifecycle adopted: no expiry, cap 10/user, creator-only cancel, competing DRAFTs not cancelled (INV-30 revoked) |
| F-21 — Pending View Configuration | **RECORDED** — HBA decision (2026-10-03), clarified 2026-10-05 | `HBA-DECISIONS-05` §2; WP-11 package §3 | INTERNAL-ONLY, configurable via Configuration Panel (Model D); creator always sees own DRAFT; Manager/Admin sees only after SUBMITTED; customer never sees pending (R-37 unchanged) |
| F-22 — Baseline Materialization | **RECORDED — HBA decision (2026-10-17): canonical promotion + file with checksum AUTHORIZED** | WP-11 package §4; HBA statement room `etc` 2026-10-17: "ubah jadi kanonik. dan saya izinkan file dengan checksum" | WP-11 baseline promoted to canonical; frozen reference artifact with digest sidecar authorized (Option B + canonical promotion). Canonical promotion is HBA's call — now made. |
| F-23 — Attachment Snapshot Semantics | **RECORDED** — HBA decision (2026-10-03), clarified 2026-10-05 | `HBA-DECISIONS-06`; WP-11 package §5 | Option B — Published Revision retains EXACT attachment/content version; replacement = new version with label; historical versions remain viewable |
| F-24 — Reason Enforcement Point | **DECIDED** — enforcement point at SUBMIT (specification/lifecycle-mechanics level, AI Manager, 2026-10-05) | WP-11 package §6 | DRAFT creation/editing: reason NOT required; SUBMIT: reason mandatory; REJECT: reason mandatory; correction after REJECT: no new reason required; requirement itself HBA-LOCKED (R-09/INV-14) |
| R-26/INV-08 vs Competing DRAFTs Collision | **RESOLVED** (supersession of earlier reading, no new business rule) | WP-11 package §11A | Single-Pending rule scopes to numbered/submitted workflow only; DRAFTs are unnumbered/pre-workflow and outside the count; INV-30 revoked; stale spec text in v2.4 flagged for corrective pass |

| Gate | Register status | Canonical support | Note |
|---|---|---|---|
| Identity-link reconciliation | LOCKED HUMAN DECISION (formal CD documentation pending) | HUMAN explicit decision: Google-only external sign-up/sign-in; sign-up alone grants no Company/PIC access; PIC registration is an application yielding PENDING; supporting evidence may be requested (no fixed taxonomy); Manager/Admin approval establishes the Verified PIC Link; Google email need not be a company email and email matching is NOT the requirement; Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company Access; no cross-company grant | Reconciled; see TADR-13 |
| QR access policy | LOCKED HUMAN DECISION: CONTROLLED ACCESS (formal CD documentation pending) | HUMAN explicit decision: SCAN QR → SIGN UP/SIGN IN (Google-only) → CHECK ACCESS → UNIT DATA; no anonymous access; QR permanent and unit-scoped; customer-safe visibility mandatory | Reconciled; see TADR-16 |
| Business Access Model (Unit Scope / Company Scope) | LOCKED HUMAN DECISION (formal CD documentation pending) | HUMAN explicit decision: no data without Google sign-up/sign-in (no preview); QR on Unit/Invoice/Surat Jalan is the same QR resolving to the same Unit; authenticated non-PIC users receive UNIT SCOPE only (unit identity, owner company, address, work/material history; no PIC details/lists, no other units, no company-level data, no prices); verified PIC receives COMPANY SCOPE (all Units of that Company in the CRM plus histories and PIC per customer-safe visibility); explicit no-price rule for the customer portal; invariants LOGIN ≠ COMPANY ACCESS, QR ≠ COMPANY ACCESS, Verified PIC = basis of Company Access | Reconciled; see TADR-12/13/14/16 |
| Customer publication model | **DECIDED — HBA D-01A = RETAIN (FINAL)** | CD-11 §§20–21 (customer-safe publication); TADR-12 | Business expectation RESOLVED: previously presented customer-facing content remains available as the historical record of what was presented; the current authoritative condition remains distinguishable. RETRACT semantics do not apply. Publication permission is **already canonical** (CD-11 §21 + IS-03 §7). Publication/serving **mechanism** (snapshot materialization, refresh, propagation, cache, replication, drift monitoring) remains an **architecture decision** (TADR-12/18). No numeric freshness/SLA. Materialized in IS-06 v1.1 (2026-09-30) |
| Reminder / automation policy | **DEFERRED by HBA** (HBA-DEC-RECORD-01 Decision 1, 2026-10-01) | CD-11, Q27 and deferred-details sections; HBA-DEC-RECORD-01 | Manual-only remains V1 baseline; automatic generation deferred to future version |
| Emergency retroactive timestamp convention | **DECIDED by HBA** (HBA-DEC-RECORD-01 Decision 2, 2026-10-01) | CD-11, deferred-details section; HBA-DEC-RECORD-01 | WO creation timestamp is authoritative; no retroactive event-time convention required |
| Deployment operational context | **DEFERRED by HBA** (HBA-DEC-RECORD-01 Decision 3, 2026-10-01) | HBA-DEC-RECORD-01 | V1 target is NUC; security split (backend local/Tailscale-only, app public) to be prepared; hosting topology, DB, backup, monitoring remain open |
| CP-C C-3 — Cross-workspace isolation unenforced on list paths / workspace-less tables | **LOCKED / RECORDED — full corrective fix authorized** (HBA decision 2026-10-07) | `HBA-DECISIONS-07`; finding in `docs/90-AUDIT/CP-C-CROSS-WORKSTREAM-CONSISTENCY-LOG.md` §3 (REPRODUCED) | HBA authorized the full fix: filter every list path by active workspace; scope the workspace-less tables; add durable per-user workspace membership; explicit negative-path tests. Enforces the IS-11 isolation invariant (I-10 / TADR-05 app-level isolation). No business rule created; implementation task `t_9fdb5c92` registered on the Hermes board |
| CP-C C-1 residual — 3 legacy visits COMPLETED tanpa jam check-in/out | **DEFERRED-LOCKED** (HBA 2026-10-07): belum ada data real → abaikan; jika data lama muncul, tandai (jangan reinterpretasi) | `HBA-DECISIONS-08` | Per-visit decision closed; no invention until first real data |
| CP-C C-2 + C-5 — general event store + acknowledge no-op | **LOCKED — AUTHORIZED** (HBA 2026-10-07) | `HBA-DECISIONS-08` | Implementation card `t_074bbe2c` ready |
| IS-01 + IS-02 — specification acknowledgement | **ACCEPTED by HBA** (2026-10-07) | `HBA-DECISIONS-08` | Status headers updated; implementation still needs separate authorization |
| IS-06 portal — price display + authentication | **LOCKED** (2026-10-07): portal TIDAK menampilkan harga; login/signup Google-only | `HBA-DECISIONS-08` | |
| IS-06 portal — serving topology | **LOCKED — EMBEDDED (menyatu)** (2026-10-07); HBA akan revisit setelah V1 running | `HBA-DECISIONS-09` | Publication mechanism O-01/O-02 remains OPEN |
| Company logo persistence (profil perusahaan) | **AUTHORIZED — DB migration** (HBA 2026-10-17, room `etc`) | HBA statement: "saya izinkan untuk buat kolom baru di tabel perusahaan" | New column in perusahaan table for logo storage authorized; implementation flows through governed pipeline; upload-file flow remains later-step (URL-first tetap kondisi berjalan sampai migrasi+UI selesai) |

## Technical Architecture Approval

| Decision | Status | Scope | Authority | Date | Source |
|---|---|---|---|---|---|
| Technical Architecture Approval | APPROVED / CANONICAL | TADR-01 … TADR-18 + Architecture Baseline | HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL | 2026-09-21 | `docs/30-ARCHITECTURE/ARCHITECTURE_BASELINE.md`, `docs/30-ARCHITECTURE/TADR/` |
| Architecture Approval Package | APPROVED / CANONICAL | Architecture direction per `ARCHITECTURE_APPROVAL_PACKAGE.md` (§1–§12); implementation detail explicitly DEFERRED | BUSINESS AUTHORITY — ARCHITECTURE APPROVAL | 2026-09-22 | `docs/30-ARCHITECTURE/ARCHITECTURE_APPROVAL_PACKAGE.md` |

* F-1 remains DEFERRED — NON-BLOCKING; not resolved by this approval.
* C-1/C-2 remain DOCUMENTATION CLEANUP — NON-BLOCKING; not edited by this task.
* This approval does not authorize implementation: Implementation / Coding / Schema /
  Migration / API / UI / Deployment = NO; Programmer handoff = NO; TASK-001 = NOT CREATED.

## Approved UI Baselines & Architecture Direction (recorded 2026-09-25)

Recorded, not created: these rows add no business decision, rule, permission, status, field, or
implementation authority. Full detail and file-level reconciliation:
`docs/90-AUDIT/UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md`.

| Item | Status | Reference | Traceability note |
|---|---|---|---|
| SR V1 UI baseline | HUMAN-APPROVED UI BASELINE (not canonical) | `REV7-SR-V1-UI-SPECIFICATION-PROPOSED.md` (sha256 `68793a1c05ef7b479941668058c9b4b494d738b1395fa95ed1c39320c8060b3a`) | Approval covers UI behaviour only; ≠ canonical amendment (SR V1 business materialization already recorded in `docs/90-AUDIT/SR-V1-reconciliation-record.md`); ≠ implementation authorization |
| WO V1 UI baseline | APPROVED HUMAN BASELINE (not canonical) | `REV1-WO-V1-UI-SPECIFICATION-PROPOSED.md` REV1.7 (sha256 `f2ef7e71aa877e01fe6d259149498b35487cfeab96c7dd0fe00e0aea287abcb4`; superseded REV1.6 `1753d5e2e6df72b1a47c52863ba64b6a807a3bcc5698c32ac8a9bcfb981063af`, REV1.5 `f8fae8187193779e0c8bb36401304cdd0aa21243d2103abd858a67a8932c6039`, REV1.4 `a621601e02d4996092122a29c8e4cc18599e1612357183e4d10861b535822dcb`, REV1.3 `01e6ac4c7d9aa9e7074ab8bc9bfb8273af43e7969157bc8fb818b8e80c5406d2`, REV1.2 `6d1360624280ddfe76546e284568bd2b14254741099e0dce72764393dced5801`); audit `3e7f248d2cd4b08922c0affd0ddcd0aa604a024d0a4911e6e65f8d51cfa06e93`; delta audit `451ae66c2b0873366870b09d98afef1e95c27b8b1f101cef9e8d4c2d67268e9c` | Same three-gate separation (UI approval ≠ canonical amendment ≠ implementation authorization). Errata only, no substantive change: REV1.3 citation correction; REV1.4/REV1.5 §15/§18 status wording refreshed to the executed state; REV1.6 O15 status wording refreshed to RESOLVED (2026-09-25 option A: display canonical `INSPEKSI`, no alias — S5-01 correction). Recorded in `docs/90-AUDIT/UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md` §8; REV1.7 E5 closure recorded (2026-09-26 — no additional JOB presentation label; §18 revision label aligned) |
| Multilingual-ready UI/architecture direction | HUMAN-APPROVED DIRECTION — recorded (not a business rule) | this register + the reconciliation record | V1 default Bahasa Indonesia; English translation-catalog foundation; UI strings via translation keys; canonical identifiers/values never translated; business/user-generated data never auto-translated; no mandatory language switcher in V1; LOCKED terminology must not be silently redefined through translation |
| V2 backlog items (DRAFT-vs-OPEN simplification; "WO Open = Draft" representation study; Job List simplification) | FUTURE / V2 — NOT V1 | reconciliation record, §V2 | Non-normative; may not justify any V1 change, shortcut, or early implementation |
| Template axis (Work Model × Service Type only) | ALREADY CANONICAL (no new decision) | `BD-WORKMODEL-001` §8/§10; `AB-01` (no third workflow/template axis) | CD-11 template/WO-type phrasing remains unchanged; recorded as documentation-only reconciliation (DOC-R1) |
| JOB provenance presentation (E5 / AMD-06 closed) | HUMAN DECISION — RECORDED (presentation only; not a business rule) | Human Business Authority decision (2026-09-25 governance discussion, recorded 2026-09-26) | No additional JOB presentation label is required: no `Planned JOB`, no `Issued Job`, no `Corrective Job`, no new JOB subtype or entity, and no replacement provenance label. `Added During Execution` remains the applicable provenance marker. The E5 optional erratum and the AMD-06 `BD-WORKTYPE-001` §5 naming erratum are closed as "no action"; `BD-WORKTYPE-001` §3 (prohibition of "Current / Planned / Pending Job" as business concepts) and `CD-11-Appendix-A` remain unchanged |

Provenance limitation: the two UI baselines and both audit reports currently live **outside** the
canonical document tree (bridge workspace `/home/anto/hermes-opencode-bridge/`). Their promotion
or relocation into an approved repository location requires separate Human authorization and is
not performed here. No file was moved, renamed, or migrated.

These entries do not create decisions, promote proposals, or authorize implementation.

## AI Governance Controls & Phase Acceptances (recorded 2026-09-26)

Recorded, not created: these rows add no business decision, rule, permission, status, field, or
implementation authority. Full detail: `docs/90-AUDIT/G1-D-ACCEPTANCE-AND-CONTROL-ADOPTION-RECORD.md`
(sha256 `7bd1ed9ce05e0c694dbe4aaff4ab71c14399b207454f54480ff1af991fe29918`).

| Item | Status | Reference | Traceability note |
|---|---|---|---|
| HD-4 materialization | **DONE — CANONICAL (recorded)** | `docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md` (sha256 `2545ae87ddbe99f4cb155b3805d7f07aa9e17be3bda87747f94749cae5cdb4c7`) | HBA decision **D-1** (2026-09-26). Materialization is documentation/governance work only: HD-4 is not reinterpreted, its authority is not expanded, no control is invented, no enforcement behaviour is changed, CRM rules and `CD-11` are untouched, and no remediation beyond the decision is authorized. Traceable to the already-decided HD-4 control set as enforced (gate `46849812…`) and to the decision history |
| Canonical location for HD-1 / HD-4 records | **DECIDED — `docs/10-DECISIONS/`** | HBA decision **D-2** (2026-09-26); recorded in the acceptance record | **Resolves SD-8.** No documentation tree restructuring; `docs/60-GOVERNANCE/`, `docs/70-GOVERNANCE/` and `docs/80-GOVERNANCE/` were **not** created; no unrelated document was moved. Only the minimum necessary records were created. `HD-1` record itself is **not** materialized by this decision and is reported OPEN (its location is decided, its materialization is not authorized here) |
| Delegation-envelope authorship policy (verbatim passing) | **DECIDED — policy recorded** | HBA decision **D-3** (2026-09-26); policy text in the acceptance record §2; duty clause in `.opencode/agent/mitrasp-manager.md` | The Manager passes the envelope verbatim as authored and must not add, complete, repair, infer or substitute missing controls before the governed enforcement boundary; a missing control stays missing and is rejected. Closes **RF-G1D-01** at the policy level. **Envelope hash-binding is NOT AUTHORIZED** (issuance, publication, comparison, hash-bound acceptance, plumbing) — a separate future decision |
| RC-1 (exactly-one-definition rule) and RC-3 (machine-enforced schema completeness) | **ADOPTED** | HBA decision **D-4** (2026-09-26); scope in the acceptance record §3; controls documented in the HD-4 record §2/§3 | Adopted only within the G1-D demonstrated scope; not expanded, and the control architecture is not redesigned as part of the adoption |
| G1-D phase verdict | **ACCEPTED: `G1-D VERIFIED WITH DECLARED FRESHNESS LIMITATIONS`** | HBA decision **D-5** (2026-09-26); mandatory qualification in the acceptance record §4 | Two criteria have **no fresh same-phase live negative-event evidence**: (1) the malformed-output rejection direction rests on current deterministic module evidence plus a prior live rejection on the same code path; (2) fail-closed was not deliberately re-broken because the destructive probe was not authorized. The deterministic battery is **regression protection, not a substitute for fresh live evidence**; the limitations must remain visible, and affected control paths must be revalidated if changed. This acceptance implies **no** CRM implementation, schema, API, migration, production-UI, MCP or autonomous-remediation authorization, **no** Bridge Contract final acceptance, and **no** hash-binding authorization |
| `mitrasp-falsifier` standing scope | **APPROVED WITH STRICT SCOPE LIMITATION** | HBA decision **D-6** (2026-09-26); scope in the acceptance record §5; scope block in `.opencode/agent/mitrasp-falsifier.md` | Standing second audit worker for audit independence only (independent perspective, falsification review, conflict testing, evidence challenge). **Not** a second Manager, **not** an authority centre; no approval, closure, dispatch, remediation, implementation, governance-promotion, subdelegation or self-escalation authority; remains a governed worker with `task: deny` intact |

Items still open after these decisions: `RR-1` (raw `opencode run` path) — OPEN; `RR-4`
(`governed_sha256` refusal path) — OPEN; `BRIDGE_CONTRACT.md` final acceptance — **ACCEPTED WITH EXPLICIT RESIDUALS** (acceptance receipt sha256 begins `27fe1db7`); `RC-01`…`RC-06`
— PROPOSED / UNTOUCHED; envelope hash-binding — NOT AUTHORIZED; `HD-1` record materialization — OPEN.

## Governance Boundary

This register does not create decisions, promote proposals, reconstruct CD-02, promote CD-11, approve technical architecture, or authorize implementation. Conflicts must follow: STOP -> IDENTIFY -> TRACE -> ESCALATE.
