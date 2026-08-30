── STEP T003 PART 2 / F040 — ROUND 16 ────────────────────────
Goal:        T003's remaining slice: the end-to-end the feature file's Task
             slicing names — "finish a fake job with the UI 'away' → reopen →
             hero with correct CTA → dismiss → no re-show" — proved on the
             CLIENT by chaining the four T002 seams that no existing test
             file chains: `decodeJobDigest` (round 6), `digestVisibility`
             (round 7), `browserDigestVisibilityPort` (round 12) and
             `digestCtaText` (round 9). This round adds ONE new vitest file
             and touches no production module: every function it calls
             already exists and is already individually red-proofed in its
             own round's test file.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R15 verdict) · C3 the new end-to-end test ·
             C4 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r16.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/plan.md`                             (C1)
               `.agent/live_review.md`                      (C2)
               `apps/ui/src/api/digestEndToEnd.test.ts`     (C3, new)
               `.agent/handoff.md`                          (C4)
             NOTHING ELSE IS EDITED. Every file under `packages/`, every file
             under `apps/cli/`, `apps/ui/src/api/jobDigest.ts`,
             `apps/ui/src/api/digestVisibility.ts`,
             `apps/ui/src/api/browserDigestPort.ts`,
             `apps/ui/src/api/digestCardCopy.ts` and every file under
             `docs/roadmap/` are READ ONLY this round.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the objection in the handback. Never repair a slice.
    `apps/ui/src/api/digestEndToEnd.test.ts` is a byte-exact SLICE this round
    (TESTFILE16 below), not a SPEC — it is a brand-new, self-contained file
    with no surrounding context to integrate against, so it carries no
    ambiguity a SPEC exists to absorb.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and it is fixed.
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 4. RECORD16 IS APPENDED, never inserted. Measured directly rather than
    assumed: read `.agent/live_review.md`'s exact byte length at the branch
    tip this round opens on and confirm whether it ends with a trailing
    newline; do not trust this line's own claim about that byte. The append
    is one newline followed by the slice's bytes. READING (b): split the
    slice into N paragraphs on blank lines (N counted by the script, never
    asserted); paragraph 1 of the slice is ALWAYS checked by asking whether
    SOME blank-line unit of the committed file ENDS WITH paragraph 1, because
    a single-newline join always fuses it with the base's own last paragraph
    whether or not paragraph 1 is also the slice's only paragraph; every
    paragraph 2..N, if N>1, is checked by RAW EQUALITY against the committed
    file's own blank-line units in order.
 5. THE NEW FILE'S BYTES. `apps/ui/src/api/digestEndToEnd.test.ts` does not
    exist before this round (`git ls-tree HEAD -- apps/ui/src/api/digestEndToEnd.test.ts`
    is empty at this round's base `c32c02ff`). Its committed content is
    TESTFILE16 below, byte for byte, and nothing else is written to that path.
 6. THE MUTATION RED-PROOF ROUTE FOR VITEST INSIDE A WORKTREE (finding
    R-0703, docs/agents/planner_reviewer_prompt.md §3 item 33):
    `apps/ui/node_modules` is gitignored, so a fresh worktree carries neither
    the vitest binary nor a loadable config. The reviewer measured the
    working route before authoring this block: from the PRIMARY checkout's
    `apps/ui` directory (so `npx` resolves the real, installed `node_modules`),
    with the worktree built at `.remedy-wt/wt-r16-g6` per constraint 7, run
      npx vitest run --config /home/decodeux/Repos/remedy/apps/ui/vitest.config.ts
        --root /home/decodeux/Repos/remedy/.remedy-wt/wt-r16-g6/apps/ui src/api/
    This resolves the runner and its plugins from the PRIMARY's
    `node_modules` while collecting and executing the WORKTREE's own source
    files. Narrowed to `src/api/` — an UNSCOPED run additionally collects
    `src/components/prompt/promptTraceLens.test.ts`, which fails to resolve
    `react/jsx-dev-runtime` under this `--root` and is a worktree artifact,
    never a result, exactly the R-0703 shape. Measured by the reviewer at
    this round's own base: the unmutated control scoped to `src/api/` is a
    REAL exit 0 (705 passed, 35 files); unscoped it is a real exit 1 on that
    one unrelated file while every `src/api/` test still passes.
 7. THE WORKTREE IS CREATED AFTER C3, at the commit C3 creates, at the fixed
    path `.remedy-wt/wt-r16-g6` (`git worktree add .remedy-wt/wt-r16-g6 HEAD
    --detach`), so it naturally carries the new test file without copying it
    in by hand. Removed before the handback; `git worktree list` one line
    after.
 8. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C4. If it appears, finish the commit in hand, write the handback and stop.
 9. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree`, removed
    before the handback. The primary checkout satisfies `git status
    --porcelain` empty at every commit.

Done when: every gate below is executed, each with its REAL exit code taken
from `subprocess.run(...).returncode`. All of them run at commits strictly
earlier than C4, and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk: report the sha256 and
    byte length of `.remedy-wt/f040-r16-block.md`, of `.agent/authored/f040-r16.md`
    and of `.agent/last_block.md`, and that all three are equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN16 slice; report
    its line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length rather than
    taking it from this block. Reading (a): the base blob is a byte PREFIX of
    the committed file and base + one newline + slice reconstructs it whole.
    Reading (b): per constraint 4. Negative control, inside a disposable
    worktree: flip one byte inside the slice's first paragraph and report
    that both readings REJECT it and both ACCEPT the unflipped bytes.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and
    the committed file, never by reading the slice: the distinct ids matching
    `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R15 — `. Report ADDED and REMOVED for each set and the open
    count (registered minus resolved, both distinct) before and after; report
    that no id's status changes this round.
 G5 THE NEW FILE'S BYTES, at C3. sha256 and byte length of the committed
    `apps/ui/src/api/digestEndToEnd.test.ts` equal to TESTFILE16's own sha256
    and byte length, stated in TESTFILE16's own BEGIN marker.
 G6 THE TEST'S OWN RUN AND ITS RED PROOF, at C3. First,
    `python3 -m pytest tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes -q`
    in the PRIMARY checkout, real exit code (this is the WHOLE-suite vitest
    colour gate, run unscoped exactly as that test itself does — no scoping
    trick here, because the primary checkout has its own real `node_modules`
    and every real source file). Second, THE RED PROOF, per constraints 6-7:
    build the worktree at the commit C3 creates; run the `src/api/`-scoped
    command of constraint 6 as the UNMUTATED CONTROL and report its real exit
    code and passed count; then, asserting the anchor `activityMs >
    dismissedAtMs` is unique in `apps/ui/src/api/digestVisibility.ts` (must be
    1) before replacing it, mutate it to `activityMs >= dismissedAtMs`; rerun
    the SAME scoped command and report the real exit code (must be 1) and the
    failing test's name; restore the file, `cmp` it byte-equal to the
    committed original, rerun the scoped command and report the control
    passed count again, matching the first run. Remove the worktree;
    `git worktree list` one line after.
 G7 THE SUITES AND THE TREE, at C3:
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    Report each REAL exit code. Then report `git status --porcelain`, the
    count from `git ls-files --others --exclude-standard`, `git worktree
    list`, and the `+` column of `git diff --numstat` for each commit from
    C0a through C3. C4's own insertion count is not orderable here and is not
    ordered (§3 item 14). Those insertion numbers are ALSO required in the
    handback's `## Commits` table `+/-` column (§3 item 28): take every cell
    from THIS gate's output and say in the handback that you did.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 4 of F040 — the round
             (16), the range, the per-commit table with the `+/-` column from
             `git diff --numstat`, one line per gate with its REAL exit code,
             the item-status table, the deviations, and the open-findings
             count. Then `git push -u origin feature/f040-completion-digest`.
             Create no pull request, merge nothing, force-push nothing, touch
             no branch.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN16
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 16.

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
| T003 CLI parity — `remedy job digest <id>` | done | round 15, PASS |
| T003 the end-to-end (away, reopen, dismiss, re-arm) | done | this round |
| the integration gate | open | next |
| closure sequence | open | after the gate |

## Next Steps
1. This round adds `apps/ui/src/api/digestEndToEnd.test.ts`, chaining
   `decodeJobDigest` to `digestVisibility` to `digestCtaText` over one of the
   frozen golden shapes, proving the feature file's own script on the client:
   finish while away, reopen, correct CTA, dismiss, no re-show, re-arm.
2. The next round is the dedicated integration-gate round
   (docs/agents/integration_gate.md); a regression there is a normal repair
   round.
3. Then the closure sequence (STATUS_closure_protocol.md): evidence job, a
   fresh review zip, the STATUS line, the PR.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN16

<<<BEGIN RECORD16
Gate: F040 R15 — T003 PART 1, CLI PARITY (`remedy job digest <id>`). VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3, reading the diff `e1050f8c..4eb957b7` in full. THE COMMAND'S SHAPE: over `apps/cli/command_catalog.py` at `4eb957b7`, exactly one `CommandEntry` carries `command_id="job.digest"`, and by direct import `get_command("job.digest").args` resolves to `(_JOB_ID, _JSON_OPT)`'s own values with `supports_json` `True`. Over `apps/cli/commands/job.py`, the diff shows `_cmd_job_digest` following the six-part shape constraint 5 orders, in order: `resolve_job_id`/`load_job` inside a `try`/`except JobNotFoundError`, then `resolve_data_root`/`load_run_events`, then `build_job_digest` as the only envelope builder, then the `if json_output`/bare-mode split; the `COMMAND_HANDLERS` dispatch entry names `_cmd_job_digest(` and `json_output=getattr(args, "json", False)` exactly once. THE GUARD'S OWN RUN AND ITS RED PROOF WERE INDEPENDENTLY REPRODUCED, not merely re-read: `python3 -m pytest tests/cli/test_job_digest_cli.py -q` at `4eb957b7` in the primary checkout, REAL EXIT 0, 9 passed; then, inside a fresh disposable worktree (`.remedy-wt/wt-review-r15`, detached at `4eb957b7`, removed after), each of the block's four mutations to a saved-and-restored copy of `apps/cli/commands/job.py` — (a) the success branch's `if json_output:` to `if True:`, (b) wrapping the JSON envelope in an extra `{'digest': ...}` key, (c) deleting the error branch's `if json_output:`/`else:` split, (d) skipping `resolve_job_id`'s short-prefix resolution — reproduced the SAME failing node ids the handback reports: `TestBareModeIsNotJson::test_bare_output_does_not_parse_as_json` for (a); both `TestJsonModeMatchesTheEnvelopeExactly` tests for (b); `TestUnknownJobId::test_json_mode_exits_1_with_a_json_payload_on_stdout` for (c); `TestShortIdPrefixResolves::test_an_eight_character_prefix_matches_the_full_id_digest` for (d) — each restore verified byte-equal to the committed file and the guard green again (9 passed) before the next mutation, `git worktree list` back to one line after removal. THE LEDGER: independently recomputed by difference between `4f405b74^` and `4f405b74` — registered ADDED `[]` REMOVED `[]`, resolved ADDED `[]` REMOVED `[]`, `DECISION F040 D` ids ADDED `[]` REMOVED `[]`, `Gate: F040 R14 —` lines 0 before, 1 after, open count 262 before and after, distinct registered 317 before and after, distinct resolved 55 before and after — matching the handback exactly. THE SUITES OF G7 WERE INDEPENDENTLY RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT AT `4eb957b7`: `tests/cli/` 1482 passed, `tests/ui_contracts/` 809 passed and 4 skipped, `tests/ui_server/` 515 passed, `tests/docs/` 295 passed — every figure matches the handback's own claim exactly; `git status --porcelain` empty, `git ls-files --others --exclude-standard` 0, `git worktree list` one line, throughout. THE ROUND PASSES: every path in the change set matches the block's order, no constraint is violated, the tree is clean and pushed. No new finding is raised by this review.
<<<END RECORD16

<<<BEGIN TESTFILE16 (apps/ui/src/api/digestEndToEnd.test.ts, new file, C3, sha256=77799c775ed9f10403a6efc248dc96120c4c7ddd1f17e5768733dd94da77b164, 4788 bytes)
import { describe, it, expect } from "vitest";
import { decodeJobDigest } from "./jobDigest";
import { browserDigestVisibilityPort } from "./browserDigestPort";
import { digestVisibility } from "./digestVisibility";
import { digestCtaText } from "./digestCardCopy";

// The feature file's own end-to-end script (T5_F040.md, Task slicing, T003):
// finish a fake job while the UI is away, reopen, the hero shows the right
// CTA, dismiss it, and it does not re-show — then new activity re-arms it.
// This file is the one place all four T002 client seams are chained together,
// because none of their own test files exercises the COMPOSITION the
// feature's Acceptance describes.
//
// Shaped after `tests/orchestration/fixtures/job_digest/golden/
// blocked_with_decisions.json` (hand-copied per the convention
// `jobDigest.test.ts` already establishes, so the fixture and the wire cannot
// drift apart in this file's imagination) — a settled, decision-blocked job
// whose `primary_action.label` carries the real backticked CLI command the
// `open-decision` rule of `recommended_next_action` appends in
// `packages/orchestration/run_report.py`.
const ENVELOPE = {
  version: 1,
  job_id: "e2e-job-1",
  state: "paused",
  headline: "The run is paused and its terminal status is blocked.",
  cost: { value: "not-measured", basis: "absent" },
  ownership: [] as string[],
  decisions: { open_count: 2, peak_urgency: 2400 },
  primary_action: {
    label:
      'Answer the open decision: `remedy decision resolve e2e-job- td:d1 --reason "postgres"`',
    rule_id: "open-decision",
  },
};

// A minimal in-memory `Storage`, narrowed to the two methods
// `browserDigestVisibilityPort` actually calls — the same narrowing the
// port's own module documents, so this fake needs no `removeItem`, `clear`,
// `key` or `length`.
function fakeStorage(): Pick<Storage, "getItem" | "setItem"> {
  const map = new Map<string, string>();
  return {
    getItem: (key: string) => (map.has(key) ? map.get(key)! : null),
    setItem: (key: string, value: string) => {
      map.set(key, value);
    },
  };
}

const T_AWAY = 1_700_000_000_000; // the UI's last known-open instant
const T_FINISH = T_AWAY + 60_000; // the job finishes while the UI is away
const T_REOPEN = T_AWAY + 300_000; // the operator reopens the UI

describe("the completion digest, end to end (T5_F040 T003)", () => {
  it("shows the right CTA on reopen, holds through a dismissal, and re-arms on new activity", () => {
    const digest = decodeJobDigest(ENVELOPE);
    expect(digest).not.toBeNull();
    const jobId = digest!.job_id;

    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeLastSeen(jobId, T_AWAY);

    // Reopen: the job finished while away, and it is SETTLED (`paused`), so
    // it shows on those grounds regardless of the last-seen instant.
    const onReopen = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_FINISH,
      nowMs: T_REOPEN,
    });
    expect(onReopen).toEqual({ show: true, reason: "settled" });

    // The CTA equals the report's own recommendation with the report's
    // Markdown removed and nothing else changed (DECISION F040 D10).
    expect(digestCtaText(digest!.primary_action.label)).toBe(
      "Answer the open decision",
    );

    // Dismiss at the reopen instant.
    port.writeDismissal(jobId, T_REOPEN);
    port.writeLastSeen(jobId, T_REOPEN);

    // No re-show: no activity has happened since the dismissal.
    const afterDismissal = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_FINISH,
      nowMs: T_REOPEN + 60_000,
    });
    expect(afterDismissal).toEqual({ show: false, reason: "dismissed" });

    // The exact dismissal instant itself does not re-arm the card either —
    // the Acceptance's "persists" half of "Dismissal persists; new activity
    // re-arms".
    const atTheBoundary = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_REOPEN,
      nowMs: T_REOPEN + 60_000,
    });
    expect(atTheBoundary).toEqual({ show: false, reason: "dismissed" });

    // New activity strictly after the dismissal re-arms it — the
    // Acceptance's "re-arms" half.
    const T_NEW_ACTIVITY = T_REOPEN + 120_000;
    const reArmed = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_NEW_ACTIVITY,
      nowMs: T_NEW_ACTIVITY + 1,
    });
    expect(reArmed).toEqual({ show: true, reason: "settled" });
  });
});
<<<END TESTFILE16
──────────────────────────────────────────────────────────────
