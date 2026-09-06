# Handoff — F272 One world completion

## Session

SESSION 2 of feature F272 · round 5 · rounds so far 5

Context self-assessment (amend0905-throughput): context is comfortable — this
round read three protocol documents, one 30713-byte block and seven production
files, ran an AST scope pass and eleven measurement passes including a
thirteen-minute worktree pair, and never approached a limit; the session can
continue for several more rounds.

Soft limit per amend0906-triage-throughput: F272's limit is 12 sessions and 40
rounds. At 2 sessions and 5 rounds the limit is far off and no scope report is
owed.

Branch: `feature/f272-one-world-completion`. No PR created, none merged, no
force-push, nothing on `main`.

## Range

Review of `78457a98`..`<C7>` (C7 is the commit that writes this file; the
reviewable substantive range is `78457a98`..`0ec1cfbf`).

## Commits

### e47515fd f272: save the round 5 step block as authored text (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r5.md` | +384/-0 | `shutil.copyfile` of the delegated block; transport leg 1 |

### 831b3f0a f272: mirror the round 5 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +336/-271 | `shutil.copyfile` of the same source over round 4's block; transport leg 2 |

### 78c7dedb f272: set the plan to round 5, the production half of the move two (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-20 | replaced by the PLANF272R5 slice, byte for byte |

### fb101360 f272: record the R-0818 resolution, the round 4 gate entry and the prose slip (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | RECORDR5 appended: the `Done: R-0818` paragraph and the `Gate: F272 R4` entry |
| `.agent/prose_slips.md` | +2/-0 | SLIPSR5 appended: the round 4 append-convention slip, the reviewer's own |

### 2f043d6a f272: rule DECISION F272 D3, the two call shapes of the name collapse (C3)
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +70/-0 | DECISIOND3 appended into the `## DECISIONs` section |

### 323acc75 f272: move pingpong_loop onto data_paths run_dir and runs_dir at all thirteen sites (C4)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | +13/-16 | SHAPE B ×13; module-level `from packages.orchestration import data_paths` added, the two names dropped from the `data_paths` from-import, `mint_run_id` kept |

### ce94f82d f272: move job_evidence onto run_dir and runs_dir, shape B at its two shadowing scopes (C5)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_evidence.py` | +14/-14 | SHAPE A ×10 in five scopes, SHAPE B ×4 in `_write_task_postmortems` and `_write_task_worktree_evidence` |

### 0ec1cfbf f272: move the five remaining production callers onto run_dir and runs_dir (C6)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_promote.py` | +4/-4 | SHAPE B ×2 in `promote_run`, SHAPE A ×2 in `load_promotion` |
| `packages/orchestration/worktree_resume.py` | +4/-4 | SHAPE A ×4; `_run_dir` stays a one-line wrapper, now around `run_dir` |
| `packages/orchestration/pingpong_evidence.py` | +2/-2 | SHAPE A ×2 in `export_evidence` |
| `packages/orchestration/repair_attest.py` | +2/-2 | SHAPE A ×2 in `_prior_provider_call_count` |
| `apps/cli/commands/do_cmd.py` | +2/-2 | SHAPE A ×2 in `_load_prompt_trace_index` |

### C7 — this commit (self-reference exception, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | (this file) | the round 5 handback; a handoff cannot table the commit that writes it |

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `.agent/authored/f272-r5.md`, byte-identical to source |
| C0b mirror the block | done | `.agent/last_block.md`, byte-identical to source and to C0a |
| C1 the plan | done | plan.md == PLANF272R5 slice, 2173 bytes, 45 lines |
| C2 the record | done | +4/-0 and +2/-0, four readers green, no id minted |
| C3 DECISION F272 D3 | done | appended; D3 ×1 beside D2 ×1 and D1 ×1 |
| C4 `pingpong_loop.py` | done | 13 sites, SHAPE B throughout |
| C5 `job_evidence.py` | done | 14 sites, SHAPE A ×10 and SHAPE B ×4 |
| C6 the five remaining production files | done | 14 sites, SHAPE A ×12 and SHAPE B ×2 |
| C7 the handback | done | this file; committed and pushed |

Every ordered item is present exactly once. Nothing skipped, nothing reordered,
no extra commit. The change set is exactly the fourteen paths of the Change line.

## External actions

| Action | Outcome |
|---|---|
| `git push -u origin feature/f272-one-world-completion` | EXIT 0, `78457a98..0ec1cfbf` |
| `git worktree add --detach .remedy-wt/f272-r5-g6 HEAD` | EXIT 0, `HEAD is now at 0ec1cfbf` |
| `git worktree remove --force .remedy-wt/f272-r5-g6` | EXIT 0 |
| `git worktree prune -v` | EXIT 0, no output |
| PR create / edit / merge | NONE — the round orders none |
| `gh` commands | NONE |
| final `git push` after C7 | EXIT 0 |

The twelve pre-existing `remedy/job-*` worktrees under `.remedy-wt/` predate this
round and were not touched; `git worktree list` after the prune shows exactly the
primary checkout and those twelve.

## Verification — one line per gate

| Gate | Exit | Result |
|---|---|---|
| G1 TRANSPORT | 0 | source, `.agent/authored/f272-r5.md` and `.agent/last_block.md` all 30713 bytes, all sha256 `eef4d9b3…38eb21`, `filecmp.cmp(shallow=False)` True both ways |
| G2 THE RECORD | 0 | readers (a)(b)(c) green over both files; (d) all seven count transitions exactly as ordered |
| G3 THE PLAN | 0 | `.agent/plan.md` == PLANF272R5, 2173 == 2173 bytes, same sha256, 45 lines < 50, `## Goal` ×1 and `## Next Steps` ×1 |
| G4 THE FEATURE FILE | 0 | reader (a) green, 14790 → 19325 bytes; D3 ×1, D2 ×1, D1 ×1; `tests/docs/` + `test_roadmap_index.py` EXIT 0, 333 passed |
| G5 THE PRODUCTION SWEEP | 0 | (i) 0 non-exempt occurrences over 367 `packages/`+`apps/` files, `data_paths.py` still 5; (ii) `tests/` still 132 in 26 files, 0 changed paths under `tests/`; (iii) 0 shadow lines; (iv) 41 sites moved, table below |
| G6 MUTATION RED-PROOF | 0 | selection 88 files (reviewer: 88); UNMUTATED CONTROL EXIT 0, 3562 passed in 405.89s; MUTATED EXIT 0, 3562 passed in 381.64s, ZERO failures and ZERO errors against the reviewer's base EXIT 1 at 330 failed / 17 errors |
| G7 LINT AND INTEGRITY | 0 | ruff over exactly the seven changed files in ONE invocation: `All checks passed!`; integrity `"passed": true`, `"fail_count": 0` |
| G8 THE TREE | 0 | status empty, `git ls-files .remedy-wt` empty, worktree created and removed, C0a–C6 insertions 384/336/21/6/70/13/14 all single-parent and under 500, marker sweep zero over all twelve written files |

NO GATE WENT RED. G6's mutated run is the round's discriminator and its GREEN is
the evidence: at `78457a98` the same mutation over the same selection was EXIT 1
at 330 failed with 17 errors, and after this round nothing in the selection
reaches `pingpong_run_dir` any more.

### G5(iv) — per-file site counts and shapes

| File | Sites (mine) | Reviewer | SHAPE A | SHAPE B | Notes |
|---|---|---|---|---|---|
| `packages/orchestration/pingpong_loop.py` | 13 | 13 | 0 | 13 | 2 in the module-level import block, 11 calls; block rules one shape for the whole file |
| `packages/orchestration/job_evidence.py` | 14 | 14 | 10 | 4 | B in `_write_task_postmortems` and `_write_task_worktree_evidence` (import + call each) |
| `packages/orchestration/pingpong_promote.py` | 4 | 4 | 2 | 2 | B in `promote_run`, A in `load_promotion` |
| `packages/orchestration/worktree_resume.py` | 4 | 4 | 4 | 0 | `_run_dir` left a wrapper, per the block |
| `packages/orchestration/pingpong_evidence.py` | 2 | 2 | 2 | 0 | |
| `packages/orchestration/repair_attest.py` | 2 | 2 | 2 | 0 | |
| `apps/cli/commands/do_cmd.py` | 2 | 2 | 2 | 0 | |
| **Total** | **41** | **41** | **22** | **19** | every per-file count agrees with the reviewer's |

Repo-wide, my own enumeration over 1063 tracked `.py` files reproduces the
reviewer's split exactly: 178 occurrences in 34 files — 41 production, 132 test,
5 in `data_paths.py`.

### G2(d) counts, before C2 → after C2

| Reading | Before | After | Ordered |
|---|---|---|---|
| distinct `^- R-\d{4} — ` ids | 302 | 302 | 302 → 302 |
| distinct `^Done: R-\d{4} — ` ids | 246 | 247 | 246 → 247 |
| open set BY DISTINCT ID | 56 | 55 | 56 → 55 |
| `^Done: R-0818 — ` | 0 | 1 | 0 → 1 |
| `^Landed: R-0818` | 1 | 1 | 1 → 1 (NOT deleted) |
| `^Gate: ` | 26 | 27 | 26 → 27 |
| `^Gate: F272 R4 ` | 0 | 1 | 0 → 1 |

Open findings: 55, down one. R-0818 is now RESOLVED by the reviewer's own
`Done:` text; its `Landed:` line is superseded in place, not removed. No id was
minted this round and no worker-authored `Done:` paragraph exists.

### G2(b) structural readings, N counted by the script from each slice

| File | Units before | Units after | Delta | N |
|---|---|---|---|---|
| `.agent/live_review.md` | 691 | 693 | 2 | 2 |
| `.agent/prose_slips.md` | 169 | 170 | 1 | 1 |
| `docs/roadmap/features/T2_F272.md` | 28 | 37 | 9 | 9 |

### STOP readings (constraint 9)

| Reading | When | `os.path.exists('.agent/STOP')` |
|---|---|---|
| 1 | before C0a | False |
| 2 | before C4 | False |
| 3 | before C7 | False |

The sentinel never appeared, so protocol G6 never bound and the full nine-commit
bundle ran.

## Authored-text proofs

Every slice extracted from the COMMITTED `.agent/authored/f272-r5.md` by exact
marker-line matching, exactly one BEGIN and one END asserted per name, each line
carrying its own terminating newline.

| Slice | Applied to | Bytes | sha256 (head) | Equal on disk |
|---|---|---|---|---|
| PLANF272R5 | `.agent/plan.md`, whole file | 2173 | `0aadda28…` | yes, byte-for-byte and by sha256 |
| RECORDR5 | `.agent/live_review.md` [1073334:] | 8182 | `337944d2…` | yes |
| SLIPSR5 | `.agent/prose_slips.md` [133531:] | 605 | `80f69c6d…` | yes |
| DECISIOND3 | `docs/roadmap/features/T2_F272.md` [14791:] | 4534 | `66e5d2e1…` | yes |

Transport chain: `.remedy-wt/f272-r5-block.md`, `.agent/authored/f272-r5.md` and
`.agent/last_block.md` are all 30713 bytes and all hash to
`eef4d9b30b7f1ab86b3119a053bec4cf8209f1f60b6e3d7ee6f0cc88cb38eb21`, the digest
the delegation named before the round began. Per §3 item 37 this chain covers the
SAVED COPY AND ITS MIRROR; it is NOT a claim about the bytes emitted into the
worker's prompt.

## Deviations & assumptions

1. **No slice was edited and no objection to any slice arose.** All four applied
   byte for byte; constraint 1 was never tested.
2. **THE SHADOW SET IS WIDER THAN SEVEN SITES, THOUGH NOT WIDER THAN SEVEN
   ASSIGNMENTS — declared as the block's "if you find an eighth" clause invites.**
   I determined the shape for every site by parsing each file with `ast` and
   computing, per function scope, the set of names bound by assignment, `for`,
   `with … as`, walrus, parameters and nested defs. That reproduces the
   reviewer's seven `run_dir = pingpong_run_dir(` assignments EXACTLY —
   `job_evidence.py` ×2, `pingpong_loop.py` ×4, `pingpong_promote.py` ×1 — and
   found NO EIGHTH ASSIGNMENT. It also found THREE FURTHER SITES that sit inside
   an already-shadowed scope without themselves assigning: `run_pingpong` in
   `pingpong_loop.py` binds `run_dir` at what was line 4076, and the three calls
   at what were lines 3009, 3303 and 3649 are in that same function body. A token
   swap at those three would have been `UnboundLocalError` too — earlier in the
   function than the assignment, so *more* certainly fatal. They need no special
   handling because the block already rules SHAPE B for all thirteen
   `pingpong_loop.py` sites, but they are worth recording: the hazard is a
   property of the SCOPE, not of the assignment line, and a round-6 sweep of the
   132 test sites should use the scope test rather than the assignment regex.
   Three further occurrences are function-local IMPORT lines inside shadowed
   scopes (`job_evidence.py` ×2, `pingpong_promote.py` ×1); those are the second
   half of each SHAPE B pair and are counted in the SHAPE B column above.
3. **The `pingpong_loop.py` from-import was collapsed to one line.** Removing two
   of its three names leaves `from packages.orchestration.data_paths import (\n
   mint_run_id,\n)`, which ruff's isort rule `I001` (enabled — `select = ["E",
   "F", "W", "I", "UP"]`) rewrites to a single line. Since G7 requires ruff EXIT 0
   over that file, I wrote the single-line form directly. The new
   `from packages.orchestration import data_paths` is placed BEFORE
   `from packages.orchestration.artifact_summary import …` for the same reason:
   isort sorts the bare package before its submodules. Both are consequences of
   the ordered gate, not choices.
4. **Behaviour is unchanged and I verified the aliasing rather than assuming it.**
   `data_paths.pingpong_runs_dir(root)` is `return runs_dir(root)` and
   `pingpong_run_dir(run_id, root)` is `return pingpong_runs_dir(root) / run_id`,
   i.e. exactly `run_dir`'s `runs_dir(root) / run_id`. Every edit is therefore a
   rename or a re-route of the same call to the same body; no function's return
   value changed. Constraint 6 was never engaged.
5. **`worktree_resume._run_dir` was left a wrapper**, as the block directs. It now
   reads `from packages.orchestration.data_paths import run_dir` / `return
   run_dir(run_id)`. `_run_dir` and `run_dir` are distinct names, so the
   function-local import does not shadow the wrapper it sits in.
6. **G7's repo-wide scope was not widened.** `ruff check .` remains EXIT 1 at 26
   errors on the base and on `main` under OPEN finding R-0468; the block
   deliberately does not order it and I did not run it as a gate.
7. **Scratch discipline.** Eleven driver scripts were written under the gitignored
   `.remedy-wt/` and removed afterwards BY EXACT PATH, never by glob:
   `f272r5_slices.py`, `f272r5_c2.py`, `f272r5_run.py`, `f272r5_survey.py`,
   `f272r5_scopes.py`, `f272r5_shapea.py`, `f272r5_shapeb.py`, `f272r5_g5.py`,
   `f272r5_g6.py`, `f272r5_g8.py`, `f272r5_wait.py`, plus the selection listing
   `f272r5_g6_selection.txt`. All runs used `python3 -B`, and `__pycache__` was
   purged inside the G6 worktree before both readings (0 directories before the
   control, 6 before the mutated run). `.remedy-wt/f272-r5-block.md` is the
   delegation's own source file and was left in place. One further removal is
   declared here because it was NOT mine: `.remedy-wt/__pycache__` held exactly
   one entry, `f272r3_slices.cpython-310.pyc`, a stale round-3 bytecode file
   whose source no longer exists; I listed the directory before removing it by
   exact path. That it held NO `f272r5_*` entry is the positive evidence that
   `python3 -B` was in force for every run of this round.
8. **No ninth production file and nothing under `tests/`.** The change set is
   exactly the fourteen paths of the Change line; `git diff --name-only
   78457a98..HEAD` lists thirteen of them before this commit and no path
   beginning `tests/`.

## Next

Reviewer re-runs G1 through G8 at `0ec1cfbf` and issues the round 5 verdict. On
PASS, round 6 is the test half of the same move — the 132 occurrences in 26 files
under `tests/` — followed in that round's LAST commit by the deletion of
`pingpong_runs_dir` and `pingpong_run_dir` from `data_paths.py`, together with
`tests/test_data_paths.py`'s
`test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir`, whose four
properties are already pinned for the real names at lines 79, 102, 376 and 396 of
that same file. Round 6 should choose its shapes by the SCOPE test of deviation 2,
not by the `run_dir = pingpong_run_dir(` assignment regex. Before authoring,
re-read `.agent/STOP` from disk (Phase 1 rule 1 before rule 2).
