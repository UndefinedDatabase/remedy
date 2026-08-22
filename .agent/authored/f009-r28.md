── STEP T003 (the route-walking 405 proof — T003 closes) — F009 ──
Goal:        Prove the 405 discipline by WALKING the routes the server really
             serves rather than a list someone wrote down. The job endpoints are
             derived from `do_GET`'s own dict literal by AST, so a new one joins
             the walk for free, and a drift test fails the moment a literal route
             appears that the walk does not know. This is the last piece of
             T003. The round also registers R-0643 against the reviewer's own
             R27 block, records the R27 verdict, and rules DECISION F009 D25.

Fortschritt: ~98 % (T001 gebaut · T002 gebaut · T003 gebaut: beide Kommandos
             dispatchen, melden sich auf dem SSE-Strom, sind import-seitig
             eingezäunt und jede andere mutierende Route ist begangen und
             beweisbar 405; offen bleiben nur Integrations-Gate und Closure) —
             Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0643 ·
             C3 the R27 verdict · C4 DECISION F009 D25 · C5 the route walk · C6
             handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r28.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2 and
             C3) · `.agent/decisions.md` (C4) ·
             `tests/ui_server/test_command_channel.py` (C5) ·
             `.agent/handoff.md` (C6). NOTHING under `packages/`, `apps/` or
             `docs/` is touched: the 405 behaviour already exists and this round
             proves it, changing no production line.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes both ledger commits because the plan must be current before them
    (checklist item 23). C2 precedes C3 because a finding persists in its OWN
    commit BEFORE anything else in the round (§4.4, clause a).
 3. THIS ROUND MINTS R-0643 AND RESOLVES NOTHING. It writes no `Done:` line and
    no `Landed:` line. The next free id is R-0644 when the round ends. R-0643
    was minted only after the reviewer searched the OPEN set for the DEFECT
    rather than for an id (checklist item 30); FINDING643 states inside itself
    which OPEN finding is its nearest neighbour and why that one's clause does
    not reach it.
 4. PAIR SHAPE, printed by the reviewer's own containment test on the exact
    bytes below:
      WALK  — `TO contains FROM: true`  → APPEND-shaped, §4.9 code obligation.
    Its FROM occurs EXACTLY 1 time in `tests/ui_server/test_command_channel.py`
    at the round base, which the reviewer counted on the base bytes whole-line
    and indent-agnostic with both agreeing. The obligation is ORDERED EQUALITY
    per §4.9 as R-0531 narrowed it, NEVER a per-line count and NEVER a
    FROM-zero count: the slice is CODE and repeats lines structurally.
 5. THREE APPENDS, each based on a DIFFERENT commit, and the difference is the
    point. FINDING643 appends to `.agent/live_review.md` at C2 based on the
    ROUND BASE. LEDGER28 appends to `.agent/live_review.md` at C3 based on
    **C2**, not on the round base, because C2 already grew that file — a gate
    that reads C3 against the round base measures two slices and reports one
    (R-0368's class). DECISION25 appends to `.agent/decisions.md` at C4 based on
    the round base. Each target ends in exactly ONE newline at the commit its
    own append is based on; the reviewer measured that on the bytes for the two
    the round base fixes, and the worker measures it for the third at C2. So
    each append is one newline followed by its slice.
 6. FINDING643 and LEDGER28 each carry ONE paragraph. DECISION25 carries more
    than one; count them with your script rather than from this sentence.
 7. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FIVE of its lines.
    Five is the reviewer's own count of this block's bytes, and it is five
    rather than the usual four because T003 closing needed the extra clause.
 8. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5: this block is 431 lines TOTAL against
    DECISION F085 D6's 490 cap, 242 of them PROSE against D5's 400. Re-measure
    both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C6: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3, C4 and C5. Report the round base
     SHA you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r28.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 8's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R28 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, under TWO independent readers, each with a negative control on the
     FIRST appended paragraph (finding R-0631). Run this THREE times, and for
     each state which commit you based it on, exactly as constraint 5 fixes:
     FINDING643 at C2 based on the round base; LEDGER28 at C3 based on **C2**;
     DECISION25 at C4 based on the round base. For each: (a) the base blob is a
     byte-exact PREFIX and the remainder equals a newline plus that slice —
     report its sha256, bytes and lines; (b) N is counted BY YOUR SCRIPT and the
     last N blank-line units equal the slice's N paragraphs IN ORDER. Then flip
     one printable byte in the FIRST appended paragraph, at equal length, and
     report that BOTH readers REJECT the flip while both ACCEPT the true file.
     Report before/after bytes and lines for each of the three.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base,
     at C2 and at C3 (finding R-0630): a leading `- R-` id with every captured
     id DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a
     leading `Gate: R` key over that many DISTINCT keys; the `Gate: R28` key;
     and a leading `- R-0643` entry. The reviewer's base readings, which yours
     must reproduce: entries 208, `Done:` 3, `Landed: ` 0, `Gate: R` keys 27,
     `Gate: R28` 0, `- R-0643` 0. Report the max REGISTERED id and the open
     count by DECISION F009 D10's rule at all three points. Read every one of
     these at line START and not as a bare substring: this file legitimately
     QUOTES ids and gate keys inside its own verdict prose, so an unanchored
     scan reports a maximum that was never registered (finding R-0630).
 G7  PAIR. For the WALK pair report, on whole lines and again
     indent-agnostically, with the two readings required to AGREE: the FROM
     count in `tests/ui_server/test_command_channel.py` at the round base and
     at C5, and the TO count at both. The reviewer's base readings, which yours
     must reproduce: FROM 1, TO 0. Read the BASE side with
     `git show <base>:<path>` into a variable or into scratch under
     `.remedy-wt/` — never by writing the base blob over the tracked file,
     which guardrail G5 forbids (finding R-0594). Report the containment
     reading your OWN script printed — the words `TO contains FROM: true` — and
     order NO FROM-zero count for it (finding R-0522).
 G8  ORDERED EQUALITY for C5, which is §4.9's obligation for a code append as
     R-0531 narrowed it: the lines C5's diff ADDS are exactly the applied
     slice's lines IN ORDER, compared as a list, plus `git show --numstat` for
     it. The reviewer measured 135 insertions and 0 deletions by applying this
     block's OWN slice to the base blob; report the numbers YOU measure and flag
     any difference rather than
     reconciling it.
 G9  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree (finding R-0518). Report each command's REAL
     exit code and the count IT printed — predict no number:
       `python3 -m ruff check tests/ui_server/test_command_channel.py`
       `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The canary is unconditional; the four-path group is owed because this
     round's change set holds `.agent/` state files and a `tests/ui_server/`
     module (finding R-0607). The reviewer ran all four at the round base before
     ordering them: each exits 0, so each can fail honestly (R-0364).
 G10 RED PROOF, in a DISPOSABLE worktree under `.remedy-wt/` at C5 and NEVER in
     the primary checkout (§4.10, guardrail G5). EVERY expected set below is
     measured under ONE named selection, and that selection is the WHOLE FILE:
     `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`, with no
     `-k` and no node id. Naming the selection is finding R-0643's own rule,
     applied in the round that registers it — an expected-failure set is a
     property of a selection, and a set stated without one is unreachable at
     some other scope the worker may reasonably pick. Three mutations of
     `packages/orchestration/ui_server.py`, each REVERTED and the file confirmed
     byte-equal to its C5 blob before the next. Each FROM below occurs EXACTLY 1
     time in that file at C5, counted by the reviewer whole-line and
     indent-agnostic with both agreeing, and each replacement is quoted at the
     indentation of the site it lands in (R-0642's rule). Mutation (a)'s FROM
     spans TWO lines for that reason and not by accident: its second line alone
     occurs 3 times in that file — `do_POST`, `do_PUT` and `do_DELETE` all
     refuse with the same bytes — so the `def` line above it is what makes the
     target unique, and a one-line FROM there would be R-0629's defect exactly
     (checklist item 25). The reviewer counted all three FROMs on the base bytes.
     (a) REPLACE these two lines
           `    def do_PUT(self) -> None:  # noqa: N802`
           `        self._send_json(*_safe_error(405, "method not allowed"))`
         with these two
           `    def do_PUT(self) -> None:  # noqa: N802`
           `        self._send_json(200, {"ok": True})`
         EXPECT exactly the ids listed here to fail:
         `test_an_unknown_path_is_405_for_every_mutating_method`,
         `test_every_route_the_server_serves_refuses_post_put_and_delete` and
         `test_put_is_405_even_on_the_commands_path`.
     (b) instead REPLACE, in `do_POST`, the two-line condition
           `        if (len(parts) == 5 and parts[1] == "api" and parts[2] == "jobs"`
           `                and parts[4] == "commands"):`
         with
           `        if (len(parts) >= 5 and parts[1] == "api" and parts[2] == "jobs"`
           `                and parts[4].startswith("command")):`
         EXPECT exactly the id named here to fail:
         `test_a_near_miss_of_the_commands_path_is_405`.
     (c) instead INSERT, directly ABOVE the line
           `        if path == "/api/layers":`
         these three lines, at the indentation shown:
           `        if path == "/api/newthing":`
           `            self._send_json(200, {})`
           `            return`
         EXPECT exactly the id named here to fail:
         `test_the_walk_knows_every_route_the_source_dispatches`.
     Mutation (c) is the one that matters most: it proves the walk cannot
     silently stop covering the server, which is how a route-walking test
     usually dies. Report the ids that actually failed and flag any difference
     from the three sets above rather than reconciling it. Remove the worktree
     and report `git worktree list` at 1 line before C6.
 G11 RANGE: the range from the round base to C5 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/` or `docs/`, which is
     this round's no-production-code constraint as a measurement. Each commit
     has ONE parent; `git show --numstat` and `git diff --numstat` AGREE on
     every cell — invoke `git show` WITHOUT a `--` before the SHA, which turns
     it into a pathspec and prints nothing; every cell equals the `+/-` column
     of the handback's `## Commits` table (checklist item 28), compared cell by
     cell. Report each pre-handback commit's insertions against the 500 cap of
     AGENTS.md DECISION F104 D1; the handback commit's own numbers belong in the
     round report (item 14). Leading `<<<SLICE ` and `<<<END ` read 0 LINES in
     every file a slice lands in, which are `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md` and
     `tests/ui_server/test_command_channel.py`. `git ls-files .remedy-wt` reads
     0. Classify THIS ROUND's reflog rows by the operation before the first `:`
     and report `amend`, `rebase` and `cherry` each 0; assert no total over the
     whole reflog (R-0601).
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4, C5 and C6, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all five of its lines. Report
     its `wc -l` against the 100-line cap AGENTS.md allows for a per-commit
     table of more than five commits, which the commit sequence constraint 2
     fixes is. EVERY numeral this file states about the round's own measurements
     is COUNTED mechanically before it is written, or no numeral is stated and
     the enumeration speaks (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C6.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R28
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R28 closes T003 and records the R27 verdict. Every route `do_GET` dispatches is
walked with POST, PUT and DELETE and answers 405; the job endpoints come out of
`do_GET`'s own dict literal by AST so a new one joins the walk automatically, and
a drift test fails the moment a literal route appears the walk does not know.
With T001, T002 and T003 built, what remains is verification rather than
construction.

## Next Steps
1. The integration gate per docs/agents/integration_gate.md — the full suite,
   once, before closure.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the authored STATUS line, and the pull request.

## Risks
- Closure needs TWO rounds, not one: the evidence-and-zip round produces the
  values the STATUS line quotes, and a separate round commits that line. Ending
  right after a verdict strands it (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R28

<<<SLICE FINDING643
- R-0643 — Low — A REVIEWER GATE ORDERED AN EXPECTED-FAILURE SET WITHOUT NAMING THE SELECTION IT IS MEASURED OVER, AND THE SET IS TRUE AT ONE SCOPE AND FALSE AT THE OTHER. The defect is the reviewer's, in the F009 R27 block saved at `f8bf6c7f`, and it was FOUND AND DECLARED BY THE WORKER as that round's first deviation. G10 ordered three mutations and after each wrote "EXPECT exactly the ids listed here to fail", naming two ids per mutation, while the block named no pytest selection anywhere in that gate — no node id, no `-k`, no command line. At the guard class `TestCommandDoorImportGuard` all three ordered sets reproduce EXACTLY; at the whole file each mutation additionally reddens 21 or 22 unrelated HTTP tests, because all three mutate methods that sit on the live dispatch path, so at that scope "exactly the ids listed" is false of every one of them. The worker ran BOTH scopes, reported both, and said which one makes the order reachable — the reviewer reproduced all six readings independently at the landed head and confirms every ordered set is a subset of its whole-file reds. WHY R-0393 DOES NOT REACH THIS, stated because it is the nearest OPEN neighbour and checklist item 30 requires the open set to be searched for the DEFECT before an id is minted. R-0393 governs a HANDBACK's transcript that measures its green run and its mutated run at DIFFERENT `-k` selections, and its fix clause is that "a red-proof states ONE selection string and uses it for the green run and every mutated run, or it declares the change of scope in the same sentence as the numbers". The R27 worker OBEYED that clause: it used one selection per reading, reported both, and declared the scope beside the numbers. The gap is one step upstream, in the ORDER rather than in the report — a block that states an expected set while leaving the selection to the worker has not stated a measurable property at all, because an expected-failure set is a property OF a selection and means nothing without one. Low, because the worker resolved it correctly and nothing false reached disk. Standing rule from here: a gate that orders an expected-failure set names, in the same gate, the exact command the set is measured under — and where the reviewer measured the set at a narrower scope than the suite command the same block orders elsewhere, it says so rather than leaving the two to be reconciled. The R28 block's own G10 is the first such gate written under this rule, and it names the whole file. OPEN.
<<<END FINDING643

<<<SLICE LEDGER28
Gate: R28 — the R27 entry. R27 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced; the round's one substantive deviation is the reviewer's own block defect, registered above as R-0643 and not counted against the round. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r27.md` at `f8bf6c7f`, `.agent/last_block.md` at `80df4d3a` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r27.md`, are all sha256 69e3b24fd4ba79b881c22ef4d50994df1b5be4fec8d38c79d50fd66bc4a3c2b8 over 35935 bytes and 438 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 6 slices over 212 CONTENT lines, and constraint 8's numerals re-measure as 438 TOTAL and 226 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `b40e79a4` is BYTE-EQUAL to that round's PLANF009R27 slice, 37 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1 and a negative control against another file differing. THE APPLICATION IS PROVED IN THE STRONGEST FORM AVAILABLE, which is stronger than the gate the block ordered: the reviewer applied the COMMITTED GUARD slice to the COMMITTED base blob with its own script and the result is BYTE-IDENTICAL to `tests/ui_server/test_command_channel.py` at `ced6e1eb`, so no line of it was hand-edited, reflowed or reconciled anywhere in the round; base FROM reads 1 and TO reads 0, the containment reading printed `true`, and no FROM-zero count was ordered for an append-shaped pair. ALL THREE APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS, AND THE ONE THAT MATTERS MOST IS THE SECOND: FINDING642 at `56926662` is based on the round base, 536117 to 538649 bytes and 1120 to 1122 lines, N counted at 1 BY THE SCRIPT; LEDGER27 at `3ee65a8b` is based on **C2** rather than on the round base, exactly as constraint 5 fixed, its base blob reading 538649 bytes and 1122 lines — the reading a round-base comparison would have got wrong by one whole slice — going to 544465 bytes and 1124 lines, N counted at 1; DECISION24 at `e2b6fb96` is based on the round base, 477421 to 480292 bytes and 6925 to 6939 lines, N counted at 7 BY THE SCRIPT. In all three an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start across all THREE points: at the round base entries 207, `Done:` 3, `Landed: ` 0, `Gate: R` keys 26, `Gate: R27` 0 and a leading `- R-0642` entry 0, max REGISTERED id R-0641, 204 open; at C2 entries 208 all DISTINCT with `- R-0642` at 1, max id R-0642 and 205 open; at C3 the `Gate: R` keys reach 27 over 27 DISTINCT keys with `Gate: R27` at 1. The ledger header was compared against the series it joins and `Gate: R27 — the R26 entry.` matches it. THE SUITES ARE THE REVIEWER'S OWN, re-run serially in the primary checkout: ruff over the changed path EXITS 0, `test_command_channel.py` EXITS 0 at 95 passed, the canary EXITS 0 at 42 passed, and the four-path state-reader group EXITS 0 at 522 passed — the 517 of R26 grown by exactly the five tests this round adds, and not one of the five predicted by the handback. THE RED PROOF IS THE REVIEWER'S OWN, re-run at the LANDED head in a disposable worktree at BOTH scopes rather than accepted from the report: the anchor line reads 1 whole-line and 1 indent-agnostic with both agreeing at eight leading spaces, and at the guard class all three ordered sets reproduce EXACTLY — a forbidden applicator import reddens the equality test and the forbidden-module test, a second name out of storage reddens the equality test and the storage test, and a renamed door method reddens `test_every_named_method_exists` with the equality test. THAT THIRD MUTATION IS THE ONE WORTH RECORDING: it proves the guard cannot silently empty its own scan, which is how a guard of this shape usually dies, and it is the reason the vacuity test was written rather than assumed. THE RANGE HELD: the range base→`a164317b` lists exactly the declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/` or `docs/`, which is that round's no-production-code constraint as a measurement; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 438/0, 349/362, 9/9, 2/0, 2/0, 14/0 and 158/0; pre-handback insertions 438, 349, 9, 2, 2, 14 and 158, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all four slice targets; `git ls-files .remedy-wt` 0; the reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict. THE HANDBACK IS 99 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits, so R-0582's repair has now held for two rounds running.
<<<END LEDGER28

<<<SLICE DECISION25
## DECISION F009 D25 — the 405 proof is a WALK over derived routes, not a list (2026-08-22)

Measured by the reviewer at `a164317b`, before this round was delegated, by reading `do_GET` end to end rather than by grepping it: the server dispatches four routes by a bare `path ==` or prefix comparison, thirteen job endpoints out of a single `handlers` dict literal, and six more STRUCTURALLY, by splitting `path` on "/" and comparing the parts — `events-since`, the SSE stream at `events/stream`, and three `nodes/<node>/…detail` routes. An AST scan for `path ==` literals alone therefore finds four of twenty-three, which is the trap this decision exists to avoid: such a scan reports a confident, small, WRONG inventory and a walk built on it would prove almost nothing while looking rigorous.

FIRST, WHERE THE WALK'S ROUTE LIST COMES FROM. CHOSEN: derive what can be derived, spell out the rest, and gate the boundary. The thirteen job endpoints are read out of the `handlers` dict literal by AST, so adding an endpoint puts it in the walk with no test edit at all; the four literal routes are read the same way and compared for EQUALITY against a named set; the six structural routes are written out, because nothing exists to derive them from. ALTERNATIVES: (a) a fully hand-written list — rejected, it proves the list rather than the server and goes stale silently. (b) a fully derived list — rejected as impossible, since a structural match has no literal to extract, and pretending otherwise is how the four-of-twenty-three inventory gets shipped.

SECOND, THE DRIFT TEST. CHOSEN: the derived literal set must EQUAL the named set, and every derived endpoint must appear among the walked paths. A route added as a new `path ==` comparison then fails the equality immediately, and a route added to the dict is walked automatically rather than being missed. The remaining hole is a new STRUCTURAL route, which neither half can see; it is named here as the known limit rather than papered over, and the sentence a reader will search for is in the class docstring.

THIRD, WHAT THE WALK ASSERTS. CHOSEN: for every walked path, POST, PUT and DELETE each answer 405 AND carry the body `{"error": "method not allowed"}`, plus a count assertion that the walk ran the number of requests it claims. A status-only walk passes against a server that answers 405 by accident from a different code path, and a walk that silently iterates an empty list is the vacuous case this repository keeps paying for.

FOURTH, THE OTHER HALF OF THE CLAIM. CHOSEN: the same class asserts that the commands path DOES answer 200, that an unknown path is 405 rather than 404 for a mutating verb, and that four near misses of the commands path — a trailing segment, a singular spelling, a missing job id and a case change — are all 405. "Every OTHER route is 405" is only meaningful beside a demonstration that this one is not, and the near misses are where a fail-open would actually arrive.

REVERSE the first by hand-writing the list, which reintroduces exactly the staleness the derivation removes; the second by deleting the drift test, which is also how to make the walk stop covering the server, so the two are deliberately the same act; the third by dropping to a status-only assertion; the fourth by removing the near-miss cases, which is the only part of this a later round might reasonably move into its own module.
<<<END DECISION25

<<<SLICE WALK_FROM
    # -- B: the GET door still behaves as it did ----------------------------
<<<END WALK_FROM

<<<SLICE WALK_TO
    # -- F: the route walk, F009's 405 discipline ---------------------------

    #: Routes `do_GET` dispatches with a bare `path ==` comparison.
    LITERAL_GET_ROUTES = frozenset({"/", "/api/state", "/api/layers"})

    @staticmethod
    def _do_get_route_facts():
        """The route literals and endpoint keys `do_GET` carries, read by AST.

        Derived rather than transcribed: a walk over a hand-written list proves
        that list, not the server. The thirteen job endpoints live in a dict
        literal inside `do_GET`, so adding one puts it in the walk for free.

        The known limit, written where a reader will search for it: a route
        matched STRUCTURALLY — by splitting `path` and comparing parts, as
        `events-since`, `events/stream` and the three `nodes/…detail` routes are
        — has no literal to extract, so it is spelled out in `_walkable_paths`
        and a NEW one of that kind is the one case neither half of the drift
        test can see.
        """
        import ast
        from pathlib import Path

        from packages.orchestration import ui_server

        tree = ast.parse(Path(ui_server.__file__).read_text(encoding="utf-8"))
        do_get = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "_RemedyHandler":
                for member in node.body:
                    if (isinstance(member, ast.FunctionDef)
                            and member.name == "do_GET"):
                        do_get = member
        assert do_get is not None, "do_GET not found"

        literals, endpoints = set(), set()
        for sub in ast.walk(do_get):
            if (isinstance(sub, ast.Compare) and isinstance(sub.left, ast.Name)
                    and sub.left.id == "path"):
                for op, comp in zip(sub.ops, sub.comparators):
                    if (isinstance(op, ast.Eq) and isinstance(comp, ast.Constant)
                            and isinstance(comp.value, str)):
                        literals.add(comp.value)
            if isinstance(sub, ast.Dict) and sub.keys:
                keys = [k.value for k in sub.keys
                        if isinstance(k, ast.Constant) and isinstance(k.value, str)]
                if len(keys) == len(sub.keys):
                    endpoints |= set(keys)
        return literals, endpoints

    def _walkable_paths(self):
        """Every concrete GET path this job exposes, ready to be POSTed at.

        The structural routes are spelled out here for the reason the docstring
        above gives: there is no literal to derive them from.
        """
        _, endpoints = self._do_get_route_facts()
        paths = ["/", "/api/state", "/api/layers", "/assets/index.js"]
        paths += [f"/api/jobs/{self.job_id}/{name}" for name in sorted(endpoints)]
        paths += [
            f"/api/jobs/{self.job_id}/events-since",
            f"/api/jobs/{self.job_id}/events/stream",
            f"/api/jobs/{self.job_id}/nodes/node-1/detail",
            f"/api/jobs/{self.job_id}/nodes/node-1/human-detail",
            f"/api/jobs/{self.job_id}/nodes/node-1/debug-detail",
        ]
        return paths

    def test_the_walk_knows_every_route_the_source_dispatches(self):
        """The drift detector. A new literal route the walk misses fails HERE.

        Without it the walk silently shrinks to whatever it was written for and
        a route added later is never walked — the way a guard of this shape
        usually stops guarding.
        """
        literals, endpoints = self._do_get_route_facts()
        assert literals == set(self.LITERAL_GET_ROUTES), {
            "unwalked": sorted(literals - set(self.LITERAL_GET_ROUTES)),
            "vanished": sorted(set(self.LITERAL_GET_ROUTES) - literals),
        }
        walked = set(self._walkable_paths())
        missing = sorted(name for name in endpoints
                         if f"/api/jobs/{self.job_id}/{name}" not in walked)
        assert missing == [], missing
        assert endpoints, "the endpoint dict came back empty, so the walk is vacuous"

    def test_every_route_the_server_serves_refuses_post_put_and_delete(self):
        """The walk itself: one real request per route per mutating method."""
        port, token = self._start_server()
        seen = []
        for path in self._walkable_paths():
            for method in ("POST", "PUT", "DELETE"):
                status, body = self._request(
                    port, method, f"{path}?token={token}",
                    body=self._valid_body(),
                    headers=self._auth_headers(token))
                seen.append((method, path, status, body.get("error")))
        wrong = [row for row in seen if row[2] != 405]
        assert wrong == [], wrong
        assert {row[3] for row in seen} == {"method not allowed"}, seen
        # A walk is only worth the name if it walked what it says it walked.
        assert len(seen) == len(self._walkable_paths()) * 3

    def test_the_commands_path_is_the_only_post_that_is_not_405(self):
        """The other half: the one door really is open, so 405 above means 405."""
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce="nonce-405-walk"),
            headers=self._auth_headers(token))
        assert status == 200, body
        assert body["outcome"] == "accepted", body

    def test_an_unknown_path_is_405_for_every_mutating_method(self):
        """404 belongs to GET; a mutating verb never gets that far."""
        port, token = self._start_server()
        for method in ("POST", "PUT", "DELETE"):
            status, body = self._request(
                port, method, f"/api/nothing/here?token={token}",
                body=self._valid_body(),
                headers=self._auth_headers(token))
            assert status == 405, (method, status, body)

    def test_a_near_miss_of_the_commands_path_is_405(self):
        """Fail closed: only an UNAMBIGUOUS commands path opens the door."""
        port, token = self._start_server()
        for path in (f"/api/jobs/{self.job_id}/commands/extra",
                     f"/api/jobs/{self.job_id}/command",
                     "/api/jobs/commands",
                     f"/api/JOBS/{self.job_id}/commands"):
            status, body = self._request(
                port, "POST", path, body=self._valid_body(),
                headers=self._auth_headers(token))
            assert status == 405, (path, status, body)

    # -- B: the GET door still behaves as it did ----------------------------
<<<END WALK_TO
