# Handback — F085 Sandbox hardening (stage 1) — R30

Branch `feature/f085-sandbox-hardening` · Base `f99a8fe2` · HEAD before this
commit `17a3e053`. First round of this block that changes `.py` files.

Fortschritt: ~63 % (T001 gebaut · R13-R29 PASS · T002a KOMPLETT · T002b 7 von 12
Sites auf dem Seam, 5 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

Deviations, declared: this file measures 150 lines against the 100-line cap for a
>5-commit round. Cause is mandated content only — six per-commit tables, the
six-row item-status table, eight gates with real readings and the constraint-8
staleness report. No section dropped, no transcript pasted.

## Range

Review of f99a8fe2..HEAD.

## Commits

### 6e1879bb docs(f085): save the R30 step block (C0a)
| Path | +/- | Reason |
| `.agent/authored/f085-r30.md` | +399/-0 | the block, sha256 fd9117aa… verified before commit |
### 23293d23 docs(f085): mirror the R30 block into last_block (C0b)
| Path | +/- | Reason |
| `.agent/last_block.md` | +317/-224 | written from `git show HEAD:.agent/authored/f085-r30.md` |
### 9668bec4 docs(f085): record the R29 PASS and resolve R-0519 (C1)
| Path | +/- | Reason |
| `.agent/live_review.md` | +58/-0 | RECORD1 appended: R29 gate entry + the R-0519 resolution |
### 10fe9a14 feat(f085): move both post-test spawns onto the guarded test seam (C2)
| Path | +/- | Reason |
| `packages/orchestration/job_promote.py` | +9/-5 | IMPF1→IMPT1, SPAWNF→SPAWNT, OUTF→OUTT |
| `packages/orchestration/pingpong_promote.py` | +10/-5 | IMPF2→IMPT2, SPAWNF→SPAWNT, OUTF→OUTT |
| `tests/orchestration/test_job_promote.py` | +25/-0 | TESTJP appended |
| `tests/orchestration/test_pingpong_promote.py` | +25/-0 | TESTPP appended |
### 17a3e053 docs(f085): advance the plan to R30 (C3)
| Path | +/- | Reason |
| `.agent/plan.md` | +12/-8 | PLANF→PLANT rewrite of Current Step and Next Steps |
### this commit docs(f085): rewrite the handback for R30 (C4)
| Path | +/- | Reason |
| `.agent/handoff.md` | self-reference | a handback cannot table its own commit (R-0149); insertions are in the round report |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | this commit |

## External actions

`git worktree add --detach .remedy-wt/r30red HEAD` → created at 10fe9a14, used
for G6's destructive red proof only. `git worktree remove --force` then
`git worktree prune` → removed before C3; `git worktree list` is one line.
`git push -u origin feature/f085-sandbox-hardening` after C4 — outcome in the
round report. No `gh` command, no PR, no merge.

## Verification

G1 STATE. `ls -la .agent/STOP` → `No such file or directory` before C0a and again
before C4. `git status --porcelain` empty at round start and after all five
commits before C4. `git worktree list` one line at the handback.
G2 TRANSPORT. Committed + working `.agent/authored/f085-r30.md` and committed +
working `.agent/last_block.md`, all four byte-EQUAL at sha256
fd9117aad06382747a59995dbeef4d32d75e14f3f7e3d19af7bc5499dc93b0a2 — 21347 B, 399
lines, 26 marker lines (193, 251, 253, 261, 263, 274, 276, 278, 280, 282, 284,
286, 288, 291, 293, 295, 297, 301, 303, 329, 331, 357, 359, 376, 378, 399),
region digests 1-100 `9e5478bc`, 101-200 `97f12afd`, 201-300 `c6bb8ee5`, 301-399
`d3cf7d6b`.
G3 APPEND SHAPE. Pre-commit blob a byte-exact PREFIX: True. Remainder equals one
blank line plus RECORD1: True. RECORD1's first line occurs 1× among the 58 added
lines. Lines matching `^(BEGIN|END)-[A-Z0-9]+$`: 0 — the bare substring `END-`
hits 10×. numstat `58	0	.agent/live_review.md`.
G4 ARITHMETIC. Base f99a8fe2: 134 registered / 15 done / 0 landed, 119 open, max
R-0519. HEAD: 134 / 16 / 0, 118 open, max R-0519, next free R-0520. Registered
symmetric difference `[]`; done `['R-0519']`; landed `[]`. Duplicate ids 0.
Resolutions naming an unregistered id 0.
G5 MIGRATION PAIRS at HEAD. SPAWNF 0× and OUTF 0× in both `job_promote.py` and
`pingpong_promote.py`; SPAWNT 1× and OUTT 1× in each. Containment measured:
SPAWNF→SPAWNT REWRITE, OUTF→OUTT REWRITE, IMPF1→IMPT1 APPEND-SHAPED, IMPF2→IMPT2
APPEND-SHAPED, PLANF→PLANT REWRITE. IMPT1 1× in `job_promote.py`, IMPT2 1× in
`pingpong_promote.py`; the guard import line occurs 1× among the lines C2 adds to
each. Each new test def occurs 1× among the lines C2 adds to its file. 0 marker
lines in any of the four files. numstat 9/5, 10/5, 25/0, 25/0.
G6 THE MIGRATION IS REAL. Round gate in the PRIMARY checkout `python3 -m pytest
tests/orchestration/test_job_promote.py tests/orchestration/test_pingpong_promote.py
-q -rf` → exit 0, reading `146 passed in 8.67s`; the same command re-measured at
base f99a8fe2 → exit 0, `144 passed in 8.53s`. RED PROOF in the disposable
worktree at 10fe9a14, never in the primary: the five-line guarded call replaced by
the bare `subprocess.run(argv, capture_output=True, text=True, timeout=timeout_sec,
cwd=str(target))` with the decode left standing → `python3 -m pytest
tests/orchestration/test_job_promote.py -q -rf` exit 1, `2 failed, 73 passed in
12.19s`, failures `TestApprovePostTest::test_post_apply_test_runs` and
`test_job_promote_post_test_runs_on_the_guarded_seam`, both raising
`AttributeError: 'str' object has no attribute 'decode'` at
`packages/orchestration/job_promote.py:429`.
G7 LINT AND STATE READERS. `python3 -m ruff check` over the four files as one
command line, repo config, no `--isolated` → exit 0, `All checks passed!`.
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` in the PRIMARY checkout → exit
0, `158 passed in 20.29s`. CANARY `python3 -m pytest tests/cli/test_golden_path.py
-q` → exit 0, `42 passed in 21.76s`. No docs gate: nothing under `docs/` changed.
All four were also run at base BEFORE C2 — exits 0 at `144 passed`, `158 passed`,
`42 passed` and `All checks passed!` — so none was already red.
G8 HYGIENE, measured before C4. `git diff --name-only f99a8fe2..HEAD` holds
exactly the change set minus `.agent/handoff.md`; symmetric difference against the
declared eight `[]`. Per-commit insertions 399, 317, 58, 69, 12 — none over 500;
all five single-parent. `git reflog -10`: 10 entries, all `commit:`.
STALENESS (constraint 8). Re-read after C3: `.agent/authored/f085-r30.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and the four C2
files. One present-tense sentence is now historical and is REPORTED rather than
edited: RECORD1's R29 gate entry says `job_promote.py` and `pingpong_promote.py`
"reference neither symbol" — true of base f99a8fe2, the range that entry is
explicitly scoped to, and false at HEAD, where each references
`run_guarded_test_command` twice. `.agent/f085_inventory.md` carries the same
reading under its own `measured at R29:` label and is outside the change set
(constraint 6), so neither file was touched. Re-derived at HEAD per file: 7 of the
12 `test`-class sites are on the seam and 5 are not — the Fortschritt numbers.

## Authored-text proofs

All thirteen slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f085-r30.md` by their marker pairs and applied byte-verbatim;
none was retyped or taken from the prompt. Each FROM matched at exactly 1 place in
each file it was applied to (measured; see G3 and G5). 0 marker lines reached any
target. The block digest was verified equal to fd9117aa… before C0a and the
committed copy is byte-EQUAL to the source (G2).

## Deviations & assumptions

No departure from the ordered sequence C0a · C0b · C1 · C2 · C3 · C4: none extra,
none dropped, none reordered. The C2 pairs were dry-run against throwaway copies
under gitignored `.remedy-wt/r30dry/` before any primary-checkout edit; that
directory is scratch and is not part of the change set. Length overage declared at
the top of this file.

## Next

Next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
R30's own verdict is NOT a §4.13 terminator: this branch continues. The next
reviewed round records R30's gate entry in `.agent/live_review.md`. Open findings:
118. Then T002b remainder — `pingpong_loop.py`:3537 first, per `.agent/plan.md`
Next Steps item 1.
