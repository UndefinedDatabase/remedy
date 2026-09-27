# Handoff — F030, round 3 (book R2, DECISION F030 D3, T003 browser half)

## Session

SESSION 1 of feature F030 · round 3 · rounds so far 3. Context remaining at
handback: comfortable — the round read every named source file once, wrote
S1–S6's production change and its five new/changed test files across six
commits plus the mutation tool in one pass, hit no red gate anywhere (tsc,
vitest, ruff, the pinned pytest selection and all eleven G5 mutations went
exactly as expected on the first try), and still has a healthy context
budget left.

## Range

Review of `59e02546d`..`HEAD` (`HEAD` is this handback's own commit, `F030
R3 C7`, on `feature/f030-steering-messages`).

## Commits

### ee4ddb5da F030 R3 C1: copy round 3 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r3-block.md | 268/0 | verbatim copy of this round's block |
| .agent/authored/f030-r3-booking.diff | 81/0 | verbatim copy of the booking payload |
| .agent/authored/f030-r3-plan.md | 30/0 | verbatim copy of the plan payload |

Measured insertions: 379 (268+81+30). Block expected 268+111=379. Match.

### bd4285942 F030 R3 C2: book round 2's PASS and record DECISION F030 D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 44/0 | DECISION F030 D3 appended (`git apply` of booking.diff) |
| .agent/live_review.md | 2/0 | F030 R2 Gate entry appended (`git apply` of booking.diff) |
| .agent/plan.md | 8/7 | rewritten to plan.md payload |
| .agent/prose_slips.md | 1/0 | R2's binding-word prose slip appended (`git apply` of booking.diff) |
| docs/ui/design_reference/assumption_log.md | 2/0 | two DECISION F030 D3 rows appended (`git apply` of booking.diff) |

Measured numstat: 44/0, 2/0, 8/7, 1/0, 2/0. Block expected exactly this. Match.

### ee860302e F030 R3 C3: carry a steering note's text on its stream frame
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 30/0 | S1 `_steering_note_summary_payload`; `_safe_event_summary` gains `note`, conditional on `steering_message_received`, task id falling back to the event's own top-level field |
| tests/ui_server/test_steering_note_frame.py | 51/0 | new: the four note fields with the text verbatim, an empty task id for a job-wide note, the top-level fallback, the metadata-wins case, no `steering` key, the base five for an unknown kind |

Measured insertions: 81. No insertion count was ordered for this commit.

### b534119ed F030 R3 C4: show a note as the operator's own line and pass the selected task
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/feedRow.test.ts | 26/0 | S2 cases: a note's own line and `author`, a malformed note keeps the catalog line and no author, every other row has no author |
| apps/ui/src/api/feedRow.ts | 10/1 | S2 `author?: "operator"`; `feedRowOf` reads `readSteeringNote`, gives a note's row its text verbatim and `author: "operator"` |
| apps/ui/src/api/steeringNote.test.ts | 79/0 | new: `readSteeringNote`, `steeringFocusTaskId`, `steeringPlaceholder` |
| apps/ui/src/api/steeringNote.ts | 70/0 | new: S2 `STEERING_NOTE_EVENT`, `SteeringNote`, `readSteeringNote`; S3 `steeringFocusTaskId`; S5 `steeringPlaceholder` (its test lives in this same new file's test, so it ships with S2/S3 rather than split into C5) |
| apps/ui/src/components/panels/ActivityFeedCard.tsx | 10/3 | S2 operator row: an initial-letter disc and "You" in place of the glyph and kind; S3 `focusedTaskId?: string` accepted (unused in this commit — its consumer is C5's composer) |
| apps/ui/src/components/panels/RightLivePanel.module.css | 15/0 | S2 `.operatorDisc`, role-disc size, `var(--remedy-*)` tokens only |
| apps/ui/src/components/panels/RightLivePanel.tsx | 2/2 | S3 `focusedTaskId?: string` accepted and passed on the one `<ActivityFeedCard` line |
| apps/ui/src/components/shell/RemedyShell.tsx | 6/1 | S3 `steeringFocusTaskId(dashboard.tasks, selectedNode ? selectedNode.nodeId : null)` computed after the prompt resolution, passed on the one `<RightLivePanel` line |

Measured insertions: 218. No insertion count was ordered for this commit.

### cbcc51621 F030 R3 C5: address the input's note to the selected task, promising no reply
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | 7/0 | S5/S6 `STEERING_REPLY_FRAMING`, at column 0, outside `STREAM_EVENT_CATALOG` |
| apps/ui/src/api/steeringSend.test.ts | 145/0 | S4 cases: `buildSteerTaskRequest`'s exact request and its three null cases, `describeSteerTaskResult`'s five outcome classes, `sendSteeringNote`'s send/refuse/unreachable flow |
| apps/ui/src/api/steeringSend.ts | 175/0 | S4 `STEER_TASK_COMMAND`, `buildSteerTaskRequest`, `SteerTaskSendReply`/`SteerTaskSubmitResult`/`submitSteerTaskRequest` (supporting infra, shaped as `vetoSend.ts`'s own), `describeSteerTaskResult`, `sendSteeringNote` |
| apps/ui/src/components/panels/ActivityFeedCard.tsx | 8/3 | S4/S5 composer wiring: `placeholder`, `hint`, and the exact `onSend` ternary between `sendSteeringNote` and `sendSteeringMessage` |
| apps/ui/src/components/panels/ChatInput.tsx | 8/4 | S5 `placeholder?: string` and `hint?: string`; the literal "Ask something…" is gone; `title` reads `hint` when live |
| tests/ui_contracts/test_steering_note_contract.py | 71/0 | new: the note event is declared, the note fields match the server's, `job.steer` is exposed, `STEERING_REPLY_FRAMING` is pinned once at column 0, the copy audit over every non-test file |
| tests/ui_contracts/test_steering_send_contract.py | 2/1 | S6: the pinned `onSend` literal becomes S4's ternary |

Measured insertions: 416. No insertion count was ordered for this commit.

### 2decf4fbd F030 R3 C6: add the round 3 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r3-mutations.py | 248/0 | G5's red-proof tool, 11 mutations (3 PYTHON over `ui_server.py`, 8 VITEST over `steeringNote.ts`/`feedRow.ts`/`steeringSend.ts`) |

Measured insertions: 248. No insertion count was ordered for this commit.

Exception (self-reference, per `docs/agents/handback_template.md`): this
handback's own commit, `F030 R3 C7`, is not tabled here.

## External actions

- `git worktree add --detach .remedy-wt/f030-r3-mut 2decf4fbd` — G5's
  red-proof worktree. Removed with
  `git worktree remove --force .remedy-wt/f030-r3-mut` and
  `git worktree prune`; `git worktree list | wc -l` read 63 both before and
  after (equal to this round's step-4 reading).
- No push, no PR create/edit/merge yet — those are G6, run after this
  commit; their real readings are in this round's reply, not here.

## Verification

**G1 transport** — payload readings (measured before use):

    block.md lines: 268 sha256: f4ec8621d821c5dff58bde4c42b3db36f5a6c5e454f7bc1204f619b7f5afbb09
    booking.diff lines: 81 bytes: 17619 sha256: ba547e5dbae5785d75c247e4c1801fbdf97ff1af0ed06ed4edf59e3e8df85c71
    plan.md lines: 30 bytes: 1039 sha256: 1ac082044653f3d73d39318d496b6b813a2b16e92ebdbe98fd2c72abe597e2d5

All three equal the delegation message's and the PAYLOADS table's readings
exactly. Each `.agent/authored/f030-r3-*` copy read back with
`git show ee4ddb5da:<path>` equalled its source byte for byte (script
output):

    .agent/authored/f030-r3-block.md byte-identical: True len 21507 21507
    .agent/authored/f030-r3-plan.md byte-identical: True len 1039 1039
    .agent/authored/f030-r3-booking.diff byte-identical: True len 17619 17619

`git apply --check .remedy-wt/f030-r3-payloads/booking.diff` → `REAL_EXIT=0`.
`git apply .remedy-wt/f030-r3-payloads/booking.diff` → `REAL_EXIT=0`.

**G2 the records** — at `bd4285942`, `git show <sha>:<path>` read:

    .agent/decisions.md   bytes: 2318512  sha256: d4a3b9066757f4ee5437a2b700f646a400c919495283585e9ef30d48c28640e9
    .agent/live_review.md bytes: 314301   sha256: fff987aee67d2cef8ac4e04dfe459aabed2f599904df779f29708bff4ede2b26
    .agent/plan.md        bytes: 1039     sha256: 1ac082044653f3d73d39318d496b6b813a2b16e92ebdbe98fd2c72abe597e2d5
    .agent/prose_slips.md bytes: 374557   sha256: 81ead1202d8dcafb5bf69ee9ee32715bd74d5a7255d02f98e25ff0fdac8a5e2b
    docs/ui/design_reference/assumption_log.md bytes: 21917 sha256: ef6dbd9c45dd711ecdcd9427efc6d83ccdea333e4f8f45520ca1751372e74f7e

All five equal the reviewer's given readings. `open_finding_ids` (from
`scripts/rotate_live_review.py`, imported and run over the ledger text at
`bd4285942`) read `[]` — empty, as the reviewer read it. `git diff
--name-only ee4ddb5da bd4285942` named exactly the five paths of the G2
table.

**G3 the code** — ruff at C6 (`2decf4fbd`):

    python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_steering_note_frame.py tests/ui_contracts/test_steering_note_contract.py tests/ui_contracts/test_steering_send_contract.py
    All checks passed!
    REAL_EXIT=0

Quoted from the diff:

    def _steering_note_summary_payload(metadata: Any) -> dict[str, str]:
    ...
        return {
            "message_id": str(meta.get("message_id", "")),
            "text": str(meta.get("text", "")),
            "channel": str(meta.get("channel", "")),
            "task_id": str(meta.get("task_id", "")),
        }

    export function readSteeringNote(envelope: Record<string, unknown>): SteeringNote | null {
      if (envelope["event"] !== STEERING_NOTE_EVENT) { return null; }
      ...
    }

    const isOperator = row.author === "operator";
    ...
    onSend={(text) => (focusedTaskId ? sendSteeringNote(target, focusedTaskId, text) : sendSteeringMessage(target, text))}

    const focusedTaskId = steeringFocusTaskId(dashboard.tasks, selectedNode ? selectedNode.nodeId : null);

**G4 the tests** — at C6, serially, real exit code:

    1851 passed, 11 skipped in 109.16s (0:01:49)
    REAL_EXIT=0

All 11 `SKIPPED` lines read as F252 quarantines (`test_graph_architecture.py`
x2, `test_ux_quality.py` x2, `test_named_bugs.py` x6 — lines 295, 312, 321,
383, 392, 399 — `test_agent_tooling.py` x1, matching the reviewer's stated
eleven exactly). `--collect-only -q` node counts for the two new Python test
files: `tests/ui_server/test_steering_note_frame.py` 6,
`tests/ui_contracts/test_steering_note_contract.py` 5. Accounting: reviewer's
base at `59e02546` (selection less the two new files) read 1840 passed; 1840
+ 6 + 5 = 1851. Matches exactly. Vitest totals the
`TestVitestFrontendTestFoundation` node's subprocess ran (reproduced directly
against the primary's own `vitest` binary for this report, same command the
gate runs): `Test Files 81 passed | 1 skipped (82)`, `Tests 1632 passed | 5
skipped (1637)` — up from the reviewer's base by 28 cases this round added:
`steeringNote.test.ts` (11, a new file), `feedRow.test.ts` (+3, measured by
`it(` count against `59e02546`'s copy: 19 base, 22 now), and
`steeringSend.test.ts` (+14, 17 base, 31 now).

`python3 -m apps.cli.main integrity check --json` →

    {"check_count": 6, "checks": [...], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
    REAL_EXIT=0

All six checks `pass`: `handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`.

**G5 the red proofs** — `git worktree add --detach .remedy-wt/f030-r3-mut
2decf4fbd`, then `python3 -B .agent/authored/f030-r3-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f030-r3-mut`:

    control (start) PYTHON: exit=0 failed=0 tests=[]
    control (start) VITEST: exit=0 failed=0 tests=[]
    m1 the note payload leaves out text: runner=PYTHON exit=1 failed=2 caught=True restored=True
    m2 note is added to every kind's frame: runner=PYTHON exit=1 failed=8 caught=True restored=True
    m3 the note payload also copies record_sha256: runner=PYTHON exit=1 failed=2 caught=True restored=True
    m4 readSteeringNote accepts a blank text: runner=VITEST exit=1 failed=1 caught=True restored=True
    m5 steeringFocusTaskId always answers empty: runner=VITEST exit=1 failed=1 caught=True restored=True
    m6 steeringPlaceholder names the whole job for a task: runner=VITEST exit=1 failed=2 caught=True restored=True
    m7 a note's row keeps the catalog line: runner=VITEST exit=1 failed=1 caught=True restored=True
    m8 a note's row gets no author: runner=VITEST exit=1 failed=1 caught=True restored=True
    m9 buildSteerTaskRequest sends chat.send: runner=VITEST exit=1 failed=2 caught=True restored=True
    m10 buildSteerTaskRequest leaves out task_id: runner=VITEST exit=1 failed=2 caught=True restored=True
    m11 a 409 task_not_steerable reads as the accepted sentence: runner=VITEST exit=1 failed=1 caught=True restored=True
    control (end) PYTHON: exit=0 failed=0 tests=[]
    control (end) VITEST: exit=0 failed=0 tests=[]
    restored byte-identical: True (x11, one line per mutation)
    PRIMARY checkout git status --porcelain: (empty)
    ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
    REAL_EXIT=0

Every one of the eleven mutations caught (exit≠0, failed>0, at least one
failing test named — the tool's own output names each one in full; trimmed
here to `caught`/`restored` for length). None stayed green. Worktree
removed: `git worktree remove --force .remedy-wt/f030-r3-mut`, `git
worktree prune`; `git worktree list | wc -l` read 63 afterward, equal to
this round's step-4 reading.

`git diff --name-only 59e02546` at the tip (before C7): exactly the paths
constraint 3 lists — the three `.agent/authored/f030-r3-*` copies plus
the mutation tool, `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md`,
`docs/ui/design_reference/assumption_log.md`,
`packages/orchestration/ui_server.py`, and under `apps/ui/src/`:
`api/steeringNote.ts`, `api/steeringNote.test.ts`, `api/feedRow.ts`,
`api/feedRow.test.ts`, `api/steeringSend.ts`, `api/steeringSend.test.ts`,
`api/humanizeCatalog.ts`, `components/panels/ActivityFeedCard.tsx`,
`components/panels/ChatInput.tsx`, `components/panels/RightLivePanel.tsx`,
`components/panels/RightLivePanel.module.css`,
`components/shell/RemedyShell.tsx`; and
`tests/ui_server/test_steering_note_frame.py`,
`tests/ui_contracts/test_steering_note_contract.py`,
`tests/ui_contracts/test_steering_send_contract.py`. No path outside that
set; `steering.py`, `event_names.py` and everything under `apps/cli/` are
untouched.

## Authored-text proofs

The three `.agent/authored/f030-r3-*` payload copies (G1, above): each
equals its source byte for byte, read back from `git show ee4ddb5da:<path>`
against the file this worker measured from `.remedy-wt/f030-r3/block.md`
and `.remedy-wt/f030-r3-payloads/`. `.agent/authored/f030-r3-mutations.py`
is this worker's own authored tool (G5), not a reviewer payload, so it
carries no fidelity comparison — its correctness is the G5 red-proof run
itself.

## Deviations & assumptions

1. **`steeringPlaceholder` shipped in C4, not split into C5.** The block's
   own TESTS section names `steeringNote.test.ts` — C4's file — as covering
   `readSteeringNote`, `steeringFocusTaskId` AND `steeringPlaceholder`
   together, even though `steeringPlaceholder` is S5's function (the copy).
   Splitting the one new file `steeringNote.ts` across two commits by
   function would have meant an empty or forward-referencing partial file
   mid-bundle; instead the whole file and its whole test file shipped in C4,
   and C5 only added the CONSUMER of `steeringPlaceholder` (the composer's
   `placeholder={steeringPlaceholder(focusedTaskId ?? "")}` line). No text
   was retyped or moved between commits; C4's `steeringNote.ts` is byte-for-
   byte what C5 still imports from.
2. **`ActivityFeedCard.tsx`'s `focusedTaskId` prop is accepted-but-unused
   in C4.** S3 (the focus) and S4 (the send) both touch this one file: S3
   only asks the card to ACCEPT `focusedTaskId?: string` on its prop type;
   its first USE (the composer's placeholder/hint/onSend) is S4/S5, ordered
   for C5. `tsc --noEmit` therefore fails on C4's tree ALONE (an unused
   destructured parameter, TS6133) — this was measured directly and is
   expected: the block's G3/G4 gates run "at C6", i.e. against the
   cumulative tree after every commit lands, never per-commit, so an
   intermediate commit is a staging point and not itself gated. G3/G4 both
   ran clean at C6, after every commit had landed.
3. No other deviation. Every step, gate and report ran in the block's
   order; no test this round wrote needed correction; no existing test
   went red.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Step 1 (STOP check) | done | `.agent/STOP` absent |
| Step 2 (shell/branch/HEAD) | done | pwd, status, branch, HEAD all matched |
| Step 3 (block bytes) | done | 268 lines, sha256 match exact |
| Step 4 (worktree count) | done | 63 |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | see Deviation 1 (steeringPlaceholder placement) and Deviation 2 (unused prop, expected) |
| C5 | done | |
| C6 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | ruff clean at C6 |
| G4 | done | 1851 passed, 11 skipped; integrity six-for-six |
| G5 | done | all 11 mutations caught, restored byte-identical, primary clean |

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from
disk) — checked at this round's step 1, absent. Then the review of round 3.
Then T003's end-to-end proof — a note sent through the door while a task
builds reaches that task's next round's trace, and the stream shows the
note before the task's next action. Open findings: 0. Operator questions: 0.
