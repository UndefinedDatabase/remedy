STEP F027 R7 — T003 FIRST HALF: the veto reaches the page's data — the dashboard's `vetoes` section, the node seeded and streamed as `vetoed`, the reason verbatim in the job's report, plain-words labels on the proposal's buttons — and R-1068's repair

GOAL
Book round 6's verdict, register R-1068, add one prose-slip line, record DECISION F027 D7, and land
it: `_build_dashboard` carries a `vetoes` section, the page normalizes it, seeds a vetoed task's
node as `vetoed` and moves a node to `vetoed` on the live `task_vetoed` event, the job's text and
exported reports carry the reason verbatim, a decision may carry `option_labels` that the inbox
card's buttons show, the replan proposal carries plain words for its two options, and the page's
event catalog names both veto events — with tests and a mutation tool proving they bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S5 below. Only the `.agent/` records travel as
payloads. Read DECISION F027 D7 in `records.diff` before you write code: it is the design, and the
design reference `docs/ui/design_reference/` binds any UI wording you choose.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r7/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r7-dry/`, `.remedy-wt/f027-r7-drafts/`, `.remedy-wt/f027-review/` and every
                                  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r7-worker/`    YOURS for logs, scripts and scratch configs; create it if
                                  absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the one Node binary you may run is
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest`, and only as G5 orders it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f027-task-veto`, and `git log --oneline -1` must read `25a295c0`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1169 | 4d77b4f10bda08af45172470de77146de1162663ebe9bd699364ed4797e812de |
| records.diff | 79 | 13526 | f1e3362d16825b2ecdbbe7a7e60c4ce6339c4cfe9ee004d3710ff233aee85965 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `25a295c0`. It appends to `.agent/live_review.md`
round 6's gate entry and R-1068's registration, one line to `.agent/prose_slips.md`, and to
`.agent/decisions.md` DECISION F027 D7.

THE SPECIFICATION
S1 R-1068: `apps/ui/src/api/humanizeCatalog.ts` gains `task_vetoed` and `veto_proposal_answered`,
   each in its sorted place with one plain sentence an operator reads in the live feed, as its
   neighbours are written.
S2 THE SECTION, in `packages/orchestration/ui_server.py`: `_build_dashboard` gains
   `"vetoes": _build_veto_section(job)` beside `task_specs`; the helper, importing `task_veto`
   inside itself, returns D7 (1)'s `tasks` (keys `task_id`, `reason`, `actor`, `requested_at`,
   `request_id`, `status_at_veto`, `unreachable_task_ids`, `answer`), `vetoable_task_ids`,
   `unreachable_task_ids` and `error`, all lists in plan order, and never raises: a `TaskVetoError`
   empties the three lists and sets `error` to its text. The door's own methods do not change.
S3 THE PAGE'S DATA, in `apps/ui/src`: a typed `RemedyVetoes` in `api/types.ts`; `api/remedyApi.ts`
   normalizes `dashboard.vetoes` defensively, as `normalizePause` does, a missing or malformed
   section reading as empty; `components/graph/brainView.ts`'s `dashboardBrainSeeds` gains the
   vetoed task ids as a parameter after the paused ones, and a task named there seeds the status
   `vetoed`, which wins over `paused`; `BrainGraphStage.tsx` passes `dashboard.vetoes`' task ids;
   `components/graph/brainOntology.ts`'s `SEED_STATUS_STATE_TABLE` gains `vetoed: "vetoed"`;
   `BRAIN_FILTER_STATES.done` gains `vetoed`, the run never touching such a node again; and
   `components/graph/brainReducer.ts` gains a `task_vetoed` case that births the node if needed
   and sets `vetoed` unless the node has passed, as `onTaskPaused` refuses to paint over a
   finished node.
S4 THE REPORT, in `packages/orchestration/pingpong_job.py`: `format_job_report_text` gives
   `TASK_VETOED` the icon `/` and prints under a vetoed task the line `      Vetoed by <actor>:
   <reason>`, the reason verbatim; `export_job_report` gives each vetoed task a `veto` object of
   `reason`, `actor`, `requested_at` and `unreachable_task_ids`. Both read the record's
   `metadata["task_vetoes"]` first and the control files for a veto no run has folded yet, a
   `TaskVetoError` there printing and exporting nothing extra; a job with no veto reports byte for
   byte as before.
S5 THE INBOX'S WORDS: `packages/orchestration/veto_proposal.py`'s decision payload gains
   `option_labels`, `replan_follow_up` → "Replan the remaining work as a new job" and
   `accept_reduced_scope` → "Accept the smaller scope"; in `apps/ui/src/api/decisionCard.ts`,
   `decisionAnswers` reads `payload.option_labels` when it is an object of strings and labels an
   option's answer with its entry, the value otherwise, the posted `value` unchanged, and nothing
   branches on the decision's type.

THE TESTS — a NEW FILE at `tests/ui_server/test_dashboard_vetoes.py` over the dashboard builder
as `tests/ui_server/test_dashboard_pause.py` does: no veto, one veto with its unreachable set and
its reason verbatim, an answered one, a finished job whose vetoable list is empty, and a corrupt
veto file setting `error` with every list empty. `tests/orchestration/test_task_veto_runner.py`
gains the text and exported reports of a vetoed job, one with a veto no run has folded, and the
report of a job with no veto unchanged. `tests/orchestration/test_veto_proposal.py` gains the
payload's `option_labels`. The vitest files beside the TypeScript you change gain: the section's
normalization, missing and malformed included; a vetoed seed winning over a paused one; the
`task_vetoed` case, a pass left as it is; the filter group; and `decisionAnswers` labelling from
`option_labels` while posting the value, with a card without them unchanged.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r7-block.md`,
  `.agent/authored/f027-r7-plan.md` and `.agent/authored/f027-r7-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 110. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R7 C2: book round 6, register R-1068, record D7`
  Expected by `git show --numstat`: 50/0 decisions.md, 4/0 live_review.md, 9/9 plan.md,
  1/0 prose_slips.md.
C3 — R-1068: S1. Subject: `F027 R7 C3: repair R-1068, name both veto events in the page's catalog`
C4 — THE SECTION, THE REPORT AND THE LABELS' SOURCE: S2, S4 and S5's Python half, with their tests.
  Subject: `F027 R7 C4: the dashboard's vetoes section, the reason in the report, and option labels`
C5 — THE PAGE: S3 and S5's TypeScript half, with their vitest tests.
  Subject: `F027 R7 C5: seed and stream the vetoed node, and label the proposal's buttons`
C6 — THE MUTATION TOOL: `.agent/authored/f027-r7-mutations.py`.
  Subject: `F027 R7 C6: the round's red-proof mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and
  appended to `.agent/live_review.md` a blank line and then exactly one line
  `Landed: R-1068 — <one sentence naming what changed>, at <C3's short SHA>.`, never a `Done:`
  line (docs/agents/planner_reviewer_prompt.md §4 item 4).
  Subject: `F027 R7 C7: rewrite handoff for round 7`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r7-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `packages/orchestration/ui_server.py`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/veto_proposal.py`, `apps/ui/src/api/humanizeCatalog.ts`,
   `apps/ui/src/api/types.ts`, `apps/ui/src/api/remedyApi.ts`, `apps/ui/src/api/decisionCard.ts`,
   `apps/ui/src/components/graph/brainView.ts`, `apps/ui/src/components/graph/brainOntology.ts`,
   `apps/ui/src/components/graph/brainReducer.ts`, `apps/ui/src/components/graph/BrainGraphStage.tsx`,
   the `.test.ts` file beside each of those TypeScript sources, `tests/ui_server/test_dashboard_vetoes.py`,
   `tests/orchestration/test_task_veto_runner.py`, `tests/orchestration/test_veto_proposal.py`, and
   `.agent/handoff.md`. One widening is allowed and must be declared: a test that pins, by an exact
   equality, a table S1, S3 or S5 widens may gain the one new entry. Report the list
   `git diff --name-only 25a295c0` measures after C7. Do NOT touch `task_veto.py`,
   `long_run_executor.py`, `decision_inbox.py`, `apps/ui/src/components/graph/renderers/`,
   `apps/ui/src/components/detail/`, `apps/ui/package.json`, `docs/`, `.agent/context.md`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back with the tree clean: a draft you cannot verify is saved as
   a patch under your own directory and removed from the tree. Do not repair the reviewer's
   payloads. Any other existing test that goes red because of S1 to S5 is reported with its
   output, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every worktree `git worktree list` showed at your step 4, and every stash, alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F027 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r7-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r7/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 314376 | aed7abbde6bb8716690f1fc70ce4b438e5d001cd35c99b8d1377d00dee77eb03 |
 | .agent/decisions.md | 2184242 | b289cafbef66c7ec3c8325d065781b934163e5148ce8a0c7ca473bc9332ae09a |
 | .agent/prose_slips.md | 369137 | a20d3776fcc502901420ca4e30cc4d9d49ad7ebf2a6b951e118cdda2cdb1ef91 |
 | .agent/plan.md | 1169 | 4d77b4f10bda08af45172470de77146de1162663ebe9bd699364ed4797e812de |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read `['R-1068']`).

G3 THE CODE — `python3 -m ruff check` over every Python file of the round's path set at the last
 code commit, and the `SKIPPED` lines of G4, which must name no TypeScript or vitest node.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_dashboard_vetoes.py tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_dashboard_pause.py tests/ui_server/test_dashboard_task_specs.py tests/ui_server/test_sse_stream.py tests/ui_server/test_live_state.py tests/orchestration/test_veto_proposal.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_token_ledger.py tests/test_role_override_flags.py tests/orchestration/test_test_runner.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the round's records, and read `1 failed, 1845 passed, 9
 skipped` at real exit code 1, the one failure R-1068's and the skips the worktree's absent UI
 toolchain among them. Your run must read no failure. Report every `SKIPPED` line, the nodes each
 new or grown test file contributes (`--collect-only -q`), and account for every difference from
 the reviewer's count. Then `python3 -m apps.cli.main integrity check --json`, which must read all
 six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r7-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs the named tests, restores the bytes, and prints one line per mutation: its
 label, the exit code, the failed count and the failing test names. It runs an unmutated control
 first and last for each runner and ends with `restored byte-identical: True` per file and a final
 line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Python mutations run
 `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/ui_server/test_dashboard_vetoes.py`, `tests/orchestration/test_task_veto_runner.py`,
 `tests/orchestration/test_veto_proposal.py` and `tests/ui_contracts/test_humanize_catalog.py` from
 the worktree's root after purging its `__pycache__` directories. TypeScript mutations run
 `/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest run --config <scratch config>` from
 `/home/decodeux/Repos/remedy/apps/ui`, where the scratch config under your own directory exports a
 PLAIN OBJECT with `root` the primary `apps/ui`, `cacheDir` under `.remedy-wt/`, and
 `test: { environment: "node", include: [<the worktree's changed .test.ts files by absolute
 path>] }` (DECISION F256 D6's route; a config importing `vitest/config` cannot resolve); before the
 mutations, prove the route reads the worktree's sources by one mutation that cannot pass whatever
 the tests import, and report it. The mutations:
  m1 `_build_veto_section` lets a `TaskVetoError` out;
  m2 the section's `unreachable_task_ids` is always empty;
  m3 the text report drops the `Vetoed by` line;
  m4 `export_job_report` drops the `veto` object;
  m5 the proposal's payload drops `option_labels`;
  m6 `task_vetoed` leaves the page's catalog;
  m7 `SEED_STATUS_STATE_TABLE` loses its `vetoed` row;
  m8 the `task_vetoed` case paints `vetoed` over a passed node;
  m9 `decisionAnswers` ignores `option_labels`;
  m10 `decisionAnswers` posts the label instead of the value;
  m11 the normalizer drops each veto's reason.
 Run it in `git worktree add --detach .remedy-wt/f027-r7-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over:
 you then say whether a test can see the behaviour at all, add the test that catches it if one
 can, and re-run the tool. Then `git worktree remove --force .remedy-wt/f027-r7-mut`,
 `git worktree prune`, and `git worktree list`; and `git status --porcelain` must be empty, a
 stray `.vite/` included.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty; `git log --oneline`
 from `25a295c0` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F027, round 7, and says in one sentence how much context you had left. Where S1 to S5
leave a choice open, make it, say so in the deviations, and never widen the path set for it
beyond constraint 3's one declared widening.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7, then the rest of T003 — the dimmed unreachable set with its link, the popover's veto
block, the veto form and the hover text. State the open-findings count, 1 (R-1068, landed this
round and awaiting the reviewer's resolution), and the operator-questions count, 5.
