# Handoff — F036, round 5 (book round 4, resolve R-1087, record DECISION F036 D6; land T003's
second half: the tour overlay with its backdrop, stepping and "Show me", its button and mount in
the shell, and a headless render)

## Session

SESSION 1 of feature F036 · round 5 · rounds so far 5. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, DECISION F036 D6
and its booking diff, and every required source file in full (`resultTour.ts`/`.test.ts` as
round 4 left them, `loadTourView`/`diffEnvelopePath` in `remedyApi.ts`, `LessonsOverlay.tsx` and
its CSS module, `AddTaskSheet.tsx`'s `createPortal` half, `RightLivePanel.tsx`,
`RemedyShell.tsx`, `shellSelectionIdOf` in `brainView.ts`, `buildDiffFileSummaries`/
`DiffFileSummary` in `diffViewModel.ts` and `DiffFileSidebar.tsx`'s own scroll pattern,
`tokens.css`, the design reference's assumption log, `test_lessons_overlay_contract.py`,
`test_main_layout_guard.py`, `test_raw_colour_ratchet.py`, `test_brain_stream_ring.py`'s
`strip_ts_comments` and its `<RightLivePanel` checks, the five `f035-r7-render_*` files and
`f035-r7-render.txt`, and `f036-r4-mutations.py`); wrote the three pure rules, `TourOverlay.tsx`
and its CSS module, the shell's tour state/mount/handlers/scroll-effect, the `RightLivePanel`
button, the vitest additions, the new contract test, the five render files, ran the render
harness twice (once to catch a Chrome `color-mix()` computed-style mismatch, once green), wrote
the mutation tool, and ran every gate (G1–G5) for real before writing this handback.

## Range

Review of `9ac3f7509..HEAD` (`HEAD` is this handback's own commit, `F036 R5 C7`, on
`feature/f036-guided-result-tour`).

## Commits

### 2044be894 F036 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r5-assumption_line.md | 1/0 | copy of the reviewer's assumption_line.md payload |
| .agent/authored/f036-r5-block.md | 270/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r5-booking.diff | 64/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r5-plan.md | 28/0 | copy of the reviewer's plan.md payload |

Measured 363 insertions total (block's 270 lines + 93, exactly as the block's own C1 note orders).

### cc96c8786 F036 R5 C2: book round 4, resolve R-1087, record DECISION F036 D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 44/0 | DECISION F036 D6 appended by booking.diff |
| .agent/live_review.md | 4/0 | round 4's `Gate: F036 R4 —` entry and `Landed: R-1087` note appended by booking.diff |
| .agent/plan.md | 7/7 | rewritten to the reviewer's plan.md payload |

Measured exactly the block's own G2/C2 expected numstat: 44/0, 4/0, 7/7.

### c3ea95fc0 F036 R5 C3: show the tour as an overlay with a backdrop, stepping and Show me
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/resultTour.ts | 30/0 | S1 `tourGeneratorLabel`, `tourCanShow`, `tourDiffRowKey` |
| apps/ui/src/components/panels/RightLivePanel.tsx | 4/1 | S3 `onOpenTour` prop and the Tour button beside Lessons |
| apps/ui/src/components/shell/RemedyShell.tsx | 46/1 | S4 `tourOpen`/`tourDiffPath` state, the scroll effect, `handleTourShowAnchor`, the `<RightLivePanel>` prop and the `<TourOverlay>` mount |
| apps/ui/src/components/tour/TourOverlay.module.css | 97/0 | S2 NEW FILE: backdrop, card and its contents' CSS, every value a `--remedy-*` token |
| apps/ui/src/components/tour/TourOverlay.tsx | 157/0 | S2 NEW FILE: the overlay component |
| docs/ui/design_reference/assumption_log.md | 1/0 | S5 assumption_line.md appended byte for byte |

335 insertions total (no expected number stated by the block for C3; measured).

### e51e5d1dc F036 R5 C4: test the overlay's rules and pin its contract
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/resultTour.test.ts | 51/1 | vitest tests of `tourGeneratorLabel`, `tourCanShow`, `tourDiffRowKey`, and `diffEnvelopePath`'s empty-task-id job scope |
| tests/ui_contracts/test_tour_overlay_contract.py | 78/0 | NEW FILE: the overlay/shell/panel source pins THE TESTS orders |

129 insertions total (no expected number stated; measured).

### 956c58ac4 F036 R5 C5a: write the render harness's page, its module and its driver
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r5-render_drive.mjs | 291/0 | the CDP driver: C-a to C-h |
| .agent/authored/f036-r5-render_index.html | 11/0 | the scratch page |
| .agent/authored/f036-r5-render_main.tsx | 129/0 | mounts the real `TourOverlay` against one fixed six-stop view |
| .agent/authored/f036-r5-render_vite.config.mjs | 28/0 | the scratch build config |

459 insertions (see Deviations — the block's single C5 was split under constraint 2).

### 6d1ee832a F036 R5 C5b: run the render harness and record its checks
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r5-render.txt | 32/0 | the harness's whole recorded output, `RENDER: 8 of 8 checks pass` |
| .agent/authored/f036-r5-render_measure.py | 191/0 | the runner: builds, serves, drives headless Chrome, stops both by pid |

223 insertions (the block's single C5's second half).

### 69649ae50 F036 R5 C6: add the round 5 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r5-mutations.py | 201/0 | the G5 red-proof tool: m1–m7 across resultTour.ts, TourOverlay.tsx and RemedyShell.tsx |

### <this commit> F036 R5 C7: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f036-r5-mut 69649ae50` — the official G5 worktree, cut
  from C6 per the block. Outcome: worktree created at detached HEAD `69649ae50`.
- `git worktree remove --force .remedy-wt/f036-r5-mut` then `git worktree prune` — the official
  G5 worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 61,
  matching the round's step-4 reading.
- `git push -u origin feature/f036-guided-result-tour` — run immediately after this commit per
  the bundle order. Its real outcome is reported in the round's reply (G6), not here, because
  this file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use), all MATCH:
```
assumption_line.md: 1 line,   825 bytes, sha256 570e89b5009aee14c13e7ee2299c3c2429314f0957e6161c8c865e15d93673d1
booking.diff:       64 lines, 10055 bytes, sha256 1a17f57ef32593028adb6d8fb4e263aa450e6f71a2359c5946f736a7182070b4
plan.md:            28 lines, 927 bytes, sha256 65255245e009e45b6849cec241238b00e3659888c49023edbd915bb58b64584b
```
Block self-check: 270 lines, sha256 `365e274af1f90f19d476aa3de206b8b5fc1aa2a12860d52019f877dbfba4f870`
— MATCH on both readings given in the delegation message. `.agent/authored/f036-r5-*` copies vs.
sources, read back via `git show 2044be894:<path>`, all byte-identical:
```
f036-r5-block.md           vs .remedy-wt/f036-r5/block.md                    MATCH
f036-r5-assumption_line.md vs .remedy-wt/f036-r5-payloads/assumption_line.md MATCH
f036-r5-booking.diff       vs .remedy-wt/f036-r5-payloads/booking.diff       MATCH
f036-r5-plan.md            vs .remedy-wt/f036-r5-payloads/plan.md            MATCH
```
`docs/ui/design_reference/assumption_log.md` at C3 (`c3ea95fc0`) equals its bytes at `9ac3f7509`
followed by `assumption_line.md`'s, byte for byte: MATCH.

**G2 THE BOOKING** — every file's bytes and sha256 at C2 (`git show cc96c8786:<path>`) MATCHED
the reviewer's table exactly:
```
.agent/decisions.md   2368177 bytes  sha256 5a4bcc1eac838c749e535d7b6ca7e17023de911365fcb17b6e2bac4da99560d2 MATCH
.agent/live_review.md  324894 bytes  sha256 0c57a55cad4cf14f9f0fd96b846b4ae952f339827d7901f2f06c68b59a2c0256 MATCH
.agent/plan.md            927 bytes  sha256 65255245e009e45b6849cec241238b00e3659888c49023edbd915bb58b64584b MATCH
```
`open_finding_ids` over `.agent/live_review.md` TEXT at C2 (via `scripts.rotate_live_review`) read
`[]`, matching the reviewer's stated reading. `latest_gate_verdict` read `PASS`, matching.
`git diff --name-only 2044be894 cc96c8786` named exactly the 3 paths of the G2 table, no more, no
fewer.

**G3 THE CODE** — `python3 -m ruff check tests/ui_contracts/test_tour_overlay_contract.py
.agent/authored/f036-r5-render_measure.py` at C6: `All checks passed!`, REAL_EXIT=0.

Quoted whole from C3 (`c3ea95fc0`):

`TourOverlay.tsx`'s read effect:
```tsx
  useEffect(() => {
    let cancelled = false;
    void loadTourView({ jobId, token: serverToken }).then((view) => {
      if (!cancelled) setRead({ view });
    });
    return () => { cancelled = true; };
  }, [jobId, serverToken]);
```

`TourOverlay.tsx`'s keydown listener:
```tsx
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      else if (event.key === "ArrowLeft") stepTo(neighbours.previous);
      else if (event.key === "ArrowRight") stepTo(neighbours.next);
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose, neighbours.previous, neighbours.next]);
```

The backdrop's CSS rule (`TourOverlay.module.css`):
```css
.backdrop {
  position: fixed;
  inset: 0;
  z-index: calc(var(--remedy-z-overlay) - 1);
  background: color-mix(in srgb, var(--remedy-ink-strong) 45%, transparent);
}
```

The card's CSS rule:
```css
.card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: var(--remedy-z-overlay);
  width: min(560px, calc(100vw - 48px));
  max-height: calc(100vh - 96px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px 22px;
  background: var(--remedy-glass-bg-strong);
  border: 1px solid var(--remedy-glass-border);
  border-radius: var(--remedy-radius-xl);
  box-shadow: var(--remedy-shadow-card);
  backdrop-filter: blur(14px);
}
```

The shell's `onShowAnchor` handler (`RemedyShell.tsx`):
```tsx
  function handleTourShowAnchor(anchor: TourAnchor) {
    if (anchor.kind === "node") {
      onSelectNode(shellSelectionIdOf(dashboard.tasks, anchor.ref));
    } else if (anchor.kind === "diff") {
      setTourDiffPath(anchor.ref);
      setOpenDiffTaskId("");
    }
  }
```

The shell's scroll effect:
```tsx
  useEffect(() => {
    if (diffEnvelope === null || tourDiffPath === null) return;
    const rowKey = tourDiffRowKey(buildDiffFileSummaries(diffEnvelope), tourDiffPath);
    if (rowKey !== null) {
      document.getElementById(rowKey)?.scrollIntoView({ block: "start" });
    }
    setTourDiffPath(null);
  }, [diffEnvelope, tourDiffPath]);
```

S1's rules (`resultTour.ts`):
```ts
export function tourGeneratorLabel(generator: string): string {
  return generator === TOUR_GENERATOR_SUMMARY_ROLE
    ? "Written by the summary model and checked against the job's records"
    : "Built from the job's records";
}

export function tourCanShow(anchor: TourAnchor): boolean {
  return anchor.kind === "node" || anchor.kind === "diff";
}

export function tourDiffRowKey(
  summaries: Array<{ path: string; rowKey: string }>,
  path: string,
): string | null {
  const found = summaries.find((summary) => summary.path === path);
  return found ? found.rowKey : null;
}
```

**G4 THE TESTS AND THE RENDER** — the block's 22-target serial selection at HEAD (C6; unchanged
since C5b, which is where G4's own text anchors it):
```
1785 passed, 5 skipped in 116.01s (0:01:56)
REAL_EXIT=0
```
The reviewer's stated baseline (the same selection, at `9ac3f7509` before this round's changes)
read `1777 passed, 5 skipped`. 1785 − 1777 = 8 new nodes, all in
`tests/ui_contracts/test_tour_overlay_contract.py` (NEW FILE, 8 test functions) — the vitest
additions in `resultTour.test.ts` run under the SAME wrapper node
(`tests/orchestration/test_test_runner.py::test_vitest_passes`, which runs the whole vitest
suite in one pytest node) the baseline already counted, so they add no new pytest node. No
discrepancy. SKIPPED lines (all 5, identical to the reviewer's stated baseline —
4 F252 quarantines in `tests/ui_contracts/` and the one in `tests/test_agent_tooling.py`):
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
```
Before the full G4 run, the browser side was checked directly for a fast signal: `apps/ui/node_modules/.bin/tsc --noEmit`
— clean, exit 0; `apps/ui/node_modules/.bin/eslint src --max-warnings 0` — clean, exit 0;
`apps/ui/node_modules/.bin/vitest run src/api/resultTour.test.ts` — 32 tests passed;
`python3 -m pytest tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_main_layout_guard.py
tests/ui_contracts/test_lessons_overlay_contract.py tests/ui_contracts/test_timeline_scrub_wiring.py
tests/ui_contracts/test_brain_stream_ring.py` — 92 passed. `python3 -m apps.cli.main integrity
check --json`: all six checks `pass`, `fail_count` 0, `ok` true.

`python3 .agent/authored/f036-r5-render_measure.py /home/decodeux/Repos/remedy` — first run
caught a real bug in the driver itself (not the product): Chrome resolves
`color-mix(in srgb, ...)` to a `color(srgb r g b / a)` computed-style string rather than
`rgba(...)`, so C-a's regex-based "not transparent" check read false; repaired to check the
computed string is neither `"transparent"` nor `"rgba(0, 0, 0, 0)"` rather than parsing a
specific colour function's syntax. Second run:
```
RENDER: 8 of 8 checks pass
drive.mjs exit code: 0
```
Real exit code 0 both times (the runner's own overall exit reflects `drive.mjs`'s, which was 1 on
the first run and 0 on the second — the whole second run's output is what is saved as
`f036-r5-render.txt`, per C5's own note that the round declares a within-round correction before
using a result). After the run, `.remedy-wt/f036-render-run` is gone and `git status --porcelain`
is empty. Screenshots: `.remedy-wt/f036-r5-worker/render-tour.png` (29666 bytes),
`.remedy-wt/f036-r5-worker/render-tour-shown.png` (31137 bytes).

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f036-r5-mut 69649ae50` then
`python3 -B .agent/authored/f036-r5-mutations.py .remedy-wt/f036-r5-mut`, whole output:
```
control (start) VITEST: exit=0 failed=0 tests=[]
control (start) CONTRACT: exit=0 failed=0 tests=[]
m1 tourCanShow holds for command: runner=VITEST exit=1 failed=1 tests=['tourCanShow fails for an evidence and a command anchor'] caught=True restored=True
m2 tourDiffRowKey answers the LAST matching summary's key: runner=VITEST exit=1 failed=1 tests=["tourDiffRowKey answers the FIRST matching summary's key"] caught=True restored=True
m3 tourGeneratorLabel calls every generator model-written: runner=VITEST exit=1 failed=1 tests=['tourGeneratorLabel reads mechanical for any other generator'] caught=True restored=True
m4 the overlay renders in place, without createPortal: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_the_overlay_is_a_dialog_portaled_to_the_document_body'] caught=True restored=True
m5 the Escape handling is removed: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_escape_closes_the_overlay'] caught=True restored=True
m6 the tour mounts inside <main> instead of after it: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_the_shell_mounts_the_overlay_outside_the_main_column'] caught=True restored=True
m7 a diff stop opens the diff of the task id "x", not the job's: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_the_shell_opens_the_jobs_whole_diff_and_finds_the_diff_stops_row'] caught=True restored=True
control (end) VITEST: exit=0 failed=0 tests=[]
control (end) CONTRACT: exit=0 failed=0 tests=[]
restored byte-identical: True (m1 tourCanShow holds for command (apps/ui/src/api/resultTour.ts))
restored byte-identical: True (m2 tourDiffRowKey answers the LAST matching summary's key (apps/ui/src/api/resultTour.ts))
restored byte-identical: True (m3 tourGeneratorLabel calls every generator model-written (apps/ui/src/api/resultTour.ts))
restored byte-identical: True (m4 the overlay renders in place, without createPortal (apps/ui/src/components/tour/TourOverlay.tsx))
restored byte-identical: True (m5 the Escape handling is removed (apps/ui/src/components/tour/TourOverlay.tsx))
restored byte-identical: True (m6 the tour mounts inside <main> instead of after it (apps/ui/src/components/shell/RemedyShell.tsx))
restored byte-identical: True (m7 a diff stop opens the diff of the task id "x", not the job's (apps/ui/src/components/shell/RemedyShell.tsx))
PRIMARY checkout git status --porcelain:
(empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. No mutation stayed green; no extra test was needed. `git worktree remove --force
.remedy-wt/f036-r5-mut`, `git worktree prune`, `git worktree list | wc -l` = 61 (matches step 4).
`git status --porcelain` empty.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5a | deviated | split from the block's single C5 under constraint 2 — the five render files plus their run output numstat to 682 insertions together, over the 500-line cap; declared here |
| C5b | deviated | the render runner and its recorded output half of the block's C5, split out for the same reason |
| C6 | done | |
| C7 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | every mutation caught first run; no extra test needed |

## Authored-text proofs

`booking.diff` applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never edited,
never retyped. All three payloads (`assumption_line.md`, `booking.diff`, `plan.md`) were verified
line count/byte count/sha256 against the PAYLOADS table before use, and the committed
`.agent/authored/f036-r5-*` copies read back byte-identical to their sources via `git show` (G1,
above). `.agent/plan.md` was REWRITTEN to the payload file by `shutil.copyfile`, never
hand-edited; its post-write sha256 equals the payload table's own row and C2's resulting file
hashes matched the reviewer's G2 table exactly for all 3 files (see Verification, G2).
`docs/ui/design_reference/assumption_log.md` gained `assumption_line.md`'s bytes appended, byte
for byte (G1). No other reviewer-authored text was applied. The S1–S6 rules/overlay/shell
wiring/tests/render harness/mutation tool are worker-authored against the block's specification,
not transcribed from a payload.

## Deviations & assumptions

- **C5 split into C5a and C5b (constraint 2).** The block's single C5 — the five render files
  (`index.html`, `main.tsx`, `vite.config.mjs`, `drive.mjs`, `measure.py`) plus
  `f036-r5-render.txt` — numstats to 682 insertions together, over the 500-line cap. Split into
  C5a (the four template files, 459 insertions) and C5b (`measure.py` plus `render.txt`, 223
  insertions), each its own subject, exactly as constraint 2 orders. `## Next`'s and G4/G5's
  references to "C5" in the block name the bundle step; this handback and the gates use
  `6d1ee832a` (C5b, the tip of the split) as the concrete commit where relevant.
- **The render harness's own C-a check needed one repair before it read green** (see G4,
  above): Chrome's computed `background-color` for a `color-mix()` value is not the `rgba(...)`
  string the first draft's regex expected. This is a defect in the EVIDENCE tool the round wrote
  this session, not in the product; it was found and repaired before C5b was committed (C5b
  carries only the corrected, green run), so no separate correction round applies and nothing
  under AGENTS.md "If Blocked" was triggered.
- No other deviation. Every mutation in G5 was caught on the first (and only) official run; no
  additional test was needed. No red gate was hit against a payload or against committed code.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of this round (F036 round 5). (3) The demo's tour and the end-to-end proof
of one real job's tour through both doors (the browser overlay and the command line), with the
feature's Built State. Open-findings count: 0. Operator-questions count: 1.
