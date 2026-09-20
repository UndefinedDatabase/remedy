# Handoff — F276 Data-root hygiene & disk budget · Round 7

## Session

SESSION 2 of feature F276 · round 7 · rounds so far 7

Context self-assessment: the worker verified the step block's bytes before doing anything else — 240 lines, sha256 `aed6c4a980dd4043f8eb1777275b928c3ace4eda4ffb7ac412aafa2a013e784a`, both readings identical to the digest the delegation message named — then read AGENTS.md in full, `docs/agents/handback_template.md`, the self-drive protocol's Phase 2 and its guardrails G1 to G8, all four payloads and the whole 172-line code diff end to end before applying a slice of it. Every numeral below is the output of a command run in this round, not a recollection; where two readings of the same thing disagree, both are printed with the reason.

## Range

Review of b9e55410..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 7 is the closure sequence's FIRST HALF. It books round 6's verdict, registers and repairs R-1006, writes the feature file's Built State, and runs this feature's one full suite.
- C1 books round 6's PASS over the five commits ending at `b9e55410`, registers R-1006, appends DECISION F276 D8, rewrites the plan, and saves byte copies of the four reviewer payloads.
- C2 repairs R-1006: the `remedy job budget` limits listing names `min_free_disk_bytes`, guarded over `JobBudgets.model_fields` so the SEVENTH limit reddens it too; plus the one `Landed:` line.
- C3 appends the Built State section to `docs/roadmap/features/T2_F276.md`, after C2 because it says R-1006 was repaired in this round.
- C4 is the integration gate's transcript. THE SUITE IS RED: `3 failed, 17636 passed, 20 skipped, 1 warning`, exit 1. Nothing was repaired, as the block orders.
- C5 is this handoff. No pull request was opened. The second half — integrity check, self-use item, evidence job, review package, ledger rotation, finding re-assignment, checklist consolidation, STATUS flip, PR — is round 8 and was NOT started.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | four payload copies + three state files; 413 insertions, 7 paths |
| C2 the R-1006 repair | done | three paths; the two new nodes ran green alone before the commit |
| C3 the Built State | done | one path, appended only; follows C2 as the block requires |
| C4 the integration gate | done | the run was made ONCE and its transcript committed; the RUN ITSELF IS RED |
| C5 handoff | done | this file |
| G1 transport + state | done | 7 readings, every one True; saved block matches the delegation digest |
| G2 code and docs transport | **partially red** | all three blob ids exact; the name-only clause reads 4 paths, not the 3 it demands — see Deviations |
| G3 the targeted suite | done | `718 passed in 188.41s`, exit 0, 0 failed |
| G4 ruff | done | `All checks passed!`, exit 0 |
| G5 the R-1006 red proof | done | control green; the mutation turned BOTH nodes red at exit 1; restored byte-identically |
| G6 push + clean tree | done | follows this commit; the reading is in the round report |
| R-1006 | registered at C1, repaired at C2, `Landed:` line written | NOT resolved: only reviewer-authored text sets a finding Resolved, and no `Done:` paragraph was written anywhere |
| R-1003 | resolved in round 6 | untouched this round |
| R-1004 | open | Medium, re-assigned to F282 by round 8; not fixed here |
| R-1005 | open | Medium, re-assigned to F282 by round 8; not fixed here |

## Commits

### f052b0fb F276 R7 C1: the round 7 bookkeeping

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r7-block.md | 240/0 | byte copy of the step block |
| .agent/authored/f276-r7-decisions.md | 49/0 | byte copy of the D8 payload |
| .agent/authored/f276-r7-ledger.md | 4/0 | byte copy of the ledger payload |
| .agent/authored/f276-r7-plan.md | 42/0 | byte copy of the plan payload |
| .agent/decisions.md | 49/0 | `b9e55410` bytes + the D8 payload |
| .agent/live_review.md | 4/0 | `b9e55410` bytes + the ledger payload: round 6's verdict and R-1006's registration |
| .agent/plan.md | 25/14 | rewritten to the plan payload |

Insertions 413 by `git show --numstat`. `git show --stat` prints 413 for the same commit, so both readings agree this round; round 6's divergence came from rewrite detection scoring a wholly-rewritten `.agent/plan.md`, and this round's plan rewrite shares enough lines with its predecessor that no rewrite was detected.

### d8779565 F276 R7 C2: the R-1006 repair

| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/commands/job.py | 9/0 | the floor's `if … is not None` print line in the labelled-limits block, listed last after `deadline`, with the comment stating why |
| tests/orchestration/test_job_budgets.py | 39/0 | `TestEveryConfiguredLimitIsNamedInTheTextOutput`: the universal over `JobBudgets.model_fields` and the narrow node pinning the floor's own value |
| .agent/live_review.md | 2/0 | one blank line and the one `Landed: R-1006` line the block quotes verbatim |

Insertions 50.

### 2eca3731 F276 R7 C3: the feature file's Built State

| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T2_F276.md | 97/0 | the `## Built State (F276, 2026-09-20)` section: T001 to T004 as built, the three import-reachability allowlist lines precondition 7 names, what became of each finding, and the deliberate absences |

Insertions 97. Appended only; nothing above the new section was touched.

### a5193724 F276 R7 C4: the integration gate's transcript

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-closure-suite.txt | 58/0 | exit code, the summary line verbatim, both durations, and the complete untruncated bad-node-id set |

Insertions 58.

### C5 — this handoff (self-reference)

| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | this file | a handoff cannot table the commit that writes it (R-0149 pattern); its own insertion count is in the round report |

## External actions

- `git worktree add --detach .remedy-wt/f276-r7-redproof 2eca3731` — created for G5 only; removed with `git worktree remove` as that step's last action.
- `git worktree list` after the removal shows exactly two entries: the primary checkout at `2eca3731` and `.remedy-wt/job-468c8e62a2cc4fac` at `1b9ae606`, which pre-existed this round and was never touched. Nothing was pruned; no branch was created or deleted.
- `git push origin feature/f276-data-root-hygiene` — follows this commit; its result is in the round report.
- No pull request was created, edited or merged. No `gh` command was run. Nothing was merged, amended, rewritten or force-pushed.

## Verification

- G1 transport + state — a python check printed 7 readings, every one True: each of the four `.agent/authored/f276-r7-*` files equals its payload byte for byte; `.agent/live_review.md` equals its `b9e55410` bytes + the ledger payload; `.agent/decisions.md` equals its `b9e55410` bytes + the decisions payload; `.agent/plan.md` equals the plan payload. R-0954, the two readings side by side — SAVED BLOCK `.agent/authored/f276-r7-block.md`: lines 240, sha256 `aed6c4a980dd4043f8eb1777275b928c3ace4eda4ffb7ac412aafa2a013e784a`; the delegation message's reading for P1: lines 240, sha256 `aed6c4a980dd4043f8eb1777275b928c3ace4eda4ffb7ac412aafa2a013e784a`. Identical. Exit 0. All five payload digests (`block.md`, `ledger.md`, `decisions.md`, `plan.md`, `f276-r7.diff`) were also verified against the block's stated values BEFORE any file was used, and all five matched.
- G2 code and docs transport — `git rev-parse` at C3 printed `apps/cli/commands/job.py` = `d3c2f9e24e5be1f9615099056330ecc29884a669`, `tests/orchestration/test_job_budgets.py` = `5f1e6e06ed1015895904079b3628f90fd46f8708`, `docs/roadmap/features/T2_F276.md` = `ec3ebeba3b9dbd8e13ce8ae99fb07a2143792388` — all three EXACTLY the objects the block names, so the committed files are byte-identical to the tree the reviewer dry-ran. `git diff --name-only f052b0fb 2eca3731` printed LENGTH 4, not 3: `.agent/live_review.md`, `apps/cli/commands/job.py`, `docs/roadmap/features/T2_F276.md`, `tests/orchestration/test_job_budgets.py`. The fourth path is the one the block's own C2 ordered written; see Deviations for the measurement that bounds it.
- G3 the targeted suite — `python3 -m pytest -q -p no:cacheprovider` over the block's six paths, serial, no `-n`, in the primary checkout: `718 passed in 188.41s (0:03:08)`, exit 0, 0 failed. Wall clock around the process 271.83s.
- G4 ruff — `python3 -m ruff check apps/cli/commands/job.py tests/orchestration/test_job_budgets.py` printed `All checks passed!`, exit 0.
- G5 the R-1006 red proof — one disposable worktree `.remedy-wt/f276-r7-redproof` at `2eca3731`, run from the worktree root with `python3 -B -m pytest -q --no-header -rf -p no:cacheprovider tests/orchestration/test_job_budgets.py::TestEveryConfiguredLimitIsNamedInTheTextOutput`. Import resolution: with cwd on `sys.path`, the way pytest imports, `apps.cli.commands.job` resolved to `/home/decodeux/Repos/remedy/.remedy-wt/f276-r7-redproof/apps/cli/commands/job.py` — inside the worktree, so no editable install shadowed it; a first probe that read the primary checkout instead is reported under Deviations with the reason. `__pycache__` directories found and removed: 0, in a freshly created worktree run under `python3 -B`. CONTROL, unmutated: `2 passed in 0.38s`, exit 0.
  - THE MUTATION. The target was DERIVED from the diff payload, never retyped: the last two added lines of the `apps/cli/commands/job.py` hunk, taken together with the newline between them and the newline after — 139 bytes, `            if _budgets.min_free_disk_bytes is not None:` and the `print` line beneath it. Occurrences of those exact bytes in the worktree's `job.py` before the edit: 1. Pre-mutation sha256 `5a0ddbd288e99aa5100ec6e07a9c917a646c99c83d93b6975012873e4e94d603`; after deleting them once, `bbc3b7553c09a22ea80a4ded58bc63b4f6400d416f5f4e30bdc74e05ff97e0a4`, 139 bytes removed.
  - RE-RUN, MUTATED: exit 1, `2 failed in 0.41s`. Failing node ids, both of them: `tests/orchestration/test_job_budgets.py::TestEveryConfiguredLimitIsNamedInTheTextOutput::test_every_field_of_job_budgets_is_named` and `tests/orchestration/test_job_budgets.py::TestEveryConfiguredLimitIsNamedInTheTextOutput::test_the_floor_prints_its_own_number`. The first read `Left contains one more item: 'min_free_disk_bytes'`, the second `assert None == '5000000000'` over an output holding only the `free_disk:` source line. TWO ASSERTIONS, TWO RED NODES: neither node is carried by the other.
  - NO MUTATION STAYED GREEN. Restored from the saved pre-mutation bytes; the restored file's sha256 read `5a0ddbd288e99aa5100ec6e07a9c917a646c99c83d93b6975012873e4e94d603`, identical to the pre-mutation reading. The worktree's own `git status --porcelain` was empty afterwards, and `git worktree list` after removal shows the two entries named under External actions. The mutation changing the outcome is also the independent proof that the test read the WORKTREE's copy of `job.py` and not the primary checkout's.
- G6 push + clean tree — follows this commit; the reading is in the round report.

## The integration gate — C4's own result

THE FULL SUITE IS RED. `python3 -m pytest -n auto -q`, run ONCE in the primary checkout at `2eca3731` with a clean tree, per amend0917-throughput rule 1. Exit code 1. Summary line verbatim: `3 failed, 17636 passed, 20 skipped, 1 warning in 232.32s (0:03:52)`; 317.10 seconds of wall clock measured around the process. BAD NODE IDS — 3, the complete set:

- `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_post_to_job_dashboard_is_405`
- `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_a_near_miss_of_the_commands_path_is_405`
- `tests/ui_server/test_live_state.py::TestUIServerIntegration::test_put_rejected`

pytest printed no ERRORS section, so there are no collection or teardown errors to add to that set. NOTHING WAS REPAIRED, which is what the block orders and what amend0917 rule 2 reserves for the next round. All three fail at one seam — `Failed: Server thread exited before publishing its info file` at `tests/ui_server/server_start.py:66`, under a captured `[remedy-ui] auto-build (dist missing)…` and `ERROR: React UI not built.` All three are in `tests/ui_server/`; none is in `tests/orchestration/`, `tests/cli/` or `tests/docs`, and none names any file F276 touched. That is a reading and not a verdict: what the three are is round 8's to decide, and the committed transcript exists so that round can be authored from a measured set.

## Open findings

17 by distinct id and 17 by the canonical formula `scripts/rotate_live_review.py::count_open_findings`, both measured on the working ledger at this commit, with no duplicate id in the raw list: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1004, R-1005, R-1006. By severity: 0 High, 9 Medium, 8 Low. Sixteen were open at `b9e55410`; the difference is R-1006, which C1's ledger append registers. R-1006 is repaired in code at C2 but stays OPEN by design: `git diff b9e55410 HEAD -- .agent/live_review.md` adds 0 lines beginning `Done:` and exactly 1 beginning `Landed:`, because only reviewer-authored text sets a finding Resolved.

## Authored-text proofs

All four reviewer payloads were copied with `shutil.copyfile` and never retyped; every digest was verified against the block's stated value before the file was used and again at G1. Disk-to-disk, as committed at C1 and re-read at G1 against the reviewer's originals under `.remedy-wt/f276-r7/`: `.agent/authored/f276-r7-block.md`, `-ledger.md`, `-decisions.md` and `-plan.md` each compare byte-equal to their payload; `.agent/live_review.md` and `.agent/decisions.md` each equal their `b9e55410` bytes plus their payload exactly; `.agent/plan.md` equals its payload. The one `Landed:` line was not retyped either — it was extracted programmatically from the block's own bytes, the extraction asserting that exactly one line in the block begins `Landed: R-1006`, and appended as those 157 bytes. The code and docs diff was applied with `git apply` in the block's two disjoint `--include` slices, each preceded by `git apply --check` with the same arguments; no hunk was retyped or edited. `git apply --stat` of the whole payload reads 3 files and 145 insertions, which is 9 + 39 across C2's slice plus 97 in C3's.

## Deviations & assumptions

- THE BLOCK'S COMMIT SEQUENCE WAS FOLLOWED EXACTLY: C1, C2, C3, C4, C5, no extra commit, none dropped, none reordered.
- **G2's NAME-ONLY CLAUSE IS UNMEETABLE AS WRITTEN, and it read 4 rather than 3.** The gate demands that `git diff --name-only <C1> <C3>` "must name exactly those three paths and no other". It names four, because the block's OWN C2 orders the `Landed:` line appended to `.agent/live_review.md` in the same commit as the code slice, and that path therefore falls inside the C1..C3 range by construction. The overage is bounded and measured, not argued: `git diff --numstat f052b0fb 2eca3731` reads `2 0 .agent/live_review.md`, and the full text diff of that path over the range is exactly one blank line plus the one `Landed:` line the block quotes verbatim — no other byte of the ledger changed between C1 and C3. G2's substantive claim is unaffected and CONFIRMED: all three blob ids are exactly the objects of the reviewer's dry run, so the committed code and docs are byte-identical to the tree the reviewer tested and red-proved. Reported here rather than routed around; nothing was withheld from the commits to make the count come out at 3.
- **THE INTEGRATION GATE IS RED AND WAS NOT REPAIRED.** Three failures, listed in full above and in the committed transcript. The block forbids repair in this round; no test was deleted, weakened, skipped or re-run, and the suite was run exactly ONCE as amend0917 rule 1 requires.
- G5's FIRST IMPORT PROBE READ THE PRIMARY CHECKOUT, and the reason is the probe's own form, not an editable install. Run as `python3 -B <script>` with the script living under `.remedy-wt/f276-r7/` in the PRIMARY checkout, `sys.path[0]` is the SCRIPT's directory, not the cwd, so the import resolved to `/home/decodeux/Repos/remedy/apps/cli/commands/job.py` and the reading printed False. Re-probed as `python3 -B -c` from the worktree root — `sys.path[0]` is `''`, which is how pytest also runs — it resolved to the worktree's own copy. Both readings are reported because the first one is exactly the shadowing hazard this gate exists to catch, and the honest answer is that it was the measurement that was wrong and not the tree. An editable install named `remedy` DOES exist at `~/.local/lib/python3.10/site-packages`; the mutation changing the test outcome is the independent proof that the run read the worktree.
- G3 WAS RUN TWICE, and both runs read `718 passed`, 0 failed. The first was piped to `tail`, which reports the pipeline's LAST exit code and would have let a pytest exit code of 1 go unseen; it was re-run through a wrapper that captures the process's real return code, which read 0. The re-run is extra work beyond the block's gate list and is reported as such. `188.41s` and `189.19s` are the two runs' in-band durations.
- C2's TWO NEW NODES WERE RUN ALONE BEFORE THE COMMIT, as the self-review loop's "what could break" step: `2 passed in 84.84s` in the primary checkout. Extra work beyond the block's gate list, reported as such. The same two nodes take 0.38s in a fresh worktree — R-1004's cost measured again in this round's own runs rather than restated.
- `.agent/authored/f276-closure-suite.txt` CARRIES ONE SECTION BEYOND THE FOUR ELEMENTS THE BLOCK MANDATES: a labelled quotation of the decisive captured output of the three failures. Nothing mandated was dropped — the exit code, the verbatim summary line, the duration and the untruncated bad-node-id list are all present — and the addition is quoted output of the ordered command, not a characterisation, because the first question round 8 must answer is whether the three are a defect of this feature or a posture of the checkout.
- `__pycache__` PURGING AT G5 REPORTED 0 DIRECTORIES both before and after. That is not a skipped step: the worktree was freshly created and every run used `python3 -B`, so no bytecode existed for the purge to find. The purge ran regardless.
- NO PATH OUTSIDE THE BLOCK'S CHANGE SET WAS TOUCHED. `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/candidates.md` are unchanged and remain round 8's. Every helper script this round used lives under `.remedy-wt/`, which `.gitignore:235` excludes, so none of it is committed.
- No test called a model provider, and nothing read, listed or wrote the operator's `.data` directory. The full suite of C4 is the repository's own suite, unchanged and unfiltered.

## Next

1. Phase 1 rule 1 — re-read `.agent/STOP` from disk; if it exists, write the handoff and end the session, doing nothing else.
2. Otherwise review round 7: re-run G1 to G6 independently and read `git diff b9e55410..HEAD` bottom-up, then book the verdict — including a ruling on G2's unmeetable name-only clause, which is a block-authoring reading and not a defect on disk.
3. Then decide what the integration gate's three red `tests/ui_server/` nodes are, from the committed transcript, and author round 8 accordingly: amend0917 rule 2 allows at most three repair rounds each strictly shrinking the bad set, and a checkout posture that reddens them is not repaired by weakening a test. The closure sequence's second half waits on that answer.

Operator questions open: 5
