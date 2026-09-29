STEP F039 R13 — THE CLOSING ROUND: book round 12, rotate the ledger, and accept F039 in STATUS with its README pins and the self-use item's consumed_by, then open the pull request

GOAL
Round 12 passed with the package READY_FOR_REVIEW. Close F039 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 12, rotate the finding
ledger, flip F039's STATUS line to `[x]` as PASS_WITH_RISKS with R-1104 carried to F286, move the
README's accepted count, Tier 5 Done cell and prose, and set `SU-035`'s `consumed_by` to `F039`, all
in the closure commit, then open the pull request.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full. You never issue a verdict and never merge. Every
change travels as a payload or is produced by the rotation script; you write only the handback.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`
rather than `cd`, and never `cd` your shell into a worktree. Use `python3 - <<'PY'` for counting,
hashing and copying (`shutil.copyfile`); a heredoc containing a dollar-brace, or a brace next to a
quote, is refused, so write such a script to a file under `.remedy-wt/f039-r13-worker/`, which is
yours. Never run npm or npx. `.remedy-wt/f039-r13/`, `.remedy-wt/f039-r13-sim/`, every other
`.remedy-wt/f039-*` path and `.remedy-wt/f039-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f039-story-replay-mode`, `git log --oneline -1`
   `7ab8d446e`.
3. Measure this block's line count and sha256 (`.remedy-wt/f039-r13/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f039-r13/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 116 | 6005 | e1e324659e1704aada41d615f7ccee2938cd3b19e499e4ab8475b3a68ee23354 |
| closure.diff | 66 | 5470 | 2d42f0a3d7d5027265ed1f189a13af77a0b6c149062df0d35b0511bcc32043c1 |
| ledger.md | 2 | 2068 | 49bca28587597157632b5b6b26e00250bcfd0db3f22df9d88330cda8c4a416ad |
| plan.md | 26 | 835 | 0607ffc559f443cc2d9a2ab9e8c66f2aefc8e6d3f2089e27543ee486f36d56e3 |
| pr_body.md | 53 | 3174 | 86da73e973aa61429ce5c5fe4a9e56874f93598bed9cf609eac4a709a3d28457 |
| readme_para.txt | 10 | 914 | e0cd34b1a56f32ef02df50d590dd154b91bf7c116edf64d7f50433bf16d93c39 |
| status_line.txt | 1 | 427 | c30cd84a7c7faa889e02a130904c9e1d966f189dfa875b6696fb0639d0209e20 |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md` by `shutil.copyfile`, never by retyping; `closure.diff`
flips F039's STATUS line, moves the README's accepted count, Tier 5 Done cell and prose, and sets
`SU-035`'s `consumed_by` in `scripts/self_use_queue.json` — it goes on with `git apply --check` then
`git apply`; `status_line.txt` is the exact STATUS line closure.diff writes, for G4's proof;
`pr_body.md` is the pull request's description, passed to `gh` as a file; `readme_para.txt` and
`build.py` are the reviewer's sources for closure.diff, copied for the record and never applied or
run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f039-r13-block.md` := this block and each payload as
   `.agent/authored/f039-r13-<name>`, by `shutil.copyfile`. Subject `F039 R13 C1: copy round 13
   block and payloads`. Its insertions are this block's line count plus 274; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F039 R13 C2: book round 12's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   5/6 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F039 R13 C3: rotate the finding ledger into its archive`. Expected: 0/54
   `.agent/live_review.md`, 54/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260929-031523-READY_FOR_REVIEW.zip`, its SHA-256
   `e9097684c735ec44a6b33f4bc409de252280e7294e3d2d142b4197684f9dee7d`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f039r12e1001`, the accepted head
   `da3d5430681239aff3419da447abbb75f2105112` and the self-use item `SU-035` consumed by `F039`; and it
   names NO pull request number, which does not exist when it is written. Subject `F039 R13 C4: accept
   F039 in STATUS with its README pins and consume SU-035`. Expected for the three applied files:
   13/2 `README.md`, 1/1 `docs/roadmap/STATUS.md`, 1/1 `scripts/self_use_queue.json`. Then
   `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f039-story-replay-mode --title "F039 — Story/replay mode"
   --body-file .remedy-wt/f039-r13/pr_body.md`. DO NOT MERGE IT. Report its number and URL in your
   final reply only.

CONSTRAINTS
1. Never edit or retype a payload. `build.py` is NOT run: it would reset the reviewer's tree.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f039-r13-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays, the self-use job's
   `remedy/job-7a88d05bed5c40dd` included.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f039-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f039-r13-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 372598 | 573f51e68f2bde547dac1ec4d6eb83ad591228905f4e0c0ff19312611e370812 |
   | .agent/plan.md | 835 | 0607ffc559f443cc2d9a2ab9e8c66f2aefc8e6d3f2089e27543ee486f36d56e3 |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `['R-1104']`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 15
   finding pairs moved: 6 (12 records)
   old ledger size: 372598 bytes
   new ledger size: 317106 bytes
   old archive size: 5419927 bytes
   new archive size: 5475419 bytes
   open findings before: 1
   open findings after: 1
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 317106 | 30e8c61c3cd95dc293799f6af32d2c9b31e11397b70ef5cbc0f582f24bd42d4e |
   | .agent/live_review_archive.md | 5475419 | 40565125afb4784a9627887a6ff557d33bba0f04960239986805647408609ceb |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 57372 | 68c236936610153607cc576be6ad3e894c34281eab629c6e6660cfa7262cd32a |
   | README.md | 44495 | c78b82434ed0a36dab17db488d6989e97b7a4d09275c459aba091482c8f91abd |
   | scripts/self_use_queue.json | 139444 | 7d996aa95f1dad19e0971968ab52dca1ad5b87d7038fcf769d90159d916cfce3 |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 114, and with the Tier 5 Done cell left at 31,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `7ab8d446e`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 2 of
feature F039, round 13, rounds so far 13, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`; the next claim books this round's verdict. State the open-findings count
as the script reads it at C3, and "Operator questions open: 1".
