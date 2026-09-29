# Handback — F042 round 8: the first closure repair round (R-1112), repaired tree's suite RED on an unrelated node

## Session

SESSION 2 of feature F042 · round 8 · rounds so far 8. Context self-assessment: ample budget
remains — well under half of the session's context window has been used through C4 and the gates.

## Range

Review of `c83be2032`..`<this commit>`.

## Commits

### `8db686033` F042 R8 C1: copy round 8 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r8-block.md | +163 | this round's block, copied verbatim |
| .agent/authored/f042-r8-records.diff | +14 | payload copy |
| .agent/authored/f042-r8-plan.md | +29 | payload copy |
| .agent/authored/f042-r8-fix.diff | +98 | payload copy |

Total 304 insertions (block's 163 + 141), matching the block's stated formula exactly; measured
`git show --numstat`: 163/0, 98/0, 29/0, 14/0.

### `1dec70291` F042 R8 C2: book F042 R7 with R-1107's resolution, register R-1112
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | round 7's gate entry booked VERDICT PASS; R-1107's `Done:` resolution; R-1112 registered |
| .agent/plan.md | +8/-8 | rewritten to round-8-in-progress state, from the plan.md payload |

Measured `git show --numstat`: 6/0 .agent/live_review.md, 8/8 .agent/plan.md — equal to the
block's expected numstat exactly.

### `aee178ef7` F042 R8 C3: give the unknown-project test a fixed uuid and refuse fresh values in parametrize arguments (R-1112)
| Path | +/- | Reason |
|---|---|---|
| tests/test_parametrize_ids_stable.py | +70/-0 | NEW FILE at tests/test_parametrize_ids_stable.py — a repository test that walks every `@pytest.mark.parametrize` call and refuses a call to a fresh-value source (`uuid4`, `token_hex`, `random`, `now`, …) inside its argument list |
| tests/ui_server/test_projects_route.py | +2/-2 | R-1112: `test_an_unknown_project_is_404`'s parametrize id fixed to a literal uuid; the now-unused `uuid4` import dropped |

Measured `git show --numstat`: 70/0 tests/test_parametrize_ids_stable.py, 2/2
tests/ui_server/test_projects_route.py — equal to the block's expected numstat exactly.

### `<this commit>` F042 R8 C4: record the repaired tree's suite transcript and rewrite handoff for round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-closure-suite.txt | rewrite | the repaired tree's one full-suite transcript — RED, 1 failed node unrelated to R-1112 |
| .agent/handoff.md | rewrite | this handback, per the write-once rule |

## External actions

- `git worktree add --detach .remedy-wt/f042-r8-mut aee178ef7` (G3's gated run) — removed via
  `git worktree remove --force` as G3's last action; `git worktree prune` run after;
  `git worktree list | wc -l` read 26 both before and after.
- `git push` after this commit: real outcome reported in the worker's final reply, since this file
  cannot record a push that follows it.
- No PR created, merged or edited. No self-use runner and no job that calls a provider was
  invoked this round.

## Verification

**BEFORE ANYTHING ELSE:** step 1 `ls .agent/STOP` — absent. step 2 `pwd`
`/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f042-multi-project-cockpit`; `git log --oneline -1` `c83be2032` — all matched. step 3
block measured at 163 lines, sha256
`a452645dcf3aedeb9fd3534afa5e4461691e742c54e3f5b27fbb04201fc4b097` — equal to the delegation
message's two readings exactly. step 4 `git worktree list | wc -l` 26; `apps/ui/dist/index.html`
present (414 bytes, from round 7's build).

**PAYLOADS:** all three measured exactly against the table — records.diff 14/8267/
`46881abfaef65f24ae9cd788fa7b4c6ef8cefe3263fa4ed36884615344a088b1`, plan.md 29/1018/
`620f83cfc5c61914c80314a935209ba58924e8f60d7e0b6fd28bae3d01c76082`, fix.diff 98/3607/
`b65865d024bd2637d9465457c00c04ffba0e816ba3eb883cbc2e6ccccee0a254` — full hashes match the
block's table digit for digit.

**C1–C3:** every `git apply --check` and `git apply` exit 0; every `git show --numstat` read
matched the block's expected numstat exactly (see per-commit tables above). No payload was
retyped or edited; `.agent/plan.md` was rewritten via `shutil.copyfile` from the plan.md payload,
never retyped.

**C4(a) the suite:** `python3 -m pytest -n auto -q`, real exit code 1, wall time 225.9s measured
wall-clock (pytest's own report 225.08s / 0:03:45), summary line `1 failed, 20941 passed, 20
skipped, 1 warning in 225.08s (0:03:45)`. Log at
`.remedy-wt/f042-r8-worker/full_suite_r8.log`. THIS IS A PER-TEST FAILURE, unrelated to R-1112 —
all xdist workers collected the same set this run (round 7's collection defect is gone). Bad node:
`tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises`
(`AssertionError: 291 excused blind handlers, above the frozen 290`). No other FAILED/ERROR line.
Neither `tests/ui_server/test_projects_route.py` nor `tests/test_parametrize_ids_stable.py`
appears in the FAILED/ERROR list. `ps -eo pid,args | grep "[s]erver.py"` after: empty, no process.
Full detail, the shrink reading against round 7's 15-item set, and the precondition-7 reading are
committed verbatim in `.agent/authored/f042-closure-suite.txt`.

**G1 transport and records:** all three payloads' lines/bytes/sha256 matched the table exactly
(above); all four `.agent/authored/f042-r8-*` copies byte-identical to source at C1 (`git show
8db686033:<path>` vs. source bytes, all equal-length and equal); the read-at-commit table's four
rows (`.agent/live_review.md` and `.agent/plan.md` at `1dec70291`; `tests/ui_server/
test_projects_route.py` and `tests/test_parametrize_ids_stable.py` at `aee178ef7`) all matched the
block's stated bytes and sha256 exactly. `open_finding_ids` over `.agent/live_review.md` at
`1dec70291` read `['R-1112']`; `latest_gate_verdict` read `PASS` — both equal to the block's
stated values.

**G2 the tests:** the named serial selection (7 modules/dirs) read `448 passed` at exit 0 —
matching the reviewer's simulation-tree reading exactly. The two-file xdist selection read `13
passed` at exit 0 — matching the reviewer's reading exactly. `ruff check` on the two changed/new
test files: `All checks passed!`, exit 0. `integrity check --json`: six `pass`, `fail_count` 0.
`integrity block .remedy-wt/f042-r8/block.md`: exit 0, `All 7 checkable items pass.` `git status
--porcelain`: empty.

**G3 the red proof of R-1112's repair:** run against `git worktree add --detach
.remedy-wt/f042-r8-mut aee178ef7`, then `git -C ... checkout 1dec70291 --
tests/ui_server/test_projects_route.py` (pre-repair file, new test kept). Mutated (i)
`tests/test_parametrize_ids_stable.py`: exit 1, `1 failed, 1 passed in 2.08s`, assertion naming
`tests/ui_server/test_projects_route.py:111: uuid4()` — exact match to spec. Mutated (ii)
`tests/ui_server/test_projects_route.py` under `-n 2`: exit 1, xdist's `Different tests were
collected between gw0 and gw1` error, `1 error in 0.34s`. Restored with `git -C ... checkout
aee178ef7 -- tests/ui_server/test_projects_route.py`; control (i): exit 0, `2 passed in 2.08s`;
control (ii): exit 0, `11 passed in 1.62s` (see Deviations below for why an extra step was needed
to get an honest control-(ii) reading). Worktree removed (`git worktree remove --force`), pruned;
`git worktree list | wc -l` read 26 after (equal to before).

**G4 the suite:** covered in full above (C4a) — real exit code 1, wall time 225.9s (pytest
225.08s), summary `1 failed, 20941 passed, 20 skipped, 1 warning in 225.08s`, bad node id
`tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises` (the only one);
shrink reading: strictly smaller by count than round 7's 15-item set, but NOT "no newly bad node"
— the ble001 node is new to this round's bad set, round 7's set named no individual node at all.
`.agent/authored/f042-closure-suite.txt` committed. server.py reading: none. Closure precondition
7 (`tests/orchestration/test_import_reachability.py`, `tests/test_no_orphan_modules.py`): both
ran clean — neither appears in the FAILED/ERROR list, and G2's serial run on the identical tree
already read both green inside its `448 passed`.

## Authored-text proofs

All four `.agent/authored/f042-r8-*` files are byte-identical, source to committed copy, verified
at C1 (see G1 above). The applied diff (records.diff → `.agent/live_review.md`), the rewritten
`.agent/plan.md` (from the plan.md payload), and the applied fix.diff (→
`tests/ui_server/test_projects_route.py`, plus the NEW FILE `tests/test_parametrize_ids_stable.py`
it adds) were each verified byte-for-byte against the reviewer's stated sizes and sha256 at the
commit that applied them (G1's four-row table, all equal) — this confirms `git apply` and
`shutil.copyfile` reproduced the reviewer-authored text exactly, not only that the source payload
itself was uncorrupted.

## Deviations & assumptions

1. **The mutation worktree needed a copied, freshened `dist/` to get an honest G3 control-(ii)
   reading.** `git worktree add` does not carry gitignored build output, so
   `.remedy-wt/f042-r8-mut/apps/ui/dist` did not exist; the server's `_load_frontend` auto-build
   path then tried to run `npm run build` and failed loudly ("React UI not built"), on BOTH the
   mutated and the control runs of test (ii) — a false failure with nothing to do with R-1112.
   Copying the primary checkout's `apps/ui/dist` into the worktree via `shutil.copytree` was not
   by itself enough: `copytree`'s default `copy2` preserves the original (older) mtimes, while the
   worktree's freshly-checked-out `apps/ui/src` files all carry a newer checkout mtime, so
   `_frontend_is_stale()` still read stale and reassigned `dist` to `None` even with
   `REMEDY_UI_NO_AUTO_BUILD=1` set (the disabled-build branch also falls through to the "not
   built" failure). Bumping `dist/index.html`'s mtime 60 seconds into the future
   (`os.utime`) fixed it; control (ii) then read `11 passed` at exit 0. This only touched files
   inside the throwaway worktree, removed before G3's last action; no committed file, no test
   assertion and no route logic was touched, and the mutated-(ii) reading (which never reaches the
   frontend-serving code — it fails at collection) was unaffected by the whole issue. Justification:
   needed an honest "both controls at exit 0" reading per spec rather than a masked, unrelated
   server-side failure.
2. **The full suite (C4) is RED, and this round does not repair it.** Per block constraint 4 ("A
   RED full suite in C4 is this feature's work, not a stop... the next repair round is the
   reviewer's to order"), the transcript is committed exactly as measured
   (`.agent/authored/f042-closure-suite.txt`) and this handback documents it in full; no test or
   production file was touched to fix or route around it, no assertion was weakened, nothing was
   skipped or marked xfail. The one bad node,
   `tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises`, is unrelated to
   R-1112 and to every file this round's commits (C1–C3) touched — it is a handler-count ratchet
   whose frozen ceiling (290) the live codebase now exceeds by one (291), surfaced only because
   this is the first FULL suite run since round 7's collection-level abort masked all test-node
   results. The new bad set is strictly smaller than round 7's by count (1 vs. 15) but does hold a
   newly bad node — round 7's 15-item set was all worker-session collection errors naming no
   individual test node, so this is the first node-level reading of any kind this feature's full
   suite has produced.

No payload was retyped or edited. No existing test was edited to pass. No file outside the
round's tracked path set (constraint 3) was touched.

## Next

Per Phase 1 rule 1 and this round's own instruction: the review of round 8 and of its suite
transcript is next. Since the suite is RED, the reviewer's likely order is the next repair round
(repair round 2 of at most 3 under amend0917-throughput rule 2) for the ble001 ratchet finding —
unless the reviewer instead treats the 290 ceiling itself as the thing to move, which is the
reviewer's call, not this round's. Once the suite reads clean, the next steps stand as before: the
closure's evidence round (booking round 8, the reclaim of staging copies, the evidence bundle and
the review package), then the closing round.

Open findings: 1. Operator questions open: 0.
