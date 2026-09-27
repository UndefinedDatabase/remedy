# Handoff — F030, round 4 (book R3, land T003's end-to-end proof)

## Session

SESSION 1 of feature F030 · round 4 · rounds so far 4. Context remaining at
handback: comfortable — the round read every named source file once (the
model, the door test, the call-boundary tests, the prompt-trace shape,
`steering.py`, `pingpong_loop.py`'s consumption call site, `ui_server.py`'s
note summary and dispatch, `pingpong_job.py`'s report map), wrote S1's new
live test and the mutation tool, caught one bug in its own tool by actually
running it rather than trusting ruff, and still has a healthy context
budget left.

## Range

Review of `34f012e3e`..`HEAD` (`HEAD` is this handback's own commit, `F030
R4 C5`, on `feature/f030-steering-messages`).

## Commits

### cd58a24c2 F030 R4 C1: copy round 4 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r4-block.md | 205/0 | verbatim copy of this round's block |
| .agent/authored/f030-r4-booking.diff | 10/0 | verbatim copy of the booking payload |
| .agent/authored/f030-r4-plan.md | 29/0 | verbatim copy of the plan payload |

Measured insertions: 244 (205+10+29). Block expected 205+39=244. Match.

### d75061f07 F030 R4 C2: book round 3's PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | F030 R3 Gate entry appended (`git apply` of booking.diff) |
| .agent/plan.md | 7/8 | rewritten to plan.md payload |

Measured numstat: 2/0, 7/8. Block expected exactly this. Match.

### dfde8e103 F030 R4 C3: prove a steering note end to end through the write door
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_steering_note_e2e_live.py | 461/0 | new: SCENARIO A (`TestSteeringNoteTakenInLive`) — a note posted while T1's round 1 build call is held in flight reaches round 2 as the `builder_operator_notes` segment (rank 5), the consumption marker names T1/round 2, and `events-since` orders `steering_message_received` before `steering_message_consumed` (round_number 2) before a later non-steering frame of T1, with no other frame carrying the note's text; SCENARIO B (`TestSteeringNoteNotTakenInLive`) — a note whose task passes at round 1 is never consumed, never reaches T2, and is listed by `export_job_report`, `format_job_report_text` and `remedy chat show --json` as `not_taken_in` |

Measured insertions: 461. No insertion count was ordered for this commit.

### f8bfe3050 F030 R4 C4: add the round 4 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r4-mutations.py | 115/0 | G5's red-proof tool: m1 `steering.py`'s address gate, m2 `pingpong_loop.py`'s operator-notes text, m3 `ui_server.py`'s stream `note` field, m4 `pingpong_job.py`'s report map |

Measured insertions: 115. No insertion count was ordered for this commit.

### e22dbc750 F030 R4 C4b: fix the mutation tool's failing-node-id extraction
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r4-mutations.py | 6/1 | `_failing_node_ids` split each `FAILED ` summary line on its first space, which lands between the word "FAILED" and the node id, so every reported node id read as the literal string "FAILED"; fixed to strip the `FAILED ` prefix and split on ` - ` instead |

Measured insertions/deletions: 6/1. Not part of the block's ordered bundle —
see Deviations.

Exception (self-reference, per `docs/agents/handback_template.md`): this
handback's own commit, `F030 R4 C5`, is not tabled here.

## External actions

- `git worktree add --detach .remedy-wt/f030-r4-mut f8bfe3050` — G5's
  red-proof worktree. Removed with
  `git worktree remove --force .remedy-wt/f030-r4-mut` and
  `git worktree prune`; `git worktree list | wc -l` read 64 both before and
  after (equal to this round's step-4 reading).
- No push, no PR create/edit/merge yet — those are G6, run after this
  commit; their real readings are in this round's reply, not here.

## Verification

**G1 transport** — payload readings (measured before use):

    block.md lines: 205 sha256: 990f0b5efaf6bd500b48a8b7320ba92ee9d91d2ef8a1405ff5a134eaa14ee159
    booking.diff lines: 10 bytes: 9582 sha256: 355943c47f4ef9f8716cbeddfd0d8cb03e44b8b12754768ffe78f5a2b19bf504
    plan.md lines: 29 bytes: 1033 sha256: 79472ac16f1e8f989d5dcd4409923d4b0be7f7f3e7501879300b142bf738c0fb

All readings equal the delegation message's and the PAYLOADS table's
readings exactly. Each `.agent/authored/f030-r4-*` copy read back with
`git show cd58a24c2:<path>` equalled its source byte for byte (sha256
comparison):

    .agent/authored/f030-r4-block.md byte-identical: True (sha 990f0b5e...ee159 both)
    .agent/authored/f030-r4-plan.md byte-identical: True (sha 79472ac1...c0fb both)
    .agent/authored/f030-r4-booking.diff byte-identical: True (sha 355943c4...bf504 both)

`git apply --check .remedy-wt/f030-r4-payloads/booking.diff` → `CHECK_EXIT=0`.
`git apply .remedy-wt/f030-r4-payloads/booking.diff` → `APPLY_EXIT=0`.

**G2 the records** — at `d75061f07`, `git show <sha>:<path>` read:

    .agent/live_review.md bytes: 317793 sha256: 988cbf32fb2fc9fabb0e7293384b41920b455261ed720b7524649145cfdf3628
    .agent/plan.md        bytes: 1033   sha256: 79472ac16f1e8f989d5dcd4409923d4b0be7f7f3e7501879300b142bf738c0fb

Both equal the reviewer's given readings. `open_finding_ids` (from
`scripts/rotate_live_review.py`, imported and run over the ledger text at
`d75061f07`) read `[]` — empty, as the reviewer read it.

**G3 the code** — ruff at C4 (`f8bfe3050`, re-verified unchanged after C4b):

    python3 -m ruff check tests/ui_server/test_steering_note_e2e_live.py
    All checks passed!
    REAL_EXIT=0

Quoted from the diff — the handshake provider:

    class HandshakeFakeProvider(FakeProvider):
        '''Holds ONLY the runner process's first build call in flight — a module-level flag,
        since `create_provider` mints a fresh provider per task and per call site. ...'''

        def build(self, prompt, **kwargs):
            global _did_handshake
            if not _did_handshake:
                _did_handshake = True
                Path({building!r}).write_text("1")
                deadline = time.monotonic() + 60.0
                while not Path({go!r}).exists() and time.monotonic() < deadline:
                    time.sleep(0.05)
            return super().build(prompt, **kwargs)

Scenario A's ordering assertions:

    recv_seq = received[0]["seq"]
    cons_seq = consumed[0]["seq"]
    assert recv_seq < cons_seq

    t1_later_non_steering = [
        e for e in events
        if e.get("task_id") == t1 and e["seq"] > cons_seq and e["event"] not in steering_kinds
    ]
    assert t1_later_non_steering, "no builder action recorded after consumption"

**G4 the tests** — the new file alone, three times, serially:

    run 1: 2 passed in 1.41s (wall 1.63s)
    run 2: 2 passed in 1.41s (wall 1.64s)
    run 3: 2 passed in 1.40s (wall 1.62s)

Then, at C4, serially, real exit code:

    569 passed, 1 skipped in 75.82s (0:01:15)
    REAL_EXIT=0

The one `SKIPPED` line: `tests/test_agent_tooling.py:43: D12 quarantine
(F252)` — the same F252 quarantine the reviewer named. `--collect-only -q`
node count for the new file: 2. Accounting: reviewer's base at `34f012e3`
(selection less the new file) read 567 passed; 567 + 2 = 569. Matches
exactly.

`python3 -m apps.cli.main integrity check --json` →

    {"check_count": 6, "checks": [...], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
    REAL_EXIT=0

All six checks `pass`: `handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`.

**G5 the red proofs** — `git worktree add --detach .remedy-wt/f030-r4-mut
f8bfe3050`. First run (before the C4b fix) caught all four mutations but
misreported every failing node id as the literal word "FAILED" (the bug
C4b fixes); re-run after the fix, from the primary checkout's corrected
script against the same worktree:

    control (first): exit=0 failed=0 nodes=[]
    m1: exit=1 failed=1 nodes=['tests/ui_server/test_steering_note_e2e_live.py::TestSteeringNoteTakenInLive::test_a_note_posted_mid_call_is_taken_in_at_round_two_and_reaches_the_stream']
    m2: exit=1 failed=1 nodes=['tests/ui_server/test_steering_note_e2e_live.py::TestSteeringNoteTakenInLive::test_a_note_posted_mid_call_is_taken_in_at_round_two_and_reaches_the_stream']
    m3: exit=1 failed=1 nodes=['tests/ui_server/test_steering_note_e2e_live.py::TestSteeringNoteTakenInLive::test_a_note_posted_mid_call_is_taken_in_at_round_two_and_reaches_the_stream']
    m4: exit=1 failed=1 nodes=['tests/ui_server/test_steering_note_e2e_live.py::TestSteeringNoteNotTakenInLive::test_a_note_whose_task_passes_in_round_one_is_never_taken_in']
    control (last): exit=0 failed=0 nodes=[]
    restored byte-identical: True (packages/orchestration/steering.py)
    restored byte-identical: True (packages/orchestration/pingpong_loop.py)
    restored byte-identical: True (packages/orchestration/ui_server.py)
    restored byte-identical: True (packages/orchestration/pingpong_job.py)
    ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
    REAL_EXIT=0

All four mutations caught (m1-m3 red Scenario A, m4 reds Scenario B — as
expected, since m4 only affects the job-report map Scenario B alone
reads). Both controls green. Every mutated file restored byte-identical.
Worktree removed: `git worktree remove --force .remedy-wt/f030-r4-mut`,
`git worktree prune`; `git worktree list | wc -l` read 64 afterward, equal
to this round's step-4 reading.

`git diff --name-only 34f012e3` before C5: exactly the paths constraint 3
lists — the three `.agent/authored/f030-r4-*` copies, the mutation tool,
`.agent/live_review.md`, `.agent/plan.md`, and
`tests/ui_server/test_steering_note_e2e_live.py`. No production file, no
existing test and no browser file changed.

## Authored-text proofs

The three `.agent/authored/f030-r4-*` payload copies (G1, above): each
equals its source byte for byte, read back from `git show cd58a24c2:<path>`
against the file this worker measured from `.remedy-wt/f030-r4/block.md`
and `.remedy-wt/f030-r4-payloads/`. `.agent/authored/f030-r4-mutations.py`
is this worker's own authored tool (G5), not a reviewer payload, so it
carries no fidelity comparison — its correctness is the G5 red-proof run
itself (and its own bug, found by running it, is C4b's fix).

## Deviations & assumptions

1. **An extra commit, C4b, not in the block's ordered C1-C5 bundle.** G5's
   first tool run correctly caught all four mutations (exit≠0, failed=1
   each) but printed every failing node id as the literal word "FAILED"
   instead of the actual test node id — `_failing_node_ids` split each
   `FAILED <node-id>` summary line on its first space, landing between
   "FAILED" and the id rather than after it. This is a bug in this round's
   own authored tool, found only by actually invoking it against a live
   mutation (ruff and reading did not catch it, since the tool is
   syntactically and structurally correct — only its string-splitting
   logic was wrong). AGENTS.md's Commit Discipline forbids amending a
   commit already made (`git commit --amend`) outside an explicit operator
   request, and CONSTRAINT 4 of this block permits correcting a test THIS
   round wrote before C5, with the correction declared — I read that
   allowance as extending to this round's own tool by the same logic (an
   authored artifact this round produced, found wrong before C5, corrected
   before C5, declared here). The fix does not change which mutations were
   caught or the restore verdict — only the printed node-id text — and it
   touches only `.agent/authored/f030-r4-mutations.py`, already inside the
   round's whole tracked path set (constraint 3), so no path-set or
   production-file boundary was crossed.
2. No other deviation. Every step, gate and report ran in the block's
   order; the test this round wrote (S1) needed no correction; no existing
   test went red.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Step 1 (STOP check) | done | `.agent/STOP` absent |
| Step 2 (shell/branch/HEAD) | done | pwd, status, branch, HEAD all matched |
| Step 3 (block bytes) | done | 205 lines, sha256 match exact |
| Step 4 (worktree count) | done | 64 |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | see Deviation 1 (node-id bug found by running the tool, fixed in C4b) |
| C4b | done | undeclared-bundle correction, declared as Deviation 1 |
| C5 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | ruff clean at C4 |
| G4 | done | 569 passed, 1 skipped; integrity six-for-six |
| G5 | done | all 4 mutations caught, restored byte-identical, worktree count restored to 64 |

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from
disk) — checked at this round's step 1, absent. Then the review of round 4.
Then the closure sequence's first round — the Built State, the checklist
consolidation, the self-use item and the one full suite. Open findings: 0.
Operator questions: 0.
