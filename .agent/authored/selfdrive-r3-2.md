Target: AGENTS.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).
Shape: REWRITE — FROM and TO are disjoint, so the proof is FROM 0x and
TO 1x after the edit.
Note: FROM is a SUBSTRING of its line, not the whole line. The line ends
with two spaces (a markdown hard break) that must survive the edit
untouched — that is why the pair stops before them.

FROM
<<<FROM
(ROADMAP.md + 250 feature detail files)
FROM>>>

TO
<<<TO
(ROADMAP.md + 255 feature detail files)
TO>>>
