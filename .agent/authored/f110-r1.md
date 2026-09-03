STEP F110 T001a / ROUND 1 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 1, ROUND 1

Goal
  Merge the F109 pull request at the Open PR Gate, claim F110 in the ledger,
  discharge the four closure candidates F109 left open WITHOUT spending an
  R-id, and land T001a: the call-site and role inventory that
  docs/roadmap/features/T3_F110.md's Orchestrator brief requires before T002.

Bundle, in this order
  A0  the Open PR Gate, the branch, and the base reading (no commit)
  C0a save this block verbatim to .agent/authored/f110-r1.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN1 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  apply PAIR S to docs/roadmap/STATUS.md and CONTEXT1 to .agent/context.md
  C3  apply DEC1 to .agent/decisions.md, SLIPS1 to .agent/prose_slips.md and
      CAND1 to .agent/candidates.md - the candidate discharge
  C4  write .agent/f110_inventory.md per SPEC INVENTORY (worker-measured)
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r1.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · docs/roadmap/STATUS.md (C2) · .agent/context.md (C2) ·
  .agent/decisions.md (C3) · .agent/prose_slips.md (C3) ·
  .agent/candidates.md (C3) · .agent/f110_inventory.md (new, C4) ·
  .agent/handoff.md (C5)

A0 - THE OPEN PR GATE, THE BRANCH, AND THE BASE
  Run the gate command and confirm the reading before merging:
      gh pr list --state open --json number,headRefName,baseRefName,isDraft
  It must show exactly one open PR, number 232, head feature/f109-semantic-dedupe,
  base main, isDraft false. Anything else: stop, write the handback, end.
  Then, and only then:
      gh pr merge 232 --merge --delete-branch
      git checkout main
      git pull --ff-only
      git rev-parse main            -> record this as BASE in the handback
      git diff --stat edb16a46 BASE -> MUST produce NO output
      git checkout -b feature/f110-model-routing-by-task-class
  The empty diff is load-bearing: every byte and count this block states was
  measured by the reviewer at edb16a46, and the empty diff is what makes those
  numbers true of BASE too. If it is NOT empty, stop and hand back. Never
  force-push, never commit on main, and create NO pull request this round.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r1.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round, before any other content
     commit, per planner_reviewer_prompt.md section 3 item 23.
  3. Newline conventions, MEASURED at edb16a46 and not guessed: .agent/plan.md,
     .agent/context.md, .agent/candidates.md and .agent/decisions.md each end
     WITH a trailing newline. .agent/prose_slips.md ends WITHOUT one (45129
     bytes, last byte not a newline) and still ends without one after C3.
  4. The STATUS edit is str.replace(FROM, TO, 1) on the file's text. No JSON or
     YAML round trip, no reformatting, no reflowing.
  5. DEC1 appends to .agent/decisions.md as the single byte newline followed by
     the slice. SLIPS1 appends to .agent/prose_slips.md as two newline bytes
     followed by the slice. CONTEXT1, PLAN1 and CAND1 REPLACE their whole files.
  6. .agent/f110_inventory.md is the worker's OWN measured content, not an
     authored slice. Every table row in it is produced by a command the file
     records verbatim, so the reviewer can re-run it.
  7. A sentence OUTSIDE the change set that this round makes stale is DECLARED
     in the handback and NOT repaired.
  8. Read .agent/STOP from disk before the first commit and again before C5. If
     it exists, finish the commit in hand, write the handback, and stop.
  9. Self-review loop before every commit (git diff --stat, git diff). Push
     after C5. No pull request, no merge beyond A0's gate.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f110-r1.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE PLAN. Extract PLAN1 from the COMMITTED authored file to scratch, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G3 THE STATUS PAIR. Count FROM in docs/roadmap/STATUS.md BEFORE C2; it must be
     exactly 1 before anything is written. After C2 report the FROM and TO counts
     and the containment test's own output, in these words:
       TO contains FROM: false
     The reviewer measured that same output at edb16a46, so this pair is a
     REWRITE and the FROM-zero count is the right proof (item 15).
  G4 THE CONTEXT AND THE CARRIER. Extract CONTEXT1 and CAND1 from the COMMITTED
     authored file and cmp each against its target -> exit 0 each. Then, on the
     written .agent/context.md, report each reading as a number, not as a word:
       grep -c '^## Active Branch'  -> 1
       grep -c '^## Steps'          -> 1
       count of 'feature/'          -> report the number
       first regex match of F followed by three digits -> report it
       'pytest' in the lowercased text -> report True
     and each of these counted to 0: steps-74_1-79 · steps-91-100 ·
     feature/steps-74 · PR #33 · Steps 91-100 · allow repo_test_run ·
     synthetic_count: 4 · job=None source_apply bypass
  G5 THE TWO APPENDS.
     (a) .agent/decisions.md, the RECORD, gets the full arithmetic amend0827
         rule 5 reserves for it. Its base size at edb16a46 is 723474 bytes:
         report base + 1 separator byte + slice length, the new size, and
         whether they are equal. Then a SECOND READER that counts no byte: split
         the WHOLE file on blank-line boundaries, let N be counted BY THE SCRIPT
         from the slice, and report whether the LAST N units equal the slice's N
         paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a scratch copy flip
         one byte inside the FIRST appended paragraph and report that the second
         reader REJECTS it.
     (b) .agent/prose_slips.md gets a BYTE-EQUALITY CHECK ONLY, which is all
         amend0827 rule 5 allows a .agent/ prose file: report whether the file's
         final bytes equal the extracted SLIPS1 slice exactly.
  G6 THE INVENTORY. On .agent/f110_inventory.md after C4:
       git ls-files .agent/f110_inventory.md -> returns the path
       the count of BASE occurrences in it   -> at least 1
       every repository path it names resolves: run git ls-files -- <path> for
         each backtick-quoted path token, and report BOTH the number checked and
         the number that did NOT resolve, which must be 0
       for each of sections A, B and C: RE-RUN the command the file records for
         that section and report whether the re-run's line count equals that
         section's table row count
       report the list of headings beginning '## ' the file actually holds
     The re-run equality is this gate's discriminator: it is what a hand-written
     table cannot pass.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. The reviewer measured
     every one of these at edb16a46; this round edits no test and no production
     code, so a MOVED COUNT IS ITSELF THE FINDING.
       python3 -m pytest tests/docs/ -q                                295 passed
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q   30 passed
       python3 -m pytest tests/ui_server/ -q                           515 passed
       python3 -m pytest tests/orchestration/test_test_runner.py -q     52 passed
       python3 -m pytest tests/regression/test_resource_safety.py -q    21 passed
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q  16 passed
       python3 -m pytest tests/cli/test_golden_path.py -q               42 passed
     THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The last is the canary
     every handback owes.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, and git ls-files .remedy-wt (no output).
     Then, for C0a, C0b, C1, C2, C3 and C4 - the commits BEFORE the handback
     commit, per item 14 - report each one's insertion count from
     git show --numstat, the '+' column ONLY (AGENTS.md DECISION F104 D1), and
     compare it CELL BY CELL against the Commits table of the handback you are
     writing (item 28). C5's own numbers go to NEITHER a round report NOR this
     file: under self-drive there is no round-report channel (item 31), and the
     reviewer measures them at the next gate. Then THE STALENESS SWEEP over
     every file this round touched, one entry per file, stale or NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. It carries the
  SESSION NUMBER of the running feature - this is SESSION 1 of F110 - the state
  block, the item-status table with every ordered item appearing exactly once,
  the Commits table, one line per gate followed by the transcripts, the
  deviations, and the next steps. It has no length cap. Report BASE, the merge
  result of pull request 232, and the push result.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN1,
CONTEXT1, PAIR S FROM, PAIR S TO, DEC1, SLIPS1 and CAND1.

<<<BEGIN PLAN1>>>
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

Round 1, session 1 — merge F109's pull request at the Open PR Gate, claim
F110 in the ledger, discharge the four closure candidates F109 left open,
and land T001a: the call-site and role inventory that
`docs/roadmap/features/T3_F110.md`'s Orchestrator brief requires as a
deliverable BEFORE T002. The inventory is MEASURED from the code, never
recalled.

## Next Steps

- T001b: the single resolver seam. The inventory decides whether model
  selection is already consolidated in
  `packages/orchestration/role_config.py` or must be consolidated first.
- T002: the resolver, the config schema, the hard-rule checks, and one
  violating fixture per rule, refused with the rule named.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The integration gate, then the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- Model selection is scattered today: `resolve_role_config` has production
  callers in several modules while `make_structured_call_fn` is called at
  sites that pass no resolved model at all. Consolidation is the first
  order and it touches live call paths.
- `R-0768` is OPEN over exactly this seam. F110 must not silently absorb
  its repair; the inventory records the overlap and leaves it registered.
<<<END PLAN1>>>

<<<BEGIN CONTEXT1>>>
# Context — F110 Model routing by task class

## Active Branch
feature/f110-model-routing-by-task-class, cut from `main` at the merge
commit of pull request 232.

## Scope
F110 (Tier 3, depends on F103 — done): each provider call declares a task
class; a router maps classes to model tiers; every routed call records the
routed model with its reason; the hard rules of
`docs/agents/model_routing_policy.md` are enforced in code; and a class
moves to a cheaper tier only against documented benchmark evidence. Task
slicing: T001 the call-site and role inventory, the single resolver seam
and the class declarations; T002 the resolver, the config schema and the
hard-rule checks with a refused fixture per rule; T003 the
promotion-evidence discipline, the evidence fields and the goldens.

## Do not touch
Failover chains, local-endpoint setup and learned routing — all explicitly
out of scope per `docs/roadmap/features/T3_F110.md` Do not touch. Model
UNAVAILABILITY belongs to the failover feature; F110 only picks the
intended model. `packages/orchestration/builder_routing.py` is a DIFFERENT
routing layer — it decides WHEN an expensive builder is worth spending, not
WHICH model a task class gets — and F110 neither edits nor absorbs it.

## Assumptions
- `docs/agents/model_routing_policy.md` is the human-readable policy and
  stays so; F110 seeds the class table FROM it and enforces it in code,
  and the acceptance line is a sync test that diffs the two.
- `packages/orchestration/role_config.py` resolves provider, model and
  effort per ROLE today. Whether it is already the single selection seam
  or only one of several is what T001a MEASURES rather than assumes.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- This session's reviewer CAN execute `ruff`, measured at the F110 claim as
  version 0.15.17 with `ruff check packages/orchestration/role_config.py`
  answering "All checks passed!" under the repository's own configuration.
  F109's opposite constraint was measured for F109 and does NOT carry
  forward: a round of F110 that ships a `.py` file may gate on ruff.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.
<<<END CONTEXT1>>>

<<<BEGIN PAIR S FROM>>>
- [ ] F110 — Model routing by task class
<<<END PAIR S FROM>>>

<<<BEGIN PAIR S TO>>>
- [~] F110 — Model routing by task class
<<<END PAIR S TO>>>

<<<BEGIN DEC1>>>
## DECISION F110 D1 (2026-09-03) — the section 3 checklist consolidation F109 owed is carried into F110's closure sequence

CONTEXT. Operator amendment amend0827-process-diet rule 4 freezes the
pre-emission checklist of `docs/agents/planner_reviewer_prompt.md` section 3
while a feature is open, and requires the consolidation pass to happen EXACTLY
ONCE per feature, inside the closure sequence, coming out the SAME LENGTH OR
SHORTER. F109 never performed it. MEASURED at `edb16a46`:
`git log 5e18a853..edb16a46 -- docs/agents/planner_reviewer_prompt.md` returns
no commit, so that file was never touched on the F109 branch. F109's own round
21 handback declared the omission as its deviation D3, and F109's closure gate
raised it as the first of the four closure candidates.

CHOSEN. F110's closure sequence runs ONE consolidation pass covering BOTH
features' lessons, against the ceiling amend0827 rule 4 names — the item count
the checklist stood at on 2026-08-27, which that rule states and this DECISION
deliberately does not restate. F109's lessons are on disk for that pass to
consume: the same round that carries this DECISION appends to
`.agent/prose_slips.md` the entries F109's rounds 8 through 21 owed and never
wrote.

ALTERNATIVE CONSIDERED AND REJECTED. Run the consolidation now, as a round of
its own on the F110 branch. Rejected because amend0827 rule 4 places the pass
inside a closure sequence and inside a round that is running anyway, while
amend0827 rule 1 forbids a round whose whole change set is corrections — so
running it now would break both halves of the order it exists to satisfy.

NOT AVAILABLE. Reopening F109 to perform the pass there: F109 is `[x]` in the
ledger, its branch is merged, and the self-drive guardrail G2 forbids rewriting
landed history.

CONSEQUENCE. The checklist stays unchanged and therefore NOT WRONG — only
unconsolidated — until F110's closure sequence. The ceiling that pass measures
against is amend0827 rule 4's own figure, and F110 may not raise it.

REVERSE by deleting this DECISION; the obligation then reverts to whatever a
later relay rules, and the checklist is untouched either way.
<<<END DEC1>>>

<<<BEGIN SLIPS1>>>
2026-09-03 · F109 R18 · The reviewer's own `R-0783` finding text called itself "THE SIXTH SITE" of the stale-prose class while its own enumeration omitted `R-0782`, making the true count SEVEN; corrected in the round 18 gate entry rather than here, because this file stopped being written after round 7. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R18 · The reviewer's own step block gate G6 required a marker string to "resolve in the modules named", where that string is defined in ONE module and reaches the other by import, so the clause was unmeetable for the second module. Reviewer-prose defect in a gate, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R18 · The reviewer's own step block gate G3(d) named a base two rounds earlier than G3(a) named, so the ledger delta that clause ordered spanned two rounds instead of one. Reviewer-prose citation drift between two clauses of one block, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R17 · The reviewer's own step block constraint 6 sent a running suite's log to a path INSIDE the measured repository on an over-wide reading of `R-0176`, which the worker corrected by measuring that `worktree_identity()` cannot see a gitignored file. Reviewer-prose over-wide constraint, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R17 · The reviewer's own step block implied `REMEDY_UI_NO_AUTO_BUILD` for the whole integration gate, where `docs/agents/integration_gate.md` scopes that variable to the BASE run alone. Reviewer-prose over-wide constraint, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R20 · The reviewer's own step block asserted the review zip would land in the repository root, where the packager archives it OUTSIDE the repository. Reviewer-prose defect in a stated location, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R21 · The reviewer's own closure block named `.agent/plan.md` in the path set its commit C3 had to touch while the same block's bundle assigned the single authored plan slice to C1, leaving C3 no plan diff to make; the worker declined both routes to a green gate, reported the gate PARTIAL and landed four paths. This is the `R-0527` class, and the checklist neighbour is section 3 item 35. Reviewer-prose contradiction between a constraint and a bundle of one block, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R21 · The reviewer's own closure block gate G6 ordered the literal U+2014 count in `scripts/self_use_queue.json` compared before and after the edit as the discriminator against a `json.dumps` round trip, and that count is 0 on both sides because `R-0785`'s damage had already escaped every such character on disk, so the reading cannot distinguish a correct text edit from the round trip it was written to catch; the worker declared it vacuous and supplied three non-vacuous readings. The checklist item is section 3 item 27, and the underlying on-disk defect stays registered as `R-0785` with no second id minted, per section 3 item 30. Reviewer-prose defect in a gate, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS1>>>

<<<BEGIN CAND1>>>
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY — no candidate is open.

The entries F109's closure gate recorded on 2026-09-03 were discharged in F110
round 1 without spending an R-id, which is what operator amendment
amend0827-process-diet rule 2 requires of a reviewer-prose inaccuracy that left
nothing wrong on disk. The entry naming the §3 checklist consolidation pass F109
owed and never performed is resolved inline as DECISION F110 D1 in
`.agent/decisions.md`, which carries that pass into F110's own closure sequence
against the ceiling amend0827 rule 4 names. The remaining entries — the lessons
rounds 8 through 21 promised `.agent/prose_slips.md` and never wrote, the round
21 block's closure path set naming a file it left nothing to write, and that
block's vacuous U+2014 gate clause — are appended to `.agent/prose_slips.md` as
dated lines in that same round. The on-disk defect underlying the vacuous clause
was already registered as `R-0785`, and no second id was minted for it, per
docs/agents/planner_reviewer_prompt.md §3 item 30.

The entry F108's closure round recorded on 2026-09-02 — `README.md` carries
F106's capability paragraph twice, the second copy misplaced under "Accepted
in Tier 5 so far" — was registered in F109 round 1 as finding `R-0769` in
`.agent/live_review.md`; the reason, the measurement and the routing are on
that record. The entry recorded after F106's closure (job/mission
resume-from-persisted-state, DECISION F106 D2) was registered in F108 round 1
as finding `R-0762` on the same record.
<<<END CAND1>>>

SPEC INVENTORY - .agent/f110_inventory.md, written by YOU from MEASUREMENT
  This is NOT an authored slice. You measure, you write. It is T001a's
  deliverable and the feature file's Orchestrator brief requires it before T002.
  It states the SHA it was measured at - BASE, the value A0 recorded - because a
  present-tense fact about a source file needs the commit it was read at
  (planner_reviewer_prompt.md section 3 item 20).
  Sections, each under a heading beginning '## ':
    A  Every PRODUCTION call site of resolve_role_config - excluding its own
       module packages/orchestration/role_config.py and excluding tests/.
       Columns: path, enclosing symbol, the role argument, what the caller does
       with the result.
    B  Every PRODUCTION call site of make_structured_call_fn. Same columns, plus
       a column answering whether a resolved model is passed at that site.
    C  Every PRODUCTION call site of create_provider. Same columns.
    D  Every role in role_config.KNOWN_ROLES, and for each, whether section A, B
       or C found a production call site for it. A role with NO call site is
       named as having none - that absence is a result, not an omission.
    E  THE VERDICT T001a EXISTS TO PRODUCE: is model selection already
       consolidated at ONE seam, or is it scattered? Answer it from A through D,
       and if scattered, state the consolidation order T001b will carry.
    F  The overlap with the OPEN finding set. R-0767 and R-0768 both sit on this
       seam. Name them, state what each would change here, and leave both
       REGISTERED and unrepaired - repairing another feature's defect from this
       branch is the scope drift AGENTS.md forbids.
    G  The routing layers this repository already has and how they differ, so no
       later reader conflates them: this feature's class-to-tier routing,
       packages/orchestration/builder_routing.py (WHEN an expensive builder is
       worth spending), and packages/orchestration/model_route_tournament.py.
  Method, and it is load-bearing: for sections A, B and C, record the EXACT
  command that produced the list, verbatim, in the file. G6 re-runs each one and
  compares its line count against your table's row count, so a hand-written
  table fails that gate.
