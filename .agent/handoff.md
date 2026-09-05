# Handback — F259 Vocabulary & concept model v1, round 1

## Session

`SESSION 1 of feature F259 · round 1 · rounds so far 1`

Fortschritt: `~10 % (T001 inventory in review · T001 page, T002, T003, T004 open) — Schätzung`

Context self-assessment (operator amendment amend0905-throughput): this worker
session used roughly a fifth of its window on one round whose largest cost was
reading 11 192 lines of source through AST summaries rather than whole files;
several more rounds of this size fit comfortably before a boundary is needed.

## Range

Review of `25961794..c2f74bd1`.

Branch `feature/f259-vocabulary`, cut from `main` at `25961794` (the merge of
pull request #239). No pull request exists for this branch and none was created.

## Commits

### 686dde44 f259: save the round-1 block to authored and mirror last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f259-r1.md` | +463 / -0 | C0 — the reviewer's block file, copied with `shutil.copyfile` |
| `.agent/last_block.md` | +445 / -399 | C0 — the same bytes mirrored as the current block |

### 951134e8 f259: re-point plan and context from F262 to F259

| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | +42 / -46 | C1 — the CTXF259 slice, whole-file |
| `.agent/plan.md` | +33 / -29 | C1 — the PLANF259R1 slice, whole-file |

### ddf1e9b3 f259: re-head the live review record at the F259 claim

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +29 / -25 | C2a — the preamble region replaced by LRHEAD_TO; everything from `## Findings` untouched |

### 6efb510b f259: book the reviewer Done record for R-0797

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | C2b — DONE0797 inserted after the surviving `Landed: R-0797` line |

### 67598164 f259: claim F259 in the roadmap ledger

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1 / -1 | C3 — the STATUS pair, `[ ]` to `[~]` |

### c2f74bd1 f259: put the T001 source inventory on disk

| Path | +/- | Reason |
|---|---|---|
| `.agent/f259_inventory.md` | +615 / -0 | C4 — new file, written to the block's SPEC |

### C5 — this file

`.agent/handoff.md`, rewritten whole. A handback cannot table the commit that
writes it (R-0149 pattern); its own `+/-` are therefore not listed here.

Every `+/-` cell above is the output of `git diff --numstat <parent> <commit>`
and comes from nothing else.

## External actions

- `git checkout -b feature/f259-vocabulary` — branch created at `25961794`.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
  printed `[]`; the Open PR Gate passed before the branch was cut.
- `git push -u origin feature/f259-vocabulary` — `* [new branch] feature/f259-vocabulary -> feature/f259-vocabulary`,
  run after C4.
- `gh pr list --state all --head feature/f259-vocabulary --json number,state,title`
  — printed `[]`. NO pull request was created this round, as the block requires.
- A second `git push` after C5.
- No worktree was added or removed; no merge; no force-push; no branch deletion.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | block copied to `.agent/authored/f259-r1.md` and `.agent/last_block.md`; one digest three times |
| C1 | done | `.agent/plan.md` and `.agent/context.md` re-pointed, one commit |
| C2a | done | preamble region replaced under its own digest guard |
| C2b | done | DONE0797 inserted; 2 insertions, 0 deletions |
| C3 | done | STATUS pair applied as a rewrite; FROM 0x, TO 1x |
| C4 | done | `.agent/f259_inventory.md` written to the SPEC |
| C5 | done | this file, then the second push |

## Verification

**G1 TRANSPORT — PASS.** `sha256sum .remedy-wt/f259-r1-block.md .agent/authored/f259-r1.md .agent/last_block.md`, exit 0:

    6b0cd1746c917224a52cfd71d07b9497729b6ea2f8441ffb85702911add499cf  .remedy-wt/f259-r1-block.md
    6b0cd1746c917224a52cfd71d07b9497729b6ea2f8441ffb85702911add499cf  .agent/authored/f259-r1.md
    6b0cd1746c917224a52cfd71d07b9497729b6ea2f8441ffb85702911add499cf  .agent/last_block.md

One digest, three paths, and it is the digest the delegation order stated.

**G2 THE PAIR AND THE TWO ANCHORED EDITS — PASS.**
STATUS pair: `FROM occurrences BEFORE: 1`. The containment test of constraint 2
was re-run before applying and printed, verbatim: `TO contains FROM: false` —
so the pair is a REWRITE and the obligation is FROM 0x / TO 1x, which is what
`FROM occurrences AFTER: 0` and `TO occurrences AFTER: 1` read. After C3:
`^- \[~\] F259 — Vocabulary & concept model v1$` counts 1 and `^- \[ \] F259`
counts 0.
C2a: the preamble digest recomputed BEFORE the edit was
`0f0355434f64b121e845eeb97166dd17e8a97ae2de92ae2383d2f454c4e9922a`, equal to
the block's `0f0355434f64b121e845eeb97166dd17e8a97ae2de92ae2383d2f454c4e9922a`;
the script would have refused otherwise. After the edit,
`^# Live Review — F037` counts 0, `^# Live Review — F259` counts 1, and
`Steps` counts 19 (≥1).
C2b: `^Landed: R-0797` counts 1 BEFORE and 1 AFTER; `^Done: R-0797` goes 0 → 1.

**G3 THE RECORD IS CARRIED FORWARD — PASS.**
C2a: the bytes from the start of `## Findings` to end of file hash to
`c9a028823fc3a8018ca85e6d90bcbdc4049e4fa2ab976ac025f6595efdb4db9e` BEFORE the
edit and `c9a028823fc3a8018ca85e6d90bcbdc4049e4fa2ab976ac025f6595efdb4db9e`
AFTER it — identical to each other and to the digest the block stated. Region
length 815 223 bytes.
C2b: `git show --numstat 6efb510b` names exactly one path and reads
`2	0	.agent/live_review.md`.
Open-finding arithmetic after C2b: `^- R-[0-9]{4} — ` counts 299,
`^Done: R-[0-9]{4} — ` counts 5, difference **294 open findings** (295 at the
branch point, less R-0797 booked this round).

**G4 STATUS INVARIANTS — PASS.** After C3: `^- \[~\] F` counts 1 (the
`assert len(in_progress) <= 1` invariant of
`tests/docs/test_docs_consistency.py` holds); `^- \[x\] F` counts 72, unchanged
from the branch point; `git diff --numstat 6efb510b 67598164` reads
`1	1	docs/roadmap/STATUS.md` and names nothing else.

**G5 THE SUITES, RUN SERIALLY, at C4 — PASS, every count exactly as expected.**

| Command | Expected | Read | Exit |
|---|---|---|---|
| `python3 -m pytest tests/docs/ -q` | 295 | `295 passed in 0.44s` | 0 |
| `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` | 30 | `30 passed in 0.36s` | 0 |
| `python3 -m pytest tests/ui_server/ -q` | 515 | `515 passed in 32.52s` | 0 |
| `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 52 | `52 passed in 5.54s` | 0 |
| `python3 -m pytest tests/regression/test_resource_safety.py -q` | 21 | `21 passed in 11.57s` | 0 |
| `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` | 16 | `16 passed in 0.27s` | 0 |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 42 | `42 passed in 20.87s` | 0 |

Seven suites, run one at a time, no failures, no errors, no skips reported. The
four state readers were run as FOUR.

**G6 THE INVENTORY IS MEASURED, NOT REMEMBERED — PASS.** Checker
`.remedy-wt/f259r1/check_citations.py` (gitignored, not committed) parses every
`path:line` citation out of the RENDERED Markdown, opens each cited file, reads
that line and compares it with the code span quoted beside it. Exit 0:

    [INVENTORY] citations found:                471
    [INVENTORY] resolved to a real file+line:   471
    [INVENTORY] quoted text did NOT match:      0
    grep -c '^## ' .agent/f259_inventory.md -> 17
    seven source paths present in the file: 7 of 7

NEGATIVE CONTROL, so this gate is not self-fulfilling: the same checker run
over a copy with one citation's line number bumped by one and one quoted
character changed reported both, exit 0 on the `--selftest` contract:

    [NEGATIVE CONTROL] quoted text did NOT match:      2
    [NEGATIVE CONTROL]   ...:175 MISMATCH packages/core/models.py:223
          quoted: 'class Job(BaseModel):'
          actual: '"""Top-level orchestration unit composed of tasks."""'
    [NEGATIVE CONTROL]   ...:609 MISMATCH packages/orchestration/dod_gate.py:101
          quoted: 'class GateResultX:'
          actual: 'class GateResult:'

**G7 THE STATE FILES MEET THEIR CONTRACTS — PASS.** `wc -l .agent/plan.md`
reads `46 .agent/plan.md`, under 50. `^## Goal$` counts 1 and `^## Next Steps$`
counts 1 in `.agent/plan.md`; `^## Active Branch$` counts 1 and
`feature/f259-vocabulary` counts 1 in `.agent/context.md`. Byte equality against
the extracted slices written to `.remedy-wt/f259r1/`, with
`filecmp.cmp(..., shallow=False)`:

    PLANF259R1 filecmp.cmp(target, extraction, shallow=False): True
    CTXF259    filecmp.cmp(target, extraction, shallow=False): True

**G8 STRUCTURE — PASS.** `git status --porcelain | wc -l` read `0` immediately
before C5 was staged. `git ls-files .remedy-wt | wc -l` read `0`, so no scratch
file is tracked. Every commit is single-parent:

    c2f74bd1 67598164 | f259: put the T001 source inventory on disk
    67598164 6efb510b | f259: claim F259 in the roadmap ledger
    6efb510b ddf1e9b3 | f259: book the reviewer Done record for R-0797
    ddf1e9b3 951134e8 | f259: re-head the live review record at the F259 claim
    951134e8 686dde44 | f259: re-point plan and context from F262 to F259
    686dde44 25961794 | f259: save the round-1 block to authored and mirror last_block

`git diff --numstat <parent> <commit>`, cell by cell, C0 through C4 — these are
the numbers the `## Commits` tables above carry:

    C0  463 0 .agent/authored/f259-r1.md   /  445 399 .agent/last_block.md
    C1   42 46 .agent/context.md           /   33  29 .agent/plan.md
    C2a  29 25 .agent/live_review.md
    C2b   2  0 .agent/live_review.md
    C3    1  1 docs/roadmap/STATUS.md
    C4  615  0 .agent/f259_inventory.md

Push result: `* [new branch] feature/f259-vocabulary -> feature/f259-vocabulary`.
No pull request was created — `gh pr list --state all --head feature/f259-vocabulary`
printed `[]`.

Two commits exceed the 500-insertion cap; both are declared under "Deviations"
below rather than silently split.

## Authored-text proofs

Four slices were applied, each extracted from the COMMITTED
`.agent/authored/f259-r1.md` by marker extraction in Python and never retyped:

| Slice | Target | Proof |
|---|---|---|
| PLANF259R1 | `.agent/plan.md` | `filecmp.cmp(..., shallow=False)` against the extraction → `True` |
| CTXF259 | `.agent/context.md` | `filecmp.cmp(..., shallow=False)` against the extraction → `True` |
| LRHEAD_TO | `.agent/live_review.md` preamble | the region it replaced matched its stated sha256 before the write, and the region it did NOT touch matched its stated sha256 before and after |
| DONE0797 | `.agent/live_review.md` insertion | asserted single-line (0 newlines, 1737 bytes); numstat `2 0` proves an insertion, not a rewrite |
| STATUS_FROM / STATUS_TO | `docs/roadmap/STATUS.md` | `str.replace(FROM, TO, 1)` after `FROM occurrences BEFORE: 1`; containment test printed `TO contains FROM: false` |

The transport chain itself is G1: the block file, the saved copy and the mirror
are one digest, so no slice can have drifted from the reviewer's text.

## Deviations & assumptions

1. **Two commits exceed the 500-insertion cap of AGENTS.md, Commit Discipline;
   both are declared here, and I am NOT claiming the "only such commit in its
   feature" exception, because there are two.** The rule says an undeclared
   oversize commit, or a second one in the same feature, is a Medium finding;
   the reviewer owns that call, and I have not adjusted anything to dodge it.
   - **C0 `686dde44`, 908 insertions** (463 + 445). The block orders both files
     in one commit and both are the SAME 28 548 bytes; splitting them would
     break the three-way digest chain that G1 exists to establish atomically.
     `.agent/last_block.md` is one of the five files AGENTS.md's counting rule
     exempts by name as "the verbatim rewrite of a SINGLE `.agent/**` state
     file", but this commit carries two paths, so I have NOT read the exemption
     as covering it. Excluding the exempt file's 445 leaves 463, under the cap.
   - **C4 `c2f74bd1`, 615 insertions** in one new file. The file's shape is
     fixed by the block's SPEC — one section per D1 word, every matching symbol
     cited — so its length is a property of the code being measured, not of my
     drafting. Splitting it would put part of a word list in one commit and the
     rest in another.
2. **The shell guard refused three command forms; each check was re-expressed in
   Python and the refusal is reported rather than the check weakened.** The
   refusals, verbatim:
   `Permission to use Bash has been denied. IMPORTANT: You *may* attempt to accomplish this action using other tools that might naturally be used to accomplish this goal, e.g. using head instead of cat. But you *should not* attempt to work around this restriction in malicious ways ... Let the user decide how to proceed.`
   It fired on (a) a compound command containing `$?`, (b) every `grep -c` whose
   pattern ends in `$` — which is most of G2, G4 and G7 — and (c) one `python3 -c`
   heredoc. Replacement for every anchored `grep -c`:

       import re
       def grepc(pat, path):
           n = 0
           for line in open(path, encoding='utf-8'):
               if re.search(pat, line.rstrip('\n')): n += 1
           return n

   run per pattern, with the original `grep -c` command echoed beside its
   number. Replacement for (c): the same code as a script under `.remedy-wt/`.
   No gate was dropped or narrowed; the two greps whose patterns carry no `$`
   (`^# Live Review — F037` was also run this way for consistency, and
   `feature/f259-vocabulary`) were additionally run natively.
3. **The block's LRHEAD_TO slice ends without a trailing blank line, so after
   C2a `## Findings` no longer has an empty line above it.** Before the edit the
   preamble's line 28 was empty; the slice's last line is
   `the integration gate → the closure sequence.` and constraint 4 orders
   exactly one newline after it. I applied it verbatim, as constraint 1 requires,
   and flag it here rather than adding a blank line the reviewer did not write.
   It changes no heading's identity — `## Findings` still begins its own line —
   and G3's byte-identity on the carried-forward region holds.
4. **The SPEC's CODE rule was read literally as substring containment.** "every
   symbol ... whose NAME contains the word, matched case-insensitively" is
   implemented as `word.lower() in name.lower()`, not as a word-boundary match.
   That is why `repair_rounds_used` appears under Round, `JOB_RUNNING` and
   `truncated_input` under Run, and `make_flight_plan_call_recorder` under Order.
   A word-boundary reading would have given Round 0 CODE symbols and Order 0,
   which would have been a materially different — and, I judged, less faithful —
   answer. The rule is stated in the file's own header so the set is
   reproducible, and no hit is editorially dropped as "spurious".
5. **A symbol excludes function locals.** The SPEC's list is "a class, a
   dataclass or pydantic field, an enum member, a module-level constant, or a
   `def`", so a name bound inside a function body is not counted. My first pass
   did count them and reported 295 hits; correcting the scope rule brought it to
   the 280 CODE citations now in the file. The set is taken with `ast`, not grep.
6. **`.agent/decisions.md` and `docs/roadmap/features/T2_F259.md` were READ but
   nothing was copied from them.** Constraint 9 forbids copying claims; the SPEC
   itself points at D1's "Is NOT" column as the hint for the COMPETING group, so
   D1 was read to know which neighbouring spelling to search for. Every line in
   the inventory is read from the file it cites.
7. **The four unrowed concepts have no single defining module, and I picked one
   each rather than leaving the row empty.** Measured across `packages/`:
   `class [A-Za-z]*Evidence[A-Za-z]*` matches 19 classes, `Decision` 22,
   `Verdict` 4, `Gate` 6. The inventory names the pick, says why, and records the
   spread, so a later round writing the D1 rows can see that the choice was a
   judgement over a scattered concept rather than a lookup.
8. **Not attempted:** `ruff check` and the built `remedy` CLI — constraint 6 says
   neither is needed and no `.py` file is in the change set. Nothing this round
   required either, so no scope escape occurred.
9. **No departure from the block's ordered commit sequence.** C0, C1, C2a, C2b,
   C3, C4, push, gates, C5, push — in that order, no extra commit, none dropped,
   none reordered.
10. **`.agent/STOP` was read from disk before C0, before C3 and before C5** — it
    did not exist at any of the three reads.

## Next

The reviewer gates this round against `25961794..c2f74bd1` and issues a verdict.
Then round 2: write the DECISION amend0905-vocab D1 table into
`docs/system/vocabulary.md`, one row per word, with the "code spelling today"
column taken from `.agent/f259_inventory.md` and from nothing else.
