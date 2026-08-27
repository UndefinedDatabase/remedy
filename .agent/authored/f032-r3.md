STEP R3 / F032 — T001a THE EVIDENCE-TRIPLE SCHEMA
Goal:        BUILD THE SCHEMA AND ITS VALIDATOR, WIRE NOTHING. Add ONE new
             module, `packages/orchestration/decision_evidence.py`, holding the
             ref type, the per-option outcome type, the triple, the kind
             vocabulary as a real constant, and the function that says why a
             triple is not acceptable. Add ONE new test file that pins every
             rule and proves the two discriminators the feature file calls for.
             `list_decisions` IS NOT TOUCHED THIS ROUND and no existing file
             under `packages/`, `apps/` or `tests/` is edited — the emit gate
             DECISION F032 D1 rules is T001b, and keeping the schema and its
             wiring in separate rounds is what lets the wiring round spend its
             whole gate budget on the guards it will move. This round also
             records DECISION F032 D4, which settles the names, and books one
             reviewer prose slip. YOU CREATE NO PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 DECISION F032 D4 and the prose slip · C3 the feature
             file's amendment A4 · C4 the new module · C5 the new tests · C6
             the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r3.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/decisions.md`,
             `.agent/prose_slips.md`, `docs/roadmap/features/T5_F032.md`,
             `packages/orchestration/decision_evidence.py` (NEW),
             `tests/orchestration/test_decision_evidence.py` (NEW),
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G7 orders a disposable
             worktree and G8 orders a push. NO EXISTING FILE under `packages/`,
             `apps/` or `tests/` is edited — the only two paths there are the
             two NEW files. `.agent/live_review.md` is NOT written this round:
             no finding is registered and none is resolved.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r3.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r3.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    four points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations. Declaring beats fixing every time.
 3. THE PRODUCTION CODE IS SPECIFIED, NOT SLICED. Items S1 through S9 below
    describe what the two new files must DO and what names they must EXPORT.
    You write the code. Follow the house style of the module you are joining —
    read `packages/orchestration/decision_inbox.py` first: a module docstring
    that states the public API, `from __future__ import annotations`, frozen
    dataclasses, the one-line WHY comment directly above a definition, and a
    stated deliberate absence where a reader would search for something that is
    not there. Nothing in S1-S9 is a byte-for-byte string except the names it
    puts in backticks and the two literal strings S3 names.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The module
    lands at C4 and its tests at C5, so C4 is a commit at which the new code
    exists and no test covers it; that is ordered and is not a defect to
    correct by reordering.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R2. That is
    ordered: the plan becomes current at C1, the FIRST substantive commit.
 6. THE TWO APPENDS ARE APPENDS. `.agent/decisions.md`, `.agent/prose_slips.md`
    and `docs/roadmap/features/T5_F032.md` each end this round as their own
    pre-commit blob, byte for byte, plus ONE newline, plus the slice. Nothing
    already in any of them is rewritten, deleted or touched.
 7. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph,
    never mint a finding id and never author a `Done:` line. NO FINDING IS
    REGISTERED OR RESOLVED THIS ROUND. `R-0710` stays OPEN and is NOT fixed
    here: its fix clause binds the T001 round that first edits
    `packages/orchestration/decision_queue.py`, and this round does not edit
    it. If you find a further defect, report it in the handback under
    Deviations and let the reviewer rule on it.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
 9. THE ONLY DESTRUCTIVE WORK IS G7's, AND IT IS ISOLATED. Mutation red-proofs
    run ONLY inside a disposable `git worktree` created under `.remedy-wt/`,
    never in the primary checkout, which reads `git status --porcelain` 0 lines
    at every commit and at the handback. Remove the worktree and prune before
    the handback, and report `git worktree list` as 1 line at the end.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
11. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `935ef1ed` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
12. THERE ARE NO FROM/TO REPLACEMENT PAIRS IN THIS BLOCK. PLANF032R3 is a
    whole-file replacement of `.agent/plan.md`; DEC4, SLIP and FEATA4 are
    appends. No slice carries a FROM-zero obligation.
13. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F032 and that R3 is the round. The handback has NO LENGTH CAP —
    amend0827 rule 3 withdrew every tier — so do not declare, measure or
    apologise for its length. It is VALID when its mandated sections are
    present.

Spec — the two NEW files. Nothing here edits an existing file.
 S1. `packages/orchestration/decision_evidence.py`, NEW. Its module docstring
     states the public API and says in one sentence that this module is pure:
     no I/O, no imports from `decision_queue`, and therefore no import cycle
     when `list_decisions` starts calling it in T001b.
 S2. THE KIND VOCABULARY IS A REAL CONSTANT, NOT A COMMENT.
     `DECISION_EVIDENCE_REF_KINDS`, a `frozenset` of exactly the four strings
     `file`, `failure`, `coverage`, `decision`. A one-line WHY comment above it
     records that this is deliberately F066's vocabulary
     (`docs/roadmap/features/T3_F066.md:24-29`) so that when F066 lands the
     migration is a rename onto its constant rather than a re-typing, per
     DECISION F032 D2 — and that the two nearest existing types,
     `provider_trust_verification.ProviderVerificationEvidenceRef` and
     `orchestrator_brain.OrchestratorEvidenceRef`, both state their vocabulary
     only in a comment, which is the failure this constant exists to avoid.
 S3. TWO MODULE-LEVEL STRING CONSTANTS, each with its WHY comment.
     `NO_MATERIAL_DOWNSIDE`, whose value is exactly
     `no material downside identified` — the literal
     `docs/roadmap/features/T5_F032.md:78-80` permits for a genuinely benign
     case. And `UNKEYED_OPTION`, whose value is the EMPTY STRING, the option
     key a decision with no options list uses, per DECISION F032 D3.
 S4. THREE FROZEN DATACLASSES. `DecisionEvidenceRef` with fields `kind`,
     `target`, `label`, all `str`. `DecisionOptionOutcome` with fields
     `option`, `expected_outcome`, `downside`, all `str`.
     `DecisionEvidenceTriple` with `refs: tuple[DecisionEvidenceRef, ...]` and
     `outcomes: tuple[DecisionOptionOutcome, ...]`. Names carry a domain word
     because `EvidenceRef` alone would not grep to itself — DECISION F032 D4.
 S5. `BOILERPLATE_PHRASES`, a `frozenset` of generic filler that must never
     stand as an outcome or a downside. Choose the members yourself from what a
     lazy producer would actually write — `n/a`, `none`, `tbd`, `unknown`,
     `see above` and their kind — and say in the WHY comment that the set is
     the anti-boilerplate denylist the feature file makes acceptance material
     (`docs/roadmap/features/T5_F032.md:71-75`), that matching is
     case-insensitive on the stripped string, and that
     `NO_MATERIAL_DOWNSIDE` is deliberately NOT a member because the feature
     file permits it by name.
 S6. `evidence_triple_problems(triple, *, options)` returns a `list[str]` —
     one plain sentence per reason the triple is unacceptable, EMPTY when it is
     acceptable. `options` is the decision's own options list, possibly empty.
     It raises on no input; a malformed triple produces problems, never an
     exception, because this function is about to be called on every card and a
     raise there would lose the decision. The rules, each producing its own
     distinct sentence: (a) `refs` is empty; (b) a ref whose `kind` is not in
     `DECISION_EVIDENCE_REF_KINDS`; (c) a ref whose `target` is empty or
     whitespace; (d) an outcome whose `expected_outcome` is empty or
     whitespace; (e) an outcome whose `downside` is empty or whitespace; (f) an
     outcome whose `expected_outcome` or `downside` is a boilerplate phrase;
     (g) WHEN `options` IS NON-EMPTY, the set of outcome `option` values must
     equal the set of options exactly — report a missing option and an unknown
     option as two different sentences; (h) WHEN `options` IS EMPTY, there must
     be exactly one outcome and its `option` must be `UNKEYED_OPTION`.
 S7. `export_decision_evidence(triple)` returns the wire dict. Its keys are
     `evidence_refs`, a list of `{kind, target, label}` dicts, and `outcomes`,
     a list of `{option, expected_outcome, downside}` dicts. THE WIRE SPELLING
     IS `evidence_refs` AND THAT IS DELIBERATE: it is the name
     `docs/roadmap/features/T5_F032.md` uses throughout, and a key inside a
     decision card cannot collide with the unrelated Python attribute
     `orchestrator_brain.OrchestratorEvidenceRef`. Say that in the WHY comment,
     because it is exactly the question a reader will have.
 S8. A DELIBERATE-ABSENCE PARAGRAPH in the module docstring, in the AGENTS.md
     idiom: Remedy deliberately does NOT resolve a ref or render a staleness
     badge here, because the resolver is F066 and is unbuilt — a badge with no
     resolver behind it would be a false live indicator. A reader searching
     this module for `resolve` must land on that sentence.
 S9. `tests/orchestration/test_decision_evidence.py`, NEW. One test per rule
     (a) through (h) of S6, each asserting on the PROBLEM SENTENCE and not
     merely on the list being non-empty, plus: a test that a fully valid triple
     with options produces `[]`; a test that a valid triple with NO options and
     one `UNKEYED_OPTION` outcome produces `[]`; a test that
     `NO_MATERIAL_DOWNSIDE` is accepted as a downside, which is the
     discriminator that keeps rule (f) from swallowing the benign case; and a
     test that `export_decision_evidence` round-trips every field and emits
     exactly the two keys S7 names. Name the file's tests after the property
     they pin, in the style of the neighbouring
     `tests/orchestration/test_decision_inbox.py`.

Done when:
 G1. HYGIENE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a, which
     must be `935ef1ed5bc24a55f81d8e2ea4eaca638fd35c00`, and
     `git branch --show-current`, which must be `feature/f032-evidence-triple`.
     Report `git status --porcelain` as a LINE COUNT after each of C0a through
     C6, each 0. Report `.agent/STOP` read from disk before C0a and before C6,
     both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f032-r3.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C5 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved
     is a run of a single repeated character at length 4 or more, which must
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     scratch file, the saved copy, its mirror and the working copy, and NOT the
     bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at
     most 490.
 G4. THE PROSE WRITES. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF032R3
     under the newline-INCLUDED convention, with the negative control against
     the slice MINUS its trailing newline reported FALSE, `^## Goal$` 1,
     `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l` STRICTLY UNDER
     50. Then, at C2: `.agent/decisions.md` equals its pre-commit blob plus ONE
     newline plus DEC4, and `.agent/prose_slips.md` equals its pre-commit blob
     plus ONE newline plus SLIP. The reviewer measured those base blobs at
     `935ef1ed` as 633319 bytes and 1681 bytes. For EACH report both byte
     counts, the sum, and that the file STARTS WITH its pre-commit blob as a
     byte PREFIX. Report `^## DECISION F032 D\d+ ` moving 3 to 4 with the ADDED
     key exactly `## DECISION F032 D4`.
 G5. THE FEATURE FILE AND THE DOCS GATE. `docs/roadmap/features/T5_F032.md` at
     C3 equals its pre-commit blob plus ONE newline plus FEATA4; the reviewer
     measured that base blob at `935ef1ed` as 7291 bytes. Report both byte
     counts, the sum, and the byte-PREFIX reading. Report `^## Design
     amendments$` still exactly 1 after C3. Then, because this round writes
     `docs/roadmap/**`, run `python3 -m pytest tests/docs/
     tests/orchestration/test_roadmap_index.py -q` from the repository root and
     report the REAL exit code and the summary line VERBATIM; the reviewer
     measured `325 passed` at a REAL exit 0 at the round base.
 G6. THE NEW MODULE, LINTED AND READ BACK. After C4 run `python3 -m ruff check
     packages/orchestration/decision_evidence.py` from the repository root and
     report the REAL exit code and output VERBATIM; the reviewer measured
     `All checks passed!` at exit 0 over the two neighbouring decision modules
     at the round base, under the repository's own `pyproject.toml` and never
     `--isolated`. Then, by IMPORTING the module in a python heredoc rather
     than by grepping it, report: the sorted members of
     `DECISION_EVIDENCE_REF_KINDS`, which must be exactly `coverage`,
     `decision`, `failure`, `file`; the exact value of `NO_MATERIAL_DOWNSIDE`
     and of `UNKEYED_OPTION`; the field names of each of the three dataclasses
     in declaration order; whether each is frozen; the sorted members of
     `BOILERPLATE_PHRASES`; and whether `NO_MATERIAL_DOWNSIDE` is a member of
     it, which must be FALSE. Report the count of `resolve` occurrences in the
     module, and quote the deliberate-absence sentence S8 orders.
 G7. THE NEW TESTS, GREEN, THEN RED UNDER MUTATION, THE MUTATIONS ISOLATED.
     After C5 run `python3 -m pytest tests/orchestration/test_decision_evidence.py
     -q` from the repository root and report the REAL exit code and the summary
     line VERBATIM. Then create ONE disposable worktree at the C5 commit under
     `.remedy-wt/`, and inside it run the SAME scoped command FIRST WITH NOTHING
     MUTATED and report its REAL exit code and summary as the CONTROL — a colour
     with no baseline is not evidence. Then, one at a time and restoring between
     each, apply these four mutations to the worktree's copy of
     `packages/orchestration/decision_evidence.py` and report for EACH the REAL
     exit code and the summary line: (i) make rule (a) never fire, so an empty
     `refs` is accepted; (ii) make rule (b) never fire, so an unknown kind is
     accepted; (iii) make rule (f) never fire, so a boilerplate phrase is
     accepted; (iv) make rule (g)'s missing-option half never fire. REPORT THE
     COLOUR AND THE COUNT YOU OBSERVE — this block names no expected number of
     failures and no test name, because a red proof that quotes a count the
     block supplied proves the block and not the tests. IF ANY MUTATION LEAVES
     THE RUN GREEN, say so plainly rather than reassuring: that is a real
     finding about the tests and the reviewer wants it. Then remove the worktree
     and prune.
 G8. STRUCTURE, ARTIFACTS, THE STATE READERS, THE OPEN PR GATE AND THE PUSH.
     Run, as ONE pytest process and never two at once, `python3 -m pytest
     tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
     -q` and report the REAL exit code, the summary VERBATIM and the COUNT of
     `^FAILED` lines, proving your extractor sighted on a string you know
     contains one; the reviewer measured `620 passed` at a REAL exit 0 at the
     round base. Compare the path set of `git diff --name-only 935ef1ed..C5`
     BOTH WAYS against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md` — and report both residues EMPTY. Report `git diff
     --stat 935ef1ed..C5` restricted to `apps/` and confirm it EMPTY, and
     restricted to `packages/` and `tests/` and confirm each holds EXACTLY the
     one NEW file S1 and S9 name. Report each commit's insertions from `git
     diff --numstat` for C0a through C5, confirm each single-parent and under
     500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in every file
     this round writes other than the two block copies, against a CONTROL over
     the C0a blob which is not 0. Report `git ls-files .remedy-wt` 0 lines,
     `git worktree list` 1 line, and `git branch --list "tmp/*"` 0 lines. Run
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     and report it VERBATIM; the reviewer read `[]` at the round base; MERGE
     NOTHING and CREATE NOTHING. After C6, run `git push origin
     feature/f032-evidence-triple`. ITS OUTCOME IS NOT A VALUE OF ANY FILE THIS
     ROUND WRITES, so `.agent/handoff.md` states the push only as an INTENT
     under `## External actions`, with NO exit code and NO remote tip; report
     the real exit code and the resulting remote tip in your completion report
     instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: the `## Session` section constraint 13 orders, feature and
             round, branch, the round base SHA `935ef1ed`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S9, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. UNDER DEVIATIONS, STATE THE FOUR
             MUTATION RESULTS IN ONE LINE EACH, and state plainly whether any
             left the suite green.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R3
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D4.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R3 is T001a: the schema and its validator, wired to nothing. One new module
`packages/orchestration/decision_evidence.py` and one new test file. The emit
gate DECISION F032 D1 rules is deliberately held back to T001b so that the
wiring round can spend its whole gate budget on the guards it moves, which
inventory Q8 lists. DECISION F032 D4 settles the names against the two
collisions the reviewer measured in the source.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 DECISION F032 D4 and one prose slip | ordered | names, and a wrapped row |
| C3 the feature file amendment A4 | ordered | where a builder reads it |
| C4 the new module | ordered | S1 through S8 |
| C5 the new tests | ordered | S9, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T001b: the emit gate at `list_decisions`, legacy rendering for records with
   no triple, and the CI canary a tripleless producer must fail. That round
   first edits `packages/orchestration/decision_queue.py`, so `R-0710`'s fix
   clause binds it.
2. T002 the per-producer upgrades, with the content goldens.
3. T003 card enrichment and the chip deep links.

## Risks
- The schema lands at C4 with no test until C5. That is ordered rather than
  accidental, and the round does not end between them.
- `R-0710` stays open through this round by design; it is not a `while I am
  here` edit and its fix has a named owner.
<<<END PLANF032R3

<<<SLICE DEC4
## DECISION F032 D4 (2026-08-27) — the Python names carry a domain word; the WIRE name stays `evidence_refs`

THE QUESTION, found by reading the source before ordering the code rather than
after. `docs/roadmap/features/T5_F032.md` names the field `evidence_refs[]`
throughout and suggests the test path
`tests/orchestration/test_evidence_triple.py`. Both spellings are already taken
in this repository, for different concepts. `packages/orchestration/watchdog.py:63`
calls its own three-part evidence "the evidence triple", and
`tests/orchestration/test_watchdog.py:533` and `:873` name two tests after it.
`packages/orchestration/orchestrator_brain.py` carries
`evidence_refs: list[OrchestratorEvidenceRef]` at `:187` and `:208` and uses the
attribute thirteen times, where `OrchestratorEvidenceRef` (`:87-95`) has fields
`source`, `status`, `ref`, `summary` — a different shape for a different
purpose. AGENTS.md's Code Discoverability Conventions require one spelling per
concept repo-wide and a name that greps to its own definition and real usages
only, so taking either spelling for F032's Python surface would make BOTH
concepts unfindable by text search, which is how every worker and reviewer here
navigates.

CHOSEN, AND IT IS A SPLIT BETWEEN THE TWO LAYERS BECAUSE THEY HAVE DIFFERENT
NAMESPACES. The Python module is `packages/orchestration/decision_evidence.py`
and its types are `DecisionEvidenceRef`, `DecisionOptionOutcome` and
`DecisionEvidenceTriple`; the kind vocabulary is `DECISION_EVIDENCE_REF_KINDS`;
the test file is `tests/orchestration/test_decision_evidence.py`, which also
satisfies the convention that a test file is named after the source it covers.
The WIRE key stays `evidence_refs`, exactly as the feature file specifies,
because a key inside a decision card's JSON is namespaced by the card and cannot
collide with a Python attribute on an unrelated dataclass — and because changing
it would put this decision at odds with the one document a later reader treats
as the specification.

ALTERNATIVES CONSIDERED. Taking `evidence_triple.py` and renaming the watchdog's
usage: rejected because AGENTS.md forbids mass renames of existing code as their
own activity and the watchdog is not in F032's scope. Prefixing only the module
and leaving bare type names: rejected because `EvidenceRef` is precisely the name
that would not grep to itself, which is the convention's own stated test.

THIS DIVERGES FROM THE FEATURE FILE'S SUGGESTED TEST PATH, and the file says
"Suggested tests", so nothing binding is broken; amendment A4 records it where a
builder reads it.

REVERSE by deleting this decision, renaming the module and its three types back
to the bare spellings, and accepting the two collisions.
<<<END DEC4

<<<SLICE SLIP
- 2026-08-27 · F032 R2 · An item-status row in the authored `.agent/plan.md`
  replacement wrapped across two source lines, so the markdown table rendered
  one ordered item as two rows; the worker applied it byte for byte and
  declared it, and the next round's plan rewrite clears it.
<<<END SLIP

<<<SLICE FEATA4
**A4 — the Python names carry a domain word; the wire name is unchanged
(DECISION F032 D4).** Both spellings this file uses are already taken in the
source for other concepts: `packages/orchestration/watchdog.py:63` calls its own
three-part evidence "the evidence triple", and
`packages/orchestration/orchestrator_brain.py:187` carries
`evidence_refs: list[OrchestratorEvidenceRef]`, a different shape for a different
purpose. So the Python surface is `packages/orchestration/decision_evidence.py`
with `DecisionEvidenceRef`, `DecisionOptionOutcome`, `DecisionEvidenceTriple` and
`DECISION_EVIDENCE_REF_KINDS`, and the tests live at
`tests/orchestration/test_decision_evidence.py` rather than at the
`test_evidence_triple.py` suggested under Do-not-touch above. THE WIRE KEY IS
STILL `evidence_refs`, exactly as this file specifies everywhere else: a key
inside a decision card is namespaced by the card and collides with nothing.
<<<END FEATA4
