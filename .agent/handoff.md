# Handback — F075 R1 (SPLIT, LARGE): PR Gate + claim + T001 + T002

Branch feature/f075-self-run-gauntlet · HEAD 4ff5ba18
Prefixes: `P/`=packages/orchestration/ `T/`=tests/orchestration/ `S/`=scripts/

## Range
Review of 563b15b4..4ff5ba18 (13 commits, incl. this one).

## Commits

### bd5fdcb0 chore(f075): claim F075 — STATUS [~] + state reset
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r1-{1..4}.md | +105 | texts saved first |
| .agent/{context,plan,live_review}.md | +74/-118 | full replacements |
| .agent/last_block.md | +220/-214 | the block, verbatim |
| docs/roadmap/STATUS.md | +1/-1 | F075 `[ ]` -> `[~]` |

### c24a8088 feat(f075): recorded gauntlet evidence schema + never-raising reader
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_evidence.py | +178 | evidence layout + loader |
| T/test_gauntlet_evidence.py | +163 | never raises; order |
| .agent/decisions.md | +41 | T001 interface decisions |

### 087220e1 feat(f075): the gauntlet pass definition as a pure evaluator
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_evaluator.py | +468 | 9 criteria, 9 failure kinds, class names |

### 8913681c test(f075): one falsification per pass criterion + class naming
| Path | +/- | Reason |
| --- | --- | --- |
| T/test_gauntlet_evaluator.py | +397 | one flip per criterion |
| P/gauntlet_evaluator.py | +11/-1 | contradictory gate verdict named |

### d7507aba feat(f075): deterministic gauntlet matrix report in markdown and json
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_matrix.py | +187 | md+json, no clock/abs path |
| T/test_gauntlet_matrix.py | +157 | determinism + content |
| P/gauntlet_evaluator.py | +6/-1 | carry injection detail |
| T/test_gauntlet_evaluator.py | +2 | assert that carry |

### 7abf15f3 test(f075): recorded gauntlet evidence fixtures for the dry-run proof
| Path | +/- | Reason |
| --- | --- | --- |
| T/fixtures/gauntlet/recorded/ | +413 | 18 files, 9 runs: 1 flawless, 1 operator command, 1 unknown postmortem, 4 degraded injections (one/class), 2 mishandled |

### 0e7d3e2e test(f075): dry-run proof over recorded evidence + golden markdown matrix
| Path | +/- | Reason |
| --- | --- | --- |
| T/fixtures/gauntlet/golden/matrix.md | +341 | golden, human half |
| T/test_gauntlet_evaluator.py | +74 | recorded set 5/9; reads only |
| T/test_gauntlet_matrix.py | +21 | byte-exact golden |
| T/test_gauntlet_evidence.py | +7 | shared fixture paths |

### 5a134791 test(f075): golden json matrix pinned to the recorded set
| Path | +/- | Reason |
| --- | --- | --- |
| T/fixtures/gauntlet/golden/matrix.json | +328 | golden, machine half |
| T/test_gauntlet_matrix.py | +18 | byte-exact; agrees with md |

### 7c1872f9 feat(f075): thin gauntlet CLI with dry-run over recorded evidence
| Path | +/- | Reason |
| --- | --- | --- |
| S/self_run_gauntlet.py | +117 | dry-run/only/format/out/label |
| T/test_self_run_gauntlet.py | +140 | exit codes; live absence stated |

### 17ca8bbb feat(f075): frozen order-set loader with manifest and set-hash checks
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_orders.py | +220 | schema, per-file sha256, set hash |
| .agent/decisions.md | +27 | T002 decisions |

### ef378861 feat(f075): the curated ten-order set, frozen at set version 1
| Path | +/- | Reason |
| --- | --- | --- |
| S/gauntlet_orders/ | +340 | 11 files: ten orders (rationale+risk+budget) + manifest, set_hash d19c999a |

### 4ff5ba18 test(f075): pin the frozen ten and prove the freeze by tampering
| Path | +/- | Reason |
| --- | --- | --- |
| T/test_gauntlet_orders.py | +245 | ten/ids/budgets/digests/kinds; edits refused |

### <this> chore(f075): handback R1
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME at handback |

## External actions
- `gh pr list --state open …` -> one: #178, f071-mission-dossier -> main, not draft.
- `gh pr merge 178 --merge --delete-branch` -> 0; main ff 097e4959..563b15b4; branch deleted.
- `git pull --ff-only` -> up to date; branch created from 563b15b4.
- `git push -u origin …` -> new branch; two further pushes after the slice gates. No PR created.

## Verification
All invoked as `python3 -m pytest <path> -q`; braces expanded here.

    $ pytest tests/docs/ -q  ->  293 passed, exit 0  (claim)
    $ pytest tests/cli/test_golden_path.py -q  ->  42 passed, exit 0  (claim)
    $ pytest T/test_gauntlet_evaluator.py -q  ->  63 passed, exit 0  T001 SLICE GATE
    $ pytest T/test_gauntlet_{evidence,matrix}.py T/test_self_run_gauntlet.py -q
      ->  44 passed, exit 0  (siblings)
    $ pytest tests/test_{imports,command_catalog,no_step_files,test_categories}.py -q
      ->  38 passed, exit 0  (collateral)
    $ pytest T/test_gauntlet_orders.py -q  ->  34 passed, exit 0  T002 SLICE GATE
    $ pytest tests/cli/test_golden_path.py -q  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Authored-text proofs
`sha256sum` on disk, applied file vs its committed `.agent/authored/` file:
- f075-r1-2 `28246a1e…1c63532d` == live_review.md · r1-3 `32729c74…73b51aeb` == plan.md · r1-4 `26b3de43…0adc8b812` == context.md
- f075-r1-1 `be68f1e9…73e05ea5` matches its BEGIN hash; applied to STATUS.md as a one-occurrence line replacement copied from the saved file (FROM grep-counted 1 before, 0 after).

## Deviations & assumptions
- **Module split** (block suggested one): the evaluator alone was 591 lines, over the 500 cap, and the seam is real — evidence reads, evaluator judges. Per `test_x.py ↔ x.py` the gate file gained siblings; both slice gates ran as ordered, siblings extra, never instead.
- **Golden pair over two commits** (md, then json), same cap. No commit exceeds 500 lines; the oversize exception is unused.
- **`S/gauntlet_orders/`** over the fixture area — campaign input, not test data (decisions.md).
- **Zero provider calls**; no live path — without `--dry-run` the CLI exits 2 saying live run is T003.
- Fixtures use `fx-NN` ids, distinct from the frozen `g01…g10`.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P0 gate+branch | done | |
| P1 claim | done | |
| T001.1 module+CLI | done | 2 modules, see Deviations |
| T001.2 pass definition | done | |
| T001.3 matrix | done | |
| T001.4 fixtures+golden | done | |
| T001.5 falsifiability tests | done | |
| T001.6 slice gate | done | exit 0 |
| T002.1 ten orders | done | |
| T002.2 manifest+set hash | done | |
| T002.3 pinning tests | done | |
| T002.4 slice gate | done | exit 0 |
| P4 handback | done | |

## Next
Window 1 reviews R1; then R2+ drives the T003 campaign and the integration gate.
