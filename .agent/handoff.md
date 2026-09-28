# Handback — F039, round 6: book round 5's FAIL with R-1100's resolution, and repair R-1101

## Session

SESSION 1 of feature F039 · round 6 · rounds so far 6. This session ran round 6 only: booking
round 5's FAIL, R-1100's resolution and R-1101's registration into the ledger, then repairing
R-1101 — the story panel's timer effect re-arming on every render of its host instead of only
when play starts or stops, the position moves, or reduced motion changes — and proving the
repair in a round 6 copy of the render harness that adds a ninth check, C-i, under host churn.
Context self-assessment: a comfortable margin remained through the round, including the targeted
pytest selection, three full runs of the render harness (two during development, one at the
gate) and the mutation tool's one complete run; the work was not near its limit.

For the operator, in plain words: round 5 is booked FAIL and R-1100 is booked landed (the
docstring fix, awaiting the next review). R-1101 — the story's Play button silently stalling
while the app was busy re-rendering (for example, while a job is still streaming) — is now fixed
and awaiting review: the panel keeps its own ref to the latest story view, updated after every
render, and its one timer now only resets when play itself starts or stops, the position moves,
or the reduced-motion setting changes — never merely because the surrounding page redrew itself.
A new headless check proves this by re-rendering the host every 50 ms and dropping in a new
ledger row every 200 ms while Play is running, and watching it keep walking regardless.

## Range

Review of `bfa50f969`..`HEAD` (the commit that writes this file is the eighth in the range).
SEVEN commits precede it: C1a, C1b, C2, C3, C4a, C4b and C5 — the block's lettered bundle with
ONE declared split (C4 became C4a/C4b; see Deviations).

## Commits

### 593142c58 F039 R6 C1a: copy round 6 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r6-block.md | 213/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f039-r6-plan.md | 29/0 | the plan payload, copied verbatim |

(measured: `git show 593142c58 --numstat` reads `213 0`, `29 0`, total 242 — exactly the block's
own expected reading (213 + 29), under the 500-line cap.)

### c8e7b6ece F039 R6 C1b: copy round 6 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r6-records.diff | 14/0 | the records-diff payload, copied verbatim |

(measured: `git show c8e7b6ece --numstat` reads `14 0` — exactly the block's expected 14.)

### 3395de941 F039 R6 C2: book round 5's FAIL and R-1100, register R-1101
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 6/0 | records.diff appends round 5's Gate entry (FAIL), R-1100's `Done:` paragraph and R-1101's registration |
| .agent/plan.md | 7/8 | records.diff, then rewritten := plan.md (round 6's plan) |

(measured: `git show 3395de941 --numstat` reads `6 0`, `7 8` — exactly the block's own expected
reading in C2's own line and G2's table.)

### c87039df0 F039 R6 C3: keep the story's pending step through its host's renders (R-1101)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | one blank line plus one `Landed: R-1101 — ` line, naming no commit |
| apps/ui/src/components/story/StoryPanel.tsx | 20/6 | S1: a `viewRef` holding the story view, set by an effect with no dependency list under an R-1101 comment, declared before the timer effect; `const { scrubTo } = scrub;` destructured out; the timer effect reads the view only through `viewRef.current` and calls `scrubTo`, dependency list exactly `[playing, position, reducedMotion, scrubTo]` |
| tests/ui_contracts/test_story_panel_contract.py | 15/0 | S2: ONE new test pinning the exact dependency line and `viewRef.current`, and that the timer's own block names neither `scrub` nor `view` bare |

(measured: `git show c87039df0 --numstat` reads `2 0`, `20 6`, `15 0`, total 37; the block gave no
expected reading for C3.)

### 01f280f5f F039 R6 C4a: build the churn render harness scaffold and host page
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r6-render_index.html | 11/0 | NEW, copied verbatim from round 5's own file (S3: unchanged) |
| .agent/authored/f039-r6-render_main.tsx | 111/0 | NEW, S3: round 5's harness plus `?churn=1` — re-renders the host every 50 ms via an unread tick counter, and appends one `feedRowOf` row of a `budget.tick` frame at the next seq every 200 ms, handing the growing `rows` to both `useTimelineScrub` and `StoryPanel` |
| .agent/authored/f039-r6-render_measure.py | 191/0 | NEW, copied verbatim from round 5's own file (S3: unchanged; its `PREFIX` logic already generalizes to any sibling-file prefix) |
| .agent/authored/f039-r6-render_vite.config.mjs | 28/0 | NEW, copied verbatim from round 5's own file (S3: unchanged) |

(measured: `git show 01f280f5f --numstat` reads `11 0`, `111 0`, `191 0`, `28 0`, total 341, under
the 500-line cap. DEVIATION: this is HALF of C4 as the block named it — see Deviations.)

### 0a280fc94 F039 R6 C4b: render the story panel under churn and record its checks
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r6-render_drive.mjs | 326/0 | NEW, S3: round 5's driver plus C-i — on `?churn=1`, after clicking "The review", Play walks positions 2 to 9 as its first eight AND at least one position past 9 within three seconds |
| .agent/authored/f039-r6-render.txt | 32/0 | NEW, S3: the harness's own saved stdout, `RENDER: 9 of 9 checks pass`, exit 0 |

(measured: `git show 0a280fc94 --numstat` reads `326 0`, `32 0`, total 358, under the 500-line
cap. DEVIATION: this is the other half of C4 — see Deviations.)

### 3b204a268 F039 R6 C5: add the mutation tool for R-1101
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r6-mutations.py | 164/0 | NEW mutation tool, m1–m3 exactly as the block specifies: `scrub` added to the timer's deps, the timer reading `view` bare with `view` added to its deps, and the ref's own updating effect deleted; runs the contract guard and `f039-r6-render_measure.py` against the worktree, both controls, byte-identical restore |

(measured: `git show 3b204a268 --numstat` reads `164 0`, under the 500-line cap.)

## External actions

`git worktree add --detach .remedy-wt/f039-r6-mut 3b204a268` before the (single, successful) G5
run; `git worktree remove --force .remedy-wt/f039-r6-mut` and `git worktree prune` after it —
`git worktree list | wc -l` read 62 before the add and 62 after the remove (step 4's reading,
unchanged). `git push origin feature/f039-story-replay-mode` after this commit — reported in the
worker's final reply, since this file is written and C6 committed before that push, per the
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
bfa50f969 F039 R5 C9: rewrite handoff for round 5
```
Block bytes: measured line count 213 and sha256
`e1d6973f148e77cbbfd308ea590c52d86e70286afda7df8b04326df8e626994e` — MATCH both given readings.
`git worktree list | wc -l` at step 4: 62.

PAYLOADS — both measured and MATCH the block's table exactly:
| file | lines | bytes | sha256 | verdict |
|---|---|---|---|---|
| plan.md | 29 | 1034 | `2f1f2e0302216a5929d4f998bd6ea77f0888ea3cb1885ee3adb11b7436c99d01` | MATCH |
| records.diff | 14 | 6938 | `ac982f7accf5a81acb8aa7ea7c14c924a8d299bbf1843452346d30ae32a7cc52` | MATCH |

C1a: measured insertions 242 (213 + 29), under the 500-line cap — no STOP required.

G1 TRANSPORT — both `.agent/authored/f039-r6-*` payload copies, read back with `git show
<commit>:<path>`, equal their sources byte for byte: block.md (against `.remedy-wt/f039-r6/block.md`,
at C1a — 16067 bytes both sides, sha256 `e1d6973f148e77cbbfd308ea590c52d86e70286afda7df8b04326df8e626994e`
both sides), plan.md (against the payload, at C1a), records.diff (against the payload, at C1b) —
all three MATCH.

G2 THE RECORDS, at C2 (`3395de941`):
```
$ git apply --check .remedy-wt/f039-r6-payloads/records.diff
CHECK_EXIT=0
$ git apply .remedy-wt/f039-r6-payloads/records.diff
APPLY_EXIT=0
```
| path | bytes | sha256 | verdict |
|---|---|---|---|
| .agent/live_review.md | 346240 | `c7934727f5d2978a407e73ad11124ec92b73335364c9da8033e2ae4156f70ae1` | MATCH |
| .agent/plan.md | 1034 | `2f1f2e0302216a5929d4f998bd6ea77f0888ea3cb1885ee3adb11b7436c99d01` | MATCH |

`open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
ledger's TEXT at C2: `['R-1101']` and `FAIL` — both match the reviewer's own reading. `git diff
--name-only c8e7b6ece 3395de941` names exactly `.agent/live_review.md` and `.agent/plan.md` —
exactly G2's table, nothing else. At C3 (`c87039df0`): the ledger is a byte-exact prefix of the
ledger at C2 (346240 bytes), and the addition is exactly 651 bytes — `"\n"` plus one line
beginning `Landed: R-1101 — ` and ending in `"\n"` — confirmed by direct byte slicing.

G3 THE CODE:
```
$ python3 -m ruff check tests/ui_contracts/test_story_panel_contract.py .agent/authored/f039-r6-render_measure.py .agent/authored/f039-r6-mutations.py
All checks passed!
REAL_EXIT=0
```
From `git show c87039df0` (C3), the ref, its effect and the whole timer effect:
```typescript
  // THE PENDING STEP OUTLIVES THE HOST'S RENDERS (R-1101): `viewRef` is kept current by an
  // effect with no dependency list — it runs after every render — so the timer effect below
  // can read the latest story view without naming `view` as a dependency, which is what made
  // the shell's own re-renders (driven by the stream while a job is still running) clear and
  // reschedule the pending step before it ever fired.
  const viewRef = useRef(view);
  useEffect(() => {
    viewRef.current = view;
  });

  const { scrubTo } = scrub;

  // THE ONE TIMER (see the header comment): re-armed only when play starts or stops, the
  // position moves or the reduced-motion setting changes (R-1101) — never by the host's own
  // re-render, and never by a new story view, which `viewRef` reads instead of a dependency.
  useEffect(() => {
    if (!playing) return;
    const currentView = viewRef.current;
    const step = autoplayStep(currentView.chapters, currentView.seqs, position, currentView.pacing, reducedMotion);
    if (step === null) {
      setPlaying(false);
      return;
    }
    const id = window.setTimeout(() => scrubTo(step.position), step.delayMs);
    return () => window.clearTimeout(id);
  }, [playing, position, reducedMotion, scrubTo]);
```
From `git show 01f280f5f` (C4a), the churn half of `main.tsx`:
```typescript
function nextTickRow(rows: ReturnType<typeof brainDemoRows>) {
  const nextSeq = rows.reduce((max, row) => Math.max(max, row.seq), 0) + 1;
  return feedRowOf(
    { seq: nextSeq, event: { seq: nextSeq, event: "budget.tick", budget: { spent_usd: 0.01 * nextSeq } } },
    0,
  );
}

function Harness() {
  const [open, setOpen] = useState(true);
  const [rows, setRows] = useState(() => brainDemoRows());
  const [, setChurnTick] = useState(0);

  // Re-renders the host every 50 ms under `?churn=1` — the tick itself is read by nothing;
  // the re-render is the whole point (R-1101).
  useEffect(() => {
    if (!CHURN) return undefined;
    const id = window.setInterval(() => setChurnTick((tick) => tick + 1), 50);
    return () => window.clearInterval(id);
  }, []);

  // Appends one budget.tick row at the next seq every 200 ms under `?churn=1` (R-1101).
  useEffect(() => {
    if (!CHURN) return undefined;
    const id = window.setInterval(() => {
      setRows((current) => [...current, nextTickRow(current)]);
    }, 200);
    return () => window.clearInterval(id);
  }, []);
```
From `git show 0a280fc94` (C4b), C-i of `drive.mjs`:
```javascript
  // C-i — R-1101's own proof: reload with `?churn=1` (host re-renders every 50 ms, a new ledger
  // row lands every 200 ms). After clicking "The review", Play still walks the positions 2 to 9
  // in order as its first eight, AND then at least one further position past 9 — a row that
  // arrived after Play was pressed — within three seconds.
  await client.send("Page.navigate", { url: `${PAGE}?churn=1` });
  await sleep(2000);
  await clickButtonByText(client, '[data-ui="story-chapters"]', "The review");
  await sleep(150);
  const beforeI = await positionsLength(client);
  await clickButtonByText(client, '[data-ui="story-panel"]', "Play");
  await sleep(3000);
  const afterI = await positionsSince(client, beforeI);
  const firstEightI = afterI.slice(0, 8);
  const restI = afterI.slice(8);
  const firstEightMatch = JSON.stringify(firstEightI) === JSON.stringify([2, 3, 4, 5, 6, 7, 8, 9]);
  const wentPastNine = restI.some((p) => p > 9);
  if (firstEightMatch && wentPastNine) {
    pass('C-i under churn (?churn=1), Play walks 2 to 9 in order and then at least one position past 9 within three seconds');
  } else {
    fail('C-i under churn (?churn=1), Play walks 2 to 9 in order and then at least one position past 9 within three seconds',
      JSON.stringify(afterI));
  }
```

G4 THE TESTS AND THE RENDER, in the primary checkout at C5 (`3b204a268`), SERIALLY:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
2246 passed, 5 skipped in 144.15s (0:02:24)
REAL_EXIT=0
```
None of the five SKIPPED lines names `node_modules`, `dist` or vitest — all five are the same
pre-existing D3/D12 quarantines every earlier handback in this feature also names, so none is a
toolchain node this checkout should have run instead. The contract test collects, by
`--collect-only -q`: `tests/ui_contracts/test_story_panel_contract.py` — 8 nodes
(`test_the_panel_is_a_region_portaled_to_the_document_body`,
`test_the_panel_drives_the_real_scrub_and_reads_reduced_motion`,
`test_the_panel_owns_exactly_one_timer_and_reads_no_door`,
`test_the_timer_reads_the_latest_view_through_a_ref_and_never_scrub_or_view_bare_r1101`,
`test_the_css_module_names_the_overlay_layer_and_the_replay_violet_with_no_raw_colour`,
`test_story_player_imports_exactly_the_three_of_s2_and_is_pure`,
`test_the_shell_mounts_the_panel_outside_main_with_the_scrub`,
`test_the_right_panel_holds_the_story_button`). The reviewer's own simulation (which carries
C1a–C2 of this round and its own version of C3) read `2241 passed, 10 skipped` at exit 0; five of
those ten skips are toolchain nodes a fresh worktree cannot run and each PASSES here instead
(2241 + 5 = 2246), together with this round's own new test and small differences from the
reviewer's own version of C3.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=168", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks' status: `pass`. `fail_count`: 0. The verdict check's message reads `last Gate
verdict FAIL`, which passes because the context does not say the work is complete (round 5's own
booked verdict).
```
$ python3 .agent/authored/f039-r6-render_measure.py /home/decodeux/Repos/remedy
...
PASS C-a the panel is a child of document.body, z-index 80, its box inside the viewport
PASS C-b chapter buttons read "The build", "The review", "The finish"; label reads "Chapter 3 of 3: The finish"
PASS C-c clicking "The review" updates the label, shows one "Verdict: needs repair" beat, timeline readout begins "Event 1 of 9"
PASS C-d Play walks the positions 2 to 9 in order and stops with the button reading "Play"
PASS C-e Play again restarts at -1, Space 400 ms later stops the positions growing, button reads "Play"
PASS C-f Escape removes the panel from the DOM and records the close
PASS C-g reduced motion: Play walks exactly the positions -1, 0, 1 and 9
PASS C-h the page with ?running=1 shows the running line
PASS C-i under churn (?churn=1), Play walks 2 to 9 in order and then at least one position past 9 within three seconds
SCREENSHOT story /home/decodeux/Repos/remedy/.remedy-wt/f039-r6-worker/render-story.png 328220 bytes
RENDER: 9 of 9 checks pass
...
drive.mjs exit code: 0
REAL_EXIT=0
```
`RENDER: 9 of 9 checks pass`, exit 0 — this run's own output was saved verbatim as
`.agent/authored/f039-r6-render.txt` at C4b (a slightly earlier, otherwise identical 9-of-9 run;
both this gate run and the committed run pass all nine, the screenshot byte count differs only by
non-deterministic PNG compression of identical pixels across runs — 328220 here, 328209 in the
committed file). After the run: `.remedy-wt/f039-render-run` is gone (`ls` fails, no such file or
directory) and `git status --porcelain` is empty.

G5 THE RED PROOFS — ONE RUN. `git worktree add --detach .remedy-wt/f039-r6-mut 3b204a268` (C5),
then:
```
$ python3 -B .agent/authored/f039-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r6-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r6-mut
CONTROL FIRST: guard exit=0 failed=0 passed=8 | render exit=0 RENDER: 9 of 9 checks pass
m1 (the timer's dependency list gains `scrub`): guard exit=1 failed=1 passed=7 | render exit=1 RENDER: 8 of 9 checks pass | caught=True restored byte-identical=True
m2 (the timer reads `view` itself and its dependency list gains `view`): guard exit=1 failed=1 passed=7 | render exit=1 RENDER: 8 of 9 checks pass | caught=True restored byte-identical=True
m3 (the ref's effect is deleted, so the timer reads the first view forever): guard exit=0 failed=0 passed=8 | render exit=1 RENDER: 8 of 9 checks pass | caught=True restored byte-identical=True
CONTROL LAST: guard exit=0 failed=0 passed=8 | render exit=0 RENDER: 9 of 9 checks pass
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
m3 reads exactly as the block anticipated: the contract STAYS GREEN (guard exit=0, failed=0 —
`viewRef.current` and the exact dependency line both survive untouched, since only the ref's own
updating effect is deleted) and only the render's own churn check (C-i) catches it, reading 8 of
9 instead of 9 of 9. All three mutations caught, every restore byte-identical, both controls
green. No repair round needed. `git worktree remove --force .remedy-wt/f039-r6-mut`, `git
worktree prune`; `git worktree list | wc -l`: 62 (unchanged from step 4's reading, both before and
after the run); `git status --porcelain`: empty.

## Authored-text proofs

The block and the plan payload were each copied verbatim (`shutil.copyfile`) at C1a and compared
byte-identical against their sources under G1 above — both MATCH. The records-diff payload was
copied verbatim at C1b and compared byte-identical under G1 above — MATCH. `.agent/live_review.md`
and `.agent/plan.md` at C2 were verified byte- and sha256-identical to the reviewer's own
simulation readings under G2 above — both MATCH. `records.diff` applied cleanly by `git apply`
(both `--check` and the real apply read exit 0). The `Landed: R-1101 — ` line at C3 is MY OWN
authored sentence (the block orders "saying in one sentence what changed", not a payload), not a
reviewer-authored text; G2 above confirms it is appended as exactly `"\n"` plus one line ending in
`"\n"`, on top of a byte-exact prefix of the C2 ledger. `f039-r6-render_index.html`,
`f039-r6-render_measure.py` and `f039-r6-render_vite.config.mjs` are byte-for-byte copies
(`shutil.copyfile`) of round 5's own committed files of the same names, per S3's "changed only as
follows" (which names no change to these three) — confirmed by direct comparison:
```
$ python3 -c "
import filecmp
for name in ['_index.html', '_measure.py', '_vite.config.mjs']:
    a = f'.agent/authored/f039-r5-render{name}'
    b = f'.agent/authored/f039-r6-render{name}'
    print(name, filecmp.cmp(a, b, shallow=False))
"
_index.html True
_measure.py True
_vite.config.mjs True
```
`f039-r6-render_main.tsx` and
`f039-r6-render_drive.mjs` are round 5's own files with exactly the additions S3 orders (the
churn host and rows in `main.tsx`, check C-i in `drive.mjs`) — both authored by the worker against
S3, as the block's ROLE AND AUTHORITY section specifies ("you write the repair, the guard's test,
the render harness and the mutation tool yourself against S1 to S3").

## Deviations & assumptions

C4 SPLIT INTO C4a/C4b. The block's S3 bundle (`f039-r6-render_index.html`,
`f039-r6-render_main.tsx`, `f039-r6-render_measure.py`, `f039-r6-render_vite.config.mjs`,
`f039-r6-render_drive.mjs`, `f039-r6-render.txt`) totals 699 insertions by `git show --numstat`,
over the 500-line cap. Per AGENTS.md Commit Discipline and the block's own constraint 2 ("split
one that would reach it into lettered parts with their own subjects, and say so"), this was split
into C4a (the scaffold and host page: index.html, main.tsx, measure.py, vite.config.mjs — 341
insertions) and C4b (the driver and its recorded run: drive.mjs, render.txt — 358 insertions),
both lettered with their own subjects, following the same route round 5's C7a/C7b split took. No
file content differs from what a single C4 would have written; only the commit boundary moved.

THREE OF S3'S FIVE FILES COPIED VERBATIM, NOT RE-AUTHORED. S3 says the five files are "copied
from round 5's and changed only as follows," and the "as follows" text names changes only to
`main.tsx` (the churn host and growing rows) and `drive.mjs` (check C-i). Read literally, that
leaves `index.html`, `measure.py` and `vite.config.mjs` UNCHANGED copies — including
`measure.py`'s own docstring, which still opens "F039 R5, T002's render harness runner" and still
names "f039-r5-render_" as its own committed-copy prefix, even though the committed file is now
`f039-r6-render_measure.py`. This reads as an intentional invariant (the same three files, same
ports 9366/8996, same work dir `f039-render-run`, carried across rounds within one feature,
exactly as F039 R5's own such file was carried from F036 with only its docstring's naming, work
dir and ports changed — a change S3 here does not order), not an oversight; declared rather than
silently "fixed," since the spec's own words bound the change to two files and a worker note in
AGENTS.md prefers repository state (what the block orders) over session judgment about what a
docstring "should" say.

SCREENSHOT PATH MOVED TO THE ROUND'S OWN WORKER DIRECTORY. `drive.mjs`'s `SCREENSHOT_PNG` constant
now reads `.remedy-wt/f039-r6-worker/render-story.png` in place of round 5's
`f039-r5-worker/render-story.png` — the directory the block's own "THE DIRECTORIES" section names
as this round's ("YOURS for logs, scripts and screenshots; create it if absent"), which this
worker created fresh since it did not exist. This is a path constant, not a check or a piece of
product/story behaviour, so it falls outside S3's "changed only as follows" governing the checks
themselves; not changing it would have left every round's screenshot landing in round 5's own
directory forever.

No other deviation from the block's ordered commit sequence. The G5 run caught all three
mutations on its first pass, so no test correction was needed before C6.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 (S1, S2, R-1101 repair and guard) | done | |
| C4 (S3 render) | deviated | split into C4a and C4b, both under the 500-line cap; see Deviations |
| C5 (mutation tool, m1-m3) | done | |
| C6 (handoff, push) | done | |
| G1 Transport | done | |
| G2 Records | done | |
| G3 Code | done | |
| G4 Tests and render | done | |
| G5 Red proofs | done | |
| G6 Tree and push | done | reported in the worker's final reply, since C6 cannot contain it |

## Next

Per Phase 1 rule 1: read `.agent/STOP` from disk first. Then the review of round 6 with the
resolution of R-1101. Then T003: the export command and its build. Open findings: 1 (R-1101,
landed and awaiting review). Operator questions: 1.
