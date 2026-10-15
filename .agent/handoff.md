# Handback — amend1014c: review closure of the `remedy do` golden path (repairs R1 to R4), replacement history

## Session

Operator amendment amend1014c (2026-10-15). Old: branch `feature/do-golden-path`, pull request #339 (closed
by this session, branch preserved, not merged), tip `fb3374b5da9d7055b0f9d87b1138d1b117fcff99`, tree
`5f8642be8f5375336902a8a6b4e1612cda8621b7` (issued at `6eb04551eb1b0bd79556e59ac7b64b323b75063b`, tree
`88eba00789562d5d8c0602294d2821c59babe34f`). New: branch `feature/do-golden-path-review-closure`, from
`main` `e688b30f3735834f66294afcdd0f9292c03d62ae`; its replayed tip tree is **byte-identical** to the old tip
tree above (`git diff` between them is empty); this file's commit is the only state-only commit after it.
The replacement pull request is open and non-draft; it is not merged and must not be merged without review.
`.agent/STOP` (untracked) and the F078 branch were not touched. Python 3.10.12, Pi 1.2.0, model `muse-glimmer:latest`.
The PR channels of #339 were empty (issue comments, review comments, reviews: 0 each).

## Result, plainly

R1 to R3 are repaired and proven; R4 is repaired by replay. No finding is left open except the limits under Deviations.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| R1 secrets in the baseline | done | only the job's deliverable paths are seeded; one name-only classifier (`sensitive_paths.py`) shared by apply, the context pack, the baseline and the target snapshot; a sensitive target is refused before any worktree or provider call |
| R2 Pi timeout floor | done | `PI_MIN_WALL_SECONDS` deleted; the 900 s Pi default lives in the timeout resolution and applies only when none was set; explicit value, remaining wall budget and deadline are ceilings; provenance in the call record |
| R3 call accounting | done | fallback path: the ledger keys rows by provider attempt and feeds budgets, so rows were not expanded; the count is `harness_invocations` on do, digest, cockpit, contract and UI, and `model_turns` is read from Pi's own call records |
| R4 643-insertion commit | done | B5 replayed as B5a (401) and B5b (242); every commit below is at most 500 |
| Tests 1, 2 | done | `test_dirty_baseline_secrets.py` (`.env`, `.env.local`, `.pem`, `.key`, `credentials.json`: not in the workspace, not in any Git object, target bytes and status unchanged) |
| Test 3 | done | same file: dirty unrelated `notes.txt` is HEAD's bytes in the workspace, byte-identical, uncommitted after `--commit-auto`, named without content |
| Test 4 | done | same file: dirty `README.md` seeded byte-exactly, diff is only the builder's delta |
| Test 5 | done | same file: `.env` and `keys/server.pem` targets refuse before `W.create` and any provider call; `test_the_order_guard_refuses_a_sensitive_target_by_name_alone` |
| Test 6 | done | same file: an ignored sensitive-shaped file stays untouched; the classifier does not read `.gitignore` |
| Test 7 | done | `test_dirty_baseline.py` (conflict, nested repository, count), `..._secrets.py` (traversal in the seed destination, sensitive file never opened); symlink and mode representation kept; a special file cannot appear in `git status`, so no fifo test |
| Tests 8 to 12 | done | `test_pi_timeouts.py`: 1 s kill with no monkeypatch and a gone process, default 900, wall-budget cap, nearer deadline wins, evidence and bounded error, the job clock bound by `run_job` |
| Tests 13 to 17 | done | `test_pi_turn_counts.py`: 3 turns and summed usage and one invocation, retry stream, zero-turn failure, do summary text and JSON, digest and cockpit |
| Test 18 | done | acceptance A to D below, each compared with a tee of Pi's own JSONL |
| Tests 19 to 24 | done | existing and updated, green in the full suite: `test_do_pi_default.py` (back-to-back, one JSON document, raw Ollama refusal), `test_dirty_baseline.py` (concurrent mutation), `test_pi_provider.py` (reviewer tools and resource switches, empty diff outvotes a pass), `test_role_override_flags.py` |
| Acceptance A to E | done | table below |
| Replacement steps 1 to 9 | done | source tip and tree recorded; #339 closed with the comment; gate re-run (no open PR); `main` fast-forwarded; branch created; replay without rebase, reset, amend or force-push (no conflicts); trees equal; insertion counts below |
| Replacement steps 10, 11 | done | the branch is pushed normally and one non-draft PR into `main` is opened right after this commit (its number is in the PR, not in this file); #339 stays closed, not deleted |

## Real acceptance (real Pi 1.2.0, real `muse-glimmer:latest`, fresh fixtures, isolated data roots, `python3 -m apps.cli.grouped`)

| | Result |
|---|---|
| A `do "<order>" --repo .` | one job, one task, planning calls 0, cockpit before the run (ui step 0.5 s), run 56.4 s; real `result.diff` (one added paragraph); target unchanged and clean; printed `builder 1 harness invocation, 9 model turns` and `reviewer 1 harness invocation, 2 model turns` (Pi call records: 9 and 2) |
| B `--apply` | exit 0, only `README.md` modified, no commit, `git stash list` empty; printed 10 and 2 turns, tee of Pi's stdout counted 10 and 2 assistant `message_end` events |
| C `--commit-auto` straight after B | exit 0, tree clean, one new commit touching only `README.md`, no stash, report says README.md already held the uncommitted edits; printed 8 and 4 turns, tee counted 8 and 4 |
| D adversarial dirty files | exit 0; untracked `.env`, untracked `server.key`, dirty tracked `notes.txt` byte-identical (sha256 before and after); only `README.md` committed; status still lists the three; no stash; seeded entries `[]`, preserved `.env` (environment file), `notes.txt`, `server.key` (private key); printed 12 and 2 turns, tee counted 12 and 2 |
| E fake Pi, explicit timeout | `PiProvider.build(timeout_sec=3)` returned after 3.0 s with `pi_timeout`; parent and child (same process group) both gone; no `PI_MIN_WALL_SECONDS` exists; with the default 900 s and a 4 s job deadline it returned after 4.0 s, record `bound_by: deadline`. The Ollama and Pi preflight was stubbed because the fake has no model behind it |

Boolean secret checks of D (marker and note sentence never printed): marker in the Pi workspace at either
invocation: absent; marker in any Git object of the target repository (all branches and refs, unreachable
objects too): no; marker in any ref tree: no (ref trees hold only `README.md` and `notes.txt` at HEAD's bytes);
marker in the data root (evidence, prompts, diffs): no; marker in Pi's stdout stream: no. The dirty `notes.txt`
sentence: absent from the Pi workspace, the data root and Pi's stream; **present as a blob in the target's object
database** under `refs/remedy/checkpoints/<job>/target-last-known` (see Deviations).

## Verification

- Focused (through `scripts/remedy_pytest.sh`): dirty baseline, secrets, sensitive paths, Pi provider, events,
  timeouts, turn counts, digest, cockpit, interface, structure ratchet, import reachability, dashboard contract.
- `scripts/remedy_test_fast.sh`: `128 passed` (at the tip before the last test-only commits).
- UI: `npx vitest run` on the three changed API test files `48 passed`; `npx tsc --noEmit` clean.
- Ruff: `ruff check packages apps tests` clean. Structure ratchet: no row rose; three file rows and the pin were
  lowered (`pingpong_loop.py`, `job_apply.py`, `pingpong_job.py`; pin 73588 to 73584).
- Final full suite, once, `scripts/remedy_pytest.sh tests -q -n auto -rfE --durations=8` on tree
  `b5e63d1c47308b2f5cea42a1bde63a4ef0e8e69e` (commit `3d676219de67a9da3561409af8891ed46c06b032`): `2 failed, 23199 passed,
  22 skipped`. Both failures were the dashboard contract's wording checks on `.agent/context.md`; commit `fb3374b5d`
  changed that one state file (5 insertions, 1 deletion) and `tests/ui_server/test_dashboard_contract.py` then passed
  (`64 passed`). The replayed tip tree `5f8642be8f5375336902a8a6b4e1612cda8621b7` differs from the gated tree by
  that state-only delta; no product, test or docs byte differs. `doctor health --json` exits 0.
- Review: `remedy-review` is not an installed skill here (the listing has `review-remedy`, which reads the planner
  prompt); a self-review of every diff and a check of `.pi`, `.claude`, `.mcp.json` (`mcpServers` empty),
  `.vscode/mcp.json` (`servers` empty) ran instead: none changed on this branch.

## Commits from main to the replayed tip (insertions, plus column of `git show --numstat`)

| Commit | Insertions | Subject |
|---|---|---|
| `7643ba83a` | 177 | amend1014 C1: fold inspection verbs and merge the tasks of one file into one (D2) |
| `23bbf3712` | 19 | amend1014 C2: two scope rules in the mission prompt (D6) |
| `6360b99cc` | 160 | amend1014 C3: --yes of do becomes --run-unattended, and a full plan keeps its approval (D3 |
| `15269b9dc` | 373 | amend1014 C4: a bounded one-deliverable order walks a lane with no planning call, and a pl |
| `57ecf678c` | 377 | amend1014 C5: say what the walk is doing, and open the cockpit before the run (D4, D5) |
| `7791f0e21` | 474 | amend1014 C6: end-to-end tests of the remedy do golden path |
| `23e93bae8` | 81 | amend1014 C7: document the two lanes, the progress lines and the plan plus state files |
| `e287776e2` | 11 | amend1014 C8: the heartbeat claims only what it knows; the plan line is honest under no-ll |
| `5b4a75191` | 51 | amend1014 C9: repair the eight failures the closure gate found |
| `e619edf25` | 8 | amend1014 C10: declare the task-plan prompt's content change in its golden |
| `e78824361` | 115 | amend1014 S1: handback with the real acceptance run and the closure gate |
| `1e3ef84cb` | 415 | amend1014b B1: a dirty working tree is the captured baseline of a job |
| `24cdf7ce5` | 183 | amend1014b B2: Pi becomes the default builder, reviewer and repair provider |
| `b36963203` | 461 | amend1014b B3: the Pi provider runs the harness in the job workspace |
| `6e9c6dbae` | 24 | amend1014b B4: a reviewer pass on an empty diff is rejected before completion |
| `64bb72418` | 401 | amend1014b B5a: tests for the Pi event stream and the Pi provider |
| `b12adf0f0` | 242 | amend1014b B5b: tests for the dirty baseline |
| `7f65344d8` | 251 | amend1014b B6: name the Pi chain in progress, report preserved dirt, document the default |
| `23d4c676f` | 388 | amend1014b B7: keep the structure ratchet, the registries and the suite green |
| `0fe486552` | 4 | amend1014b B8: read the dirty start from the job record in its tests |
| `66966b2e9` | 25 | amend1014b B9: do names target_changed_during_run and the changed paths when the apply sto |
| `fa4da89ce` | 1 | amend1014b B10: the sequence test reads the new target_changed_during_run sentence |
| `16b796ad5` | 79 | amend1014b S1: handback with the real acceptance A to E and the closure gate |
| `5588021be` | 137 | amend1014c R1a: one sensitive-path classifier; the target snapshot hashes no secret |
| `7acc6b862` | 316 | amend1014c R1b: seed only the job's deliverables; every other dirty path is named, never r |
| `f65634849` | 192 | amend1014c R2: an explicit Pi timeout and the job's remaining budget are ceilings |
| `4b5eafbed` | 180 | amend1014c R3a: do reports harness invocations and model turns as two measured counts |
| `83a4e3966` | 114 | amend1014c R3b: digest, cockpit, contract and UI name harness invocations and model turns |
| `9c90d27ce` | 43 | amend1014c D1: document the baseline scope, timeout ceilings and the two counts |
| `66048f0bd` | 17 | amend1014c D2: state the snapshot limit in the guide; pin the job clock binding in a test |
| `ec9982c40` | 5 | amend1014c S0: keep the context state file inside the dashboard contract's wording |

The state-only commit that carries this file is far below 500 insertions.

## Deviations and remaining limits

- An ordinary unrelated dirty file (the `notes.txt` case) is still hashed into the target repository's object
  database by the pre-existing human-change snapshot (F263) under a Remedy checkpoint ref. It is on no job branch,
  in no workspace and in no evidence, and Pi's tools share the repository's object database, so a determined agent
  could read it by hash. Sensitive names are excluded from that snapshot. Removing the rest means redesigning that
  snapshot, which is outside this repair; it is the one thing I would ask the operator to decide.
- `remedy cost` and `remedy stats` keep their ledger-level `calls` columns; they report ledger rows, which are
  harness invocations. The renamed surfaces are do, the status digest, the mission cockpit, the contract and the UI.
- An order that merely mentions a sensitive path (to forbid touching it) is refused, since a name in prose cannot be
  told from a target.
- Acceptance A had no independent tee of Pi's stream (the tap was added for B to D); A is compared with the Pi call
  records only. Test 18 is therefore proven by B, C and D.
- The Pi job-clock binding is per thread (a context variable set when `run_job` claims the workspace); `run_job` runs
  provider calls on that thread.
- Older cockpit processes from the previous session's probes (data roots `dataAccB`, `dataAccD`) were left running.

## Next expected operator action

Review the replacement pull request. Do not merge it automatically. F078 resumes on its own branch after a merge decision.
