# Handoff — F109 Semantic dedupe, SESSION 3, round 14

## Session

`SESSION 3 of feature F109 · round 14 · rounds so far 14`

Soft limit is 25 rounds / 7 sessions (self-drive protocol G7, amend0827 rule 6).
At 14 rounds and 3 sessions the limit is NOT reached, so no scope report is due.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## THE ROUND ENDS GREEN

`packages/orchestration/prompt_trace.py` gains ONE PURE FUNCTION,
`measure_dedupe_savings_from_traces`, which reads a run's own trace entries and
reports what the run did NOT resend. It is landed UNWIRED, as constraint 4
ordered. All fifteen suites the block names are exit 0; only the two that gain
cases moved, and only upward (128 → 130, 49 → 54). The production edit is ONE
INSERT OPCODE AND ZERO DELETED LINES. Both red-proofs went red on the intended
case and green again on restore, each beside its unmutated control.

The honesty branch is load-bearing and was PROVED so, not asserted: dropping it
(`latest_full_chars.get((entry.role, name))` →
`latest_full_chars.get((entry.role, name), 0)`) reddens SPEC H case 4 with
`Right contains one more item: 'builder_context'`, i.e. the segment stops being
NAMED as unmeasured and starts being counted as a zero saving. That is exactly
the confusion the function exists to prevent.

## Range

Review of `5fe32449..069f1c02` (production + tests), plus the handoff commit
below.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f109-r14.md` | done | |
| C0b mirror to `.agent/last_block.md` | done | |
| C1 SLICE PLAN → `.agent/plan.md` | done | |
| C2 SLICE RECORD → `.agent/live_review.md` | done | |
| C3 SPEC F → `tests/orchestration/test_semantic_dedupe.py` | done | |
| C4 SPEC G → `packages/orchestration/prompt_trace.py` | done | |
| C5 SPEC H → the two test files | done | |
| C6 rewrite `.agent/handoff.md` | done | this commit |

## Commits

### 07b53fa1 F109 R14 C0a: save the round 14 block verbatim under .agent/authored
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f109-r14.md` | +378 / -0 | the block, `cp`'d from `.remedy-wt/f109-r14.md`, never retyped |

### 7ed7e82e F109 R14 C0b: mirror the round 14 block into .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +209 / -200 | `cp` of the authored copy; a whole-file replacement of round 13's block |

### 231e764b F109 R14 C1: plan for round 14 - measure the savings from the trace record
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14 / -15 | SLICE PLAN, extracted mechanically by delimiter index |

### b1ea60a8 F109 R14 C2: book the round 13 gate and register R-0779
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +5 / -1 | SLICE RECORD appended: the R13 gate paragraph and the `R-0779` registration |

### 79edbcbf F109 R14 C3: repair R-0779 - the dedupe suite module docstring names what the file covers
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | +6 / -3 | SPEC F pairs F1 and F2, applied byte for byte; no case touched |

### 71897c7c F109 R14 C4: a pure measurement of what a run did not resend, read from its own traces
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/prompt_trace.py` | +104 / -0 | SPEC G: `DedupeSavingsMeasurement` + `measure_dedupe_savings_from_traces`, appended |

### 069f1c02 F109 R14 C5: pin the measurement - exact arithmetic on entries, the claim on the real loop
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_prompt_trace.py` | +138 / -0 | SPEC H cases 1-5 + the two imports they need |
| `tests/orchestration/test_semantic_dedupe.py` | +98 / -0 | SPEC H cases 6-7 as one new class at the file's end + one import |

### C6 — the handoff commit
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/g5-r14 069f1c02` | created, detached at `069f1c02` |
| `git worktree remove .remedy-wt/g5-r14` | removed; `git -C .remedy-wt/g5-r14 status --porcelain` was EMPTY first |
| `git worktree prune` | exit 0 |
| `git push -u origin feature/f109-semantic-dedupe` | run after this commit; result below |

No PR created, nothing merged, no force-push, branch never left
`feature/f109-semantic-dedupe`.

## Verification — the eight gates, real readings

**G1 TRANSPORT — PASS.** `sha256sum .remedy-wt/f109-r14.md
.agent/authored/f109-r14.md .agent/last_block.md` printed ONE digest three
times:
`d391081163058c104207886d8beb09eac0a42eec24cc8321d395f2523487e558`.

**G2 THE PLAN — PASS.** SLICE PLAN extracted by delimiter index (opening line
index 204, closing 244, 39 lines between). `cmp` against `.agent/plan.md`:
exit 0, no output. `wc -l .agent/plan.md` = 39 (< 50). `grep -c '^## Goal'` = 1,
`grep -c '^## Next Steps'` = 1.

**G3 THE RECORD APPEND — PASS, four readings.**
(a) ARITHMETIC. base size 2096539, base sha
`c68325ca44ef99742b412988a4a0b508f9eefb0a32a4c01532b5c65c51d32cee`; appended
length S = 4745 after stripping trailing newlines; new size 2101284;
`2096539 + 4745 == 2101284` → True. New sha
`1d2111bcf7ef35cd291bbfaf33aeabf4625f023f0f05410b0a30ee29651e3d70`. The file
still ends WITHOUT a trailing newline (last bytes `the file does not cover.`).
(b) SECOND READER, counts no byte. Split the WHOLE file on blank-line
boundaries: 877 units. N = 2, taken from the PAYLOAD itself. The LAST 2 units
equal the appended paragraphs in order — unit -2 opens
`'Gate: F109 R13 — the round 13 entry. VERDICT PASS, over the '`, unit -1 opens
`"- R-0779 — Low, THE DEDUPE SUITE'S MODULE DOCSTRING DESCRIBE"`. ACCEPTED,
exit 0.
(c) NEGATIVE CONTROL, on the scratch copy
`.remedy-wt/live_review_negative_control.md` and never on the tracked file.
Flipped offset 2096551 (byte `' '` → `'X'`), which is INSIDE the first appended
paragraph. Reader (b) REJECTED it, exit 1, showing
`'Gate: F109XR13 — the round 13 entry. …'`, having ACCEPTED the tracked file at
exit 0. Tracked sha BEFORE `1d2111bc…651e3d70`, AFTER `1d2111bc…651e3d70` — it
did not move. Scratch deleted by exact path; `os.path.exists` on that exact path
is False.
(d) COUNTS, AS A SET DIFFERENCE and never a subtraction (`R-0778`). Base read
from `git show 5fe32449:.agent/live_review.md`, never by rewinding the tracked
file:

| Reading | base `5fe32449` | after this round |
|---|---|---|
| registered ids | 339 | 340 |
| DISTINCT registered ids | 339 | 340 |
| `Done:` lines | 65 | 65 |
| DISTINCT resolved ids | 63 | 63 |
| open set — `set(registered) - set(resolved)` | 276 | **277** |

Every base figure matches the block's stated 339 / 339 / 65 / 63 / 276, and the
after-figures match its stated 340 and 277, with `Done:` lines and distinct
resolved ids UNCHANGED because this round resolves nothing.
`grep -c '^Gate: F109 R13 — '` = 1. `grep -c '^- R-0779 — '` = 1.

**G4 THE EDIT SHAPE — PASS, read from `git show <sha>:<path>` blobs only.**
(a) ACROSS C4 (`79edbcbf` → `71897c7c`) on
`packages/orchestration/prompt_trace.py`, via
`difflib.SequenceMatcher(None, before, after, autojunk=False)`:
`('equal', 0, 261, 0, 261)` and `('insert', 261, 261, 261, 365)`. Non-equal
tags = `['insert']`; no `replace`, no `delete`. **TOTAL LINES DELETED = 0.**
(b) ACROSS C3 (`b1ea60a8` → `79edbcbf`): `grep -c '    def test_'` on
`tests/orchestration/test_semantic_dedupe.py` is **102 before and 102 after** —
UNCHANGED, because C3 touches no case.
(c) ACROSS C5 (`71897c7c` → `069f1c02`): `test_semantic_dedupe.py` 102 → 104
(**rose by 2**); `test_prompt_trace.py` 49 → 54 (**rose by 5**). Seven added
cases, matching SPEC H's seven.
(d) THE FUNCTION IS PURE, proved on the SOURCE with `ast`. Located
`measure_dedupe_savings_from_traces` at line 285; walked 251 AST nodes in its
body. `Import` / `ImportFrom` / `Global` / `Nonlocal` nodes found: `[]`. Every
call name in the body: `['DedupeSavingsMeasurement', 'append', 'get', 'int',
'list', 'set', 'str', 'tuple']`. Every attribute read: `['append',
'deduped_segment_names', 'get', 'role', 'segment_manifest']`. WHAT WAS SEARCHED
FOR, so the absence is only as wide as the search: `Path`, `__import__`,
`append_trace_jsonl`, `compile`, `eval`, `exec`, `input`, `mkdir`, `open`,
`print`, `read`, `read_text`, `unlink`, `write`, `write_text`,
`write_trace_jsonl`, `writelines`. Intersection with the calls actually made:
`[]`. Probe exit 0.

**G5 THE COLOUR — PASS, two red-proofs, each with its unmutated control.**
Worktree added BY EXACT PATH at `/home/decodeux/Repos/remedy/.remedy-wt/g5-r14`,
detached at C5 `069f1c02`. IMPORT PROBE FIRST: `python3 -B -c "import
packages.orchestration.prompt_trace as m; print(m.__file__)"` with the worktree
as cwd resolved to
`/home/decodeux/Repos/remedy/.remedy-wt/g5-r14/packages/orchestration/prompt_trace.py`
— INSIDE the worktree, so no editable install shadows it and the gate stands.
`__pycache__` purged before every run (0 dirs found each time); every child was
`python3 -B -m pytest -q -p no:cacheprovider`.

| Run | exit | decisive line |
|---|---|---|
| UNMUTATED CONTROL, both cases | **0** | `2 passed in 0.27s` |
| (a) mutated, SPEC H case 4 | **1** | `E Right contains one more item: 'builder_context'` |
| (a) control after restore | **0** | `1 passed in 0.27s` |
| (b) mutated, SPEC H case 3 | **1** | `E assert 1200 == 1160` |
| (b) control after restore | **0** | `1 passed in 0.27s` |

(a) DROP THE HONESTY BRANCH. Bytes about to change, counted in that file before
writing: the string `full = latest_full_chars.get((entry.role, name))` occurs
**exactly 1** time. Replaced with
`full = latest_full_chars.get((entry.role, name), 0)`, so an unobserved full
size becomes a zero saving that is COUNTED instead of an occurrence that is
NAMED. FAILING NODE:
`tests/orchestration/test_prompt_trace.py::TestMeasureDedupeSavingsFromTraces::test_a_deduped_name_with_no_observed_full_size_is_unmeasured_not_zero`.
(b) COUNT THE MARKER AS FREE. The string
`net_chars_saved=chars_avoided - chars_spent,` occurs **exactly 1** time.
Replaced with `net_chars_saved=chars_avoided,` — gross instead of net. FAILING
NODE:
`tests/orchestration/test_prompt_trace.py::TestMeasureDedupeSavingsFromTraces::test_the_saving_is_the_full_size_minus_the_marker_it_paid_for`,
reading `assert 1200 == 1160`, which is the proof that the case pins a NUMBER
and not merely a direction.
Restored from the C5 blob by exact path between the mutations and after the
last (15326 bytes each time);
`git -C .remedy-wt/g5-r14 status --porcelain` was EMPTY before removal. After
`git worktree remove` + `git worktree prune`, `git worktree list` holds the
primary checkout and the four pre-existing `remedy/job-*` worktrees and nothing
else:

    /home/decodeux/Repos/remedy                                  069f1c02 [feature/f109-semantic-dedupe]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

**G6 THE SUITES — PASS. ALL FIFTEEN EXIT 0**, run SERIALLY: one process
started, finished, and only then the next.

| Suite | base | mine | exit |
|---|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | 128 | **130** (MOVED +2) | 0 |
| `tests/orchestration/test_prompt_trace.py` | 49 | **54** (MOVED +5) | 0 |
| `tests/orchestration/test_pingpong_cli.py` | 173 | 173 | 0 |
| `tests/orchestration/test_pingpong.py` | 34 | 34 | 0 |
| `tests/orchestration/test_session_resume.py` | 27 | 27 | 0 |
| `tests/orchestration/test_token_ledger.py` | 120 | 120 | 0 |
| `tests/orchestration/test_token_truth.py` | 37 | 37 | 0 |
| `tests/orchestration/test_token_truth_v1_contract.py` | 101 | 101 | 0 |
| `tests/orchestration/test_job_evidence.py` | 93 | 93 | 0 |
| `tests/orchestration/test_provider_evidence_integration.py` | 64 | 64 | 0 |
| `tests/orchestration/test_cost_report.py` | 22 | 22 | 0 |
| `tests/ui_server/test_prompt_trace_payload.py` | 20 | 20 | 0 |
| `tests/ui_server/test_prompt_trace_lens.py` | 13 | 13 | 0 |
| `tests/test_observability_index.py` | 14 | 14 | 0 |
| `tests/cli/test_golden_path.py` | 42 | 42 | 0 |

THE TWO THAT MOVED are the two the block permits to move, and both moved
UPWARD: `test_semantic_dedupe.py` 128 → 130 (SPEC H cases 6-7) and
`test_prompt_trace.py` 49 → 54 (SPEC H cases 1-5). The other thirteen are
identical to their base.

**G7 THE TREE — PASS.** `git status --porcelain` is EMPTY (no output).
`git ls-files .remedy-wt` returns nothing. Insertion counts from
`git show --numstat`, the `+` column only, per AGENTS.md DECISION F104 D1:

| Commit | insertions | under 500 |
|---|---|---|
| 07b53fa1 C0a | 378 | yes |
| 7ed7e82e C0b | 209 | yes |
| 231e764b C1 | 14 | yes |
| b1ea60a8 C2 | 5 | yes |
| 79edbcbf C3 | 6 | yes |
| 71897c7c C4 | 104 | yes |
| 069f1c02 C5 | 236 (138 + 98) | yes |

Every commit is single-parent — `git log --format="%h parents=%p" 5fe32449..HEAD`
gives `069f1c02←71897c7c←79edbcbf←b1ea60a8←231e764b←7ed7e82e←07b53fa1←5fe32449`,
one parent each. I RAN THE CELL-BY-CELL COMPARISON of these `--numstat` figures
against my own `## Commits` table above, path by path and number by number, and
every cell agrees; C5's two rows (138 and 98) sum to the 236 quoted here. The
handback commit's own insertion count is not quoted, per constraint 7.

**G8 THE STALENESS SWEEP — RUN, and it found four things.** Each file this
round touched was re-read end to end.

*`.agent/authored/f109-r14.md` and `.agent/last_block.md`* — verbatim copies of
the reviewer's block, never edited. Their count-bearing sentences were all
checked and all HOLD: the change set names 8 paths and 8 were touched; "EIGHT
GATES" and G1-G8 agree; ten numbered constraints are present; G6 lists fifteen
suites and fifteen ran; the 339/339/65/63/276 base and the predicted 340/277
were measured and match; "the four pre-existing `remedy/job-*` worktrees" is 4.

*`.agent/plan.md`* — "Round 14, session 3" HOLDS. "two ids carry two `Done:`
lines each" HOLDS (65 lines over 63 distinct ids). "`R-0769` is registered, not
fixed" HOLDS (`grep -c '^Done: R-0769\b'` = 0).

*`.agent/live_review.md`* — the appended R13 gate paragraph's numerals
(128/49 up from 125/46, and 339/65/63/276) are a DATED record of `5fe32449` and
were verified true there; this round moving those suites to 130/54 does not
falsify a dated reading. `R-0779`'s own text quotes the docstring line
`"""Tests for the per-session sent-hash index (F109 T001a).` — that quotation is
NO LONGER TRUE OF DISK, because C3 repaired it three commits later. That is by
design and is what "resolved" will mean; the reviewer owns the resolution.
Its "the third instance of it on this branch" was re-derived: `R-0749`,
`R-0773` and `R-0779` are each registered exactly once, so 3 HOLDS.

*`packages/orchestration/prompt_trace.py`* — TWO STALE SENTENCES FOUND, both
PRE-EXISTING and neither caused by this round. (1) The module docstring says
"Each trace entry captures what Remedy actually sent to a Builder or Reviewer
provider" and (2) `PromptTraceEntry.role` carries the inline comment
`# "builder" or "reviewer"`. Both state a TWO-ITEM list of roles that is now
INCOMPLETE: `build_trace_entry` ships with `role="intake"`
(`packages/orchestration/intake.py:137`), `role="mission_plan"`
(`mission_compiler.py:282`), `role="flight_plan"` (`flight_plan.py:183`),
`role="orchestrator"` (`orchestrator_loop.py:922`) and `role="planner"`
(`apps/cli/commands/job.py:242`) as well. A third, same shape: `prompt_kind`'s
comment `# "initial", "repair", "review", "re-review"` omits at least `"plan"`
and `"plan-retry"` (`apps/cli/commands/job.py:246`). NOT REPAIRED — SPEC G says
"Nothing already in the file is edited or deleted" and G4(a) demands zero
deleted lines across C4, so repairing them would have broken the round's own
gate; declared here instead. `build_trace_entry`'s docstring, which round 13
widened, was re-read and STILL HOLDS: it names `segment_manifest` and
`segment_manifest_chars` as "BOTH" derived from `composed_prompt` and then adds
`deduped_segment_names` as joining them, which quantifies over the two it names
rather than over everything derived. The "Two writers" comment above
`append_trace_jsonl` HOLDS — there are still exactly two writers, and this
round's addition writes nothing. THE NEW TEXT makes no count claim that can go
stale: it names `estimate_token_savings` and its file by path (both resolve) and
PARAPHRASES rather than quotes that function's "never claims verified savings".

*`tests/orchestration/test_semantic_dedupe.py`* — the two known staleness
defects are REPAIRED, not new: SPEC F pair F1 replaced the opening line, which
now names T001a, T002, T002c and T003c; SPEC F pair F2 removed the "final class"
singular and states no numeral, deliberately. ONE MORE FOUND, and it is a
POSITIONAL claim of the `R-0775` class: the same module docstring still says
"The manifest in the first case is built through the REAL producer in
``prompt_segments``", where `_real_manifest_rows` is in fact called from ELEVEN
sites in this file. NOT REPAIRED — SPEC F gave two literal pairs and this
sentence is in neither; widening the byte-for-byte pairs would have been a
silent correction of the reviewer.

*`tests/orchestration/test_prompt_trace.py`* — ONE FOUND, pre-existing: the
module docstring reads "Steps 5085-5086: Verifies that prompt traces redact
secrets and capture complete builder/reviewer metadata." The file now also
covers the F105 segment manifest (`TestSegmentManifest`), F109
`deduped_segment_names` (`TestDedupedSegmentNames`), this round's F109 T003d
measurement (`TestMeasureDedupeSavingsFromTraces`), and Steps 5088/5089's
`do_cmd` helpers — so the step map is incomplete in both directions. NOT
REPAIRED: SPEC H orders added cases only and the block forbids repairing
outside the change set without declaring it. Declared.

Repaired nothing outside the change set.

## Authored-text proofs

| Authored text | Proof | Result |
|---|---|---|
| the block | `sha256sum` of `.remedy-wt/f109-r14.md`, `.agent/authored/f109-r14.md`, `.agent/last_block.md` | one digest three times, `d3910811…3487e558` |
| SLICE PLAN | `cmp` of the delimiter-extracted slice against `.agent/plan.md` | exit 0, no output |
| SLICE RECORD | G3(a) byte arithmetic + G3(b) paragraph reader + G3(c) negative control | 2096539 + 4745 = 2101284; last 2 units equal, in order; mutated copy REJECTED |
| SPEC F pairs F1, F2 | extracted by delimiter index and applied with `str.replace`; each FROM counted **exactly 1** occurrence before the commit, and `TO contains FROM` was **False** for both | applied byte for byte |

SPEC G and SPEC H are specifications, not slices, and were implemented in the
repository's idiom; no byte-fidelity claim is made for them.

## Deviations & assumptions

1. **SPEC G's honesty branch was WIDENED by one condition, deliberately, and
   this is the round's one real design deviation.** SPEC G defines "unmeasured"
   as a deduped name with no earlier FULL-CONTENT observation. The shipped
   predicate is `if full is None or spent is None:` — it ALSO reports a name as
   unmeasured when the entry carries no manifest row for it at all, so the
   MARKER's own cost was never observed either. The spec's alternative is
   `marker_chars.get(name, 0)`, which would silently claim a marker cost zero
   characters and therefore OVER-report the saving — the exact dishonesty the
   branch exists to prevent. I applied the widening rather than the literal
   text; G5(a) is unaffected, because SPEC H case 4 builds its entry WITH a
   marker row, so only the "no earlier full size" limb can fire there and the
   ordered mutation still reddens exactly that case. Reviewer: if you want the
   literal spec, the one-line revert is stated above.
2. **SPEC H's five arithmetic cases were inserted after `TestDedupedSegmentNames`
   rather than at the end of `tests/orchestration/test_prompt_trace.py`.** The
   file's last two classes are unrelated `do_cmd` helpers from Steps 5088/5089;
   appending F109 material after them would have split the F109 section in two.
   No existing case was edited, renamed or deleted. SPEC H's "at the very END"
   applies to `test_semantic_dedupe.py`, and there the new class IS the last
   thing in the file.
3. **Two module-level import statements were added** — `PromptTraceEntry` and
   `measure_dedupe_savings_from_traces` into `test_prompt_trace.py`'s existing
   `from packages.orchestration.prompt_trace import (…)` block, and a new
   one-line `from packages.orchestration.prompt_trace import
   measure_dedupe_savings_from_traces` into `test_semantic_dedupe.py`. The first
   edits three existing lines of an import block; SPEC H's "no existing case is
   edited" is untouched by it, but the block did not name it, so it is declared.
4. **The function takes `list[PromptTraceEntry]`, not a `Sequence`.** SPEC G says
   "an ordered sequence". Typing it as `Sequence` would have required editing the
   existing `from typing import Any` line, which G4(a) forbids by demanding an
   insert-only diff across C4 — and `build_trace_summary` directly above already
   takes `list[PromptTraceEntry]`, so this is the file's own idiom rather than a
   compromise.
5. **Three stale sentences in `packages/orchestration/prompt_trace.py` and one
   in each test file were found and NOT repaired** — see G8. Repairing the two
   in `prompt_trace.py` would have put deletions into C4 and broken G4(a);
   repairing the test-file ones would have widened SPEC F beyond its two literal
   pairs. All five are declared instead, which is what guardrail G8 asks for.
6. **No commit was added, dropped or reordered.** The bundle ran C0a, C0b, C1,
   C2, C3, C4, C5, C6 in exactly the block's order.
7. **`.agent/plan.md` described round 13 during C0a and C0b**, because the block
   fixes C1 as the first substantive commit and C1 is what advances it. This is
   the block's order, not a departure from it.
8. `.agent/context.md` and `.agent/decisions.md` needed no update: scope,
   assumptions and constraints are unchanged from round 13, and the one
   non-obvious choice (deviation 1) is recorded here and in the code's own
   comment. `docs/` is untouched — the T003 docs are the NEXT slice, and this
   round's function is landed unwired, so nothing in the built-state docs is yet
   false.

## Open findings

**277**, and it is a SET DIFFERENCE, never a subtraction (`R-0778`):
`len(set(registered_ids) - set(resolved_ids))` = `len(340 distinct registered −
63 distinct resolved)` = 277. The `Done:` LINE count is 65, which is two more
than the 63 distinct ids it resolves; subtracting 65 from 340 would give 275 and
would be wrong. `R-0779` was REPAIRED this round (C3) but is NOT marked
resolved — only the reviewer writes that, and this round writes no `Done:` line.

Landed: R-0779 — the dedupe suite's module docstring now names the slices the
file covers and states no numeral for the real-loop classes.

## Next

Review `5fe32449..HEAD`: read the C4 diff and the seven added cases, re-run the
fifteen suites, and — before anything else — re-read `.agent/STOP` from disk
(Phase 1 rule 1) before Phase 1 rule 2. On PASS, mark `R-0779` resolved and
order the T003 DOCS slice: describe the built state and register the doc in
`docs/README.md` in the same commit. The savings function is landed UNWIRED, so
that round must also either wire it into `run_pingpong` or say plainly why it
stays a library.
