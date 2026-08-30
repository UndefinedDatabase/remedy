── STEP INTEGRATION GATE / F040 — ROUND 17 ───────────────────
Goal:        The dedicated integration-gate round (verification tier 3,
             docs/agents/planner_reviewer_prompt.md §3): run the full suite
             on this branch and at the merge base, compare, and attribute
             every branch-only failure — docs/agents/integration_gate.md
             steps 1-4, in full, exactly as that file states them. This
             block does not restate that procedure; it points at it and
             gates the evidence it produces. PER THAT FILE'S OWN RULE, ONLY
             THE REVIEWER ISSUES THE GATE VERDICT — this round reports raw
             evidence and per-id classifications and issues NO verdict of
             its own on the feature's readiness.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R16 verdict) · C3 the integration gate run
             and its evidence · C4 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r17.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/plan.md`                             (C1)
               `.agent/live_review.md`                      (C2)
               `.agent/gate_f040_r17/`                      (C3, new dir)
               `.agent/handoff.md`                          (C4)
             NOTHING UNDER `packages/`, `apps/` or `tests/` IS EDITED THIS
             ROUND — this is a read-only verification round over the branch
             as it stands at this round's base. If step 4 of
             docs/agents/integration_gate.md finds a reproducible
             branch-only failure coupled to feature code, that is a BLOCKER:
             STOP per that file's own rule, record the finding text in the
             handback (not in `.agent/live_review.md` — only the reviewer
             mints an R-id, per §4 item 30), and do not attempt a fix this
             round.

Constraints:
 1. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and it is fixed.
 2. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 3. RECORD17 IS APPENDED, never inserted, exactly as constraint 4 of the
    round 16 block already stated it (read `.agent/last_block.md` at this
    round's base if the exact wording is needed) — the reading is unchanged
    and is not restated here to keep this block short. Measure the
    pre-commit byte length and trailing-newline state directly; do not
    assume them.
 4. THE MERGE BASE FOR THE BASE RUN IS `f5b1e6c5` — re-confirm with
    `git merge-base feature/f040-completion-digest main` before using it;
    if the branch has been rebased since this block was authored and the
    merge base differs, use the FRESHLY COMPUTED value and declare the
    discrepancy in the handback.
 5. THE BASE WORKTREE IS A BRANCH, NEVER DETACHED (docs/agents/integration_gate.md
    step 2, DECISION D3, F053 R2): `git worktree add -b tmp/base-gate-r17
    .remedy-wt/wt-r17-base f5b1e6c5`. Remove it AND delete the `tmp/base-gate-r17`
    branch before the handback; `git worktree list` and `git branch --list
    'tmp/*'` both empty of it after.
 6. NODE_MODULES/DIST PARITY (docs/agents/integration_gate.md step 3):
    before the base run, copy the PRIMARY checkout's `apps/ui/node_modules`
    and `apps/ui/dist` into the base worktree with `shutil.copytree(...,
    symlinks=True)` — NEVER the default `symlinks=False`, which dereferences
    npm's bin shims and fabricates base-only failures (finding R-0591). Set
    `REMEDY_UI_NO_AUTO_BUILD=1` for the base run but do not trust it alone;
    record the mtime of every file under the base worktree's `apps/ui/dist`
    immediately before and immediately after the base run and report the
    window — any mtime falling inside it voids the parity claim for that
    run and forces per-id attribution instead of the parity shortcut.
 7. RUN LOGS STAY OUT OF THE TRACKED TREE WHILE A SUITE RUNS
    (docs/agents/integration_gate.md step 2's own reasoning: a growing
    in-repo log changes the worktree digest mid-run and produces false
    manifest-identity failures). Use `subprocess.run(..., capture_output=True)`
    so stdout/stderr are held in the calling PROCESS's memory, never written
    to a file inside either checkout while the suite runs; write the
    captured text to `.agent/gate_f040_r17/branch_run.txt` and
    `.agent/gate_f040_r17/base_run.txt` only AFTER each run exits, as part
    of commit C3.
 8. FOR EVERY BRANCH-ONLY id (docs/agents/integration_gate.md step 4):
    serial re-run (`python3 -m pytest <node id> -q`, no `-n`) at the branch
    tip; a serial pass is the xdist-flake class (record, not a blocker); a
    serial failure is re-run at the merge base worktree before any
    conclusion. Record the classification of EVERY branch-only id in
    `.agent/gate_f040_r17/attribution.md` — none may be silently omitted.
 9. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C4. If it appears, finish the commit in hand, write the handback and
    stop.
10. DESTRUCTIVE / LONG-RUNNING VERIFICATION ONLY INSIDE THE DISPOSABLE
    WORKTREE OF CONSTRAINT 5. The primary checkout satisfies `git status
    --porcelain` empty at every commit boundary; the branch run (step 1) is
    the one exception that reads the primary checkout without mutating it.

Done when: every gate below is executed, each with its REAL exit code taken
from `subprocess.run(...).returncode`. All of them run at commits strictly
earlier than C4, and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk: report the sha256 and
    byte length of `.remedy-wt/f040-r17-block.md`, of `.agent/authored/f040-r17.md`
    and of `.agent/last_block.md`, and that all three are equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN17 slice; report
    its line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length rather than
    taking it from this block. Reading (a): the base blob is a byte PREFIX
    of the committed file and base + one newline + slice reconstructs it
    whole. Reading (b): per round 16's constraint 4 (unchanged). Negative
    control, inside a disposable worktree: flip one byte inside the slice's
    first paragraph and report that both readings REJECT it and both ACCEPT
    the unflipped bytes.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and
    the committed file, never by reading the slice: the distinct ids
    matching `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R16 — `. Report ADDED and REMOVED for each set and the open
    count (registered minus resolved, both distinct) before and after;
    report that no id's status changes this round.
 G5 THE BRANCH RUN, at C3. `.agent/gate_f040_r17/branch_run.txt` exists and
    is non-empty; report the real exit code of `python3 -m pytest -n auto -q`
    at this round's own branch tip (captured per constraint 7), the wall
    time, and the count of lines in `.agent/gate_f040_r17/branch_failed.txt`
    (`grep '^FAILED'` over the captured output, sorted).
 G6 THE BASE RUN, at C3. `.agent/gate_f040_r17/base_run.txt` exists and is
    non-empty; report the real exit code, the wall time, the count of lines
    in `.agent/gate_f040_r17/base_failed.txt`, the dist mtime window from
    constraint 6, and that the base worktree and its `tmp/base-gate-r17`
    branch are both gone after (`git worktree list`, `git branch --list
    'tmp/*'`).
 G7 THE COMPARISON AND ATTRIBUTION, at C3. Report the line counts of
    `comm -13 base_failed.txt branch_failed.txt` (branch-only) and
    `comm -23 base_failed.txt branch_failed.txt` (base-only, environment- or
    parity-attributed per constraint 6) saved as
    `.agent/gate_f040_r17/branch_only.txt` and
    `.agent/gate_f040_r17/base_only.txt`; report that
    `.agent/gate_f040_r17/attribution.md` names EVERY id in `branch_only.txt`
    with its classification per constraint 8, and that
    `git status --porcelain` is empty and `git worktree list` shows one line
    at this gate.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 4 of F040 — the
             round (17), the range, one line per gate with its REAL exit
             code, the item-status table, the deviations, the open-findings
             count, and — because this round issues no verdict of its own —
             a plain summary of what the evidence shows so the reviewer can
             issue the gate verdict at the next review. Then
             `git push -u origin feature/f040-completion-digest`. Create no
             pull request, merge nothing, force-push nothing, touch no
             branch other than the throwaway `tmp/base-gate-r17`, which is
             deleted before this commit.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN17
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 17.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D10 | done | rounds 2-9 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam through the mount | done | rounds 6-14, all PASS |
| T003 CLI parity + the client end-to-end | done | rounds 15-16, all PASS |
| the integration gate | in progress | this round |
| closure sequence | open | next, if the gate is clean |

## Next Steps
1. This round runs docs/agents/integration_gate.md steps 1-4: branch run,
   base run at the merge base `f5b1e6c5` in a throwaway worktree, the
   `comm` comparison, and per-id attribution for every branch-only failure.
   Evidence lands under `.agent/gate_f040_r17/`. Per the gate's own rule,
   ONLY THE REVIEWER ISSUES THE VERDICT — this round reports raw evidence
   and classifications, and the next round's review carries the verdict.
2. If the gate is clean (or every branch-only id is attributed to the known
   xdist-flake or environment-parity classes), the next round starts the
   closure sequence (STATUS_closure_protocol.md): evidence job, a fresh
   review zip, the STATUS line, the PR.
3. If a branch-only failure is coupled to feature code, that is a BLOCKER
   per the gate's own rule: STOP and hand back rather than repairing it in
   the same round, per docs/agents/integration_gate.md step 4.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN17

<<<BEGIN RECORD17
Gate: F040 R16 — T003 PART 2, THE CLIENT END-TO-END. VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3, reading the diff `c32c02ff..f5e9a92e` in full. THE NEW FILE: `apps/ui/src/api/digestEndToEnd.test.ts` is byte-for-byte identical to the block's own TESTFILE16 slice — sha256 `77799c775ed9f10403a6efc248dc96120c4c7ddd1f17e5768733dd94da77b164`, 4788 bytes, measured directly off the committed blob. THE RECORD APPEND, at `e4ab5a14`: the pre-commit base is 1735586 bytes ending in a trailing newline, the committed file is 1738793 bytes, and `base + "\n" + RECORD16 == committed` holds byte for byte against the reviewer's own surviving copy of RECORD16. THE LEDGER, independently recomputed by difference between `e4ab5a14^` and `e4ab5a14`: registered ADDED `[]` REMOVED `[]`, resolved ADDED `[]` REMOVED `[]`, `DECISION F040 D` ids ADDED `[]` REMOVED `[]`, `Gate: F040 R15 —` lines 0 before, 1 after, open count 262 before and after, distinct registered 317 before and after, distinct resolved 55 before and after — matching the handback exactly. THE TEST'S OWN RUN AND ITS RED PROOF WERE INDEPENDENTLY REPRODUCED, not merely re-read: `python3 -m pytest tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes -q` at `f5e9a92e`, REAL EXIT 0, 1 passed; then, inside a fresh disposable worktree (`.remedy-wt/wt-review-r16`, detached at `f5e9a92e`, removed after), the `src/api/`-scoped vitest run (`--config` pointed at the primary's own `apps/ui/vitest.config.ts`, `--root` at the worktree's `apps/ui`, per finding R-0703) gave a REAL exit 0 control at 705 passed across 35 files; mutating the unique occurrence of `activityMs > dismissedAtMs` in `apps/ui/src/api/digestVisibility.ts` to `activityMs >= dismissedAtMs` gave a REAL exit 1 with 2 failing tests — the pre-existing `digestVisibility.test.ts` boundary case AND the new file's own `atTheBoundary` assertion, both reported by name, matching the handback's declared deviation exactly; restoring the file byte-equal to the committed original brought the control back to exit 0 at 705 passed. THE SUITES OF G7 WERE INDEPENDENTLY RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT AT `f5e9a92e`: `tests/ui_contracts/` 809 passed and 4 skipped, `tests/cli/test_golden_path.py` 42 passed — both matching the handback's own claim exactly; `git status --porcelain` empty, `git ls-files --others --exclude-standard` 0, `git worktree list` one line, throughout. Both declared deviations are accepted as non-blocking: the two-test red spread is the new test proving itself a genuine discriminator rather than a contradiction of the block's singular wording, and the sandbox's denial of bare `echo`/`$?`/`$( )` forced every real exit code through `subprocess.run(...).returncode`, which the block already required as the measurement source. THE ROUND PASSES: every path in the change set matches the block's order, no constraint is violated, the tree is clean and pushed. No new finding is raised by this review.
<<<END RECORD17
──────────────────────────────────────────────────────────────
