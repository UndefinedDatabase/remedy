# Handoff — F281 round 1

## Session

SESSION 1 of feature F281 · round 1 · rounds so far 1

## Range

`c617dd74`..`dd56b151` (5 commits: C0a, C0b, C1, C2, C3)

## Commits

### f427225c F281 R1 C0a: save the round 1 step block under the authored directory
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f281-r1.md` | +348/-0 | Block file, verbatim transport |

### b53154aa F281 R1 C0b: mirror the round 1 step block into the last block state file
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +336/-141 | Copy of C0a block file |

### 62d65f9c F281 R1 C1: book F280 round 26 PASS, register R-0954, empty candidates, record DECISION F281 D1, and re-point plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +1/-0 | Append RECORD26 (Gate + Finding R-0954) |
| `.agent/candidates.md` | +3/-7 | Replace CANDIDATE paragraph with EMPTY notice |
| `docs/roadmap/features/T2_F273.md` | +3/-0 | Insert R-0954 acceptance line after R-0940 |
| `.agent/plan.md` | +39/-45 | Replace with PLAN1 (F281 round 1 scope) |
| `.agent/decisions.md` | +53/-0 | Append DECISION F281 D1 (scope boundary) |

### 6352b176 F281 R1 C2: claim F281 on the STATUS line and re-point the context file
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1/-1 | Flip F281 from `[ ]` to `[~]` |
| `.agent/context.md` | +40/-24 | Replace with CONTEXT1 (F281 scope and assumptions) |

### dd56b151 F281 R1 C3: rename the Worker: role label to Builder: in the pingpong report renderers (DECISION F281 D1)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +2/-2 | Change `Worker:` to `Builder:` at lines 618, 621 |
| `packages/orchestration/pingpong_evidence.py` | +2/-2 | Change `Worker:` to `Builder:` at lines 230, 232 |
| `tests/cli/test_cli_ux.py` | +2/-2 | Update assertions at lines 592, 665 to expect `Builder:` |

## External actions

```
git push -u origin feature/f281-cli-help-surface
Branch 'feature/f281-cli-help-surface' set up to track remote branch 'feature/f281-cli-help-surface' from 'origin'.
```

## Verification

All gates pass:

**G1 TARGETED**: `python3 -m pytest tests/cli/test_cli_ux.py tests/orchestration/test_evidence_bundle.py tests/orchestration/test_job_evidence.py -q`
```
........................................................................ [ 31%]
........................................................................ [ 63%]
........................................................................ [ 95%]
...........                                                              [100%]
227 passed in 19.80s
```

**G2 CANARY**: `python3 -m pytest tests/cli/test_golden_path.py -q`
```
..........................................                               [100%]
42 passed in 17.58s
```

**G3 SWEEP**: `grep -rn '"Worker:' apps/ packages/ tests/ --include=*.py`
```
apps/cli/commands/worker.py:67:        print(f"Worker: {match.display_name} ({match.provider_id})")
apps/cli/commands/worker.py:227:        print(f"Worker: {status.worker_id or '(none)'}")
packages/orchestration/brain_detail.py:1175:        title=f"Worker: {node.label}",
packages/orchestration/project_brain.py:630:            label=f"Worker: {spec.display_name}", status=spec.status,
[plus brain_viewer.py (2 lines) and RightLivePanel.tsx (1 line) — 7 untouched sites as DECISION F281 D1 names]
```
Result: zero remaining `"Worker:` in do_cmd.py, pingpong_evidence.py, test_cli_ux.py; all 7 untouched sites in worker.py, brain_viewer.py, brain_detail.py, project_brain.py, RightLivePanel.tsx preserved.

**G4 RUFF**: `python3 -m ruff check apps/cli/commands/do_cmd.py packages/orchestration/pingpong_evidence.py tests/cli/test_cli_ux.py`
```
All checks passed!
```

**G5 MUTATION RED-PROOF**: Disposable worktree `.remedy-wt/f281-r1-mutate` (removed after)
- Green control: `python3 -m pytest tests/cli/test_cli_ux.py::TestTextReportTokenProof::test_text_report_shows_provider_evidence -q` → `1 passed in 0.36s`
- Mutation (revert `do_cmd.py:618` to `Worker:`): `python3 -m pytest tests/cli/test_cli_ux.py::TestTextReportTokenProof::test_text_report_shows_provider_evidence -q` → `1 failed` (AssertionError: assert 'Builder:' in out — output shows "Worker: fake")
- Revert mutation: `python3 -m pytest tests/cli/test_cli_ux.py::TestTextReportTokenProof::test_text_report_shows_provider_evidence -q` → `1 passed in 0.24s`
- Worktree removed; verified by `git worktree list`

**G6 TREE**: `git status --porcelain` and `git worktree list`
```
[empty git status]
/home/decodeux/Repos/remedy  dd56b151 [feature/f281-cli-help-surface]
```

## Authored-text proofs

- `.agent/authored/f281-r1.md`: sha256 cfed923da9ec02aaced12bfbf2b4fd6845bf9fcc0207538702368e5cbfb116d7, 20608 bytes, 348 lines — byte-identical to block file (verified by `cmp` and sha256)
- `.agent/last_block.md`: sha256 cfed923da9ec02aaced12bfbf2b4fd6845bf9fcc0207538702368e5cbfb116d7, 20608 bytes, 348 lines — byte-identical to block file (verified by `cmp` and sha256)
- RECORD26 slice: appended verbatim to `.agent/live_review.md`
- FINDING954 slice: appended verbatim immediately after RECORD26 to `.agent/live_review.md`
- PLAN1 slice: replaced `.agent/plan.md` whole, verbatim
- DECISION F281 D1: appended verbatim to `.agent/decisions.md`
- CONTEXT1 slice: replaced `.agent/context.md` whole, verbatim
- Code edits (C3 FROM/TO blocks): applied verbatim to do_cmd.py, pingpong_evidence.py, test_cli_ux.py

## Deviations & assumptions

None. The round followed the block exactly: five commits in the ordered sequence (C0a, C0b, C1, C2, C3), each with the specified path set; all gates passed on the first run with the specified output format; the branch was pushed; the worktree was cleaned up after mutation red-proof.

## Next

1. The remaining slices of T001, in the orchestrator brief's order (per `.agent/plan.md`'s "Next Steps"):
   - Descriptions (175 catalog strings; 294 `_meaning_violations()` + 6 `_synonym_offenders()` per `tests/docs/test_vocabulary.py`)
   - Help wrap
   - `doctor core` dead-commands section (D11d, unbuilt)
   - D11a catalog group-reach test (unbuilt)
   - Visible-order data-pinned test (D4/amend0911-feedback D1's eighteen-slot order)
   - F259 `VOCABULARY_MODE` flip to `enforced`
   - README quickstart's R-0895 broken line (`job create --plan plan.yaml`)

2. One open scope question before touching descriptions: see `.agent/plan.md` "Next Steps" section 2 — `dev.agent-loop`'s `command_id` contains "loop" but this feature cannot change command ids.

This round claimed F281, booked F280's last unbooked round (round 26, PASS), registered the closure candidate R-0954 as finding, emptied the candidates.md file, recorded DECISION F281 D1 (scope boundary for the role-label rename), and landed the first slice of T001: the `Worker:` → `Builder:` rename at three production sites (do_cmd.py, pingpong_evidence.py) and two test assertions in test_cli_ux.py, leaving seven untouched sites that label worker adapters and processes, not the retired role label.
