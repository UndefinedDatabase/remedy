Target: .agent/authored/selfdrive-r5-4-body.md — the PR body actually
published this round.
Operation: FIRST copy the already committed receipt
.agent/authored/selfdrive-r4-4.md to
.agent/authored/selfdrive-r5-4-body.md unchanged, THEN replace FROM
with TO in the COPY. FROM occurs exactly 1x (verify first).
Shape: REWRITE — FROM and TO are disjoint, so the proof is FROM 0x and
TO 1x in the copy after the edit.
Why a copy: selfdrive-r4-4.md is a committed receipt and stays the
record of what was authored; the published body is a separate artifact
and is what `gh pr edit --body-file` consumes.

FROM
<<<FROM
- Open findings: 0. R-0207, R-0208 and R-0209 all Done; next free ID
  R-0210.
- Rounds: 4. Tokens and cost: not-measured — no provider run was
  executed on this branch.
FROM>>>

TO
<<<TO
- Open findings: 0. R-0207, R-0208, R-0209 and R-0210 all Done; next
  free ID R-0211.
- Rounds: 5 — R4's first attempt was stopped by a truncated reviewer
  receipt and reported rather than guessed; nothing was written from
  reconstructed text. Tokens and cost: not-measured — no provider run
  was executed on this branch.
TO>>>
