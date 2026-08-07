# Handback — F254 R6 (worker)

Feature T2_F254 · Round R6 · Branch `feature/f254-model-alias-table`

## Range
Review of c77dfc0d..HEAD (5 commits: 08dcdd3b, 1743d252, a31112d7, 0a60ec7c + handoff).

## Commits
### 08dcdd3b docs(f254): persist the R5 verdict and finding R-0215
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f254-r6-1.md | +118 / -0 | reviewer receipt, live_review target |
| .agent/authored/f254-r6-2.md | +72 / -0 | reviewer receipt, plan target |
| .agent/live_review.md | +75 / -8 | R5 PASS, R-0215, step list |
| .agent/plan.md | +18 / -15 | current step R6, next steps, next free ID |

### 1743d252 fix(f254): make the dead-model warning readable and its count honest
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/worker_facade_cmd.py | +62 / -19 | R-0215 (a)+(b): summary/detail split, count label |
| tests/cli/test_worker_facade_cmd.py | +108 / -3 | new shape pinned; 1 assertion inverted (see Deviations) |

### a31112d7 test(f254): pin that no built-in model id is spelled outside the alias table
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_model_aliases.py | +124 / -0 | ast repo scan; acceptance criterion 2 |

### 0a60ec7c docs(f254): document the model alias table and the dead-model check
| Path | +/- | Reason |
|---|---|---|
| docs/system/model-defaults-and-dead-model-check-v0.md | +62 / -0 | new ist-doc |
| docs/README.md | +2 / -0 | quick-find row + system table row |

### handoff commit (self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions
`git push` after 0a60ec7c → c77dfc0d..0a60ec7c, exit 0. Second push after the
handoff commit. `git worktree add --detach <scratchpad>/wt-redproof HEAD` exit 0;
`git worktree remove --force` exit 0; `git worktree prune` exit 0; `git worktree list`
afterwards shows ONLY `/home/decodeux/Repos/remedy a31112d7`. No PR, no gh call, no force-push.

## Verification
| Gate | exit | count |
|---|---|---|
| tests/cli/test_worker_facade_cmd.py | 0 | 63 passed |
| tests/orchestration/test_model_aliases.py | 0 | 24 passed |
| tests/orchestration/test_dead_model_list.py | 0 | 23 passed |
| tests/cli/test_product_spine.py | 0 | 72 passed |
| tests/cli/test_cli_ux.py | 0 | 57 passed |
| tests/orchestration/test_development_artifact_boundary.py | 0 | 18 passed |
| tests/docs/ | 0 | 294 passed |
| tests/ui_server/test_dashboard_contract.py | 0 | 70 passed |
| tests/orchestration/test_test_runner.py | 0 | 51 passed |
| tests/regression/test_resource_safety.py | 0 | 21 passed |
| tests/cli/test_golden_path.py | 0 | 42 passed |
| ruff check (3 touched .py paths) | 0 | All checks passed |
| `remedy doctor core` | 0 | READY, 11 checks, 0 blockers, 2 warnings |
| `remedy doctor core --json` | 0 | keys ready/checks/blockers/warnings; each warning has warning+summary+detail |

Doctor text-mode longest `[WARN]` line: BEFORE 839 chars (other 834); AFTER 224 (other 220).
JSON detail lengths unchanged in substance (772/777) and now carry the full reason.
`dead_model_list` detail before `2 shipped + 0 configured dead ids`, after
`2 shipped + 0 config-only dead ids (2 total)`.

Scan-test red proof (disposable worktree at a31112d7, primary checkout untouched):
inserted `REDPROOF_MODEL = "claude-opus-4-20250514"` at role_config.py:23 → test exit 1,
message `packages/orchestration/role_config.py:23: 'claude-opus-4-20250514'`. Reverted;
then the SAME id in a `#` comment at the same line → exit 0, 3 passed (D11 boundary holds
by mechanism). Worktree removed and pruned; `git status --porcelain` in the primary
checkout empty at every point.

## Authored-text proofs
`cp` + `cmp` disk-to-disk against the reviewer's scratchpad originals, both exit 0.
f254-r6-1.md sha256 f4962b96b5be638ae5f015cb11badb2813b10f728b14acf4c067aa15266e4d95 (identical both sides).
f254-r6-2.md sha256 a7c3f3a1ba2bf6502c9ad12d6c7752f200224f2acbbeb5272e74994ce45c9907 (identical both sides).
Six pairs, all REWRITE-shaped, pre FROM 1x / TO 0x → post FROM 0x / TO 1x:
live_review pairs 1,2,3 and plan pairs 1,2,3. Structure after: live_review keeps its four
`##` headings 1x each (Steps, Findings, Decisions, Verdicts); plan keeps `## Goal` and
`## Next Steps` and is 49 lines.

## Deviations & assumptions
- B2 implemented as "emit only when it ADDS information": with a recorded reason present the
  trailing replacement sentence is dropped; with NO recorded reason (config-extension ids) it is
  still emitted, because nothing else would say it. Consequence: existing
  `test_missing_replacement_is_stated_not_implied` was replaced by
  `test_missing_replacement_is_not_repeated_after_the_reason` (asserting the inverse for the
  reason-present case). `test_config_extension_id_says_it_came_from_config` is untouched and still
  proves the sentence appears when no reason exists. No `ready`/`blockers` assertion was weakened.
- B3 solved by LABELLING (`config-only dead ids`, plus a total), not by recomputing: the real
  configured count is only reachable through `dead_model_list._configured_dead_model_ids`, and the
  step forbade editing that module; importing a private helper into the CLI was the worse trade.
- Summary text deliberately omits the replacement id — the step's mandated summary content is
  id + origin + fix + provenance, and the replacement is what `--json` is for.
- Text mode gained one trailing line `(run with --json for each warning's full recorded reason)`
  so the compact rendering is not silently lossy. Additive, printed only when warnings exist.
- Doc decision: NEW doc, not an update. Checked the index first — no docs/system or docs/guides
  file covers built-in model defaults (`grep` for DEFAULT_MODEL / default model / model alias /
  dead model over docs/system, docs/guides, docs/agents returned zero files).
  `agents/model_routing_policy.md` is the F110 class→tier seed, a different concern;
  `system/core-product-spine-v0.md` is product terminology. No banner added: the index's banner
  rules cover DEPRECATED, overnight-superseded and roadmap-superseded docs only, and this is a
  current ist-doc.
- Observation (NOT fixed, out of scope): `.agent/live_review.md` now carries TWO R6 lines in
  `## Steps` — the new one from pair 1 and the pre-existing `- R6: the repo-scan test that no
  built-in model id survives outside the alias module …`. The authored FROM did not cover it, and
  retyping reviewer text is forbidden. Reviewer's call.
- Observation: the repo scan found ZERO violations outside the alias module at HEAD; no exclusion
  was added to make anything pass.
- Handoff length: this file is 136 lines — 76 OVER the step block's 60-line target, and 36 over
  the AGENTS.md ≤100 allowance for >5-commit per-commit tables. The mandated content is what
  costs it: the 5 per-commit tables (~26 lines), the 14-row verification table (~17), the
  authored-text + red-proof proofs (~15) and the A-E item-status table (~9) are ~67 lines before
  a word of prose. That is R-0214's evidence, per the step block; no section was dropped to hit
  a number. (Written twice, not once: the line count is self-referential and the item-status
  table was added on the second pass — the PH v3 write-once rule cannot hold for a file that
  reports its own length.)

## Item status
| Item | Status | Reason |
|---|---|---|
| A receipts persist first | done | own commit 08dcdd3b, precedes all code |
| B R-0215 doctor fix | done | B1/B2/B3; B2 shaped as "adds information" — see Deviations |
| C repo-scan acceptance test | done | red-proof + D11 comment proof recorded |
| D docs + index row | done | new doc, no banner — see Deviations |
| E commits, push, handoff | done | 5 commits, 2 pushes, no PR |

## Open findings
0 open. R-0215 closed in this round (both defects). Next free ID R-0216.
`.agent/candidates.md` still holds the R-0214 handoff-cap amendment for the next feature claim.

## Next
Reviewer: review c77dfc0d..HEAD, re-run the gates above, and issue the R6 verdict. On PASS the
next round is R7 — the integration gate per docs/agents/integration_gate.md.
