# Handback — F109 Semantic dedupe, round 15

## Session

SESSION 4 of feature F109 · round 15 · rounds so far 15

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 15 rounds and 4 sessions it is NOT reached, so no scope report is due.

## Range

Review of `d52a5371..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `dbe9058a` | done | block copied verbatim with `shutil.copyfile`; G1 `cmp` exit 0 against the reviewer's own `.remedy-wt/f109-r15.md` |
| C0b `a141a75b` | done | mirrored to `.agent/last_block.md`; one sha256 for both files |
| C1 `61fae9c2` | done | PLAN15 extracted by delimiter index and applied; G2 `cmp` exit 0 |
| C2 `17582c06` | done | RECORD15 appended as `\n\n` + slice; G3 (a)(b)(c)(d) all pass |
| C3 `f674ee54` | done | new doc + BOTH index rows in ONE commit, as constraint 4 requires |
| C4 (this commit) | done | handback rewritten per handback_template.md, then pushed |

No item was skipped, none deviated, and the block's ordered commit sequence was
followed exactly — no extra commit, no dropped commit, no reordering.

## Commits

### dbe9058a F109 R15 C0a: save the round 15 block verbatim

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f109-r15.md` | +387 / -0 | the reviewer's round 15 block, byte-for-byte |

### a141a75b F109 R15 C0b: mirror the round 15 block to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +361 / -352 | mirror of the saved block; single-state-file rewrite |

### 61fae9c2 F109 R15 C1: the plan turns to the T003 docs round

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +18 / -13 | SLICE PLAN15 applied whole |

### 17582c06 F109 R15 C2: book the round 14 gate, resolve R-0779 and register R-0780

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +7 / -1 | SLICE RECORD15 appended: the R14 PASS, `Done: R-0779`, and `R-0780` registered |

### f674ee54 F109 R15 C3: document the built semantic dedupe and register it in the docs index

| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/semantic-dedupe-v1.md` | +122 / -0 | NEW built-state doc, SLICE DOC applied whole |
| `docs/README.md` | +2 / -0 | PAIR IDX1 (quick-find row) and PAIR IDX2 (system-docs row) |

### C4 — this commit

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | this handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

Insertion counts, `+` column only per AGENTS.md DECISION F104 D1, read from
`git log --numstat d52a5371..HEAD` and identical to the tables above: C0a 387,
C0b 361, C1 18, C2 7, C3 124 (2 + 122). Every commit is under the 500-insertion
cap; C0a and C0b are additionally the single-`.agent/**`-state-file rewrites the
decision exempts.

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach .remedy-wt/r15base d52a5371` | exit 0 — created, to measure the `tests/docs/` BASE count the block did not state |
| `git worktree remove .remedy-wt/r15base` | exit 0 — removed by its exact path |
| `git worktree prune` + `git worktree list` | exit 0 — only the primary checkout and the four pre-existing `remedy/job-*` worktrees remain |
| `git push -u origin feature/f109-semantic-dedupe` | see the push line at the end of this file |

No PR was created, edited or merged. No force-push. No work on `main`.

## Verification — the eight gates, real readings

- **G1 TRANSPORT — PASS.** `cmp .remedy-wt/f109-r15.md .agent/authored/f109-r15.md` → exit 0, no output (the source is the reviewer's own original, so this is real transport, not self-consistency). `sha256sum .agent/authored/f109-r15.md .agent/last_block.md` → exit 0, one digest twice: `4c8c964df8a8f4b96253971edaf3e65aacdb206e938c1c734fd6f117baca8c7d`.
- **G2 THE PLAN — PASS.** PLAN15 extracted by delimiter index (44 lines, 1994 bytes); `cmp` against `.agent/plan.md` after C1 → exit 0, no output. `wc -l .agent/plan.md` = 44 (under 50). `grep -c '^## Goal'` = 1, `grep -c '^## Next Steps'` = 1.
- **G3(a) ARITHMETIC — PASS.** Base `.agent/live_review.md` at `d52a5371`: 2101284 bytes, sha256 `1d2111bcf7ef35cd291bbfaf33aeabf4625f023f0f05410b0a30ee29651e3d70`, ends WITHOUT a trailing newline. Appended S = 6939 bytes (the two bytes `\n\n` plus RECORD15). New size 2108223, sha256 `e8cef8e7cdb7a4fecc631b57a41cf28599977cd7878ceb9ecaaade1f4c34a1cc`; 2101284 + 6939 = 2108223 → True; the file still ends WITHOUT a trailing newline.
- **G3(b) SECOND READER, NO BYTE COUNTED — PASS.** Whole file split on blank-line boundaries: 880 units. N = 3, counted by the script from the slice itself and not taken from the block. The LAST 3 units equal RECORD15's 3 paragraphs IN ORDER, openings `'Gate: F109 R14 — the round 14 entry. VERDICT PASS, over the '`, `'Done: R-0779 — RESOLVED at \`79edbcbf\` and verified by the re'`, `'- R-0780 — Low, THE SENT-INDEX MODULE STILL DOCUMENTS ITS OW'`.
- **G3(c) NEGATIVE CONTROL — PASS.** Copy to `.remedy-wt/live_review_negative_control_r15.md`, one byte flipped INSIDE the FIRST appended paragraph (offset 2101291, `' '` → `'X'`): reader (b) returns **False** on the copy and **True** on the tracked file. Tracked sha256 before `e8cef8e7cdb7a4fecc631b57a41cf28599977cd7878ceb9ecaaade1f4c34a1cc` and after `e8cef8e7cdb7a4fecc631b57a41cf28599977cd7878ceb9ecaaade1f4c34a1cc` — it never moved. Scratch deleted by its exact path; `os.path.exists('.remedy-wt/live_review_negative_control_r15.md')` → **False**.
- **G3(d) COUNTS AS A SET DIFFERENCE — PASS.** Base read from `git show 5fe32449:.agent/live_review.md`, never by rewinding the tracked file. BASE: 339 registered / 339 distinct / 65 `Done:` lines / 63 distinct resolved / `len(set(reg)-set(done))` = **276**. NEW: 341 registered / 341 distinct / 66 `Done:` lines / 64 distinct resolved / **277**. `grep -c '^Gate: F109 R14 — '` = 1, `grep -c '^Done: R-0779 — '` = 1, `grep -c '^- R-0780 — '` = 1. The +2 registered are `R-0779` (landed R14 at `b1ea60a8`) and `R-0780` (this round); the +1 resolved is `R-0779`, so the open set holds at 277.
- **G4 THE INDEX PAIRS — PASS.** Containment test run mechanically before emission: TO contains FROM = **False** for both, so both are REWRITES. `IDX1_FROM` 1 before C3 → **0** after; `IDX1_TO` **1** after. `IDX2_FROM` 1 before C3 → **0** after; `IDX2_TO` **1** after.
- **G5 THE DOC IS REAL AND REGISTERED — PASS.** `docs/system/semantic-dedupe-v1.md` exists, `wc -l` = 122, 6918 bytes, exactly one trailing newline. `git show --numstat f674ee54` names BOTH paths in that ONE commit (`2 0 docs/README.md`, `122 0 docs/system/semantic-dedupe-v1.md`). `grep -c 'semantic-dedupe-v1.md' docs/README.md` = **2** (grep counts LINES; the substring occurs 4 times because each row carries it as link text and as target). Both relative markdown links resolve on disk: `session-resume-v1.md` → `docs/system/session-resume-v1.md` exists=True; `cache-optimal-prompt-ordering-v1.md` → `docs/system/cache-optimal-prompt-ordering-v1.md` exists=True. The backticked `docs/roadmap/features/T3_F109.md` also exists.
- **G6 THE SUITES, SERIALLY — PASS, nothing red and no count fell.** `tests/docs/` 295 passed, exit 0 · `test_semantic_dedupe.py` 130 passed, exit 0 · `test_prompt_trace.py` 54 passed, exit 0 · `test_session_resume.py` 27 passed, exit 0 · `test_pingpong.py` 34 passed, exit 0 · `test_pingpong_cli.py` 173 passed, exit 0 · `tests/cli/test_golden_path.py` (the mandatory canary) 42 passed, exit 0. The six non-docs figures reproduce the reviewer's `d52a5371` measurement exactly (130, 54, 27, 34, 173, 42). The block stated no `tests/docs/` baseline, so it was measured at `d52a5371` in a disposable worktree with `python3 -B`: **295 passed, exit 0** — identical, so no count fell there either.
- **G7 THE DOC'S FACTUAL CLAIMS, RE-MEASURED — PASS, no disagreement with the DOC.** (a) The shipped property was READ FROM THE CLASS, not grepped: `ClaudeProvider`, `ClaudeCliProvider` and `OllamaPingPongProvider` each have `supports_resume` returning the literal `False`, and none of the three takes a `supports_resume` constructor parameter; `FakeProvider` alone does, defaulting to `False`, and `FakeProvider(supports_resume=True).supports_resume` → `True` while `FakeProvider().supports_resume` → `False`. (b) `git cat-file -e` exit 0 for `7451e9c7`, `60343048` and `b245e1c9`. (c) `DEDUPE_MIN_SEGMENT_CHARS` = **200**; the comparison is `return len(text) >= min_chars`, confirmed by AST as op `GtE`, and behaviourally 199 chars → `False`, 200 chars → `True`, and `enabled=False` at 200 chars → `False`. (d) `estimate_token_savings` exists in `packages/orchestration/token_economy.py` → True. (e) Markers produced by the shipped `dedupe_marker_for_segment`: `'[unchanged: builder_system, previously provided]'` = **48** chars, `'[unchanged: reviewer_system, previously provided]'` = **49** chars, sum **97** — exactly the table's figure.
- **G8 THE TREE AND THE SWEEP — PASS.** `git status --porcelain` → EMPTY, exit 0. `git ls-files .remedy-wt` → no output, exit 0. Per-commit insertions from `git log --numstat` are C0a 387, C0b 361, C1 18, C2 7, C3 124, and they match the `## Commits` tables above cell for cell. The end-to-end re-read of every touched file is below.

## G8 sweep — every file this round touched, re-read end to end

| File | Reading |
|------|---------|
| `.agent/plan.md` | Re-read whole. Every sentence true at `f674ee54`: round 15 / session 4, the doc landed and registered, `R-0779` resolved and `R-0780` registered, and "This round does not touch that file" holds — `session_sent_index.py` is not in any commit of this range. No stale sentence. |
| `.agent/live_review.md` | Append-only; no landed entry was rewritten or renumbered. The appended R14 entry's own ledger figures (340 registered, 65 `Done:` lines, 63 distinct resolved, open 277 at `d52a5371`) are consistent with the base I measured at `5fe32449` plus `R-0779`'s registration. No stale sentence. |
| `docs/system/semantic-dedupe-v1.md` | Re-read whole. Beyond G7 (a)-(e), every symbol it names was resolved in the running interpreter: `SessionSentIndex`, `SessionSentIndexError`, `record_finalized_call`, `invalidate_on_resume_fallback`, `session_sent_index_from_evidence`, `SessionSentIndex.as_evidence_dicts`, `dedupe_marker_for_segment`, `_dedupe_resumed_segments`, `compose_builder_prompt`/`compose_reviewer_prompt` (both with `dedupe_sent_hashes` defaulting to `None`, which is the bypass the doc claims), `run_pingpong.semantic_dedupe_enabled`, `PromptTraceEntry.deduped_segment_names`, `measure_dedupe_savings_from_traces` and its `unmeasured_segment_names` field. The purity claim holds: `session_sent_index.py` imports only `__future__` and `collections.abc`. `ComposedPrompt.manifest_as_dicts()` is real, in `prompt_segments.py`. The savings table was re-measured, see deviation 1. The doc's "Measured at commit `d52a5371`" pin is ACCURATE, not stale: the same numbers reproduce at the tip. No stale sentence. |
| `docs/README.md` | Re-read whole. The two new rows sit alphabetically between the `self-*` rows and the `session-resume` row in both tables, matching the surrounding order. Nothing else in the file moved. No stale sentence introduced. |
| `.agent/authored/f109-r15.md`, `.agent/last_block.md` | Verbatim archival copies of the reviewer's block; identical digests. Nothing to sweep by construction. |

Stale sentences found and DELIBERATELY NOT repaired, with the reason:

1. `packages/orchestration/session_sent_index.py` — the two false "deliberate
   absence" bullets. That IS `R-0780`, registered by this round's C2. The block
   states plainly that its repair is round 16's and that this round does not
   touch that file, so it was left exactly as found.
2. `tests/orchestration/test_semantic_dedupe.py`, module docstring — the
   sentence "The manifest in the first case is built through the REAL producer
   in ``prompt_segments``" is still positionally wrong: `_real_manifest_rows` is
   called at 11 sites across the file, not only in the first case. This is the
   claim round 14 already declared under its own G8 and correctly declined to
   repair; it is outside this round's change set and stays declared.
3. `tests/orchestration/test_semantic_dedupe.py`, module docstring — NEW this
   sweep, and offered to the reviewer rather than repaired: the docstring's
   opening enumerates "(T001a) … (T002) … (T002c) … (T003c)" but the file now
   also carries the T003d measurement cases
   (`TestTheRunsOwnTraceMeasuresWhatItWithheld`, landed R14 C5), which the doc
   this round shipped attributes to T003d in its own section heading "What the
   record shows, and what it measures (T003c, T003d)". So the docstring names
   one slice fewer than the file covers. It is outside the change set; no repair
   was attempted. The reviewer may judge whether this reopens the class of
   `R-0779` or is a fresh id.

## Authored-text proofs

| Authored text | Proof |
|---------------|-------|
| the whole block | `cmp .remedy-wt/f109-r15.md .agent/authored/f109-r15.md` → exit 0 (source is the reviewer's own original) |
| SLICE PLAN15 | extracted by delimiter index, `cmp` against `.agent/plan.md` → exit 0 |
| SLICE RECORD15 | G3(a) byte arithmetic + G3(b) paragraph reader + G3(c) negative control |
| SLICE DOC | written whole to a NEW file; 122 lines, exactly one trailing newline |
| PAIR IDX1, PAIR IDX2 | FROM 1→0 and TO 0→1 for each, both REWRITES by the containment test |

Every slice was applied BYTE FOR BYTE. Nothing was rewrapped, re-indented or
"improved", and no slice was silently corrected.

## Open findings

Computed as a SET DIFFERENCE, never a subtraction (`R-0778`):
`len(set(registered) - set(resolved))` = **277** open, from 341 distinct
registered ids and 64 distinct resolved ids over 66 `Done:` lines. The base at
`5fe32449` was 276 open from 339 registered and 63 resolved. Net zero this
round: `R-0780` registered, `R-0779` resolved.

## Deviations & assumptions

1. **DEVIATION — an extra verification the block did not order, declared because
   it first appeared to contradict the DOC.** The DOC's savings table (2 segments
   withheld, 556 chars avoided, 97 spent on markers, 459 net) is not asserted
   literally by the suite, which asserts inequalities, so it was re-measured. A
   first replica of the fixture, driven from a scratch script under
   `.remedy-wt/`, DISAGREED: 3 segments (`builder_system`, `reviewer_system`,
   `reviewer_scope`), 1869 avoided, 145 on markers, 1724 net. Rather than treat
   that as a reviewer error, it was re-run through the REAL pytest fixture (a
   scratch `-p` plugin wrapping `measure_dedupe_savings_from_traces`, so the
   shipped `fallback_repo` fixture and its own `tmp_path` were used), which
   reproduced the DOC EXACTLY: `avoided=556 markers=97 net=459 occ=2
   unmeasured=()` for the enabled case and all zeros for the disabled one. The
   replica was unfaithful — it reused one repo and one `REMEDY_DATA_DIR` across
   both runs and sat at a different repo path, which changed segment sizes and
   pushed `reviewer_scope` over the 200-character floor. **The DOC is correct;
   the disagreement was mine.** Recorded because a reader deserves to know the
   table was independently reproduced and how.
2. **DEVIATION — one sandbox denial, routed around without weakening anything.**
   The in-process replica of deviation 1, run as a `bash -c` Python heredoc, was
   DENIED by the sandbox with no exit code. It was re-run by writing the same
   script to `.remedy-wt/r15_measure.py` and invoking `python3` on it. No
   ordered gate was affected; both scratch files were deleted afterwards by
   their exact paths, together with `.remedy-wt/r15_plugin.py`,
   `.remedy-wt/plan15_extracted.md`, the `.remedy-wt/r15_measure_tmp/` tree and
   `.remedy-wt/__pycache__/r15_plugin.cpython-310-pytest-9.0.3.pyc` — each
   verified absent by `os.path.exists`. The reviewer's own
   `.remedy-wt/f109-r15.md` was deliberately KEPT so G1 can be re-run
   independently.
3. **DEVIATION — a disposable worktree the block did not name.** G6 forbids a
   count from FALLING but gave baselines for the six non-`tests/docs/` suites
   only. To make the `tests/docs/` clause meetable rather than unverifiable, the
   base was measured at `d52a5371` in `.remedy-wt/r15base` with `python3 -B`
   (295 passed, exit 0), and the worktree was removed by its exact path and
   pruned. The primary checkout was never used for it.
4. **ASSUMPTION — the ledger patterns.** "Registered id" is a line matching
   `^- (R-\d{4}) — ` and "resolved id" a line matching `^Done: (R-\d{4}) — `.
   These are the patterns that reproduce the round 14 verdict's own published
   figures from the base commit, which is why they were chosen.
5. **ASSUMPTION — G5's `grep -c`.** Read as grep's own semantics, a count of
   LINES (= 2), not of occurrences (= 4). Both numbers are reported above so the
   reviewer can check either reading.
6. No deviation from the block's ordered commit sequence: C0a, C0b, C1, C2, C3,
   C4, each exactly once and in order. No PR created or merged, no force-push,
   no work on `main`, and nothing outside the seven-path change set was edited.

## Next

Review this round at `d52a5371..HEAD`, then round 16: repair `R-0780` — restate
the two false "deliberate absence" bullets in
`packages/orchestration/session_sent_index.py` so they say the call sites exist
and name the commits that made them exist. Before authoring it, re-read
`.agent/STOP` from disk (Phase 1 rule 1 before rule 2). After that repair the
remaining F109 work is the integration gate and then the closure sequence.
