# Handoff — F036, round 4 (book round 3, register R-1087, record DECISION F036 D5; land T003's
first half: the `tour` route over one shared view, the browser's pure tour module and its
loader, and the R-1087 repair)

## Session

SESSION 1 of feature F036 · round 4 · rounds so far 4. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, DECISION F036 D5
and finding R-1087 in the booking diff, and every required source file in full (`result_tour.py`
as round 3 left it, `_build_ownership_json`/`_build_lessons_json`/`_load_job`/the `handlers` dict
of `_RemedyHandler.do_GET` in `ui_server.py`, `_tour_section` in `apps/cli/commands/job.py`,
`test_ownership_route.py`, `test_handler_table_walk.py`, `_walkable_paths` in
`test_command_channel.py`, `ownership.ts`, `ownership.test.ts`, `fetchJson`/`ownershipViewPath`'s
use/`loadOwnershipView` in `remedyApi.ts`, `test_ownership_view_contract.py`, `strip_ts_comments`
in `test_brain_stream_ring.py`, and `.agent/authored/f035-r5-mutations.py`); wrote `tour_view`,
the route, the rewritten `_tour_section`, the R-1087 regex repair and its regenerated golden, the
pure `resultTour.ts` module, `loadTourView`, their tests (Python, vitest, contract) and the
mutation tool from the specification; ran the payload-verification, G1/G2 byte-equality and hash
checks, ruff, tsc, eslint, vitest directly (before the full G4 run), the full G4 pytest selection,
`integrity check`, and the G5 mutation tool once in the official worktree.

## Range

Review of `09782a43..HEAD` (`HEAD` is this handback's own commit, `F036 R4 C6`, on
`feature/f036-guided-result-tour`).

## Commits

### 605d5f76e F036 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r4-block.md | 290/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r4-booking.diff | 58/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r4-plan.md | 28/0 | copy of the reviewer's plan.md payload |

### cb0e69a2d F036 R4 C2: book round 3, register R-1087, record DECISION F036 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 38/0 | DECISION F036 D5 appended by booking.diff |
| .agent/live_review.md | 4/0 | round 3's `Gate: F036 R3 —` entry and R-1087's registration appended by booking.diff |
| .agent/plan.md | 7/7 | rewritten to the reviewer's plan.md payload |

### 7debee4a9 F036 R4 C3: serve one tour view to the browser and the command line, repair R-1087
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/result_tour.py | 33/3 | S1 `TOUR_VIEW_KEYS`, `tour_view(job)`; S3 `_TOUR_PATH_TOKEN_RE`'s slashed-path half repaired for R-1087 |
| packages/orchestration/ui_server.py | 8/0 | S2 `_build_tour_json(job)`, `"tour"` appended to `handlers` after `"lessons"` |
| apps/cli/commands/job.py | 11/23 | S2 `_tour_section` rewritten to build from `tour_view(job)`, same behaviour as round 3 |
| tests/orchestration/fixtures/result_tour/golden_generated.json | 1/1 | S3 the one path reason regenerated from the code |

### 27d4ae8cc F036 R4 C4: decode the tour view in the browser and load it without a throw
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/resultTour.ts | 198/0 | S4 the pure module: interfaces, `TOUR_ANCHOR_KINDS`, `MAX_TOUR_STOPS`, `decodeTourView`, `tourViewPath`, the panel-state/neighbours/step-label/progress/anchor-label helpers |
| apps/ui/src/api/remedyApi.ts | 24/0 | S5 `TourFetcher`, `loadTourView`, import of `decodeTourView`/`tourViewPath` |

### 145335aed F036 R4 C5a: test the tour route, the browser module and R-1087
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_result_tour.py | 85/0 | `tour_view` for stored/none/unreadable, the invented dotted-hyphenated path dropped whole, a recorded path closing a sentence kept (R-1087) |
| tests/ui_server/test_tour_route.py | 142/0 | NEW FILE: the route's byte-for-byte pin, stored/none/unreadable, 404, neighbour, wrong token |
| apps/ui/src/api/resultTour.test.ts | 173/0 | NEW FILE: the decoder's acceptances/refusals, the path, each panel state, neighbours, step label, progress, anchor labels, `loadTourView` never throwing |
| tests/ui_contracts/test_tour_view_contract.py | 81/0 | S6 NEW FILE: payload/tour/stop/anchor/drop keys, anchor-kind order, no socket/clock/storage, `loadTourView` reads through `tourViewPath`/`decodeTourView` |

### dfaf5b116 F036 R4 C5b: add the round 4 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r4-mutations.py | 240/0 | the G5 red-proof tool: 10 mutations (m1–m10 of the block) across 3 Python files and 2 TypeScript files, all caught |

### <this commit> F036 R4 C6: rewrite handoff for round 4, mark R-1087 landed
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |
| .agent/live_review.md | +1 | `Landed: R-1087 —` line appended, naming C3's short SHA `7debee4a9` |

## External actions

- `git worktree add --detach .remedy-wt/f036-r4-mut dfaf5b116` — the official G5 worktree, cut
  from C5b per the block. Outcome: worktree created at detached HEAD `dfaf5b116`.
- `git worktree remove --force .remedy-wt/f036-r4-mut` then `git worktree prune` — the official
  G5 worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 63,
  matching the round's step-4 reading.
- `git push -u origin feature/f036-guided-result-tour` — run immediately after this commit per
  the bundle order. Its real outcome is reported in the round's reply (G6), not here, because
  this file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use), all MATCH:
```
booking.diff: 58 lines, 13496 bytes, sha256 53ce68fc4cbea645eba7c84652de075490cc20868a94bf7e98c9347c341a6f98
plan.md:      28 lines,   960 bytes, sha256 02058c3525a3779798d8fa16cfc2d55725c11ba2ff6466b55e2f4c33fe4cb288
```
Block self-check: 290 lines, sha256 `2ab9f891289b70128f961525897d91b96c4d30f852febb797b836fe1f7517dea` — MATCH on both readings given in the
delegation message. `.agent/authored/f036-r4-*` copies vs. sources, read back via
`git show 605d5f76e:<path>`, all byte-identical:
```
f036-r4-block.md     vs .remedy-wt/f036-r4/block.md              MATCH
f036-r4-booking.diff vs .remedy-wt/f036-r4-payloads/booking.diff MATCH
f036-r4-plan.md       vs .remedy-wt/f036-r4-payloads/plan.md     MATCH
```

**G2 THE BOOKING** — every file's bytes and sha256 at C2 (`git show cb0e69a2d:<path>`) MATCHED
the reviewer's table exactly:
```
.agent/decisions.md   2364324 bytes  sha256 bb8dd2356464c2b92517898203a0bdc1d3b5d8861b8f8001f8ed72100d1d7661 MATCH
.agent/live_review.md  320834 bytes  sha256 d702ff0c0a19abb03bf0db696afca3cc8370be6ad39f14c21b292d69cb8cd203 MATCH
.agent/plan.md            960 bytes  sha256 02058c3525a3779798d8fa16cfc2d55725c11ba2ff6466b55e2f4c33fe4cb288 MATCH
```
`open_finding_ids` over `.agent/live_review.md` TEXT at C2 (via `scripts.rotate_live_review`) read
`['R-1087']`, matching the reviewer's stated reading. `latest_gate_verdict` read `PASS`, matching.
`git diff --name-only 605d5f76e cb0e69a2d` named exactly the 3 paths of the G2 table, no more,
no fewer.

**G3 THE CODE** — `python3 -m ruff check packages/orchestration/result_tour.py
packages/orchestration/ui_server.py apps/cli/commands/job.py tests/orchestration/test_result_tour.py
tests/ui_server/test_tour_route.py tests/ui_contracts/test_tour_view_contract.py` at C5b:
`All checks passed!`, REAL_EXIT=0. `tour_view`, `_build_tour_json`, the new `_tour_section`, the
new `_TOUR_PATH_TOKEN_RE`, `decodeTourView` and `loadTourView` were quoted whole from the commits
that wrote them (C3 `7debee4a9` for the four Python pieces, C4 `27d4ae8cc` for the two TypeScript
functions) — see the round's reply for the full text; behaviour matches S1–S6 exactly.

**G4 THE TESTS** — the block's 22-target serial selection (with `tests/ui_server/test_tour_route.py`
included, unlike the reviewer's baseline run) at C5b:
```
1777 passed, 5 skipped in 109.65s (0:01:49)
REAL_EXIT=0
```
The reviewer's stated baseline (the same selection less `test_tour_route.py`, at `09782a43` before
any change) read `1758 passed, 5 skipped`. 1777 − 1758 = 19 new nodes: 5 in
`tests/orchestration/test_result_tour.py` (3 `tour_view` tests + 2 R-1087 claim-check tests), 6 in
`tests/ui_server/test_tour_route.py` (NEW FILE), and 8 in `tests/ui_contracts/test_tour_view_contract.py`
(NEW FILE) — no discrepancy. SKIPPED lines (all 5, identical to the reviewer's stated baseline —
4 F252 quarantines in `tests/ui_contracts/` and the one in `tests/test_agent_tooling.py`):
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
```
Before the full G4 run, the browser side was checked directly (all within the same 22-target
selection's own `test_vitest_passes`/`test_typescript_compiles`/`test_ui_lint` wrappers, re-run
here individually for a fast signal): `apps/ui/node_modules/.bin/vitest run
src/api/resultTour.test.ts src/api/ownership.test.ts` — 2 files, 52 tests passed;
`apps/ui/node_modules/.bin/tsc --noEmit` — clean, exit 0; `apps/ui/node_modules/.bin/eslint src
--max-warnings 0` — clean, exit 0. `python3 -m apps.cli.main integrity check --json`: all six
checks `pass`, `fail_count` 0, `ok` true.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f036-r4-mut dfaf5b116` then
`python3 -B .agent/authored/f036-r4-mutations.py <worktree>`, whole output:
```
control (start) PYTHON: exit=0 failed=0 tests=[]
control (start) VITEST: exit=0 failed=0 tests=[]
m1 tour_view reads stored true when none is stored: runner=PYTHON exit=1 failed=3 tests=['tests/orchestration/test_result_tour.py::test_tour_view_for_none_stored', 'tests/ui_server/test_tour_route.py::TestTourRoute::test_tour_endpoint_answers_the_view_for_a_job_with_none_stored', 'tests/cli/test_job_show.py::TestTourSection::test_nothing_stored_reads_stored_false_and_version_zero'] caught=True restored=True
m2 tour_view lets a ResultTourError propagate: runner=PYTHON exit=1 failed=3 tests=['tests/orchestration/test_result_tour.py::test_tour_view_for_an_unreadable_stored_tour', 'tests/ui_server/test_tour_route.py::TestTourRoute::test_tour_endpoint_answers_200_with_the_error_for_an_unreadable_stored_tour', 'tests/cli/test_job_show.py::TestTourSection::test_an_unreadable_stored_tour_gives_tour_unreadable_and_exits_zero'] caught=True restored=True
m3 the slashed-path half is round 3's pattern again: runner=PYTHON exit=1 failed=2 tests=['tests/orchestration/test_result_tour.py::test_golden_generated_tour_equals_its_fixture', 'tests/orchestration/test_result_tour.py::test_a_model_stop_naming_an_invented_dotted_hyphenated_path_is_dropped_with_the_whole_path'] caught=True restored=True
m4 the slashed-path half no longer has to end at a word character: runner=PYTHON exit=1 failed=1 tests=['tests/orchestration/test_result_tour.py::test_a_model_stop_whose_body_ends_with_a_recorded_path_and_a_full_stop_is_kept'] caught=True restored=True
m5 the tour entry of handlers serves the ownership view: runner=PYTHON exit=1 failed=3 tests=['tests/ui_server/test_tour_route.py::TestTourRoute::test_tour_endpoint_answers_the_view_for_a_job_with_a_stored_tour', 'tests/ui_server/test_tour_route.py::TestTourRoute::test_tour_endpoint_answers_the_view_for_a_job_with_none_stored', 'tests/ui_server/test_tour_route.py::TestTourRoute::test_tour_endpoint_answers_200_with_the_error_for_an_unreadable_stored_tour'] caught=True restored=True
m6 the decoder accepts more than MAX_TOUR_STOPS stops: runner=VITEST exit=1 failed=1 tests=['decodeTourView refuses the whole view for nine stops'] caught=True restored=True
m7 the decoder accepts an anchor kind outside TOUR_ANCHOR_KINDS: runner=VITEST exit=1 failed=1 tests=['decodeTourView refuses the whole view for an unknown anchor kind'] caught=True restored=True
m8 tourNeighbours answers a next at the last stop: runner=VITEST exit=1 failed=2 tests=['tourNeighbours answers null past both ends', 'tourNeighbours answers null at both ends for a single stop'] caught=True restored=True
m9 tourPanelState answers stops for a tour with none: runner=VITEST exit=1 failed=1 tests=['tourPanelState reads empty for a loaded view with no stops'] caught=True restored=True
m10 loadTourView lets a rejected fetch throw: runner=VITEST exit=1 failed=1 tests=['loadTourView answers null, never throws, when the fetcher rejects'] caught=True restored=True
control (end) PYTHON: exit=0 failed=0 tests=[]
control (end) VITEST: exit=0 failed=0 tests=[]
restored byte-identical: True (all 10 mutations)
PRIMARY checkout git status --porcelain: (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
No mutation stayed green; no extra test was needed. `git worktree remove --force
.remedy-wt/f036-r4-mut`, `git worktree prune`, `git worktree list | wc -l` = 63 (matches step 4).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5a | deviated | split from the block's single C5 under constraint 2 — the tests plus the mutation tool together numstat to 721 insertions; declared here |
| C5b | deviated | the mutation tool half of the block's C5, split out for the same reason |
| C6 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | every mutation caught first run; no extra test needed |

## Authored-text proofs

`booking.diff` applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never edited,
never retyped. The two payloads (`booking.diff`, `plan.md`) were verified line count/byte
count/sha256 against the PAYLOADS table before use, and the committed `.agent/authored/f036-r4-*`
copies read back byte-identical to their sources via `git show` (G1, above). `.agent/plan.md` was
REWRITTEN to the payload file by `shutil.copyfile`, never hand-edited; its post-write sha256 equals
the payload table's own row and C2's resulting file hashes matched the reviewer's G2 table exactly
for all 3 files (see Verification, G2). No reviewer-authored text was applied outside these two
payloads; the S1–S6 view/route/section/regex-repair/browser-module/loader code, its tests
(Python, vitest, contract) and the mutation tool are worker-authored against the block's
specification, not transcribed from a payload.

## Deviations & assumptions

- **C5 split into C5a and C5b (constraint 2).** The block's single C5 — the tests of THE TESTS,
  `tests/ui_contracts/test_tour_view_contract.py`, and the mutation tool — numstats to 721
  insertions together (481 tests + 240 tool), over the 500-line cap. Split into C5a (the four test
  files, 481 insertions) and C5b (`.agent/authored/f036-r4-mutations.py`, 240 insertions), each its
  own subject, exactly as constraint 2 and the block's own C5 note ("split into C5a and C5b under
  constraint 2 if needed") anticipate. `## Next`'s and G5's references to "C5" in the block name
  the bundle step; this handback and G5 use `dfaf5b116` (C5b, the tip of the split) as the concrete
  commit.
- No other deviation. Every mutation in G5 was caught on the first (and only) official run; no
  additional test was needed. No red gate was hit; nothing under AGENTS.md "If Blocked" applies
  this round.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of this round (F036 round 4). (3) T003's second half — the overlay with its
spotlight, stepping and navigation to each anchor, its place in the shell, and a headless render.
Open-findings count: 1 (R-1087, landed and awaiting the reviewer's resolution). Operator-questions
count: 1.
