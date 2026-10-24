# CD-11 Amendment Appendix B — Work Model / Continuation / ON HOLD

```text
Parent document: docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md
  (SIGNED-OFF / LOCKED / CLOSED — historical content UNCHANGED by this appendix)
Authority: BD-WORKMODEL-001 — APPROVED / CANONICAL (BA DECISION 2026-09-23)
Status: APPROVED / CANONICAL appendix (operative clarification only)
```

This appendix adds operative meaning per BD-WORKMODEL-001. It does not rewrite,
delete, or reinterpret any historical CD-11 sentence. Where operative wording below
narrows usage, the historical text remains readable as period text.

## B.1 JOB minimum on official WO (CD-11 §§2, 12)

- An official WO (from Submit/OPEN onward) contains `1..N JOBs` (BD-WORKMODEL-001 §3,
  partially superseding BD-WORKTYPE-001 minimum-cardinality wording only).
- DRAFT is not a WO (CD-11 §2: creator-owned, pre-Submit, not official, outside the
  operational workflow) and may carry zero JOBs. The minimum applies when the DRAFT
  becomes an official WO.

## B.2 Continuation vs ON HOLD (CD-11 §§10, 11)

- Same work unfinished because Visit time ran out → next Visit, same WO, WO stays
  `IN_PROGRESS`. This is operational continuation: not ON HOLD, not a new Visit Type,
  not a new status/field (BD-WORKMODEL-001 §4). The next Visit carries the canonical
  Visit Type per system mechanism (`ON PROCESS` for second and subsequent visits).
- ON HOLD is used only when work is blocked pending action/decision/approval/condition
  from another/external party (BD-WORKMODEL-001 §5). Mechanism unchanged (CD-11 §11:
  reason mandatory; same-WO continuation; `IN_PROGRESS` + indicator; no HOLD workflow).

## B.3 Emergency response sequence (CD-11 §§6, 12, 16, 24)

- Within the same Emergency response sequence, `Troubleshoot` (JOB) → diagnosis
  (analysis/result, never a JOB name) → necessary action/repair where feasible is part
  of the Emergency response (BD-WORKMODEL-001 §1.3), not an "exception" to Service /
  Add Job rules.
- Follow-up that has become new business (quotation, approval, spare part, major work,
  or a new visit as new work) → new WO, generally SERVICE (BD-WORKMODEL-001 §1.3a;
  cf. CD-11 §3 substantial-work path). Add Job minor-only + actually-performed-only
  (CD-11 §12 + Appendix A) continues to govern work outside that response sequence.

## B.4 Work Model stability; Minor Job (CD-11 §§12, 16)

- Work Model follows the WO's initial purpose and does not switch automatically
  (BD-WORKMODEL-001 §2). Minor work / in-SERVICE diagnosis does not move the WO to
  another model (cf. CD-11 §16 Inspection minor-repair note).
- Minor Job guidance (BD-WORKMODEL-001 §6): relatively little time, no special
  equipment, minimal risk, within the visiting technician's capacity. No hour figures,
  thresholds, scores, weights, SLA, or automated duration rules.

## B.5 What this appendix does NOT do

- Does not alter CD-11 lifecycle, approval, closure, evidence, HM, review,
  cancellation, reopen/re-create, publication, reminder, or workspace rules.
- Does not create a Service Type, Work Model, status, outcome, Visit Type, or field.
- Does not create timers, SLA, thresholds, scores, routing, permission, or any
  automatic transition/creation/closure/JOB rule.
- Does not create schema, API, UI, or implementation obligations.

*End of CD-11 Amendment Appendix B.*
