STEP F289 R7 — THE CLOSING ROUND: book round 6, rotate the ledger, and accept F289 in STATUS with its README pins and the self-use item's consumption, then open the pull request

GOAL
Round 6 passed with the package READY_FOR_REVIEW. Close F289 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 6, rotate the finding
ledger, flip F289's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose, set `SU-033`'s `consumed_by` to `F289` in the same commit, and open the pull request.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full. You never issue a verdict and never merge. Every
change travels as a payload or is produced by the rotation script; you write only the handback.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`
rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`); a
heredoc containing a dollar-brace is refused, so write such a script to a file under
`.remedy-wt/f289-r7-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f289-r7/` and
`.remedy-wt/f289-review/` are the reviewer's and read-only.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f289-self-use-sources`, `git log --oneline -1` `439162d5`.
3. Measure this block's line count and sha256 (`.remedy-wt/f289-r7/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f289-r7/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 104 | 5938 | 8a4b3078e4f5533dc881d7109c4626d4ee05f7f60b6f4bd26b227925829d8b8d |
| closure.diff | 66 | 4526 | 882df928f577de08b4ef51f04e6a24a892a4afdc565dca5385ebe254abacadf4 |
| ledger.md | 2 | 2206 | 6b4150c210d782baeb23c139706d6c88245d791401b309181ccdb57228b0bc64 |
| plan.md | 26 | 800 | 90f11e973934f5ec128d9b872ec0f4fd0745a62b6896758b72403fea73f71d05 |
| pr_body.md | 70 | 4220 | 03dea724075433925670e300a718fe10cf4c81201bf4178b44c1e6620f8df44a |
| readme_para.txt | 10 | 835 | 48f8d768ffef26d4580165c420f6113bff79ecac8df2fb4dacce55b476d4015f |
| status_line.txt | 1 | 437 | 74adcc1ea805b17d2449e8c32e739b5cfa48e089eba15622931449f7859cba62 |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line); `plan.md`
REWRITES `.agent/plan.md`; `closure.diff` flips F289's STATUS line, moves the README's accepted
count, Tier 5 Done cell and prose, and sets `SU-033`'s `consumed_by` — it goes on with
`git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff writes,
for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f289-r7-block.md` := this block and each payload as
   `.agent/authored/f289-r7-<name>`. Subject `F289 R7 C1: copy round 7 block and payloads`. Its
   insertions are this block's line count plus 279.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F289 R7 C2: book round 6's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   5/5 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F289 R7 C3: rotate the finding ledger into its archive`. Expected: 0/36 `.agent/live_review.md`,
   36/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260926-225640-READY_FOR_REVIEW.zip`, its SHA-256
   `7044a4959459a9144a0b3030453ed74944ab4edad8125fd67c2eb2e6cc488a62`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f289r6e1001`, the accepted head
   `32013a054ea65dce679cc65fe2cd01fe8d73a76d` and the self-use item `SU-033`; and it names NO pull
   request number, which does not exist when it is written. Subject `F289 R7 C4: accept F289 in
   STATUS with its README pins and consume SU-033`. Expected for the three applied files: 13/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`, 1/1 `scripts/self_use_queue.json`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head feature/f289-self-use-sources
   --title "F289 — Self-use sources completion" --body-file .remedy-wt/f289-r7/pr_body.md`. DO NOT
   MERGE IT. Report its number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f289-r7-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f289-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f289-r7-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 335873 | 9211cf470be28b391704b488d15fae05158ee7f8aa9e00dd77a1c4d85808e8ab |
   | .agent/plan.md | 800 | 90f11e973934f5ec128d9b872ec0f4fd0745a62b6896758b72403fea73f71d05 |
   and `open_finding_ids` over the ledger at C2 — the simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 14
   finding pairs moved: 2 (4 records)
   old ledger size: 335873 bytes
   new ledger size: 296545 bytes
   old archive size: 5153462 bytes
   new archive size: 5192790 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 296545 | 5a049d48852ed2a8e899c3813247c2cccb1cedcb9b2892fc6459be49ac09f49d |
   | .agent/live_review_archive.md | 5192790 | eab2bff591ce02a6e8cdeea4d66d54b9f56cd61018fceca517b783a06225351d |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 54469 | af9e624757cf74f6cca374356e243662a122c0cc93bbb2bcf559161a9a8dfdd1 |
   | README.md | 37263 | 73421f27a982eab80e32119e1a9a0c8b2ff39a2a38b1792b189571edffcf6e03 |
   | scripts/self_use_queue.json | 137083 | 7012f06621b14f3847659ae44b779a9e23d205ee19b21d736e041ebfc7551a0d |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `SU-033`'s `consumed_by` read through `load_self_use_queue` from
   `packages.orchestration.self_use_queue`, which must be `F289`, with no pending item left;
   serially, `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py
   tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py`, which the simulation
   read WITHOUT the golden path as `470 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0. The reviewer
   red-controlled both README pins: with the accepted count left at 106, and with the Tier 5 Done
   cell left at 23, `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; and the count of
   `pull/` in it, which must be 0.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `439162d5`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit, the pull request and each gate), the deviations, and
the next action. Session section: SESSION 1 of feature F289, round 7, plus one sentence on how much
context you had left. `## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round
opens is merged by the NEXT feature's session, never by this one — then Rule A5, the first unchecked
feature in `docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and
"Operator questions open: 0".
