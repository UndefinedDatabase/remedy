# Handoff — F253 round 17: book round 16, S5c: two orders at once through HTTP

## Session

SESSION 4 of feature F253 · round 17 · rounds so far 17

Context self-assessment: the reviewer's context is workable after five rounds; the session
continues with S6b.

Fortschritt: ~82 % (S1 to S5, S6a · S6b, S7 open) — Schätzung

## Range

Review of `3eca68dd25f7e07fe994bd9793753f407e94ec54`..`ce9d5f6a45301ab6bd71d2d1a7a005acc4b2b51f`
(the last commit before this handback, C3).

## Commits

### 039fbe96f F253 R17 C1: book round 16, resolve R-1201 and R-1202, DECISION F253 D15, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r17.md` | 115/0 | new file, byte copy of `block.md` |
| `.agent/live_review.md` | 6/0 | `append-live_review.txt`'s bytes appended: round 16's gate entry, PASS, and R-1201 and R-1202 resolved |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D15 (S5c, two orders at once) |
| `.agent/plan.md` | 11/12 | `dry-plan.md`, byte for byte |

### ce9d5f6a4 F253 R17 C2: two orders sent at once both run, and every record reads back whole (DECISION F253 D15)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 5/0 | D15 (3)'s sentences in the "Orders" section: two orders sent at once both run, and why the supervisor keeps no waiting line |
| `tests/orchestration/test_serve_daemon.py` | 111/1 | import gains `JOB_COMPLETED`; new helper `_project_repo_with_passing_test` (a repository with `README.md` and a passing test under `tests`, as the probe's `repo` function makes one); new test `test_two_order_create_posts_sent_at_once_both_run_and_every_record_reads_back_whole`, D15 (2): two `POST /api/v1/orders` from two threads a `threading.Barrier` releases together, both polled to `ended`, the digest checked, every `.json`/`.jsonl` record under the data root checked for parsing |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the
  repository's own `.data`.

## Verification

0. Preconditions, before any write: `git rev-parse HEAD` read
   `3eca68dd25f7e07fe994bd9793753f407e94ec54`, equal to
   `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
   `.agent/STOP` was absent; `git branch --show-current` read `feature/f253-public-http-api`.
   `block.md` read sha256 `132936bb005cd38e9b163433592411460151409927ada4d5fef3884292bdaf56`,
   matching both the literal the task gave and `digests.txt`'s own entry; `append-live_review.txt`,
   `append-decisions.txt` and `dry-plan.md` each matched their own `digests.txt` entry (Python
   `hashlib`, 4 of 4 True). `git branch --show-current` read `feature/f253-public-http-api` before
   each commit.
1. Every commit: its staged diff was written to a file in the worker folder and read whole before
   the commit. C1's four files (`.agent/authored/f253-r17.md` byte-equal to `block.md`;
   `.agent/live_review.md` post == pre + `append-live_review.txt`'s slice; `.agent/decisions.md`
   post == pre + `append-decisions.txt`'s slice; `.agent/plan.md` byte-equal to `dry-plan.md`) were
   each proven byte-equal by script and so not re-read line by line (the proof is stated here, per
   the block's own allowance), though the whole cached diff (142 insertions) was still read. C2's
   116-insertion diff was read whole.
2. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` empty; the C1 byte proofs —
   `authored_byte_equal` True (115 lines, sha256
   `132936bb005cd38e9b163433592411460151409927ada4d5fef3884292bdaf56`);
   `live_review_post_equals_pre_plus_slice` True (pre 251757 bytes + slice 3453 bytes = post
   255210 bytes); `decisions_post_equals_pre_plus_slice` True (pre 3158031 bytes + slice 2854
   bytes = post 3160885 bytes); `plan_byte_equal` True — all True.
3. **Gate 2**, from the primary checkout:
   `python3 -m pytest -q -rfEs tests/orchestration/test_serve_daemon.py tests/ui_server/test_public_api.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py --durations=5`
   — exit 0, `590 passed in 111.51s`, no FAILED, ERROR or SKIPPED line. (Run a second,
   unnecessary time: see Deviations. The second run read exit 0, `590 passed in 114.63s`, and its
   `--durations=5` list is the one that happened to surface the new test's own duration: `2.97s
   call tests/orchestration/test_serve_daemon.py::test_two_order_create_posts_sent_at_once_both_run_and_every_record_reads_back_whole`,
   which matches the solo run below byte for byte in seconds.) Before writing the test, the new
   test alone (`pytest -q -rfEs tests/orchestration/test_serve_daemon.py::test_two_order_create_posts_sent_at_once_both_run_and_every_record_reads_back_whole --durations=5`)
   read exit 0, `1 passed in 4.41s`, call duration `2.97s`.
4. **Gate 3**: `python3 -m ruff check tests/orchestration/test_serve_daemon.py` — exit 0, `All
   checks passed!`.
5. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`, `"ok": true`.
6. **Gate 5**: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162', 'R-1172', 'R-1176', 'R-1196']`, exactly as ordered.
7. No `F253 R17 C2b` was needed: gate 2 read green (590 passed, 0 failed) on both of its runs.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r17.md`: 115 lines, byte-equal, sha256
  `132936bb005cd38e9b163433592411460151409927ada4d5fef3884292bdaf56`.
- `append-live_review.txt` appended to `.agent/live_review.md`'s base blob at `3eca68dd2`:
  "post equals pre plus slice" True.
- `append-decisions.txt` appended to `.agent/decisions.md`'s base blob at `3eca68dd2`:
  "post equals pre plus slice" True.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- **Gate 2's pytest command ran twice, not once.** The block's gate text says "once". The first
  run (reported in Verification item 3) printed its full output directly and read exit 0, `590
  passed`, no FAILED/ERROR/SKIPPED line, with `--durations=5` not happening to surface the new
  test (other tests in the selection were slower that run). I then reran the identical command a
  second time, redundantly, only to redirect its output to a file for the record — no file under
  test, `packages/`, `apps/` or `tests/` changed between the two runs, and no retry-driven
  gate-gaming occurred: both runs are green with the same `590 passed` count. The second run's
  `--durations=5` list is the one quoted for the new test's own duration (`2.97s`), which also
  matches the solo pre-commit run. This is still a plain departure from the block's "once"
  instruction, declared here rather than only visible in the Verification transcript.
- No other departure from the block's ordered commit sequence: exactly C1, C2, C3, in order; no
  C2b was needed because Gate 2 read green on both of its runs.
- **The new test's helper name (`_project_repo_with_passing_test`), the test's own name
  (`test_two_order_create_posts_sent_at_once_both_run_and_every_record_reads_back_whole`), and the
  exact synchronization numbers are my own choices**, not specified exactly by the block beyond "a
  `threading.Barrier` releases together" and "each poll loop gives up after 180 seconds": a 10-
  second `barrier.wait` timeout, a 30-second `thread.join`, and a 180-second poll deadline per
  order (not a combined 180 seconds across both).
- **The test asserts two distinct mission ids and that both jobs' digest `state` reads
  `JOB_COMPLETED`.** D15 (2) says "each naming its own mission and job" and "both jobs
  `completed`"; I read this as two distinct missions (one per order, same project) and both jobs'
  `state` equal to the `JOB_COMPLETED` constant, consistent with DECISION F253 D15's own CONTEXT
  measurement ("each with its own mission and its own completed job"). I added `JOB_COMPLETED` to
  the file's existing `pingpong_job` import rather than compare against the literal string
  `"completed"`, matching the module's own convention (`client_digest.py` imports it the same way)
  and the repo's code-discoverability rule against magic strings.
- **The record-parsing check (every `*.json` and every non-empty `*.jsonl` line under the scratch
  data root, each unparseable one named) mirrors the reviewer's `probe_two_orders.py` almost
  verbatim**, including its exact exception tuples (`(ValueError, UnicodeDecodeError)` for `.json`,
  `(ValueError,)` for `.jsonl` lines) — the probe is read-only per the block, so this is a
  hand-written equivalent, not a copy of that file.
- **The doc sentence (D15 (3)) was placed as a new paragraph directly after the existing
  `api_command_failed` paragraph in the "## Orders" section**, before "## Staying current", leaving
  the route table (the `POST /api/v1/orders` row) untouched — the block asked for prose "in the
  part about orders," and the table row already states the route's own behavior; the two-orders
  behavior is cross-route, so I judged it belonged in prose, not the table.
- `PUBLIC_API_VERSION` left at `1.7`, per DECISION F253 D15 (4); no production code changed, per
  the block's Goal line and DECISION F253 D15 (4).
- Everything else matches the block exactly: the four C1 files, the two C2 files, the gates' order,
  commands and content (aside from the declared double run of gate 2).
- Nothing about this commit's own self-review belongs here (per the block); see the reply's
  separate self-review report.

## Round verdicts

Round 16's PASS, resolving R-1201 and R-1202, is booked by C1 above. Round 17's verdict is the
reviewer's.

## For the operator, in plain sentences

Round sixteen's repairs passed review; when a program sends two orders at the same moment, Remedy
now runs both, and a test proves that both finish and that nothing Remedy writes down about them
is damaged; Remedy does not make the second order wait, and the limits on what a program may order
come in the next step, with the program's own key.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch, so it finds none to
   merge.
3. Then book round 17's verdict in the next round's first commit.
4. Then S6b: client tokens carry the operator's policy.

Operator questions open: 0.
Open findings: 12 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176 and R-1196, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 16, resolve R-1201 and R-1202, DECISION F253 D15, the plan and the block | done | `039fbe96f` |
| C2: two orders sent at once both run, and every record reads back whole | done | `ce9d5f6a4` |
| Gates 1 to 5 | done | all green; gate 2 run twice (declared deviation), both green with 590 passed |
| C2b (conditional repair commit) | skipped | not needed, gate 2 was green on both of its runs |
| C3: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
