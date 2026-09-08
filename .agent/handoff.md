# Handback — F274 ROUND 9 — a DELETION ROUND: six cockpit sections and their six map edges cut

Written by the delegated worker. Every gate below was RUN, and every number in it is a real reading
taken with the command it names. No gate went red. Two clarifications are declared under
"Deviations"; neither is a repair and neither changed a byte on disk.

## Session

SESSION 5 of feature F274 · round 9 · feature rounds so far 9 of the soft limit of 25, sessions 5 of
7. Branch `feature/f274-one-world-completion-part-two`, base for every reading
`a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a`. `.agent/STOP` ABSENT at the start of the round. No pull
request exists and none was created.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context was not the binding constraint
for this round — the block arrived as a verified file on disk, every span it named matched the tree
exactly, and the only cost was the two full-suite runs at roughly three minutes each.

## Commits, in order

| # | SHA | + | - | Subject |
|---|---|---|---|---|
| C0a | `ec954a44` | 403 | 0 | save the round 9 step block verbatim as an authored artifact |
| C0b | `62ed9a19` | 327 | 159 | mirror the round 9 block into the last block state file |
| C1 | `bc237346` | 17 | 11 | point the plan at round 9, the six cockpit section deletions |
| C2 | `2aa946f0` | 4 | 0 | book round 8 PASS and the R-0819 recurrence in the record |
| C3 | `0f01d8ef` | 70 | 0 | land DECISION F274 D4 before a line is cut |
| C4 | `340e527b` | 4 | 0 | append the two round 8 prose slips to the slips log |
| C5 | `13f1d5e2` | 0 | 275 | cut six read-only cockpit sections and their six map edges |
| C6 | this file | — | — | the handback |

Every commit C0a through C5 is SINGLE-PARENT, verified with `git rev-list --parents -n 1`. Every
insertion count is under the 500-line cap of AGENTS.md DECISION F104 D1, and no oversize commit was
declared. C5's insertion count is ZERO: the cut adds no line to any file, which is what
amend0906-triage-throughput rule 1 requires of a deletion round.

## Changed files, `a903a44c..13f1d5e2`

| File | + | - |
|---|---|---|
| `.agent/authored/f274-r9.md` | 403 | 0 |
| `.agent/last_block.md` | 327 | 159 |
| `.agent/plan.md` | 17 | 11 |
| `.agent/live_review.md` | 4 | 0 |
| `.agent/decisions.md` | 70 | 0 |
| `.agent/prose_slips.md` | 4 | 0 |
| `packages/orchestration/ui_server.py` | 0 | 213 |
| `tests/orchestration/cluster_deletion_map.txt` | 0 | 6 |
| `tests/ui_server/test_dashboard_cockpit_truth.py` | 0 | 34 |
| `tests/orchestration/test_overnight_mission_integration.py` | 0 | 8 |
| `tests/orchestration/test_model_route_tournament_integration.py` | 0 | 14 |

Eleven paths, exactly the change set minus `.agent/handoff.md`, which this commit writes.

## Gates — one line per gate, real results

G1 TRANSPORT — PASS. The block was verified on disk BEFORE any work: `.remedy-wt/f274-r9-FINAL.md`
measured 34385 bytes at `a1cf8219765b1b75f8b23df24fcd4c40e806f1b373208bd59ee521996ceac95b`, exactly
the digest and byte count the delegation states; it was then copied with `shutil.copyfile` rather
than retyped, and the COMMITTED blobs of `.agent/authored/f274-r9.md` and `.agent/last_block.md` at
`62ed9a19` are both 34385 bytes at that same digest.

G2 THE RECORD APPEND — PASS, re-derived from the committed blobs `bc237346:` and `2aa946f0:`.
(a) 563333 -> 569829 bytes, pre-image a byte-exact PREFIX, post-image EQUAL to pre plus the
6496-byte RECORD9 slice with no separator added. (b) N counted from the slice itself is 2; units
225 -> 227; the file's last 2 units equal the slice's units IN ORDER and everything before them is
unchanged. (c) The byte at zero-indexed offset 563334 read as `G`, the `G` opening the first appended
paragraph; flipped in memory, the byte reader and the structure reader BOTH reject it. (d)
registrations 68 -> 68, resolutions 5 -> 5 BY DISTINCT ID, OPEN SET 63 -> 63 BY DISTINCT ID,
`^Gate: ` 39 -> 40, `^Gate: F274 R8` 0 -> 1, `^Landed: ` UNCHANGED at 37. This round spent no id and
the open set did not move in either direction.

G3 THE DECISION APPEND — PASS, re-derived from `2aa946f0:` and `0f01d8ef:`. (a) 889313 -> 894911
bytes, prefix true, post equal to pre plus the 5598-byte DECISION9 slice. (b) N from the slice is 9;
units 1959 -> 1968; last 9 units equal the slice's units in order; everything before unchanged. (c)
The byte at offset 889314 read as `#`; flipped, both readers reject it. (d) `^## DECISION F274 D4`
occurs exactly ONCE in the post-image and ZERO times in the pre-image.

G4 THE PROSE STATE FILES — PASS. `.agent/plan.md` at `bc237346` is BYTE-EQUAL to the 2808-byte PLAN9
slice, is 47 lines against the cap of 50, and carries both `## Goal` and `## Next Steps`.
`.agent/prose_slips.md` at `340e527b` goes 160319 -> 161300 bytes with the pre-image a byte-exact
prefix, post equal to pre plus the 981-byte slice, and each of the two appended lines occurring
exactly once in the post-image.

G5 THE DELETION ROUND'S FOUR MEASUREMENTS — PASS, at C5 `13f1d5e2`. (a)
`python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` EXIT 0, 3 passed. (b)
`python3 -m pytest -q -n auto` in the PRIMARY CHECKOUT: EXIT 0, 19785 passed, 23 skipped, 0 failed,
in 125s — exactly the reading the block predicted, and exactly six fewer passes than the 19791 at
the base. It was run TWICE and both runs were green; the R-0569 flake of constraint 9 did not appear
and nothing was edited. (c) Over all 1313 tracked files under `packages/`, `apps/`, `tests/` and
`scripts/` — enumerated with `git ls-files`, ALL FILE TYPES, NO FILTER, read as bytes — the six
deleted symbols total ZERO, against 18 at the base; each of the six individually reads 0. (d)
`python3 -m ruff check` over the four touched `.py` paths EXIT 0, "All checks passed!"; and
`python3 -m ruff check .` reports 26 errors, unchanged from the base, so DECISION F083 D5's frozen
ceiling is untouched.

G6 THE EDGE TRUTH AND THE RATCHET — PASS, in a disposable worktree at `.remedy-wt/f274r9wt` checked
out detached at `13f1d5e2`, with `__pycache__` purged first (0 directories found) and `python3 -B`
used for every run. (a) CONTROL `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q`
EXIT 0, 3 passed. (b) measured edges 31, recorded edges 31, sets EQUAL with APPEARED and DISAPPEARED
both empty; the cluster modules with NO measured edge are exactly the ten the block names —
`candidate_quality`, `context_optimizer`, `context_pack`, `external_builder_sandbox`,
`local_candidate_generator`, `model_route_tournament`, `overnight_mission`, `repair_loop_v2`,
`review_bundle` and `self_repair_proposal` — out of 24 cluster modules; the non-`.py` consumers the
widened walk finds are THE EMPTY LIST; and the two HELD modules still have exactly one edge each,
`packages.orchestration.overnight_readiness <- packages/orchestration/ui_server.py` and
`packages.orchestration.builder_routing <- packages/orchestration/ui_server.py`, which is the fact
DECISION F274 D4 turns on. (c) RED: the line
`packages.orchestration.repair_loop_v2 <- packages/orchestration/ui_server.py` occurs ZERO times in
the map after C5; appended back, the control command is EXIT 1, 1 failed 2 passed, reporting
`DISAPPEARED (1) — an edge was cut but its line was left behind` and naming that exact line. Restored
BY EXACT PATH, the file is byte-identical to the committed blob at
`d0cad9afd865deec689deba4f42e38c63d3f608e140e8bab55025113b3390722`, and the control returns to EXIT 0,
3 passed.

G7 THE CUT'S SHAPE — PASS, measured against the committed blobs at `13f1d5e2`. (a) LINE ARITHMETIC,
all five as ordered: `ui_server.py` 4278 -> 4065; `cluster_deletion_map.txt` 52 -> 46;
`test_dashboard_cockpit_truth.py` 450 -> 416; `test_overnight_mission_integration.py` 76 -> 68;
`test_model_route_tournament_integration.py` 111 -> 97. (b) PARSE AND STRUCTURE with `ast`: all four
`.py` blobs parse; the six deleted symbols are absent from `ui_server.py`'s top-level definitions
while `_build_overnight_section`, `_build_builder_routing_section` and `_build_dashboard` are all
still present; `TestDashboardShape` keeps 15 methods with the three deleted ones absent;
`TestSafeSurfaces` in the overnight file keeps `_job`, `test_review_bundle_summary_no_contract` and
`test_review_bundle_with_contract`; `TestSafeSurfaces` in the tournament file keeps `_job` and
`test_review_bundle_summary_safe`. (c) The map holds 31 non-comment lines and still holds both the
`overnight_readiness` and the `builder_routing` line.

G8 THE TREE — PASS. `git status --porcelain` EMPTY at every commit boundary; `git ls-files .remedy-wt`
EMPTY; `git worktree list` 14 before the first worktree, 15 while it existed, 14 after
`git worktree remove --force` and `git worktree prune`;
`git diff --name-only a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a..13f1d5e2` names exactly the eleven
paths of constraint 3 and nothing else; every commit C0a through C5 single-parent; per-commit
INSERTIONS 403, 327, 17, 4, 70, 4 and ZERO for C5.

## Deviations — two clarifications, no repairs

FIRST, THE READING OF "BOTH READERS" IN G2(c) AND G3(c), stated because a literal reading of one
clause is unmeetable by construction. G2(a) contains two byte properties: that the pre-image is a
PREFIX of the post-image, and that the post-image EQUALS pre plus the slice. A flip at zero-indexed
offset 563334 lies INSIDE the appended region — the pre-image ends at 563333 — so the prefix clause
alone cannot see it, and it returned true on the flipped image. The two readers taken as the gate's
two independent checks, the BYTE reader of (a) (`post == pre + slice`) and the STRUCTURE reader of
(b) (last N units equal the slice's units in order), BOTH rejected the flipped image, which is the
property the negative control exists to establish. The same holds at offset 889314 for G3(c). Nothing
was changed to make this pass; only the reading is declared.

SECOND, `ruff check .` EXITS 1, AND THAT IS THE GATE PASSING. G5(d) asks for EXIT 0 over the four
touched `.py` paths, which is what happened, and separately for `ruff check .` to report 26 errors
unchanged, which is what happened. The repo-wide command necessarily exits 1 while the frozen ceiling
is 26 rather than 0; the exit code is reported here so no later reader mistakes it for a red gate.

NOT A DEVIATION, RECORDED BECAUSE THE BLOCK ASKED FOR IT: constraint 9's known flake R-0569 did NOT
appear. Two consecutive full-suite runs under `-n auto` in the primary checkout were both green, so
no serial re-run of `tests/ui_server/test_command_channel.py` was needed and no file was edited.

ALSO CONFIRMED RATHER THAN ASSUMED: every span the block's C5 section names matched the tree at the
base exactly. `ast` placed the six functions at 596-631, 961-989, 1030-1066, 1069-1100, 1146-1176 and
1179-1208, each followed by exactly two blank lines, which is the block's 596-633, 961-991, 1030-1068,
1069-1102, 1146-1178 and 1179-1210 to the line; the six dashboard dict lines sat at 1951, 1952, 1953,
1956, 1957 and 1960 carrying the six named keys; and each of the six map lines occurred exactly once.
The deletion was applied bottom-up by symbol. The `"repair_loop"` key of the PIPELINE payload and the
`_build_overnight_section` and `_build_builder_routing_section` builders with their dict lines and
presence tests are UNTOUCHED, and `tests/orchestration/test_cluster_deletion_map.py` is unchanged.

## Open findings

63 BY DISTINCT ID at `13f1d5e2`, the number G2(d) measured: 68 distinct registrations against 5
distinct resolutions. Unchanged across this round, because round 9 spends no id — the R-0819
paragraph booked at C2 is a RECURRENCE under an already-open finding. The next free id is R-0835. The
open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this feature's, per
DECISION F272 D12.

## What this round moved

The deletion map went from 37 edges to 31, and the cluster modules with NO recorded edge went from
four to TEN: `candidate_quality`, `external_builder_sandbox`, `local_candidate_generator`,
`model_route_tournament`, `overnight_mission` and `repair_loop_v2` joined `context_optimizer`,
`context_pack`, `review_bundle` and `self_repair_proposal`. NO CLUSTER MODULE WAS DELETED — only
consumer edges were cut, and all 24 module files survive. DECISION F274 D4 landed at C3 before a line
was cut and rules why the number is SIX rather than the eight the round 8 handback measured:
`_build_overnight_section` and `_build_builder_routing_section` are HELD because their subject
modules are the sources of F260's two carry-overs, so cutting their edges would make the map read
"deletable" for two modules that are not.

## Next expected action

The reviewer re-runs G1 through G8 against the committed blobs of `a903a44c..13f1d5e2` and issues the
round 9 verdict. It is not booked into `.agent/live_review.md` by this round; under amend0827
rule 1 the pushed handback is the durable carrier and the verdict is booked by round 10's first
ledger commit.

Round 10, per the plan at `bc237346`, is `worker_recommend`'s three edges in `agent_loop.py`,
`autonomy_loop.py` and `dashboard.py` — LIVE RUNTIME CALLS rather than read-only views, so a DECISION
naming what inherits worker recommendation is authored before the cut. Then the two F260 carry-overs
with the cockpit sections this round held back, the surviving `ui_server.py` edges, the
`worker_facade_cmd.py` and `feature_cmd.py` edges, DECISION F260 D3, the cluster deletion itself, and
last T001 and T002.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a block saved verbatim | done | `ec954a44`, byte-for-byte file copy |
| C0b block mirrored | done | `62ed9a19`, same digest |
| C1 plan replaced by PLAN9 | done | `bc237346`, byte-equal, 47 lines |
| C2 RECORD9 appended | done | `2aa946f0`, round 8 PASS and the R-0819 recurrence |
| C3 DECISION9 appended | done | `0f01d8ef`, DECISION F274 D4 |
| C4 SLIPS9 appended | done | `340e527b`, two lines |
| C5 the cut | done | `13f1d5e2`, 275 deletions, 0 insertions |
| C6 the handback | done | this file, then pushed |
| G1 transport | done | PASS |
| G2 record append | done | PASS |
| G3 decision append | done | PASS |
| G4 prose state files | done | PASS |
| G5 deletion round measurements | done | PASS |
| G6 edge truth and ratchet | done | PASS |
| G7 the cut's shape | done | PASS |
| G8 the tree | done | PASS |
| Round 9 verdict booked | not done — carried | the reviewer issues it; round 10's first ledger commit books it |
| Pull request | not done | none exists and none was ordered; the branch is pushed |
