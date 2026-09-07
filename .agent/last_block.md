STEP T004 (deletion 1) — F272 One world completion — ROUND 19
EVERY RULE LINE IN THIS BLOCK IS EXACTLY SIX U+2500 CHARACTERS.
WORKER for docs/agents/self_drive_protocol.md; AGENTS.md binds in full.
SESSION 9 of F272, round 19, base `4c70ba90`. Soft limit 12 sessions / 40
rounds — not reached, no scope report owed.
DELETION ROUND under amend0906-triage-throughput: four measurements and nothing
else over the deleted code — no byte forensics over production text, no
mutation red-proof. THAT PARAGRAPH ALSO CAPS SUCH A BLOCK AT SIXTY LINES AND
THIS BLOCK EXCEEDS IT, which is declared here rather than glossed: the
instruction prose runs to 131 lines, counted on these final bytes. What the
extra lines buy is not
deletion forensics — amend0906 removes those and none is ordered — but
obligations other live rules impose on EVERY round: booking the previous
round's verdict into the ledger in this round's first commit (amend0827 rule 1),
carrying `.agent/plan.md` in the change set because the round touches the
ledger (§3 item 23), and proving transport, the record append and the tree.
A future consolidation should decide whether amend0906's cap was meant to bind
a deletion round that also books a verdict; this round does not decide it, and
does not pretend to meet it.
SANDBOX: env assignment denied in all forms — use `os.environ`; `cp` denied —
use `shutil.copyfile`; real exit codes via `bash -c '<cmd>; echo "REAL_EXIT=$?"'`
with NO pipe between command and echo.
Goal: delete the classic `job run-loop` command surface — T004's first deletion.
──────
C0a save this block verbatim to `.agent/authored/f272-r19.md`
C0b mirror the same bytes into `.agent/last_block.md`
C1  REPLACE `.agent/plan.md` with PLANF272R19
C2  APPEND RECORDR19 to `.agent/live_review.md` as `pre + b"\n" + slice`,
    against a pre-image read immediately before the write
C3  THE DELETION — all four paths in ONE commit, since deleting the command
    without its tests leaves a red tree the round must not pass through
C4  rewrite `.agent/handoff.md`
──────
C3 deletes exactly this and nothing else:
1. `apps/cli/commands/job.py` — the whole `def _cmd_run_loop(...)`, and the
   `"job.run-loop": lambda args: _cmd_run_loop(...)` COMMAND_HANDLERS entry.
2. `apps/cli/command_catalog.py` — the whole
   `CommandEntry(command_id="job.run-loop", ...)`. Its `related=` tuple dies
   with it; measured at `4c70ba90`, no other entry names `job.run-loop`.
3. `tests/test_agent_loop_execution.py` — classes `TestRunLoopCLI` and
   `TestRunLoopGroupedHelp`, which exist only to pin this command; then the two
   imports that orphans, `subprocess` and `sys` (ruff reports F401 if left);
   then the module docstring sentence "Tests: run_agent_loop, job.run-loop CLI,
   run-log events." — it names a command that will no longer exist, so correct
   that one sentence.
4. `tests/cli/test_command_catalog.py` — the class `TestRunLoopCLIHelp`.
DO NOT delete `packages/orchestration/autonomy_loop.py`. Measured at
`4c70ba90`: after C3 its only callers are `tests/orchestration/test_autonomy.py`
and `tests/storage/test_persistence.py`, so it becomes production-unreachable —
which is precisely what T005's reachability test and cluster deletion exist for,
and the Orchestrator brief forbids splitting inside T005.
`job.run-next` and `job.run` STAY: measured at `4c70ba90`,
`_cmd_run_next_task_local` has a production caller at
`packages/orchestration/agent_loop.py:626` and `_cmd_job_run_cycles` is called
by `_cmd_job_resume`, so neither is a clean cut and both need a ruled design.
──────
Constraints
1. Slices are applied BYTE FOR BYTE, extracted programmatically from
   `.agent/authored/f272-r19.md` between their `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. If one looks wrong, apply it and DECLARE it.
2. After C3, `^<<<(BEGIN|END) .*>>>$` counts 0 in `.agent/plan.md` and
   `.agent/live_review.md`. Both are already 0 at `4c70ba90`; the ledger's 15
   mid-line `<<<` substrings are PRE-EXISTING prose, not marker lines.
3. ZERO ids minted. R-0823 stays free.
4. C3's diff shows NO added line except the corrected docstring sentence. No
   shim, no alias, no deprecation: AGENTS.md "Replacing is deleting".
5. Read `.agent/STOP` with `os.path.exists` before C0a, before C3 and before
   C4, and report every reading.
──────
Done when — every gate RUN with its REAL exit code; G1-G6 before C4
G1 TRANSPORT — one digest comparison: `.remedy-wt/f272-r19-block.md`,
   `.agent/authored/f272-r19.md` and `.agent/last_block.md` share one sha256,
   one byte length, one line count. Hash the source on arrival, before any other
   work. C0a and C0b are both `shutil.copyfile`.
G2 THE RECORD, over the C2 append. (a) BYTE: the pre-image's length, sha256,
   terminal twelve bytes and trailing-newline run; `pre` a byte-exact PREFIX of
   `post`; `post == pre + b"\n" + slice`. (b) STRUCTURAL: strip the single
   terminal newline before splitting on blank lines and say so; N is COUNTED BY
   YOUR SCRIPT from the slice, never taken from here; report units before and
   after, that the last N equal the slice's N paragraphs IN ORDER, and that
   everything before is unchanged. (c) NEGATIVE CONTROL on the FIRST appended
   paragraph, in memory only, never on disk. (d) COUNTS before and after:
       ^- R-\d{4} distinct     306 -> 306     ^Gate:           41 -> 42
       ^Done: R-\d{4} distinct 249 -> 249     ^Gate: F272 R18   0 ->  1
       open set BY DISTINCT ID  57 ->  57
   Report any difference; adjust nothing to make it agree.
G3 THE PLAN — `.agent/plan.md` byte-equals PLANF272R19; report bytes, line count
   against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps` are
   present.
G4 THE DELETION, BY EXACT SYMBOL — over every tracked `.py` from `git ls-files`,
   report the occurrence count of `_cmd_run_loop` and of `job.run-loop` before
   C3 and after C3; both must reach 0. DO NOT sweep the bare word `run-loop`:
   measured at `4c70ba90` it occurs in NINE tracked `.py` files, most of them
   `dogfood.run-loop` and the `mission` group, so a zero-gate over it is
   unmeetable and would be a false gate. Also report that
   `packages/orchestration/autonomy_loop.py` still EXISTS.
G5 THE FULL SUITE — in the PRIMARY checkout, never a worktree:
       python3 -B -m pytest -n auto -q -p no:randomly
   Report the REAL exit code and the counted line. The reviewer measured the
   BASE at `4c70ba90` in the primary checkout as EXIT 0, 19785 passed, 23
   skipped, and measured the SAME suite inside a fresh worktree failing about
   ten tests for want of `apps/ui/node_modules` — which is why this gate names
   the primary checkout. C3 removes 4 test functions, so the expected reading is
   EXIT 0 at 19781 passed. RECONCILE rather than assert: `ast`-count the test
   functions in the two touched test files before and after C3 and report that
   arithmetic beside the number that ran.
G6 RUFF — `python3 -m ruff check apps/cli/commands/job.py
   apps/cli/command_catalog.py tests/test_agent_loop_execution.py
   tests/cli/test_command_catalog.py`; real exit code, which must be 0. An F401
   means an orphaned import was left, which C3 item 3 already names.
   NOT ORDERED, stated so nobody reads it as skipped: the import-reachability
   test amend0906 names as a deletion round's first measurement DOES NOT EXIST
   at `4c70ba90` — no tracked file matches `reachab` in its name. It is the D11c
   test T005 builds; ordering it would name a path that cannot resolve.
G7 THE TREE — `git status --porcelain` at EVERY commit boundary, real output
   each time, empty every time; `git ls-files .remedy-wt` (expected empty);
   `git worktree list` (expected 13). Per-commit insertions from
   `git diff --numstat <parent> <commit>`, C4 EXCLUDED, each under 500. Report
   the three `.agent/STOP` readings.
──────
Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md; no
length cap. Carry SESSION NUMBER 9 and round 19; the range and branch; a
per-commit changed-files table whose `+/-` comes from `git diff --numstat` and
matches G7 cell for cell; an item-status table with C0a, C0b, C1, C2, C3, C4
each exactly once; the open-findings count BY DISTINCT ID with its arithmetic;
ONE LINE PER GATE with its real exit code; every deviation and assumption;
external actions; one sentence of context self-assessment.
DO NOT create a PR. DO NOT merge. DO NOT force-push. Push the branch and stop.
──────

<<<BEGIN PLANF272R19>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 18 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and T003
are COMPLETE. T004 has begun.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

T004's first deletion: the classic `job run-loop` command surface — its handler,
its catalog entry and the tests that exist only to pin it. It is the one of the
three classic-runner commands that deletes cleanly; the other two have
production callers and are deliberately left standing.

## Next Steps

1. Rule and then delete `job.run-next` and `job.run`. Measured at `4c70ba90`,
   neither is a clean cut: `_cmd_run_next_task_local` has a production caller
   at `packages/orchestration/agent_loop.py:626`, and `_cmd_job_run_cycles` is
   called by `_cmd_job_resume`, so the fate of `job resume` and of the agent
   loop's step must be ruled by measurement before either command dies.
2. The resolver collapse, which DECISION F260 D5 puts in the SAME commit range
   as the classic store deletion. `.agent/f272_t004_deletion_inventory.md`
   bounds that store at 199 tracked files, 72 of them production, so it is
   many rounds and its staging is designed from that file.
3. T005, the reachability test and the cluster deletion, which is never split.
   `packages/orchestration/autonomy_loop.py` becomes production-unreachable
   this round and is left for it rather than deleted early.

## Risks

- A half-performed deletion is the one state the feature's Orchestrator brief
  says this work must not leave behind, so every deletion round ends with the
  full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 9
  and round 19 the feature is inside it and no scope report is owed.
<<<END PLANF272R19>>>

<<<BEGIN RECORDR19>>>
Gate: F272 R18 — the F272 round 18 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `4c70ba90`. Range `7b1590dc`..`4c70ba90`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the change set exactly the eight ordered paths and nothing else, `git status --porcelain` empty and every commit's insertions under the DECISION F104 D1 cap of 500 at a maximum of 396. THE ROUND SHIPPED NO PRODUCTION CODE ON PURPOSE and is not the pure-bookkeeping round amend0827 rule 1 forbids: its substance is the ruling §4 item 7 requires when a spec is wrong, plus a probe-measured inventory, and neither is a verdict, a registration or a correction. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r18-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r18.md` and `.agent/last_block.md` are all 31489 bytes at 396 lines and all hash to `943666a116f848ccfdde76742cf4f5e20bacd28446461aec021fa9f87027f712`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces on every reader: `.agent/live_review.md` 1163718 to 1169833, pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, N counted from the slice as 1 with units 717 to 718, a byte flipped in the appended paragraph rejected by BOTH readers; and all five ordered counts reproduce — registrations 306 unchanged, resolutions 249 unchanged, open set BY DISTINCT ID 57 unchanged, `^Gate: ` 40 to 41 and `^Gate: F272 R17 ` 0 to 1. The C3 append to `.agent/prose_slips.md` reproduces on the byte reader at 145313 to 146054. G3 THE PLAN is 2089 bytes byte-equal to its slice at 43 lines against the cap of 50. G4 THE FEATURE FILE reproduces exactly: the ACCEPTPAIR is a REWRITE by a containment test the reviewer RAN rather than judged, its FROM goes 1 to 0 and its TO 0 to 1, the D12 append satisfies `post == pre + NL + slice`, `^### DECISION F272 D` goes 11 to 12 with `D12` in exactly one heading, and the file moves 41411 to 47484 bytes and 639 to 662 lines — every one of those figures predicted by the reviewer BEFORE delegation and reproduced after. G5 THE INVENTORY is re-runnable and was re-run: the INVPROBE script extracted from the COMMITTED authored copy prints production 72, tests 127, scripts 0, total 199, with `save_job` 152, `load_job` 105, `JobNotFoundError` 45, `list_jobs` 6, `JobStoreError` 6, `load_job_safe` 5 and `list_jobs_safe` 5; all 199 entries appear in `.agent/f272_t004_deletion_inventory.md` with their paths AND their symbol lists, untruncated, and the file names the C4 commit `230c5f2c` as the commit its reading was taken at. G6 the docs-round gate EXIT 0 at 303 passed and the canary EXIT 0 at 42 passed. G7 integrity EXIT 0 with `"passed": true`, `"fail_count": 0`, `"check_count": 5`; no ruff was owed because no `.py` outside gitignored scratch was touched. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, thirteen worktree entries being the primary plus the twelve pre-existing `remedy/job-*`, and the local tip equal to `origin/feature/f272-one-world-completion`. THE SUBSTANCE OF THE ROUND IS UPHELD ON REVIEW. DECISION F272 D12 rules the 2026-09-06 triage the winner over this feature's own Acceptance sentence, which the reviewer independently confirmed reads "BOOK, do not build" for R-0803 through R-0812 in `.agent/live_review.md`; T003 is therefore COMPLETE, and the `job stop --status <prefix>` defect the ruling names was correctly NOT given an id because `- R-0809` is open and already describes it, which is §3 item 30 applied rather than quoted. The worker's three assumptions are accepted AS assumptions: the inclusive-of-terminal-newline reading of a slice, which the reviewer's own byte proofs confirm; the conservative Commit Gate reading at C0a and C0b; and one blank line added to its own C5 prose, which touched no probe output.
<<<END RECORDR19>>>
