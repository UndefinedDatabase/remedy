── STEP T003-close + ACCEPTANCE — F110 model routing by task class ────────────
Round 14 · SESSION 4 of F110 · base `f0bbdc5c` (F110 R13 C7)

Goal:
  Repair the two deliberate-absence notes round 13 falsified — finding R-0789,
  whose fix clause this block obeys — and build the acceptance clause of
  `docs/roadmap/features/T3_F110.md` this branch has not yet built: the
  REVIEWER/WORKER PAIRING ASSERTED ON A REAL FIXTURE ROUND. Round 13's PASS
  verdict, that finding and two prose slips are booked in the same round.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r14.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   apply PLAN14 to `.agent/plan.md`
  C2   append RECORD14 to `.agent/live_review.md` and SLIPS14 to
       `.agent/prose_slips.md`
  C3   the R-0789 repair: SPEC (a) and SPEC (b), ONE commit, both files
  C4   SPEC (c): IMPORT14 and the new tests, into
       `tests/orchestration/test_role_config.py`
  C5   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r14.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/prose_slips.md`
  `packages/orchestration/model_routing.py`
  `packages/orchestration/config.py`
  `tests/orchestration/test_role_config.py`
  `.agent/handoff.md`
  `config.py` is named for SPEC (b) alone, as R-0789's fix clause requires.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or re-wrap
     one. If a slice looks wrong, apply it anyway and DECLARE the problem in the
     handback: a declared conflict is worth more than a silent repair.
  2. `.agent/STOP` is read FROM DISK before the first commit and again before
     C5. If it exists at either reading: finish the commit in hand, write the
     handback, push, and stop.
  3. Slices are transported, not typed: C0a is `shutil.copyfile` from
     `remedy-review-r9-scratch/f110-r14.md`, and every slice is EXTRACTED from
     the COMMITTED `.agent/authored/f110-r14.md` by locating its `<<<BEGIN X>>>`
     and `<<<END X>>>` marker lines with `list.index` and joining the lines
     BETWEEN them, markers excluded. Nothing is taken from this prompt.
  4. `.agent/plan.md`, `.agent/live_review.md` and `.agent/prose_slips.md` each
     keep their own newline convention and THE TARGET WINS: `.agent/plan.md`
     ends WITH exactly one trailing newline and the PLAN14 extraction carries
     none, so the applied file is the extraction PLUS that one byte; the other
     two end WITHOUT a trailing newline and each append is `\n\n` + the slice.
  5. Do NOT run `ruff`, `npm`, or any formatter. Linting is the reviewer's, and
     a formatter would rewrite bytes a gate proves.
  6. `packages/orchestration/model_routing.py` and
     `packages/orchestration/config.py` are edited for PROSE ONLY this round —
     one function docstring and one comment block. NO constant, signature,
     import, expression or statement in either file changes. A deletion whose
     line is neither inside the docstring of `promotion_evidence_from_mapping`
     nor a `#`-prefixed comment line is a STOP: write the handback and end.
  7. `tests/orchestration/test_role_config.py` is only ADDED to. No existing
     test, fixture or helper is edited, renamed, deleted, skipped or
     re-ordered, and that commit's deletion count for the file must be ZERO.
     Reuse the helpers already in the file rather than writing new ones that do
     the same work — `_configure_promotion_tables` and
     `_well_formed_evidence_entry` are named in SPEC (c) for that reason.
  8. A sentence THIS ROUND makes stale, ANYWHERE INSIDE THE CHANGE SET, is
     repaired in the commit that falsifies it. A stale sentence OUTSIDE the
     change set is DECLARED in the handback and left alone. Constraint 6 scopes
     WHICH REGION of the two production files may lose lines; it does not
     narrow this obligation, and if the two ever conflict, STOP and declare —
     that conflict is exactly what R-0789 records.
  9. No `remedy.toml` is ever written to the repository root: it would change
     how every test in the suite resolves configuration. Fixture TOML goes to a
     pytest `tmp_path`, which the reused helper already does.
  10. Every destructive check runs ONLY inside a disposable `git worktree`
      created UNDER the repository at a path matching `remedy-review-*`, which
      `.gitignore:223` covers, and is removed by its EXACT path with
      `git worktree remove <path>` plus `git worktree prune`. The primary
      checkout reads `git status --porcelain` EMPTY at every verdict.
  11. This sandbox denies `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd` and
      `cp`. Copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`, set
      environment in-process, and capture a real exit code by wrapping the gate
      as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` — the Bash tool does not surface
      a non-zero exit on its own.
  12. `.agent/decisions.md`, `.agent/candidates.md` and
      `docs/roadmap/features/T3_F110.md` are NOT touched — the feature file's
      Design and Task-slicing bullets are the closure sequence's work.

SPEC (a) — `packages/orchestration/model_routing.py`, the docstring of
`promotion_evidence_from_mapping` ONLY.
  Its last paragraph currently opens "NOTHING IN PRODUCTION CALLS THIS YET" and
  says the call "arrives with the wiring round". Round 13's C3 `8efa2330` IS
  that round, so both clauses are false while the paragraph's LOCATION
  prediction turned out exactly right. Replace that paragraph with one that
  states, in this module's own idiom:
    - `packages.orchestration.role_config.resolve_promotion_evidence` is this
      function's ONE production caller, and it landed at `8efa2330`;
    - that caller reads `model_routing.promotion_evidence` from the
      configuration and hands the records to BOTH consumers — the table builder
      `build_effective_task_class_tiers` and the seam `route_role_call` — so a
      documented run both licenses a cheaper tier and names itself on the
      routed call;
    - the deliberate-absence note is retired because the absence is over: a
      reader searching for the caller must land on the caller's name.
  Keep every other paragraph of that docstring word for word. Write it better
  than the wording above if you can — the SPEC fixes the facts, not the prose.

SPEC (b) — `packages/orchestration/config.py`, the `#` comment block directly
above the `ConfigKeySpec` whose key is `model_routing.promotion_evidence`.
  It currently reads "NOTHING READS THIS KEY YET — the reader arrives with the
  wiring round, in packages/orchestration/role_config.py beside the one that
  already reads the tiers table." Replace that sentence, and only it, with one
  naming `role_config.resolve_promotion_evidence` as the reader that now
  exists, landed at `8efa2330`, beside the one that reads the tiers table. The
  comment's first sentence — that this is the first table of RECORDS in the
  registry, so it declares `entry_type` dict where its sibling declares str —
  is still true and is kept verbatim. The `ConfigKeySpec` itself, including its
  `description`, does not change.

SPEC (c) — `tests/orchestration/test_role_config.py`, purely additive.
  Apply IMPORT14 as placed below, then add the acceptance tests described here
  at the END of the file, in this file's own idiom: the obligations are fixed,
  the prose and the assertion order are yours.

  WHY THIS IS NOT ALREADY COVERED, measured at `f0bbdc5c`: every existing guard
  for policy hard rule 1 lives in `tests/orchestration/test_model_routing.py`
  and judges an OVERRIDE MAP through `validate_task_class_tier_overrides`; none
  resolves a ROUND. A map the validator refuses and a round that nevertheless
  routes the refused table are different failures, and only the second reaches
  a provider call — which is why the Acceptance section asks for the pairing
  "asserted on a real fixture round" as a line of its own.

  (c1) A derivation, not a literal: build the list of
       `(worker_role, reviewer_role, worker_class, reviewer_class)` rounds by
       crossing `REVIEWER_WORKER_CLASS_PAIRS` with the roles `ROLE_TASK_CLASSES`
       declares for each half. Assert the list is NON-EMPTY — so an emptied
       pair table is a failure and not a vacuous pass — and assert for each
       entry that both roles declare the classes of a declared pair. Every test
       below is parametrized over that list. Measured by the reviewer at
       `f0bbdc5c`, it holds four rounds.
  (c2) A helper that runs ONE fixture round: resolve BOTH halves through the
       production `resolve_role_config`, inside `warnings.catch_warnings(
       record=True)` with `simplefilter("always")`, and return both configs and
       the captured messages. The tier under test is read off
       `cfg.routed_call["tier"]` — what the seam RECORDED — and ranked with
       `model_tier_rank`, never compared as a string.
  (c3) EVIDENCE COMPLETE. On an unconfigured round, both halves carry a
       non-empty `cfg.model`, a `routed_call` whose keys are exactly
       `ROUTED_CALL_EVIDENCE_FIELDS`, the `task_class` the role declares, the
       tier `TASK_CLASS_TIERS` seeds for it, and a non-None `reason`; and no
       warning is raised. This is the Acceptance line "every call's evidence
       shows class, routed model, reason" stated over a round.
  (c4) THE SEEDED ROUND PAIRS CORRECTLY: reviewer rank >= worker rank, no
       warning.
  (c5) A DOCUMENTED RUN MAY CHEAPEN THE WORKER HALF AND THE PAIR STILL HOLDS.
       Configure, through `_configure_promotion_tables`, a tiers table moving
       ONLY the worker class to `MODEL_TIERS[0]` plus a
       `_well_formed_evidence_entry` for that class. Assert: no warning; the
       worker's tier is that cheapest tier; its reason is `OVERRIDE_REASON`;
       its `promoted_by` is truthy; and the pairing still holds. This is the
       case that stops the suite asserting a table which never moves.
  (c6) A TABLE DEMOTING THE REVIEWER HALF IS REFUSED BY NAME. Configure a tiers
       table moving ONLY the reviewer class to `MODEL_TIERS[0]`, with NO
       evidence. Assert: at least one warning; EVERY captured message contains
       `RULE_REVIEWER_WEAKER_THAN_WORKER`; the pairing still holds; and the
       reviewer's tier is its SEEDED tier, i.e. the refused table did not route.
  (c7) EVIDENCE DOES NOT DISCHARGE THE PAIRING RULE — the discriminator, and the
       one case without which this whole class of test passes while a benchmark
       run is allowed to buy a weaker reviewer. Same demotion as (c6) but WITH a
       `_well_formed_evidence_entry` for the REVIEWER class. Assert: at least
       one warning; every message contains `RULE_REVIEWER_WEAKER_THAN_WORKER`;
       NO message contains `RULE_PROMOTION_WITHOUT_EVIDENCE`, because the
       benchmark discharged that rule and only that one; the pairing still
       holds; the reviewer's tier is its seeded tier; and its `promoted_by` is
       None. Measured by the reviewer at `f0bbdc5c`, this is exactly what the
       shipped code does.

<<<BEGIN IMPORT14>>>
    RULE_REVIEWER_WEAKER_THAN_WORKER,
<<<END IMPORT14>>>

IMPORT14 goes into the existing
`from packages.orchestration.model_routing import (...)` block IMMEDIATELY
AFTER the line `    RULE_PROMOTION_WITHOUT_EVIDENCE,` and IMMEDIATELY BEFORE
`    SAFETY_RELEVANT_CLASSES,`. Measured by the reviewer at `f0bbdc5c`: the
anchor occurs exactly once in that file and `RULE_REVIEWER_WEAKER_THAN_WORKER`
zero times. CONTAINMENT TEST, run mechanically before emission over the FROM
(the anchor followed by `    SAFETY_RELEVANT_CLASSES,`) and the TO that inserts
IMPORT14 between them — `TO contains FROM: false` — so this pair is a REWRITE by
measurement, no FROM-zero count is owed, and the proof it does owe is G5's
additive reconstruction. That placement is the isort order this repository's own
configuration produces: inside the ALL-CAPS run, `RULE_R…` sorts after `RULE_P…`
and before `SAFETY_…`.

<<<BEGIN PLAN14>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 14, session 4 — THE R-0789 REPAIR AND THE PAIRING ACCEPTANCE. Two
deliberate-absence notes that round 13's own wiring falsified are repaired in
one commit, in `model_routing.py` and in `config.py`. The feature file's last
unbuilt acceptance clause — the reviewer/worker pairing asserted on a REAL
fixture round — is built as tests that resolve BOTH halves of a round through
the production seam under four real configurations, including the one where a
documented benchmark run is supplied for the reviewer class and the hard rule
refuses the table anyway. Round 13's PASS verdict, the finding and two prose
slips are booked in the same round.

## Next Steps

- The integration gate round, which docs/agents/integration_gate.md governs
  and which needs the R-0736 base-worktree mtime-parity repair and a cold
  `dist` build budgeted for.
- The closure sequence, which takes two rounds, runs the one §3 checklist
  consolidation pass DECISION F110 D1 carries into it, and updates the Design
  and Task-slicing bullets of `docs/roadmap/features/T3_F110.md`.

## Risks

- The pairing acceptance rests on `REVIEWER_WORKER_CLASS_PAIRS` holding at
  least one pair whose halves are both declared by a role; SPEC (c1) asserts
  exactly that, so an emptied table is reported as a failure rather than as a
  vacuous pass.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN14>>>

<<<BEGIN RECORD14>>>
Gate: F110 R13 — the round 13 entry. VERDICT PASS, over the range `f943e436..be850b92` plus the handback commit `69090d90`; the verdict text was written into `.agent/handoff.md` at `f0bbdc5c` and is booked here in the first record commit of round 14, per operator amendment amend0827-process-diet rule 1. THE EVIDENCE IS WIRED AND A DOCUMENTED RUN NOW LICENSES A CHEAPER TIER, which completes T003 on this branch: `role_config.py` gained `PROMOTION_EVIDENCE_CONFIG_KEY` and `resolve_promotion_evidence`, the round-12 parser's one production caller, and those records reach BOTH consumers — `build_effective_task_class_tiers` through `resolve_effective_task_class_tiers`, and `route_role_call` through `resolve_routed_call_evidence`. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES: `cmp` between the reviewer's scratch original and the committed `.agent/authored/f110-r13.md` exits 0, and one digest `b7f4c58449a0d61cbf2a753f29f250dc747843c0d246340ab6796a342de07d29` at 26618 bytes covers the original, the saved copy at `745c5665` and the mirror at `347a84bb`; the block is 316 lines against the reviewer's own projection of 316, under the §3 item 1 cap of 400. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE and every size matched the pre-emission projection: `.agent/plan.md` equals PLAN13 plus the one trailing newline the target's convention adds, at 41 lines; `.agent/live_review.md` is 2209946 + 2 + 5350 = 2215298, still ending without a newline, base an exact prefix; `.agent/prose_slips.md` is 61137 + 2 + 1212 = 62351. `ruff check` over all three changed code files answers "All checks passed!", run reviewer-side because the worker's permission layer refuses the tool. THE WIRING WAS RUN BY THE REVIEWER ACROSS FIVE CONFIGURATION STATES, NOT READ. With BOTH tables configured, `architecture` — seeded at the TOP tier — comes back at `cheap` with reason `per_project_override` and `promoted_by` naming the run, and no warning is raised. With the TIERS table alone the same promotion is REFUSED, one warning names `promotion_without_evidence`, and the class comes back at its seeded `top`. With EVIDENCE alone and no promotion asked, the records parse and the table is unchanged with `promoted_by` correctly None — evidence licenses, it does not promote. With NOTHING configured every answer is identical to round 9's. And with a BARE STRING where the evidence table belongs, `validate_config` reports "expected table, got str", the reader returns an empty mapping, and `provider`, `model` and `effort` come back unchanged — DECISION F110 D5's principle holding one layer further out, with no crash in a config resolution. THE DELETIONS WERE PROVED, NOT INSPECTED: C3 is 17 insertions against 13 deletions in `model_routing.py` and 86 against 3 in `role_config.py`, and the reviewer parsed the BASE file with `ast` to establish that its module docstring spans base lines 1..171, then read the diff's own hunk headers — the deleted base ranges are 41-43 and 47-56, both strictly inside that span, so that round's constraint 7 is MEASURED and no constant, signature or function body of rounds 4 through 12 was revised. `git diff --stat` over `packages/` and `apps/` with the two edited files excluded is EMPTY, which proves `config.py` was not touched, and over `docs/` it lists exactly the one configuration document. THE SUITES WERE RE-RUN BY THE REVIEWER at 101 passed for `test_role_config.py`, grown from 92 by the nine tests C4 adds, then 406 with 3 skipped, 81, 20, 68, 304, 199, 295 and 42, every one exit 0 and every unmoved count matching the block. The G6 red proof's four mutations each go red and every revert returns to the control, with the primary checkout clean at every reading; the worker reports the red sets as NOT pairwise disjoint — mutations (i) and (iii) produce identical sets — and reports that as a measured result rather than as a fault, which is what the gate asked for. Per-commit insertions are 316, 219, 14, 6, 103, 265 and 36, every one under the AGENTS.md cap; `69090d90` is 449 insertions, a full-file rewrite of a single `.agent/**` state file and exempt under DECISION F104 D1. The open set is 278 over 349 registered and 71 UNIQUE resolved — derived as a set difference over unique ids, because `R-0721` and `R-0725` each carry two `Done:` paragraphs and the ledger holds 73 such lines. `R-0767` stays OPEN. ONE FINDING IS OWED AND ITS ROOT CAUSE IS THE REVIEWER'S OWN BLOCK; it is registered immediately below as `R-0789`, and the two prose slips that round also owed are in `.agent/prose_slips.md`. The tree is clean, no worktree of the round's making survives, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed with no pull request open.

- R-0789 — Low, TWO DELIBERATE-ABSENCE NOTES IN PRODUCTION CODE OUTLIVED THE ABSENCE THEY DOCUMENT, AND THE BLOCK THAT SHIPPED THE WIRING FORBADE THEIR REPAIR. Registered by the reviewer at the F110 R13 gate, against the reviewer's own block. MEASURED at `f0bbdc5c`: `packages/orchestration/model_routing.py` line 895 opens a paragraph of `promotion_evidence_from_mapping`'s docstring with the words "NOTHING IN PRODUCTION CALLS THIS YET", and `packages/orchestration/config.py` line 672 carries a comment reading "NOTHING READS THIS KEY YET" of `model_routing.promotion_evidence`; each of those strings occurs exactly once in its own file. Both were true when written in round 12 and both were falsified by round 13's own C3 at `8efa2330`, which added `role_config.resolve_promotion_evidence` — the caller and the reader they each say does not exist. Both sentences additionally point a searching reader at where the caller "arrives", and it has arrived. THIS IS ONE DEFECT IN TWO FILES AND IT TAKES ONE ID, per docs/agents/planner_reviewer_prompt.md §3 item 30: the same wiring falsified both notes, and one commit repairs both. THE ROOT CAUSE IS A CONTRADICTION INTERNAL TO THE R13 BLOCK, not a worker fault: its constraint 9 required a sentence the round makes stale to be repaired in the commit that falsifies it, while its constraint 7 and its gate G5 made ANY deletion in `model_routing.py` outside the MODULE docstring a STOP — and the false sentence sits in a FUNCTION docstring. The worker obeyed both, declared the conflict, and repaired neither, which is exactly what that block's constraint 1 asks for. `config.py` was additionally outside that round's change set, so its constraint 9 forbade touching it at all. FIX: repair both sentences in ONE commit in the next round, whose block must scope its permitted-deletion region to the FILE rather than to its module docstring, and must name `config.py` in the change set for that purpose alone. WHY LOW rather than Medium: nothing routes differently and no gate is blind — the module docstring two paragraphs above the first sentence already names the caller correctly, so a reader who searches for it lands on the truth first and on the contradiction second.
<<<END RECORD14>>>

<<<BEGIN SLIPS14>>>
2026-09-03 · F110 R13 · The round 13 block set its constraint 9 ("a sentence this round makes stale INSIDE the change set is repaired in the commit that falsifies it") against its constraint 7 and its gate G5 ("model_routing.py is edited for its MODULE DOCSTRING ONLY and any deletion outside that docstring is a STOP"), and the sentence the round falsified sits in a FUNCTION docstring — so the two clauses could not both be obeyed and the worker was correct to declare the conflict and repair nothing. Registered as R-0789 because the false sentences are on disk in production code. THE LESSON: a permitted-deletion region is scoped to the SMALLEST region that still contains every sentence the round can falsify, and a block that names "the module docstring" must first grep the file for the other prose its own change makes false — a deliberate-absence note lives wherever the absence was, and this feature has now written such notes in three files.

2026-09-03 · F110 R13 · The block's gate G2 ordered "cmp the PLAN13 extraction against `.agent/plan.md` — exit 0" while its own constraint 4 states that the TARGET's convention adds one trailing newline the slice does not carry, so a literal cmp of the raw extraction cannot exit 0 and the two clauses disagree. Every round from 8 onward has carried this same wording and every worker has resolved it the same correct way, but this round's worker was the first to say so, running BOTH comparisons and reporting both exit codes rather than silently picking the green one. THE LESSON: state the gate as "cmp the slice PLUS the target's trailing newline", so the ordered command and the stated convention agree on the page instead of relying on the worker to reconcile them. Applied in this round's own G2.
<<<END SLIPS14>>>

Done when — the gates below, within the amend0827 rule 5 budget, each RUN and
each reported as ONE LINE in the handback with its real exit code. Every gate
runs at a commit STRICTLY EARLIER than C5, the commit that writes the handback.

G1 TRANSPORT — one digest comparison, per amend0827 rule 5.
   `cmp remedy-review-r9-scratch/f110-r14.md .agent/authored/f110-r14.md` — exit
   0. `sha256sum` those two plus `.agent/last_block.md` — one digest, repeated.
   Report `wc -l .agent/authored/f110-r14.md`. This proves the scratch original,
   the saved copy and the mirror agree; it claims nothing about other bytes.

G2 THE PLAN — a byte-equality check of the plan slice, and nothing more.
   Extract PLAN14 by delimiter index from the COMMITTED authored file. `cmp` the
   extraction PLUS ONE TRAILING NEWLINE against `.agent/plan.md` — exit 0.
   Report the bare extraction's `cmp` exit code beside it, so the record carries
   both readings rather than the flattering one. Report `wc -l .agent/plan.md`
   (must be under 50), `grep -c '^## Goal'` and `grep -c '^## Next Steps'`.

G3 THE RECORD APPENDS — full byte forensics, which amend0827 rule 5 reserves for
   exactly this target.
   `.agent/live_review.md`: base 2215298 bytes at `f0bbdc5c`, ending WITHOUT a
   newline. Append `\n\n` + RECORD14. Report the arithmetic
   `2215298 + 2 + <len> = <total>` against the real size; that the pre-C2
   content is an exact byte PREFIX; and that the file still ends without a
   newline. SECOND READER, covering the WHOLE appended region: let N be the
   number of paragraphs your script COUNTS in the slice — do not take N from
   this block — and compare the LAST N blank-line units of the whole file
   against the slice's N paragraphs IN ORDER. NEGATIVE CONTROL on the FIRST
   appended paragraph: flip its byte 0 in a COPY and confirm the second reader
   REJECTS it; the real file is never written. HEADER SHAPE, per §3 item 26:
   report the count of lines matching the slice's own
   `Gate: F110 R13 — the round 13 entry.` prefix in the file BEFORE C2 (expected
   0) and AFTER C2 (expected 1).
   `.agent/prose_slips.md`: base 62351 bytes, ending WITHOUT a newline. Append
   `\n\n` + SLIPS14. Report the same arithmetic, the prefix property and the
   no-trailing-newline property.
   THE OPEN SET, recomputed mechanically and never carried forward: paragraphs
   matching `^- R-\d+ — ` and lines matching `^Done: R-\d+ — `, each reduced to
   UNIQUE IDS, the open set their set difference. Report registered, unique
   resolved, the `Done:` LINE count beside it, the open total, and whether
   `R-0767` and `R-0789` are each in the open set.

G4 THE TWO PRODUCTION FILES — full byte forensics, prose region proven.
   `git show --numstat <C3>` for both paths. `ast.parse` both — report OK per
   path. QUOTE EVERY DELETED LINE VERBATIM, per file. Then PROVE the region,
   mechanically and per line: for `model_routing.py`, parse the BASE file with
   `ast`, take the `promotion_evidence_from_mapping` FunctionDef's docstring
   node span, and report that every deleted base line number lies inside it; for
   `config.py`, report that every deleted line's stripped text starts with `#`.
   Either proof failing is the STOP constraint 6 names.
   Then report, at C3: the count of `NOTHING IN PRODUCTION CALLS THIS YET` in
   `model_routing.py` (expected 0) and of `NOTHING READS THIS KEY YET` in
   `config.py` (expected 0); that the AST-extracted docstring of
   `promotion_evidence_from_mapping` CONTAINS `resolve_promotion_evidence`; and
   the count of `resolve_promotion_evidence` in `config.py`, which the reviewer
   measured as 0 at `f0bbdc5c` and which must now be at least 1.
   THEN RUN THE SHIPPED CODE, not read it: with nothing configured, print
   `resolve_role_config` for `builder` and for `reviewer` — provider, model,
   effort and the whole `routed_call` mapping. The reviewer's own reading at
   `f0bbdc5c`, which yours must reproduce exactly: both roles answer provider
   `ollama`, model `muse-glimmer:latest`, effort `medium`; `builder` answers
   `{'task_class': 'standard_build', 'tier': 'mid', 'reason': 'seed_mapping',
   'promoted_by': None}` and `reviewer` the same with `'standard_review'`. A
   prose commit that moves a routed answer is a STOP.

G5 THE TEST FILE — one additive reconstruction, covering the commit's edits at
   once. `git show --numstat <C4>` for that path: the deletion column must be 0,
   which is constraint 7 MEASURED rather than asserted. Read the BASE blob with
   `git show f0bbdc5c:tests/orchestration/test_role_config.py`. Take the
   COMMITTED file, remove the FIRST occurrence of the IMPORT14 line from it, and
   report that the base blob is then a byte-exact PREFIX of what remains — which
   says the import went in at its anchor and everything else was APPENDED, with
   nothing edited in between. Report the anchor line's occurrence count in the
   base (must be 1) and `ast.parse` OK on the committed file.

G6 THE RED PROOF — mandatory in full for production code, and untouched by the
   gate budget.
   In a disposable worktree created under the repository at
   `remedy-review-r14-redproof`, detached at C4, NEVER `cd`-ed into (pass `cwd=`
   instead). Purge `__pycache__` before every run and use
   `python3 -B -m pytest tests/orchestration/test_role_config.py -q` for every
   run. Print `role_config.__file__` and `model_routing.__file__` FROM INSIDE
   the worktree, to prove no editable install shadows it. A pytest node id is
   EVERYTHING AFTER THE FIRST SPACE of a `FAILED ` line, never a whitespace-token
   index; print one RAW line beside the parsed set and report whether its own
   after-first-space form is in that set.
   CONTROL FIRST, in the same worktree, unmutated: report exit code and counts.
   Then, one mutation at a time, each reverted with `git checkout -- <path>`
   before the next and each followed by a return to the control:
   (i)  in `packages/orchestration/model_routing.py`, replace the line
        `    if model_tier_rank(reviewer_tier) < model_tier_rank(worker_tier):`
        with `    if False:`. Count that exact line in that file first: it must
        be 1. MEASURED BY THE REVIEWER at `f0bbdc5c` in a disposable worktree, as
        a behavioural probe rather than as a colour: under this mutation a table
        demoting the reviewer half WITH evidence stops being refused and the
        round's pairing reads False, and the same table WITHOUT evidence stops
        naming `reviewer_weaker_than_worker`. So SPEC (c6) and (c7) are the tests
        this must redden.
   (ii) in `packages/orchestration/role_config.py`, replace the unique
        three-line string `            stacklevel=2,` / `        )` /
        `        return TASK_CLASS_TIERS` with the same three lines whose last is
        `        return dict(configured)`. Count that three-line string in that
        file first: it must be 1 — the bare `        return TASK_CLASS_TIERS`
        line occurs TWICE, which is why the revert target is the longer string.
        This routes a REFUSED table, so SPEC (c6) and (c7) must redden on the
        pairing assertion itself rather than on the rule name.
   For each: exit code, passed/failed counts, and the FULL red id list, never
   truncated. Then report pairwise disjointness of the red sets AS A MEASURED
   RESULT, not as a fault. Read `git status --porcelain` on the PRIMARY CHECKOUT
   immediately after every mutation and after every revert, and report every
   reading. Remove the worktree by its EXACT path
   `/home/decodeux/Repos/remedy/remedy-review-r14-redproof` with
   `git worktree remove` plus `git worktree prune`, and report `ls -d` on that
   path afterwards.

G7 THE SUITES — each its own invocation, run SERIALLY, every exit code reported.
   The reviewer's reading at `f0bbdc5c` is bracketed; only the suite this round
   adds to may move. A row carrying no bracket is a suite the reviewer did not
   read at this base: report its real numbers and compare them to nothing.
     `pytest tests/orchestration/test_role_config.py -q`   [101]
     `pytest tests/orchestration/test_model_routing.py -q` [406 passed, 3 skipped, 1 warning]
     `pytest tests/orchestration/test_config.py -q`        [81]
     `pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q`   [34]
     `pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/cli/test_teach_cmd.py -q`
     `pytest tests/cli/test_init_cmd.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_budget_stop_integration.py -q`
     `pytest tests/docs/ -q`                               [295]
     `pytest tests/cli/test_golden_path.py -q`             [42, the canary]

G8 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C5 is staged — EMPTY.
   `git ls-files .remedy-wt` — EMPTY. `git worktree list` — no worktree of this
   round's making survives. `ls /home/decodeux/Repos/remedy/remedy.toml` — must
   report no such file, which is constraint 9 measured.
   `git diff --stat f0bbdc5c..<C4> -- packages/ apps/
   ':(exclude)packages/orchestration/model_routing.py'
   ':(exclude)packages/orchestration/config.py'` — must be EMPTY.
   `git diff --stat f0bbdc5c..<C4> -- docs/` — must be EMPTY.
   PER-COMMIT INSERTIONS, the `+` column only (DECISION F104 D1), for every
   commit from C0a through C4 — the commits that exist when this gate runs —
   reported cell by cell against the handback's own `## Commits` table and each
   confirmed under 500. C5's own numbers are not this gate's business: it does
   not exist yet, and §3 item 14 routes them to the next ledger entry.

Handback: rewrite `.agent/handoff.md` in full — feature and round, SESSION 4 of
F110, branch, base and head SHAs, the per-commit changed-files table with its
`+/-` column, ONE line per gate above with its real exit code, the item-status
table AGENTS.md mandates covering every C-commit and every SPEC letter, the
deviations, the open-findings count, the next expected action. It has NO length
cap (amend0827 rule 3). Then `git push -u origin
feature/f110-model-routing-by-task-class`; create NO pull request, merge nothing.
