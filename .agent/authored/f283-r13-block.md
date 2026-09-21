STEP F283 R13 — `remedy runtime` refuses through `fail()`, keyed on its error class (D8)

GOAL
Book round 12's PASS and record DECISION F283 D8, then replace `runtime_cmd.py`'s local
`_fail` with refusals through `fail()` whose token is keyed on the error class, and make the
module's four result-shaped failure exits answer one envelope under `--json`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. Read DECISION F283 D8 in this round's decisions payload before C3; it fixes
the helper, the token table and the payload rule, and this block does not restate them.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r13-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r13-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt`, `selection_serial.txt`, `build_selection.py` and
      `run_sel.py`, which are read-only to you. `run_sel.py <dir> <label>` runs selection
      A under `-n auto` and selection B (the five `tests/runtimes/` suites) SERIALLY —
      `tests/runtimes/test_supervisor_portability.py` flakes under xdist — and prints each
      exit code, summary and bad node ids. It takes about nine minutes.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a file in your
scratch directory (written with your file tool) for counting, hashing, copying
(`shutil.copyfile`) and running pytest; use `git -C <dir>` for a worktree.
NEVER USE `git stash` IN ANY FORM, and never check out another commit in the primary
checkout: take each reading after the commit it belongs to.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `2ac999da`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r13-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r13-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 33 | 2560 | 6252d54e5af0222b387cf36105d6d947c6417f76d6eadba78ebf571ea0b35511 |
| ledger.md | 2 | 3391 | 5677bff91ed0979ac370bc016d34ed21328d5ea908b60e8003f37c45fee79239 |
| plan.md | 33 | 1311 | b755761d22094dc38d0d150954fa67fe14425cd58f7cccd5bb92a72e974a2195 |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 12 `Gate:` entry; decisions carries
DECISION F283 D8. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C5, in this order.

C1 — `.agent/authored/f283-r13-block.md` := this block; `.agent/authored/f283-r13-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R13 C1: copy round 13 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R13 C2: book round 12's PASS, record D8`

C3 — `apps/cli/commands/runtime_cmd.py`: `_fail` deleted; `RUNTIME_ERROR_TOKENS` and
  `_runtime_refusal` as D8 states them, the helper's return type `NoReturn`; every former
  `_fail` call becomes a `_runtime_refusal` call with the same message, exit code, class
  and payload keys. Update the module docstring to name the envelope and the tokens beside
  the exit-code contract. SPEC, tests: repair every assertion that read the old sentence
  out of `error` (at `2ac999da` they sit in `tests/runtimes/test_runtime_cli_process_boundary.py`,
  `tests/runtimes/test_runtime_lifecycle_safety.py`, `tests/runtimes/test_runtime_state_machine.py`
  and `tests/runtimes/test_supervisor_portability.py`) to read `message`, keeping what they
  assert. In `tests/cli/test_runtime_cmd.py`, `serve --json` and `probe --json` on a
  directory with no runtime spec each answer one envelope — `schema_version` 1, `ok` false,
  `runtime_config_error`, `error_class` `config`, exit 2 — and one test asserts that every
  value of `RUNTIME_ERROR_TOKENS` is distinct and every class the module passes is a key.
  In `tests/cli/test_job_refusal_envelope.py`, a ratchet: `runtime_cmd.py` defines no
  `_fail`, and no `print(..., file=sys.stderr)` + exit pair survives except those the
  result-shaped exits keep in their text branches (count them and name why).
  Subject: `F283 R13 C3: runtime refusals answer through fail(), keyed on error_class (D8)`

C4 — the four result-shaped failure exits D8 names — the one-shot probe's cleanup
  survivors (`runtime_stop_failed`), the one-shot probe that did not reach readiness (its
  result's class through the table), the served runtime whose health URL failed
  (`runtime_not_ready`) and `stop` that did not stop (`runtime_stop_failed` when survivors
  remain, `runtime_state_error` otherwise, the message its `stop_error` or `reason`) —
  answer ONE envelope under `--json` by D8's payload rule; text branches unchanged, exit
  codes unchanged. SPEC, tests: repair the assertions that read these outputs' old shape;
  `tests/cli/test_runtime_cmd.py::...::test_a_probe_timeout_exits_4` or a sibling asserts
  the probe's envelope (`runtime_not_ready`, `error_class` `ready`, exit 4), and
  `test_stop_never_kills_a_reused_pid` or a sibling asserts `stop --json`'s envelope token
  at exit 5 — name the tests.
  Subject: `F283 R13 C4: runtime result-shaped failures answer one envelope under --json`

C5 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R13 C5: rewrite handoff for round 13`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the four `.agent/authored/f283-r13-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/commands/runtime_cmd.py`, `tests/cli/test_runtime_cmd.py`,
   `tests/cli/test_job_refusal_envelope.py`, and the five `tests/runtimes/` files
   `selection_serial.txt` lists. Report the set you measure. Nothing under `packages/`
   (`packages/runtimes/` included — `error_class` is its contract) or `docs/`, no
   `README.md`, no `scripts/`, no `apps/cli/json_envelope.py`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves BOTH selections at zero failed: run `run_sel.py` after C3
   and after C4 and report all four readings. A node of
   `test_supervisor_portability.py` that fails once serially is re-run alone three times
   and all three readings are reported; it counts as red unless all three pass.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C5 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r13-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r13-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `2ac999da` (504225 bytes)
     plus ledger.md; the reviewer composed 507616. `.agent/decisions.md` (1806637)
     plus decisions.md; the reviewer composed 1809197.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R12 — ` 1. Open set by distinct
     id via `open_finding_ids` from `scripts/rotate_live_review.py` at `2ac999da` and at
     C2: the reviewer measured 22 and 22, ADDED empty, REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 and C4 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C4
 report the count of lines holding `_fail(` and holding `_runtime_refusal(` in
 `runtime_cmd.py` (the reviewer read 27 lines holding `_fail(` at `2ac999da`, the
 definition included; at C4 it must read 0) and
 `python3 .remedy-wt/f283-r6-scratch/pairs.py runtime_cmd.py`'s summary line (the reviewer
 read `exits 5 mechanical 0` at `2ac999da`). List every
 token C3 and C4 use, each confirmed absent from `fail("` over `apps/cli/` before its
 commit. `git diff --name-only 2ac999da <C4> -- packages/` must print nothing.

G4 THE SELECTIONS — `.remedy-wt/f283-r13-scratch/selection.txt` (109 paths, `-n auto`) and
 `selection_serial.txt` (5 paths, serial). Run `python3 .remedy-wt/f283-r13-scratch/run_sel.py
 . <label>` in the primary checkout after C3 and after C4. The reviewer read at
 `2ac999da`: A `4565 passed, 1 skipped`, B `204 passed`, both exit 0. Zero failed and zero
 errors at each; passed counts may only rise. Then `python3 -m ruff check` over every
 `.py` path the round touched, and `python3 -m apps.cli.main integrity check --json`, all
 five checks `pass`. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C4, never committed.
 Run `tests/cli/test_runtime_cmd.py` and `tests/cli/test_job_refusal_envelope.py`
 UNMUTATED first and report it (exit 0). Then each mutation alone, reverted before the
 next, over those two files, reporting the summary line, the exit code and the failing
 test names:
 (a) `RUNTIME_ERROR_TOKENS["config"]` changed — C3's config envelope tests must fail.
 (b) `_runtime_refusal` stops passing `error_class` in the payload — C3's tests asserting
     `error_class` must fail.
 (c) the one-shot probe's not-ready failure passes `json_output=False` — C4's probe
     envelope test must fail.
 (d) `stop`'s failure envelope token changed — C4's stop envelope test must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain` empty; `git log --oneline -n 7`;
 `git worktree list` (primary plus the three `remedy/job-*`); `git stash list`'s first line
 unchanged from its reading before C1; the push's real outcome; `gh pr list --state open
 --json number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not
 the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 3 of feature F283, round 13, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 13, then T001's catalog half as `.agent/plan.md` lists it. State the
open-findings count, 22 after this round, and the operator-questions count, 2.
