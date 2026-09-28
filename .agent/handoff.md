# Handoff — F035, round 8 (the closure sequence's first round: book round 7, register and repair
R-1085 and R-1086, write the Built State, consolidate the checklist, and take the feature's one
full suite)

## Session

SESSION 1 of feature F035 · round 8 · rounds so far 8. Context remaining at handback: a
comfortable majority of the budget is left — the round read AGENTS.md, the block, the three
payloads and the handback template once; read `docs/roadmap/STATUS_closure_protocol.md`
preconditions 2/3/7, `docs/agents/integration_gate.md`, both CSS modules' `.ownershipList` rules,
`test_r_1083_both_ownership_lists_take_the_panel_s_type_scale` and the surrounding contract test
file, the module docstring of `tests/ui_server/test_ownership_e2e_live.py`, round 7's mutation
tool (`.agent/authored/f035-r7-mutations.py`) as the pattern for this round's, and round 7's own
`.agent/handoff.md` and two prior `*-closure-suite.txt` files as format precedent; ran the
contract test standalone once before committing C3, the mutation tool twice (once misplaced in
`.agent/authored/` — caught by the self-review loop before any commit, moved to the gitignored
worker directory, re-run there so G4's "PRIMARY checkout git status --porcelain, empty" reading
was genuine), the G3 selection once, `integrity check` once, the UI build once and the full suite
once.

## Range

Review of `9c42693fb`..`HEAD` (`HEAD` is this handback's own commit, `F035 R8 C6`, on
`feature/f035-ownership-ledger`).

## Commits

### 0e21a44b4 F035 R8 C1: copy round 8 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r8-block.md | 175/0 | verbatim copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f035-r8-booking.diff | 46/0 | verbatim copy of the booking.diff payload |
| .agent/authored/f035-r8-closure_docs.diff | 110/0 | verbatim copy of the closure_docs.diff payload |
| .agent/authored/f035-r8-plan.md | 29/0 | verbatim copy of the plan.md payload |

Measured insertions: 360 (175+46+110+29). Block expected the block's own line count (175) plus
185 = 360. Match, under the 500-line cap.

### 0e59ffb58 F035 R8 C2: book round 7, resolve R-1083 and R-1084, register R-1085 and R-1086, record D8
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 19/0 | DECISION F035 D8 appended by `git apply booking.diff` |
| .agent/live_review.md | 8/2 | round 7's PASS Gate entry, R-1085's and R-1086's registrations, R-1083's and R-1084's `Landed:` lines replaced by `Done:` lines |
| .agent/plan.md | 9/9 | rewritten to the plan.md payload |

Measured numstat: 19/0, 8/2, 9/9 — equal to the block's G1 expectation exactly (the three files'
sha256 also matched the reviewer's simulation-tree reading; see Verification).

### 861d28954 F035 R8 C3: repair R-1085 and R-1086
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | `Landed: R-1085` and `Landed: R-1086` lines appended |
| apps/ui/src/components/detail/DetailPopover.module.css | 3/3 | `.ownershipList li + li`'s row gap is now a plain `6px`, under a comment naming the missing design-reference spacing token |
| apps/ui/src/components/graph/EvidencePanel.module.css | 3/3 | same repair, same comment |
| tests/ui_contracts/test_ownership_view_contract.py | 12/0 | one new test: neither module's `.ownershipList` rules name `--remedy-radius` |
| tests/ui_server/test_ownership_e2e_live.py | 4/3 | module docstring now says the run ends blocked because every remaining task was vetoed, in place of "completes normally" / "nothing parks"; nothing else in the file changed |

Measured insertions: 26 (4+3+3+12+4), 9 deletions. Under the 500-line cap.

### 5fa19d8b9 F035 R8 C4: add the round 8 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r8-mutations.py | 123/0 | the G4 red-proof tool: two mutations, each restoring `EvidencePanel.module.css`'s and `DetailPopover.module.css`'s row gap to `var(--remedy-radius-sm)`, an unmutated control first and last, restore-and-verify |

Measured insertions: 123. Under the 500-line cap. Committed AFTER G4 ran, per the block.

### 106e7db61 F035 R8 C5: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | 8/0 | the consolidation paragraph, inserted directly before "The next consolidation measures against 34." — that line occurs once before and once after (containment verified) |
| docs/roadmap/features/T5_F035.md | 83/0 | the Built State section: T001–T003, Acceptance, Deliberate absences, Findings |

Measured numstat: 8/0, 83/0 — equal to the block's G1 expectation exactly (both files' sha256
also matched the reviewer's simulation-tree reading; see Verification).

### This commit F035 R8 C6: record the closure suite transcript and rewrite handoff for round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-closure-suite.txt | 6/0 | the integration gate's transcript: command, real exit code, wall time, summary line, bad node ids (NONE), the tree (C5, `106e7db61`) |
| .agent/handoff.md | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- `git apply --check .remedy-wt/f035-r8-payloads/booking.diff` — exit 0; `git apply` the same —
  exit 0.
- `git apply --check .remedy-wt/f035-r8-payloads/closure_docs.diff` — exit 0; `git apply` the
  same — exit 0.
- `git worktree add .remedy-wt/f035-r8-mut HEAD` at C3 (`861d28954`) — succeeded; ran the round's
  mutation tool from the gitignored worker copy (both mutations caught on the only run); `git
  worktree remove .remedy-wt/f035-r8-mut` — succeeded, `git worktree list | wc -l` read 61
  afterward, unchanged from before.
- `npm --prefix apps/ui run build` at C5 — succeeded, exit 0, `git status --porcelain` empty
  after.
- `git push origin feature/f035-ownership-ledger` — reported in the reply per the block (G6
  cannot go in this file, written before the push).
- No PR created or merged — the block orders none, and none was created.

## Verification

G1 TRANSPORT AND RECORDS — payloads measured against the PAYLOADS table before use:
```
booking.diff:      46 lines, 11027 bytes, sha256 e79dfa7046fa5526f2e3efdae80dbc7aee8cb5035bcdd74114f08dcf6e90b3f0 — MATCH
closure_docs.diff: 110 lines, 8738 bytes,  sha256 e92816286879438731ce16dce0085418f85d56a03834436a3000fbed33392a8c — MATCH
plan.md:           29 lines, 1033 bytes,   sha256 fb11f045b48acc4dba3e8c48539d2245768071d2e9b6cf7308b0cb6124b34b1c — MATCH
```
Copies at C1, read back with `git show <C1>:<path>` and compared byte-for-byte against the source
by `diff`: `.agent/authored/f035-r8-block.md`, `.agent/authored/f035-r8-booking.diff`,
`.agent/authored/f035-r8-closure_docs.diff`, `.agent/authored/f035-r8-plan.md` — all IDENTICAL
(also matching the block's own stated table: block 175 lines / sha256
`cfa52dce3ebbed530bbc94b51360db3c8a710bb09c7a2f5a03f106e6639928d0`).

The booking, at C2 (`0e59ffb58`), `git show <C2>:<path>` read and hashed:
```
.agent/live_review.md 330639 bytes  18b60ad9c28928966cced64e1e9d964ca265fc70aecf8ad6c07bf1903430a2d9 — MATCH
.agent/decisions.md   2344873 bytes 4ecf75a9f53ad403edf83167bd594fb183f79c114dfa02efa1abd69962fb0f9a — MATCH
.agent/plan.md        1033 bytes    fb11f045b48acc4dba3e8c48539d2245768071d2e9b6cf7308b0cb6124b34b1c — MATCH
```
`scripts.rotate_live_review.open_finding_ids` over the current ledger text: `['R-1085',
'R-1086']` — equal to the reviewer's own reading. Lines beginning `Landed: R-1083` or `Landed:
R-1084`: 0 (both replaced by `Done:` lines by the booking diff).

`packages.orchestration.block_lint.live_checklist_items` over `docs/agents/planner_reviewer_prompt.md`:
34 items at `9c42693fb` and 34 items at C5 (`106e7db61`), same keys both times.

At C5, `git show <C5>:<path>` read and hashed:
```
docs/roadmap/features/T5_F035.md       11421 bytes  15c13450cb2f978129dbede9948fcbf1067a1bf55498f6aeeb6de360d268b98b — MATCH
docs/agents/planner_reviewer_prompt.md 108703 bytes f56e558c318dd471bd517716154d7b2b69fc48f7a1455cc16502e18ac8e94696 — MATCH
```

G2 THE LINTER — at C5 (`106e7db61`):
```
$ python3 -m apps.cli.main integrity block .remedy-wt/f035-r8/block.md
  [OK] item 1 (size): 175 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 29 lines
  [OK] item 10 (open set recomputed): states 2; .agent/live_review.md holds 2 open by distinct id, and the block registers 0 and resolves 0, leaving 2
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```

G3 THE TESTS AND THE TREE — serially, in the primary checkout at C5:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/docs/ tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/ui_contracts/test_ownership_view_contract.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_server/test_ownership_e2e_live.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py
551 passed in 65.45s (0:01:05)
REAL_EXIT=0
```
No SKIPPED line (grep count 0). Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0. `git status --porcelain` — empty, no untracked file.

G4 THE RED PROOFS — one run, over C3 (`861d28954`) in a disposable worktree: `git worktree add
.remedy-wt/f035-r8-mut HEAD` (HEAD was C3 at the time), then ran the mutation tool FROM ITS
GITIGNORED WORKER-DIRECTORY COPY (`.remedy-wt/f035-r8-worker/f035-r8-mutations.py`, identical
bytes to the one committed at C4) so that the tool's own not-yet-committed file never appeared in
the primary checkout's `git status --porcelain` while G4 ran:
```
control (start) PYTHON: exit=0 failed=0 tests=[]
m1 the row gap reads var(--remedy-radius-sm) again: exit=1 failed=1 tests=['tests/ui_contracts/test_ownership_view_contract.py::test_r_1085_neither_ownership_list_reads_a_radius_token'] caught=True restored=True
m2 the row gap reads var(--remedy-radius-sm) again: exit=1 failed=1 tests=['tests/ui_contracts/test_ownership_view_contract.py::test_r_1085_neither_ownership_list_reads_a_radius_token'] caught=True restored=True
control (end) PYTHON: exit=0 failed=0 tests=[]
restored byte-identical: True (m1 EvidencePanel.module.css)
restored byte-identical: True (m2 DetailPopover.module.css)
PRIMARY checkout git status --porcelain: (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
`git worktree remove .remedy-wt/f035-r8-mut` — succeeded; `git worktree list | wc -l` read 61
(equal to step 4's reading, unchanged).

G5 THE INTEGRATION GATE — the UI build, at C5:
```
$ npm --prefix apps/ui run build
✓ built in 2.17s
REAL_EXIT=0
```
`git status --porcelain` after — empty. Then the full suite, once, after C5:
```
$ python3 -m pytest -n auto -q
20294 passed, 20 skipped, 1 warning in 172.30s (0:02:52)
REAL_EXIT=0
```
Wall time 173s measured wall-clock (172.30s pytest-reported). Bad node ids (failed plus errors):
NONE. Saved verbatim to `.agent/authored/f035-closure-suite.txt`, naming the tree as C5
(`106e7db61`). Closure precondition 7: `tests/orchestration/test_import_reachability.py` and
`tests/test_no_orphan_modules.py` both ran inside that full-suite pass (0 failures overall) and
were separately re-confirmed together (`9 passed`, real exit 0) — neither holds a bad node.

## Authored-text proofs

`.agent/authored/f035-r8-block.md`, `.agent/authored/f035-r8-booking.diff`,
`.agent/authored/f035-r8-closure_docs.diff` and `.agent/authored/f035-r8-plan.md`, each compared
byte-for-byte at C1 against its payload source — all IDENTICAL (see G1 above). `booking.diff`'s
and `closure_docs.diff`'s own effects on `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` and
`docs/roadmap/features/T5_F035.md`, read at C2 and C5 by size and sha256 — all equal to the
reviewer's own reading (see G1 above).

## Deviations & assumptions

None. The bundle ran in the block's own order (C1–C6, no splits, no extra commits), every commit
under the 500-line cap, and every gate's measured reading matched the block's stated expectation
exactly. The one process note worth recording for a later reader: the mutation tool was drafted
first directly under `.agent/authored/` (the block's eventual home for it), which would have left
it untracked in the primary checkout while G4 ran, contradicting G4's own "PRIMARY checkout git
status --porcelain, empty" reading; caught by the self-review loop before any commit, the draft
was moved to the gitignored `.remedy-wt/f035-r8-worker/` instead, G4 ran from there, and only
after G4 read clean was the identical file copied into `.agent/authored/` for C4. No commit was
made, edited or reordered because of this — it left no trace in git history — so it is noted here
rather than filed as a commit-sequence deviation.

## Next

Per AGENTS.md Phase 1 rule 1 (read `.agent/STOP` from disk) and the block's own ordering: the
review of round 8, including the repairs of R-1085 and R-1086, then the closure's evidence round
— the booking of round 8 with those findings' resolutions, the self-use generator's reading, any
repair the suite requires, the evidence bundle and the review package — and then the closing
round. Open findings: 2 (R-1085 and R-1086, landed and awaiting review). Operator questions open:
0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 (`.agent/STOP` check) | done | absent |
| Step 2 (primary checkout, branch, HEAD) | done | |
| Step 3 (block byte verification) | done | |
| Step 4 (worktree/branch counts) | done | |
| Payload verification (3 payloads) | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| R-1085 | done | repaired in C3, landed |
| R-1086 | done | repaired in C3, landed |
| G1 Transport and records | done | |
| G2 The linter | done | |
| G3 The tests and the tree | done | |
| G4 The red proofs | done | both mutations caught on the only run |
| G5 The integration gate | done | build + full suite, 20294 passed, 20 skipped, NONE bad |
| G6 Tree and push | done | reported in the reply, not this file (block: "cannot go in C6") |
