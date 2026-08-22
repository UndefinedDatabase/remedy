── STEP SESSION-CLOSE — F009 ──
Goal:        Land this session's last reviewer output on disk and end cleanly.
             The R30 verdict is recorded, the two reviewer-block defects R30's
             worker found are written to `.agent/candidates.md` as the carrier
             of record, and the handback states the next session's first action.
             The session reached its stated round cap; the self-drive protocol
             calls a session that ends at its limit WITH a written handoff a
             SUCCESS, and this round is that handoff.

Fortschritt: ~99 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN; offen bleiben nur die zwei
             Closure-Runden: Evidenz und Zip, dann STATUS-Zeile und PR) —
             Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R30
             verdict · C3 the two candidates · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r31.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/candidates.md` (C3) · `.agent/handoff.md` (C4). NOTHING
             under `packages/`, `apps/`, `docs/` or `tests/` is touched.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (checklist
    item 23).
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. The next free id is R-0646
    when the round ends, exactly as it was when the round began. The two
    defects this round records are written to `.agent/candidates.md` as
    CANDIDATES, without ids, under the disk-vehicle rule of
    docs/roadmap/STATUS_closure_protocol.md — the NEXT reviewed round spends
    the ids. Recording them on disk rather than in a round report is finding
    R-0494's rule applied: under self-drive, a reading routed to the round
    report dies with the session.
 4. ONE APPEND AND ONE WHOLE-FILE REPLACEMENT. LEDGER31 appends to
    `.agent/live_review.md` at C2 based on the ROUND BASE. CANDIDATES replaces
    `.agent/candidates.md` at C3 in full. PLANF009R31 replaces `.agent/plan.md`
    at C1 in full. There is NO FROM/TO pair in this round; order no containment
    reading and no FROM count anywhere. The reviewer measured both append and
    replacement targets at the round base
    `002e0e83d57bad21fd88a24880a5a0e9e2552e70`: `.agent/live_review.md` is
    571277 bytes over 1136 lines and ends in exactly ONE newline;
    `.agent/candidates.md` is 620 bytes over 12 lines. So the append is one
    newline followed by its slice.
 5. LEDGER31 carries ONE paragraph. Count it with your script rather than from
    this sentence.
 6. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 7. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5: this block is 242 lines TOTAL against
    DECISION F085 D6's 490 cap, 153 of them PROSE against D5's 400. Re-measure
    both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C4: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2 and C3. Report the round base SHA you
     read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r31.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for all three. C0b is written FROM the committed
     C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 7's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R31 and
     `.agent/candidates.md` at C3 is BYTE-EQUAL to CANDIDATES — report `cmp`
     exit and both sha256 for EACH, each with a negative control against
     another file exiting non-zero. Report `wc -l` for the plan against the
     50-line cap of AGENTS.md. Line-anchored in the plan, `^## Goal$` and
     `^## Next Steps$` each read 1.
 G5  THE APPEND, under TWO independent readers, with a negative control on the
     FIRST appended paragraph (finding R-0631). LEDGER31 at C2 based on the
     round base. (a) the base blob is a byte-exact PREFIX and the remainder
     equals a newline plus that slice — report its sha256, bytes and lines;
     (b) N is counted BY YOUR SCRIPT and the last N blank-line units equal the
     slice's N paragraphs IN ORDER. Then flip one printable byte in the FIRST
     appended paragraph, at equal length, and report that BOTH readers REJECT
     the flip while both ACCEPT the true file. Report before/after bytes and
     lines.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     and at C2 (finding R-0630): a leading `- R-` id with every captured id
     DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; and the `Gate: R31` key. The
     reviewer's base readings, which yours must reproduce: entries 211, `Done:`
     3, `Landed: ` 0, `Gate: R` keys 30 over 30 DISTINCT, `Gate: R31` 0, max
     REGISTERED id R-0645, open 208. Report the max REGISTERED id and the open
     count by DECISION F009 D10's rule at BOTH points, and report the entry
     count at C2 — constraint 3 fixes that it is UNCHANGED at 211, which is the
     reading that shows this round minted nothing.
 G7  RANGE: the range from the round base to C3 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or
     `tests/`. Each commit has ONE parent; `git show --numstat` and
     `git diff --numstat` AGREE on every cell — invoke `git show` WITHOUT a `--`
     before the SHA, which turns it into a pathspec and prints nothing; every
     cell equals the `+/-` column of the handback's `## Commits` table
     (checklist item 28), compared cell by cell. Report each pre-handback
     commit's insertions against the 500 cap; the handback commit's own numbers
     belong in the round report (item 14). Leading `<<<SLICE ` and `<<<END `
     read 0 LINES in every file a slice lands in, which are `.agent/plan.md`,
     `.agent/live_review.md` and `.agent/candidates.md` — read that count
     LINE-ANCHORED and not as a substring, because LEDGER31 legitimately QUOTES
     both marker strings mid-line in its own range sentence. `git ls-files
     .remedy-wt` reads 0. Classify THIS ROUND's reflog rows by the operation
     before the first `:` and report `amend`, `rebase` and `cherry` each 0;
     assert no total over the whole reflog (R-0601).
 G8  CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the
     PRIMARY checkout, serially, with no other pytest process alive (finding
     R-0518). Report its REAL exit code and the count IT printed. No docs gate
     is owed: this round's change set holds no `docs/` path. The reviewer ran
     the canary at the round base before ordering it — it exits 0, so it can
     fail honestly (R-0364).
 G9  The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3 and C4, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all four of its lines. Report
     its `wc -l` against the 100-line cap AGENTS.md allows for a per-commit
     table of more than five commits, which the commit sequence constraint 2
     fixes is. Its `## Next` section states, in this order, that the next
     session's first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk
     — before rule 2, that `.agent/candidates.md` is NON-EMPTY and its entries
     are a block condition the first reviewed round must register or resolve,
     and that the R31 verdict is unwritten by construction because the session
     ended (R-0583: a session end is not a branch terminator). EVERY numeral
     the file states about the round's own measurements is COUNTED mechanically
     before it is written, or no numeral is stated and the enumeration speaks
     (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C4.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R31
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
R31 closes the session. It records the R30 verdict and writes the two
reviewer-block defects R30 surfaced into `.agent/candidates.md`, which is the
carrier of record across a session boundary. The build and its integration gate
are done; what remains is closure.

## Next Steps
1. Register or resolve both entries of `.agent/candidates.md` and empty that
   file — the FIRST reviewed round of the next session owes this.
2. Closure round one: the evidence job and a FRESH review zip, whose values the
   STATUS line quotes.
3. Closure round two: the authored STATUS line, the README capability sync in
   the SAME commit, and the pull request.

## Risks
- Closure needs TWO rounds, not one: ending right after a verdict strands it
  (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The closure zip's known blockers are on disk, not in memory: sorted
  `verification_runs[].test_files`, an `output_hash` that is sha256 of
  `stdout_summary` exactly, node ids from `--collect-only`, and no full-suite
  node-id list (STATUS_closure_protocol.md, algorithm step 1).
<<<END PLANF009R31

<<<SLICE LEDGER31
Gate: R31 — the R30 entry. R30 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced; the round's two substantive findings are both defects in the reviewer's own block text, both were found and declared by the WORKER, and both are recorded in `.agent/candidates.md` rather than registered here, because this session reached its round cap after issuing this verdict and the next reviewed round spends the ids. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r30.md` at `e46e5d0c`, `.agent/last_block.md` at `1cabcfd5` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r30.md`, are all sha256 8af694b228cc5d3e10c0a1cb233c5ae9490962481be9f8289a00690be724df7d over 28915 bytes and 303 lines, and that digest is the one the block itself named before the round began. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 6 slices over 111 CONTENT lines, and constraint 9's numerals re-measure as 303 TOTAL and 192 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `41bdb583` is BYTE-EQUAL to that round's PLANF009R30 slice, 40 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1. ALL THREE APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS: FINDING645 at `55504d45` is based on the round base, 561653 to 564667 bytes and 1132 to 1134 lines, N counted at 1; LEDGER30 at `146d02a8` is based on **C2** rather than on the round base, exactly as constraint 5 fixed, its base blob reading 564667 bytes and 1134 lines — the reading a round-base comparison would have got wrong by one whole slice — going to 571277 bytes and 1136 lines, N counted at 1; BUILTSTATE at `d8d48b7f` is based on the round base, 4901 to 8736 bytes and 92 to 151 lines, N counted at 4. THE PAIR IS PROVED IN THE STRONGEST FORM AVAILABLE, which is stronger than the gate the block ordered: the reviewer applied the COMMITTED GATEDOC pair to the COMMITTED base blob with its own script and the result is BYTE-IDENTICAL to `docs/agents/integration_gate.md` at `cc82ab44`, so no line of it was hand-edited or reflowed; base FROM reads 1 and TO 0, at C4 FROM reads 0 and TO 1, the containment reading printed `false` so the pair is a REWRITE and the FROM-zero count was legitimately ordered and legitimately met. THE SETS HELD line-anchored at line start at all THREE points: at the round base entries 210 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 29 over 29 DISTINCT, `Gate: R30` 0, max REGISTERED id R-0644, 207 open; at C2 entries 211 all DISTINCT, max R-0645, 208 open; at C3 the `Gate: R` keys reach 30 over 30 DISTINCT with `Gate: R30` at 1. THE SUITES ARE THE REVIEWER'S OWN, re-run serially in the primary checkout: the docs gate EXITS 0 at 295 passed and the canary EXITS 0 at 42 passed. THE BUILT STATE LANDED CORRECTLY AND WAS READ, NOT ONLY GATED: `docs/roadmap/features/T5_F009.md` now carries a `## Built State` section beginning at line 94 with exactly one blank line separating it from the section above, and the reviewer checked its claims against the source rather than against the feature file's intent — `_handle_command_submission`, the `len(parts) == 5` guard, `UI_EXPOSED_COMMANDS` holding `job.stop` and `decision.resolve`, `server_token_matches` using `secrets.compare_digest`, `token_fingerprint`'s `tf:` handle over sixteen hex characters, the 0600 modes and fixed field order of `command_audit.py`, the directory-fd nonce records of `command_nonce.py`, and the AST walk with its drift test all read as the section describes them. That section satisfies closure precondition 4. THE RANGE HELD: the range base→`d8d48b7f` lists exactly the six declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/` or `tests/`; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own table, at 303/0, 204/172, 12/11, 2/0, 2/0, 8/3 and 59/0; pre-handback insertions 303, 204, 12, 2, 2, 8 and 59, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all four slice targets; `git ls-files .remedy-wt` 0; the round's reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict. THE TWO DEFECTS, BOTH THE REVIEWER'S AND BOTH CONFIRMED AGAINST THE FILE: G8 ordered the line-anchored `^## ` heading count of `docs/agents/integration_gate.md` to match at the base and at C4, and that file holds ONE `# ` title and ZERO `^## ` headings, so the clause reads 0 against 0 and could not have failed for any round; and G6 cited R-0630 while ordering a max-REGISTERED-id reading that does not discriminate in a round whose own newly minted id is the file's ceiling, since the anchored and unanchored maxima are both R-0645 — the readings that DO discriminate are 211 anchored ids against 271 unanchored strings with 60 never registered, and 30 anchored `Gate: R` keys against 78 unanchored, and the worker reported all of them unprompted. Neither defect put a false value on disk and both gates were also met by readings that discriminate, which is why both are candidates at Low rather than block conditions. THE HANDBACK IS 100 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits; it was trimmed to fit by cutting wording and never a section, and the worker declared the trimming rather than leaving it to be discovered.
<<<END LEDGER31

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. Two candidates, both REVIEWER-BLOCK DEFECTS in the F009 R30 block
saved at `e46e5d0c`, both found and declared by the WORKER in its handback and
both confirmed by the reviewer by measuring the named file. They are recorded
here rather than registered because the session reached its stated round cap
after the R30 verdict was issued; the FIRST reviewed round of the next session
registers each (next free id R-0646) or resolves it inline as a
docs/agents/planner_reviewer_prompt.md §4.7 DECISION, and empties this file in
that same round. Writing them to disk rather than to a round report is finding
R-0494's rule applied: under self-drive, a reading routed to the round report
dies with the session.

- A GATE COUNTED A MARKDOWN CONSTRUCT THE FILE IT NAMES DOES NOT CONTAIN, so the
  clause could not fail for any round · F009 R30 · 2026-08-22. G8 ordered that
  the line-anchored `^## ` headings of `docs/agents/integration_gate.md` read the
  same count at the round base and at C4. That file carries ONE `# ` title and a
  numbered list, and ZERO `^## ` headings, so the reviewer measured 0 at both
  commits and "the same count" is true of every possible round. This is the
  R-0438 vacuous-gate class arriving through a document's STRUCTURE rather than
  through a missing path: checklist item 24 makes a reviewer resolve every PATH a
  gate names, and nothing makes it resolve the CONSTRUCT a gate counts, which is
  why R-0438's own clause does not reach it — the path here is real and only the
  heading level is absent. Candidate counter-measure for the round that registers
  this: before ordering a count of a markup construct, read that construct's
  count in the target at the base, and where it is 0 either drop the clause or
  count the construct the file actually uses.

- A GUARD-TEST CONTROL THAT DOES NOT DISCRIMINATE IN THE ROUND THAT RUNS IT ·
  F009 R30 · 2026-08-22. G6 ordered the max REGISTERED id read line-anchored and
  cited R-0630, whose warning is that an unanchored scan "reports a maximum that
  was never registered". Because R-0645 is minted by that same round and is the
  highest id in the file, the anchored and the unanchored maxima are BOTH R-0645
  and the reading demonstrates nothing. The discriminating readings exist and the
  worker reported them without being asked — 211 anchored ids against 271
  unanchored strings, 60 of which were never registered and which reach R-0627,
  and 30 anchored `Gate: R` keys against 78 unanchored — but the block ordered
  the one reading that is blind precisely when the round's own new id is the
  ceiling. Candidate counter-measure for the round that registers this: a control
  that exists to show an anchoring matters is ordered as the DIFFERENCE between
  the anchored and unanchored populations, never as a maximum, because the
  maximum coincides whenever the newest id is the reviewer's own.
<<<END CANDIDATES
