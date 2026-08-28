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
