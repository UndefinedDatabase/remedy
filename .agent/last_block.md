── STEP T003 — F275 — ROUND 102 ──
Goal: The first BRIDGE round. Book round 101's verdict; let `ruff`'s own fixer take the import
rows the flip added; repair eleven guard and pin nodes the transform renamed without reading;
run the full suite once and show its bad-node set strictly shrinking with no node newly bad.

Base commit: `7f2991c9`. Round type: SPLIT. Operator amendment amend0914-f275-sprint in
`docs/agents/self_drive_protocol.md` governs this round; read that paragraph first. The
production edits are import order and unused imports made by `ruff --fix`, so no mutation
probe is ordered.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0 `.agent/authored/f275-r102.md` and `.agent/last_block.md`, both the block as received
C1 THE BOOKKEEPING COMMIT: `.agent/plan.md` gets slice PLAN102 as a full replacement;
   `.agent/live_review.md` gets slice RECORD102 appended; `.agent/prose_slips.md` gets slice
   SLIP102 appended; `.agent/decisions.md` gets slice DEC102 appended
C2 SPEC L, the import rows
C3 SPEC E, the eleven nodes
C4 `.agent/authored/f275-r102-suite.txt`, per SPEC S
C5 `.agent/handoff.md`, the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's `.agent/` paths; at C2 the paths SPEC L's fixer changes; at C3 the paths SPEC E
names.

## SPEC L — at C2

From the primary checkout's root: `ruff check --fix --select I001,F401` followed by exactly the
paths `git diff --name-only b184040c ebc0182c` prints. No other edit. One commit.

## SPEC E — at C3

Slice EDITS102 is a JSON object: each key a path, each value a list of `[old, new]` pairs. Load
the slice's bytes with `json.loads`. For each path in the object's order, and each pair in list
order, `old` must occur EXACTLY ONCE in the file as it stands after C2 and the pairs before it;
then it is replaced by `new`. A count other than one is a STOP: restore the path with `git
checkout -- <path>`, commit nothing further and write only the handback. No other edit.

## SPEC S — the suite, once, after C3 and before C4

The round's FIRST AND ONLY full-suite run, from the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with
`PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`,
stdout and stderr saved under `.remedy-wt/r102w/`. A bad node is the text after a line-initial
`FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The transcript file holds: line 1
`EXIT=<pytest's return code>`; line 2 the run's last output line with its leading and trailing
`=` and spaces stripped; then every distinct bad node, sorted, one per line; nothing after the
last line's newline.

## Constraints

1. NO SLICE IS EDITED. PLAN102, RECORD102, SLIP102, DEC102 and EDITS102 are used byte for byte;
   a discrepancy inside one is DECLARED, never repaired.
2. READ `.agent/STOP` before C0, before C2 and before C5, with real exit codes. If it appears,
   finish the commit in hand, write the handback and end.
3. No `.py` file under `.agent/`; scratch under `.remedy-wt/r102w/`, uncommitted, every scratch
   output path absolute. The reviewer's `.remedy-wt/r101/` is not opened.
4. The appends at C1 have a ZERO deletion column. Every commit stays under 500 insertions.
5. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Push after C1, C3, C4 and C5. No worktree is created.
6. THE BLOCK'S OWN SIZE, measured on its final bytes: 283 lines TOTAL and 160 lines of
   PROSE, against the caps of 490 and 400.
7. GATE ORDER. G1 runs at C1. G2 runs after C3. G3 runs after G2 and before the suite. G4 runs
   after the suite and before C4, with its committed-transcript reading at C4. G5 and G6 run
   after C4 and before C5. No gate runs after C5; C5's own numbers are the reviewer's.
8. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT AND BOOKKEEPING, at C1. The sha256 of `.agent/authored/f275-r102.md` at C0 equals
the digest received with the block, and `.agent/last_block.md` at C0 is byte-identical to it.
Extract the slices by their markers, report how many were FOUND, and check each against its
BEGIN-marker sha256. `.agent/plan.md` at C1 is byte-identical to PLAN102, with at most 50 lines,
one `## Goal` and one `## Next Steps`. For each append, the blob `git show 7f2991c9:<path>`
followed by the slice equals the file at C1: 1168612 bytes for `.agent/live_review.md`, 305304
for `.agent/prose_slips.md` and 1318510 for `.agent/decisions.md`. Lines matching
`^Gate: F\d+ R\d+ — ` read 123 at `7f2991c9` and 124 at C1, with `Gate: F275 R101 — ` once. The
open set BY DISTINCT ID, the ids of `^- R-\d{4} — ` paragraphs minus the ids of `^Done: R-\d{4}`
lines, reads 89 at `7f2991c9` and at C1 with identical membership.

G2 THE CODE, after C3. At C2: the fixer's own summary line, which the reviewer read as
`Found 354 errors (354 fixed, 0 remaining).`; `git show --numstat` of C2 lists only paths the
flip changed, and the reviewer read 184 paths, 355 insertions and 527 deletions. At C3: every
pair's count, each 1. Then `git rev-parse C3:packages`, `C3:apps` and `C3:tests` read the
reviewer's dry-run trees d3a40d00c8222f687bb9f7136f18592ed20288e2,
625e9faa3c5ef8f34f7e6b11a45ba05360191ec2 and 50b1076580d05561527332c701393243b3b2c274.
`ruff check . --output-format concise` rows as a MULTISET with line and column dropped, at
`5ce0c5a2` from a `git archive` tree under `.remedy-wt/r102w/` and at C3 in the primary
checkout: the reviewer read 26 and 11, with no row at C3 absent at `5ce0c5a2`.

G3 THE TARGETED FILES, before the suite. `python3 -B -m pytest -q -p no:randomly -p
no:cacheprovider` with SPEC S's environment over `tests/test_data_paths.py`,
`tests/orchestration/test_job_digest.py`, `tests/orchestration/test_uuid_record_ratchet.py`,
`tests/test_model_construction_keywords.py`, `tests/ui_server/test_command_channel.py` and
`tests/orchestration/test_ci_budgets.py`: exit 0 with no failure and no error. The reviewer's
worktree read 250 passed.

G4 THE BRIDGE, per SPEC S. BASE is the set of bad nodes in `.agent/authored/f275-r101-suite.txt`
at `7f2991c9`. Report pytest's real exit code, the summary line, the count of distinct bad
nodes, FIXED (in BASE and not bad now) and NEWLY BAD (bad now and not in BASE), each by node id.
Each NEWLY BAD node is re-run by its node id ALONE three times with SPEC S's environment, and
reported FLAKY with the three tallies only if all three pass; the reviewer saw
`tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_job_id_is_checked_after_the_credentials`
fail once under the full suite and pass ten times alone. NEWLY BAD less FLAKY: MUST be empty.
FIXED MUST hold these nodes: `tests/orchestration/test_ci_budgets.py::test_this_repository_really_is_at_or_below_the_lint_ceiling`;
`tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_imports_exactly_the_allowed_set`;
in `tests/test_data_paths.py::TestRoutedHandler`, `test_a_routed_handler_accepts_a_short_classic_prefix`,
`test_attaching_by_short_prefix_stores_the_full_job_id` and
`test_stopping_by_an_unhyphenated_id_files_the_stop_under_the_canonical_id`; in
`tests/orchestration/test_job_digest.py`, `test_the_normalized_envelope_equals_its_stored_golden`
with each of `[blocked_with_decisions]`, `[budget_stopped]`, `[green]` and `[mid_run]`;
`tests/orchestration/test_uuid_record_ratchet.py::TestNoRecordOutsideTheClassicPairDeclaresAUuidId::test_the_matcher_can_see_a_uuid_field_at_all`;
and `tests/test_model_construction_keywords.py::TestEveryConstructionKeywordIsADeclaredField::test_an_undeclared_keyword_really_is_dropped_rather_than_rejected`.
At C4 the committed transcript equals the file rebuilt from the saved stdout, and before C4
`git status --porcelain` listed only that file.

G5 TREE, CANARY, PATH SET, OPEN SET, after C4. `git status --porcelain` prints `''` and
`git worktree list` one row. The canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`:
exit code and tally REPORTED. The changed-path set of `7f2991c9`..C4 against the union of the
Bundle's `.agent/` paths other than `.agent/handoff.md`, C2's paths and C3's paths: MISSING and
EXTRA by name. The open set at C4 equals C1's.

G6 THE INSERTION CAP over `7f2991c9`..C4: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 35 of feature F275 · round 102 · rounds so far 102`; the Commits table read from
`git show --numstat` and compared cell by cell against G6, C5's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; one sentence of context self-assessment;
`## Next` stating `Operator questions open: 1`. NO SCOPE REPORT AND NO SESSION-LIMIT BANNER,
by amendment amend0911-f275-to-scope.

── SLICE PLAN102 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN102 sha256=b84b5c90f0e43c4d244ba2fc5f81d561192e14349de3e8493e4baf930ab801f6
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, the classic runner's whole
command surface is gone as of round 34, and the record flip landed in round 101.

## Current Step

ROUND 102 IS THE FIRST BRIDGE ROUND, per operator amendment amend0914-f275-sprint rule 3. It
removes the lint rows and the guard and pin failures the flip left: `ruff`'s own fixer sorts
the import blocks and drops the unused imports in the files the flip changed, the three
routed-handler tests of `tests/test_data_paths.py` build a unified record with a classic-shaped
id, the job digest's golden normalizer reads the unified record's id, two guard tests about
the classic pydantic models import those models again, and the command door's import guard
rules `save_job_plan` where it ruled `save_job`. The full suite runs once and its bad-node set
must be a strict subset of round 101's committed transcript.

## Next Steps

1. MORE BRIDGE ROUNDS on the real tree, each strictly shrinking the committed bad-node set with
   no node newly bad: production code that hands a `JobPlan` a `JobBudgets` model where the
   record holds its serialized dict, and the `job resume` tests of `tests/cli/test_plan_approval.py`;
   what is left of the classic runner under `job resume`, whose kill-and-resume fixture still
   builds a classic job; the scoped job listings; and the single failures left in the job
   context command, the golden path, the runtime smokes, the repair loop, the proposed-task
   store, the cockpit adapter and the task runner — until a round's transcript reads exit 0.
2. THE CLASSIC STORE, with the which-store branches and adapters the flip leaves unreached.
3. THE CLOSURE SEQUENCE.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE BRANCH IS RED until a bridge round's transcript reads exit 0, and hosted CI on the branch
  is expected to be red in that span, per amend0914 rule 3.
- THE BRIDGE IS BOUNDED at eight rounds after the flip commit: a ninth writes an operator
  question and stops, and a round that adds a bad node is FAIL.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 89 by distinct id, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open.
  Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN102

── SLICE RECORD102 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD102 sha256=5d9cc617b65dedd3cf21afbc0c09150eb1cd48979fbbbf0ee39ab57b1850b08a

Gate: F275 R101 — the F275 round 101 entry. VERDICT PASS. Written by the planner and reviewer of session 35 after reading the committed range `5ce0c5a2`..`7f2991c9` and re-deriving every reading that bears on a product path; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 102 that writes the record, per operator amendment amend0827-process-diet rule 1. THE FLIP LANDED as `ebc0182c`, 293 paths, 5839 insertions and 5584 deletions, declared oversize under operator amendment amend0914-f275-sprint rule 1.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r101.md` and `.agent/last_block.md` equal the reviewer's original at 26772 bytes from `475a36a2` through `7f2991c9`; `.agent/plan.md` equals PLAN101 and `.agent/operator_questions.md` equals OPQ101 at `7f2991c9`. Both appends at `b184040c` are exact: 1163586 bytes followed by RECORD101 in the review record, and 1315515 followed by DEC101 in the decisions. The ledger's `Gate: F<n> R<n> — ` heads read 122 at `5ce0c5a2` and 123 at `b184040c`, and the open set went from 88 to 89 with `R-0884` the only id added, `R-0809`, `R-0880` and `R-0883` open.

THE FLIP IS THE TREE THE REVIEWER BUILT. Before authoring, the reviewer transformed its own worktree at `844a7f21` from its own generator output and applied the committed carriers of rounds 90 to 100; the `packages`, `apps` and `tests` trees of `ebc0182c` are identical to that tree's, `87f97702`, `38d2d958` and `ccc08005`, and `docs`, `scripts` and `.agent` do not change in that commit. Every other commit of the range touches `.agent/` alone, and `ebc0182c` is the only one at 500 insertions or more. The reviewer's own thin-site check at `5ce0c5a2` read all eleven sites of DECISION F275 D48 reached by their named witnesses, and 2 of 11 with each site given the next site's witness.

THE SUITE. The committed transcript `.agent/authored/f275-r101-suite.txt` reads exit 1 with 33 failed, 18408 passed, 23 skipped and 7 errors, and lists 40 distinct bad nodes, sorted. The reviewer's own full run in the primary checkout at `7f2991c9`, the first of the three that amendment amend0914 rule 4 grants the reviewer, read 34 failed, 18407 passed, 23 skipped and 7 errors, 41 bad nodes: the transcript's 40, and `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_job_id_is_checked_after_the_credentials`, whose failure is a `JSONDecodeError` on the test server's info file read before the server wrote it, and which passed in ten of ten runs alone. No node is bad in the transcript and good in the reviewer's run. All 40 are among the 53 bad nodes of the reviewer's fresh round 100 worktree run. The reviewer's dry-run tree, identical in `packages`, `apps` and `tests`, read `ruff check .` at 366 rows against 26 at `5ce0c5a2`: added `I001` 320, `F401` 18 and `F821` 3, which the bridge owes.

ONE WORDING DEFECT OF THE BLOCK, declared by the worker. G3 ordered the staged numstat against `5ce0c5a2`, which also counts the five `.agent/` paths C0 and C1 had already committed; the worker reported both readings, and the ordered figures of 293 paths, 5839 insertions and 5584 deletions are the reading against `b184040c`. It is booked as one line in `.agent/prose_slips.md` by the commit that books this entry.
END RECORD102

── SLICE SLIP102 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP102 sha256=be33cf0f09cc92c8abe625aa649c4ce689eef188dc65ca81b4ff5a15c0da36f0

2026-09-14 · F275 R101 · G3 of the round 101 block ordered the flip's staged numstat as `git diff --cached --numstat 5ce0c5a2` while the same block's C0 and C1 had already committed five `.agent/` paths after that base, so the literal command read 298 rows and +6370 -5820 against the ordered 293 and +5839 -5584; the worker reported both and declared it. THE RULE THAT FOLLOWS: a staged-diff reading names the commit the index was built on, never the round's base, when commits of the same round precede it.
END SLIP102

── SLICE DEC102 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC102 sha256=776a61f8f665c80608c81fa77a5cd4af1525f561238a2ccbd55cf68bf9a21857

## DECISION F275 D76 (2026-09-14, F275 round 102) — the first bridge round: `ruff`'s own fixer takes the flip's import rows, a guard test about the classic models keeps the classic models, and the command door rules the unified store's writer

CONTEXT. Round 101's flip left 40 bad test nodes in its committed transcript, and `ruff check .` rows far above the repository's frozen ceiling of 26. In the reviewer's dry-run tree of the flip, identical to `ebc0182c` in `packages`, `apps` and `tests`, the rows added are 320 import-order rows, 18 unused imports and 3 undefined names, all in files the flip changed. Eleven of the bad nodes are guards and pins whose subject the transform renamed without reading: the lint ceiling itself; the command door's import guard, which still rules `storage.save_job` while the door imports `pingpong_job.save_job_plan`; three routed-handler tests in `tests/test_data_paths.py` that call a `mint_job_id` they never import and read `id` off a unified record; the four job digest goldens, whose normalizer reads the job's id with `getattr(job, "id", "")`, a string the transform does not rewrite; and two guard tests whose subject is a classic pydantic model, the UUID ratchet's discriminator and the undeclared-keyword premise, which now point at unified dataclasses that are neither UUID-typed nor pydantic.

CHOSEN, FIRST: THE LINT ROWS ARE `ruff`'S OWN FIX. `ruff check --fix --select I001,F401` runs over the paths `ebc0182c` changed and nothing else. It also clears 15 rows those files already carried at `5ce0c5a2`, so the reviewer's dry run reads 11 rows, each of them also present at `5ce0c5a2`. The production edits are import order and unused imports only, so no mutation probe applies. ALTERNATIVE: sorting only the import blocks the transform touched, rejected because `I001` is reported per import block and the fixer cannot be told which of a file's blocks to leave.

CHOSEN, SECOND: A GUARD KEEPS ITS SUBJECT. The ratchet's discriminator and the undeclared-keyword premise import `packages.core.models` again, because the property each pins belongs to the classic models, which exist until the classic store is deleted. The three routed-handler tests keep their classic-shaped premise on the unified record: each saves a `JobPlan` whose `job_id` is a string UUID, and passes its first eight characters or its unhyphenated hex, the shape of an id written before the flip. ALTERNATIVE: a minted sixteen-hex id, rejected because such an id has no hyphens, so the stop test's two assertions would read the same string and contradict each other.

CHOSEN, THIRD: THE DOOR'S ONE WRITE-SIDE IMPORT IS `pingpong_job.save_job_plan`, in `ALLOWED_IMPORTS`, as `STORAGE_MODULE` with its one allowed name, and in the violation fixture, which imports `_persist_job` from that module. The guard's comment asks for the ruling decision beside a change to its allowed set; amendment amend0914-f275-sprint rule 5 puts this paragraph in the round's bookkeeping commit, which precedes the test edit.

CONSEQUENCE. Eleven nodes leave the bad set if nothing else moves, and amend0914 rule 3 binds round 102's transcript against round 101's. `R-0809`, `R-0880`, `R-0883` and `R-0884` stay open.

HOW TO REVERSE. Delete this paragraph block and revert round 102's two code commits; the eleven nodes are bad again, and `ruff check .` reads above its ceiling again.
END DEC102

── SLICE EDITS102 ── target SPEC E, applied to the paths it names ── JSON INPUT ──
BEGIN EDITS102 sha256=da534028847ffa5c0c23d10009c969b269e42695a1b49284b45165b4c939a61f
{
 "tests/test_data_paths.py": [
  [
   "        job = JobPlan(job_id=mint_job_id(), job_title=\"routed-handler\")\n        save_job_plan(job)\n        exit_code = None\n        try:\n            _cmd_guide_job(str(job.id)[:8], json_output=True)\n",
   "        job_id = str(uuid4())\n        save_job_plan(JobPlan(job_id=job_id, job_title=\"routed-handler\"))\n        exit_code = None\n        try:\n            _cmd_guide_job(job_id[:8], json_output=True)\n"
  ],
  [
   "        job = JobPlan(job_id=mint_job_id(), job_title=\"attach-by-prefix\")\n        save_job_plan(job)\n        project = RemyProject(name=\"attach-by-prefix\")\n        save_project(project)\n        short = str(job.id)[:8]\n        _cmd_attach_project_job(str(project.id), short)\n        assert load_project(project.id).job_ids == [str(job.id)]\n",
   "        job_id = str(uuid4())\n        save_job_plan(JobPlan(job_id=job_id, job_title=\"attach-by-prefix\"))\n        project = RemyProject(name=\"attach-by-prefix\")\n        save_project(project)\n        short = job_id[:8]\n        _cmd_attach_project_job(str(project.id), short)\n        assert load_project(project.id).job_ids == [job_id]\n"
  ],
  [
   "        job = JobPlan(job_id=mint_job_id(), job_title=\"stop-by-hex\")\n        save_job_plan(job)\n        _cmd_job_stop(job.id.hex)\n        assert stop_requested(str(job.id)) is not None\n        assert stop_requested(job.id.hex) is None\n",
   "        uid = uuid4()\n        save_job_plan(JobPlan(job_id=str(uid), job_title=\"stop-by-hex\"))\n        _cmd_job_stop(uid.hex)\n        assert stop_requested(str(uid)) is not None\n        assert stop_requested(uid.hex) is None\n"
  ]
 ],
 "tests/orchestration/test_job_digest.py": [
  [
   "    job_id = str(getattr(job, \"id\", \"\") or \"\")\n",
   "    job_id = str(getattr(job, \"job_id\", \"\") or \"\")\n"
  ]
 ],
 "tests/orchestration/test_uuid_record_ratchet.py": [
  [
   "        from packages.orchestration.pingpong_job import JobPlan\n\n        assert \"id\" in _uuid_fields(JobPlan), (\n",
   "        from packages.core.models import Job\n\n        assert \"id\" in _uuid_fields(Job), (\n"
  ]
 ],
 "tests/test_model_construction_keywords.py": [
  [
   "        from packages.orchestration.pingpong_job import TaskEntry\n\n        task = TaskEntry(**{\"title\": \"d\", })\n",
   "        from packages.core.models import Task\n\n        task = Task(**{\"description\": \"d\", \"type\": \"write_readme\"})\n"
  ]
 ],
 "tests/ui_server/test_command_channel.py": [
  [
   "        (\"packages.orchestration.storage\", \"save_job\"),                    # D21\n",
   "        (\"packages.orchestration.pingpong_job\", \"save_job_plan\"),          # D21\n"
  ],
  [
   "    #: `storage` is the one write-side module the door may reach, and only for\n    #: the single name DECISION F009 D21 puts in the effect table: the answer is\n    #: durable only once `save_job` returns. Any OTHER name from it is the\n    #: \"handler touching storage directly\" the Acceptance forbids.\n    STORAGE_MODULE = \"packages.orchestration.storage\"\n    STORAGE_ALLOWED_NAMES = frozenset({\"save_job\"})\n",
   "    #: `pingpong_job` is the one write-side module the door may reach, and only for\n    #: the single name DECISION F009 D21 puts in the effect table: the answer is\n    #: durable only once `save_job_plan` returns. Any OTHER name from it is the\n    #: \"handler touching storage directly\" the Acceptance forbids.\n    STORAGE_MODULE = \"packages.orchestration.pingpong_job\"\n    STORAGE_ALLOWED_NAMES = frozenset({\"save_job_plan\"})\n"
  ],
  [
   "            \"        from packages.orchestration.storage import delete_job\\n\"\n            \"        return apply_source_patch, delete_job\\n\"\n",
   "            \"        from packages.orchestration.pingpong_job import _persist_job\\n\"\n            \"        return apply_source_patch, _persist_job\\n\"\n"
  ]
 ]
}
END EDITS102
