# SR V2 Future Note — Canonical Intake Object (BACKLOG, NON-NORMATIVE)

```text
Status: FUTURE / V2 BACKLOG — NOT LOCKED, NOT A DECISION
Scope: idea parking only. No business rule, no field, no schema, no workflow,
  no approval, and no implementation is established by this note.
Authority: BA idea (O-10 handprompt V2 Future Note). Requires a future BA decision
  before any of it becomes normative.
```

## Idea

In V2, SR may become the canonical intake object for multiple channels:

- Customer Portal
- Landing Page
- WhatsApp
- QR-triggered Request
- Email
- Internal users
- Future external channels

Conceptual flow (future):

```text
Customer / PIC
     │
     ├── Portal
     ├── Landing Page
     ├── WhatsApp
     ├── QR Unit
     └── Other Channel
             │
             ▼
            SR
             │
       Follow-up / Review
             │
             ▼
            WO
             │
            JOB
```

## Constraints carried forward

- All channels yield the **same SR concept**. Never create per-channel entities
  (`WhatsApp Request`, `Landing Page Request`, `QR Request`, `Customer Request`, …).
- V1 decisions stay intact: SR is internal-only, no external intake, no portal SR,
  no channel integration (O-10 TASK 9 exclusions).

## Evaluate only in V2 (not now)

Request source/channel taxonomy; requester identity for external reporters;
company/customer context resolution; unit context from QR/portal; external intake
validation and abuse handling; automation; AI-assisted intake. No fields for any of
this are created now to anticipate V2.

*End of V2 future note. STOP — awaiting future BA instruction.*
