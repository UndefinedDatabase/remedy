── STEP CLOSURE PART 2 / F040 — ROUND 19 ─────────────────────
Goal:        STATUS_closure_protocol.md algorithm steps 1-2: build the
             closure evidence bundle (`create_manual_completion_bundle`)
             and the review zip (`scripts/make_review_zip.sh`), and report
             the four values a later round needs to author the STATUS
             line — evidence job id, package filename, SHA-256, accepted
             HEAD — spelled exactly as the tools print them. This round
             does NOT author the STATUS line itself (R-0371: a value
             cannot be quoted before the tool that produces it runs — see
             [[feedback_closure_needs_two_rounds]] in spirit, restated
             here as the reason the split exists). Neither the evidence
             dir nor the zip is committed to git (DECISION 2026-08-01,
             STATUS_closure_protocol.md "Evidence dir is not committed");
             both are reported in the handback instead.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R18 verdict) · C3 the evidence bundle and
             the review zip · C4 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r19.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/plan.md`                             (C1)
               `.agent/live_review.md`                      (C2)
               `.agent/handoff.md`                          (C4)
             C3 WRITES NO TRACKED PATH — its outputs (the evidence dir and
             the zip) are both gitignored (`remedy-job-evidence-*/`,
             `remedy-review-*.zip` under `REMEDY_REVIEW_DIR`) and are
             reported in the handback, not committed. NOTHING UNDER
             `packages/`, `apps/` or `tests/` IS EDITED THIS ROUND — this
             round only READS them to run verification.

Constraints:
 1. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and it is fixed.
 2. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23).
 3. RECORD19 IS APPENDED to `.agent/live_review.md`, never inserted, under
    the same generalized reading round 18's own constraint 4 already
    established (read `.agent/last_block.md` at this round's base — i.e.
    round 18's committed block — before you overwrite it at C0b, if the
    exact wording is needed).
 4. THE EVIDENCE SCRIPT IS AN ADAPTATION, NOT AN INVENTION. Start from
    `.agent/authored/f009-r33.md`'s `EVIDENCESCRIPT` slice (read it in
    full) and change ONLY the following — everything else in that script
    (the double path scrub in `_tail`, node ids taken from
    `--collect-only` rather than a `-v` log, the `len(node_ids) ==
    selected` assert, the `build_review_manifest._unsafe_text` pre-scan
    with its own red control, the `OUTPUT_HASH` re-derivation against
    `sha256(stdout_summary)`) is load-bearing and stays exactly as
    written:
      EVIDENCE_DIR = os.path.join(REPO, ".remedy-wt", "f040_closure_evidence",
                                   "remedy-job-evidence-f040-closure")
      BASE = "f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1"
        (re-confirm with `git merge-base feature/f040-completion-digest
        main` before using it; declare in the handback if it differs)
      job_id = "f040-closure"
      job_title = "F040 Completion/return digest - closure"
      step_range = "T001-T003"
      prior_job_ids = ["f033-closure"]
      num_tasks = 3
      note_prefix = "operator-attested manual completion - F040 closure"
      review_feature_id = "f040"
      The `mkrun(...)` list — 9 runs, in this order, none omitted:
        mkrun("vr-0001", "tests/orchestration/test_job_digest.py", 46)
        mkrun("vr-0002", "tests/ui_server/test_digest_route.py", 7)
        mkrun("vr-0003", "tests/cli/test_job_digest_cli.py", 9)
        mkrun("vr-0004", "tests/ui_contracts/test_digest_card_copy.py", 23)
        mkrun("vr-0005", "tests/ui_contracts/test_digest_hero_card.py", 25)
        mkrun("vr-0006", "tests/ui_contracts/test_digest_hero_css.py", 7)
        mkrun("vr-0007", "tests/ui_contracts/test_digest_mount.py", 26)
        mkrun("vr-0008", "tests/ui_contracts/test_job_digest_card_contract.py", 29)
        mkrun("vr-0009",
              "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes",
              1)
      Every one of these 9 expected counts was measured fresh by the
      reviewer via `--collect-only` immediately before this block was
      authored and all 9 files together passed 172 (the first 8) plus 1
      (the 9th) with ZERO skips, ZERO failures — if a re-run under this
      script disagrees with any of these 9 numbers, that is a STOP
      condition (constraint 8), not a number to silently update.
 5. IF ANY NODE ID OR COMMAND STRING IS REJECTED by
    `build_review_manifest._unsafe_text` (the pre-scan the adapted script
    runs before ever calling `create_manual_completion_bundle`, per the
    template's own assert), that is expected to be RARE for this feature
    (no path-traversal-torture parametrization is known to exist in any
    of the 9 files above) but if it happens, follow the template's own
    `-k`-deselect pattern exactly as `mkrun`'s own docstring describes
    rather than deleting the id from the count, and declare the
    discovery in the handback.
 6. THE ZIP BUILD is the canonical sequence from
    STATUS_closure_protocol.md's "Canonical zip build sequence": confirm
    the tree is clean and pushed (it will be, from C0a-C2 of THIS round,
    committed and pushed before C3 begins — do not build the zip from a
    dirty tree), then
      bash scripts/make_review_zip.sh --evidence-dir <EVIDENCE_DIR above>
    Record the exact printed zip filename and its SHA-256. `REMEDY_REVIEW_DIR`
    is unset in this shell, so the script's own default
    (`$HOME/Repos/remedy-history/zips`) is where the package lands; record
    that absolute path as the package's ARCHIVED PATH (DECISION amend0827
    D1) rather than assuming it.
 7. AFTER THE ZIP BUILDS, verify from the package itself, never from a
    script's own printed claim alone: open the zip, read
    `committed_review_subject.head_commit` out of its manifest, and
    confirm it equals the `HEAD` this round's own C2 commit produced
    (the accepted HEAD). Confirm `PACKAGE_STATUS` in the filename (or the
    manifest) reads `READY_FOR_REVIEW` — any other status is a closure
    BLOCKER per the protocol's own "Packaging-deadlock rule": STOP, do
    not repair the underlying cause in this round, and report the exact
    rejection in the handback instead (constraint 8).
 8. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN
    BEFORE C4. If it appears, finish the commit in hand, write the
    handback and stop. Likewise, if constraint 6's manifest check or
    constraint 7's status check fails, STOP after finishing the commit in
    hand (do not attempt a fix this round) and hand back with the exact
    failure.
 9. DESTRUCTIVE / LONG-RUNNING VERIFICATION (the evidence script's own
    test runs, the zip build) may run in the primary checkout — none of
    it mutates a tracked file, per the Change set above, and every
    tracked-file write this round is one of C0a-C2/C4. The primary
    checkout satisfies `git status --porcelain` empty at every commit
    boundary.

Done when: every gate below is executed, each with its REAL exit code or
REAL measured value taken directly from `subprocess.run(...).returncode`,
`hashlib.sha256`, or a plain `open(...).read()` byte comparison.

 G1 TRANSPORT, at C0b. sha256 and byte length of
    `.remedy-wt/f040-r19-block.md`, `.agent/authored/f040-r19.md` and
    `.agent/last_block.md`; all three equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to PLAN19; line count
    under 50; holds `## Goal`, `## Next Steps`, `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Reading (a) and (b) per constraint 3, with
    the negative control inside a disposable worktree.
 G4 THE LEDGER, at C2. Distinct registered/resolved/`DECISION F040 D`
    ADDED and REMOVED (report none of either), `^Gate: F040 R18 — ` lines
    0 before 1 after, open count unchanged.
 G5 THE VERIFICATION RUNS, at C3. For each of the 9 `mkrun` calls: real
    exit code (must be 0), passed/failed/skipped counts matching
    constraint 4's stated expectations exactly, `len(node_ids) ==
    selected`, and the pre-bundle `_unsafe_text` scan rejecting zero
    strings across every run's node ids and command.
 G6 THE BUNDLE AND THE ZIP, at C3. `create_manual_completion_bundle`'s own
    returned result (job id, paths); the zip build's real exit code;
    the printed filename and SHA-256; the manifest's own
    `committed_review_subject.head_commit` read back OUT OF THE PACKAGE
    equal to this round's C2 commit SHA; `PACKAGE_STATUS` reading
    `READY_FOR_REVIEW`; the OUTPUT_HASH re-derivation from the template
    matching for every run.
 G7 THE TREE, at C3/C4. `git status --porcelain` empty; `git worktree
    list` one line; no path under `.remedy-wt/f040_closure_evidence/` or
    the zip's own directory is tracked by git (`git check-ignore` on
    each, or `git status --porcelain` staying empty after they exist,
    is sufficient proof).

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry SESSION 4, round 19, the range, one line per gate with
             its real exit code or value, the item-status table, the
             FOUR VALUES this round exists to produce (evidence job id,
             package filename, SHA-256, accepted HEAD) spelled exactly as
             the tools printed them, deviations, open-findings count, and
             the next expected action (round 20: the STATUS line, README
             sync and the final closure commit + PR — reviewer-authored,
             worker-applied verbatim, per algorithm steps 3-5). Then
             `git push -u origin feature/f040-completion-digest`. Create
             no pull request, merge nothing, force-push nothing.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN19
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 19.

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
| closure preconditions + Built State | done | round 18, all six CLEAR/NONE |
| closure evidence job + review zip | in progress | this round |
| STATUS line + README sync + PR | open | next, if the zip is READY |

## Next Steps
1. This round builds the closure evidence bundle and the review zip
   (STATUS_closure_protocol.md algorithm steps 1-2) and reports the four
   values a later round needs: evidence job id, package filename,
   SHA-256, accepted HEAD.
2. If the package reads READY_FOR_REVIEW, round 20 authors the STATUS
   line and syncs README in the same final closure commit (R-0154: they
   may never disagree in any committed state), then opens the PR. The PR
   merges at the next feature's Open PR Gate, not this session
   (STATUS_closure_protocol.md algorithm step 6).
3. If the zip build fails or packages BLOCKED_EVIDENCE, that is a closure
   BLOCKER: STOP and hand back with the exact rejection rather than
   repairing it in the same round.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   documented in the Built State section, not a blocker to closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN19

<<<BEGIN RECORD19
Gate: F040 R18 — THE CLOSURE PRECONDITION ROUND (STATUS_closure_protocol.md preconditions 1-6; the closure-round bookkeeping exception of amend0827-process-diet rule 1). VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, reading the diff `403d8087..4db6c088` in full. THE TRANSPORT: `.remedy-wt/f040-r18-block.md`, `.agent/authored/f040-r18.md` and `.agent/last_block.md` sha256-equal at `de6ad99cd996c3125f209f18b70ac20b598aecc6c05a946554489d92e10ddfae`, 20312 bytes, all three, against the reviewer's OWN scratch original rather than a copy taken on faith. THE PLAN: byte-equal to PLAN18, 2394 bytes, 47 lines, holding `## Goal`, `## Next Steps`, `F040`. THE RECORD APPEND: base 1741925 bytes trailing-newline-terminated; `base + "\n" + RECORD18` equals the committed 1745755-byte file exactly. THE LEDGER, recomputed by difference between `135bb0bc^` and `135bb0bc`: registered/resolved ADDED `[]` REMOVED `[]` (317/55 distinct both sides), `DECISION F040 D` ADDED `[]` REMOVED `[]`, `Gate: F040 R17 —` lines 0 before → 1 after, open count 262 unchanged. THE BUILT STATE APPEND, independently reconstructed: base (`docs/roadmap/features/T5_F040.md` at `9ff9dac5^`) 6647 bytes with no `## Built State` heading; `base + "\n" + BUILTSTATE` equals the committed 10081-byte file exactly; the committed file carries exactly one `## Built State (F040, ` heading. ONE DEVIATION IS CONFIRMED AND ACCEPTED, NON-BLOCKING: the committed file carries TWO blank lines before the new heading rather than one — the reviewer's OWN authored BUILTSTATE slice began with its own leading blank line while the block's constraint 5 also specified a one-newline join on top of the base file's own trailing newline, so the double blank is an authoring slip in the REVIEWER's block text, not a worker error; the worker applied it byte for byte per constraint 1 ("never repair a slice") and declared it. Pure whitespace, no effect on any heading anchor or rendered structure beyond one extra blank line; no id is minted. THE SIX CLOSURE PRECONDITIONS were independently re-measured by the reviewer, not read back from the handback: (1) CLEAR — 16 distinct `^Gate: F040 R` lines on record (R1-R9, R11-R17; R10 folded into R11's own text), every F040-scoped open id is a documented Low/Medium risk, latest verdict PASS. (2) CLEAR — satisfied by round 17's own integration gate, re-cited rather than re-run a third time this session. (3) CLEAR — `packages.orchestration.integrity_gate.run_integrity_checks()` called directly by the reviewer: `.passed=True`, `.fail_count=0`. (4) CLEAR — the Built State section is present and non-empty, confirmed above. (5) CLEAR — `git status --porcelain` empty, `git worktree list` one line, `git branch --list 'tmp/*'` empty, both push directions confirmed empty by the reviewer's own `git fetch`. (6) NONE (queue exhausted) — `git diff 403d8087..4db6c088 -- scripts/self_use_queue.json` is EMPTY (confirmed unedited by the reviewer directly), and its one item `SU-001` already carries `consumed_by: "F257"` — no pending item exists for F040 to consume. THE ROUND PASSES: every path in the change set matches the block's fixed order, the tree is clean and pushed, no `tmp/*` branch or extra worktree survives. F040 is CLEAR on every closure precondition; round 19 is the evidence job and review zip build (STATUS_closure_protocol.md algorithm steps 1-2). No new finding is raised by this review.
<<<END RECORD19
──────────────────────────────────────────────────────────────
