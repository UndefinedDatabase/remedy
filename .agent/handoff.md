# Handoff — F106 Session resume instead of rebuild

## Session

SESSION 3 of feature F106 · round 9 · rounds so far 9

## Range

Review of `1470c3d74133906afc760b7d0a828a4900ae49cf..HEAD`.

## Commits

### bcd4dea5 F106 R9 C0a: save round 9 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f106-r9.md` | +395/-0 | C0a: `shutil.copyfile` of the round's step block from `.remedy-wt/f106-r9-block.md` (new file, never `cp`, never retyped). 35918 bytes, byte-equal to the source (sha256 `8467a03410b6d4c2d8915a6ddb7a0b8a1eee8e040b5e26feffd91ac4dfcba57c` both). Exempt from the 500-line cap as a verbatim single-`.agent/**`-state-file save (AGENTS.md Commit Discipline carve-out). |

### 13c5b8b3 F106 R9 C0b: mirror round 9 block into last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +313/-318 (`git diff --numstat`) | C0b: `shutil.copyfile` of the committed `.agent/authored/f106-r9.md` into `.agent/last_block.md`. Byte-equal to the source, 35918 bytes each, sha256 `8467a03410b6d4c2d8915a6ddb7a0b8a1eee8e040b5e26feffd91ac4dfcba57c` both — three-way equal with the reviewer's own scratch original `.remedy-wt/f106-r9-block.md`. Exempt from the 500-line cap (verbatim single-state-file rewrite) regardless. |

### 549109a9 F106 R9 C1: rewrite plan.md for round 9 (hoist step, D1)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +16/-11 | C1: rewritten from slice PLAN9 extracted from the committed `.agent/authored/f106-r9.md` using the marker convention (content starts the line after `<<<BEGIN`, ends WITH the newline before `<<<END`). Byte/sha256-equal to PLAN9 (`7d85b690799285aee85ba63c58e2e1b37e6e043cfe080fe37f0efc120fc4c911` both), 41 lines (`wc -l`, under 50), holds `## Goal` and `## Next Steps`. States SESSION 3, round 9. |

### e6f53a58 F106 R9 C2: append RECORD9, DECISION F106 D1, R-0758 to live_review.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6/-0 | C2: append-only, THREE paragraphs in order. Base 1833342 bytes + separator `\n` + RECORD9 (5274 bytes) + `\n` + DECISIONF106D1 (7098 bytes) + `\n` + R0758 (1802 bytes) = 1847519 bytes, matching the committed file exactly. Books the round 8 PASS verdict (T002c-ii CLOSED, T002c CLOSED in full), mints DECISION F106 D1 (the delta-prompt shrink's two-round split), and registers finding R-0758 (four `test_provider_retry.py` failures unrelated to this round, OPEN). Exempt from the 500-line cap (verbatim single-state-file append). |

### 78cfef55 F106 R9 C3: append session-numbering prose slip for round 8
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +2/-0 | C3: append-only. Base 34537 bytes + separator `\n` + PROSESLIPR8 (509 bytes) = 35047 bytes, matching the committed file exactly. Books the round 8 SESSION-numbering correction (should have read SESSION 3, not SESSION 2) as a dated prose line, no R-id, per amend0827-process-diet rule 2. Exempt from the 500-line cap (verbatim single-state-file append). |

### 1fe6b6d0 F106 R9 C4: hoist builder/reviewer resume-ref before prompt composition
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +33/-25 | C4: applied all four pairs (BUILDER-HOIST-REMOVE, BUILDER-HOIST-INSERT, REVIEWER-HOIST-REMOVE, REVIEWER-HOIST-INSERT). `builder_resume_ref` moves from immediately before the Builder's `_call_with_retry(...)` call to immediately before the `# --- Builder phase ---` / `repair_diff = ""` block (i.e. before `builder_composed` is built). `reviewer_resume_ref` moves from immediately before the Reviewer's `_call_with_retry(...)` call to immediately before `reviewer_composed = compose_reviewer_prompt(...)`. Each hoisted block carries one added 3-line comment naming this round and DECISION F106 D1; the CONDITION (`is_repair and getattr(provider, "supports_resume", False) and result.rounds`) and the session-id extraction logic are confirmed byte-identical between the pre-hoist and post-hoist text (verified directly, not assumed — see Verification, constraint 14). `packages/orchestration/pingpong_provider.py` and `packages/orchestration/provider_token_evidence.py` confirmed untouched, both before and after this commit. |

### (this commit) F106 R9 C5: rewrite handoff for round 9 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (self-reference, not tabled per template exception) | C5: this handback, written once |

## External actions

- `git worktree add .remedy-wt/f106-r9-negctrl HEAD --detach` (at commit `e6f53a58`, after C2) — created a disposable worktree to run the G3 negative control (constraint 8's one named exception). Outcome: worktree created cleanly at `e6f53a58`.
- One byte flipped inside the worktree copy's `.agent/live_review.md`, inside RECORD9 (the first appended paragraph, not the last), via a targeted script — never `cp`, no destructive action against the primary checkout.
- `git worktree remove .remedy-wt/f106-r9-negctrl --force` — removed cleanly; `git worktree list` afterward shows only the primary checkout at `e6f53a58 [feature/f106-session-resume]`; primary tree confirmed `git status --porcelain` empty immediately after.
- `git push` (after C5) — outcome reported in this round's completion message to the operator, per the write-once-handback convention; not re-run here.
- No PR created this round, per constraint 11 — this round closes only step 1 of T002b-ii (the hoist); step 2 (the actual delta-prompt shrink) and T003 both remain open.
- No `gh pr list` Open PR Gate check re-run this round — this round continues the existing `feature/f106-session-resume` branch with no branch switch.

## Verification

### Item-status summary

Every bundle item and every gate, exactly once, with its real measured result:

| Item | Status | Real result |
|------|--------|-------------|
| C0a save block verbatim | done | 35918 bytes, sha256 `8467a034...ba57c` — 3-way equal to `.remedy-wt/f106-r9-block.md` |
| C0b mirror into last_block.md | done | 35918 bytes, sha256 equal to C0a's file |
| C1 rewrite plan.md (PLAN9) | done | sha256-equal to PLAN9, 41 lines, holds `## Goal`/`## Next Steps` |
| C2 append RECORD9 + DECISIONF106D1 + R0758 | done | 1833342 + 1 + 5274 + 1 + 7098 + 1 + 1802 = 1847519 bytes, matches committed file exactly |
| C3 append PROSESLIPR8 | done | 34537 + 1 + 509 = 35047 bytes, matches committed file exactly |
| C4 pingpong_loop.py four pairs | done | all four FROM 1x→0x, TO 0x→1x; containment both-ways `False` for all four |
| C5 rewrite handoff | done | this file, written once |
| G1 transport | PASS | 35918 = 35918, equal, sha256 equal |
| G2 the plan | PASS | sha256-equal to PLAN9, 41 lines (<50), both headers present |
| G3 the record append | PASS | reading (a) whole reconstruction `True`; reading (b) last-3-paragraph-units `True`; reading (c) negative control in disposable worktree correctly REJECTED |
| G4 the ledger | PASS with one declared discrepancy from the block's own stated count — see below | registered 318→319, resolved unmoved 55, DECISION 19→20; `Gate: F106 R8 — ` measured 0x before C2, **2x** after (block's constraint 5 stated 1x) |
| G5 pair shape + ordered application | PASS | all four pairs match constraint 12's expected shape exactly; `ast.parse` exit 0; `ruff check` exit 0 |
| G6 zero behavior change | PASS | exit 0, 199 passed (matches reviewer's stated 122+26+51=199 exactly) |
| G7 the prose slip append | PASS | 35047 bytes matches; last blank-line unit byte-equal to PROSESLIPR8 |
| G8 the tree | PASS | `git status --porcelain` empty, 0 untracked, all commits <500 lines; `pingpong_provider.py`/`provider_token_evidence.py` diff --stat empty both before and after C4 |

### Detailed transcripts

G1 TRANSPORT, at C0b — `.agent/authored/f106-r9.md` 35918 bytes, `.agent/last_block.md` 35918 bytes (`len(open(path,'rb').read())` both). Equal. sha256 `8467a03410b6d4c2d8915a6ddb7a0b8a1eee8e040b5e26feffd91ac4dfcba57c` for all three of `.agent/authored/f106-r9.md`, `.agent/last_block.md`, and the reviewer's own scratch original `.remedy-wt/f106-r9-block.md` — three-way equal.

G2 THE PLAN, at C1 — `.agent/plan.md` sha256-equal to slice PLAN9 (`7d85b690799285aee85ba63c58e2e1b37e6e043cfe080fe37f0efc120fc4c911` both), 41 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2 — base re-measured 1833342 bytes at `1470c3d7` (matches the block's own stated base exactly; C0a/C0b/C1 never touch `live_review.md`). Three readings:
- (a) Whole reconstruction: base (1833342) + `\n` (1) + RECORD9 (5274) + `\n` (1) + DECISIONF106D1 (7098) + `\n` (1) + R0758 (1802) = 1847519, matching `len(open(path,'rb').read())` on the committed file exactly. `True`.
- (b) Structural reader over the WHOLE three-paragraph region: splitting the committed file on `\n\n` (blank-line units) and reading the last three units confirms unit[-3] == RECORD9, unit[-2] == DECISIONF106D1, unit[-1] == R0758, each byte-equal (accounting for the trailing newline convention: each unit plus its consumed `\n` reconstructs the slice exactly). `True`.
- (c) Negative control, in a disposable worktree (`git worktree add .remedy-wt/f106-r9-negctrl HEAD --detach` at `e6f53a58`): one byte flipped inside RECORD9 (offset 1833383, well inside the first appended paragraph, 40 bytes past its own header, not touching the marker line) — reading (b) applied to the mutated copy correctly reports unit[-3] != RECORD9 (`False`), while unit[-2] and unit[-1] still match (isolating the mutation to exactly the intended paragraph). REJECTED as required. `True`. Worktree removed afterward (`git worktree remove --force`), primary tree unaffected throughout.

G4 THE LEDGER, at C1 and C2 — same line-anchored regexes as constraint 5 (`^- R-\d+`, `^Done:\s*(R-\d+)`, `^DECISION F\d+ D\d+ — `). Registered: 318 before C2, 319 after (R-0758 added). Resolved: 55 distinct `Done:` ids, unmoved (unchanged by this round). DECISION: 19 before C2, 20 after (DECISION F106 D1 added). All match the block's stated expectations.

One declared discrepancy: `Gate: F106 R8 — ` (line-anchored substring count) measured **0x** before C2 and **2x** after — the block's own constraint 5 states "1x after — RECORD9's own header, not a new finding." The second occurrence is RECORD9's own G4 paragraph quoting itself: "`Gate: F106 R8 — ` exactly 0x before this entry" (its own self-referential measurement narrative, not a second finding or a second header). This is the SAME self-quoting pattern already present in the file for prior rounds' headers — independently confirmed `Gate: F106 R7 — ` already read 2x in `live_review.md` BEFORE this round's own C2 touched the file at all (RECORD8's own G4 paragraph quotes "`Gate: F106 R7 — ` exactly 0x before this entry" the same way). Applied byte-for-byte as instructed (constraint 1); declaring the measurement rather than treating the block's "1x" as ground truth or silently rounding it to match. No gate outcome changes: RECORD9 landed exactly once as a header, exactly as ordered.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C4. Own containment test (both ways) and occurrence counts for each of the four pairs, run independently before/after the commit:
- BUILDER-HOIST-REMOVE: `TO in FROM` = `False`, `FROM in TO` = `False`. FROM 1x→0x, TO 0x→1x.
- BUILDER-HOIST-INSERT: `TO in FROM` = `False`, `FROM in TO` = `False`. FROM 1x→0x, TO 0x→1x.
- REVIEWER-HOIST-REMOVE: `TO in FROM` = `False`, `FROM in TO` = `False`. FROM 1x→0x, TO 0x→1x.
- REVIEWER-HOIST-INSERT: `TO in FROM` = `False`, `FROM in TO` = `False`. FROM 1x→0x, TO 0x→1x.

All four match the reviewer's stated expectations in constraint 12 exactly; no discrepancy to declare.

After C4: `python3 -c "import ast; ast.parse(open('packages/orchestration/pingpong_loop.py').read())"` real exit `0`. `python3 -m ruff check packages/orchestration/pingpong_loop.py` real exit `0`, `All checks passed!`.

Constraint 14's confirmation, done directly rather than assumed: the CONDITION text `is_repair and getattr(builder_provider, "supports_resume", False) and result.rounds` / `is_repair and getattr(reviewer_provider, "supports_resume", False) and result.rounds` and the full session-id extraction block (`prev_*_out = result.rounds[-1].*_output` through `if prev_session_id: *_resume_ref = prev_session_id`) are present VERBATIM in both the REMOVE-FROM text (pre-hoist position) and the INSERT-TO text (post-hoist position) for both Builder and Reviewer — confirmed by direct substring containment, not by re-derivation. The only text present in INSERT-TO that is not present in REMOVE-FROM is one added comment (wrapped across 3 physical lines: "F106 T002b-ii step 1 (DECISION F106 D1): hoisted here, before / prompt composition, so a later round can gate the repair-diff [or safe-diff] segment on this same value without recomputing it.") plus pre-existing surrounding context lines (the closing `)` of the prior call, blank lines, the `# --- Builder phase ---` / `# F115 D1: compose...` comments) that were already elsewhere in the file and are simply now adjacent to the re-anchored block. Noting for precision: the block's constraint 14 phrase "one added comment line each" is, read literally, a 3-physical-line comment note, not a single line; the SUBSTANCE of constraint 14 (condition and extraction logic unchanged, only position moves) holds exactly as stated.

Constraint 15's confirmation, done BEFORE C4 and re-confirmed AFTER: `git diff --stat -- packages/orchestration/pingpong_provider.py packages/orchestration/provider_token_evidence.py` — empty both times.

G6 ZERO BEHAVIOR CHANGE (BROADENED SUITE per constraint 16), at C4 — `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py tests/orchestration/test_session_resume.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_builder_prompt_quality.py tests/orchestration/test_builder_prompt_hunk_rejections.py -q`: real exit `0`, `199 passed in 2.19s`, matching the reviewer's stated 122+26+51=199 exactly. Per-file breakdown (each run independently to confirm the sum): `test_pingpong.py` 34, `test_provider_mode.py` 24, `test_provider_evidence_integration.py` 64, `test_session_resume.py` 26, `test_builder_prompt_golden.py` 21, `test_builder_prompt_quality.py` 14, `test_builder_prompt_hunk_rejections.py` 16 — sum 199, real exit 0 on every file individually as well. `tests/orchestration/test_provider_retry.py` deliberately NOT run as part of this gate, per constraint and R-0758's own scope statement.

G7 THE PROSE SLIP APPEND, at C3 — base re-measured 34537 bytes (matches the block's implicit base). Base + `\n` + PROSESLIPR8 (509 bytes) = 35047 bytes = committed file's actual length (`True`). Committed file's last blank-line unit, split on `\n\n`, byte-equal to PROSESLIPR8 exactly (`True`).

G8 THE TREE, at C4 (rechecked before writing this handback, since C5 necessarily dirties the tree until its own commit) — `git status --porcelain`: empty. `git ls-files --others --exclude-standard`: 0 untracked files. Every commit's insertions via `git diff --numstat <sha>^..<sha>`: `bcd4dea5` 395, `13c5b8b3` 313, `549109a9` 16, `e6f53a58` 6, `78cfef55` 2, `1fe6b6d0` 33 — the first two are exempt from the 500-line cap as verbatim single-`.agent/**`-state-file saves/rewrites (AGENTS.md Commit Discipline carve-out); the latter four are ordinary code/state commits, all well under 500. `git diff --stat -- packages/orchestration/pingpong_provider.py packages/orchestration/provider_token_evidence.py`: empty, confirmed both before and after C4.

## Authored-text proofs

- The step block itself (`.agent/authored/f106-r9.md`) ← `.remedy-wt/f106-r9-block.md`: byte-equal, 35918 bytes both, sha256-equal (`8467a03410b6d4c2d8915a6ddb7a0b8a1eee8e040b5e26feffd91ac4dfcba57c`), C0a. `.agent/last_block.md` mirror: byte-equal to the committed `.agent/authored/f106-r9.md`, sha256-equal, C0b.
- PLAN9 → `.agent/plan.md`: sha256-equal (`7d85b690799285aee85ba63c58e2e1b37e6e043cfe080fe37f0efc120fc4c911` both), disk-to-disk, C1.
- RECORD9, DECISIONF106D1, R0758 → appended to `.agent/live_review.md`: byte-exact append arithmetic (1833342 + 1 + 5274 + 1 + 7098 + 1 + 1802 = 1847519) and all three G3 readings `True` (including the disposable-worktree negative control), C2.
- PROSESLIPR8 → appended to `.agent/prose_slips.md`: byte-exact append arithmetic (34537 + 1 + 509 = 35047) and the G7 last-unit reading `True`, C3.
- BUILDER-HOIST-INSERT-TO, REVIEWER-HOIST-INSERT-TO → `packages/orchestration/pingpong_loop.py`: each TO occurs exactly 1x after the commit, each corresponding FROM 0x, C4. Condition/extraction logic confirmed byte-identical to pre-hoist form (constraint 14, see Verification).

## Deviations & assumptions

Two declared observations, neither a defect on disk (constraint 1's spirit — applied byte-for-byte as given, declaring rather than fixing or smoothing over):

1. G4's `Gate: F106 R8 — ` occurrence count reads 2x after C2, not the 1x stated in the block's own constraint 5. The second occurrence is RECORD9's own G4 paragraph quoting the phrase "`Gate: F106 R8 — ` exactly 0x before this entry" as part of its self-referential measurement narrative — the same self-quoting shape already established for `Gate: F106 R7 — ` (also 2x, present before this round's own C2 ever touched the file) and, by the same pattern, presumably `Gate: F106 R6 — ` before it. Nothing on disk is wrong — RECORD9 landed exactly once as an actual header — but the block's literal "1x" undercounts by exactly the self-quote, and I did not alter RECORD9's text to make the count match.

2. Constraint 14 says the hoisted blocks are "byte-identical... except for one added comment line each." Measured directly: the added comment is one coherent note wrapped across 3 physical lines (not 1), for each of the Builder and Reviewer sites. The SUBSTANCE constraint 14 actually gates — the CONDITION and session-id extraction logic being unchanged, only their position moving — holds exactly, confirmed by direct substring containment (see Verification). No code was altered because of this; it is a word-choice imprecision in the block's own prose, applied as given.

No other deviation. The bundle landed exactly as ordered — C0a, C0b, C1, C2, C3, C4, C5 — one commit per bundle item, no extra commit, no dropped commit, no reordering. The one worktree used this round (for the G3(c) negative control) was created and removed exactly as constraint 8 scoped it, and never touched the primary checkout.

## Next

T002b-ii step 1 (the hoist) is CLOSED: `builder_resume_ref`/`reviewer_resume_ref` now compute before their respective prompt-composition call sites, zero-behavior-change-proven against the broadened 199-test suite. T002b-ii step 2 (the actual delta-prompt shrink — gating a hunk-selected repair-diff rendering on the hoisted resume-ref, reusing `select_repair_hunks`/`parse_diff_line_ranges` per DECISION F106 D1) remains open and is NOT started: it still needs a new hunk-rendering convention invented and frozen (none exists to borrow), and confirmation of whether the three `test_builder_prompt_*.py` files need updating once that rendering lands. T003 (measured fixture comparison + docs) follows once T002 is fully closed, i.e. after step 2 lands. R-0758 (four pre-existing `test_provider_retry.py` failures, `resume` kwarg gap in four test-only provider subclasses) is registered OPEN, not fixed this round — left for a future round to add `resume: str | None = None` to the four affected signatures.
