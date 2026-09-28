# Handoff — F035, round 4 (T003's first half: `remedy job ownership` and the browser's
`ownership` read route answer one shared view, and plan edits read in plain verbs)

## Session

SESSION 1 of feature F035 · round 4 · rounds so far 4. Context remaining at handback: a
comfortable majority of the budget is left — the round read AGENTS.md, the block, the two
payloads and the handback template once, read `ownership_phrases.py`, its test and golden,
`job_steer_cmd.py` and its test, the catalog's `job.steer` entry and `_JOB_ID`/`_JSON_OPT`,
`apps/cli/commands/__init__.py`, `exit-codes.md`, `ui_server.py`'s `do_GET` handler table and
`_build_digest_json`, `test_digest_route.py`, `test_handler_table_walk.py`,
`test_exit_codes.py`, `job_id_arg.py`, `job_veto_cmd.py`, `job_digest.py`'s own ownership
reading and its tests, `ownership.py`'s `build_ownership_ledger`, and `pingpong_job.py`'s
`load_job_plan`, before writing the view, the command, the route, the golden and its ten new
sentences, three test files and the mutation tool, ran the full gate selection twice and the
mutation tool once.

## Range

Review of `490a81f46`..`HEAD` (`HEAD` is this handback's own commit, `F035 R4 C5`, on
`feature/f035-ownership-ledger`).

## Commits

### 9f401de42 F035 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r4-block.md | 267/0 | verbatim copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f035-r4-booking.diff | 55/0 | verbatim copy of the booking.diff payload |
| .agent/authored/f035-r4-plan.md | 28/0 | verbatim copy of the plan.md payload |

Measured insertions: 350 (267+55+28). Block expected the block's own line count (267) plus 83 =
350. Match, under the 500-line cap.

### ec4e5e268 F035 R4 C2: book round 3, record D4, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 37/0 | DECISION F035 D4 appended by `git apply booking.diff` |
| .agent/live_review.md | 2/0 | round 3's Gate entry appended by `git apply booking.diff` |
| .agent/plan.md | 6/6 | rewritten to the plan.md payload |

Measured numstat: 37/0, 2/0, 6/6 — equal to the block's G2 expectation exactly.

### a1e6c0f5d F035 R4 C3: remedy job ownership and the ownership route over one view, plain edit verbs
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 15/0 | NEW `job.ownership` entry, directly above `job rerun-subtree`, under a width-75 comment matching its neighbours |
| apps/cli/commands/__init__.py | 2/1 | `job_ownership_cmd` imported alphabetically and added to the handler-collection tuple |
| apps/cli/commands/job_ownership_cmd.py | 62/0 | NEW: `_cmd_job_ownership`, modelled on `job_steer_cmd.py` — text form, `--json`, `job_not_found` at 3, `ownership_unreadable` at 1 |
| docs/guides/exit-codes.md | 1/0 | `remedy job ownership` row added directly under `remedy job steer`'s |
| packages/orchestration/ownership_phrases.py | 74/15 | S1 plain-verb plan-edit templates (`_version_phrase`, six named commands, the unknown-command fallback), S2 `ownership_view` |
| packages/orchestration/ui_server.py | 8/0 | `_build_ownership_json`, `"ownership"` joins the `handlers` table directly after `"digest"` |
| tests/orchestration/fixtures/ownership/golden/sentences.txt | 8/2 | the two existing plan-edit lines re-worded, six new lines for S1's named commands |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | `apps.cli.commands.job_ownership_cmd` added in its sorted place, the only new reachable module |

Measured insertions: 171 (15+2+62+1+74+8+8+1), 18 deletions. The block states no expectation for
C3; this is what was measured, under the 500-line cap. `test_import_reachability.py` was run
standalone (see G4) and named no module beyond `job_ownership_cmd`.

### 2b099efb2 F035 R4 C4a: test the ownership view, command and route (SPLIT — see Deviations)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_ownership.py | 117/0 | NEW: text form with/without entries, `--json`'s keys, exit 1/3/1 for a malformed id/unknown job/raising ledger |
| tests/orchestration/test_ownership_phrases.py | 175/13 | NEW inline assertions for every S1 plan-edit sentence, `version 7` for ref `v7`, the unknown-command fallback, `ownership_view`'s shape and error form; golden-count docstring/assertions updated 22→28 |
| tests/ui_server/test_ownership_route.py | 127/0 | NEW: 200 with the view's keys and sentences, 404 unknown job, 403 wrong token, a neighbouring name still unhandled |

Measured insertions: 419 (117+175+127), 13 deletions. The block states no expectation for C4;
this is what was measured.

### bea197297 F035 R4 C4b: add the mutation tool for the round's red proofs (SPLIT — see Deviations)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r4-mutations.py | 157/0 | the G5 red-proof tool: eight mutations across the three production files, an unmutated control first and last, restore-and-verify |

Measured insertions: 157. Combined with C4a's 419, the un-split total would have been 576,
over the 500-line cap; split per constraint 2, declared here and in Deviations below.

### This commit F035 R4 C5: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- `git apply --check .remedy-wt/f035-r4-payloads/booking.diff` — exit 0.
- `git apply .remedy-wt/f035-r4-payloads/booking.diff` — exit 0.
- `git worktree add --detach .remedy-wt/f035-r4-base 490a81f46` — succeeded, used ONLY to
  measure `--collect-only -q` node counts of the round's selection at the base commit for G4's
  accounting (the block gave no such counts to start from, unlike its PASS reading); removed
  with `git worktree remove --force .remedy-wt/f035-r4-base` and `git worktree prune` before G5
  began. Declared under Deviations — the block names one extra worktree (G5's).
- `git worktree add --detach .remedy-wt/f035-r4-mut bea197297` at C4b — succeeded; ran the
  mutation tool (all eight caught on the only run); `git worktree remove --force
  .remedy-wt/f035-r4-mut` and `git worktree prune` — both succeeded.
- `git push` — reported in the reply per the block (G6 cannot go in this file, written before
  the push).
- No PR created or merged — the block orders none, and none was created.

## Verification

G1 TRANSPORT — payloads measured against the PAYLOADS table before use:
```
booking.diff: 55 lines, 14156 bytes, sha256 0c8dda65eccf2223d8de6c5eacf21d7f92b3737d59331e754588bca17214c6ec — MATCH
plan.md:      28 lines, 891 bytes,   sha256 166499d5d686f7ca8ae76e09ab94c5a77407ea5a16dddefc66bd7f07f4c78067 — MATCH
```
Copies at C1, read back with `git show <C1>:<path>` and compared byte-for-byte against the
source: `.agent/authored/f035-r4-block.md` vs `.remedy-wt/f035-r4/block.md` — IDENTICAL (sha256
`2309387f3d167956af94b2148c8191d2b8745bb4a0e5763cd9f23432be6c24fe` both sides);
`.agent/authored/f035-r4-plan.md` vs the plan.md payload — IDENTICAL;
`.agent/authored/f035-r4-booking.diff` vs the booking.diff payload — IDENTICAL.

G2 THE BOOKING — at C2 (`ec4e5e268`), `git show <C2>:<path>` read and hashed:
```
.agent/decisions.md    2335016 bytes  00dcdd7272a756ca58599ad03c5aaa44124cce450d6d6fed38706ec11970ba62 — MATCH
.agent/live_review.md   309756 bytes  d8ab67afee13dd427fbff5d4bbab12c30a2ff06e52edb2c9415e08c8bf57d161 — MATCH
.agent/plan.md             891 bytes  166499d5d686f7ca8ae76e09ab94c5a77407ea5a16dddefc66bd7f07f4c78067 — MATCH
```
`scripts.rotate_live_review.open_finding_ids` over the C2 ledger text: `[]` (empty, as the
reviewer read). The ledger's last line at C2 begins `Gate: F035 R3 — ` (confirmed by direct
read of the last line).

G3 THE CODE — at C4b (`bea197297`):
```
$ python3 -m ruff check packages/orchestration/ownership_phrases.py packages/orchestration/ui_server.py \
    apps/cli/command_catalog.py apps/cli/commands/job_ownership_cmd.py apps/cli/commands/__init__.py \
    tests/orchestration/test_ownership_phrases.py tests/cli/test_job_ownership.py tests/ui_server/test_ownership_route.py
All checks passed!
REAL_EXIT=0
```
The golden file's changed lines, quoted from `git show a1e6c0f5d -- tests/orchestration/fixtures/ownership/golden/sentences.txt`:
```
-You (browser, token #1) edited the plan (task edit T2 --acceptance add) for task T2 (Task Two); the plan is now v7.
-You edited task T3 (Task Three) while the job ran (task edit T3 --files add src/x.py); the plan is now v8.
+You (browser, token #1) edited the plan (task edit T2 --acceptance add) for task T2 (Task Two); the plan is now version 7.
+You changed task T1 (Task One) in the plan; the plan is now version 9.
+You changed the acceptance checks of task T2 (Task Two) in the plan; the plan is now version 10.
+You deleted task T3 (Task Three) from the plan; the plan is now version 11.
+You split task T4 (Task Four) in the plan; the plan is now version 12.
+You merged tasks in the plan; the plan is now version 13.
+You reordered the plan's tasks; the plan is now version 14.
+You edited task T3 (Task Three) while the job ran; the plan is now version 8.
```
The catalog entry, quoted from `git show a1e6c0f5d:apps/cli/command_catalog.py`:
```python
    # ── job ownership (F035 T003, DECISION F035 D4) ──────────────────────
    CommandEntry(
        command_id="job.ownership",
        group_id="job",
        subcommand="ownership",
        description="Show who did what in a job under its mission: every recorded action of "
                    "the operator on the job or one of its tasks, every default the operator "
                    "accepted and every choice Remedy's planner made, one plain sentence each, "
                    "read from the job's own records and never written by this command (F035).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("job.show", "job.veto-task", "job.steer"),
        exit_codes=(0, 1, 2, 3),
    ),
```
The handler, quoted from `git show a1e6c0f5d:packages/orchestration/ui_server.py`:
```python
def _build_ownership_json(job: Any) -> dict[str, Any]:
    """Build the ownership-ledger payload — the SAME view `remedy job ownership` prints
    (F035 T003, DECISION F035 D4)."""
    from packages.orchestration.ownership_phrases import ownership_view
    return ownership_view(job)
```
and the `handlers` table entry `"ownership": _build_ownership_json,` directly after
`"digest": _build_digest_json,`.

The real output of `python3 -B -m apps.cli.main job ownership --help`:
```
 Usage: remedy job ownership [OPTIONS] JOB_ID

 Show who did what in a job under its mission: every recorded action of the operator on the job or one of its tasks, every default the operator accepted and every choice Remedy's planner made, one plain sentence each, read from the job's own records and never written by this command (F035).

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│  job_id  UUID of the job (under its mission)                                 │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Options ────────────────────────────────────────────────────────────────────╮
│  --json  Output as JSON                                                      │
│  --help  Show this message and exit.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

G4 THE TESTS — SERIALLY, at C4b (`bea197297`), the block's full 29-path selection:
```
$ python3 -m pytest -q -p no:cacheprovider -rs <the block's 29-path selection>
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1296 passed, 1 skipped in 84.16s
REAL_EXIT=0
```
Accounting for 1296: the reviewer's own baseline at `490a81f46` (this selection LESS the two
new test files) read 1272 passed, 1 skipped — confirmed by `--collect-only -q` over that exact
selection in a disposable worktree at `490a81f46`: 1273 collected (matches 1272+1). `--collect-
only -q` node counts, measured fresh: `test_ownership_phrases.py` 18 at `490a81f46` → 29 at C4
(+11, the new S1/S2 inline tests); `tests/cli/test_job_ownership.py` 7 (new file);
`tests/ui_server/test_ownership_route.py` 4 (new file); `tests/cli/test_exit_codes.py` +2 new
parametrized nodes (`test_declared_codes_are_the_floor_plus_named_codes[job.ownership]`,
`test_declared_codes_equal_the_codes_the_handler_reaches[job.ownership]`, both parametrized
over `CATALOG`, which now carries the new entry). 1273 + 11 + 7 + 4 + 2 = 1297 collected at C4,
confirmed directly by `--collect-only -q` over the same 29-path selection at C4: 1297. 1297 =
1296 passed + 1 skipped. Match, real exit 0.

Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks read `pass`.

G5 THE RED PROOFS — one run, over C4b (`bea197297`): `git worktree add --detach
.remedy-wt/f035-r4-mut bea197297`, then `python3 -B .agent/authored/f035-r4-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f035-r4-mut`:
```
control (before): exit=0 failed=0 nodes=[]
m1 (plan_delete_task reads with the unknown-command fallback): exit=1 failed=2 nodes=[...test_the_golden_ledger_s_sentences_match_byte_for_byte, ...test_plan_delete_task_reads_deleted_t_from_the_plan]
m2 (the version keeps its leading v): exit=1 failed=10 nodes=[...golden..., every plan-edit sentence test]
m3 (ownership_view leaves out each entry's sentence): exit=1 failed=4 nodes=[...test_ownership_view_carries_a_sentence_on_every_entry, ...test_the_text_form_lists_one_sentence_per_entry, ...test_the_json_form_carries_a_sentence_on_every_entry, ...test_ownership_endpoint_answers_the_view_for_a_job_with_an_action]
m4 (ownership_view answers an empty error when the ledger raises): exit=1 failed=2 nodes=[...test_ownership_views_error_form, ...test_a_ledger_that_raises_exits_1]
m5 (an unknown job exits 1 instead of 3): exit=1 failed=1 nodes=[...test_an_unknown_job_exits_3]
m6 (a ledger error exits 0 and prints nothing): exit=1 failed=1 nodes=[...test_a_ledger_that_raises_exits_1]
m7 (a job with no entry prints nothing): exit=1 failed=1 nodes=[...test_the_text_form_reports_no_action_for_an_empty_ledger]
m8 (the ownership key is left out of the handlers table): exit=1 failed=1 nodes=[...test_ownership_endpoint_answers_the_view_for_a_job_with_an_action]
control (after): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
`git worktree remove --force .remedy-wt/f035-r4-mut` and `git worktree prune` — both succeeded;
`git worktree list | wc -l` read 61 (equal to step 4's reading, unchanged) and `git branch
--list 'remedy/*' | wc -l` read 197 (unchanged).

## Authored-text proofs

`.agent/authored/f035-r4-block.md`, `.agent/authored/f035-r4-plan.md` and
`.agent/authored/f035-r4-booking.diff`, each compared byte-for-byte at C1 against its payload
source — all IDENTICAL (see G1 above). `booking.diff`'s own effect on `.agent/decisions.md`,
`.agent/live_review.md` and `.agent/plan.md`, read at C2 by size and sha256 — all equal to the
reviewer's simulation tree (see G2 above).

## Deviations & assumptions

1. C4 was split into C4a (`2b099efb2`, 419 insertions: the three test files) and C4b
   (`bea197297`, 157 insertions: the mutation tool) — combined they would have measured 576
   insertions, over the 500-line cap. Per constraint 2 this is a declared split, not a
   departure from the block's ordered sequence in substance: both parts together carry exactly
   what the block's single C4 orders, in the same order (tests, then the tool). The golden's
   changed lines landed in C3 with the S1 code, and the catalog entry landed in C3 with its
   module, registration, exit-code row and reachability line — C3 itself measured 171
   insertions and did not need splitting, so this is the whole of the split.

2. THE MALFORMED-ID EXIT CODE. The block states, and DECISION F035 D4's booked text (applied
   verbatim from `booking.diff`, never edited) repeats: "`resolve_job_id_or_fail` answers a
   malformed id with 2" and orders a test for "exit 2 for a malformed id". MEASURED against the
   real, unmodified `apps/cli/job_id_arg.py` (a file this round does not touch and is not in its
   tracked path set): `resolve_job_id_or_fail` catches `JobIdAmbiguous` (a prefix matching TWO
   OR MORE real jobs) separately at exit 2 via `refuse_ambiguous_job_id`, but every other
   `JobIdError` — `JobIdInvalid` (a malformed shape) AND `JobIdNotFound` (a well-formed prefix
   matching no job) — falls to the same generic `except JobIdError:` branch, which calls
   `fail("invalid_job_id", ..., json_output=json_output)` with NO `exit_code` override, so it
   exits 1, `fail()`'s own default — confirmed by a direct interactive run of
   `resolve_job_id_or_fail` against five malformed/absent strings (`"../etc"`, `"a/b"`, `""`,
   65 `"x"`s, and a well-formed-but-absent 16-hex id): all five exited 1 with `invalid_job_id`,
   none exited 2. This exactly matches `job_steer_cmd.py`'s and `job_veto_cmd.py`'s own existing
   tests (`test_a_job_that_does_not_exist_exits_1`), which this block named as the pattern to
   follow. Exit 2 is reachable ONLY through a genuinely ambiguous prefix (two real jobs sharing
   one), which no malformed-shape string can ever produce. `job_ownership_cmd.py` therefore
   calls `resolve_job_id_or_fail` exactly as `job_steer_cmd.py` does, unmodified, and
   `tests/cli/test_job_ownership.py::test_a_malformed_job_id_exits_1` asserts the MEASURED
   behaviour (exit 1) rather than the block's stated one (exit 2); its docstring states the
   measurement. `exit_codes=(0, 1, 2, 3)` was kept exactly as the block specifies — 2 remains a
   legitimate member of the declared set (reachable through the real ambiguous-prefix path, and
   through the argument-parser floor every command shares) even though no test in this round
   exercises the ambiguous-prefix path specifically, since manufacturing two real jobs sharing a
   hex prefix is outside what the block's four named test scenarios ask for. This is a load-
   bearing factual point for whoever reconciles DECISION F035 D4's prose against the code; it is
   recorded here rather than by editing the booked decision text, which is a payload.

3. `apps/cli/commands/__init__.py`'s SECOND registration site — the module tuple inside
   `collect_all_handlers`'s `for mod in (...)` loop — is not itself in alphabetical order (it
   predates this round, ordered by when each command was historically added: `job_plan_cmd`,
   `job_veto_cmd`, `job_inject_cmd`, `job_rerun_cmd`, `job_steer_cmd` in that sequence, not
   alphabetical). The block orders registration "in both places, alphabetically." The import
   statement above it IS fully alphabetical, and `job_ownership_cmd` was inserted there at its
   true alphabetical point (between `job_inject_cmd` and `job_pause_cmd`). In the second,
   already-unsorted tuple, `job_ownership_cmd` was inserted immediately after its nearest true
   alphabetical predecessor already present in that tuple's later job-command cluster
   (`job_inject_cmd`, before `job_rerun_cmd`), without reordering the rest of that
   pre-existing tuple — a full re-sort of 44 existing entries would be unrelated churn outside
   this round's scope and is not something the block's tracked path set anticipates. Both
   locations register the new module; `apps/cli/commands/job_ownership_cmd` is reachable and
   collected (confirmed live by `python3 -B -m apps.cli.main job ownership --help` above, and by
   every test in `tests/cli/test_job_ownership.py` passing through the real `apps.cli.grouped`
   dispatcher).

4. `git worktree add --detach .remedy-wt/f035-r4-base 490a81f46` — one worktree beyond the one
   the block names for G5 — was created, used only to run `--collect-only -q` against the base
   commit's test selection (the block gave a PASS count for that base but no node-count
   breakdown, and G4 orders "account for the total"), and removed before G5 began; `git
   worktree list | wc -l` and the `remedy/*` branch count were confirmed unchanged (61 / 197)
   both before this worktree was added and after it was removed. No production or test file was
   read FROM it beyond that collection count; nothing in it was ever committed.

5. No test written by this round needed correction; G5 caught all eight mutations on its only
   run.

## Next

Per AGENTS.md Phase 1 rule 1 (read `.agent/STOP` from disk) and the block's ordering: the review
of round 4, then T003's second half — the chips at a task's detail, the evidence panel's
ownership tab, and the end-to-end proof. Open findings: 0. Operator questions: 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 (`.agent/STOP` check) | done | |
| Step 2 (primary checkout, branch, HEAD) | done | |
| Step 3 (block byte verification) | done | |
| Step 4 (worktree count) | done | |
| Payload verification (2 payloads) | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4a | deviated | C4 split into C4a/C4b: combined insertions (576) exceeded the 500-line cap; see Deviations 1 |
| C4b | deviated | see Deviations 1 |
| C5 (this handback) | done | |
| G1 Transport | done | |
| G2 The booking | done | |
| G3 The code | done | |
| G4 The tests | done | |
| G5 The red proofs | done | all eight mutations caught on the only run |
| G6 Tree and push | done | reported in the reply, not this file (block: "cannot go in C5") |
