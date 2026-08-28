# F033 source inventory — read from disk at `32cde54e`

Answers to the nine questions the F033 R1 block ordered. Every path, symbol and
quoted line was read from the working tree at this round's base, the merge
commit of pull request #218. Where nothing in this repository does the thing
asked about, the section says so in those words; `docs/roadmap/features/T5_F033.md`
Design section is a PROPOSAL and is never quoted here as description.

## 1. WHAT IDENTIFIES A HUNK TODAY

THE FIELD IS `id`, a string, one per hunk of the viewer JSON.
`parse_unified_diff_to_view` in `packages/orchestration/diff_parser.py` documents
the per-hunk shape as `{"id", "header", "old_start", "new_start", "lines"}`.

WHERE IT IS COMPUTED. In one place only, the flush loop at the end of
`parse_unified_diff_to_view`:

    for file_index, region in enumerate(regions):
        ...
        for hunk_index, raw in enumerate(region.hunks):
            ...
            hunks_out.append(
                {
                    "id": f"{file_index}:{hunk_index}",

During the walk the hunk dict is created with `"id": ""` and the comment
`# assigned on flush, when the file index is known`. Both indices are
ZERO-BASED. `file_index` runs over `regions` AFTER
`_collapse_doubled_header_regions` has folded the `workspace.diff` header echo
away and AFTER the `DIFF_VIEW_MAX_FILES` cut, which the module states is
deliberate: "fold the `workspace.diff` header echo away BEFORE regions become
files, so file indices — and therefore hunk ids — are numbered over the real
files."

A SECOND PRODUCER OF THE SAME SHAPE EXISTS ON THE CLIENT.
`apps/ui/src/api/diffViewModel.ts` line 244 synthesises the id when the wire
carries none:

    id: rawId !== "" ? rawId : `${fileIndex}:${hunkIndex}`,

So F033 must move TWO id producers, not one.

DOES IT SURVIVE AN EDIT MADE ELSEWHERE IN THE SAME FILE? NO. The id is a pair of
positional indices and nothing else. Insert or remove a hunk earlier in the same
file and every later hunk's `hunk_index` shifts, so its id changes; add or remove
a FILE earlier in the diff and every later file's `file_index` shifts, so every
one of its hunks changes id. The module says so itself in its docstring:

    Hunk ``id`` values are PROVISIONAL — ``"<file_index>:<hunk_index>"``, both
    zero-based, stable only within a single parse of a single diff text. F033
    replaces them with content-hash ids, and ``DIFF_VIEW_VERSION`` is the seam
    through which it does so.

The client repeats the same warning in the `buildDiffRowModels` docstring and
adds the one constraint the renderer really depends on: "Nothing here depends on
the id's SHAPE, only on the server assigning distinct ones."

TESTS THAT PIN THE CURRENT SHAPE, and therefore go red on a content-hash id:

- `tests/orchestration/test_diff_parser.py:409`
  `assert ids == ["0:0", "1:0"]`
  in `test_parse_unified_diff_to_view_keeps_input_order_and_distinct_hunk_ids`
- `tests/orchestration/test_diff_parser.py:417`
  `assert [h["id"] for h in entry["hunks"]] == ["0:0", "0:1"]`
  in `test_parse_unified_diff_to_view_seeds_each_hunk_from_its_own_header`
- `apps/ui/src/api/diffViewModel.test.ts:146` `expect(...hunks[0].id).toBe("0:0")`
  and `:217` `expect(readDiffEnvelope(noId).files[0].hunks[0].id).toBe("0:0")`,
  the latter pinning the CLIENT fallback specifically.

Two other tests assert only DISTINCTNESS and survive a reshape:
`test_diff_parser.py:872` and `:931` (`len(set(hunk_ids)) == len(hunk_ids)`).

## 2. THE VIEWER JSON'S VERSION FIELD

THE FIELD is `version`. THE CONSTANT is `DIFF_VIEW_VERSION`, declared in
`packages/orchestration/diff_parser.py:67` as `DIFF_VIEW_VERSION = 1`, with the
comment "Bumped whenever the returned shape changes; F033's content-hash hunk ids
are the first planned bump, and consumers gate on this rather than on key
sniffing."

THE SITES THAT SET IT — three in the parser, one in the source resolver:

- `diff_parser.py:490` the non-string early return
- `diff_parser.py:704` the normal return of `parse_unified_diff_to_view`
- `diff_parser.py:448` the docstring stating the returned shape
- `diff_view_source.py:105` seeds the envelope with `DIFF_VIEW_VERSION`, and
  `:191` overwrites it with `parsed["version"]` once the parse succeeds. That
  module imports the constant directly:
  `from packages.orchestration.diff_parser import DIFF_VIEW_VERSION, parse_unified_diff_to_view`

TESTS THAT PIN THE VALUE. Two classes, and only the second breaks on a bump.

Against the imported constant (bump-safe):

- `tests/orchestration/test_diff_parser.py:314` `assert view["version"] == DIFF_VIEW_VERSION`
- `tests/orchestration/test_diff_view_source.py:98-100`, all three assertions of
  `test_version_is_the_parsers_imported_contract_version`

Against the LITERAL `1` (these go red on a bump):

- `tests/orchestration/test_diff_parser.py:391-395`
  `test_parse_unified_diff_to_view_reads_empty_input_as_no_files` asserts
  `== {"version": 1, "truncated": False, "files": []}`
- `tests/orchestration/test_diff_parser.py:401`
  `test_parse_unified_diff_to_view_reads_non_diff_text_as_no_files`, same literal
- `apps/ui/src/api/diffViewModel.test.ts:138` `expect(envelope.version).toBe(1);`
  plus the wire fixtures at `:62`, `:79` and `:113` which set `version: 1`

The client's own default for an untrusted payload is `version: 0`, in
`unavailableDiffEnvelope()` (`diffViewModel.ts:270`); `readDiffEnvelope` reads the
wire value through `asInt` at `:301`. NO CLIENT CODE COMPARES `version` TO
ANYTHING — the field is carried, not gated on, today.

IS THERE A PRECEDENT FOR BUMPING A SCHEMA VERSION IN THIS REPOSITORY? YES, two.

- `packages/orchestration/token_ledger.py` `SCHEMA_VERSION` went 1 → 2 at commit
  `d84b4f8f` "feat(f115): add the call_segments table as migration step 2". The
  commit touched that ONE file, 25 insertions, and kept the sibling
  `SCHEMA_VERSION_KEY = "schema_version"` whose comment reads "so a future reader
  can tell old DBs apart".
- `packages/orchestration/runtime_integration_gate.py` `SCHEMA_VERSION` is
  `"1.1.0"`; the string was introduced at `fdbbe6e9` "fix(f018): runtime gate
  binds to test execution records, not name existence".

`gauntlet_orders.GAUNTLET_ORDER_SET_VERSION = 4` is NOT a precedent: it was born
at 4 in `17ca8bbb` and has never been changed.

## 3. THE HUNK LIBRARY `diff_repair` KEEPS TO ITSELF

`packages/orchestration/diff_repair.py` is 202 lines. Its public API, quoted from
its own docstring:

    select_repair_hunks(repo_root, changed_line_ranges, *,
                        margin_lines=3, max_total_chars=20000)
        -> RepairHunkSelection
    changed_line_ranges_from_patch(patch) -> {path: [[start, end], ...]}

`RepairHunk` is a frozen dataclass of `path`, `start_line`, `end_line`, `text` —
a SOURCE span with a margin, NOT a diff hunk. `RepairHunkSelection` is
`hunks`, `omitted` (`(path, reason)` pairs) and `total_chars`. The five omission
reasons are `missing`, `binary`, `no_ranges`, `out_of_bounds` and `budget`.

THE MODULE HOLDS NO PARSER AND NO APPLIER, and says so:

    It holds no unified-diff parser and no applier, on purpose. `review_scope`
    already turns a unified diff into per-file line ranges ... and
    `source_apply` is already the strict hunk applier that lands changes.
    Remedy deliberately does not add a third place that understands
    unified-diff syntax.

THE ONLY PRODUCTION CONSUMER is `packages/orchestration/builder_bridge.py`, which
imports both public names at `:25-27` and calls them inside
`_attach_diff_repair_hunks` at `:362` and `:366`. There is no other importer of
`packages.orchestration.diff_repair` anywhere under `packages/`, `apps/` or
`tests/`.

THE FIVE FILES THE BLOCK NAMES ALL CONTAIN THE STRING `diff_repair` — confirmed
by `grep -rln "diff_repair" tests/`, which returns exactly those five and no
others. BUT ONLY ONE OF THEM GUARDS THE THREE SYMBOLS THE BLOCK NAMES. Reported
honestly, because T001's safety net is narrower than the file list suggests:

- `tests/orchestration/test_diff_repair.py` — 404 lines, 30 tests. THE ONLY file
  that imports `RepairHunk`, `RepairHunkSelection`, `select_repair_hunks` and
  `changed_line_ranges_from_patch` (`:15-19`). Asserts: margin clamping at both
  file ends and a margin wider than the file; overlapping and adjacent range
  merging and distant ranges staying separate; sort order `(path, start_line)`;
  omission of NUL-byte, undecodable and missing files, and that one omitted path
  does not block a present one; the `max_total_chars` budget cut and that
  `total_chars` never exceeds the cap; zero margin; the `no_ranges` vs
  `out_of_bounds` distinction including the empty-file case; `text` equal to the
  exact source lines; that both result types are frozen dataclasses; and, for
  `changed_line_ranges_from_patch`, one hunk to one span, two hunks in order, two
  diffs to two paths, a declared path with no hunk header surviving as an empty
  list, `file_ops` paths carrying no lines, a markdown patch yielding nothing,
  and two end-to-end tests feeding those ranges into `select_repair_hunks`.
- `tests/orchestration/test_diff_repair_apply.py` — 398 lines, 9 tests. Guards
  `packages/orchestration/diff_repair_apply.py`, a DIFFERENT module: clean diff
  applies and reports diff mode; a conflicting hunk falls back leaving BOTH files
  untouched; an incomplete rollback reports the real count; a fence-denied path
  never reaches the applicator; validation rejection short-circuits before the
  applicator; new-file creation falls back; a stripped blank context line lands;
  a two-file answer whose first file continues past its hunk lands; job fences
  are derived when the caller passes none.
- `tests/orchestration/test_diff_repair_response.py` — 372 lines, 32 tests.
  Guards `packages/orchestration/diff_repair_response.py`: locating and decoding
  the JSON wrapper (fenced, bare, trailing prose, prose-only, broken JSON), the
  five missing-field errors, wrong `format`, unsupported `version`, declared-vs-
  touched path agreement, the fence precheck over absolute / `..` / dotenv /
  denied / out-of-allow-glob paths, blank-context-line repair, and conversion to
  a patch the validator accepts.
- `tests/orchestration/test_builder_repair_loop.py` — 619 lines, 14 tests.
  Guards `builder_bridge.run_builder_bridge_loop`. Reaches `select_repair_hunks`
  only INDIRECTLY, through `_attach_diff_repair_hunks`: the relevant tests are
  `test_diff_mode_attaches_margin_expanded_hunks_to_the_repair_context`,
  `test_diff_mode_off_leaves_the_repair_context_on_the_full_file_path`,
  `test_a_patch_without_line_ranges_reports_full_file_with_a_reason`,
  `test_the_diff_payload_is_a_fraction_of_the_full_file_payload` and
  `test_the_full_file_denominator_is_the_bytes_actually_on_disk`.
- `tests/ui_server/test_command_channel.py` — 1810 lines, 103 tests. Its ONE
  mention of the string is `"packages.orchestration.diff_repair_apply"` inside
  the `FORBIDDEN_MODULES` frozenset of the write-door import guard. It guards
  `diff_repair` only in the negative sense of forbidding the door to import the
  apply half. See section 5.

## 4. THE APPLICATOR

TWO MODULES, TWO ENTRY POINTS, AND THEY ARE NOT INTERCHANGEABLE.

`packages/orchestration/source_apply.py` — "Source Patch Apply v2". THE ENTRY
POINT F033 WOULD REUSE:

    apply_structured_patch(patch, repo_path, *, data_dir, job_id, job, intent_id) -> ApplyResult

Its preconditions, in the order the function checks them: `Capability.repo_generated_write`
via `permissions.is_allowed`; a non-None `intent_id`; that intent found by
`approval_queue.get_patch_intent` and in state `APPROVAL_APPROVED`;
`validate_structured_patch(patch)` clean; the repo root a directory; then the
F017 fence preflight `scope_fences.enforce_change_set(...)` with
`applicator="source_apply"`; then a MANDATORY durable snapshot —
`build_snapshot_path_set`, `create_snapshot`, `verify_snapshot` — and the apply
is BLOCKED if either the creation or the verification fails
(`snapshot_blocked:` / `snapshot_verify_failed:`).

ATOMICITY CONTRACT, and this is the answer to "what it does when ONE hunk of a
set conflicts": the apply loop is transactional AT THE FILE LEVEL and rolls the
whole set back.

    elif patch.intent_kind == "unified_diff":
        for diff in patch.unified_diffs:
            _apply_unified_diff(diff, repo_root, result)
            if not result.success:
                if result.snapshot_id:
                    _rollback_from_snapshot(...)
                break

`_apply_unified_diff` calls `_apply_hunks(original, diff.diff)`, which returns
`None` if ANY hunk of that file fails, and the caller then records
`"<path>: diff hunks did not apply cleanly"` and sets `success = False`. So ONE
conflicting hunk discards the whole file's diff AND triggers
`_rollback_from_snapshot` over every file already touched.
`_rollback_from_snapshot` restores from the durable snapshot BLOBS, deletes files
that did not exist before, and — this is the honest part — appends
`rollback_incomplete (<n> file(s)): ...` when it cannot restore everything, so a
partial rollback is reported rather than presented as a clean tree.

`_apply_hunks` applies STRICTLY, never fuzzily: every context and removal line is
compared byte-for-byte against the file (`if lines[actual_idx] != line[1:]: return None`),
an index outside the original file returns `None`, a header declaring a pure
insertion whose body consumed lines returns `None` ("Guessing which one is right
is how fuzzy apply starts; this repository applies diffs strictly"), and a
negative splice index returns `None`.

On success `apply_structured_patch` writes a `DurableApplyRecord` with
`state="applied"`, `before_proof` and `after_proof` (sha256 + byte counts, never
content) and emits the run event `source_patch_applied`.
`revert_apply(apply_id, repo_path, *, job_id, data_dir)` delegates to
`repository_snapshot.revert_repository_apply`.

`packages/orchestration/patch_apply.py` — "Patch Apply v0", entry point
`apply_patch_intent(job, intent_id, *, data_dir=None, target_repo_override=None)`.
NOT the applicator F033 wants: it is markdown-only, append-only for existing
files, applies no diffs at all ("no arbitrary diff application"), blocks
high/unknown risk intents, and is idempotent through metadata records under
`artifact.metadata["patch_intent_apply_records"][intent_id]` whose `state` is
`"applied" | "noop" | "blocked"`.

The Do-not-touch list of `docs/roadmap/features/T5_F033.md` forbids changing
applicator internals, so both of the above are recorded here as they stand.

## 5. THE WRITE CHANNEL

`UI_EXPOSED_COMMANDS` is declared at `apps/cli/command_catalog.py:4809`:

    UI_EXPOSED_COMMANDS: frozenset[str] = frozenset({
        "job.stop",
        "decision.resolve",
    })

CONFIRMED: exactly the two ids the block names. Its comment reads "The whole
surface of the UI write door: no other `command_id` above is reachable from a
browser". `tests/ui_server/test_command_channel.py:1562` pins it exactly —
`assert sorted(UI_EXPOSED_COMMANDS) == ["decision.resolve", "job.stop"]` — and
`:1566` pins that it is a `frozenset`, `:1571` that every member resolves through
`get_command`.

THE DOOR is `_handle_command_submission(self, job_id_str)` at
`packages/orchestration/ui_server.py:3605`, reached only from `do_POST` and only
for a path of exactly five segments `/api/jobs/<id>/commands`; every other POST,
and every PUT and DELETE, is 405.

EVERY GUARD A NEW COMMAND MUST SATISFY, in the order the door applies them, with
the test file each lives in. All of them are in
`tests/ui_server/test_command_channel.py` unless stated.

1. METHOD AND PATH — only the commands path opens the door
   (`test_post_to_non_commands_path_is_405`, `test_a_near_miss_of_the_commands_path_is_405`).
2. BEARER TOKEN — `_bearer_token_accepted`, constant-time via
   `server_token_matches`; 403 and audited `rejected_token` with `create=False`
   (`test_missing_bearer_is_403` and the four beside it).
3. CSRF HEADER — `COMMAND_CSRF_HEADER`, checked AFTER the bearer
   (`test_csrf_is_checked_after_the_bearer`).
4. JOB RESOLUTION — `_load_job`; 404, audited `rejected_job`
   (`test_unresolvable_job_id_is_404`, `test_job_id_is_checked_after_the_credentials`).
5. BODY SHAPE — `_read_command_payload` (`ui_server.py:3983`): `Content-Length`
   present, positive and `<= COMMAND_REQUEST_MAX_BYTES`; valid UTF-8 JSON; a JSON
   OBJECT; `command` a non-empty string; `client_nonce` a non-empty string that
   `command_nonce.nonce_is_valid` accepts as a filename ("1-64 characters of
   letters, digits, '-' or '_'"); `args` absent or a JSON object. Each failure is
   400 on its own field name and audited `rejected_shape` (eleven tests,
   `test_absent_body_is_400_on_field_body` through `test_non_object_args_is_400_on_field_args`).
6. EXPOSED-SUBSET MEMBERSHIP — `_command_is_ui_exposed` (`:3916`), which imports
   `UI_EXPOSED_COMMANDS` inside the function. 400 on field `command` with
   `COMMAND_NOT_EXPOSED_MESSAGE`, audited `rejected_command`
   (`test_unexposed_catalog_command_is_400_on_field_command`,
   `test_the_two_refusals_are_indistinguishable`).
7. NONCE REPLAY — `_replayed_command_result`, placed after the subset check and
   before the budget; a hit returns the ORIGINAL body and audits `replayed`
   (`test_a_replayed_nonce_answers_from_the_store_byte_for_byte`,
   `test_a_replay_is_not_the_acceptance_it_repeats`).
8. RATE LIMIT — `_rate_limit_admits_command`, spent LAST; 429 audited
   `rejected_rate` (`test_the_last_command_in_budget_is_accepted_and_the_next_is_429`,
   `test_a_shape_error_does_not_spend_budget`).
9. A DISPATCH BRANCH — a command in the exposed set with no `if payload["command"] == ...`
   clause falls through to 501 `not_implemented`
   (`test_an_exposed_id_with_no_dispatch_branch_is_the_501_guard`). SO ADDING AN
   ID TO THE FROZENSET WITHOUT A BRANCH IS A 501, NOT A CRASH.
10. WRITE ORDER — effect first, then the `accepted` audit line, then the nonce
    publication, then the SSE announcement; the last two fail SOFT
    (`test_a_dispatched_command_is_audited_as_accepted`,
    `test_an_accepted_command_reaches_the_sse_frame_it_announces`,
    `test_an_event_writer_that_raises_changes_neither_status_nor_body`).
11. THE AUDIT VOCABULARY IS CLOSED —
    `test_every_outcome_the_door_writes_is_in_the_ruled_vocabulary`.

THE IMPORT GUARD, and it is the single most consequential fact in this section.
`tests/ui_server/test_command_channel.py:1414-1470` holds an AST-based guard over
`DOOR_METHODS` — the ten methods listed at `:1414` — with an `ALLOWED_IMPORTS`
frozenset of exactly 16 `(module, name)` pairs, and a `FORBIDDEN_MODULES`
frozenset:

    FORBIDDEN_MODULES = frozenset({
        "packages.orchestration.source_apply",
        "packages.orchestration.patch_apply",
        "packages.orchestration.diff_repair_apply",
        "packages.orchestration.job_fulfillment",
        "packages.orchestration.exec_guard",
        "packages.orchestration.workspace",
        "packages.common.secure_fs",
        "subprocess",
        "shutil",
    })

THE DOOR MAY NOT IMPORT THE APPLICATOR. An `approve_hunks` command whose effect
calls `apply_structured_patch` from inside `_handle_command_submission` or a new
`_dispatch_approve_hunks` listed in `DOOR_METHODS` turns this guard red. Widening
`ALLOWED_IMPORTS` is possible — the comment says "Adding an entry means widening
the P3 contract, so it belongs in the same commit as the decision that widens it"
— but `FORBIDDEN_MODULES` is an absolute list and `source_apply` is on it. The
guard also requires `test_every_named_method_exists` to keep `DOOR_METHODS`
honest, and `storage` is reachable only for the single name `save_job`.

THE WALKABLE-PATH LIST is `_walkable_paths` at `:1280`. It derives the per-job GET
endpoints from `do_GET`'s own dict literals by AST walk, then adds six structural
routes by hand, including `f"/api/jobs/{self.job_id}/task-runs/T001/diff"`.
`test_the_walk_knows_every_route_the_source_dispatches` is what stops that list
from going stale, and `test_every_route_the_server_serves_refuses_post_put_and_delete`
asserts the commands path is the ONLY POST that is not 405.

## 6. THE VALIDATION PRECEDENT

NO COMMAND IN THIS REPOSITORY REQUIRES A REASON ON A NEGATIVE ANSWER TODAY.
Searched: every `reject`/`reason` pairing under `packages/` and `apps/`; every
test function name matching `test_.*reason` under `tests/`; the strings "requires
a reason", "reason required", "mandatory reason", "veto"; `approval_queue.py`,
`flight_plan.py`, `escalation.py`, `decision_queue.py`, `proposed_tasks.py` and
`apps/cli/commands/decision.py` read directly.

The feature this repository calls the veto is `F027 — Task veto`, and
`docs/roadmap/STATUS.md:93` carries it as `- [ ] F027`, i.e. NOT BUILT.
`docs/roadmap/ROADMAP.md:805` describes it as "Forbid a not-yet-applied node with
a mandatory reason". So "the veto lesson" names an unbuilt feature's rule, not an
existing enforcement.

WHAT IS NEGATIVE-ANSWER-ADJACENT AND OPTIONAL, so F033 must not mistake it for
the precedent:

- `approval_queue.set_approval_state(job, intent_id, state, *, reason=None, ...)`
  — `reason` is documented "optional free-text note from the user"; the pair
  `test_reject_with_reason_prints_recorded` / `test_reject_without_reason_prints_none`
  in `tests/test_patch_intent_approval.py:619` and `:626` pins that BOTH are legal.
- `proposed_tasks.reject_proposed_task(..., reason: str = "")` writes
  `evaluation_notes` only `if reason:`; `tests/orchestration/test_proposed_tasks.py:361`.
- `_dispatch_decision_resolve` in `ui_server.py:3740` accepts exactly `approve`
  and `reject` for an `fp:`-prefixed id and carries no reason at all.

THE TWO REAL PRECEDENTS FOR "AN EXCEPTIONAL STATE MUST NAME ITS REASON OR IT
BLOCKS", which is the rule F033 actually wants:

1. `JobFulfillmentContract.check` in `packages/orchestration/job_fulfillment.py:130-136`:

       if self.requires_proof_verified:
           if record.proof_status == "verified":
               pass  # OK
           elif record.proof_status == "accepted" and record.proof_accepted_reason:
               pass  # explicit accept with reason
           else:
               blockers.append(f"proof_not_verified:{record.proof_status}")

   An `accepted` proof with an EMPTY `proof_accepted_reason` blocks. Tested in
   `tests/orchestration/test_job_fulfillment.py:254`
   `test_accepted_proof_without_reason_blocks` against its positive twin
   `test_accepted_proof_with_reason_passes` at `:268`.
2. The run-manifest snapshot phase requirement: an `unavailable` workspace
   identity with an empty `problems` list is a hole. Tested in
   `tests/orchestration/test_run_manifest_snapshot_phase_requirements.py:70`
   `test_an_unavailable_workspace_identity_without_a_reason_blocks` ("A blank
   unavailable is a hole"), asserting the problem text contains "gives no
   reason", against `test_an_unavailable_workspace_identity_with_a_reason_is_accepted`
   at `:78`.
3. A weaker third, on the CLI: `apps/cli/commands/decision.py:240-249` refuses a
   task-decision resolution whose `--reason` is blank AND whose record has no
   `safe_default`, with "Error: --reason carries the answer for a task decision,
   and this one has no safe default to fall back on."

## 7. THE SEAM A REJECTION RIDES INTO THE NEXT ROUND'S PROMPT

THERE IS NO MODULE, FUNCTION OR CONSTANT NAMED "steering" OR "volatile injection"
IN THIS REPOSITORY. `grep -rn "steering"` over `packages/` and `apps/` returns
exactly ONE line, and it is prose inside a docstring:
`packages/orchestration/context_compiler.py:1031`, in
`register_compiled_context_segment`, explaining that `JOB_CONTEXT` "composes after
the stable system and conventions prefixes a provider cache wants byte-identical,
and before the volatile task and steering tails." `packages/orchestration/prompt_segments.py:52`
carries the same idea as "Stable prefixes first so the provider cache can hit
them, volatile tails last." The `SegmentStabilityRank` ordering is real; a
"steering" segment is not.

THE SEAM THAT ACTUALLY EXISTS, and the one F033's rejections must ride:

- MODULE `packages/orchestration/repair_context.py`, FUNCTION
  `build_repair_context(job_id, test_run_event, events) -> dict`. It returns a
  flat dict with keys `version` (1), `job_id`, `test_run_id`,
  `related_apply_id`, `status`, `safe_summary`, `failure_kind`, `affected_files`,
  `estimated_tokens`, `truncated`. Its contract is "suitable for logging as
  ``repair_context_created`` event metadata — never contains raw stdout/stderr or
  tracebacks."
- THE ENRICHMENT SITE is `_attach_diff_repair_hunks` in
  `packages/orchestration/builder_bridge.py:342`. It is the ONLY place that adds
  keys to that dict:

      repair_ctx["diff_hunks"] = [ {path, start_line, end_line, text}, ... ]
      repair_ctx["diff_hunks_omitted"] = [list(entry) for entry in selection.omitted]

  and it sets `repair_ctx["repair_mode"]` to `"diff"` or `"full_file"` plus
  `full_file_reason` on the fallback arm (`:493-494`). Its docstring warns
  "`build_repair_context`'s contract is that its dict is safe to log; source
  [text is not put in the metadata]" — hunk TEXT goes into the CONTEXT but the
  EVIDENCE metadata carries counts only.
- THE CARRIER into the prompt is `run_builder_bridge_loop` at
  `builder_bridge.py:402`, which calls `output = build_fn(repair_ctx)` at `:436`.
- ONE CONCRETE `build_fn` shows what "flows through it today":
  `long_run_executor.default_repair_step` at `:1137` builds

      prior_task_summaries=[json.dumps(repair_context or findings, sort_keys=True)]

  inside a `TaskExecutionContext`. So the repair context is serialised WHOLE, as
  sorted JSON, into `prior_task_summaries`.
- `long_run_executor.build_cycle_repair_findings` at `:1155` is the other
  producer: it starts from `build_repair_context` and adds `source`,
  `cycle_index`, `repair_round`, `failing_test_ids`, `failure_tail` and
  `changed_files`.

WHAT ALREADY FLOWS THROUGH IT TODAY: the failure kind and exit code, the related
apply id, the affected file list, the failing test ids, a bounded failure tail,
the changed files, the repair mode and — since F111 — the margin-expanded source
hunks and the per-path omission reasons. NOTHING carrying a human's words flows
through it yet.

## 8. WHERE A TASK'S CHANGE STATE IS RECORDED

THREE RECORDS, at three levels. None of them has a value meaning PARTIAL.

1. THE TASK'S OWN LIFECYCLE. `packages/core/models.py:125` — `Task.status: RunState`.
   `RunState` (`:38-47`) accepts exactly `pending`, `planned`, `running`,
   `paused`, `completed`, `failed`, `cancelled`. This is a RUN state, not a
   change state.
2. THE PER-CHANGE APPLY STATE, which is the real answer. `ProofChange` in
   `packages/orchestration/proof_chain.py:69`, field `apply_state`, whose
   declaring comment at `:79` is the whole vocabulary:

       apply_state: str          # not_applied | applied | reverted

   `proof_status` beside it is drawn from `PROOF_VERIFIED`, `PROOF_FAILED`,
   `PROOF_INCOMPLETE`, `PROOF_UNVERIFIED`, `PROOF_NOT_APPLICABLE`
   (`proof_chain.py:34-42`).
3. THE PER-TASK ROLL-UP the UI reads. `_task_truth_maps(chain)` at
   `packages/orchestration/ui_server.py:508` groups `chain.changes` by `task_id`
   and folds:

       apply_states = [getattr(c, "apply_state", "") for c in changes]
       if "applied" in apply_states:
           apply_by_task[tid] = "applied"
       elif "reverted" in apply_states:
           apply_by_task[tid] = "reverted"
       else:
           apply_by_task[tid] = "not_applied"

   The call site at `:1829` adds one more value — `"unknown"` when the proof
   chain is unavailable — into the dashboard field `apply_status`.

DOES ANY EXISTING VALUE ALREADY MEAN PARTIAL? NO. And the fold above is worse
than merely silent: `if "applied" in apply_states` is an ANY, so a task whose
changes are half applied and half not reports `applied` today. That is the exact
untruth F033's partial state has to replace, and it lives in one function.

The nearest thing to the word in the tree is `DurableApplyRecord.state`
(`packages/orchestration/repository_snapshot.py:144`), documented
`"pending" | "applied" | "reverted" | "revert_failed" | "partial_revert"`. Its
`partial_revert` means a ROLLBACK that could not finish — see
`_rollback_from_snapshot`'s `rollback_incomplete` in section 4 — and NOT a
partially approved change. Reusing that token for hunk approval would collide
with an existing meaning.

## 9. THE THREE SURFACES A PARTIAL STATE MUST RENDER IN

1. THE VIEWER. `apps/ui/src/components/diff/DiffView.tsx`, exporting
   `DiffViewProps` (`:86`) and `function DiffView({ envelope })` (`:94`), with
   `apps/ui/src/components/diff/DiffFileSidebar.tsx` exporting
   `DiffFileSidebarProps` (`:45`) and `DiffFileSidebar` (`:53`), both mounted
   side by side in `apps/ui/src/components/shell/RemedyShell.tsx:136-137`. The
   row model they render is `buildDiffRowModels(envelope, collapsed)` in
   `apps/ui/src/api/diffViewModel.ts:281`, whose row keys are `file:<i>` and
   `hunk:<hunkId>`; per-hunk state therefore has a per-row seat already.
   Styling is `apps/ui/src/components/diff/DiffView.module.css`; the envelope
   reader is `readDiffEnvelope` (`diffViewModel.ts:291`) and the fetch seam is
   `apps/ui/src/api/remedyApi.ts`, which imports `readDiffEnvelope` at `:3`.
2. THE NODE GLYPH. `apps/ui/src/components/detail/DetailPopover.tsx`, function
   `StateIcon({ state })` at `:17`, which maps `done` → `TaskDoneGlyph`,
   `current` → `TaskCurrentGlyph`, `blocked` → `TaskPlannedGlyph` in red, and
   everything else → `TaskPlannedGlyph` in `--remedy-ink-soft`. The label table
   beside it is `STATE_LABELS` at `:6` (`done`, `current`, `planned`, `blocked`,
   `pending`, `suggested`), and the same file already renders the apply state
   through `applyStatus(task)` at `:34`, which returns "Applied", "Reverted",
   "Not applied" or `UNKNOWN` — the function a `partial` value has to reach.
   The glyphs themselves are `TaskDoneGlyph`, `TaskCurrentGlyph` and
   `TaskPlannedGlyph` in `apps/ui/src/components/icons/RemedyGlyphs.tsx` (`:44`,
   `:60`, `:52`); THERE IS NO PARTIAL GLYPH IN THAT FILE. The graph node state
   vocabulary is narrowed in `apps/ui/src/components/graph/buildForceBrainModel.ts:76`
   to `done | current | blocked | suggested | planned`, defaulting anything
   unknown to `planned` — a new state added upstream renders as `planned` unless
   that line is widened. `apps/ui/src/components/panels/TaskChecklistCard.tsx:7`
   is the second glyph consumer, with only a done/else branch.
3. THE REPORT LINE. `_task_lines(sources)` at
   `packages/orchestration/run_report.py:424`, whose body is exactly:

       f"- `{t.task_id}` — {_text(t.description)} — **{_text(t.status)}**"
       + (f" — {_link('evidence', t.evidence_ref)}" if t.evidence_ref else "")

   `t` is a `TaskOutcome` (`:227`) of `task_id`, `description`, `status`,
   `evidence_ref`. Its `status` is filled in `collect_report_sources(job)` at
   `:727` from `getattr(getattr(t, "status", None), "value", ...)` — that is
   `Task.status`, the RunState of section 8, NOT the apply state. So a report
   line reading "partially approved (5/8 hunks)" needs a NEW field on
   `TaskOutcome`; today the record carries nothing that could say it.
   `recommended_next_action` at `:360` reads the same statuses and treats
   `all(status == "completed")` as `all-green`, so a partial task must not be
   allowed to reach `completed` without that rule being revisited.

## Unanswered

None. Every question above is answered from code read at this round's base. The
two answers that are ABSENCES rather than findings — no reason-on-rejection
enforcement exists (section 6), and no steering/volatile-injection symbol exists
(section 7) — are stated as absences on purpose.
