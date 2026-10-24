# IS-08 APPROVAL & UI BUILD DECISIONS — RECORD

```text
Record ID:      IS08-APPROVAL-DECISIONS-01
Date:           2026-10-01
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         DECISIONS RECORDED as stated by HBA in session 2026-10-01
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution tracked in §5.
```

> Records the HBA decisions that unblock the UI workstream. Does not itself modify
> IS-08, IS-06, or any canonical document — that is a separate authorized act.

---

## 1. Decision — Portal scope (was Finding 1, P1)

**HBA decision: A — approve IS-08 as-is; the customer portal is DEFERRED to a later
increment.**

What this settles:

| Aspect | Outcome |
|---|---|
| IS-08 scope | Unchanged — internal UI behaviour only |
| Customer/PIC portal UI | **Not built in this increment** |
| IS-06 (portal specification) | Remains DRAFT; not approved in this act |
| Conflict with the earlier "portal included" answer | **Resolved in favour of the specification** — the portal moves to a later increment |

The earlier session answer (portal included in the first build) is superseded by this
decision. The deferral keeps implementation behind the specification gate.

---

## 2. Decision — Build authorization (was Finding 2, P2)

**HBA decision: grant UI build authorization.**

Two acts are therefore both in force, and they remain distinct:

| Act | State |
|---|---|
| Approve IS-08 | **GRANTED** |
| Authorize UI build | **GRANTED** |

Per IS-00 §13 these are separate acts; HBA has issued both. The build proceeds within
the approved IS-08 behaviour, and the boundary that approval alone grants nothing is
preserved in the record.

---

## 3. Decision — Technology stack (was Finding 4, P3)

**HBA decision:**

| Layer | Decision | Nature |
|---|---|---|
| Application architecture | **React + TypeScript** | Architecture decision |
| Build tooling | **Vite** | Tooling decision |
| Styling | **CSS + design tokens** | Styling decision |
| Tailwind / shadcn | **Conditional — only if demonstrably beneficial** | Deferred, evidence-gated |

Key point preserved: **architecture and styling are separate decisions.** React is not
bundled with Tailwind. The styling decision is "plain CSS driven by design tokens";
Tailwind/shadcn may be added later only on demonstrated benefit, and adding them must
not require re-deciding the architecture.

Consequence: the first screens can be built with zero styling dependencies — consistent
with the backend's zero-dependency posture.

---

## 4. Pending — Finding 3 (deviation log)

HBA stated the item was not understood. Re-explained in plain language in session
2026-10-01. Decision still open; see the explanation record below.

### Plain-language restatement

The master specification document (`IS-00`) promised that the UI specification
(`IS-08`) would carry one extra section — a **deviation log**. A deviation log is a
short list recording: *"a design prototype showed something that conflicted with, or
asked a question about, a business rule — here is the question and here is how it was
settled."* The stated purpose was to guarantee that a design mockup can never silently
override a business rule.

Reality found by audit:

| Promised | Actual |
|---|---|
| A deviation log section inside IS-08 | **Absent** |
| A Figma prototype whose questions it would log | **Does not exist** in the repository |

So the promise was not kept, but the thing it was meant to guard against never
occurred. Nothing is broken.

### Options

| Option | Action | Effect |
|---|---|---|
| **A (recommended)** | Add one line to IS-08 recording that no prototype deviation arose, so the deliverable is accounted for | IS-08 becomes v1.1; the gap closes |
| **B** | Leave IS-08 exactly as approved | The promise stays unaccounted for in the document; recorded here as a known, non-blocking gap |
| **C** | Author a full deviation-log section | Only meaningful if a prototype exists — none does |

Option A is a one-line documentation completeness fix, not a business decision.

---

## 5. Execution status

| Item | State |
|---|---|
| IS-08 status change to APPROVED | **NOT YET EXECUTED** — pending Finding 3 outcome so a single controlled edit covers both |
| UI build start | **AUTHORIZED** — may begin once IS-08 is materialized |
| Portal work | **DEFERRED** |
| Styling dependencies | **None** for the first increment |

---

## 6. Boundary

This record:
- modified no document;
- changed no document status;
- created no business decision;
- authorized nothing beyond what HBA stated above.

*End of decision record.*
