── STEP D2 LINKAGE — F021 ──
Goal:        Record R32, which PASSED, and land DECISION F021 D2's single
             additive field: the envelope both event transports share gains
             `task_id`, the linkage a feed row needs to jump to its node. The
             field is resolved from TWO places, which is the part D2's text
             does not say and the part a naive implementation gets silently
             wrong. Two corrections are appended naming OPEN findings R-0661
             and R-0607; NEITHER mints an id. Both are the REVIEWER's defects.

Fortschritt: ~98 % (T002 fertig; T003 beginnt hier mit dem Server-Feld, dem
             der Klick-Sprung und der deaktivierte Steuer-Eingang folgen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R32 verdict
             and the two corrections · C3 the envelope field TOGETHER WITH the
             two test changes that keep the suite green · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r33.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `packages/orchestration/ui_server.py` (C3) ·
             `tests/ui_server/test_sse_stream.py` (C3) · `.agent/handoff.md`
             (C4). Resolve any count in this block against that list. NO client
             file is touched: `apps/ui/src/api/feedRow.ts` and
             `ActivityFeedCard.tsx` consume this field in R34. A server field
             with no consumer yet is the correct first half — the envelope has
             ONE writer, and the client cannot be wired to a field that does
             not exist.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap,
    reflow, reindent or whitespace-adjust one. If a slice looks wrong, STOP and
    say so in the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `6e529304` — resolve its full form with
    `git rev-parse`.
 3. C3 IS ONE COMMIT AND NOT TWO, and this is the one place this block departs
    from "one step per commit". The source change and the test changes are one
    logical step because two EXISTING assertions pin the envelope against
    exactly the shape the field changes: `test_the_envelope_carries_the_safe_
    fields_only` pins the key set to exactly four names, and `TestFramingGolden`
    pins the wire bytes. Either half committed alone is a commit that fails its
    own gate. MEASURED, not reasoned: in a disposable worktree at `6e529304` I
    applied the two test pairs WITHOUT the source pair and
    `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` printed
    `4 failed, 62 passed`. Insertions stay far under 500 either way.
 4. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it, in
    `.agent/live_review.md`: 224 registered under the canonical pattern
    `^- R-\d+ — `, maximum R-0661, `Done: R-` 1. After C2: still 224, still all
    DISTINCT, still maximum R-0661, `Done: R-` still 1. Both corrections name
    OPEN findings rather than new ids, per §3 checklist item 30, and each of
    `^- R-0661 — ` and `^- R-0607 — ` stays at exactly 1 across C2.
 5. NO PARAGRAPH OF RECORD33 BEGINS WITH THE BYTES `- R-`. Two open with
    `Recurrence: `, the prefix R30 introduced for a correction that mints no
    id, and the verdict opens `Gate: R33 — `. G5 measures this rather than
    trusting it. RECORD33's paragraphs are separated from one another by
    EXACTLY ONE BLANK LINE, the separator every entry in that file uses.
 6. THE APPEND CONVENTION FOR `.agent/live_review.md` AT C2: the slice is
    quoted WITHOUT a trailing newline; add EXACTLY ONE newline, then RECORD33,
    then one terminator, so the join carries EXACTLY ONE BLANK LINE. A
    WHOLE-FILE write (PLANF021R33) is the slice PLUS one terminator.
 7. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` entry or
    `Recurrence:` entry is edited. A dated correction that names the landed
    text is how this record stays honest (§3 item 20).
 8. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES THE PATTERN IT IS READ UNDER.
 9. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round
    — do not run it and do not report it. Create and merge NO pull request.
    Push the branch after C4. ONE worktree under `.remedy-wt/` is ordered, for
    G6's red-proof alone; remove it and prove the tree clean afterwards.
10. THE THREE PAIRS ARE SUMMARYPAIR, PINPAIR and GOLDENPAIR, and their shapes
    are MEASURED, not asserted. I ran the containment test over their own bytes
    before emission and it printed `TO contains FROM: False` for all three, so
    NONE is append-shaped and a FROM-zero count IS orderable for each. Each
    FROM occurs EXACTLY ONCE in its target at the round base, a reading my
    script printed over the bytes this block prints. SUMMARYPAIR and PINPAIR
    were dry-run in a worktree at `6e529304`; GOLDENPAIR's FROM is the two
    adjacent `GOLDEN_STREAM` lines and is anchored on their per-line timestamp
    literals, because the shorter tail `, "outcome": "ok"}` occurs FIVE times
    in that file and a bulk replacement over it corrupts three INPUT fixtures.
    That is a reading my script printed, after it made exactly that mistake.
11. PINPAIR is applied BEFORE GOLDENPAIR. Neither FROM contains the other and
    they do not overlap, but §4.9's ordering rule stands and the count gates in
    G4 are written for that order.
12. A KNOWN FLAKE, NOT THIS ROUND'S AND NOT TO BE FIXED HERE: in ONE full-suite
    worktree run of `tests/ui_server/` I saw
    `test_command_channel.py::TestCommandChannelDoor::test_post_to_non_commands
    _path_is_405` and `::test_put_is_405_even_on_the_commands_path` fail. Both
    passed in isolation, passed on a re-run of the same tree, and passed in a
    full-suite run at the UNMODIFIED base. They are order or timing dependent
    and no id is minted on one observation. If they go red in G7, re-run the
    suite ONCE and report BOTH results; do not repair them, do not deselect
    them, and do not fold them into this round.
13. Block size, measured on these final bytes AFTER the last edit: TOTAL 312
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 199 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r33.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my
     emitted copy at `.remedy-wt/f021-r33.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices and pairs from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `, and report how many whole
     texts, how many pairs and how many CONTENT lines your extractor printed —
     each a number YOU measured, not one I named — re-measuring constraint 13's
     two numerals from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R33 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU
     measure against AGENTS.md's "keep it short (<50 lines)". If that count is
     50 or more, STOP and report — do NOT trim the file to reach it (R-0654).
 G4  THE THREE PAIRS, at C3. For EACH of SUMMARYPAIR, PINPAIR and GOLDENPAIR
     report its FROM occurring EXACTLY 1x in its target at the round base and
     EXACTLY 0x at C3 — none is append-shaped (constraint 10), so the zero IS
     owed here. Report additionally, over the lines THAT COMMIT'S DIFF ADDS,
     that each TO-only line appears exactly once (§4.9). Then report these
     counts in `tests/ui_server/test_sse_stream.py`, base then C3: the string
     `, "outcome": "ok"}` 5 then 5 — UNCHANGED, which is the proof GOLDENPAIR
     did not bulk-replace the three input fixtures — and `"task_id"` 0 then a
     number YOU count. In `packages/orchestration/ui_server.py`: `task_id` 0 at
     base and a number YOU count at C3.
 G5  THE LEDGER, at C2, every count naming its pattern, base then C2:
     canonical `^- R-\d+ — ` 224 then 224, ALL DISTINCT at both, maximum
     R-0661 at both; loose `^- R-` 225 then 225, its gap to the canonical
     reading 1 at both; `Done: R-` 1 then 1; `^Gate: R` 31 then 32, DISTINCT at
     both; `^Gate: R33` 0 then 1; `^Recurrence: ` 5 then 7;
     `^Recurrence: R-0661 — ` 0 then 1; `^Recurrence: R-0607 — ` 0 then 1;
     `^- R-0661 — ` 1 then 1 and `^- R-0607 — ` 1 then 1. Report also that the
     number of RECORD33 paragraphs opening with the bytes `- R-` is 0, and
     that the base blob is a byte-exact PREFIX of the C2 blob whose remainder
     is EXACTLY one newline plus RECORD33 plus one newline.
 G6  THE RED-PROOF, in a disposable worktree at the round base under
     `.remedy-wt/`, never in the primary checkout. Apply PINPAIR and GOLDENPAIR
     there WITHOUT SUMMARYPAIR and run
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf`. Report the
     failure COUNT and the failing node ids, which must include
     `TestFrameShape::test_the_envelope_carries_the_linkage_from_both_event_
     sources` — the test that exists only to prove the two-source resolution,
     and the one that must not be able to pass without it. Then remove the
     worktree and report `git status --porcelain` at 0 lines and
     `git worktree list` naming the primary checkout alone.
 G7  THE SUITES, SERIAL, in the PRIMARY checkout, from the repository root,
     never two pytest processes at once. `python3 -m pytest tests/ui_server/ -q
     -rf` — I measured 438 passed at the round base and 439 with this round
     applied, the difference being PINPAIR's one new test; report the numbers
     YOU measure and treat constraint 12 as the classifier if the 405 pair is
     among them. Then, because this round rewrites `.agent/` state, ALL FOUR
     state readers — `python3 -m pytest tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf` beside the ui_server
     run above; the fourth file is named because R-0607 rules it in and R32's
     block left it out, which is the recurrence C2 records. Then the canary,
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — 42 at the base.
     Then `python3 -m ruff check packages/orchestration/ui_server.py
     tests/ui_server/test_sse_stream.py`, which I measured GREEN on both files
     at the round base, so exit 0 is an honest demand here and a repository-wide
     ruff run is NOT ordered (R-0364).
 G8  STRUCTURE. `git diff --name-only 6e529304..HEAD` EQUALS the six non-handoff
     `Change:` paths, both set differences reported EMPTY; 6 commits, every one
     single-parent; `git show --numstat` and `git diff --numstat` agree cell by
     cell; every commit's insertions under 500, each number reported. Marker
     sweep, LINE-ANCHORED, 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `,
     `<<<TO `, and 0 for any `<<<` at all, over EXACTLY these four:
     `.agent/plan.md`, `.agent/live_review.md`,
     `packages/orchestration/ui_server.py` and
     `tests/ui_server/test_sse_stream.py`. The two block copies at C0a and C0b
     are NOT swept — they are the marked text itself, and a sweep that
     included them could never pass.
     Reflog read BY OPERATION: every one of this round's rows is `commit`, with
     `amend`, `rebase` and `cherry` 0 each in that field. `gh pr list --state
     open` reported verbatim.

<<<SLICE PLANF021R33
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R33 records R32, which PASSED, and opens T003 at the only place it can start:
the server. Jump-to-node needs a linkage the envelope has never carried, so this
round lands DECISION F021 D2's single additive field, `task_id`, at
`_safe_event_summary` — the one writer both transports share. It is resolved
from TWO sources, because the run log carries the id at the TOP LEVEL while
`_load_job_plan_events` nests it under `metadata`; reading only the first would
leave jump-to-node dead for exactly the trace-driven jobs. Two corrections are
appended against OPEN findings R-0661 and R-0607, neither minting an id.

## Next Steps
1. R34: the client half of T003 — `feedRow.ts` carries the linkage, and a feed
   row click resolves it to a node id through the task list the dashboard
   already carries and emits `onSelectNode`.
2. R35: the steering input, rendered DISABLED with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- The envelope is a wire format with a byte golden. Any further field is a
  deliberate edit of `GOLDEN_STREAM` and of the key-set pin beside it, and the
  short tail those lines share occurs in three INPUT fixtures too.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- Two tests in `tests/ui_server/test_command_channel.py` were seen to fail once
  under a full-suite worktree run and passed everywhere else. Unregistered on
  one observation; a second sighting mints the id.
- No code defect of F021 is open. R-0364, R-0403, R-0587, R-0607 through
  R-0609, R-0611, R-0613, R-0618, R-0622, R-0629, R-0630, R-0644, R-0651,
  R-0653 through R-0659 and R-0661 stay routed to a paydown branch.
<<<END PLANF021R33

<<<SLICE RECORD33
Recurrence: R-0661 — THE FOUR CUSTOM PROPERTIES THIS FINDING ROUTES TO PAYDOWN AS NEEDING A DECIDED VALUE ALL CARRY A `var()` FALLBACK, SO NONE OF THEM DROPS A DECLARATION AND THE ROUTING RESTS ON A FALSE PREMISE. First instance, in the reviewer's own F021 R32 text; NO NEW ID IS MINTED, because this corrects R-0661's own registered wording rather than reporting a different defect (§3 checklist item 30). MEASURED by the reviewer at `6e529304`, over `apps/ui/src`, with a pattern matching a `var(` opening on each of the four names: all four uses are `var(--remedy-mono, ui-monospace, monospace)` in `PromptTracePanel.module.css` and `var(--remedy-warning-bg, #fff3cd)`, `var(--remedy-warning-fg, #664d03)` and `var(--remedy-warning-border, #ffecb5)` in `DegradedBanner.module.css`. A `var()` with a fallback renders the fallback; the browser drops nothing. R-0661's own body states the rule correctly — "no definition AND no fallback" — and then applies it to a set it never tested the second half against, which is why the ONE property that really broke, `--remedy-radius-pill`, was also the ONE whose use had no fallback. THE CONSEQUENCE FOR THE PIN LANDED AT R32 C4: `TestEveryCustomPropertyResolves._unresolved` reads definitions and `var()` names and NEVER reads fallbacks, so its allowlist holds four benign entries and a future BENIGN `var(--new-thing, fallback)` will turn it red. The pin still catches every real instance — its predicate is a superset of the true one — so it is not weakened and is NOT to be changed as a repair of this correction. WHAT THE PAYDOWN BRANCH INHERITS IS THEREFORE SMALLER AND DIFFERENT THAN R-0661 SAYS: not four values to decide against the design reference, but one predicate to narrow to uses that carry no fallback, after which the allowlist should empty itself.

Recurrence: R-0607 — A BLOCK WHOSE CHANGE SET REWRITES `.agent/` STATE ORDERED THREE OF THE FOUR STATE-READER SUITES. Second instance, in the reviewer's own F021 R32 block; NO NEW ID IS MINTED, because R-0607 already rules that "a block whose change set includes any `.agent/` state file also carries the four state-reader files, stated as gates rather than inferred from the change set". THE INSTANCE: the R32 block's G7 ordered `tests/ui_server/`, `tests/orchestration/test_test_runner.py` and `tests/regression/test_resource_safety.py` and stopped there, omitting `tests/orchestration/test_integrity_gate.py`, which reads `.agent/live_review.md` and which R32's C2 rewrote. It cost that round nothing and that is luck rather than design, exactly as R-0607's own first instance was: the reviewer ran the omitted file itself at `6e529304` while gating R32 and measured exit 0 at 16 passed, so the three-suite figure of 511 and the four-suite figure of 527 differ by precisely those 16. THE CAUSE IS THE ONE R-0607 NAMES AND IS WORTH REPEATING because the counter-measure is still not on disk in `docs/agents/planner_reviewer_prompt.md` §3: the four are a SET fixed by what reads `.agent/`, and a block that lists them from memory drops one. G7 of the R33 block names all four and says why.

Gate: R33 — the R32 entry. R32 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND BOTH DEFECTS THIS ROUND RECORDS ARE THE REVIEWER'S OWN, IN THE TWO ENTRIES ABOVE. R32 IS THE ROUND THAT MADE A CSS CUSTOM PROPERTY VISIBLE TO A REPOSITORY WITH NO RENDERER: `apps/ui/src/styles/tokens.css` gained `--remedy-radius-pill: 999px`, the value `docs/ui/design_reference/tokens.css` has always carried, and `tests/ui_contracts/test_design_drift.py` gained an allowlist pin over the unresolved set. THE PIN'S DISCRIMINATOR IS REAL AND THE REVIEWER PROVED IT WITHOUT TRUSTING THE HANDBACK: rebuilding the base CSS tree from `git show 6e529304~5:<path>` over all 19 `.css` files under `apps/ui/src` and running the pin's own predicate printed an unresolved set of EXACTLY FIVE including `--remedy-radius-pill`, against FOUR at the tip, so both new tests are red at the base and green at the tip for the reason the round claims. RE-MEASURED GATES: `tests/ui_contracts/` 486 passed and 4 skipped for 490; `npx tsc --noEmit` from `apps/ui` exit 0 with EMPTY output; the state readers 511 over the three the block ordered, plus 16 for the fourth it omitted; the canary 42. THE LEDGER went 223 to 224 under `^- R-\d+ — `, all distinct, maximum R-0660 to R-0661. STRUCTURE: seven commits, every one single-parent, insertions 330, 248, 16, 8, 4, 46 and 54, each under 500. C5's own three readings, which no handback can state about itself, are `6e529304`, +54/-67, and 83 lines. THE ONE DECLARED DEVIATION WAS VERIFIED TRUE RATHER THAN ACCEPTED: `^Recurrence: R-0587 — ` reads 1 at the round base and 2 at C2, so the R32 block's G5 clause ordering it 0 then 1 was indeed false as written, the slice was right, and the worker was right to declare it rather than repair reviewer text under constraint 1.
<<<END RECORD33

<<<FROM SUMMARYPAIR
    server meant (DECISION F008 D1).
    """
    return {
        "seq": seq,
        "event": event.get("event", ""),
        "timestamp": event.get("timestamp", ""),
        "outcome": event.get("outcome", ""),
    }
<<<TO SUMMARYPAIR
    server meant (DECISION F008 D1).

    `task_id` is DECISION F021 D2's single additive field, and it is resolved
    from TWO places because this repository has two event sources: the run log
    carries it as a top-level `RunEvent` field, while `_load_job_plan_events`
    nests it under `metadata`. Reading only the top level would leave the
    feed's jump-to-node dead for exactly the trace-driven jobs while every
    run-log job worked, which is a half-feature rather than a visible failure.
    Empty string when neither source carries one: a row with no linkage simply
    does not jump.
    """
    metadata = event.get("metadata")
    nested = metadata.get("task_id", "") if isinstance(metadata, dict) else ""
    linkage = event.get("task_id") or nested
    return {
        "seq": seq,
        "event": event.get("event", ""),
        "timestamp": event.get("timestamp", ""),
        "outcome": event.get("outcome", ""),
        "task_id": linkage if isinstance(linkage, str) else "",
    }
<<<END SUMMARYPAIR

<<<FROM PINPAIR
        assert set(summary) == {"seq", "event", "timestamp", "outcome"}
<<<TO PINPAIR
        assert set(summary) == {"seq", "event", "timestamp", "outcome", "task_id"}
        # No linkage in either place is not an error: the row cannot jump.
        assert summary["task_id"] == ""

    def test_the_envelope_carries_the_linkage_from_both_event_sources(self):
        """DECISION F021 D2's single additive field, resolved from TWO places.

        `load_run_events` yields run-log rows whose `task_id` is TOP-LEVEL,
        while `_load_job_plan_events` nests it under `metadata`. A summary
        reading only the top level would leave jump-to-node dead for every
        trace-driven job while every run-log job worked -- a silent half
        feature, and the failure mode no suite here would have surfaced.
        """
        from_run_log = mod._safe_event_summary(
            1, {"event": "task_started", "task_id": "T-7"})
        assert from_run_log["task_id"] == "T-7"

        from_trace = mod._safe_event_summary(
            2, {"event": "task_started", "metadata": {"task_id": "T-9"}})
        assert from_trace["task_id"] == "T-9"

        # Top level wins when both carry one: the run log is the ledger.
        both = mod._safe_event_summary(3, {
            "event": "x", "task_id": "T-1", "metadata": {"task_id": "T-2"}})
        assert both["task_id"] == "T-1"
<<<END PINPAIR

<<<FROM GOLDENPAIR
    b'id: 0\ndata: {"seq": 0, "event": "e0", "timestamp": "2026-08-21T00:00:00Z", "outcome": "ok"}\n\n'
    b'id: 1\ndata: {"seq": 1, "event": "e1", "timestamp": "2026-08-21T00:00:01Z", "outcome": "ok"}\n\n'
<<<TO GOLDENPAIR
    b'id: 0\ndata: {"seq": 0, "event": "e0", "timestamp": "2026-08-21T00:00:00Z", "outcome": "ok", "task_id": ""}\n\n'
    b'id: 1\ndata: {"seq": 1, "event": "e1", "timestamp": "2026-08-21T00:00:01Z", "outcome": "ok", "task_id": ""}\n\n'
<<<END GOLDENPAIR
