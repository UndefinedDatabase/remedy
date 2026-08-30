── STEP CLOSURE PART 1 / F040 — ROUND 18 ─────────────────────
Goal:        Book the R17 verdict (PASS, the integration gate is clean — see
             RECORD18 below), author F040's missing "Built State" section
             (STATUS_closure_protocol.md precondition 4 — the section does
             not exist yet on disk, `grep -c '^## Built State'
             docs/roadmap/features/T5_F040.md` at this round's base is 0),
             and DECLARE the status of every closure precondition (1-6)
             against a real measurement, not a guess. This round does NOT
             build the evidence job or the review zip — that is round 19,
             per the "closure needs two rounds" split (the STATUS line
             needs values only the zip build can produce, so mixing them
             into one round forces a fabricated value). If every
             precondition reads clear, round 19 is the evidence+zip round;
             if one does not, this round's handback says which and why,
             and the next round repairs it instead.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R17 verdict) · C3 the Built State section +
             the precondition declarations · C4 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r18.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/plan.md`                             (C1)
               `.agent/live_review.md`                      (C2)
               `docs/roadmap/features/T5_F040.md`           (C3)
               `.agent/handoff.md`                          (C4)
             NOTHING UNDER `packages/`, `apps/` or `tests/` IS EDITED THIS
             ROUND. The precondition declarations in C3/the handback are
             READ-ONLY measurements (an integrity-check call, a queue read,
             `git` status/log calls) — none of them write a file.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply
    it anyway and DECLARE the objection in the handback. Never repair a
    slice.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and it is fixed.
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 4. RECORD18 IS APPENDED to `.agent/live_review.md`, never inserted, under
    the SAME generalized reading round 17's own constraint 3 already
    established (read `.agent/last_block.md` at this round's base if the
    exact wording is needed — it is unchanged and not restated here to
    keep this block short). Measure the pre-commit byte length and
    trailing-newline state directly; do not assume them.
 5. THE BUILT STATE APPEND, to `docs/roadmap/features/T5_F040.md`. Confirm
    FIRST that no `^## Built State` heading exists in the file at this
    round's base (grep, anchored). The append is pure concatenation: base
    + one newline + BUILTSTATE's own bytes (the leading blank line before
    the new `## ` heading is INSIDE the slice, per the EOF-append
    convention — do not additionally prepend one). Reading (a): the base
    blob is a byte PREFIX of the committed file and the concatenation
    above reconstructs it whole. Reading (b): split BUILTSTATE on blank
    lines into N paragraphs (counted by the script, never asserted);
    paragraph 1 is checked by asking whether SOME blank-line unit of the
    committed file ENDS WITH it (it fuses with the base file's own last
    paragraph across the one-newline join); paragraphs 2..N, N>1 this
    time, are checked by RAW EQUALITY against the committed file's own
    blank-line units in order. Negative control, inside a disposable
    worktree: flip one byte inside BUILTSTATE's own first paragraph and
    report that both readings REJECT it and both ACCEPT the true bytes.
 6. THE CLOSURE PRECONDITIONS (STATUS_closure_protocol.md, all six) are
    measured fresh this round, never assumed from an earlier round's
    prose, and every one of the six gets a stated verdict in the handback:
      (1) every step has a PASS round; every R-id is Resolved or a
          documented Medium/Low risk; latest live_review verdict is PASS
          or PASS_WITH_RISKS. Re-derive this from the ledger itself
          (the same registered/resolved/open-count reading G4 already
          uses) plus a grep for `^Gate: F040 R` lines, rather than citing
          a prior round's claim about it.
      (2) full relevant suite green, verified by the reviewer running it.
          This is ALREADY SATISFIED by round 17's own dedicated
          integration-gate PASS (RECORD18 below) — cite the round number
          and the two exit codes rather than re-running the ~2-minute
          full suite a third time this session for the same commit range.
      (3) `remedy integrity check --json` → PASS. The `remedy` CLI is
          denied session-wide in this sandbox: call
          `packages.orchestration.integrity_gate.run_integrity_checks`
          directly instead and read its `.passed` / `.fail_count`
          attributes (it is a dataclass-like object, not a dict — `.get`
          raises). Report both, plus whether any FAIL is feature-coupled.
      (4) the feature file's Built State section is current — this is
          what C3 makes true; confirm the committed section is present
          and non-empty.
      (5) working tree clean, branch pushed, worker idle — `git status
          --porcelain` empty and `git log
          feature/f040-completion-digest..origin/feature/f040-completion-digest`
          empty (nothing local unpushed) at the gate.
      (6) exactly one self-use item is consumed by this close (F257).
          Read `scripts/self_use_queue.json` fresh: report every item's
          `id` and `consumed_by`. If every item already carries a
          non-null `consumed_by`, the queue is EXHAUSTED for this close —
          record `self-use NONE (queue exhausted)` per the protocol's own
          words, not a fabricated consumption. Do not edit the file this
          round regardless of the reading (consuming an item is a
          write action the round's own Change set above does not permit
          — a real pending item would be a reason to STOP and hand back
          for a dedicated precondition round, not to consume it inline).
 7. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN
    BEFORE C4. If it appears, finish the commit in hand, write the
    handback and stop.
 8. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree`,
    removed before the handback. The primary checkout satisfies `git
    status --porcelain` empty at every commit boundary.

Done when: every gate below is executed, each with its REAL exit code or
REAL measured value taken directly from `subprocess.run(...).returncode`,
`hashlib.sha256`, or a plain `open(...).read()` byte comparison — never
from a pipe, never from `$?`. All of them run at commits strictly earlier
than C4, and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk: report the sha256 and
    byte length of `.remedy-wt/f040-r18-block.md`, of
    `.agent/authored/f040-r18.md` and of `.agent/last_block.md`, and that
    all three are equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN18 slice;
    report its line count and that it is under 50; report that it holds
    `## Goal`, `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length rather than
    taking it from this block. Reading (a) and reading (b) per constraint
    4. Negative control, inside a disposable worktree: flip one byte
    inside RECORD18's first paragraph and report that both readings
    REJECT it and both ACCEPT the unflipped bytes.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base
    and the committed file, never by reading the slice: the distinct ids
    matching `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R17 — `. Report ADDED and REMOVED for each set and the
    open count (registered minus resolved, both distinct) before and
    after; report that no id's status changes this round.
 G5 THE BUILT STATE APPEND, at C3. Per constraint 5: report the pre-commit
    absence of `^## Built State`, the sha256/byte length of BUILTSTATE
    itself, readings (a) and (b) with the negative control, and that the
    committed file's `^## Built State (F040, ` heading appears exactly
    once.
 G6 THE CLOSURE PRECONDITIONS, at C3 or immediately after (read-only,
    no commit of its own). Report the stated verdict for each of the six
    preconditions per constraint 6, with the real command/call and its
    real output for (2), (3), (5) and (6); a ledger-derived reading for
    (1); and the commit reference for (4).
 G7 THE TREE, at C3/C4. `git status --porcelain` empty; `git worktree
    list` one line (primary checkout only); `git branch --list 'tmp/*'`
    empty of any name this round created.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — SESSION 4 of F040 — the round (18),
             the range, one line per gate with its REAL exit code or
             measured value, the item-status table, the six precondition
             verdicts as their own table, the deviations, the open-findings
             count, and the next expected action (round 19: the evidence
             job + review zip, IF every precondition reads clear; otherwise
             a named repair). Then
             `git push -u origin feature/f040-completion-digest`. Create no
             pull request, merge nothing, force-push nothing, touch no
             branch other than any disposable one this round's own
             negative-control worktrees created, all deleted before this
             commit.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN18
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 18.

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
| the integration gate | done | round 17, PASS |
| closure sequence | in progress | this round: Built State + preconditions |

## Next Steps
1. This round appends the R17 verdict to the ledger, writes F040's missing
   Built State section into its feature file, and declares the status of
   all six STATUS_closure_protocol.md preconditions against a fresh
   measurement.
2. If every precondition reads clear, round 19 builds the closure evidence
   job and the review zip (algorithm steps 1-2), reporting the four values
   (job id, package filename, SHA-256, accepted HEAD) a later round needs
   to author the STATUS line — never in the same round that authors it
   (R-0371: a value cannot be quoted before the tool that produces it
   runs).
3. Round 20 (or later) authors the STATUS line and README sync in the
   final closure commit, then opens the PR. The PR is not merged this
   session (G1 of self_drive_protocol.md; STATUS_closure_protocol.md
   algorithm step 6 defers the merge to the next feature's Open PR Gate).
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   this is documented in the Built State section this round adds, not a
   blocker to closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN18

<<<BEGIN RECORD18
Gate: F040 R17 — THE INTEGRATION GATE (verification tier 3, docs/agents/planner_reviewer_prompt.md §3; docs/agents/integration_gate.md steps 1-4). VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3, reading the diff `564bb945..403d8087` in full — C0a-C2 were committed by a stalled prior attempt this session inherited and are reviewed here for the first time alongside C3-C4. THE TRANSPORT, independently re-measured: `.agent/authored/f040-r17.md` and `.agent/last_block.md` sha256-equal at `f28a71ff0df2061cd2c7b7a74db1678ba42bd39d6c66952d331fc287159534c0`, 15198 bytes, both. THE PLAN, independently re-derived from the block's own PLAN17 slice against the committed `.agent/plan.md`: byte-equal (True), 2303 bytes both sides, 44 lines, holding `## Goal`, `## Next Steps` and `F040`. THE RECORD APPEND, independently reconstructed: `.agent/live_review.md` at `564bb945^` is 1738793 bytes ending in a trailing newline; `base + "\n" + RECORD17` (3131 bytes) equals the committed 1741925-byte file, exactly. THE LEDGER, independently recomputed by difference between `564bb945^` and `564bb945`: registered ids ADDED `[]` REMOVED `[]` (317 distinct both sides), resolved ids ADDED `[]` REMOVED `[]` (55 distinct both sides), `DECISION F040 D` ids ADDED `[]` REMOVED `[]`, `Gate: F040 R16 —` lines 0 before → 1 after, open count 262 before and after. THE BRANCH RUN WAS INDEPENDENTLY REPRODUCED, not merely re-read: `python3 -m pytest -n auto -q` at branch tip `564bb945` in the primary checkout, REAL EXIT 0, 18642 passed, 20 skipped — matching the handback's own figure exactly. THE BASE RUN WAS INDEPENDENTLY REPRODUCED IN A FRESH DISPOSABLE WORKTREE THE REVIEWER BUILT ITSELF (`git worktree add -b tmp/review-gate-r17 .remedy-wt/wt-review-r17-base f5b1e6c5`, matching the freshly recomputed merge base `f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`; removed, with its branch, after): `apps/ui/node_modules` and `apps/ui/dist` copied from the primary checkout with `symlinks=True`, the R-0736 mtime-parity fix applied proactively (dist mtimes advanced past the worktree's own max source mtime, content untouched), `REMEDY_UI_NO_AUTO_BUILD=1` set. The reviewer's FIRST invocation of the base run (pytest launched from the primary checkout's own process cwd with the worktree given as a path argument) produced 5 unrelated failures inside `tests/test_grouped_cli.py` — a review-side artifact of the wrong process cwd/rootdir affecting which installed package the CLI subprocess resolved, not a real base-branch defect; corrected by re-invoking with the subprocess's own `cwd` set to the worktree root and no path argument, which reproduced the handback's own reported figure exactly: REAL EXIT 0, 18447 passed, 20 skipped, 0 FAILED. Both `comm -13`/`comm -23` against the reviewer's own captured FAILED lists (both empty on both sides) confirm `branch_only.txt`/`base_only.txt` as committed: empty, empty. R-0736 (Medium, OPEN) is confirmed the correct, already-registered attribution for the mtime-staleness class the handback names — no id is minted this round. THE ROUND PASSES: every path in the change set matches the block's fixed order, no constraint is violated, the reused leftover worktree/branch from the stalled prior attempt were independently re-verified against constraints 4-5 before reuse (freshly recomputed merge base match, clean `git status --porcelain` inside it), the primary checkout's tree is clean and pushed. Per docs/agents/integration_gate.md step 5 this verdict is the reviewer's alone to give: THE GATE IS CLEAN. F040 is READY for the closure sequence (STATUS_closure_protocol.md precondition 2 is satisfied by this round). No new finding is raised by this review.
<<<END RECORD18

<<<BEGIN BUILTSTATE

## Built State (F040, 2026-08-30)

What exists on disk at the close of F040, so a later reader need not reconstruct
it from this file's future tense.

**T001 — the envelope composition and endpoint.**
`packages/orchestration/job_digest.py:build_job_digest(job, events=None)`
returns a TOTAL eight-key envelope — `version`, `job_id`, `state`, `headline`,
`cost`, `ownership`, `decisions`, `primary_action` — that never raises on any
input. `ownership` is always `[]` (DECISION F040 D3: F035 owns the ownership
sentences and is unbuilt, so there is no source to read; no version bump is
needed when F035 fills the key). `primary_action` is read straight off
`recommended_next_action(sources)`, the ONE-SOURCE property: the same
`ReportSources` object the digest describes is the one the rule table is asked
about, so the two halves of the answer can never drift apart.
`packages/orchestration/ui_server.py:_build_digest_json` serves this envelope at
`GET /api/jobs/<job_id>/digest`. Goldens live under
`tests/orchestration/fixtures/job_digest/golden/`, one stored JSON per state
shape, compared whole after normalizing exactly three identities that differ on
every build — the job's UUID, its first-eight prefix, and each `td:` decision
id.

**T002 — the client trigger, the card and the storage edge.**
`apps/ui/src/api/jobDigest.ts` decodes the envelope on the client.
`apps/ui/src/api/digestVisibility.ts:digestVisibility` is a PURE total rule
deciding whether the hero card shows: it reads no clock (`nowMs` arrives as a
parameter), keeps no storage, opens no socket, mints nothing, and writes no
presentation copy — `apps/ui/src/api/digestCardCopy.ts:digestCtaText` owns the
CTA phrasing instead, the same split `TopMetricsBar.tsx` already makes one
layer down. `apps/ui/src/api/browserDigestPort.ts:browserDigestVisibilityPort`
is the one storage edge — per-job last-seen and dismissal, keyed in
`window.localStorage` (DECISION F040 D8).
`apps/ui/src/components/digest/DigestHeroCard.tsx` renders the card;
`apps/ui/src/components/shell/RemedyShell.tsx` mounts it as the first child of
the viewport div immediately after `<DegradedBanner>`, conditioned on
`digest !== null`, wired to `loadJobDigest`, `digestVisibility`, and the
storage port's lazy reads for `lastSeenMs` and `dismissedAtMs`.

**T003 — CLI parity and the end-to-end.**
`apps/cli/commands/job.py:_cmd_job_digest` (`remedy job digest <id>`) makes the
SAME two calls `_cmd_job_summary` already makes — `resolve_job_id`/`load_job`,
then `load_run_events` — and prints the SAME `build_job_digest` envelope the
route builds, so the CLI and the route can never disagree about the same job.
`apps/ui/src/api/digestEndToEnd.test.ts` chains `decodeJobDigest` to
`digestVisibility` to `browserDigestVisibilityPort` to `digestCtaText` over one
frozen golden shape, proving the feature file's own script on the client:
finish while away, reopen, correct CTA, dismiss, no re-show, re-arm on new
activity.

**What is deliberately NOT here.** `onOpenDecisions`/`onPrimaryAction` are not
wired to a real action — DECISION F040 D5's "in-page action" needs its own
resolution design and is not yet scheduled; the card renders without them.
`browserDigestPort.ts`'s open risk — a real browser refusing a write (private
mode, quota, disabled storage) — is unaddressed and deferred to whichever round
first meets it, a documented risk rather than a defect.
<<<END BUILTSTATE
──────────────────────────────────────────────────────────────
