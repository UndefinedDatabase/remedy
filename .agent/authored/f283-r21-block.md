STEP F283 R21 — T002's sweep: every `--json` command answered under test, and the one gap it found (D13)

GOAL
Book round 20's PASS, correct round 19's verdict token on the record and resolve R-1032, register
R-1033 and R-1034, record DECISION F283 D13, land the sweep and the catalog-to-dispatch parity in
`tests/cli/test_json_contract.py`, and make `stats report --json` answer in the envelope.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors only the RECORD payloads; every change
under `apps/` and `tests/` is yours, written to the SPEC in each commit. DECISION F283 D13, in this
round's decisions payload, IS the SPEC for C3, and finding R-1033, in this round's ledger payload,
IS the SPEC for C4 — read both before you start them. Never read `.agent/decisions.md` whole.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r21-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r21-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1, which is read-only to you.
      `python3 .remedy-wt/f283-r21-scratch/run_sel.py . <label>` runs selection A under `-n auto`
      and prints its exit code, summary and bad node ids; about four minutes. It skips a listed
      path that does not exist yet, so `tests/cli/test_json_contract.py` joins the selection once
      C3 creates it.
      `python3 .remedy-wt/f283-r21-scratch/probe_inproc.py` is the reviewer's dry run of D13's
      success half: it calls the grouped CLI in process for each candidate command and prints the
      exit code, the shape and the seconds. `probe_sweep.py invalid` is the same for the invalid
      half, in subprocesses. Both are references; the test is yours.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`, a
`grep` pattern holding `$`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`; put multi-step code in a scratch file. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. NEVER USE `git stash` IN
ANY FORM, and never check out another commit in the primary checkout: take each reading after the
commit it belongs to. Draft and commit one commit's change at a time. No test may launch a real
browser, opener, provider or blocking server: mock them, and never let a swept command reach one.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `a100a48a`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r21-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.

THE BRANCH TIP IS RED WHEN YOU START, AT EXACTLY ONE TEST:
`tests/orchestration/test_final_audit_evidence.py::TestReviewStateExtraction::test_the_manifest_reads_the_real_ledger_as_the_canonical_reader_does`.
Finding R-1032 in this round's ledger payload registers it against the reviewer's own round 20
payload, and C2 repairs it. No other failure is expected at any reading; report any you see.

PAYLOADS — under `.remedy-wt/f283-r21-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 12 | 11354 | ba64bd98153d99a150ba91848facfcbb859f87e65508c314a9732080a4800412 |
| decisions.md | 53 | 4272 | e941fe11faecf70a86f4616012c7719290c94ce58d623f9d403a5d78b8bd97fa |
| plan.md | 35 | 1512 | 850a578badeab646c381a760ad585d116d997a201238cee7a73b7536ccc3cc6d |
| prose_slips.md | 1 | 303 | 69ab8a6e4f0615f35ec6e0a5ef6d7e0b635da393779292e16810b5376b23e50b |

`ledger.md`, `decisions.md` and `prose_slips.md` are APPENDS; the first two begin with the single
newline that separates records, and `prose_slips.md` is one line that joins a list of lines.
`plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C5, in this order.

C1 — `.agent/authored/f283-r21-block.md` := this block; `.agent/authored/f283-r21-<name>` for each
  payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R21 C1: copy round 21 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/prose_slips.md` += prose_slips.md · `.agent/plan.md` := plan.md
  Subject: `F283 R21 C2: book round 20's PASS, correct round 19's verdict token, register R-1033 and R-1034`

C3 — THE SWEEP, D13, in a NEW `tests/cli/test_json_contract.py`:
  (a) the INVALID half, over every `supports_json` catalog command: the command with one
      unrecognised option and `--json`;
  (b) the SUCCESS half, over the candidate set D13 (1) defines, with the exclusions D13 (3) names
      written as a mapping from command id to its reason;
  (c) both halves assert D13 (2)'s three properties of what the command printed;
  (d) PARITY, D13 (5): every catalog `command_id` has exactly one handler and every handler key is
      a catalog `command_id`.
  Report the candidate count of each half and the wall-clock seconds of the file. The reviewer's
  dry run at `a100a48a` measured 144 invalid candidates and 33 success candidates after the one
  exclusion, and about three seconds for the success half in process.
  Subject: `F283 R21 C3: sweep every --json command's envelope and the catalog-dispatch parity (D13)`

C4 — R-1033, whose registration paragraph in this round's ledger payload carries the SPEC and the
  fix clause: `stats report --json` answers `emit_ok(**document)` where the document is the dict
  `cost_report_json` returns, with every key the old document carried, and the readers of the old
  shape in `tests/cli/test_stats_report.py` change in this same commit. The text branch and
  `cost_report_json_bytes`, which writes a report to disk, are untouched — nothing under
  `packages/` changes. At least one test asserts `schema_version` 1 and `ok` true on a `stats
  report --json` run that HAS a ledger, since an empty data root makes the command refuse before
  it reaches this document.
  Subject: `F283 R21 C4: stats report answers --json success in the envelope (R-1033)`

C5 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and in
  the SAME commit one line appended to `.agent/live_review.md`:
  `Landed: R-1033 — <one line: what changed, and C4's sha>`. That is the worker's mark for a fix
  whose resolution the reviewer has not authored yet; never write a `Done:` paragraph.
  Subject: `F283 R21 C5: rewrite handoff for round 21 and mark R-1033 landed`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the `.agent/authored/f283-r21-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `.agent/handoff.md`, `apps/cli/commands/stats_ledger_cmd.py`,
   `tests/cli/test_json_contract.py`, `tests/cli/test_stats_report.py`,
   `tests/orchestration/import_reachability_allowlist.txt`, and a test file listed in
   `.remedy-wt/f283-r21-scratch/selection.txt` whose guard a commit of this round turns red.
   Report the set you measure. Nothing under `packages/`, nothing else under `apps/`, nothing
   under `docs/`, no root `README.md`, no `scripts/`, and none of `.agent/candidates.md`,
   `.agent/context.md`, `.agent/operator_questions.md`.
4. EVERY COMMIT from C2 on leaves selection A at zero failed and zero errors: run `run_sel.py`
   after C2, C3 and C4 and report all three readings. The tip's one known failure is repaired by
   C2, so the reading after C2 is the first that may be clean and must be.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
8. No swept command may write outside the suite's isolated data root, reach a network or start a
   server: if one does, exclude it BY NAME with its reason, report the exclusion, and say which
   reading showed it.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C5 and the handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f283-r21-*` blob, read with `git show <C1>:<path>`, compared
 byte-for-byte with its source (the block copy against `.remedy-wt/f283-r21-block.md`). One
 reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `a100a48a`: `.agent/live_review.md`
     (543665) plus ledger.md, the reviewer composed 555019; `.agent/decisions.md` (1834490) plus
     decisions.md, 1838762; `.agent/prose_slips.md` (362989) plus prose_slips.md, 363292.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R20 — ` 1, `^Gate: F283 R19 correction — `
     1, `^Done: R-1032 — ` 1, and one `^- R-103[234] — ` line each. Open set by distinct id via
     `open_finding_ids` from `scripts/rotate_live_review.py` at `a100a48a` and at C2: the reviewer
     measured 24 and 26, ADDED `R-1033` and `R-1034`, REMOVED none.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).
 (d) `python3 -m pytest tests/orchestration/test_final_audit_evidence.py -q` after C2: the test
     R-1032 names must pass, and the whole file with it.

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 and C4 report `git diff --name-only <parent>
 <commit>` and `git show --numstat` insertions. Report the two candidate counts and the exclusion
 list your sweep measured, and the node count `python3 -m pytest tests/cli/test_json_contract.py
 --collect-only -q` prints. `git diff --name-only a100a48a <C4> -- packages/` must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r21-scratch/selection.txt`, under `-n auto`. The reviewer read
 at `a100a48a`: `1 failed, 11752 passed, 13 skipped`, exit 1, over 308 paths, the one failure being
 R-1032's. After C2, C3 and C4: zero failed and zero errors. Then `python3 -m ruff check` over
 every `.py` path the round touched, and `python3 -m apps.cli.main integrity check --json`, all
 five checks `pass`. `python3 -m pytest tests/cli/test_golden_path.py -q` once after C4. DO NOT
 run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C4, never committed. The files:
 `tests/cli/test_json_contract.py` and `tests/cli/test_stats_report.py`. Run the control first and
 report it; it must exit 0. Then each mutation alone, reverted before the next, reporting the
 summary line, the exit code and the failing test names:
 (a) C4's `emit_ok` in `_cmd_stats_report` prints the old renderer's text again — C4's own test
     must fail.
 (b) in `apps/cli/grouped.py`, `_usage_refusal` prints its prose line instead of calling
     `emit_error` when `--json` is given — the invalid half must fail, and report how many of its
     cases do.
 (c) one command's handler is removed from its module's dispatch table — the parity test must fail
     naming that command id.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain` empty; `git log --oneline -n 8`; `git
 worktree list` (the primary checkout alone); `git stash list`'s first line unchanged from its
 reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the handback —
 the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit changed-files
table with the insertions git MEASURED, every gate's real output and exit code, the sweep's two
candidate counts and its exclusions, the item-status table with one row per C-item, gate and
mutation, the deviations, and the next action. Your Session section reads SESSION 5 of feature
F283, round 21, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
21, then the closure sequence as `.agent/plan.md` lists it. State the open-findings count, 26 after
this round, and the operator-questions count, 0.
