# Handoff — F106 Session resume instead of rebuild

## Session

SESSION 2 of feature F106 · round 8 · rounds so far 8

## Range

Review of `2a17ee639be5f8cc4319e57f4dd1b7e0d7e85fe9..HEAD`.

## Commits

### 36cc5bcd F106 R8 C0a: save round 8 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f106-r8.md` | +400/-0 | C0a: `shutil.copyfile` of the round's step block from the reviewer's scratch original `.remedy-wt/f106-r8-block.md` (new file, never `cp`, never retyped). 24283 bytes, byte-equal to the source (sha256 `4d9f218082307c01402af19a9f61c0ccbb6a78aa666910e96feeed5eff112689` both). Exempt from the 500-line cap as a verbatim single-`.agent/**`-state-file save (AGENTS.md Commit Discipline carve-out). |

### 3034a63a F106 R8 C0b: mirror round 8 block into last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +216/-416 (`git diff --numstat`; `git commit`'s own commit-time summary printed +400/-600 for this same commit — see Deviations) | C0b: `shutil.copyfile` of the committed `.agent/authored/f106-r8.md` into `.agent/last_block.md`. Byte-equal to the source, 24283 bytes each, sha256 `4d9f218082307c01402af19a9f61c0ccbb6a78aa666910e96feeed5eff112689` both. Exempt from the 500-line cap (verbatim single-state-file rewrite) regardless of which reading is used — both are far under 500. |

### 46b15d41 F106 R8 C1: rewrite plan.md for round 8
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +8/-13 | C1: rewritten from slice PLAN8 extracted from the committed `.agent/authored/f106-r8.md` using the marker convention (content starts the line after `<<<BEGIN`, ends WITH the newline before `<<<END`). Byte/sha256-equal to PLAN8 (`26f9dda00b7962ffc231b9f5e13fe1803bc012f467d494192319dd816b6acb1f` both), 36 lines (`wc -l`, under 50), holds `## Goal` (line 6) and `## Next Steps` (line 25). |

### 8d5ebeb3 F106 R8 C2: append RECORD8 verdict to live_review.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C2: append-only. Base 1828730 bytes + separator `\n` + RECORD8 (4611 bytes, inclusive of its trailing newline) = 1833342 bytes, matching the committed file exactly. Books the round 7 PASS verdict (T002c-i CLOSED); mints no new R-id or DECISION id. Exempt from the 500-line cap (verbatim single-state-file append). |

### 6a5c9116 F106 R8 C3: ReviewerOutput.resume_fallback + FakeProvider.review early-fail
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_provider.py` | +14/-0 | C3: applied the REVIEWEROUTPUT-FIELD and FAKEPROVIDER-REVIEW-EARLYFAIL pairs. `ReviewerOutput` gains `resume_fallback: bool = False` (mirrors `BuilderOutput.resume_fallback` from round 7). `FakeProvider.review` gains an early-return branch — `if resume and self._supports_resume and self._resume_fails:` returns `ReviewerOutput(error="resume_lost: session context unavailable", provider="fake")` — never on a plain (non-resume) call, and unreachable on every existing call site since every one constructs `FakeProvider()` with `resume_fails` left at its default `False`. `ClaudeProvider`/`ClaudeCliProvider` untouched. |

### 2e8e4049 F106 R8 C4: Reviewer call falls back once on resume error, same round
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +32/-0 | C4: applied the REVIEWER-CALL-FALLBACK pair. Immediately after the Reviewer's primary `_call_with_retry(...)` call, `if reviewer_resume_ref and reviewer_out.error:` fires a second, structurally parallel `_call_with_retry(...)` call with `resume=None` (fresh `_begin_stream_call`, fresh `reviewer_call_reasons = []`), and sets `reviewer_out.resume_fallback = True` on the fallback's own output. The fallback call reuses the exact same shape as the primary attempt above it — same `on_call=_rev_trace(...)`, same `on_provider_attempt=on_provider_call`, `stop_check=_stopped`, `rate_governor=_rate_governor` — only `resume=reviewer_resume_ref`→`resume=None` and the reset `reviewer_call_reasons` differ. Only fires when a resume was actually attempted (`reviewer_resume_ref` set); a plain call failure with no resume in play falls straight through to the existing, unpaired terminal-error / `malformed_output:` bounded parse-retry handling below, unchanged, and both of those run exactly once per round against whichever `reviewer_out` the fallback leaves behind. Only this call site changed — confirmed by `git diff` showing exactly ONE hunk in the file; the Builder call site (round 7's own fallback) and the bounded parse-retry call site are outside that hunk, confirmed byte-identical. `_build_provider_evidence` and `packages/orchestration/provider_token_evidence.py` confirmed untouched (`git diff --stat` empty for that file, checked both before and after this commit). |

### 99b6a45c F106 R8 C5: TestT002cReviewerFallbackOnce test coverage
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_session_resume.py` | +50/-3 | C5: applied TESTFILE-DOCSTRING-HEADER (rewrite), TESTFILE-DOCSTRING-T002C (rewrite) and TESTFILE-APPEND (append) pairs. Module docstring header now names T002c-ii; the T002c docstring paragraph is extended to describe both halves and states T002c CLOSED. New `TestT002cReviewerFallbackOnce` class with 3 tests: a resume error falls back and the round completes with `resume_fallback is True`/`resume_used is False`/`error == ""`/`final_status == "staged_review_passed"`; no fallback fires when no resume was attempted; no fallback fires when the provider doesn't support resume. `TestZeroBehaviorChange`, `TestT002aBuilderResumeThreading`, `TestT002bReviewerResumeThreading` and `TestT002cBuilderFallbackOnce` (all existing, round 7) untouched. |

### (this commit) F106 R8 C6: rewrite handoff for round 8 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (self-reference, not tabled per template exception) | C6: this handback, written once |

## External actions

- `git push` (after C6) — outcome reported in this round's completion message to the operator, per the write-once-handback convention; not re-run here.
- No PR created this round, per constraint 11 — T002c-ii closes T002c on both sides, but T002b-ii and T003 remain open on the feature.
- No worktree used this round — constraint 8 states this round's checks are all read-only against the primary checkout (imports, `ast.parse`, pytest runs); no destructive check and no worktree needed.
- No `gh pr list` Open PR Gate check re-run this round — this round continues the existing `feature/f106-session-resume` branch with no branch switch.

## Verification

### Item-status summary

Every bundle item and every gate, exactly once, with its real measured result:

| Item | Status | Real result |
|------|--------|-------------|
| C0a save block verbatim | done | 24283 bytes, sha256 `4d9f2180...12689` — 3-way equal to `.remedy-wt/f106-r8-block.md` |
| C0b mirror into last_block.md | done | 24283 bytes, sha256 equal to C0a's file |
| C1 rewrite plan.md (PLAN8) | done | sha256-equal to PLAN8, 36 lines, holds `## Goal`/`## Next Steps` |
| C2 append RECORD8 | done | 1828730 + 1 + 4611 = 1833342 bytes, matches committed file exactly |
| C3 pingpong_provider.py pairs | done | REVIEWEROUTPUT-FIELD + FAKEPROVIDER-REVIEW-EARLYFAIL, both FROM 1x→0x, TO 0x→1x |
| C4 pingpong_loop.py pair | done | REVIEWER-CALL-FALLBACK, FROM 1x→0x, TO 0x→1x, single hunk |
| C5 test file pairs | done | 2 rewrite pairs + 1 append pair, all shapes match constraint 12 |
| C6 rewrite handoff | done | this file, written once |
| G1 transport | PASS | 24283 = 24283, equal |
| G2 the plan | PASS | sha256-equal to PLAN8, 36 lines (<50), both headers present |
| G3 the record append | PASS | both readings (whole reconstruction, last blank-line unit) `True` |
| G4 the ledger | PASS | registered 318, resolved 55, DECISION 19 unmoved; `Gate: F106 R7 — ` 0x→1x across C2 |
| G5 pair shape + ordered application | PASS | all six pairs match constraint 12's expected shape; `ast.parse` exit 0 x2; `ruff check` exit 0 |
| G6 zero behavior change | PASS | exit 0, 122 passed (matches base) |
| G7 the new surface | PASS | exit 0, 26 passed (23 carried + 3 new, matches reviewer's stated count) |
| G8 state readers/canary/tree | PASS | exit 0 x5 (515/52/21/16/42, all match base); tree clean, 0 untracked, all commits <500 |

G1 TRANSPORT, at C0b — `.agent/authored/f106-r8.md` 24283 bytes, `.agent/last_block.md` 24283 bytes (`os.path.getsize` both). Equal. sha256 `4d9f218082307c01402af19a9f61c0ccbb6a78aa666910e96feeed5eff112689` for all three of `.agent/authored/f106-r8.md`, `.agent/last_block.md`, and the reviewer's own scratch original `.remedy-wt/f106-r8-block.md` — three-way equal.

G2 THE PLAN, at C1 — `.agent/plan.md` sha256-equal to slice PLAN8 (`26f9dda00b7962ffc231b9f5e13fe1803bc012f467d494192319dd816b6acb1f` both), 36 lines (`wc -l`, under 50), holds `## Goal` (line 6) and `## Next Steps` (line 25).

G3 THE RECORD APPEND, at C2 — base re-measured 1828730 bytes at `2a17ee63` (matches RECORD8's own stated base and the round 7 handback's committed reading exactly; C0a/C0b/C1 never touch `live_review.md`). Base + `\n` + RECORD8 (4611 bytes, inclusive of trailing newline) = 1833342 bytes = committed file's actual length. Reading (a) whole reconstruction: `True` (1828730 + 1 + 4611 = 1833342, matches `os.path.getsize` on the committed file). Reading (b) committed file's last blank-line unit (last 4611 bytes via `tail -c 4611`) equals RECORD8.txt exactly (`diff` empty): `True`.

G4 THE LEDGER, at C1 and C2 — same line-anchored regexes as constraint 5 (`^- R-\d+ — `, `^Done: (R-\d+) — `, `^DECISION F\d+ D\d+ — `). Registered: 318 matching lines. Resolved: 55 (distinct-id count over `Done:` lines; raw `Done:` line count is 57 due to `R-0721`/`R-0725` each carrying two `Done:` lines, same known wrinkle carried since round 5 — 55 is the correct reading). DECISION: 19 matching lines. All three unmoved between C1 and C2 (RECORD8 contains none of the three patterns as a new mint). `Gate: F106 R7 — ` line-anchored count: **0x** before C2 (base at `46b15d41`/C1), **1x** after (at HEAD, RECORD8's own header) — confirmed by direct regex against the pre-C2 and post-C2 file contents.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3-C5. Own containment test (`TO contains FROM`) and occurrence counts for each of the six pairs, run independently before/after each commit:
- REVIEWEROUTPUT-FIELD: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- FAKEPROVIDER-REVIEW-EARLYFAIL: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- REVIEWER-CALL-FALLBACK: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- TESTFILE-DOCSTRING-HEADER: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- TESTFILE-DOCSTRING-T002C: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- TESTFILE-APPEND: `TO contains FROM` = `True` (APPEND-shaped, as expected — FROM survives as TO's exact prefix). FROM 1x→1x, TO 0x→1x.

All six readings match the reviewer's stated expectations in constraint 12 exactly; no discrepancy to declare.

After C3/C4: `python3 -c "import ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"` real exit `0`. Same for `pingpong_loop.py`: real exit `0`. After C5: `python3 -m ruff check tests/orchestration/test_session_resume.py` real exit `0`, `All checks passed!`.

Constraint 14's confirmation: `FAKEPROVIDER-REVIEW-EARLYFAIL`'s new branch (`if resume and self._supports_resume and self._resume_fails:`) requires all three of `resume` truthy, `supports_resume=True` and `resume_fails=True` simultaneously — every existing call site in the repo constructs `FakeProvider()` with `resume_fails` left at its default `False`, so the branch can never fire on the pre-existing default path; G6 below is the run-time proof, and the existing, untouched `TestZeroBehaviorChange` class covers it.

Constraint 15's confirmation: `REVIEWER-CALL-FALLBACK`'s FROM/TO span starts right after the primary attempt's own `_call_with_retry(...)` call (unpaired, untouched, immediately above at what is now line ~3278-3297) and ends right before `_finalize_call(...)`. The fallback branch's own `_call_with_retry(...)` call, read directly in the pair's TO text, is structurally parallel to the primary attempt immediately above it — identical `role="reviewer"`, `provider=reviewer_name`, `on_call=_rev_trace(reviewer_effective, "review", "re-review" if is_repair else "review")`, `on_provider_attempt=on_provider_call`, `stop_check=_stopped`, `rate_governor=_rate_governor`; only `resume=reviewer_resume_ref` → `resume=None` and a reset `reviewer_call_reasons = []` differ. Reading the lines immediately following the pair's TO span in the committed file confirms `_finalize_call`, the `malformed_output:` bounded parse-retry, and the terminal-error handling below (all unpaired, untouched) run exactly once per round, against whichever `reviewer_out` the fallback logic leaves behind (the fallback's own result if a fallback fired, the primary attempt's result otherwise).

Constraint 16's confirmation, done BEFORE C4: `git diff --stat -- packages/orchestration/provider_token_evidence.py` — empty (untouched) both before C3/C4 and re-confirmed after C4. `git diff --stat -- packages/orchestration/pingpong_loop.py` was empty before C4 (confirming the Builder call site, with round 7's own fallback, and the parse-retry call site both still read byte-identical to the round's base immediately before this round's own C4 touched the file for the first time). A full `git diff -- packages/orchestration/pingpong_loop.py` after C4 shows exactly ONE hunk, at the Reviewer call site (starting at line 3295 onward) — the Builder call site and the bounded parse-retry call site are both outside that single hunk, confirmed byte-identical to their pre-C4 state.

G6 ZERO BEHAVIOR CHANGE ON THE DEFAULT PATH, at C3/C4 — `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q`: real exit `0`, `122 passed in 1.85s`, matching the reviewer's stated base of 122 exactly.

G7 THE NEW SURFACE, at C5 — `python3 -m pytest tests/orchestration/test_session_resume.py -q`: real exit `0`, `26 passed in 0.51s`, matching the reviewer's stated count of 26 exactly (the 23 carried in from round 7, unchanged, plus 3 new in `TestT002cReviewerFallbackOnce`). No discrepancy to declare, so `--collect-only` restatement was not additionally required.

G8 THE STATE READERS, CANARY AND THE TREE, after C2 — `tests/ui_server/`: real exit `0`, `515 passed in 31.78s`. `test_test_runner.py`: real exit `0`, `52 passed in 5.33s`. `test_resource_safety.py`: real exit `0`, `21 passed in 11.54s`. `test_integrity_gate.py`: real exit `0`, `16 passed in 0.30s`. Canary `test_golden_path.py`: real exit `0`, `42 passed in 20.59s`. All five match the reviewer's stated base (515/52/21/16/42) exactly.

Tree, at C5 (checked before writing this handback, since C6 necessarily dirties the tree until its own commit) — `git status --porcelain`: empty. `git ls-files --others --exclude-standard`: 0 untracked files. Every commit's insertions via `git diff --numstat <sha>^..<sha>`: 36cc5bcd 400, 3034a63a 216 (see Deviations for the commit-time-summary discrepancy), 46b15d41 8, 8d5ebeb3 2, 6a5c9116 14, 2e8e4049 32, 99b6a45c 50 — the first two are exempt from the 500-line cap as verbatim single-`.agent/**`-state-file saves/rewrites (AGENTS.md Commit Discipline carve-out); the latter five are ordinary code/test/state commits, all well under 500.

## Authored-text proofs

- The step block itself (`.agent/authored/f106-r8.md`) ← `.remedy-wt/f106-r8-block.md`: byte-equal, 24283 bytes both, sha256-equal (`4d9f218082307c01402af19a9f61c0ccbb6a78aa666910e96feeed5eff112689`), C0a. `.agent/last_block.md` mirror: byte-equal to the committed `.agent/authored/f106-r8.md`, sha256-equal, C0b.
- PLAN8 → `.agent/plan.md`: sha256-equal (`26f9dda00b7962ffc231b9f5e13fe1803bc012f467d494192319dd816b6acb1f` both), disk-to-disk, C1.
- RECORD8 → appended to `.agent/live_review.md`: byte-exact append arithmetic (1828730 + 1 + 4611 = 1833342) and both G3 readings `True`, C2.
- REVIEWEROUTPUT-FIELD-TO, FAKEPROVIDER-REVIEW-EARLYFAIL-TO → `packages/orchestration/pingpong_provider.py`: each TO occurs exactly 1x after commit, each FROM 0x, C3.
- REVIEWER-CALL-FALLBACK-TO → `packages/orchestration/pingpong_loop.py`: TO occurs exactly 1x after commit, FROM 0x, C4.
- TESTFILE-DOCSTRING-HEADER-TO, TESTFILE-DOCSTRING-T002C-TO, TESTFILE-APPEND-TO → `tests/orchestration/test_session_resume.py`: all confirmed by post-write counts (see G5 above), C5.

## Deviations & assumptions

One measurement discrepancy, declared rather than smoothed over per constraint 1's spirit (the commit itself is correct and unaffected — this is a reporting-method difference, not a defect in the committed bytes): for C0b (`3034a63a`), `git commit`'s own commit-time auto-printed summary read `1 file changed, 400 insertions(+), 600 deletions(-)`, but re-measuring the SAME commit afterward with `git diff --numstat 3034a63a^..3034a63a` (the exact method constraint/G8 names for the insertions-cap check) reads `216 416`. `git log --stat` on the same commit agrees with the `--numstat` reading (216/416), not with the commit-time message. Both readings are far under the 500-line cap and the commit is additionally exempt as a verbatim single-`.agent/**`-state-file rewrite, so this affects no gate's outcome; independent sha256/byte-count equality (G1) confirms the committed content of `.agent/last_block.md` is byte-for-byte correct regardless of which diffstat split is read. Root cause not investigated further (out of this round's scope) — plausibly a diff-heuristic difference between the porcelain commit-summary path and a plain `git diff --numstat` invocation on a full-file rewrite; flagged here rather than silently picking the friendlier number.

No other deviation. The bundle landed exactly as ordered — C0a, C0b, C1, C2, C3, C4, C5, C6 — one commit per bundle item (C3 applies both of its named pairs in a single commit, C5 applies all three of its named pairs in a single commit, matching the block's Bundle list of one commit per lettered item), no extra commit, no dropped commit, no reordering.

## Next

T002c-ii is CLOSED: the Reviewer side of the fallback-once rule (a resume attempt that errors falls back once, same round, to `resume=None`, recorded honestly on `ReviewerOutput.resume_fallback`, under the same gating as the Builder side) is landed, tested, and zero-behavior-change-proven on the default path. With both halves landed, **T002c is now CLOSED on both sides**. T002b-ii (the F111 delta-prompt shrink via existing diff-repair hunk selection) and T003 (measured fixture comparison + docs) both remain open. T002b-ii needs its own research pass into F111's hunk-selection code before a round can be designed for it — not started; that research pass, not a build round, is the expected next action. T003 follows once T002 is fully closed (i.e., after T002b-ii lands).
