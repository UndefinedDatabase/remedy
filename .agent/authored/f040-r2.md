# STEP R2/F040 — SETTLE THE THREE SPEC QUESTIONS AND LAND THE ONE-SOURCE URGENCY

Goal: book the round-1 verdict, register the one finding round 1 turned up,
settle by DECISION the three places where F040's Design cannot be built as
written, amend the feature file where those decisions change it, and land the
urgency formula in Python as its SINGLE home with a contract pin that stops the
TypeScript copy drifting from it.

Base: `6664bf5e5e88b11708e5f350f2da90222072a558`, the round-1 handback commit and
the tip of `feature/f040-completion-digest`. Stay on that branch; do not cut a
new one and do not open a pull request.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r2.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN2
- C2  append slice RECORD2 to `.agent/live_review.md`
- C3  append slice SLIP2 to `.agent/prose_slips.md`
- C4  apply pairs PAIR-OWNERSHIP and PAIR-TESTPATH to
      `docs/roadmap/features/T5_F040.md`
- C5  apply pair PAIR-COMMENT to `packages/orchestration/run_report.py`
- C6  add `decision_urgency` to `packages/orchestration/decision_inbox.py`
      per the SPEC below
- C7  add the unit tests to `tests/orchestration/test_decision_inbox.py`
- C8  add the parity pin `tests/ui_contracts/test_decision_urgency_parity.py`
- C9  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r2.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/roadmap/features/T5_F040.md
    packages/orchestration/run_report.py
    packages/orchestration/decision_inbox.py
    tests/orchestration/test_decision_inbox.py
    tests/ui_contracts/test_decision_urgency_parity.py
    .agent/handoff.md

NOTHING under `apps/` changes this round. In particular
`apps/ui/src/api/decisionOrder.ts` is NOT edited — DECISION F040 D2 below
schedules its retirement for T002 and this round only PINS it.

## Constraints

1. Apply every slice and every pair BYTE FOR BYTE. Do not fix, rewrap or improve
   one. If a slice looks wrong, apply it as given and DECLARE the problem in the
   handback's deviations.
2. C0a is a COPY, never a retype: the block is at `.remedy-wt/f040-r2-block.md`.
   Use `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append, because this
   round registers a finding and AGENTS.md's Commit Gate requires the plan to
   match the work before every commit.
4. `.agent/live_review.md` and `.agent/prose_slips.md` are APPEND-ONLY. Revise
   nothing already in either. R-0570's landed paragraph is not edited.
5. `.agent/plan.md` stays under 50 lines. PLAN2 is authored to fit.
6. Every exit code you report is REAL, from `subprocess.run(...).returncode` in a
   script under the gitignored `.remedy-wt/`. Never take one through a pipe.
7. The mutation red-proof of G7 runs ONLY inside a disposable `git worktree`, and
   the primary checkout satisfies `git status --porcelain` empty at every reading.
   Purge `__pycache__` and run `python3 -B` there, or a stale cache will answer
   instead of the mutated source.
8. `decision_urgency` is NEW PUBLIC API on a module the write door imports. Do not
   change `build_decision_inbox`'s return shape, its three added card keys, or
   `DECISION_INBOX_VERSION`. This round ADDS a function and nothing else in that
   file.
9. The `remedy` console script is DENIED in this sandbox; use
   `python3 -m apps.cli.grouped ...` if you need it and say so.
10. Commit subjects carry no leading-slash token, no absolute path and no
    secret-like string, and no `Co-Authored-By` trailer.
11. Push after C9. Open NO pull request.
12. Pair shapes, each measured and reported separately, not generalised:
    PAIR-OWNERSHIP `TO contains FROM: true` — APPEND-shaped, so its obligation is
    FROM exactly 1x plus each TO-ONLY added line exactly 1x AMONG THE LINES C4's
    DIFF ADDS, and NEVER a FROM-zero count. PAIR-TESTPATH
    `TO contains FROM: false` — a REWRITE, so FROM 0x and TO 1x after C4.
    PAIR-COMMENT `TO contains FROM: false` — a REWRITE, so FROM 0x and TO 1x
    after C5.

## Slices

The authored units are PLAN2, RECORD2, SLIP2 and the six pair halves. Each sits
between its own BEGIN and END marker line; the markers are NOT part of the unit,
which starts on the line after BEGIN and ends with the newline before END.

<<<BEGIN PLAN2
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, round 2.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the two F033 closure candidates | done | round 1; no id spent |
| the F040 claim and the seam inventory | done | round 1, PASS |
| the three spec decisions D2, D3 and D4 | done | this round |
| the one-source urgency in Python and its pin | done | this round |
| R-0751, the stale rule-table comment | done | this round |
| T001 the endpoint composition | open | next round |
| T002 the hero card, triggers and the TS retirement | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round settles the three questions the inventory raised, amends the
   feature file where they change it, and lands `decision_urgency` in Python as
   the single home of the formula.
2. The round after it builds the digest composition module over
   `build_report_sources` and the inbox read path, with the four state fixtures.
3. The endpoint wiring and its goldens follow, then T002 and T003.

## Risks
- R-0570 (Low) stays OPEN and is not repaired here: its fix edits `README.md` and
  `tests/docs/test_docs_consistency.py`, which F040 does not own.
- Two homes for the urgency formula exist between this round and T002. They are
  pinned equal by a contract test rather than trusted, and D2 schedules the
  retirement of the TypeScript one.
<<<END PLAN2

<<<BEGIN RECORD2
Gate: F040 R1 — THE CLAIM ROUND. VERDICT PASS. Reviewed by re-running every gate against the reviewer's own scratch original rather than against the worker's report. TRANSPORT is a REAL comparison this time and not the self-consistent chain docs/agents/planner_reviewer_prompt.md §3 item 37 warns about: the block was written by the reviewer to `.remedy-wt/f040-r1-block.md` before delegation, and the committed `.agent/authored/f040-r1.md` and `.agent/last_block.md` both equal it at sha256 `9c0c71913863c6f9c15bc648cc94ecf9aefed84fd55d474732a63e9e5ad3e276`, 21083 bytes. THE PLAN is byte-equal to slice PLAN1 at 37 lines. THE RECORD APPEND reconstructs: 1640101 + 1 separator + 3531 = 1643633, the committed length, with N counted as 2 and the last two blank-line units equal to RECORD1's paragraphs in order. THE LEDGER moved by nothing — 311 registered and 53 resolved before and after, ADDED registered `[]`, ADDED resolved `[]`, `DECISION F040` ADDED exactly `['D1']`, and `^Done: R-0570` still counts 0. THE CANDIDATES FILE is byte-equal to CAND1 at 796 bytes with zero occurrences of the stale entry marker, so the block condition on the F040 claim is lifted on disk. THE CLAIM applied once: PAIRSTATUS-FROM 0x, PAIRSTATUS-TO 1x, the only `^- \[~\] F\d{3} — ` line in the ledger is F040, and the accepted `[x]` count is unmoved at 63. SEVEN SUITES were re-run by the reviewer in the primary checkout, every one a REAL exit 0 and every count equal to the base reading: `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 508, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 and the canary `tests/cli/test_golden_path.py` 42. NINE COMMITS, each touching exactly one path, insertions 339, 308, 25, 4, 6, 1, 19, 499 and — the reading the handback could not take of itself, supplied here per §3 item 31 — C7 at 274, every one under 500. The `## Commits` table's `+/-` column matches `git diff --numstat` cell for cell, which is §3 item 28's obligation and the half a handback most often gets wrong. THREE INVENTORY CLAIMS WERE SPOT-CHECKED BY THE REVIEWER AND ALL THREE HELD: the `NEXT_ACTION_RULES` annotation is `tuple[tuple[str, str], ...]` against a comment naming three fields; `git grep -i -E "urgency|significance" -- packages/` returns zero lines; and `build_report_sources` is `collect_report_sources` merged with `_evidence_sources`, so only it fills the fields rules 1 and 3 branch on. The worker's four amends and one reset on C6 were all pre-push on an unpublished commit — no published history was rewritten and no force-push occurred, which the branch reflog shows directly.

- R-0751 — Low, A SHIPPED COMMENT DOCUMENTS THE NEXT-ACTION RULE TABLE AS THREE-TUPLES AND THE TABLE HOLDS PAIRS, ON THE ONE SEAM F040 IS REQUIRED TO IMPORT RATHER THAN RESTATE. Raised by the WORKER of F040 R1 as deviation 3 while measuring the seam, declared rather than fixed because the round's change set held no production path, and CONFIRMED by the reviewer at `6664bf5e` by reading the file. THE MEASUREMENT: `packages/orchestration/run_report.py:170` reads `#:   (rule id, condition, action template)` while the value at :175 is annotated `tuple[tuple[str, str], ...]` and every one of its five entries is a PAIR — the action template is not in the table at all, it is built inside `recommended_next_action` at :383. Low, because nothing executes a comment and every caller in the repository today unpacks correctly; the cost is that the next caller is F040's digest, whose whole design premise is that the CTA and the report's recommendation cannot disagree because they read ONE table, and a builder who specifies from the comment writes a three-way unpack that raises on the shipped value. The open set was searched for this defect before an id was minted, per §3 item 30: `R-0745` and `R-0746` are the only open findings naming a `packages/orchestration` module of this class and neither describes this comment — `R-0746` is `proof_chain.py`'s public-API list. FIX: C5 of this round replaces the comment with the arity the value actually has. This is in scope for F040 rather than a paydown item because the digest imports this exact table, which is the test `docs/agents/planner_reviewer_prompt.md` §4 item 7 applies to an unrelated-fix question.

DECISION F040 D2 — THE URGENCY FORMULA GETS A PYTHON HOME, AND THE TYPESCRIPT COPY IS PINNED TO IT UNTIL T002 RETIRES IT. THE PROBLEM, measured in `.agent/f040_inventory.md` section 2 and re-verified by the reviewer: `docs/roadmap/features/T5_F040.md:57-58` requires digest significance to be "the urgency formula, one source with the inbox", and that formula is `decisionUrgency` at `apps/ui/src/api/decisionOrder.ts:21-39`, browser-side TypeScript returning `(blockedCount + 1) * age`. `git grep -i -E "urgency|significance" -- packages/` returns ZERO lines, so a Python digest endpoint cannot import it, and `apps/ui/src/api/decisionOrder.ts:9-11` records that Remedy deliberately keeps exactly one home for the rule. CHOSEN: move the home to Python. C6 adds `decision_urgency` to `packages/orchestration/decision_inbox.py`, beside `_decision_age_seconds` and `_blocked_subtree_size`, which already compute its two inputs onto every card; the digest and the CLI both read the number from there; and C8 adds `tests/ui_contracts/test_decision_urgency_parity.py`, which reads BOTH implementations as comment-stripped TEXT and asserts they agree over a shared table of inputs, in the manner `tests/ui_contracts/test_apply_state_partial.py` establishes. Two homes therefore exist between this round and T002, and they are PINNED rather than trusted. ALTERNATIVES CONSIDERED: (a) compute in Python and accept two unpinned homes — rejected, that is precisely what `decisionOrder.ts:9-11` refuses and nothing would catch a drift; (b) have the digest carry only the two inputs and let the client score — rejected because T003 requires `remedy job digest` to print the same composition and a Python CLI cannot call a TypeScript function, so the parity the feature asks for would break at exactly the surface that proves it; (c) move the formula to Python AND retire the TypeScript one in this round — rejected on scope, because that edits F031's shipped inbox ordering and belongs with the client work in T002, where the hero card reads the wire value anyway. HOW TO REVERSE: delete `decision_urgency` and its two test files; nothing else imports it until T001. WHAT IT COSTS TO BE WRONG: one duplicated four-line arithmetic expression for the length of one T-slice, with a test that fails the moment the two disagree.

DECISION F040 D3 — THE OWNERSHIP BLOCK IS AN HONEST ABSENCE, NOT AN INVENTION, AND THE FEATURE FILE SAYS SO. THE PROBLEM: `docs/roadmap/features/T5_F040.md:41` orders "top ownership sentences (≤3)" from the phrase catalog of F035, and F035 is `[ ]` at `docs/roadmap/STATUS.md:99`. `.agent/f040_inventory.md` section 4 records six searches across ALL of `packages/` and `apps/` — the widest of them, `git grep -l -i ownership`, matched nine files, every one process, file or repo ownership and not one a human-attribution ledger. The reviewer re-ran that search and confirms it. There is nothing to compose over. CHOSEN: the digest's envelope carries `ownership` as an empty list from the first version, and the card OMITS the section rather than rendering an empty block or inventing a sentence — which is the README's own "if something is unproven, Remedy says so instead of guessing" applied to a missing producer rather than a missing measurement. C4 amends the feature file to record this as amendment A1, so a later builder reads the amendment rather than rediscovering the absence. Keeping the FIELD from the start is deliberate: F035 then fills it without a version bump on an endpoint other surfaces already read. ALTERNATIVES CONSIDERED: (a) build a minimal ownership source inside F040 — rejected, that IS F035, and AGENTS.md's Scope Control forbids the "while I'm here" widening; (b) drop the field entirely and add it with F035 — rejected because adding a field later is a version bump on a published envelope, which is a cost paid to avoid writing one empty list. HOW TO REVERSE: delete amendment A1 from the feature file; no code depends on the amendment's wording. THE SAME COMMIT corrects a second defect in that file, found by the reviewer at `6664bf5e` and not by the inventory: `docs/roadmap/features/T5_F040.md:93` suggests `tests/ui_contract/test_digest.py`, and that DIRECTORY has never existed — `ls -d tests/ui_contract` fails while `tests/ui_contracts/` holds twenty entries. A worker following the file verbatim would create a second, near-homonymous test directory that no suite convention reaches. THIS IS THE THIRD FEATURE FILE CARRYING THAT TYPO AND THE PRECEDENT IS SETTLED, which is why it is corrected here rather than re-argued: F009 hit it at R2, ruled it in a DECISION recorded at `.agent/decisions.md:6625` — "(a) create `tests/ui_contract/` as the feature file names it — rejected, it would be a third directory one character from an existing one, which is precisely the synonym drift those rules forbid" — and F031 R7 recorded the same absence again. AGENTS.md's Code Discoverability Conventions ("one spelling per concept repo-wide") is the standing authority and this correction only applies it. The retired spelling SURVIVES on purpose in the append-only records under `.agent/`, which are not rewritten, so a repository-wide count of it can never reach zero and this round's gate reports the hits and requires only that the feature file is not among them — the item-2 trap F009's own R4 gate names.

DECISION F040 D4 — "BASIS" IN THE DIGEST MEANS EXACTNESS, THE TICKER'S VOCABULARY, AND NOT THE REPORT'S PROVENANCE. THE PROBLEM, from `.agent/f040_inventory.md` section 3: this repository carries TWO fields called basis and they are not the same thing. The report's `ReportSources.cost_basis` at `packages/orchestration/run_report.py:321` is PROVENANCE — `BudgetCounters.actual_sources`, whose closed set at `packages/orchestration/budget_guard.py:34-37` is `pingpong_actuals`, `pingpong_live`, `persisted_job_actuals`, `token_actuals` and `aggregate_actuals`, none of which says "estimated". The ticker's basis at `packages/orchestration/safe_points.py:637-640` is EXACTNESS, a two-key dict over `actual`, `lower_bound` and `absent`, and it is the one the client reads: `apps/ui/src/api/costMetric.ts:126-129` treats everything other than `actual` as estimated, and `apps/ui/src/components/metrics/TopMetricsBar.tsx` renders the mark `~` (:46), the aria phrase `, estimated` (:50) and the tooltip `Figures are an estimate` (`costMetric.ts:164-166`). CHOSEN: exactness. `docs/roadmap/features/T5_F040.md:52-53` asks for "the '~'/basis treatment (the ticker's vocabulary)", which resolves to those three strings and to no member of the provenance set, so the digest's `cost.basis` carries the exactness value and the digest RE-DERIVES it from the same `BudgetCounters` object the value comes from rather than joining a second source: `measured_cost_usd is None` gives `absent`, unpriced provider calls give `lower_bound`, otherwise `actual`. ALTERNATIVES CONSIDERED: (a) carry the provenance tuple, which the report already renders — rejected because the hero card's whole cost treatment is the `~`, and provenance cannot decide whether to draw it; (b) carry both — rejected as two fields named basis on one payload, which is the drift this decision exists to stop. HOW TO REVERSE: change the field's value set and the three client strings together; they are one decision. NOTE FOR T001, recorded because it is the non-obvious half: the ticker's basis is NOT on any per-job read route — `.agent/f040_inventory.md` section 5 measures it reaching the client only through budget tick events — so the digest derives it rather than reading it, and that derivation is the thing T001's tests must cover.
<<<END RECORD2

<<<BEGIN SLIP2
2026-08-29 · F040 R1 · The reviewer's PLAN1 slice marked "the seam inventory" as `done` in the Current Step table applied at C1, five commits before C6 wrote that inventory; the row was true when the round ended and false for the length of the round, and the block fixed the commit order without naming it in the slice, which is what §3 item 20's R-0524 carve-out asks for.
<<<END SLIP2

<<<BEGIN PAIROWNERSHIP-FROM
- Endpoint: digest per job {state, headline result line, cost
  {value, basis}, top ownership sentences (≤3), open decisions
  count + urgency peak, primary_action {label, deep link}} — pure
  composition, versioned.
<<<END PAIROWNERSHIP-FROM

<<<BEGIN PAIROWNERSHIP-TO
- Endpoint: digest per job {state, headline result line, cost
  {value, basis}, top ownership sentences (≤3), open decisions
  count + urgency peak, primary_action {label, deep link}} — pure
  composition, versioned.
  AMENDMENT A1 (DECISION F040 D3, 2026-08-29): the ownership
  sentences arrive with F035, which is `[ ]` in the ledger and ships
  no importable source — measured across all of `packages/` and
  `apps/` in `.agent/f040_inventory.md` section 4. Until F035 lands,
  the digest carries `ownership` as an EMPTY LIST and the card OMITS
  the section rather than rendering an empty one or inventing a
  sentence. The field is in the envelope from the first version so
  F035 fills it without a version bump.
  AMENDMENT A2 (DECISION F040 D4, 2026-08-29): `basis` here means
  EXACTNESS — the ticker's `actual` / `lower_bound` / `absent` — and
  never `BudgetCounters.actual_sources`, which is provenance. The
  digest re-derives it from the same counters object the value comes
  from; it is on no per-job read route.
<<<END PAIROWNERSHIP-TO

<<<BEGIN PAIRTESTPATH-FROM
home grid (next-but-one). Suggested tests:
tests/ui_contract/test_digest.py.
<<<END PAIRTESTPATH-FROM

<<<BEGIN PAIRTESTPATH-TO
home grid (next-but-one). Suggested tests:
tests/ui_contracts/test_digest.py — the PLURAL directory name, which
is the one that exists; the singular spelling this line carried until
DECISION F040 D3 never has (measured at `6664bf5e`).
<<<END PAIRTESTPATH-TO

<<<BEGIN PAIRCOMMENT-FROM
#:   (rule id, condition, action template)
<<<END PAIRCOMMENT-FROM

<<<BEGIN PAIRCOMMENT-TO
#:   (rule id, condition)
<<<END PAIRCOMMENT-TO

## SPEC for C6 — `decision_urgency` in `packages/orchestration/decision_inbox.py`

WRITE THIS YOURSELF from the specification; it is not sliced above, because
production code is described and not dictated. Place it after
`_answerable_by_decision_resolve` and before `build_decision_inbox`. It is
PUBLIC — no leading underscore — because the digest and the CLI both import it.

Signature and contract:

    def decision_urgency(card: dict[str, Any]) -> int:

- It reads exactly two keys of an inbox card, `blocked_count` and `age_seconds`,
  which `build_decision_inbox` already sets at :152-153.
- It is TOTAL: no input makes it raise. A missing key, a None, a non-numeric
  value, a bool, a NaN or an infinity is read as 0 for that input.
- `age` is the age in seconds when that is a real number strictly greater than
  0, and 0 otherwise — a None age is the endpoint's own answer for an unreadable
  `created_at` and is not evidence of urgency; a negative age means the clocks
  disagree.
- `blocked` is the blocked-subtree size clamped at 0 when it is a real number,
  and 0 otherwise.
- It returns `(blocked + 1) * age` as an `int`.
- The `+ 1` carries the WHY comment directly above the return, naming DECISION
  F031 D6: a literal `blocked * age` collapses every card that blocks NOTHING to
  0 whatever its age, so a question asked a week ago and one asked a second ago
  tie and their order becomes whatever the endpoint happened to send. Adding one
  keeps blocked size dominant and leaves age as the total order among the cards
  that block nothing.
- The docstring names `apps/ui/src/api/decisionOrder.ts` as the copy this is
  pinned against, and names the pin file, so a reader who changes one finds the
  other. It also states that this is the SINGLE HOME per DECISION F040 D2 and
  that the TypeScript copy retires in T002.

Match the module's existing style: a WHY docstring, `Any` from the module's
existing imports, no new import beyond what is already at the top of the file.

## SPEC for C7 — tests in `tests/orchestration/test_decision_inbox.py`

APPEND a new test class; do not edit an existing test. Cover, one test each and
named for the property rather than the input:

- the ordinary case: blocked 3, age 3600 gives 14400;
- a card that blocks nothing scores its age, so 0 blocked and age 42 gives 42;
- a None age scores 0 whatever the blocked count;
- a negative age scores 0;
- a negative blocked count is clamped, so it scores as blocking nothing;
- missing keys score 0 rather than raising;
- a non-numeric or NaN input scores 0 rather than raising;
- the ordering property the formula exists for: over a list of cards, sorting by
  `decision_urgency` descending puts a card blocking one task ahead of an
  equally aged card blocking none.

Read the existing file first and follow its fixture and naming conventions.

## SPEC for C8 — `tests/ui_contracts/test_decision_urgency_parity.py`

A NEW file in the established shape of `tests/ui_contracts/test_apply_state_partial.py`:
it reads the TypeScript as TEXT, imports nothing from `apps/`, and strips comments
before asserting, because both implementations carry WHY comments that name the very
expressions under test and an unstripped guard is satisfied by the prose describing
the branch rather than by the branch (finding R-0584).

It must:

- locate `decisionUrgency` in `apps/ui/src/api/decisionOrder.ts` and FAIL LOUDLY,
  in its own test, if the function cannot be found at all — an empty extraction
  must never pass the assertions beneath it;
- assert the TypeScript body still returns the `(blockedCount + 1) * age` shape,
  from comment-stripped source;
- assert the Python `decision_urgency` returns the same numbers as a table of at
  least six input pairs shared by both halves, including the None-age, negative
  and zero-blocked cases;
- carry a module docstring stating that two homes exist by DECISION F040 D2, that
  this file is the pin, and that T002 retires the TypeScript one.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C9, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — the scratch original
   `.remedy-wt/f040-r2-block.md`, the committed `.agent/authored/f040-r2.md` and
   the committed `.agent/last_block.md` — reported with the byte length, all
   three EQUAL. This block states no expected digest: a file cannot carry its
   own sha256, and the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN2 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit byte length yourself; the
   reviewer read 1643633 at `6664bf5e`. Base + one separator newline + RECORD2
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION against
   the entire committed file, not a prefix test; (b) PARAGRAPH ORDER — the last N
   blank-line units equal RECORD2's N paragraphs IN ORDER, N COUNTED by your
   script. NEGATIVE CONTROL in a disposable worktree: flip one byte inside the
   FIRST appended paragraph and report that BOTH readings reject it and accept
   the unflipped bytes.

G4 THE LEDGER, at C2 and C3. Distinct `^- R-\d+ — ` ids before and after, with
   ADDED exactly `['R-0751']`; ADDED resolved `[]`; distinct
   `^DECISION F040 D\d+ — ` with ADDED exactly `['D2','D3','D4']`; exactly one
   `^Gate: F040 R1 — ` line; `^Done: R-0570` still 0. For `.agent/prose_slips.md`
   report the line count before and after — the difference is 1 — and that the
   file's earlier lines are a byte-exact PREFIX of the new file.

G5 THE FEATURE FILE, at C4. PAIROWNERSHIP is APPEND-shaped: report FROM occurring
   exactly 1x in the committed file and each TO-ONLY line occurring exactly 1x
   AMONG THE LINES C4's DIFF ADDS — do NOT count FROM to zero. PAIRTESTPATH is a
   REWRITE: FROM 0x, TO 1x. Then `git grep -n "tests/ui_contract/"` over the whole
   repository — report every hit; `docs/roadmap/features/T5_F040.md` must not be
   among them. Then `python3 -m pytest tests/docs/ -q` and
   `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, each its own
   REAL exit code; the reviewer measured 295 and 30 at the base.

G6 THE PRODUCTION EDITS, at C5 and C6. PAIRCOMMENT: FROM 0x and TO 1x in
   `packages/orchestration/run_report.py`. Then, in one reading each:
   `python3 -c "from packages.orchestration.run_report import NEXT_ACTION_RULES as R; print(len(R), {len(r) for r in R})"`
   printing 5 and `{2}`, which is the value the repaired comment now describes;
   `ruff check packages/orchestration/run_report.py packages/orchestration/decision_inbox.py`;
   and `python3 -m compileall -q packages/orchestration/decision_inbox.py`.
   Report that `DECISION_INBOX_VERSION` is still 1 and that
   `build_decision_inbox`'s returned key set is unchanged, by calling it.

G7 THE NEW BEHAVIOUR AND ITS RED PROOF, at C8. First
   `python3 -m pytest tests/orchestration/test_decision_inbox.py tests/ui_contracts/test_decision_urgency_parity.py -q`
   — REAL exit 0, with the passed count. Then, INSIDE A DISPOSABLE WORKTREE at
   C8 and never in the primary checkout: report the UNMUTATED control's exit code
   over those same two files FIRST — it must be 0 — then make ONE mutation,
   changing `decision_urgency`'s returned expression from `(blocked + 1) * age`
   to `blocked * age` in
   `<worktree>/packages/orchestration/decision_inbox.py`, and report the exit
   code and the failing count with that mutation in place. Purge `__pycache__`
   and use `python3 -B`. Name the worktree path you created and report that you
   removed it and that `git worktree list` no longer holds it. A colour with no
   baseline is not evidence, which is why the control is ordered first.

G8 THE SUITES AND THE TREE, at C8. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`,
   `python3 -m pytest tests/orchestration/test_run_report.py -q`, and the canary
   `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer measured
   508, 52, 21, 16 and 42 at the base for all but `test_run_report.py`, which it
   did not run — report yours for that one without a base comparison. Then
   `git status --porcelain` EMPTY, `git ls-files --others --exclude-standard`
   count 0, and the per-commit insertion counts for C0a through C8 from
   `git diff --numstat`, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state block,
the `## Commits` table with a `+/-` column taken from `git diff --numstat` and not
from file line counts, the deviations, the item-status table with every bundle
item and every gate appearing exactly once, and the next steps. It states
`SESSION 1` of F040 and round 2, and has NO length cap. Name R-0751 as FIXED this
round and R-0570 as OPEN and routed off this branch.
