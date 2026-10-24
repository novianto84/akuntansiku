# Architecture Authority Index

**Status:** AUTHORITY INDEX ONLY

## Purpose

This file records the current authority boundary for business decisions and technical architecture. It is an index and governance control document, not a new architecture decision.

## Current Authority Status

| Decision | Status | Canonical source |
|---|---|---|
| CD-01 | FINAL / LOCKED | `docs/10-DECISIONS/CD-01-business-scope.md` |
| CD-02 | DEFERRED / UNVERIFIED | No current canonical document present |
| CD-03 | LOCKED | `docs/10-DECISIONS/CD-03-business-master.md` |
| CD-04 | LOCKED | `docs/10-DECISIONS/CD-04-operational-acquisition-price.md` |
| CD-05 | LOCKED | `docs/10-DECISIONS/CD-05-sales-transaction-quotation.md` |
| CD-06 | LOCKED | `docs/10-DECISIONS/CD-06-vendor-offer-price.md` |
| CD-07 | LOCKED | `docs/10-DECISIONS/CD-07-multi-workspace.md` |
| CD-08 | LOCKED | `docs/10-DECISIONS/CD-08-data-ownership.md` |
| CD-09 | LOCKED | `docs/10-DECISIONS/CD-09-purchasing-transaction-boundary.md` |
| CD-10 | LOCKED | `docs/10-DECISIONS/CD-10-inventory-operational-boundary.md` |
| CD-11 | SIGNED-OFF / LOCKED / CLOSED | `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md` |

CD-11 status was raised from HUMAN-ACCEPTED to SIGNED-OFF / LOCKED / CLOSED by explicit BA SIGN-OFF (CD-11 Business Finalization, CD11-001…CD11-029). This index records that sign-off; it does not itself promote, modify, or reinterpret the decision.

## Technical Architecture

Technical architecture: APPROVED / CANONICAL (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21), covering TADR-01 … TADR-18 and the Architecture Baseline. Architecture direction additionally APPROVED via BUSINESS AUTHORITY — ARCHITECTURE APPROVAL (2026-09-22) per `docs/30-ARCHITECTURE/ARCHITECTURE_APPROVAL_PACKAGE.md` (§1–§12); implementation detail remains explicitly DEFERRED. This index records those approvals; it does not create or modify any architecture decision. No TADR is created or approved by this file.

## Implementation Authorization

**ISSUED 2026-10-03** (HBA-DECISIONS-03 §1). Implementation authorization is issued for work already executed (WP-01…WP-10 backend + internal UI). Work not yet started requires a new authorization before it begins.

## Non-Authority Statement

This file does not create, modify, weaken, expand, reinterpret, or supersede any business decision. The canonical decision documents remain authoritative for their contents. CD-02 must not be reconstructed from evidence or inferred from implementation.
