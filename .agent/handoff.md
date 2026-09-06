# Handoff — F260 One world · round 11 · ONE SPELLING FOR THE RUN STORE

## Session

SESSION 3 of feature F260 · round 11 · rounds so far 11

Context self-assessment (amend0905-throughput): context is comfortable — this
round read four protocol files, one 399-line block and roughly 900 lines of
target source, and spent no rounds on rework. The one long wait was the
`tests/orchestration/` suite at 12m13s, which costs wall clock and not context.
More delegated rounds fit in this session.

## Range

Review of `2cedf98c9fbc85c90c85a3ed45cfd257164c7361`..`HEAD`.

Nine commits, all single-parent. The block's ordered sequence C0a → C7 has EIGHT
slots; this round used nine commits because SPEC (4) — the two new tests in
`tests/test_data_paths.py` — is assigned to NO commit anywhere in the Bundle.
It landed as an extra commit, recorded below as C6b and declared under
Deviations. No reordering, no dropped commit. Largest insertion count 399
(`.agent/authored/f260-r11.md`, a single `.agent/**` state write and exempt under
the AGENTS.md DECISION F104 D1 counting rule); largest CODE commit 97
(`efbc0164`, the test sweep). Nothing approached the 500-insertion cap, so C6
was not split.

## Commits

### aad539d1 f260: save the round 11 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r11.md | +399 / -0 | C0a — the block copied byte-for-byte with `shutil.copyfile`, verified by `filecmp.cmp(shallow=False)` before staging |

### 68335324 f260: mirror the round 11 step block into the last block file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +310 / -231 | C0b — same bytes, same copy route, same byte-equality check |

### 966ec420 f260: point the plan at one spelling for the ping-pong run store
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -21 | C1 — whole-file replacement by the PLAN slice plus one trailing newline; 47 lines, under the 50-line cap |

### c242d663 f260: book the round 10 PASS verdict into the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — GATE_R10 appended; 912232 → 918017 bytes |

### 36f61fa4 f260: append the two round 10 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +4 / -0 | C3 — SLIP7 and SLIP8 appended; 105750 → 108734 bytes |

### d497fedf f260: record DECISION D5 moving the resolver collapse to T004
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +47 / -1 | C4 — DECISION_D5 APPENDED; the −1 is the pre-image's last line gaining its terminating newline, because this file ended WITHOUT one (see Deviations) |
| docs/roadmap/features/T2_F260.md | +46 / -0 | C4 — DECISION_D5 INSERTED at byte offset 15662, between DECISION F260 D4 and the `## Design` heading |

### 1ab21212 f260: give the ping-pong run store one spelling in data paths and delete the loop helper
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/data_paths.py | +23 / -0 | C5 SPEC (1) — the `pingpong_runs_dir` / `pingpong_run_dir` pair, its WHY comment, and two `Public API::` lines |
| packages/orchestration/pingpong_loop.py | +18 / -20 | C5 SPEC (2) — `_pingpong_runs_dir` DELETED; 11 uses moved; the misleading local `runs_dir` → `pp_runs_root` in `list_runs` |
| packages/orchestration/job_evidence.py | +15 / -15 | C5 SPEC (2) — 13 references moved, incl. the `_pp_runs` alias; the misleading local `runs_dir` → `pp_runs_root` |
| packages/orchestration/pingpong_promote.py | +5 / -4 | C5 SPEC (2) — 4 references moved |
| packages/orchestration/worktree_resume.py | +7 / -6 | C5 SPEC (2) — 4 references moved; the misleading local `runs_dir` → `pp_runs_root` |
| packages/orchestration/pingpong_evidence.py | +2 / -2 | C5 SPEC (2) — 2 references moved |
| packages/orchestration/repair_attest.py | +2 / -2 | C5 SPEC (2) — 2 references moved |
| apps/cli/commands/do_cmd.py | +2 / -2 | C5 SPEC (2) — 2 references moved |

### efbc0164 f260: move the test references onto the one spelling for the ping-pong run store
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_pingpong_promote.py | +46 / -46 | C6 SPEC (3) |
| tests/orchestration/test_job_evidence.py | +8 / -8 | C6 SPEC (3) |
| tests/orchestration/test_failure_wiring.py | +4 / -4 | C6 SPEC (3) |
| tests/orchestration/test_worktree_safety.py | +4 / -4 | C6 SPEC (3) |
| tests/orchestration/test_job_worktree_integration.py | +3 / -3 | C6 SPEC (3) |
| tests/orchestration/test_pingpong_cli.py | +3 / -3 | C6 SPEC (3) |
| tests/orchestration/test_worktree_isolation.py | +3 / -3 | C6 SPEC (3) |
| tests/orchestration/test_stream_export_e2e.py | +2 / -3 | C6 SPEC (3) — the only file where the counts differ, because two `data_paths` imports merged into one line |
| tests/orchestration/test_job_worktree_handoff.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_job_worktree_integrity.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_persisted_call_episode_membership.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_persisted_call_ownership.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_persisted_run_call_schema.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_repair_loop.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_run_manifest_ledger_semantics.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_run_manifest_task_lifecycle_binding.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_run_manifest_zero_call_expectations.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_worktree_lifecycle.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_worktree_persistence.py | +2 / -2 | C6 SPEC (3) |
| tests/orchestration/test_worktree_resume_cli.py | +2 / -2 | C6 SPEC (3) |

### 2be351cc f260: guard the one spelling and the deleted run dir helper
| Path | +/- | Reason |
|---|---|---|
| tests/test_data_paths.py | +65 / -0 | C6b — SPEC (4) tests (A) and (B), both inside `TestJobAndRunLayout`; the Bundle assigns this work no commit (declared) |

### C7 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C7 — a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/r11-mut 2be351cc` | created, detached HEAD at `2be351cc` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r11-mut` | removed |
| `git worktree prune` | exit 0; `git worktree list` shows only the primary checkout and the eleven pre-existing `remedy/job-*` worktrees |
| `git push -u origin feature/f260-one-world` | see the Verification transcript below |

No PR created. No PR merged. No `gh` command run. No force push. No branch deleted.

## Verification

ONE LINE PER GATE, with its real exit code.

| Gate | Command / reading | Exit | Result |
|---|---|---|---|
| G1 | `sha256sum .agent/authored/f260-r11.md .agent/last_block.md` | 0 | both `e2dc8680811953e9119c64eaabd552bdfe5285bafef7bba74b5644a84b777fac`, equal to the digest named in the delegation |
| G2(a) | exact-image equality of `.agent/live_review.md` | 0 | `post == pre + b"\n" + GATE_R10 + b"\n"` is True; 912232 + 1 + 5783 + 1 = **918017** measured bytes |
| G2(b) | structural, split on `"\n\n"` | 0 | units **430 → 431**; last unit with its terminating newline stripped EQUALS GATE_R10; it carries exactly one newline |
| G2(c) | negative control | 0 | byte at offset 912333 flipped (`E`→`e`) INSIDE the appended paragraph: (a) rejects, (b) rejects; after restore both accept |
| G2(d) | counts after C2 | 0 | `^Gate: ` **20**, all distinct · registrations **299** over **299** distinct ids · `^Done: ` **5** lines over **3** distinct ids · open set **296** by distinct id |
| G3 | exact-image equality of `.agent/prose_slips.md` | 0 | `post == pre + b"\n" + SLIP7 + b"\n\n" + SLIP8 + b"\n"` is True; 105750 → **108734** bytes; blank-line units **137 → 139**, a rise of exactly TWO |
| G4(a) | `.agent/plan.md` | 0 | equals the PLAN slice plus exactly one trailing newline (True); **47 lines**, 2468 bytes, under the 50-line cap |
| G4(b) | whole-file identity of `docs/roadmap/features/T2_F260.md` | 0 | `post == pre[:15662] + ins + pre[15662:]` is True. `off` = **15662 bytes** (15565 characters — see Deviations), inserted length **3022** bytes (the 3020-byte slice with one leading and one trailing newline). D5 text occurs **exactly once**; file still ends with exactly one newline; `^### DECISION F260 D` matches **6** times, D0/D1/D2/D3/D4/D5 each exactly once; byte offsets D4 **13191** < D5 **15663** < `## Design` **18685** |
| G4(c) | `.agent/decisions.md` | 0 | the D5 text occurs **exactly once**; 836338 → 839361 bytes |
| G5(a) | attribute readings | 0 | `hasattr(pingpong_loop, "_pingpong_runs_dir")` = **False**; non-vacuity control `hasattr(data_paths, ...)` = **True** for BOTH `pingpong_runs_dir` and `pingpong_run_dir` |
| G5(b) | AST over 1030 tracked `.py` files under `packages/`, `apps/`, `tests/` | 0 | `_pingpong_runs_dir` (Name + Attribute + alias + FunctionDef/AsyncFunctionDef/ClassDef) = **0**, in zero files. NON-VACUITY: the same reading over `pingpong_run_dir` = **138** in 29 files. CAN-FAIL CONTROL re-measured at the base by the worker: at `2cedf98c` the same reading over `_pingpong_runs_dir` = **135** in 27 files |
| G5(c) | the literal `pingpong_runs` | **FAILS AS WORDED** | see Deviations — reported, not asserted. Raw substring: **51** occurrences in **13** files. AST string-constant `== "pingpong_runs"`: **17** in **9** files. Under `packages/` + `apps/` ONLY (367 files): **exactly 1**, at `packages/orchestration/data_paths.py:216` |
| G5(d) | value reading, `REMEDY_DATA_DIR` at a scratch dir | 0 | `pingpong_run_dir(r) == pingpong_runs_dir() / r` True; `pingpong_runs_dir(arg) == arg/"pingpong_runs"` True; `pingpong_run_dir(r,arg) == arg/"pingpong_runs"/r` True; neither answered from the env root; nothing created on disk |
| G6 (1) | `pytest tests/test_data_paths.py -q -p no:randomly` | **0** | **48 passed** in 0.68s |
| G6 (2) | `pytest tests/orchestration/ -q -p no:randomly` | **0** | **12805 passed, 10 skipped**, 1 warning in 733.13s |
| G6 (3) | `pytest tests/cli/test_golden_path.py -q -p no:randomly` (canary) | **0** | **42 passed** in 20.95s |
| G6 (4) | `pytest tests/docs/ -q -p no:randomly` (run AFTER C4) | **0** | **303 passed** in 0.49s |
| G6 (5) | `python3 -m apps.cli.grouped integrity check --json` | 0 | `"passed": true`, `"fail_count": 0`, `"check_count": 5` |
| G7(i) | control in `.remedy-wt/r11-mut` at `2be351cc`, `python3 -B` | **0** | **48 passed**. Module resolution CONFIRMED from that worktree before any colour was trusted: `data_paths.__file__` and `pingpong_loop.__file__` both under `/home/decodeux/Repos/remedy/.remedy-wt/r11-mut/`. `__pycache__` dirs present: **0** |
| G7(ii) | `pingpong_run_dir` made to ignore its `root` argument | **1** | **1 failed, 47 passed** — the failure is exactly test (A) `test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir`, at the `arg_root` assertion. Revert target `    return pingpong_runs_dir(root) / run_id` verified to occur **exactly once** in `packages/orchestration/data_paths.py` before editing |
| G7(iii) | `_pingpong_runs_dir` revived in `pingpong_loop` as an UNCALLED `def` | **1** | **1 failed, 47 passed** — the failure is exactly test (B) `test_pingpong_loop_has_no_runs_dir_helper_at_all`. Anchor `def _persist_run(result: PingPongResult) -> Path \| None:` verified **exactly once** before editing. WHICH READING CATCHES IT, measured while the mutation was live: `hasattr` → True (**catches**); `_names_of` → 1 (**catches**), of which the FunctionDef arm supplies **1** at line 4233 and the reference-only arm supplies **0** (**blind**) |
| G7(iv) | restore after EACH mutation | 0 | after (ii): control **48 passed**, exit 0, `git status --porcelain` in that worktree EMPTY. After (iii): revert target verified exactly once, `git status --porcelain` and `git diff --stat` in that worktree both EMPTY, control **48 passed**, exit 0 |
| G8 (lint) | `python3 -m ruff check <the 29 paths this round edited>` | **0** | `All checks passed!` |
| G8 (tree) | `git status --porcelain` / `git ls-files .remedy-wt` | 0 / 0 | both EMPTY |

Base redness confirming G8's file-scoping is necessary, not a dodge:
`python3 -m ruff check tests/orchestration/` exits **1** with **11** pre-existing
I001 errors, none of them in any of the 20 files this round edited
(`test_checkpoints`, `test_dag_schedule`, `test_gauntlet_matrix`,
`test_gauntlet_runner`, `test_long_run_executor` ×2, `test_mission_compiler`,
`test_predictive_budget`, `test_prompt_trace` ×2 and one more in that set).

The push runs AFTER this file is committed, so its transcript cannot appear in
the commit that carries it (the R-0149 self-reference pattern, same reason the
C7 row of the commit table has no `+/-`). Its outcome is verifiable directly:
`origin/feature/f260-one-world` points at the C7 commit.

## Authored-text proofs

| Slice | Target | Shape | Proof |
|---|---|---|---|
| the whole block | `.agent/authored/f260-r11.md` | file copy | `shutil.copyfile`, then `filecmp.cmp(shallow=False)` = True, then sha256 equal to the delegation digest |
| the whole block | `.agent/last_block.md` | file copy | same route, same two proofs |
| PLAN | `.agent/plan.md` | whole-file REWRITE | disk bytes `== slice + "\n"`, True |
| GATE_R10 | `.agent/live_review.md` | APPEND | exact-image equality + structural + negative control (G2) |
| SLIP7, SLIP8 | `.agent/prose_slips.md` | APPEND | exact-image equality (G3) |
| DECISION_D5 | `docs/roadmap/features/T2_F260.md` | INSERTION | whole-file identity at `off` = 15662 (G4(b)) |
| DECISION_D5 | `.agent/decisions.md` | APPEND | exact-image equality; occurs exactly once |

Every slice was extracted from the COMMITTED `.agent/authored/f260-r11.md` by
taking the lines strictly between its marker lines, joined by `"\n"`, with no
trailing newline. No marker line reached any file.

## Deviations & assumptions

**1. G5(c) IS UNMEETABLE AS WORDED, under every reading. DECLARED, NOT REPAIRED.**
The gate says the literal `pingpong_runs` occurs under `packages/`, `apps/` and
`tests/` "ONLY inside `packages/orchestration/data_paths.py`". It cannot: the
IDENTIFIER this round introduces, `pingpong_runs_dir`, CONTAINS that literal, so
every module that imports the new name is a hit by construction. Measured after
the sweep: raw substring **51** in **13** files; AST string-constant reading
**17** in **9** files. Neither is one file. This is the same class of mistake the
gate's own note warns about ("Round 9's G5(c) was exactly that mistake") — round
9 wrote an unmeetable zero, round 11 wrote an unmeetable one. Nothing was
reshaped to make it go green; the gate's operative half ("report the count and
the file list rather than asserting a total") was obeyed literally, above.
THE PROPERTY THAT IS TRUE AND IS THIS ROUND'S DELIVERABLE: over the 367 tracked
`.py` files under `packages/` and `apps/`, the string constant `"pingpong_runs"`
occurs **exactly once**, at `data_paths.py:216`. Every other production mention
is a docstring, a comment or the identifier itself. Suggested wording for a
future round: "the string CONSTANT `"pingpong_runs"` occurs exactly once under
`packages/` and `apps/`, in `data_paths.py`".

**2. OBSERVED, NOT FIXED — fourteen hand-spelled `"pingpong_runs"` literals under `tests/`.**
Falling out of deviation 1: `tests/cli/test_task_input.py` (2),
`tests/orchestration/test_evidence_bundle.py` (2), `test_failure_postmortem.py`
(1), `test_failure_wiring.py` (4), `test_job_stop_integration.py` (2),
`test_manual_completion_bundle.py` (1) and `test_pingpong_cli.py` (2) build the
run-store path BY HAND — the test-side twin of the defect R-0814 named in
production. Five of those seven files hold NO `_pingpong_runs_dir` reference, so
SPEC (3) never reached them and constraint 2 forbids writing to them; the other
two are in scope for SPEC (3) but SPEC (3) orders only that REFERENCES move, not
that literals go. Left untouched deliberately. The two literals in
`tests/test_data_paths.py` are MINE and deliberate: test (A) pins the layout the
same way `test_the_root_override_is_honoured_by_all_four` pins `"jobs"` and
`"runs"`.

**3. THE BUNDLE ASSIGNS SPEC (4) NO COMMIT.** C5 is "SPEC (1) and (2)", C6 is
"SPEC (3)", and SPEC (4) — the two new tests — appears in the change set
(`tests/test_data_paths.py`) but in no Bundle slot. It landed as a ninth commit,
`2be351cc`, after C6. This is a departure from the block's ordered commit
sequence and is recorded here as the handback template requires, not only in the
commit table.

**4. G4(b)'S "MEASURED AT THE BASE FOR YOU" OFFSETS ARE CHARACTER OFFSETS, NOT BYTE OFFSETS.**
The gate orders a BYTE offset and then hands over "D4's heading is at offset
13104 and `\n## Design` at 15565". Measured at `2cedf98c`: those are the
CHARACTER (code-point) offsets. The BYTE offsets are **13191** and **15662** —
the file carries multi-byte em-dashes and arrows. A worker reporting the byte
`off` of 15662 against the stated range would look out of bounds. Both readings
are reported above, and the gate's real property (D4 < D5 < `## Design`) holds
under both. Nothing was changed to accommodate this.

**5. CONSTRAINT 4 SAYS "BOTH `.agent/` APPENDS"; THERE ARE THREE.** It names
`.agent/live_review.md` (912232 bytes) and `.agent/prose_slips.md` (105750
bytes), both verified to end in exactly one newline. C4 appends into a THIRD
`.agent/` file, `.agent/decisions.md`, which the constraint does not cover and
which at `2cedf98c` ended at **836338 bytes with NO trailing newline** (terminal
byte `.`). Per the constraint's own instruction to derive each recipe from its
own target's terminal byte, that append used `pre + b"\n\n" + D5 + b"\n"` — two
newlines to open the blank-line separator the file's other entries use, one to
close it. That is why the C4 numstat reads `+47 / -1` for a pure append: the
pre-image's final line gained its terminator.

**6. `cmp` AND THE `remedy` CONSOLE SCRIPT ARE DENIED IN THIS SANDBOX.** The
block and the delegation both order `cmp` for the C0a/C0b byte comparison. It is
refused here, so the byte-for-byte comparison was made with
`filecmp.cmp(shallow=False)` — the same property, a full byte comparison, not a
stat comparison — and backed by sha256 on both files. `remedy` was invoked as
`python3 -m apps.cli.grouped` and `ruff` as `python3 -m ruff`, as the delegation
directs.

**7. THE RECORD I APPENDED AT C2 CONTAINS A NUMERAL THAT DOES NOT DESCRIBE
`tests/test_data_paths.py`.** GATE_R10 states "THE SUITES, re-run serially by the
reviewer, all exit 0 at 59, 1537 and 203". Measured this round:
`tests/test_data_paths.py` collects **48** at `2be351cc`, and
`git diff --numstat 2cedf98c..HEAD -- tests/test_data_paths.py` is `65 0` from a
single commit that adds exactly two test functions — so the file collected
**46** at the base, not 59. Likewise this round's `tests/orchestration/` run
collects **12805**, not 1537. The slice was applied BYTE FOR BYTE as constraint 1
requires and is NOT repaired; the discrepancy is declared here so the reviewer
can decide whether round 10's three suites were a different selection or whether
the record needs a correction round.

**8. G7(iii)'s FRAMING IS SLIGHTLY OFF, AND THE MEASUREMENT IS REPORTED
INSTEAD.** The gate says to "note which of its two readings catches it: a `def`
is invisible to a reference-only reading". Measured: BOTH of test (B)'s readings
catch the revived `def` — `hasattr` finds it because a `def` becomes a module
attribute, and `_names_of` finds it through its FunctionDef arm. The reading that
is blind is the reference-ONLY reading (`_references_to`), which returned **0** —
and which test (B) deliberately does not use alone. The gate's point stands; its
wording implies only one of (B)'s two readings fires, and in fact both do.

**9. G2(c)'S NEGATIVE CONTROL WAS RUN IN MEMORY.** The gate says to flip a byte,
confirm both readings reject, then restore. The flip and both restores were
performed on `bytes` objects in the checking process rather than by writing a
corrupted image to `.agent/live_review.md` and back, so the primary checkout was
never left holding known-bad bytes (self-drive G5). The property measured is
identical: offset 912333, `E` → `e`, inside the appended paragraph; (a) and (b)
both reject the flipped image and both accept the restored one.

**10. NO `__pycache__` PURGE WAS NEEDED, AND THAT WAS VERIFIED RATHER THAN
ASSUMED.** The delegation orders a purge before the mutation work. The freshly
created worktree contained **0** `__pycache__` directories (enumerated, not
assumed) and every run used `python3 -B`, which writes none. No deletion was
performed, so the "never delete by glob" rule was not exercised.

**Assumption, stated:** SPEC (2) says to follow each file's existing convention
for where `data_paths` is imported. Read at the base: `pingpong_loop` already
imports `data_paths` AT MODULE LEVEL (`mint_run_id`, line 33), so the pair joined
that import; `job_evidence`, `pingpong_promote`, `worktree_resume`,
`pingpong_evidence` and `do_cmd` import `data_paths` inside function bodies, so
the pair was imported function-locally there. `repair_attest` has a module-level
`data_paths` import but its `_pingpong_runs_dir` use sat inside a function-local
`try:`; the function-local form was kept there, because moving it to module level
would have changed WHEN the import runs inside a `try` that exists to swallow
failures.

**Not a deviation, recorded because it was checked:** the evidence-owning guard
`test_no_module_that_owns_job_evidence_spells_the_path_itself` was read before
editing. It matches on the RESOLVED name `jobs_dir` via `_references_to`, so
`pingpong_runs_dir` and `pingpong_run_dir` are correctly invisible to it, and
`job_evidence`, `repair_attest` and `do_cmd` took the new import safely. The
guard was not weakened; it is green in G6 (1).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 PLAN slice | done | |
| C2 GATE_R10 append | done | |
| C3 SLIP7 + SLIP8 append | done | |
| C4 DECISION_D5 (both targets) | done | |
| C5 SPEC (1) the pair | done | |
| C5 SPEC (2) the 39-reference sweep + 3 local renames | done | 39 measured, 39 moved; all three locals renamed to `pp_runs_root` |
| C6 SPEC (3) the 97-reference test sweep | done | not split — 97 insertions, far under the cap |
| SPEC (4) the two new tests | deviated | the Bundle assigns it no commit; landed as the extra commit `2be351cc` (deviation 3) |
| C7 handback | done | this file |
| G1 transport | done | pass |
| G2 the record | done | pass, all four parts |
| G3 the slips | done | pass |
| G4 plan + decision | done | pass, all three parts |
| G5 the spelling | deviated | (a), (b), (d) pass; (c) is unmeetable as worded — reported, not asserted (deviation 1) |
| G6 the suites | done | pass, all five readings |
| G7 mutation red-proof | done | pass, both mutations red on exactly the intended test, both restored |
| G8 lint + clean tree | done | pass |

## Reference counts — the block's checklist versus my own measurement

Production, measured at `2cedf98c`: `pingpong_loop.py` 12 (incl. the
definition), `job_evidence.py` 13, `pingpong_promote.py` 4, `worktree_resume.py`
4, `pingpong_evidence.py` 2, `repair_attest.py` 2, `do_cmd.py` 2 — **39**, in
seven modules. IDENTICAL to the block.

Tests, measured at `2cedf98c`: 46 · 8 · 4 · 4 · 3 · 3 · 3, then thirteen files at
2 — **97** across **20** files, all under `tests/orchestration/`. IDENTICAL to
the block's checklist, file by file. (The delegation prose said "roughly 95"; the
block's own per-file list sums to 97, and 97 is what is on disk.)

The three misleading locals were re-grepped before editing, as §3 item 9
requires. All three line numbers held at `2cedf98c`: `worktree_resume.py:136`,
`job_evidence.py:1498`, `pingpong_loop.py:4271`.

## Open findings

**296** by DISTINCT ID, measured after C2 (299 registrations over 299 distinct
ids, minus 3 distinct ids carrying a `Done:` line). No finding was registered or
resolved by this round.

## Next

Review this round: read `git diff 2cedf98c..HEAD` bottom-up, re-run the eight
gates independently, and rule on the ten declared deviations — deviation 1
(G5(c) unmeetable), deviation 3 (SPEC (4) has no commit slot) and deviation 7
(the round-10 suite numerals in the record I just appended) are the three that
need a verdict rather than an acknowledgement. Before AUTHORING the next round,
re-read `.agent/STOP` from disk (Phase 1 rule 1, then rule 2). The next step the
plan names is the run MOVE itself: `pingpong_runs_dir` / `pingpong_run_dir`
collapse into `runs_dir` / `run_dir`, with the run LOG at
`<data_root>/runs/<job_id>/` moving to the run id in the SAME commit, or
`timeline.load_run_events` reads a directory keyed two ways (DECISION F260 D0).
