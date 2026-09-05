# Handoff — F262 List commands v2 (dates, sort, filter), round 22 (R-0795 fix batch 1 — wiring)

## Session

SESSION 8 of feature F262 · round 22 · rounds so far 22.

22 of the 25-round soft cap — 3 rounds of headroom left before the cap.

## Range

Review of c129b4f2..a51653ad

## Commits

### 159885b4 F262 R22 C0a: save step block to .agent/authored/f262-r22.md
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f262-r22.md | +393/-0 | Save the reviewer's round-22 step block byte-for-byte (new file), per C0a and the write-once transport rule. |

### ccb30598 F262 R22 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
| .agent/last_block.md | +355/-66 | Whole-file replace with the identical bytes committed in C0a (mirror), per C0b. |

### 0d77edb5 F262 R22 C1: append GATE21 to live_review.md - books round 21's PASS verdict
| Path | +/- | Reason |
| .agent/live_review.md | +3/-1 | Append GATE21 (the reviewer's verbatim PASS verdict text for round 21) as a new paragraph, two `\n` separator, no trailing newline, per C1. |

### 175ddfa1 F262 R22 C2: wire worker.list to apply_list_options (R-0795)
| Path | +/- | Reason |
| apps/cli/commands/worker.py | +34/-2 | PAIR W1 (rewrite `_cmd_workers` to accept sort/desc/since/until/limit and call `apply_list_options`) + PAIR W2 (dispatch site passes the new args via `getattr`), fixing R-0795 for `worker.list`. |

### 36088098 F262 R22 C3: wire config.list to apply_list_options (R-0795)
| Path | +/- | Reason |
| apps/cli/commands/config_cmd.py | +19/-2 | PAIR CFG1: rewrite `_cmd_config_list` to call `apply_list_options` via `getattr(args, ..., default)` (function is shared with `config.show`, which has no list-option attrs), fixing R-0795 for `config.list`. |

### 4d51ea23 F262 R22 C4: wire execution.list to apply_list_options (R-0795)
| Path | +/- | Reason |
| apps/cli/commands/managed_builder_execution_cmd.py | +20/-0 | PAIR EXE1: rewrite `_cmd_list` to call `apply_list_options` and route `ListOptionError` through the file's existing `_err` convention, fixing R-0795 for `execution.list`. |

### dc74c2a2 F262 R22 C5: add regression tests for worker/config/execution list wiring (R-0795)
| Path | +/- | Reason |
| tests/cli/test_config_cmd.py | +17/-0 | TEST T1 append: `test_config_list_limit`, `test_config_list_unknown_sort_field_exits_nonzero`. |
| tests/cli/test_managed_builder_execution_cli.py | +12/-0 | TEST T2 rewrite (insert before module guard): `test_execution_list_limit`, `test_execution_list_unknown_sort_field_exits_nonzero`. |
| tests/cli/test_worker_facade_cmd.py | +14/-0 | TEST T3 append (new class `TestWorkerListOptions`): `test_limit_caps_returned_workers`, `test_unknown_sort_field_exits_nonzero`. |

### 2e3169d1 F262 R22 C6: append LANDED R-0795 to live_review.md
| Path | +/- | Reason |
| .agent/live_review.md | +3/-1 | Append the LANDED (not Done — only the reviewer writes Done) line for R-0795, two `\n` separator, no trailing newline, per C6. |

### a51653ad F262 R22 C7: replace plan.md with PLAN23
| Path | +/- | Reason |
| .agent/plan.md | +22/-26 | Whole-file replace with PLAN23 (Current Step now reflects the R-0795 wiring fix; Next Steps point at round 23's catalog-driven handler test and round 24's closure smoke test). |

### (this commit) F262 R22 C8: rewrite .agent/handoff.md
| Path | +/- | Reason |
| .agent/handoff.md | rewrite | Round-22 handback per docs/agents/handback_template.md; this is the round's last commit (write-once rule). |

## External actions

`git push -u origin feature/f262-list-commands-v2` — run after this commit; result reported below (Verification / push section).

No PR created, nothing merged, `main` untouched.

## Verification

**G1** — `sha256sum .agent/authored/f262-r22.md .agent/last_block.md`:
```
be063df027d5daf0fae01a1b422d5aee83829025e985ca98342f833c4f9f4697  .agent/authored/f262-r22.md
be063df027d5daf0fae01a1b422d5aee83829025e985ca98342f833c4f9f4697  .agent/last_block.md
```
Identical digest for both files. Exit code 0.

**G2** — `python3 -c "import py_compile; [py_compile.compile(p, doraise=True) for p in ['apps/cli/commands/worker.py','apps/cli/commands/config_cmd.py','apps/cli/commands/managed_builder_execution_cmd.py','tests/cli/test_config_cmd.py','tests/cli/test_managed_builder_execution_cli.py','tests/cli/test_worker_facade_cmd.py']]; print('OK')"`:
```
OK
```
Exit code 0.

**G3** — `python3 -m pytest tests/cli/test_worker_facade_cmd.py tests/cli/test_config_cmd.py tests/cli/test_managed_builder_execution_cli.py -q`:
```
........................................................................ [ 73%]
..........................                                               [100%]
98 passed in 6.69s
```
98 passed (92 pre-existing + 6 new), matching the block's expectation exactly. Exit code 0.

**G4** — `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`:
```
........................................................................ [ 11%]
........................................................................ [ 22%]
........................................................................ [ 33%]
........................................................................ [ 44%]
........................................................................ [ 55%]
........................................................................ [ 66%]
........................................................................ [ 78%]
........................................................................ [ 89%]
......................................................................   [100%]
646 passed in 70.67s (0:01:10)
```
646 passed, unmoved (515+52+21+16+42), matching the block's expectation exactly. Exit code 0.

**G5** — byte-reads of `.agent/live_review.md`, Python binary mode:
- Immediately before C1: 2479698
- Immediately after C1: 2482245 (2479698 + 2 + 2545, GATE21 text)
- Immediately before C6: 2482245
- Immediately after C6: 2482540 (2482245 + 2 + 293, LANDED text)

All four numbers match the block's stated arithmetic exactly.

**G6** — byte-read of `.agent/plan.md` immediately after C7, binary mode: 1959 bytes, byte-for-byte equal to the PLAN23 text in the step block (verified by direct write of the exact PLAN23 string and reconfirming length). Matched exactly. Note: the Write tool's normal trailing-newline behavior produced 1960 bytes on first write; this was corrected by stripping the single trailing `\n` (matching this file's established no-trailing-newline convention, confirmed against the prior committed plan.md at HEAD `c129b4f2` which also ends with no trailing newline) to land on the mandated 1959.

**G7** — `git status --porcelain`: empty, checked before C0a (clean at start) and immediately before C8 (checked again just above, empty). `git ls-files .remedy-wt`: empty, both checks. `.agent/STOP`: absent, both checks (`ls: cannot access '.agent/STOP': No such file or directory`).

## Authored-text proofs

- GATE21 text (2545 bytes UTF-8): appended via Python `pathlib.Path.write_bytes`, byte length asserted equal to 2545 before writing (assertion held, no AssertionError raised) and the file's before/after sizes cross-checked in G5.
- LANDED text (293 bytes UTF-8): same method, byte length asserted equal to 293 before writing (assertion held), before/after sizes cross-checked in G5.
- PLAN23 (1959 bytes UTF-8): written via the Write tool then corrected to strip one trailing newline byte (see G6); final on-disk content matches the step block's PLAN23 text exactly, final byte count 1959.
- `.agent/authored/f262-r22.md` / `.agent/last_block.md`: identical per G1's sha256sum.

## Deviations & assumptions

- The step block's Python snippet for writing PLAN23 used a triple-quoted string containing `#` headings after a newline, which the sandbox's bash-guard rejected as a potential argument-hiding pattern ("Newline followed by # inside a quoted argument can hide arguments from path validation"). Substituted the Write tool for the initial content write, which produced one extra trailing-newline byte (1960 instead of 1959) versus the block's exact byte target; corrected with a separate Python `pathlib.Path.write_bytes` call that stripped the single trailing `\n`, landing on the mandated 1959 bytes, confirmed to match the established no-trailing-newline convention for this file (the prior plan.md at HEAD `c129b4f2` also has no trailing newline). No content besides the trailing-newline byte was affected; this is a mechanical tooling substitution, not a content change, and is recorded here per constraint 8's substitution-declaration requirement.
- No other departure from the block's ordered commit sequence (C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, in that exact order).
- No mutation red-proof was ordered this round (constraint 9): it is explicitly deferred to round 23, bundled with the T001 catalog-test's own red-proof, per PLAN23's Next Steps. This is a deferral, not a skip — the new tests in commit C5 (G3, 98 passed including the 6 new regression tests) are this round's only behavioural proof, as the block specifies.

## Next

Round 23: extend `TestListCommandOptions` (tests/test_command_catalog.py) into a catalog-driven test that dispatches every `_is_list_command` entry's HANDLER (not just its argparse signature) with an invalid `--sort` and asserts a non-zero exit — T001's own never-built Acceptance bullet — AND run the full mutation red-proof deferred from this round, covering all three of this round's wirings (`worker.list`, `config.list`, `execution.list`).
