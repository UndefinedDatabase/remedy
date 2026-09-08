# Handback — F274 ROUND 11 — a DELETION ROUND: the `feature` command group dies and two modules reach zero edges

Written by the delegated worker. Every gate below was RUN, and every number in it is a real reading
taken with the command it names. SIX GATES PASSED IN FULL. TWO GATES CARRY A RED CLAUSE — G7(b) and
G8 — and in both cases the red is a PREDICTED NUMERAL in the block that does not match the tree, not
a defect in the cut. Nothing was edited to make any gate green; the real numbers are stated below
beside the numbers the block predicted, under "Deviations".

## Session

SESSION 5 of feature F274 · round 11 · feature rounds so far 11 of the soft limit of 25, sessions 5
of 7. Branch `feature/f274-one-world-completion-part-two`, base for every reading
`fb0d56c419f7bc8441f461dac1a6ea1e44a044d7`. `.agent/STOP` ABSENT at the start of the round. No pull
request exists and none was created.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context was not the binding constraint
for this round — the block arrived as a verified file on disk whose digest and byte count matched
before a line was written, and the only real costs were one full-suite run at under three minutes and
two collect-only runs, but the round did spend extra reading resolving two of the block's predicted
line counts against the actual file structure before committing.

## Range

Review of `fb0d56c419f7bc8441f461dac1a6ea1e44a044d7`..`HEAD`.

## Commits, in order

| # | SHA | + | - | Subject |
|---|---|---|---|---|
| C0a | `51f7c541` | 405 | 0 | save the round 11 step block verbatim |
| C0b | `0c6a0c57` | 253 | 252 | mirror the round 11 block into the last block state file |
| C1 | `2ec3ed82` | 12 | 11 | point the plan at round 11 and the feature command deletion |
| C2 | `87e5249d` | 2 | 0 | book round 10 PASS in the record |
| C3 | `5c6a234b` | 69 | 0 | rule DECISION F274 D6 before the feature group is cut |
| C4 | `af99dcf8` | 2 | 0 | append the round 10 prose slip to the slips log |
| C5 | `43516dc7` | 2 | 226 | delete the feature command group, its wiring, its docs row and its two map edges |
| C6 | this file | — | — | the handback |

The `+/-` column is taken from `git diff --numstat` per commit and was compared cell by cell against
the counts G8 reports; the two agree. Every commit C0a through C5 is SINGLE-PARENT, verified with
`git rev-list --parents -n 1`. Every insertion count is under the 500-line cap of AGENTS.md DECISION
F104 D1, and NO oversize commit was declared. C5 is +2 / -226: the two insertions are exactly the two
lines the block declares in its header as EDITED rather than removed — the registration tuple in
`apps/cli/commands/__init__.py` and the narrowed sentence in
`docs/system/development-artifact-boundary-v0.md`. The DELETION count is 226 rather than the 217 the
block predicted; see "Deviations".

## Changed files, `fb0d56c4..43516dc7`

| File | + | - |
|---|---|---|
| `.agent/authored/f274-r11.md` | 405 | 0 |
| `.agent/last_block.md` | 253 | 252 |
| `.agent/plan.md` | 12 | 11 |
| `.agent/live_review.md` | 2 | 0 |
| `.agent/decisions.md` | 69 | 0 |
| `.agent/prose_slips.md` | 2 | 0 |
| `apps/cli/commands/feature_cmd.py` | 0 | 101 (DELETED, `git rm`) |
| `apps/cli/commands/__init__.py` | 1 | 2 |
| `apps/cli/command_catalog.py` | 0 | 29 |
| `pyproject.toml` | 0 | 1 |
| `docs/system/development-artifact-boundary-v0.md` | 1 | 2 |
| `tests/cli/test_progress_feature_runtime.py` | 0 | 87 |
| `tests/orchestration/cluster_deletion_map.txt` | 0 | 2 |
| `tests/orchestration/import_reachability_allowlist.txt` | 0 | 1 |
| `tests/orchestration/test_development_artifact_boundary.py` | 0 | 1 |

Fifteen paths, exactly the change set minus `.agent/handoff.md`, which this commit writes.
`packages/orchestration/feature_planner.py`, `packages/orchestration/progress_ledger.py` and their own
test files are UNTOUCHED, as the block requires: an edge cut is not a module deletion.

## External actions

`git worktree add --detach .remedy-wt/r11-base fb0d56c4` — created for the BASE collect-only reading
of G5(b), count 14 -> 15; removed with `git worktree remove --force` and `git worktree prune`, count
back to 14.
`git worktree add --detach .remedy-wt/r11-c5 43516dc7` — created for G6, count 14 -> 15; removed and
pruned the same way, count back to 14.
`git push` on `feature/f274-one-world-completion-part-two` after this commit. No `gh` command was run,
no PR was created, edited or merged. The `remedy` CLI was not used.

## Gates — one line per gate, real results

G1 TRANSPORT — PASS. The block was verified on disk BEFORE any work: `.remedy-wt/f274-r11-FINAL.md`
measured 32441 bytes at `47f17119d101c2246c23fa7a1a43804b9658031925f2e5d31058240d3d5a447f`, exactly
the digest and byte count the delegation states; it was then copied with `shutil.copyfile` rather than
retyped, and the COMMITTED blobs of `.agent/authored/f274-r11.md` and `.agent/last_block.md` at
`0c6a0c57` are both 32441 bytes at that same digest. All three files are byte-identical.

G2 THE RECORD APPEND — PASS, re-derived from the committed blobs `fb0d56c4:` and `87e5249d:`.
(a) `.agent/live_review.md` 574989 -> 579917 bytes, pre-image a byte-exact PREFIX, post-image EQUAL to
pre plus the 4928-byte RECORD11 slice with no separator added. (b) N counted from the slice itself is
1; units 228 -> 229; the file's last 1 unit equals the slice's unit and everything before it is
unchanged. (c) NEGATIVE CONTROL: the byte at zero-indexed offset 574990 read as `G`, the `G` opening
the first appended paragraph; flipped in memory to `g`, the BYTE reader of (a) — the
`post == pre + slice` clause the block names as carrying that half — and the STRUCTURAL reader of (b)
each rejected it. (d) registrations 68 -> 68, resolutions 5 -> 5, OPEN SET 63 -> 63 BY DISTINCT ID,
`^Gate: ` 41 -> 42, `^Gate: F274 R10` 0 -> 1, `^Landed: ` UNCHANGED at 37. This round spent no id.

G3 THE DECISION APPEND — PASS, re-derived from `87e5249d:` and `5c6a234b:`. (a) `.agent/decisions.md`
899779 -> 905078 bytes, prefix true, post equal to pre plus the 5299-byte DECISION11 slice. (b) N from
the slice is 9; units 1977 -> 1986; the last 9 units equal the slice's units IN ORDER and everything
before them is unchanged. (c) The byte at zero-indexed offset 899780 read as `#`, the `#` opening the
first appended paragraph; flipped, the byte reader and the structural reader each rejected it. (d)
`^## DECISION F274 D6` occurs exactly ONCE in the post-image and ZERO times in the pre-image.

G4 THE PROSE STATE FILES — PASS. `.agent/plan.md` at `2ec3ed82` is BYTE-EQUAL to the 2985-byte PLAN11
slice, is 48 lines against the cap of 50, and carries both `## Goal` and `## Next Steps`.
`.agent/prose_slips.md` at `af99dcf8` goes 161811 -> 162264 bytes with the pre-image a byte-exact
prefix, post equal to pre plus the 453-byte slice, and the one appended line occurring exactly once.

G5 THE DELETION ROUND'S FOUR MEASUREMENTS — PASS on every property; ONE PREDICTED NUMERAL IN (a) WAS
WRONG AT THE BASE TOO. All four ran AFTER the C5 commit `43516dc7`. (a)
`python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` EXIT 0, 3 passed in 1.25s,
exactly as predicted; `python3 -B -m pytest tests/docs/ -q` EXIT 0, 303 passed in 0.51s — the block
predicted 306. That suite is 303 AT THE BASE AS WELL, re-measured in a worktree at `fb0d56c4` (EXIT 0,
303 passed in 0.67s), so the number did not move this round and the block's 306 is a stale numeral,
not a lost test. (b) `python3 -m pytest -q -n auto` in the PRIMARY CHECKOUT per constraint 7: EXIT 0,
19765 passed, 23 skipped, 0 failed, 1 warning, in 157.43s — exactly the reading the block predicted.
THE DELTA AS A SET: `python3 -B -m pytest --collect-only -q` collected 19804 at the base (in a
disposable worktree at `fb0d56c4`) and 19788 at C5 (primary checkout); diffing the node-id SETS,
EXACTLY 16 ids DISAPPEAR and ZERO APPEAR, and the sixteen are exactly the eight the block names from
`TestFeaturePlanRuntime` and `TestFeatureAcceptRuntime` plus the eight `[feature]` parametrizations in
`tests/test_grouped_cli.py` (`TestBootcampStyleGroupHelp` x4, `TestGroupHelpContent`,
`TestGroupHelpExitsZero`, `TestGroupHelpNoLeaks`, `TestMainEntrypointDelegatesGroupHelp`). (c) Over all
1719 tracked files under `packages/`, `apps/`, `tests/`, `scripts/` and `docs/` — enumerated with
`git ls-files`, ALL FILE TYPES, NO FILTER, read as bytes and matched as FIXED strings — the five
strings `feature_cmd`, `_cmd_feature_plan`, `_cmd_feature_accept`, `feature.plan` and `feature.accept`
TOTAL ZERO, against 16 over 1720 files at the base. (d) `python3 -m ruff check` over the four
surviving touched `.py` paths EXIT 0, "All checks passed!"; and `python3 -m ruff check .` reports 26
errors, unchanged from the base, so DECISION F083 D5's frozen ceiling is untouched — that command
exits 1 while reporting them, which is the gate passing, because the ceiling is 26 rather than 0.

G6 THE EDGE TRUTH AND THE RATCHET — PASS, in a disposable worktree at `.remedy-wt/r11-c5` checked out
detached at `43516dc7`, with `__pycache__` purged first (0 directories found) and `python3 -B` used
for every run. (a) CONTROL `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q`
EXIT 0, 3 passed in 1.17s. (b) measured edges 23, recorded edges 23, sets EQUAL with APPEARED and
DISAPPEARED both empty; the cluster modules with NO measured edge are EXACTLY THE TWELVE the block
names — `candidate_quality`, `context_optimizer`, `context_pack`, `external_builder_sandbox`,
`feature_planner`, `local_candidate_generator`, `model_route_tournament`, `overnight_mission`,
`progress_ledger`, `repair_loop_v2`, `review_bundle` and `self_repair_proposal` — out of 24 cluster
modules, so `feature_planner` and `progress_ledger` joined the set this round; the non-`.py` consumers
are THE EMPTY LIST. (c) RED: the byte string
`packages.orchestration.feature_planner <- apps/cli/commands/feature_cmd.py` occurs ZERO times in the
map after C5; appended back as one line with no internal break, the control command is EXIT 1, 1
failed 2 passed, reporting `DISAPPEARED (1) — an edge was cut but its line was left behind` and naming
that exact line. Restored BY EXACT PATH from `git show 43516dc7:tests/orchestration/cluster_deletion_map.txt`,
the file is byte-identical to the committed blob at
`cfdbbe8ecdf2727a526cf49083265201d4f1ab43aabad85fe2204c29cf980702`, the worktree's
`git status --porcelain` is empty, and the control returns to EXIT 0, 3 passed.

G7 THE CUT'S SHAPE — (a) and (c) PASS; (b) IS RED ON TWO OF ITS EIGHT READINGS. Measured against the
committed blobs at `43516dc7`. (a) `apps/cli/commands/feature_cmd.py` is ABSENT from
`git ls-tree -r --name-only 43516dc7` and PRESENT at the base. (b) LINE ARITHMETIC, one reading per
surviving file — `apps/cli/commands/__init__.py` 102 -> 101 as ordered; `apps/cli/command_catalog.py`
4946 -> 4917 against the ordered 4918; `pyproject.toml` 158 -> 157 as ordered;
`tests/orchestration/import_reachability_allowlist.txt` 327 -> 326 as ordered;
`tests/orchestration/test_development_artifact_boundary.py` 299 -> 298 as ordered;
`docs/system/development-artifact-boundary-v0.md` 86 -> 85 as ordered;
`tests/cli/test_progress_feature_runtime.py` 160 -> 73 against the ordered 81;
`tests/orchestration/cluster_deletion_map.txt` 40 -> 38 as ordered. The two misses are arithmetic in
the block, not a wider or narrower cut; both are worked out line by line under "Deviations". (c) PARSE
AND STRUCTURE with `ast` rather than grep: all four surviving touched `.py` blobs parse;
`tests/cli/test_progress_feature_runtime.py` holds EXACTLY ONE class, `TestProgressChecklistRuntime`;
and the catalog at C5 holds NO `CommandEntry` whose `group_id` is `feature` and NO `GroupDef` keyed
`feature` (both walks returned the empty list).

G8 THE TREE — PASS except the declared insertion/deletion clause. `git status --porcelain` EMPTY at
every commit boundary; `git ls-files .remedy-wt` EMPTY; `git worktree list` 14 before the first
worktree, 15 while each existed, 14 after the last `git worktree remove --force` and
`git worktree prune`;
`git diff --name-only fb0d56c419f7bc8441f461dac1a6ea1e44a044d7..43516dc7` names exactly the fifteen
paths of constraint 3 and nothing else, with no extra and none missing; every commit C0a through C5
SINGLE-PARENT. Per-commit INSERTIONS and DELETIONS: C0a +405/-0, C0b +253/-252, C1 +12/-11, C2 +2/-0,
C3 +69/-0, C4 +2/-0, C5 +2/-226. C5's INSERTIONS ARE EXACTLY +2 AS ORDERED and they are exactly the
two declared edited lines; its DELETIONS are 226 against the ordered 217. C6's own numbers are not
reported here; the reviewer measures them at the next gate.

## Authored-text proofs

Four reviewer-authored slices applied this round, each verified against its own `BEGIN` marker BEFORE
it was written and each byte-exact:
PLAN11 2985 bytes `106a18864711787f43c19cd99f5313ef34a7453ec43d6c6556b77147b85d9ae3`;
RECORD11 4928 bytes `12b28768abafce8e529fb86dd8d556795dda3e2adfe4bf9816f2396fc1d44839`;
SLIPS11 453 bytes `9ea22e6f04c60bcc4fed7c0517382240a4da4db12dc50f0eb7f3820d097f2394`;
DECISION11 5299 bytes `7f898f1f84413b42adffcf1b2e5f3b43ab1539cae3bd88d38f3644dabc67d6dc`.
The block itself was transported as a FILE and copied with `shutil.copyfile`, never retyped; the
disk-to-disk comparison against the committed `.agent/authored/f274-r11.md` is byte-identical, and so
is the comparison against `.agent/last_block.md`.

## Deviations & assumptions

NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. The commits are C0a, C0b, C1, C2, C3, C4, C5,
C6 in exactly that order, with no extra commit, no dropped commit and no reordering. No file outside
the change set was written.

DEVIATION 1 — `apps/cli/command_catalog.py` ENDS AT 4917 LINES, NOT THE ORDERED 4918, AND THE BLOCK'S
TWO CLAUSES FOR THIS FILE CANNOT BOTH BE MET. The block orders, in prose, the removal of "the
contiguous run that begins at the banner comment `# ── feature ─` and ends at the last line of the
`feature.accept` `CommandEntry`, together with the blank line that follows it and before the
`# ── plan (` banner", plus the `GroupDef` line. The tree at the base puts the banner at 4346, the last
line of the `feature.accept` entry (`    ),`) at 4372, the blank at 4373 and the `# ── plan (` banner
at 4374, all confirmed by reading the blob. So the prose names 4346..4373 = 28 lines, plus the
`GroupDef` at 157 = 29 lines, and 4946 - 29 = 4917. Reaching the ordered 4918 would require KEEPING
the blank line at 4373, which leaves TWO consecutive blank lines between the previous entry and the
`# ── plan (` banner and contradicts the prose. I APPLIED THE PROSE — the run and its trailing blank
line are both gone, one blank line separates the preceding entry from the `# ── plan (` banner, and
the surrounding style is preserved — and I report the real 4917 rather than leaving cruft to satisfy a
numeral. The block's own span "lines 4346 to 4372" is correct; only the derived total is off by one.

DEVIATION 2 — `tests/cli/test_progress_feature_runtime.py` ENDS AT 73 LINES, NOT THE ORDERED 81. The
block orders the deletion of "the whole classes `TestFeaturePlanRuntime` and `TestFeatureAcceptRuntime`,
each with the blank lines and any comment banner separating it from what precedes it". `ast` on the
base blob places `TestProgressChecklistRuntime` at 42-73, `TestFeaturePlanRuntime` at 81-118 and
`TestFeatureAcceptRuntime` at 126-160, with the separator before each deleted class being seven lines
(two blanks, a three-line `# ---` banner, two blanks) at 74-80 and 119-125 respectively. The two
classes with their separators are therefore 74..118 (45 lines) and 119..160 (42 lines) = 87 lines, and
160 - 87 = 73. There is no cut that both deletes the two classes with their banners and lands on 81:
81 is the line number of `class TestFeaturePlanRuntime:` itself. I DELETED 74..160, so the file now
ends at the last line of the surviving class, holds exactly one class, and keeps every import it still
uses (`json`, `os`, `subprocess`, `sys` are all still referenced — ruff is clean). The block's 81 is
arithmetic, not a description of a different cut.

DEVIATION 3 — C5 IS -226, NOT THE ORDERED -217, AND THE DIFFERENCE IS EXACTLY DEVIATIONS 1 AND 2.
9 = 1 (the catalog's trailing blank line) + 8 (the eight lines of separator/banner the block's 81 keeps
and its own prose deletes). The INSERTION half of the clause is met exactly: +2, and they are the two
lines the block declares — the registration tuple in `apps/cli/commands/__init__.py` and the
boundary-doc sentence, applied from the block's explicit whole-line FROM/TO pair (`progress_cmd.py`
and `feature_cmd.py` read it for developer convenience display. -> `progress_cmd.py` reads it for
developer convenience display.). Per-file: the deleted handler 101, the runtime tests 87, the catalog
29, `__init__.py` 2, the docs 2, the map 2, and 1 each for `pyproject.toml`, the allowlist and the
boundary test = 226.

DEVIATION 4, DECLARED DOUBT RATHER THAN A CHANGE — TWO PROSE MENTIONS OF THE DELETED COMMANDS SURVIVE
BECAUSE THE BLOCK DOES NOT ORDER THEM CUT, AND NEITHER IS REACHED BY G5(c)'s FIVE STRINGS.
`docs/system/development-artifact-boundary-v0.md` line 60 (post-cut) still reads
"2. Development commands (`feature`, `progress`) may continue reading `.agent/` files", and line 1 of
`tests/cli/test_progress_feature_runtime.py` still reads "Runtime subprocess tests for ``remedy
progress`` and ``remedy feature`` CLI." The block's C5 section says "Nothing else" and its docs step
names ONLY the table row and the one sentence it gives as a FROM/TO pair, so I changed neither. Both
are now stale prose naming a command that no longer exists; a later round or the reviewer should
decide whether they are worth a line.

NOT A DEVIATION, RECORDED BECAUSE THE BLOCK ASKED FOR IT: constraint 9's known flake R-0569 did NOT
appear. The single full-suite run under `-n auto` in the primary checkout was green, so no serial
re-run of `tests/ui_server/test_command_channel.py` was needed and no file was edited. Constraint 7's
missing-UI-build failure class did not arise either: the full suite ran in the PRIMARY checkout, and
the worktrees were used only for the base collect-only reading and for the three map-test runs of G6,
neither of which touches a UI build. THE TWO GIT-ENUMERATING TESTS THE BLOCK WARNS ABOUT WERE NEVER
SEEN RED, because no suite was run between staging and committing C5: `git rm` and `git add -A` were
followed immediately by the commit, and G5 ran only afterwards.

ALSO CONFIRMED RATHER THAN ASSUMED: every line the block's C5 section names was matched against the
base blob by EXACT CONTENT before it was removed, with an assertion per line rather than by line
number alone — the `feature_cmd,` import line, the `feature_cmd, ` token inside the registration tuple,
the `"feature": GroupDef(...)` line, the `# ── feature ─` banner and the `# ── plan (` banner that
bounds the run, the `apps.cli.commands.feature_cmd` lines in `pyproject.toml` and the allowlist, the
`"apps/cli/commands/feature_cmd.py"` line in the boundary test, the boundary-doc table row and
sentence, and both map lines. The two module files the block protects,
`packages/orchestration/feature_planner.py` and `packages/orchestration/progress_ledger.py`, and their
test files, are not in the diff at all.

## Open findings

63 BY DISTINCT ID at `43516dc7`, the number G2(d) MEASURED: 68 distinct registrations against 5
distinct resolutions. Unchanged across this round, because round 11 spends no id — RECORD11 registers
nothing and resolves nothing, and no `Done:` paragraph of the worker's own was written. The next free
id is R-0835. The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than
this feature's, per DECISION F272 D12.

## What this round moved

The `feature` command group is GONE: `remedy feature plan` and `remedy feature accept` no longer
exist, `apps/cli/commands/feature_cmd.py` is the FIRST FILE this feature deletes outright rather than
trimming, and the group's advertisements — catalog `GroupDef`, both `CommandEntry` blocks, the package
import and registration entry, the packaging and allowlist memberships, the boundary-doc row and
sentence, the boundary test entry — died in the SAME commit, as DECISION F272 D13 requires. The
deletion map went from 25 edges to 23, and `feature_planner` and `progress_ledger` reached ZERO
recorded edges, taking the cluster modules with no recorded edge from ten to TWELVE, half of the
twenty-four-module cluster. NO CLUSTER MODULE WAS DELETED; both newly-zero modules survive with their
own tests and die with the cluster. DECISION F274 D6 landed at C3 before a line was cut and rules that
nothing inherits the idea, that the two modules are not deleted here, that the test file keeps its
name, and that this round is NOT a pure deletion.

## Next expected action

The reviewer re-runs G1 through G8 against the committed blobs of `fb0d56c4..43516dc7` and issues the
round 11 verdict, resolving in particular whether the two red clauses of G7(b) and G8 are, as this
handback argues, arithmetic in the block rather than a defect in the cut. The verdict is not booked
into `.agent/live_review.md` by this round; under amend0827 rule 1 the pushed handback is the durable
carrier and the verdict is booked by round 12's first ledger commit.

Round 12, per the plan at `2ec3ed82`, is `worker_recommend`'s three edges in `agent_loop.py`,
`autonomy_loop.py` and `dashboard.py` — LIVE RUNTIME CALLS rather than read-only views that feed the
`token_policy_applied` run-log event and `CycleDecision.selected_worker`, so a DECISION naming what
inherits worker recommendation is authored before the cut and the ruled event vocabulary is part of
the question. Then the two F260 carry-overs, `orchestrator_brain.py`'s four edges, the four
`worker_facade_cmd.py` edges and `worker_registry`'s remaining pair, DECISION F260 D3, the cluster
deletion itself, and last T001 and T002.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a block saved verbatim | done | `51f7c541`, byte-for-byte file copy |
| C0b block mirrored | done | `0c6a0c57`, same digest |
| C1 plan replaced by PLAN11 | done | `2ec3ed82`, byte-equal, 48 lines |
| C2 RECORD11 appended | done | `87e5249d`, books round 10 PASS, registers and resolves nothing |
| C3 DECISION11 appended | done | `5c6a234b`, DECISION F274 D6, before the cut |
| C4 SLIPS11 appended | done | `af99dcf8`, one line |
| C5 the cut | deviated | `43516dc7`, nine paths, +2 as ordered, -226 against the ordered -217; see Deviations 1-3 |
| C6 the handback | done | this file, then pushed |
| G1 transport | done | PASS |
| G2 record append | done | PASS |
| G3 decision append | done | PASS |
| G4 prose state files | done | PASS |
| G5 deletion round measurements | done | PASS on every property; the block's `tests/docs/` numeral 306 is 303 at the base as well |
| G6 edge truth and ratchet | done | PASS, 23 edges, twelve zero-edge modules, red proof and restore both confirmed |
| G7 the cut's shape | deviated | (a) and (c) PASS; (b) red on 2 of 8 line counts, Deviations 1 and 2 |
| G8 the tree | deviated | tree, path set and parents PASS; C5 is +2 as ordered and -226 against -217, Deviation 3 |
| Round 10 verdict booked | done | `87e5249d`, RECORD11 |
| Round 11 verdict | not done — carried | the reviewer issues it; round 12's first ledger commit books it |
| Pull request | not done | none exists and none was ordered; the branch is pushed |
