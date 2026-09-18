# Handoff — F268 remedy do: the one-command start · Round 11 (closure: integration gate)

## Session

SESSION 2 of feature F268 · round 11 · rounds so far 11

## Range

Review of a70e66a8..HEAD — branch `feature/f268-remedy-do`.

## Summary

Round 11 is the integration-gate round of the closure sequence. It booked round 10's PASS and one prose slip (C1). It rewrote the three product-spine pins of the old quick start by design under DECISION F268 D15 (C2) and appended the feature file's Built State (C3). It then ran the full suite once in the primary checkout and committed its transcript (C4).

**Closure suite (C4), verbatim from `.agent/authored/f268-closure-suite.txt`:**

    3 failed, 17735 passed, 23 skipped, 1 warning in 149.83s (0:02:29)
    tests/orchestration/test_prompt_trace.py::TestSegmentManifest::test_every_cli_call_site_hands_its_composition_down
    tests/orchestration/test_prompt_trace.py::TestSegmentManifest::test_the_cli_recorder_passes_the_composed_prompt
    tests/orchestration/test_prompt_trace.py::TestSegmentManifest::test_the_cli_task_plan_recorder_passes_the_composed_prompt

Per the block, nothing was repaired after the run and the suite was not run again. All three failures are source-text pins on `apps/cli/commands/do_cmd.py`, read with `inspect.getsource`. The assertions that fail are `'make_intake_call_recorder' in <do_cmd source>` (test_prompt_trace.py:274), `'make_task_plan_call_recorder' in …` (:298) and `'composed=intake_composed,' in …` (:335). Those strings belonged to the `do` v1 wiring that rounds 9 and 10 removed. Classifying them (by design, or a lost behaviour) is for the next round.

- **C2:** there is a new module-level helper, `_quick_start_commands()`, which regex-reads the command of every numbered quick-start line in order, plus `_QUICK_START_SETUP = ("remedy init", "remedy doctor core")`.
  - `test_happy_path_starts_with_do` asserts that the first two commands equal the setup pair and that the first command outside that pair starts with `remedy do `.
  - `test_happy_path_has_job_show` is renamed `test_happy_path_lists_the_jobs`. It asserts `remedy job list` is a numbered command.
  - `test_happy_path_uses_do_run` asserts that some numbered command starts with `remedy do `.
  - Each new assertion is at least as strong as the old one: numbered-line membership replaces substring-anywhere, and an ordering of the setup lines was added.
  - In-memory red probe: three `_QUICK_START` mutations (a `job list` line before the first `do`; no `do` line and `job show` in place of `job list`) turned each of the three tests red.
- **Sweep:** `git grep -c _QUICK_START` at HEAD, untruncated. The code hits are `apps/cli/grouped.py:2`, `tests/cli/test_cli_ux.py:7`, `tests/cli/test_product_spine.py:8` and `tests/test_cli_execution_loop_closure.py:6`. The other hits are all under `.agent/**` plus `docs/roadmap/features/T2_F281.md:1`, all prose. This confirms the block's list.

## Commits

### 7f46f7a2 F268 R11 C1: bookkeeping — book round 10's verdict and a prose slip, round 11 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r11-block.md` | +73 / -0 | Byte copy of the block |
| `.agent/authored/f268-r11-built_state.md` | +50 / -0 | Byte copy of built_state.md |
| `.agent/authored/f268-r11-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f268-r11-plan.md` | +24 / -0 | Byte copy of plan.md |
| `.agent/authored/f268-r11-slips.md` | +1 / -0 | Byte copy of slips.md |
| `.agent/live_review.md` | +2 / -0 | `a70e66a8` bytes + ledger.md (Gate F268 R10 PASS) |
| `.agent/plan.md` | +7 / -6 | := plan.md |
| `.agent/prose_slips.md` | +1 / -0 | `a70e66a8` bytes + slips.md |

### 668d5d41 F268 R11 C2: pins — the three product-spine quick-start pins read the five lines of DECISION F268 D15, by design
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_product_spine.py` | +22 / -11 | Three pins rewritten, one renamed; `re` import and helper |

### 12f83da7 F268 R11 C3: Built State — the feature file records what exists on disk at the close of F268
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F268.md` | +50 / -0 | `a70e66a8` bytes + built_state.md |

### 322626a2 F268 R11 C4: the integration gate — the full suite run once, its summary line and three bad node ids committed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-closure-suite.txt` | +4 / -0 | Summary line + 3 sorted bad node ids |

### C5 (this commit) F268 R11 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines; the largest is C1 with 160.

## External actions

- `git push origin feature/f268-remedy-do` after C4: `a70e66a8..322626a2  feature/f268-remedy-do -> feature/f268-remedy-do`.
- `git push origin feature/f268-remedy-do` after C5 (this commit).
- No PR, worktree or gh action.

## Verification

G1 to G3 ran after C3 (at `12f83da7`) and before C4.

- **G1** — `python3 .remedy-wt/f268-r11/g1.py`, exit 0:
  - `ledger.md digest True authored-copy True`, and the same for `slips.md`, `plan.md`, `built_state.md` and `block.md`.
  - `live_review True`, `prose_slips True`, `T2_F268 True` (each file == `git show a70e66a8:<path>` + payload).
  - `plan True` (`.agent/plan.md` == plan.md).
  - `block digest 2795607532493b94860ee4ebddf4b6406a7823f873a2b05b3d4ba278b7fe1f81`.
- **G2** — the block's exact command, exit 0: `514 passed in 44.79s`.
- **G3** — `python3 -m ruff check tests/cli/test_product_spine.py`, exit 0: `All checks passed!`
- **G4** — `python3 -m pytest -n auto -q` in the primary checkout, run once and serially after C3 with no other pytest running:
  - Exit code 1.
  - Summary: `3 failed, 17735 passed, 23 skipped, 1 warning in 149.83s (0:02:29)`.
  - Bad-node count: 3 (listed under Summary).
  - The committed transcript `.agent/authored/f268-closure-suite.txt` has sha256 `43597e65d5d8c3d4667972b8a380c799d72622d23f02844f82e5c3acc2f4cf77`.
  - The raw log is at `.remedy-wt/f268-r11/closure-suite-raw.txt` (gitignored).
  - Wall time 2:29, under the ~5 min perf note.
- **G5** at `322626a2`, after the first push:
  - `git status --porcelain` printed nothing.
  - `git rev-parse HEAD origin/feature/f268-remedy-do` printed `322626a279021f6f3d9d20630d9c1ecd35aada01` twice.
  - `git worktree list` showed one row (`/home/decodeux/Repos/remedy  322626a2 [feature/f268-remedy-do]`).
  - The `remedy/job-*` branch count was `31` before C4 and `31` after it.
  - The same checks run again after the C5 push, and the round report carries that run.

## Authored-text proofs

- All four payload digests (`ledger.md`, `slips.md`, `plan.md`, `built_state.md`) and the block's own digest matched before use.
- Byte copies are at `.agent/authored/f268-r11-{block,built_state,ledger,plan,slips}.md`. Each is byte-equal to its payload (G1).
- `.agent/authored/f268-r11-block.md` sha256: `2795607532493b94860ee4ebddf4b6406a7823f873a2b05b3d4ba278b7fe1f81`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `7f46f7a2` |
| C2 pins | done | `668d5d41` |
| C3 Built State | done | `12f83da7` |
| C4 integration gate | done | `322626a2`; the run is red, 3 nodes, not repaired (per block) |
| C5 handoff | done | This commit |

## Open findings

125 open by distinct id, from `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 15 `Done:` ids. This is unchanged from round 10; this round opens and resolves no finding.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, C4, C5). No repair commit was needed, because G1 to G3 were green.
- **Pushed before the handoff.** C1 to C4 were pushed before C5 so that G5 could be read with real output (the round 10 precedent). C5 is pushed after.
- **Transcript format:** the summary line is exactly as pytest printed it, followed by the node ids alone (without the `FAILED ` prefix), sorted. There were no ERROR nodes.
- **The shell guard refuses `$?`,** so exit codes are the tool's own report: a non-zero exit surfaces as an error, and only G4 did so, with exit code 1.

## Next

Reviewer: review round 11 and book its verdict. The closure suite is red on 3 nodes in `tests/orchestration/test_prompt_trace.py::TestSegmentManifest`, so the next round is repair round 1 of at most three (amend0917-throughput (2)). The repair classifies the three `do_cmd.py` source pins against the deleted `do` v1 wiring.
