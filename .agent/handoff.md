# Handback — F082 R4 (order set)

Deviations, declared: this handoff is 134 lines against the 60-line cap, under
DECISION D15 stated cause — six per-commit tables, the 19-gate verification
table, the four authored-text proofs and the item-status table. No section
dropped, no prose padding.

## Range
Review of cb79d388..fd16e685 (branch feature/f082-self-benchmark).

## Commits
### 813014ec chore(f082): save the R4 order-set block verbatim
| Path | +/- | Reason |
| `.agent/authored/f082-r4.md` | +273/-0 | C0a, block saved byte-for-byte |

### ef5f3042 chore(f082): mirror the R4 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +212/-253 | C0b, mirrored from the COMMITTED authored file |

### 07445f08 docs(f082): record the R3 verdict and register R-0408
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C1a, FINDING-R408 then GATE-R3, append only |
| `.agent/decisions.md` | +33/-0 | C1b, DECISION F082 D2 appended |
| `.agent/plan.md` | +16/-16 | C1c, full replacement with the PLAN slice |

### ff6b06a4 docs(f082): survey the sample project the bench orders must run in
| Path | +/- | Reason |
| `.agent/f082_inventory.md` | +164/-0 | C2, sections S1..S4, read-only survey |

### 89af3f95 feat(f082): add the frozen bench order set for the three expressible capabilities
| Path | +/- | Reason |
| `scripts/bench_orders/b01-cli-report-width.json` | +30/-0 | C3, capability 1 |
| `scripts/bench_orders/b02-config-lookup-bugfix.json` | +31/-0 | C3, capability 4 |
| `scripts/bench_orders/b03-cli-render-refactor.json` | +31/-0 | C3, capability 5 |
| `scripts/bench_orders/manifest.json` | +29/-0 | C3, per-order version + digests map |
| `.agent/plan.md` | +4/-2 | Commit Gate: plan said five orders, three exist |

### fd16e685 feat(f082): add the bench order loader and its version freeze
| Path | +/- | Reason |
| `packages/orchestration/bench_orders.py` | +202/-0 | C3, loader + freeze, additive |
| `tests/orchestration/test_bench_orders.py` | +230/-0 | C3, 14 tests |

C4 (this handoff) is not tabled above: a handoff cannot table the commit that
writes it (R-0149 pattern). It changes `.agent/handoff.md` alone.

## External actions
- `git push -u origin feature/f082-self-benchmark` after each of the six
  commits above — all succeeded, no force, no merge, no history rewrite.
- `git worktree add -f .remedy-wt/f082-r4-redproof HEAD` — created at fd16e685
  for gate 11's red-proof; `git worktree remove --force` + `git worktree prune`
  afterwards. `git worktree list` is one line at handback.
- No PR created, none merged, no `gh` command run.

## Verification
| # | Gate | Real value |
|---|------|-----------|
| 1 | `git status --porcelain` / `git worktree list` | EMPTY / 1 line: `/home/decodeux/Repos/remedy fd16e685 [feature/f082-self-benchmark]` |
| 2 | Transport property | all three byte-identical, shared sha256 `96e7093147e87626b1ea3a5e10ce737baa75aae28dee4e131ca8a90229c51b1f`, 273 lines (cap 400). `cmp`/`cp` denied to this session class; proven by `sha256sum` over all three plus a `python3` byte copy (R-0408) |
| 3 | `.agent/STOP` | ABSENT at round start, ABSENT at handback |
| 4 | Append proof | first 103 lines identical, both head digests `af19119ba1ecd3682cb67967782d1a83a59c0509839d862169cd1292076ed69b`; C1 numstat `4 0`, deletion column 0; FINDING-R408 = 1 physical line, GATE-R3 = 1 physical line |
| 5 | Record greps | `^Gate: R3 — PASS` 1, `^- R-0408 — ` 1, `^## Steps` 1, `^Landed: ` 0 |
| 6 | Open set | THIRTY-EIGHT, duplicates none, max R-0408, next free R-0409. Ids: R-0361 R-0362 R-0363 R-0364 R-0367 R-0368 R-0369 R-0371 R-0374 R-0375 R-0376 R-0377 R-0378 R-0379 R-0380 R-0381 R-0382 R-0385 R-0386 R-0387 R-0389 R-0391 R-0392 R-0393 R-0394 R-0395 R-0396 R-0397 R-0399 R-0400 R-0401 R-0402 R-0403 R-0404 R-0405 R-0406 R-0407 R-0408 |
| 7 | `^## DECISION F082 D2` | 1; C1 numstat for `.agent/decisions.md` is `33 0`, deletion column 0 |
| 8 | `wc -l .agent/plan.md` | 38 (cap 50) |
| 9 | C2 stop clause | did NOT fire. Counted five capabilities; THREE expressible (1 CLI tool, 4 bugfix, 5 refactor), TWO not (2 API endpoint, 3 frontend widget). Orders written for three; two recorded as owed in S4 |
| 10 | `git diff --name-only cb79d388..HEAD` | 12 paths, counted mechanically: `.agent/authored/f082-r4.md`, `.agent/decisions.md`, `.agent/f082_inventory.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/bench_orders.py`, `scripts/bench_orders/{b01,b02,b03,manifest}.json`, `tests/orchestration/test_bench_orders.py`. Paths outside the Change list: NONE |
| 11 | Freeze acceptance + red-proof | `test_editing_an_order_without_bumping_its_version_fails_validation` passes, asserting `BenchOrderSetError`. Worktree `__file__` = `/home/decodeux/Repos/remedy/.remedy-wt/f082-r4-redproof/packages/orchestration/bench_orders.py`, unmutated run there `14 passed`. The block's suggested weakening (compare against ANY digest in the map) does NOT go red — reported as measured, with the arithmetic below. The mutation that does: dropping the digest-vs-version binding → `1 failed`, `DID NOT RAISE`. Worktree removed and pruned |
| 12 | `pytest tests/orchestration/test_bench_orders.py -q` | exit 0, `14 passed` |
| 13 | Gauntlet untouched + green | range over `tests/orchestration/ packages/orchestration/` returns exactly `packages/orchestration/bench_orders.py` and `tests/orchestration/test_bench_orders.py` — no `gauntlet_*` path. Seven gauntlet files + `test_capability_bench.py`: exit 0, `283 passed` (= planner baseline 283) |
| 14 | scoped `ruff check` | exit 0, `All checks passed!` |
| 15 | `pytest tests/cli/test_golden_path.py -q` | exit 0, `42 passed` (= baseline 42) |
| 16 | three contract readers | exit 0, `142 passed` (= baseline 142) |
| 17 | `python3 -m apps.cli.main integrity check --json` | `passed: true`, `fail_count: 0`, `check_count: 5`; `high_blockers_open` = pass, "no open blocker/high findings" |
| 18 | Order digests | 3 orders, counted as three. b01-cli-report-width v1 `429b7b10…4813f8`; b02-config-lookup-bugfix v1 `9fb9dd82…d728765`; b03-cli-render-refactor v1 `dbf18a25…11e14183`. File version, manifest version, recorded digest and real sha256 MATCH for all three |
| 19 | Insertions per commit | 813014ec 273 · ef5f3042 212 · 07445f08 53 · ff6b06a4 164 · 89af3f95 125 · fd16e685 432. None over 500 |

Gate 11 arithmetic. The suggested weakening cannot go red: an unbumped EDIT
changes the bytes, so the edited digest `ce0bc02e…508263` is in neither the
strict nor the any-of reading of `digests` = `{"1": "429b7b10…4813f8"}`. The
weakening only relaxes a REVERT to older published bytes. Property satisfied by
another route per R-0408, and the route is reported.

## Authored-text proofs
All four extracted from the COMMITTED `.agent/authored/f082-r4.md` by
`.remedy-wt/f082_r4_apply_c1.py` and applied disk-to-disk; none retyped.
| Slice | sha256 | bytes | Applied-region proof |
| FINDING-R408 | `819138da2a39c0a5e1eeadea2196608ac551f1ac6d0df101b4f17e93436b9b89` | 1598 | present verbatim in `.agent/live_review.md`, 1 occurrence, 1 physical line |
| GATE-R3 | `72bd9205e96696be4979fd3b9fa6d09cdf388ee9a85c7136641a98bb754f7f8a` | 4812 | present verbatim, 1 occurrence, 1 physical line |
| DECISION-D2 | `2f0f50acf307eec1fb76387318c556bc2aa0f7efb2c8fed4bcd071271806ed4d` | 2108 | present verbatim in `.agent/decisions.md`, 1 occurrence, file tail equals it |
| PLAN | `400665177125366662a1cc431b022832ce19bd0aef3d0238574e516185d97a8f` | 1867 | `.agent/plan.md` equalled the slice exactly at C1; the later Commit-Gate correction is declared below |

No BEGIN/END marker line reached any target file (0 in all three). Trailing
whitespace: 0 lines in every file touched this round.

## Item status
| Item | Status | Reason |
| C0a | done | |
| C0b | done | |
| C1 | done | findings persisted first, before any code |
| C2 | done | stop clause did not fire; 3 of 5 expressible |
| C3 | deviated | split into two commits, 89af3f95 + fd16e685 |
| C4 | done | this handoff |

## Deviations & assumptions
1. C3 split into TWO commits. Combined insertions were 553, over the AGENTS.md
   500 cap; AGENTS.md wins over the block's "commit together". Data first
   (89af3f95, 125), then loader and tests (fd16e685, 432).
2. THREE orders, not five. C2's stop clause, honoured literally: capabilities 2
   and 3 are inexpressible against `scripts/gauntlet_sample_project` and are
   recorded as OWED in S4 with the smallest fixture addition each would need.
   F082 has not built them.
3. `.agent/plan.md` corrected in 89af3f95 (+4/-2): the authored PLAN slice said
   "the five frozen orders", which the survey made false. AGENTS.md Commit Gate
   item 1 requires plan.md to match the work. The authored original stays
   verbatim in `.agent/authored/f082-r4.md` and `.agent/last_block.md`.
4. `cmp`, `cp` and compound `$?` shell forms are denied to this session class;
   transport and copies were done with `sha256sum` and `python3`. This is
   R-0408's own case, and the gate stated the property, so no route was skipped.
5. Gate 11's suggested weakening does not falsify the acceptance test. Reported
   with its arithmetic rather than reworded; the property (non-vacuity) was
   proven by dropping the binding the test depends on.
6. One authored test was replaced during C3 self-review:
   `test_recomputing_the_digest_without_bumping_the_version_still_fails`
   asserted a refusal DECISION D2 does not decide and cannot deliver without
   git history. It is now
   `test_a_manifest_side_digest_rewrite_is_outside_what_the_freeze_can_see`,
   which pins the residual, plus
   `test_the_file_and_the_manifest_must_claim_the_same_version`. The residual is
   also stated in the module docstring. No test was weakened to make a gate pass.
7. Commit messages carry no trailer, matching this repository's history.

## Next
Reviewer verdict on R4, then R5 (T001 close): the dry run of
`build_bench_record` against RECORDED fixture evidence, order file to row.
