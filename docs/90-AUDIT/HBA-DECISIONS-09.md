# HBA DECISION RECORD — IS-06 status RECORDED-LOCKED, serving topology EMBEDDED, eksekusi diotorisasi (2026-10-07)

```text
Record ID:      HBA-DECISIONS-09
Date:           2026-10-07
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decisions as stated by HBA in group chat 2026-10-07
Classification: Audit record. NOT a canonical specification document.
Implementation: Execution of C-3 and C-2/C-5 work packages is AUTHORIZED by HBA in this
                record (item 3); the record itself writes no code.
```

---

## Decisions (verbatim intent)

1. **IS-06 status header**: HBA ordered the header changed to **RECORDED-LOCKED**. Applied to
   `docs/40-SPECIFICATION/IS-06-customer-projection-portal.md` under explicit HBA authorization.
2. **Serving topology**: HBA chose **EMBEDDED (menyatu)** for the current phase — "embedded saja
   untuk saat ini. nanti kita akan bahas lagi setelah proyek V1 ini sudah running dan bisa
   digunakan." Locked. Revisit is scheduled by HBA only after V1 is running and usable.
3. **Execution**: HBA ordered **"kunci keputusannya. dan eksekusi!"** — this authorizes starting
   the governed execution of the already-locked work packages:
   - C-3 full workspace-isolation fix (card `t_9fdb5c92`, HBA-DECISIONS-07)
   - C-2 general event store + C-5 acknowledge fix (card `t_074bbe2c`, HBA-DECISIONS-08)

### Previously locked portal decisions (HBA-DECISIONS-08, unchanged)

- Portal MUST NOT display prices (acquisition price and other prices in any form).
- Portal login/signup is Google-only.
- Publication/serving mechanism (IS-06 O-01/O-02) remains OPEN — architecture work, not a
  business blocker for embedded serving.

## Applied edits

- `IS-06-customer-projection-portal.md` — status header updated to RECORDED-LOCKED (per item 1).
- `DECISION_REGISTER.md` — rows added for IS-06 serving topology (EMBEDDED locked) and the
  HBA-DECISIONS-08 cluster.

## Not decided by this record

- IS-06 publication/serving mechanism (O-01/O-02) — OPEN, deferred architecture task.
- Post-V1 revisit of embedded-vs-separate (scheduled by HBA after V1 is running).

*End of decision record.*
