OUTCOME: pending
── STEP T001–T003/3 — F051 Escalate instead of block (LARGE round) ──────
Goal:        An unattended run never stalls on a human question: a
             needs_decision task pauses only its branch, the executor
             keeps running disjoint branches and picks up answered
             branches at batch boundaries, open decisions render first
             in status/report.
Bundle:      1 Open PR Gate (merge #164) · 2 branch · 3 authored texts ·
             4 claim+state commit · 5 inspection · 6 T001 · 7 T002 ·
             8 T003 · 9 round gate · 10 push + PR · 11 handback
Change:      docs/roadmap/STATUS.md (one line), .agent/**,
             packages/orchestration/** (escalation + executor),
             status/report render paths found in inspection,
             tests/orchestration/test_escalation.py,
             tests/cli/test_open_decisions_view.py.
Constraints: Reuse the EXISTING decision queue and CLI unchanged (A6) —
             a second queue is an automatic reject; extend queue records
             ADDITIVELY only. No polling loops — answered decisions are
             noticed at batch boundaries (assert the check count in a
             test). Do not touch: notification channels, inbox UI,
             decision auto-answering. Commits small (<500-line diffs),
             several per slice is fine. STOP-ON-RED: if a slice gate is
             red after one focused fix attempt, stop the bundle at that
             slice, commit honest state, hand back with the raw output —
             never continue past a red gate. Closure is NOT part of this
             round.
Done when:   Every verification below green: per-slice gates + the round
             gate (feature tests + tests/docs + canary), raw output
             recorded.
Handback:    Completion report + rewrite .agent/handoff.md (per-commit
             changed-files tables, inspection map, sha256sum outputs
             verbatim, raw gate outputs, fixture pause/resume timeline).

AUTHORED-TEXT PROTOCOL (all three blocks below): bytes = the lines
strictly BETWEEN the BEGIN and END marker lines, joined with LF, plus
one final LF. Save to .agent/authored/<name>.md, verify sha256sum
against the BEGIN-marker hash BEFORE any use. Mismatch: rejoin
hard-wrapped lines with a single space and re-verify; if still
mismatched, STOP that item, record received bytes + computed hash in
the handoff, hand back. Never apply an unverified text.

1. Open PR Gate:
   gh pr list --state open --json number,headRefName,baseRefName,isDraft
   Expected: exactly one PR — #164, feature/docs-discoverability-amend
   -> main, not draft. Anything else: STOP, report, hand back.
   Reviewer verdict amend0730-R1 = PASS; merging under the standing
   same-session operator approval (2026-07-30):
   gh pr merge 164 --merge --delete-branch
   git checkout main
   git pull --ff-only
   Verify: gh pr list --state open -> empty.

2. git checkout -b feature/f051-escalate-instead-of-block

3. Save and verify the three authored texts per the protocol:
   .agent/authored/f051-r1-1.md, f051-r1-2.md, f051-r1-3.md.
   Record the sha256sum lines verbatim for the handoff.

4. Commit 1 — claim + state, own commit:
   - docs/roadmap/STATUS.md: verify the exact line
     "- [ ] F051 — Escalate instead of block (unattended)"
     occurs exactly once (grep -cF -> 1), then replace it with the
     one-line bytes of f051-r1-1.md. Touch no other line.
     Proofs: new line grep -cF -> 1, old line grep -cF -> 0,
     git diff --stat shows +1/-1 on STATUS.md only.
   - .agent/live_review.md := full replace with f051-r1-2.md (cmp).
   - .agent/plan.md        := full replace with f051-r1-3.md (cmp).
   - .agent/last_block.md  := guard entry (block f051-r1 received,
     transport notes, OUTCOME pending).
   Commit message: chore(f051): claim F051 + state reset (amend0730 verdict persisted)
   Immediately after: python3 -m pytest tests/docs/ -q  (expect exit 0 —
   catches any ledger-pin effect of the [~] flip early; on red: STOP,
   hand back).

5. Inspection (read-only, BEFORE building): locate and record in the
   handoff a file:line map of (a) the existing decision queue — record
   schema, enqueue call sites used by plan approval and budget stops,
   the answer CLI command; (b) the executor's batch boundary from F050
   (where the ready set recomputes in
   packages/orchestration/long_run_executor.py); (c) where status and
   report render today. Build on exactly these seams.

6. T001 — needs_decision outcome:
   Additive task outcome "needs_decision". On it, the executor
   enqueues ONE decision on the existing queue carrying task id,
   question, options, and a safe default where one exists;
   cross-reference payloads when two tasks raise the same question
   (two decisions — no dedup). Mark the task awaiting-decision;
   awaiting is NOT failed: downstream stays blocked like
   blocked_downstream, and the run does not end because of it.
   A decision with a safe default is still ASKED in attended mode —
   defaults auto-apply only under --yes/unattended, recorded in the
   assumption log (A9 consistency).
   Unit tests in tests/orchestration/test_escalation.py.
   Slice gate: python3 -m pytest tests/orchestration/test_escalation.py -q
   plus the existing decision-queue test file(s) found in item 5 — all
   exit 0.

7. T002 — executor continuation + pickup + fixture:
   The executor continues pulling ready tasks from disjoint branches
   while a branch awaits a decision; at every ready-set recompute
   (batch boundary) it re-checks awaiting tasks for answered
   decisions and unblocks the branch — no polling loop; a test
   asserts the check count. End of run with open decisions ->
   terminal status blocked.
   Three-branch fixture (the acceptance heart): one root fans into
   three branches; branch 1's task raises needs_decision and has at
   least one downstream task; branches 2 and 3 are free and complete;
   the run ends blocked with exactly one open decision listed;
   answering via the EXISTING decision CLI + resume completes branch
   1's remainder; additionally a decision answered while the run is
   still executing other branches is picked up at the next batch
   boundary without restart. Linear plans behave exactly as before.
   Slice gate: python3 -m pytest tests/orchestration/test_escalation.py
   tests/orchestration/test_long_run_executor.py
   tests/orchestration/test_dag_schedule.py -q  -> exit 0.

8. T003 — surfacing:
   Status and report render open decisions FIRST, each with the exact
   command that answers it; the final report of a blocked run carries
   a next-action line naming that command. Tests in
   tests/cli/test_open_decisions_view.py.
   Slice gate: python3 -m pytest tests/cli/test_open_decisions_view.py -q
   -> exit 0.

9. Round gate — raw output into the handoff:
   python3 -m pytest tests/orchestration/test_escalation.py \
     tests/orchestration/test_long_run_executor.py \
     tests/orchestration/test_dag_schedule.py \
     tests/cli/test_open_decisions_view.py -q      (exit 0)
   python3 -m pytest tests/docs/ -q                (exit 0)
   python3 -m pytest tests/cli/test_golden_path.py -q   (exit 0)
   The full suite is NOT part of this round — the integration gate is
   its own later round.

10. Final state commit (handoff rewrite + last_block OUTCOME executed),
    then: git push -u origin feature/f051-escalate-instead-of-block
    gh pr create --base main \
      --title "F051 — Escalate instead of block (T001–T003)" \
      --body per AGENTS.md PR workflow (what/why, changed-files table,
      verdict PENDING R1, open findings R-0155/R-0156 carry-forward).
    Do NOT merge.

11. Hand back with the completion report.

TRANSPORT NOTES (worker, f051-R1):
(1) The three authored texts arrived CLEAN. All three sha256sum outputs
    matched their BEGIN-marker hashes on first computation, before any
    use — no rejoin needed.
(2) Cosmetic wraps in the block's own instruction text only (the three
    BEGIN marker lines kept their trailing "-----" on the same line this
    time; item 4's and item 10's commit-message/title lines are recorded
    above rejoined). No authored bytes affected.
