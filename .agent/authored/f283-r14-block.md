STEP F283 R14 — T001's catalog half, first group: `init`, `dev`, `memory`, `blocker`, `patch` (D9)

GOAL
Book round 13's PASS and a prose slip, record DECISION F283 D9, then make the first thirteen
commands of the read-only-without-`supports_json` set declare `supports_json` and answer in
the envelope, with a ratchet pinning the commands still missing it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. Read DECISION F283 D9 in this round's decisions payload before C3; it fixes the
payload rule, the lambda rule and the ratchet, and this block does not restate them.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r14-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r14-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt`, `build_selection.py`, `run_sel.py`, `show.py`,
      `build_payloads.py`, `dry_catalog.py`, `d9.txt` and `plan.txt`, which are read-only
      to you. `python3 .remedy-wt/f283-r14-scratch/run_sel.py . <label>` runs selection A
      under `-n auto` and prints its exit code, summary and bad node ids; about three minutes.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops with `$f`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a file in
your scratch directory (written with your file tool) for counting, hashing, copying
(`shutil.copyfile`) and running pytest; use `git -C <dir>` for a worktree.
NEVER USE `git stash` IN ANY FORM, and never check out another commit in the primary
checkout: take each reading after the commit it belongs to.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `dc4c1e60`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r14-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r14-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2702 | 85d001b50a55b0a56c24c39e040916fc25f09d3e075863752002e0964d88a820 |
| decisions.md | 52 | 4173 | 9fdd85b0a7b0409f5bf3c9333d3cef60a3b4e73ad4bdc0274d4a56979d7642c6 |
| plan.md | 37 | 1638 | 05cbd93bc5c81d45e2a173b8491c228baeaa51f520c424ab71928aa7f1da7f94 |
| slips.md | 1 | 413 | ba81abebcc7c2117d04fcf0671debda78a3c5dddf3925b5d2255287e818e152f |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 13 `Gate:` entry; decisions carries DECISION
F283 D9. `slips.md` is an APPEND of one dated line to `.agent/prose_slips.md`. `plan.md` is a
REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r14-block.md` := this block; `.agent/authored/f283-r14-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R14 C1: copy round 14 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/prose_slips.md` += slips.md · `.agent/plan.md` := plan.md
  Subject: `F283 R14 C2: book round 13's PASS and a prose slip, record D9`

C3 — `init run`, `dev status`, `dev smoke-help`, and the ratchet.
  `apps/cli/command_catalog.py`: those three entries declare `supports_json=True`;
  `dev smoke-help` gains `_JSON_OPT`. `apps/cli/commands/dev.py`: `dev smoke-help --json`
  answers `emit_ok(commands=[...])`, the list holding the two command lines its text prints;
  its lambda passes `getattr(args, "json", False)`. `apps/cli/commands/init_cmd.py`: the
  not-a-repository refusal under `--json` answers `fail("not_a_git_repo", <its sentence>,
  json_output=True, exit_code=4)`; the text branch stays byte-for-byte as it is (DECISION
  F283 D7). Success documents of `init run` and `dev status` are NOT changed (D9 (4)).
  SPEC, tests: `tests/test_command_catalog.py` gains a class that (i) computes the set of
  catalog commands with neither `may_mutate_repo` nor `may_execute_commands` nor
  `supports_json` and asserts it EQUALS a module-level frozenset constant naming what is
  left after this commit, and (ii) asserts every catalog command carrying a `--json` arg
  declares `supports_json`. `tests/cli/test_init_cmd.py`: `init --json` outside a git repo
  answers one envelope — `schema_version` 1, `ok` false, `not_a_git_repo`, exit 4. A test
  that `dev smoke-help --json` through the CLI dispatcher answers `ok` true with
  `commands`, in `tests/test_cli_execution_loop_closure.py`.
  Subject: `F283 R14 C3: init, dev status and dev smoke-help declare --json; the ratchet`

C4 — the `memory` group: `memory store`, `card-approve`, `card-reject`, `card-stale`,
  `card-supersede`, `card-contradict`. Catalog: `_JSON_OPT` and `supports_json=True` on each.
  `apps/cli/commands/memory.py`: `_cmd_memory_store` takes `json_output`; under `--json` each
  success answers `emit_ok` — store: `id`, `key`; approve, reject, stale: `id`, `key`, and the
  card's `review_status`, `validity` and `approved` after the change; supersede: `old_id`,
  `new_id`; contradict: `memory_id`, `by_id` (full ids as given, never the `[:8]` the text
  prints). Text branches unchanged. The ratchet constant loses these six.
  SPEC, tests, in `tests/cli/test_memory_cmd.py`: through the CLI dispatcher with `--json`,
  one success envelope per command asserting the keys above, and one `memory_card_not_found`
  envelope for a card command. Replace `TestTheCatalogStillDeclaresWhatItDeclared` — its
  premise ends in this commit — with a test that all six card commands declare
  `supports_json`, and rewrite the module docstring's sentence about the gap to say it closed.
  Subject: `F283 R14 C4: the memory store and card commands answer --json in the envelope`

C5 — `blocker resolve` and the three `patch` commands. Catalog: `_JSON_OPT` and
  `supports_json=True` on `blocker.resolve`, `patch.show`, `patch.approve`, `patch.reject`.
  `blocker.py`: success answers `emit_ok(id=<full id>, reason_code=...)`.
  `patch.py`: the three handlers take `json_output` and pass it to every refusal;
  `patch show`'s two-line not-found refusal becomes ONE `fail("patch_intent_not_found", ...)`
  whose message is both lines joined by `\n`, so its text stays byte-for-byte; `patch show
  --json` answers `emit_ok(job_id=..., intent=<the intent record>, diff_preview=...)`;
  approve and reject answer `emit_ok(intent_id, target_path, risk, state, reason_recorded)`
  with `state` `approved` or `rejected`. Text branches unchanged. The ratchet constant loses
  these four and must then name exactly the twenty D9 leaves to the later groups.
  SPEC, tests: in `tests/cli/test_blocker_cmd.py` and `tests/cli/test_patch_cmd.py`, through
  the CLI dispatcher with `--json`, a success envelope per command asserting its keys, and a
  refusal envelope for `blocker_not_found` and for `patch show`'s `patch_intent_not_found`.
  Two guards pin what this commit changes, and you repair both keeping what they assert:
  `tests/cli/test_job_refusal_envelope.py::TestPatchRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains`
  (the show-intent pair is gone: assert none remains, and correct the class docstring), and
  `tests/cli/test_advertised_commands.py::test_flag_scanner_reports_a_flag_the_command_does_not_declare`,
  which uses `patch approve ... --json` as its example of an undeclared flag — give it a flag
  no command declares, and keep both of its assertions.
  Subject: `F283 R14 C5: blocker resolve and the patch commands answer --json in the envelope`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R14 C6: rewrite handoff for round 14`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the five `.agent/authored/f283-r14-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`,
   `.agent/plan.md`, `.agent/handoff.md`, `apps/cli/command_catalog.py`,
   `apps/cli/commands/init_cmd.py`, `apps/cli/commands/dev.py`,
   `apps/cli/commands/memory.py`, `apps/cli/commands/blocker.py`,
   `apps/cli/commands/patch.py`, `tests/test_command_catalog.py`,
   `tests/cli/test_init_cmd.py`, `tests/test_cli_execution_loop_closure.py`,
   `tests/cli/test_memory_cmd.py`, `tests/cli/test_blocker_cmd.py`,
   `tests/cli/test_patch_cmd.py`, `tests/cli/test_job_refusal_envelope.py`,
   `tests/cli/test_advertised_commands.py`. Report the set you measure. Nothing under
   `packages/` or `docs/`, no `README.md`, no `scripts/`, no `apps/cli/json_envelope.py`,
   no `apps/cli/grouped.py`, and none of `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`.
4. EVERY COMMIT from C3 on leaves selection A at zero failed and zero errors: run
   `run_sel.py` after C3, after C4 and after C5 and report all three readings.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r14-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r14-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `dc4c1e60`:
     `.agent/live_review.md` (514680) plus ledger.md, the reviewer composed 517382;
     `.agent/decisions.md` (1819599) plus decisions.md, 1823772;
     `.agent/prose_slips.md` (361415) plus slips.md, 361828.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R13 — ` 1. Open set by distinct
     id via `open_finding_ids` from `scripts/rotate_live_review.py` at `dc4c1e60` and at
     C2: the reviewer measured 24 and 24, ADDED empty, REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3, C4 and C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions, and the
 derived set (D9's rule, computed by importing `CATALOG`) as a sorted list after each; after
 C5 it must be exactly the twenty D9 leaves to the later groups. At C5 report
 `python3 .remedy-wt/f283-r6-scratch/pairs.py patch.py init_cmd.py`'s summary lines (the
 reviewer read `patch.py exits 4 mechanical 2 flagged 1 unflagged 1` and `init_cmd.py exits
 1 mechanical 0 flagged 0 unflagged 0` at `dc4c1e60`). List every token the round's `fail(`
 and `emit_error(` calls introduce or reuse, each with its `git grep -c` count over
 `apps/cli/` at `dc4c1e60`. `git diff --name-only dc4c1e60 <C5> -- packages/` must print
 nothing.

G4 THE SELECTION — `.remedy-wt/f283-r14-scratch/selection.txt` (148 paths, `-n auto`).
 The reviewer read at `dc4c1e60`: `5702 passed, 8 skipped`, exit 0. After C3, C4 and C5:
 zero failed and zero errors; the passed count may only rise. Then `python3 -m ruff check`
 over every `.py` path the round touched, and `python3 -m apps.cli.main integrity check
 --json`, all five checks `pass`. `python3 -m pytest tests/cli/test_golden_path.py -q`
 once after C5. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed.
 Run `tests/test_command_catalog.py`, `tests/cli/test_init_cmd.py`,
 `tests/cli/test_memory_cmd.py`, `tests/cli/test_blocker_cmd.py` and
 `tests/cli/test_patch_cmd.py` UNMUTATED first and report it (exit 0). Then each mutation
 alone, reverted before the next, over those five files, reporting the summary line, the
 exit code and the failing test names:
 (a) `card-approve`'s success prints its text line even under `--json` — C4's
     card-approve envelope test must fail.
 (b) `patch show`'s not-found refusal passes `json_output=False` — C5's `patch show`
     refusal envelope test must fail.
 (c) `blocker.resolve`'s catalog entry drops `supports_json=True`, keeping its `--json` arg
     — both halves of C3's ratchet class must fail.
 (d) `init`'s `--json` not-a-repository branch prints the old `{"error": ...}` document
     again — C3's init envelope test must fail.
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
Session section reads SESSION 4 of feature F283, round 14, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 14, then the catalog half's second group as `.agent/plan.md` lists it.
State the open-findings count, 24 after this round, and the operator-questions count, 0.
