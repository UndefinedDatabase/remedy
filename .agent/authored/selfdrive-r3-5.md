Target: .agent/live_review.md
Operation: three independent replacements. Each FROM occurs exactly 1x
(verify all three before editing).
Apply PAIR 1 only after AGENTS.md and docs/README.md are corrected, and
PAIRS 2 and 3 only after every fix in this round is on disk — a Done
line must never be true before its fix.

PAIR 1 — the R-0208 fix itself. Shape: REWRITE (FROM 0x, TO 1x after).

FROM
<<<FROM
  (breaks the ROADMAP.md Part C grammar and the 250-item ledger
FROM>>>

TO
<<<TO
  (breaks the ROADMAP.md Part C grammar and the 255-item ledger
TO>>>

PAIR 2 — mark R-0208 done. Shape: APPEND (FROM 1x, TO-only line 1x).

FROM
<<<FROM
  decision itself is unaffected (the pins reject an invented line at
  either count), but a wrong number persisted in a decision record is
  exactly the class this project polices. Fix: correct the number in
  D7.
FROM>>>

TO
<<<TO
  decision itself is unaffected (the pins reject an invented line at
  either count), but a wrong number persisted in a decision record is
  exactly the class this project polices. Fix: correct the number in
  D7.
  Done: R-0208 — D7 now reads 255-item.
TO>>>

PAIR 3 — mark R-0209 done. Shape: APPEND (FROM 1x, TO-only line 1x).

FROM
<<<FROM
  README.md line 89 ("Roadmap (250 features + registered items)") is
  a DIFFERENT and still-true statement — F001-F250 plus the five
  later registered items — and is deliberately not touched.
FROM>>>

TO
<<<TO
  README.md line 89 ("Roadmap (250 features + registered items)") is
  a DIFFERENT and still-true statement — F001-F250 plus the five
  later registered items — and is deliberately not touched.
  Done: R-0209 — both texts corrected and pinned in one commit.
TO>>>
