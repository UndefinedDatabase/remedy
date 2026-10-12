# Handback — F305 round 2: book round 1, DECISION F305 D3, and T002

## Session

SESSION 1 of feature F305 · round 2 · rounds so far 2

Context self-assessment: the session verified the block's own line count and sha256, the four
gate scripts' digests, and all fifteen digest-bearing Bundle-listed prepared `dry-*` files before
any write; checked, read-only, that base `4f15ac59e` plus each of the three append files equals
its stated `dry-*` file for `.agent/live_review.md`, `.agent/decisions.md` and
`.agent/prose_slips.md` before C1 was staged; copied every file by small, single-purpose Python
scripts under `.remedy-wt/f305-r2-worker/`; confirmed each commit's staged numstat against the
Bundle's stated pairs before every commit; and ran all six gates in one uninterrupted pass, each
green on its first and only run; context remains comfortable at handback.

Fortschritt: ~60 % (T001 and T002 landed · T003 and the closure open) — Schätzung

## Range

Review of `4f15ac59e`..HEAD.

## Commits

### 03f9bc7c9 F305 R2 C1: book round 1, DECISION F305 D3, and the plan for round 2

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f305-r2.md` | +138/-0 | NEW FILE, byte copy of `.remedy-wt/f305-r2/prep/block.md` (138 lines, sha256 `ea21700c3d6b8628fa858153ab8a277ec29b9b276dc07af963c0362e40dc0f1b`) |
| `.agent/decisions.md` | +12/-0 | byte copy of base `.agent/decisions.md` plus `prep/append-decisions.txt`: DECISION F305 D3 (the missions panel's design) |
| `.agent/live_review.md` | +2/-0 | byte copy of base `.agent/live_review.md` plus `prep/append-live_review.txt`: the `Gate: F305 R1` entry appended, VERDICT PASS |
| `.agent/plan.md` | +13/-13 | rewritten in full for F305 round 2, byte copy of `prep/dry-plan.md` |
| `.agent/prose_slips.md` | +1/-0 | byte copy of base `.agent/prose_slips.md` plus `prep/append-prose_slips.txt`: one line dated 2026-10-12 for F305 round 1 |

### fb635e7fa F305 R2 C2: the mission card's client seam and its vitest file (T002)

| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/missionCard.ts` | +290/-0 | NEW FILE, byte copy of `prep/dry-missionCard.ts`: the pure seam decoding the missions and orders envelopes, naming their paths and wording the card, touching no network/clock/storage/page |
| `apps/ui/src/api/missionCard.test.ts` | +131/-0 | NEW FILE, byte copy of `prep/dry-missionCard.test.ts`: the seam's vitest file |

### 3e8e24722 F305 R2 C3: the mission card's two doors and their vitest file (T002)

| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/missionCardDoor.ts` | +43/-0 | NEW FILE, byte copy of `prep/dry-missionCardDoor.ts`: the two loaders, each with an injected fetcher, no throw, and its own GET on the page's origin |
| `apps/ui/src/api/missionCardDoor.test.ts` | +48/-0 | NEW FILE, byte copy of `prep/dry-missionCardDoor.test.ts`: the doors' vitest file |

### 164d23fb8 F305 R2 C4: the missions panel, its button, its mount, a chip's way to its job, and their contract test (T002)

| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/missions/MissionPanel.tsx` | +149/-0 | NEW FILE, byte copy of `prep/dry-MissionPanel.tsx`: the panel reading the project's missions on open and a mission's orders on that card's open, its chain band of chips |
| `apps/ui/src/components/missions/MissionPanel.module.css` | +106/-0 | NEW FILE, byte copy of `prep/dry-MissionPanel.module.css`: the panel's own CSS module |
| `apps/ui/src/components/shell/ProjectProvider.tsx` | +14/-4 | byte copy of `prep/dry-ProjectProvider.tsx`: `openJob(slug, jobId)` added to the context, begins the switch gate at the chip's project and pushes the address with no summary to wait for |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +4/-1 | byte copy of `prep/dry-RightLivePanel.tsx`: the "Missions" button added beside "Results", in the same quiet style |
| `apps/ui/src/components/shell/RemedyShell.tsx` | +10/-1 | byte copy of `prep/dry-RemedyShell.tsx`: `missionsOpen` state, the panel's mount as a sibling directly after the results panel, wired to the button and to `openJob` |
| `tests/ui_contracts/test_mission_card_door.py` | +166/-0 | NEW FILE, byte copy of `prep/dry-test_mission_card_door.py`: the contract test pinning every client interface to exactly the keys the server answers, and the wiring |
| `docs/system/operator-cockpit-v1.md` | +7/-0 | byte copy of `prep/dry-operator-cockpit-v1.md`: the paragraph documenting the Missions button, the panel and the chip's click |

### this commit F305 R2 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

None yet in this commit. `git -C /home/decodeux/Repos/remedy push origin
feature/f305-multi-repo-chain-band` follows this commit, per the block's push-after-C5 instruction.
Its outcome is reported in the final reply, not in this file. No pull request is opened this round
(the block forbids it). No other `gh` command run. No worktree added or removed by the worker.

## Verification

**Preconditions (before C1):** `git branch --show-current` read `feature/f305-multi-repo-chain-band`;
`git rev-parse HEAD` read `4f15ac59e7085a33b5276d19e570aec626185a5c`; `git status --porcelain` empty.

**Block and Bundle digests (before any write):** `wc -l block.md` read `138`, `sha256sum` read
`ea21700c3d6b8628fa858153ab8a277ec29b9b276dc07af963c0362e40dc0f1b` — both equal to the values the
prompt delivered. All four gate-script digests (`verify.py`, `build_ui.py`, `run_selection.py`,
`selection.txt`) were checked against the prompt's stated values and matched. All fifteen
digest-bearing Bundle-listed `dry-*` prepared files were hashed via `sha256sum`: every one matched
the block's stated digest exactly. The three append-based records
(`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`) were checked, read-only,
before C1 was staged: base `4f15ac59e` plus each `prep/append-*.txt` equals its stated `dry-*`
file byte-for-byte (`c1_verify_formula.py`, `ALL True`).

**C1:** `c1_copy.py` byte-copied `dry-live_review.md`, `dry-decisions.md`, `dry-plan.md` and
`dry-prose_slips.md` to their destinations, and byte-copied `block.md` to
`.agent/authored/f305-r2.md`. Every one of the five comparisons printed `True`; the authored
copy's own line count (`138`) and sha256 matched the block exactly; `ALL True`. `git diff --cached
--numstat` after `git add` read exactly the Bundle's five C1 pairs (see Commits table above), no
other path. `git branch --show-current` read `feature/f305-multi-repo-chain-band` immediately
before the commit.

**C2:** `c2_copy.py` byte-copied the two files as NEW FILES and re-hashed both pairs: `True` for
each, `ALL True`. `git diff --cached --numstat` read exactly the Bundle's two C2 pairs, no other
path. `git branch --show-current` re-read correctly before the commit.

**C3:** `c3_copy.py` byte-copied the two files as NEW FILES and re-hashed both pairs: `True` for
each, `ALL True`. `git diff --cached --numstat` read exactly the Bundle's two C3 pairs, no other
path. `git branch --show-current` re-read correctly before the commit.

**C4:** `c4_copy.py` byte-copied three files as NEW FILES and rewrote four existing tracked files,
re-hashing all seven pairs: `True` for each, `ALL True`. `git diff --cached --numstat` read exactly
the Bundle's seven C4 pairs, no other path. `git branch --show-current` re-read correctly before
the commit. The diffs of the four rewritten files were read in full before the commit (self-review
loop): the "Missions" button beside "Results" in `RightLivePanel.tsx`, `openJob` added to
`ProjectProvider.tsx`'s context value and default, the panel's mount and its `missionsOpen` state
in `RemedyShell.tsx` directly after the results panel, and the new paragraph in
`docs/system/operator-cockpit-v1.md` — each coherent with DECISION F305 D3 and with no unrelated
edit.

**Gate 1:** `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f305-r2/prep/verify.py
/home/decodeux/Repos/remedy` →
```
equal True .agent/authored/f305-r2.md
equal True .agent/live_review.md
equal True .agent/decisions.md
equal True .agent/plan.md
equal True .agent/prose_slips.md
equal True apps/ui/src/api/missionCard.ts
equal True apps/ui/src/api/missionCard.test.ts
equal True apps/ui/src/api/missionCardDoor.ts
equal True apps/ui/src/api/missionCardDoor.test.ts
equal True apps/ui/src/components/missions/MissionPanel.tsx
equal True apps/ui/src/components/missions/MissionPanel.module.css
equal True apps/ui/src/components/shell/ProjectProvider.tsx
equal True apps/ui/src/components/panels/RightLivePanel.tsx
equal True apps/ui/src/components/shell/RemedyShell.tsx
equal True tests/ui_contracts/test_mission_card_door.py
equal True docs/system/operator-cockpit-v1.md
base plus slice True .agent/live_review.md
base plus slice True .agent/decisions.md
base plus slice True .agent/prose_slips.md
ALL True
```
Exit 0, every line `True`, last line `ALL True`.

**Gate 2:** `python3 -m ruff check tests/ui_contracts/test_mission_card_door.py` →
`All checks passed!`, exit 0.

**Gate 3 (build `apps/ui` so the next gate's UI server tests find this round's `dist`):**
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f305-r2/prep/build_ui.py
/home/decodeux/Repos/remedy` →
```
vite build exit 0 :: - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
porcelain empty True
```
Exit 0.

**Gate 4 (the round's one test selection, run once):**
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f305-r2/prep/run_selection.py
/home/decodeux/Repos/remedy` →
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
4833 passed, 13 skipped in 26.97s
exit 0
```
Exactly the reviewer's dry-tree reading (seconds differ, as expected): the same thirteen SKIPPED
lines in the same order, the same `4833 passed, 13 skipped`, and `exit 0`; no FAILED or ERROR
line; no line containing `process(es) behind`.

**Gate 5:** `python3 -m apps.cli.main integrity check --json` → exit 0,
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` handlers=184; `live_review_verdict` last Gate verdict PASS; `plan_consistency`
unchecked=0; `relevant_untracked` untracked=0/relevant=0; `repo_root_hygiene` clean;
`high_blockers_open` none open), exactly the reviewer's stated dry reading (`fail_count` 0, all six
`pass`).

**Gate 6:** `git -C /home/decodeux/Repos/remedy log --format=%s 4f15ac59e..HEAD` →
```
F305 R2 C4: the missions panel, its button, its mount, a chip's way to its job, and their contract test (T002)
F305 R2 C3: the mission card's two doors and their vitest file (T002)
F305 R2 C2: the mission card's client seam and its vitest file (T002)
F305 R2 C1: book round 1, DECISION F305 D3, and the plan for round 2
```
Subjects of C1 to C4, newest first, as required.

No mutation run (the block forbids it this round; the reviewer ran them in a disposable worktree).
No test run beyond gate 4's one pytest selection; `REMEDY_TEST_MAX_WORKERS` was never set, no extra
`-n` was passed, no two test commands ran at once. No full suite. No `npm` or `npx` run; the one UI
tool run was gate 3's build, through its script. No worktree of the worker's own beyond the
pre-existing, gitignored `.remedy-wt/f305-r2-worker/` scratch directory this session created for
its own copy/hash scripts. No provider call.

## Authored-text proofs

1. `block.md` → `.agent/authored/f305-r2.md` (C1): byte-equal, confirmed by `c1_copy.py` and again
   by gate 1's `verify.py`.
2. The base `.agent/live_review.md` + `prep/append-live_review.txt` → `.agent/live_review.md`
   (C1): built by the formula gate 1's `verify.py` checks, byte-equal to `prep/dry-live_review.md`,
   confirmed read-only by `c1_verify_formula.py` before the write, by `c1_copy.py` at the write, and
   again by gate 1.
3. The base `.agent/decisions.md` + `prep/append-decisions.txt` → `.agent/decisions.md` (C1): built
   the same way, byte-equal to `prep/dry-decisions.md`, confirmed the same way.
4. The base `.agent/prose_slips.md` + `prep/append-prose_slips.txt` → `.agent/prose_slips.md`
   (C1): built the same way, byte-equal to `prep/dry-prose_slips.md`, confirmed the same way.
5. Every other Bundle-listed prepared file (`dry-plan.md`, `dry-missionCard.ts`,
   `dry-missionCard.test.ts`, `dry-missionCardDoor.ts`, `dry-missionCardDoor.test.ts`,
   `dry-MissionPanel.tsx`, `dry-MissionPanel.module.css`, `dry-ProjectProvider.tsx`,
   `dry-RightLivePanel.tsx`, `dry-RemedyShell.tsx`, `dry-test_mission_card_door.py`,
   `dry-operator-cockpit-v1.md`) was copied and re-hashed byte-equal at its own commit's working
   tree, per the per-commit verification above — gate 1's `verify.py` `ALL True` covers every one
   of them again, together, against the committed state.

## Deviations & assumptions

None. Every commit matched the block's ordered commit sequence (C1 to C4, then C5) with no extra
commit, no dropped commit and no reordering. No file was written outside each commit's named path
set; no mutation was run (none was ordered); no two test commands ran at once;
`REMEDY_TEST_MAX_WORKERS` was never set and no extra `-n` was passed; `npm`/`npx` were never run;
`.agent/STOP` did not appear during the round; no merge, branch create/switch beyond the one
feature branch, or force-push was performed; no pull request was opened. All four gate-script
digests (including `build_ui.py`, new this round) and all fifteen `dry-*` digests matched the
block's stated values on the first check, so no stop-and-report was triggered.

## For the operator, in plain sentences

The cockpit's right-hand column now has a Missions button. It opens a panel listing the project's
missions. Opening one shows its newest orders, each with how many model calls and tokens its jobs
used and one small button per job in every repository the order reached. A click on such a button
opens that job in its own project's view. The next round proves this in a real browser.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first,
   before anything else, per protocol order.
2. The Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The next round's first commit books round 2's verdict.
5. T003, the browser proof and the user page.

Operator questions open: 1.
Open findings: 5 — R-1248, owned by F305, and R-1235, R-1246, R-1251 and R-1252, owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | round 1 booked (VERDICT PASS), DECISION F305 D3 recorded, one `.agent/prose_slips.md` line added, `.agent/plan.md` rewritten for round 2; all byte proofs `True` |
| C2 | done | T002's client seam `missionCard.ts` and its vitest file |
| C3 | done | T002's two doors `missionCardDoor.ts` and their vitest file |
| C4 | done | the missions panel and its CSS module, the "Missions" button, `openJob` in the project context, the shell's mount, the contract test, the cockpit page's paragraph |
| C5 | done | this handback |
| T002 | done | the mission card's client seam and doors, the missions panel, its button and mount, `openJob`, the contract test; resolves R-1248 per DECISION F305 D3 |
| Gate 1 | passed | every line `True`, `ALL True` |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | `vite build exit 0`, `porcelain empty True` |
| Gate 4 | passed | exit 0, `4833 passed, 13 skipped`, no FAILED/ERROR, no `process(es) behind` line, exact match to the reviewer's dry-tree reading |
| Gate 5 | passed | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 6 | passed | subjects of C1 to C4, newest first, as shown above |
