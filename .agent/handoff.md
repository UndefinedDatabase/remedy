# Handoff — F071 Mission dossier · R1 (SPLIT, LARGE)

## Range
Review of 097e4959..\<HEAD\> · feature/f071-mission-dossier

## Commits — paths: pkg=`packages/orchestration/`, t=`tests/orchestration/`

### 4b5f940d chore(f071): claim F071 and reset agent state for R1
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f071-r1-1..4.md | +94 | reviewer texts, sha256-verified |
| .agent/live_review · plan · context.md | +89/-260 | authored replacements |
| docs/roadmap/STATUS.md | +1/-1 | F071 `[ ]` -> `[~]` |

### 31684c88 feat(f071): mission dossier structure and update mechanics (T001)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +263 | new: 5 fixed sections, merge-by-id append, resolve_risk |
| t/test_mission_dossier.py | +189 | ordering, goal immutability, append, one-home-per-fact |

### 64306334 feat(f071): dossier token budget, labeled counting basis and versioning (T001)
| Path | +/- | Reason |
|---|---|---|
| pkg/config.py | +13 | new key `dossier.max_tokens` (int, 3000) |
| pkg/mission_dossier.py | +130/-6 | budget, DossierTokenCount + basis, dossier_v\<N\>.md |
| t/test_mission_dossier.py | +170/-6 | budget precedence, basis label, versioning, flag-is-metadata |

### c0124741 feat(f071): dossier compression call, rules and schema (T002)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +245/-9 | DossierCompression (no goal field), prompt, rule enforcement, compress_dossier |
| t/test_mission_dossier.py | +199/-9 | rules verbatim; open items survive, resolved merge, violations refused |

### fd989184 feat(f071): budget-disciplined dossier update with honest over-budget flag (T002)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +81/-4 | update(), DossierUpdate, _flag |
| t/test_mission_dossier.py | +90/-4 | honest flag on every failure route; in-budget makes no call |

### dc809a21 chore(f071): record R1 decisions and sync plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +55 | four F071 design decisions |
| .agent/plan.md | +28/-11 | current step -> R1 delivered |

### \<handoff sha\> chore(f071): handback R1 — self-reference (R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| T001 structure/update/budget/versioning + tests | done | split 31684c88 + 64306334 (500-line rule) |
| T002 compression call/rules/schema + fake-provider tests | done | split c0124741 + fd989184 (500-line rule) |

## External actions
- `gh pr list --state open …` -> `[]` — Open PR Gate: zero open PRs.
- `git worktree add --detach <scratch>/wt-f071 HEAD` -> ok; `remove --force` -> ok; `worktree list` = primary only.
- `git push -u origin feature/f071-mission-dossier` -> exit 0, new branch. No PR (comes at closure).

## Verification
```
pytest t/test_mission_dossier.py -q          64 passed  EXIT=0
pytest tests/cli/test_golden_path.py -q      42 passed  EXIT=0   (canary)
pytest t/test_config.py t/test_orchestrator_loop.py -q  162 passed  EXIT=0
pytest tests/docs/ -q                       293 passed  EXIT=0
ruff check <the two F071 files>       All checks passed  EXIT=0
```
Mutation red-proofs (disposable worktree at HEAD, each restored): drop
keep-every-open-item 1F · drop merge-resolved-risks-away 1F · goal rewritten 1F ·
truncate-not-flag 5F · reorder sections 3F · overwrite version file 2F ·
baseline 64 passed. `git status --porcelain` empty at handback.

## Authored-text proofs
sha256 of all four `.agent/authored/f071-r1-<n>.md` match the BEGIN digests
(`ca3d0283…` `6dd2dcb8…` `42e6b074…` `ee2bedf3…`). `cmp` authored vs applied in
4b5f940d: live_review 0, plan 0, context 0. STATUS `grep -c`: FROM 1->0, TO 0->1.

## Deviations & assumptions
1. T001 and T002 each split into TWO commits (single commits: 760 / 585 lines).
   Split, not declared oversize; each slice is code + tests and green alone.
2. `compress_dossier` passes `allow_parse_retry=False` — the order says ONE
   call; the shared engine would otherwise make two. decisions.md.
3. `DossierCompression` has NO `goal` field — "never drop the goal" is enforced
   by schema shape; the other two rules post-validation by
   `compression_rule_violation`, which refuses the answer.
4. Budget counts on the labeled ESTIMATE basis (`token_economy.estimate_text_tokens`),
   not a call's `UsageActuals`: a prompt's measured tokens are not this
   document's size. decisions.md.
5. `orchestrator_loop.py` unchanged (R1); imported lazily, read-only, for
   `measure_call_cost` — R2 integration cannot cycle.
6. Assumption: one update produces exactly ONE version. decisions.md.
7. DECLARED: 100 lines (cap met) but ~1.2k tokens vs the ≤800 cap — the seven
   mandatory per-commit tables are ~600 tokens alone. Transcripts are already
   command+exit only. Reported, not met by dropping a section.

## Next
Reviewer verdict on R1. On PASS: R2 — T003 loop integration through the existing
`dossier` seam + recall harness + integration gate.
