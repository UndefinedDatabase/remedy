STEP F025 R9 — THE CLOSURE SEQUENCE'S FIRST HALF: BOOK ROUND 8, WRITE THE BUILT STATE, CONSOLIDATE THE CHECKLIST, RUN THE SELF-USE ITEM AND THE ONE FULL SUITE

GOAL
Book round 8's PASS and R-1056's resolution; append the Built State to
`docs/roadmap/features/T5_F025.md`; run the checklist consolidation pass, which joins nothing and
keeps `docs/agents/planner_reviewer_prompt.md` §3 at 34 items; generate the closure's self-use item
and run it to its approval gate (closure precondition 6); and run this feature's ONE full suite,
committing its transcript. This round closes nothing: the evidence bundle, the review package, the
ledger rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line of your own. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3, 6 and 7;
`docs/agents/integration_gate.md`; `.agent/authored/f263-r7-block.md`'s C5 and C6, which this
round's C5 and C6 follow; and `.agent/selfuse_f263/`, whose file names C5 mirrors.

THE DIRECTORIES
  `.remedy-wt/f025-r9/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r9-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use `git -C
<path>`, never `cd` your shell into a worktree. Copy and hash with python (`shutil.copyfile`). A
heredoc containing a dollar-brace is refused: write such a script under your own directory and run
the file. The ONE npm command this round may run is C6's `npm --prefix apps/ui run build`; never
`npm install`, `npm ci` or `npx`. Never `git stash`, never `pkill -f`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In the primary checkout `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain`
   must be empty, `git branch --show-current` must read `feature/f025-pause-resume`, and
   `git log --oneline -1` must read `1172c5cf`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r9/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found, and `git branch --list 'remedy/job-*'`.

PAYLOADS — under `.remedy-wt/f025-r9/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| built_state.md | 79 | 6111 | 6bf899e332d7145ad45b969ec59de77ab13db3b6795eae3429239022d2a2438e |
| consol_from.txt | 1 | 46 | 4aa784fbe92535f6cd688e3dd9e27b7c5aeb5bc9b243dd8923e13a81ade24e04 |
| consol_to.txt | 8 | 737 | 8cdf3907a663ed01e207fbe10a07171fb548b482b2637e20ae2c9887c707a9da |
| ledger.md | 4 | 3855 | 0e62113e0598a1de99c4632858184ce7b4b8abc6f9b88480b0a4a82f8d4c6099 |
| plan.md | 30 | 1096 | c969f2a7010b67c545a71f4859fa81e9af9bf5a3a35d52512399d54680ec827b |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line); `plan.md`
REWRITES `.agent/plan.md`; `built_state.md` is appended to `docs/roadmap/features/T5_F025.md` (it
starts with its own blank line). In `docs/agents/planner_reviewer_prompt.md` the bytes of
`consol_from.txt` are replaced by the bytes of `consol_to.txt` — containment test: TO contains
FROM: true, so the pair is an APPEND: FROM occurs exactly once in the file before the edit, and
after it TO occurs exactly once and the file equals its `1172c5cf` bytes with FROM replaced by TO.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f025-r9-block.md` := this block and each payload as
    `.agent/authored/f025-r9-<name>`. Subject `F025 R9 C1: copy round 9 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 122, that is the block copy's own lines and 79/0 `.agent/authored/f025-r9-built_state.md`, 1/0 `.agent/authored/f025-r9-consol_from.txt`, 8/0 `.agent/authored/f025-r9-consol_to.txt`, 4/0 `.agent/authored/f025-r9-ledger.md`, 30/0 `.agent/authored/f025-r9-plan.md`.
C2 RECORDS: the ledger append and the plan rewrite, one commit. Subject
    `F025 R9 C2: book round 8's PASS and resolve R-1056`. Expected: 4/0 `.agent/live_review.md`, 9/8 `.agent/plan.md`.
C3 THE BUILT STATE AND THE CONSOLIDATION: the append to T5_F025.md and the planner prompt pair.
    Subject `F025 R9 C3: write the Built State and consolidate the checklist`. Expected: 7/0 `docs/agents/planner_reviewer_prompt.md`, 79/0 `docs/roadmap/features/T5_F025.md`.
C4 THE SELF-USE ITEM (closure precondition 6), from a scratch Python file of yours run in the
    primary checkout:
    (a) `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST, with no
        arguments. The reviewer's dry run in a worktree at `1172c5cf` appended `SU-030`, "Address
        ledger finding R-1055", provenance `generated (self-use-generator tier 1, ledger scan,
        R-1055)`. Report what yours does, and `next_self_use_item()`'s answer after it.
    (b) RUN it with `packages.orchestration.self_use_runner.run_next_self_use_item`, with
        `dest_dir` = `/home/decodeux/Repos/remedy/.remedy-wt/f025-r9-selfuse` and nothing else,
        so `max_tasks` stays 1 and both roles resolve from the one `self_use` role configuration
        (DECISION amend0920-selfuse-real D2). It runs to the approval gate and is NEVER applied. A
        blocked or stopped job is an outcome to record, not a reason to stop.
    (c) Save under `.agent/selfuse_f025/`, mirroring `.agent/selfuse_f263/`'s file names: the item
        markdown as `<id>.md` for the id (a) really produced, `entry_and_job_file.txt`,
        `execution_config.txt`, `result_state.txt`, `timing.txt`, `full_transcript.txt`, and
        `run_defects.txt` holding every string
        `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
        run's own `JobPlan`, verbatim, or the literal `NONE` for an empty tuple.
    (d) Then `python3 -m pytest tests/docs/ -q -p no:cacheprovider`; the generated item's text
        lands in `scripts/self_use_queue.json`, which a docs test reads (finding R-1015). Red is a
        STOP under constraint 5.
    This commit's paths: `scripts/self_use_queue.json` and `.agent/selfuse_f025/**`. You register
    no finding: the reviewer authors every registration from `run_defects.txt` next round.
    Subject `F025 R9 C4: generate and run the closure's self-use item, record its defects`.
C5 THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4:
    (a) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
        — a refused or failing build is a STOP under constraint 5 — then `git status
        --porcelain`, which must still be empty.
    (b) `python3 -m pytest -n auto -q`, its log written outside the repository at
        `/home/decodeux/remedy-gate-scratch/f025-full-suite.txt`, or under
        `.remedy-wt/f025-r9-worker/` if the sandbox refuses that path, said so; measure its wall
        time. Write `.agent/authored/f025-closure-suite.txt` holding the command, the real exit
        code, the wall time, the summary line and the FULL list of bad node ids (failed plus
        errors), or the literal `NONE`.
    (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
        with the transcript. Subject `F025 R9 C5: record the closure suite transcript and rewrite
        handoff for round 9`. Then `git push origin feature/f025-pause-resume`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. Append and replace by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`; C4's queue and record files included.
3. The round's tracked path set is: the `.agent/authored/f025-r9-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T5_F025.md`,
   `docs/agents/planner_reviewer_prompt.md`, `scripts/self_use_queue.json`,
   `.agent/selfuse_f025/**`, `.agent/authored/f025-closure-suite.txt` and `.agent/handoff.md`.
   Nothing under `packages/`, `apps/` or `tests/`; no edit to `README.md`,
   `docs/roadmap/STATUS.md`, any `consumed_by` field, `.agent/decisions.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If the full suite in C5 is RED, that is this feature's work and not a stop: commit the transcript
   exactly as measured, report every bad node id, and hand back; the repair rounds are the
   reviewer's to order (amend0917-throughput rule 2). Never weaken an assertion, delete a test or
   mark anything xfail on your own initiative.
5. Any other red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md
   "If Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. The self-use run may leave `remedy/job-*` branches, worktrees or evidence directories behind.
   Report them; delete nothing you did not create as scratch, never delete a branch, and leave
   every existing worktree alone.
7. The full suite runs ONCE, in C5, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run
before C5 is written; G5 is C5's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r9-*` payload copy byte-equal to its source by `git show <C1>:<path>`
   (the block copy against `.remedy-wt/f025-r9/block.md`).
G2 THE RECORDS, THE BUILT STATE AND THE CONSOLIDATION: at C2 `.agent/live_review.md` equals its
   `1172c5cf` bytes plus ledger.md and `.agent/plan.md` equals plan.md; at C3 T5_F025.md equals its
   `1172c5cf` bytes plus built_state.md, and the planner prompt pair holds as PAYLOADS states;
   `open_finding_ids` over the ledger at C2 — the reviewer's simulation read `['R-1008', 'R-1055']`; and
   `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt at
   `1172c5cf` and at C3, the same 34 numbers at both.
G3 THE LINTER ON THIS BLOCK, at C3: `python3 -m apps.cli.main integrity block
   .remedy-wt/f025-r9/block.md`, real exit code 0; report the whole output.
G4 THE TESTS AND THE TREE, in the primary checkout at C4, serially:
   `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_block_lint.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py
   tests/cli/test_golden_path.py` — exit 0, summary line reported; C4's readings verbatim, with the
   self-use job's id, its builder and reviewer names and models — the `self_use` role's
   configured provider, never `fake` — its state, and `run_defects.txt`; then `python3 -m
   apps.cli.main integrity check --json`, six `pass` at `fail_count` 0; and `git status
   --porcelain` empty with no untracked file (closure precondition 3).
G5 THE INTEGRATION GATE: the UI build's last line and real exit code, `git status --porcelain` after
   it, then the full suite's real exit code, wall time, summary line and every bad node id, all in
   `.agent/authored/f025-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G6 AFTER C5 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 7`, `git worktree list`,
   `git branch --list 'remedy/job-*'`, the push's real outcome, and `gh pr list --state open --json
   number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the self-use readings, the full suite's summary line and bad
node ids, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit
and per gate), the deviations, and the next action. Session section: SESSION 2 of feature F025,
round 9, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review
of round 9, then the closure's second half — the booking of round 9, the registrations the self-use
defects ask for, any repair the suite requires, the evidence bundle and the review package — and
then the closing round. State the open-findings count as the script reads it at C2, and "Operator
questions open: <the count of `### Q` headings in the file at C2>".
