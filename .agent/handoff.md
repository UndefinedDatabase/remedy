# Handback — F032 R12 (T002g: the last producer, and the gate goes fully live)

## Session

SESSION 3 of feature F032 · round R12 · rounds so far 12

Session 1 was R1 through R5, session 2 was R6 through R9, and session 3 began at
R10 and continues here at R12. Twelve rounds across three sessions is inside the
soft limit of 25 rounds or 7 sessions, so no limit report is owed.

## State

- Feature: F032, approval with the evidence triple. Round R12, task slice T002g.
- Branch: `feature/f032-evidence-triple`, round base `da6b64fc` (the commit that
  handed back R11), as constraint 12 names.
- Commits this round: `9857f7ee`, `7f1ca6f6`, `868a26a7`, `c9616a88`, `6439bc5b`,
  `a83abda3`, plus this handback commit.
- **T002 IS COMPLETE.** `task_decision` was the eighth and last producing type,
  and it joined `TRIPLE_REQUIRED_TYPES` in C3, the same commit that gave its
  producer a real triple.
- **THE EMIT GATE IS FULLY LIVE OVER ALL EIGHT PRODUCING TYPES**: `token_budget`,
  `test_failure`, `patch_approval`, `stop_reason`, `repo_dirty`, `memory_review`,
  `flight_plan_approval` and `task_decision`. Measured, not asserted: every
  member of `PRODUCING_DECISION_TYPES` in
  `tests/orchestration/test_decision_inbox.py` is in the set, and the residue is
  the empty list. That is the end condition the constant documented for itself.
- The constant is NOT deleted, and C3 states why in its own comment: the two
  types in `DECISION_TYPES` with NO producer at all — `worker_approval` and
  `revert_missing`, per DECISION F031 D3 — are why a set is still needed rather
  than an unconditional check, and two tests depend on `revert_missing` staying
  outside it.
- Open findings after C2: 250 (274 registered ids minus 24 resolved). Maximum id
  `R-0713`. C2 registers no id and resolves none — it books the R11 gate verdict.
- No pull request was created and nothing was merged.

## Range

Review of `da6b64fc`..HEAD.

## Commits

Every `+/-` below is read from `git diff --numstat <sha>^ <sha>`. The insertion
counts reported under G8 come from that same single pass; the two were compared
cell by cell and they AGREE.

### 9857f7ee docs(agent): save the F032 R12 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f032-r12.md | +357 / -0 | C0a — byte-preserving copy of `.remedy-wt/f032-r12.md` |

### 7f1ca6f6 docs(agent): mirror the R12 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +244 / -302 | C0b — same bytes as C0a; git resolves both to blob `be1d3fe9` |

### 868a26a7 docs(agent): set the plan to the R12 round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +25 / -24 | C1 — the PLANF032R12 slice, applied byte for byte |

### c9616a88 docs(agent): book the R11 verdict for both flight-plan arms
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C2 — the LEDGER12 slice appended; the only commit touching the ledger |

### 6439bc5b feat(orchestration): the task-decision card builds an outcome per option
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +133 / -0 | C3 — S2 to S4 and S6: the refs, the built outcomes, the unkeyed fallback |
| packages/orchestration/decision_evidence.py | +12 / -3 | C3 — S5: `task_decision` joins `TRIPLE_REQUIRED_TYPES` and the constant's comment records the end condition |

### a83abda3 test(orchestration): pin the built task-decision outcomes and close the gate set
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_decision_evidence.py | +296 / -1 | C4 — S7: the new T002g tests and the exact-membership assertion updated to eight |

### C5 — this handback
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | not tabled | A handoff cannot table the commit that writes it (R-0149 pattern); C5's own numstat is not a value this round writes anywhere |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror into `last_block` | done | |
| C1 the plan | done | |
| C2 the R11 verdict | done | the only commit touching the ledger |
| C3 the triple, the gate entry and the constant's comment | done | one commit, per constraint 7 and DECISION F032 D5 |
| C4 the tests | done | |
| C5 the handback | done | this commit |
| S1 read first, and the measurements the design rests on | done | confirmed on disk at `da6b64fc`; see Deviations |
| S2 the refs come from the record, and one is unguarded | done | unguarded `decision_id` ref, one guarded ref per non-empty `cross_references` entry, guarded `answer` and `answer_source`; no ref targets the empty string |
| S3 the outcomes are built, not written out | done | one `DecisionOptionOutcome` per option, keyed with the option's own string from the SAME list the payload carries; `UNKEYED_OPTION` when the list is empty |
| S4 what each built outcome says | done | default / non-default / neutral pairs, plus the record's own `impact` appended to every expected outcome; wording is the worker's and no half is a `BOILERPLATE_PHRASES` member. See Deviations for the unkeyed case |
| S5 `task_decision` joins `TRIPLE_REQUIRED_TYPES` in C3 | done | same commit as the triple; the constant's comment now states the end condition is reached and why the constant survives it |
| S6 do not change `payload`, `next_actions`, `safe_summary`, id, status, severity | done | the C3 diff over branch 8 adds only `evidence=` and the values that build it; no existing line of the `HumanDecision(...)` call was touched |
| S7 the new tests | done | 14 new test functions in `tests/orchestration/test_decision_evidence.py` and nowhere else, taking the file from 85 to 99 test functions; `pytest --collect-only -q` now reports `134 tests collected`. The two guards R11 repointed to `revert_missing` were NOT moved |

## External actions

- `git worktree add --detach .remedy-wt/f032-r12-mut a83abda3` — created, used for
  the four G7 mutations, then `git worktree remove .remedy-wt/f032-r12-mut` +
  `git worktree prune`. `git worktree list` is back to 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
  Nothing merged, nothing created, as the block orders.
- `git push -u origin feature/f032-evidence-triple` after this commit.
- Gate scratch scripts were written under the gitignored `.remedy-wt/`;
  `git ls-files .remedy-wt` is 0 lines.

## Verification

- G1 HYGIENE, BASE AND THE SENTINEL — `git rev-parse HEAD` before C0a printed
  `da6b64fc1f4bd46d6ff95f663cd29d0ebc8e2d75`, the round base of constraint 12;
  `git rev-parse --abbrev-ref HEAD` printed `feature/f032-evidence-triple`;
  `git status --porcelain | wc -l` printed 0 after each of C0a, C0b, C1, C2, C3
  and C4 — five readings after the five commits G1 covers, plus the reading taken
  before C0a, every one of them 0. `.agent/STOP` was re-read FROM DISK at both
  readings constraint 9 orders — once before C0a and once before C5 — with
  `python3 -c "import os; print(os.path.exists('.agent/STOP'))"`, and printed
  `False` both times, so the sentinel does not exist.
- G2 TRANSPORT — sha256
  `54d38edecca151a2d01a5c59dc0369dcba942975eeaaef718e4e13e021b9217d` over 29343
  bytes and 357 lines is EQUAL for all three artefacts: the reviewer's scratch
  original `.remedy-wt/f032-r12.md`, the committed `.agent/authored/f032-r12.md`
  blob at `9857f7ee` and the committed `.agent/last_block.md` blob at `7f1ca6f6`.
  A byte-for-byte comparison of the three payloads is also True. `git rev-parse`
  on both committed paths returns the SAME blob,
  `be1d3fe9c07c2882249bcf632fcdf161f4460590`. This proves the reviewer's scratch
  original, the saved copy and the mirror agree; it says NOTHING about the bytes
  of any prompt.
- G3 EXTRACTION AND CAPS — from the committed C0a blob: region `PLANF032R12`
  with 49 content lines, region `LEDGER12` with 1 content line. 2 regions.
  CONTENT total 50. TOTAL 357 lines. PROSE = 357 − 50 = 307. PROSE under 400 =
  True. TOTAL under 490 = True.
- G4 THE PLAN — `.agent/plan.md` at `868a26a7` is byte-equal to slice
  PLANF032R12 under constraint 2 (True). NEGATIVE CONTROL with the trailing
  newline removed: False, as required, so the comparison is not vacuous.
  `wc -l` = 49, under 50 = True. `^## Goal$` = 1, `^## Next Steps$` = 1.
- G5 THE LEDGER APPEND — read with `git show da6b64fc:.agent/live_review.md`,
  never by writing over the tracked file.
  - READER 1, byte identity — 1081523 + 1 + 5227 = 1086751, actual 1086751,
    MATCH True; the C2 blob is byte-equal to the base blob + `\n` + the LEDGER12
    slice, True; the base blob is a byte PREFIX of the C2 blob, True. The
    `da6b64fc` blob measures 1081523 bytes over 428 blank-line units, matching
    the reviewer's stated measurement exactly.
  - READER 2, independent structural — the LEDGER12 slice is N = 1 blank-line
    paragraph as my script counts it, and the LAST 1 unit of the whole file
    matches that paragraph IN ORDER, True. The file has 429 blank-line units
    after C2.
  - NEGATIVE CONTROL — one byte flipped in memory at offset 1081524, inside the
    FIRST appended paragraph (`G` → `H`): reader 1 rejects True, reader 2
    rejects True.
  - Counts before → after C2: `^Gate: F\d+ R\d+ — ` 63 → 64; `^- R-\d+ — ` 274 →
    274; `^Done: R-\d+ — ` 24 → 24; `^Landed: R-` 1 → 1; `^Gate: R\d+ — ` 19 →
    19. Open set (registered minus resolved) 250 → 250. Maximum id `R-0713`
    before and after. Gate keys ADDED: `F032 R11`, exactly one, none removed.
    Ids ADDED to the resolved set: none. All five base numbers, the base open set
    of 250 and the base maximum `R-0713` match what the block states.
- G6 THE CODE, LINTED AND READ BACK —
  `python3 -m ruff check packages/orchestration/decision_queue.py packages/orchestration/decision_evidence.py`
  exit code 0, verbatim output `All checks passed!`. Calling `list_decisions`
  at C3, with every record built by `enqueue_task_decision`:
  - AN OPEN RECORD WITH TWO OPTIONS AND `safe_default="retry"` — refs
    `[('decision', 'td:t1', 'the escalation record this decision was raised from')]`;
    outcomes `[('retry', 'Answering retry is the course the task itself proposed as safe, so the waiting branch resumes on the path the run was already prepared for.', 'A default accepted without reading the question is how an assumption nobody checked becomes a finished result.'), ('skip', 'The waiting branch resumes on skip instead of the course the task proposed.', 'The run departs from what the task prepared for, so work already done for that path may be spent again.')]`;
    own `payload["options"]` `['retry', 'skip']`; `evidence_triple_problems` with
    THOSE options `[]`; `evidence_status` `present`, `status` `open`.
  - AN OPEN RECORD WITH TWO OPTIONS AND NO `safe_default` — the same single ref
    (`td:t2`); outcomes
    `[('retry', 'The waiting branch resumes on retry, the course this answer chooses.', 'The tasks blocked behind this question stay blocked until it is answered, and a course chosen without reading the question is paid for downstream.'), ('skip', 'The waiting branch resumes on skip, the course this answer chooses.', 'The tasks blocked behind this question stay blocked until it is answered, and a course chosen without reading the question is paid for downstream.')]`;
    own options `['retry', 'skip']`; `evidence_triple_problems` `[]`;
    `evidence_status` `present`, `status` `open`.
  - AN OPEN RECORD WITH NO OPTIONS AT ALL — the single ref (`td:t3`); outcomes
    `[('', 'An answer in free text resumes the waiting branch, which continues with that answer recorded on its task.', 'A question left unanswered blocks everything behind it, and this branch of the run makes no progress until it is answered.')]`;
    own options `[]`; `evidence_triple_problems` with those options `[]`;
    `evidence_status` `present`, `status` `open`.
  - A RECORD WITH A NON-EMPTY `impact` (`the release branch stays unbuilt`) — the
    single ref (`td:t4`); outcomes
    `[('retry', 'Answering retry is the course the task itself proposed as safe, so the waiting branch resumes on the path the run was already prepared for.  The task states this consequence: the release branch stays unbuilt', 'A default accepted without reading the question is how an assumption nobody checked becomes a finished result.'), ('skip', 'The waiting branch resumes on skip instead of the course the task proposed.  The task states this consequence: the release branch stays unbuilt', 'The run departs from what the task prepared for, so work already done for that path may be spent again.')]`;
    own options `['retry', 'skip']`; `evidence_triple_problems` `[]`;
    `evidence_status` `present`, `status` `open`.
  - A RECORD WHOSE `cross_references` IS NON-EMPTY (the same question raised
    twice) — the FIRST card's refs
    `[('decision', 'td:t5', 'the escalation record this decision was raised from'), ('decision', 'td:t6', 'the same question raised again and cross-referenced by the queue')]`
    and the SECOND card's refs
    `[('decision', 'td:t6', 'the escalation record this decision was raised from'), ('decision', 'td:t5', 'the same question raised again and cross-referenced by the queue')]`;
    both carry the two neutral-pair outcomes above; own options `['retry', 'skip']`
    on each; `evidence_triple_problems` `[]` on each; `evidence_status` `present`,
    `status` `open` on each.
  - A RESOLVED RECORD (answered `skip`, source `human`) — refs
    `[('decision', 'td:t7', 'the escalation record this decision was raised from'), ('decision', 'skip', 'the answer that was recorded'), ('decision', 'human', 'where that answer came from')]`;
    outcomes identical to the first case's; own options `['retry', 'skip']`;
    `evidence_triple_problems` with those options `[]`; `evidence_status`
    `present`, `status` `resolved`.

  `sorted(TRIPLE_REQUIRED_TYPES)` =
  `['flight_plan_approval', 'memory_review', 'patch_approval', 'repo_dirty', 'stop_reason', 'task_decision', 'test_failure', 'token_budget']`.
  `sorted(PRODUCING_DECISION_TYPES)` from
  `tests/orchestration/test_decision_inbox.py` is the SAME eight strings, and the
  residue `set(PRODUCING_DECISION_TYPES) - set(TRIPLE_REQUIRED_TYPES)` is `[]`, so
  EVERY producing type is now enforced.
- G7 TESTS GREEN, THEN RED UNDER MUTATION, AND THE WIDER SUITES UNMOVED —
  `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` in the
  PRIMARY checkout at C4: exit code 0, `134 passed in 0.35s`, 0 `^FAILED` lines.
  In the disposable worktree `.remedy-wt/f032-r12-mut` at `a83abda3`, with
  `__pycache__` purged and `-B` passed before every run, and each exact byte
  string counted 1 in its file before it was applied and the file restored byte
  for byte afterwards (each restoration verified by re-reading the file and
  comparing to the pre-mutation text, True in all four cases):
  - CONTROL before any mutation — exit 0, `134 passed in 0.43s`, 0 `^FAILED`.
  - mutation (a), the built outcome keyed with a constant string instead of with
    the option it was built for (`                    option=_option,` →
    `                    option="a-constant-key",` in
    `packages/orchestration/decision_queue.py`, count 1) — exit 1,
    `20 failed, 114 passed in 1.11s`, 20 `^FAILED`. This is the rule (g)
    violation in BOTH directions: the payload offers `retry` and `skip` that no
    outcome answers, and the outcomes name `a-constant-key`, which the card does
    not offer.
  - mutation (b), the `answer` ref of S2 emitted unconditionally
    (`            if _td_answer:` → `            if True:` in
    `packages/orchestration/decision_queue.py`, count 1) — exit 1,
    `21 failed, 113 passed in 1.15s`, 21 `^FAILED`. On an OPEN record `answer`
    is the empty string, so rule (c) refuses the card.
  - mutation (c), `task_decision` removed from `TRIPLE_REQUIRED_TYPES`
    (`"repo_dirty", "memory_review", "flight_plan_approval", "task_decision",` →
    `"repo_dirty", "memory_review", "flight_plan_approval",` in
    `packages/orchestration/decision_evidence.py`, count 1) — exit 1,
    `2 failed, 132 passed in 0.46s`, 2 `^FAILED`.
  - mutation (d), the safe-default branch of S4 made unreachable so every option
    gets the neutral pair
    (`            _td_default = str(record.get("safe_default", "") or "")` →
    `            _td_default = ""` in
    `packages/orchestration/decision_queue.py`, count 1) — exit 1,
    `2 failed, 132 passed in 0.46s`, 2 `^FAILED`. See Deviations for why the
    mutation was applied at the assignment rather than at the branch.
  - CONTROL after all four restorations — exit 0, `134 passed in 0.42s`, 0
    `^FAILED`, and the worktree's `git status --porcelain` was the empty string,
    0 lines.

  Then, as ONE pytest process in the primary checkout:
  `python3 -m pytest tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_run_report.py tests/orchestration/test_watchdog.py tests/cli/test_open_decisions_view.py -q`
  — exit code 0, `303 passed in 0.85s`, 0 `^FAILED` lines.
- G8 STRUCTURE, CANARY AND THE PR GATE —
  `python3 -m pytest tests/cli/test_golden_path.py -q` exit code 0,
  `42 passed in 20.64s`, 0 `^FAILED` lines.
  `git diff --name-only da6b64fc..a83abda3` yields exactly
  `.agent/authored/f032-r12.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `packages/orchestration/decision_evidence.py`,
  `packages/orchestration/decision_queue.py`,
  `tests/orchestration/test_decision_evidence.py` — the seven Change-set paths
  other than `.agent/handoff.md`. BOTH residues are EMPTY: changed-but-not-listed
  `[]`, listed-but-unchanged `[]`.
  `git diff --stat da6b64fc..a83abda3 -- apps/` and the same for `-- docs/` are
  both the empty string, so no docs-round gate is owed.
  Per-commit insertions, each single-parent (1 parent) and each under 500:
  `9857f7ee` 357, `7f1ca6f6` 244, `868a26a7` 25, `c9616a88` 2, `6439bc5b` 145,
  `a83abda3` 296. Those counts and the `+/-` column of the `## Commits` section
  above are one reading written twice, both derived from `git diff --numstat`,
  compared cell by cell, and they AGREE.
  Marker sweep at C4, counts of `^<<<SLICE ` and `^<<<END `: `.agent/plan.md`
  0/0, `.agent/live_review.md` 0/0,
  `packages/orchestration/decision_queue.py` 0/0,
  `packages/orchestration/decision_evidence.py` 0/0,
  `tests/orchestration/test_decision_evidence.py` 0/0 — against the CONTROL over
  the committed C0a blob, which is 2/2 and therefore non-zero.
  `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line,
  `git branch --list "tmp/*"` 0 lines.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  printed `[]`; nothing was merged and nothing was created.

## Authored-text proofs

Two reviewer-authored slices were applied, plus the block itself.

- The BLOCK — `.remedy-wt/f032-r12.md`, the committed `.agent/authored/f032-r12.md`
  blob and the committed `.agent/last_block.md` blob all carry sha256
  `54d38edecca151a2d01a5c59dc0369dcba942975eeaaef718e4e13e021b9217d` over 29343
  bytes and 357 lines, and the two committed paths are the same git blob
  `be1d3fe9c07c2882249bcf632fcdf161f4460590`. Disk-to-disk comparison: EQUAL.
- Slice PLANF032R12 — `.agent/plan.md` at `868a26a7` is byte-equal to the slice
  extracted from the committed C0a blob under convention 2. The negative control
  (trailing newline removed) is False, so the comparison is not vacuous.
- Slice LEDGER12 — `.agent/live_review.md` at `c9616a88` is byte-equal to the
  `da6b64fc` blob plus one newline plus the slice, proven by two independent
  readers, with a one-byte negative control inside the first appended paragraph
  that both readers reject.

No slice was edited. Nothing looked wrong enough to report under constraint 1.

## Deviations & assumptions

- COMMIT ORDER WAS EXACTLY C0a, C0b, C1, C2, C3, C4, C5, with no commit between
  them, no extra commit and no reordering. C2 is the only commit touching
  `.agent/live_review.md`; C3 carries the triple, the gate entry and the
  constant's comment together, as constraint 7 and DECISION F032 D5 require.
- THE `answer` AND `answer_source` REFS ARE GUARDED ON EMPTINESS ALONE, with no
  `status` test. S2 orders them "for a RESOLVED record only … each ONLY when its
  value is non-empty, because an OPEN record carries both as the empty string".
  `enqueue_task_decision` writes both fields as `""` until the record is
  answered, so the emptiness guard IS the resolved-only restriction and a second
  `status` branch would be dead code. It also keeps the guard load-bearing, which
  is what makes mutation (b) reach the tests instead of being vacuous.
- THE `impact` NOTE IS APPENDED TO THE UNKEYED OUTCOME TOO. S4 orders it appended
  to "EVERY option's expected outcome" and states the UNKEYED sentence
  separately, which leaves the optionless case unaddressed. The note is appended
  uniformly to every outcome the branch emits, because a record can carry an
  `impact` with no options at all and dropping the task's own stated consequence
  there would lose the only thing the record knows about the cost of waiting.
  This is a superset of what S4 orders and satisfies its assertion either way.
- MUTATION (d) WAS APPLIED AT THE ASSIGNMENT, NOT AT THE BRANCH. G7 orders "the
  safe-default branch of S4 removed so every option gets the neutral pair".
  Deleting the `if`/`elif` arms would need a multi-line excision with no single
  exact byte string to count; setting `_td_default = ""` makes both arms
  unreachable and routes EVERY option to the neutral pair, which is precisely the
  ordered effect, at a single byte string whose count in the file is 1 — the
  property G7 asks to be reported.
- TWO IMPORT LINES NOT IN THE SPEC. `tests/orchestration/test_decision_evidence.py`
  now imports `datetime, timezone` from `datetime` and `answer_task_decision,
  enqueue_task_decision` from `packages.orchestration.escalation`. S7 orders the
  records to be built by `enqueue_task_decision`, whose `now` parameter is
  keyword-only and required, and orders a RESOLVED case, which only
  `answer_task_decision` can produce. `python3 -m ruff check` on the file is exit
  0 with `All checks passed!`.
- SIX NEW TEST HELPERS CARRY `task_decision` IN THEIR NAMES. The first draft named
  one of them `_resolved_decision`, which SHADOWED the flight-plan helper of the
  same name that R11 added to this file, and eight R11 tests went red with
  `TypeError: _resolved_decision() takes 0 positional arguments but 1 was given`.
  All six factories were renamed to
  `_keyed_open_task_decision`, `_defaultless_open_task_decision`,
  `_optionless_open_task_decision`, `_impact_task_decision`,
  `_cross_referenced_task_decisions` and `_resolved_task_decision` before C4 was
  committed, per the one-spelling-per-concept rule in AGENTS.md. No R11 test was
  altered; the collision was in the new code only.
- S1 CONFIRMED ON DISK at `da6b64fc`. `escalation.py::enqueue_task_decision` is
  the only writer of these records and always sets `decision_id`, `safe_default`,
  `impact` and `cross_references`, defaulting the last three to `""`, `""` and a
  list, so the unguarded `decision_id` ref of S2 can never target the empty
  string. Branch 8's `payload` always carries an `options` key whose value is the
  branch's own `options` list, and the outcomes are built from that SAME object,
  not from a re-read of the record.
- THE SUITE WAS NOT RUN AT C3, and no claim is made about its colour there. C3
  enforces `task_decision` while the exact-membership assertion still names seven
  types; S7's update lands at C4 and constraint 7 fixes that order. Every colour
  reported under G7 was measured at C4 or later.
- GATE SCRATCH LIVES IN `.remedy-wt/`. The G2 through G8 measurement scripts and
  the mutation harness were written there because it is gitignored;
  `git ls-files .remedy-wt` is 0 lines and the primary checkout is clean at every
  commit.

## Next

1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md`: re-read `.agent/STOP`
   FROM DISK before anything else. It does not exist as of this handback, but the
   check is one-shot per round and binds at any point.
2. The Open PR Gate —
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`. It
   returned `[]` at this handback; re-run it, do not assume.
3. T003: card enrichment and the chip deep links. It is the first F032 work to
   touch `apps/`, and therefore the first round bound by the canonical design
   reference in `docs/ui/design_reference/`.
