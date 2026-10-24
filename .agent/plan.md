# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 8 BLOCKED after C2. C1 (book round 7, R-1454, plan, block, self-use script) and C2 (the
checklist's consolidation pass) are committed and pushed. C3's self-use run (SU-081, job
11b187c9221f49b1) completed and passed, but the commit recording its ten evidence files under
`.agent/selfuse_f157/` was refused by the pre-commit secret/path scanner on `job_diff.txt`: the
job's own task was to write the first tests for `packages/common/public_text_redaction.py`, so its
diff legitimately contains fake credentials and home-directory-style absolute paths as
redaction-test fixtures, which the scanner cannot distinguish from a real leak. The round's block orders exactly
this response: "stop and report the refusal; edit nothing." C4 (the one full suite) and C5 were
therefore NOT run, because C4 must run on the committed tree and the suite would otherwise pick up
the uncommitted `tests/test_public_text_redaction.py` on disk. `scripts/self_use_queue.json`
(one appended SU-081 entry, `consumed_by` empty) and `.agent/selfuse_f157/` (ten files) are left
staged, uncommitted, exactly as the failed commit attempt produced them, for the reviewer's own
inspection.

## Next Steps
1. The reviewer designs the repair for the self-use evidence capture (e.g. a scanner exception for
   test-fixture diffs under `.agent/selfuse_f157/`, or redacting `job_diff.txt` before it is
   written) and re-issues C3 in a fresh round.
2. C4 (the one full suite), then C5 (handback), as round 8's block originally ordered.
3. The evidence bundle and the review package (closure algorithm steps 1 and 2).
4. The closing round: the Built State, the ledger rotation, the STATUS line, the README and the
   pull request.

## Risks
- A red full suite or a self-use run defect, once C3 lands, turns the next round into a repair
  round first.
- The staged, uncommitted C3 files in the working tree must not be lost before the reviewer's
  repair round reads them.
