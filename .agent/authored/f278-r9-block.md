STEP F278 R9 — the closure sequence's first half: the built state, the one checklist pass, the self-use item and the feature's one full suite

GOAL
Book round 8's PASS and resolve R-1037 and R-1038, write the feature file's Built State, fold this
feature's two prose lessons into the reviewer checklist without lengthening it, run the closure's
self-use item to its approval gate, and run this feature's ONE full suite, committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors the RECORD payloads and the checklist
pairs; the feature file's Built State prose is yours, written to the SPEC in C3. This round closes
nothing: the STATUS line, the evidence job, the review zip and the pull request belong to later
rounds, and no commit of this round may touch `docs/roadmap/STATUS.md`, `README.md` or
`scripts/self_use_queue.json`'s `consumed_by` fields.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r9-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1 (`build_payloads.py`, `dry_run.py`), which is read-only to you.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file. Capture real exit codes
as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. NEVER USE
`git stash` IN ANY FORM, and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f278-durable-writes-loud-failures`, `git log --oneline -1` reads `e5497b6b`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f278-r9-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record, before anything runs: `git branch --list 'remedy/job-*'` count, `git worktree list`,
   and the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f278-r9-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| checklist18_from.txt | 1 | 56 | db4cdf464518e1501ce3a0fb4b455639d29e9cf4eb3952e28c4a246c6647eb47 |
| checklist18_to.txt | 10 | 784 | 01ea6c2ce33bde1d2d659245e809223382f0e1ab8dc0678dfc4b91ee3e3e8fb4 |
| checklist28_from.txt | 1 | 86 | b2547124fdde6c4efa0352a441cd124b47c8de42d337f36e70e4985a30e4817d |
| checklist28_to.txt | 8 | 648 | 0ab9bfe595b6017932d680a9277e6809cbb4f63a75650ed771aa875b3b4dd275 |
| ledger.md | 6 | 5056 | 55393049737567eacd15bae413b2472644da47426e71842310a899f7bcc52225 |
| plan.md | 30 | 1198 | ccfce1593f91c9f5affb45edf3f8f7e7e3ea0120450d64b7d1b1fc3d0bc2a6ad |
| prose_slips.md | 1 | 477 | 59591f21ed9145b2010551e3fd95aa20c2eefebc55b1473141694a8de49aed21 |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 8's
`Gate:` entry and the `Done:` paragraphs of R-1037 and R-1038. `prose_slips.md` is an APPEND of
one dated line. `plan.md` is a REWRITE. `checklist18_from.txt`/`checklist18_to.txt` and
`checklist28_from.txt`/`checklist28_to.txt` are replacement pairs for
`docs/agents/planner_reviewer_prompt.md`; the reviewer's containment test printed
`TO contains FROM: True` for each, so each pair is an APPEND and no FROM-zero count is owed —
each FROM stays at exactly one occurrence, and each line only its TO holds appears exactly once
among the lines that commit ADDS. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f278-r9-block.md` := this block; `.agent/authored/f278-r9-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F278 R9 C1: copy round 9 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/prose_slips.md` += prose_slips.md ·
  `.agent/plan.md` := plan.md. Appends are strict byte concatenation onto the file as it stands
  at `e5497b6b`.
  Subject: `F278 R9 C2: book round 8's PASS and resolve R-1037 and R-1038`

C3 — THE BUILT STATE, in `docs/roadmap/features/T2_F278.md`: a `## Built State` section appended
  at the end of the file, written in plain complete sentences, that states for each Acceptance
  line what meets it and where:
  - the fsync of the file and of its parent directory, and the eight concurrent writers:
    `tests/orchestration/test_secure_fs_durable_write.py`, naming the two test functions;
  - no private atomic-write helper outside `packages/common/`:
    `tests/orchestration/test_durable_write_guard.py`, with the planted-helper test as its red
    proof and its migration ratchet now empty;
  - every surviving call site on the shared helper, one deletion per commit: rounds 2 to 4 under
    DECISIONS F278 D1, D2 and D3;
  - BLE001 on, its excused sites frozen at 290 with a reason each: `pyproject.toml` and
    `tests/test_ble001_ratchet.py`. Read DECISIONS F278 D4 and D7 in `.agent/decisions.md` first,
    and say in one sentence how the shipped shape differs from the file's T003 wording (inline
    `# noqa: BLE001 — <reason>` marks held by a count ratchet, rather than a separate ignore list);
  - the stream artifact's `degradations`: `tests/orchestration/test_stream_evidence.py`'s
    `TestDegradations`, round 5.
  Then one paragraph on the fail-open handlers the marking found and repaired rather than excused:
  `_contains_secret` under DECISION F278 D5, R-1036 at round 7, R-1037 and R-1038 at round 8, and
  the one handler narrowed at round 8. Name the DECISIONS this feature recorded (F278 D1 to D7) as
  a list of ids with one clause each, taken from their headings. Name the three test files this
  feature added — the two above under `tests/orchestration/` and `tests/test_ble001_ratchet.py` —
  and state that it added no module under `packages/`, `apps/` or `scripts/` and no line to the
  import-reachability allowlist (closure precondition 7). Correct nothing else in the file and
  remove nothing from it.
  Subject: `F278 R9 C3: write the feature file's Built State`

C4 — THE ONE CHECKLIST PASS (operator amendment amend0827 rule 4): apply both payload pairs to
  `docs/agents/planner_reviewer_prompt.md`. Each clause joins an existing item — 18 and 28 — and
  the list does not grow. Apply each pair byte for byte; edit nothing else in that file.
  Subject: `F278 R9 C4: fold F278's two prose lessons into checklist items 18 and 28`

C5 — THE SELF-USE ITEM (closure precondition 6):
  (a) `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST. The
      reviewer's dry run at `e5497b6b` appended `SU-027`, "Address ledger finding R-0998"; report
      what yours does, and report `next_self_use_item()`'s answer afterwards.
  (b) RUN it with `packages.orchestration.self_use_runner.run_next_self_use_item`, whose
      `dest_dir` is a path under `.remedy-wt/` and never a tracked one. Pass no
      `builder_name`/`reviewer_name`, so both resolve from the one `self_use` role configuration
      (DECISION amend0920-selfuse-real D2); report the `execution_config` the returned `JobPlan`
      carries, which is the proof of which provider actually ran. It is run to the approval gate
      and NEVER applied.
  (c) Save under `.agent/selfuse_f278/`, mirroring `.agent/selfuse_f283/`'s file names: the item
      markdown, the entry and job-file path, the execution config, the result state, the timing,
      the transcript, and `run_defects.txt` holding every string
      `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
      run's own `JobPlan` — verbatim, and the literal `NONE` if it returns an empty tuple.
  (d) Then `python3 -m pytest tests/docs/ -q`. The generated item's text lands in the tracked
      `scripts/self_use_queue.json`, and `tests/docs/test_retired_promote_word.py` reads it
      (finding R-1015). If that guard goes red on the text the generator wrote, repair its
      `KEPT_BY_SENSE` entry for `scripts/self_use_queue.json` — the tokens the NEW text carries,
      or the entry removed when it carries none — IN THIS COMMIT, and report both readings. The
      reviewer's dry run read `315 passed` at exit 0 with the generated item in place.
  This commit's paths: `scripts/self_use_queue.json`, `.agent/selfuse_f278/**`, and
  `tests/docs/test_retired_promote_word.py` only if (d) requires it. You do not register
  findings: the reviewer authors every registration from `run_defects.txt` at the next round.
  Subject: `F278 R9 C5: generate and run the closure's self-use item, record its defects`

C6 — THE INTEGRATION GATE, this feature's ONE full suite (operator amendment amend0917-throughput
  rule 1): `python3 -m pytest -n auto -q` in the PRIMARY checkout, after C5, with its log written
  outside the repository (`~/remedy-gate-scratch/` is writable). Commit the summary line and the
  FULL list of bad node ids as `.agent/authored/f278-closure-suite.txt`, together with the
  handback. `.agent/handoff.md` is rewritten per `docs/agents/handback_template.md` in this same
  commit.
  Subject: `F278 R9 C6: record the closure suite transcript and rewrite handoff for round 9`
  Then `git push origin feature/f278-durable-writes-loud-failures`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the `.agent/authored/f278-r9-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `.agent/authored/f278-closure-suite.txt`, `.agent/selfuse_f278/**`,
   `docs/roadmap/features/T2_F278.md`, `docs/agents/planner_reviewer_prompt.md`,
   `scripts/self_use_queue.json`, and `tests/docs/test_retired_promote_word.py` under C5 (d).
   Report the set you measure. Nothing under `packages/`, nothing under `apps/`, no
   `docs/roadmap/STATUS.md`, no root `README.md`, nothing else under `scripts/`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/decisions.md`.
4. If the full suite in C6 is RED, that is this feature's work and not a reason to stop: commit
   the transcript exactly as measured, report every bad node id, and hand back. The repair rounds
   and their rules are the reviewer's to order (amend0917-throughput rule 2). Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no `consumed_by` edit, no review zip, no evidence job.
7. The self-use run may leave `remedy/job-*` branches, worktrees or evidence directories behind.
   Report them; delete NOTHING you did not create as scratch, and never delete a branch.
8. Any Python you run that edits a module and then imports it again runs under `python3 -B`
   (the lesson C4 writes into item 18).

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f278-r9-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f278-r9-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`:
 (a) By strict byte CONCATENATION onto the `e5497b6b` bytes, the reviewer's dry run composed
     `.agent/live_review.md` at 453125 bytes, sha256
     `17900f7de3042f5f3b5ba3a15691fab2e458f9eeb63d48331d55797dac91ab38`, and
     `.agent/prose_slips.md` at 364068 bytes, sha256
     `882d773a0f6152f182786a34b2938aa01a55f8752691e61588088479b571560e`. Report yours beside them.
 (b) Line-anchored on the committed ledger: `^Gate: F278 R8 — ` 1, `^Done: R-1037 — ` 1 and
     `^Done: R-1038 — ` 1. Open set by distinct id via `open_finding_ids` from
     `scripts/rotate_live_review.py` at `e5497b6b` and at C2: the reviewer measured 28 and 26,
     REMOVED `R-1037` and `R-1038`, ADDED none.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (under 50).

G3 THE DOCS — at C4: each FROM occurs exactly ONCE in `docs/agents/planner_reviewer_prompt.md`
 before and after (the pairs are APPENDs), and each line only a TO holds occurs exactly once among
 the lines C4's diff ADDS. The file's sha256 after C4: the reviewer's dry run read
 `7dd51bc306fc62aabd2b3564836bbf6233649f951ab29e2d255a0b2499384c70`. The numbered items of the
 pre-emission checklist, read mechanically, count 34 before and 34 after, in the same order — the
 reviewer read
 `1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37`
 at `e5497b6b`. Then `python3 -m pytest tests/docs/ -q` after C3 and again after C4, since C3
 writes a roadmap file; the reviewer's dry run of C2 and C4 read exit 0.

G4 THE SELF-USE ITEM — at C5: the generator's answer and `next_self_use_item()`'s afterwards; the
 runner's returned entry id, job file path and job state; the `execution_config`'s builder and
 reviewer names and models, which must be the `self_use` role's configured provider and never a
 raw fallback; the `describe_self_use_run_defects` output verbatim; `python3 -m pytest tests/docs/
 -q` after the queue file is written, with its exit code; and `git branch --list 'remedy/job-*'`
 counted before C1 and after C5 with `git worktree list` beside each.

G5 THE INTEGRATION GATE — at C6: `python3 -m pytest -n auto -q` in the primary checkout, its real
 exit code, its summary line and every bad node id, all of it in
 `.agent/authored/f278-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` and `tests/test_no_orphan_modules.py` are among
 the bad nodes (closure precondition 7). Then `python3 -m apps.cli.main integrity check --json`,
 all five checks `pass`, and `git status --porcelain`, which must be empty with no relevant
 untracked file (closure precondition 3).

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`; `git
 worktree list`; `git stash list`'s first line unchanged from its reading before C1; the push's
 real outcome; `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item and gate: state block, the per-commit changed-files
table with the insertions git MEASURED, every gate's real output and exit code, the self-use run's
entry id, provider, state and defect list, the full suite's summary line and bad node ids, the
deviations, and the next action. Your Session section reads SESSION 2 of feature F278, round 9,
and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
9, then the closure sequence's second half — the registrations the self-use defects ask for, the
evidence job and the review zip — and then the closing round: the ledger rotation, the STATUS line
with the README counters in the same commit, and the pull request. State the open-findings count,
26 after this round, and the operator-questions count, 0.
