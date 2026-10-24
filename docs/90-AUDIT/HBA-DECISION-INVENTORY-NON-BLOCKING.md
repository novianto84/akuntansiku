# HBA DECISION INVENTORY — NON-BLOCKING GATES

> **SUPERSEDED IN PART — see `HBA-DECISION-RECORD-01-REMINDER-TIMESTAMP-DEPLOYMENT.md`.**
> HBA has since responded to all three items (2026-10-01):
> Reminder = deferred to a future version; WO timestamp = DECIDED (creation time is
> authoritative); Deployment = deferred, NUC target, security split to be prepared.
> This inventory remains as the evidence package that informed those decisions.

**Date:** 2026-10-01
**Status:** Evidence-only analysis. No business decision made.
**Authority:** Hermes Orchestrator (preparatory work only)

---

## 1. REMINDER / AUTOMATION POLICY

### A. Decision Required

HBA must decide:
- Whether automatic reminder generation is wanted at all (V1 or later)
- If yes: intervals, surfacing behavior, escalation rules
- If no: confirm manual-only as permanent V1 baseline

### B. Existing Evidence

| Source | Fact |
|---|---|
| CD-11 §23 | Manual reminder by Admin/Manager/Sales is the business baseline |
| IS-01 §14 OQ-07 | Reminder/automation policy (generation + intervals) — UNRESOLVED / PENDING HUMAN DECISION |
| IS-01 §11 | SLA is DISABLED (H-1). Overdue calculation DISABLED. Escalation automation DISABLED |
| IS-02 §20 | Manual reminder baseline; automatic generation + intervals not locked |
| TADR-15 | Background Jobs / Notifications — Partly blocking (reminder/automation policy) |
| ARCHITECTURE_APPROVAL_PACKAGE §8 | H-1: DISABLED. Manual reminder = baseline; automatic generation and intervals are not locked |
| TECHNICAL_ARCHITECTURE_FINALIZATION §9 | Reminders: manual reminder by Admin/Manager/Sales is the business baseline. Automatic reminder generation and intervals are not locked |

### C. Dependencies

| Blocked Item | Depends On |
|---|---|
| TADR-15 enablement | Reminder/automation policy decision |
| IS-16 (if exists) | Reminder/automation policy decision |
| Any automatic reminder generation | Reminder/automation policy decision |

### D. Non-Dependent Work (Can Proceed Now)

- Manual reminder implementation (already LOCKED as baseline)
- Reminder data model (E-55)
- Reminder API endpoints (manual creation)
- Reminder UI (manual reminder surface)
- Test coverage for manual reminder

### E. Alternatives

| Alternative | Description |
|---|---|
| A: Manual-only (V1) | No automatic generation. Manual reminder by Admin/Manager/Sales only. |
| B: Automatic with fixed intervals | System generates reminders at fixed intervals (e.g., daily, weekly). |
| C: Automatic with configurable intervals | Admin configures intervals per reminder type. |
| D: Automatic with SLA-based escalation | Reminders escalate based on SLA thresholds (requires SLA enablement). |

### F. Consequences

| Alternative | Implementation | Operational | Audit | Governance |
|---|---|---|---|---|
| A: Manual-only | Low | Low | Simple | No new policy |
| B: Fixed intervals | Medium | Medium | Medium | New policy + intervals |
| C: Configurable | High | High | High | New policy + admin UI |
| D: SLA-based | High | High | High | Requires SLA enablement (currently DISABLED) |

### G. Recommendation Status

**NO RECOMMENDATION MADE.** HBA must decide.

---

## 2. EMERGENCY RETROACTIVE TIMESTAMP CONVENTION

### A. Decision Required

HBA must decide:
- Precedence rule for emergency retroactive timestamps: event-time vs record-time
- Whether event-time can be backdated arbitrarily or bounded
- Whether record-time is always "now" or can also be backdated

### B. Existing Evidence

| Source | Fact |
|---|---|
| IS-01 §14 OQ-08 | Emergency retroactive timestamp convention (event-time vs record-time precedence) — UNRESOLVED / PENDING HUMAN DECISION |
| IS-01 §11 H-06 | Dual time capture. Event-time plus record-time capture proceeds for (retroactive) |
| IS-02 §20 | Dual capture proceeds; precedence undecided (OQ-08) |
| IS-02 §20 IS02-O07 | Emergency retroactive timestamp convention — OPEN. Dual capture proceeds; precedence undecided |
| TADR-08 | Depends on emergency retroactive timestamp convention |
| CD-11 §23 | Retroactive timestamp convention dan retroactive completion deadline menyusul (tidak ada SLA numerik yang dikunci) |

### C. Dependencies

| Blocked Item | Depends On |
|---|---|
| TADR-08 | Emergency retroactive timestamp convention |
| Emergency WO timestamp display | Precedence rule |
| Audit trail for retroactive timestamps | Precedence rule |

### D. Non-Dependent Work (Can Proceed Now)

- Dual time capture (event-time + record-time) — already proceeding
- Emergency WO creation (without retroactive timestamp)
- Emergency WO lifecycle (without retroactive timestamp)
- Test coverage for emergency WO (without retroactive timestamp)

### E. Alternatives

| Alternative | Description |
|---|---|
| A: Event-time precedence | Event-time is authoritative; record-time is metadata only |
| B: Record-time precedence | Record-time is authoritative; event-time is metadata only |
| C: Both authoritative (context-dependent) | Precedence depends on context (e.g., emergency vs non-emergency) |
| D: Event-time with bounded backdate | Event-time can be backdated up to N days; beyond that requires approval |

### F. Consequences

| Alternative | Implementation | Operational | Audit | Governance |
|---|---|---|---|---|
| A: Event-time precedence | Low | Low | Simple | No new policy |
| B: Record-time precedence | Low | Low | Simple | No new policy |
| C: Context-dependent | Medium | Medium | Medium | New policy + context rules |
| D: Bounded backdate | Medium | High | High | New policy + approval workflow |

### G. Recommendation Status

**NO RECOMMENDATION MADE.** HBA must decide.

---

## 3. DEPLOYMENT OPERATIONAL CONTEXT

### A. Decision Required

HBA must decide:
- Deployment environment (cloud, on-premise, hybrid)
- Operational constraints (backup, monitoring, scaling)
- Integration boundaries (Accurate 5, external systems)
- Security context (network, access control, data residency)

### B. Existing Evidence

| Source | Fact |
|---|---|
| IS-01 §14 OQ-10 | Deployment operational context — UNRESOLVED / PENDING HUMAN DECISION |
| IS-00 §7 | IS must be implementation-agnostic except where architecture already constrains it |
| IS-10 | Integration, Deployment & Migration Specification — deferred |
| IS-03 §148 | Deployment context — formal CD documentation pending |
| IS-04 §123 | Deployment — deferred |
| IS-05 §110 | Deployment — deferred |
| IS-06 §11 | Deployment — deferred |
| IS-11 §167 | Deployment context — deferred |

### C. Dependencies

| Blocked Item | Depends On |
|---|---|
| IS-10 (Integration, Deployment & Migration) | Deployment operational context |
| Any deployment execution | Deployment operational context |
| Any migration execution | Deployment operational context |
| Any integration with Accurate 5 | Deployment operational context |

### D. Non-Dependent Work (Can Proceed Now)

- All specification work (IS-00 through IS-FINAL)
- All architecture work (TADR-01 through TADR-18)
- All implementation work (WP-01 through WP-08)
- All test work
- All audit work

### E. Alternatives

| Alternative | Description |
|---|---|
| A: Cloud (single provider) | Deploy to single cloud provider (e.g., AWS, GCP, Azure) |
| B: On-premise | Deploy to on-premise infrastructure |
| C: Hybrid | Mix of cloud and on-premise |
| D: Multi-cloud | Deploy to multiple cloud providers |

### F. Consequences

| Alternative | Implementation | Operational | Audit | Governance |
|---|---|---|---|---|
| A: Cloud (single) | Medium | Medium | Medium | Cloud provider dependency |
| B: On-premise | High | High | High | Full operational responsibility |
| C: Hybrid | High | High | High | Complex operational model |
| D: Multi-cloud | Very High | Very High | Very High | Multi-provider dependency |

### G. Recommendation Status

**NO RECOMMENDATION MADE.** HBA must decide.

---

## SUMMARY

| Item | Decision Type | Blocking Scope | Non-Blocking Work Available |
|---|---|---|---|
| Reminder/Automation Policy | Business policy | TADR-15, IS-16 | Manual reminder implementation |
| Emergency Retroactive Timestamp | Business policy | TADR-08 | Dual time capture, emergency WO |
| Deployment Operational Context | Operational | IS-10, deployment, migration | All specification, architecture, implementation, test, audit work |

---

## AUTHORIZATION BOUNDARY

This document is **evidence-only analysis**. No business decision has been made.
No implementation has been authorized by this document.
No existing decision has been modified.

HBA retains full authority over all three items.
