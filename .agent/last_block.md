── STEP R3/1 — F008 SSE event stream ─────────────────────────
Goal:        Discharge the findings order the feature file's Orchestrator
             brief dispatches FIRST, and land what it measured. The
             reviewer measured the two preconditions in the source at
             `da2aabf9`; both contradict a prediction the feature file
             carries, so this round records the R2 verdict, registers that
             spec defect as R-0612, amends the feature file with the
             measured state, and rules the consequence as DECISION F008 D1.
             No production code is written this round.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0612 · C3 record the R2 verdict · C4 amend the
             feature file and rule the DECISION · C5 write the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r3.md            (C0a, new file)
             - .agent/last_block.md                  (C0b, full rewrite)
             - .agent/plan.md                        (C1, full rewrite)
             - .agent/live_review.md                 (C2 and C3, appends)
             - docs/roadmap/features/T5_F008.md      (C4, the amendment)
             - .agent/decisions.md                   (C4, append)
             - .agent/handoff.md                     (C5, full rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r3.md, extracted by its marker lines. No slice is
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R3,
    FEATFROM and FEATTO are applied with their trailing newline INCLUDED —
    FEATFROM and FEATTO are whole-line blocks, so including the terminator
    keeps the surrounding paragraph structure intact. FIND0612 and
    RECORDR2 are each applied as `\n` plus their single line, appended to
    the end of `.agent/live_review.md` after exactly one blank line.
    DECISION1 is applied as `\n` plus its body, appended to the end of
    `.agent/decisions.md`, which at `da2aabf9` ends with exactly one
    newline and no trailing blank line. Every file ends with exactly one
    newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5.
    `.agent/plan.md` is advanced at C1, the first substantive commit —
    only the two block-save commits may precede it (checklist item 23).
    R-0612 is registered at C2 BEFORE the verdict lands at C3, which is
    the order §4.4 requires.
 4. Pair shape, from a containment test the reviewer ran before emission.
    FEATFROM/FEATTO: `TO contains FROM: false` — therefore a REWRITE, so
    the obligation is FROM 1x→0x and TO 0x→1x in
    docs/roadmap/features/T5_F008.md, and NO append reading is owed.
 5. The C4 amendment replaces ONLY the nine lines FEATFROM names. The
    heading `## How it fits (inspect current shape before building)`
    immediately above them is NOT part of the pair and stays exactly as it
    is, and neither is line 1 nor line 2 of that file — those two lines
    are what `tests/orchestration/test_roadmap_index.py` parses for the
    title, tier, `Depends on` and `Blocks/used by` fields, and this round
    leaves them untouched.
 6. Destructive checks run only inside a disposable git worktree under
    .remedy-wt/, never in the primary checkout. `git status --porcelain`
    is empty after every commit and at the handback, and
    `git worktree list` names the primary checkout alone at the handback.
 7. Two pytest processes never run at once, and every suite runs in the
    PRIMARY checkout.
 8. No production code. No path under packages/, apps/ or tests/ is
    touched. In particular this round does NOT make the server threaded:
    DECISION F008 D1 rules that change a prerequisite of T001 and gives it
    its own round, because it is production code and needs its own tests.
 9. The reviewer's readings at `da2aabf9`, taken before this block was
    emitted, which the gates below re-derive rather than trust:
    `python3 -m pytest tests/docs/ -q -rf` exits 0 at 295 passed;
    `tests/orchestration/test_roadmap_index.py` exits 0 at 30 passed; the
    state-reader four exit 0 at 160 passed; the canary exits 0 at 42
    passed.

Done when:
 G1  `.agent/STOP` is absent, checked immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback; `git worktree list` names the
     primary checkout alone at the handback. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of
     .remedy-wt/f008-r3.md, of .agent/authored/f008-r3.md at C0a and of
     .agent/last_block.md at C0b, and state whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     .agent/authored/f008-r3.md by their marker lines, take the COUNT from
     that listing, and report per slice its newline-INCLUDED sha256, byte
     count and line count.
 G4  Plan. Report the sha256, byte count and line count of .agent/plan.md
     at C1 and whether it is byte-equal to PLANF008R3. Its line count is
     under 50. `## Goal` and `## Next Steps` each occur exactly once as
     line-anchored headings and `F008` occurs at least once. C1 is the
     first commit after C0a and C0b.
 G5  The two appends, each measured the same two ways, which must agree.
     For C2 against C1, and then for C3 against C2: (a) the earlier blob is
     a byte-exact PREFIX of the later one and the remainder equals `\n`
     plus the slice — report each remainder's sha256, byte count and line
     count; (b) split the later file on blank lines with an INDEPENDENT
     extractor and report that its LAST unit equals that slice. Then run a
     NEGATIVE CONTROL on ONE of them: flip a byte of the remainder in
     memory and report that BOTH readings reject it.
 G6  The sets. Report line-anchored counts in .agent/live_review.md at C1,
     C2 and C3: `^- R-\d+ — ` reads 183, 184, 184; `^Done: R-\d+ — ` is 0
     at all three; `^Landed: ` is 0 at all three; `^Gate: R\d+ — ` reads 2,
     2, 3 — a finding paragraph and a gate paragraph each add exactly one
     line of their own kind and none of the other. The three `Gate: R` keys
     at C3 are DISTINCT. `^- R-0612 — ` occurs 0 times at C1 and exactly 1
     time at C2 and C3.
 G7  The amendment pair. In docs/roadmap/features/T5_F008.md, count
     FEATFROM and FEATTO as exact multi-line blocks at `da2aabf9` and at
     C4: FROM reads 1 then 0, TO reads 0 then 1. Report the containment
     test's own output for the pair. Confirm that line 1 of that file is
     unchanged between the two commits and that the line
     `## How it fits (inspect current shape before building)` occurs
     exactly 1 time at BOTH commits — the reviewer measured 1 at
     `da2aabf9`, so constraint 5 held.
 G8  The DECISION. In .agent/decisions.md, report that the string
     `DECISION F008 D1` occurs 0 times at `da2aabf9` and exactly 1 time at
     C4 as a line-anchored `^## DECISION F008 D1 — ` heading, and that the
     C4 blob is a byte-exact PREFIX-plus-remainder append whose remainder
     equals `\n` plus DECISION1.
 G9  Docs and roadmap gates, in the primary checkout, run SERIALLY. This
     round's change set touches docs/roadmap/features/**, so BOTH commands
     are required — the second by finding R-0493, which measured that
     tests/docs/ asserts nothing whatever about a feature file's BODY and
     that test_roadmap_index.py is the only suite that parses those files:
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
     Report each exit code and each passed count. Both exit 0, at 295 and
     30 respectively — the same totals as at `da2aabf9`, this round adding
     and removing no test.
 G10 Red control for G9's second command, proving it reaches the file this
     round edits. In a disposable worktree created with
     `git worktree add .remedy-wt/redctl-r3 <C4 sha> --detach`, and NEVER
     in the primary checkout: replace line 2 of
     docs/roadmap/features/T5_F008.md — the reviewer measured that line as
     `**Tier 5 · Depends on: F004, F146 · Blocks/used by: every live UI feature**`
     occurring exactly once in that file at `da2aabf9` — with the single
     word `broken`, and report the exit code and last line of
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
     in that worktree. Then restore the line and report that the same
     command exits 0. Remove the worktree with
     `git worktree remove .remedy-wt/redctl-r3 --force`. Report all three
     readings. If the broken run exits 0, the gate does not reach this
     file: STOP and report rather than proceeding on a gate that cannot
     fail.
 G11 State-reader gate and canary, in the primary checkout, SERIALLY and
     never alongside G9:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     Report each exit code and each passed count. Both exit 0.
 G12 The measured facts, re-derived by you rather than read out of this
     block, because a slice that lands in the permanent record may not
     rest on the reviewer's word. Report the real output of each:
     (a) `grep -n 'HTTPServer' packages/orchestration/ui_server.py`
     (b) `grep -rn 'ThreadingMixIn\|ThreadingHTTPServer\|daemon_threads' packages/ apps/`
         — expected to print nothing and exit 1;
     (c) `python3 -c "from dataclasses import fields; from packages.orchestration.event_ledger import LedgerEvent; f=[x.name for x in fields(LedgerEvent)]; print(len(f), f)"`
         run from the repository root, reporting the field count and the
         names. If any reading contradicts what FEATTO or FIND0612 states,
         STOP and report it: the slice is then wrong and must not land.
 G13 Range. With BASE `da2aabf9`, run `git diff --name-only BASE..C5` and
     report that its output equals the Change list above with no path on
     either side alone. Every commit in BASE..C5 has exactly one parent.
     Report each commit's INSERTION count from `git show --numstat`, all
     under 500, and compare those numbers cell by cell against the `+/-`
     column of the handback's `## Commits` table, reporting that the two
     readings agree. C5's own numbers belong to the round report, not to
     its own table cell (finding R-0149).
 G14 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     .agent/plan.md at C1, .agent/live_review.md at C3,
     docs/roadmap/features/T5_F008.md at C4, .agent/decisions.md at C4 and
     .agent/handoff.md at C5. Every count is 0.
 G15 History. Over this round's OWN reflog entries only, report the count
     containing `amend`, `rebase` or `cherry`; it is 0. Do not order that
     every entry read `commit:` (finding R-0601), and do not count an
     unstage as a rewrite (finding R-0608). State NO entry total: this
     round's handback cannot count the entries its own commits create.
 G16 Handback. .agent/handoff.md at C5 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Report its
     line count; the cap for this round is 100, this round having more
     than five commits.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 8 % (F008 beansprucht · R21-, R1- und R2-Urteil im
            Ledger · die Findings-Order aus dem Orchestrator-Brief ist
            gemessen und beantwortet: der UI-Server ist NICHT threaded und
            Ledger-Einträge tragen KEINE seq · DECISION F008 D1 ordnet
            beides · T001 baut noch nicht) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R3
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, for the next free finding id and for the round map; this file
repeats none of them.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat, and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the client transcript byte-equals the
ledger's envelope sequence, the heartbeat holds cadence, and the fallback
engages on a disabled EventSource and recovers to live.

## Current Step
R3 discharges the findings order the feature file's Orchestrator brief
dispatches first. Both preconditions were MEASURED in the source and both
contradict a prediction the feature file carried: the UI server is not threaded,
so a long-lived response would block every other request; and `LedgerEvent`
carries no seq, the enumeration position being consumed into a hash and
discarded. This round registers that spec defect as R-0612, amends the feature
file with the measured state and rules the consequence as DECISION F008 D1.

## Next Steps
1. R4 makes the UI server threaded and proves it behaviourally — a slow
   request must stop blocking a concurrent one — as its own commit with its
   own tests. DECISION F008 D1 makes this a prerequisite of T001, not a part
   of it, because it is production code on a path every cockpit feature uses.
2. R5 builds T001 proper: the stream endpoint, the heartbeat, 404 and 429,
   and the framing golden, with seq read from the ledger position.
3. R6 onward builds T002 and T003 in the feature file's own order.

## Risks
- Making the server threaded touches a path every existing UI feature shares,
  so R4's blast radius is wider than its diff: the state-reader four and the
  dashboard contract are the suites that would show it.
- 184 findings are open once R-0612 lands and none is a code defect of F008.
  Promoting R-0387's clause into the §3 checklist edits `docs/agents/**` and
  stays routed to the paydown branch with R-0403, R-0607, R-0608, R-0609 and
  R-0611.
<<<END PLANF008R3

<<<SLICE FIND0612
- R-0612 — Medium — THE FEATURE FILE PREDICTED TWO PRECONDITIONS AS SETTLED FACT AND BOTH ARE FALSE IN THE SOURCE, SO THE ROUND THAT TRUSTED THEM WOULD HAVE BUILT ON NEITHER. Raised by the reviewer at the R3 findings order, measured in the source at `da2aabf9` rather than read off the feature file, which is what the Orchestrator brief's "dispatch it as a findings order first" exists to force. FIRST PREDICTION, "the stdlib server may need a threading confirmation — a prerequisite finding, not an assumption": the confirmation is that it is NOT threaded. `packages/orchestration/ui_server.py` imports `BaseHTTPRequestHandler, HTTPServer` and instantiates `HTTPServer((host, port), handler_class)` bare, its `handler_class` being a plain `type()` subclass of `_RemedyHandler` with three bound attributes and no mixin, and `grep -rn 'ThreadingMixIn\|ThreadingHTTPServer\|daemon_threads' packages/ apps/` prints nothing at all. `http.server.HTTPServer` resolves through `TCPServer` to `BaseServer` and serves ONE request at a time, so a single open SSE connection would block every other cockpit request for as long as it lived — which is not a degradation but a deadlock of the whole dashboard, and it is why this had to be measured before an endpoint was designed rather than after. SECOND PREDICTION, "verify whether ledger entries already carry an index — they do by construction": they do not. `LedgerEvent` is a frozen dataclass whose fields, read from the dataclass itself and not counted by eye, are exactly the eight `event_id`, `event_type`, `job_id`, `run_id`, `timestamp`, `scope`, `outcome` and `metadata`, and none of them is a seq or an index. `_normalize_event(raw, index)` takes the enumeration position, spends it inside `_make_event_id` on a truncated sha256 of `run_id:index`, and then DISCARDS it, so the surviving identifier is a 16-hex-character digest that is neither ordered nor monotonic; and `list_events` filters by type and timestamp while enumerating, so even the position it walks is not the position of the result. The prediction is half right in the way that matters least: the ledger's ORDER is stable and the position IS real at read time, which is exactly why the fix is cheap — but "already carry an index" describes a field that does not exist, and a round that believed it would have looked for a value to read and found none. WHY MEDIUM AND NOT HIGH: nothing false has reached disk, no code is wrong, and no round has yet built on either prediction — the brief's findings-order dispatch caught both at the first opportunity, which is the outcome it was written for. The cost is that T001 as sliced is not buildable in one round, because making the server threaded is production code on a path every existing UI feature shares and owes its own tests. FIX, landing in the SAME round that registers this finding: the feature file's "How it fits" section is amended to state the measured state in place of the two predictions, and DECISION F008 D1 rules the consequence — the threading change becomes a prerequisite round before T001, and the stream EXPOSES the ledger position as seq rather than assigning one, which is what "the stream must not renumber" was always protecting. This is a spec defect routed to planning per §4 item 7, not a defect in any round's work, and no round is asked to redo anything.
<<<END FIND0612

<<<SLICE RECORDR2
Gate: R3 — the R2 entry. R2 PASSED with NO finding against its work and none against its block, and it repaired the red R1 was forbidden to touch. THE REPAIR IS REAL AND STRICTLY STRONGER THAN WHAT IT RETIRED, which is the one thing a repair of this shape must prove, because a pin that is merely different is a weakening wearing a fix's clothes. The reviewer re-ran the control ITSELF in a disposable worktree at `da2aabf9`, never in the primary checkout: with F008 returned to `- [ ] ` the suite exits 1 at 1 failed and 294 passed; with a SECOND `[~]` injected on the F009 line it exits 1 again at 1 failed and 294 passed; restored, it exits 0 at 295 passed. The retired sentence could only ever have caught the first of those two, so the count of states the ledger is pinned against went UP, and `python3 -m pytest tests/docs/ -q -rf` is now exit 0 at 295 passed — the same 295 the base reported as 1 failed plus 294 passed, so exactly one test was repaired and none was added, removed or renamed. THE PAIR APPLIED CLEANLY AND TOUCHED NOTHING ELSE: PINFROM reads 1 then 0 and PINTO 0 then 1 as exact multi-line blocks between `05894327` and `84da10ae`, the containment test printing `TO contains FROM: false` so no append reading was owed, and the `assert re.search(r"^- \[x\] F017 —", text, re.M)` line that follows the pair reads 2 at BOTH commits — the second occurrence living at line 281 in a different test method, which is why the block ordered 2 rather than the 1 an eye would have written. THE ROUND'S OWN SHAPE HOLDS, re-measured off disk: transport byte-equal three ways at sha256 fa4f38925f90290d115538484265cf1473848c7b9e3907c917e9ca7a859c2b6e over 21496 B and 246 lines, equal to the digest stated at delegation; FOUR slices, a count from the reviewer's own ordered extraction — PLANF008R2 6fc59970, PINFROM 0c5f8c52, PINTO 986c4293 and RECORDR1 d51c3a45; `.agent/plan.md` at `c0b3659e` byte-equal to PLANF008R2 over 2611 B and 45 lines, under the 50-line cap and first after the two block-save commits; the verdict append at `8cdfce8b` a byte-exact prefix-plus-remainder of 6388 B equal to a newline plus RECORDR1, agreed by an INDEPENDENT 189-unit blank-line split whose last unit is that same paragraph, with a one-byte flip rejected by both readings; sets 183 registered, 0 resolved and 0 `Landed:` at both ends, `Gate: R` moving 1 to 2 with distinct keys, and `R-0612` reading 1 at both commits as the header's own `Next free id:` line with zero `^- R-0612 — ` entries — the block having ordered that reading rather than the 0 a careless zero-gate would have demanded. SIX single-parent commits over exactly the six declared paths with no path on either side alone, insertions 246, 184, 18, 2, 9 and 46, all under the 500 cap; zero marker lines in any target; `ruff check` clean on the edited test at the round tip; the state-reader four exit 0 at 160 passed and the canary at 42 passed, run serially in the primary checkout; a 94-line handback under its cap carrying every mandated section and an item table naming C0a through C4 exactly once; the tree clean and `git worktree list` naming the primary checkout alone. NO DEVIATION WAS DECLARED AND NONE WAS OWED. WHAT R1 AND R2 TOGETHER SETTLE is worth recording once: R1's red was the reviewer's own defect, a recurrence of R-0387 rather than a new id, and the whole episode — a red round, a finding attributed to the block that caused it, and a repair proved in both directions — cost one round. That is the same shape and the same price as the F255 R19 episode, and it is the price this workflow is designed to pay instead of the alternative, which is a green word over an unproven change.
<<<END RECORDR2

<<<SLICE FEATFROM
Events exist as the file-based ledger with stable ordering — the
stream is a READER: tail the job's events from a cursor, assign/
carry monotonic seq (verify whether ledger entries already carry an
index — they do by construction; the stream must not renumber),
serve via the existing UI server process (inspect how the current
server handles long-lived responses; the stdlib server may need a
threading confirmation — a prerequisite finding, not an assumption).
The envelope follows the roadmap's Part E event contract — cite it,
don't restate it.
<<<END FEATFROM

<<<SLICE FEATTO
Events exist as the file-based ledger with stable ordering — the
stream is a READER: tail the job's events from a cursor and carry a
monotonic seq without renumbering, served by the existing UI server
process. The envelope follows the roadmap's Part E event contract —
cite it, don't restate it.

MEASURED AT R3 in the source at `da2aabf9`, replacing two predictions
this section carried as settled fact. Both were false; see finding
R-0612 and DECISION F008 D1.

- The UI server is NOT threaded. `packages/orchestration/ui_server.py`
  instantiates `HTTPServer` bare, and no `ThreadingMixIn`,
  `ThreadingHTTPServer` or `daemon_threads` occurs anywhere under
  `packages/` or `apps/`. `http.server.HTTPServer` resolves through
  `TCPServer` and serves one request at a time, so one open SSE
  connection would block every other cockpit request for as long as it
  lived. Making the server threaded is a PREREQUISITE of T001 and gets
  its own round, being production code on a shared path.
- Ledger entries do NOT carry an index. `LedgerEvent` has exactly eight
  fields — `event_id`, `event_type`, `job_id`, `run_id`, `timestamp`,
  `scope`, `outcome`, `metadata` — and none is a seq.
  `_normalize_event(raw, index)` spends the enumeration position inside
  `_make_event_id`, a truncated sha256 of `run_id:index`, and discards
  it. The ORDER is stable and the position is real at read time, so
  T001 EXPOSES that position as the seq rather than assigning one —
  which is what "must not renumber" was always protecting.
<<<END FEATTO

<<<SLICE DECISION1
## DECISION F008 D1 — the server becomes threaded in its own round before T001, and seq is the ledger position (2026-08-21)

CONTEXT. The feature file's Orchestrator brief dispatches T001's
server-capability question as a findings order before anything is built, and
R3 discharged it by measuring the source at `da2aabf9` rather than reading the
feature file's own prediction. Both predictions were false, and finding R-0612
records the measurement: `packages/orchestration/ui_server.py` instantiates
`http.server.HTTPServer` bare with no threading mixin anywhere under
`packages/` or `apps/`, so it serves one request at a time; and `LedgerEvent`
carries none of a seq, an index or any ordered field, its enumeration position
being spent inside `_make_event_id` and discarded. T001 as sliced assumed the
opposite of both.

CHOSEN. Two rulings, one for each measurement.

1. Making the UI server threaded is a PREREQUISITE ROUND before T001, not a
   step inside it. It is production code on the single path every existing
   cockpit feature already uses, so it carries its own commit, its own
   behavioural test — a slow request must stop blocking a concurrent one, an
   assertion that fails today — and its own gate over the state-reader four
   and the dashboard contract, which are the suites that would show a
   regression there.
2. The stream EXPOSES the ledger's own position as `seq` and assigns nothing.
   T001 adds the position to the read path rather than minting a parallel
   counter, so "the stream must not renumber" is satisfied by construction
   instead of by discipline, and `event_id` keeps its present meaning as an
   opaque digest rather than being pressed into service as an ordinal.

ALTERNATIVES CONSIDERED and rejected. Folding the threading change into T001 —
rejected because a blocking-server fix and a new endpoint would land in one
diff, and a regression in either could not be attributed to the right half.
Serving the stream from a second, separate threaded server on its own port —
rejected because it doubles the auth surface the token model has to cover and
splits the cockpit across two origins for no gain the first option does not
give. Persisting a new `seq` field onto every ledger event — rejected because
it rewrites the ledger format, which this feature's Do-not-touch section
excludes by name, and because the position it would persist is the one already
available for free. Deriving order from `timestamp` — rejected because
timestamps are strings of unspecified resolution here and two events can share
one, which is precisely the gap-detection failure T002 must prove absent.

CONSEQUENCE. T001 is preceded by one prerequisite round, so the feature is one
round longer than its Task slicing implies; the feature file's "How it fits"
section now states measured facts where it stated predictions; and the
Do-not-touch line on the ledger format is preserved rather than negotiated.

Reverse this decision by deleting this section, restoring the two predictions
in `docs/roadmap/features/T5_F008.md` and resolving R-0612 as rejected.
<<<END DECISION1
