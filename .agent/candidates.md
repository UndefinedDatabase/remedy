# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. Three candidates, raised by the reviewer during the F021 closure
review and recorded here without ids because the closure protocol reserves ids
for the next session's first reviewed round. Each was MEASURED by the reviewer
at `4db0a2e4`, not read back out of a handback.

- AN ALIGNMENT SUMMARY REPORTS ONE DIRTY FILE WHILE EVERY LIST IT SUMMARIZES IS
  EMPTY · F021 R40 · 2026-08-23. In the manifest inside
  `remedy-review-20260823-005026-READY_FOR_REVIEW.zip`,
  `review_subject_evidence_alignment.dirty_file_count_total` reads 1 while
  `dirty_source_test_files` and `uncovered_source_test_files` are both empty,
  `issues` is empty and the verdict is `PASS`. The package was built from a tree
  whose `git status --porcelain` printed 0 lines, so either that count has a
  source none of the lists expose or it is stale. Nothing about this closure is
  unsound because of it — the verdict rests on the empty lists and the PASS —
  but a non-zero count beside three empty collections is the kind of number a
  later reader will either trust or panic about, and neither is justified today.
  Candidate counter-measure: find the producer of that field, and either make it
  name the file it counted or derive it from the lists it sits beside.

- TWO GATES IN ONE PACKAGE DISAGREE ABOUT WHETHER A HUMAN MUST STILL APPROVE ·
  F021 R40 · 2026-08-23. `commit_execution_gate.json` in the evidence bundle and
  the `commit_execution_gate` field of `final_verifier_report.json` both read
  `NEEDS_HUMAN_APPROVAL`, and `human_final_reviewer_required` is true, while the
  same package's `ready_gate_matrix.ok` is true over an empty
  `blocking_reasons` and `PACKAGE_STATUS` is `READY_FOR_REVIEW`. Both readings
  are defensible on their own terms and the closure protocol treats the ready
  gate as the blocker, so nothing here blocked F021; the cost is that a reader
  cannot tell from the package alone which authority governs. NOTE ON ITS
  ADDRESS, because the R40 handback got this wrong and the correction belongs
  with the candidate: that handback located the verdict at a manifest key
  `gate_verdicts.commit_execution_gate`, and the package manifest carries no
  `gate_verdicts` key at all — the two addresses above are where the value
  really lives. Candidate counter-measure: have the packager either surface the
  commit-execution verdict in the manifest beside the ready gate, or record why
  the ready gate supersedes it.

- EVERY CLOSURE BUNDLE ON THIS MACHINE CARRIES A ZERO-BYTE `job_report.json` ·
  F021 R40 · 2026-08-23. The reviewer measured all thirteen
  `remedy-job-evidence-*` directories under `.remedy-wt/` and `job_report.json`
  is 0 bytes in every one of them, F021's included. The producer emits the file
  and writes nothing into it, inside a bundle whose entire purpose is evidence,
  and no gate notices because nothing reads it. This is not an F021 defect and
  it blocked nothing — the substance lives in `final_verifier_report.json`,
  `verification_tests.json` and `review_subject.json`, all of which the reviewer
  read and re-derived — but an always-empty evidence artifact is either a
  producer bug or a file that should not be emitted. Candidate counter-measure:
  decide which, and either populate it or stop writing it.

NOT A CANDIDATE, recorded so the next round does not mint an id for it
(`docs/agents/planner_reviewer_prompt.md` §3 item 30): 10646 of the package's
13921 members are `.remedy-wt/` scratch. That is the already-registered R-0403,
which routes to a paydown branch, and it is unchanged rather than new.
