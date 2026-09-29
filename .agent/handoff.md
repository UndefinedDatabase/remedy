# Handback — F042 round 7: the integration gate, closure suite RED (xdist collection defect, not a code failure)

## Session

SESSION 2 of feature F042 · round 7 · rounds so far 7 (re-delegated after session 1's halt at
`.agent/STOP`). Context self-assessment: ample budget remains — well under a tenth of the
session's context window has been used through C6 and the gates.

## Range

Review of `c36841c6f`..`<this commit>`.

## Commits

### `7c5de666e` F042 R7 C1: copy round 7 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r7-block.md | +175 | this round's block, copied verbatim |
| .agent/authored/f042-r7-records.diff | +45 | payload copy |
| .agent/authored/f042-r7-selfuse.diff | +103 | payload copy |
| .agent/authored/f042-r7-built_state.diff | +17 | payload copy |
| .agent/authored/f042-r7-plan.md | +29 | payload copy |

Total 369 insertions (block's 175 + 194), matching the block's stated formula exactly.

### `e3122983c` F042 R7 C2: book F042 R6 with R-1111's resolution, record D7
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +25/-0 | DECISION F042 D7 (self-use item SU-036 landed with one added assertion) |
| .agent/live_review.md | +4/-0 | F042 R6 gate entry booked VERDICT PASS; R-1111 resolution |
| .agent/plan.md | +9/-17 | rewritten to round-7-in-progress state, from payload |

### `7b712a3a4` F042 R7 C3: land the closure's self-use item SU-036, the repair of R-1107
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_story_export_file_live.py | +42/-5 | job `6dad54d0e18348c4`'s diff plus D7's one added assertion (`"chrome: startup" in str(exc.value)`) |

### `a5100f6f7` F042 R7 C4: record the self-use item in F042's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F042.md | +9/-0 | self-use paragraph appended, per payload |

### `cdf694630` F042 R7 C5: add the round 7 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r7-mutations.py | +122/-0 | G3's mutation/red-proof tool for R-1107's repair |

### `<this commit>` F042 R7 C6: record the closure suite transcript and rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-closure-suite.txt | new | the one full-suite transcript, RED, root-caused |
| .agent/handoff.md | rewrite | this handback, per the write-once rule |

## External actions

- `git worktree add --detach .remedy-wt/f042-r7-dryrun HEAD` (at `a5100f6f7`, before C5 was
  committed) — a self-test of the mutation tool's logic ahead of the gated run; removed via
  `git worktree remove --force` immediately after. Declared as a deviation below.
- `git worktree add --detach .remedy-wt/f042-r7-mut cdf694630` (G3's gated run) — removed via
  `git worktree remove --force` as G3's last action; `git worktree prune` run after both removals;
  `git worktree list | wc -l` read 25 both before and after.
- `git push -u origin feature/f042-multi-project-cockpit` after this commit: real outcome reported
  in the worker's final reply, since this file cannot record a push that follows it.
- No PR created, merged or edited. No self-use runner or provider-calling job was invoked this
  round; the self-use job's own branch `remedy/job-6dad54d0e18348c4` was left untouched and never
  applied, per constraint 3.

## Verification

**BEFORE ANYTHING ELSE:** step 1 `ls .agent/STOP` — absent. step 2 `pwd`
`/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f042-multi-project-cockpit`; `git log --oneline -1` `c36841c6f` — all matched. step 3
block measured at 175 lines, sha256
`12b996b511e5107b697ff65861ab4887dea73dcb4a93f21d0bc80402bff83a57` — equal to the delegation
message's two readings exactly. step 4 `git worktree list | wc -l` 25; `git branch --list
'remedy/*' | wc -l` 16.

**PAYLOADS:** all four measured exactly against the table — records.diff 45/7630/`4e2523cc...`,
selfuse.diff 103/5091/`2a2834a7...`, built_state.diff 17/1283/`289ab257...`, plan.md 29/971/
`0d064dc2...` — full hashes match the block's table digit for digit.

**C1–C5:** every `git apply --check` and `git apply` exit 0; every `git show --numstat` read
matched the block's expected numstat exactly (C2: 25/0, 4/0, 9/17; C3: 42/5; C4: 9/0); C5's ruff
check (deferred to after the commit, since the file it names did not exist before C5) read `All
checks passed!`, exit 0.

**C6(a) UI build:** `apps/ui/node_modules/.bin/vite build` (cwd `apps/ui`) — exit 0, last line
`✓ built in 2.25s`. `git status --porcelain` after: empty.

**C6(b) the one full suite:** `python3 -m pytest -n auto -q`, real exit code 1, wall time 12
seconds, summary line `15 errors in 12.39s`. THIS IS NOT A TEST FAILURE — it is a pytest-xdist
COLLECTION-time abort: 15 of 16 workers (all but the gw1 reference) each reported "Different tests
were collected between gw1 and gwN," and zero tests of any kind executed (grep of the full
transcript for "passed" or any `tests/...` result line returns nothing). Root cause, confirmed by
a scoped (single-file, not full-suite) re-run of `pytest -n auto -q
tests/ui_server/test_projects_route.py` — same shape, 15 errors in 1.08s:
`tests/ui_server/test_projects_route.py:111` —
`@pytest.mark.parametrize("name", ["gamma", str(uuid4())])` — evaluates `str(uuid4())` at MODULE
IMPORT time, once per xdist worker process, so each worker collects
`test_an_unknown_project_is_404` under a different parametrize id and xdist's collection-
consistency check fails deterministically. `git blame` names `06376f3569` ("F042 R1 C5: add the
reviewer's route tests for the project list and summary") as the line's origin — pre-existing on
this branch since round 1, not introduced this round. No file was edited to investigate or route
around it. FULL list of bad node ids (failed plus errors): NONE at the individual test-node level
— no test reached pass or fail. The 15 collection ERRORS are xdist worker-session errors (gw0,
gw2–gw15), all tracing to the one non-deterministic parametrize id at
`tests/ui_server/test_projects_route.py::TestProjectRoutes::test_an_unknown_project_is_404[<uuid4,
regenerated per worker>]`. Tree it ran on: `cdf694630`. Full transcript and this analysis are
committed verbatim in `.agent/authored/f042-closure-suite.txt`.
`tests/orchestration/test_import_reachability.py` and `tests/test_no_orphan_modules.py` hold NO
reading from this transcript — neither ran; closure precondition 7 is UNKNOWN from this run, not
satisfied, and needs a real full-suite pass before closure.

`pgrep -af server.py` immediately after: one line, but it is `pgrep`'s own invocation matching its
own command text (contains the literal string "server.py"), not a real process — confirmed by
`ps aux | grep "[s]erver.py"`, which returned nothing. No `server.py` process is running.

**G1 transport and records:** all five `.agent/authored/f042-r7-*` copies byte-identical to source
at C1 (`git show 7c5de666e:<path>` vs. source bytes, all `True`); the read-at-commit table's five
rows (decisions.md/live_review.md/plan.md at `e3122983c`; the story test at `7b712a3a4`; the
Built State at `a5100f6f7`) all matched the reviewer's stated bytes and sha256 exactly.
`open_finding_ids` over `.agent/live_review.md` at `e3122983c` read `['R-1107']`;
`latest_gate_verdict` read `PASS` — both equal to the block's stated values.

**G2 the tests:** the named selection read `551 passed, 1 skipped` at exit 0 (the one SKIPPED line
is the D12 quarantine only — this checkout has `vite`, so the story test ran and passed, one more
than the reviewer's `550 passed, 2 skipped` reference which lacked `vite`). `ruff check` on the
story test and the mutation tool: `All checks passed!`, exit 0. `integrity check --json`: six
`pass`, `fail_count` 0. `integrity block .remedy-wt/f042-r7/block.md`: exit 0, `All 7 checkable
items pass.` `git status --porcelain`: empty, no untracked file.

**G3 the red proofs of R-1107's repair:** run against `git worktree add --detach
.remedy-wt/f042-r7-mut cdf694630`. Control-before: exit 0, failed 0 (pass). r1 (tail left out of
the message): exit 1, failed 1, caught; restored byte-identical: True. r2 (path left out of the
message): exit 1, failed 1, caught; restored byte-identical: True. r3 (stderr sent to DEVNULL
again): exit 1, failed 1, caught; restored byte-identical: True. Control-after: exit 0, failed 0
(pass). Last line: `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Worktree removed
(`git worktree remove --force`), pruned; `git worktree list | wc -l` read 25 after.

**G4 the integration gate:** covered above (C6a/b) — UI build exit 0 / `✓ built in 2.25s`;
`git status --porcelain` empty after; full suite exit 1, wall 12s, `15 errors in 12.39s`, bad node
ids NONE at test-node level (xdist collection defect, described in full above);
`.agent/authored/f042-closure-suite.txt` committed; server.py reading none (false self-match
explained); `tests/orchestration/test_import_reachability.py` and `tests/test_no_orphan_modules.py`
hold no reading this run — closure precondition 7 unmet by this transcript.

## Authored-text proofs

All five `.agent/authored/f042-r7-*` files are byte-identical, source to committed copy, verified
at C1 (see G1 above). The three applied diffs (records.diff → `.agent/decisions.md` and
`.agent/live_review.md`; selfuse.diff → the story test; built_state.diff → the Built State) and
the rewritten `.agent/plan.md` were each verified byte-for-byte against the reviewer's stated
sizes and sha256 at the commit that applied them (G1's five-row table, all `True`) — this confirms
`git apply` reproduced the reviewer-authored text exactly, not only that the source payload itself
was uncorrupted.

## Deviations & assumptions

1. **An extra, unordered worktree add/remove.** Before committing C5, this session added a
   throwaway worktree (`git worktree add --detach .remedy-wt/f042-r7-dryrun HEAD`, at `a5100f6f7`)
   to dry-run the mutation tool's logic before trusting it for the gated G3 run, then removed it
   immediately. The block names only G3's worktree at C5's SHA; this extra one was not ordered.
   Justification: catching a bug in the tool before committing it and before the gated run was
   judged safer than debugging inside the one gated worktree G3 names. It was fully cleaned up
   (`git worktree remove --force`, `prune`) before C5 was committed, and `git worktree list`
   returned to 25 both before and after. No commit and no gate reading depends on it.
2. **An extra, scoped test run to root-cause the RED full suite.** After C6(b)'s full-suite run
   went red on a collection-time xdist error, this session ran
   `pytest -n auto -q tests/ui_server/test_projects_route.py` (one file only) to confirm the root
   cause before writing it up. This is NOT the full suite (amend0917 rule 1 reserves that run to
   once, in C6, and it was): it is a single-file diagnostic read, analogous to G2's and G3's own
   scoped runs. No file was edited as a result; the run only confirmed the diagnosis recorded in
   `.agent/authored/f042-closure-suite.txt`.
3. **The full suite is RED, and this round does not repair it.** Per block constraint 4
   ("A RED full suite in C6 is this feature's work, not a stop... the repair rounds are the
   reviewer's to order, amend0917-throughput rule 2"), the transcript is committed exactly as
   measured and this handback documents the root cause in full; no test or production file was
   touched to fix or route around it, no assertion was weakened, nothing was skipped or marked
   xfail. `tests/ui_server/test_projects_route.py:111`'s `str(uuid4())` parametrize default is the
   candidate fix surface for whichever round the reviewer orders it to.

No payload was retyped or edited. No existing test was edited to pass. No file outside the
round's tracked path set (constraint 3) was touched.

## Next

Per Phase 1 rule 1 and this round's own instruction: the review of round 7 and of its suite
transcript is next, then the closure's evidence round (booking round 7, whatever repair the suite
requires, the evidence bundle and the review package), then the closing round. The full-suite RED
and its xdist-collection root cause (`tests/ui_server/test_projects_route.py:111`) is the first
thing that review needs to weigh before ordering a repair round.

Open findings: 1. Operator questions open: 0.
