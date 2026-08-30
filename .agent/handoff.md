# Handoff — F106 Session resume instead of rebuild

## Session

SESSION 2 of feature F106 · round 7 · rounds so far 7

## Range

Review of `e41b96395dd4251fd458c37fe37d2e3065a1633b..HEAD`.

## Commits

### e1ddd7f2 F106 R7 C0a: save round 7 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f106-r7.md` | +600/-0 | C0a: `shutil.copyfile` of the round's step block from the reviewer's scratch original `.remedy-wt/f106-r7-block.md` (new file, never `cp`, never retyped). 30595 bytes, byte-equal to the source (sha256 `0e918483ed59840630d8c69430f5b8cb2ef68e0063b28ea2550fdd138c175dba` both). Exempt from the 500-line cap as a verbatim single-`.agent/**`-state-file save (AGENTS.md Commit Discipline carve-out). |

### de0e56c3 F106 R7 C0b: mirror block into last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +310/-243 | C0b: `shutil.copyfile` of the committed `.agent/authored/f106-r7.md` into `.agent/last_block.md`. Byte-equal to the source, 30595 bytes each, sha256 `0e918483ed59840630d8c69430f5b8cb2ef68e0063b28ea2550fdd138c175dba` both. Exempt from the 500-line cap (verbatim single-state-file rewrite). |

### daa81110 F106 R7 C1: rewrite plan.md for round 7
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +14/-14 | C1: rewritten from slice PLAN7 extracted from the committed `.agent/authored/f106-r7.md` using the marker convention (content starts the line after `<<<BEGIN`, ends WITH the newline before `<<<END`) verified correct across prior rounds. Byte/sha256-equal to PLAN7 (`018804af6767866f42c8f01ee531d1dfdae3eafee2bf37037fdbca80c2b261eb` both), 41 lines (`wc -l`, under 50), holds `## Goal` (line 6) and `## Next Steps` (line 25). Exempt from the 500-line cap (verbatim single-state-file rewrite). |

### 1204330a F106 R7 C2: append RECORD7 verdict to live_review.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C2: append-only. Base 1826027 bytes + separator `\n` + RECORD7 (2702 bytes, inclusive of its trailing newline) = 1828730 bytes, matching the committed file exactly. Books the round 6 PASS verdict (T002b-i CLOSED); mints no new R-id or DECISION id. Exempt from the 500-line cap (verbatim single-state-file append). |

### f7fb3c84 F106 R7 C3: add resume_fallback field and FakeProvider resume-fail hook
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_provider.py` | +15/-0 | C3: applied the BUILDEROUTPUT-FIELD, FAKEPROVIDER-INIT and FAKEPROVIDER-BUILD pairs. `BuilderOutput` gains `resume_fallback: bool = False`. `FakeProvider.__init__` gains a test-only `resume_fails: bool = False` override. `FakeProvider.build` returns a `resume_lost: session context unavailable` error only when `resume` is truthy AND `self._supports_resume` AND `self._resume_fails` — never on a plain (non-resume) call, and never with either flag left at its default. `ClaudeProvider`/`ClaudeCliProvider` untouched. |

### b7624e63 F106 R7 C4: Builder call falls back once on resume error, same round
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +26/-0 | C4: applied the BUILDER-CALL-FALLBACK pair. Immediately after the Builder's primary `_call_with_retry(...)` call, `if builder_resume_ref and builder_out.error:` fires a second, structurally parallel `_call_with_retry(...)` call with `resume=None` (fresh `_begin_stream_call`, fresh `builder_call_reasons`), and sets `builder_out.resume_fallback = True` on the fallback's own output. Only fires when a resume was actually attempted (`builder_resume_ref` set); a plain call failure with no resume in play falls straight through to the existing, unpaired terminal-error handling below, unchanged. Only this call site changed — the Reviewer call site and the bounded parse-retry call site are outside the diff's single hunk, confirmed byte-identical. `_build_provider_evidence` and `packages/orchestration/provider_token_evidence.py` confirmed untouched (`git diff --stat` empty for that file). |

### 88827371 F106 R7 C5: add TestT002cBuilderFallbackOnce test coverage
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_session_resume.py` | +52/-3 | C5: applied TESTFILE-DOCSTRING (rewrite) and TESTFILE-APPEND (append) pairs. Docstring extended to describe T002c-i's coverage. New `TestT002cBuilderFallbackOnce` class with 3 tests: a resume error falls back and the round completes with `resume_fallback is True`/`resume_used is False`; no fallback fires when no resume was attempted; no fallback fires when the provider doesn't support resume. `TestZeroBehaviorChange`, `TestT002aBuilderResumeThreading` and `TestT002bReviewerResumeThreading` (all existing) untouched. |

### (this commit) F106 R7 C6: rewrite handoff for round 7 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (self-reference, not tabled per template exception) | C6: this handback, written once |

## External actions

- `git push` (after C6) — outcome reported in this round's completion message to the operator, per the write-once-handback convention; not re-run here.
- No PR created this round, per constraint 11 (T002c-i closes only one more slice of T002; T002b-ii, T002c-ii, T003 remain).
- No worktree used this round — constraint 8 states this round's checks are all read-only against the primary checkout (imports, `ast.parse`, pytest runs); no destructive check and no worktree needed.
- No `gh pr list` Open PR Gate check re-run this round — this round continues the existing `feature/f106-session-resume` branch with no branch switch.

## Verification

G1 TRANSPORT, at C0b — `.agent/authored/f106-r7.md` 30595 bytes, `.agent/last_block.md` 30595 bytes (`wc -c`/`os.path.getsize` both). Equal. sha256 `0e918483ed59840630d8c69430f5b8cb2ef68e0063b28ea2550fdd138c175dba` both, and equal to the reviewer's own held original `.remedy-wt/f106-r7-block.md` (three-way equal, confirmed by `.remedy-wt/r7/c0a.py`/`c0b.py`).

G2 THE PLAN, at C1 — `.agent/plan.md` sha256-equal to slice PLAN7 (`018804af6767866f42c8f01ee531d1dfdae3eafee2bf37037fdbca80c2b261eb` both), 41 lines (`wc -l`, under 50), holds `## Goal` (line 6) and `## Next Steps` (line 25).

G3 THE RECORD APPEND, at C2 — base re-measured 1826027 bytes (matches the round 6 handback's committed reading exactly; C0a/C0b/C1 never touch `live_review.md`). Base + `\n` + RECORD7 (2702 bytes, inclusive of trailing newline) = 1828730 bytes = committed file's actual length, confirmed by direct read via `.remedy-wt/r7/c2.py`. Reading (a) whole reconstruction: `True`. Reading (b) last blank-line unit equals RECORD7 exactly: `True`.

G4 THE LEDGER, at C1 and C2 — same line-anchored regexes as constraint 5 (`^- (R-\d{4}) — `, `^Done: (R-\d{4}) — `, `^DECISION F\d+ D\d+ — `), run via `.remedy-wt/r7/ledger.py`. Registered: 318 (318 matching lines, all distinct ids). Resolved: 55 (distinct-id count; raw `Done:` line count is 57 due to `R-0721`/`R-0725` each carrying two `Done:` lines, same known wrinkle as rounds 5/6 — 55 is the correct reading). DECISION: 19 matching lines. All three unmoved between C1 and C2 (RECORD7 contains none of the three patterns). `Gate: F106 R6 — ` line-anchored count: **0x** before C2 (base at `daa81110`/C1), **1x** after (at HEAD, RECORD7's own header) — confirmed by direct regex against the pre-C2 and post-C2 file contents.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3-C5. Own containment test (`TO contains FROM`) and occurrence counts for each of the six pairs, run independently via `.remedy-wt/r7/pair_tools.py` (`report()`) before/after each commit:
- BUILDEROUTPUT-FIELD: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- FAKEPROVIDER-INIT: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- FAKEPROVIDER-BUILD: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- BUILDER-CALL-FALLBACK: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- TESTFILE-DOCSTRING: `TO contains FROM` = `False` (REWRITE, as expected). FROM 1x→0x, TO 0x→1x.
- TESTFILE-APPEND: `TO contains FROM` = `True` (APPEND-shaped, as expected — FROM survives as TO's exact prefix). FROM 1x→1x, TO 0x→1x.

All six readings match the reviewer's stated expectations in constraint 12 exactly; no discrepancy to declare.

After C3/C4: `python3 -c "import ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"` real exit `0`. Same for `pingpong_loop.py`: real exit `0`. After C5: `python3 -m ruff check tests/orchestration/test_session_resume.py` real exit `0`, `All checks passed!`.

Constraint 14's confirmation: `FAKEPROVIDER-BUILD`'s new branch (`if resume and self._supports_resume and self._resume_fails:`) requires all three of `resume` truthy, `supports_resume=True` and `resume_fails=True` simultaneously — every existing call site in the repo constructs `FakeProvider()` with `resume_fails` left at its default `False`, so the branch can never fire on the pre-existing default path; G6 below is the run-time proof.

Constraint 15's confirmation: `BUILDER-CALL-FALLBACK`'s fallback branch's own `_call_with_retry(...)` call, read directly in the pair's TO text, is structurally parallel to the primary attempt immediately above it — identical `role="builder"`, `provider=builder_name`, `on_provider_attempt=on_provider_call`, `stop_check=_stopped`, `rate_governor=_rate_governor`; only `resume=builder_resume_ref` → `resume=None` and a reset `builder_call_reasons = []` differ. Reading the ~10 lines immediately following the pair's TO span in the committed file confirms `rd.builder_output = builder_out` → `_finalize_call(...)` → the unpaired terminal-error `if builder_out.error:` block run exactly ONCE per round, against whichever `builder_out` the fallback logic leaves behind (the fallback's own result if a fallback fired, the primary attempt's result otherwise).

Constraint 16's confirmation, done BEFORE C4: `git diff --stat -- packages/orchestration/provider_token_evidence.py` — empty (untouched), re-confirmed again after C4. A full `git diff -- packages/orchestration/pingpong_loop.py` after C4 shows exactly ONE hunk, at the Builder call site (lines 3037-3038 onward) — the Reviewer call site (`reviewer_out = _call_with_retry(...)`, now at line 3278) and the bounded parse-retry call site (`retry_out = _call_with_retry(...)`, now at line 3336) are both outside that single hunk, so both are confirmed byte-identical to their state at the round's base; the ~26-line downward shift in their line numbers is exactly the BUILDER-CALL-FALLBACK insertion's own line count, not a content change.

G6 ZERO BEHAVIOR CHANGE ON THE DEFAULT PATH, at C3/C4 — `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q`: real exit `0`, `122 passed in 1.83s`, matching the reviewer's stated base of 122 exactly.

G7 THE NEW SURFACE, at C5 — `python3 -m pytest tests/orchestration/test_session_resume.py -q`: real exit `0`, `23 passed in 0.44s`, matching the reviewer's stated count of 23 exactly (the 20 carried in from round 6, unchanged, plus 3 new in `TestT002cBuilderFallbackOnce`). No discrepancy to declare, so `--collect-only` restatement was not additionally required.

G8 THE STATE READERS AND CANARY, after C2 — `tests/ui_server/`: real exit `0`, `515 passed in 31.92s`. `test_test_runner.py`: real exit `0`, `52 passed in 5.35s`. `test_resource_safety.py`: real exit `0`, `21 passed in 11.51s`. `test_integrity_gate.py`: real exit `0`, `16 passed in 0.29s`. Canary `test_golden_path.py`: real exit `0`, `42 passed in 20.49s`. All five match the reviewer's stated base (515/52/21/16/42) exactly.

G9 THE TREE, at C5 (checked before writing this handback, since C6 necessarily dirties the tree until its own commit) — `git status --porcelain`: empty. `git ls-files --others --exclude-standard`: 0 untracked files. Every commit's insertions via `git diff --numstat <sha>^..<sha>`: e1ddd7f2 600, de0e56c3 310, daa81110 14, 1204330a 2, f7fb3c84 15, b7624e63 26, 88827371 52 — the first two are exempt from the 500-line cap as verbatim single-`.agent/**`-state-file saves/rewrites (AGENTS.md Commit Discipline carve-out); the latter five are ordinary code/test/state commits, all well under 500.

## Authored-text proofs

- The step block itself (`.agent/authored/f106-r7.md`) ← `.remedy-wt/f106-r7-block.md`: byte-equal, 30595 bytes both, sha256-equal (`0e918483ed59840630d8c69430f5b8cb2ef68e0063b28ea2550fdd138c175dba`), C0a. `.agent/last_block.md` mirror: byte-equal to the committed `.agent/authored/f106-r7.md`, sha256-equal, C0b.
- PLAN7 → `.agent/plan.md`: sha256-equal (`018804af6767866f42c8f01ee531d1dfdae3eafee2bf37037fdbca80c2b261eb` both), disk-to-disk, C1.
- RECORD7 → appended to `.agent/live_review.md`: byte-exact append arithmetic (1826027 + 1 + 2702 = 1828730) and both G3 readings `True`, C2.
- BUILDEROUTPUT-FIELD-TO, FAKEPROVIDER-INIT-TO, FAKEPROVIDER-BUILD-TO → `packages/orchestration/pingpong_provider.py`: each TO occurs exactly 1x after commit, each FROM 0x — confirmed by `.remedy-wt/r7/run_pairs_c3.py`'s post-write counts, C3.
- BUILDER-CALL-FALLBACK-TO → `packages/orchestration/pingpong_loop.py`: TO occurs exactly 1x after commit, FROM 0x, C4.
- TESTFILE-DOCSTRING-TO, TESTFILE-APPEND-TO → `tests/orchestration/test_session_resume.py`: both confirmed by `.remedy-wt/r7/run_pairs_c5.py`'s post-write counts (see G5 above), C5.

## Deviations & assumptions

None. The bundle landed exactly as ordered — C0a, C0b, C1, C2, C3, C4, C5, C6 — one commit per bundle item (C3 applies all three of its named pairs in a single commit, C5 applies both of its named pairs in a single commit, matching the block's Bundle list of one commit per lettered item), no extra commit, no dropped commit, no reordering.

## Next

T002c-i is CLOSED: the Builder side of the fallback-once rule (a resume attempt that errors falls back once, same round, to `resume=None`, recorded honestly on `BuilderOutput.resume_fallback`) is landed, tested, and zero-behavior-change-proven on the default path. T002b-ii (the F111 delta-prompt shrink via existing diff-repair hunk selection) and T002c-ii (the identical fallback-once mirror on the Reviewer side) both remain open. T002b-ii needs its own research pass into F111's hunk-selection code before a round can be designed for it — not started. T003 (measured fixture comparison + docs) follows once T002 is fully closed.
