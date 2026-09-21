STEP R19 — F277 CI REPAIR: book round 18's PASS, register two findings, unpin the test from the machine

GOAL
Pull request 263 is open and F277 is closed, but CI run 35552041486 at `3d59a870` ended RED
on BOTH matrix legs at exactly one node. Operator amendment amend0820-gate-autonomy makes
repairing this branch the session's work order and explicitly allows commits on the open
pull request's branch for it. Book round 18's PASS, register R-1018 (the test) and R-1019
(the product ordering it uncovered, owned by F283), and land the one-test repair. No
production line changes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict, you never merge, and you never create a pull request
— 263 already exists and this branch's push updates it.

WHAT IS WRONG, SO YOU CAN RECOGNISE IT RATHER THAN TRUST IT
`tests/cli/test_worker.py::TestAWorkerRefusalIsShapedLikeTheCaller::test_unload_without_a_target_names_both_flags`
asserts that `_cmd_worker_unload(json_output=True)` with no target raises `SystemExit`
carrying the `missing_argument` token. `apps/cli/commands/worker.py` probes
`shutil.which("ollama")` at line 157 and returns early when it is None, BEFORE the refusal
at line 186. This machine has `ollama` at `/usr/local/bin/ollama`, so the test passes here;
the hosted runner has none, so it fails there. The repair pins the probe in the test, in
the idiom `TestWorkerDoctor` three classes up in the SAME FILE already uses four times, and
in the idiom `tests/storage/test_persistence.py::test_unload_requires_model_or_all` uses
for the SAME refusal. No assertion is touched. The product ordering is R-1019 and is NOT
fixed here: moving the check changes user-visible CLI behaviour and is F283's T001.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r19-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r19-scratch/`   YOURS. Every log, exit-code capture and script goes
      here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and never pipe pytest into `tail` without reading
`${PIPESTATUS[0]}` for the exit code. Use `python3 -c` or `python3 - <<'PY'` for counting,
hashing and copying (`shutil.copyfile`); a `python3 -c` script containing a newline
followed by `#` is rejected, so use the heredoc there. A `PATH=...` prefix on a `bash -c`
command line IS permitted and G4 needs it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `3d59a870`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r19-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all four under `.remedy-wt/f277-r19-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| worker_test.diff | 17 | 906 | d5fb79c0405340990579e66d2486c8aef3391a929d357647c5fce383b09cd954 |
| ledger.md | 6 | 11095 | 59f12b3d6dc5fd427d5eaf44d7c37ebac0fa1ff1a6e18d9379fe6eb9e06b48d6 |
| plan.md | 45 | 2350 | 4b197db68afdfc5eb05c9093bdeec52d3de8cc7372d13977c705b5756150ab58 |
| f283.diff | 23 | 1311 | 51d84d64bd3b97dffb247e368cc10ea8bf7b18305a0b37b60ce48137caaaae26 |

`ledger.md` is an APPEND of THREE PARAGRAPHS beginning with a single newline that is the
record separator: the round 18 `Gate:` entry, the `- R-1018` registration and the `- R-1019`
registration, in that order. `plan.md` is a REWRITE. `f283.diff` and `worker_test.diff` go
on with `git apply`; both were generated from the tree at `3d59a870` and both dry-ran with
`git apply --check` at real exit code 0. There is no slips payload and no decisions payload
this round.

BUNDLE — the commits are C1, C2, C3 and C4, in this order

C1 — copy this block and all four payloads into `.agent/authored/`
  `.agent/authored/f277-r19-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r19-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R19 C1: copy round 19 payloads into .agent/authored/`
  SIZE. The payloads total 91 lines, so this commit's insertions are 91 plus this block's
  own line count. Round 12 spent this FEATURE'S ONE permitted oversize declaration, so
  there is no second one available. Compute `500 minus 91 minus <the block line count you
  measured>`, report it, and STOP rather than commit if it is negative.

C2 — book round 18's PASS and register R-1018 and R-1019
  `.agent/live_review.md`                += ledger.md (append, +6)
  `.agent/plan.md`                       := plan.md   (rewrite, +26/-27)
  `docs/roadmap/features/T2_F283.md`     := `git apply` of f283.diff (+8/-0)
  All three land in ONE commit: amend0917 rule 4 puts the plan slice, the verdict booking
  and any ownership edit of a round in a single commit, and amend0911-feedback rule A
  requires the owning feature's Acceptance line to ride in the SAME commit as the
  registration that assigns it.
  Subject: `F277 R19 C2: book round 18's PASS and register R-1018 and R-1019`
  EXPECTED INSERTIONS: 40 by `git show --numstat` — 6 plus the plan rewrite's own DIFF
  insertions of 26 plus the F283 file's 8, measured by applying these payloads in a
  disposable worktree at `3d59a870`. If yours differs, report what you measured and say so.

C3 — THE REPAIR
  `git apply .remedy-wt/f277-r19-payloads/worker_test.diff`, touching only
  `tests/cli/test_worker.py`.
  Subject: `F277 R19 C3: pin the ollama probe in the worker refusal test`
  Expected insertions: 5.
  FINDINGS PERSIST BEFORE THE REPAIR, WHICH IS WHY C2 COMES FIRST. Do not reorder these.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F277 R19 C4: rewrite handoff for round 19`
  Then `git push origin feature/f277-machine-contracts`. DO NOT create a pull request —
  263 exists and this push updates it. DO NOT MERGE IT.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the five `.agent/authored/f277-r19-*` copies, `.agent/live_review.md`, `.agent/plan.md`,
   `docs/roadmap/features/T2_F283.md`, `tests/cli/test_worker.py` and `.agent/handoff.md`.
   Report the length you measure rather than checking it against a number this block
   states. In particular do NOT touch `.agent/candidates.md`, `.agent/decisions.md`,
   `.agent/operator_questions.md`, `docs/roadmap/STATUS.md`, `README.md` or any file under
   `apps/` or `packages/`.
4. NO PRODUCTION LINE CHANGES. `apps/cli/commands/worker.py` is READ ONLY this round. If
   you believe the product must change to make the gate green, STOP and hand back — that
   belief is R-1019 and it belongs to F283.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no
   `gh pr create`.
7. Leave the three `remedy/job-*` worktrees and both review packages alone. Any worktree
   you add for G4 goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT — for each of the four payload files report the line count, byte count and
 sha256 you measured against the PAYLOADS table above; twelve readings, all equal. Then for
 each `.agent/authored/f277-r19-*` copy at C1 — one per payload plus the block copy —
 compare it byte-for-byte with its source under `.remedy-wt/f277-r19-payloads/` (the block
 copy against `.remedy-wt/f277-r19-block.md`). Report one reading per copy and how many you
 compared; all True.

G2 THE BOOKING — at C2:
 (a) The append by strict byte CONCATENATION, not by length: the file's bytes at
     `3d59a870` plus the payload's bytes equal the file's bytes at C2. The reviewer
     measured 421313 plus 11095 equals 432408; report your three beside those.
 (b) The open set by distinct id in `.agent/live_review.md`, computed with the
     repository's OWN canonical reader — `open_finding_ids` from
     `scripts/rotate_live_review.py`, which takes the file's TEXT — at `3d59a870` and at
     C2. The reviewer measured 22 then 24, the two new ids being exactly `R-1018` and
     `R-1019`. Report both counts AND the set difference, not just the counts.
 (c) `.agent/plan.md` at C2 equals `plan.md` byte-for-byte at 45 lines. Report both
     sha256s and the line count, and confirm 45 is under the AGENTS.md 50-line rule.
 (d) `git diff --name-only 3d59a870 <C2>` names exactly three paths. Report the list and
     its length.

G3 THE REPAIR IS THE REVIEWER'S BYTES — at C3, report `git apply --check`'s real exit code
 before the real apply, then `git diff --name-only <C2> <C3>`, which must name exactly
 `tests/cli/test_worker.py`, and then `git diff <C2> <C3>`, which must be the payload's own
 hunk. Confirm by reading that `apps/cli/commands/worker.py` is NOT in that list.

G4 THE REPAIR IS PROVED IN BOTH ENVIRONMENTS AND STILL GATES THE PRODUCT — three readings:
 (a) WITH `ollama` HIDDEN, which is the hosted runner's condition and the one that was red:
```
bash -c 'PATH=/usr/bin:/bin python3 -m pytest -q -p no:cacheprovider tests/cli/test_worker.py; echo "REAL_EXIT=$?"'
```
     The reviewer measured `14 passed` at real exit code 0 on the repaired tree, and on the
     UNrepaired tree at `3d59a870` the same command reads `1 failed, 2 passed` for the
     class alone with captured stdout
     `{"version": 1, "provider": "ollama", "attempted": 0, "stopped": [], "skipped": [], "errors": [], "unavailable": true}`.
     Take the RED reading too, at `3d59a870` in a disposable worktree, so the gate is shown
     to be one that CAN fail.
 (b) With PATH untouched, the same file, real exit code 0.
 (c) THE MUTATION RED-PROOF, in a disposable worktree under `.remedy-wt/` at your C3 tree:
     replace the two-line `fail("missing_argument", "specify --model NAME or --all",
     json_output=json_output)` call in `apps/cli/commands/worker.py` with `targets = []`,
     run the single node
     `tests/cli/test_worker.py::TestAWorkerRefusalIsShapedLikeTheCaller::test_unload_without_a_target_names_both_flags`,
     and report that it goes RED — the reviewer read `Failed: DID NOT RAISE SystemExit` at
     exit 1. Then REMOVE the worktree and report `git worktree list`. This is what proves
     the pin isolated the environment without making the test vacuous.

G5 NO COLLATERAL — run and report with real exit codes, in the primary checkout, with
 `ollama` hidden so the readings are the hosted runner's:
```
bash -c 'PATH=/usr/bin:/bin python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_worker.py tests/cli/test_golden_path.py tests/orchestration/test_command_discovery.py tests/storage/test_persistence.py; echo "REAL_EXIT=$?"'
```
 The reviewer measured `399 passed` at real exit code 0 over this exact selection with the
 whole round staged. `tests/docs/` is in it because `docs/roadmap/**` changed; the other
 three files are every other test file that exercises `_cmd_worker_unload`. Then
 `python3 -m ruff check tests/cli/test_worker.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must still read all five checks
 `pass` with the two new findings registered — the reviewer measured `passed: True`,
 `fail_count: 0`. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one
 full-suite run and F277 spent it at round 15.

G6 TREE, PUSH AND CI — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 4`, which must show C4, C3, C2, C1 in that order;
 `git worktree list`, which must show the primary checkout and the three `remedy/job-*`
 worktrees and nothing else; `git push origin feature/f277-machine-contracts` with its real
 outcome; then `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must still show exactly pull request 263, not a draft, from
 `feature/f277-machine-contracts` into `main`. Finally report the CI run the push started:
 `gh run list --branch feature/f277-machine-contracts --limit 3 --json databaseId,status,conclusion,headSha`.
 Report the run id and its status as you read it. DO NOT wait for it and DO NOT merge.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 8 of feature F277, round 19, and states in one sentence how
much context you had left at the handback.

YOUR `## Next` NAMES, IN ORDER:
Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 19, then the Open
PR Gate — which waits for the CI run this push starts, and merges pull request 263 only
once that run is green. Then Rule A5, which proposes F283. Name two carried items
explicitly: (i) `R-1018` is FIXED by this round but its `Done:` line is owed to the FIRST
commit of the next round under amend0827 rule 1, and (ii) `.agent/candidates.md` still
holds three entries, which F283's first reviewed round resolves and empties. State the
open-findings count, which is 24 after C2, and the operator-questions count, which is 2.
