── STEP FIX R-0790 — F112 Prompt budget per task class ──────────────────────
Round 24 · session continuing F112 · base `811638cd` (F112 R23 C3, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 23's PASS verdict AND register finding R-0790 (RECORD23,
  given verbatim below — it is a Gate paragraph followed by a blank line
  followed by the R-0790 finding paragraph; both already fully written by
  the reviewer, who independently reproduced everything RECORD23 claims —
  do not re-derive it, just apply it byte-for-byte). Then FIX R-0790: a
  one-character punctuation tail (e.g. the `-` in `+/-`) satisfies
  `ABS_PATH_RE`'s POSIX branch's "non-empty tail" requirement (R-0206's own
  earlier fix) without being any part of a real filesystem path.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r24.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD23 to `.agent/live_review.md`
  C2   apply PLAN24 to `.agent/plan.md`
  C3   apply PAIR_FIX to `packages/common/path_redaction.py`
  C4   apply PAIR_TEST to `tests/orchestration/test_failure_postmortem.py`
  C5   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f112-r24.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `packages/common/path_redaction.py`
  `tests/orchestration/test_failure_postmortem.py`
  `.agent/handoff.md`
  NO other file under `packages/`, `apps/`, `tests/` or `docs/` is touched.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or
     re-wrap one. If a slice looks wrong, apply it anyway and DECLARE the
     problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C5. If it exists at either reading: finish the commit in hand,
     write the handback, push, stop.
  3. `.agent/plan.md` ends WITHOUT a trailing newline; PLAN24 is applied
     as an exact whole-file replacement, no trailing newline added.
     `.agent/live_review.md` also ends WITHOUT a trailing newline; append
     it as `content_bytes + b"\n" + RECORD23_bytes` — ONE newline, no
     blank line. RECORD23 ITSELF already contains one internal blank line
     (`\n\n`) between its Gate paragraph and its `- R-0790 —` finding
     paragraph — that internal blank line is PART of RECORD23's own bytes
     and is preserved exactly as extracted; do not add a second one and do
     not remove it.
  4. PAIR_FIX is a REWRITE of exactly one line inside an existing
     multi-line `re.compile(...)` call (constraint per §3 item 4: this is
     NOT an append — the TO does not contain the FROM as a prefix, they
     are alternatives). Verify FROM occurs EXACTLY ONCE in
     `packages/common/path_redaction.py` before applying (`grep -cF` the
     exact FROM text), apply it as a literal string replacement (not by
     retyping the file), and verify AFTER that TO now occurs once and FROM
     occurs zero times.
  5. PAIR_TEST is a pure END-OF-FILE APPEND: FROM is the file's own exact
     last line (verify the file's tail ends with FROM's bytes before
     applying — `tail -c <n>` or a direct byte comparison), TO is
     `FROM_bytes + NEW_TESTS_bytes` where NEW_TESTS itself starts with a
     blank line (so the visual separation from the existing last test
     method is correct) and ends with a trailing newline. Verify the
     resulting file's byte length matches the arithmetic given below.
  6. THE RED-PROOF (mandatory, this touches a security-sensitive shared
     utility with four production consumers — treat this as load-bearing,
     not decorative): AFTER C3 and C4 both land (fix applied AND new tests
     added, both committed), create a DISPOSABLE git worktree at the
     current HEAD. Inside it, reintroduce ONLY the bug by replacing PAIR_FIX's
     TO text back to its FROM text (the exact single-line revert) — do NOT
     touch the test file in the worktree. Run
     `python3 -m pytest tests/orchestration/test_failure_postmortem.py::TestABareSlashIsNotAPath -v`
     in that worktree and report: the exact set of node ids that go RED
     (expected: exactly the two new ones,
     `test_a_punctuation_only_tail_is_not_a_path` for all three
     parametrized cases and
     `test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail`)
     and confirm every PRE-EXISTING test in that class (the R-0206 cases)
     stays GREEN under the mutation — a mutation that also breaks the old
     tests is not evidence the NEW tests discriminate this specific defect.
     Remove the worktree and prune afterward; the mutation must never touch
     the primary checkout.
  7. AFTER the red-proof, run the FULL relevant test surface against the
     real, fixed, committed code in the PRIMARY checkout (not the
     worktree): `python3 -m pytest tests/orchestration/test_failure_postmortem.py -v`,
     `python3 -m pytest tests/runtimes/test_supervisor_portability.py -q`,
     `python3 -m pytest tests/orchestration/test_review_manual_completion_shapes.py -q`,
     and `python3 -m pytest tests/docs/ -q`. Report each command's real
     exit code and pass/fail/skip counts. Every one must be green; if any
     is not, STOP before C5, do not paper over it, declare it fully.
  8. Do NOT run `ruff` — report that `python3 -m ruff check
     packages/common/path_redaction.py tests/orchestration/test_failure_postmortem.py`
     is clean anyway if you have access to it, but do not gate the round on
     it if the tool is denied (reviewer will confirm ruff cleanliness
     independently).
  9. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
     `docs/roadmap/features/T3_F112.md` are NOT touched this round.
  10. A sentence THIS ROUND makes stale, anywhere inside the change set, is
      repaired in the commit that falsifies it.
  11. NEVER force-push, never work on `main`, create NO pull request, merge
      nothing.

THIS ROUND'S PARAMETERS, measured by the reviewer at `811638cd` before this
block was authored:
  LIVE_REVIEW PRE-C1    `.agent/live_review.md` measures 2302928 bytes,
                        ending WITHOUT a trailing newline.
  RECORD23 LENGTH       7895 bytes total (Gate paragraph 4011 bytes + one
                        `\n\n` separator, 2 bytes + finding paragraph 3882
                        bytes = 7895 — measure this yourself against the
                        committed authored file's own extracted slice, as
                        ONE contiguous span between the delimiters).
  POST-C1 EXPECTED      2302928 + 1 + 7895 = 2310824 bytes.
  HEADER SHAPE          lines matching `^Gate: F\d+ R\d+ — ` currently
                        number 270; matching `^Gate: F112 R23 — `
                        currently 0. Expected after C1: 271 and 1.
  OPEN SET BEFORE C1    350 registered (unique `^- R-\d+ — ` ids), 72
                        unique `^Done: R-\d+ — ` ids, 278 open.
  OPEN SET AFTER C1     351 registered (R-0790 is new), 72 `Done:`, 279
                        open — THIS ROUND MOVES THE OPEN SET, unlike every
                        prior F112 round since R19; reconfirm both sides
                        yourself rather than assuming UNMOVED.
  PLAN.MD PRE-C2        46 lines (`wc -l`), ends WITHOUT a trailing
                        newline, currently holds PLAN23 (2154 bytes).
  PATH_REDACTION PRE-C3 6548 bytes.
  PATH_REDACTION POST-C3 6610 bytes (FROM 77 bytes, TO 139 bytes, delta
                        +62).
  TEST_FILE PRE-C4      49245 bytes, 1079 lines (`wc -l`), ends WITH a
                        trailing newline.
  TEST_FILE POST-C4     50148 bytes (FROM 79 bytes is the file's own last
                        line; NEW_TESTS is 903 bytes; TO = FROM + NEW_TESTS
                        = 982 bytes, replacing a 79-byte tail with a
                        982-byte one, net +903), 1098 lines (`wc -l`; 19
                        newlines added).

<<<BEGIN RECORD23>>>
Gate: F112 R23 — the round 23 entry, closure algorithm steps 1-2 (evidence job + review zip; no repository diff from the evidence/zip work itself). VERDICT PASS, over the range `dd80e564..811638cd` (commits C0a `6a6d6bf8`, C0b `6f3d3bc0`, C1 `555da9c2`, C2 `c1d8ae02` — four real content commits — plus handback commit `811638cd`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r23.md` and `HEAD:.agent/last_block.md` both print blob `76bf48c1fc8b85d3dea4f0fe62cf4d2b9579e78b`, reproduced directly; `wc -l` reproduced 276. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL: PLAN23 extracted from the committed authored file (2154 bytes) compared byte-for-byte against `.agent/plan.md` at C2 — equal, 2154 bytes both sides, no trailing newline, `## Goal` / `## Next Steps` each exactly once. THE RECORD APPEND AT C1 (booking RECORD22) HELD BYTE-IDENTICAL: pre-append `.agent/live_review.md` measured 2299057 bytes at `dd80e564`, RECORD22 extracted measured 3870 bytes exactly as pinned, appended as one newline plus RECORD22, post-append measured 2302928 bytes exactly matching `2299057 + 1 + 3870`; the pre-append content is an exact byte prefix; the file still ends WITHOUT a trailing newline; the open set recomputed mechanically read 350 registered / 72 `Done:` / 278 open on both sides, and lines matching `^Gate: F\d+ R\d+ — ` read 270 after C1 with exactly one matching `^Gate: F112 R22 — `. THE EVIDENCE JOB SUCCEEDED, REPRODUCED INDEPENDENTLY: `job_evidence.create_manual_completion_bundle` (job_id `dc2ae9fec6c342e3`, review_feature_id `f112`) built cleanly from three SCOPED verification runs (`test_class_prompt_budget.py` 24 passed, the two named `test_context_compiler.py` fixtures 2 passed, the `test_golden_path.py` canary 42 passed — no full-suite node-id list, per the closure protocol's own rule), verdict `PASS_WITH_RISKS`. THE REVIEW ZIP CORRECTLY BLOCKED, AND THE WORKER'S ROOT-CAUSE TRACE IS CONFIRMED BY THE REVIEWER'S OWN INDEPENDENT REPRODUCTION, NOT TAKEN ON TRUST: re-running `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure` directly reproduced the exact same `REVIEW_ZIP_ERROR: ReviewSubjectError: review_subject commit[123] subject is missing, too long, or carries a secret/path/control`, exit 2. Reading `review_commit_chain.json`'s own commits[123] confirms it is `c7d68c58`, subject "F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback" — a real, pre-existing, non-secret commit from this branch's own history. THE REVIEWER TRACED THE ROOT CAUSE TO ITS SOURCE INDEPENDENTLY: `packages/common/path_redaction.py`'s `ABS_PATH_RE`, POSIX branch `/{PATH_TAIL}+`, matches the bare `/-` inside `+/-` — reproduced directly with `ABS_PATH_RE.search(subject)` returning a match spanning exactly `/-`. The call chain is `review_subject.validate_review_commit_schema` -> `_metadata_is_safe` -> `run_manifest._contains_local_path` -> `failure_postmortem.safe_text` -> `ABS_PATH_RE.sub(...)`, each hop confirmed by direct reading, not assumed. Registered below as `R-0790`. No second id is minted for the ZIP BLOCK itself, since it is `R-0790`'s DIRECT, immediate consequence, not a second finding. NOT FIXED THIS ROUND: the fix touches a security-sensitive, adversarially-reviewed shared utility (four consumers) and deserves its own reviewer-gated repair round with a full mutation red-proof and the complete relevant test surface re-run, per the same discipline a reproducible branch-only regression gets. G6 RE-VERIFIED BY THE REVIEWER DIRECTLY: `git status --porcelain` and `git status --porcelain --ignored=no` both read empty; every commit's insertion count (277, 208, 2, 26) is under 500. THE OPEN SET IS NOW 279 (350 registered plus `R-0790`, 72 `Done:`) — the first movement since round 19. Round 24 fixes `R-0790`, re-runs the evidence job against the new head, rebuilds the zip, and — once it succeeds — the reviewer authors the STATUS line.

- R-0790 — Medium, `ABS_PATH_RE`'S POSIX BRANCH REDACTS A BARE PUNCTUATION TAIL AS IF IT WERE A FILESYSTEM PATH, BLOCKING THE REVIEW-ZIP PACKAGING GATE ON AN ORDINARY COMMIT SUBJECT. Found and registered by the reviewer at the F112 R23 gate (round 24), against the reviewer's own round 23 block, which correctly declared the zip's BLOCKED outcome without attempting a fix. MEASURED independently at `811638cd`: `packages/common/path_redaction.py`'s `ABS_PATH_RE`, POSIX branch `/{PATH_TAIL}+` (`PATH_TAIL = [^\s'"`,;)\]}]`), matches `/-` inside the literal text `+/-` — `ABS_PATH_RE.search("... changed-files +/- counts in handback")` returns a match spanning exactly `/-`, because the character before the `/` (`+`) is not excluded by the lookbehind `(?<![\w:/\\])`, and a lone `-` satisfies `{PATH_TAIL}+`'s one-or-more requirement. `failure_postmortem.safe_text` then rewrites this false match via `_safe_path_reference`, so `safe_text(subject) != subject`, so `run_manifest._contains_local_path` returns True, so `review_subject._metadata_is_safe` returns False, so `validate_review_commit_schema` rejects the commit subject as unsafe — which is exactly what `scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure` hit against commit `c7d68c58` ("F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback"), a real, ordinary, non-secret commit subject from this very branch's own history, raising `ReviewSubjectError: review_subject commit[123] subject is missing, too long, or carries a secret/path/control` and exiting 2. THIS IS THE SAME DEFECT CLASS AS `R-0206` (`TestABareSlashIsNotAPath`, `tests/orchestration/test_failure_postmortem.py`), which registered and fixed an earlier instance — a BARE slash in prose (`"plan status / plan next"`) matching as a zero-tail path and blocking an earlier closure the same way. R-0206's fix required the tail to be non-empty (`{PATH_TAIL}+` instead of `{PATH_TAIL}*`), which correctly stopped a BARE slash from matching but left a ONE-CHARACTER PUNCTUATION tail — `-`, and by the same reasoning `+`, `=`, `*` and similar — fully able to satisfy the "non-empty" requirement while still not being any part of a real filesystem path. WHY MEDIUM AND NOT HIGH: no secret or real local path is ever mis-redacted by this defect — the failure mode is the OPPOSITE, an over-eager false positive that blocks packaging rather than a false negative that leaks anything; the four production call sites (`failure_postmortem.py`, `provider_trust.py`, `self_repair_proposal.py`, `dev_server.py`) are otherwise unaffected in normal operation, and the defect is dormant until a commit subject happens to contain a bare operator-punctuation character immediately after a stray `/` with nothing else path-like around it — measured here as `+/-`, a notation this project's own commit messages use routinely for insertion/deletion counts, which is exactly why it recurred. FIX: narrow the POSIX branch with a positive lookahead requiring the character immediately after the leading `/` to be a word character, `.`, `~`, or another `/` — `/(?=[\w.~/]){PATH_TAIL}+` — which the reviewer dry-ran directly (by runtime-patching the compiled pattern, not editing the file) against every existing assertion in `TestABareSlashIsNotAPath` (`tests/orchestration/test_failure_postmortem.py`) plus the four real-path cases it pins, and against the new `+/-` case: every existing assertion held, and the new case correctly stopped matching. Owed to the next round, with a full mutation red-proof and the complete relevant test surface (`test_failure_postmortem.py`, `test_supervisor_portability.py`, any other file importing `path_redaction`) re-run green, per the same discipline this project already applies to a reproducible branch-only regression — never folded into the gate round that found it.
<<<END RECORD23>>>

<<<BEGIN PLAN24>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use consumed round 21, Built
State landed round 22, evidence job succeeded round 23 but the review
zip BLOCKED on a real pre-existing bug (R-0790: `ABS_PATH_RE` false-
positives on `/-` inside `+/-`). Round 24 fixes R-0790, then re-runs the
evidence job and zip against the new head.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 24 books RECORD23 (registers R-0790), fixes
`packages/common/path_redaction.py`'s `ABS_PATH_RE` POSIX branch with a
positive lookahead (dry-run confirmed against the full existing test
surface), adds a pinning test case, mutation red-proofs it in a
disposable worktree, re-runs the full relevant test surface, then
re-runs the evidence job and the review zip to confirm it now succeeds.

## Next Steps

- Once the zip succeeds: reviewer authors the STATUS line from the new
  job_id/package/hash/path/accepted-HEAD.
- Closure commit: STATUS `[x]`, README capability sync (same commit,
  R-0154 pin), `scripts/self_use_queue.json` SU-007 `consumed_by=F112`,
  final `.agent/` state.
- AGENTS.md PR workflow; merge deferred to the next feature's start.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to F112.
- R-0790's fix touches a security-sensitive, four-consumer shared
  utility — full relevant test surface must stay green, not just the
  narrow case that motivated the fix.
- If the fix reveals a SECOND, different blocking commit subject once
  this one clears, that is its own registered finding, not folded here.
<<<END PLAN24>>>

<<<BEGIN PAIR_FIX>>>
FROM (packages/common/path_redaction.py, exactly one line, verify count 1 before applying):
          | /{PATH_TAIL}+                    # /posix/path — one tail char

TO (replaces the FROM line, same file, same position):
          | /(?=[\w.~/]){PATH_TAIL}+        # /posix/path — real path start (R-0790: excludes a bare-punctuation tail like "-" in "+/-")
<<<END PAIR_FIX>>>

<<<BEGIN PAIR_TEST>>>
FROM (tests/orchestration/test_failure_postmortem.py, the file's own exact last line, verify the file's tail matches before applying):
        assert _contains_local_path("fix: read /home/user/secret.txt") is True

TO (FROM, followed immediately by the new test methods below — this is a pure append, TO contains FROM as its prefix):
        assert _contains_local_path("fix: read /home/user/secret.txt") is True

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
<<<END PAIR_TEST>>>

Done when — the gates below, each RUN and reported as ONE LINE in the
handback with its real reading. Every gate runs at a commit STRICTLY
EARLIER than C5.

G1 TRANSPORT — `sha256sum` and byte length of the committed
   `.agent/authored/f112-r24.md`. Report that
   `git rev-parse HEAD:.agent/authored/f112-r24.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.

G2 THE PLAN — extract PLAN24 by delimiter, compare byte-for-byte against
   `.agent/plan.md` at C2 — must be equal. Report `wc -l .agent/plan.md`
   (must be under 50), no trailing newline, `## Goal` and `## Next Steps`
   each exactly once.

G3 THE RECORD APPEND — extract RECORD23 by delimiter as ONE contiguous
   span (Gate paragraph + internal blank line + finding paragraph),
   report its byte length (expected 7895). Report the arithmetic
   `2302928 + 1 + <len> = <total>` against the real post-append size, the
   byte-prefix property, no trailing newline, a NEGATIVE CONTROL. Report
   lines matching `^Gate: F112 R23 — ` before (0) and after (1) C1, AND
   `^- R-0790 — ` before (0) and after (1) C1. Report registered/`Done:`/
   open counts on BOTH sides of C1 — expect 350/72/278 before and
   351/72/279 after (THIS round moves the open set).

G4 PAIR_FIX — report `grep -cF` of the exact FROM text against
   `packages/common/path_redaction.py` BEFORE C3 (expected 1) and the
   exact TO text AFTER C3 (expected 1), and FROM's count after C3
   (expected 0). Report the file's byte size before (6548) and after
   (6610) C3.

G5 PAIR_TEST — report that the file's tail matches FROM before C4, and
   the file's byte size before (49245) and after (50148) C4, with `wc -l`
   before (1079) and after (1098).

G6 THE RED-PROOF — report the disposable worktree's path, the exact node
   ids that went RED under the mutation (expected: the parametrized
   `test_a_punctuation_only_tail_is_not_a_path` cases and
   `test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail`),
   and that every OTHER test in `TestABareSlashIsNotAPath` (the R-0206
   cases) stayed GREEN under the same mutation. Report the worktree's
   removal.

G7 THE FULL RELEVANT SUITE — report each of the four commands in
   constraint 7's real exit code and pass/fail/skip counts, all green.

G8 THE TREE AND THE COMMITS — `git status --porcelain` immediately before
   C5 is staged — EMPTY. `git diff --stat 811638cd..<C4> -- packages/
   apps/ tests/ docs/` with `packages/common/path_redaction.py` and
   `tests/orchestration/test_failure_postmortem.py` excluded — must be
   EMPTY. PER-COMMIT INSERTIONS (the `+` column) for C0a through C4, each
   confirmed under 500.

Handback: rewrite `.agent/handoff.md` in full — feature and round, session
number, branch, base and head SHAs, per-commit changed-files table, ONE
line per gate above with its real reading, the item-status table
AGENTS.md mandates, deviations, the open-findings count (expected 279,
MOVED from 278), and the next expected action: re-run the evidence job
against the new head and the review zip (should now succeed), then the
reviewer authors the STATUS line. It has NO length cap. Do not write a
`Done:` or `Gate:` paragraph anywhere beyond applying RECORD23 verbatim —
`Done: R-0790` is the NEXT round's line, once the zip proves the fix
closes the loop, not this round's. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing.
══END BLOCK══