── STEP R7 — F255 Teacher role ────────────────────────────────
Goal:        Record the R6 verdict and BUILD the conventions half of T001:
             `teacher` joins `ConventionsRole`, its reviewed document lands
             under `docs/agents/`, the mapping pins and the rule anchors extend
             with it, and the docs index registers it. The `teacher.model`
             config key is R8's: the block cap forces that split, and the plan
             slice below says so.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST, ahead of
             the record and ahead of the work · C2 record the R6 verdict · C3
             the conventions vocabulary, its document and its pins, together ·
             C4 the docs index · C5 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r7.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `packages/orchestration/role_conventions.py` AND
                 `docs/agents/teacher_conventions.md` (CREATED by this commit)
                 AND `tests/orchestration/test_role_conventions.py` — ONE
                 commit, three files, because the enum member, the document it
                 points at and the pins that freeze the mapping are RED in
                 every subset (R-0151; measured, see constraint 5).
             C4  `docs/README.md`
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base `eb8aa9ae` and must stay untouched:
             `packages/orchestration/role_config.py`,
             `tests/orchestration/test_role_config.py`,
             `packages/orchestration/config.py`,
             `packages/orchestration/prompt_segments.py`,
             `docs/agents/worker_conventions.md`,
             `docs/agents/reviewer_conventions.md`,
             `docs/roadmap/features/T5_F255.md`, `.agent/decisions.md`,
             `.agent/context.md`, `AGENTS.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r7.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r7.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST THIS ROUND, AND THAT IS A FIX. Findings R-0377, R-0491
   and R-0548 are all OPEN and all rule that the `.agent/plan.md` update is the
   FIRST substantive commit of a round with substance to record, so that only
   the two block-save commits precede it. The R6 bundle advanced the plan at its
   C4 while its C1 registered a finding, and `.agent/plan.md` at `9d28d93c` still
   named R5 as the current step — the exact state those three findings exist to
   prevent. No new id is minted for that recurrence: checklist item 30 rules that
   an OPEN finding describing the defect takes the new evidence rather than a
   second id, and the R6 record slice below carries it.
4. TEN PAIRS, AND THEIR SHAPES DIFFER. The reviewer ran the containment test
   over each before emission and quotes each result as the test printed it.
   ENUMFROM→ENUMTO: `TO contains FROM: True` — APPEND-shaped. All nine others —
   MODDOC, PATH, NAME, HELP, SEGPIN, PATHPIN, ANCHOR, IDXQUICK, IDXTABLE —
   printed `False` and are REWRITES. G7 orders the FROM-zero count for the nine
   rewrites ONLY, and never for the append, whose FROM the applied file
   necessarily still carries (§4.9, R-0207).
5. THE ENUM, THE DOCUMENT AND THE PINS LAND IN ONE COMMIT. C3 changes three
   files at once, which this project otherwise avoids, because
   `tests/orchestration/test_role_conventions.py` parametrizes over
   `list(ConventionsRole)`: the enum member alone, with no document on disk,
   turns that file RED. The reviewer measured it — with the document deleted and
   everything else applied, that suite reports 7 failed, 28 passed. Splitting
   them is the R-0151 defect, not tidiness.
6. EVERY FROM IS UNIQUE IN ITS TARGET. The reviewer measured each of the ten
   FROM texts at exactly 1 occurrence in its file at the base. Apply each by a
   count-checked replacement: assert the FROM occurs exactly once BEFORE
   replacing, and stop if it does not.
7. THE DOCUMENT IS CREATED, NOT EDITED. `docs/agents/teacher_conventions.md`
   does not exist at `eb8aa9ae`. C3 creates it holding exactly TEACHERDOC and
   nothing else — no header, no trailing edit, no re-wrap.
8. THE LEDGER APPEND IS BLANK-SEPARATED. RECORDR6 at C2 is appended preceded by
   exactly one blank line (R-0578). This round registers NO finding and resolves
   none: the registered count stays 180 and the resolved count stays 3.
9. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
10. NOTHING ELSE IS BUILT. No `teacher.model` config key, no CLI flag, no
   narration code, no event set. If the change looks incomplete, that is because
   the config key is R8's and T002 is R9's.
11. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
12. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round: the reviewer already ran every destructive control G9 reports.
13. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R7
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R7: record the R6 verdict and build the CONVENTIONS half of T001 — `teacher`
joins `ConventionsRole`, its reviewed document lands under `docs/agents/`, the
mapping pins and rule anchors extend with it, and the docs index registers it.

## Next Steps
1. R8 ADDS THE `teacher.model` CONFIG KEY, modelled on the existing
   `orchestrator.model` spec, with its pin in the same commit. It is a round of
   its own because the R7 block reached its line cap without it.
2. R9 BUILDS T002 AND T003 TOGETHER — Stage 1 narration over an enumerated
   event set, and the behavioural read-only proof — because a read-only feature
   whose read-only-ness is unproven is this feature's likeliest failure.
3. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real.

## Risks
- FIVE ROLE LISTS EXIST AND T001 TOUCHES TWO. DECISION F255 D1 rules that the
  CLI-override and token-cost lists are deliberately NOT extended, so a later
  reader finding `teacher` absent from them is seeing a decision, not an
  omission.
- THE CONVENTIONS DOCUMENT IS CAPPED. `CONVENTIONS_TOKEN_CAP` is 800 tokens
  estimated as chars/4; the document this round authors measures 1972 chars and
  493 tokens, so 307 tokens of headroom absorb later edits.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
<<<END PLAN255R7

<<<SLICE RECORDR6
Gate: R7 — the R6 entry. R6 PASSED. No finding is registered this round and none is resolved; the one defect the gate found belongs to the R6 BLOCK and is a recurrence of findings that are already OPEN, which checklist item 30 rules must take the evidence rather than a new id. Every gate the R6 block ordered was RE-EXECUTED by the reviewer over `9d28d93c..eb8aa9ae` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r6.md`, the committed `.agent/authored/f255-r6.md` at `e6aa3338` and the committed `.agent/last_block.md` at `b83a71a4` are byte-EQUAL at sha256 e12761e56c23f6249bd50defe6d91b69cbd3e01f013195604664c16d3cbe024e over 23360 B and 284 lines, the digest stated at delegation. ELEVEN SLICES, counted by the reviewer from its own ordered extraction of the committed blob and not from the handback: the worker's independent count agrees, and the block stated no numeral of its own, which is what R-0604 asked of it one round after that finding was registered. THE TWO LEDGER APPENDS ARE PREFIX-CLEAN: the blob at `9d28d93c` is a byte-exact prefix of the blob at `033605c8` with a 1872 B, 2-line remainder equal to a newline followed by R0604, and that blob is a byte-exact prefix of the blob at `f3ae2244` with a 4990 B, 2-line remainder equal to a newline followed by RECORDR5; an independent paragraph split of the `f3ae2244` blob yields 193 units whose LAST unit is RECORDR5 byte for byte. THE SETS MOVED EXACTLY AS ORDERED: 179 registered / 3 resolved / 176 open / 0 line-anchored `Landed:` at `9d28d93c`, and 180 / 3 / 177 / 0 at both `033605c8` and `f3ae2244`; `- R-0604 — ` occurs 1x, no id is registered twice, and `Gate: R6 — the R5 entry.` occurs 1x, sits last among the lines beginning `Gate: R`, and repeats no header key. THE SOURCE COMMIT WAS RECONSTRUCTED RATHER THAN READ: applying the four authored pairs to the blobs at `9d28d93c` in the block's own order reproduces `packages/orchestration/role_config.py` and `tests/orchestration/test_role_config.py` at `c4866547` BYTE FOR BYTE, so no edit reached those files that the block did not order. The pair shapes held as declared: ROLEDOCFROM→ROLEDOCTO printed `TO contains FROM: True` and its FROM reads 1x at BOTH ends, which is why no FROM-zero count was ordered or reported for it, while the three REWRITE pairs each read FROM 1x then 0x and TO 0x then 1x; the numstat is 5/0 and 4/1. THE VOCABULARY IS REAL AND ITS PIN IS A TRIPWIRE, both re-measured by the reviewer: `python3 -m pytest tests/orchestration/test_role_config.py -q -rf` exits 0 at 32 passed in a disposable worktree at `9d28d93c` and exits 0 at 33 passed in the primary checkout at `eb8aa9ae`, the one new case being the parametrize over `KNOWN_ROLES` gaining teacher; under `warnings.simplefilter("error")` `len(KNOWN_ROLES)` is 8 and `resolve_role_config("teacher")` returns `.role == "teacher"` with model `muse-glimmer:latest` and effort `medium` and raises nothing; and the reviewer RE-RAN the mutation red-proof itself in a second disposable worktree at `eb8aa9ae` — deleting the single line holding `"teacher",` from the `KNOWN_ROLES` tuple in `packages/orchestration/role_config.py`, where those bytes occur exactly once, turns `test_all_eight_roles_present` RED at `tests/orchestration/test_role_config.py:124` with 1 failed and 31 passed. Both worktrees were removed and pruned before this verdict and `git worktree list` reports the primary checkout alone. RUFF WAS MEASURED AT BOTH ENDS so a pre-existing error could not be read as a new one: `python3 -m ruff check packages/orchestration/role_config.py tests/orchestration/test_role_config.py` exits 0 at `All checks passed!` at `9d28d93c` and again at `eb8aa9ae`. THE ROUND GATE WAS RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT, never two pytest processes at once: the four state-reader files exit 0 at 160 passed and the canary `tests/cli/test_golden_path.py` exits 0 at 42 passed. THE RANGE AND THE HISTORY HOLD: seven paths over seven single-parent commits; per-commit insertions 284, 209, 2, 2, 9, 15 and 37, every one under the 500 cap, and every `+/-` cell in the handback's `## Commits` table byte-identical to `git diff --numstat` — the reading checklist item 28 exists to force, since the worker derives that column a second time; all eight paths the block named untouched are PRESENT at `9d28d93c` and ABSENT from the range; zero lines beginning `<<<SLICE ` or `<<<END ` in any written file; `.agent/plan.md` at `94e9c4c2` byte-equals PLAN255R6 at sha256 3ca563eadb06bd687be0c6b36a624275b08b5fa60290fe38044639a0f0ae2f55 over 42 lines, under its 50-line cap; and the handback at `eb8aa9ae` is 82 lines, inside the ≤100 its seven-commit table earns. THE ONE DEFECT IS THE BLOCK'S AND NOT THE ROUND'S, AND IT IS A RECURRENCE RATHER THAN A NEW FINDING: checklist item 23 rules that a round whose bundle registers a finding advances `.agent/plan.md` as its FIRST substantive commit, and the R6 block ordered the plan at C4 while C1 registered R-0604 — so `.agent/plan.md` named R5 as the current step across `033605c8`, `f3ae2244` and `c4866547`, and AGENTS.md's Commit Gate item 1 was unmeetable at each of them. The worker followed the ordered sequence, as constraint 1 required, and nothing false was written into the record. R-0377, R-0491 and R-0548 are all registered and all unresolved, and all three rule exactly this counter-measure, so item 30 routes the evidence here instead of minting R-0605: this is their next instance, the fourth block in the family, and the R7 bundle that carries this paragraph ORDERS THE PLAN AS ITS FIRST SUBSTANTIVE COMMIT, which is the rule being obeyed rather than restated.
<<<END RECORDR6

<<<SLICE MODDOCFROM
The worker and the reviewer conventions live in ``docs/agents/`` as reviewed
documents. This module LOADS them, verbatim, and registers each one as the
<<<END MODDOCFROM

<<<SLICE MODDOCTO
Each role's conventions live in ``docs/agents/`` as a reviewed document. This
module LOADS them, verbatim, and registers each one as the
<<<END MODDOCTO

<<<SLICE ENUMFROM
    WORKER = "worker"
    REVIEWER = "reviewer"
<<<END ENUMFROM

<<<SLICE ENUMTO
    WORKER = "worker"
    REVIEWER = "reviewer"
    TEACHER = "teacher"
<<<END ENUMTO

<<<SLICE PATHFROM
    ConventionsRole.REVIEWER: "docs/agents/reviewer_conventions.md",
}
<<<END PATHFROM

<<<SLICE PATHTO
    ConventionsRole.REVIEWER: "docs/agents/reviewer_conventions.md",
    ConventionsRole.TEACHER: "docs/agents/teacher_conventions.md",
}
<<<END PATHTO

<<<SLICE NAMEFROM
    ConventionsRole.REVIEWER: "reviewer_conventions",
}
<<<END NAMEFROM

<<<SLICE NAMETO
    ConventionsRole.REVIEWER: "reviewer_conventions",
    ConventionsRole.TEACHER: "teacher_conventions",
}
<<<END NAMETO

<<<SLICE HELPFROM
    """A throwaway repo root carrying both documents at their real relative paths."""
<<<END HELPFROM

<<<SLICE HELPTO
    """A throwaway repo root carrying every document at its real relative path."""
<<<END HELPTO

<<<SLICE SEGPINFROM
            (ConventionsRole.WORKER, "worker_conventions"),
            (ConventionsRole.REVIEWER, "reviewer_conventions"),
        ],
<<<END SEGPINFROM

<<<SLICE SEGPINTO
            (ConventionsRole.WORKER, "worker_conventions"),
            (ConventionsRole.REVIEWER, "reviewer_conventions"),
            (ConventionsRole.TEACHER, "teacher_conventions"),
        ],
<<<END SEGPINTO

<<<SLICE PATHPINFROM
            (ConventionsRole.WORKER, "docs/agents/worker_conventions.md"),
            (ConventionsRole.REVIEWER, "docs/agents/reviewer_conventions.md"),
        ],
<<<END PATHPINFROM

<<<SLICE PATHPINTO
            (ConventionsRole.WORKER, "docs/agents/worker_conventions.md"),
            (ConventionsRole.REVIEWER, "docs/agents/reviewer_conventions.md"),
            (ConventionsRole.TEACHER, "docs/agents/teacher_conventions.md"),
        ],
<<<END PATHPINTO

<<<SLICE ANCHORFROM
            (
                ConventionsRole.REVIEWER,
                ("## Stance", "## Findings", "## Block conditions"),
            ),
        ],
<<<END ANCHORFROM

<<<SLICE ANCHORTO
            (
                ConventionsRole.REVIEWER,
                ("## Stance", "## Findings", "## Block conditions"),
            ),
            (
                ConventionsRole.TEACHER,
                ("## Stance", "## Grounding sources", "## Isolation"),
            ),
        ],
<<<END ANCHORTO

<<<SLICE IDXQUICKFROM
| agent conventions | [worker_conventions.md](agents/worker_conventions.md), [reviewer_conventions.md](agents/reviewer_conventions.md) | agents |
<<<END IDXQUICKFROM

<<<SLICE IDXQUICKTO
| agent conventions | [worker_conventions.md](agents/worker_conventions.md), [reviewer_conventions.md](agents/reviewer_conventions.md), [teacher_conventions.md](agents/teacher_conventions.md) | agents |
<<<END IDXQUICKTO

<<<SLICE IDXTABLEFROM
Canonical, model-agnostic role conventions and routing policy. The worker and
reviewer files are the F105 conventions prompt segments (token-capped); the
routing policy seeds F110.

| File | Description |
|------|-------------|
| [worker_conventions.md](agents/worker_conventions.md) | Worker/builder role rules (F105 conventions segment) |
| [reviewer_conventions.md](agents/reviewer_conventions.md) | Reviewer role rules + block conditions (F105 conventions segment) |
<<<END IDXTABLEFROM

<<<SLICE IDXTABLETO
Canonical, model-agnostic role conventions and routing policy. The worker,
reviewer and teacher files are the conventions prompt segments (token-capped);
the routing policy seeds F110.

| File | Description |
|------|-------------|
| [worker_conventions.md](agents/worker_conventions.md) | Worker/builder role rules (F105 conventions segment) |
| [reviewer_conventions.md](agents/reviewer_conventions.md) | Reviewer role rules + block conditions (F105 conventions segment) |
| [teacher_conventions.md](agents/teacher_conventions.md) | Teacher role rules: read-only stance, grounding sources (F255 conventions segment) |
<<<END IDXTABLETO

<<<SLICE TEACHERDOC
# Teacher Conventions (stable prompt segment)

> The F255 "conventions" segment for the teacher role: the CONTENT rules only.
> Cap 800 tokens, estimated as chars/4 (P4) — keep headroom, and point at a rule
> rather than restate it.

## Stance

The teacher reads and explains; it never writes, steers or decides. It has no
write path to a run and no influence on orchestrator, worker or reviewer
decisions. Narration that changed a run would be a defect, not a feature.

## Grounding sources

Every answer names which of the three sources below it speaks from, and never
blends them silently:

1. LEDGER AND EVIDENCE — what is happening. Assert only what the evidence
   shows; where the evidence is silent, say unknown.
2. WORKSPACE CODE, read-only — what this function or file does. Explain code
   that exists; never invent a call site, a flag or a file.
3. LANGUAGE AND CONCEPT KNOWLEDGE — what a term means. Ordinary tutor
   knowledge, and explicitly NOT a claim about this repository's state.

## Two stages, deliberately unequal in cost

Stage 1 narration is deterministic: templates keyed to an enumerated set of
run-log event names, zero tokens, no network, no model. An event outside that
set is narrated as unknown rather than guessed at — the honesty rule applied to
the feature's own blind spot.

Stage 2 answers a question through the teacher's own model over a small
context: the relevant ledger slice plus the code location asked about. Spend is
attributed to the role name `teacher` in the F103 ledger.

## Isolation

The run log is opened READ-ONLY and re-read whole through the production
reader. A malformed trailing line is dropped, never repaired. The teacher holds
no lock, subscribes to nothing, and adds no follow or tail API.

## Honesty

Say unknown. A confident narration of an event the templates do not cover, or
an explanation of code the teacher did not read, is the failure this role is
most likely to produce and the one it must refuse.
<<<END TEACHERDOC

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r7.md`, of `.agent/authored/f255-r7.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r7.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R7; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b
   (constraint 3).
G5 THE R6 VERDICT RECORDED. C2 appends RECORDR6 preceded by exactly one blank
   line. Report the PREFIX property, the remainder's sha256, byte and line
   counts, and that the separator is present. Report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR6, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base and at C2: the reviewer measured 180 / 3 / 177 / 0 at
   `eb8aa9ae`, and C2 owes the same four numbers, because a `Gate:` paragraph
   adds neither kind of line. Report that `Gate: R7 — the R6 entry.` occurs 1x,
   is the LAST line beginning `Gate: R`, and repeats no header key.
G6 THE FROM TEXTS WERE UNIQUE BEFORE THEY WERE REPLACED. For each of the ten
   FROM slices report its occurrence count in its target file at the base
   `eb8aa9ae`. The reviewer measured each at exactly 1. A count other than 1
   stops the round.
G7 THE TEN PAIRS, BY THEIR OWN SHAPES. For the nine REWRITE pairs — MODDOC,
   PATH, NAME, HELP, SEGPIN, PATHPIN, ANCHOR, IDXQUICK and IDXTABLE — report
   FROM's count at the base and after its commit, and TO's count at both ends;
   each owes FROM 0x and TO 1x afterwards. For the APPEND-shaped pair
   ENUMFROM→ENUMTO report FROM 1x at BOTH ends and each TO-ONLY line exactly 1x
   among the lines C3's diff ADDS, and do NOT report a FROM-zero count for it:
   that count is unreachable by construction (§4.9, R-0207). Report
   `git diff --numstat` for every file at C3 and at C4.
G8 THE DOCUMENT IS THE AUTHORED BYTES. Report that
   `docs/agents/teacher_conventions.md` is ABSENT at `eb8aa9ae` and PRESENT at
   C3, and that its content at C3 byte-equals TEACHERDOC — give its sha256,
   byte count, character count and line count. Report, from a short `python3 -c`
   you run yourself, the value of
   `estimate_text_tokens(role_conventions_text(ConventionsRole.TEACHER))` and
   that it is at or under `CONVENTIONS_TOKEN_CAP`. The reviewer measured 1972
   characters and 493 tokens against a cap of 800.
G9 THE CONVENTIONS VOCABULARY IS REAL, AND ITS PINS ARE TRIPWIRES. Report the
   exact command, exit code and tail of
     `python3 -m pytest tests/orchestration/test_role_conventions.py -q -rf`
   at C3. The reviewer measured exit 0 at 26 passed at the base and exit 0 at
   35 passed with this block applied — the parametrize over
   `list(ConventionsRole)` and the three literal pins gain the teacher cases.
   Do NOT run a mutation red-proof: the reviewer already ran three in a
   disposable worktree before emitting this block — deleting the document gives
   7 failed / 28 passed, renaming the document's `## Isolation` heading to
   `## Sandboxing` gives 1 failed / 34 passed at
   `tests/orchestration/test_role_conventions.py:220`, and appending 4000
   characters to the document gives 5 failed / 30 passed — and constraint 12
   forbids you creating a worktree.
G10 RUFF, SCOPED TO THE TWO PYTHON FILES C3 TOUCHES, measured against the SAME
   two files at the base so a pre-existing error is not read as a new one
   (R-0364). Report the exact command, exit code and output of
     `python3 -m ruff check packages/orchestration/role_conventions.py tests/orchestration/test_role_conventions.py`
   at C3. The reviewer measured `All checks passed!` for those two paths at the
   base and again with this block applied.
G11 THE DOCS SUITE AS A REGRESSION CHECK, because C4 edits `docs/README.md`,
   which `tests/docs/test_docs_consistency.py` reads as a PRIMARY doc. Report
   the exact command, exit code and tail of
     `python3 -m pytest tests/docs/ -q -rf`
   at C4. The reviewer measured exit 0 at 295 passed with this block applied.
   THAT RUN IS A REGRESSION CHECK AND NOT EVIDENCE ABOUT THE NEW DOCUMENT: that
   suite reads feature FILENAMES and the primary docs' own claims, and is blind
   to the body of anything under `docs/agents/`, so the proof for C3's document
   is G8 and G9 and not this gate.
G12 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state, so the four state-reader files
   gate alongside the canary. Report the exact command, exit code and tail of
   each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `eb8aa9ae` in the primary checkout.
G13 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only eb8aa9ae..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the ten paths the Change section names as untouched is
   PRESENT at the base and absent from the range; that every commit in the range
   has one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table (checklist item 28). C5's own cell and the
   complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601):
   the count of this round's reflog entries that PRODUCED a commit and read
   `commit`, which must equal the number of commits the round makes; and the
   count whose OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — contains `amend`, `reset`, `rebase` or `cherry`,
   which must be 0. Read the prefix, never the whole line.
G14 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
   `packages/orchestration/role_conventions.py`,
   `docs/agents/teacher_conventions.md` and
   `tests/orchestration/test_role_conventions.py` at C3, `docs/README.md` at C4
   and `.agent/handoff.md` at C5. Every count must be 0.
G15 THE PUSH. After C5, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 13).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C5 bundle, the `## Commits` table
             G13 pins, and one LINE per gate rather than its transcript
             (R-0582). The LINE cap your commit count earns is the bound; the
             template's token cap was removed at R5. Its `## Next` section names
             the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R8, the `teacher.model`
             config key modelled on `orchestrator.model` with its pin in the
             same commit, and states that R7 awaits review. There is no open
             pull request. The full transcripts go in the round report you
             return, never in the file. The handback also carries this
             Fortschritt line verbatim, because with no relay you never see the
             operator brief that would otherwise state it (R-0418):
             Fortschritt: ~28 % (F086 merged · F255 claimed · six DECISIONs
             ruled · the spec written · T001's vocabulary half BUILT at R6 ·
             T001's conventions half BUILT here: the teacher has a role name, a
             reviewed conventions document and a capped prompt segment) —
             Schätzung
──────────────────────────────────────────────────────────────
