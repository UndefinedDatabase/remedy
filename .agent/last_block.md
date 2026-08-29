# STEP R5/F040 — T001'S LAST ACCEPTANCE CLAUSE: THE ENVELOPE GOLDENS

Goal: meet the acceptance criterion T001 has carried unmet since it was
sliced — "Fixture goldens exact" — with one stored envelope per state shape,
and book the round 4 verdict, finding R-0754 and DECISION F040 D6.

Base: `458e8d51`, the round-4 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

WHY THIS ROUND EXISTS, so the worker knows what it is repairing. Round 4's
gates were all green and its work was correct, but `docs/roadmap/features/
T5_F040.md:76-78` slices T001 as "the endpoint composition + rule-table import
+ fixtures per state shape ... + goldens", and its Acceptance at :86 opens
"Fixture goldens exact". The fixtures exist and the composition is pinned
field by field; NO GOLDEN EXISTS. Round 4's plan slice quietly narrowed the
item from "the endpoint, its route tests and goldens" to "the endpoint and its
route tests" and declared T001 complete. That narrowing is the REVIEWER's, not
any worker's — the round-4 worker applied the slice byte for byte, as its
constraint 1 required, and declared no departure because none was asked of it.
This round closes the clause instead of arguing it away.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r5.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN5
- C2  append slice RECORD5 to `.agent/live_review.md`
- C3  add the four goldens AND the golden section of
      `tests/orchestration/test_job_digest.py`, per the SPEC below
- C4  apply pair PAIRACCEPT to `docs/roadmap/features/T5_F040.md`
- C5  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r5.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/orchestration/fixtures/job_digest/golden/green.json
    tests/orchestration/fixtures/job_digest/golden/blocked_with_decisions.json
    tests/orchestration/fixtures/job_digest/golden/budget_stopped.json
    tests/orchestration/fixtures/job_digest/golden/mid_run.json
    tests/orchestration/test_job_digest.py
    docs/roadmap/features/T5_F040.md
    .agent/handoff.md

NO PRODUCTION CODE CHANGES THIS ROUND. `packages/orchestration/job_digest.py`
and `packages/orchestration/ui_server.py` are NOT edited: the goldens record
what the composition already produces. If a golden cannot be made to match
without editing production code, STOP and say so in the handback — that would
mean the composition is wrong, which is a finding and not a thing to paper over
by editing the module until the golden agrees.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. If one looks wrong, apply it as
   given and DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r5-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` is APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. Mutation and red-proof checks run ONLY in a disposable `git worktree`;
   purge `__pycache__` and use `python3 -B`. The primary checkout is
   `git status --porcelain` empty at every reading.
8. C3 IS ONE COMMIT holding the four goldens and their reader. A golden with no
   reader is dead data and a reader with no goldens is a red commit on the
   branch.
9. THE GOLDENS ARE GENERATED ONCE AND THEN FROZEN. The test that reads them
   NEVER writes them — no write mode, no `write_text`, no `json.dump` to the
   golden directory, no "regenerate" flag or environment switch. A golden a
   test re-blesses on mismatch checks nothing; `tests/orchestration/
   test_cost_report.py:13` states that rule and this round inherits it.
10. THE NORMALIZATION IS THE NARROWEST THAT MAKES THE COMPARISON STABLE, and
    every normalized value is an IDENTITY, never content. Exactly three
    substitutions are permitted, and each is measured below. Normalizing a
    headline, a label's WORDS, a rule id, a count or an urgency number would
    make the golden vacuous and is forbidden.
11. The `remedy` console script is DENIED to this session; use
    `python3 -m apps.cli.main ...` if needed and say so.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
13. Push after C5. No pull request, no merge, no force-push.
14. Pair shape, measured: PAIRACCEPT `TO contains FROM: true` — APPEND-shaped,
    so its obligation is FROM exactly 1x plus the TO-only lines exactly 1x
    among the lines C4's diff ADDS, and NEVER a FROM-zero count.

## SANDBOX NOTES — read these before writing a script, they cost earlier
## workers whole rounds

- Env-var assignment is DENIED in all three shell forms (`VAR=x cmd`,
  `env VAR=x cmd`, `export VAR=x; cmd`). Set it in-process with
  `os.environ[...]` or with `monkeypatch.setenv` inside a test.
- `cp` is denied; copy with `shutil.copyfile`.
- `$(...)` inside a compound, `;`/`&&` chains, and process substitution are
  rejected by FORM. One command per call, or a driver script run as a single
  `bash script.sh`, or `python3 - <<'PY'`.
- The Bash tool does not surface non-zero exits; capture them as
  `subprocess.run(...).returncode` inside a Python driver.

## Slices

The authored units are PLAN5, RECORD5 and the two halves of PAIRACCEPT, each
between its own BEGIN and END marker line. The markers are NOT part of the
unit; the newline ENDING the last content line IS.

<<<BEGIN PLAN5
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 5.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D5 | done | rounds 2 and 3 |
| the one-source urgency and R-0751 | done | round 2, PASS |
| T001 the composition module and its tests | done | round 3, PASS |
| T001 the endpoint and its route tests | done | round 4, PASS |
| T001 the envelope goldens and R-0754 | done | this round |
| T002 the hero card, triggers, the TS retirement | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round meets T001's last acceptance clause: one stored envelope golden
   per state shape, frozen and never self-blessed. T001 is complete when it
   lands — the goldens were the clause round 4 left open.
2. T002 builds the hero card against the design reference, wires the trigger,
   dismiss and last-seen mechanics, and retires the TypeScript urgency copy per
   DECISION F040 D2.
3. T003 adds `remedy job digest` and the end-to-end, then the integration gate
   and closure.

## Risks
- R-0570, R-0752 and R-0753 stay OPEN. The first two are routed to the paydown
  branch; R-0753 is a documented risk this feature carries, because the persisted
  actuals record has no money field for the digest's cost basis to read.
- Two homes for the urgency formula exist until T002, pinned equal by
  `tests/ui_contracts/test_decision_urgency_parity.py` rather than trusted.
<<<END PLAN5

<<<BEGIN RECORD5
Gate: F040 R4 — T001 PART 2, THE DIGEST ENDPOINT. VERDICT PASS. Reviewed by re-running every gate in the reviewer's own driver rather than reading the handback's numbers, and every figure the worker reported reproduced exactly. TRANSPORT is REAL: all three copies equal at sha256 `0fbcdaa55a4219804489248f5c3d45a4f5114ae9d3e518838ba1d1440eb374e4` over 18243 bytes. THE PLAN is byte-equal to PLAN4 at 1786 bytes and 38 lines. THE RECORD APPEND reconstructs whole at 1662667 + 1 + 5385 = 1668053 with N counted as 2 and paragraph order holding, and the base is a prefix of the committed file, so the append is append-only by construction. THE LEDGER moved as ordered — registered 313 to 314 with ADDED `['R-0753']`, resolved ADDED `[]` and REMOVED `[]`, exactly one `^Gate: F040 R3 — ` line, `^Done:` zero for R-0570, R-0752 and R-0753, open count 261. THE WIRING is measured at BOTH ends, which the block asked for and which matters here: at the base `2b063387` the `handlers` dict literal sits at line 3452 with FIFTEEN keys and `_build_digest_json` occurs ZERO times, and at HEAD the same literal sits at 3459 with SIXTEEN distinct keys and the builder name occurs exactly twice, its definition and its registration; the exact string `"digest": _build_digest_json,` occurs once; `ruff check` and `compileall` are both REAL exit 0. THE REVIEWER RE-PROVED THE RED PROOF IN ITS OWN WORKTREE AND ADDED A SECOND MUTATION THE BLOCK DID NOT ORDER, control first in both cases. M1, deleting the 46-byte registration line the worker deleted: unmutated 7 passed at REAL exit 0, mutated REAL exit 1 at 4 failed and 3 passed, restored 7 passed — reproducing the worker's split exactly, and the three survivors are the ones that must survive, since the unknown-job 404, the neighbour 404 and the invalid-token 403 are all answered before dispatch reaches the handlers dict. M2, the reviewer's own, aimed at the property the round actually claims: adding one key to the builder's returned payload gave REAL exit 1 at 2 failed and 5 passed, and the two that died are `test_digest_endpoint_is_a_pass_through_of_the_composition` and `test_digest_body_carries_exactly_the_envelope_key_set` — so the pass-through assertion BITES, and block constraint 9 is enforceable rather than aspirational, which is the whole point of the round. THE REQUIRED RISE was measured at both ends by the reviewer rather than taken from the record: `tests/ui_server/` collects 508 at the base and 515 at HEAD, a difference of exactly the 7 tests C4 adds. Six suites re-run serially, every one REAL exit 0: 515, 40, 699 passed with 4 skipped, 16, 21 and 42. The tree is clean, untracked count 0, seven commits with one path each at insertions 257, 177, 16, 4, 8, 161 and 288, every one under 500, no subject carrying a leading-slash token, an absolute path or a secret-like string, and no `Co-Authored-By` trailer anywhere. THE WORKER'S ELEVEN DEVIATIONS WERE ALL CORRECTLY DECLARED and two were checked at their source: the merge-base IS `f5b1e6c5` with the subject `Merge pull request #222`, and the block's own "the dict at line 3467" IS the imprecision the worker named — 3467 was the pair's FROM anchor and the last entry of the dict, while the dict's assignment was at 3452 — declared rather than silently corrected, which is the right handling of a block that is slightly wrong about its own target. ONE THING THE ROUND DID NOT DO, and it is the reviewer's fault rather than the worker's: see R-0754 below. The verdict is PASS because the round built what it was ordered to build and built it correctly; the missing clause was never ordered.

- R-0754 — Medium, T001 WAS DECLARED COMPLETE WITH ONE OF ITS ACCEPTANCE CLAUSES NEVER BUILT AND NEVER DISCHARGED, AND THE PLAN TEXT WAS NARROWED IN THE SAME ROUND THAT DECLARED IT DONE. Raised by the reviewer at the F040 R4 gate, against its own earlier authoring. THE MEASUREMENT at `458e8d51`: `docs/roadmap/features/T5_F040.md:76-78` slices T001 as "the endpoint composition + rule-table import + fixtures per state shape (green, blocked-with-decisions, budget-stopped, mid-run) + goldens", and its Acceptance at :86 opens "Fixture goldens exact". The four fixtures exist and are parametrized over in `tests/orchestration/test_job_digest.py`; NO GOLDEN EXISTS — `find tests -ipath "*digest*golden*"` returns nothing, and the only occurrence of the word in that file is line 12, a docstring sentence arguing against one. The narrowing is on the record and is precise: round 3's plan carried the item "T001 the endpoint, its route tests and goldens | open | next round", and round 4's PLAN4 slice rewrote it to "T001 the endpoint and its route tests | done | this round". No DECISION discharged the clause between those two rounds — D1 through D5 settle the F033 candidates, the urgency home, ownership, the cost basis and the deep link, and not one of them mentions goldens. THIS IS THE REVIEWER'S DEFECT AND NOT ANY WORKER'S: the R4 block ordered no golden and its fourteen constraints named none, and the R4 worker applied PLAN4 byte for byte exactly as constraint 1 required. WHY MEDIUM: nothing on disk is wrong-valued and no test is false, so no running code misbehaves — but a feature file under `docs/` carries an acceptance criterion the feature had stopped intending to meet, and closure reads that list, so the gap would have surfaced as a closure blocker several rounds later with the cheap moment to fix it long past. It is also a gate-blindness of the kind §3 exists to catch: seven green gates in R4 and eight in R3, and not one of them measured T001 against its own acceptance text. WHY IT IS NOT ARGUED AWAY: the docstring sentence at `test_job_digest.py:12` — "A golden would keep passing while the digest and the report drifted apart" — is a correct argument about ONE field, the CTA label, and it is answered by keeping the one-source test rather than by dropping the goldens; it is not an argument against pinning the envelope, and this repository already runs exactly that convention for this surface's sibling at `tests/orchestration/fixtures/cost_report/golden/`. The open set was searched for the defect before this id was minted, per §3 item 30: `R-0411` is the nearest shape — a feature file naming five frozen orders where three were built, registered against the plan and discharged by a DECISION — but it names F082 and its bench orders, so the evidence does not join it. FIXED IN THE SAME ROUND THAT REGISTERS IT, by DECISION F040 D6 below and the goldens it specifies. The counter-measure, binding the reviewer from R6 on: a block whose plan slice marks a T-slice `done` states, in the block itself, the feature file's acceptance clauses for that slice and where each one is met — a T-slice is complete against its acceptance text, never against a plan row the same block rewrote.

DECISION F040 D6 — "FIXTURE GOLDENS EXACT" IS MET BY ENVELOPE GOLDENS WITH THREE NORMALIZED IDENTITIES AND NOTHING ELSE NORMALIZED. THE PROBLEM: T001's acceptance clause asks for exact fixture goldens over a composition whose envelope carries values that differ on every build, so a naive golden would be flaky and an over-normalized one would be vacuous. MEASURED by the reviewer at `458e8d51`, by building all four shapes twice in one process: the ONLY unstable top-level key for `green`, `budget_stopped` and `mid_run` is `job_id`, and for `blocked_with_decisions` it is `job_id` and `primary_action`, because that shape's label embeds both the job id's first eight characters and a `td:` decision id — `Answer the open decision: ` followed by a `remedy decision resolve <prefix> td:<hex>` command. Everything else — the headline sentences, the state strings, the cost value and basis, the empty ownership list, the open counts, the peak urgency and the rule ids — is byte-stable under the module's own autouse `_frozen_inbox_clock` and `_isolated_data_root` fixtures. CHOSEN: one stored JSON per shape under `tests/orchestration/fixtures/job_digest/golden/`, compared WHOLE against the freshly built envelope after exactly three substitutions — the job's full UUID, the job's first-eight-character prefix, and each `td:<hex>` decision id — each replaced by a fixed placeholder everywhere it occurs, including inside strings. Nothing else is substituted, and the goldens live beside the shape fixtures in the module that owns the frozen clock, because the determinism the comparison depends on comes from that module's autouse fixtures and would not follow the test into a new file. The one-source CTA test STAYS exactly as it is: the golden pins the rendered envelope and the one-source test pins the agreement with the report, and a label change reddens both — which is the answer to the `test_job_digest.py:12` objection, since that sentence argues against a golden REPLACING the one-source assertion and not against one standing beside it. ALTERNATIVES CONSIDERED: (a) discharge the clause by decision and build no golden, on the strength of the field-by-field assertions already in place — rejected, because those assertions were written from the same reading of the code that produces the values and share its blind spots, and because the blocked shape's label leaking a job-id prefix and a decision id into published copy is exactly the class a whole-envelope comparison catches and a field-wise one does not; (b) normalize the entire `primary_action.label` — rejected as vacuous, since the label's WORDS are the CTA the acceptance criterion is about; (c) store the goldens under a new test module — rejected, the frozen clock is autouse in `test_job_digest.py` and a golden that depends on a fixture it does not inherit is a flake waiting for a slow machine. HOW TO REVERSE: delete the four files and the golden section; nothing imports them. WHAT IT COSTS TO BE WRONG: four small JSON files to re-generate by hand, and the re-generation is deliberately manual — no flag, no environment switch, no self-blessing path — because a golden a test can rewrite on mismatch is not a golden.
<<<END RECORD5

<<<BEGIN PAIRACCEPT-FROM
## Acceptance
- Fixture goldens exact; the CTA equals the report's recommended
  action per fixture (the one-source test). Cost basis treatment
  matches the ticker's. Dismissal persists; new activity re-arms.
  Absence detection never claims more than last-seen truth (copy
  audit: "since you were last here" not "while you slept").
<<<END PAIRACCEPT-FROM

<<<BEGIN PAIRACCEPT-TO
## Acceptance
- Fixture goldens exact; the CTA equals the report's recommended
  action per fixture (the one-source test). Cost basis treatment
  matches the ticker's. Dismissal persists; new activity re-arms.
  Absence detection never claims more than last-seen truth (copy
  audit: "since you were last here" not "while you slept").
  AMENDMENT A3 (DECISION F040 D6, 2026-08-29): "fixture goldens
  exact" is met by ENVELOPE goldens — one stored JSON per state
  shape under `tests/orchestration/fixtures/job_digest/golden/`,
  compared WHOLE against the envelope the same fixture builds.
  Exactly three identities are normalized first, because they
  differ on every build: the job's UUID, the job's first-eight
  prefix, and each `td:` decision id, each replaced by a fixed
  placeholder everywhere it occurs including inside strings.
  Nothing else is normalized — headlines, labels, rule ids, counts
  and urgencies are compared as they are — and the test never
  writes a golden.
<<<END PAIRACCEPT-TO

## SPEC for C3 — the four goldens and their reader

Read `tests/orchestration/test_cost_report.py` around lines 453-470 first for
the convention this repository already uses for a stored golden, and
`tests/orchestration/test_job_digest.py` end to end for the module you are
extending. Follow both; invent no new harness.

THE FILES. Four JSON goldens under
`tests/orchestration/fixtures/job_digest/golden/`, named for the shape
constants the module already defines: `green.json`,
`blocked_with_decisions.json`, `budget_stopped.json`, `mid_run.json`. Each
holds the NORMALIZED envelope its shape builds, pretty-printed with a trailing
newline so a diff is readable. GENERATE them by running the composition — never
by typing them — then read the generated files back and check them by eye
against the shape fixture before committing.

THE READER, appended as a new section at the END of
`tests/orchestration/test_job_digest.py`, under a section comment in the
style the module already uses for its other sections:

- a module-level `GOLDEN_DIR` pointing at the directory, in the manner
  `test_cost_report.py` defines its own;
- a `_normalize(envelope, job)` helper performing EXACTLY the three
  substitutions DECISION F040 D6 names — the job's full UUID, the job's
  first-eight-character prefix, and every `td:<hex>` decision id — each to a
  fixed placeholder, applied recursively so occurrences INSIDE strings are
  reached. Give it a one-line WHY comment saying that these are identities and
  that nothing else may be added to the list;
- one test parametrized over `SHAPES` asserting the normalized envelope EQUALS
  the parsed golden for that shape;
- one test asserting the golden DIRECTORY holds exactly four files and that
  their names are exactly the four shape names — so a shape added later without
  a golden fails here rather than being silently unpinned;
- one test asserting the normalization is NARROW: for the
  `blocked_with_decisions` shape, the normalized label still contains the words
  `Answer the open decision` and the token `remedy decision resolve`, so a
  future widening of `_normalize` that swallowed the CTA's wording reddens.

Per constraint 9 the section contains no write path of any kind.

## SPEC for C4 — the feature file

Apply pair PAIRACCEPT. It appends AMENDMENT A3 to the Acceptance bullet,
following the shape amendments A1 and A2 already use at :44 and :52 — the
amendment sits inside the bullet it amends, wrapped to the file's column width.
Nothing else in that file changes.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C5, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — `.remedy-wt/f040-r5-block.md`,
   the committed `.agent/authored/f040-r5.md` and `.agent/last_block.md` — with
   the byte length, all three EQUAL. This block states no expected digest.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN5 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1668053 at `458e8d51`. Base + one separator newline + RECORD5
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION against
   the entire committed file; (b) PARAGRAPH ORDER — the last N blank-line units
   equal RECORD5's N paragraphs IN ORDER, N COUNTED by your script. Also report
   that the base bytes are a PREFIX of the committed file. NEGATIVE CONTROL in a
   disposable worktree: flip one byte inside the FIRST appended paragraph and
   report that BOTH readings reject it and accept the unflipped bytes.

G4 THE LEDGER, at C2. Distinct `^- R-\d+ — ` ids before and after with ADDED
   exactly `['R-0754']` and REMOVED `[]`; ADDED resolved `[]`; exactly one
   `^Gate: F040 R4 — ` line; distinct `DECISION F040 D\d+` ids with ADDED
   exactly `['D6']`; `^Done: R-0753` and `^Done: R-0754` both 0. Report the open
   count.

G5 THE GOLDENS BITE, at C3. First
   `python3 -m pytest tests/orchestration/test_job_digest.py -q` — REAL exit 0
   with the passed count, and report the RISE from the 40 the reviewer measured
   at the base. Then, INSIDE A DISPOSABLE WORKTREE, control FIRST: report the
   unmutated exit code over that file, then MUTATE PRODUCTION CODE — change the
   text of ONE rule label in the next-action rule table that `green` resolves to
   (find it yourself; `primary_action.rule_id` for that shape is `all-green`) —
   and report the exit code and which tests died. At least the `green` golden
   test MUST die; report honestly whether the one-source CTA test died with it.
   Restore, re-run, report the restored exit code and that the bytes equal the
   original. Name the worktree, remove it, report `git worktree list` no longer
   holds it. This proves the goldens pin CONTENT and not merely shape.

G6 THE GOLDENS CANNOT SELF-BLESS AND THE NORMALIZATION IS NARROW, at C3. Two
   readings, both over the COMMITTED tree. (a) Parse
   `tests/orchestration/test_job_digest.py` with `ast` and report that the
   golden section contains NO call to `open` with a write mode, no `write_text`,
   no `write_bytes` and no `json.dump`, and that the string `GOLDEN_DIR` appears
   in no assignment target other than its own definition — quote the mechanism,
   not a claim. (b) In a disposable worktree, perturb ONE byte inside ONE stored
   golden — report which file and which byte — and report the REAL exit code
   with it perturbed and again after restoring. A golden the suite accepts when
   perturbed is not pinning anything.

G7 THE FEATURE FILE, at C4. PAIRACCEPT is APPEND-shaped: report FROM occurring
   exactly 1x in the committed file and each TO-only line occurring exactly 1x
   AMONG THE LINES C4's DIFF ADDS — do NOT count FROM to zero. Then report that
   `AMENDMENT A3` occurs exactly once in the file, that `AMENDMENT A1` and
   `AMENDMENT A2` each still occur exactly once, and that the file's Task
   slicing line for T001 is UNCHANGED by this round — the amendment records how
   the clause is met and does not delete the clause.

G8 THE SUITES AND THE TREE, at C4. Each its own REAL exit code:
   `python3 -m pytest tests/orchestration/test_job_digest.py -q`,
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/ui_contracts/ -q`,
   `python3 -m pytest tests/docs/ -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured 40, 515, 699 passed with 4 skipped, 16 and 42 at the base and did
   not measure `tests/docs/` this round — report what you find and, if it is not
   green, say so plainly rather than repairing it, since `tests/docs/` reads the
   feature file C4 edits and a red there is this round's business to REPORT.
   Then `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, and the per-commit insertion counts for C0a
   through C4, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat` and never from file line counts, the deviations, the
item-status table with every bundle item and every gate appearing exactly once,
and the next steps. State `SESSION 2` of F040 and round 5. No length cap. Record
that T001 is COMPLETE INCLUDING ITS GOLDENS CLAUSE with this round, name R-0570,
R-0752 and R-0753 as OPEN and R-0754 as registered-and-fixed in this same round,
and name the next action as T002 — the hero card, its trigger, dismiss and
last-seen mechanics, and the retirement of the TypeScript urgency copy per
DECISION F040 D2.
