# Handback — F115 · R25 (CLOSURE retry) — ITEM B LANDED, HALTED at ITEM A

## Range
Review of c9aed5c0..HEAD (branch feature/f115-prompt-cost-report).
C0 and ITEM B landed. ITEM A and ITEMs 3-7 NOT executed: no integrity check,
no evidence job, no stash, no zip, no STATUS/README edit, no PR.

## Commits
### f245624f chore(f115): save the R25 closure block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r25-1.md | +150/-0 | C0 block, verbatim, 150 lines |
| .agent/last_block.md | rewrite | cmp exit 0 against the authored file |

### 0fc9c051 docs(f115): record the Built State of the cost report
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F115.md | +74/-0 | ITEM B appended at EOF, nothing above touched |

### <this commit> chore(f115): record the R25 halt in the plan and the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | AGENTS.md If-Blocked: the exact blocker, 49 lines |
| .agent/handoff.md | rewrite | this file |

## ITEM B — 30 claims, ALL TRUE, applied byte-identical
Verified against the disk, not against the block. Highlights, each re-derived:
catalog entry `command_id="stats.report"` → `_cmd_stats_report`, args exactly
`--since --until --job --by --label` + `_PROJECT_SCOPE_OPT`(`--project`) +
`_JSON_OPT`(`--json`), `_ALL_PROJECTS_FLAG` absent; `render_cost_report_markdown`
and `cost_report_json_bytes` both `-> str`, `cost_report_json`
`-> dict[str, Any]`, all three taking `CostReport`/`SegmentShareReport`;
`COST_REPORT_VERSION = 3` and the json key `report_version`;
`SCHEMA_VERSION = 2` (base 0d6c97aa has 1) and all eight new names absent from
the base file; the three literals; `grep -rn` over `tests/` for `unlabelled`,
`COST_DEFAULT_LABEL`, `COST_UNNAMED_BUCKET_LABEL` and (with -F) `(unnamed)` →
NOTHING, exit 1; the four `_PRIOR_REASON_*` sentences read verbatim and matched
to their guards (`not since or not until`, `except ValueError`, `except
TypeError`, `length <= timedelta(0)`); `COST_EMPTY_COMPARISON` /
`COST_NO_COMPARISON_DEFAULT` in `cost_report.py`; `on_prompt_composed` after
the `*` in `plan_job_with_llm` and passed at `job.py`; `builder_composed` /
`reviewer_composed` in `pingpong_loop.py`; `git diff --name-only 0d6c97aa..HEAD
-- packages/ apps/` → exactly the seven listed paths; `grep -c task_class
token_ledger.py` → 0; `"role": "builder"` hardcoded in the accounting dict
(`pingpong_loop.py:4022`) that `token_ledger.py` reads the role column from;
`_ROLE_LIMIT_NOTE` read at exactly two sites, both in functions
`_cmd_stats_cache` calls, and neither it nor any task-class text in the whole
`_cmd_stats_report` body; `GOLDEN_DIR` only ever `read_text`, never written;
the golden `cost_report.md` is a verbatim substring of the guide (Python `in`,
True); `test_the_cli_hands_the_planner_composition_down` uses
`inspect.getsource` and asserts the wiring string.
One NUANCE, not a defect and not a blocker: `unmeasured` also occurs in 13
further test files beyond the cost-report tests and the two goldens. The block
does not claim exclusivity and its conclusion ("only the first of the three is
pinned") is correct, so it was applied unchanged.

## THE STOP — ITEM A, one false claim
R-0343 states: "R24's block ordered `git stash list` non-empty as a closure
gate". FALSE, and it is a round attribution, the coordinate class again.
- `grep -n "stash list" .agent/authored/f115-r24-1.md` → lines 104-106
  "Its ITEM 5 step 2 gate is REPLACED… must contain" and 138 "`git stash list |
  head -1` contains `f115-closure:`". The R24 block carries the CORRECTED gate.
- `grep -n stash .agent/authored/f115-r23-1.md` → line 131 "e) git stash list
  non-empty AND git status --porcelain EMPTY before the zip". THAT is the block
  that ordered it, inherited from R22's ITEM 5 step 2 / done-when (e).
- R-0343's own R24 draft (`.agent/authored/f115-r24-1.md:8`, never committed to
  live_review.md) says the worker found it "and it is fixed in R24".
- The R24 handback (previous `handoff.md`, verification line (e)) records "The
  block's amendment 2 is therefore correct and stands for the next round".
The worker may not edit an authored finding, so ITEM A is handed back rather
than applied. Its other claims verified TRUE: the `tests/` searches return
nothing; `BOX_WIDTH = 78` with `content[: BOX_WIDTH - 1] + "…"` in
`help_renderer.py`; the stale comment above the catalog entry
(`command_catalog.py:2965-2968`) does assert what `remedy stats --help` prints;
`_PRIOR_REASON_EMPTY_PERIOD` is the ends-at-or-before-it-starts case and
`COST_EMPTY_COMPARISON` is the read-but-empty one; `git stash list` → five
pre-existing unrelated entries.

## Why ITEMs 3-7 are blocked
ITEM 6 (c) must write "open findings 15 … R-0343 … next free ID R-0344" and
closure precondition 1 requires every R-XXXX registered. With R-0343 not on
disk both are false. The closure commit must be LAST, so it cannot precede
ITEM A's commit. Closing now would need the accepted HEAD to be re-cut next
round — the definition of a stale STATUS line.

## Verification
- (a) `cmp .agent/authored/f115-r25-1.md .agent/last_block.md` → no output,
  exit 0. 150 lines, zero trailing-whitespace lines.
- (b) ITEM A's gates NOT RUN — not applied. `grep -c "^- R-0343 — Low"
  .agent/live_review.md` → 0. `grep -c "^## Steps" …` → 1.
- (c) `python3 -m pytest tests/docs/ -q` → `294 passed in 0.27s`, exit 0. No
  regression against 294. Byte-identity proof: authored lines 18-90 (73 lines)
  vs the applied section in T2_F115.md → list equality True.
- (d)-(g), (l) NOT RUN. DECISION F115 D7 still pends, so
  ` M scripts/make_review_zip.sh` is untouched. No stash pushed, none popped.
- (e) `git stash list` → five PRE-EXISTING entries, none from this session:
  f003-v2-before-materialize · visual-design-intelligence… · steps-1917-1960… ·
  steps-975-994… · steps-880-894…. Amendment 2 remains correct.
- (h)/(i) not applicable: STATUS.md still `[~] F115`, README still 44.
- (j) `git status --porcelain` → ` M .agent/plan.md` (this commit) and
  ` M scripts/make_review_zip.sh`.
- (k) `git log --oneline 142e80c8..HEAD` → this commit, 0fc9c051, f245624f,
  c9aed5c0, d4a27801, 1df61a43.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | f245624f, cmp exit 0 |
| ITEM A | skipped | false round attribution for the stash gate; stop-on-false-claim |
| ITEM B | done | 0fc9c051, 30/30 claims TRUE, byte-identical |
| ITEM 3 | skipped | blocked by ITEM A |
| ITEM 4 | skipped | blocked by ITEM A |
| ITEM 5 | skipped | blocked by ITEM A |
| ITEM 6 | skipped | blocked by ITEM A |
| ITEM 7 | skipped | blocked by ITEM A |
Declared deviation 1: ITEM B was executed BEFORE ITEM A, reversing the block's
C1/C2 order. ITEM B has no dependency on ITEM A, it verified clean, and
landing it satisfies closure precondition 4 after three rounds of failing to.
Declared deviation 2: `.agent/plan.md` and this file land as a commit the block
did not order. AGENTS.md If-Blocked mandates the plan carry the exact blocker,
and the ITEM 6 that would have rewritten both was never reached.
Deviations, declared: 133 lines, over the 60-line cap (AGENTS.md DECISION
D15). Cause is mandated content — three per-commit tables, the per-claim
verification result the block's done-when (c) requires, the stop evidence with
its raw greps, the verification transcript and the eight-row item-status table.
No section was dropped.

## Next
Reviewer re-authors R-0343 with the stash-gate attribution corrected (R22/R23
ordered it, the R23 worker found it, R24 fixed it), then re-orders the closure
from ITEM A. ITEM B is DONE — do not re-order it. Open findings still 14; next
free ID still R-0343. `git push` follows this commit; its result is in the
transcript.
