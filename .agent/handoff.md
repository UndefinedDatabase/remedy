# Handback — F037 Rendered diff viewer, round 17

## Session

SESSION 5 of feature F037 · round 17 · rounds so far 17

Soft limit not reached: 17 of 25 rounds, session 5 of 7.

## Range

Review of `44a8493b..HEAD`, where HEAD is the C5 commit that writes this file.

## Commits

### 02a1686f docs(agent): save the F037 R17 step block

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r17.md | +362/-0 | C0a: the reviewer's block saved byte for byte |

### b5ff1e04 docs(agent): mirror the R17 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +339/-448 | C0b: the same bytes, extracted from the committed C0a blob |

### 637c2822 docs(agent): set the plan to F037 R17

| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +23/-26 | C1: full rewrite from the PLANF037R17 slice |

### f63d1d15 docs(agent): record the F037 R16 gate verdict

| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4/-0 | C2: the GATER16 slice appended |

### b5537973 feat(ui): open the diff envelope door in the api client

| Path | +/- | Reason |
|------|-----|--------|
| apps/ui/src/api/remedyApi.ts | +78/-0 | C3: SPEC S1–S5, the request shape, the fetcher type, `diffEnvelopePath`, `loadDiffEnvelope` and the two imports |
| apps/ui/src/api/remedyApi.test.ts | +71/-1 | C3: SPEC S6, one new `describe` of 8 `it` blocks; the edited line is the existing import |

### 91f7d8bd test(ui-contracts): pin the diff door against the server routes

| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_diff_envelope_door.py | +226/-0 | C4: SPEC S7, the cross-language guard (new file) |
| tests/ui_contracts/test_diff_view_render.py | +19/-0 | C4: SPEC S8, the `aria-expanded` polarity test |

### C5 docs(agent): hand back F037 R17

| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C5: this file; a handoff cannot table the commit that writes it (R-0149) |

## External actions

- `git worktree add .remedy-wt/f037-r17-wt 91f7d8bd --detach` — created, used for G6 only.
- `git worktree remove .remedy-wt/f037-r17-wt --force` + `git worktree prune` — removed; `git worktree list` shows the primary checkout alone.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
- `git push -u origin feature/f037-rendered-diff-viewer` after C5.
- No PR created, nothing merged, no history rewritten, no `remedy` CLI invoked.

## Verification

G1 HYGIENE — exit 0. `.agent/STOP` ABSENT before C0a; ABSENT again immediately before C5.
`git rev-parse HEAD` before C0a = `44a8493b46d274bcb6e461e41543485d102b5fec` = `44a8493b`.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` after C0a 0, C0b 0, C1 0, C2 0, C3 0, C4 0.

G2 TRANSPORT — exit 0. `git show 02a1686f:.agent/authored/f037-r17.md`: 25246 bytes, 362 lines,
sha256 `4dcbeecf2ac614c28f55206d91447fe5779b3f7c9560f9b362e4303959d42fa9`. All three equal the
three readings the delegation named (25246 / 362 / `4dcbeecf…`). `git rev-parse
b5ff1e04:.agent/authored/f037-r17.md` and `git rev-parse b5ff1e04:.agent/last_block.md` are the
SAME blob `a0a8dc82582c9e2715b2bbcbf91118c58fc4493b`.

G3 EXTRACTION AND CAPS — exit 0, measured on the committed C0a blob. PLANF037R17 46 content
lines, GATER16 3 content lines, CONTENT 49, TOTAL 362, PROSE = 362 − 49 = 313.
TOTAL <= 490 True. PROSE <= 400 True.

G4 THE PLAN AT C1 — exit 0. PLANF037R17 extracted programmatically from the committed C0a blob.
`git show 637c2822:.agent/plan.md` byte equal to the slice INCLUDING its trailing newline: True.
Negative control against the slice minus its trailing newline: False. `wc -l` 46, strictly under
50: True. Lines exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1.

G5 THE RECORD AT C2 — exit 0. GATER16 extracted from the committed C0a blob.
Reader (a) `git show 44a8493b:.agent/live_review.md` + one newline + slice ==
`git show f63d1d15:.agent/live_review.md`: True.
Reader (b) N = 2 (counted by the script from the slice's blank-line-separated units); the last 2
units of the committed file equal the slice's 2 units in order: True.
Negative control, one byte flipped inside the FIRST appended paragraph: reader (a) False,
reader (b) False. Pre-round blob is a byte PREFIX of the committed one: True.
Line-anchored over the committed file, base figure in brackets: `^- R-\d+ — ` 285 [285];
`^Done: R-\d+ — ` 34 [34]; `^Landed: R-` 1 [1]; `^Gate: F\d+ R\d+ — ` 87 [86, +1 = this round's
append]; open set 252 [252]; every registered id distinct: True (285 ids, 285 unique).
Note on the open set: 252 is the SET reading — registered ids minus the ids named by a `Done:`
or `Landed:` line. The arithmetic reading 285 − 34 − 1 = 250 at BOTH `44a8493b` and `f63d1d15`;
the block's figure of 252 is reproduced by the set reading, so that is the one reported.

G6 THE RED-PROOFS — all runs in the disposable worktree `.remedy-wt/f037-r17-wt` at the C4 tree
`91f7d8bd`, `__pycache__` purged before every run, `python3 -B` throughout, one pytest process at
a time, node set
`tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_view_render.py`.
- CONTROL BEFORE: exit 0, `25 passed in 0.23s`.
- Mutation (a) `task-runs` → `task-run` in `remedyApi.ts`. My reading before editing: the string
  occurs 1 time in that file, so no extension was needed. exit 1, `1 failed, 24 passed in 0.24s`,
  failing `tests/ui_contracts/test_diff_envelope_door.py::TestTheTaskRunScopeRouteAgrees::test_the_client_addresses_the_task_run_segment`.
  Restored byte-identically: True, sha256 `9345c4c746aff527…`.
- Mutation (b) delete the `catch` clause of `loadDiffEnvelope`. My reading before editing: `catch`
  occurs 5 times and `} catch {` 5 times in `remedyApi.ts`, so per the block I EXTENDED the string
  to the whole try/catch of `loadDiffEnvelope` — `  try {\n    const payload = await
  fetchPayload(diffEnvelopePath(request));\n    return readDiffEnvelope(payload);\n  } catch {\n
  return readDiffEnvelope(null);\n  }\n` — which occurs 1 time, and replaced it with the two
  statements alone so the rejection propagates and the file stays valid TypeScript.
  exit 1, `1 failed, 24 passed in 0.24s`, failing
  `tests/ui_contracts/test_diff_envelope_door.py::TestTheDoorNormalizesThroughOneFunction::test_the_loader_really_catches_a_rejection`.
  Restored byte-identically: True, sha256 `9345c4c746aff527…`.
- Mutation (c) drop `token=` from the diff path. My reading before editing: `token=` occurs 2
  times in `remedyApi.ts` (the other is `loadRemedyDashboard`'s), so I EXTENDED the string to
  ``  const q = `token=${encodeURIComponent(request.token)}`;\n`` — count 1 — and replaced it with
  ``  const q = `${encodeURIComponent(request.token)}`;\n``.
  exit 1, `1 failed, 24 passed in 0.24s`, failing
  `tests/ui_contracts/test_diff_envelope_door.py::TestTheTokenTravelsOnTheDiffRoute::test_the_diff_path_carries_the_token_parameter`.
  Restored byte-identically: True, sha256 `9345c4c746aff527…`.
- Mutation (d) `aria-expanded={!row.collapsed}` → `aria-expanded={row.collapsed}` in
  `DiffView.tsx`. My own count before editing: 1, which reproduces the reviewer's measurement.
  exit 1, `1 failed, 24 passed in 0.24s`, failing
  `tests/ui_contracts/test_diff_view_render.py::TestTheHunkHeadIsAControl::test_the_declared_state_is_the_negation_of_the_collapse_flag`.
  Restored byte-identically: True, sha256 `e13f97ecdd039353…`.
- CONTROL AFTER the last restore: exit 0, `25 passed in 0.23s`.
No mutation came back green.

G7 SUITES, TYPES, LINT AND CANARY AT C4 — primary checkout, one pytest process at a time.
- `python3 -m pytest tests/ui_contracts/ -q` → exit 0, `616 passed, 4 skipped in 5.44s`
  (603 passed, 4 skipped at base; +13 = 12 in the new door guard and 1 polarity test).
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → exit 0, `52 passed in 5.27s`
  (52 at base). This is the node that runs `npx vitest run`.
- `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -k typescript` → exit 0,
  `1 passed, 73 deselected in 1.93s`. The typescript node PASSED — it did NOT skip, so
  `apps/ui/node_modules/.bin/tsc --noEmit` really ran and the new door was type-checked.
- `python3 -m pytest tests/docs/ -q` → exit 0, `295 passed in 0.44s` (295 at base).
- `python3 -m ruff check tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_view_render.py`
  → exit 0, `All checks passed!`.
- canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.44s`
  (42 at base).
The new `describe` really EXECUTED: measured with a throwaway pytest probe under the gitignored
`.remedy-wt/` that spawns `npx vitest run --reporter=verbose src/api/remedyApi.test.ts` the same
way `test_test_runner.py::test_vitest_passes` spawns `npx vitest run` — exit 0,
`Test Files  1 passed (1)`, `Tests  64 passed (64)`, and all 8 `it` blocks of
`the diff envelope door` appear as individual `✓` lines. Nothing from that probe is committed.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C4 — exit 0.
`git diff --name-only 44a8493b..91f7d8bd` = `.agent/authored/f037-r17.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `apps/ui/src/api/remedyApi.test.ts`,
`apps/ui/src/api/remedyApi.ts`, `tests/ui_contracts/test_diff_envelope_door.py`,
`tests/ui_contracts/test_diff_view_render.py`.
ACTUAL MINUS EXPECTED: empty. EXPECTED MINUS ACTUAL: `.agent/handoff.md` alone.
`git diff --stat 44a8493b..91f7d8bd -- packages/` is EMPTY.
Per-commit insertions from `git show --numstat`, each under 500 and each matching the `+/-`
column of the `## Commits` tables above cell by cell: 02a1686f 362, b5ff1e04 339, 637c2822 23,
f63d1d15 4, b5537973 149 (78 + 71), 91f7d8bd 245 (226 + 19).
Lines matching `^<<<SLICE ` or `^<<<END ` at `91f7d8bd`: `.agent/plan.md` 0,
`.agent/live_review.md` 0, `apps/ui/src/api/remedyApi.ts` 0,
`tests/ui_contracts/test_diff_envelope_door.py` 0. CONTROL over the C0a blob: 4 — non-zero, so
the counter is shown not to be blind.
`git ls-files .remedy-wt | wc -l` = 0.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

- `.agent/authored/f037-r17.md` — copied with `cp` from `.remedy-wt/f037-r17-block.md`, not
  retyped. Disk-to-disk: sha256 of the copy `4dcbeecf2ac614c28f55206d91447fe5779b3f7c9560f9b362e4303959d42fa9`,
  25246 bytes, 362 lines — identical to the source file and to the three readings the delegation
  named. The committed blob reproduces all three (G2).
- `.agent/last_block.md` — written from `git show 02a1686f:.agent/authored/f037-r17.md`, never
  from this session's memory; one blob with the authored file at C0b (G2).
- `.agent/plan.md` — PLANF037R17 extracted programmatically from the committed C0a blob; byte
  equal at C1 including the trailing newline, negative control False (G4).
- `.agent/live_review.md` — GATER16 extracted programmatically from the committed C0a blob; both
  readers True, both negative controls False, base blob a byte prefix (G5).

## Deviations & assumptions

1. SPEC S6 says the test file "imports the three new exports". The door exports FOUR names
   (S1–S4: `DiffEnvelopeRequest`, `DiffEnvelopeFetcher`, `diffEnvelopePath`, `loadDiffEnvelope`).
   I imported THREE — `diffEnvelopePath`, `loadDiffEnvelope` and the type `DiffEnvelopeRequest` —
   and did not import `DiffEnvelopeFetcher`, since the fake fetcher is a plain arrow function and
   an unused type import would not compile clean. This is consistent with S7 (e), whose reach is
   "the same reach `tests/ui_contracts/test_diff_view_model.py` gives the model module", and that
   file's scan is over exported VALUES only, deliberately excluding `export interface` and
   `export type`. Declared because the block's numeral and the block's export list disagree and I
   applied the numeral.
2. S7 (e) says "every name the door EXPORTS". I scoped the scan to exported values whose name
   spells `diff` (case-insensitively), which yields exactly `diffEnvelopePath` and
   `loadDiffEnvelope`. An UNSCOPED scan of `remedyApi.ts` would have been red before this round
   for reasons outside it: the module predates the door and also exports `normalizePromptTrace`
   and `loadRemedyDashboard`, each of which `remedyApi.test.ts` names 0 times (measured). A
   fourth test in the not-vacuous class asserts the scan really reaches both door names, so the
   scoping cannot silently empty the set.
3. Mutation (b): the block names "the `catch` clause" as the replaced string. `catch` occurs 5
   times in `remedyApi.ts` and `} catch {` also 5 times, so per the block's own extension rule I
   extended to the whole try/catch of `loadDiffEnvelope` (count 1) and replaced it with its two
   statements. Reported in full under G6.
4. Mutation (c): `token=` occurs 2 times in `remedyApi.ts`, so I extended to the whole `const q`
   line of `diffEnvelopePath` (count 1). Reported in full under G6.
5. G7 asks me to state that the new `describe` really EXECUTED. `test_test_runner.py` asserts
   only vitest's return code, so I measured the reach with a throwaway pytest probe under the
   gitignored `.remedy-wt/`, spawning vitest exactly as that node does. It is not committed and
   `git ls-files .remedy-wt` is 0. Declared because the measurement is mine, not the block's.
6. `diffEnvelopePath` percent-encodes the task id as GIVEN rather than trimmed: a whitespace-only
   id selects the job scope per S3, but an id with surrounding whitespace is encoded intact,
   because silently rewriting a path segment would address a different resource than the caller
   named. S3 does not rule on this case and no test in the block's S6 list covers it.
7. No commit was added, dropped or reordered. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5
   was followed exactly.
8. No `remedy` CLI command was run; the environment denies it to subagents and no step needed it.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the plan | done | |
| C2 the R16 verdict | done | |
| C3 the envelope door and its vitest tests | done | S1–S6; see deviation 1 |
| C4 the cross-language guard and the polarity test | done | S7–S8; see deviation 2 |
| C5 the handback | done | this file |
| G1 hygiene | done | exit 0; STOP ABSENT twice; porcelain 0 after every commit |
| G2 transport | done | exit 0; all three readings match; one blob at C0b |
| G3 extraction and caps | done | exit 0; TOTAL 362, PROSE 313 |
| G4 the plan at C1 | done | exit 0; byte equal True, control False |
| G5 the record at C2 | done | exit 0; both readers True, both controls False |
| G6 the red-proofs | done | controls exit 0; all four mutations exit 1; see deviations 3 and 4 |
| G7 suites, types, lint and canary | done | six commands, every one exit 0; tsc PASSED, not skipped |
| G8 structure, artifacts, Open PR Gate | done | exit 0; set differences as ordered; no open PR |

## Next

The reviewer re-runs G1 through G8 over `44a8493b..HEAD` and issues the R17 verdict. Before
authoring R18 it re-reads `.agent/STOP` from disk (Phase 1 rule 1) and then checks the Open PR
Gate (rule 2). R18's expected subject is the first still-open piece of T003: mounting the viewer
behind the "Open diff" button of `component_spec.md:113-116`, with the opened-task state and
`DiffView` behind it — the door this round built is not called from anywhere yet.
