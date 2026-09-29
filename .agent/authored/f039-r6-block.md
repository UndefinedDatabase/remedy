STEP F039 R6 — REPAIR ROUND 5: book its FAIL with R-1100's resolution, register and repair R-1101 so the story's autoplay survives its host's renders, and prove it in the headless render

GOAL
Round 5 is reviewed FAIL at `bfa50f96`: everything it ordered passed, and its panel's autoplay
stalls while the shell re-renders faster than one step, which is finding R-1101. FIRST, in its own
commit, book round 5's gate entry, R-1100's resolution and R-1101's registration with the plan. Then
repair R-1101 in `apps/ui/src/components/story/StoryPanel.tsx`: the timer re-arms only when play
starts or stops, the position moves or the reduced-motion setting changes, and reads the latest
story view through a ref. Pin that in the panel's contract guard, and prove it in a round 6 copy of
the render harness with a ninth check in which the host re-renders every 50 ms and gains a ledger
row every 200 ms while Play still walks to the end. Nothing else in the product changes.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
repair, the guard's test, the render harness and the mutation tool yourself against S1 to S3. Only
the `.agent/` records travel as payloads. Read R-1101 in the records diff before you write code.
Before you write anything, read whole: `apps/ui/src/components/story/StoryPanel.tsx`;
`useTimelineScrub` in `apps/ui/src/components/timeline/useTimelineScrub.ts`, noting that its
`scrubTo` is a `useCallback` over a stable `cancelCatchUp` while the object it answers is new on
every render; `tests/ui_contracts/test_story_panel_contract.py`; the five
`.agent/authored/f039-r5-render_*` files and `.agent/authored/f039-r5-render.txt`; and your round 5
tool `.agent/authored/f039-r5-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r6-dry/`, `.remedy-wt/f039-r6-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r6-worker/`    YOURS for logs, scripts and screenshots; create it if absent.
                                  `.remedy-wt/f039-render-run/` is the harness's own work dir,
                                  created and removed by it. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the file.
Never run npm or npx. Stop a process only by its own recorded pid, never with `pkill -f`. Never
`git reset` a commit: a commit made out of order is declared, not rewritten.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `bfa50f969`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1034 | 2f1f2e0302216a5929d4f998bd6ea77f0888ea3cb1885ee3adb11b7436c99d01 |
| records.diff | 14 | 6938 | ac982f7accf5a81acb8aa7ea7c14c924a8d299bbf1843452346d30ae32a7cc52 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `bfa50f96`. It appends to `.agent/live_review.md`
round 5's gate entry, R-1100's `Done:` paragraph and the registration of R-1101.

THE SPECIFICATION.
S1 THE REPAIR, in `StoryPanel.tsx` and nowhere else in the product. A ref holding the story view,
   `useRef(view)`, is set to the current view by an effect with NO dependency list, declared before
   the timer effect, under a comment naming R-1101. The timer effect reads the view only through
   that ref, calls the scrub's `scrubTo` taken out of `scrub` by destructuring
   (`const { scrubTo } = scrub;`), and its dependency list is exactly
   `}, [playing, position, reducedMotion, scrubTo]);`. Its behaviour is otherwise unchanged: no step
   left ends play, and its cleanup clears the timeout. In C3, append to `.agent/live_review.md` one
   blank line and one line beginning `Landed: R-1101 — ` saying in one sentence what changed; it
   names no commit. Never write a `Done:` line.
S2 THE GUARD. `tests/ui_contracts/test_story_panel_contract.py` gains one test that the panel's
   comment-stripped source holds that exact dependency line and `viewRef.current`, and holds no
   dependency list of the timer naming `scrub` or `view` bare. Nothing else in it changes.
S3 THE RENDER, five NEW files `.agent/authored/f039-r6-render_measure.py`, `_index.html`,
   `_main.tsx`, `_vite.config.mjs` and `_drive.mjs`, copied from round 5's and changed only as
   follows. `main.tsx`, when the page's query holds `churn=1`, re-renders its host every 50 ms and
   appends to its rows every 200 ms one `feedRowOf` row of a `budget.tick` frame at the next seq,
   handing the growing rows to both `useTimelineScrub` and `StoryPanel`. `drive.mjs` gains C-i: on
   the page with `churn=1`, after clicking `The review`, Play records the positions 2, 3, 4, 5, 6, 7,
   8 and 9 as its first eight AND then at least one position greater than 9, a row that arrived
   after Play was pressed, within three seconds; it prints `RENDER: <n> of 9 checks pass`, with C-a
   to C-h as round 5 has them. Its whole output is saved as `.agent/authored/f039-r6-render.txt`.
   The reviewer's own probe of this check read the panel at `bfa50f96` advance no position, a panel
   keyed on the view stop at position 8, and a panel whose ref is never updated stop at position 9.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.
C1a — `.agent/authored/f039-r6-block.md` := this block and `.agent/authored/f039-r6-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R6 C1a: copy round 6 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 29; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r6-records.diff` := records.diff. Subject: `F039 R6 C1b: copy round 6
  records diff into .agent/authored/`. Expected insertions: 14.
C2 — THE FINDINGS FIRST: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F039 R6 C2: book round 5's FAIL and R-1100, register R-1101`. Expected by
  `git show --numstat`: 6/0 live_review.md, 7/8 plan.md.
C3 — S1 and S2. Subject: `F039 R6 C3: keep the story's pending step through its host's renders
  (R-1101)`.
C4 — S3's five files and `.agent/authored/f039-r6-render.txt`. Subject: `F039 R6 C4: render the
  story panel under churn and record its checks`.
C5 — your mutation tool as `.agent/authored/f039-r6-mutations.py`. Subject: `F039 R6 C5: add the
  mutation tool for R-1101`.
C6 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R6 C6:
  rewrite handoff for round 6`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r6-*` files,
   `.agent/live_review.md`, `.agent/plan.md`, `apps/ui/src/components/story/StoryPanel.tsx`,
   `tests/ui_contracts/test_story_panel_contract.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only bfa50f969` measures after C6. Do NOT touch anything else, and never a
   round 5 file under `.agent/authored/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`, no `git reset`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree listed at
   your step 4, and every stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as
   that gate's last action, and `git worktree list | wc -l` is reported afterwards.
7. DO NOT run the full suite: it belongs to F039's closure (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f039-r6-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r6/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it. One reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 346240 | c7934727f5d2978a407e73ad11124ec92b73335364c9da8033e2ae4156f70ae1 |
 | .agent/plan.md | 1034 | 2f1f2e0302216a5929d4f998bd6ea77f0888ea3cb1885ee3adb11b7436c99d01 |
 Also: `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2, which the reviewer read as `['R-1101']` and `FAIL`; `git diff --name-only
 <C1b> <C2>`, which must name exactly the paths of the table; and at C3, the ledger at C2 is a
 byte-exact prefix of the ledger at C3 and what C3 adds to it is exactly "\n" plus one line
 beginning `Landed: R-1101 — ` and ending in "\n".

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_story_panel_contract.py
 .agent/authored/f039-r6-render_measure.py .agent/authored/f039-r6-mutations.py` at C5, with its
 real exit code. Then report, quoted from C3, the ref, its effect and the whole timer effect, and
 from C4 the churn half of `main.tsx` and C-i of `drive.mjs`.

G4 THE TESTS AND THE RENDER — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of C3, and read `2241 passed, 10 skipped` at real exit code 0.
 Every skip of that run which names `node_modules`, `dist` or vitest is a toolchain node a fresh
 worktree lacks, and in the primary checkout each must PASS rather than skip. Report every
 `SKIPPED` line and the node count of the contract test. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass` at `fail_count` 0, the
 verdict check's message reading `last Gate verdict FAIL`, which it passes because the context does
 not say the work is complete. Then `python3 .agent/authored/f039-r6-render_measure.py
 /home/decodeux/Repos/remedy`, whose whole output C4 saves: it must print
 `RENDER: 9 of 9 checks pass` and exit 0, and afterwards `.remedy-wt/f039-render-run` must be gone
 and `git status --porcelain` empty.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r6-mutations.py` edits `StoryPanel.tsx` in a
 disposable worktree, runs `tests/ui_contracts/test_story_panel_contract.py` there with the
 worktree's root first on `PYTHONPATH`, AND runs `.agent/authored/f039-r6-render_measure.py` with
 the worktree as its repository root, so the page imports the worktree's panel; it prints one line
 per mutation with the contract's exit code and failed count and the render's `RENDER:` line,
 controls first and last, `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED
 CLEANLY: <bool>`. A mutation is caught when the contract fails AND the render reads fewer than 9:
  m1 the timer's dependency list gains `scrub`;
  m2 the timer reads `view` itself and its dependency list gains `view`;
  m3 the ref's effect is deleted, so the timer reads the first view forever.
 For m3 the contract may stay green; report what it reads, and the mutation counts as caught when
 the render reads fewer than 9. Run it on `git worktree add --detach .remedy-wt/f039-r6-mut <C5>`
 and report its whole output. EVERY mutation must be caught; one that is not is reported as it is,
 and you then add the check that catches it before C6 and re-run. Then remove the worktree,
 `git worktree prune`, and report `git worktree list | wc -l` and `git status --porcelain`, which
 must be empty.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6 to C1a and `bfa50f969` in order (more lines if a
 commit was split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C5 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 1 of feature F039, round 6, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 6
with the resolution of R-1101, then T003: the export command and its build. State the open-findings
count, 1 (R-1101, landed and awaiting review), and the operator-questions count, 1.
