── STEP CORRECT-THE-GROUND — F021 ──
Goal:        Record the R4 verdict, add the new evidence to the OPEN finding
             R-0419, and rule DECISION F021 D3, which corrects the seed
             DECISION F021 D1 chose for T001's coverage constant. The reviewer
             re-measured the emitter sweep D1 rests on and it reads 82 call
             sites and 60 distinct literals over three roots where the
             `packages/`-only sweep read 35 and 23, so T001 is built at R6 on
             ground this round makes correct. This round BUILDS NOTHING and
             touches no file under `apps/`, `packages/` or `tests/`.

Fortschritt: ~12 % (T001 offen · T002 offen · T003 offen; R1 beansprucht, R2
             vermessen, R3 und R5 entschieden, R4 verdiktiert — R5 korrigiert
             den Boden, gebaut wird ab R6) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R4 verdict
             with the R-0419 evidence · C3 DECISION F021 D3 · C4 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r5.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `.agent/handoff.md` (C4).
             Resolve any count in this block against that list rather than
             against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). C3 lands DECIDE3 at the commit DIRECTLY AFTER the one that lands
    RECORD4, which is the ordering RECORD4's closing sentence names and the
    only thing that makes that sentence true. C4 carries only the handback.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. R-0648 stays the maximum
    registered id and R-0649 is the next free one. The one defect this round
    records is the REVIEWER'S OWN, in DECISION F021 D1's CONTEXT, and it is
    recorded as evidence against the OPEN finding R-0419 inside RECORD4 rather
    than under a new id, because §3 checklist item 30 requires the open set to
    be searched for the DEFECT first and that search returned R-0419 holding
    exactly it — its standing rule is that a repository-wide absence claim
    needs a repository-wide search.
 4. ONE WHOLE-FILE REPLACEMENT AND TWO APPENDS. PLANF021R5 replaces
    `.agent/plan.md` at C1 in full. RECORD4 appends to `.agent/live_review.md`
    at C2 and DECIDE3 appends to `.agent/decisions.md` at C3, both based on the
    ROUND BASE, which is `91d14c88a0b2a083fa83bde57df1d6d248e2de52` and is the
    commit every "round base" in this block names. There is NO FROM/TO pair
    this round, so no containment reading
    is owed and none is stated. Measured by the reviewer on the slices' own
    bytes before emission: RECORD4 is ONE blank-line unit and DECIDE3 is FIVE,
    which is the property G6's reader (b) depends on for each of them.
 5. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place.
 6. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature. Push the branch.
 7. DECIDE3 NAMES `apps/ui/src/api/humanize.ts` AND A TEST UNDER
    `tests/ui_contracts/` AS FUTURE WORK. Neither is created this round. The
    directory `tests/ui_contracts/` exists at the round base; the module does
    not, and DECIDE3 says so in the future tense on purpose.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 238
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 186 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C4; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. C4's own reading goes in the round report (§3 checklist item 14).
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r5.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r5.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 8's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R5, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against DECIDE3 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE EMITTER RE-DERIVATION, the reading DECIDE3 rests on, taken by YOU and
     not read back from this block. Walk `packages/`, `apps/` and `scripts/`
     with `ast.parse` over every `*.py` that parses, and count a call site when
     the callee is an attribute named `log` or `append_run_event`, or a bare
     name `append_run_event`, AND an event argument is present — the first
     positional argument for `log`, or the `event=` keyword for either. Report:
     total call sites, DISTINCT string-constant names, and how many event
     arguments are NOT string constants. Then report how many of those distinct
     names lie in the union of `NARRATED_EVENTS`
     (`packages/orchestration/teacher_narration.py`), `EVENT_METADATA_SCHEMAS`
     (`packages/orchestration/event_schemas.py`), `TRACE_EVENT_KINDS` and the
     VALUES of `_STREAM_EVENT_KINDS` (both
     `packages/orchestration/agent_run_trace.py`). The expected readings are 82,
     60, 11 and 15. RED CONTROL, in the same run: restrict the roots to
     `packages/` alone and report the same four numbers again; they must read
     35, 23, 10 and 1, which is the `.agent/f021_inventory.md` reading at
     `4a7b5cbf` and is what makes the sweep provably scope-sensitive rather
     than merely differently written. Report the static stream vocabulary too —
     the distinct literals over the three roots, plus `TRACE_EVENT_KINDS`, plus
     the values of `_STREAM_EVENT_KINDS`, plus the value of
     `COMMAND_ACCEPTED_EVENT` in `packages/orchestration/ui_server.py` — as a
     single size, expected 83, together with the size of the intersection of
     the literals with those trace sets, expected 0. Every one of these numbers
     appears in DECIDE3; a disagreement is reported RED and the round stops
     rather than being reconciled.
 G6  THE TWO APPENDS, each under TWO INDEPENDENT READERS. Obtain every base blob
     with `git show <round base>:<path>` into memory or into scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision,
     which docs/agents/self_drive_protocol.md guardrail G5 forbids outright.
     For C2 over
     `.agent/live_review.md` and again for C3 over `.agent/decisions.md`:
     reader (a) — the round-base blob is a byte-exact PREFIX of the committed
     file and the remainder is EXACTLY one newline plus the slice; report the
     remainder's sha256, byte count and line count, and the file's byte and
     line counts before and after. Reader (b), the SET-WISE form — split BOTH
     blobs on the blank line into units and confirm the new unit LIST equals
     the base unit list followed by the slice's own units, compared ELEMENTWISE
     over the whole list and not at the tail; report N at both points and the
     slice's own unit count. NEGATIVE CONTROL, run once per file: replace one
     printable byte of the FIRST paragraph of the committed file at equal
     length and confirm BOTH readers REJECT that mutant while BOTH ACCEPT the
     true file; name the file, the byte offset and the substitution. Run every
     destructive step inside a disposable worktree under `.remedy-wt/`, never
     in the primary checkout, and remove and prune it before the handback.
 G7  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R5` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. Nothing is
     minted, so the maximum reads R-0648 at both and `Gate: R5` reads 0 then 1.
     Report `- R-0419 —` at both points as well; it must read 1 at both, since
     this round adds evidence to that finding and does not re-register it.
 G8  THE DECISION HEADINGS, line-anchored, at the round base then at C3:
     `^## DECISION ` in `.agent/decisions.md`, expected 112 then 113, and
     `^## DECISION F021 D3 ` expected 0 then 1, so the append lands once and
     not twice. Report both at both points.
 G9  THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY after C4:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED. No docs
     gate is ordered because the `Change:` list holds no `docs/roadmap/**`
     path — check that against the list before you accept this sentence.
 G10 CANARY, run serially and after G9 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
 G11 NO PRODUCTION FILE CHANGED: report that the range from the round base to C4
     holds 0 paths beginning `apps/`, `packages/` or `tests/`, and that
     `git ls-files .remedy-wt` reads 0.
 G12 RANGE, executed after C4: the range from the round base to C4 lists exactly
     the paths of this block's `Change:` list, with the set difference EMPTY in
     both directions. Report both differences. Then: every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's own `## Commits` table (§3 checklist item 28); every
     insertion count for C0a through C3 under the 500 cap, with C4's own count
     reported in the round report rather than here (§3 checklist item 14);
     leading `<<<SLICE ` and `<<<END ` reading 0 LINES in all three files a
     slice lands in; and this round's reflog rows classified with `amend`,
     `rebase` and `cherry` each 0 in the operation field.
 G13 NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list.
 G14 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3 and C4, the round base SHA, ONE LINE PER GATE with the
     transcripts kept in the round report rather than in the file (R-0582), the
     block's `Fortschritt:` line verbatim across all three of its lines, and a
     `## Next` section naming R6 and T001 as the next work. Its own `wc -l` is
     reported against the 60-line cap, with a DECISION D15 line declaring any
     overage and naming the mandated content that caused it. Every commit
     heading in the `## Commits` table carries that commit's FULL subject, and
     where a commit cannot name its own SHA the role and the reason are written
     INSIDE the heading rather than left to a channel that ends with this
     session — that omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R5
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps the streamed event kinds to plain lines, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers the
kind set DECISION F021 D3 rules and an unknown kind renders an honest generic
line rather than vanishing, the feed renders fixture streams per the binding CSS,
jump-to-node focuses the right node, and the steering input renders DISABLED with
its honest tooltip until F030 lands.

## Current Step
R5 records the R4 verdict, adds new evidence to the open finding R-0419, and
rules DECISION F021 D3, which corrects the seed DECISION F021 D1 chose for
T001's coverage constant. It edits no production file: T001 is built at R6, on
ground this round makes correct.

## Next Steps
1. R6 builds T001 headless-first: `apps/ui/src/api/humanize.ts` with the catalog
   and its honest generic line, the vitest generic-path test, and the
   `tests/ui_contracts/` derivation test DECISION F021 D3 rules.
2. R7 rules the frontend test environment, which today collects no component
   test, and the single-subscription fan-out, before T002 needs them.
3. R8 onward T002 then T003, in the feature file's Task slicing order.

## Risks
- The vocabulary DECISION F021 D3 rules is 83 kinds wide. If a catalog entry per
  kind pushes T001 past the 500-insertion commit cap, R6 splits it by source —
  the run-log half and the JobPlan-trace half — in two commits of one round.
- T002 cannot be tested until the frontend test environment changes: measured at
  `4a7b5cbf`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R5

<<<SLICE RECORD4
Gate: R5 — the R4 entry. R4 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK. The reviewer re-derived all twelve gates from the round base `1674333f` and every number the handback states reproduces. TRANSPORT: `.agent/authored/f021-r4.md` at `1141b7ee` and `.agent/last_block.md` at `e77a3128` are byte-equal at sha256 72c0ae517777a33ccd9c0fcddedf3bb92f38fe4bbce36acfb7ada7fe28d8c013 over 16628 bytes and 192 lines. SLICES: the marker extractor over the committed C0a blob prints 2 slices over 43 CONTENT lines, with TOTAL 192 against DECISION F085 D6's 490 and PROSE 149 against D5's 400. PLAN: `.agent/plan.md` at `92aabc95` is byte-equal to PLANF021R4 at 42 lines under the 50 cap, with `^## Goal$` and `^## Next Steps$` each 1. THE APPEND: `.agent/live_review.md` at `5ba3e60a` is the base blob plus one newline plus RECORD3, remainder sha256 9b743544679208c680633ffcfad930549db19c867f7f49e95dc0a5e98f67dc05 over 4494 bytes and 2 lines, the file going 431116 bytes and 1074 lines to 435610 bytes and 1076 lines; reader (b) in its SET-WISE elementwise form reads 218 units at the base, 1 unit of RECORD3 and 219 at C2, with all 219 positions equal. THE NEGATIVE CONTROL WAS REPRODUCED AND IT REALLY DISCRIMINATES: swapping the single printable byte at offset 2 of the C2 file from `L` to `l` at equal length is REJECTED by reader (a) and by reader (b) at carried index 0 of 219, ACCEPTED by the tail-only form the R3 block had ordered, and both readers ACCEPT the true file — the R-0631 evidence RECORD3 records, holding under the reviewer's own run rather than only under the worker's. THE LEDGER SETS reproduce line-anchored at the base then at C2: 211 entries all DISTINCT at both, `Done: R-` 0, `Landed: ` 0, `Gate: R` keys 3 then 4 all DISTINCT, `Gate: R4` 0 then 1, maximum registered id R-0648 at both. THE RANGE reproduces: five commits every one single-parent, the path set EQUAL to the block's five with both set differences EMPTY, 0 paths beginning `apps/`, `packages/` or `tests/`, `git ls-files .remedy-wt` 0, per-commit insertions 192, 119, 15, 2 and 77 with the maximum under the 500 cap, `<<<SLICE ` and `<<<END ` reading 0 lines in both files a slice lands in, and this round's reflog rows all `commit:` with `amend`, `rebase` and `cherry` each 0. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the three contract suites at exit 0 and 511 passed, and the canary `tests/cli/test_golden_path.py` at exit 0 and 42 passed. `git worktree list` shows the primary checkout alone and `gh pr list --state open` prints the empty list. NEW EVIDENCE FOR THE OPEN FINDING R-0419, ADDED HERE RATHER THAN UNDER A NEW ID because §3 checklist item 30 requires the open set to be searched for the DEFECT before minting and that search returned R-0419 holding exactly this shape. R-0419's standing rule is that a block may state a repository-wide absence — "nothing does X", "only one Y exists" — only after a repository-wide search, and that an absence claimed from a narrower search is an unrun claim. DECISION F021 D1, landed in `.agent/decisions.md` at `14060467`, breaks it: its CONTEXT states that "of the distinct literals actually passed at run-log emission sites, only one appears in any of those four sets". That reading came from `.agent/f021_inventory.md` at `4a7b5cbf`, which HONESTLY named its own scope as "an AST sweep of `packages/**/*.py`" — the DECISION dropped the scope and kept the number. Measured by the reviewer at `91d14c88` over `packages/`, `apps/` and `scripts/` with the same AST predicate, the run log has 82 emission call sites, 60 distinct literal names and 11 names computed at runtime, and FIFTEEN of the 60 lie in those four sets rather than one — including every one of `NARRATED_EVENTS`' eleven members, which are emitted from `apps/cli/commands/job.py` and its siblings and which a `packages/`-only sweep cannot see. THE CLAIM WAS LOAD-BEARING, which is why this is evidence against a Medium rather than a note: D1's CHOSEN seeds T001's authoritative coverage constant from that same reading, so the catalog it ordered would have covered 23 of the 83 kinds the stream can statically carry and would have dropped `task_run_started`, `verification_passed` and every other name the feature file's own Goal quotes as an example of a readable story into the unknown-kind fallback. WHY R4 IS PASS AND NOT FAIL: the defect is neither R4's work nor R4's gate. R4 recorded a verdict and closed a session, it minted nothing, it edited no file this evidence concerns, and every gate it ran reproduces exactly. The correction is DECISION F021 D3, which constraint 2 of the block committing this entry orders at the commit directly after it.
<<<END RECORD4

<<<SLICE DECIDE3
## DECISION F021 D3 (2026-08-22) — T001's coverage constant is DERIVED from the Python sources by a contract test rather than hand-seeded, and D1's seeding reading is corrected

CONTEXT, measured by the reviewer at `91d14c88` over `packages/`, `apps/` and `scripts/`. DECISION F021 D1 seeds T001's authoritative coverage constant from "the emission literals that can be enumerated STATICALLY", and supports that with "of the distinct literals actually passed at run-log emission sites, only one appears in any of those four sets". Both readings come from `.agent/f021_inventory.md` at `4a7b5cbf`, which named its own scope as an AST sweep of `packages/**/*.py` and was correct within it; D1 dropped the scope and kept the number. The same AST predicate over all three roots reads 82 emission call sites, 60 distinct string-constant names and 11 event arguments that are not string constants, and 15 of the 60 lie in the four defined sets — every one of `NARRATED_EVENTS`' eleven among them, emitted from `apps/cli/commands/job.py` and its siblings. A second omission compounds it: `_load_events` in `packages/orchestration/ui_server.py` has TWO branches, and the JobPlan branch `_load_job_plan_events` writes the trace event kind straight into the envelope's `event` field, so `TRACE_EVENT_KINDS` and the values of `_STREAM_EVENT_KINDS` in `packages/orchestration/agent_run_trace.py` — 16 and 6 names, whose intersection with the 60 is empty — also reach a reader. With `command.accepted`, emitted through the module constant `COMMAND_ACCEPTED_EVENT` rather than as a call-site literal, the vocabulary that can be enumerated statically is 83 names, not 23. D1's own text is NOT rewritten here: `.agent/decisions.md` is append-only and §3 checklist item 20 makes the dated correction the counter-measure rather than an edit.

CHOSEN: the coverage constant is DERIVED rather than written down. T001 ships a pytest contract test under `tests/ui_contracts/` that re-derives the static kind set from the Python sources — the AST predicate above over the three roots, plus `TRACE_EVENT_KINDS`, plus the values of `_STREAM_EVENT_KINDS`, plus the value of any module-level string constant a run-log call site passes by name — and asserts it EQUALS the key set of the catalog in `apps/ui/src/api/humanize.ts`, read as source text in the manner the files under `tests/ui_contracts/` already use for the stream hook. Drift then goes red from EITHER side: a new Python emitter with no catalog entry, and a catalog entry no emitter can produce. D1's unknown-kind rule stands exactly as ruled and carries the 11 runtime-computed names, which no static derivation can reach, so T001 still ships the generic-path test beside the coverage test.

ALTERNATIVES CONSIDERED. Hand-list the names in the humanize module as D1's constant, corrected to 83: rejected, it is the same maintenance contract with none of the drift protection, because a hand list is exactly the artefact that was wrong here and nothing would ever re-measure it. Generate the TypeScript constant from Python at build time: rejected, `apps/ui` has no generator step and adding one is a build-system change far outside F021. Keep the 23 `packages/` literals and route the rest to the generic line: rejected, it would send `task_run_started` and `verification_passed` — names the feature file's Goal quotes as examples of the story it wants — into the fallback that exists for names nobody can enumerate.

REVERSE IT by deleting the contract test and its equality assertion; the catalog and the unknown-kind rule stand without them, which is the reversal D1 already described.
<<<END DECIDE3
