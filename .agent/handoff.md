# Handoff — F261 round 25

## Session

SESSION 6 of feature F261 · round 25 · rounds so far 25

Context self-assessment: the round was one record commit and two measured tables of 15 and 11 rows,
every gate passed on its first run, and the worker's context stayed comfortable, with the full suite
the only long wait.

## Scope report — F261 at its soft limit

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F261 reached the standing soft limit of 25 delegated rounds with round 25, in the feature's
sixth session. Operator amendments amend0905-throughput and amend0906-split-placement make
split-and-close the default the session executes, and this round executed it under DECISION
F261 D25, which the operator may reverse through operator question Q3.

FINISHED. T001: `do job-evidence`, `do job-promote` and `do job-run` became `job evidence`,
`job apply` and `job run`, and `do job-flow`, `do job-plan` and `do plan` were deleted
(DECISIONs F261 D1 to D3). T002: `do promote` and the run-level apply library were deleted,
`job_promote.py` became `job_apply.py` with its words, `job show` gained `--json`, `--full`
and the findings of blocked tasks, and the eight read views became its sections (D4 to
D11). T003, reached part: the hidden `roadmap` group (D12); fifteen groups deleted, from
`orchestrator` to `repair` (D13 to D17, D21); `do report` became the `run` group and five
further `do` words left (D18 to D20); the queue words of `job`, `worker run`, `mission
ledger` and `job rerun` were deleted (D22, D23); `teach` became `teacher` (D23); and the
`settings` alias now reaches `config` (D24).

MISSING, and now F280's: the `propose` group and `job fulfill`, each deferred because
deleting it breaks a surviving command (D21 to D23); `job budget <id> set`; `job create`,
`job attach-repo` and `job permit` with their fixtures; the `--builder` and `--reviewer`
flags with the `job run` provider wiring and the ping-pong path of `do run`; the
`flight_plan` rename; and all of T004 — descriptions, role labels, help wrapping, the
catalog ownership test, the dead-command doctor check, the enforced F259 test, the visible
group order and the README quickstart. Findings R-0767, R-0805, R-0809, R-0894, R-0895,
R-0906 and R-0909 move with them.

PROPOSAL EXECUTED. F280 is registered directly after F261 with that scope, and F261 closes
at the scope it reached through the normal closure sequence, which is the next session's
work.

## Range

Review of `d5e0a7b5`..`HEAD`.

## Commits

### 9c5f654e F261 R25 C0a: save the round 25 step block under the authored directory
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r25.md` | +302 / -0 | the block file the delegating message names, copied with `shutil.copyfile`, sha256 `cc0b0ba7…a357cf3` verified after the copy |

Insertions read by `git show --numstat --format= 9c5f654e`: 302, deletions 0.

### 1c838a73 F261 R25 C0b: mirror the round 25 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +176 / -139 | the same bytes, byte-identical to the C0a copy |

Insertions: 176, deletions 139.

### 73fd6e08 F261 R25 C1: book round 24's PASS, record DECISIONs F261 D24 and D25 and open operator question Q3
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15 / -19 | full replacement by slice PLAN25 |
| `.agent/live_review.md` | +2 / -0 | slice RECORD25 appended — the `Gate: F261 R24` PASS paragraph |
| `.agent/decisions.md` | +22 / -0 | slices DEC24 and then DEC25 appended — DECISIONs F261 D24 and D25 |
| `.agent/operator_questions.md` | +9 / -1 | pair QOP applied: the EMPTY line replaced by operator question Q3 |

Insertions: 48, deletions 20. This is the FIRST SUBSTANTIVE COMMIT of the round.

### 76ee0149 F261 R25 C2: land the settings alias over config through an aliases field of GroupDef and one group resolver, by the alias table
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r25-alias.jsonl` | +15 / -0 | the edit table's own carrier, copied with `shutil.copyfile`, sha256 `58f810e31bffb2fb8c2fbce5251b776a2df29fb641cd1a400984719052f3423f` verified |
| `apps/cli/command_catalog.py` | +20 / -4 | `GroupDef.aliases`, `config` carries `aliases=("settings",)`, `resolve_group`, `get_group` and `get_commands_for_group` resolve through it |
| `apps/cli/grouped.py` | +18 / -9 | argparse registers the aliases; group help, the help pre-scan, the unknown-group error and default-subcommand injection resolve through `resolve_group` |
| `apps/cli/help_renderer.py` | +6 / -1 | `render_group_help` takes `also` and prints `Also reachable as:` |
| `tests/cli/test_cli_ux.py` | +77 / -1 | `TestSettingsAlias`, eleven tests |

Insertions: 136, deletions 15 — under the 500-insertion cap of constraint 5.

### 7994c69e F261 R25 C3: register F280 directly after F261 with its feature file, STATUS line, counters and Depends-on lines, by the split table
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r25-split.jsonl` | +11 / -0 | the edit table's own carrier, copied with `shutil.copyfile`, sha256 `0bb2f13086a36429f4d9e3ab62f4d4f8e688f339da1f3fdb6abd2ba2a9e81243` verified |
| `README.md` | +2 / -2 | `77 of 280` and Tier 2 total 33 |
| `docs/roadmap/STATUS.md` | +1 / -0 | the `[ ] F280` line directly after F261's, inside the same Tier 2 heading |
| `docs/roadmap/features/T2_F261.md` | +54 / -0 | the Built State section: what is complete, what moved to F280 and why the close is self-consistent |
| `docs/roadmap/features/T2_F268.md` | +1 / -1 | F280 added to Depends on |
| `docs/roadmap/features/T2_F270.md` | +1 / -1 | F280 added to Depends on |
| `docs/roadmap/features/T2_F271.md` | +1 / -1 | F280 added to Depends on |
| `docs/roadmap/features/T2_F277.md` | +1 / -1 | F280 added to Depends on |
| `docs/roadmap/features/T2_F279.md` | +1 / -1 | F280 added to Depends on |
| `docs/roadmap/features/T2_F280.md` | +147 / -0 | the new feature file, created by the table |
| `tests/docs/test_docs_consistency.py` | +6 / -2 | `TOTAL_FEATURES = 280` with its comment |

Insertions: 226, deletions 9 — under the 500-insertion cap.

### Item status — the block's ordered bundle

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | all 15 table rows applied, every count exactly as stated |
| C3 | done | all 11 table rows applied, every count exactly as stated, the one `create` target absent before |
| C4 | done | this commit, then the push |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r25w/wt 7994c69e` | created, detached at C3 — for G5 only |
| `git worktree remove --force .remedy-wt/f261r25w/wt` | removed; `git worktree list` back to one row |
| `git push origin feature/f261-cli-vocabulary-v2` | run after this commit; its outcome is in the completion message |

No pull request created, edited or merged. No `gh` command run. No `remedy` CLI invocation. No
runner and no `run_job` call: `git branch --list 'remedy/job-*'` reads 16 lines, unchanged.

## Verification

STOP reads, before C0a, C2 and C4: `ls .agent/STOP` → exit 2, `No such file or directory` each
time.

### G1 TRANSPORT — exit 0

    PASS authored block sha256 at C0a == delegating digest
         cc0b0ba700b7fb977ab1e3287c330ca3668e5316ba506c493e9c836cba357cf3
    PASS last_block.md at C0b byte-identical to it
    PASS slice PLAN25     FOUND  d874f5c0…
    PASS slice RECORD25   FOUND  20902ad0…
    PASS slice DEC24      FOUND  06cbaa23…
    PASS slice DEC25      FOUND  95dec9ab…
    PASS slice QOP-FROM   FOUND  522daeae…
    PASS slice QOP-TO     FOUND  7a5ca72e…
    PASS slice SCOPE25    FOUND  22fd48d0…
    PASS committed carrier .agent/authored/f261-r25-alias.jsonl
         58f810e31bffb2fb8c2fbce5251b776a2df29fb641cd1a400984719052f3423f
    PASS committed carrier .agent/authored/f261-r25-split.jsonl
         0bb2f13086a36429f4d9e3ab62f4d4f8e688f339da1f3fdb6abd2ba2a9e81243

### G2 THE RECORD at C1 — exit 0

    PASS plan.md byte-identical to PLAN25, 33 lines, ^## Goal$ once, ^## Next Steps$ once
    PASS live_review.md == d5e0a7b5 blob + RECORD25
    PASS decisions.md   == d5e0a7b5 blob + DEC24 + DEC25
    PASS operator_questions.md == d5e0a7b5 blob with QOP applied; FROM base=1 C1=0; TO C1=1
    PASS ^Gate: F\d+ R\d+ —          base=133  C1=134
    PASS Gate: F261 R24 —            base=0    C1=1
    PASS distinct ^- R-\d+ — ids     base=134  C1=134
    PASS distinct ^Done: R-\d+ — ids base=9    C1=9
    PASS open set by distinct id     base=125  C1=125

    python3 -m pytest tests/docs/ -q   → exit 0, "310 passed in 1.05s"

### G3 THE TABLES — exit 0

HALF C2: `git diff --no-renames --name-only 76ee0149^ 76ee0149` prints exactly 5 paths: the carrier
plus the 4 the block names. `git rev-parse 76ee0149:<object>`, all ten equal to the reviewer's dry
run:

    apps            4b3561d9c973b739fdd9c19bf18c4ed2c1fea95e   PASS
    packages        ec2c3efd7541c8cc7d30b2b226b109e1b285da45   PASS
    scripts         3e3c450e0dffcdd11abbc52b0a7b085359df38e4   PASS
    tests           69cc72df6f8a81d55c5d8d94de401c7b0c88153f   PASS
    docs/guides     52e345b71419d519c98eba49cea68cc424c249ce   PASS
    docs/system     cc42698197076bc70d79a91b05ca633d7ebd2df8   PASS
    docs/roadmap    76bf53fdf467ecbf6bd80b35905b6609f7ede105   PASS
    docs/README.md  c282d425ef909cf9257605294f23aba7d9457fac   PASS
    README.md       9cef3616d99c9689b6b100ea7792e9d8c2b7e57d   PASS
    .claude         e3cd5e0ac262f3f993506e95825e270e39c03ec0   PASS

    python3 -B -m pytest -q tests/cli/test_golden_path.py tests/cli/test_cli_ux.py  (primary checkout, at C2)
      → exit 0, "114 passed in 21.01s"

HALF C3: `git diff --no-renames --name-only 7994c69e^ 7994c69e` prints exactly 11 paths: the carrier
plus the 10 the block names. `git rev-parse 7994c69e:<object>`, all ten equal:

    apps            4b3561d9c973b739fdd9c19bf18c4ed2c1fea95e   PASS
    packages        ec2c3efd7541c8cc7d30b2b226b109e1b285da45   PASS
    scripts         3e3c450e0dffcdd11abbc52b0a7b085359df38e4   PASS
    tests           29f5fccda172e532390a092be69d42357bfedf09   PASS
    docs/guides     52e345b71419d519c98eba49cea68cc424c249ce   PASS
    docs/system     cc42698197076bc70d79a91b05ca633d7ebd2df8   PASS
    docs/roadmap    dd955d0ca9a2ede0eb9c6282b527bb738a0770b7   PASS
    docs/README.md  c282d425ef909cf9257605294f23aba7d9457fac   PASS
    README.md       60ded8dcaca796e8d61856b67d51f75a59f9440e   PASS
    .claude         e3cd5e0ac262f3f993506e95825e270e39c03ec0   PASS

Insertions per constraint 5: C2 136, C3 226.

### G4 THE BEHAVIOUR at C3 — exit 0

From the primary checkout's root:

    python3 -B -m apps.cli.grouped settings --help  → exit 0
      " Also reachable as: remedy config"
    python3 -B -m apps.cli.grouped config --help    → exit 0
      " Also reachable as: remedy settings"
    python3 -B -m apps.cli.grouped roadmap status   → exit 0
      "Next unchecked: F280 — CLI vocabulary v2, part two — the gated prunes, the flight-plan rename and the help surface"
    python3 -B -m pytest -q tests/docs/             → exit 0, "310 passed in 1.22s"
    python3 -m ruff check  (5 paths: apps/cli/command_catalog.py, apps/cli/grouped.py,
      apps/cli/help_renderer.py, tests/cli/test_cli_ux.py, tests/docs/test_docs_consistency.py)
                                                    → exit 0, "All checks passed!"
    git status --porcelain                          → ''

### G5 THE RED-PROOF — exit 0 (every row as ordered)

In `git worktree add --detach .remedy-wt/f261r25w/wt 7994c69e`, each run through a runner that
changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, disables bytecode
writing, and asserts `apps.cli.grouped` loaded from
`.remedy-wt/f261r25w/wt/apps/cli/grouped.py`, with
`-q -p no:randomly -p no:cacheprovider -rf --tb=no` over `tests/cli/test_cli_ux.py`,
`tests/test_command_catalog.py`, `tests/test_help_renderer.py`,
`tests/cli/test_advertised_commands.py` and `tests/docs/`. Mutation carrier sha256
`8275e65a0ef5cdc752122c144d44b41e596ff6ab6cc418c4cf17170c70a8b491`, verified; READ in place, never
committed and never copied into `.agent/`.

| Run | FROM count | exit | summary | failed nodes | row's node among them |
|---|---|---|---|---|---|
| CONTROL | — | 0 | `446 passed in 2.64s` | 0 | — |
| A1-alias-unregistered | 1 | 1 | `9 failed, 437 passed in 2.65s` | 9 | yes |
| A2-parser-drops-aliases | 1 | 1 | `4 failed, 442 passed in 2.53s` | 4 | yes |
| A3-help-prescan-ignores-resolver | 1 | 1 | `1 failed, 445 passed in 2.64s` | 1 | yes |
| A4-help-omits-other-word | 1 | 1 | `3 failed, 443 passed in 2.74s` | 3 | yes |
| A5-resolver-ignores-aliases | 1 | 1 | `5 failed, 441 passed in 2.66s` | 5 | yes |
| S1-status-line-dropped | 1 | 1 | `2 failed, 444 passed in 2.66s` | 2 | yes |
| S2-total-pin-reverted | 1 | 1 | `3 failed, 443 passed in 2.68s` | 3 | yes |

The further nodes pin the same property: for A1 to A5 they are other `TestSettingsAlias` tests;
for S1 `test_there_are_250_unique_status_entries`; for S2 that test and
`test_the_readme_accepted_count_equals_the_status_count`. Each file was restored with
`git -C .remedy-wt/f261r25w/wt checkout -- <path>` after its run (exit 0) and the worktree read
`git status --porcelain` empty each time. After `git worktree remove --force` (exit 0):
`git worktree list` one row, `git branch --list 'remedy/job-*'` 16 lines.

### G6 THE SUITE, SPEC S at C3 — exit 0

    python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs
    (primary checkout root; PYTHONPATH, REMEDY_PROJECT and REMEDY_DATA_DIR removed in-process;
     PYTHONDONTWRITEBYTECODE=1; transcript under .remedy-wt/f261r25w/)

    RETURN CODE: 0
    LAST OUTPUT LINE: 17653 passed, 23 skipped, 1 warning in 1274.38s (0:21:14)
    DISTINCT BAD NODES: 0

No line-initial `FAILED ` or `ERROR ` in the transcript, so no node needed a lone re-run.

## Authored-text proofs

PLAN25, RECORD25, DEC24, DEC25, QOP-FROM, QOP-TO and SCOPE25 were extracted as the bytes strictly
between their `BEGIN` and `END` lines and matched their BEGIN-marker sha256 before use; none was
edited. The applied results were re-read from the git objects at C1 and compared to base blob plus
slice (G2). SCOPE25 sits in this file byte for byte directly after the Session section, assembled
from the extracted slice bytes. The edit tables `.agent/authored/f261-r25-alias.jsonl` and
`.agent/authored/f261-r25-split.jsonl` are byte-identical to their `.remedy-wt/f261-block/`
originals; their 15 and 11 rows applied in file order, each count read exactly as stated.

## Deviations & assumptions

None to the ordered commit sequence: C0a, C0b, C1, C2, C3 and C4 landed in that order, each
single-parent, on `d5e0a7b5`; no gate was skipped, weakened or re-valued. Declared: (1) one
directory listing at the start of the round read the top level of `.remedy-wt/` while locating the
block directory, beyond the two directories constraint 4 names; nothing there was opened or
written. (2) The G5 runner also removed `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, as SPEC S does.
(3) G4's ruff path list was read as the `.py` paths added or modified between C1 and C3.

## Next

1. Phase 1 rule 1 — re-read `.agent/STOP` from disk before anything else.
2. The reviewer's verdict on round 25.
3. The closure sequence of F261 under `docs/roadmap/STATUS_closure_protocol.md`.

Open findings: 125 by distinct id, with the High ids R-0803, R-0804 and R-0807.

Operator questions open: 1

## Session close — session 41, written after the reviewer's verdict on round 25

The planner and reviewer of session 41 reviewed rounds 23, 24 and 25 of F261, all three PASS, and
ends the session after those three delegated rounds — below the operator's target of six to eight
and below the floor of four. THE REASON, stated in one sentence as operator amendment
amend0905-throughput requires: round 25 reached F261's soft limit of 25 rounds and executed the
split-and-close default, so the feature's next work is its closure sequence — the integration
gate, the ledger rotation, the one consolidation pass of the §3 checklist, the evidence package,
the STATUS flip and the pull request — a procedure this session has not read, which the
reviewer's context, spent on three wide rounds with four research helpers, five stacked dry-run
tables, twenty mutation red-proofs and three pre-emission checklists, would author badly. No run
of authoring slips accumulated: the reviewer's own pre-emission reading caught and corrected, before
emission, a helper's wrong description of two open findings and a split generator whose Built
State contradicted the Acceptance variant chosen, and no slip reached a landed file. Nothing is
half-written; the branch is pushed at `1752331c`; one worktree; `git status --porcelain` empty.

### The verdict to book

The first commit of F261's closure sequence that writes the record appends the paragraph below to
`.agent/live_review.md` byte for byte, preceded by one empty line, per operator amendment
amend0827-process-diet rule 1.

Gate: F261 R25 — the F261 round 25 entry. VERDICT PASS. Written by the planner and reviewer of session 41 after reading the committed range `d5e0a7b5`..`1752331c` and re-deriving every reading below; the worker's report was evidence for none of them. It is booked here by the first commit of F261's closure sequence that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r25.md` at `9c5f654e` and `.agent/last_block.md` at `1c838a73` are byte-identical to the reviewer's scratch original, sha256 `cc0b0ba700b7fb977ab1e3287c330ca3668e5316ba506c493e9c836cba357cf3`, and the tables committed at `76ee0149` and `7994c69e` are byte-identical to the reviewer's carriers, sha256 `58f810e31bffb2fb8c2fbce5251b776a2df29fb641cd1a400984719052f3423f` and `0bb2f13086a36429f4d9e3ab62f4d4f8e688f339da1f3fdb6abd2ba2a9e81243`; the first is a research helper's generator output, regenerated by the reviewer on `d5e0a7b5` and byte-identical to the helper's, and the second is another helper's registration generator after the reviewer's own two corrections — the soft-limit wording and a Built State paragraph that matches F261's Acceptance section left as registered — run on the reviewer's alias dry-run commit. THE STATE: at `73fd6e08` and again at `1752331c`, `.agent/plan.md` equals PLAN25, `.agent/live_review.md` equals its `d5e0a7b5` blob followed by RECORD25, `.agent/decisions.md` its blob followed by DEC24 and DEC25, and `.agent/operator_questions.md` its blob with the pair QOP applied, which opens operator question Q3; the `Gate:` count reads 133 then 134, the distinct registered ids 134 then 134, the distinct `Done:` ids 9 then 9, and the open set 125 then 125. THE TABLE COMMITS: at `76ee0149` and at `7994c69e` the `apps`, `packages`, `scripts`, `tests`, `docs/guides`, `docs/system`, `docs/roadmap`, `docs/README.md`, `README.md` and `.claude` objects equal the reviewer's two stacked dry-run commits object for object, all twenty, and each `--no-renames` name list equals its dry run's; `git show --numstat` reads 136 insertions against 15 deletions and 226 against 9. THE HANDBACK at `1752331c` carries slice SCOPE25 exactly once, the Session line of round 25 and `Operator questions open: 1`. THE BEHAVIOUR, read by the reviewer in the primary checkout at `1752331c`: `python3 -B -m apps.cli.grouped settings --help` prints ` Also reachable as: remedy config` over the seven `config` commands, and `roadmap next` still proposes F261 as the active line, which is right until its closure flips it; on the reviewer's dry-run tree `roadmap status` printed `Next unchecked: F280 — `. THE RED-PROOFS ran twice in the reviewer's own worktree on the tree whose objects `7994c69e` reproduces, over the exact selection the block ordered: a control of 446 passed at exit 0, and each of the seven rows of the mutation carrier `8275e65a0ef5cdc752122c144d44b41e596ff6ab6cc418c4cf17170c70a8b491` exiting 1 with its named node among the failures, with nine, four, one, three, five, two and three failed nodes — unregistering the alias, dropping the parser's aliases, a help pre-scan that ignores the resolver, a help page that omits the other word, a resolver that ignores aliases, the F280 STATUS line dropped and the `TOTAL_FEATURES` pin reverted; every FROM is whole lines occurring exactly once. THE REVIEWER'S RUN in the primary checkout at `1752331c` of the whole of `tests/cli/` and `tests/docs/`, `tests/test_command_catalog.py`, `tests/test_help_renderer.py`, `tests/test_cli_main.py`, both command-discovery test files and `tests/orchestration/test_import_reachability.py` read 1708 passed, and `python3 -m ruff check` over the five edited `.py` files printed `All checks passed!`. The worker ran the full suite once in the primary checkout, as the block orders: exit 0, `17653 passed, 23 skipped, 1 warning in 1274.38s`, with no line-initial `FAILED ` or `ERROR ` in its transcript, which the reviewer read. The worker declared one listing of the top of `.remedy-wt/` beyond the two directories constraint 4 opens, which read no file and wrote nothing. The open set reads 125 by distinct id at `1752331c`.

### What this session did

Three rounds of T003, each built from research helpers' measured tables that the reviewer
re-applied in its own worktree and gated on tree ids. Round 23 deleted the queue words of `job`,
`worker run` and `mission ledger` (DECISION F261 D22; R-0927 to R-0930), after measuring that the
queue gate DECISION F261 D21 named had `worker run` as its only production caller — and kept
`propose` deferred, because `self execute` and the cockpit's `can_finalize` still gate on its
store. Round 24 deleted `job rerun` and renamed `teach` to `teacher`, words and names, in two
table commits (DECISION F261 D23; R-0931), and deferred `job fulfill`, whose fixture contract is
the only production write of a non-zero test-run budget that `test run` needs. Round 25 landed the
`settings` alias over `config` (DECISION F261 D24) and, at the soft limit, registered F280 and
wrote the scope report (DECISION F261 D25; operator question Q3). The catalog reads 30 groups and
154 commands.

### What the next session needs to know

- F261 IS AT ITS SOFT LIMIT WITH SPLIT-AND-CLOSE EXECUTED. Its next rounds are the closure
  sequence of `docs/roadmap/STATUS_closure_protocol.md`, which is exempt from the no-bookkeeping
  rule of amend0827 rule 1; its first record commit books `Gate: F261 R25` from this section.
  F261's Built State says the Goal & Done sentence is not met and F280 owns the rest.
- OPERATOR QUESTION Q3 is open: the split may be reversed by the operator.
- A CLOSURE READING TO CHECK: F261's teacher Acceptance line asks that a grep for the group id
  `teach` return only accepted history, while DECISION F261 D23 deliberately kept four lines of
  `docs/system/vocabulary.md` that record the rename and four prose uses of the verb; the Built
  State calls that line reached in part, and F280 carries the whole line.
- METHOD: a generator that takes its base commit as an argument let two tables stack in one round
  twice, with the second regenerated on the reviewer's own first dry-run commit and proved
  byte-identical. A helper's description of open findings is a lead, not a reading: one helper
  named R-0898 and R-0745 as touching the run contract and the manifest writer, and neither does.

### Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first; then the Open PR Gate, which finds
   no open pull request for this branch.
2. F261's closure sequence, whose first record commit books `Gate: F261 R25` from this section.
3. After F261 merges, Rule A5 proposes F280.

Operator questions open: 1
