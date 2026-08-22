── STEP CLOSURE-PREP — F009 ──
Goal:        Make the record true and make closure possible. Record the R29
             verdict AND the integration-gate verdict, register R-0645, repair
             the procedure that ordered a blind parity gate — R-0444 recurred
             under its own standing rule — and give the feature file the
             `## Built State` section closure precondition 4 requires. No
             production line changes.

Fortschritt: ~99 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN: Branch-only-Menge leer, alle sechs
             Base-only-Ids per Einzelbeweis der Umgebung zugeordnet; offen
             bleiben nur die zwei Closure-Runden) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register
             R-0645 · C3 the R29 and integration-gate verdicts · C4 repair
             docs/agents/integration_gate.md · C5 the feature file's Built
             State · C6 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r30.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2 and
             C3) · `docs/agents/integration_gate.md` (C4) ·
             `docs/roadmap/features/T5_F009.md` (C5) · `.agent/handoff.md`
             (C6). NOTHING under `packages/`, `apps/` or `tests/` is touched.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes both ledger commits because the plan must be current before them
    (checklist item 23). C2 precedes C3 because a finding persists in its OWN
    commit BEFORE anything else in the round (§4.4, clause a).
 3. THIS ROUND MINTS R-0645 AND RESOLVES NOTHING. It writes no `Done:` line and
    no `Landed:` line. The next free id is R-0646 when the round ends.
 4. EXACTLY ONE FINDING IS MINTED, AND THE OTHER DEFECT THIS ROUND FOUND GETS NO
    ID ON PURPOSE. The R29 parity defect — a `apps/ui/dist` CONTENT digest
    ordered for a property `_frontend_is_stale()` decides by MTIME — is already
    OPEN as R-0444, whose own standing rule ("a gate that asserts something did
    NOT HAPPEN measures the event, not the outcome") is the rule the R29 block
    broke. Checklist item 30 forbids a second id for one defect, so the new
    evidence rides in LEDGER30 and the counter-measure lands in C4. Do NOT mint
    an id for it and do NOT append a second `- R-0444` entry: G6 requires every
    leading `- R-` id to be DISTINCT and a duplicate would break it.
 5. TWO APPENDS, each based on a DIFFERENT commit, and one PAIR. FINDING645
    appends to `.agent/live_review.md` at C2 based on the ROUND BASE. LEDGER30
    appends to `.agent/live_review.md` at C3 based on **C2**, not on the round
    base, because C2 already grew that file (R-0368's class). BUILTSTATE appends
    to `docs/roadmap/features/T5_F009.md` at C5 based on the ROUND BASE. The
    reviewer measured each target at the round base
    `bcf295f951957ebdf0047fba315b344b1a2ce212`: `.agent/live_review.md` is
    561653 bytes over 1132 lines and `docs/roadmap/features/T5_F009.md` is 4901
    bytes over 92 lines, and EACH ends in exactly ONE newline there. The worker
    measures the C2 target for itself. So each append is one newline followed by
    its slice.
 6. FINDING645 and LEDGER30 each carry ONE paragraph. BUILTSTATE carries more
    than one; count them with your script rather than from this sentence.
 7. PAIR SHAPE, printed by the reviewer's own containment test on the exact
    bytes below:
      GATEDOC — `TO contains FROM: false` → REWRITE, so the FROM-zero count IS
    ordered for it (§4.9). Its FROM occurs EXACTLY 1 time in
    `docs/agents/integration_gate.md` at the round base, counted by the reviewer
    whole-line and indent-agnostic with both agreeing.
 8. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 9. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5: this block is 303 lines TOTAL against
    DECISION F085 D6's 490 cap, 192 of them PROSE against D5's 400. Re-measure
    both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C6: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3, C4 and C5. Report the round base
     SHA you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r30.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for all three. C0b is written FROM the committed
     C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 9's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R30 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, under TWO independent readers, each with a negative control on the
     FIRST appended paragraph (finding R-0631). Run this THREE times, and for
     each state which commit you based it on, exactly as constraint 5 fixes:
     FINDING645 at C2 based on the round base; LEDGER30 at C3 based on **C2**;
     BUILTSTATE at C5 based on the round base. For each: (a) the base blob is a
     byte-exact PREFIX and the remainder equals a newline plus that slice —
     report its sha256, bytes and lines; (b) N is counted BY YOUR SCRIPT and the
     last N blank-line units equal the slice's N paragraphs IN ORDER. Then flip
     one printable byte in the FIRST appended paragraph, at equal length, and
     report that BOTH readers REJECT the flip while both ACCEPT the true file.
     Report before/after bytes and lines for each of the three.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base,
     at C2 and at C3 (finding R-0630): a leading `- R-` id with every captured
     id DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a
     leading `Gate: R` key over that many DISTINCT keys; the `Gate: R30` key;
     and a leading `- R-0645` entry. The reviewer's base readings, which yours
     must reproduce: entries 210, `Done:` 3, `Landed: ` 0, `Gate: R` keys 29,
     `Gate: R30` 0, `- R-0645` 0, max REGISTERED id R-0644, open 207. Report the
     max REGISTERED id and the open count by DECISION F009 D10's rule at all
     three points. Read every one of these at line START and not as a bare
     substring: this file legitimately QUOTES ids and gate keys inside its own
     verdict prose, so an unanchored scan reports a maximum that was never
     registered (finding R-0630).
 G7  PAIR. For the GATEDOC pair report, on whole lines and again
     indent-agnostically, with the two readings required to AGREE: the FROM
     count in `docs/agents/integration_gate.md` at the round base and at C4, and
     the TO count at both. The reviewer's base readings, which yours must
     reproduce: FROM 1, TO 0. Because the containment reading is `false` this is
     a REWRITE, so the FROM count at C4 must read 0 and the TO count 1. Read the
     BASE side with `git show <base>:<path>` into a variable or into scratch
     under `.remedy-wt/` — never by writing the base blob over the tracked file,
     which guardrail G5 forbids (finding R-0594).
 G8  C4 CONTENT: `git show --numstat` for C4, and the whole file re-read to
     confirm the paragraph still reads as one sentence sequence — report the 18
     lines spanning `parity before the base run (COPY` through
     `An unattributed \`comm -23\`` verbatim so the reviewer can read the seam
     itself. Line-anchored, `^## ` headings in that file read the same count at
     the round base and at C4; report both numbers.
 G9  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree (finding R-0518). Report each command's REAL
     exit code and the count IT printed — predict no number:
       `python3 -m pytest tests/docs/ -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     The docs gate is owed because this round's change set holds
     `docs/roadmap/**` (planner_reviewer_prompt.md §3, docs-round gate); the
     canary is unconditional. The reviewer ran both at the round base before
     ordering them: each exits 0, so each can fail honestly (R-0364). KNOWN AND
     STATED RATHER THAN IMPLIED: `tests/docs/` reads feature FILENAMES and the
     ledger counts, not any feature file's BODY, so it CANNOT fail on the
     BUILTSTATE slice's content. It is ordered because the change set owes it,
     not as evidence that the section is correct; the reviewer reads that
     section itself.
 G10 RANGE: the range from the round base to C5 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/` or `tests/`. Each
     commit has ONE parent; `git show --numstat` and `git diff --numstat` AGREE
     on every cell — invoke `git show` WITHOUT a `--` before the SHA, which
     turns it into a pathspec and prints nothing; every cell equals the `+/-`
     column of the handback's `## Commits` table (checklist item 28), compared
     cell by cell. Report each pre-handback commit's insertions against the 500
     cap; the handback commit's own numbers belong in the round report (item
     14). Leading `<<<SLICE ` and `<<<END ` read 0 LINES in every file a slice
     lands in, which are `.agent/plan.md`, `.agent/live_review.md`,
     `docs/agents/integration_gate.md` and
     `docs/roadmap/features/T5_F009.md`. `git ls-files .remedy-wt` reads 0.
     Classify THIS ROUND's reflog rows by the operation before the first `:` and
     report `amend`, `rebase` and `cherry` each 0; assert no total over the
     whole reflog (R-0601).
 G11 The handback carries every mandated section of
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

<<<SLICE PLANF009R30
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
R30 is closure preparation. It records the R29 verdict and the integration-gate
verdict, registers R-0645, repairs docs/agents/integration_gate.md so the base
run's neutralisation check measures the EVENT rather than the outcome — R-0444
recurred at R29 under its own standing rule — and adds the `## Built State`
section that closure precondition 4 requires of the feature file. The build
itself is done: the integration gate found an EMPTY branch-only set.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md, in TWO rounds: the
   evidence job and a FRESH review zip first, then the authored STATUS line,
   the README capability sync and the pull request.

## Risks
- Closure needs TWO rounds, not one: the evidence-and-zip round produces the
  values the STATUS line quotes, and a separate round commits that line. Ending
  right after a verdict strands it (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The closure zip's known blockers are on disk, not in memory: sorted
  `verification_runs[].test_files`, an `output_hash` that is sha256 of
  `stdout_summary` exactly, node ids from `--collect-only`, and no full-suite
  node-id list (STATUS_closure_protocol.md, algorithm step 1).
<<<END PLANF009R30

<<<SLICE FINDING645
- R-0645 — Low — THE INTEGRATION GATE DERIVES ITS BRANCH-ONLY SET FROM ONE RUN OF A COMMAND WHOSE FAILURE SET IS NOT STABLE, AND THE REVIEWER'S RE-RUN FOUND TWO IDS THE WORKER'S RUN DID NOT. Found by the reviewer while re-executing the F009 R29 gate off disk rather than reading the handback back. The worker's branch run of `python3 -m pytest -n auto -q` at `bcf295f9`'s parent exited 0 with `17572 passed, 20 skipped` and an EMPTY `branch_failed.txt`; the reviewer's run of the identical command from the same primary checkout about twenty minutes later exited 1 with `2 failed, 17570 passed, 20 skipped`, the two ids being `tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_a_mutated_workspace_shows_blocking_drift` and `::test_an_unchanged_stopped_workspace_shows_no_drift`. Both were then re-run SERIALLY and both EXIT 0, and the whole file serially reads `8 passed`, so they classify as the xdist-flake class that docs/agents/integration_gate.md step 4 records rather than blocks on — which is why this finding does not change the R29 gate verdict. THE DEFECT IS NOT THE FLAKE, IT IS THE INFERENCE THE GATE DRAWS FROM ONE SAMPLE. Step 1 of that procedure takes a single branch run, step 3 subtracts the base set from it, and step 4 then reasons per id over the difference; nothing in the procedure states that the branch set is a SAMPLE, so an empty branch-only set reads on the page as "this branch introduces no failures" when what was measured is "this run introduced none". The two readings here differ by two ids over the same tree, so the gap is real and not hypothetical. WHY R-0499 AND R-0479 DO NOT REACH THIS, stated because they are the nearest OPEN neighbours and checklist item 30 requires the open set to be searched for the DEFECT before an id is minted: R-0499 is a specific member of the eight-file structural sweep going red about once in twenty runs INSIDE A FRESH WORKTREE, and its fix clause is to order that sweep as a PROBE and capture the node id — it is about one test's flakiness, not about what a gate may conclude from one run; R-0479 is about a generated untracked file contaminating WORKING-TREE readings taken concurrently with a suite, and its fix clause binds when such a reading may be taken, not how a failure set is derived. The cause of THIS pair's flakiness is not captured and is deliberately not guessed at here. WHY LOW: the gate's blocking rule is per id and survives — every branch-only id, however it arrives, is serial-re-run and reproduced at the merge base before the feature is blamed, so a genuine regression appearing in either run is still caught by step 4. What is overstated is only the completeness of an EMPTY branch-only set. Counter-measure for a later round to weigh rather than one applied here: either state in the procedure that the branch-only set is a per-run sample and that an empty one is evidence rather than proof, or order the branch run repeated until two consecutive runs agree on the set. OPEN.
<<<END FINDING645

<<<SLICE LEDGER30
Gate: R30 — the R29 entry. R29 PASSED, AND THE INTEGRATION GATE PASSES WITH IT — that verdict is issued here, by the reviewer, and the worker correctly issued none. Every gate was RE-EXECUTED off disk and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r29.md` at `0c9a5a5c`, `.agent/last_block.md` at `4c833e42` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r29.md`, are all sha256 f0df008bf0860d6c36805b09879310e9f0de8a8f66df9945fb3923215b057d32 over 28469 bytes and 271 lines, compared against the emitted original rather than against a recorded digest, and that digest is the one the block itself named before the round began. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 4 slices over 46 CONTENT lines, and constraint 8's numerals re-measure as 271 TOTAL and 225 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `d2671f7b` is BYTE-EQUAL to that round's PLANF009R29 slice, sha256 940d103c…26eefe, 39 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1. ALL THREE APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS, AND THE ONE THAT MATTERS MOST IS THE SECOND: FINDING644 at `d86146c2` is based on the round base, 552059 to 555475 bytes and 1128 to 1130 lines, N counted at 1 BY THE SCRIPT; LEDGER29 at `5b497416` is based on **C2** rather than on the round base, exactly as constraint 5 fixed, its base blob reading 555475 bytes and 1130 lines — the reading a round-base comparison would have got wrong by one whole slice — going to 561653 bytes and 1132 lines, N counted at 1; CORRECTD25 at `30203bb5` is based on the round base, 483709 to 485030 bytes and 6953 to 6959 lines, N counted at 3. In all three an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start across all THREE points: at the round base entries 209 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 28 over 28 DISTINCT, `Gate: R29` 0 and a leading `- R-0644` entry 0, max REGISTERED id R-0643, 206 open; at C2 entries 210 all DISTINCT with `- R-0644` at 1, max id R-0644 and 207 open; at C3 the `Gate: R` keys reach 29 over 29 DISTINCT keys with `Gate: R29` at 1 and 207 open. THE INTEGRATION GATE ITSELF, WHICH IS THE ROUND'S SUBJECT: the worker's branch run exited 0 at `17572 passed, 20 skipped` over 17592 collected with an EMPTY `branch_failed.txt`; the base run at `ce49348b`, taken in a throwaway worktree ON the branch `tmp/base-gate-f009r29` and never detached, exited 1 at `6 failed, 17406 passed, 20 skipped`; `comm -13` is EMPTY and `comm -23` holds 6 ids. ALL SIX BASE-ONLY IDS ARE ATTRIBUTED BY DIRECT EVIDENCE AND NOT ON THE STRENGTH OF A PARITY CLAIM, which is what docs/agents/integration_gate.md step 3 requires and what makes the verdict reachable: each fails with `ERROR: React UI not built.` emitted at `packages/orchestration/ui_server.py:3016`, reached because `_frontend_is_stale()` reads True — the reviewer read that function and it compares `f.stat().st_mtime > dist_mtime` over `apps/ui/src`, so mtime and not content is the deciding property — and `_auto_build_frontend()` returns None under `REMEDY_UI_NO_AUTO_BUILD=1`, after which `start_ui_server` exits 1 and the test's server thread never binds. The worker's controlled proof at `ce49348b` closes it: with `dist/index.html` set older than `src` the id FAILS with that exact error, and with the mtime restored and no byte of content changed it PASSES; all six re-run serially at the merge base EXIT 0. So no branch-only failure is coupled to feature code, there is no BLOCKER, and the branch-only flake-class count the operator brief owes is 0 for that run. THE REVIEWER'S OWN RE-RUN OF THE BRANCH SUITE DISAGREED WITH THE WORKER'S, AND IT IS REGISTERED ABOVE AS R-0645 RATHER THAN HIDDEN: the identical command from the same checkout exited 1 at `2 failed, 17570 passed, 20 skipped`, both ids in `tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift`, both serial-PASSING and so of the xdist-flake class step 4 records rather than blocks on. The gate verdict stands because step 4's blocking rule is per id and neither id survives a serial re-run. R-0444 RECURRED IN THIS ROUND UNDER ITS OWN STANDING RULE, AND NO SECOND ID WAS MINTED FOR IT: the R29 block's G8 ordered a recursive CONTENT digest of `apps/ui/dist` before and after the base run as the parity criterion, the digests came back EQUAL at 2139f2fe…501dc8, and the worker then measured that every file under that tree carries mtime 1787376153.535 — about 81 seconds into a run that began at 1787376072 — against the 1787375952.935 the parity copy had left. The tree was rewritten mid-run with byte-identical content, which is precisely the case R-0444 says a content digest cannot distinguish from no rebuild at all, and R-0444's fix clause already reads "a gate that asserts something did NOT HAPPEN measures the event, not the outcome". The defect is the reviewer's; checklist item 30 forbids a second id for a defect the open set already holds; and C4 of this round repairs docs/agents/integration_gate.md, which is the document that ordered the blind criterion in the first place. The worker found it, declared it, and went beyond its order to make the attribution independent of it — which is the round rescuing the reviewer, and it is why the gate verdict is issuable at all. THE RANGE HELD: the range base→`62079678` lists exactly the 11 declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or `tests/`; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own table, at 271/0, 171/331, 12/10, 2/0, 2/0, 6/0 and the six evidence files of C5; pre-handback insertions 271, 171, 12, 2, 2, 6 and 85, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all three slice targets; `git ls-files .remedy-wt` 0; the round's reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree, the temporary base branch deleted, and a clean tree at the verdict. THE CANARY IS THE REVIEWER'S OWN at 42 passed, and the docs gate reads 295 passed at this round's base. THE HANDBACK IS 90 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits, so R-0582's repair has now held for four rounds running.
<<<END LEDGER30

<<<SLICE GATEDOC_FROM
   VERIFY the neutralization: hash `apps/ui/dist` before and after
   the base run; a changed hash voids the parity claim and forces
   per-id attribution; or run the same install/build there), or
<<<END GATEDOC_FROM

<<<SLICE GATEDOC_TO
   VERIFY the neutralization by measuring the EVENT, not the outcome
   (R-0444, recurring at F009 R29): record the mtime of every file under
   `apps/ui/dist` before and after the base run and report the window; ANY
   mtime falling inside the run window voids the parity claim and forces
   per-id attribution. A content hash may accompany that reading but never
   stands alone, because equal content is consistent both with no rebuild
   and with a byte-identical one — the case F009 R29 actually hit; or run
   the same install/build there), or
<<<END GATEDOC_TO

<<<SLICE BUILTSTATE
## Built State
Measured at `bcf295f951957ebdf0047fba315b344b1a2ce212`, the head the F009
integration gate covers.

- **T001 — the door, its validation, its auth and its rate limit:**
  `POST /api/jobs/{jid}/commands` is handled by
  `_RemedyHandler._handle_command_submission` in
  `packages/orchestration/ui_server.py`, reached from the `do_POST` branch that
  requires `len(parts) == 5` with `parts[4] == "commands"` — so a near miss such
  as `.../commands/extra` or `.../command` falls through to 405. The UI-exposed
  subset is a single source: `UI_EXPOSED_COMMANDS: frozenset[str]` in
  `apps/cli/command_catalog.py`, holding `job.stop` and `decision.resolve`, is
  imported by the endpoint and checked by `_command_is_ui_exposed`. Auth is a
  bearer token compared in constant time by `server_token_matches`
  (`secrets.compare_digest`) plus the `X-Remedy-CSRF` double-submit named by
  `COMMAND_CSRF_HEADER`. Rate limiting is `accept_command_under_rate_limit`,
  one minute budget per (token fingerprint, job) over
  `COMMAND_RATE_WINDOW_SECONDS`, configured by `ui.command_rate_limit_per_minute`
  (`COMMAND_RATE_LIMIT_CONFIG_KEY`) and serialised by `_COMMAND_RATE_LOCK`
  because the server is threaded. Bodies are capped at
  `COMMAND_REQUEST_MAX_BYTES` (64 KiB); typed field errors come from
  `_command_field_error`.

- **T002 — nonce idempotency, the audit trail and the accepted event:**
  `packages/orchestration/command_nonce.py` writes one 0600 record per nonce
  under `commands_nonce/` (`NONCE_DIRNAME`) through a directory fd, capped at
  `MAX_NONCE_RECORD_BYTES`; `publish_nonce_result` stores the outcome and
  `lookup_nonce_result` returns it, so `_replayed_command_result` answers a
  repeated `client_nonce` with the ORIGINAL status and body rather than an
  error, and the effect fires once. `packages/orchestration/command_audit.py`
  appends every attempt to `commands_audit.jsonl` (`AUDIT_FILENAME`, mode 0600)
  in the fixed field order `("ts", "token_fp", "command", "args_hash", "nonce",
  "outcome")`, with the token reduced by `token_fingerprint` to a `tf:` handle
  over sixteen hex characters of SHA-256 and the args by `args_fingerprint` —
  no raw token and no raw args ever reach the file.
  `_emit_command_accepted_event` puts `command.accepted`
  (`COMMAND_ACCEPTED_EVENT`) onto the SSE stream F008 built, so the UI sees its
  own writes through the same channel as everything else.

- **T003 — the effect table, the queue-only guards and the 405 walk:**
  both exposed commands dispatch through their own seam, `_dispatch_job_stop`
  and `_dispatch_decision_resolve`, and neither touches files, jobs or shells
  directly. The queue-only promise is pinned twice: `TestCommandDoorImportGuard`
  in `tests/ui_server/test_command_channel.py` fails if the handler reaches an
  applicator or a storage writer, and
  `tests/ui_server/test_command_dispatch.py::TestJobStopDispatchEffects` asserts
  the per-command side effects. The 405 discipline is proved by a WALK over the
  routes the server really serves rather than by a list: `_do_get_route_facts`
  reads `do_GET`'s literal routes and its `handlers` dict by AST,
  `_walkable_paths` turns them into concrete paths, and
  `test_every_route_the_server_serves_refuses_post_put_and_delete` sends POST,
  PUT and DELETE at every one of them, asserting 405 AND the body's
  `method not allowed`, plus a count assertion so an empty walk cannot pass
  silently. `test_the_walk_knows_every_route_the_source_dispatches` is the drift
  detector: a route added as a new literal comparison fails it immediately. The
  known limit is written where a reader will search for it — a NEW route matched
  STRUCTURALLY has no literal to derive, and is the one case neither half sees
  (DECISION F009 D25, its route inventory corrected 2026-08-22).
<<<END BUILTSTATE
