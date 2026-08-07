Target: .agent/plan.md
Round: R5. Operation: two independent replacements. Each FROM occurs
exactly 1x (verify both before editing). Apply in the order given.

PAIR 1 — the header state line. Shape: REWRITE (FROM 0x after, TO 1x).

FROM
<<<FROM
manual-review window. R1, R2 and R3 all PASSed; 0 open findings; next
free finding ID R-0211 — R-0210 was raised and fixed in R4.
FROM>>>

TO
<<<TO
manual-review window. R1 through R4 all PASSed; 0 open findings; next
free finding ID R-0211 — R-0210 was raised and fixed in R4. R5 is the
S4 rehearsal session's opening round.
TO>>>

PAIR 2 — the current step. Shape: REWRITE (FROM 0x after, TO 1x).

FROM
<<<FROM
## Current Step
Build complete. The only remaining commitment before the hard date is
the S4 rehearsal.
FROM>>>

TO
<<<TO
## Current Step
R5 — the S4 rehearsal session's opening round: record the R4 PASS
verdict in .agent/live_review.md so the build's evidence chain is
closed before PR #185 is merged. This round performs no merge and
creates no branch; the Open PR Gate is the next round's first action.
TO>>>
