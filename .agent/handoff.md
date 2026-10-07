# Handoff — F287 session 2, round 11: the closure sequence's first round — round 10 booked,
# R-1163 resolved, the closure's self-use item (SU-046) run to its approval gate, never applied;
# review pending

## Session

SESSION 2 of feature F287 · round 11 · rounds so far 11

Context self-assessment, quoted: "The reviewer's context is still workable after five delegated
rounds and two audits in this session."

Fortschritt: ~90 % (T001 to T003 complete; the hardening stage closed; the closure's self-use run
done; the one full suite, the evidence, the package and the closing commit remain) — Schätzung.

## Range

Review of `b30b0f717`..HEAD (HEAD is C3 below, the commit that carries this handback).

## Commits

### e53fe6c26 F287 R11 C1: book round 10, resolve R-1163, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f287-r11.md` | 125/0 (new) | byte copy of `block.md` |
| `.agent/authored/f287-r11-selfuse.py` | 122/0 (new) | byte copy of `selfuse.py` (derived from `.agent/authored/f295-r23-selfuse.py`) |
| `.agent/live_review.md` | 4/0 | append `append-live_review.txt`, unchanged: books the F287 R10 gate entry (VERDICT PASS) and resolves R-1163 |
| `.agent/plan.md` | 10/10 | rewrite to round 11's current step, replaced with `dry-plan.md` |

### 1be96e720 F287 R11 C2: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry, `SU-046`, `consumed_by` empty |
| `.agent/selfuse_f287/SU-046.md` | 13/0 (new) | the job file `run_next_self_use_item` wrote |
| `.agent/selfuse_f287/changed_paths.txt` | 2/0 (new) | the job's two changed paths |
| `.agent/selfuse_f287/entry_and_job_file.txt` | 5/0 (new) | entry id/title/provenance/consumed_by and the job file path |
| `.agent/selfuse_f287/execution_config.txt` | 39/0 (new) | the `self_use` role's resolved execution config |
| `.agent/selfuse_f287/full_transcript.txt` | 14/0 (new) | job and task summary |
| `.agent/selfuse_f287/job_diff.txt` | 27/0 (new) | the job branch's diff against `HEAD`, verbatim |
| `.agent/selfuse_f287/result_state.txt` | 12/0 (new) | job state, budgets, budget actuals, task states |
| `.agent/selfuse_f287/run_defects.txt` | 1/0 (new) | `describe_self_use_run_defects()` output: `NONE` |
| `.agent/selfuse_f287/staleness_after.txt` | 2/0 (new) | the staleness catalog read from the job branch: `NONE` |
| `.agent/selfuse_f287/timing.txt` | 3/0 (new) | started/finished/wall seconds |

### F287 R11 C3: handback (self-reference exception — the handoff is committed by this same commit)

Measured before the handoff joined it (`git diff --cached --numstat`):

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f287-provider-session-continuity` after C3: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch`, no branch moved or deleted, no force-push, no pull,
  no `gh` command, no pull request, no worktree add/remove by this worker in the primary checkout.
  (The self-use script itself, reviewer-authored and run unedited, added and removed its own
  temporary worktree `.remedy-wt/f287-r11-jobtree` to read the job branch's staleness catalog —
  that is the script's own documented action, not a separate action by this worker.)

## Verification

0. Before any write: digests of all eight reviewer-prepared files (`block.md`, `selfuse.py`,
   `append-live_review.txt`, `dry-plan.md`, `launch_selfuse.py`, `wait_selfuse.py`,
   `run_selection.py`, `selection.txt`), computed by a worker-written Python sha256 script, all
   matched the prompt's sha256 lines exactly (8/8 OK). `HEAD` read `b30b0f717`, equal to
   `origin/feature/f287-provider-session-continuity`, and `git status --porcelain` was empty before
   any write. `git branch --show-current` read `feature/f287-provider-session-continuity` before
   every commit.
1. C1 copy/append/replace step (`.remedy-wt/f287-r11-worker/c1_apply.py`): `.agent/authored/f287-r11.md`
   read `block_equal=True` against `block.md` (sha256
   `b7337c11c97030498970d49dbd69656e388c8720bae3ac96bb3bdfb875835cd9` on both sides; 125 lines).
   `.agent/authored/f287-r11-selfuse.py` read `selfuse_equal=True` against `selfuse.py` (sha256
   `1d0297e88f5ef589c25560455827e7847ebb1773e3a1860977fd8d1879038b95` on both sides; 122 lines).
   `.agent/live_review.md`'s append read `append_byte_equal=True`: base blob (207501 bytes, sha256
   `0b6a52389056543533a17292e5f5c1ea90f9edb0259f9a1bdcf79c64a0c3c3a8`) + `append-live_review.txt`'s
   bytes (2054 bytes, sha256 `8dbde55b93be8e1e7704367fa0f8b500b8e697c6ec1cd47b324f79f52be7f632`)
   hashed to `f555c7a9c2503ccf7542f9d38745e2a648fe464e470dfb3cbb37c54ff3c06c12`, equal to the file
   after the append. `.agent/plan.md` read `plan_equal=True` against `dry-plan.md` (sha256
   `588c1df779bffc7c4153928024757b6046d21e69f6a64b4b15748f4243e16f9c` on both sides; 27 lines).
   `git status --porcelain` and `git diff --stat` before staging matched expectation exactly (only
   `.agent/live_review.md` and `.agent/plan.md` modified, the two new `authored/` files untracked).
   `git diff --cached --numstat` (before the C1 commit) read exactly the four paths the block
   names: `122 0 .agent/authored/f287-r11-selfuse.py`, `125 0 .agent/authored/f287-r11.md`,
   `4 0 .agent/live_review.md`, `10 10 .agent/plan.md`. The full cached diff was read before
   committing (self-review): the append booked round 10's PASS and R-1163's resolution exactly as
   prepared, and the plan rewrite matched round 11's current step; no unrelated edit found.
2. C2 self-use run: launched once via
   `python3 /home/decodeux/Repos/remedy/.remedy-wt/f287-r11/launch_selfuse.py /home/decodeux/Repos/remedy /home/decodeux/Repos/remedy/.remedy-wt/f287-r11-worker`
   (printed `started, wrapper pid 484980 log .../selfuse.log`), then waited with
   `python3 /home/decodeux/Repos/remedy/.remedy-wt/f287-r11/wait_selfuse.py /home/decodeux/Repos/remedy/.remedy-wt/f287-r11-worker 50`,
   which ended on the first call with **exit 0**. Full captured output (the script's own prints,
   verbatim):

   ```
   generate_and_append_if_empty(): ('SU-046', 'Narrow the excused handler at apps/cli/commands/do_cmd.py:184', 'generated (self-use-generator tier 4, excused handler, apps/cli/commands/do_cmd.py:1:except Exception:  # noqa: BLE001 — never pushes based on a config value it cannot read)')
   next_self_use_item(): SU-046 Narrow the excused handler at apps/cli/commands/do_cmd.py:184 generated (self-use-generator tier 4, excused handler, apps/cli/commands/do_cmd.py:1:except Exception:  # noqa: BLE001 — never pushes based on a config value it cannot read)
   === SU-046.md ===
   # Job: Narrow the excused handler at apps/cli/commands/do_cmd.py:184

   ## Task 1
   Line 184 of `apps/cli/commands/do_cmd.py` excuses a blind exception handler from ruff's BLE001 rule:

       except Exception:  # noqa: BLE001 — never pushes based on a config value it cannot read

   Narrow this handler to the exception types the code it guards can really raise, and delete its `# noqa: BLE001` mark. In the same change lower `MAX_EXCUSED` in `tests/test_ble001_ratchet.py` by one, because that test holds the number of marks equal to it. Add no mark anywhere else, and do not edit any file under `.agent/`.

   Acceptance:
   - The handler at line 184 of `apps/cli/commands/do_cmd.py` no longer carries a `# noqa: BLE001` mark, and `python3 -m ruff check apps/cli/commands/do_cmd.py` reports nothing.
   - `python3 -m pytest -q tests/test_ble001_ratchet.py` passes, with `MAX_EXCUSED` one lower than before.
   - No file under `.agent/` is changed by this task.

   === changed_paths.txt ===
   apps/cli/commands/do_cmd.py
   tests/test_ble001_ratchet.py

   === entry_and_job_file.txt ===
   Entry ID: SU-046
   Entry Title: Narrow the excused handler at apps/cli/commands/do_cmd.py:184
   Entry Provenance: generated (self-use-generator tier 4, excused handler, apps/cli/commands/do_cmd.py:1:except Exception:  # noqa: BLE001 — never pushes based on a config value it cannot read)
   Entry Consumed By:
   Job File Path: /home/decodeux/Repos/remedy/.remedy-wt/f287-r11-selfuse/SU-046.md

   === execution_config.txt ===
   { "builder": "claude-cli", "builder_effort": "medium", "builder_model": "claude-sonnet-4-6",
     "reviewer": "claude-cli", "reviewer_effort": "medium", "reviewer_model": "claude-sonnet-4-6",
     "max_tasks": 1, "repair_rounds_allowed": 2, "timeout_sec": 600, ... (full JSON in the committed
     file) }

   === full_transcript.txt ===
   Job ID: a4cfeca74efa42d8
   Job State: completed
   Task T001: Status applied_to_job_workspace, Reviewer Verdict pass, Final Status staged_review_passed

   === job_diff.txt ===
   (see "Self-use run" section below — quoted there VERBATIM in full)

   === result_state.txt ===
   Job ID: a4cfeca74efa42d8
   Job State: completed
   Budgets: max_cost_usd=6.0, max_provider_calls=8
   Budget Actuals: measured_cost_usd=0.6613442999999999, provider_call_count=2, total_tokens=7367
   Task T001: applied_to_job_workspace (verdict: pass; final_status: staged_review_passed; repair_rounds_used: 0)

   === run_defects.txt ===
   NONE

   === staleness_after.txt ===
   Read from: the job branch remedy/job-a4cfeca74efa42d8
   NONE

   === timing.txt ===
   Started: 2026-10-07T12:00:19.267549+00:00
   Finished: 2026-10-07T12:02:20.330325+00:00
   Wall seconds: 121.1
   ```

   (The transcript above is trimmed per the handback template's "keep transcripts trimmed" rule
   where a file's content is reproduced verbatim elsewhere in this handback — `job_diff.txt` and
   `run_defects.txt` are quoted in full, unabridged, in the Self-use run section below; every other
   file's content is quoted in full above, nothing omitted except the execution-config JSON's
   remaining key/value pairs, all of which are recorded in the committed file and in the Self-use
   run section.)
   After the run: `git status --porcelain` showed exactly `M scripts/self_use_queue.json` and
   `?? .agent/selfuse_f287/`, matching the block's constraint. `git diff scripts/self_use_queue.json`
   showed exactly one appended entry, id `SU-046`, `"consumed_by": ""`. All ten files under
   `.agent/selfuse_f287/` were present and non-empty (sizes in Gate 2 below). `git diff --cached
   --numstat` before the C2 commit read exactly the eleven paths the block names (table above).
3. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty (after C2). C1's
   byte proofs re-verified against the COMMITTED blobs (`.remedy-wt/f287-r11-worker/gate1_verify.py`,
   reading `git show HEAD:<path>` and `git show b30b0f717:.agent/live_review.md` for the append's
   base): `block.md` → `HEAD:.agent/authored/f287-r11.md` equal=True (sha
   `b7337c11c97030498970d49dbd69656e388c8720bae3ac96bb3bdfb875835cd9` both sides); `selfuse.py` →
   `HEAD:.agent/authored/f287-r11-selfuse.py` equal=True (sha
   `1d0297e88f5ef589c25560455827e7847ebb1773e3a1860977fd8d1879038b95` both sides); live_review append
   equal=True (sha `f555c7a9c2503ccf7542f9d38745e2a648fe464e470dfb3cbb37c54ff3c06c12` both sides);
   `dry-plan.md` → `HEAD:.agent/plan.md` equal=True (sha
   `588c1df779bffc7c4153928024757b6046d21e69f6a64b4b15748f4243e16f9c` both sides). All four `True`.
   PASS.
4. **Gate 2**: the ten files under `.agent/selfuse_f287/`, each non-empty, byte sizes (`ls -la`):
   `SU-046.md` 945, `changed_paths.txt` 57, `entry_and_job_file.txt` 387, `execution_config.txt`
   1203, `full_transcript.txt` 1419, `job_diff.txt` 1295, `result_state.txt` 809, `run_defects.txt`
   5, `staleness_after.txt` 59, `timing.txt` 105. All ten present and non-empty. PASS.
5. **Gate 3**: `python3 /home/decodeux/Repos/remedy/.remedy-wt/f287-r11/run_selection.py
   /home/decodeux/Repos/remedy` — **exit 0**. No `FAILED` or `ERROR` line; no `process(es) behind`
   line. Every `SKIPPED` line as printed:
   ```
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   Summary: `3754 passed, 3 skipped in 25.99s`. The selection held the canary
   `tests/cli/test_golden_path.py` (named in `selection.txt`). PASS.
6. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0:
   `{"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status":
   "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
   {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
   {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
   {"message": "no reviewer scratch, evidence dir or archive at the root", "name":
   "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name":
   "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
   "schema_version": 1, "version": 1}`; all six checks `pass`, `fail_count: 0`. `python3 -c "import
   scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   read `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162']`, exactly as the block orders. PASS.
7. **Gate 5** (after the push): reported in the worker's final reply (write-once rule; not known
   when this file is written).

## Authored-text proofs

- `block.md` → `.agent/authored/f287-r11.md`: 125 / 125 lines, sha256
  `b7337c11c97030498970d49dbd69656e388c8720bae3ac96bb3bdfb875835cd9` / same.
- `selfuse.py` → `.agent/authored/f287-r11-selfuse.py`: 122 / 122 lines, sha256
  `1d0297e88f5ef589c25560455827e7847ebb1773e3a1860977fd8d1879038b95` / same.
- `append-live_review.txt` → `.agent/live_review.md`: append proof `True` (base blob + slice, byte
  for byte).
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.

## Self-use run

- **Entry id**: `SU-046`. **Title**: "Narrow the excused handler at
  apps/cli/commands/do_cmd.py:184". **Provenance**: generated (self-use-generator tier 4, excused
  handler, `apps/cli/commands/do_cmd.py:1:except Exception:  # noqa: BLE001 — never pushes based on
  a config value it cannot read`).
- **Job id**: `a4cfeca74efa42d8`.
- **Builder and reviewer provider and model** (from `execution_config.txt`): builder
  `claude-cli` / model `claude-sonnet-4-6` / effort `medium`; reviewer `claude-cli` / model
  `claude-sonnet-4-6` / effort `medium` — the `self_use` role's own configured frontier provider,
  not the local model.
- **Job state and stop reason** (from `result_state.txt`): Job State `completed`; Stop Reason
  (empty); Stop Source (empty); Error (empty); Run Manifest Error (empty).
- **Each task's status and reviewer verdict** (from `result_state.txt`): `T001: applied_to_job_workspace
  (verdict: pass; final_status: staged_review_passed; repair_rounds_used: 0; run_id:
  fa8f14d9fcbb451e)`.
- **Wall seconds** (from `timing.txt`): `121.1`.
- **Paths** (from `changed_paths.txt`): `apps/cli/commands/do_cmd.py`,
  `tests/test_ble001_ratchet.py`.
- **Job diff** (from `job_diff.txt`, VERBATIM):

  ```
  $ git diff HEAD...remedy/job-a4cfeca74efa42d8  (exit 0)
  diff --git a/apps/cli/commands/do_cmd.py b/apps/cli/commands/do_cmd.py
  index 1a5841cf4..425af31f1 100644
  --- a/apps/cli/commands/do_cmd.py
  +++ b/apps/cli/commands/do_cmd.py
  @@ -181,7 +181,7 @@ def _resolve_do_commit_flags(
           top = None                     # not a repository: the init step fails and says so
       try:
           key = push_after_mission_enabled(load_config(Path(top or repo) / "remedy.toml"))
  -    except Exception:  # noqa: BLE001 — never pushes based on a config value it cannot read
  +    except ValueError:
           key = False                    # Remedy never pushes on a value it cannot read
       source = "--push" if push else ("apply.push_after_mission" if key and mode else "")
       if key and not mode:
  diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
  index ff1f68ae3..cb21e641a 100644
  --- a/tests/test_ble001_ratchet.py
  +++ b/tests/test_ble001_ratchet.py
  @@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")

   #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
   #: commit that removes a mark lowers this number in the same commit, and it is never raised.
  -MAX_EXCUSED = 285
  +MAX_EXCUSED = 284


   def _marks() -> list[tuple[str, int, str]]:
  ```

- **run_defects.txt** (VERBATIM): `NONE`
- No finding is registered by this worker for this run: `describe_self_use_run_defects()` returned
  an empty tuple (rendered as `NONE` above), which per
  `docs/roadmap/STATUS_closure_protocol.md` precondition 6 means nothing to register, not that
  nothing was checked.

## Deviations & assumptions

1. None from the block's ordered commit sequence — C1 and C2 landed exactly as ordered, in order,
   with no extra commit and none dropped; this C3 is the handback the block orders next.
2. Helper scripts under `.remedy-wt/f287-r11-worker/` (gitignored, left untracked) did the digest
   checks, the HEAD/branch checks, the C1 copy/append/replace operations and their proofs, and the
   gate-1 re-verification of C1's byte proofs against the committed blobs; none touched any path
   outside the one named per commit, and none touched `.remedy-wt/f287-r11/`.
3. The self-use script (`.agent/authored/f287-r11-selfuse.py`, itself a byte copy of the
   reviewer's `selfuse.py`) was run exactly once, only through `launch_selfuse.py` then
   `wait_selfuse.py`; it was never edited and never re-run. It exited 0 on the first `wait_selfuse.py`
   call (no `running` poll was needed).
4. Gate 3's selection (`run_selection.py`) was run exactly once this round, directly as the
   reviewer prepared it (not edited); no mutation red-proofs were run; no full suite was run; the
   `REMEDY_TEST_MAX_WORKERS` environment variable was never set; never two test commands at once.
   Note: `run_selection.py` itself invokes pytest with `-n auto` (pytest-xdist's own worker-count
   flag), which is distinct from the `REMEDY_TEST_MAX_WORKERS` variable the constraint names — this
   worker set no such variable and ran the reviewer's helper unedited, exactly once.
5. `.agent/STOP` was not present at any point in the round.
6. Real money was spent by the self-use run, exactly as this round's budgeted, expected item:
   measured cost `$0.6613442999999999` against a `max_cost_usd` budget of `$6.00`, and
   `provider_call_count=2` against a `max_provider_calls` budget of `8`. This is the closure
   precondition's expected spend, not a deviation.
7. No other departure.

## Round verdicts

Round 10 PASS and R-1163 resolved, booked by C1 (the F287 R10 gate entry and the R-1163
`Done:` paragraph appended to `.agent/live_review.md` exactly as `append-live_review.txt` prepared
it, byte proof `True` above). Round 11's verdict is the next session's reviewer's to give and book
in that session's first commit, together with the registration of any self-use run defect (none
found this round).

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, to show it
is used on itself. This time the work was to narrow one place in its own command-line code that
catches every kind of error. The run stops before anything is applied; its record is saved for the
next round to read. The run cost about sixty-six cents. It ended successfully: the model's proposed
fix passed its own reviewer's check and sits staged on the job's own branch, untouched by this
round. Nothing waits for you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop. (Not present as of this handback.)
2. Phase 1 rule 2 (the Open PR Gate): no pull request is open for this branch yet.
3. The reviewer reviews round 11, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The integration-gate round: the one full suite.
5. The evidence bundle, the review package, the rotation, the STATUS line and the pull request.

Operator questions open: 0.
Open findings: 9 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and
R-1162, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 10, resolve R-1163, the plan, save the block and the self-use script | done | `e53fe6c26` |
| C2: the closure's self-use item run to its approval gate, never applied | done | `1be96e720` |
| C3: handback | done | this file |
| Gate 1 | done | tree clean after C2, C1 byte proofs all `True` re-verified against committed blobs |
| Gate 2 | done | 10 files under `.agent/selfuse_f287/`, each non-empty (sizes recorded above) |
| Gate 3 | done | exit 0, no FAILED/ERROR/`process(es) behind`, `3754 passed, 3 skipped in 25.99s` |
| Gate 4 | done | integrity 6/6 pass, `fail_count: 0`; open findings list exact |
| Push, gate 5 | pending | run right after this commit, reported in the worker's final reply |
