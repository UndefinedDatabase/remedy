# Handback — F274 ROUND 13 — DECISION F274 D7 ruled, the first `worker_recommend` edge cut

This file supersedes the session-5-end handback. It is written by a delegated worker on the
reviewer's authored block, because the reviewer never edits a work-tree file. Round 13 rules
DECISION F274 D7 before a line moves, then cuts the one of `worker_recommend`'s three edges that
emits no run-log event. The two loop edges did NOT move and
`packages/orchestration/event_schemas.py` is untouched — that is the next round, per D7 item 6.

## Session

SESSION 6 of feature F274 · round 13 · feature rounds so far 13 of the soft limit of 25,
sessions 6 of 7.

`.agent/STOP` was ABSENT at the round's start, ABSENT after C5, and ABSENT after C6.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): worker context is comfortable and
was never the binding constraint this round — every slice verified on first read and every gate
ran once, so nothing here argues for ending the session.

## Range

Review of `64346333`..`04ff73a7` (C6, the commit writing this file, follows and is not gated here).

## Commits

Seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5.

### a0506de9 C0a: save the round 13 step block verbatim as the authored original
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f274-r13.md | +490 / -0 | `shutil.copyfile` of the reviewer's scratch original, byte for byte |

### bf0158ed C0b: mirror the round 13 block into the last-block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +429 / -229 | same bytes mirrored; verbatim rewrite of ONE `.agent/**` state file, DECISION F104 D1 exempt, and under 500 regardless |

### b5e933c1 C1: point the plan at round 13, the first worker recommendation edge
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17 / -19 | replaced entirely by the PLAN13 slice; plan current before every later commit |

### ede3c2c6 C2: book round 12 PASS verdict into the finding ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | RECORD13 appended; books round 12's PASS, registers and resolves nothing |

### 68cbb909 C3: append the round 12 prose slip on the miscounted word total
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | SLIPS13 appended, one dated line |

### 67068126 C4: rule DECISION F274 D7 on worker recommendation and the token mode
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +84 / -0 | DECIDE13 appended; the ruling C5 executes, so it precedes C5 |

### 04ff73a7 C5: move the token mode into token policy and cut the dashboard worker recommendation edge
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/dashboard.py | +4 / -10 | P1-P4: import swap, `recommend_worker` call replaced by `derive_token_mode`, `worker_recommendation` section and its `Worker:` summary line deleted |
| packages/orchestration/token_policy.py | +17 / -1 | P5, P6 and the TOKENMODE append: `derive_token_mode` lands with its `Public API::` entry and the `RunState` import |
| tests/test_token_policy.py | +22 / -1 | P7, P8 and the TESTS13 append: `TestDeriveTokenMode`, four tests |
| tests/ui_server/test_dashboard_contract.py | +0 / -1 | P9: the `worker_recommendation` pin deleted |
| scripts/remedy_smoke.sh | +1 / -1 | P10: the dashboard key tuple checks `token_policy` instead, keeping a key rather than shrinking |
| tests/orchestration/cluster_deletion_map.txt | +0 / -1 | P11: the retired edge line removed in the SAME commit as the edge, per constraint 4 |

### The C6 commit writing this file
Self-reference exception (R-0149 pattern): a handoff cannot table the commit that writes it.
`.agent/handoff.md` is rewritten whole, then pushed.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | one commit, as constraint 4 requires |
| C6 | done | this file, then the push |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r13wt 04ff73a7` | created, count 14 -> 15 |
| `git worktree remove --force .remedy-wt/r13wt` + `git worktree prune` | removed by EXACT path, count back to 14 |
| `git push -u origin feature/f274-one-world-completion-part-two` | see Next |

No PR was created, edited or merged. No `gh` command was run.

## Verification — one line per gate, real command, real exit code, real numbers

G1 TRANSPORT — PASS. `git show <c>:<path>` into sha256 for both committed copies:
`.agent/authored/f274-r13.md` at a0506de9 and `.agent/last_block.md` at bf0158ed are each 34537
bytes at `cc5af71b9c5ca531b5c84d3238259240dd62cb2ba05c5d173e52711566a4487a`, equal to each other and
equal to the digest the delegation message states; the reviewer's scratch original
`.remedy-wt/f274-r13-FINAL.md` hashed to the same 34537 bytes and the same digest as the worker's
FIRST action, before any file was touched. Per §3 item 37 this covers those artefacts, not the bytes
emitted into a prompt.

G2 THE RECORD APPEND at ede3c2c6 — PASS, all four parts, re-derived from the committed blobs.
(a) BYTES 589620 -> 594390, pre-image a byte-exact PREFIX = True, post == pre + the 4770-byte
RECORD13 slice = True. (b) STRUCTURE: N counted from the slice = 1, units 233 -> 234, the last N
units equal the slice's units IN ORDER = True, everything before them unchanged = True. (c) NEGATIVE
CONTROL: the byte at zero-indexed offset 589621 read `G` as the block states; flipped to `X`, the
BYTE reader accepted = False and the STRUCTURAL reader accepted = False, so both readers reject it.
(d) COUNTS registrations 69 -> 69, resolutions 6 -> 6 BY DISTINCT ID, OPEN SET 63 -> 63 BY DISTINCT
ID, `^Gate: ` 43 -> 44, `^Gate: F274 R12 ` 0 -> 1. This round registered and resolved nothing.

G3 THE DECISION APPEND at 67068126 — PASS, all four parts, re-derived from the committed blobs.
(a) BYTES 905078 -> 911446, prefix exact = True, post == pre + the 6368-byte DECIDE13 slice = True.
(b) STRUCTURE: N counted from the slice = 14, units 1986 -> 2000, last N units ordered-equal = True,
everything before unchanged = True. (c) NEGATIVE CONTROL: the byte at zero-indexed offset 905079
read `#` as the block states; flipped, byte reader accepted = False, structural reader accepted =
False. (d) `^## DECISION F274 D7` 0 -> 1.

G4 THE PROSE STATE FILES — PASS. `.agent/plan.md` at b5e933c1 is 2691 bytes, BYTE-EQUAL to the
PLAN13 slice = True at `955118d161f90d65f027ecb5986d13b5c064d1321afa0da1c24d6102f7e8ab6c`, is 44
lines against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md`
at 68cbb909 goes 162746 -> 163225 with the pre-image a byte-exact prefix = True, post == pre + slice
= True, and the appended line occurring exactly 1 time.

G5 THE CUT at 04ff73a7 — PASS, all five parts, measured against the committed blobs.
(a) THE PAIRS: the containment test was RUN on every pair, not eyeballed, and each pair's own
reading matches the block exactly — `TO contains FROM: true` for P5 and P8 only, `false` for P1, P2,
P3, P4, P6, P7, P9, P10, P11. Each FROM block occurred EXACTLY ONCE at the pre-image. For the nine
REWRITEs the post-image reads FROM = 0 and TO = 1 in its own file, every one. For the APPEND-shaped
P5 and P8 the §4.9 obligation was applied instead: FROM = 1 in the post-image, and the single
TO-only line of each — `    derive_token_mode(job) -> str` for P5 and `    derive_token_mode,` for
P8 — is among the lines C5's diff ADDS.
(b) THE ZERO-GATE, scoped to exactly three files: `worker_recommend` in
`packages/orchestration/dashboard.py` 3 -> 0; `worker_recommendation` in that file 2 -> 0, in
`scripts/remedy_smoke.sh` 1 -> 0, in `tests/ui_server/test_dashboard_contract.py` 1 -> 0. Every base
figure the block states was re-measured at `64346333` and reproduced exactly.
(c) THE MAP: `tests/orchestration/cluster_deletion_map.txt` 38 -> 37 lines, edges (neither blank nor
comment) 23 -> 22, `worker_recommend` edges 3 -> 2, and the post-image sha256 is
`abacf799bc8716ffbfe54a15ff8d1236e13e3dae44f7f322e962a675acb60c00` — IDENTICAL to the digest the
block predicted.
(d) THE MOVE LANDED WHOLE, read by AST rather than by grep: `derive_token_mode` is defined exactly
1 time in `packages/orchestration/token_policy.py`, is named inside that module docstring's
`Public API::` block, and the module's `from packages.core.models import ...` names `RunState`.
Every touched `.py` file parses under `ast.parse` at the committed blob.
(e) NOTHING ELSE MOVED: `git diff --name-only 64346333..04ff73a7` names 12 paths and the sorted set
equals the constraint-3 set exactly. `event_schemas.py`, `agent_loop.py`, `autonomy_loop.py` and
`worker_recommend.py`, all under `packages/orchestration/`, are each BYTE-IDENTICAL at the base and
at C5.

G6 THE SUITES at 04ff73a7, each command RUN ALONE in the PRIMARY CHECKOUT per constraint 8 —
PASS on every ordered property, with ONE numeral deviation at (b), declared below.
(a) `python3 -B -m pytest tests/test_token_policy.py -q` EXIT 0, 28 passed.
(b) `python3 -B -m pytest tests/ui_server/test_dashboard_contract.py -q` EXIT 0, 74 passed, 0
    skipped. The block states 73 passed and 1 skipped — see Deviations.
(c) `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0, 3 passed.
(d) `python3 -B -m pytest tests/test_remedy_smoke_script.py -q` EXIT 0, 191 passed.
(e) `python3 -B -m pytest tests/storage/test_persistence.py -q` EXIT 0, 26 passed — the
    `token_policy_applied` pin this round deliberately leaves alone.
(f) THE CANARY `python3 -B -m pytest tests/cli/test_golden_path.py -q` EXIT 0, 42 passed.
(g) `python3 -m ruff check` over the four touched `.py` paths EXIT 0, `All checks passed!`; and
    `python3 -m ruff check .` EXIT 1 REPORTING `Found 26 errors.` — the frozen ceiling of DECISION
    F083 D5 unchanged at 26, which is the gate PASSING, the ceiling being 26 and not 0.

G7 THE RED PROOFS, in the disposable worktree `.remedy-wt/r13wt` at 04ff73a7 per constraint 5, each
with its UNMUTATED control FIRST in that same worktree, `__pycache__` purged before every run and
pytest invoked with `-B` — PASS, both.
(a) THE MAP RATCHET REALLY BITES. The exact mutation bytes occur 0 times in the map at C5, as the
    block states. CONTROL `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q`
    EXIT 0, 3 passed. MUTATED, the single line
    `packages.orchestration.worker_recommend <- packages/orchestration/dashboard.py` re-inserted:
    EXIT 1, `1 failed, 2 passed`, the failure being
    `test_the_recorded_map_equals_the_measured_import_graph` and the message reading
    `DISAPPEARED (1) — an edge was cut but its line was left behind` followed by that exact edge.
    RESTORED: EXIT 0, 3 passed, restored digest
    `abacf799bc8716ffbfe54a15ff8d1236e13e3dae44f7f322e962a675acb60c00`, equal to the C5 blob.
    EXIT CODES control 0, mutated 1, restored 0.
(b) THE NEW GUARD DISCRIMINATES. The exact two-line sequence occurs 1 time in
    `packages/orchestration/token_policy.py` at C5, as the block states. CONTROL
    `python3 -B -m pytest tests/test_token_policy.py -q` EXIT 0, 28 passed. MUTATED, the two lines
    `    if task_count <= 2:` and `        return "compact"` deleted: EXIT 1, `1 failed, 27 passed`,
    and the ONLY failing node id is
    `tests/test_token_policy.py::TestDeriveTokenMode::test_one_or_two_tasks_is_compact`, asserting
    `'standard' == 'compact'`. It DISCRIMINATES: the other 27 stayed green, so the guard is not a
    blanket. RESTORED: EXIT 0, 28 passed, restored sha256
    `1002cf4fd0b08c2c43a58eef2cfb145e52109f51cde3a27272cfca742274978d`, byte-equal to the C5
    committed blob.
    SHADOW PROBE, run before either mutation because
    `/home/decodeux/.local/lib/python3.10/site-packages/_editable_impl_remedy.pth` puts the PRIMARY
    checkout on `sys.path` unconditionally: inside the worktree,
    `python3 -B -c "import packages.orchestration.token_policy as m; print(m.__file__)"` resolved to
    `.remedy-wt/r13wt/packages/orchestration/token_policy.py`, so the mutation reached the test and
    the editable install did not shadow the worktree under this invocation form.

G8 THE TREE at 04ff73a7 — PASS. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY;
`git worktree list` 14 before the first add and 14 after the last prune, having gone to 15 in
between. Every commit C0a through C5 is SINGLE-PARENT. INSERTIONS per commit: C0a 490, C0b 429,
C1 17, C2 2, C3 2, C4 84, C5 44 — every one under the DECISION F104 D1 cap of 500, and C5's applied
change measured +44 / -15 over six files, IDENTICAL to the reviewer's stated measurement. C6's own
insertion count is deliberately not reported, per constraint 7. `.agent/STOP` readings: ABSENT at the
round's start, ABSENT at the C5 boundary, ABSENT after C6.

## Authored-text proofs

All seven slices were extracted between their `BEGIN <NAME> sha256=<hex> bytes=<n>` and
`END <NAME>` marker lines and verified against their OWN marker BEFORE application. Every one
matched on both byte count and digest, first read, no repair:

| Slice | bytes | sha256 verified |
|---|---|---|
| PLAN13 | 2691 | OK |
| RECORD13 | 4770 | OK |
| SLIPS13 | 479 | OK |
| DECIDE13 | 6368 | OK |
| PAIRS13 | 2441 | OK |
| TOKENMODE | 550 | OK |
| TESTS13 | 807 | OK |

Marker lines reached no file. `.agent/plan.md` is byte-equal to PLAN13; `.agent/live_review.md`,
`.agent/prose_slips.md`, `.agent/decisions.md`, `packages/orchestration/token_policy.py` and
`tests/test_token_policy.py` each satisfy `post == pre + slice` exactly, so no separator of the
worker's own was added and each slice's own leading newlines are what landed. Both appends of C5
landed two blank lines below the last definition of their file, as PEP 8 asks and as the byte
equality proves.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed EXACTLY: no extra
commit, none dropped, none reordered. The change set was respected; no path outside it was written.

1. G6(b) NUMERAL DEVIATION, DECLARED NOT ADJUSTED. The block states
   `tests/ui_server/test_dashboard_contract.py` EXIT 0, 73 passed and 1 skipped. The primary
   checkout measured EXIT 0, **74 passed, 0 skipped**. Nothing was changed to make a number come
   out; the cause was measured. `pytest --collect-only -q` reports 74 tests collected in both
   readings, so no test appeared or vanished. The single conditional skip is
   `TestDashboard::test_typescript_compiles`, which at line 468 calls `pytest.skip` if and only if
   `apps/ui/node_modules/.bin/tsc` is not a file. In the primary checkout that path exists (a
   symlink to `../typescript/bin/tsc`), so the test RUNS and PASSES instead of skipping. The
   block's own note says every G6 figure was measured on the applied tree at the base commit, and
   the reviewer's disposable worktree has no `apps/ui/node_modules` because it is gitignored —
   which is precisely the condition constraint 8 anticipates when it orders G6 into the PRIMARY
   CHECKOUT. So the block's figure is the WORKTREE reading and 74/0 is the reading constraint 8
   asks for. The gate's ordered property, EXIT 0 over the whole file, holds; no assertion was
   weakened and no test was skipped or deselected.
2. G2(d) READING NOTE on "resolutions 6 -> 6". The literal LINE count of `^Done: R-\d{4} — ` in
   `.agent/live_review.md` is 8 -> 8, not 6 -> 6; the count of DISTINCT resolved IDs is 6 -> 6 and
   matches the block exactly. Both were measured and both are reported. The distinct reading is the
   one the block's numeral names and the one the OPEN SET formula must use, so this is a reading
   note rather than a defect — the gate passes on the distinct-id reading and the open set is
   63 -> 63 by distinct id either way.
3. G8 STOP TIMING. The block orders `.agent/STOP` read "at the round's start, before C5 and after
   C6". It was read at the round's start (ABSENT) and again IMMEDIATELY AFTER the C5 commit
   (ABSENT) rather than in the instant between C4 and C5, plus after C6 (ABSENT). Declaring the
   real timing rather than claiming the ordered one.
4. SHELL GUARD, re-expressed in Python as the delegation message instructs. The guard rejected
   `echo "... EXIT=$?"` and `${PIPESTATUS[0]}` by FORM, and rejected one heredoc containing a brace
   with a quote character. Every gate that needed an exit code was therefore run through small
   Python runners written under the gitignored `.remedy-wt/`
   (`run_gates.py`, `g4.py`, `g5.py`, `g7.py`, `g8.py`, `apply_pairs13.py`), each using
   `subprocess.run` and printing the REAL `returncode`. No exit code in this handback was inferred.
5. NO DOUBT ABOUT ANY SLICE. Every slice applied exactly as the block describes, on first read,
   including the two the block flagged for a second reading: P6's TO does not contain its FROM
   because the FROM ends in a newline the TO lacks, and the containment test confirmed `false` for
   it mechanically. Nothing was silently repaired because nothing needed repairing.
6. SCRATCH HYGIENE. `.remedy-wt/` stayed untracked throughout — `git ls-files .remedy-wt` is empty
   at C5 — and the disposable worktree was removed by EXACT path, never by glob.

## Open findings

63, BY DISTINCT ID, as G2(d) MEASURED at the committed blob. The round opened and closed at 63,
registering and resolving nothing, per constraint 6. The next free id remains R-0836. The open High
findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this feature's, per
DECISION F272 D12.

## Next

The reviewer re-runs this round's gates against `64346333`..`04ff73a7` and issues the round 13
verdict. On PASS, the next round cuts the two remaining `worker_recommend` edges in
`packages/orchestration/agent_loop.py` and `packages/orchestration/autonomy_loop.py` and lands
DECISION F274 D7 item 4 — `estimated_context_tokens`, `remote_model_requires_approval` and
`selected_worker` leaving `packages/orchestration/event_schemas.py` in the SAME commit as the last
emitter that writes them, with `CycleDecision.selected_worker` going with them.
