── STEP findings + checklist — F086 R24 ──────────────────────
Goal:
Record R23's verdict, register the three defects R23 exposed — all of them in the
reviewer's own block text, none in the worker's execution — and promote each one's
counter-measure onto the §3 pre-emission checklist, which is the only place a rule
in this repository actually binds the next block. This round writes no production
code and runs no suite of its own beyond the canary.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R24 (§3 item 23 — this round touches the ledger,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains FIND0589, FIND0590, FIND0591 and RECORD22.
4. `docs/agents/planner_reviewer_prompt.md` gains three clauses in ONE commit:
   item 14 grows the constant-sweep rule, item 18 widens from a red-proof's two
   halves to any ordered recipe, and a new item 27 is added after item 26.
5. The handback, then the reviewer's VERDICT appended to it.

Change:
Exactly these paths:
  `.agent/authored/f086-r24.md`            (C0a)
  `.agent/last_block.md`                   (C0b)
  `.agent/plan.md`                         (C1)
  `.agent/live_review.md`                  (C2)
  `docs/agents/planner_reviewer_prompt.md` (C3)
  `.agent/handoff.md`                      (C4, then C5)
Nothing else. In particular NOT `.agent/gate_f086_r23/attribution.txt`, not
`tests/test_install_smoke.py`, not `tests/conftest.py`, not `pyproject.toml`, not
`packages/orchestration/ci_stages.py`, not `packages/orchestration/ui_server.py`,
not `apps/cli/version_report.py`, and nothing else under `apps/`, `packages/`,
`tests/`, `docs/roadmap/` or `.github/`. Every path this paragraph FORBIDS exists
at `39bfc199` — checked with `git ls-tree` at emission, per §3 item 24 — so the
prohibition forbids something real.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.
   R23 declared three such problems and was right to; that is the system working.

2. The change set is the path list above and nothing else.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` that entered at `4dc7cbdf` stays exactly as it is, and so does every
   word of the R23 block committed at `67224395`, defects included; §3 item 20
   rules that the counter-measure for landed text is a dated correction in NEW
   text. You append only. G7 is written so that duplicate is EXPECTED rather than
   forbidden, and a gate that reported it as a violation would be the defect.

4. PLAN24, FIND0589, FIND0590, FIND0591, RECORD22, the three CHECK pairs and
   VERDICT are the reviewer's text. Do not summarise, rewrap or reformat them. Do
   not write a verdict of your own anywhere — not in the handoff, not in a commit
   message, not in your report. Reporting what a gate MEASURED is your job; ruling
   on a round is not. A worker-authored `Done:` paragraph is a finding however
   honestly it is hedged (§4.4).

5. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback, and `git worktree list` reads ONE line throughout.
   This round orders NO mutation and NO disposable worktree: it edits documents
   and a record, so there is nothing to red-prove, and inventing a mutation to
   look thorough would prove nothing about a documentation edit.

6. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`,
   brace-with-quote literals and env-prefix command forms. Route that work through
   `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.

7. THE THREE CHECK PAIRS LAND IN ONE COMMIT, C3, applied in the order 14, 18, 27.
   Each is APPEND-shaped — the containment test was run per pair at emission and
   printed `TO contains FROM: true` for all three, so §4.9's APPEND obligation
   applies to each and a "FROM 0x" count is unattainable by construction and must
   not be attempted. Each FROM occurs exactly 1x in the file at `39bfc199`,
   verified at emission. Item 27 is appended AFTER item 26's last line and BEFORE
   the paragraph beginning "Why this is on disk and not a habit", so nothing is
   renumbered and no existing item moves.

8. THE HANDBACK'S ARITHMETIC IS STATED ONCE, HERE, AND NOWHERE ELSE — which is
   R-0589's own counter-measure applied to the block that registers it. The
   VERDICT slice this block ships is 47 lines, measured at emission on its final
   bytes, and C5 appends it by pure concatenation, so the file at C5 is exactly
   C4's length plus 47. KEEP C4 AT 53 LINES OR FEWER, which puts C5 at 100 or
   fewer with no DECISION D15 overage to declare. Write C4 in the COMPACT form:
   ONE commits table with a per-commit row, ONE LINE PER GATE in the Verification
   section, the transcript going to your round report and not into the file
   (R-0582). G13 below NAMES this constraint instead of restating its numerals,
   deliberately: measured at emission, 47 and 53 occur in this constraint and in no
   other clause of this block, so there is no second copy to fall out of step.
   If C4 nevertheless lands above that bound, do NOT drop a mandated section —
   exceed the cap, write the DECISION D15 "Deviations, declared" line naming the
   real count and the mandated content that caused it, and say so in the report.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 5's two readings
   both taken and both reported.

G2 TRANSPORT. `.remedy-wt/f086-r24.md`, the committed `.agent/authored/f086-r24.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN24 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND. The pre-C2 `.agent/live_review.md` blob is a byte-exact PREFIX
   of the post-C2 blob, and the remainder is byte-equal to a blank line, FIND0589,
   a blank line, FIND0590, a blank line, FIND0591, a blank line, RECORD22 — all
   four extracted from the committed C0a. Report the remainder's sha256 and line
   count.

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = lines matching `^- R-\d+ — `; resolved = lines matching
   `^Done: R-\d+ — `. Report at `39bfc199` and at C2: registered count, resolved
   count, duplicate count, unregistered-resolution count, `Landed:` line count and
   open count. The RESOLVED set must be UNCHANGED between the two — this round
   resolves nothing — and the REGISTERED set must gain exactly `R-0589`, `R-0590`
   and `R-0591` and nothing else. CONTROL, which must MOVE so the reading is not
   vacuous: the same two extractions over `f0b27118..7b84524c` report `[]`
   registered while the resolved set gains exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST — a token a finding QUOTES is not a token it USES
   (R-0584) — then count `\bHEAD\b` in what remains. It must read 0. RED CONTROL,
   same two-step extractor over the lines `fd166295` adds to the same file: it must
   read 3. A control that does not read 3 means the extractor is broken and the 0
   proves nothing.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `39bfc199` and at C2, and
   the SET of strings occurring more than once at each. That duplicate set must be
   UNCHANGED and must be exactly `Gate: R19 — the R18 entry.` — constraint 3
   forbids repairing it, so it is the expected reading. Then: `Gate: R24 — the R23
   entry.` occurs exactly 1x, it is the LAST such header in the file, and the text
   immediately following it begins `R23 `.

G8 THE THREE PAIRS, PROVED IN THE APPEND FORM (§4.9), never as a FROM-zero count.
   For each of CHECK14, CHECK18 and CHECK27: print the containment test's own
   output, confirm the FROM occurs exactly 1x at `39bfc199` AND exactly 1x at C3.
   Then the ORDERED EQUALITY that covers all three at once: the file at C3 is
   byte-equal to the `39bfc199` blob with CHECK14FROM's single occurrence replaced
   by CHECK14TO, CHECK18FROM's by CHECK18TO and CHECK27FROM's by CHECK27TO, and
   nothing else changed. Report C3's sha256 and line count against the base's 820.

G9 STRUCTURE, which is what proves nothing was renumbered.
   `grep -c '^  14\. \*\*'`, `grep -c '^  15\. \*\*'`, `grep -c '^  18\. \*\*'`,
   `grep -c '^  19\. \*\*'`, `grep -c '^  26\. \*\*'` and `grep -c '^  27\. \*\*'`
   over `docs/agents/planner_reviewer_prompt.md` at C3 each read 1. Report the line
   that FOLLOWS each TO's last line: after CHECK14TO it is item 15's heading line,
   after CHECK18TO it is item 19's heading line, and after CHECK27TO it is the line
   beginning `  Why this is on disk and not a habit:`.

G10 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md` and
    `docs/agents/planner_reviewer_prompt.md` at C4: each must be 0. Count marker
    LINES, not substrings — this handback quotes gate text, so a substring gate
    over `.agent/handoff.md` would be unmeetable (F086 R5). The `.agent/handoff.md`
    reading can only be taken after C5 and goes in the round report.

G11 SUITES, serially in the PRIMARY checkout, the second started only after the
    first has ENDED and reported its exit code (F085 R64: two concurrent pytest
    processes produce false reds here). First `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf`, then the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both exit codes
    and both summary lines. NOTE, so the handback does not claim more than it
    proves: no suite in this repository reads
    `docs/agents/planner_reviewer_prompt.md`, so G8 and G9 are C3's whole evidence
    and a green suite says nothing about it.

G12 CHANGE SET AND HISTORY. Print the range's path set and confirm it equals the
    Change list above other than `.agent/handoff.md`, with no path on either side
    alone. Confirm every path the Change section FORBIDS is PRESENT at `39bfc199`.
    Confirm the range is linear — every commit at exactly one parent — that the
    round's `git reflog` entries are all `commit:`, and report each commit's
    INSERTION count (the `+` column only, per DECISION F104 D1), none over 500.

G13 THE HANDBACK, BOTH HALVES, per §3 item 14. Report `wc -l` of
    `.agent/handoff.md` at C4 and again at C5, and confirm each against the bound
    CONSTRAINT 8 states for it — this gate deliberately names that constraint
    rather than restating its numerals. All seven mandated headings of
    docs/agents/handback_template.md are present in the template's order and no
    section is dropped. The prefix-and-remainder equality against VERDICT is
    measurable only after C5 and goes in the round report.

G14 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Then
append VERDICT verbatim as C5. Push the branch once, after C5.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN24>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs to
its closure round. `.agent/live_review.md` is the source of truth for the open set,
for the next free finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R24: record R23's verdict, register the three defects R23 exposed — R-0589 a
constant stated twice and corrected once, R-0590 a gate whose conditional
discharged itself, R-0591 an ordered recipe whose default broke the parity it was
meant to restore — and promote all three counter-measures onto the §3 checklist,
where a rule has to live to bind the next block.

## Next Steps
1. THE INTEGRATION GATE IS DONE and it is GREEN: at R23 the branch full suite ran
   17192 passed / 20 skipped / 0 failed, the branch-only failure set was EMPTY, and
   all 23 base-only ids were attributed to the throwaway worktree's missing build
   artefacts by demonstration at `76661dc1`. Evidence: `.agent/gate_f086_r23/`.
2. CLOSURE is the next substantive round, per docs/roadmap/STATUS_closure_protocol.md
   — evidence job, FRESH review zip, the STATUS line, the PR. The packaging ist-doc
   is written there, when the built state stops moving.
3. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has yet paid
  down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN24>>>

<<<SLICE FIND0589>>>
- R-0589 — Low — A CONSTANT THE BLOCK COMPUTED FOR ITSELF WAS STATED IN TWO CLAUSES AND CORRECTED IN ONLY ONE, SO THE BLOCK ORDERED A READING NO ROUND COULD MEET. The R23 block, committed at `67224395`, re-measured its own VERDICT slice after a trim, found 44 lines rather than the 43 an earlier draft carried, and corrected constraint 9 to read 44 with a C4 bound of 56. Gate G15 of the same block carried both numerals too and was not swept: it still ordered `.agent/handoff.md` "at C4 is at most 57" and "at C5 it is exactly (a) plus 43, at most 100". Measured over the landed round: VERDICT is 44 lines, C4 is 56 and C5 is 100, the prefix-and-remainder equality holds exactly and the remainder is byte-equal to VERDICT — so constraint 9 was met precisely while G15's second half was unmeetable for every possible round, and the two clauses of one block disagreed on both numerals. The worker applied the block as written, met constraint 9, and spent a declared deviation demonstrating the contradiction; that is the correct handling and nothing false reached disk. WHY LOW: the two bounds are compatible where it mattered — 56 satisfies both "at most 56" and "at most 57" — so no wrong value landed and the only cost was the deviation. THE CLASS IS NOT NEW AND THAT IS THE POINT: R-0486 and R-0488 record that correcting a count is exactly where the next wrong count lands, and this instance happened INSIDE the round whose own item 14 clause requires the block to compute the constant. Computing it once and stating it twice is what item 14 as worded permits. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: item 14 gains the rule that a self-computed constant is stated ONCE and named elsewhere, and that where it must be repeated every occurrence is re-grepped after the last edit. This block is the first to obey it — its constraint 8 holds the arithmetic and its G13 names that constraint instead of repeating the numbers.
<<<END FIND0589>>>

<<<SLICE FIND0590>>>
- R-0590 — Medium — A GATE MADE ITS OBLIGATION CONDITIONAL ON A GUARD THAT TURNED OUT FALSE, SO IT DEMANDED NOTHING OF TWENTY-THREE REAL FAILURES. The R23 block, committed at `67224395`, ordered in G10: "For every BASE-ONLY id: if the parity claim went VOID, attribute it to its environment class BY DIRECT EVIDENCE, naming the missing or rebuilt artifact PER ID". The guard encoded a false implication. Parity is a statement about what the base RUN rebuilt; the base-only failure set is a statement about what the base worktree LACKS; the two are independent, and at R23 parity HELD on both digest and mtime while 23 base-only ids existed. Under the gate as written those 23 ids carried no attribution obligation at all, even though docs/agents/integration_gate.md step 3 makes the obligation UNCONDITIONAL — "either restore parity before the base run, or attribute EVERY `comm -23` id" — and rules that an unattributed id counts as a genuine base failure and blocks the gate verdict. The gate would have been satisfied by silence over exactly the evidence the integration gate exists to produce. WHY MEDIUM RATHER THAN LOW: this is a gate that cannot fail, the R-0438 vacuous-gate class, and it sat on the feature's tier-3 verdict rather than on a document; had the worker read it narrowly, F086's integration gate would have shipped with 23 unexplained base failures and the reviewer's own re-run would have been the only thing standing between that and closure. WHAT SAVED THE ROUND was the worker, which attributed all 23 anyway — by DEMONSTRATION, repairing each artefact in the throwaway worktree and re-running the ids at `76661dc1` — declared that it had gone beyond the gate, and named integration_gate.md step 3 as its authority. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: a new checklist item 27 requires every conditional done-when to be read against the case where its condition is FALSE, and the condition dropped rather than narrowed wherever the obligation survives it.
<<<END FIND0590>>>

<<<SLICE FIND0591>>>
- R-0591 — Low — A BLOCK ORDERED THE MECHANISM AND NOT ITS ARGUMENT, AND THE MECHANISM'S DEFAULT DESTROYED THE PROPERTY THE GATE EXISTED TO ESTABLISH. The R23 block, committed at `67224395`, ordered in G9 that `apps/ui/node_modules` and `apps/ui/dist` be restored into the base worktree by COPY, "with `shutil.copytree` — NEVER symlink", to give the base run artefact parity with the primary checkout. `shutil.copytree` defaults to `symlinks=False`, which DEREFERENCES symlinks rather than preserving them, and npm's bin shims under `apps/ui/node_modules/.bin` are symlinks: the copy turned 23 of them into regular files whose relative imports then resolved from `.bin/` instead of from the package directory. Seven of R23's 23 base-only failures were CAUSED by the restore step itself, with `ERR_MODULE_NOT_FOUND: Cannot find module '<base-wt>/apps/ui/node_modules/dist/node/cli.js' imported from '.../.bin/vite'` in the base log as direct evidence. Measured by the worker: 23 symlinks under `apps/ui/node_modules` at maxdepth 2 in the primary checkout, 0 in the copy; after a re-copy with `symlinks=True` all seven ids PASSED at `76661dc1`. THE PRECEDENT WAS RIGHT AND THE BLOCK DROPPED IT: `.agent/gate_f085_r72/base_parity.txt` records "shutil.copytree, symlinks preserved", and the R23 block kept the citation while losing the qualifier — which is how a correct precedent becomes an incorrect order. WHY LOW: nothing false reached disk, the gate's verdict is unaffected because all seven were attributed and demonstrated to pass at base, and the cost was wasted base-run failures plus a declared deviation. The `symlinks=True` reading is safe here and the block should have said so: these shims point WITHIN `node_modules` and never into the primary checkout, so the F053 R3 write-through hazard the "NEVER symlink" clause guards against does not reach them. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: item 18 widens from a red-proof's two halves to ANY ordered recipe read against the property it must establish, using the mechanism's real defaults rather than its intent.
<<<END FIND0591>>>

<<<SLICE RECORD22>>>
Gate: R24 — the R23 entry. R23 PASSED, and F086'S INTEGRATION GATE IS GREEN. Every gate R23's block ordered was RE-EXECUTED by the reviewer over `43e7f1e0..39bfc199` rather than read from the handback, and every reading reproduces. THE GATE ITSELF, which is this round's point: the reviewer re-ran the full suite in the primary checkout and read 17192 passed, 20 skipped, exit 0 — the same 17192/20 the worker recorded in `branch_meta.txt`, from an independent run — so `branch_failed.txt` is empty, `comm -13` is empty, and THE BRANCH-ONLY FAILURE SET IS EMPTY BY CONSTRUCTION rather than by interpretation. The base run at `76661dc1` failed 23 ids and every one is attributed in `attribution.txt` with none silently absent, in two classes, and attributed by DEMONSTRATION rather than hypothesis: 7 to npm bin shims dereferenced by the block's own restore step, which PASSED at base once re-copied with `symlinks=True`, and 16 to `_frontend_is_stale()` calling the copied `apps/ui/dist` stale because `git worktree add` stamps sources newer than it, which PASSED at base once the dist mtime was corrected without a rebuild. That is a stronger reading than docs/agents/integration_gate.md step 3 requires, which asks only for the artefact to be named per id. THE PARITY CLAIM HELD ON BOTH HALVES — digest and mtime, base worktree and primary, all four readings identical before and after at sha256 c14681f28e79a0c908642a03ceeda315b5d5150f079860fe20fcfbc9d3a26873 — so nothing was rebuilt during the base run, which at F085 R72 it was. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r23.md`, the committed `.agent/authored/f086-r23.md` at `67224395` and the committed `.agent/last_block.md` at `17e60f3a` are byte-EQUAL at sha256 886e7b86b10ac302f6f4299ead87433440399aea4a073cb90c52e42bf02fc52d, 25631 B over 334 lines. EVERY SLICE LANDED BYTE-EXACT, each checked disk-to-disk against an extraction from the COMMITTED C0a: `.agent/plan.md` at `c24aa05e` equals PLAN23 at sha256 63533396d445866a0aab7f30d44b79f7b6caae5d9d683f116a123e4b02b6de68 over 44 lines, under the AGENTS.md cap of 50 and carrying `## Goal`, `## Next Steps` and `F086`; and the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, RECORD21, a blank line and DONE0588 at sha256 93d27a26788e3e7fd0aec74f7aff9dde171c2c4bc5de0369475be23d8f0c90a7. THE LEDGER MOVED ONLY ON THE RESOLVED SIDE: both extractions AGREE at each end — 171 registered / 3 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 168 open at `43e7f1e0`, and 171 / 4 / 0 / 0 / 0 / 167 at `181ade7e` — the registered SETS are equal, the resolved set gains exactly `R-0588`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`. R-0586'S SCAN HELD WITH ITS CONTROL BITING: over the lines `181ade7e` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0, while the same two-step extractor over `fd166295`'s added lines reads 3. R-0587'S CHECK HELD IN THE FORM THAT LETS A LANDED DEFECT STAND: the duplicated-header SET is unchanged and is exactly `Gate: R19 — the R18 entry.`; `Gate: R23 — the R22 entry.` occurs 1x, is the LAST such header, and the text after it begins `R22 `. THE HYGIENE HELD: five state paths plus twelve new gate-evidence files over seven single-parent commits inserting 334, 285, 14, 4, 243, 32 and 44 lines, none over 500 and no DECISION F104 D1 exemption invoked; all six paths the block FORBIDS exist at `43e7f1e0` and none is touched; every `git reflog` entry of the round is `commit:`; no marker line reached any target; the throwaway worktree and its branch `tmp/base-gate-r23` are both gone and `git worktree list` is one line; and the tree is clean at `39bfc199`, which is also what `origin` holds. THE HANDBACK IS 56 LINES AT C4 AND 100 AT C5, the first a byte-exact prefix of the second with a 44-line remainder byte-equal to VERDICT, all seven mandated headings present in the template's order. WHERE R23 WENT WRONG IS IN NONE OF THE WORKER'S WORK BUT IN THREE PLACES IN ITS BLOCK, and the worker declared all three rather than quietly routing around them: G15 carried numerals constraint 9 had corrected (R-0589), G10 made the base-only attribution conditional on a parity failure that did not occur (R-0590), and G9 ordered `shutil.copytree` without the `symlinks=True` its own precedent records, causing seven of the base-only failures it was meant to prevent (R-0591). A round whose only defects are the reviewer's, all declared by the worker and none reaching disk, is the split doing exactly what it exists for.
<<<END RECORD22>>>

<<<SLICE CHECK14FROM>>>
      which is which.
<<<END CHECK14FROM>>>

<<<SLICE CHECK14TO>>>
      which is which.
      Finding R-0589 adds the SWEEP this item's arithmetic needs and does not state. A
      constant the block computes for ITSELF — an appended slice's length, and the bound
      on the earlier commit derived from it — is stated ONCE, in one clause, and every
      other clause NAMES that clause rather than repeating its numeral. Where a numeral
      genuinely must appear twice, every occurrence is re-grepped after the LAST edit and
      before emission, because correcting one occurrence is precisely where the next wrong
      one lands: R-0486 and R-0488 are that shape, and this instance arrived inside the
      round whose own clause above requires the block to compute the constant. Computing
      it once and stating it twice is what this item as first written permits. The R23
      instance: the block re-measured its VERDICT slice at 44 lines after a trim, corrected
      constraint 9 to 44 with a C4 bound of 56, and left gate G15 ordering "at most 57" and
      "exactly (a) plus 43" — so one block held both numerals twice and the second copy was
      unmeetable for every possible round, while the handback landed at 56 and 100 and met
      the corrected clause exactly.
<<<END CHECK14TO>>>

<<<SLICE CHECK18FROM>>>
      the node must FAIL and name `wall_timeout`".
<<<END CHECK18FROM>>>

<<<SLICE CHECK18TO>>>
      the node must FAIL and name `wall_timeout`".
      Finding R-0591 widens this item from a RED-PROOF's two halves to ANY ordered recipe
      and the property that recipe is ordered to establish. A block that names a MECHANISM
      — a copy call, a flag, an environment variable, a shell builtin — is read against
      what the mechanism must PRESERVE, using its real defaults rather than its intent, and
      the argument that carries the property is named in the order rather than assumed. The
      R23 instance: G9 ordered `apps/ui/node_modules` restored into a base worktree "with
      `shutil.copytree` — NEVER symlink" to give the base run artefact parity, and
      `copytree` defaults to `symlinks=False`, so it dereferenced npm's 23 bin shims and
      CAUSED 7 of the 23 base-only failures the parity existed to prevent. The repository's
      own precedent had it right — `.agent/gate_f085_r72/base_parity.txt` reads "symlinks
      preserved" — and the block kept the citation while dropping the qualifier, which is
      how a correct precedent becomes an incorrect order. Where a mechanism's DEFAULT is
      the hazard, order the argument, not the function.
<<<END CHECK18TO>>>

<<<SLICE CHECK27FROM>>>
      item 20 forbids.
<<<END CHECK27FROM>>>

<<<SLICE CHECK27TO>>>
      item 20 forbids.
  27. **A conditional gate is read against the case where its condition is FALSE.** Finding
      R-0590. A done-when of the form "if X, then attribute / report / prove Y" is checked at
      emission against NOT-X, and wherever the obligation Y survives that case the condition
      is DROPPED rather than narrowed. A gate that discharges itself the moment its guard
      fails is indistinguishable on the page from one that binds, and it fails silently and
      in the safe-looking direction — the vacuous-gate class of R-0438, arriving through a
      guard rather than through a missing path. Item 8 checks a gate's expected VALUE against
      the code and item 18 reads an ordered recipe against the property it must establish;
      neither reaches this one, because the value is right and the recipe is sound and only
      the REACHABILITY of the demand is wrong. The R23 instance: G10 ordered every base-only
      failure attributed by direct evidence "if the parity claim went VOID", and at that round
      parity HELD on both digest and mtime while 23 base-only ids existed — the two are
      independent, parity being a statement about what the RUN rebuilt and the base-only set
      about what the base LACKS — so the gate demanded nothing of 23 real failures, over
      exactly the evidence an integration gate exists to produce.
      docs/agents/integration_gate.md step 3 makes that attribution unconditional, and the
      worker attributed all 23 by demonstration on its own initiative and said so, which is
      the round rescuing the reviewer rather than the gate doing its job.
<<<END CHECK27TO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk cannot be
told apart from one never issued. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming at `43e7f1e0` under a three-round cap
declared up front per guardrail G7. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and every verdict below rests on gates the
reviewer RE-EXECUTED over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R22 | e7cdae4d..43e7f1e0 | PASS — no finding |
| R23 | 43e7f1e0..39bfc199 | PASS — three findings, all against the reviewer |
| R24 | 39bfc199..HEAD | verdict not yet on disk; see the last paragraph |

R22 was inherited ungated, so Phase 1 rule 4 reviewed it before any new work was
planned. It produced NO finding, and it closed R-0588 in the strong form: R22 landed
that finding's counter-measure into §3 item 14 and its own handback was then bounded by
the rule it had just written.

R23 IS THIS FEATURE'S INTEGRATION GATE AND IT IS GREEN. The reviewer re-ran the full
suite independently and read 17192 passed, 20 skipped, exit 0 — matching the worker's
own run — so the branch-only failure set is empty by construction. All 23 base-only
failures were attributed by DEMONSTRATION at `76661dc1`, stronger than
docs/agents/integration_gate.md step 3 asks for. Only the integration-gate round may
claim "full suite green" (§4.6); this one may, and does.

R23's three findings are ALL DEFECTS OF THE REVIEWER'S OWN BLOCK TEXT and none is in the
worker's execution: R-0589 a self-computed constant stated twice and corrected once,
R-0590 a gate whose conditional discharged itself over 23 real failures, R-0591 an
ordered recipe whose default destroyed the parity it was meant to restore. THE WORKER
DECLARED ALL THREE, applied each slice verbatim as constraint 1 required, and went
BEYOND the vacuous gate to attribute the evidence the feature actually needed — an
independent executor catching three reviewer defects that no gate the reviewer wrote
could have caught, because the reviewer wrote the gates.

WHAT THIS FEATURE STILL OWES: closure alone. NO INSTALL HAS BEEN PROVEN in this session
or any other and no round of this workflow can prove one; DECISION F086 D4 records that
with its measurement, the release workflow has never been dispatched, and closure names
both as unproven rather than counting a skipped test as coverage.

R24 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last verdict to
be recorded (R-0583). THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then rule 2,
then rule 4: review `39bfc199..HEAD` and record R24's verdict as `Gate: R25 — the R24
entry.`, the header shape §3 item 26 binds. Its first substantive work is closure.
<<<END VERDICT>>>
