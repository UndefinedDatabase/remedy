# Handoff — F287 session 2, round 8: the plan and the acceptance audit are booked; the
hardening-stage repair (R-1163) is BLOCKED, not landed — full account below

## Session

SESSION 2 of feature F287 · round 8 · rounds so far 8

Context self-assessment: "The reviewer's context is comfortable after two delegated rounds and one audit in this session."

Fortschritt: ~75 % (T001 to T003 complete · hardening stage: audit done, repair of R-1163 attempted but NOT landed this round · the repeated audit and closure still open) — Schätzung. (Deviation from the block's prescribed Fortschritt line, which asserted "repair of R-1163 landed, review pending" — it did not land; see Deviations & assumptions.)

## Range

Review of `4c24c266c`..HEAD (HEAD is C4 below, the commit that carries this handback).

## Commits

### d30d853dc F287 R8 C1: book round 7, register R-1163, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f287-r8.md` | 136/0 (new) | byte copy of this round's block |
| `.agent/live_review.md` | 4/0 | append the F287 R7 gate entry (PASS) and the R-1163 finding, exactly as prepared |
| `.agent/plan.md` | 10/8 | rewrite to round 8's current step |

### dce860ef3 F287 R8 C2: save the acceptance audit of the hardening stage

| Path | +/- | Reason |
|---|---|---|
| `.agent/f287_acceptance_audit.md` | 321/0 (new) | byte copy of the acceptance audit |

### C3 — NOT LANDED (no commit)

The block's `tests/cli/test_job_run_session_resume.py` was drafted, exercised, found to be
unmeetable exactly as specified, and deleted before this handback. No path was committed. Full
technical account in Deviations & assumptions below.

### F287 R8 C4: handback (self-reference exception — the handoff is committed by this same commit)

Measured before the handoff joined it (`git diff --cached --numstat`):

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f287-provider-session-continuity` after C4: outcome reported in the worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch`, no branch moved or deleted, no force-push, no pull, no `gh` command, no pull request, no worktree add/remove by this worker.

## Verification

0. Before any write: digests of all four reviewer-prepared files (`block.md`, `append-live_review.txt`, `dry-plan.md`, `f287_acceptance_audit.md`), computed by a worker-written Python sha256 script, all matched the prompt's sha256 lines exactly (4/4 MATCH). `HEAD` read `4c24c266c`, equal to `origin/feature/f287-provider-session-continuity`, and `git status --porcelain` was empty before any write. `git branch --show-current` read `feature/f287-provider-session-continuity` before every commit.
1. C1 copy/append/replace step (`.remedy-wt/f287-r8-worker/c1_apply.py`): `.agent/authored/f287-r8.md` read `byte_equal=True` against `block.md` (sha256 `2f031c2d0b270e5f6c0d1f0a10281060cc8fc96a98338de55acfdfcd05f7fb06` on both sides; 136 lines by both newline count and `splitlines()` — the Read tool's own cat-n display showed a trailing line number one higher, an artifact of displaying the file's final trailing newline, not an extra line). `.agent/live_review.md`'s append read `byte_equal=True`: base blob (199708 bytes, sha256 `296757593d81ed933454a5e32ce245222bedee083682e696e39460f4ccc40976`) + `append-live_review.txt`'s bytes (3794 bytes, sha256 `9988eacd89840c56f4b133c3c7cd89cb4970b4acb1954aed081048f1e9d44fae`) hashed to the same sha256 (`3310ccca0def408f02a23253993c7cddaaaeea9cb33fd52b75e838e9ef0605fd`) as the file after the append. `.agent/plan.md` read `byte_equal=True` against `dry-plan.md` (sha256 `ab717039e5eb45d62d6514293b6970d70c14cb38c2148cc2233bb703b6b4e813` on both sides). `git diff --cached --numstat` (before the C1 commit) read exactly the three paths the block names — `136 0` `.agent/authored/f287-r8.md` (new), `4 0` `.agent/live_review.md`, `10 8` `.agent/plan.md`. The full cached diff was read before committing (self-review): the plan rewrite and the append matched the prepared bytes exactly; no unrelated edit found.
2. C2 copy step (`.remedy-wt/f287-r8-worker/c2_apply.py`): `.agent/f287_acceptance_audit.md` read `byte_equal=True` against `f287_acceptance_audit.md` (sha256 `82e0c9c9392c04145fde194d160d26ca5f97cd000a5b678d756ff46ca436e79a` on both sides; 321 lines inserted). `git diff --cached --numstat` before the C2 commit read exactly the one path the block names: `321 0 .agent/f287_acceptance_audit.md`. The full cached diff was read before committing: a clean new-file insertion, no unrelated edit.
3. C3 — NOT LANDED. See Deviations & assumptions for the full technical account, including the exact exit codes and JSON observed.
4. **Gate 1** (adapted — C3 did not land, so its clause does not apply; reported honestly rather than silently skipped): `git -C /home/decodeux/Repos/remedy status --porcelain` — empty, both before any write and after the exploratory C3 draft was deleted. C1's and C2's byte proofs all `True` (above). `git show --numstat --format=` of `d30d853dc` (C1) read exactly `136 0 .agent/authored/f287-r8.md`, `4 0 .agent/live_review.md`, `10 8 .agent/plan.md`; of `dce860ef3` (C2) read exactly `321 0 .agent/f287_acceptance_audit.md`. No C3 commit exists to check. PASS for the clauses that apply.
5. **Gate 2** (adapted — the block's literal command names `tests/cli/test_job_run_session_resume.py`, which this round could not land as a passing file; run without that one path, to confirm C1/C2 disturbed nothing): `python3 -m pytest -q -rfEs tests/orchestration/test_relaunch_session_resume.py tests/cli/test_job_pause.py tests/cli/test_golden_path.py`, from the primary checkout, run once: exit 0, last line `106 passed in 61.01s (0:01:01)`; no `FAILED`, `ERROR` or `SKIPPED` line anywhere in the captured output (checked line by line). The literal block command, including the uncommitted path, was not additionally run — it would have reported only a collection error for a path that does not exist, carrying no information about C1/C2's health.
6. **Gate 3**: N/A. `tests/cli/test_job_run_session_resume.py` was not committed (see Deviations); there is no new file to ruff.
7. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0: `{"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}`; all six checks `pass`, `fail_count: 0`. `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` read `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1163']`, exactly as ordered. PASS.
8. **Gate 5** (after the push): reported in the worker's final reply (write-once rule; not known when this file is written).

## Authored-text proofs

- `block.md` → `.agent/authored/f287-r8.md`: 136 / 136 lines, sha256 `2f031c2d0b270e5f6c0d1f0a10281060cc8fc96a98338de55acfdfcd05f7fb06` / same.
- `append-live_review.txt` → `.agent/live_review.md`: append proof `True` (base blob + slice, byte for byte).
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.
- `f287_acceptance_audit.md` → `.agent/f287_acceptance_audit.md`: byte-equal, `True`.

## Deviations & assumptions

1. **C3 was not committed — this is the round's central finding, not a minor note.** The block's shared setup for both tests pins the parked run's exact argv: `job run <id> --builder-provider claude-cli --reviewer-provider claude-cli --builder-model claude-sonnet-4-6 --reviewer-model claude-sonnet-4-6 --repair-rounds 0 --json`. This persists `repair_rounds_allowed=0` onto the job's `execution_config` (`packages/orchestration/pingpong_job.py::run_job`, the "Step 4869: Resolve each config field" block, ~line 2734: `if repair_rounds is not None: ... elif ec is not None: repair_rounds = ec.repair_rounds_allowed; rr_src = "persisted"`), read back on every later relaunch of the same job that omits `--repair-rounds`.

   Test 1's prescribed relaunch (same providers, same `--repair-rounds 0`) passes cleanly: the stand-in's reviewer payload always answers verdict `"pass"` on its very first call, so one round is always enough. Verified: exit 0, `status: "completed"`, `resume_used: true`, `resume_session_ref` equal to the parked builder call's session id, `resume_declined: {}`. This test alone was written, run, and is green.

   Test 2's prescribed relaunch — `job run <id> --builder-provider fake --reviewer-provider fake --json`, **no** `--repair-rounds` — inherits the persisted `repair_rounds=0`. The CLI's provider factory (`packages/orchestration/pingpong_provider.py::create_provider`, `if name == "fake": return FakeProvider()`) builds a `FakeProvider` with every constructor default: `pass_on_round=2` (the reviewer only answers `"pass"` on its *second* call; `fail_on_round=1` is stored but never read anywhere in the class — a dead field). There is no CLI flag that can change a CLI-built `FakeProvider`'s `pass_on_round`/`fail_on_round` — the factory ignores `--builder-model` and takes no other provider-tuning flag for `"fake"`. With `repair_rounds=0`, the relaunch's `run_pingpong` allows exactly one round; the reviewer's first, and only, verdict is `"needs_repair"`; `validate_job_task_result` (`packages/orchestration/pingpong_job.py`, ~line 1995) requires `final_status == "staged_review_passed"`, which this run never reaches, so the task is blocked (`completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=needs_repair"`) and `job.state` becomes `"blocked"`, never `"completed"`.

   Measured directly, twice — once calling `run_job` directly, once through the real CLI dispatcher via `run_cli_in_process` exactly as the draft test did — with identical results: the relaunch's exit code was `0` (as the block anticipates), but its JSON `status` read `"blocked"`, not `"completed"`; `tasks[0]["final_status"]` read `"repair_exhausted"`; `tasks[0]["error"]` read `"completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=needs_repair"`; `stderr` was empty. `run show <run_id> --json` on that run correctly read `resumed_from_run_id` equal to the parked run id and `resume_declined` equal to `{"builder": "the fake provider cannot resume a session"}` — the F287 mechanism this test exists to prove DID work — but `rounds` held only one entry, never reaching a passing verdict, so `status == JOB_COMPLETED` cannot be asserted.

   The one thing that would make a CLI-built `FakeProvider` pass on round 1 — constructing it as `FakeProvider(pass_on_round=1, fail_on_round=99)`, exactly as the existing `tests/orchestration/test_relaunch_session_resume.py::TestAnOfferedSessionAProviderCannotResumeIsNamed::test_the_relaunch_names_the_role_and_reason_the_provider_declined_to_resume` already does by calling `run_job` directly — is unreachable from `remedy job run --builder-provider fake`, which only ever builds the bare default. A `--repair-rounds` override on the relaunch call would dodge the gate, but would depart from the block's literal, explicitly-parenthesized `"(no model flags, no --repair-rounds)"` invocation — a change to the test's own CLI arguments, not "within this one new file" in the sense the block means by the phrase, since it would silently stop testing the scenario the block describes (inheriting the parked run's persisted budget).

   Per the block's own instruction for exactly this situation — "If either test cannot be met without a change outside this one new file, stop and report exactly what you observed (exit codes, the JSON, stderr)" — the worker stopped. The exploratory draft (test 1 passing, test 2 failing exactly as described above) was deleted before this handback so the tree stays clean; nothing under `tests/cli/` was committed or is left on disk.

2. Gates 2 and 3 could not be run exactly as the block specifies, both naming the uncommitted file; gate 2 was run with that one path omitted (reported above, green); gate 3 is N/A. Gate 1's "C3 lists exactly its one path" clause does not apply since C3 was never committed.

3. The block's prescribed `Fortschritt` line, `Session` self-assessment aside, the `## For the operator` paragraph, and the `## Next` list are each rewritten below to state the true outcome rather than the block's assumed-successful wording, per AGENTS.md's "If Blocked" rule ("do not pretend the task is finished; clearly state what remains unfinished").

4. No new `live_review.md` finding (R-id) was minted for this discovery. Minting follows the SEARCHED-BEFORE-MINTING ritual (checklist item 30) that belongs to the review/audit side of this split workflow, not this worker's delegated commits; this handback instead carries the full technical account above so the next reviewer or planner round can decide whether a new finding is warranted, or whether the fix is simply a revised block (an explicit `--repair-rounds` value for the fake-provider relaunch, or a provider choice the CLI can actually tune to pass on round 1).

5. `.agent/plan.md`'s "Current Step" (committed in C1, before C3 was attempted, byte-identical to the block's own `dry-plan.md`) describes this round's *intended* work ("This round repairs it with a test...") rather than its outcome. It is not rewritten a second time — no second write to `plan.md` was ordered, and the handback template's write-once rule governs `.agent/handoff.md`, not `.agent/plan.md` — so the mismatch between the plan's framing and this handback's finding is noted here rather than silently left for a reader to discover.

6. No mutation red-proofs were run; no full suite was run; `-n` / `REMEDY_TEST_MAX_WORKERS` were never used; never two test commands at once (pytest was invoked exactly once, for the adapted gate 2 selection, beyond the one permitted while-writing run of the draft C3 file itself). No real `claude` process and no network call started anywhere in this round — every provider path exercised was a `FakeProvider`, or `claude-cli` with `_guarded_cli_run` patched to the existing test class's own stand-in (`TestAParkedClaudeCliTaskResumesOnRelaunch._make_stand_in`).

7. Helper scripts under `.remedy-wt/f287-r8-worker/` (gitignored, left untracked) did the digest checks, the C1/C2 copy/append/replace operations and their proofs, the exploratory C3 draft and its debugging (including its deletion), and the gate runs reported above; none of them touched any path outside `.agent/` (C1, C2) and the one now-deleted draft test file, and none touched `.remedy-wt/f287-r8/`.

8. `.agent/STOP` was not present at any point in the round.

9. No other departure.

## Round verdicts

Round 7 PASS is booked by C1 above (carried in the `append-live_review.txt` slice, re-deriving the F287 R7 gate entry). Round 8's verdict is the next session's reviewer's to give and book in that session's first commit — this handback reports C1 and C2 landed and verified, and C3 blocked with full technical evidence, for the reviewer to re-derive and decide.

## For the operator, in plain sentences

Remedy filed this round's finding and saved its audit, exactly as planned. The new test that was supposed to prove the fix works by typing the real commands — pause, then run again — could not be finished this round. Its first half, proving that Remedy resumes an interrupted conversation with the Claude command-line tool, works and was checked to pass. Its second half, proving that Remedy correctly notes when a cheaper practice service cannot continue a conversation, runs into an unrelated limit: the first half's own setup tells Remedy's practice service it may not redo its own work even once, and that practice service always needs one redo to finish by default, so the job ends "blocked" instead of "done." No working code was touched, nothing is broken, and nothing was deleted from the record; the exact reason, with the exact commands and their exact answers, is written down for whoever looks at this next, so it can be fixed by changing the test, not the product. Nothing else waits for you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handoff and stop. (Not present as of this handback.)
2. Phase 1 rule 2 (the Open PR Gate): check for open pull requests before any new branch.
3. Resolve the C3 blocker above — a revised block for the hardening-stage repair test (an explicit `--repair-rounds` value for the fake-provider relaunch that still inherits the parked run's budget meaningfully, or a provider choice the CLI can tune to pass on round 1), or an operator question, before the test is attempted again.
4. Once C3 lands: review round 8 and book its verdict in the next round's first commit (its block is `.agent/authored/f287-r8.md`).
5. Repeat the acceptance audit for the user-path proof with a fresh worker.
6. The closure sequence.

Operator questions open: 0.
Open findings: 10 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and R-1162, Low, owned by F297; R-1163, Low, owned by F287).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7, register R-1163, the plan | done | `d30d853dc` |
| C2: save the acceptance audit of the hardening stage | done | `dce860ef3` |
| C3: a relaunch through `remedy job run` resumes the parked `claude-cli` session, and names a declined resume (R-1163) | skipped | test 2's exact prescribed CLI invocation cannot reach `JOB_COMPLETED` under the exact prescribed parked-run setup (`FakeProvider`'s fixed `pass_on_round=2` vs. persisted `repair_rounds=0`); test 1 alone was verified to pass; full account in Deviations & assumptions |
| Gate 1 | deviated | C1/C2 clauses PASS; the "C3's one path" clause does not apply since C3 was not committed |
| Gate 2 | deviated | ran without the uncommitted file: `106 passed in 61.01s`, exit 0, no FAILED/ERROR/SKIPPED |
| Gate 3 | skipped | no new file to ruff (C3 not committed) |
| Gate 4 | done | integrity 6/6 pass, `fail_count: 0`; open findings list exact |
| C4 handback commit | done | this file |
| Push, gate 5 | pending | run right after this commit, reported in the worker's final reply |
