# STEP R1/F040 — CLAIM THE FEATURE, DISCHARGE THE TWO CLOSURE CANDIDATES, MEASURE THE SEAMS

Goal: open F040 on its own branch, settle the two candidates the F033 closure
gate left in `.agent/candidates.md` so the block condition lifts, and MEASURE the
four read paths the digest is a composition over — recording what is there, and
what is not.

Base: `f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`, the merge commit of pull
request 222 and the current tip of `main`. Cut the branch from it.

Branch: `feature/f040-completion-digest`

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r1.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN1
- C2  append slice RECORD1 to `.agent/live_review.md`
- C3  rewrite `.agent/candidates.md` from slice CAND1
- C4  apply pair PAIR-STATUS to `docs/roadmap/STATUS.md`
- C5  rewrite `.agent/context.md` from slice CONTEXT1
- C6  write `.agent/f040_inventory.md` — YOUR measurement, per the SPEC below
- C7  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r1.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/candidates.md
    docs/roadmap/STATUS.md
    .agent/context.md
    .agent/f040_inventory.md
    .agent/handoff.md

No file under `packages/`, `apps/`, `tests/`, `docs/guides/`, `docs/system/` or
`docs/roadmap/features/` changes this round. This round writes NO production code
and NO test.

## Constraints

1. Apply every slice BYTE FOR BYTE. Do not fix, rewrap, retitle or improve a
   slice. If a slice looks wrong, apply it as given and DECLARE the problem in
   the handback's deviations — that is the honest route and it costs nothing.
2. C0a is a COPY, never a retype: the block is on disk at
   `.remedy-wt/f040-r1-block.md`. Use `shutil.copyfile` for C0a and again for
   C0b. Its sha256 is stated in gate G1; verify BEFORE saving.
3. C1 is the FIRST substantive commit, ahead of C2, because this round touches
   the finding ledger and AGENTS.md's Commit Gate requires `.agent/plan.md` to
   match the current work before every commit.
4. The record is APPEND-ONLY. C2 appends RECORD1 and revises NOTHING already in
   `.agent/live_review.md`. R-0570's landed paragraph is NOT edited.
5. NO NEW R-ID IS MINTED THIS ROUND. The count of distinct `^- R-\d+ — ` ids is
   the same before and after C2. R-0570 stays OPEN — do not write a `Done:` or
   `Landed:` line for it.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md). PLAN1 is authored to fit;
   do not add to it.
7. Every exit code you report is REAL, taken from `subprocess.run(...).returncode`
   inside a script under the gitignored `.remedy-wt/`. Never read an exit code
   through a pipe, and never report a colour you did not run.
8. Destructive verification — the G3 byte flip — runs ONLY inside a disposable
   `git worktree`, never in the primary checkout, which satisfies
   `git status --porcelain` empty at every reading.
9. The `remedy` console script is DENIED in this sandbox. Where you need it, use
   `python3 -m apps.cli.grouped ...` and say so.
10. Commit subjects carry no leading-slash token, no absolute path and no
    secret-like string. Match the branch convention: no `Co-Authored-By` trailer.
11. Push the branch after C7 and open NO pull request. This is round 1 of the
    feature; the PR is created at closure.
12. Pair shape, measured not asserted — PAIR-STATUS: `TO contains FROM: false`,
    so it is a REWRITE, and the FROM-zero / TO-one count applies to it.

## Slices

The authored units below are PLAN1, RECORD1, CAND1, CONTEXT1 and the two halves
of PAIR-STATUS. Each is delimited by its own BEGIN and END marker line; the
marker lines are NOT part of the slice, and the slice's own bytes start on the
line after BEGIN and end with the newline before END.

<<<BEGIN PLAN1
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, opening the feature.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the two F033 closure candidates | done | this round; no id spent |
| the F040 claim and the branch | done | this round |
| the seam inventory | done | this round, `.agent/f040_inventory.md` |
| T001 the endpoint composition | open | next round, ordered from the inventory |
| T002 the hero card and its triggers | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round claims F040, discharges the two candidates the F033 closure gate
   raised, and measures the four read paths the digest composes over.
2. The round after it orders T001 — the endpoint, the next-action rule-table
   import and the fixture goldens — from what the inventory measured.
3. The ownership seam is unbuilt: F035 is `[ ]` in the ledger. The inventory
   measures that directly, and the T001 order carries the decision that settles
   what the digest does about it.

## Risks
- R-0570 (Low) stays OPEN and is deliberately NOT repaired here. Its fix edits
  `README.md` and `tests/docs/test_docs_consistency.py`, neither of which F040
  owns, and AGENTS.md forbids mixing an unrelated fix into a feature branch.
- F040's Design section names an ownership source that does not exist on disk.
  Building T001 against it verbatim would compose over nothing.
<<<END PLAN1

<<<BEGIN RECORD1
Note: F040 — THE TWO CLOSURE CANDIDATES F033 LEFT IN `.agent/candidates.md` ARE DISCHARGED IN THIS ROUND AND THE FILE IS EMPTIED, which lifts the block condition on the F040 claim. NO ID WAS SPENT ON EITHER, and the reasons differ. THE FIRST — the README's per-tier accepted list is guarded in one direction only and is now one feature short — IS NOT NEW: `R-0570` already registers exactly that defect, raised at the F085 R74 closure and OPEN ever since, and docs/agents/planner_reviewer_prompt.md §3 item 30 rules that a defect the open set already describes takes new evidence rather than a second id. THE NEW EVIDENCE, measured by the reviewer at `f5b1e6c5`: the Tier 5 block of `README.md` opens "Accepted in Tier 5 so far:" and its paragraphs name F255, F008, F009, F021, F022, F031, F032, F037, F256 and F257 — ten — while `docs/roadmap/STATUS.md` carries ELEVEN Tier 5 lines matching `^- \[x\] F\d{3} — `, the eleventh being F033 itself, and the README's own tier table reads `| 5 | Operator Cockpit | 11 | 31 |`. That is the R-0570 shape reproduced one tier over and one feature short instead of eight: `test_the_readme_reports_the_accepted_foundation_and_no_later_feature` in `tests/docs/test_docs_consistency.py` iterates the ids the README LISTS and asserts each is accepted in the ledger, which is the list-to-ledger direction only, so an accepted feature the README omits can never fail it. R-0570 STAYS OPEN and its routing is unchanged: the fix edits `README.md` and that test, neither of which F040 owns, so it belongs to the paydown branch R-0570's own text names and not to this feature.

DECISION F040 D1 — THE SECOND F033 CLOSURE CANDIDATE IS SETTLED AS NO DEFECT, AND NOTHING IS EDITED FOR IT. THE CANDIDATE claimed that the README's Tier 5 block "names ELEVEN ids of which only TEN are distinct, because `F037` occurs twice", read that as a duplicate in a hand-maintained inventory, and prescribed a deletion. THE MEASUREMENT, taken by the reviewer at `f5b1e6c5` over the region from the line `Accepted in Tier 5 so far:` to the line `Full per-feature state:`: the arithmetic is right and the diagnosis is wrong. Eleven occurrences of `F\d{3}` and ten distinct ids is what the region holds, but the ids that begin a paragraph — the entries of the list — are exactly ten, one per accepted feature, with no repeat. The eleventh occurrence is at `README.md` line 96, INSIDE the F256 paragraph, in the clause "the highlighting F037 only modelled is now rendered": a prose cross-reference to the feature F256 completes, and true. CHOSEN: no edit. Deleting that occurrence, as the candidate prescribed, would remove a correct sentence and leave F256's paragraph unable to say what F256 did. ALTERNATIVES CONSIDERED: (a) register it as a finding anyway and resolve it as a non-defect, rejected because amend0827 rule 2 reserves an id for a defect with product effect and there is nothing on disk to repair; (b) rewrite the counting so paragraph-initial ids are the only ones the region holds, rejected because the cross-reference is the useful half and a list that may not name its neighbours is a worse list. HOW TO REVERSE: any later relay may delete the clause at `README.md` line 96; D1 binds no round and pins no text. WHAT IT COSTS TO BE WRONG HERE: nothing on disk, because the candidate's own remedy was a deletion and this decision declines it — the counting rule it leaned on is recorded above so a later reader re-measuring the region does not raise the same candidate a third time.
<<<END RECORD1

<<<BEGIN CAND1
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY — no candidate is open.

The two entries the F033 closure gate raised were discharged in F040 round 1 and
the reasons are on the record in `.agent/live_review.md`: the first as new
evidence on the OPEN finding `R-0570`, which already describes that defect and
keeps its own routing, and the second as DECISION F040 D1, which measured it and
found no defect to repair. No id was spent on either.
<<<END CAND1

<<<BEGIN CONTEXT1
# Context — F040 Completion/return digest

## Active Branch
feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge commit
of pull request 222, which is the commit that accepted F033 into the ledger.

## Scope
Feature F040, `docs/roadmap/features/T5_F040.md` — a digest endpoint that
composes state, cost with its basis, ownership sentences, open decisions and ONE
primary action, the hero card that renders it, and CLI parity through
`remedy job digest`.

## Do not touch
Report content, notification channels and the home grid, per the feature file's
own Do-not-touch. `docs/roadmap/ROADMAP.md` is not edited. The digest is a
COMPOSITION: it reads finished sources and owns no new storage.

## Assumptions
- The next-action rule table is ONE source. The digest's primary action imports
  `NEXT_ACTION_RULES` from `packages/orchestration/run_report.py` rather than
  restating it, so the CTA and the report's recommendation cannot disagree.
- The ownership source named in the feature file's Design is unbuilt — F035 is
  `[ ]` in the ledger. What the digest does about it is decided from the round-1
  inventory's measurement, not assumed here.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path: the `REMEDY_DATA_DIR` single-reader invariant, the path-utils
  single-implementation invariant, the bare-`except: pass` ban, and the
  development-artifact boundary.

- This feature is UI work, so `docs/ui/design_reference/` is binding and any
  visual deviation is documented in the assumption log with a technical reason.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.
<<<END CONTEXT1

<<<BEGIN PAIRSTATUS-FROM
- [ ] F040 — Completion/return digest
<<<END PAIRSTATUS-FROM

<<<BEGIN PAIRSTATUS-TO
- [~] F040 — Completion/return digest
<<<END PAIRSTATUS-TO

## SPEC for C6 — `.agent/f040_inventory.md`, YOUR measurement

This file is NOT authored above and must not be invented. MEASURE the repository
at C5 and write what you find, with a `file:line` for every claim and the exact
command beside every count. Where something is ABSENT, say so and say how you
searched — an absence is only as wide as the search that looked for it. Six
sections, in this order:

1. THE NEXT-ACTION RULE TABLE. `NEXT_ACTION_RULES` and
   `recommended_next_action` in `packages/orchestration/run_report.py`: the
   exact type of the table, every rule id in it with its condition string, the
   signature of the function, and the type it returns. Name what a caller must
   construct to call it — the `ReportSources` fields and where each comes from.
   This is the one-source seam the digest's CTA must import rather than restate.
2. THE DECISION INBOX READ PATH. `build_decision_inbox` in
   `packages/orchestration/decision_inbox.py`: signature, what it returns, the
   per-card fields, and the ordering rule it applies. Report whether an
   URGENCY or significance value is computed there and is importable, or
   whether ordering is inlined — the feature file requires the digest's
   significance to be ONE source with the inbox, so state which it is.
3. THE COST LINE AND ITS BASIS. Where a job's cost and its ESTIMATED-versus-
   MEASURED basis are read: name the module and function, the field that
   carries the basis, and the exact vocabulary the live cost ticker renders for
   an estimated basis. Say whether one function returns both value and basis or
   whether a caller must join two sources.
4. THE OWNERSHIP SEAM. The feature file's Design orders "top ownership sentences
   (≤3)" from a phrase catalog. F035 — Ownership ledger is `[ ]` in
   `docs/roadmap/STATUS.md`. SEARCH FOR IT AND REPORT THE RESULT: give the exact
   commands you ran across `packages/` and `apps/`, what they matched, and
   whether any importable ownership source exists. This is the section the next
   round's decision rests on, so measure it rather than concluding it.
5. THE SERVER SEAM. `packages/orchestration/ui_server.py`: how an existing
   per-job read endpoint is registered and dispatched, the shape of its JSON
   envelope, and whether a route carries an explicit version field. Name the
   nearest existing endpoint the digest should be modelled on and quote its
   registration line.
6. THE UI AND CLI SEAMS. The design-reference files under
   `docs/ui/design_reference/` that bind a card of this kind, and which of the
   `--remedy-*` tokens named in the feature file's binding CSS already exist in
   the shipped `tokens.css` — report any that do NOT. For the CLI, name the
   module and the registration pattern a `remedy job digest <id>` subcommand
   would follow, quoting a sibling subcommand's registration.

Report every ABSENCE explicitly. A section that says "not found, searched with
<command>" is worth more than a confident guess, and this inventory is the
evidence the T001 order is built from.

## Done when — the gates

Run each gate and report ONE line per gate in the handback with its REAL exit
code. Every gate below runs at a commit STRICTLY EARLIER than C7, which writes
the handback; C7's own numbers are measured by the reviewer at the next gate and
are not owed here.

G1 TRANSPORT, at C0b. Compute sha256 over THREE files: the scratch original
   `.remedy-wt/f040-r1-block.md`, the committed `.agent/authored/f040-r1.md`,
   and the committed `.agent/last_block.md`. Report the one digest and the byte
   length, and state that all three are equal. This block deliberately states no
   expected digest — a file cannot carry its own sha256, and the reviewer holds
   the original and checks your reported value against its own measurement at
   the gate. ONE digest comparison, not a chain.

G2 THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to slice PLAN1 (report both
   sha256 values), its line count is under 50, and it holds `## Goal` and
   `## Next Steps`.

G3 THE RECORD APPEND, at C2. The MEASURED pre-commit byte length of
   `.agent/live_review.md` plus one separator newline plus RECORD1's byte length
   equals the committed length — re-measure the base yourself at the commit you
   append at; the reviewer read 1640101 at `f5b1e6c5`. Then TWO independent
   readings: (a) WHOLE RECONSTRUCTION — base + separator + slice compared to the
   entire committed file, not a prefix test; (b) PARAGRAPH ORDER — the last N
   blank-line units of the committed file equal RECORD1's N paragraphs IN ORDER,
   where N is COUNTED by your script and not taken from this block. NEGATIVE
   CONTROL, inside a disposable worktree: flip one byte inside the FIRST
   appended paragraph and report that BOTH readings reject the flipped file and
   accept the unflipped one.

G4 THE LEDGER, at C1 and at C2. Report, for each of the two commits: distinct
   `^- R-\d+ — ` ids, distinct `^Done: R-\d+ — ` ids, and the open count. The
   ADDED registered ids and the ADDED resolved ids must BOTH be the empty list —
   this round mints nothing and resolves nothing. Report the distinct
   `^DECISION F040 D\d+ — ` ids before and after; ADDED must be exactly
   `['D1']`. Report whether `R-0570` still has zero `^Done: R-0570` lines.

G5 THE CANDIDATES FILE, at C3. `.agent/candidates.md` is BYTE-EQUAL to slice
   CAND1 (report both sha256 values), and the string `· F033 · 2026-08-29` occurs
   0 times in it. Report its byte length before and after.

G6 THE CLAIM AND THE DOCS PINS, at C4. In `docs/roadmap/STATUS.md`:
   PAIRSTATUS-FROM occurs 0 times and PAIRSTATUS-TO occurs exactly 1 time;
   `git diff --numstat` for C4 alone reads exactly one insertion and one
   deletion over that one path; and the count of lines matching
   `^- \[~\] F\d{3} — ` in the whole file is 1. Then, at C4:
   `python3 -m pytest tests/docs/ -q` and
   `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, each its
   own REAL exit code. The reviewer measured both green at the base, 295 passed
   and 30 passed; report YOUR numbers.

G7 THE STATE READERS AND THE CANARY, at C6. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured these at the base at 508, 52, 21, 16 and 42 passed; report YOURS.

G8 THE INVENTORY AND THE TREE, at C6. `.agent/f040_inventory.md` exists and
   carries all six SPEC sections — report the heading line of each. Report the
   `file:line` count it cites and confirm every cited path resolves with
   `git ls-tree HEAD -- <path>`. Then `git status --porcelain` is EMPTY,
   `git ls-files --others --exclude-standard` has count 0, and the per-commit
   insertion counts for C0a through C6 from `git diff --numstat`, every one
   under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
state block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat` (not from file line counts — those differ on a full-file
rewrite), the deviations, the item-status table with every bundle item and every
gate appearing exactly once, and the next steps. It states `SESSION 1` of F040
and round 1. It has NO length cap. Report the two candidates as discharged and
name R-0570 as OPEN and routed away from this branch.
