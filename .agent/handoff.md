# Handback — F085 R42 (session-closing round)

F085 sandbox hardening · R42 · branch feature/f085-sandbox-hardening · base 0e2cdacd ·
open findings 124 (122 + R-0535 + R-0536, nothing resolved) · counts are `splitlines`.

## Range
Review of 0e2cdacd..HEAD.

## Commits
### e993e64f docs(f085): save the R42 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r42.md | +332/-0 | C0a — block saved byte-for-byte |
### 7b02da1c docs(f085): mirror the R42 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +273/-339 | C0b — identical bytes mirrored |
### dc34997a docs(review): record the R41 PASS and register R-0535 and R-0536
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +72/-0 | C1 — RECORD10 appended |
### 5695c2b0 docs(f085): rule DECISION F085 D4 for the ci_run migration
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +61/-0 | C2 — DEC4 appended |
### 7c4a2583 docs(f085): advance the plan to R42
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +7/-8 | C3 — PLANF10 to PLANT10 rewrite |
### this commit docs(f085): rewrite the handback for R42
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handoff cannot table its own commit (R-0149) |

| Item | C0a | C0b | C1 | C2 | C3 | C4 |
|---|---|---|---|---|---|---|
| Status | done | done | done | done | done | done (this commit) |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C4. No PR, no merge, no gh
command, no worktree added or removed.

## Verification
G1 `ls -la .agent/STOP` exit 2, "No such file or directory", before C0a and again before
C4. `git status --porcelain` empty at round start and after each of C0a-C3.
`git worktree list` one line throughout.
G2 TRANSPORT, disk-to-disk, five reads all byte-EQUAL — committed authored and committed
last_block at 7b02da1c, both working copies, `.remedy-wt/f085-r42.md`: sha256
b6ba33717b92a47ea970148d9cca0d082e95acd464c6631dc9c55b50f7161c25, 23195 B, 332 lines,
8 marker lines; region 1-100 sha 3bc171fb05e29fa9 / 6720 B, region 101-end sha
d0ad2b78183925d3 / 16475 B, reassembling to the whole (True for each of the five).
G3 APPEND SHAPE, per file.
- `.agent/live_review.md`, C1 dc34997a: pre 420193 B is a byte-exact PREFIX of post
  426006 B; remainder 5813 B is exactly one blank line plus the slice; slice an exact
  suffix; RECORD10 sha256 407c8ff2e3c61ac6…, 5812 B, 71 lines, 3 empty (exempt); 0 lines
  matching `^(BEGIN|END)-[A-Z0-9]+$` in the file; each of the 68 non-empty slice lines
  occurs exactly once among the 72 added, and added == blank + slice IN ORDER.
  numstat 72  0  .agent/live_review.md
- `.agent/decisions.md`, C2 5695c2b0: pre 358646 B PREFIX of post 363135 B; remainder
  4489 B is one blank line plus the slice; exact suffix; DEC4 sha256 fa6f2e9fd40c883f…,
  4488 B, 60 lines, 6 empty (exempt); 0 marker LINES; each of the 54 non-empty slice lines
  occurs exactly once among the 61 added, ordered equality holds.
  numstat 61  0  .agent/decisions.md
G4 ARITHMETIC, from the line-start patterns. 0e2cdacd 149 / 27 / 0, 122 open, max
registered R-0534, max resolved R-0532; HEAD 151 / 27 / 0, 124 open, max registered R-0536,
max resolved R-0532. Registered symmetric difference exactly R-0535 and R-0536; done and
landed symmetric differences empty; 0 duplicate ids; 0 resolutions naming an unregistered
id; next free id R-0535 → R-0537.
G5 `^## DECISION F085 D\d+ —` counts 2 at 0e2cdacd, 3 at HEAD, `## DECISION F085 D4 —`
exactly 1x; no `## DECISION F085 D1` section at either SHA, as the block states. Headings:
  ## DECISION F085 D2 — the streaming seam takes the guard's CHILD half, not `run_guarded` (2026-08-17)
  ## DECISION F085 D3 — the `test`-class seam gains an `extra_env` overlay (2026-08-17)
  ## DECISION F085 D4 — the `ci_run.py` stage spawn migrates with output re-emitted and the wall as a backstop (2026-08-17)
G6 THE PLAN at 7c4a2583: PLANF10 0x, PLANT10 1x; 45 lines against the 50-line cap;
`## Goal` and `## Next Steps` present; 0 marker lines; PLANF10 matched at exactly 1 place
before C3. numstat 7  8  .agent/plan.md
G7 SUITES, both in the primary checkout /home/decodeux/Repos/remedy, neither in a worktree.
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` → `159 passed in 20.24s`, exit 0
  (base 159).
- `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 20.26s`, exit 0
  (base 42).
G8 HYGIENE. `git diff --name-only 0e2cdacd..HEAD` before C4 holds exactly
.agent/authored/f085-r42.md, .agent/decisions.md, .agent/last_block.md,
.agent/live_review.md, .agent/plan.md — the change set minus .agent/handoff.md, nothing
else. Insertions before C4: 332, 273, 72, 61, 7, none over 500; C4's own are in the round
report. Every commit single-parent; `git reflog -10` 10 entries, 0 non-`commit:`.

## Authored-text proofs
All four slices extracted programmatically from the committed `.agent/authored/f085-r42.md`
at 7b02da1c by marker pair. RECORD10 sha256 407c8ff2e3c61ac6…, DEC4 sha256
fa6f2e9fd40c883f…, PLANF10 988 B / 15 lines, PLANT10 978 B / 14 lines. Pair shape measured:
`TO contains FROM` is False, so PLANF10→PLANT10 is a REWRITE reading FROM 1x → 0x, TO 0x →
1x. 0 marker lines reached any target file.

## Deviations & assumptions
COMMIT SEQUENCE: no departure — C0a, C0b, C1, C2, C3, C4 in order, none extra or dropped.
CONSTRAINT 8, measured at 7c4a2583 over the five files this round edited:
- RECORD10's transport clause survives C0b, which overwrote `.agent/last_block.md` BEFORE
  RECORD10 landed: it qualifies the working copies "as they stand at 0e2cdacd", and all
  five copies read a3716bdf9fa2… / 28265 B / 398 lines / 14 markers at that SHA. The
  R-0535 shape, handled correctly.
- RECORD10's plan clause survives C3, which took PLANT9 1x → 0x: that reading is qualified
  "at 0e2cdacd", and its trailing UNQUALIFIED readings still hold at HEAD — `## Goal` and
  `## Next Steps` present, 0 marker lines, bb07a759 numstat 4/3.
- RECORD10's arithmetic clause carries a SHA on both readings and states no next-free id,
  so C1 cannot falsify it; its trailing readings (0 duplicate ids, 0 orphan resolutions)
  hold at HEAD. Hygiene clause likewise: reflog -10 still 0 non-`commit:`, worktree list
  one line, insertions 398/361/102/14/49/4/101 re-measured exact, seven commits
  single-parent, checklist labels contiguous 1..20 at 93226220 and 1..22 at 0e2cdacd.
- DEC4 and PLANT10: nothing falsified. No `.py` is in the round diff, so DEC4's code claims
  could not be; spot-checked true at HEAD (`_run_via_subprocess` and the quoted
  `subprocess.run(...)` form in `packages/orchestration/ci_run.py`,
  `tests/orchestration/test_ci_run.py` tracked and naming it, dce66faa touching
  `extra_env`).
DECLARED, NOT FIXED (constraint 9): R-0536's closing sentence, landed this round at
dc34997a, reads "Measured at 0e2cdacd with `splitlines`: 706, 643 and 46." Measured:
`docs/agents/planner_reviewer_prompt.md` is 706 at 0e2cdacd and 643 at 93226220;
`.agent/plan.md` is 46 at 0e2cdacd. The 643 is a reading at 93226220, so the sentence's
single SHA qualifier over-reaches one of its three values — the mis-scoped-qualifier shape
R-0534 and R-0535 register, recurring inside the finding that registers a
measurement-convention defect. Positional mapping onto the three quoted predictions
recovers the intent and nothing false about the repository follows; left as it landed.
R-0536's quotations of the R41 block are faithful: it reads "707 lines at HEAD against 644
at 93226220" (wrapped) and "put it at 47 lines".
CAP, DECISION D15 stated cause: 153 lines against the 100-line >5-commit cap. The overage
is mandated content only — six per-commit tables, the eight-gate transcript with its exact
command lines and the three headings G5 orders reported verbatim, the authored-text proofs,
the constraint-8 measurement with its declared finding, and the two verbatim texts below.
No section dropped, no transcript padded.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). R42's own verdict is NOT a §4.13 terminator,
because this branch continues. The next reviewed round records R42's gate entry.

  R43 applies DECISION F085 D4 to `packages/orchestration/ci_run.py`: `_run_via_subprocess`
  moves onto `run_guarded_test_command`, the per-stage budget travels through the
  `extra_env` overlay that landed at dce66faa, the captured stdout and stderr are re-emitted
  to the console before returning, and the guard's wall is set ABOVE `stage.timeout_sec` as
  a backstop so the child's own 124 exit code stays the operative timeout. D4 leaves the
  size of that grace margin to R43 and says why. R43 owes three tests it does not have
  today: that the captured output reaches the console, that the budget still arrives in the
  child, and that a wall trip maps to the `timed out` note.
  `packages/orchestration/builder_bridge.py` follows; then T002c-d, then T003 and the
  integration gate.

Fortschritt: ~77 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R41 PASS
· T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, Design für ci_run.py als DECISION
F085 D4 gerulet, R43 setzt es um · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
