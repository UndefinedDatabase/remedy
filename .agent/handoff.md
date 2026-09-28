# Handoff — F036, round 6 (book round 5, register R-1088 and R-1089, record DECISION F036 D7;
repair both — the model-written tour switched on by the operator, the card docked while a stop is
shown — and prove one real job's tour end to end)

## Session

SESSION 1 of feature F036 · round 6 · rounds so far 6. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, DECISION F036 D7
and its booking diff, and every required source file in full (`write_result_tour`, `tour_call_fn`
and `tour_view` in `result_tour.py`; the `teacher.lessons` family of `ConfigKeySpec` entries,
`reset_config` and `write_environment_guide` in `config.py`; `lessons_enabled` and how
`test_lessons.py` switches its key; `test_environment_guide.py`; `TourOverlay.tsx` and its CSS
module; `test_tour_overlay_contract.py`; the five `f036-r5-render_*` files; `test_resume_kill.py`;
`test_tour_route.py`; and `f036-r5-mutations.py`); wrote the switch (`tour.model_written`,
`tour_model_written()`, the sentinel repair in `write_result_tour`), the dock (`data-shown` on the
card, the new CSS rule), the five round-6 render files (two changed, three byte-copied) and ran the
harness (10 of 10 on the first real run), wrote the new end-to-end live test against a real
`run_cycles` + fake-provider child process, wrote the mutation tool, and ran every gate (G1–G5) for
real before writing this handback.

## Range

Review of `8c98cadf1..HEAD` (`HEAD` is this handback's own commit, `F036 R6 C7`, on
`feature/f036-guided-result-tour`).

## Commits

### bdd8869c4 F036 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r6-block.md | 243/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r6-booking.diff | 59/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r6-plan.md | 27/0 | copy of the reviewer's plan.md payload |

329 insertions total, exactly the block's own C1 note (243-line block + 86).

### 705d427eb F036 R6 C2: book round 5, register R-1088 and R-1089, record DECISION F036 D7
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 37/0 | DECISION F036 D7 appended by booking.diff |
| .agent/live_review.md | 6/0 | round 5's `Gate: F036 R5 —` entry and the R-1088/R-1089 registrations appended by booking.diff |
| .agent/plan.md | 7/8 | rewritten to the reviewer's plan.md payload |

Measured exactly the block's own G2/C2 expected numstat: 37/0, 6/0, 7/8.

### 58eab1c36 F036 R6 C3: write the model's tour only when the operator switches it on
| Path | +/- | Reason |
|---|---|---|
| docs/guides/environment.md | 1/0 | S1 regenerated row for `REMEDY_TOUR_MODEL_WRITTEN` |
| packages/orchestration/config.py | 13/0 | S1 the `tour.model_written` `ConfigKeySpec`, directly after `teacher.lesson_max_tokens` |
| packages/orchestration/result_tour.py | 23/4 | S1 `tour_model_written()`, and `write_result_tour`'s sentinel repair + docstring |
| tests/orchestration/test_result_tour.py | 83/1 | THE TESTS: the switch's default, off/on unset behaviour, a handed-in call function whatever the key, and `_apply_terminal`'s own off-switch proof |

120 insertions, 5 deletions (no expected number stated by the block for C3; measured).

### 0228efe9c F036 R6 C4a: dock the tour's card over the left rail while a stop is shown
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/tour/TourOverlay.module.css | 12/0 | S2 `.card[data-shown="true"]` dock rule |
| apps/ui/src/components/tour/TourOverlay.tsx | 2/1 | S2 the card's `data-shown` attribute |
| tests/ui_contracts/test_tour_overlay_contract.py | 9/0 | THE TESTS: `data-shown=` on the overlay, the CSS rule and `--remedy-left-width` in the module |

23 insertions, 1 deletion — the PRODUCT half of the block's single C4 (see Deviations: split under constraint 2).

### ab641a963 F036 R6 C4b: write the render harness's page, module and config, and copy its runner
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r6-render_index.html | 11/0 | S3 byte-copy of round 5's scratch page |
| .agent/authored/f036-r6-render_main.tsx | 130/0 | S3 round 5's copy plus the `globals.css` import |
| .agent/authored/f036-r6-render_measure.py | 191/0 | S3 byte-copy of round 5's runner (its `PREFIX` logic adapts to the new filename unchanged) |
| .agent/authored/f036-r6-render_vite.config.mjs | 28/0 | S3 byte-copy of round 5's scratch build config |

360 insertions (the block's single C4, render half, part 1 — see Deviations).

### 4057564e9 F036 R6 C4c: run the render harness's driver and record its checks
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r6-render.txt | 34/0 | S3 the harness's whole recorded output, `RENDER: 10 of 10 checks pass` |
| .agent/authored/f036-r6-render_drive.mjs | 356/0 | S3 round 5's driver plus C-i (dock geometry after "Show me") and C-j (re-centre after the following ArrowRight) |

390 insertions (the block's single C4, render half, part 2 — see Deviations).

### 95d4ca1be F036 R6 C5: prove one real job's tour through its file, its route and the command line
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_tour_e2e_live.py | 228/0 | NEW FILE: S4's live proof — a two-task job to `all_green` through `run_cycles` + a fake `ProviderCall`, read back by file, by the `tour` route and by `job show --tour` |

### 95cb5bf08 F036 R6 C6: add the round 6 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r6-mutations.py | 195/0 | the G5 red-proof tool: m1–m3 through pytest against the worktree's own `config.py`/`result_tour.py`, m4–m5 through the CONTRACT test |

### <this commit> F036 R6 C7: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |
| .agent/live_review.md | 4/0 | two `Landed:` lines appended, each preceded by a blank line, naming C3 and C4a |

## External actions

- `git worktree add --detach .remedy-wt/f036-r6-mut-dryrun HEAD` then `git worktree remove --force
  .remedy-wt/f036-r6-mut-dryrun` then `git worktree prune` — a DRY validation of the mutation tool
  before C6 was committed (the primary checkout was still dirty with the uncommitted tool itself,
  so this run's own verdict read False on the `git status --porcelain` leg only; every mutation was
  caught and every restoration was byte-identical). Not the official G5 run; declared here for
  transparency. Outcome: worktree created, tool run, worktree removed; `git worktree list | wc -l`
  read 61 before and after.
- `git worktree add --detach .remedy-wt/f036-r6-mut 95cb5bf08` — the OFFICIAL G5 worktree, cut from
  C6 per the block. Outcome: worktree created at detached HEAD `95cb5bf08`.
- `git worktree remove --force .remedy-wt/f036-r6-mut` then `git worktree prune` — the official G5
  worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 61,
  matching the round's step-4 reading.
- `git push -u origin feature/f036-guided-result-tour` — run immediately after this commit per the
  bundle order. Its real outcome is reported in the round's reply (G6), not here, because this file
  is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use), all MATCH:
```
booking.diff: 59 lines, 14886 bytes, sha256 b97f22efea18b1b032b0a7647c6409beb6e233d1e2094a3d8cbdf33ceee61592
plan.md:      27 lines,   970 bytes, sha256 75c9d356ee468bd07d91185ed4ec839b12e9352538afbe50fa7c32f607d464df
```
Block self-check: 243 lines, sha256 `2fa4bcd370ff0cf59342fc0df9a547be3a6b0989e67219709fc315cfc9939fc7`
— MATCH on both readings given in the delegation message. `.agent/authored/f036-r6-*` copies vs.
sources, read back via `git show bdd8869c4:<path>`, all byte-identical:
```
f036-r6-block.md     vs .remedy-wt/f036-r6/block.md                  MATCH (19542 bytes both)
f036-r6-booking.diff vs .remedy-wt/f036-r6-payloads/booking.diff     MATCH (14886 bytes both)
f036-r6-plan.md       vs .remedy-wt/f036-r6-payloads/plan.md         MATCH (970 bytes both)
```

**G2 THE BOOKING** — every file's bytes and sha256 at C2 (`git show 705d427eb:<path>`) MATCHED the
reviewer's table exactly:
```
.agent/decisions.md   2371422 bytes  sha256 c1b761a933b5d89860973792dc6b2fecb27536ab0806e646d62d6e7e1424f73d MATCH
.agent/live_review.md  332264 bytes  sha256 e8cf27b58933833780d67eaad26e903254bbe61ee3dad4ab0e5f249d91302174 MATCH
.agent/plan.md            970 bytes  sha256 75c9d356ee468bd07d91185ed4ec839b12e9352538afbe50fa7c32f607d464df MATCH
```
`open_finding_ids` over `.agent/live_review.md` TEXT at C2 (via `scripts.rotate_live_review`) read
`['R-1088', 'R-1089']`, matching the reviewer's stated reading. `latest_gate_verdict` read `PASS`,
matching.

**G3 THE CODE** — `python3 -m ruff check packages/orchestration/config.py
packages/orchestration/result_tour.py tests/orchestration/test_result_tour.py
tests/ui_contracts/test_tour_overlay_contract.py tests/ui_server/test_tour_e2e_live.py
.agent/authored/f036-r6-render_measure.py` at C6: `All checks passed!`, REAL_EXIT=0.

Quoted whole from the commits that wrote them:

The new key entry (`config.py`, C3 `58eab1c36`):
```python
    ConfigKeySpec(
        key="tour.model_written",
        env_var="REMEDY_TOUR_MODEL_WRITTEN",
        description=(
            "Let the summary model write each job's guided tour at the end of "
            "its run (F036). Off by default: each tour is one summary model "
            "call, and a run makes no call the operator did not switch on; "
            "with it off, every job still gets the tour built from its own "
            "records."
        ),
        value_type=bool,
        default=False,
    ),
```

`tour_model_written` (`result_tour.py`, C3):
```python
def tour_model_written() -> bool:
    """Whether a reported terminal asks the summary model for a tour: the
    `tour.model_written` key, off by default (DECISION F036 D7 (1)).

    Reads the key the way `lessons.lessons_enabled` reads its own — the
    config import stays lazy so this module never forces `config.py` to
    load at import time.
    """
    from packages.orchestration.config import get_config

    return bool(get_config().get("tour.model_written"))
```

The changed lines of `write_result_tour` (`result_tour.py`, C3):
```python
    try:
        if call_fn is _UNSET_CALL_FN:
            resolved_call_fn = tour_call_fn() if tour_model_written() else None
        else:
            resolved_call_fn = call_fn
        tour = generate_result_tour(job, resolved_call_fn)
```

The overlay's `data-shown` line (`TourOverlay.tsx`, C4a `0228efe9c`):
```tsx
      <section role="dialog" aria-label="Guided tour" className={styles.card} data-ui="tour-overlay"
               data-shown={backdropVisible ? "false" : "true"}>
```

The new CSS rule (`TourOverlay.module.css`, C4a):
```css
/* While a stop is shown (DECISION F036 D7 (2), R-1088), the card leaves the centre for the
   lower left of the left rail — the place "Show me" opens is undimmed, not covered by the
   card that pointed at it — and returns to the centre rule above when stepping dims again. */
.card[data-shown="true"] {
  top: auto;
  left: 16px;
  bottom: 16px;
  transform: none;
  width: calc(var(--remedy-left-width) - 32px);
  max-height: 60vh;
}
```

**G4 THE TESTS AND THE RENDER** — the block's 28-target serial selection at C5 (`95d4ca1be`, tip
unchanged through C6):
```
1994 passed, 5 skipped in 97.42s (0:01:37)
REAL_EXIT=0
```
The reviewer's stated baseline (the same selection less `test_tour_e2e_live.py`, at `8c98cadf`)
read `1988 passed, 5 skipped`. 1994 − 1988 = 6 new nodes: `tests/orchestration/test_result_tour.py`
went from 49 to 53 collected tests (+4: the switch's default, the off/on unset split and the
handed-in-call-function test replacing the one old test whose "unset always calls it once" reading
DECISION F036 D7 (1) deliberately overturns, plus `_apply_terminal`'s own off-switch test), plus
one new test in `test_tour_overlay_contract.py` (8 → 9), plus the one test in the new
`test_tour_e2e_live.py` file (0 → 1, excluded from the reviewer's own baseline by name). 4 + 1 + 1
= 6. No discrepancy. SKIPPED lines (all 5, identical to the reviewer's stated baseline — 4 F252
quarantines in `tests/ui_contracts/` and the one in `tests/test_agent_tooling.py`):
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
```
`python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0, `ok`
true.

`python3 .agent/authored/f036-r6-render_measure.py /home/decodeux/Repos/remedy`, run at C6 tip for
this gate's own record:
```
RENDER: 10 of 10 checks pass
drive.mjs exit code: 0
```
REAL_EXIT=0, first run, no repair needed. After the run, `.remedy-wt/f036-render-run` is gone and
`git status --porcelain` is empty. Screenshots:
`.remedy-wt/f036-r6-worker/render-tour.png` (199290 bytes),
`.remedy-wt/f036-r6-worker/render-tour-shown.png` (369133 bytes).

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f036-r6-mut 95cb5bf08` then
`python3 -B .agent/authored/f036-r6-mutations.py .remedy-wt/f036-r6-mut`, whole output:
```
control (start) PYTHON: exit=0 failed=0 tests=[]
control (start) CONTRACT: exit=0 failed=0 tests=[]
m1 the key's default is True: runner=PYTHON exit=1 failed=3 tests=['tests/orchestration/test_result_tour.py::test_tour_model_written_reads_false_by_default', 'tests/orchestration/test_result_tour.py::test_unset_calls_tour_call_fn_only_when_the_switch_is_on', 'tests/orchestration/test_result_tour.py::TestApplyTerminalWritesTheTour::test_with_the_switch_off_all_green_writes_a_fallback_tour_and_never_calls_tour_call_fn'] caught=True restored=True
m2 write_result_tour asks tour_call_fn() whatever the key: runner=PYTHON exit=1 failed=2 tests=['tests/orchestration/test_result_tour.py::test_unset_calls_tour_call_fn_only_when_the_switch_is_on', 'tests/orchestration/test_result_tour.py::TestApplyTerminalWritesTheTour::test_with_the_switch_off_all_green_writes_a_fallback_tour_and_never_calls_tour_call_fn'] caught=True restored=True
m3 tour_model_written answers the key's opposite: runner=PYTHON exit=1 failed=3 tests=['tests/orchestration/test_result_tour.py::test_tour_model_written_reads_false_by_default', 'tests/orchestration/test_result_tour.py::test_unset_calls_tour_call_fn_only_when_the_switch_is_on', 'tests/orchestration/test_result_tour.py::TestApplyTerminalWritesTheTour::test_with_the_switch_off_all_green_writes_a_fallback_tour_and_never_calls_tour_call_fn'] caught=True restored=True
m4 the .card[data-shown="true"] rule is removed: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_the_card_carries_data_shown_and_docks_over_the_left_rail_while_shown'] caught=True restored=True
m5 the card's data-shown attribute is removed: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_the_card_carries_data_shown_and_docks_over_the_left_rail_while_shown'] caught=True restored=True
control (end) PYTHON: exit=0 failed=0 tests=[]
control (end) CONTRACT: exit=0 failed=0 tests=[]
restored byte-identical: True (m1 the key's default is True (packages/orchestration/config.py))
restored byte-identical: True (m2 write_result_tour asks tour_call_fn() whatever the key (packages/orchestration/result_tour.py))
restored byte-identical: True (m3 tour_model_written answers the key's opposite (packages/orchestration/result_tour.py))
restored byte-identical: True (m4 the .card[data-shown="true"] rule is removed (apps/ui/src/components/tour/TourOverlay.module.css))
restored byte-identical: True (m5 the card's data-shown attribute is removed (apps/ui/src/components/tour/TourOverlay.tsx))
PRIMARY checkout git status --porcelain:
(empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. No mutation stayed green; no extra test was needed. `git worktree remove --force
.remedy-wt/f036-r6-mut`, `git worktree prune`, `git worktree list | wc -l` = 61 (matches step 4).
`git status --porcelain` empty.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4a | deviated | the block's single C4 (product repair) split under constraint 2 — declared below |
| C4b | deviated | C4, render half part 1, split under constraint 2 — declared below |
| C4c | deviated | C4, render half part 2, split under constraint 2 — declared below |
| C5 | done | |
| C6 | done | |
| C7 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | every mutation caught first run; no extra test needed |

## Authored-text proofs

`booking.diff` applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never edited,
never retyped. Both payloads (`booking.diff`, `plan.md`) were verified line count/byte count/sha256
against the PAYLOADS table before use, and the committed `.agent/authored/f036-r6-*` copies read
back byte-identical to their sources via `git show` (G1, above). `.agent/plan.md` was REWRITTEN to
the payload file by `shutil.copyfile`, never hand-edited; its post-write sha256 equals the payload
table's own row and C2's resulting file hashes matched the reviewer's G2 table exactly for all 3
files (see Verification, G2). No other reviewer-authored text was applied this round. The switch,
the dock, the render files' two real changes (`main.tsx`'s import, `drive.mjs`'s C-i/C-j), the
end-to-end live test and the mutation tool are worker-authored against the block's specification,
not transcribed from a payload; the other three render files (`index.html`, `vite.config.mjs`,
`measure.py`) are byte-copies of round 5's own committed files by `shutil.copyfile`, per S3's "copies
of round 5's with these changes only" — verified by re-reading each after the copy.

## Deviations & assumptions

- **C4 split into C4a, C4b and C4c (constraint 2).** The block's single C4 — the product repair
  (`TourOverlay.tsx`, its CSS module, the contract test's additions) plus the five render files
  plus `f036-r6-render.txt` — numstats to 773 insertions together, over the 500-line cap. Split
  into C4a (the product repair, 23 insertions), C4b (the render harness's page, module, config and
  runner — `index.html`, `main.tsx`, `vite.config.mjs`, `measure.py`, 360 insertions) and C4c (the
  driver and its recorded run — `drive.mjs`, `f036-r6-render.txt`, 390 insertions), each its own
  subject, exactly as constraint 2 orders. `## Next`'s and G3/G4/G5's references to "C4" in the
  block name the bundle step; this handback and the gates use `0228efe9c` (C4a, the commit holding
  the actual product repair) where a single concrete commit is named for R-1088's own fix, and
  `4057564e9` (C4c, the tip of the split) is the commit `.agent/authored/f036-r6-render.txt` and
  `f036-r6-render_drive.mjs` live at.
- **An existing test's assertion was corrected to match this round's own mandated behaviour
  change (declared per AGENTS.md "If Blocked" / commit-gate transparency, not silently).**
  `tests/orchestration/test_result_tour.py::test_call_fn_none_never_calls_tour_call_fn_and_unset_calls_it_once`,
  written before this round, asserted that `write_result_tour(job)` with `call_fn` UNSET always
  called `tour_call_fn()` once — exactly the R-1089 defect DECISION F036 D7 (1) orders repaired.
  S1 is explicit and verbatim about the new contract ("`write_result_tour` with no call function
  handed in uses `tour_call_fn()` when `tour_model_written()` is true and `None` otherwise"), and
  "THE TESTS beside S4" names this exact scenario as required new coverage. The old test was
  replaced by four narrower tests covering exactly what S1 and "THE TESTS" ask for: the key's
  default (`test_tour_model_written_reads_false_by_default`), `call_fn=None` never calling
  `tour_call_fn` whatever the key (`test_call_fn_none_never_calls_tour_call_fn_whatever_the_key`),
  unset calling it only when the switch is on
  (`test_unset_calls_tour_call_fn_only_when_the_switch_is_on`, using `monkeypatch.setenv` +
  `reset_config()` exactly as `test_lessons.py` does), and a handed-in call function used whatever
  the key (`test_a_call_function_handed_in_is_used_whatever_the_key`). This is not the constraint-4
  "an EXISTING test that goes red is never edited to pass" case — that rule guards against silently
  hiding a real regression; here the block's own specification is the authority ordering the old
  assertion false, and the replacement is a strict superset of coverage, landed in C3 and declared
  here rather than passed over silently.
- No other deviation. Every mutation in G5 was caught on the first (and only) official run; no
  additional test was needed. No red gate was hit against a payload or against committed code. The
  DRY validation run of the mutation tool before C6 was committed (see External actions) is not a
  gate and is declared for transparency only — its own "primary checkout clean" leg read False
  purely because the tool file itself was still untracked at that moment; every mutation's catch and
  restoration already read exactly as the official G5 run later confirmed.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of this round (F036 round 6). (3) The closure sequence: the Built State and
the docs, the one full-suite run, the evidence package and the STATUS acceptance. Open-findings
count: 2 (R-1088 and R-1089, landed and awaiting the reviewer's resolution). Operator-questions
count: 1.
