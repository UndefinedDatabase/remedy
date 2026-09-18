# Handoff — F269 Contract & contract templates · Round 3 (T003 templates)

## Session

SESSION 1 of feature F269 · round 3 · rounds so far 3

Context self-assessment: the round fit in one worker context with room to spare; every gate below was run in this session at C4 `5a384d0c`, none carried over from memory.

## Range

Review of b487e3f7..HEAD — branch `feature/f269-contract`.

## Summary

Round 3 lands T003's template half under DECISION F269 D1:

- C1 books round 2's verdict (ledger), appends DECISION F269 D1, writes the round 3 plan, and saves the payloads and the block.
- C2 ships the four templates under `docs/contracts/`, byte-exact, and registers them in `docs/README.md`.
- C3 adds `packages/orchestration/contract_templates.py`: list, load and validate (every D1 violation refused with `<file>:<line>`), compile through `mission_contract.compile_contract_criteria` (a `check:` line becomes the criterion's check), the deterministic proposal, and the writer onto a mission with no contract.
- C4 wires `remedy do --contract <name>`: the flag leaves `_DO_FLAGS_NOT_YET_AVAILABLE`, an unknown name exits 2 naming the templates before any step, and the plan step writes the forced or proposed template onto the new mission before `plan_mission`.
- C5 is this handoff.

## Commits

### ef80afa6 F269 R3 C1: bookkeeping — round 2 verdict, DECISION F269 D1, the round 3 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r3-block.md` | +102 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r3-decisions.md` | +38 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r3-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r3-plan.md` | +28 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +38 / -0 | `b487e3f7` bytes + decisions.md (D1) |
| `.agent/live_review.md` | +2 / -0 | `b487e3f7` bytes + ledger.md (Gate F269 R2 PASS) |
| `.agent/plan.md` | +8 / -9 | := plan.md |

### 0375029c F269 R3 C2: the four contract templates under docs/contracts, registered in the docs index
| Path | +/- | Reason |
|------|-----|--------|
| `docs/README.md` | +13 / -0 | Quick-Find row "contract templates" (after "context"); new `## Contract Templates (`docs/contracts/`)` section before `## Roadmap` with a File \| Description table, one row per template |
| `docs/contracts/api-service.md` | +26 / -0 | := api-service.md payload |
| `docs/contracts/cli-tool.md` | +25 / -0 | := cli-tool.md payload |
| `docs/contracts/python-library.md` | +24 / -0 | := python-library.md payload |
| `docs/contracts/website.md` | +25 / -0 | := website.md payload |

### a9f5b7d4 F269 R3 C3: the contract template loader, its compile through F061's compiler, and the deterministic proposal from the order
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/contract_templates.py` | +272 / -0 | NEW. `CONTRACT_TEMPLATES_DIR` (= `docs/contracts/` beside `packages/`), `list_contract_templates`, `parse_contract_template`, `load_contract_template`, `compile_contract_template`, `propose_contract_template`, `write_template_contract`, `ContractTemplateError` |
| `tests/orchestration/test_contract_templates.py` | +213 / -0 | NEW. 19 tests: the directory and the four names; each shipped template loads and its fixture order proposes it (4); bare and tied orders propose nothing; phrase boundaries; compiled website = `C001`..`C004`, origin `template`, whole-mission, file blocking flags, checks `ctr-<id>` valid as `DoDCheck`; unknown name refused naming the four; `check:` line compiles to that check; five parametrized D1 violations naming their line (wrong title, unknown section, malformed bullet, invalid check, no criteria); upper-case phrase and two fixture paragraphs refused; writer onto a fresh mission; a mission with a contract refused and left unchanged |

### 5a384d0c F269 R3 C4: remedy do --contract forces a template, the plan step applies the proposed one, and a name that is no template exits 2
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +1 / -1 | `do.run --contract` help: forces a template as the floor of the mission's acceptance criteria, names the four |
| `apps/cli/commands/do_cmd.py` | +18 / -3 | `--contract` row removed from `_DO_FLAGS_NOT_YET_AVAILABLE`; `_cmd_do` exits 2 on a name that is no template, before any step; `_cmd_do_order(contract=)` → `DoContext.contract_template` |
| `docs/guides/do-run-v1.md` | +7 / -4 | The `plan` row and the flags list: `--contract` is no longer "not yet available" (deviation 1) |
| `packages/orchestration/do_sequence.py` | +32 / -3 | `DoContext.contract_template`; `_step_plan` writes the forced or else proposed template onto the new mission before `plan_mission`; the detail ends `; contract template <name>, forced by --contract` / `, proposed from the order` / `; no contract template, none proposed from the order` |
| `tests/cli/test_do_sequence_cli.py` | +75 / -4 | The `--contract` case removed from `NOT_YET_AVAILABLE` (the one deletion D1 orders); `_recorded_contract` takes the expected origin set (default `{"planner"}`, so its existing caller keeps its property); 4 new tests: `--contract website` on the bare order, `--contract website` with one extra requirement, the website fixture order proposing `website` without the flag, `--contract nosuch` exit 2 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 | Regenerated from `reachable_closure()`: `packages.orchestration.contract_templates` |

### C5 (this commit) F269 R3 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

## External actions

- `git worktree add --detach .remedy-wt/f269-r3-g4 5a384d0c` for G4; removed with `git worktree remove .remedy-wt/f269-r3-g4` (exit 0); `git worktree list` afterwards: `/home/decodeux/Repos/remedy  5a384d0c [feature/f269-contract]`.
- `git push` runs after this commit; its outcome and G5 are in the worker's final report.
- No PR created, edited or merged.

## Verification

All gates ran at C4 `5a384d0c` with a clean tree, through the helper scripts in `.remedy-wt/f269-r3/` (exit codes are subprocess return codes).

G1 transport + state, `python3 .remedy-wt/f269-r3/g1.py`, exit 0:
```
digests True
templates True plan True live_review True decisions True authored True
True
```

G2, `python3 -m pytest -q -p no:cacheprovider` over the block's 14 paths (the two test files this round created or edited, `tests/orchestration/test_contract_templates.py` and `tests/cli/test_do_sequence_cli.py`, are in that list), exit 0:
```
624 passed in 94.28s (0:01:34)
```
Additionally run (not ordered): the other suites that drive `remedy do` — `tests/cli/test_do_evidence_package.py`, `tests/cli/test_job_commands.py`, `tests/cli/test_mission_cmd.py`, `tests/cli/test_scoped_listings.py`, `tests/test_cli_execution_loop_closure.py`, `tests/test_role_override_flags.py`, `tests/test_data_paths.py`: `272 passed in 65.79s`.

G3, `python3 -m ruff check` over the six .py files C3 and C4 touched (`packages/orchestration/contract_templates.py`, `tests/orchestration/test_contract_templates.py`, `packages/orchestration/do_sequence.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/command_catalog.py`, `tests/cli/test_do_sequence_cli.py`), exit 0:
```
All checks passed!
```

G4, `python3 .remedy-wt/f269-r3/g4.py`: one worktree at `5a384d0c`, `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_contract_templates.py tests/cli/test_do_sequence_cli.py` from the worktree root, `__pycache__` purged before each run, each mutation reverted by writing the original bytes back and the worktree status read clean after every revert:
```
module paths: /home/decodeux/Repos/remedy/.remedy-wt/f269-r3-g4/packages/orchestration/contract_templates.py | /home/decodeux/Repos/remedy/.remedy-wt/f269-r3-g4/packages/orchestration/do_sequence.py
[control] exit 0: 58 passed in 16.83s
[mutation a] exit 1: 1 failed, 57 passed in 15.34s
    FAILED tests/orchestration/test_contract_templates.py::test_a_tied_order_proposes_nothing
[mutation b] exit 1: 2 failed, 56 passed in 13.22s
    FAILED tests/orchestration/test_contract_templates.py::test_a_check_line_compiles_to_that_check
    FAILED tests/orchestration/test_contract_templates.py::test_a_d1_violation_is_refused_naming_its_line[invalid-check]
[mutation c] exit 1: 2 failed, 56 passed in 24.70s
    FAILED tests/cli/test_do_sequence_cli.py::test_contract_website_on_a_bare_order_gives_the_website_templates_criteria
    FAILED tests/cli/test_do_sequence_cli.py::test_contract_website_with_an_extra_requirement_adds_planner_criteria_and_drops_none
```
Mutations: (a) in `propose_contract_template`, the three lines `if top == 0 or len(winners) != 1: return None` / `return winners[0]` → `return next((name for name, score in scores.items() if score), None)`; (b) in `parse_contract_template`, `continue` inserted as the first line of the `check:` branch, so the line is skipped; (c) in `_step_plan`, `if template is not None:` → `if template is not None and ctx.contract_template is None:`, so a forced template is never written.

The full suite was not run (amend0917-throughput).

## Authored-text proofs

- The four payloads (block, decisions, ledger, plan) are committed byte-identical as `.agent/authored/f269-r3-*` (G1 `authored True`).
- `.agent/plan.md` equals plan.md; `.agent/live_review.md` and `.agent/decisions.md` equal their `b487e3f7` bytes + the payload (G1 True).
- The four `docs/contracts/<name>.md` equal their payloads (G1 `templates True`).

## Deviations & assumptions

1. `docs/guides/do-run-v1.md` is outside the block's change set. Its flags list said `--contract` is not yet available and exits 2 naming F269, which C4 made false; AGENTS.md (Documentation Updates) requires the doc to follow a changed behaviour, so C4 rewrites that bullet and the `plan` row. Round 2 accepted the same kind of deviation on the same file.
2. The `check:` line's check is stored as a `DoDCheck` with `source` `plan_acceptance`: D1 has it validate as a `DraftCheck` (which has no `source`), but `merge_contract_slice_into_dod` reads every stored check with `DoDCheck.model_validate`, and `plan_acceptance` is F061's own label for a check covering an acceptance line. The line's `id`, `acceptance_refs` and `blocking`, if given, are overridden by D1 (2)'s values; a `source` key is refused as `DraftCheck` forbids unknown fields.
3. D1 details this round settled: a template needs all three sections, at least one criterion and a non-empty fixture order; a section heading that appears twice is refused; a phrase bullet must be lowercase with no surrounding blanks; a `check:` line must directly follow a criterion bullet (one per criterion); a missing section, no criteria or no fixture order are refused naming the file's last line; a template with zero phrases loads (it can only be forced). The listing is the sorted stems of `docs/contracts/*.md`.
4. The unknown-name exit is in `_cmd_do` after the F270 flag refusals, so `--contract nosuch --push` still reports the `--push` refusal first. The message: `Error: --contract 'nosuch' is not a contract template; the templates are api-service, cli-tool, python-library, website. Nothing was run.`
5. A template that fails to load or write inside the plan step (only reachable by a broken shipped template, or a `DoContext` built directly with a bad name) fails the plan step with `mission <id> was not planned: <reason>`; the mission record already exists at that point, as for a planning failure today.
6. The plan step's detail gains a clause in every walk, including when no template applies (`; no contract template, none proposed from the order`); no existing test pinned the detail's end.
7. `do.run --contract`'s help avoids the word "order": `tests/docs/test_vocabulary.py` requires a description using the binding word to carry the page's meaning for it, and the first wording failed that test.
8. C3 is one commit of 485 insertions, under 500, so no code/test split was needed.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 templates + docs index | done | |
| C3 loader + compiler + proposal | done | |
| C4 `do --contract` | deviated | one doc file outside the change set (deviation 1) |
| C5 handoff + push | done | push follows this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 3 (T003 templates), with its verdict booked in round 4's first commit.

Operator questions open: 4
