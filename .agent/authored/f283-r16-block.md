STEP F283 R16 — T001's catalog half, last group: `ui` and `project`; the read-only set empty (D9)

GOAL
Book round 15's PASS and a prose slip, pin what round 15's review found unpinned and narrow
one key, then make the five `ui` and five `project` commands declare `supports_json` and
answer in the envelope, so the read-only-without-`supports_json` set is empty and the
ratchet asserts it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/`, `packages/` and `tests/` is yours, written to
the SPEC in each commit. DECISION F283 D9 (search `.agent/decisions.md` for `DECISION F283
D9`; never read that file whole) fixes the payload rule: success through `emit_ok`, no
`version` key, behaviour other than output unchanged, warnings on stderr, one envelope on
stdout, and `ui start` printing its one envelope once the server is bound. DECISION F283 D7
fixes an unprefixed text refusal in a `--json` handler: the envelope under `--json`, the
text kept byte-for-byte, shaped as `if json_output: fail(...)` / `else: <the prints>` with
the `sys.exit(...)` AFTER that `if`/`else`, so no print-then-exit pair survives.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r16-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r16-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file
      the reviewer put there before C1, which is read-only to you.
      `python3 .remedy-wt/f283-r16-scratch/run_sel.py . <label>` runs selection A under
      `-n auto` and prints its exit code, summary and bad node ids; about four minutes.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a
file in your scratch directory (written with your file tool) for counting, hashing, copying
(`shutil.copyfile`) and running pytest; use `git -C <dir>` for a worktree.
NEVER USE `git stash` IN ANY FORM, and never check out another commit in the primary
checkout: take each reading after the commit it belongs to. Draft and commit one commit's
change at a time; do not pre-edit files belonging to a later commit. No test may launch a
real browser, opener or blocking server: mock them.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `f6527092`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r16-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r16-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 3705 | d4af305fd4d4850dafb69c5d5479e96ec6f5722aca1916fa40f40bf46934c2ad |
| plan.md | 34 | 1442 | 840a502b8cfb79fc0755a263563f05f32ada009d3bac7ecee2d3fb10ac6df424 |
| slips.md | 1 | 504 | 4a9043ea1e8c2f0216d789b27a36bd2568b017b8a545d9942fac17975380105b |

`ledger.md` is an APPEND beginning with the single newline that separates records; it
carries the round 15 `Gate:` entry. `slips.md` is an APPEND of one dated line to
`.agent/prose_slips.md`. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r16-block.md` := this block; `.agent/authored/f283-r16-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R16 C1: copy round 16 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/prose_slips.md` += slips.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R16 C2: book round 15's PASS and a prose slip`

C3 — THE PIN AND THE NARROWED KEY. `apps/cli/commands/decision.py`: the `answered`
  envelope's `next_command` becomes the command alone, `remedy job resume <job> --json`,
  while the text line keeps its `Resume the run: ` prefix byte-for-byte. Tests: the
  `answered` envelope test asserts that exact `next_command` value; in
  `tests/cli/test_decision_cmd.py`, `decision resolve` on a derived decision WITHOUT
  `--json` writes exactly its two old stderr lines and exits 1.
  Subject: `F283 R16 C3: pin the derived-decision text refusal; next_command is the command`

C4 — the five `project` commands. Catalog: `_JSON_OPT` and `supports_json=True` on
  `project.create`, `project.attach-repo`, `project.attach-job`, `project.attach`,
  `project.adopt`. `apps/cli/commands/project.py`: their handlers take `json_output`
  (keyword-only, default False) and pass it to every refusal. Success under `--json`:
  `create` → `project_id`, `name`, `slug`; `attach-repo` → `project_id`, `repo`,
  `changed`; `attach-job` → `project_id`, `job_id`, `added`; `attach` → `project_id`,
  `slug`, `old_repo`, `new_repo`, `changed` (its text branch keeps printing the raw
  document it prints today); `adopt` → `job_id`, `project_id`, `slug`. `_cmd_project_attach_repo`'s
  unprefixed `(ProjectNotFoundError, InvalidProjectSelectorError)` refusal answers under
  `--json` exactly as `_cmd_project_current`'s identical branch already does (the same two
  tokens by exception class, exit 3), in D7's shape. Text branches unchanged. The ratchet
  loses these five.
  SPEC, tests, in `tests/cli/test_project_current.py` or
  `tests/orchestration/test_project_resolution.py`: through the CLI dispatcher with
  `--json`, a success envelope per command asserting its keys and one refusal envelope for
  `project attach`'s selector branch. Repair
  `tests/cli/test_job_refusal_envelope.py::TestProjectRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains`
  to assert none remains, rename it `test_no_unflagged_site_remains`, and correct its
  class docstring; its flagged count stays 1. In the same file rename
  `TestDecisionsRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains`, whose
  assertion round 15 already made `unflagged == []`, to `test_no_unflagged_site_remains`.
  Subject: `F283 R16 C4: the project create and attach commands answer --json in the envelope`

C5 — the five `ui` commands; the set is empty. Catalog: `_JSON_OPT` and
  `supports_json=True` on `ui.start`, `ui.latest`, `ui.status`, `ui.stop`, `ui.open`.
  `apps/cli/commands/ui.py`: handlers take `json_output`. `latest` → `url`, `job_id`,
  `pid`; `status` → `sessions` (each live one's `job_id`, `port`, `pid`, `url`) and `dead`
  (the archived ones with `ended_at` under `--all`, else an empty list); `stop` →
  `stopped` and `failed` (each entry's `pid` and `job_id`, `failed` adding `error`);
  `open` → `url`, `job_id`. `latest`'s and `open`'s unprefixed no-session refusals answer
  `ui_session_not_found` under `--json`, text kept, in D7's shape. `ui start` passes
  `json_output` into `packages/orchestration/ui_server.py::start_ui_server`, which gains
  it keyword-only (default False): under `--json` its host refusal answers
  `host_not_allowed` and its job refusal `job_not_found` (a 404) or `invalid_job_id` (a
  400), both through `fail()` imported inside the function from `apps.cli.json_envelope`,
  as that module already imports `apps.cli.command_catalog` inside a function; once bound
  it prints `emit_ok(url=..., host=..., port=..., job_id=..., pid=..., info_file=...)` in
  place of its two prose lines, flushes stdout, and then serves. The text path is
  unchanged, and keep the literal `("127.0.0.1", "localhost", "::1")` and the absence of
  `0.0.0.0` that `tests/ui_server/` source guards pin. The ratchet class now asserts the
  derived set is EMPTY and the constant is deleted (D9 (6)).
  SPEC, tests, in `tests/ui_server/test_live_state.py`: through the CLI dispatcher with
  `--json`, a success envelope for `latest`, `status`, `stop` and `open`, a
  `ui_session_not_found` envelope, and `ui start --json` answering its bound envelope
  with `serve_forever` patched to return and the browser opener mocked.
  Subject: `F283 R16 C5: the ui commands answer --json in the envelope; the read-only set is empty`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R16 C6: rewrite handoff for round 16`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the four `.agent/authored/f283-r16-*` copies,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/decision.py`,
   `apps/cli/commands/project.py`, `apps/cli/commands/ui.py`,
   `packages/orchestration/ui_server.py`, `tests/test_command_catalog.py`,
   `tests/cli/test_decision_cmd.py`, `tests/cli/test_decision_answers.py`,
   `tests/cli/test_project_current.py`, `tests/orchestration/test_project_resolution.py`,
   `tests/cli/test_job_refusal_envelope.py`, `tests/ui_server/test_live_state.py`.
   Report the set you measure. Nothing else under `packages/`, nothing under `docs/`, no
   `README.md`, no `scripts/`, no `apps/cli/json_envelope.py`, no `apps/cli/grouped.py`,
   and none of `.agent/decisions.md`, `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`.
4. EVERY COMMIT from C3 on leaves selection A at zero failed and zero errors: run
   `run_sel.py` after C3, C4 and C5 and report all three readings.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r16-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r16-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `f6527092`:
     `.agent/live_review.md` (520781) plus ledger.md, the reviewer composed 524486;
     `.agent/prose_slips.md` (362485) plus slips.md, 362989.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R15 — ` 1. Open set by distinct
     id via `open_finding_ids` from `scripts/rotate_live_review.py` at `f6527092` and at
     C2: the reviewer measured 24 and 24, ADDED empty, REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3, C4 and C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions, and the
 derived set (D9's rule, computed by importing `CATALOG` from each commit's own tree) as a
 sorted list after C4 and C5; after C5 it must be empty. At C5 report
 `python3 .remedy-wt/f283-r6-scratch/pairs.py project.py ui.py decision.py`'s summary
 lines (the reviewer read `project.py exits 2 mechanical 2 flagged 1 unflagged 1`,
 `ui.py exits 2 mechanical 2 flagged 0 unflagged 2` and `decision.py exits 1 mechanical 0
 flagged 0 unflagged 0` at `f6527092`). List every token the round's `fail(` and
 `emit_error(` calls introduce or reuse, each with its `git grep -c` count over `apps/`
 and `packages/` at `f6527092`. `git diff --name-only f6527092 <C5> -- packages/` prints
 `packages/orchestration/ui_server.py` alone.

G4 THE SELECTION — `.remedy-wt/f283-r16-scratch/selection.txt` (285 paths, `-n auto`).
 The reviewer read at `f6527092`: `10983 passed, 13 skipped`, exit 0. After C3, C4 and C5:
 zero failed and zero errors; the passed count may only rise. Then `python3 -m ruff check`
 over every `.py` path the round touched, and `python3 -m apps.cli.main integrity check
 --json`, all five checks `pass`. `python3 -m pytest tests/cli/test_golden_path.py -q`
 once after C5. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed.
 Run `tests/test_command_catalog.py`, `tests/cli/test_decision_cmd.py`,
 `tests/cli/test_decision_answers.py`, `tests/cli/test_project_current.py`,
 `tests/orchestration/test_project_resolution.py` and `tests/ui_server/test_live_state.py`
 UNMUTATED first and report it (exit 0). A worktree has no built UI, so if the unmutated
 control is not exit 0, report its bad node ids and judge each mutation only by the tests
 it adds to that set. Then each mutation alone, reverted before the next, over those six
 files, reporting the summary line, the exit code and the failing test names:
 (a) `next_command` carries the `Resume the run: ` prefix again — C3's exact-value
     assertion must fail.
 (b) the derived-decision text's first line is reworded — C3's text pin must fail.
 (c) `project attach`'s selector refusal passes `json_output=False` — C4's refusal
     envelope test must fail.
 (d) `project create --json` prints the bare id instead of the envelope — C4's create
     envelope test must fail.
 (e) `ui latest`'s no-session refusal passes `json_output=False` — C5's
     `ui_session_not_found` envelope test must fail.
 (f) `start_ui_server` prints its two prose lines even under `--json` — C5's `ui start`
     envelope test must fail.
 (g) `ui.status`'s catalog entry drops `supports_json=True`, keeping its `--json` arg —
     the ratchet class must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (the primary checkout alone); `git stash list`'s first line unchanged
 from its reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the
 handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 4 of feature F283, round 16, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 16, then T002 as `.agent/plan.md` lists it. State the open-findings count,
24 after this round, and the operator-questions count, 0.
