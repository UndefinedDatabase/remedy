# Handback — F032 R11 (T002f: the flight plan, both arms, and the ruling they need)

## Session

SESSION 3 of feature F032 · round R11 · rounds so far 11

Session 1 was R1 through R5, session 2 was R6 through R9, and session 3 began at
R10 and continues here at R11. Eleven rounds across three sessions is inside the
soft limit of 25 rounds or 7 sessions, so no limit report is owed.

## State

- Feature: F032, approval with the evidence triple. Round R11, task slice T002f.
- Branch: `feature/f032-evidence-triple`, round base `91b00286` (the commit that
  handed back R10), as constraint 12 names.
- Commits this round: `cd88a6c6`, `7b4c3c65`, `1bed03cc`, `44c9668c`, `09f0ebaf`,
  `8b115a64`, `0d027074`, plus this handback commit.
- Open findings after C2: 250 (274 registered ids minus 24 resolved). Maximum id
  `R-0713`. C2 registers no id and resolves none — it books the R10 gate verdict
  and one prose-slip line.
- SEVEN of the eight producing types are now enforced: `token_budget`,
  `test_failure`, `patch_approval`, `stop_reason`, `repo_dirty`, `memory_review`
  and `flight_plan_approval`. Only `task_decision` remains.
- DECISION F032 D7 is on disk at C3; it is the authority for the resolved arm's
  triple and for the gate keeping its type-only selection.
- No pull request was created and nothing was merged.

## Range

Review of `91b00286`..HEAD.

## Commits

Every `+/-` below is read from `git diff --numstat <sha>~1 <sha>`. The same
reading produces the insertion counts reported under G8; both were derived from
one `git diff --numstat` pass, compared cell by cell, and they agree.

### cd88a6c6 docs(agent): save the F032 R11 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f032-r11.md | +415 / -0 | C0a — byte-preserving copy of `.remedy-wt/f032-r11.md` |

### 7b4c3c65 docs(agent): mirror the R11 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +301 / -218 | C0b — same bytes as C0a; git resolves both to blob `9f8f4292` |

### 1bed03cc docs(agent): set the plan to the R11 round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +23 / -23 | C1 — the PLANF032R11 slice, applied byte for byte |

### 44c9668c docs(agent): book the R10 verdict and record one prose slip
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | C2 — the LEDGER11 slice appended; the only commit touching the ledger |
| .agent/prose_slips.md | +6 / -0 | C2 — the SLIP11 slice appended; the only commit touching the slip file |

### 09f0ebaf docs(agent): record DECISION F032 D7 on the resolved arm triple
| Path | +/- | Reason |
|------|-----|--------|
| .agent/decisions.md | +54 / -0 | C3 — the DECISION11 slice appended; the only commit touching the decision record |

### 8b115a64 feat(orchestration): both flight-plan arms carry their evidence triple
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +114 / -0 | C4 — S2 to S5: the pending arm's refs and keyed outcomes, the resolved arm's refs and one unkeyed outcome |
| packages/orchestration/decision_evidence.py | +1 / -1 | C4 — S6: `flight_plan_approval` joins `TRIPLE_REQUIRED_TYPES` in the same commit |

### 0d027074 test(orchestration): pin both flight-plan arms and stabilise the guards
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_decision_evidence.py | +354 / -7 | C5 — S7 and S8: the new T002f tests, both guards repointed to `revert_missing`, the exact-membership assertion updated to seven |

### C6 — this handback
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | not tabled | A handoff cannot table the commit that writes it (R-0149 pattern); C6's own numstat is not a value this round writes anywhere |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror into `last_block` | done | |
| C1 the plan | done | |
| C2 the R10 verdict and one prose-slip line | done | |
| C3 DECISION F032 D7 | done | |
| C4 both arms and the gate entry | done | one commit, per constraint 7 |
| C5 the tests and the repointed guards | done | |
| C6 the handback | done | this commit |
| S1 read first, and the readings that make the guards load-bearing | done | confirmed on disk at `91b00286`; see Deviations |
| S2 the pending arm's refs | done | one unguarded `fp:approval` ref, one guarded ref per open question with a non-empty `id`; no mission-offer ref |
| S3 the pending arm's keyed outcomes | done | exactly `approve` and `reject`; wording is the worker's, no half is a `BOILERPLATE_PHRASES` member |
| S4 the resolved arm's refs | done | unguarded `fp:approval`, guarded `reason` reusing the branch's own variable, guarded `mode` |
| S5 the resolved arm's unkeyed outcome | done | no `payload`; one outcome keyed `UNKEYED_OPTION`, stating the consequence of the answer already recorded |
| S6 `flight_plan_approval` joins `TRIPLE_REQUIRED_TYPES` in C4 | done | same commit as both arms' triples |
| S7 end the guard churn permanently | done | both guards repointed to `revert_missing`, docstrings state why via DECISION F031 D3; exact-membership assertion updated |
| S8 the new tests | done | 11 new test functions, taking the file from 74 to 85 and its collected cases from 86 to 108; all drive the real branches through `list_decisions` |

## External actions

- `git worktree add --detach .remedy-wt/f032-r11-mut 0d027074` — created, used for
  the four G7 mutations, then `git worktree remove --force` + `git worktree prune`.
  `git worktree list` is back to 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
  Nothing merged, nothing created, as the block orders.
- `git push -u origin feature/f032-evidence-triple` after this commit.
- Gate scratch scripts were written under the gitignored `.remedy-wt/`;
  `git ls-files .remedy-wt` is 0 lines.

## Verification

- G1 HYGIENE, BASE AND THE SENTINEL — `git rev-parse HEAD` before C0a printed
  `91b002868e0269b9f302a06567a729a920b8f1ce`, the round base of constraint 12;
  `git rev-parse --abbrev-ref HEAD` printed `feature/f032-evidence-triple`;
  `git status --porcelain | wc -l` printed 0 after each of C0a, C0b, C1, C2, C3,
  C4 and C5 — seven readings, each 0. `ls -la .agent/STOP` printed
  `ls: cannot access '.agent/STOP': No such file or directory` at BOTH readings
  constraint 9 orders, once before C0a and once before C6, so the sentinel does
  not exist.
- G2 TRANSPORT — sha256
  `fefaa48f3641824d64c93247a7517f36042f7ee6bae6fa801ccf4bc15d2f7761` over 32994
  bytes and 415 lines is EQUAL for all three artefacts: the reviewer's scratch
  original `.remedy-wt/f032-r11.md`, the committed `.agent/authored/f032-r11.md`
  blob at `cd88a6c6` and the committed `.agent/last_block.md` blob at `7b4c3c65`.
  A byte-for-byte comparison of the three payloads is also True. `git rev-parse`
  on both committed paths returns the SAME blob,
  `9f8f4292d0fdab734660b54eebdba655d24b4e5a`. This proves the reviewer's scratch
  original, the saved copy and the mirror agree; it says NOTHING about the bytes
  of any prompt.
- G3 EXTRACTION AND CAPS — from the committed C0a blob: region `PLANF032R11`
  with 48 content lines, region `LEDGER11` with 1 content line, region `SLIP11`
  with 5 content lines, region `DECISION11` with 53 content lines. 4 regions.
  CONTENT total 107. TOTAL 415 lines. PROSE = 415 − 107 = 308. PROSE under 400 =
  True. TOTAL under 490 = True.
- G4 THE PLAN AND THE SLIP — `.agent/plan.md` at `1bed03cc` is byte-equal to
  slice PLANF032R11 under constraint 2 (True). NEGATIVE CONTROL with the trailing
  newline removed: False, as required. `wc -l` = 48, under 50 = True.
  `^## Goal$` = 1, `^## Next Steps$` = 1. `.agent/prose_slips.md` at `44c9668c`
  equals its pre-commit blob plus ONE newline plus slice SLIP11 byte for byte:
  1971 + 1 + 356 = 2328, actual 2328, byte-equal True.
- G5 THE TWO RECORD APPENDS — both read with `git show <sha>:<path>`, never by
  writing over the tracked file.
  - `.agent/live_review.md` at C2 (`44c9668c`): READER 1, byte identity —
    1076472 + 1 + 5050 = 1081523, actual 1081523, MATCH True; byte-equal to
    pre-commit blob + `\n` + slice True; the pre-commit blob is a byte PREFIX
    True. The `91b00286` blob measures 1076472 bytes over 427 blank-line units,
    matching the reviewer's stated measurement exactly. READER 2, structural —
    the LEDGER11 slice is 1 blank-line paragraph as my script counts it, and the
    LAST 1 unit of the file matches that paragraph IN ORDER, True. NEGATIVE
    CONTROL, one byte flipped in memory inside the FIRST appended paragraph:
    reader 1 rejects True, reader 2 rejects True.
  - `.agent/decisions.md` at C3 (`09f0ebaf`): READER 1 — 642072 + 1 + 3617 =
    645690, actual 645690, MATCH True; byte-equal True; pre-commit blob is a byte
    PREFIX True. READER 2 — the DECISION11 slice is 6 paragraphs, and the LAST 6
    units match those 6 paragraphs IN ORDER, True. NEGATIVE CONTROL as above:
    both readers reject, True and True.
  - Counts before → after C2: `^Gate: F\d+ R\d+ — ` 62 → 63; `^- R-\d+ — ` 274 →
    274; `^Done: R-\d+ — ` 24 → 24; `^Landed: R-` 1 → 1; `^Gate: R\d+ — ` 19 →
    19. Open set (registered minus resolved) 250 → 250. Maximum id `R-0713`
    before and after. Gate keys ADDED: `F032 R10`, exactly one, none removed. Ids
    ADDED to the resolved set: none. All five base numbers, the base open set of
    250 and the base maximum `R-0713` match what the block states.
  - `^## DECISION F032 D\d+ ` in `.agent/decisions.md`: 6 before C3, 7 after.
- G6 THE CODE, LINTED AND READ BACK —
  `python3 -m ruff check packages/orchestration/decision_queue.py packages/orchestration/decision_evidence.py`
  exit code 0, verbatim output `All checks passed!`. Calling `list_decisions` at
  C4:
  - THE MINIMAL PENDING JOB of S1, `Job(name="t", flight_plan={"_approval": "pending"})` —
    refs `[('decision', 'fp:approval', 'the flight-plan approval this job is waiting on')]`;
    outcomes `[('approve', "The run starts and the plan's tasks execute in the order it records, so the work that follows is the work that was reviewed.", 'Work begins against whatever the plan assumed, and an assumption nobody checked is paid for in rework.'), ('reject', 'Nothing executes and the plan goes back for revision, so a wrong scope costs a replan rather than a run.', 'The job makes no progress until a new plan is approved, and the context this planning built is spent again.')]`;
    own options `['approve', 'reject']`; `evidence_triple_problems` with THOSE
    options `[]`; `evidence_status` `present`, `status` `open`.
  - A PENDING JOB WITH TWO OPEN CLARIFICATIONS (`q1`, `q2`) — refs
    `[('decision', 'fp:approval', 'the flight-plan approval this job is waiting on'), ('decision', 'q1', 'the open question that ships with this plan'), ('decision', 'q2', 'the open question that ships with this plan')]`;
    the same two outcomes; own options `['approve', 'reject']`;
    `evidence_triple_problems` with those options `[]`; `evidence_status`
    `present`, `status` `open`.
  - THE RESOLVED ARM, audit `{"reason": "approved"}` — refs
    `[('decision', 'fp:approval', 'the flight-plan approval this record answers'), ('decision', 'approved', 'the reason recorded when the plan was approved')]`;
    outcomes `[('', 'The run executes the plan this approval named, so the tasks it carries out are the agreed scope.', 'A plan approved on an assumption that has since changed keeps the run pointed at the old scope until someone revisits it.')]`;
    own options `[]`; `evidence_triple_problems` with those options `[]`;
    `evidence_status` `present`, `status` `resolved`.
  - THE RESOLVED ARM, audit `{"reason": "approved", "mode": "auto"}` — refs
    `[('decision', 'fp:approval', 'the flight-plan approval this record answers'), ('decision', 'approved', 'the reason recorded when the plan was approved'), ('decision', 'auto', 'how the approval was given')]`;
    the same one outcome; own options `[]`; `evidence_triple_problems` `[]`;
    `evidence_status` `present`, `status` `resolved`.

  `sorted(TRIPLE_REQUIRED_TYPES)` =
  `['flight_plan_approval', 'memory_review', 'patch_approval', 'repo_dirty', 'stop_reason', 'test_failure', 'token_budget']`.
- G7 TESTS GREEN, THEN RED UNDER MUTATION, AND THE WIDER SUITES UNMOVED —
  `python3 -B -m pytest tests/orchestration/test_decision_evidence.py -q` in the
  PRIMARY checkout at C5: exit code 0, `108 passed in 0.38s`, 0 `^FAILED` lines.
  In the disposable worktree `.remedy-wt/f032-r11-mut` at `0d027074`, with
  `__pycache__` purged and `-B` passed before every run, and each exact byte
  string counted 1 in its file before it was applied and the file restored byte
  for byte afterwards:
  - CONTROL before any mutation — exit 0, `108 passed in 0.40s`, 0 `^FAILED`.
  - mutation (a), the non-empty-`id` guard of S2 removed so every clarification
    emits a ref (`                if _question_id:` → `                if True:`
    in `decision_queue.py`, count 1) — exit 1, `4 failed, 104 passed in 0.50s`,
    4 `^FAILED`.
  - mutation (b), the `mode` ref of S4 emitted unconditionally
    (`            if _fp_mode:` → `            if True:` in
    `decision_queue.py`, count 1) — exit 1, `4 failed, 104 passed in 0.54s`, 4
    `^FAILED`.
  - mutation (c), `flight_plan_approval` removed from `TRIPLE_REQUIRED_TYPES`
    (`"repo_dirty", "memory_review", "flight_plan_approval",` →
    `"repo_dirty", "memory_review",` in `decision_evidence.py`, count 1) — exit
    1, `3 failed, 105 passed in 0.43s`, 3 `^FAILED`.
  - mutation (d), the `reject` outcome of S3 deleted so the pending arm keys only
    `approve` (its whole `DecisionOptionOutcome(...)` block in
    `decision_queue.py`, count 1, replaced with nothing) — exit 1,
    `12 failed, 96 passed in 0.70s`, 12 `^FAILED`.
  - CONTROL after all four restorations — exit 0, `108 passed in 0.39s`, 0
    `^FAILED`, and the worktree's `git status --porcelain` was the empty string,
    0 lines.

  Then, as ONE pytest process in the primary checkout:
  `python3 -B -m pytest tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_mission_state.py tests/orchestration/test_bundled_clarification.py -q`
  — exit code 0, `263 passed in 0.75s`, 0 `^FAILED` lines.
- G8 STRUCTURE, CANARY AND THE PR GATE —
  `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit code 0,
  `42 passed in 20.66s`, 0 `^FAILED` lines.
  `git diff --name-only 91b00286..0d027074` yields exactly
  `.agent/authored/f032-r11.md`, `.agent/decisions.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/decision_evidence.py`,
  `packages/orchestration/decision_queue.py`,
  `tests/orchestration/test_decision_evidence.py` — the nine Change-set paths
  other than `.agent/handoff.md`. BOTH residues are EMPTY: changed-but-not-listed
  `[]`, listed-but-unchanged `[]`.
  `git diff --stat 91b00286..0d027074 -- apps/` and the same for `-- docs/` are
  both the empty string. Per-commit insertions, each single-parent (1 parent) and
  each under 500: `cd88a6c6` 415, `7b4c3c65` 301, `1bed03cc` 23, `44c9668c` 8,
  `09f0ebaf` 54, `8b115a64` 115, `0d027074` 354. Those counts and the `+/-`
  column of the `## Commits` section above are one reading written twice, both
  derived from `git diff --numstat`, compared cell by cell, and they AGREE.
  Marker sweep at C5, counts of `^<<<SLICE ` and `^<<<END `: `.agent/plan.md`
  0/0, `.agent/live_review.md` 0/0, `.agent/prose_slips.md` 0/0,
  `.agent/decisions.md` 0/0, `packages/orchestration/decision_queue.py` 0/0,
  `packages/orchestration/decision_evidence.py` 0/0,
  `tests/orchestration/test_decision_evidence.py` 0/0 — against the CONTROL over
  the committed C0a blob, which is 4/4 and therefore non-zero.
  `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line,
  `git branch --list "tmp/*"` 0 lines.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  printed `[]`; nothing was merged and nothing was created.

## Authored-text proofs

Four reviewer-authored slices were applied, plus the block itself.

- The BLOCK — `.remedy-wt/f032-r11.md`, the committed `.agent/authored/f032-r11.md`
  blob and the committed `.agent/last_block.md` blob all carry sha256
  `fefaa48f3641824d64c93247a7517f36042f7ee6bae6fa801ccf4bc15d2f7761` over 32994
  bytes and 415 lines, and the two committed paths are the same git blob
  `9f8f4292d0fdab734660b54eebdba655d24b4e5a`. Disk-to-disk comparison: EQUAL.
- Slice PLANF032R11 — `.agent/plan.md` at `1bed03cc` is byte-equal to the slice
  extracted from the committed C0a blob under convention 2. The negative control
  (trailing newline removed) is False, so the comparison is not vacuous.
- Slice LEDGER11 — `.agent/live_review.md` at `44c9668c` is byte-equal to the
  `1bed03cc` blob plus one newline plus the slice, proven by two independent
  readers, with a one-byte negative control that both readers reject.
- Slice SLIP11 — `.agent/prose_slips.md` at `44c9668c` is byte-equal to its
  pre-commit blob plus one newline plus the slice: 1971 + 1 + 356 = 2328.
- Slice DECISION11 — `.agent/decisions.md` at `09f0ebaf` is byte-equal to the
  `44c9668c` blob plus one newline plus the slice, proven by the same two
  readers, with the same one-byte negative control that both reject.

No slice was edited. Nothing looked wrong enough to report under constraint 1.

## Deviations & assumptions

- COMMIT ORDER WAS EXACTLY C0a, C0b, C1, C2, C3, C4, C5, C6, with no commit
  between them, no extra commit and no reordering. C2 is the only commit touching
  `.agent/live_review.md` and `.agent/prose_slips.md`; C3 is the only commit
  touching `.agent/decisions.md`; C4 carries both arms and the gate entry
  together, as constraint 7 requires.
- ONE IMPORT NOT IN THE SPEC. `tests/orchestration/test_decision_evidence.py`
  now imports `replace` from `dataclasses`. S8 orders a test proving a resolved
  `flight_plan_approval` card with its triple dropped still raises, and
  `HumanDecision` is a frozen dataclass whose local `_decision` helper hardcodes
  `status="open"`; `replace` builds the resolved variant without duplicating the
  twelve-field constructor. `python3 -m ruff check` is exit 0.
- THE SUITE WAS NOT RUN AT C4, and no claim is made about its colour there. C4
  enforces `flight_plan_approval` while the two S7 guards still name it, and S7's
  repointing lands at C5 — constraint 7 requires that order. Every colour
  reported under G7 was measured at C5 or later.
- MUTATIONS (a) AND (b) WERE APPLIED AS `if <expr>:` → `if True:` rather than by
  deleting the `if` line and de-indenting its body. That is a faithful removal of
  the guard — the ref is emitted on every pass — and it keeps the mutation to a
  single exact byte string whose count in the file is 1, which is what the gate
  asks to be reported.
- GATE SCRATCH LIVES IN `.remedy-wt/`. The G2 through G8 measurement scripts were
  written there because it is gitignored; `git ls-files .remedy-wt` is 0 lines and
  the primary checkout is clean at every commit.
- S1 CONFIRMED ON DISK at `91b00286`. `tests/orchestration/test_mission_state.py`
  builds `Job(name="t", flight_plan={"_approval": "pending"})` with no
  clarifications and no intake; `tests/orchestration/test_decision_inbox.py`
  drives the resolved arm with `_approval_audit` `{"reason": "approved"}` and no
  `mode` key, through `_fixture_flight_plan_approval` and the auto-approved job at
  its line 367; `open_clarification_questions` returns records carrying `id`,
  `question`, `default_answer` and `impact`, each defaulted to the empty string.
  So the `id` guard of S2 and the `mode` guard of S4 are load-bearing rather than
  defensive, which mutations (a) and (b) confirm.
- S7'S SECOND GUARD ALSO GAINED A DOCSTRING.
  `test_a_tripleless_decision_exports_empty_lists_and_the_legacy_status` had none;
  S7 orders the WHY to be stated in the docstring, so one was written naming
  DECISION F031 D3. The first guard's existing docstring was rewritten for the
  same reason.

## Next

1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md`: re-read `.agent/STOP`
   FROM DISK before anything else. It does not exist as of this handback, but the
   check is one-shot per round and binds at any point.
2. The Open PR Gate —
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`. It
   returned `[]` at this handback; re-run it, do not assume.
3. `task_decision`, the last producer. Its options come from the escalation
   record and are arbitrary strings, so its outcomes are built per option rather
   than written out, and its resolved arm is already ruled on by DECISION F032
   D7. With it the gate set is complete and T002 ends.
