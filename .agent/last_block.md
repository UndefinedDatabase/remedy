STEP — F274 ROUND 11 — a DELETION ROUND: the `feature` command group dies, and two modules reach zero edges

Goal: delete the `feature` command group entirely — the handler file, its two catalog entries and
their group, its package wiring, its packaging and allowlist memberships, its boundary-doc row and
sentence, its two runtime test classes, and its two lines in the deletion map. That takes the map
from 25 edges to 23, and takes `feature_planner` and `progress_ledger` to ZERO recorded edges, so
the cluster modules with no recorded edge go from ten to TWELVE. Book round 10's PASS
verdict. NO CLUSTER MODULE IS DELETED THIS ROUND — the two modules survive with their own tests and
die with the cluster.

Base commit for every reading in this block: `fb0d56c419f7bc8441f461dac1a6ea1e44a044d7`.

THIS IS A DELETION ROUND under operator amendment amend0906-triage-throughput rule 1, and it is the
first of this feature to delete COMMANDS rather than read-only views. DECISION F272 D13 requires a
command's ADVERTISEMENTS to die in the same commit as the command, and DECISION F272 D14 part 1 rules
that cluster-bound consumers are never migrated. THE CUT IS NOT A PURE DELETION AND THIS BLOCK SAYS
SO IN ADVANCE: two lines are EDITED rather than removed — the registration tuple in
`apps/cli/commands/__init__.py`, where `feature_cmd` is one token in a long line, and the boundary-doc
sentence that named two commands and must now name one. Both are "the test/import edits those
deletions force", which rule 1 permits by name. The commit is +2 insertions against -217 deletions,
and gate G8 orders exactly that rather than zero.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. Marker lines are never written to any file.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r11.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN11 slice.
C2   Append the RECORD11 slice to `.agent/live_review.md` — books round 10's PASS verdict. It
     registers no id and resolves none.
C3   Append the DECISION11 slice to `.agent/decisions.md` — DECISION F274 D6.
C4   Append the SLIPS11 slice to `.agent/prose_slips.md`.
C5   THE CUT, all nine paths in ONE commit, because the catalog entry, its handler and its map line
     must not exist apart for even one commit.
C6   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (docs/agents/planner_reviewer_prompt.md §3 item 23). C3 lands D6 BEFORE
C5 cuts a line, which is the order DECISION F274 D3, D4 and D5 all set.


## Change set — these paths and nothing else

  .agent/authored/f274-r11.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/decisions.md
  .agent/prose_slips.md
  .agent/handoff.md
  apps/cli/commands/feature_cmd.py            (DELETED OUTRIGHT)
  apps/cli/commands/__init__.py
  apps/cli/command_catalog.py
  pyproject.toml
  docs/system/development-artifact-boundary-v0.md
  tests/cli/test_progress_feature_runtime.py
  tests/orchestration/cluster_deletion_map.txt
  tests/orchestration/import_reachability_allowlist.txt
  tests/orchestration/test_development_artifact_boundary.py


## C5 — the cut

USE `git rm` FOR THE DELETED FILE, and stage every other change, so that the commit records the
deletion. This is not housekeeping: two tests enumerate paths FROM GIT rather than from disk, and
both are RED while the deletion is unstaged or staged-but-uncommitted and GREEN once committed. The
reviewer measured that in a worktree and it is why gate G5 runs after the commit rather than beside
it. Do not read either red as a defect if you happen to run the suite mid-flight; report it if you
see it, and re-run after committing.

1. `apps/cli/commands/feature_cmd.py` — DELETE THE FILE. All 101 lines. An `ast` walk shows all
   three of its top-level definitions import a cluster module, so there is no surviving half.

2. `apps/cli/commands/__init__.py` (102 lines at the base) — remove the whole line whose content is
   `feature_cmd,` inside the import block, and remove the token `feature_cmd, ` from the long
   registration tuple. ONE LINE DELETED, ONE LINE EDITED. The file goes to 101 lines.

3. `apps/cli/command_catalog.py` (4946 lines at the base) — remove the `GroupDef` line whose key is
   `"feature"`, and remove the contiguous run that begins at the banner comment `# ── feature ─` and
   ends at the last line of the `feature.accept` `CommandEntry`, together with the blank line that
   follows it and before the `# ── plan (` banner. That run is lines 4346 to 4372 at the base and
   holds the two entries `feature.plan` and `feature.accept`. The file goes to 4918 lines.

4. `pyproject.toml` — delete the single line holding `apps.cli.commands.feature_cmd`. 158 -> 157.

5. `tests/orchestration/import_reachability_allowlist.txt` — delete the single line
   `apps.cli.commands.feature_cmd`. 327 -> 326.

6. `tests/orchestration/test_development_artifact_boundary.py` — delete the single line holding
   `"apps/cli/commands/feature_cmd.py"`. 299 -> 298.

7. `docs/system/development-artifact-boundary-v0.md` (86 lines at the base) — delete the table row
   beginning `| Feature command display |`, and REWRITE one whole line in place. It is the only line
   of the file that mentions the deleted handler in prose. Its exact content at the base is the FROM
   line below, and it becomes the TO line below; both are given whole so no substring has to be
   guessed, and the backticks shown are literal bytes of the file. This is a REWRITE, not an append:
   the TO does not contain the FROM.

     FROM: `progress_cmd.py` and `feature_cmd.py` read it for developer convenience display.
     TO:   `progress_cmd.py` reads it for developer convenience display.

   That is the second of the two edited lines the header of this block declares. The file goes to 85
   lines.

8. `tests/cli/test_progress_feature_runtime.py` (160 lines at the base) — delete the whole classes
   `TestFeaturePlanRuntime` and `TestFeatureAcceptRuntime`, each with the blank lines and any comment
   banner separating it from what precedes it. `TestProgressChecklistRuntime` SURVIVES and is the
   only class left. The file goes to 81 lines. Do not rename the file; DECISION F274 D6 states why.

9. `tests/orchestration/cluster_deletion_map.txt` (40 lines at the base) — delete the two lines whose
   consumer is `apps/cli/commands/feature_cmd.py`:

     packages.orchestration.feature_planner <- apps/cli/commands/feature_cmd.py
     packages.orchestration.progress_ledger <- apps/cli/commands/feature_cmd.py

   The file goes to 38 lines, 23 edges.

Nothing else. In particular `packages/orchestration/feature_planner.py`,
`packages/orchestration/progress_ledger.py` and their own test files SURVIVE UNTOUCHED — an edge cut
is not a module deletion, and those modules die with the cluster.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks wrong,
   apply it as given and DECLARE the doubt in the handback.
2. RECORD11, DECISION11 and SLIPS11 are APPENDS: the target's existing bytes are a byte-exact PREFIX
   of the result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own. PLAN11 replaces `.agent/plan.md` entirely.
3. The path set of C0a through C5 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C6 writes.
4. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary. Remove and prune each
   worktree you create.
5. Do not write a `Done:` paragraph of your own. RECORD11 resolves nothing and registers nothing.
6. Every gate below runs at a commit STRICTLY EARLIER than C6, so the handback can quote each.
7. RUN THE FULL SUITE IN THE PRIMARY CHECKOUT, never in a fresh worktree: `apps/ui/node_modules` and
   `apps/ui/dist` are gitignored, so a fresh worktree has neither and both the vitest foundation test
   and the npm-backed tests then fail on the missing build rather than on anything this round did.
8. READING A COMMITTED BLOB, since several gates below measure one. Use `git show <commit>:<path>`
   into memory or into a scratch file under the gitignored `.remedy-wt/`, or read it in a disposable
   worktree. NEVER write a blob over the tracked file and restore it afterwards: that mutates the
   primary checkout, which constraint 4 and docs/agents/self_drive_protocol.md guardrail G5 forbid.
9. THE KNOWN FLAKE, stated so you do not repair it. Finding R-0569 is OPEN and names the fixed port
   5273 under xdist, pinned at `tests/orchestration/test_product_smoke.py` line 90. If a server-backed
   file such as `tests/ui_server/test_command_channel.py` fails under `-n auto`, RE-RUN THAT FILE
   SERIALLY and report both results. Do NOT edit any file to make such a red go away; report it.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r11.md` equals `sha256` of the
    committed `.agent/last_block.md`, and both equal the digest the delegation message states. Report
    the digest you measured.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 574989 -> 579917; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the 4928-byte RECORD11 slice with no separator added. THESE ARE THE TWO
        READINGS gate (c) calls the BYTE reader: the prefix comparison alone cannot see a flip inside
        the appended region, so it is the `post == pre + slice` clause that carries that half.
    (b) STRUCTURE, over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice itself; the file's last N units equal the slice's units IN ORDER
        and everything before them is unchanged. Units 228 -> 229.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED BYTE offset 574990 of the post-image — read as
        bytes, not characters; it is the `G` opening the FIRST appended paragraph — and confirm that
        the BYTE reader of (a) and the STRUCTURAL reader of (b) each reject it.
    (d) COUNTS: registrations 68 -> 68, resolutions 5 -> 5, OPEN SET 63 -> 63 BY DISTINCT ID (distinct
        `^- R-\d+ — ` ids minus distinct `^Done: R-\d+ — ` ids), `^Gate: ` 41 -> 42,
        `^Gate: F274 R10` 0 -> 1, `^Landed: ` UNCHANGED at 37 lines. This round spends NO id.

G3  THE DECISION APPEND, at C3, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/decisions.md` 899779 -> 905078; prefix true; post equal to pre plus the
        5299-byte DECISION11 slice.
    (b) STRUCTURE over the whole appended region, N counted from the slice: units 1977 -> 1986, last N
        units equal the slice's units IN ORDER, everything before unchanged.
    (c) NEGATIVE CONTROL at zero-indexed byte offset 899780 — the `#` opening the FIRST appended
        paragraph — rejected by the byte reader and by the structural reader.
    (d) `^## DECISION F274 D6` occurs exactly ONCE in the post-image and ZERO times in the pre-image.

G4  THE PROSE STATE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN11 slice, is 48 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md` at
    C4 goes 161811 -> 162264 with the pre-image a byte-exact prefix and the appended line once.

G5  THE DELETION ROUND'S FOUR MEASUREMENTS, at C5, all of them AFTER the commit.
    (a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` EXIT 0, and
        `python3 -B -m pytest tests/docs/ -q` EXIT 0 — this round edits a file under `docs/`. The
        reviewer measured 3 passed and 306 passed.
    (b) THE FULL SUITE green, in the PRIMARY CHECKOUT per constraint 7: `python3 -m pytest -q -n auto`.
        Report the exit code and the passed/failed/skipped counts. The reviewer measured 19765 passed,
        23 skipped, 0 failed with this cut applied, against 19781 at the base.
        AND THE DELTA IS ORDERED AS A SET, NOT AS A COUNT: collect with
        `python3 -B -m pytest --collect-only -q` at the base and at C5, and report that EXACTLY 16 node
        ids disappear and ZERO appear. The sixteen are the eight tests of `TestFeaturePlanRuntime` and
        `TestFeatureAcceptRuntime`, and eight `[feature]` parametrizations in `tests/test_grouped_cli.py`,
        which parametrize over catalog GROUPS and lose the group this round deletes. Collected totals
        19804 -> 19788.
    (c) A grep over every tracked file under `packages/`, `apps/`, `tests/`, `scripts/` and `docs/`,
        ALL FILE TYPES AND NO FILTER. The strings `feature_cmd`, `_cmd_feature_plan`,
        `_cmd_feature_accept`, `feature.plan` and `feature.accept` TOTAL ZERO. Report the total. THE
        SCOPE IS DELIBERATE AND THE REVIEWER MEASURED WHY: `.agent/` is excluded because THIS BLOCK
        NAMES ALL FIVE STRINGS and C0a and C0b commit this block there, and `.data/` is excluded
        because it holds evidence exports of past runs, which are historical artefacts this feature
        does not rewrite. `docs/` IS INCLUDED here, unlike in rounds 9 and 10, because this round
        edits the one doc that named the command.
    (d) `python3 -m ruff check` EXIT 0 over the four surviving touched `.py` paths —
        `apps/cli/commands/__init__.py`, `apps/cli/command_catalog.py`,
        `tests/cli/test_progress_feature_runtime.py` and
        `tests/orchestration/test_development_artifact_boundary.py`. AND the frozen ceiling:
        `ruff check .` REPORTS 26 ERRORS, unchanged, so DECISION F083 D5 is untouched — that command
        EXITS 1 while reporting them, which is the gate passing, because the ceiling is 26 rather
        than 0.

G6  THE EDGE TRUTH AND THE RATCHET, at C5, in a disposable worktree. Purge `__pycache__` there before
    the first run and use `python3 -B` for every run.
    (a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0.
    (b) Measured edges equal recorded edges at 23, with APPEARED and DISAPPEARED both empty. The
        cluster modules with NO measured edge are exactly these TWELVE: `candidate_quality`,
        `context_optimizer`, `context_pack`, `external_builder_sandbox`, `feature_planner`,
        `local_candidate_generator`, `model_route_tournament`, `overnight_mission`, `progress_ledger`,
        `repair_loop_v2`, `review_bundle` and `self_repair_proposal`. The non-`.py` consumers are THE
        EMPTY LIST. Report all three readings.
    (c) RED: append the line `packages.orchestration.feature_planner <- apps/cli/commands/
        feature_cmd.py` back to `tests/orchestration/cluster_deletion_map.txt`, as ONE line with no
        internal break. Count that exact byte string in that file first: it must be ZERO after C5. The
        command of (a) must then be EXIT 1 reporting `DISAPPEARED (1)` and naming that exact edge.
        Restore BY EXACT PATH, confirm byte-identity against the committed blob, and confirm the
        control of (a) returns to EXIT 0.

G7  THE CUT'S SHAPE, at C5, measured against the COMMITTED blobs.
    (a) `apps/cli/commands/feature_cmd.py` is ABSENT from `git ls-tree` at C5 and PRESENT at the base.
    (b) LINE ARITHMETIC, one reading per surviving file: `apps/cli/commands/__init__.py` 102 -> 101;
        `apps/cli/command_catalog.py` 4946 -> 4918; `pyproject.toml` 158 -> 157;
        `tests/orchestration/import_reachability_allowlist.txt` 327 -> 326;
        `tests/orchestration/test_development_artifact_boundary.py` 299 -> 298;
        `docs/system/development-artifact-boundary-v0.md` 86 -> 85;
        `tests/cli/test_progress_feature_runtime.py` 160 -> 81;
        `tests/orchestration/cluster_deletion_map.txt` 40 -> 38.
    (c) PARSE AND STRUCTURE, with `ast` rather than grep: every touched `.py` file parses;
        `tests/cli/test_progress_feature_runtime.py` holds EXACTLY ONE class,
        `TestProgressChecklistRuntime`; and the catalog at C5 holds no command whose `group_id` is
        `feature` and no `GroupDef` keyed `feature`.

G8  THE TREE, at C5. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY; `git worktree
    list` the same count as before your first worktree and after your last prune; `git diff
    --name-only fb0d56c419f7bc8441f461dac1a6ea1e44a044d7..<C5>` naming exactly the paths of
    constraint 3 and nothing else; every commit C0a through C5 single-parent. Report the INSERTION
    and DELETION counts of each commit C0a through C5 — per AGENTS.md DECISION F104 D1 the 500-line
    cap counts insertions only — and confirm that C5 is +2 and -217, the two insertions being the
    edited registration tuple and the narrowed boundary-doc sentence this block declares in its
    header. Do not report C6's own numbers; the reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C6, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits table
with its `+/-` column taken from `git diff --numstat` and compared cell by cell against the counts G8
reports, the changed-files table, ONE LINE PER GATE G1 through G8 with its real result, the
deviations, the open-findings count, and the next expected action. No length cap. Name the SESSION
NUMBER as SESSION 5 of feature F274 and the round as 11. State the open-findings count as the number
G2(d) MEASURED. Add the one sentence of context self-assessment amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any slice does not apply as described,
report the real command, the real exit code and the real output and say what you did.


BEGIN PLAN11 sha256=106a18864711787f43c19cd99f5313ef34a7453ec43d6c6556b77147b85d9ae3 bytes=2985
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 11, a DELETION ROUND under operator amendment amend0906-triage-throughput and the first that
deletes COMMANDS rather than read-only views: delete the `feature` command group entirely — the
handler file `apps/cli/commands/feature_cmd.py`, its two catalog entries and their group, its
package wiring, its packaging and allowlist memberships, its boundary-doc row, its two runtime test
classes and its two deletion-map lines. `feature_planner` and `progress_ledger` both reach ZERO
recorded edges. DECISION F274 D6 rules the deletion before a line is cut. Book round 10's PASS
verdict. No cluster module is deleted this round.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views: the reviewer measured that they feed
   the `token_policy_applied` run-log event and `CycleDecision.selected_worker`, and that
   `selected_worker` is named in `packages/orchestration/event_schemas.py`, so a DECISION naming
   what inherits worker recommendation is authored before the cut and the ruled event vocabulary
   is part of the question.
2. The two carry-overs F260's Design names, each freeing a cockpit section held back so far:
   overnight readiness to `mission readiness`, and the route-policy knobs checked against F110's
   config keys. `mission report` waits for the commit that deletes its current holder, per
   DECISION F274 D2, and that holder is in `worker_facade_cmd.py`.
3. `orchestrator_brain.py`'s four edges, which the reviewer measured as live signal reads in
   `_scrub`, `_review_state`, `_gather_signals` and `consult_local_advisor_for_decision` — a
   surviving module reading cluster modules, so a behaviour change rather than a deletion.
4. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is now fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN11


BEGIN RECORD11 sha256=12b28768abafce8e529fb86dd8d556795dda3e2adfe4bf9816f2396fc1d44839 bytes=4928

Gate: F274 R10 — the F274 round 10 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in a disposable worktree, against the COMMITTED blobs rather than the working tree. Range `3bcaa45c85c779dece35a02d369cc333416a0963`..`fb0d56c4`, eight commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the path set over the range to C5 naming exactly the twelve declared paths and nothing else. G1 TRANSPORT COVERS THE EMITTED BYTES rather than only the worker's self-consistency, because the block travelled as a FILE the worker copied rather than as text it retyped: the reviewer's scratch original `.remedy-wt/f274-r10-FINAL.md`, written and hashed BEFORE delegation, is BYTE-IDENTICAL to both committed copies, all three 33364 bytes at `13573077f22c9c70cede71252067536036538a650c4c53be17178164dadf8994`. G2 THE RECORD APPEND at `2ab5bb20`: 569829 to 574989 bytes, pre-image a byte-exact PREFIX, post-image equal to pre plus the 5160-byte RECORD10 slice, N counted from the slice as 1, units 227 to 228, ordered equality true with everything before unchanged, and the control flipped at zero-indexed byte offset 569830 rejected by both the byte reader and the structural reader; registrations 68 to 68, resolutions 5 to 5, OPEN SET 63 TO 63 BY DISTINCT ID, `^Gate: ` 40 to 41, `^Gate: F274 R9` 0 to 1, `^Landed: ` unchanged at 37 lines. G3 THE DECISION APPEND at `de3cbcb8`: 894911 to 899779 bytes against the 4868-byte DECISION10 slice, N counted as 9, units 1968 to 1977, ordered equality true, the control at byte offset 894912 rejected by both readers, and `^## DECISION F274 D5` exactly once in the post-image against zero in the pre-image. G4: `.agent/plan.md` byte-equal to its slice at 47 lines against the cap of 50 with both mandated headings; `.agent/prose_slips.md` 161300 to 161811 bytes with the appended line occurring once. G5 THE DELETION ROUND'S FOUR MEASUREMENTS: import reachability EXIT 0 at 3 passed; THE FULL SUITE GREEN IN THE REVIEWER'S OWN RUN IN THE PRIMARY CHECKOUT at 19781 passed, 23 skipped, 0 failed, against 19785 at the base — a difference of exactly the four deleted cockpit presence tests; the six deleted builder symbols TOTAL ZERO over the 1313 tracked files of `packages/`, `apps/`, `tests/` and `scripts/` with NO file-type filter, against 18 at the base; `ruff check` EXIT 0 over the five touched `.py` paths and the frozen ceiling of DECISION F083 D5 unchanged at 26 errors. G6 THE EDGE TRUTH AND THE RATCHET, in the reviewer's own disposable worktree at `60827166`: control EXIT 0 at 3 passed, measured equals recorded at 25 with APPEARED and DISAPPEARED both empty, THE ZERO-EDGE SET UNMOVED at exactly the ten modules round 9 left — which is what this round was designed to do rather than a shortfall in it — the non-`.py` consumers THE EMPTY LIST, and the modules still holding an edge into `ui_server.py` exactly `builder_routing`, `overnight_readiness` and `worker_registry`. THE RED PROOF BIT: the line `packages.orchestration.main_builder_adapter <- packages/orchestration/ui_server.py` occurs ZERO times in the map after C5, and appending it back gives EXIT 1 reporting `DISAPPEARED (1)` and naming that exact edge, after which a restore by exact path returns the file to `a43ec9d3f4d4ed57abc562b39dfda599ab655fcac00054713193cfebec8ab446` and the control to EXIT 0. G7 THE CUT'S SHAPE, from the committed blobs: `ui_server.py` 4065 to 3841, the map 46 to 40, `test_dashboard_cockpit_truth.py` 416 to 365, `test_provider_trust.py` 389 to 387, `test_provider_patch_material.py` 301 to 299 and `test_overnight_executor.py` 429 to 427, every one as ordered; all five files parse under `ast`; the six deleted symbols are absent from the top-level definitions of `ui_server.py` while all five named survivors are present; THE THREE REDACTION GUARDS SURVIVE WITH THEIR ASSERTIONS INTACT — 69, 49 and 81 `assert` statements respectively and ZERO remaining references to either deleted builder — so each lost one surface and nothing else, which is the property this round most needed to be true. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 before and after, per-commit insertions 404, 230, 14, 2, 61, 2 and ZERO for C0a through C5 — C5 is 287 deletions against 0 insertions across six files, a PURE DELETION as a deletion round requires. ONE CLARIFICATION WAS DECLARED AND THE REVIEWER SUSTAINS IT AS A CLARIFICATION RATHER THAN A DEFECT, and it is the same one round 9 produced: a flip inside the appended region is invisible to a bare PREFIX comparison by construction, so the byte reader is the `post == pre + slice` clause rather than the prefix clause beside it. The round 10 block had already been reworded to say exactly that, and the worker read it correctly and said so. NO FINDING IS REGISTERED OR RESOLVED BY THIS GATE AND NO NEW ID IS MINTED.
END RECORD11


BEGIN SLIPS11 sha256=9ea22e6f04c60bcc4fed7c0517382240a4da4db12dc50f0eb7f3820d097f2394 bytes=453

2026-09-08 · F274 R10 · The round 10 dry run measured 19 full-suite failures in a fresh worktree and only 7 of them belonged to the cut; the other 12 were the R-0569 fixed-port flake and the missing `apps/ui/node_modules`, and every one passed when re-run serially — recorded because the reviewer nearly read a worktree's environment as a property of the change, which is the same misreading round 6 of this feature made in the opposite direction.
END SLIPS11


BEGIN DECISION11 sha256=7f898f1f84413b42adffcf1b2e5f3b43ab1539cae3bd88d38f3644dabc67d6dc bytes=5299

## DECISION F274 D6 — the `feature` command group is DELETED with its module edges, and nothing inherits it (2026-09-08)

Date: 2026-09-08. Feature F274, round 11. Status: decided by the reviewer under
docs/agents/planner_reviewer_prompt.md §4 item 7; the operator's veto is any later session.

CONTEXT, MEASURED AT `fb0d56c4`. `apps/cli/commands/feature_cmd.py` is the last consumer of TWO
prototype-cluster modules, `packages.orchestration.feature_planner` and
`packages.orchestration.progress_ledger`, and it is WHOLLY cluster-bound: an `ast` walk shows all
three of its top-level definitions — `_build_ledger_and_plan`, `_cmd_feature_plan` and
`_cmd_feature_accept` — import one or both. There is no surviving half to keep, so the file dies
rather than being trimmed. DECISION F272 D14 part 1 already rules that the cluster-bound consumers
are never migrated, and DECISION F272 D13 that a command's ADVERTISEMENTS die in the same commit as
the command.

CHOSEN. The whole `feature` group goes in one commit: the handler file, the catalog `GroupDef`
`"feature"` and both `CommandEntry` blocks (`feature.plan` and `feature.accept`), the import and the
registration-tuple entry in `apps/cli/commands/__init__.py`, the `apps.cli.commands.feature_cmd`
memberships in `pyproject.toml` and
`tests/orchestration/import_reachability_allowlist.txt`, the row and the sentence naming it in
`docs/system/development-artifact-boundary-v0.md`, its entry in
`tests/orchestration/test_development_artifact_boundary.py`, the two runtime test classes
`TestFeaturePlanRuntime` and `TestFeatureAcceptRuntime`, and the two deletion-map lines. NOTHING
INHERITS THE IDEA. `remedy feature plan` printed deterministic feature suggestions and
`remedy feature accept` turned one into a ProposedTask; both read `.agent/live_review.md` for
developer convenience, both are classified as DEVELOPMENT rather than product commands by
`docs/system/development-artifact-boundary-v0.md`, and the roadmap they served is now kept in
`docs/roadmap/STATUS.md` and driven by the planner/reviewer loop rather than by a CLI suggestion
engine. AGENTS.md's Scope Control requires this to be said out loud rather than left implicit.

WHAT IS DELIBERATELY NOT DONE, so a later reader does not read it as an omission. The modules
`feature_planner.py` and `progress_ledger.py` SURVIVE this round with their own tests
(`test_feature_planner.py` and the progress-ledger suites) and die with the cluster, which is the
same separation every round of this feature has kept: an edge cut is not a module deletion.
`tests/cli/test_progress_feature_runtime.py` keeps its name although it now covers only
`TestProgressChecklistRuntime`, because renaming it would break `git log --follow` on a file this
round already touches and buys nothing that the surviving class name does not already say; F261 owns
renames.

THIS ROUND IS NOT A PURE DELETION AND SAYS SO. amend0906-triage-throughput rule 1 permits "the
test/import edits those deletions force", and two lines are EDITED rather than removed: the
registration tuple in `apps/cli/commands/__init__.py`, where `feature_cmd` is one token in a long
line, and the sentence in the boundary doc that named two commands and now names one. The commit is
+2 insertions against -217 deletions. Rounds 9 and 10 happened to reach +0; this one cannot, and the
difference is declared rather than discovered at review.

EVIDENCE THIS RESTS ON, all of it measured by the reviewer in a disposable worktree with the cut
applied and COMMITTED, before this decision was written. THE COMMIT MATTERS TO THE MEASUREMENT: two
tests enumerate paths from git rather than from disk —
`tests/cli/test_advertised_commands.py::test_every_advertised_command_exists_in_the_catalog` and
`tests/orchestration/test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`
— so both are RED while the deletion sits unstaged or staged-but-uncommitted, and both are GREEN once
it is committed. That is an artefact of measuring mid-flight, not a property of the change, and it is
recorded here because the next reader to delete a tracked file will see the same two reds. The
collected-test set goes from 19804 to 19788 and the reviewer diffed the node-id SETS rather than the
counts: exactly 16 ids disappear and NONE appears — the eight tests of the two deleted runtime
classes, and eight `[feature]` parametrizations in `tests/test_grouped_cli.py`, which parametrize over
catalog GROUPS and lose the group this round deletes. The full suite is 19765 passed, 23 skipped, 0
failed. `ruff check .` is 26 errors before and after, so DECISION F083 D5's frozen ceiling is
untouched, and `tests/docs/` is green at 306 passed.

CONSEQUENCE. The map goes from 25 edges to 23, and the cluster modules with NO recorded edge go from
ten to TWELVE — `feature_planner` and `progress_ledger` join the set — which is half the
twenty-four-module cluster. `apps/cli/commands/feature_cmd.py` is the first FILE this feature deletes
outright rather than trimming.

REVERSE THIS DECISION by restoring `apps/cli/commands/feature_cmd.py`, its catalog group and two
entries, its wiring, packaging, allowlist and boundary-doc rows, its two runtime test classes and its
two map lines from git history at `fb0d56c4`.
END DECISION11
