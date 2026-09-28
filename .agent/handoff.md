# Handback — F039, round 5: book round 4 with R-1100's repair, and land T002's in-app story panel

## Session

SESSION 1 of feature F039 · round 5 · rounds so far 5. This session ran round 5 only: booking
round 4's PASS, registering and repairing finding R-1100 (three docstrings that promised a
configuration change reaches the cockpit without a restart, when `get_config` loads it once per
process and keeps it), recording DECISION F039 D6, and landing T002's in-app story panel — the
pure rules of `storyPlayer.ts` with its golden walkthrough, the docked panel `StoryPanel.tsx`
with its CSS module and its Story entry in `RightLivePanel.tsx`/`RemedyShell.tsx`, one line in the
assumption log, and a headless render that proves the panel over the real timeline scrub. Context
self-assessment: a comfortable margin remained through the round, including the full targeted
pytest selection, the headless render (run twice — once during development, once at the gate) and
all ten mutation red-proofs in one run of the tool; the work was not near its limit.

For the operator, in plain words: round 4 is booked PASS and R-1100 is booked landed (awaiting the
next review). A finished job can now be replayed as a story from inside the cockpit: a small panel
docks over the graph's lower-left corner, says which chapter the timeline is at in plain words, and
offers a Play button that walks the ledger chapter by chapter and event by event, at a steady pace,
narrating each beat's outcome and — when the ownership ledger can say so — who acted. Previous and
Next step between chapters directly; the timeline's own scrubber, the graph and the phase bar all
move together with it, because the story drives the SAME position they already read, not a copy of
its own. Escape closes it; the space bar pauses and resumes it. T002 is now closed.

## Range

Review of `c4a1cf5d7`..`HEAD` (the commit that writes this file is the eleventh in the range). TEN
commits precede it: C1a, C1b, C2, C3, C4, C5, C6, C7a, C7b and C8 — the block's lettered bundle
with ONE declared split (C7 became C7a/C7b; see Deviations).

## Commits

### c87b7a59f F039 R5 C1a: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r5-block.md | 309/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f039-r5-plan.md | 30/0 | the plan payload, copied verbatim |
| .agent/authored/f039-r5-assumption_line.md | 1/0 | the assumption-log-line payload, copied verbatim |

(measured: `git show c87b7a59f --numstat` reads `1 0`, `309 0`, `30 0`, total 340 — exactly the
block's own expected reading (309 + 31), under the 500-line cap.)

### 045093e42 F039 R5 C1b: copy round 5 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r5-records.diff | 58/0 | the records-diff payload, copied verbatim |

(measured: `git show 045093e42 --numstat` reads `58 0` — exactly the block's expected 58.)

### 241f3c6bc F039 R5 C2: book round 4, register R-1100, record D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 38/0 | records.diff appends DECISION F039 D6 |
| .agent/live_review.md | 4/0 | records.diff appends round 4's Gate entry and R-1100's registration |
| .agent/plan.md | 6/10 | records.diff, then rewritten := plan.md (round 5's plan) |

(measured: `git show 241f3c6bc --numstat` reads `38 0`, `4 0`, `6 10` — exactly the block's own
expected reading in C2's own line and G2's table.)

### 0bbf11543 F039 R5 C3: say when a configuration change takes effect (R-1100)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | one blank line plus one `Landed: R-1100 — ` line, naming no commit |
| packages/orchestration/ui_server.py | 7/6 | S1: the docstrings of `_build_story_section` and `_rate_limit_admits_command` now say the value is read on every request from the process's configuration, which `get_config` loads once and keeps, so a change takes effect when the cockpit restarts (R-1100); no code changed |
| tests/ui_server/test_story_section.py | 18/2 | S1: the module docstring gets the same correction; ONE new test — `step_ms` reads 420 with the variable unset, STILL reads 420 after `monkeypatch.setenv("REMEDY_STORY_STEP_MS", "900")` (the cache holds), then reads 900 after `reset_config()`, undoing the variable and resetting again in a `finally` |

(measured: `git show 0bbf11543 --numstat` reads `2 0`, `7 6`, `18 2`, total 27; the block gave no
expected reading for C3.)

### bb6c38fc5 F039 R5 C4: golden the story's walkthrough and the panel's words
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyPlayer.ts | 80/0 | NEW pure module, S2: `STORY_RUNNING_LINE`, `storyPositionLabel`, `storyPlayStart`, `storyBeatsAt`, `StoryFrame`, `storyWalk` — importing only from `./storyAutoplay`, `./storyNarration` and `./storyView` |
| apps/ui/src/components/story/storyPlayer.test.ts | 99/0 | NEW vitest goldens, HAND-DERIVED: `storyWalk` over the demo recording as one ten-frame literal (waits 2020, 2020, 420×7, 2020; labels; cards; beat counts 0,1,1,2,2,2,1,1,2,0) and one three-frame reduced-motion literal (positions -1→0→1→9 read as 0,1,9 each 1600ms, beat counts 0,1,0); `[]` for an empty ledger; every `storyPositionLabel` case including position 10's "After the last event"; `STORY_RUNNING_LINE` verbatim; `storyPlayStart` for LIVE, the last seq, position 4, position -1, and an empty view |

(measured: `git show bb6c38fc5 --numstat` reads `99 0`, `80 0`, total 179, under the 500-line cap;
the block gave no expected reading for C4.)

### fab964e41 F039 R5 C5: tell the story in a panel over the timeline's scrub
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/StoryPanel.tsx | 159/0 | NEW, S3: the docked panel, portaled to `document.body`, no backdrop; chapters, the reached card's beats/cost, Previous/Next/Play-Pause/Close, one timer effect, Escape/Space keydown |
| apps/ui/src/components/story/StoryPanel.module.css | 84/0 | NEW, S3: every colour/shadow/radius a `--remedy-*` token; docked left/bottom, 360px, 60vh scroll, z-overlay; current chapter in `--remedy-purple` |
| apps/ui/src/components/panels/RightLivePanel.tsx | 4/1 | S4: optional `onOpenStory?: () => void`; Story button directly after Tour |
| apps/ui/src/components/shell/RemedyShell.tsx | 10/1 | S4: `storyOpen` state under a DECISION F039 D6 comment; `onOpenStory` passed beside `onOpenTour`; `StoryPanel` mounted directly after the tour's mount, outside `<main>` (still exactly four children) |
| docs/ui/design_reference/assumption_log.md | 1/0 | S5: the assumption line, appended byte for byte |

(measured: `git show fab964e41 --numstat` reads `4 1`, `10 1`, `84 0`, `159 0`, `1 0`, total 258 net
(260 insertions, 2 deletions), under the 500-line cap; the block gave no expected reading for C5.)

### 4e66afb6e F039 R5 C6: pin the story panel's seams
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_story_panel_contract.py | 87/0 | NEW Python guard, S6: the panel's `createPortal`/`document.body`/`data-ui`/`role`/`autoplayStep`/`buildStoryView`/`useReducedMotion`/exactly-one-`setTimeout`/`clearTimeout`/no-`fetch`; the CSS's `--remedy-z-overlay` and `--remedy-purple` with no raw colour; `storyPlayer.ts`'s three import specifiers and purity; the shell's `</main>` before `<StoryPanel`, `onOpenStory` and `scrub={scrub}`; the right panel's Story button |

(measured: `git show 4e66afb6e --numstat` reads `87 0`, under the 500-line cap.)

### 371e4c412 F039 R5 C7a: build the story panel's render harness scaffold and host page
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r5-render_index.html | 11/0 | NEW, S7: the harness's host page |
| .agent/authored/f039-r5-render_main.tsx | 77/0 | NEW, S7: mounts the real `useTimelineScrub`, `PhaseTimeline` and `StoryPanel` over the demo recording inside `ReducedMotionProvider`; records every scrub position and the close on `window` |
| .agent/authored/f039-r5-render_measure.py | 191/0 | NEW, S7: the runner — fresh work dir, vite build, http.server on 8996, headless Chrome on CDP 9366, `drive.mjs`, pid-based teardown |
| .agent/authored/f039-r5-render_vite.config.mjs | 28/0 | NEW, S7: the scratch vite config |

(measured: `git show 371e4c412 --numstat` reads `11 0`, `77 0`, `191 0`, `28 0`, total 307, under
the 500-line cap. DEVIATION: this is HALF of C7 as the block named it — see Deviations.)

### c217bde63 F039 R5 C7b: render the story panel headless and record its checks
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r5-render_drive.mjs | 298/0 | NEW, S7: the CDP driver — checks C-a through C-h, one screenshot after C-c |
| .agent/authored/f039-r5-render.txt | 31/0 | NEW, S7: the harness's own saved stdout, `RENDER: 8 of 8 checks pass`, exit 0 |

(measured: `git show c217bde63 --numstat` reads `298 0`, `31 0`, total 329, under the 500-line cap.
DEVIATION: this is the other half of C7 — see Deviations.)

### 8654dbafb F039 R5 C8: add the mutation tool for the story panel and R-1100
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r5-mutations.py | 187/0 | NEW mutation tool, `m1`–`m10`, following `f039-r4-mutations.py`'s route: vitest over the worktree's `storyPlayer.test.ts` from the primary's `apps/ui`, pytest over `test_story_panel_contract.py` and `test_story_section.py` from the worktree with it first on `PYTHONPATH` |

(measured: `git show 8654dbafb --numstat` reads `187 0`, under the 500-line cap.)

## External actions

`git worktree add --detach .remedy-wt/f039-r5-mut 8654dbafb` before the (single, successful) G5
run; `git worktree remove --force .remedy-wt/f039-r5-mut` and `git worktree prune` after it —
`git worktree list | wc -l` read 62 before the add and 62 after the remove (step 4's reading,
unchanged). `git push origin feature/f039-story-replay-mode` after this commit — reported in the
worker's final reply, since this file is written and C9 committed before that push, per the
block's ordering.

## Verification

BEFORE ANYTHING ELSE:
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
(absent, as required)
```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f039-story-replay-mode
$ git log --oneline -1
c4a1cf5d7 F039 R4 C8: rewrite handoff for round 4
```
Block bytes: measured line count 309 and sha256
`250889aace7c88f1f9114db89b2ae52f46896028d6f8047f5ad7646757099f0a` — MATCH both given readings.
`git worktree list | wc -l` at step 4: 62.

PAYLOADS — all three measured and MATCH the block's table exactly:
| file | lines | bytes | sha256 | verdict |
|---|---|---|---|---|
| assumption_line.md | 1 | 1014 | `027fa00d2ae812d32da0d39199ca12068eb34984ccf8b0642abcf80c3fd5a678` | MATCH |
| plan.md | 30 | 1040 | `81aec753edd444ae1d213bb207528c99539c1cc747dfde8fbeee0792635a5385` | MATCH |
| records.diff | 58 | 10965 | `9000671547adb1d6fd6f7a7b261e460d2c2581ccf17d9e518785d564389508f9` | MATCH |

C1a: measured insertions 340 (309 + 31), under the 500-line cap — no STOP required.

G1 TRANSPORT — all three `.agent/authored/f039-r5-*` payload copies, read back with `git show
<commit>:<path>`, equal their sources byte for byte: block.md (against
`.remedy-wt/f039-r5/block.md`, at C1a — 25057 bytes both sides), plan.md (against the payload, at
C1a), assumption_line.md (against the payload, at C1a), records.diff (against the payload, at
C1b) — all four MATCH. The assumption log at C5 (`fab964e41`) equals the log at `c4a1cf5d7`
followed byte-for-byte by `assumption_line.md`'s bytes — MATCH.

G2 THE RECORDS, at C2 (`241f3c6bc`):
```
$ git apply --check .remedy-wt/f039-r5-payloads/records.diff
CHECK_EXIT=0
$ git apply .remedy-wt/f039-r5-payloads/records.diff
APPLY_EXIT=0
```
| path | bytes | sha256 | verdict |
|---|---|---|---|
| .agent/decisions.md | 2434466 | `dfde6038391a4fc455d9ff38df35e21bac1a384bb6548b3350f54cca576a8f0f` | MATCH |
| .agent/live_review.md | 341289 | `a5ced3615b60dd02fcab40ae354cc779bbbbd4d82c6398bcb69f7104286acb12` | MATCH |
| .agent/plan.md | 1040 | `81aec753edd444ae1d213bb207528c99539c1cc747dfde8fbeee0792635a5385` | MATCH |

`open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT: `[]` at `c4a1cf5d7`
and `['R-1100']` at C2 — both match the reviewer's own reading. `git diff --name-only 045093e42
241f3c6bc` names exactly `.agent/decisions.md`, `.agent/live_review.md` and `.agent/plan.md` —
exactly G2's table, nothing else. At C3 (`0bbf11543`): the ledger is a byte-exact prefix of the
ledger at C2, and the addition is exactly `"\n"` plus one line beginning `Landed: R-1100 — ` and
ending in `"\n"` — confirmed by direct byte slicing.

G3 THE CODE:
```
$ python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_story_section.py tests/ui_contracts/test_story_panel_contract.py .agent/authored/f039-r5-render_measure.py .agent/authored/f039-r5-mutations.py
All checks passed!
REAL_EXIT=0
```
From `git show 0bbf11543` (C3), the three S1 docstrings:
```python
def _build_story_section() -> dict[str, Any]:
    """The story's autoplay pacing (F039 T002, DECISION F039 D5): the two
    configuration keys, `story.step_ms` and `story.chapter_pause_ms`, read on
    every request from the process's configuration, which `get_config` loads
    once and keeps, so a change takes effect when the cockpit restarts
    (R-1100).
    """
```
```python
    def _rate_limit_admits_command(self, job_id: str) -> bool:
        """True while this token and this job still hold minute budget.

        The limit is read on every request from the process's configuration,
        which `get_config` loads once and keeps, so a change takes effect
        when the cockpit restarts (R-1100). A value that is not a whole
        number falls back to the registered default rather than raising: a
        typo in `remedy.toml` must not turn every command into a 500, and the
        door has to stay limited while the typo is there.
        """
```
```python
"""
Domain tests: ui_server/test_story_section.py

F039 T002, DECISION F039 D5. The story's autoplay pacing reaches the browser
as the dashboard's `story` section: `_build_story_section` reads the two
configuration keys, `story.step_ms` and `story.chapter_pause_ms`, on every
call from the process's configuration, which `get_config` loads once and
keeps, so a change takes effect when the cockpit restarts (R-1100); and
`_build_dashboard` carries that section under `story`.
"""
```
From `git show bb6c38fc5` (C4), the whole of `storyPlayer.ts`:
```typescript
// T5_F039.md T002, DECISION F039 D6 — the story's own pacing words and its
// golden walkthrough, composed once from the pure rules three sibling
// modules already own: storyAutoplay's `autoplayStep` decides where and
// when the next move lands, storyNarration's `chapterAt` and `cardAt`
// answer where the scrub sits, and storyView's whole `StoryView` carries
// the chapters, cards, seqs and pacing this module reads. Remedy
// deliberately invents no narration here either: every word this module
// prints is a chapter's own title or copied straight from `storyNarration`.
import { autoplayStep } from "./storyAutoplay";
import { cardAt, chapterAt, type NarrationBeat, type NarrationCard } from "./storyNarration";
import type { StoryView } from "./storyView";

/** What the story says while the job is still recording, so a person reading
 *  it mid-run is never told the record is the whole run (DECISION F039 D6 (2)). */
export const STORY_RUNNING_LINE =
  "This job is still running, so its story ends where the record ends now.";

/** The scrub position in words: no chapter at all when the view holds none,
 *  before the first chapter's own start, past every chapter `chapterAt` can
 *  place it in, or the chapter and title `chapterAt` finds there. */
export function storyPositionLabel(view: StoryView, position: number): string {
  if (view.chapters.length === 0) return "No event is recorded yet.";
  if (position < view.chapters[0].startSeq) return "Before the first event";
  const at = chapterAt(view.chapters, position);
  if (at === -1) return "After the last event";
  const chapter = view.chapters[at];
  return `Chapter ${at + 1} of ${view.chapters.length}: ${chapter.title}`;
}

/** Where Play starts: before the first event while the scrub is LIVE, when
 *  the view holds no seq at all, or once `position` has already reached the
 *  ledger's own last seq; otherwise exactly where the scrub already stands,
 *  so resuming mid-story never jumps the reader back. */
export function storyPlayStart(view: StoryView, position: number, live: boolean): number {
  if (live || view.seqs.length === 0) return -1;
  const lastSeq = view.seqs[view.seqs.length - 1];
  if (position >= lastSeq) return -1;
  return position;
}

/** A card's beats the scrub has reached: `[]` for no card, else the beats at
 *  or before `position`, in the card's own order — never the beats a
 *  position has not drawn on the graph yet. */
export function storyBeatsAt(card: NarrationCard | null, position: number): readonly NarrationBeat[] {
  if (card === null) return [];
  return card.beats.filter((beat) => beat.seq <= position);
}

/** One move of the golden walkthrough: the position it lands on, how long it
 *  waited to get there, that position's words, the card reached there (its
 *  first seq, or null), and how many of that card's beats the position has
 *  reached. */
export interface StoryFrame {
  position: number;
  delayMs: number;
  label: string;
  cardFirstSeq: number | null;
  beats: number;
}

/** The whole autoplay walk, from position -1 until `autoplayStep` answers
 *  null: the golden walkthrough every `storyPlayer.test.ts` literal is
 *  hand-derived against. */
export function storyWalk(view: StoryView, reducedMotion: boolean): StoryFrame[] {
  const frames: StoryFrame[] = [];
  let position = -1;
  for (;;) {
    const step = autoplayStep(view.chapters, view.seqs, position, view.pacing, reducedMotion);
    if (step === null) return frames;
    position = step.position;
    const card = cardAt(view.chapters, view.cards, position);
    frames.push({
      position,
      delayMs: step.delayMs,
      label: storyPositionLabel(view, position),
      cardFirstSeq: card === null ? null : card.firstSeq,
      beats: storyBeatsAt(card, position).length,
    });
  }
}
```
From `git show fab964e41` (C5), the panel's timer effect, its Play and its keydown listener:
```typescript
  function goToChapter(startSeq: number) {
    setPlaying(false);
    scrub.scrubTo(startSeq);
  }

  const startPlaying = useCallback(() => {
    const live = scrub.state.mode === "live";
    const start = storyPlayStart(view, position, live);
    if (live || start !== position) scrub.scrubTo(start);
    setPlaying(true);
  }, [scrub, view, position]);

  const togglePlaying = useCallback(() => {
    if (playing) setPlaying(false);
    else startPlaying();
  }, [playing, startPlaying]);

  // THE ONE TIMER (see the header comment): re-armed by `position` itself, so a manual scrub
  // while playing reschedules from the new position rather than racing an old plan.
  useEffect(() => {
    if (!playing) return;
    const step = autoplayStep(view.chapters, view.seqs, position, view.pacing, reducedMotion);
    if (step === null) {
      setPlaying(false);
      return;
    }
    const id = window.setTimeout(() => scrub.scrubTo(step.position), step.delayMs);
    return () => window.clearTimeout(id);
  }, [playing, position, view, reducedMotion, scrub]);

  // Escape stops play and closes; Space toggles play unless a text field has focus, so typing
  // a space elsewhere on the page never pauses the story by accident.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setPlaying(false);
        onClose();
        return;
      }
      if (event.key === " " || event.code === "Space") {
        const active = document.activeElement as HTMLElement | null;
        const tag = active ? active.tagName.toLowerCase() : "";
        if (tag === "input" || tag === "textarea") return;
        event.preventDefault();
        togglePlaying();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose, togglePlaying]);
```
The shell's and the right panel's changed lines, from `git show fab964e41`:
```typescript
+import { StoryPanel } from "../story/StoryPanel";
...
+  // THE STORY (F039 T002, DECISION F039 D6): open or closed; the panel reads the ledger, the
+  // ownership view and the timeline's own scrub this shell already owns, and drives that same
+  // scrub rather than keeping a position of its own.
+  const [storyOpen, setStoryOpen] = useState(false);
...
-        <RightLivePanel dashboard={dashboard} serverToken={serverToken} onSelectNode={onSelectNode} streamStatus={stream.status} replay={scrub.state.mode === "scrubbed"} recent={stream.recent} recentDropped={stream.recentDropped} onOpenLessons={() => setLessonsOpen(true)} onOpenTour={() => setTourOpen(true)} focusedTaskId={focusedTaskId} />
+        <RightLivePanel dashboard={dashboard} serverToken={serverToken} onSelectNode={onSelectNode} streamStatus={stream.status} replay={scrub.state.mode === "scrubbed"} recent={stream.recent} recentDropped={stream.recentDropped} onOpenLessons={() => setLessonsOpen(true)} onOpenTour={() => setTourOpen(true)} onOpenStory={() => setStoryOpen(true)} focusedTaskId={focusedTaskId} />
...
+      {/* THE STORY (F039 T002, DECISION F039 D6), a sibling directly after the guided tour for
+          the reason both are siblings outside <main>. */}
+      {storyOpen && (<StoryPanel dashboard={dashboard} rows={ledgerRows} ownership={ownership} scrub={scrub} onClose={() => setStoryOpen(false)} />)}
```
```typescript
-export function RightLivePanel({ dashboard, serverToken, onSelectNode, streamStatus, replay, recent, recentDropped, onOpenLessons, onOpenTour, focusedTaskId }: { ...; onOpenTour?: () => void; focusedTaskId?: string }) {
+export function RightLivePanel({ dashboard, serverToken, onSelectNode, streamStatus, replay, recent, recentDropped, onOpenLessons, onOpenTour, onOpenStory, focusedTaskId }: { ...; onOpenTour?: () => void; onOpenStory?: () => void; focusedTaskId?: string }) {
...
+      {/* The in-app story's entry point (F039 T002, DECISION F039 D6), beside Tour in the same
+          quiet style; the shell owns whether the story is open. */}
+      {onOpenStory && (<button type="button" className={styles.advancedToggle} onClick={onOpenStory}>Story</button>)}
```

G4 THE TESTS AND THE RENDER, in the primary checkout at C8 (`8654dbafb`), SERIALLY:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
2352 passed, 5 skipped in 148.22s (0:02:28)
REAL_EXIT=0
```
None of the five SKIPPED lines names `node_modules`, `dist` or vitest — all five are the same
pre-existing D3/D12 quarantines every earlier handback in this feature also names, so none is a
toolchain node this checkout should have run instead. This round's two Python test files collect,
by `--collect-only -q`: `tests/ui_server/test_story_section.py` — 4 nodes
(`test_the_section_reads_the_defaults_with_both_variables_unset`,
`test_the_section_reads_the_configured_values_when_both_are_set`,
`test_the_dashboard_carries_the_section`,
`test_a_changed_variable_takes_effect_only_after_reset_config_r1100`);
`tests/ui_contracts/test_story_panel_contract.py` — 7 nodes
(`test_the_panel_is_a_region_portaled_to_the_document_body`,
`test_the_panel_drives_the_real_scrub_and_reads_reduced_motion`,
`test_the_panel_owns_exactly_one_timer_and_reads_no_door`,
`test_the_css_module_names_the_overlay_layer_and_the_replay_violet_with_no_raw_colour`,
`test_story_player_imports_exactly_the_three_of_s2_and_is_pure`,
`test_the_shell_mounts_the_panel_outside_main_with_the_scrub`,
`test_the_right_panel_holds_the_story_button`). The reviewer's own simulation (which carries
C1a–C2 of this round plus its own version of C3–C6) read `2344 passed, 10 skipped` at exit 0;
five of those ten skips are toolchain nodes a fresh worktree cannot run and each PASSES here
instead, accounting for the count differing from that simulation reading, together with this
round's own new tests and small differences from the reviewer's own version of C3–C6.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=168", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks' status: `pass`. `fail_count`: 0.
```
$ python3 .agent/authored/f039-r5-render_measure.py /home/decodeux/Repos/remedy
...
PASS C-a the panel is a child of document.body, z-index 80, its box inside the viewport
PASS C-b chapter buttons read "The build", "The review", "The finish"; label reads "Chapter 3 of 3: The finish"
PASS C-c clicking "The review" updates the label, shows one "Verdict: needs repair" beat, timeline readout begins "Event 1 of 9"
PASS C-d Play walks the positions 2 to 9 in order and stops with the button reading "Play"
PASS C-e Play again restarts at -1, Space 400 ms later stops the positions growing, button reads "Play"
PASS C-f Escape removes the panel from the DOM and records the close
PASS C-g reduced motion: Play walks exactly the positions -1, 0, 1 and 9
PASS C-h the page with ?running=1 shows the running line
SCREENSHOT story /home/decodeux/Repos/remedy/.remedy-wt/f039-r5-worker/render-story.png 328163 bytes
RENDER: 8 of 8 checks pass
...
drive.mjs exit code: 0
REAL_EXIT=0
```
`RENDER: 8 of 8 checks pass`, exit 0 — matches the whole output saved as
`.agent/authored/f039-r5-render.txt` (from an earlier identical run; both runs read 8 of 8). After
the run: `.remedy-wt/f039-render-run` is gone (`ls` fails, no such file or directory) and
`git status --porcelain` is empty. Screenshot: `.remedy-wt/f039-r5-worker/render-story.png`, 328163
bytes (the committed `render.txt`'s own run wrote 328209 bytes to the same path; both runs are
8-of-8 passes, the byte count differs only by non-deterministic PNG compression of identical
pixels across runs).

G5 THE RED PROOFS — ONE RUN. `git worktree add --detach .remedy-wt/f039-r5-mut 8654dbafb` (C8),
then:
```
$ python3 -B .agent/authored/f039-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r5-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r5-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=16 | guard exit=0 failed=0 passed=11
m1 (storyBeatsAt answers every beat of the card): vitest exit=1 failed=2 passed=14 | guard exit=0 failed=0 passed=11 | caught=True restored byte-identical=True
m2 (storyPlayStart restarts only when the scrub is LIVE): vitest exit=1 failed=1 passed=15 | guard exit=0 failed=0 passed=11 | caught=True restored byte-identical=True
m3 (storyPlayStart always answers -1): vitest exit=1 failed=1 passed=15 | guard exit=0 failed=0 passed=11 | caught=True restored byte-identical=True
m4 (storyPositionLabel counts chapters from 0): vitest exit=1 failed=6 passed=10 | guard exit=0 failed=0 passed=11 | caught=True restored byte-identical=True
m5 (storyWalk's frames carry a wait of 0): vitest exit=1 failed=2 passed=14 | guard exit=0 failed=0 passed=11 | caught=True restored byte-identical=True
m6 (the panel's timer cleanup no longer clears the timeout): vitest exit=0 failed=0 passed=16 | guard exit=1 failed=1 passed=10 | caught=True restored byte-identical=True
m7 (the panel renders in place, without createPortal): vitest exit=0 failed=0 passed=16 | guard exit=1 failed=1 passed=10 | caught=True restored byte-identical=True
m8 (the shell mounts the panel inside <main>, after the phase timeline): vitest exit=0 failed=0 passed=16 | guard exit=1 failed=1 passed=10 | caught=True restored byte-identical=True
m9 (the Story button is removed from RightLivePanel.tsx): vitest exit=0 failed=0 passed=16 | guard exit=1 failed=1 passed=10 | caught=True restored byte-identical=True
m10 (_build_story_section reads load_config() instead of get_config()): vitest exit=0 failed=0 passed=16 | guard exit=1 failed=1 passed=10 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=16 | guard exit=0 failed=0 passed=11
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
All 10 mutations caught (m1–m5 by `storyPlayer.test.ts`'s goldens through vitest; m6–m10 by
`test_story_panel_contract.py`'s and `test_story_section.py`'s plain-text and behavioural checks
through pytest — m10 is R-1100's own proof), every restore byte-identical, both controls green. No
repair round needed. `git worktree remove --force .remedy-wt/f039-r5-mut`, `git worktree prune`;
`git worktree list | wc -l`: 62 (unchanged from step 4's reading, both before and after the run);
`git status --porcelain`: empty.

## Authored-text proofs

The block, the plan payload and the assumption-line payload were each copied verbatim
(`shutil.copyfile`) at C1a and compared byte-identical against their sources under G1 above — all
three MATCH. The records-diff payload was copied verbatim at C1b and compared byte-identical under
G1 above — MATCH. `.agent/decisions.md`, `.agent/live_review.md` and `.agent/plan.md` at C2 were
verified byte- and sha256-identical to the reviewer's own simulation readings under G2 above — all
three MATCH. `records.diff` applied cleanly by `git apply` (both `--check` and the real apply read
exit 0). The assumption-log line was appended to `docs/ui/design_reference/assumption_log.md` by a
small Python script reading both files as bytes and writing `before + payload_bytes` — never
retyped — and G1 confirms the result equals the pre-round log plus the payload's own bytes.

## Deviations & assumptions

C7 SPLIT INTO C7a/C7b. The block's S7 bundle (`f039-r5-render_index.html`,
`f039-r5-render_main.tsx`, `f039-r5-render_measure.py`, `f039-r5-render_vite.config.mjs`,
`f039-r5-render_drive.mjs`) plus `f039-r5-render.txt` totals 636 insertions by `git show
--numstat`, over the 500-line cap. Per AGENTS.md Commit Discipline and the block's own constraint
2 ("split one that would reach it into lettered parts with their own subjects, and say so"), this
was split into C7a (the scaffold and host page: index.html, main.tsx, measure.py,
vite.config.mjs — 307 insertions) and C7b (the driver and its recorded run: drive.mjs,
render.txt — 329 insertions), both lettered with their own subjects. No file content differs from
what a single C7 would have written; only the commit boundary moved.

SPACE-KEY FIX DURING DEVELOPMENT (before any commit touched the file). While building and
exercising the render harness ahead of C5's commit, the first working draft of `StoryPanel.tsx`
read `event.target` to decide whether a text field had focus before treating Space as play/pause.
That works for a real keypress (the browser sets `target` to the focused element and the event
bubbles to `window` with it intact), but the render harness dispatches its synthetic `keydown`
directly on `window`, where `target` is `window` itself — `target.tagName` then threw inside the
listener (an uncaught exception CDP reported, and C-e's Space press silently did nothing because
the throw happened inside the browser's own event dispatch, never reaching the driver script).
The committed code reads `document.activeElement` instead, the same standard idiom other apps use
for "ignore this key while a form field is focused" — correct for both a real keypress and a
CDP-dispatched one. This was caught and fixed BEFORE C5 was committed, so no commit content, no
production behavior and no test differs from what is described above; it is recorded here only
because a fix discovered through the harness is worth naming.

No other deviation from the block's ordered commit sequence. The G5 run caught all 10 mutations on
its first pass, so no test correction was needed before C9.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 (S1, R-1100) | done | |
| C4 (S2, storyPlayer.test.ts) | done | |
| C5 (S3, S4, S5) | done | |
| C6 (S6 contract test) | done | |
| C7 (S7 render) | deviated | split into C7a and C7b, both under the 500-line cap; see Deviations |
| C8 (mutation tool) | done | |
| C9 (handoff, push) | done | |
| G1 Transport | done | |
| G2 Records | done | |
| G3 Code | done | |
| G4 Tests and render | done | |
| G5 Red proofs | done | |
| G6 Tree and push | done | reported in the worker's final reply, since C9 cannot contain it |

## Next

Per Phase 1 rule 1: read `.agent/STOP` from disk first. Then the review of round 5 with the
resolution of R-1100. Then T003: the export command and its build, beginning with the font
licensing finding before any font is bundled. Open findings: 1 (R-1100, landed and awaiting
review). Operator questions: 1.
