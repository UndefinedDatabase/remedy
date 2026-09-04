STEP F262 CLAIM / ROUND 1 - F262 List commands v2 (dates, sort, filter)
FEATURE F262 - List commands v2 (Tier 2) - SESSION 1, ROUND 1

Goal
  Claim F262 in the STATUS ledger and set .agent/plan.md and
  .agent/context.md for the branch, which the reviewer already cut from
  main at pull request 235's merge commit (7c65d9cc). No production code
  this round: T001 (the shared listing-option surface) lands in round 2.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r1.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN1 to .agent/plan.md (FIRST substantive commit)
  C2  apply PAIR S to docs/roadmap/STATUS.md and CONTEXT1 to .agent/context.md
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r1.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - docs/roadmap/STATUS.md (C2) - .agent/context.md (C2) -
  .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f262-r1.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice
     looks wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round, before any other
     content commit.
  3. Newline conventions, measured on the scratch originals before
     emission and re-measured on the committed file after C1/C2: PLAN1
     and CONTEXT1 both end WITHOUT a trailing newline (the last byte of
     each slice, between its own END marker's preceding newline and the
     marker line, is not itself a newline) - .agent/plan.md and
     .agent/context.md must match, byte for byte, after C1/C2
     respectively. Report `tail -c 1 <path> | od -An -tx1` for both
     written files; neither may print `0a`.
  4. The STATUS edit is str.replace(FROM, TO, 1) on the file's text. No
     JSON or YAML round trip, no reformatting, no reflowing.
  5. PLAN1 and CONTEXT1 REPLACE their whole files.
  6. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  7. Read .agent/STOP from disk before the first commit and again before
     C3. If it exists, finish the commit in hand, write the handback, and
     stop.
  8. Self-review loop before every commit (git diff --stat, git diff).
     Push after C3 (git push -u origin feature/f262-list-commands-v2).
     No pull request, no merge.
  9. This branch was cut directly by the reviewing session (git plumbing
     only - no file content was authored by that session; every byte in
     every commit still comes from a worker). PR #235, the PREVIOUS
     feature's PR, was already merged by the reviewer in an earlier
     session - do not touch it, do not run the Open PR Gate, do not
     re-create the branch. `git rev-parse HEAD` before C0a must read
     `7c65d9ccfb512aef1c3eea0245030647332c26ea` (report the full SHA);
     `git branch --show-current` must read
     `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r1.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE PLAN. Extract PLAN1 from the COMMITTED authored file to scratch,
     then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G3 THE STATUS PAIR. Count FROM in docs/roadmap/STATUS.md BEFORE C2; it
     must be exactly 1 before anything is written. After C2 report the
     FROM and TO counts and the containment test's own output, in these
     words:
       TO contains FROM: false
     This pair is a REWRITE and the FROM-zero count is the right proof.
  G4 THE CONTEXT. Extract CONTEXT1 from the COMMITTED authored file and
     cmp against .agent/context.md -> exit 0. Then, on the written
     .agent/context.md, report each reading as a number, not as a word:
       grep -c '^## Active Branch'  -> 1
       grep -c '^## Steps'          -> 1
       count of 'feature/'          -> report the number
       first regex match of F followed by three digits -> report it
       'pytest' in the lowercased text -> report True
  G5 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. This round edits
     no test and no production code, so a MOVED COUNT IS ITSELF THE
     FINDING.
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report the pass count of each; the reviewer will diff them against a
     base reading taken independently. THE FOUR STATE READERS ARE RUN AS
     FOUR, NOT AS THREE. The last is the canary every handback owes.
  G6 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C3 is staged, and git ls-files .remedy-wt (no
     output - nothing under .remedy-wt/ is ever committed). Then, for
     C0a, C0b, C1 and C2 - the commits BEFORE the handback commit - report
     each one's insertion count from git show --numstat, the '+' column
     ONLY, and compare it CELL BY CELL against the Commits table of the
     handback you are writing. C3's own numbers go to NEITHER a round
     report NOR this file - the reviewer measures them at the next gate.
     Then THE STALENESS SWEEP over every file this round touched, one
     entry per file, stale or NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. It
  carries the SESSION NUMBER of the running feature - this is SESSION 1
  of F262 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are
PLAN1, CONTEXT1, PAIR S FROM and PAIR S TO.

<<<BEGIN PLAN1>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 1, session 1 — claim F262 in the STATUS ledger and set this file
and `.agent/context.md`. Branch already cut. Round 2 builds T001: the
shared listing-option surface (four flags defined once, wired into the
argument layer), plus a test deriving the list-command set mechanically
from `apps/cli/command_catalog.py`, failing loudly with the valid set
named — first, per the feature file's Orchestrator brief.

## Next Steps

- Round 2 (T001): state the exact mechanical rule for "list command"
  over the catalog (`subcommand` equal to `list` or ending `-list` is
  the working hypothesis; `checklist` a same-suffix false positive,
  `snapshot list-applies` a narrower listing to classify explicitly),
  wire the four flags once, ship the coverage test.
- T002: CREATED/UPDATED on every row, per store; an unknown date renders
  as unknown, never invented. Widest slice — plan its commit split first.
- T003: the sort/filter/limit behaviour plus the newest-first default.
  Depends on both T001 and T002.

## Risks

- Measured at this branch's base (`7c65d9cc`): 28 catalog `subcommand=`
  values are exactly `list` or end `-list` — a sizing signal only, not a
  spec; round 2 states and gates the real rule.
- Some stores may lack a CREATED/UPDATED timestamp today; T002 surfaces
  each gap per store, not assumed here.
- `--json`'s existing keys are not renamed, only added to (Do not touch);
  every T002/T003 store change is checked against that before landing.
<<<END PLAN1>>>

<<<BEGIN CONTEXT1>>>
# Context — F262 List commands v2 (dates, sort, filter)

## Active Branch
feature/f262-list-commands-v2, cut from `main` at the merge commit of
pull request 235.

## Scope
F262 (Tier 2, depends on nothing, blocks nothing): every list command —
`job list`, the `do` run listings, `queue list`, `mission list`,
`memory list`, `event list` and the rest of the catalog's list-shaped
commands — shows a CREATED and an UPDATED date and supports the same
`--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags with the same spelling; default ordering is newest-first
everywhere, without a flag. Task slicing: T001 the shared listing-option
surface, defined once and pinned by a catalog-derived coverage test; T002
CREATED/UPDATED dates surfaced from each store; T003 the sort/filter/limit
behaviour plus the newest-first default.

## Do not touch
The stores' own schemas beyond adding a missing timestamp, and the
`--json` contract's existing keys — this feature ADDS keys, it does not
rename them (docs/roadmap/features/T2_F262.md, Do not touch).

## Assumptions
- The list-command set is derived MECHANICALLY from
  `apps/cli/command_catalog.py` in round 2, never hand-written; today's
  measurement (28 subcommands matching `list` or `*-list`) is a sizing
  signal for this file only, not the rule itself.
- `--sort <field>` validates against the CALLING list's own columns and
  fails non-zero naming the valid set, per the feature file's Design
  section — the valid-field set is therefore per-command, not global.
- Dates render human-readable in the text UI and ISO-8601 with a
  timezone under `--json`; any probe added by this feature reads the
  TEXT-UI value, never the internal one (feature file, Design).
- A list whose store cannot order by recency says so rather than
  presenting arbitrary order as newest-first (feature file, Design).

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
- `ruff check` is DENIED to this session's reviewer, re-measured at the
  F262 claim (`ruff check apps/cli/command_catalog.py` answers "This
  command requires approval"). A round of F262 that ships a `.py` file
  gates `python3 -m py_compile <path>` instead, and the worker attempts
  `ruff check` itself, reporting success or the exact refusal.
- `remedy` (the built CLI) is DENIED to this session's reviewer
  session-wide; a round needing to run it delegates that run to the
  worker and reports the exact output.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.
<<<END CONTEXT1>>>

<<<BEGIN PAIR S FROM>>>
- [ ] F262 — List commands v2 (dates, sort, filter)
<<<END PAIR S FROM>>>

<<<BEGIN PAIR S TO>>>
- [~] F262 — List commands v2 (dates, sort, filter)
<<<END PAIR S TO>>>
