STEP F283 R15 — T001's catalog half, second group: `decision`, `job plan`, `brain` (D9)

GOAL
Book round 14's PASS and a prose slip, pin the two properties round 14's review found
unpinned, then make `decision resolve`, `decision explain`, `job plan` and the seven `brain`
commands declare `supports_json` and answer in the envelope, shrinking the ratchet to the
`ui` and `project` commands.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. DECISION F283 D9 (in `.agent/decisions.md`, appended by round 14) fixes the
payload rule: success through `emit_ok`, no `version` key, a report string under `text`
beside the ids, behaviour other than output unchanged, warnings on stderr, one envelope on
stdout. DECISION F283 D7 fixes an unprefixed text refusal in a `--json` handler: the
envelope under `--json`, the text kept byte-for-byte.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r15-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r15-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt`, `build_selection.py`, `run_sel.py`, `dry_catalog.py`,
      `build_payloads.py`, `plan.txt`, `rev14.raw` and `rev14.out`, which are read-only to
      you. `python3 .remedy-wt/f283-r15-scratch/run_sel.py . <label>` runs selection A
      under `-n auto` and prints its exit code, summary and bad node ids; about three minutes.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a
file in your scratch directory (written with your file tool) for counting, hashing, copying
(`shutil.copyfile`) and running pytest; use `git -C <dir>` for a worktree.
NEVER USE `git stash` IN ANY FORM, and never check out another commit in the primary
checkout: take each reading after the commit it belongs to. Draft and commit one commit's
change at a time; do not pre-edit files belonging to a later commit.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `dfce6076`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r15-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r15-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 3399 | 959dfcf5ee3186b3ba7d64024f9a28fcce0e04293cfb72335d7370f698059870 |
| plan.md | 35 | 1537 | 5c68196e44ad2359a590f140a05d23aac0de69cae40715e9a7f9723193b8d1e5 |
| slips.md | 1 | 657 | aac50187368c6ff2258fe1b7c7d04bdf0ce71997e0fe38fba5008095aef2d35f |

`ledger.md` is an APPEND beginning with the single newline that separates records; it
carries the round 14 `Gate:` entry. `slips.md` is an APPEND of one dated line to
`.agent/prose_slips.md`. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C7, in this order.

C1 — `.agent/authored/f283-r15-block.md` := this block; `.agent/authored/f283-r15-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R15 C1: copy round 15 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/prose_slips.md` += slips.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R15 C2: book round 14's PASS and a prose slip`

C3 — THE TWO PINS, tests only. In `tests/cli/test_blocker_cmd.py`, `blocker resolve --json`
  with a stop id longer than eight characters answers that FULL id in `id`. In
  `tests/cli/test_patch_cmd.py`, `patch show` without `--json` on a missing intent writes
  exactly the two old stderr lines — `Error: patch intent '<id>' not found in job <job>.` and
  `Use 'remedy patch list <job_id>' to see available intent IDs.` — and exits 1.
  Subject: `F283 R15 C3: pin blocker resolve's full id and patch show's text refusal`

C4 — the `decision` group. Catalog: `_JSON_OPT` and `supports_json=True` on
  `decision.resolve` and `decision.explain`. `apps/cli/commands/decision.py`: both handlers
  take `json_output` (keyword-only, default False) and pass it to every refusal they reach,
  `_load_job_events` and `_create_mission_for_job` included; `_create_mission_for_job`
  prints its three lines only in text mode and hands the mission back to its caller.
  `decision explain --json` answers `emit_ok(job_id=..., text=<the explanation>)`.
  `decision resolve --json` answers ONE envelope per success, always with `decision_id`,
  `job_id` and `outcome`: `sr:` → `outcome` `resolved`, `stop_id`, `reason_code`; a task
  decision → `answered`, `answer`, `cross_references`, `follow_up_mission` (the id or null),
  `next_command` (the resume line it prints); `plan:` approve → `approved`, `answers` (a list
  of objects with `id`, `source`, `answer`), `assumption_log`, `mission_id` (null without
  `--as-mission`); `plan:` reject → `rejected`, `next_step`; `proposal:` → `approved`,
  `rejected` or `deferred`, with `task_id`. The derived-decision refusal at the end of the
  handler answers `fail("decision_not_resolvable", <its two lines joined by \n>,
  json_output=True)` under `--json` while its text branch keeps both lines byte-for-byte
  (D7) — shape it with the `sys.exit(1)` after an `if json_output: ... else: <the two
  prints>` so no print-then-exit pair survives. Text branches unchanged. The ratchet loses
  these two.
  SPEC, tests, in `tests/cli/test_decision_cmd.py`, `tests/cli/test_decision_answers.py` or
  `tests/cli/test_plan_approval.py`: through the CLI dispatcher with `--json`, one success
  envelope for `decision explain` and for each `decision resolve` outcome family above
  (`resolved`, `answered`, plan `approved`, plan `rejected`, one proposal outcome) asserting
  its keys, and refusal envelopes for `decision_not_found` and `decision_not_resolvable`.
  Repair `tests/cli/test_job_refusal_envelope.py::TestDecisionsRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains`
  — the derived-decision pair is gone: assert none remains, and correct the class docstring.
  Subject: `F283 R15 C4: decision resolve and decision explain answer --json in the envelope`

C5 — `job plan`. Catalog: `_JSON_OPT` and `supports_json=True` on `job.plan`.
  `apps/cli/commands/job.py::_cmd_plan_job_local` takes `json_output` and passes it to every
  refusal; success answers `emit_ok(job_id=..., changed=<bool>, model=..., task_count=...,
  log_path=...)` plus `elapsed_ms` when it changed the plan. Text branches unchanged. The
  ratchet loses `job.plan`.
  SPEC, tests, in `tests/orchestration/test_structured_planner_cli.py`: through the CLI
  dispatcher with `--json`, a success envelope and a `planner_failed` refusal envelope.
  Subject: `F283 R15 C5: job plan answers --json in the envelope`

C6 — the seven `brain` commands. Catalog: `_JSON_OPT` and `supports_json=True` on
  `brain.view`, `brain.trust`, `brain.timeline`, `brain.cockpit`, `brain.constitution`,
  `brain.open`, `brain.export-viewer`. `apps/cli/commands/brain.py`: each of their handlers
  and `_prepare_viewer` take `json_output` and pass it to every refusal. Success under
  `--json`: `view` → `job_id`, `index_path`, `node_count`, `edge_count`, `detail_count`;
  `trust`, `cockpit`, `constitution` → `job_id`, `text`; `timeline` → `job_id`,
  `event_count`, `text` (its no-events line when there are none); `open` → `job_id`,
  `index_path`, `opened` (whether an opener was launched without error; the opener still
  runs); `export-viewer` → `job_id`, `out_dir`, `files` (the three file names it prints).
  Text branches unchanged; warnings stay on stderr. The ratchet must then name exactly the
  ten `ui` and `project` commands.
  SPEC, tests, in `tests/test_brain_viewer.py`: through the CLI dispatcher with `--json`, a
  success envelope per command asserting its keys (`timeline` on a job with no events among
  them), and one `job_not_found` refusal envelope.
  Subject: `F283 R15 C6: the brain report and viewer commands answer --json in the envelope`

C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R15 C7: rewrite handoff for round 15`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the four `.agent/authored/f283-r15-*` copies,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/decision.py`,
   `apps/cli/commands/job.py`, `apps/cli/commands/brain.py`,
   `tests/test_command_catalog.py`, `tests/cli/test_blocker_cmd.py`,
   `tests/cli/test_patch_cmd.py`, `tests/cli/test_decision_cmd.py`,
   `tests/cli/test_decision_answers.py`, `tests/cli/test_plan_approval.py`,
   `tests/cli/test_job_refusal_envelope.py`,
   `tests/orchestration/test_structured_planner_cli.py`, `tests/test_brain_viewer.py`.
   Report the set you measure. Nothing under `packages/` or `docs/`, no `README.md`, no
   `scripts/`, no `apps/cli/json_envelope.py`, no `apps/cli/grouped.py`, and none of
   `.agent/decisions.md`, `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`.
4. EVERY COMMIT from C3 on leaves selection A at zero failed and zero errors: run
   `run_sel.py` after C3, C4, C5 and C6 and report all four readings.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C7 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r15-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r15-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `dfce6076`:
     `.agent/live_review.md` (517382) plus ledger.md, the reviewer composed 520781;
     `.agent/prose_slips.md` (361828) plus slips.md, 362485.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R14 — ` 1. Open set by distinct
     id via `open_finding_ids` from `scripts/rotate_live_review.py` at `dfce6076` and at
     C2: the reviewer measured 24 and 24, ADDED empty, REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 to C6 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions, and the
 derived set (D9's rule, computed by importing `CATALOG` from each commit's own tree) as a
 sorted list after C4, C5 and C6; after C6 it must be exactly the five `ui` and five
 `project` commands. At C6 report
 `python3 .remedy-wt/f283-r6-scratch/pairs.py decision.py brain.py job.py`'s summary lines
 (the reviewer read `decision.py exits 1 mechanical 1 flagged 0 unflagged 1`, `brain.py
 exits 0 mechanical 0 flagged 0 unflagged 0` and `job.py exits 2 mechanical 0 flagged 0
 unflagged 0` at `dfce6076`). List every token the round's `fail(` and `emit_error(` calls
 introduce or reuse, each with its `git grep -c` count over `apps/cli/` at `dfce6076`.
 `git diff --name-only dfce6076 <C6> -- packages/` must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r15-scratch/selection.txt` (197 paths, `-n auto`).
 The reviewer read at `dfce6076`: `8452 passed, 10 skipped`, exit 0. After C3, C4, C5 and
 C6: zero failed and zero errors; the passed count may only rise. Then `python3 -m ruff
 check` over every `.py` path the round touched, and `python3 -m apps.cli.main integrity
 check --json`, all five checks `pass`. `python3 -m pytest tests/cli/test_golden_path.py
 -q` once after C6. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C6, never committed.
 Run `tests/cli/test_blocker_cmd.py`, `tests/cli/test_patch_cmd.py`,
 `tests/cli/test_decision_cmd.py`, `tests/cli/test_decision_answers.py`,
 `tests/cli/test_plan_approval.py`, `tests/orchestration/test_structured_planner_cli.py`
 and `tests/test_brain_viewer.py` UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, over those seven files, reporting the summary
 line, the exit code and the failing test names:
 (a) `blocker resolve`'s envelope carries `sr.id[:8]` as `id` — C3's full-id pin must fail.
 (b) `patch show`'s not-found message joins its two lines with a space instead of `\n` —
     C3's text-refusal pin must fail.
 (c) the derived-decision refusal passes `json_output=False` under `--json` — C4's
     `decision_not_resolvable` envelope test must fail.
 (d) the `plan:` approve branch prints its text even under `--json` — C4's plan-approved
     envelope test must fail.
 (e) `job plan`'s `planner_failed` refusal passes `json_output=False` — C5's refusal
     envelope test must fail.
 (f) `brain timeline`'s no-events branch prints its line even under `--json` — C6's
     no-events envelope test must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain` empty; `git log --oneline -n 9`;
 `git worktree list` (the primary checkout alone); `git stash list`'s first line unchanged
 from its reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the
 handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 4 of feature F283, round 15, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 15, then the catalog half's last group as `.agent/plan.md` lists it.
State the open-findings count, 24 after this round, and the operator-questions count, 0.
