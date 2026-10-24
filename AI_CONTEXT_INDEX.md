# Brainstrom CRM - AI Context Index

## 1. FIRST READ

Before performing any project task, load:

1. `AI_OPERATING_RULES.md`
2. `ARCHITECTURE_LOCK.md`
3. `DECISION_REGISTER.md`

These documents define the current operating context and authority map.

## 2. CURRENT PROJECT MODE

The project follows:

**Business Authority -> Architecture -> Approval -> Implementation -> Audit**

Do not skip stages.

## 3. DOCUMENT AUTHORITY

Use documents according to their status.

### Current Authority

`docs/10-DECISIONS/` contains formal business decisions and their current status.

### Architecture

`docs/30-ARCHITECTURE/` contains the approved technical architecture. Technical architecture is **APPROVED / CANONICAL** — Human Final Technical Architecture Approval, 2026-09-21 (TADR-01 … TADR-18 and the Architecture Baseline), plus Business Authority Architecture Approval of the direction, 2026-09-22 (`ARCHITECTURE_APPROVAL_PACKAGE.md`, §1–§12). Current status is stated in §6. This approval does not authorize implementation.

### System Specification (IS)

`docs/40-SPECIFICATION/` contains the specification layer: `IS-00` (IS governance / master plan) and `IS-01` … `IS-11` with their technical decompositions and design notes. Status: SPECIFICATION — non-LOCKED. Business OPEN items remain owned by the Human / Business Authority per `IS-00` §7/§8, and the layer relationship is defined in `IS-00` §4.2.

Note on historical stage records: `docs/90-AUDIT/00-INDEX.md` and `docs/20-WORKSTREAMS/00-INDEX.md` are materialisation stage records dated 2026-09-18 (each declares `Status dokumen: PROPOSED` and limits itself to "tahap ini"). They document the file counts that were correct for that stage (2 of 5 and 3 of 5 canonical files respectively) and are retained unchanged as historical evidence. They are not the live index; current canonical status is recorded in `DECISION_REGISTER.md`, and the current directory contents are authoritative for what exists now.

### Workstreams

`docs/20-WORKSTREAMS/` contains structured workstream material.

### Audit / Evidence

`docs/90-AUDIT/` contains evidence, audit findings, observations, and supporting material.

Historical material is evidence unless explicitly designated as current authority.

### Manager Agent Operating Summary (non-canonical)

`SOUL.md` — the Manager agent's operating summary, held outside this repository in the Manager
profile home (`~/.hermes/SOUL.md`) — is a **non-canonical operational summary** of Manager
behaviour, derived from the canonical documents above. It carries no authority of its own:
each point in it names the canonical section it comes from, and where SOUL.md and a canonical
document differ, **the canonical document prevails**. SOUL.md exists to keep the Manager's
core behaviour stable in context; it is not a source of business decisions, rules, roles,
permissions, or status.

## 4. CONTEXT LOADING RULE

Do not read the entire repository by default.

```text
Level 0:
AI_CONTEXT_INDEX.md
AI_OPERATING_RULES.md

Level 1:
ARCHITECTURE_LOCK.md
DECISION_REGISTER.md

Level 2:
Only task-relevant canonical documents

Level 3:
Evidence / historical material only when required
```

## 5. TASK PROMPT FORMAT

Future task prompts should normally contain only:

```text
TASK:
<task name>

MODE:
READ / PROPOSE / APPROVE / IMPLEMENT

OBJECTIVE:
<what must be accomplished>

AUTHORITATIVE INPUTS:
<document IDs / paths>

OUTPUT:
<expected deliverable>

TASK-SPECIFIC CONSTRAINTS:
<only constraints unique to this task>
```

Do not repeat the full AI Operating Rules in every task prompt.

## 6. CURRENT ARCHITECTURE STATUS

At the current project checkpoint:

### Business Architecture

* CD-01 = FINAL / LOCKED.
* CD-03 through CD-10 = LOCKED.
* CD-11 = SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF — CD-11 Business Finalization, CD11-001…CD11-029).
* CD-02 = DEFERRED / UNVERIFIED and remains absent from the current decision directory.

CD-11 reached SIGNED-OFF / LOCKED / CLOSED via explicit BA sign-off; it must not be treated as HUMAN-ACCEPTED or PROPOSED.

### Technical Architecture

Technical architecture: APPROVED / CANONICAL (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21), covering TADR-01 … TADR-18 and the Architecture Baseline. Architecture direction additionally APPROVED by BUSINESS AUTHORITY — ARCHITECTURE APPROVAL (2026-09-22) per `docs/30-ARCHITECTURE/ARCHITECTURE_APPROVAL_PACKAGE.md`; implementation detail explicitly DEFERRED to IS Specification. F-1 remains DEFERRED; C-1/C-2 are documentation cleanup only. This approval does not authorize implementation.

### Implementation

**ISSUED 2026-10-03** (HBA-DECISIONS-03 §1). Implementation authorization is issued for work already executed (WP-01…WP-10 backend + internal UI). Work not yet started requires a new authorization before it begins.

## 7. ACTIVE HUMAN DECISION GATES

Decision-gate status is recorded in `DECISION_REGISTER.md`, which is the authority for it. This section is a summary only; do not infer a gate's status from a list position.

**LOCKED business decisions — the decisions are made; formal CD documentation is pending only where explicitly recorded in `DECISION_REGISTER.md` (it adds no new decision):**

* identity-link reconciliation
* QR access policy (CONTROLLED ACCESS)
* Business Access Model (Unit Scope / Company Scope)
* Customer publication retention — **HBA D-01A = RETAIN (FINAL)**; D-01B semantic freshness only, no numeric SLA; OQ-02 publication permission already canonical. Serving/snapshot/refresh mechanisms remain architecture work.

**UNRESOLVED decisions — no business decision exists yet; pending Human decision:**

* reminder / automation policy
* emergency retroactive timestamp convention
* deployment operational context

Do not resolve these by technical assumption.

## 8. TRACEABILITY

Preferred chain:

```text
Human Decision
    v
CD / BD / DD
    v
Technical Requirement
    v
TADR
    v
Implementation Specification
    v
Implementation
    v
Test
    v
Audit
```

Any missing link should be reported.

## 9. CONFLICT HANDLING

If sources conflict:

**STOP -> IDENTIFY -> TRACE -> ESCALATE**

Never silently choose a source.

## 10. CONTEXT EFFICIENCY PRINCIPLE

Persistent rules belong here or in referenced governance documents. Task prompts should carry only task-specific information.

## 11. FINAL RULE

> Read the context once.
> Read only what the task needs.
> Never invent what the project has not decided.
> Never implement what the Human has not authorized.
