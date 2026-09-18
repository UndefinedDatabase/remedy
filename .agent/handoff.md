# Handoff — F268 remedy do: the one-command start · Round 7 (T005 + R-0892 docs half)

## Session

SESSION 2 of feature F268 · round 7 · rounds so far 7

## Range

Review of 8746b21e..HEAD — branch `feature/f268-remedy-do`.

## Summary

The round landed C1 (bookkeeping: round 6's verdict booked, DECISION F268 D15 recorded, plan), C2 (T005: the five-line quick start in `remedy --help` and the README, with the four pins it turned red rewritten to the new lines) and C3 (the test that runs the printed lines). C4 (R-0892's SKILL.md half) is SKIPPED: the permission system refused both the Write and the Edit tool on `.claude/skills/remedy-evidence-review/SKILL.md`; per the block, no shell route was tried, and an operator question (kind A) is added in this commit.

- **C2 (a)/(b).** `_QUICK_START` in `apps/cli/grouped.py` and the Quickstart fence of `README.md` are the payload bytes (G1: each contained exactly once). The rendered help prints, after the command box: `Quick start (in a git repository):`, the five lines `  1. remedy init` … `  5. remedy job list`, a blank line and `Show all commands:  remedy --all-commands`.
- **C2 (c), measured before rewriting:** with (a) and (b) applied, `tests/cli/test_cli_ux.py tests/test_cli_execution_loop_closure.py tests/cli/test_advertised_commands.py tests/docs/` read `4 failed, 426 passed` — exactly the four pins the block names. Rewrites:
  - `TestHappyPath::test_happy_path_in_help`: `"do run"`/`"job show"` in the help → `'remedy do "Write a CONTRIBUTING.md"'`/`"remedy job list"` in the help.
  - `TestQuickStart::test_quick_start_has_auto_job_id` → renamed `test_quick_start_needs_no_job_id` (see Deviations): `"  5. remedy job list\n"` in the help, and none of `JOB_ID`, `$`, `job_id` in it.
  - `TestQuickStart::test_quick_start_no_manual_job_id`: `re.findall(r"<[a-z_-]+>", …) == ["<goal>"]` → `re.findall(r"<[^>]*>", _QUICK_START) == []` (no placeholder of any spelling); the `<job_id>` assertion kept.
  - `TestDocsHelpReviewMemoryCommands::test_quick_start_updated`: same substitution as the happy-path test, on `_QUICK_START`.
  - `test_quick_start_has_tee` → replaced by `test_quick_start_has_exactly_five_numbered_lines` (numbers read by `^  (\d+)\. (remedy .*)$` equal `[1, 2, 3, 4, 5]`).
  - `test_quick_start_flags_are_declared_by_their_commands` rewritten: every numbered line is `shlex.split`, its group resolved with `resolve_group`, the pair taken from the next word when it is a subcommand of the group and otherwise from `apps.cli.grouped._DEFAULT_COMMAND` (a group with no default fails the test); every `-`-prefixed word after the pair must be declared by that catalog entry; the resolved pairs must equal `[("init","run"), ("doctor","core"), ("do","run"), ("do","run"), ("job","list")]`.
- **C3.** `tests/cli/test_quick_start.py`: the `repo` fixture and `no_model_call` tripwire of `test_do_sequence_cli.py`, plus a `builtins.input` tripwire. `test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it` reads the numbered lines from `main([])`'s output, runs each through `main(shlex.split(line)[1:] + suffix-if-do)`, and asserts the exit codes are `[0, 0, 0, 0, 0]` (SystemExit `None` → 0) and `git status --porcelain` after line 5 equals the reading after line 1. `test_each_line_runs_with_its_printed_words_and_only_a_do_line_gets_the_suffix` runs the same runner with a recorder and asserts each executed argv starts with the printed words, a `do` line's tail equals the literal suffix list, every other line's argv equals its words, and there are exactly two `do` lines. A scratch probe of the fixture after line 5 (basetemp under `.remedy-wt/`, removed) read `?? .remedy/` and `?? remedy.toml`, matching D15's measurement.

## Commits

### dfb8cb46 F268 R7 C1: bookkeeping — book round 6's verdict, record DECISION F268 D15, round 7 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r7-block.md` | +115 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r7-decisions.md` | +23 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r7-ledger.md` | +2 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r7-plan.md` | +26 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r7-quickstart_to.txt` | +9 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r7-readme_to.txt` | +7 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r7-skill.md` | +71 / -0 | Byte copy of the payload (for the operator, C4 skipped) |
| `.agent/decisions.md` | +23 / -0 | `git show 8746b21e:` bytes + decisions.md (append) |
| `.agent/live_review.md` | +2 / -0 | `git show 8746b21e:` bytes + ledger.md (append) |
| `.agent/plan.md` | +4 / -4 | := plan.md payload |

### db2629bc F268 R7 C2: T005 — remedy --help and the README carry the five-line quick start of DECISION F268 D15; the pins it turns red assert the new lines
| Path | +/- | Reason |
|------|-----|--------|
| `README.md` | +5 / -8 | Quickstart fence := readme_to.txt |
| `apps/cli/grouped.py` | +8 / -6 | `_QUICK_START` assignment := quickstart_to.txt |
| `tests/cli/test_cli_ux.py` | +38 / -22 | C2 (c): the three red `TestHappyPath`/`TestQuickStart` pins rewritten; `test_quick_start_has_tee` replaced; the flags test rewritten; module constant `_NUMBERED_LINE` |
| `tests/test_cli_execution_loop_closure.py` | +2 / -2 | C2 (c): `test_quick_start_updated` asserts the new lines |

### f638e910 F268 R7 C3: T005 test — every quick-start line printed by remedy --help exits 0 on a fixture repository and leaves the target as line one left it (DECISION F268 D15)
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_quick_start.py` | +134 / -0 | New: the two tests of C3 |

### C4 — not made
The permission system refused the write (see Deviations). No commit.

### (this commit) F268 R7 C5: handoff — round 7
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |
| `.agent/operator_questions.md` | appended | Q2, kind (A): the operator applies the SKILL.md payload (C4-refused case) |

## External actions

- G4: `git worktree add --detach .remedy-wt/f268-r7-g4 f638e910` (exit 0); removed with `git worktree remove .remedy-wt/f268-r7-g4` (exit 0) after its `git status --porcelain` read empty.
- Scratch probe of the C3 fixture with `--basetemp=.remedy-wt/f268-r7-probe`, directory removed with `shutil.rmtree` on that exact path.
- `git push` after this commit (no force); outcome and G5 in the round report.
- No PR create, edit or merge.

## Verification

All runs at `f638e910` (C3; C4 skipped). C5 changes only `.agent/` files.

- G1 (`.remedy-wt/f268-r7/g1.py`) → `EXIT-0`:
  - `ledger.md True authored copy True`, and the same line for `decisions.md`, `plan.md`, `quickstart_to.txt`, `readme_to.txt`, `skill.md` and `block.md`.
  - `live_review append True`, `decisions append True`, `plan equal True`.
  - `grouped.py count 1`, `README.md count 1`.
  - `git diff --numstat 8746b21e -- apps/cli/grouped.py README.md` → `5	8	README.md`, `8	6	apps/cli/grouped.py`, `EXIT-0`.
- G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_quick_start.py tests/cli/test_cli_ux.py tests/test_cli_execution_loop_closure.py tests/cli/test_advertised_commands.py tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py tests/docs/` → `510 passed in 67.62s (0:01:07)`; re-run with output redirected to a log for an unpiped exit code → `510 passed in 68.84s (0:01:08)`, `EXIT-0`. 0 failed.
- G3 `python3 -m ruff check apps/cli/grouped.py tests/cli/test_quick_start.py tests/cli/test_cli_ux.py tests/test_cli_execution_loop_closure.py` → `All checks passed!`, `EXIT-0`.
- G4 (`.remedy-wt/f268-r7/g4.py`), one worktree at `f638e910`, each run from the worktree root with `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_quick_start.py tests/cli/test_cli_ux.py`, `__pycache__` purged before each run; each mutation a single-occurrence replacement in `apps/cli/grouped.py` (asserted count 1), reverted by writing the original bytes back (asserted equal), and `git status --porcelain` read clean at the end:
  - imported path: `/home/decodeux/Repos/remedy/.remedy-wt/f268-r7-g4/apps/cli/grouped.py`.
  - control → `76 passed in 4.44s`, `exit=0`.
  - (a) `  5. remedy job list` → `  5. remedy job lst` → `4 failed, 72 passed`, `exit=1`: `test_quick_start.py::test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it`, `TestHappyPath::test_happy_path_in_help`, `TestQuickStart::test_quick_start_needs_no_job_id`, `TestQuickStart::test_quick_start_flags_are_declared_by_their_commands`.
  - (b) `CONTRIBUTING.md" --plan-only` → `CONTRIBUTING.md" --plan-everything` → `2 failed, 74 passed`, `exit=1`: `test_quick_start.py::test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it`, `TestQuickStart::test_quick_start_flags_are_declared_by_their_commands`.
  - (c) `  4. remedy do "Write a CONTRIBUTING.md"\n` → same line + ` --apply` → `1 failed, 75 passed`, `exit=1`: `test_quick_start.py::test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it`. Re-run alone (`.remedy-wt/f268-r7/g4c.py`), the failing line is `assert status_after[5] == status_after[1]`, the diff `+ ?? docs/` — the git-status assertion, not an exit code.
  - `git worktree list`: one row (main checkout) before, two during, one after. `remedy/job-*` branch count: 31 before, 31 after.
- G5 (clean tree, HEAD == origin) runs after the push; it is in the round report.

## Authored-text proofs

Seven payloads verified by sha256 before use and again in G1: `block.md` `2a1b4ffd…250a`, `ledger.md` `5cd7b3de…8ff`, `decisions.md` `d2d0b9a8…22b`, `plan.md` `39084c47…c45`, `quickstart_to.txt` `78282113…186`, `readme_to.txt` `2ce89dbc…55e`, `skill.md` `4a6bf8da…cc8`. Each copied byte-exact to `.agent/authored/f268-r7-<name>`; G1 prints every copy identical, both appends equal `git show 8746b21e:` bytes + payload, `.agent/plan.md` equal to plan.md, and each replacement payload contained exactly once in its target.

For the operator (Q2): the SKILL.md payload is `.agent/authored/f268-r7-skill.md`, sha256 `4a6bf8da8b59f9dac84ae9e183205fbfb08d84fbf0d9e8274da4d4d59494ccc8`; it replaces `.claude/skills/remedy-evidence-review/SKILL.md` whole. The block's own copy is `.agent/authored/f268-r7-block.md`, sha256 `2a1b4ffdc3047cf73a993c8f5ed09e3bf13796996be5450719078ef20743250a`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `dfb8cb46` |
| T005 (C2, C3) | done | `db2629bc`, `f638e910`; red under G4 (a), (b), (c) |
| R-0892 docs half (C4) | skipped | Write and Edit on `.claude/skills/remedy-evidence-review/SKILL.md` refused by the permission system; operator question Q2 added |
| C5 handoff | done | This commit |

Landed: T005 — `remedy --help` and the README Quickstart carry the five lines of DECISION F268 D15 (`remedy init`, `remedy doctor core`, `remedy do "Write a CONTRIBUTING.md" --plan-only`, `remedy do "Write a CONTRIBUTING.md"`, `remedy job list`); `tests/cli/test_quick_start.py::test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it` runs the printed lines on a fixture repository, each exits 0 and the target's `git status --porcelain` after line five equals its reading after line one; `test_each_line_runs_with_its_printed_words_and_only_a_do_line_gets_the_suffix` pins the executed argv (C2, C3).

## Open findings

126 open by distinct id, derived with `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 14 `Done:` ids, unchanged from round 6 (C1 books a verdict, no `Done:`). This round opens no finding. R-0892 stays open (its SKILL.md half).

## Deviations & assumptions

- **Commit sequence.** The block ordered C1–C5; the round ran C1, C2, C3, C5. C4 was not made: the Write tool and then the Edit tool on `.claude/skills/remedy-evidence-review/SKILL.md` were both refused by the permission system. Per the block, no shell route was tried; `.agent/operator_questions.md` gets Q2 (kind A) in C5. Under amend0917-throughput rule 5 the recommendation would be executed in the same round; it cannot be here, because executing it is the refused write — the entry says so.
- **A renamed pin.** `TestQuickStart::test_quick_start_has_auto_job_id` is now `test_quick_start_needs_no_job_id`: the new quick start deliberately has no job id, so the old name would state the opposite of what the test asserts. It still reads the rendered help and asserts more than before (the line-five text, and three absent tokens instead of one present one).
- **Additions beyond the letter of C2 (c)/C3, all strictening:** the flags test also pins the resolved pair list; the five-lines test pins the numbers in order; `test_quick_start.py` adds a `builtins.input` tripwire (constraint 2: no test reads real stdin); `tests/cli/test_cli_ux.py` gains the module constant `_NUMBERED_LINE`, shared by the two `TestQuickStart` tests that read numbered lines.
- **Exit codes.** The shell guard refuses `$?`, so each gate's exit code is shown as an `&& echo EXIT-0` suffix (printed only on exit 0); G2's first run was piped through `tail`, so it was re-run with output redirected to `.remedy-wt/f268-r7/g2.log` for an unpiped exit code. G1 and G4 ran from script files under `.remedy-wt/f268-r7/` for the same guard.
- **Full suite** not run (amend0917-throughput).

## Next

Reviewer: review round 7 at this branch tip and book its verdict in round 8's first commit. Operator questions open: 2 (Q2 asks the operator to apply the SKILL.md payload, which closes R-0892's last half). Then `.agent/plan.md` step 2, the `do` flag-list deletion round that closes R-0933.
