STEP F038 R1 — CLAIM F038, REPAIR R-1091, AND LAND T001's NODE SCOPE: the chat's evidence items, the node-scope collector and the composer under the token cap

GOAL
Pull request 291 is merged; `main` is at `fec08a5b`. The first unchecked STATUS line is F286, the
fifth findings paydown, and no finding is open, so DECISION F038 D2 moves F286 one feature down
again and F038 is claimed. Cut F038's branch, claim it, re-head the live review record, book
F036's round 9 verdict, register finding R-1091, and record DECISIONS F038 D1 and D2. Then repair
R-1091 — the two readers of an evidence directory's `task_runs/` accept only `T<digits>`, while
every task `remedy do` plans carries a sixteen-hex id — and land the node scope of T001 in a NEW
module `packages/orchestration/chat_evidence.py`: the evidence item and its problems, the
composer that keeps an ordered prefix under the 4000-token cap after redaction, and the collector
of one task's own records — plus their tests. The module writes no file, nothing calls it yet, no
model is called, and no command, route, event name or browser code changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S7 below. Only the `.agent/` records and the
two roadmap files travel as payloads. Read DECISION F038 D1 and finding R-1091 in the claim diff
before you write code: they are the design and the defect this specification implements. Before
you write anything, read whole: `packages/orchestration/diff_view_source.py`; `_task_ids`,
`_aggregate_gate` and `build_final_verifier_report` in `packages/orchestration/final_verifier.py`;
`build_task_run_rounds` and `_round_facts` in `packages/orchestration/run_rounds_view.py`;
`resolve_job_evidence_dir` in `packages/orchestration/evidence_index.py`; `load_run_events` in
`packages/orchestration/timeline.py`; `resolve_data_root`, `job_evidence_dir`,
`job_evidence_index_dir`, `run_dir`, `run_log_dir` and `mint_task_id` in
`packages/orchestration/data_paths.py`; `redact_text` in `packages/orchestration/stream_evidence.py`;
`estimate_text_tokens` in `packages/orchestration/token_economy.py`; `TaskEntry` and `JobPlan` in
`packages/orchestration/pingpong_job.py`; `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py`;
and, for fixtures, the helpers at the top of `tests/orchestration/test_result_tour.py`,
`tests/orchestration/test_diff_view_source.py` and `tests/orchestration/test_final_verifier.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f038-r1-dry/`, `.remedy-wt/f038-r1-sim/`, `.remedy-wt/f038-r1-src/`,
  `.remedy-wt/f038-review/`       The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f038-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set `REMEDY_DATA_DIR` inside tests with `monkeypatch.setenv`, never on a command line.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `fec08a5b9`. Report all three. Then
   `git checkout -b feature/f038-grounded-chat` and report the branch. Do NOT pull: the Open PR
   Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 182 | 23540 | 556b42c2fc81538f1db10f8d2d7e2c74b6b21d89043d64558f7fc57b58ddfe31 |
| context.md | 37 | 1657 | c37f18655f13025184c808c0e63685f66a81af13769b8aa68868addb096a7624 |
| plan.md | 33 | 1233 | 11d6ca8cb63017a9b3b9e8e1b2af28ddcee0a64f03b811bbbf651acb4da1a673 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`fec08a5b` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F036's round 9 gate entry and the
registration of R-1091 appended), `docs/roadmap/STATUS.md` (F038's line `[ ]` to `[~]`, moved
above F286's Tier 2 heading), `docs/roadmap/features/T2_F286.md` (one two-line note) and
`.agent/decisions.md` (DECISIONS F038 D1 and D2 appended).

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 R-1091, THE REPAIR. In `packages/orchestration/diff_view_source.py`, `SAFE_TASK_RUN_ID_RE`
   becomes `re.compile(r"^(?:T\d{3,}|[0-9a-f]{16})$")`, and the comment above it gains a sentence
   saying both shapes are the ones the evidence exporter writes — `T<digits>` from a parsed job
   file and the sixteen hex characters `data_paths.mint_task_id` mints for every task
   `remedy do` plans — naming finding R-1091. In `packages/orchestration/final_verifier.py`,
   `_SAFE_TASK_ID_RE` becomes the same expression, with a comment above it saying the same and
   naming R-1091. Nothing else in either file changes.
S2 THE MODULE, a NEW FILE at `packages/orchestration/chat_evidence.py`. A docstring naming F038
   T001 and DECISION F038 D1, with one sentence stating that Remedy deliberately does not let a
   scope's evidence reach past its own records. At module level it imports the standard library
   and, from `packages.orchestration`, only: `data_paths.resolve_data_root`, `diff_view_source.build_diff_view`,
   `evidence_index.resolve_job_evidence_dir`, `run_rounds_view.build_task_run_rounds`,
   `stream_evidence.redact_text`, `timeline.load_run_events` and
   `token_economy.estimate_text_tokens` — nothing from `pingpong_job`, `ui_server` or `apps`.
   Constants `CHAT_SCOPE_NODE = "node"`, `CHAT_SCOPES = (CHAT_SCOPE_NODE,)`,
   `CHAT_ANCHOR_KINDS = ("node", "round", "diff", "event")`, `CHAT_EVIDENCE_TOKEN_CAP = 4000`,
   `CHAT_ITEM_TEXT_MAX_CHARS = 400`, `CHAT_NOT_RECORDED = "not recorded"`, and
   `class ChatEvidenceError(ValueError)`.
S3 THE ITEM. Frozen dataclasses `ChatEvidenceItem(kind: str, ref: str, text: str)` and
   `ChatEvidenceSet(scope: str, subject: str, items: tuple[ChatEvidenceItem, ...], omitted: int,
   tokens_estimated: int)`. `chat_item_problems(item) -> list[str]` answers one line per breach,
   in this order and with these exact words: not a `ChatEvidenceItem` → only
   `not a ChatEvidenceItem`; a kind outside `CHAT_ANCHOR_KINDS` →
   `kind <repr> is not one of node, round, diff, event` (the kinds joined by ", " from the
   constant); a ref that is not a non-empty string → `ref is not a non-empty string`; a text that
   is not a string or is empty after stripping → `text is not a non-empty string`, otherwise a text
   holding `\n` or `\r` → `text holds a line break`, and one longer than the bound →
   `text is longer than 400 characters` (spelled from the constant). `[]` for a sound item.
   `make_chat_item(kind, ref, text) -> ChatEvidenceItem` applies `redact_text` FIRST, then folds
   every whitespace run to one space and strips the ends (`" ".join(s.split())`), then, when the
   result is longer than the bound, keeps its first `bound - 1` characters plus "…".
   `render_chat_item(number, item) -> str` is `f"[{number}] {item.kind}:{item.ref} — {item.text}"`
   and `render_chat_evidence(evidence_set) -> str` joins the rendered items, numbered from 1, with
   "\n" ("" for no item).
S4 THE COMPOSER. `compose_chat_evidence(scope, subject, items, *, token_cap=CHAT_EVIDENCE_TOKEN_CAP)
   -> ChatEvidenceSet` raises `ChatEvidenceError` with `scope <repr> is not one of node` for a
   scope outside `CHAT_SCOPES`, and with `item <index>: <the problems joined by "; ">` for the
   first item with any problem, index counted from 0. Otherwise it walks the items in order and
   keeps each while `estimate_text_tokens` of the rendered kept items plus this one, joined by
   "\n", is at most `token_cap`; at the first item that does not fit it stops. `items` is the kept
   prefix, `omitted` the count not kept, `tokens_estimated` the estimate of the kept rendering
   (0 when none is kept).
S5 THE NODE SCOPE. `collect_node_evidence(job, task_id) -> list[ChatEvidenceItem]` finds the task
   whose `str(task_id)` EQUALS `task_id`, else raises `ChatEvidenceError` with
   `task <repr> is not a task of job <job id>`. Then, in this order, every item made with
   `make_chat_item`:
   (a) the record, each anchored `node` with the task id: `Task <id>: <title or "not recorded">`;
       `Status: <status>`, followed by `; final status: <final_status>` when that is set and then
       ` (<final_status_detail>)` when that is set too; `Reviewer verdict: <verdict or
       "not recorded">`; `Tests: passed`, `Tests: failed` or `Tests: not recorded` for
       `test_passed` True, False or anything else; `Repair rounds used: <used> of <allowed>`;
       then `Error: <error>` and `Tripped limit: <tripped_limit>`, each only when set.
   (b) the rounds, from `build_task_run_rounds(job, task_id)`: when `available`, one item per
       round, kind `round`, ref `<task id>#<round>`, text `Round <round> (<kind or
       "not recorded">): tests <passed/failed/not recorded>; reviewer verdict <the reviewer's
       verdict or "not recorded">`; otherwise one `node` item `Run rounds: not recorded (<reason>)`.
   (c) the diff, from `build_diff_view(resolve_job_evidence_dir(<job id>), task_id=task_id)`: when
       `available`, one item per file in order, kind `diff`, ref the path, text
       `Changed <path> (<status>, +<added> −<deleted>)` with U+2212 as the minus sign, then, when
       the view is `truncated`, one `node` item
       `Diff: cut at its size ceiling; later files are not listed`; otherwise one `node` item
       `Diff: not recorded (<reason>)`.
   (d) the run log, from `load_run_events(resolve_data_root(), <job id>)`, NEWEST FIRST (the
       reverse of the list it returns): every event whose `event` is a non-empty string and whose
       task is this task — its top-level `task_id` when that is set, else `metadata["task_id"]`
       when `metadata` is a dict — gives kind `event`, ref `<event>@<timestamp>`, text
       `<timestamp> <event>`, followed by `: <message>` when `message` is set and
       ` (outcome <outcome>)` when `outcome` is set; when no event qualifies, one `node` item
       `Run log: not recorded for this task`.
   `node_evidence_set(job, task_id, *, token_cap=CHAT_EVIDENCE_TOKEN_CAP) -> ChatEvidenceSet` is
   `compose_chat_evidence(CHAT_SCOPE_NODE, task_id, collect_node_evidence(job, task_id),
   token_cap=token_cap)`.
S6 THE GUARD. `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py` gains, between the
   `bench_run.py` and `ci_budgets.py` entries, `("packages/orchestration/chat_evidence.py",
   "F038's grounded chat evidence, the node scope and the composer; the chat command wires it in a
   later round (DECISION F038 D1 (6)) and removes this line")`, split over lines as its neighbours
   are. Nothing else in that file changes.
S7 THE LANDED LINE. In C3, append to `.agent/live_review.md` one blank line and then one line that
   begins `Landed: R-1091 — ` and says in one sentence what changed, naming both files; it names no
   commit, because its own commit is the one that lands it. Never write a `Done:` line.

THE TESTS. In `tests/orchestration/test_diff_view_source.py`, one new test: an evidence tree holding
`T001` and the minted run `0123456789abcdef`, each with a `safe.diff`, plus four near-miss
directories `0123456789abcde`, `0123456789abcdef0`, `0123456789ABCDEF` and `0123456789abcdeg`;
`list_task_run_ids` reads exactly `["0123456789abcdef", "T001"]`, and `build_diff_view` serves the
minted run: available, its `source`, and its file paths. In
`tests/orchestration/test_final_verifier.py`, one new test: `_seed_pass_task` under
`0123456789abcdef`, its `spec_compliance_check.json` rewritten to `FAIL`; the report's
`spec_compliance` reads `FAIL` and its `verdict` is not `PASS`. No existing test changes.
A NEW FILE `tests/orchestration/test_chat_evidence.py`, `REMEDY_DATA_DIR` under `tmp_path`, records
written by the real writers (`save_job_plan`; a run report at `run_dir(<run id>)/"result.json"`; a
`safe.diff` under `job_evidence_dir(job_id)/"task_runs"/<task id>` with an index record
`<job_evidence_index_dir()>/<job id>.json` holding `{"evidence_dir_local": "<dir>"}`; events as
JSON lines under `run_log_dir(job_id)`). Tasks carry the minted default id. At least, one test each:
a task with a title, a status and final status, a verdict, tests passed, repair rounds, a run
report of two rounds, a two-file diff and three events — one naming it at the top level, one
naming another task, one naming it under `metadata` with a message and an outcome — yields
EXACTLY the eleven items S5 states in order, compared as `(kind, ref, text)`; a task with nothing
recorded yields exactly the eight items S5 states, reasons `no_run_recorded` and
`evidence_dir_unavailable` included; the status detail, a failed test, an error and a tripped
limit each appear; an unknown id, an eight-character prefix of a real id and "" are refused; an
event with no name gives no item; `make_chat_item` removes an `sk-ant-` key, folds a line break,
cuts a 1000-character text to exactly 400 ending "…" and keeps a 400-character text whole;
`chat_item_problems` reads each of its lines; under the default cap two hundred items whose texts
run about a hundred characters keep a strict, ordered prefix, count the rest omitted, report the kept
rendering's estimate, and the next item would have passed the cap; a cap of 1 keeps nothing, omits
both and estimates 0, and `render_chat_evidence` of two items reads `[1] node:T001 — a` and
`[2] diff:x.py — b` on two lines; a malformed second item and the scope `project` are refused
with their messages; two builds of the same task's set are equal and name scope, subject and
nothing omitted; and building a set writes no file under `tmp_path`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f038-r1-block.md` := this block, and `.agent/authored/f038-r1-plan.md` and
  `.agent/authored/f038-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F038 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 70. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f038-r1-claim.diff` := claim.diff.
  Subject: `F038 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 182.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F038 R1 C2: claim F038, move F286 behind it, book F036 R9, register R-1091, record D1 and D2`
  Expected by `git show --numstat` (insertions and deletions): 15/15 context.md, 77/0
  decisions.md, 27/22 live_review.md, 20/13 plan.md, 1/1 STATUS.md, 2/0 T2_F286.md.

C3 — THE REPAIR: S1, its two tests and S7's line, which is the only change to the ledger.
  Subject: `F038 R1 C3: read minted task runs in the diff view and the final verifier (R-1091)`

C4 — THE CODE: `packages/orchestration/chat_evidence.py` and S6's line.
  Subject: `F038 R1 C4: collect a task's chat evidence and compose it under the token cap`

C5 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_evidence.py` and your mutation tool
  (G5) saved as `.agent/authored/f038-r1-mutations.py`.
  Subject: `F038 R1 C5: test the chat's node evidence and composer, add the mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f038-grounded-chat`. Do NOT create a pull request: the branch
  opens one at F038's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b, C5a and C5b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F286.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `.agent/context.md`,
   `packages/orchestration/diff_view_source.py`, `packages/orchestration/final_verifier.py`,
   `tests/orchestration/test_diff_view_source.py`, `tests/orchestration/test_final_verifier.py`,
   `packages/orchestration/chat_evidence.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_chat_evidence.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only fec08a5b9` at the branch tip after C6. Do NOT touch anything
   under `apps/`, any other file under `packages/`, `tests/orchestration/import_reachability_allowlist.txt`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `docs/roadmap/design/grounded-chat-spec.md` or `docs/roadmap/features/T5_F038.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2377956 | 220036983718a6da8b7f9363d80a3fe77f69e97935074df23904189b89f040aa |
 | .agent/live_review.md | 308676 | 7acc4f97b4ed5640e8d62432d3c41927042b22dec7068a6d925ae16bb33f199c |
 | docs/roadmap/STATUS.md | 56619 | 3f0e60fdeb3a5f545a12589754f2ceb74cc1eab2a9216f91de8bf01850ee13c1 |
 | docs/roadmap/features/T2_F286.md | 2399 | 5c6602629e06daacca9e86bf5af3742aa7e74f759a25337559f2f3b6e9a278af |
 | .agent/plan.md | 1233 | 11d6ca8cb63017a9b3b9e8e1b2af28ddcee0a64f03b811bbbf651acb4da1a673 |
 | .agent/context.md | 1657 | c37f18655f13025184c808c0e63685f66a81af13769b8aa68868addb096a7624 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT read with `git show <commit>:<path>`, at
 `fec08a5b9` and at C2 (the reviewer read `[]` and `['R-1091']`); at C2 the ledger has exactly one line reading `## Findings` and exactly
 one reading `## Steps`, and its last non-empty line begins `- R-1091 — High, `; the STATUS lines
 of F036, F038 and F286 at C2 read back with their line numbers, where F038's must read
 `- [~] F038 — Grounded chat & intent dispatch` directly after F036's and before F286's; and
 `git diff --name-only <C1b> <C2>`, which must name exactly the paths of the table above. At C3:
 the ledger at C2 is a byte-exact prefix of the ledger at C3, and what C3 adds is exactly "\n"
 plus one line beginning `Landed: R-1091 — ` and ending in "\n".

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_evidence.py
 packages/orchestration/diff_view_source.py packages/orchestration/final_verifier.py
 tests/orchestration/test_chat_evidence.py tests/orchestration/test_diff_view_source.py
 tests/orchestration/test_final_verifier.py tests/test_no_orphan_modules.py` at C5, with its real
 exit code. Then report, quoted from `git show <C3>` and `git show <C4>`, both changed expressions
 with their comments, the whole of `compose_chat_evidence`, and the event filter of S5 (d).

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_evidence.py tests/cli/test_do_evidence_package.py tests/cli/test_patch_cmd.py tests/orchestration/test_artifact_contract_gate.py tests/orchestration/test_commit_execution_gate.py tests/orchestration/test_diff_view_source.py tests/orchestration/test_failure_wiring.py tests/orchestration/test_final_verifier.py tests/orchestration/test_human_change_evidence.py tests/orchestration/test_hunk_decision_record.py tests/orchestration/test_job_evidence.py tests/orchestration/test_manual_completion_bundle.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_repair_attest.py tests/orchestration/test_result_tour.py tests/orchestration/test_review_final_verifier_reproducible.py tests/orchestration/test_review_package_status.py tests/orchestration/test_round13_evidence_alignment.py tests/orchestration/test_verification_matrix.py tests/ui_server/test_diff_endpoint.py tests/ui_server/test_task_run_rounds.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially over its simulation tree, which carries this round's
 records and the reviewer's own version of the code and tests, and read `1079 passed, 6 skipped`
 at real exit code 0; the six skips are the F252 quarantine in `tests/regression/test_named_bugs.py`
 and stay skipped. Your test count will differ from the reviewer's by what your tests hold: report
 the node count of each new or changed test file by `--collect-only -q`, every `SKIPPED` line, and
 the summary. Then `python3 -m apps.cli.main integrity check --json`: it must read five checks
 `pass` and `high_blockers_open` `fail` with the message `1 open blocker/high: R-1091`, at
 `fail_count` 1 and exit code 1, because R-1091 stays open until the reviewer resolves it. Any
 other reading is red.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_chat_evidence.py tests/orchestration/test_diff_view_source.py
 tests/orchestration/test_final_verifier.py` from the worktree's root after purging its
 `__pycache__` directories, with the worktree's root first on `PYTHONPATH` because the editable
 install otherwise imports the primary checkout's modules, restores the bytes, and prints one line
 per mutation: its label, the exit code, the failed count and the failing node ids. It runs an
 unmutated control first and last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `diff_view_source.py` lists `T<digits>` runs only again;
  m2 `final_verifier.py` lists `T<digits>` runs only again;
  m3 the composer keeps every item whatever the cap;
  m4 an item's text is not redacted;
  m5 the run-log events come oldest first;
  m6 an event naming its task only under `metadata` is not the task's;
  m7 the task is found by a prefix of its id;
  m8 an over-long text is not cut;
  m9 the composer accepts a malformed item;
  m10 the diff is read at job scope instead of the task's;
  m11 a `test_passed` that is neither True nor False reads `failed`;
  m12 `omitted` is always 0.
 Run it: `git worktree add --detach .remedy-wt/f038-r1-mut <C5>`, then
 `python3 -B .agent/authored/f038-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C5 before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r1-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `fec08a5b9` in that
 order (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal
 your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3, C4 and C5 — report what
you measure), every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F038, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1 with the resolution of R-1091, then T001's project scope over the spec's evidence set with
the spec's set-list update. State the open-findings count, 1 (R-1091, landed and awaiting review),
and the operator-questions count, 1.
