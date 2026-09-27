STEP F029 R11 — THE CLOSING ROUND: book round 10, rotate the ledger, and accept F029 in STATUS with its README pins, then open the pull request

GOAL
Round 10 passed with the package READY_FOR_REVIEW. Close F029 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 10, rotate the finding
ledger, flip F029's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose in the same commit, and open the pull request. No self-use item is consumed: round 9 read
the queue exhausted, so closure precondition 6 reads `self-use NONE (queue exhausted)`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full. You never issue a verdict and never merge. Every
change travels as a payload or is produced by the rotation script; you write only the handback.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`
rather than `cd`, and never `cd` your shell into a worktree. Use `python3 - <<'PY'` for counting,
hashing and copying (`shutil.copyfile`); a heredoc containing a dollar-brace, or a backslash inside
an f-string, is refused or fails, so write such a script to a file under
`.remedy-wt/f029-r11-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f029-r11/`,
`.remedy-wt/f029-r11-sim/` and `.remedy-wt/f029-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f029-subtree-rerun`, `git log --oneline -1`
   `6bf13920`.
3. Measure this block's line count and sha256 (`.remedy-wt/f029-r11/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f029-r11/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 104 | 5842 | c9db1e5739113e5698f54fc24869230e0d221d3faa0c4099feb4329fb1c372a9 |
| closure.diff | 55 | 3865 | 505d699ef7f55ab6c52a49b8aaaf93d947ed5b5952a205bf91ee38be3f570a06 |
| ledger.md | 2 | 2097 | 17589bad400a0af20a95ada580cf2360afa7613ced850f75831364eb39f96709 |
| plan.md | 27 | 873 | 8222fd694c6bb2c4a3a9cf993696cbfef78b586c8ae401b163df5556fd6a202d |
| pr_body.md | 85 | 5308 | 6d6891ae5c4611cfca69b7fbc0a948f3ade4727c107b00fe07235733319f5ab5 |
| readme_para.txt | 12 | 1095 | 973e8edf7a50b5cbffe538fbaa403f6034c7a219354a2b909412a3ef0886af84 |
| status_line.txt | 1 | 388 | c8a01fe88fcec510aec69f83d359b73807f0fbe7f076c2831e0b16d7444ece4a |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md` by `shutil.copyfile`, never by retyping; `closure.diff`
flips F029's STATUS line and moves the README's accepted count, Tier 5 Done cell and prose — it goes
on with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f029-r11-block.md` := this block and each payload as
   `.agent/authored/f029-r11-<name>`, by `shutil.copyfile`. Subject `F029 R11 C1: copy round 11
   block and payloads`. Its insertions are this block's line count plus 286; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F029 R11 C2: book round 10's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   5/6 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F029 R11 C3: rotate the finding ledger into its archive`. Expected: 0/32
   `.agent/live_review.md`, 32/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260927-201630-READY_FOR_REVIEW.zip`, its SHA-256
   `9a0d0eb2ac1576e96149aca426e6aec301eedc6247c9ee0fb0b4a8eb01e9bf4b`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f029r10e1001`, the accepted head
   `e56e82f733ec51609598590eda05aa1b2b7329ca` and `self-use NONE (queue exhausted)`; and it names NO pull
   request number, which does not exist when it is written. Subject `F029 R11 C4: accept F029 in
   STATUS with its README pins`. Expected for the two applied files: 15/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f029-subtree-rerun --title "F029 — Subtree rerun"
   --body-file .remedy-wt/f029-r11/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f029-r11-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f029-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f029-r11-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 339372 | dec48129b6976a72ee4dbe16a027091de3db8561a633e054ae325061169a8f0f |
   | .agent/plan.md | 873 | 8222fd694c6bb2c4a3a9cf993696cbfef78b586c8ae401b163df5556fd6a202d |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 12
   finding pairs moved: 2 (4 records)
   old ledger size: 339372 bytes
   new ledger size: 306611 bytes
   old archive size: 5251681 bytes
   new archive size: 5284442 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 306611 | 732faa4aa43e4114ef87bb4070f74336425cdf63229d0a86ac1c80ac608b112e |
   | .agent/live_review_archive.md | 5284442 | 95da423b1576fda9ed6b98b8dc38d63d953d93739572805b0768c502db8fddde |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 55545 | 59926b9ab218f1ea6c7b2af5e34f61749a6f41f030f61c8e83a70c3e8745a4e1 |
   | README.md | 40144 | dc94074530fa75e972d514cef8bdb84483c3d5cf613a2f9d52ae8a326218d606 |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 109, and with the Tier 5 Done cell left at 26,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `6bf13920`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 2 of
feature F029, round 11, rounds so far 11, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and "Operator
questions open: 0".
