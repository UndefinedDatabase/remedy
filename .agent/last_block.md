── STEP FIX R-0791 + REBUILD EVIDENCE/ZIP — F112 Prompt budget per task class ─
Round 25 · session continuing F112 · base `6dfdff5d` (F112 R24 C5, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 24's PASS verdict AND register finding R-0791 (RECORD24,
  given verbatim below — a Gate paragraph, one blank line, then the
  R-0791 finding paragraph; already fully written and independently
  verified by the reviewer — do not re-derive it). Fix R-0791: a
  whitespace-only defect in a test file (double blank line at an append
  seam, missing trailing newline). Then re-run the evidence job and the
  mandatory review zip against the new head — R-0790's fix (round 24) is
  confirmed correct and complete, so the zip should now succeed.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r25.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD24 to `.agent/live_review.md`
  C2   apply PLAN25 to `.agent/plan.md`
  C3   apply PAIR25 to `tests/orchestration/test_failure_postmortem.py`
       (fixes R-0791)
  C4   the handback: rewrite `.agent/handoff.md` (the evidence-job/zip
       rebuild below is an EXTERNAL ACTION reported in this handback, not
       its own commit — the evidence dir is never committed)

Change set for COMMITS — NOTHING outside these paths:
  `.agent/authored/f112-r25.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `tests/orchestration/test_failure_postmortem.py`
  `.agent/handoff.md`
  NO other file under `packages/`, `apps/`, `tests/` or `docs/` is
  touched. `scripts/self_use_queue.json` is NOT touched this round.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE. If a slice looks wrong,
     apply it anyway and DECLARE the problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C4. If it exists at either reading: finish the commit in
     hand, write the handback, push, stop.
  3. `.agent/plan.md` ends WITHOUT a trailing newline; PLAN25 is applied
     as an exact whole-file replacement, no trailing newline added.
     `.agent/live_review.md` also ends WITHOUT a trailing newline; append
     it as `content_bytes + b"\n" + RECORD24_bytes` — ONE newline, no
     extra blank line. RECORD24 itself already contains one internal
     blank line between its Gate paragraph and its `- R-0791 —` finding
     paragraph — preserve that exactly as extracted, do not add or remove
     one.
  4. PAIR25 IS GIVEN AS TWO SEPARATE, CLEAN DELIMITED BLOCKS BELOW —
     `<<<BEGIN PAIR25_FROM>>>...<<<END PAIR25_FROM>>>` and
     `<<<BEGIN PAIR25_TO>>>...<<<END PAIR25_TO>>>` — each containing
     NOTHING but the literal bytes to match/replace, learning directly
     from round 24's own R-0791 mistake of mixing prose labels with
     literal content in the same delimited span. Extract each
     PROGRAMMATICALLY (read the file, slice between its own markers,
     nothing else) — never retype either one by hand. Verify PAIR25_FROM
     occurs EXACTLY ONCE in `tests/orchestration/test_failure_postmortem.py`
     before applying (a plain byte `.count()`, not a line-based search,
     since this span itself contains blank lines). Apply via a single
     literal string replacement of that one occurrence with PAIR25_TO.
     Verify AFTER: the file's total byte count is UNCHANGED at 50148 (the
     fix is whitespace-neutral: -1 byte from collapsing the double blank
     line, +1 byte from the added trailing newline), `wc -l` still reads
     1098, the file NOW ends WITH a trailing newnewline, and there is
     exactly ONE blank line (not two, not zero) at the seam between
     `is True` and `@pytest.mark.parametrize`. Run
     `python3 -m ruff check tests/orchestration/test_failure_postmortem.py`
     — must report zero issues (`All checks passed!`), where it reported
     the one `W292` before this commit.
  5. Do NOT touch `packages/common/path_redaction.py` this round — R-0790
     is already fully fixed and verified; this round's ONLY code change
     is the whitespace normalization in the test file.
  6. THE EVIDENCE + ZIP REBUILD (external action, no commit of its own):
     build a driver script (write it with the Write tool, run it with
     `python3 -c "import runpy; runpy.run_path('/absolute/path.py')"` if
     you need any `.remedy-wt` path — this round's evidence dir is at
     repo root and should not need that route) that:
       a. Confirms the merge base is unchanged:
          `git merge-base main HEAD` should still answer
          `5c28c6741db2d9073fc75cd159d91037e0757fb0` — declare if it has
          moved.
       b. Removes any stale `remedy-job-evidence-f112-closure/` directory
          from round 23's attempt first (it is untracked/gitignored
          scratch, safe to remove and rebuild fresh — confirm with `git
          check-ignore -v` before removing anything, exactly as round 23
          did before creating it).
       c. Runs `_run_verifications` from `packages.orchestration.job_evidence`
          against the SAME three scoped commands round 23 used (never a
          full-suite node-id list):
            "python3 -m pytest tests/orchestration/test_class_prompt_budget.py"
            "python3 -m pytest tests/orchestration/test_context_compiler.py -k \"test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded or test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic\""
            "python3 -m pytest tests/cli/test_golden_path.py"
          If any exits non-zero, STOP and declare it — that would mean a
          regression since round 19's own gate, which this round's own
          commits (whitespace-only, test-only) should not have caused.
       d. Calls `create_manual_completion_bundle` from
          `packages.orchestration.job_evidence` with:
          `evidence_dir="remedy-job-evidence-f112-closure"`,
          `repo_root="."`,
          `base_commit="5c28c6741db2d9073fc75cd159d91037e0757fb0"` (full
          40-char SHA),
          `head_commit=<the FULL SHA of this round's own C3 commit — the
          real current HEAD at the moment you call this, reconfirm it
          fresh, do not assume it in advance>`,
          `job_id=uuid4().hex[:16]` (fresh),
          `job_title="F112 Prompt budget per task class — closure evidence (v2, post R-0790 fix)"`,
          `step_range="T001-T003"`,
          `prior_job_ids=["dc2ae9fec6c342e3"]` (round 23's own evidence
          job id — this bundle SUPERSEDES it, so it is a genuine prior,
          unlike round 23's own empty list),
          `verification_runs=<the "runs" list from step (c)>`,
          `timestamp=<current UTC ISO-8601>`,
          `generated_at=<current UTC ISO-8601 with microseconds>`,
          `num_tasks=3`,
          `note_prefix="F112 closure evidence v2"`,
          `review_feature_id="f112"`.
          Print and capture the returned summary dict in full. If this
          raises, capture the full exception and STOP — declare it, do
          not retry blindly.
       e. Runs
          `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure`
          as a plain shell command. Capture full stdout/stderr and the
          real exit code. THIS SHOULD NOW SUCCEED. If it still fails,
          capture the FULL error text (do not summarize it) and STOP —
          this would mean R-0790's fix was insufficient or a SECOND,
          different commit subject is also blocked, either of which is
          its own new finding, not something to paper over.
       f. If the zip built, independently confirm its printed SHA-256
          with your own `sha256sum` of the produced file. Attempt to copy
          it into `/home/decodeux/Repos/remedy-history/zips/` (create the
          directory if needed and you have permission); report the
          absolute archived path, or `NOT ARCHIVED` with the reason.
  7. Do not `git add` or commit the evidence directory or the zip file —
     confirm `git status --porcelain` and `git status --porcelain
     --ignored=no` both read empty with respect to tracked paths after
     all of this.
  8. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
     `docs/roadmap/features/T3_F112.md` are NOT touched this round.
  9. NEVER force-push, never work on `main`, create NO pull request, merge
     nothing, run no `--approve` / promotion of anything.

THIS ROUND'S PARAMETERS, measured by the reviewer at `6dfdff5d` before
this block was authored:
  LIVE_REVIEW PRE-C1   `.agent/live_review.md` measures 2310824 bytes,
                       ending WITHOUT a trailing newline.
  RECORD24 LENGTH      5824 bytes total (Gate paragraph 3816 bytes + one
                       `\n\n` separator, 2 bytes + finding paragraph 2006
                       bytes = 5824 — measure this yourself against the
                       committed authored file's own extracted slice, as
                       ONE contiguous span between the delimiters).
  POST-C1 EXPECTED     2310824 + 1 + 5824 = 2316649 bytes.
  HEADER SHAPE         lines matching `^Gate: F\d+ R\d+ — ` currently
                       number 271; matching `^Gate: F112 R24 — `
                       currently 0. Expected after C1: 272 and 1.
  OPEN SET BEFORE C1   351 registered, 72 `Done:`, 279 open.
  OPEN SET AFTER C1    352 registered (R-0791 is new), 72 `Done:`, 280
                       open — reconfirm both sides yourself.
  PLAN.MD PRE-C2       44 lines (`wc -l`), ends WITHOUT a trailing
                       newline, currently holds PLAN24 (2073 bytes).
  TEST_FILE            50148 bytes both BEFORE and AFTER C3 (whitespace-
                       neutral fix), 1098 lines (`wc -l`) both before and
                       after.

<<<BEGIN RECORD24>>>
Gate: F112 R24 — the round 24 entry, R-0790's fix (production code + test). VERDICT PASS, over the range `811638cd..6dfdff5d` (commits C0a `22f1e186`, C0b `6739a759`, C1 `79aaadbb`, C2 `a5877e45`, C3 `488af2d1`, C4 `6a02a40b` — six real content commits — plus handback commit `6dfdff5d`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r24.md` and `HEAD:.agent/last_block.md` both print blob `8df85e4dad2c994440752a1204784e8ae5199310`. THE PLAN REPLACEMENT AT C2 AND THE RECORD APPEND AT C1 (booking RECORD23, registering `R-0790`) BOTH HELD BYTE-IDENTICAL: PLAN24 equal 2073 bytes both sides; RECORD23 (7895 bytes, one internal blank line preserved) appended to a 2302928-byte base gives exactly 2310824, matching the real post-append size, prefix and no-trailing-newline both confirmed; the open set MOVED for the first time since round 19, reproduced independently: 350 registered / 72 `Done:` / 278 open before, 351 / 72 / 279 after, with `- R-0790 — ` appearing exactly once post-append. THE FIX AT C3 IS CORRECT AND VERIFIED AGAINST THE SHIPPED CODE, NOT THE HANDBACK: `git show 488af2d1` changes exactly the one PAIR_FIX line to `/(?=[\w.~/]){PATH_TAIL}+`, reproduced byte-for-byte against the block's own PAIR_FIX TO text. THE RED-PROOF IS REAL, REPRODUCED INDEPENDENTLY BY THE REVIEWER A SECOND TIME (not merely re-read from the handback): reverting `ABS_PATH_RE` to its pre-fix form in a throwaway in-process monkey-patch (not the worker's own disposable worktree — an independent second instrument) and running `tests/orchestration/test_failure_postmortem.py::TestABareSlashIsNotAPath` reproduces EXACTLY the worker's claimed red set — the three `test_a_punctuation_only_tail_is_not_a_path` parametrizations and `test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail`, 4 failed, all ten pre-existing R-0206 cases still passing, 10 passed — and the fixed code reproduces 14 passed, 0 failed. THE FULL RELEVANT SUITE WAS RE-RUN BY THE REVIEWER DIRECTLY: `test_failure_postmortem.py` 141 passed, `test_supervisor_portability.py` 99 passed, `test_review_manual_completion_shapes.py` 23 passed — all matching the worker's own counts exactly. `python3 -m ruff check packages/common/path_redaction.py tests/orchestration/test_failure_postmortem.py` reproduced by the reviewer reads exactly ONE finding, `W292` (no trailing newline) in the test file, matching the worker's own declared deviation. ONE FINDING IS OWED FROM THIS ROUND'S OWN TRANSPORT AND IT IS REGISTERED BELOW AS `R-0791`: PAIR_TEST's applied bytes carry TWO blank lines at the append seam instead of one, and the file ends WITHOUT a trailing newline, both confirmed by direct reading of `tests/orchestration/test_failure_postmortem.py` — the root cause is the reviewer's OWN block mixing prose labels with literal file content inside the PAIR_TEST delimited section rather than giving one unambiguous literal byte span (the same class checklist item 15 already names), not a worker transcription error; the worker applied what the block's own mixed format made ambiguous, exactly as constraint 1 asks of an honest worker facing an unclear slice. NEITHER DEFECT CHANGES ANY TEST'S BEHAVIOUR: all 14 tests in the class pass either way, confirmed above. `git status --porcelain` reads empty; `git diff --stat 811638cd..6dfdff5d -- packages/ apps/ tests/ docs/` with the two edited files excluded is EMPTY; every commit's insertion count is under 500. THE OPEN SET IS 280 (351 registered plus `R-0791`, 72 `Done:`) after this round's own append. Round 25 fixes `R-0791` (a trivial whitespace normalization), re-runs the evidence job against the new head, and rebuilds the review zip — which should now succeed, since `R-0790`'s fix is confirmed correct and complete.

- R-0791 — Low, THE ROUND 24 BLOCK'S OWN PAIR_TEST FORMAT WAS AMBIGUOUS AND THE APPLIED TEXT CARRIES A DOUBLE BLANK LINE AND A MISSING TRAILING NEWLINE. Found and registered by the reviewer at the F112 R24 gate (round 25), against the reviewer's own round 24 block — the worker declared both symptoms honestly in its handback rather than silently normalizing them, exactly as an honest worker facing an unclear slice should. MEASURED independently at `6dfdff5d`: `tests/orchestration/test_failure_postmortem.py` reads `...is True\n\n\n    @pytest.mark.parametrize...` (two blank lines, not one) at the seam where the new test methods were appended, and the file's last byte is `e` (of `False`) with no trailing `\n` — `python3 -m ruff check` confirms exactly one finding, `W292`. ROOT CAUSE: the round 24 block's PAIR_TEST section gave the new content as a mix of prose instruction ("FROM, followed immediately by the new test methods below") and a REPEATED LITERAL copy of the FROM line, rather than one single unambiguous literal byte span the way every other slice in this feature's rounds has been given (a clean `<<<BEGIN X>>>...<<<END X>>>` pair with nothing but the literal bytes inside) — checklist item 15's own lesson, that a pair's shape must be verified by a mechanical containment test rather than read by eye, applies equally to how a REVIEWER authors the pair in the first place. WHY LOW: both symptoms are pure whitespace, no Python syntax is affected, no test's assertions or behaviour differ (`test_failure_postmortem.py` reads 141 passed either way, confirmed above), and the defect is confined to one test file with no runtime or production impact. FIX: a single whitespace-only edit collapsing the double blank line to one and adding the missing trailing newline, net zero byte-count change (911 bytes either way), verified by direct byte comparison before applying — never re-typed. Owed to round 25, alongside the evidence-job and review-zip rebuild it already needs to do.
<<<END RECORD24>>>

<<<BEGIN PLAN25>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
all closure preconditions satisfied. R-0790 fixed round 24 (positive
lookahead in ABS_PATH_RE); a trivial transport whitespace defect
(R-0791) is owed. Round 25 fixes R-0791, re-runs the evidence job and
review zip against the new head.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 25 books RECORD24 (registers R-0791), fixes R-0791 with a single
whitespace-only edit to `tests/orchestration/test_failure_postmortem.py`
(net zero byte-count change), confirms `ruff` clean, then re-runs the
evidence job (`job_evidence.create_manual_completion_bundle`, fresh
job_id, new head) and the review zip. If the zip succeeds: report the
package/hash/path for the STATUS line.

## Next Steps

- Once the zip succeeds: reviewer authors the STATUS line.
- Closure commit: STATUS `[x]`, README capability sync (same commit,
  R-0154 pin), `scripts/self_use_queue.json` SU-007 `consumed_by=F112`,
  final `.agent/` state.
- AGENTS.md PR workflow; merge deferred to the next feature's start.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to F112.
- If the zip finds a SECOND blocking commit subject, that is its own
  registered finding — do not attempt a blanket regex widening to
  pre-empt one that has not been measured.
<<<END PLAN25>>>

<<<BEGIN PAIR25_FROM>>>
is True


    @pytest.mark.parametrize("text", [
        "F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback",
        "changed-files +/- counts",
        "a+/-b",
    ])
    def test_a_punctuation_only_tail_is_not_a_path(self, text):
        # R-0790: a ONE-CHARACTER punctuation tail like the "-" in "+/-"
        # satisfied R-0206's own "tail is now mandatory" fix without being
        # any part of a real filesystem path, and blocked a real closure's
        # review zip on this exact ordinary commit subject.
        assert FP.safe_text(text) == text

    def test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail(self):
        from packages.orchestration.run_manifest import _contains_local_path

        assert _contains_local_path(
            "F112 R18 C5-fix: correct Range placeholder and changed-files "
            "+/- counts in handback") is False
<<<END PAIR25_FROM>>>

<<<BEGIN PAIR25_TO>>>
is True

    @pytest.mark.parametrize("text", [
        "F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback",
        "changed-files +/- counts",
        "a+/-b",
    ])
    def test_a_punctuation_only_tail_is_not_a_path(self, text):
        # R-0790: a ONE-CHARACTER punctuation tail like the "-" in "+/-"
        # satisfied R-0206's own "tail is now mandatory" fix without being
        # any part of a real filesystem path, and blocked a real closure's
        # review zip on this exact ordinary commit subject.
        assert FP.safe_text(text) == text

    def test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail(self):
        from packages.orchestration.run_manifest import _contains_local_path

        assert _contains_local_path(
            "F112 R18 C5-fix: correct Range placeholder and changed-files "
            "+/- counts in handback") is False

<<<END PAIR25_TO>>>

Done when — the gates below, each RUN and reported as ONE LINE in the
handback with its real reading. Every gate runs at a commit STRICTLY
EARLIER than C4.

G1 TRANSPORT — `sha256sum` and byte length of the committed
   `.agent/authored/f112-r25.md`. Report that
   `git rev-parse HEAD:.agent/authored/f112-r25.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.

G2 THE PLAN — extract PLAN25 by delimiter, compare byte-for-byte against
   `.agent/plan.md` at C2 — must be equal. Report `wc -l .agent/plan.md`
   (must be under 50), no trailing newline, `## Goal` and `## Next Steps`
   each exactly once.

G3 THE RECORD APPEND — extract RECORD24 by delimiter as ONE contiguous
   span (Gate paragraph + internal blank line + finding paragraph),
   report its byte length (expected 5824). Report the arithmetic
   `2310824 + 1 + <len> = <total>` against the real post-append size, the
   byte-prefix property, no trailing newline, a NEGATIVE CONTROL. Report
   lines matching `^Gate: F112 R24 — ` before (0) and after (1) C1, AND
   `^- R-0791 — ` before (0) and after (1) C1. Report registered/`Done:`/
   open counts on both sides — expect 351/72/279 before, 352/72/280
   after.

G4 PAIR25 — report the exact `.count()` of PAIR25_FROM's bytes in the
   test file before C3 (expected 1). Report the file's total byte count
   before AND after C3 (both expected 50148), `wc -l` before and after
   (both expected 1098), that the file now ends WITH a trailing newline,
   and that exactly one blank line separates `is True` from
   `@pytest.mark.parametrize`. Report `python3 -m ruff check
   tests/orchestration/test_failure_postmortem.py` — expected clean.

G5 THE EVIDENCE + ZIP REBUILD — report: the reconfirmed merge base; the
   three scoped verification commands' real exit codes and pass counts;
   the full summary dict `create_manual_completion_bundle` returns (or
   the full exception); the zip script's real exit code and, if it
   succeeded, the printed filename and SHA-256 plus your own independent
   `sha256sum` confirming it; the archiving outcome (path or `NOT
   ARCHIVED`). STATE PLAINLY whether the zip now succeeds — this is the
   round's central, load-bearing result.

G6 THE TREE AND THE COMMITS — `git status --porcelain` and `git status
   --porcelain --ignored=no` immediately before C4 is staged — both
   EMPTY. `git diff --stat 6dfdff5d..<C3> -- packages/ apps/ tests/
   docs/` with `tests/orchestration/test_failure_postmortem.py` excluded
   — must be EMPTY. PER-COMMIT INSERTIONS for C0a through C3, each
   confirmed under 500.

Handback: rewrite `.agent/handoff.md` in full — feature and round,
session number, branch, base and head SHAs, per-commit changed-files
table, ONE line per gate above with its real reading, the item-status
table AGENTS.md mandates, deviations, the open-findings count (expected
280, MOVED from 279), and the next expected action: if the zip
succeeded, the reviewer authors the STATUS line and the closure commit
follows; if it did not, name the exact new blocker for the reviewer to
design the next round around. It has NO length cap. Do not write a
`Done:` or `Gate:` paragraph anywhere beyond applying RECORD24 verbatim
— `Done: R-0790` and `Done: R-0791` are the NEXT round's lines, once the
reviewer accepts this round's own verdict. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing.
══END BLOCK══