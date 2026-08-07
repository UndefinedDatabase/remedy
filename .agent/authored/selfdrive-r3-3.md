Target: docs/README.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).
Shape: REWRITE — FROM and TO are disjoint, so the proof is FROM 0x and
TO 1x after the edit.
Note: FROM is a SUBSTRING of its line; the line continues after it.

FROM
<<<FROM
the full 250-feature
FROM>>>

TO
<<<TO
the full 255-feature
TO>>>
