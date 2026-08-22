── STEP T003 (the queue-only import guard) — F009 ──
Goal:        Make the P3 contract mechanical. The write door ENQUEUES; it never
             applies. An AST guard over the door's own methods pins the exact
             set of imports it may make, names the applicator and shell/
             filesystem modules it may never reach, and carries the violation
             fixture the feature file's Acceptance demands. The round also
             registers R-0642 against the reviewer's own R26 block, records the
             R26 verdict, and rules DECISION F009 D24.

Fortschritt: ~96 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen, melden sich auf dem SSE-Strom und sind jetzt
             import-seitig eingezäunt; offen bleibt nur noch die
             405-Routenprobe) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0642 ·
             C3 the R26 verdict · C4 DECISION F009 D24 · C5 the guard · C6
             handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r27.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2 and
             C3) · `.agent/decisions.md` (C4) ·
             `tests/ui_server/test_command_channel.py` (C5) ·
             `.agent/handoff.md` (C6). NOTHING under `packages/`, `apps/` or
             `docs/` is touched: this round adds a guard over code that already
             satisfies it and changes no production line.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes both ledger commits because the plan must be current before them
    (checklist item 23). C2 precedes C3 because a finding persists in its OWN
    commit BEFORE anything else in the round (§4.4, clause a): a session that
    dies mid-round must not lose it.
 3. THIS ROUND MINTS R-0642 AND RESOLVES NOTHING. It writes no `Done:` line and
    no `Landed:` line. The next free id is R-0643 when the round ends. R-0642
    was minted only after the reviewer searched the OPEN set for the DEFECT
    rather than for an id (checklist item 30): R-0629 asserts a uniqueness it
    never measured and R26's G10 did measure one, R-0560 quotes a line that is
    not unique and R26's was unique at 2 whole-line and 2 indent-agnostic, and
    R-0591 governs a mechanism whose DEFAULT is the hazard where this has no
    mechanism at all — so no open finding holds it.
 4. PAIR SHAPE, printed by the reviewer's own containment test on the exact
    bytes below:
      GUARD  — `TO contains FROM: true`  → APPEND-shaped, §4.9 code obligation.
    Its FROM occurs EXACTLY 1 time in `tests/ui_server/test_command_channel.py`
    at the round base, which the reviewer counted on the base bytes. The
    obligation is ORDERED EQUALITY per §4.9 as R-0531 narrowed it, NEVER a
    per-line count and NEVER a FROM-zero count: the slice is CODE and repeats
    lines structurally.
 5. THREE APPENDS, each based on a DIFFERENT commit, and the difference is the
    point. FINDING642 appends to `.agent/live_review.md` at C2 based on the
    ROUND BASE. LEDGER27 appends to `.agent/live_review.md` at C3 based on
    **C2**, not on the round base, because C2 already grew that file — a gate
    that reads C3 against the round base measures two slices and reports one
    (R-0368's class). DECISION24 appends to `.agent/decisions.md` at C4 based on
    the round base. All three targets end in exactly ONE newline at the commit
    each is based on, which the reviewer measured on the bytes for the two the
    round base fixes and which the worker measures for the third at C2, so each
    append is one newline followed by its slice.
 6. FINDING642 and LEDGER27 each carry ONE paragraph. DECISION24 carries more
    than one; count them with your script rather than from this sentence.
 7. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 8. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5: this block is 438 lines TOTAL against
    DECISION F085 D6's 490 cap, 226 of them PROSE against D5's 400. Re-measure
    both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C6: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3, C4 and C5. Report the round base
     SHA you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r27.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 8's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R27 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, under TWO independent readers, each with a negative control on the
     FIRST appended paragraph (finding R-0631). Run this THREE times, and for
     each state which commit you based it on, exactly as constraint 5 fixes:
     FINDING642 at C2 based on the round base; LEDGER27 at C3 based on **C2**;
     DECISION24 at C4 based on the round base. For each: (a) the base blob is a
     byte-exact PREFIX and the remainder equals a newline plus that slice —
     report its sha256, bytes and lines; (b) N is counted BY YOUR SCRIPT and the
     last N blank-line units equal the slice's N paragraphs IN ORDER. Then flip
     one printable byte in the FIRST appended paragraph, at equal length, and
     report that BOTH readers REJECT the flip while both ACCEPT the true file.
     Report before/after bytes and lines for each of the three.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base,
     at C2 and at C3 (finding R-0630): a leading `- R-` id with every captured
     id DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a
     leading `Gate: R` key over that many DISTINCT keys; the `Gate: R27` key;
     and a leading `- R-0642` entry. The reviewer's base readings, which yours
     must reproduce: entries 207, `Done:` 3, `Landed: ` 0, `Gate: R` keys 26,
     `Gate: R27` 0, `- R-0642` 0. Report the max REGISTERED id and the open
     count by DECISION F009 D10's rule at all three points. Read every one of
     these at line START and not as a bare substring: this file legitimately
     QUOTES ids and gate keys inside its own verdict prose, so an unanchored
     scan reports a maximum that was never registered (finding R-0630).
 G7  PAIR. For the GUARD pair report, on whole lines and again
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
     it. The reviewer measured 158 insertions and 0 deletions on its own dry
     run; report the numbers YOU measure and flag any difference rather than
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
     the primary checkout (§4.10, guardrail G5). A guard nobody has watched fail
     is a guard nobody knows works. Three mutations of
     `packages/orchestration/ui_server.py`, each REVERTED and the file confirmed
     byte-equal to its C5 blob before the next, each reported with the ids that
     failed. In every one, the line to insert is quoted BELOW at the exact
     indentation of the site it goes to — eight leading spaces, matching the
     `from packages.orchestration.safe_points import request_stop` line it is
     placed directly beneath inside `_dispatch_job_stop`, which occurs EXACTLY
     1 time in that file at C5, counted by the reviewer whole-line and
     indent-agnostic and both agreeing. This clause is finding R-0642's own
     rule, applied in the round that registers it.
     (a) insert, directly below that anchor line:
         `        from packages.orchestration.source_apply import apply_source_patch`
         EXPECT exactly the ids listed here to fail:
         `test_the_door_imports_exactly_the_allowed_set` and
         `test_the_door_imports_nothing_from_a_forbidden_module`.
     (b) instead insert, directly below that same anchor line:
         `        from packages.orchestration.storage import delete_job`
         EXPECT exactly the ids listed here to fail:
         `test_the_door_imports_exactly_the_allowed_set` and
         `test_the_door_reaches_storage_only_for_the_name_D21_rules`.
     (c) instead rename one door method: replace
         `    def _publish_command_result(self` with
         `    def _publish_command_result_renamed(self`
         EXPECT exactly the ids listed here to fail:
         `test_every_named_method_exists` and
         `test_the_door_imports_exactly_the_allowed_set`.
     Mutation (c) is the one that matters most: it proves the guard cannot
     silently empty its own scan under a rename, which is how a guard of this
     shape usually dies. Report the ids that actually failed and flag any
     difference from the three sets above rather than reconciling it. Remove the
     worktree and report `git worktree list` at 1 line before C6.
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
     block's `Fortschritt:` line VERBATIM across all four of its lines. Report
     its `wc -l` against the 100-line cap AGENTS.md allows for a per-commit
     table of more than five commits, which the commit sequence constraint 2
     fixes is. EVERY numeral this file states about the round's own measurements
     is COUNTED mechanically before it is written, or no numeral is stated and
     the enumeration speaks (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C6.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R27
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
R27 makes the P3 contract mechanical and records the R26 verdict. An AST guard
pins the exact import set the door's own methods may make, names the applicator
and shell/filesystem modules they may never reach, admits `save_job` alone out of
storage because DECISION F009 D5's effect mapping names it, and carries both the
violation fixture the feature file's Acceptance demands and a test that stops the
guard from emptying its own scan under a rename.

## Next Steps
1. The route-walking 405 test proving every other mutating POST, PUT and DELETE
   answers 405 — the last piece of T003.
2. Then the integration gate, then closure.

## Risks
- `answer_source` is a two-valued field the escalation assumption log COUNTS.
  DECISION F009 D22 rules that this door must NOT pass its own source into it,
  the opposite of D20's rule for `request_stop`; a later round that generalises
  one to the other silently drops answers from both tallies.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R27

<<<SLICE FINDING642
- R-0642 — Low — A DESTRUCTIVE CONTROL'S INSERT HALF QUOTED A LINE AT THE INDENTATION OF WHERE IT CAME FROM RATHER THAN WHERE IT WAS GOING. The defect is the reviewer's, in the F009 R26 block saved at `232e5a6a`, and it was FOUND AND DECLARED BY THE WORKER as that round's only deviation. G10 mutation (b) ordered "that SAME line, with `payload` in place of `accepted_body`, directly BELOW the `rejected_state` audit call in the `decision.resolve` clause". The line it calls "the SAME" is the one mutation (a) quotes, and (a) quotes it with its own TWELVE leading spaces, because twelve is the indentation of the two accepted exits it is deleted FROM; the `rejected_state` audit call sits at SIXTEEN, nested one level deeper inside `if accepted_body is None:`. Applied as quoted, the insertion is an `IndentationError` that reddens the whole module — so the property the same gate states, that exactly `test_a_refused_command_announces_nothing` fails, is unreachable by the recipe written to establish it, and the worker was left choosing between an unmeetable order and a silent repair. It chose correctly: it inserted at sixteen spaces, matching the clause the sentence names, and declared the substitution. WHY NO EXISTING ITEM REACHES THIS. Checklist item 25 governs the BYTES a destructive control orders CHANGED and requires them unique inside a named file, and R26's G10 did measure exactly that, at 2 whole-line and 2 indent-agnostic and both agreeing — the deletion half was sound. Item 18 as R-0591 widened it reads an ordered MECHANISM against what it must preserve, and this order names no mechanism. Nothing governs the POSITION an INSERT half puts its bytes at, and in Python indentation is part of a line's MEANING while being no part of its IDENTITY, so a line can be correctly counted, correctly unique and still wrong at its destination. Low, because the worker caught it, the substitution it declared is the very one the reviewer's own pre-delegation dry run had used, and the ordered outcome held exactly, so nothing false reached disk. Standing rule from here, and it belongs in §3 item 25 beside the uniqueness rule that item already carries: a destructive control that orders a line INSERTED quotes that line as it must appear AT the insertion site, and a control that deletes a line at one indentation and re-inserts it at another quotes it TWICE, once per site, rather than calling the second occurrence "the SAME line". The R27 block's own G10 is the first control written under this rule. OPEN.
<<<END FINDING642

<<<SLICE LEDGER27
Gate: R27 — the R26 entry. R26 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced; the round's one deviation is the reviewer's own block defect, registered above as R-0642 and not counted against the round. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r26.md` at `232e5a6a`, `.agent/last_block.md` at `392a94eb` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r26.md`, are all sha256 9db61842f2287d052a03e144b7437d0584fcd3b25aa98b2245a608345bdfa068 over 33832 bytes and 451 lines, compared against the emitted original rather than against a recorded digest — the primary §4.9 proof, not the fallback R25 had to use. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 11 slices over 218 CONTENT lines, and constraint 9's numerals re-measure as 451 TOTAL and 233 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `58b9932a` is BYTE-EQUAL to that round's PLANF009R26 slice at sha256 `05884bfa…`, 37 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1 and a negative control against another file differing. THE THREE APPLICATIONS ARE PROVED IN THE STRONGEST FORM AVAILABLE, which is stronger than any gate the block ordered: the reviewer applied the COMMITTED slices to the COMMITTED base blobs with its own script and the results are BYTE-IDENTICAL to what landed — `packages/orchestration/ui_server.py` at `69b5f890` and `tests/ui_server/test_command_channel.py` at `77114cd4` both compare equal — so no line of either file was hand-edited, reflowed or reconciled anywhere in the round. BOTH APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS: at `a573210c` the round-base blob is a byte-exact prefix of `.agent/live_review.md` with the remainder exactly a newline plus LEDGER26 at sha256 `6b5e0603…` over 5692 bytes and 2 lines, 530425 to 536117 bytes and 1118 to 1120 lines, N counted at 1 BY THE SCRIPT; at `f36f46b2` the same holds for `.agent/decisions.md` with the remainder a newline plus DECISION23 at sha256 `1f88275c…` over 3623 bytes and 16 lines, 473798 to 477421 bytes and 6909 to 6925 lines, N counted at 8 BY THE SCRIPT; in both an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE PAIRS HELD: base FROM counts CONST 1, METH 1, PUB 2 and TESTS 1 with every TO 0, and after application every TO reads its FROM's base count while the one REWRITE pair, PUB, reads FROM 0 — the containment reading printed `true` for CONST, METH and TESTS and `false` for PUB, so no FROM-zero count was ordered for an append-shaped pair, which is finding R-0522's rule holding. THE SETS HELD line-anchored at line start, round base and C2: entries 207 at BOTH with every id DISTINCT at each — R26 minted none — leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 25 and 26 over that many DISTINCT keys, the `Gate: R26` key 0 and 1, a leading `- R-0642` entry 0 at both, max REGISTERED id R-0641 at both, and 204 open at both by DECISION F009 D10's rule. THE LEDGER HEADER WAS COMPARED AGAINST THE SERIES IT JOINS, which is checklist item 26 run rather than recalled: `Gate: R26 — the R25 entry.` matches the shape of every entry above it, and of the 26 keys the ONE that does not match that shape is `Gate: R1 — the F008 R36 entry.`, which names the previous feature's closing round correctly and is not a defect. THE SUITES ARE THE REVIEWER'S OWN, re-run serially in the primary checkout: ruff over the two changed paths EXITS 0, `test_command_channel.py` EXITS 0 at 90 passed, the canary EXITS 0 at 42 passed, and the four-path state-reader group EXITS 0 at 517 passed — the 513 of R25 grown by exactly the four tests this round adds, and not one of the four predicted by the handback. THE RED PROOF IS THE REVIEWER'S OWN, re-run at the LANDED head in a disposable worktree rather than accepted from the report: the target line reads 2 whole-line and 2 indent-agnostic with both agreeing, deleting both call sites fails exactly `test_an_accepted_command_reaches_the_sse_frame_it_announces`, `test_a_replay_announces_nothing_a_second_time` and `test_an_event_writer_that_raises_changes_neither_status_nor_body`, and making D21's 409 announce fails exactly `test_a_refused_command_announces_nothing` — the two sets the block ordered, neither reaching the other, and the file restored byte-equal after each. That the soft-failure test discriminates at all is the reviewer's own pre-delegation repair: measured before the round was delegated, it PASSED against a door with no call site whatsoever, so a call counter was added and it now fails under mutation (a) with the other two. THE RANGE HELD: the range base→`c98d57f0` lists exactly the declared paths, set difference EMPTY in both directions, and 0 paths beginning `apps/` or `docs/`; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 451/0, 366/91, 8/8, 2/0, 16/0, 40/0 and 112/0; pre-handback insertions 451, 366, 8, 2, 16, 40 and 112, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all five slice targets; `git ls-files .remedy-wt` 0; the reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict. THE HANDBACK IS 99 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits, so R25's overage is gone rather than merely smaller: R-0582's cheaper repair, ordered for the second round running, has brought this workflow back inside its own cap.
<<<END LEDGER27

<<<SLICE DECISION24
## DECISION F009 D24 — the P3 import contract: what the door may reach, stated as a set (2026-08-22)

Measured by the reviewer at `c98d57f0`, before this round was delegated, by walking `_RemedyHandler` with `ast` rather than by reading it: the write door is twelve methods and every import any of them makes is FUNCTION-SCOPED, so the door's import surface is exactly thirteen `(module, name)` pairs and an AST scan over those methods is exact rather than approximate. That is the fact this decision is built on, and it is what makes the guard cheap.

FIRST, ALLOWLIST OR DENYLIST. CHOSEN: BOTH, with the allowlist as the mechanism. The scan's union must EQUAL a named frozen set, so a new import is a failing test until a decision adds it; the forbidden-module set then says WHY that allowlist is the shape it is. ALTERNATIVES: (a) denylist alone — rejected, it passes silently on any import nobody thought to forbid, which is the whole failure mode of a contract enforced by convention. (b) allowlist alone — rejected, it pins the present without stating the rule, so a later reader cannot tell a ruled entry from an accident.

SECOND, `save_job`. CHOSEN: `packages.orchestration.storage` is reachable for the single name `save_job` and no other. DECISION F009 D21 rules that `answer_task_decision` and `save_job` are BOTH one effect, because the answer is durable only once `save_job` returns, so banning it would ban the effect table D5 already ruled. Any OTHER name out of that module is the "handler touching storage directly" the feature file's Acceptance forbids, and the guard says so as its own test.

THIRD, WHERE THE GUARD LIVES. CHOSEN: `tests/ui_server/test_command_channel.py`, as a class beside the file's existing non-HTTP classes. DECISION F009 D1 rules that file the command channel's contract home, and this is a contract over the same door; the repo's guard-test pattern in `tests/test_no_interactive_guard.py` keeps the scan in the test rather than in production, so no production line exists only to be checked.

FOURTH, THE VACUITY TEST. CHOSEN: the method list is itself asserted against the class. A guard of this shape dies by scanning nothing — rename a method and the union becomes empty, the equality against a non-empty allowlist then fails loudly, but a rename plus an allowlist trimmed to match would pass while guarding nothing. `test_every_named_method_exists` is what makes that a two-step mistake instead of a one-step one, and the red proof this round runs exercises it.

REVERSE the first by deleting either half and keeping the other; the second by removing `save_job` once the effect table stops naming it; the third by moving the class to its own module, which costs a rename and nothing else; the fourth by deleting that one test, which is also how to make the guard vacuous, so the two are deliberately the same act.
<<<END DECISION24

<<<SLICE GUARD_FROM
class TestUiExposedCommands:
<<<END GUARD_FROM

<<<SLICE GUARD_TO
class TestCommandDoorImportGuard:
    """F009's P3 contract as a guard: the write door ENQUEUES, it never applies.

    The feature file's Design makes this mechanical rather than conventional —
    "the handler may not import applicators/storage-writers (import guard — the
    P3 contract in CI)" — and its Acceptance requires the guard to FAIL on a
    handler touching storage directly, which is what the violation fixture
    below is. Detection is AST-based, following the repo's guard-test pattern
    in `tests/test_no_interactive_guard.py`: a module named in a docstring is
    prose, and a guard that cannot tell prose from an `import` gets muted by
    its own false positives.

    Every import the door makes is function-scoped, so the scan is per method
    and an import added anywhere else in `ui_server.py` is out of scope by
    construction.
    """

    #: The methods that together ARE the write door. `test_every_named_method_exists`
    #: is what stops this tuple from silently emptying itself under a rename —
    #: a guard that scans nothing passes, which is the worst way for it to fail.
    DOOR_METHODS = (
        "_handle_command_submission",
        "_dispatch_job_stop",
        "_dispatch_decision_resolve",
        "_publish_command_result",
        "_emit_command_accepted_event",
        "_audit_attempt",
        "_command_is_ui_exposed",
        "_replayed_command_result",
        "_rate_limit_admits_command",
        "_read_command_payload",
    )

    #: Every (module, name) the door is allowed to import, each because a ruled
    #: DECISION puts it there. Adding an entry means widening the P3 contract,
    #: so it belongs in the same commit as the decision that widens it.
    ALLOWED_IMPORTS = frozenset({
        ("datetime", "datetime"),                                   # D21's `now`
        ("datetime", "timezone"),                                   # D21's `now`
        ("apps.cli.command_catalog", "UI_EXPOSED_COMMANDS"),        # D4's subset
        ("packages.orchestration.command_audit",
         "audit_command_attempt"),                                  # D6's audit
        ("packages.orchestration.command_nonce", "lookup_nonce_result"),   # D8
        ("packages.orchestration.command_nonce", "publish_nonce_result"),  # D8
        ("packages.orchestration.config", "get_config"),            # D9's limit
        ("packages.orchestration.config", "get_key_spec"),          # D9's limit
        ("packages.orchestration.data_paths", "resolve_data_root"), # D23's root
        ("packages.orchestration.escalation", "answer_task_decision"),     # D5
        ("packages.orchestration.safe_points", "request_stop"),            # D5
        ("packages.orchestration.storage", "save_job"),                    # D21
        ("packages.orchestration.timeline", "append_run_event"),           # D23
    })

    #: Modules the door may NEVER import from, whatever the name. These are the
    #: applicators and the shell/filesystem writers the P3 contract exists to
    #: keep out of an HTTP handler. Every path here resolves on disk.
    FORBIDDEN_MODULES = frozenset({
        "packages.orchestration.source_apply",
        "packages.orchestration.patch_apply",
        "packages.orchestration.diff_repair_apply",
        "packages.orchestration.job_fulfillment",
        "packages.orchestration.exec_guard",
        "packages.orchestration.workspace",
        "packages.common.secure_fs",
        "subprocess",
        "shutil",
    })

    #: `storage` is the one write-side module the door may reach, and only for
    #: the single name DECISION F009 D21 puts in the effect table: the answer is
    #: durable only once `save_job` returns. Any OTHER name from it is the
    #: "handler touching storage directly" the Acceptance forbids.
    STORAGE_MODULE = "packages.orchestration.storage"
    STORAGE_ALLOWED_NAMES = frozenset({"save_job"})

    @staticmethod
    def _door_imports(source: str, method_names) -> set:
        """Every (module, name) imported inside the named methods of the handler."""
        import ast

        wanted = set(method_names)
        found = set()
        for node in ast.walk(ast.parse(source)):
            if not (isinstance(node, ast.ClassDef) and node.name == "_RemedyHandler"):
                continue
            for member in node.body:
                if not isinstance(member, ast.FunctionDef) or member.name not in wanted:
                    continue
                for sub in ast.walk(member):
                    if isinstance(sub, ast.ImportFrom):
                        for alias in sub.names:
                            found.add((sub.module or "", alias.name))
                    elif isinstance(sub, ast.Import):
                        for alias in sub.names:
                            found.add((alias.name, alias.name))
        return found

    def _server_source(self) -> str:
        from pathlib import Path

        from packages.orchestration import ui_server

        return Path(ui_server.__file__).read_text(encoding="utf-8")

    def test_every_named_method_exists(self):
        """Without this the guard empties itself the first time a method is renamed."""
        import ast

        handler = [n for n in ast.walk(ast.parse(self._server_source()))
                   if isinstance(n, ast.ClassDef) and n.name == "_RemedyHandler"]
        assert len(handler) == 1, handler
        defined = {n.name for n in handler[0].body if isinstance(n, ast.FunctionDef)}
        missing = sorted(set(self.DOOR_METHODS) - defined)
        assert missing == [], missing

    def test_the_door_imports_exactly_the_allowed_set(self):
        """Equality, not containment: a NEW import is a finding until it is ruled."""
        found = self._door_imports(self._server_source(), self.DOOR_METHODS)
        assert found == set(self.ALLOWED_IMPORTS), {
            "unruled": sorted(found - set(self.ALLOWED_IMPORTS)),
            "vanished": sorted(set(self.ALLOWED_IMPORTS) - found),
        }

    def test_the_door_imports_nothing_from_a_forbidden_module(self):
        """The P3 contract stated as the class of module it keeps out."""
        found = self._door_imports(self._server_source(), self.DOOR_METHODS)
        offending = sorted((m, n) for m, n in found if m in self.FORBIDDEN_MODULES)
        assert offending == [], offending

    def test_the_door_reaches_storage_only_for_the_name_D21_rules(self):
        found = self._door_imports(self._server_source(), self.DOOR_METHODS)
        from_storage = {n for m, n in found if m == self.STORAGE_MODULE}
        assert from_storage <= self.STORAGE_ALLOWED_NAMES, sorted(from_storage)

    def test_the_guard_fails_on_a_handler_that_touches_storage_directly(self):
        """The violation fixture the feature file's Acceptance requires.

        A guard nobody has watched fail is a guard nobody knows works. This runs
        the SAME extractor over a synthetic handler, so the proof costs no
        mutation of the real file and cannot leave one behind.
        """
        violation = (
            "class _RemedyHandler:\n"
            "    def _dispatch_job_stop(self):\n"
            "        from packages.orchestration.source_apply import apply_source_patch\n"
            "        from packages.orchestration.storage import delete_job\n"
            "        return apply_source_patch, delete_job\n"
        )
        found = self._door_imports(violation, self.DOOR_METHODS)
        assert ("packages.orchestration.source_apply",
                "apply_source_patch") in found, found
        # Each of the three assertions above would now fail, which is the point.
        assert found != set(self.ALLOWED_IMPORTS)
        assert [(m, n) for m, n in found if m in self.FORBIDDEN_MODULES] != []
        assert not {n for m, n in found
                    if m == self.STORAGE_MODULE} <= self.STORAGE_ALLOWED_NAMES


class TestUiExposedCommands:
<<<END GUARD_TO
