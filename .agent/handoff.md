# Handoff — F295 session 4, round 19: round 18 booked, R-1153 registered and repaired, T004's contract page and its test

## Session

SESSION 4 of feature F295 · rounds 16 to 19 · rounds so far 19

Context self-assessment (quoted from the block): "The reviewer's context is still workable after four
rounds; the reviewer decides after this round's review whether the hardening stage starts in this
session or the next."

Fortschritt: ~92 % (T001 to T004 landed, T004's second part review pending; then the SLOW MODE hardening stage and the closure) — Schätzung

## Range

Review of `c4878bd45`..`e34128197`, plus this handback commit.

## Commits

### 0620e6693 F295 R19 C1: book round 18's PASS, register R-1153, DECISION F295 D17, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r19.md` | 119/0 (new) | byte copy of this round's block |
| `.agent/live_review.md` | 4/0 | append round 18's gate entry and R-1153, exactly as prepared |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D17, exactly as prepared |
| `.agent/plan.md` | 10/7 | rewrite to round 19's current step |

### 4b1fab0f1 F295 R19 C2: the machine client contract page, linked from the docs index (DECISION F295 D17)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/machine-client-contract-v1.md` | 148/0 (new) | the contract page, byte copy of the prepared file |
| `docs/README.md` | 2/0 | two index links, byte copy of the prepared file |

### 7f8af0c03 F295 R19 C3: the contract page's tables are held to the gate test's own names (DECISION F295 D17)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_machine_client_contract.py` | 98/0 | tests holding the page's tables to the gate test, byte copy of the prepared file |

### e34128197 F295 R19 C4: the proof chain page names the job applies (R-1153)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/proof-chain.md` | 11/0 | section "Job Applies", byte copy of the prepared file |

### F295 R19 C5: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

No `gh` command was run, no PR opened. After C5:
`git push origin feature/f295-machine-client-contract-v1`; its outcome is in the worker's final reply
(write-once rule). `.agent/STOP` was absent throughout.

## Verification

Gates ran in the block's order, once each, after C4 and before C5; all five read green.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Byte comparison of every file C1
   to C4 wrote (`git show <commit>:<path>`) against its prepared file, eight of eight equal.
   ```
   porcelain: ''
   0620e6693 .agent/authored/f295-r19.md == block.md : True
   0620e6693 .agent/live_review.md == dry-live_review.md : True
   0620e6693 .agent/decisions.md == dry-decisions.md : True
   0620e6693 .agent/plan.md == dry-plan.md : True
   4b1fab0f1 docs/system/machine-client-contract-v1.md == dry-machine-client-contract-v1.md : True
   4b1fab0f1 docs/README.md == dry-README.md : True
   7f8af0c03 tests/cli/test_machine_client_contract.py == dry-test_machine_client_contract.py : True
   e34128197 docs/system/proof-chain.md == dry-proof-chain.md : True
   ALL EQUAL: True
   ```
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check tests/cli/test_machine_client_contract.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r19/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   3595 passed, 3 skipped in 38.34s
   ```
   No FAILED line, no ERROR line, no `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 0
   {"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1153']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r19.md`: 119 lines / 119 lines, sha256
  `943378dcdb2cd5877a3773046129c38acaa97acf05f934efd51707cc073b5564` / same, verified before any
  other read; byte comparison equal from the committed bytes in gate 1.
- Every prepared file's sha256 was read with Python before use and matched the block's value (ten of
  ten, re-checked before each commit). `HEAD` equalled `origin/feature/f295-machine-client-contract-v1`
  at `c4878bd450f1e023760e9a771553fd998db5041f` before any write.
- Append proofs, each `True`: `git show c4878bd45:.agent/live_review.md` plus `append-live_review.txt`
  equals the new ledger; `git show c4878bd45:.agent/decisions.md` plus `append-decisions.txt` equals
  the new decisions file.
- `git diff --cached --numstat` before each commit matched the block's cells exactly: C1 `119 0`,
  `10 0`, `4 0`, `10 7`; C2 `148 0`, `2 0`; C3 `98 0`; C4 `11 0`.

## Deviations & assumptions

None. Every file in C1 to C4 is a byte copy of a reviewer-prepared file; the worker authored no code
and no record text beyond this handback. Gates ran once each in the block's order, none red. No
mutation red-proof, no full suite, no `REMEDY_TEST_MAX_WORKERS`, never two test commands at once. No
commit exceeded 500 insertions. Every commit ends with `Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>`. Helper scripts under `.remedy-wt/f295-r19-worker/` (gitignored) did the
digest checks, copies and proofs. The selection read 3595 passed against round 18's 3538; the
selection helper is the reviewer's and was run unchanged.

## Round verdicts

Rounds 1 to 5, 7 to 13 and 15 to 18 PASS, rounds 6 and 14 FAIL, booked in the ledger (round 18 by
this round's C1); round 19's verdict is the reviewer's to give and book in the next round's first
commit.

## For the operator, in plain sentences

Remedy now has one written page that tells a program exactly how to drive it: how to write an order,
which commands to run in which order, which fields to read in each answer, which command answers each
kind of question, and what Remedy never does on its own. A test fails whenever that page and the test
that plays the program disagree. The page that explains Remedy's record of proof now also describes
the list of applied changes added two rounds ago. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 19 and books its verdict and R-1153's resolution in the
   next round's first commit.
4. The SLOW MODE hardening stage.

Operator questions open: 0.
Open findings: 5 (R-1153 Low, owned by F295, repaired, review pending; R-1138, R-1139, R-1143 and
R-1149, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (book round 18, R-1153, D17, plan) | done | `0620e6693` |
| C2 (contract page, docs index) | done | `4b1fab0f1` |
| C3 (contract page tests) | done | `7f8af0c03` |
| C4 (proof chain "Job Applies") | done | `e34128197` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, eight of eight equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `3595 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1153']` |
| C5 handback commit | done | this file |
| Push after C5 | pending | runs right after this commit, reported in the worker's final reply |

## Reviewer verdict on round 19 and the end of session 4, added after the handback

Written by the reviewer of F295's fourth session after it reviewed round 19, and applied by a
worker as this file's one later commit. Under operator amendment amend0827-process-diet rule 1
this committed and pushed handoff is the durable carrier of the verdict and of the paragraphs
below; the next session does not review round 19 again, it books the texts and goes on.

THE SESSION ENDS HERE, after four delegated rounds, 16 to 19, the floor of the target. Two
reasons. First, the building rounds are finished, and the next step, the SLOW MODE hardening
stage, starts with an acceptance audit that the rules give to a fresh worker who sees only the
feature file; that stage is best begun from a cold start. Second, this reviewer's own slips
accumulated: its round 17 block changed what `remedy change proof` answers and named no
document (R-1153), and once it moved its own shell into a dry worktree and had to move it back.
This sentence replaces the self-assessment above.

VERDICT ON ROUND 19: PASS, verified by dry run, bytes identical. Every file C1 to C4 committed
equals the reviewer's prepared file under `.remedy-wt/f295-r19/`, eight of eight, on the same base
`c4878bd45`.

THE TEXTS TO BOOK. The next round's FIRST commit appends to `.agent/live_review.md`, in this
order, each paragraph preceded by one blank line, exactly the two paragraphs between the marker
lines below (the marker lines themselves are not copied):

BEGIN-R19-BOOKING
Gate: F295 R19 — the F295 round 19 entry, T004's contract page and R-1153's repair, over `c4878bd45`..`881e4c90b` (5 commits, each single-parent; insertions by `git show --numstat`: `0620e6693` 143, `4b1fab0f1` 150, `7f8af0c03` 98, `e34128197` 11, `881e4c90b` 78). VERDICT PASS, verified by dry run, bytes identical: every file C1 to C4 committed equals the reviewer's prepared file under `.remedy-wt/f295-r19/`, eight of eight, on the same base `c4878bd45`, and the reviewer's dry run of the round's selection over those bytes in a disposable worktree read `3594 passed, 4 skipped`, the fourth skip being the UI toolchain a worktree lacks; the worker's one run in the primary checkout read `3595 passed, 3 skipped`. The handback `881e4c90b` was the one file the dry run did not hold, and the three selected files that name it read `43 passed, 1 skipped` at `881e4c90b`. `4b1fab0f1` and `7f8af0c03` land DECISION F295 D17, and with them T004 and the building rounds of F295 close. RED CONTROLS of the page's tests in that worktree, the unmutated control `5 passed` before and after, seven of seven red: the page dropping a flag the gate test uses, the page naming a key the gate test does not read, the gate test reading a key the page does not name, the page's order file differing from the gate test's, the page dropping an exit code, the page naming a command the gate test does not run, and the gate test passing a flag the page does not name. `remedy integrity check --json` read `"fail_count": 0`.

Done: R-1153 — RESOLVED at F295 R19 by `e34128197`, proved by the reviewer's reading of the committed page at `881e4c90b`. `docs/system/proof-chain.md` carries the section "Job Applies": `remedy job apply` lands a result without a patch intent, the proof lists the job's apply records under `job_applies` in its JSON answer with their nine fields and as a `Job applies (<count>):` list in its text answer, `--path` keeps the applies that wrote that path, a job apply is never called verified, and the next action of a proof with no change and a landed apply says so.
END-R19-BOOKING

THE NEXT ROUND, in order: (1) the booking above, with `.agent/plan.md` advanced, as its first
commit. (2) The SLOW MODE hardening stage of operator amendment amend0930b-slow-cap, rule (2):
the reviewer delegates an acceptance audit to a fresh worker subagent given only
`docs/roadmap/features/T12_F295.md` and the repository — no block, no handoff, no verdict — which
names, for every statement under the feature file's Acceptance and Goal & Done headings, the test
that turns red when that statement stops being true, and proves each by one mutation of the
production code in a disposable worktree under `.remedy-wt/`, at least one proof reaching the
feature through the command line; its report lands as `.agent/f295_acceptance_audit.md`, after the
precedent of `.agent/f294_acceptance_audit.md`. Every gap becomes a finding owned by F295,
repaired in reviewed rounds, at most three, and the feature file's Built State gains the
paragraph rule (4) asks for. (3) Then the closure sequence, with the one full suite.

OBSERVATIONS FOR THE HARDENING STAGE, measured by this reviewer and not yet registered: eleven
local branches `remedy/<16 hex>` with prunable worktree entries, made on 2026-10-07 at
`c2b9a817f` and `4ae5d4d33`, came from F295's round 13 and 14 tests, most likely while they ran
inside a reviewer's linked worktree, since this session's selections, run in linked worktrees
without those test files, left none; after an extended job completes, the contract remainder
decision its budget stop raised stays open in the digest, its question still saying that the
mission stopped at its budget; and one broad run of the whole `tests/cli/` directory together with
other directories, in a dry worktree at `741ba4013` plus round 16's draft, failed six tests of
`tests/cli/test_study_cmd.py` that passed when that file ran alone and when `tests/cli/` ran with
`-k study`.

LESSONS THIS SESSION TAUGHT ITS OWN BLOCKS, for the next reviewer: a block that changes what a
command answers names the page under `docs/system/` that documents that command (R-1153);
`remedy do` itself takes `--deadline`, and a deadline already past is the way a fake run on the
`remedy do` path raises a budget decision; the digest lists jobs under `client.jobs`, not inside
the projects; and a job `remedy do` ran shows its hunks only after `remedy job evidence <job>`.

FOR THE OPERATOR, IN PLAIN SENTENCES: this session finished building the way a program can drive
Remedy without a person at the keyboard. A program can now read the individual changes of a
proposed edit and the decisions taken on them, read afterwards which files an approved change
wrote, and follow one written page that lists every command and field it needs; one test plays
that program from a written order to the final record and fails if the page and the behaviour
ever disagree. What remains is a careful check that every promise of this feature is guarded by a
test, then the closing steps. Nothing waits for the operator.

Fortschritt: ~92 % (T001 to T004 landed; then the SLOW MODE hardening stage and the closure) —
Schätzung.

Open findings after the booking: 4 (R-1138, R-1139, R-1143 and R-1149, Low, owned by F297; R-1153
resolved by the booking). Operator questions open: 0.
