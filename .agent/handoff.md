# Handback — F085 Sandbox hardening, R31

Branch: feature/f085-sandbox-hardening. Base SHA: d4fe1674.
Fortschritt: ~67 % (T001 gebaut · R13-R30 PASS · T002a KOMPLETT · T002b 8 von 12
Sites auf dem Seam, 4 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

## Range

Review of d4fe1674..HEAD.

## Commits

### 8149fa06 docs(f085): save the R31 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r31.md | +352/-0 | C0a, block saved byte-for-byte |

### 00a34d16 docs(f085): mirror the R31 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +174/-221 | C0b, mirror of the committed blob |

### f7f8914c docs(review): record the R30 PASS and register R-0520
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +67/-0 | C1, RECORD1 appended verbatim |

### 11ebcc80 feat(f085): move the pingpong loop test spawn onto the guarded seam
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_loop.py | +9/-5 | C2, SPAWNF→SPAWNT, OUTF→OUTT, IMPF→IMPT |
| tests/orchestration/test_pingpong.py | +25/-0 | C2, TESTPL appended |

### fddff602 docs(f085): advance the plan to R31
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +5/-8 | C3, PLANF→PLANT |

### (this commit) docs(f085): rewrite the handback for R31
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | round report | C4 cannot table itself (R-0149) |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

`git worktree add --detach .remedy-wt/r31red HEAD` → created at 11ebcc80 (G6).
`git worktree remove --force` + `git worktree prune` → gone before C3;
`git worktree list` is one line. `git push -u origin feature/f085-sandbox-hardening`
— outcome in the round report. No PR, no merge, no gh command.

## Verification

G1 STATE. `.agent/STOP` absent before C0a and again before C4 (`ls` → No such
file). `git status --porcelain` empty at round start and after every commit.
`git worktree list` one line at the handback.

G2 TRANSPORT. The committed authored file, the committed `.agent/last_block.md`,
both working copies and the source file are all five byte-EQUAL: sha256
9023be74ce151bf00b833090c733fe9f77210a50519f4c14790f615adc6cf2a4, 20195 B, 352
lines, 20 marker lines; regions 1-100 def02d5c, 101-200 afd442cb, 201-352 b083f1bd.

G3 APPEND SHAPE (C1). Pre-commit blob is a byte-exact PREFIX (True); remainder is
exactly one blank line + RECORD1 (5193 = 1 + 5192 B, True); RECORD1's first line
1× among the 67 added lines; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` (substring
`END-` 11×). `git show --numstat f7f8914c` → `67 0 .agent/live_review.md`.

G4 ARITHMETIC. Base d4fe1674: 134 registered / 16 done / 0 landed, 118 open, 0
duplicate ids, 0 resolutions naming an unregistered id, max R-0519, next free
R-0520 — reproduces the ordered base reading. HEAD: 135 / 16 / 0, 119 open, 0
duplicates, 0 unregistered resolutions, max R-0520, next free R-0521. Registered
symmetric difference `['R-0520']`; done and landed both `[]`.

G5 MIGRATION PAIRS at HEAD, in `pingpong_loop.py`: SPAWNF 0×, OUTF 0×, SPAWNT 1×,
OUTT 1×, IMPT 1× (IMPF is a prefix of IMPT, so no whole-file FROM count — constraint
2). `from packages.orchestration.exec_guard import run_guarded_test_command` 1×
among C2's added lines to that file;
`def test_pingpong_loop_test_command_runs_on_the_guarded_seam(tmp_path, monkeypatch):`
1× among C2's added lines to the test file; 0 marker lines in either.
`git show --numstat 11ebcc80` → `9 5 packages/orchestration/pingpong_loop.py`,
`25 0 tests/orchestration/test_pingpong.py`.

G6 ROUND GATE + RED PROOF. Primary checkout:
`python3 -m pytest tests/orchestration/test_pingpong.py -q -rf` → exit 0,
`34 passed in 0.79s` (a reading, not a target; base d4fe1674 was 33 passed).
RED PROOF in the disposable worktree `.remedy-wt/r31red` at 11ebcc80, never in the
primary checkout: the five-line `run_guarded_test_command(` call matched 1× and
became the bare
`subprocess.run(argv, capture_output=True, text=True, timeout=timeout_sec, cwd=str(staging))`
with the decode line left standing. Same command → exit 1, `1 failed, 33 passed in
1.04s`. Failing node
`tests/orchestration/test_pingpong.py::test_pingpong_loop_test_command_runs_on_the_guarded_seam`,
exception `AttributeError: 'str' object has no attribute 'decode'. Did you mean:
'encode'?` at `packages/orchestration/pingpong_loop.py:3549`.

G7 LINT AND STATE READERS, all in the PRIMARY checkout.
`python3 -m ruff check packages/orchestration/pingpong_loop.py tests/orchestration/test_pingpong.py`
(repo configuration, no `--isolated`) → exit 0, `All checks passed!`.
`python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`
→ exit 0, `158 passed in 19.84s` (base 158; R-0518's `test_vitest_passes` red did
NOT occur). CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0,
`42 passed in 20.32s`. No docs gate: nothing under `docs/` changed.

G8 COMMIT HYGIENE, before C4. `git diff --name-only d4fe1674..HEAD` → exactly
`.agent/authored/f085-r31.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `packages/orchestration/pingpong_loop.py`,
`tests/orchestration/test_pingpong.py` — the declared set minus `.agent/handoff.md`,
nothing else. Per-commit insertions 352, 174, 67, 34, 5; none exceeds 500; C4's own
is in the round report. All five are single-parent; `git reflog -10` holds only
`commit:` entries.

STALENESS (constraint 8). Re-read at HEAD: the authored file and `last_block.md`
(still byte-equal), `live_review.md`, `plan.md`, `pingpong_loop.py`,
`test_pingpong.py`. R-0520's text survives C2 — it names d4fe1674 in the sentence,
and `job_promote.py` and `pingpong_promote.py` reference `run_guarded_test_command`
2× each at BOTH d4fe1674 and HEAD, C2 touching neither. PLANT's four remaining
sites are still bare at HEAD: `builder_bridge.py`:220, `ci_run.py`:79,
`integrity_gate.py`:283, `mission_state.py`:833 each show `subprocess.run(` with 0
guard references; `pingpong_loop.py`:3537 is correctly gone from the plan. No
sentence this round put on disk was falsified by a later commit of the round.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f085-r31.md` by BEGIN-/END- marker pair — never retyped, never
taken from the prompt. sha256 (first 12): RECORD1 b314db9c6ad3 (5192 B), SPAWNF
4880de1c4d8c, SPAWNT 4b00b3c594fa, OUTF 636de4dfa7c1, OUTT cfb4a03724fe, IMPF
37f58e93625c, IMPT 225acdb277e2, TESTPL b72084ce889e, PLANT 59d8979450b5. Each
FROM matched exactly ONE place in its target: SPAWNF, OUTF, IMPF, PLANF all 1×.
Disk-to-disk: the committed authored file equals the source byte-for-byte (G2).

## Deviations & assumptions

No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 ran in
that order, one commit each, none extra and none dropped.
Declared: (a) this handback is 162 lines against the 100-line cap; the cause is
mandated content — six per-commit tables, the item-status table, eight gate
transcripts with exit codes and the staleness sweep. No section was dropped to
meet it (AGENTS.md D15). (b) Before C2 the three pairs were dry-run against
throwaway COPIES of the two targets in a gitignored scratch dir
(`.remedy-wt/r31apply` — not a git worktree, no git operation) to confirm each
FROM matched once and ruff stayed green; the dir was deleted, nothing committed.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from
disk — BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
R-0520 is OPEN and awaits the next reviewed round's authored resolution: this
round registered it and resolved nothing, so the done set is unchanged at 16.
R31's own verdict is NOT a §4.13 terminator, because this branch continues.
The next reviewed round records R31's gate entry in `.agent/live_review.md`.
Expected next action: the reviewer gates d4fe1674..HEAD and re-runs G1-G8.
