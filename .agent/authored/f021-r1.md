── STEP CLAIM — F021 ──
Goal:        Claim F021. Create the branch, reset the review record carrying the
             F009 open set forward, gate F009 R34, register the one closure
             candidate F009 carried as a finding, empty the candidates file, and
             claim F021 in the roadmap ledger. This round BUILDS NOTHING: no
             file under `apps/`, `packages/` or `tests/` is touched.

Fortschritt: ~0 % (T001 offen · T002 offen · T003 offen; diese Runde beansprucht
             das Feature, setzt das Review-Record zurueck, gatet F009 R34 und
             registriert den Kandidaten — gebaut wird ab R4) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 context · C3 the
             review-record reset with the F009 R34 gate and R-0648 · C4 empty the
             candidates file · C5 the roadmap claim and the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r1.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/context.md` (C2) ·
             `.agent/live_review.md` (C3) · `.agent/candidates.md` (C4) ·
             `docs/roadmap/STATUS.md` and `.agent/handoff.md` (BOTH in C5).
             That list is EIGHT paths; resolve any count in this block against
             this list rather than against a numeral written elsewhere.

Preface:     Before C0a, create the branch. `main` is at
             `4548995d` — the merge commit of pull request #210, which the
             reviewer merged at the Open PR Gate before this block was written.
             Run `git checkout main`, `git pull --ff-only`, then
             `git checkout -b feature/f021-live-activity-feed`. NO `gh pr merge`
             and NO `gh pr create` runs this round: F021 opens its pull request
             at closure, exactly as F009 did.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes every other substantive commit because the plan must be current
    before them (§3 checklist item 23). C5 is the LAST commit and carries the
    handback, so the handback's own row is measured on staged content.
 3. THIS ROUND MINTS EXACTLY ONE FINDING ID, `R-0648`, and resolves nothing. It
    writes no `Done:` line and no `Landed:` line. The reviewer searched the open
    set for the DEFECT before minting it (§3 checklist item 30): the symbol
    `_check_high_blockers_open` and the string `high blocker` each occur 0 times
    in `.agent/live_review.md` at `c848e17d`, so no open finding describes it.
 4. TWO defects the reviewer found while gating F009 R34 are NOT given ids,
    because item 30's search returned an OPEN finding for each and a second id
    for one defect is a second thing to resolve. Both are recorded as new
    evidence inside GATE1 instead, naming the id they belong to:
      (a) the R34 block's G12 said "the seven declared paths" over a change set
          its own `Change:` section declared with eight members — the shape
          R-0585 already holds OPEN, which is a count resolved against a list
          living elsewhere in the same block;
      (b) the R34 block gated `tests/docs/` alone for a commit touching
          `docs/roadmap/STATUS.md` — the subject R-0493 already holds OPEN.
    This block APPLIES (b)'s counter-measure in its own gate list: G7 runs
    `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
 5. ONE SCRIPTED FILE REBUILD, THREE WHOLE-FILE REPLACEMENTS AND ONE FROM/TO
    PAIR. PLANF021R1 replaces `.agent/plan.md` at C1 in full. CONTEXTF021R1
    replaces `.agent/context.md` at C2 in full. `.agent/live_review.md` is
    REBUILT BY SCRIPT at C3 per constraint 6. CANDIDATES1 replaces
    `.agent/candidates.md` at C4 in full. The single pair applies at C5. Its
    containment reading, PRINTED BY THE REVIEWER'S OWN SCRIPT against
    `docs/roadmap/STATUS.md` at `c848e17d` and recorded here (§3 checklist item
    15): CLAIM `TO contains FROM: false`, so REWRITE — order the FROM-zero
    count for it. CLAIM's FROM occurs EXACTLY ONCE in that file at `c848e17d`;
    the reviewer's script printed 1. Apply it with `count=1` and report the
    occurrence count measured BEFORE the replacement.
 6. THE C3 REBUILD, specified as an algorithm and not as byte surgery, because
    40 of this file's finding entries are hard-wrapped and a line-based reading
    truncates them (R-0572). Read `.agent/live_review.md` at the round base.
    Split the WHOLE file on the two-character sequence newline-newline into
    units. Classify each unit by its FIRST line: a unit whose first line matches
    `^- R-\d+ — ` is a FINDING, one starting `Done: ` is a RESOLUTION, one
    starting `Landed: ` is a LANDED line, one starting `Gate: R` is a GATE, and
    anything else is HEADER. The reviewer measured that classification at the
    round base and it printed 213 FINDING, 3 RESOLUTION, 0 LANDED, 34 GATE and 4
    HEADER units. Build the new file as, in order: LRHEAD, then every FINDING
    unit whose id does NOT appear in a RESOLUTION unit, in their original order,
    then R0648, then GATE1 — each unit stripped of leading newlines and joined
    with exactly one blank line between neighbours, and the file ending in
    exactly one newline. The RESOLUTION, GATE and HEADER units are DROPPED; git
    history is their archive, per the same reset rule F009's own record cites,
    DECISION F057 D1 in `.agent/decisions.md` and finding R-0362.
 7. Report the numbers the C3 script itself printed — the five unit counts, the
    number of FINDING units carried forward, and the ids dropped as resolved.
    Do not restate the reviewer's numerals as your own reading; if your script
    disagrees with constraint 6, that disagreement is the finding and the
    handback says so instead of reconciling it.
 8. The three `.agent/` state texts must satisfy the repo's own contract tests,
    which the reviewer validated against every test that reads those paths
    (§4.11): `.agent/plan.md` carries `## Goal`, `## Next Steps`, the substring
    `Steps` and a three-digit F-id; `.agent/context.md` carries `## Active
    Branch`, a `feature/` slug, the substring `Steps`, a three-digit F-id and
    the substring `pytest`; `.agent/live_review.md` carries the substring
    `Steps`. Those properties are gated at G5 and G6, not assumed.
 9. Block size, measured on these final bytes: TOTAL 350 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 206
    against DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C5; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. C5's own reading goes in the round report, because a commit cannot
     report the tree state that follows it (§3 checklist item 14).
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r1.md` at C0a, over
     `.agent/last_block.md` at C0b, and over the bytes you received are all
     equal. Write C0b FROM the committed C0a blob, never from the received text
     a second time, and report the digest and the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R1 and `.agent/context.md`
     at C2 is byte-equal to CONTEXTF021R1 and `.agent/candidates.md` at C4 is
     byte-equal to CANDIDATES1 — each proved with `cmp` at exit 0 against the
     slice extracted from the committed C0a blob, and each paired with a
     NEGATIVE CONTROL comparing that slice against a different one of the three,
     which must exit 1. Report all six exit codes.
 G5  THE CONTRACT PROPERTIES, line-anchored where the anchor is meaningful, at
     the commit that writes each file: in `.agent/plan.md` at C1, `^## Goal$` 1
     and `^## Next Steps$` 1 and `wc -l` at most 50; in `.agent/context.md` at
     C2, `^## Active Branch$` 1 and the substrings `feature/` and `Steps` and
     `pytest` each present and a match for `\bF\d{3}\b` present; in
     `.agent/live_review.md` at C3, the substring `Steps` present.
 G6  THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY, never two
     pytest processes at once, after C5: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf`. Report the exit code
     and the passed-plus-skipped total, and COUNT BY PASSED PLUS SKIPPED because
     data-dependent skips in `tests/ui_server/` move the split run to run.
 G7  THE DOCS GATES, both of them, run serially after C5 because C5 touches
     `docs/roadmap/STATUS.md`: `python3 -m pytest tests/docs/ -q -rf` and
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`.
     Report both exit codes and both totals. The second is ordered because
     `tests/docs/` asserts nothing about a roadmap ledger row's own content,
     which is finding R-0493, and constraint 4(b) is why it appears here.
 G8  CANARY, run serially and after G6 and G7 have finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
 G9  THE C3 REBUILD UNDER TWO INDEPENDENT READERS. Reader (a) is the unit
     classifier of constraint 6. Reader (b) is a line-anchored count over the
     SAME two blobs: `^- R-\d+ — ` entries and `^Done: R-\d+ ` lines at the
     round base, and the same two at C3. Report both readers' numbers at both
     points and state whether they AGREE. Then the NEGATIVE CONTROL: take the
     C3 file, replace one printable byte inside the FIRST carried finding entry
     at equal length, and confirm reader (a) REJECTS that mutant while ACCEPTING
     the true file — the control must probe the head of the region, not its tail
     (R-0631). Run every destructive step of this gate inside a disposable
     worktree under `.remedy-wt/`, never in the primary checkout, and remove it
     before the handback.
 G10 THE LEDGER SETS at C3, line-anchored at line start: `- R-` entries and how
     many are DISTINCT; `Done: R-` lines; `Landed: ` lines; `Gate: R` keys and
     how many are DISTINCT; `Gate: R1` occurrences; and the MAXIMUM registered
     id. Report each as a number. Nothing but `R-0648` may be minted, so the
     maximum id at C3 is `R-0648` and the next free id is `R-0649`.
 G11 THE ROADMAP LEDGER, line-anchored, at the round base then at C5:
     `^- \[~\] ` and `^- \[~\] F021 — ` and `^- \[ \] F021 — ` and `^- \[x\] `.
     Report all four at both points.
 G12 RANGE, executed after C5 because it reads C5: the range from the round base
     to C5 lists exactly the paths of this block's `Change:` list, with the set
     difference EMPTY in both directions, and 0 paths beginning `packages/`,
     `apps/` or `tests/`. Report the two set differences and that count. Then:
     every commit single-parent; `git show --numstat` and `git diff --numstat`
     agreeing cell by cell with the handback's own `## Commits` table (§3
     checklist item 28); every insertion count under the 500 cap; leading
     `<<<SLICE ` and `<<<END ` reading 0 LINES in each of the five files a slice
     lands in; `git ls-files .remedy-wt` reading 0; and this round's reflog rows
     classified with `amend`, `rebase` and `cherry` each 0.
 G13 NO PULL REQUEST IS CREATED AND NONE IS MERGED. Report the output of
     `gh pr list --state open --json number,headRefName` and state that this
     round ran neither `gh pr create` nor `gh pr merge`.
 G14 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4 and C5, the round base SHA, ONE LINE PER GATE with the
     transcripts kept in the round report rather than in the file (R-0582), and
     the block's `Fortschritt:` line verbatim across all three of its lines. Its
     own `wc -l` is reported, and a DECISION D15 line declares any overage with
     the mandated content that caused it.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R1
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps every Part E event kind to a plain line, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers every
Part E kind and an unknown kind renders an honest generic line rather than
vanishing, the feed renders fixture streams per the binding CSS, jump-to-node
focuses the right node, and the steering input renders DISABLED with its honest
tooltip until F030 lands.

## Current Step
R1 is the claim round. It creates the branch, resets the review record carrying
the F009 open set forward, gates F009 R34, registers the one closure candidate
F009 carried, empties the candidates file and claims F021 in the roadmap ledger.
It builds nothing.

## Next Steps
1. R2 the inventory, MEASURED in the source rather than read off the feature
   file: which module owns the F008 SSE subscription and how the client store
   fans it out, where the Part E event-kind list is defined, and what the graph
   already exposes as a focus API.
2. R3 record R2 and rule the feed's shape as a DECISION: the humanize catalog's
   module and its coverage-test contract, the ACTION-class subset the NowCard
   reads, and the disabled-steering flag.
3. R4 onward the built work, in the T001 then T002 then T003 order the feature
   file's Task slicing names.

## Risks
- F021 is a UI feature, so docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority; any visual deviation needs
  an assumption_log entry with a technical reason.
- One SSE subscription with client-side fan-out is an architecture line from the
  feature file's Orchestrator brief: a second EventSource is rejected.
- The open set carried into the review record at C3 holds no code defect of
  F021; R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a
  paydown branch.
<<<END PLANF021R1

<<<SLICE CONTEXTF021R1
# Context — F021 Live activity feed + now-card

## Active Branch
feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge commit
of pull request #210, which the reviewer merged at the Open PR Gate before this
branch existed. Self-drive session per docs/agents/self_drive_protocol.md: the
main session plans and reviews and writes nothing in the work tree, and one
delegated worker per round makes every commit. The branch carries no pull
request; F021 opens one at its closure.

## Scope
In: the humanization catalog that maps every Part E event kind to a plain line
with an honest generic fallback for unknown kinds; the activity feed and its
rows, carrying seq and emitting focus to the graph store on click; the NowCard
over the ACTION-class subset with its recency-driven activity dot; the
scroll discipline that never yanks a reader who has scrolled up; and the
steering input rendered DISABLED with the tooltip its not-yet feature warrants.

Out, per the feature file's Do not touch: steering's backend, which is F030; the
event schema; and graph internals beyond the focus API.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- One SSE subscription feeds both graph and feed, with fan-out in the client
  store. A second EventSource is rejected rather than negotiated — the feature
  file's Orchestrator brief states it as an architecture line.
- docs/ui/design_reference/ is binding for every visual surface and
  assets_spec.md is the asset authority. No new font, icon, glyph style or asset
  source without an assets_spec.md update and an assumption_log entry.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, the second because
  tests/docs/ asserts nothing about a roadmap row's own content (R-0493). A
  round rewriting .agent/ state also gates tests/ui_server/,
  tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Frontend rounds additionally gate
  the apps/ui suite the R2 inventory identifies.
- COUNT BY PASSED-PLUS-SKIPPED. Data-dependent skips in tests/ui_server/ make
  the split vary run to run at an unchanged tree.
- Destructive and red-proof checks run only inside a disposable git worktree
  under .remedy-wt/, so resource safety stays intact and the primary checkout
  satisfies an empty `git status --porcelain` at every verdict. Two pytest
  processes never run at once.
- Repository-wide `ruff check .` is RED at base and is NOT a gate (R-0364); ruff
  is gated scoped to the files a round touches, measured against the SAME files
  at the base. `npm run lint` in apps/ui is likewise red at base and is R-0622.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXTF021R1

<<<SLICE LRHEAD
# Live Review — F021 Live activity feed + now-card

> Round-by-round review record for the F021 branch, reset at the feature claim.
> The F009 record closed with pull request #210, merged into `main` at this
> feature's Open PR Gate. That branch's LAST round, R34, has no gate entry in its
> own record by construction, because a round's verdict is written by the NEXT
> reviewed round (DECISION F085 D9) and R34 was the last round F009 had; its
> entry is therefore the first `Gate:` paragraph below. Finding ids continue the
> monotonic R-XXXX series across the reset.
>
> This header carries NO next-free-id sentence, and its absence is the fix for
> R-0406 rather than an omission: `docs/agents/planner_reviewer_prompt.md` §3
> item 10 already requires every emission to recompute the ceiling mechanically
> from this record. Derive it with `max` over the line-anchored `^- R-\d+ — `
> entries below.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when the
> F009 record closed are reproduced verbatim below, extracted BY ID out of the
> previous record by script and never retyped, never rewrapped and never
> summarised. The pre-reset record held no `Landed:` line, and the three findings
> it had resolved are dropped here with git history as their archive.

## Steps
R1 claim F021 in the roadmap ledger, create the branch, reset this record
carrying the F009 open set forward, gate F009 R34 and register the candidate F009
carried → R2 the feed inventory: which module owns the F008 SSE subscription and
how the client store fans it out, where the Part E event-kind list is defined,
and what the graph exposes as a focus API — each MEASURED in the source rather
than read off the feature file → R3 record R2 and rule the feed's shape as a
DECISION: the humanize catalog's module and coverage-test contract, the
ACTION-class subset and the disabled-steering flag → R4 onward the built work, in
the T001/T002/T003 order the feature file's Task slicing names.

## Findings
<<<END LRHEAD

<<<SLICE R0648
- R-0648 — Medium, THE CLOSURE PRECONDITION THAT IS SUPPOSED TO BLOCK ON OPEN HIGH FINDINGS CANNOT PARSE THIS REPOSITORY'S FINDING LEDGER, SO IT PASSES VACUOUSLY. Raised by the reviewer during the F009 closure review, carried in `.agent/candidates.md` as a closure candidate per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings", and registered here because this is F021's first reviewed round. Measured by the reviewer at `06aeb749`, not inferred: `_check_high_blockers_open` in `packages/orchestration/integrity_gate.py` looks for findings shaped `### R-XXXX:` with `- **Status**:` and `- **Severity**:` lines beneath them, and reports PASS with "no open blocker/high findings" when it matches none, while `.agent/live_review.md` at that commit contains 0 of those headings, 0 `- **Status**:` lines and 0 `- **Severity**:` lines against 213 entries in the form `- R-XXXX — <Severity> — <headline>` that the record actually uses. Two of those entries, R-0495 and R-0574, are High and carry no `Done:` line, so the check answers PASS for a ledger holding exactly what it exists to catch. Medium rather than Low because this is the silently-vacuous-gate class of R-0438 in PRODUCTION code rather than in a reviewer block: a reviewer block is read by a human every round and this parser is not, so nothing else in the pipeline would notice. Nothing about the F009 closure is unsound because of it — the reviewer read the severities directly, found both Highs inherited from the closed features F085 and F086, and recorded PASS_WITH_RISKS on that basis — but closure precondition 3 contributed nothing to that judgement and has contributed nothing to any closure since the ledger took its present form. Counter-measure, NOT applied in this block because F021 must not touch `packages/` before its own inventory round: teach the parser the `- R-XXXX — <Severity> —` form the ledger actually uses, with `Done:` as the resolution marker, and give it a test whose fixture is a ledger in the REAL format holding one open High, so the check goes red where today it is blind. Route it to a paydown branch rather than into F021's change set.
<<<END R0648

<<<SLICE GATE1
Gate: R1 — the F009 R34 entry. R34 PASSED AND F009 IS CLOSED AND MERGED. The reviewer re-executed all fourteen of that round's gates off disk, plus one the block never ordered, and 13 of the 14 reproduce exactly; the one that does not is a false numeral beside a correct check, not a false check. TRANSPORT HELD: `.agent/authored/f009-r34.md` at `744b7c97` and `.agent/last_block.md` at `ac0f0bcc` are both sha256 cc6873fa1a5a3e1215b8f479bf7c08b1787ca7cc2100e4737ef53a7b7b6f1bfc over 26081 bytes and 327 lines, and byte-equal to each other; the reviewer's emitted original no longer exists, so the digest fallback of §4.9 was used and is named here rather than glossed. The reviewer's own extraction out of the committed C0a blob printed 11 slices over 87 CONTENT lines, and constraint 10's numerals re-measure as 327 TOTAL and 240 PROSE, under DECISION F085 D6's 490 and D5's 400. THE APPLIED TEXTS ARE BYTE-EQUAL DISK TO DISK: `.agent/plan.md` at `7a54eb1a` equals PLANF009R34 at sha256 4d7fc193f3102b9602e0b171fdd03afaaf4679219bec54499e4a3078b919eb1b over 36 lines against the 50-line cap, and `.agent/candidates.md` at `c848e17d` equals CANDIDATES34 at sha256 3ce7d0550c4f12e9de830df8811243bedfac67dd2574ca04ce4ecd1fd8bb9e80, each with a negative control that differs. THE APPEND HELD UNDER THE REVIEWER'S OWN TWO READERS: at `6413f223` the round-base blob is a byte-exact PREFIX, the remainder is exactly one newline plus LEDGER34 at sha256 1be2426d44fbdc30e18311e1b6d8104f297850977496bd05b56828de8dcc8ce7 over 5462 bytes and 1 line, the file going 589646 to 595109 bytes and 1146 to 1148 lines, and the last blank-line separated unit equals that slice. THE FOUR PAIRS HELD with the FROM of each occurring exactly once at the round base: the three REWRITES read FROM 0x and TO 1x at `c848e17d`, and the APPEND READMEC reads FROM 1x with each of its three TO-only lines occurring exactly 1x among the 5 lines that commit's diff ADDS to `README.md`, which is the §4.9 reading rather than a whole-file count. THE SETS HELD line-anchored at both points: entries 213 all DISTINCT then 213 all DISTINCT, `Done:` 3 then 3, `Landed: ` 0 then 0, `Gate: R` keys 33 over 33 DISTINCT then 34 over 34 DISTINCT, `Gate: R34` 0 then 1, max registered id R-0647 at both and 210 open at both — nothing was minted. THE CLOSURE VALUES ARE THE REVIEWER'S OWN READING OF THE ARTEFACT AND NOT OF THE HANDBACK: the roadmap row at `c848e17d` moved `^- \[x\] ` from 54 to 55 and `^- \[~\] ` from 1 to 0, and the package it names, `remedy-review-20260822-085607-READY_FOR_REVIEW.zip`, is 72237000 bytes on disk, recomputes to sha256 ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f exactly as the row states, opens to 12906 members, and its in-zip `.review_zip_manifest.json` reads `package_status` READY_FOR_REVIEW, `packaged_evidence_job_id` f009-closure, `base_commit` ce49348b8f5b0374417f5b6c47d8c04966e7108e, `head_commit` 97d028980b5781cbf22a0f651f7e879eea1a0485 equal to the accepted commit the row names, `base_is_ancestor` true, `commit_count` 233, `file_count` 64, `ready_gate_matrix.ok` true with an EMPTY `blocking_reasons`, and `review_subject_evidence_alignment` carrying 0 issues and 0 hash mismatches. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `tests/docs/` exit 0 at 295 passed and `tests/cli/test_golden_path.py` exit 0 at 42 passed. THE RANGE HELD: five commits, every one single-parent, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's table at 327/0, 241/376, 13/14, 2/0 and the four cells of C3, every insertion under the 500 cap, zero leading marker LINES in all five slice targets, `git ls-files .remedy-wt` 0, and the round's reflog rows classified with `amend`, `rebase` and `cherry` each 0. THE HANDBACK IS 177 LINES against the 60-line cap a five-commit round allows, declared in its own DECISION D15 line with the mandated closure content that caused it and no section dropped. TWO DEFECTS ARE RECORDED HERE AGAINST THE OPEN FINDINGS THAT ALREADY HOLD THEM, rather than under new ids, because §3 checklist item 30 requires the open set to be searched for the DEFECT before an id is minted and both searches returned a hit. FIRST, AGAINST R-0585: the R34 block's G12 ordered the range to list "the seven declared paths" while that same block's `Change:` section declared eight — `.agent/authored/f009-r34.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md` and `.agent/handoff.md` — and the handback transcribed the wrong numeral into `.agent/handoff.md` at `c848e17d`. This is exactly the shape R-0585 holds open, a count resolved against a list living elsewhere in the same block rather than against the list it names. The check itself was sound and PASSED under the reviewer's own re-execution: the declared set and the range's set are equal with the difference empty in both directions, both holding 8 members, and 0 of them begin `packages/`, `apps/` or `tests/`. Nothing false reached a verdict, and only the sentence beside the check was wrong. SECOND, AGAINST R-0493: the R34 block's G10 gated `tests/docs/` alone although C3 touched `docs/roadmap/STATUS.md`, and `.agent/context.md` at `06aeb749` states in its own Constraints that a round touching `docs/roadmap/**` also gates `tests/orchestration/test_roadmap_index.py`. The reviewer ran the omitted suite at `c848e17d` and it is GREEN at exit 0 and 30 passed, so the omission hid nothing; the defect is a gate a stated constraint required and the block did not order, which is R-0493's subject reached through the ledger row rather than through a feature file. The counter-measure is APPLIED in the block this entry is committed by, whose gate list runs both suites. THE VERDICT IS PASS: the shipped change is a roadmap row, a README capability sync, a plan, a ledger append and a closure candidate, every one of them verified byte-equal to its authored slice, and both defects above are the reviewer's own block text rather than the worker's execution, which deviated from nothing. F009's pull request #210 was merged at this feature's Open PR Gate as `4548995d` with its branch deleted, its CI check having completed SUCCESS on `c848e17d`, the exact commit the pull request carried.
<<<END GATE1

<<<SLICE CANDIDATES1
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY. The one candidate F009 carried — the closure precondition that cannot
parse this repository's finding ledger — was registered as R-0648 in
`.agent/live_review.md` by the commit before this one, which is F021's first
reviewed round, exactly as the closure protocol requires.
<<<END CANDIDATES1

<<<SLICE CLAIMFROM
- [ ] F021 — Live activity feed + "agent is doing now"
<<<END CLAIMFROM

<<<SLICE CLAIMTO
- [~] F021 — Live activity feed + "agent is doing now"
<<<END CLAIMTO
