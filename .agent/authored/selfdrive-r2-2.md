Target: docs/agents/planner_reviewer_prompt.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).
Shape: APPEND — the TO contains the FROM verbatim, so the proof is
FROM 1x plus the TO-only paragraph 1x. Do NOT claim FROM 0x.

FROM
<<<FROM
   digests recorded in the reviewer's own emitted block; the verdict
   text states that the fallback was used, so the evidence chain
   stays honest. cmp-against-scratchpad remains the primary proof
   whenever the originals exist.
FROM>>>

TO
<<<TO
   digests recorded in the reviewer's own emitted block; the verdict
   text states that the fallback was used, so the evidence chain
   stays honest. cmp-against-scratchpad remains the primary proof
   whenever the originals exist.
   Two proof shapes, never one (R-0207, S1+S2 R1): a FROM→TO pair is
   a REWRITE when FROM and TO are disjoint, and APPEND-shaped when
   the TO contains the FROM verbatim — the normal form for adding a
   table row, a list item or a numbered sub-point. Order the
   "FROM 0x, TO 1x" proof only for a rewrite. For an append-shaped
   pair that count is unattainable by construction, and demanding it
   invites either a fabricated number or a pointless repair round;
   the obligation there is FROM exactly 1x plus each TO-ONLY
   addition exactly 1x. The reviewer states which shape each pair is
   at authoring time, in the receipt itself.
TO>>>
