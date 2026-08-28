# Handback — F256 Diff viewer completion, round 6 (THE SERVER-SIDE MEASUREMENT)

## Session

SESSION 2 of feature F256 · round 6 · rounds so far 6

## Range

Review of 08f6218a..HEAD (branch `feature/f256-diff-viewer-completion`).

## Commits

### 250529ba chore(f256): save the round 6 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r6.md` | +396 / -0 | C0a: the block copied byte for byte from `.remedy-wt/f256-r6-block.md` |

### b402da84 chore(f256): mirror the round 6 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +322 / -271 | C0b: written from the COMMITTED C0a blob, so the two are one blob id |

### 221c1dd2 docs(f256): advance the plan to the measurement round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -14 | C1: whole-file replacement by the `PLANF256R6` slice |

### 1962f8ef docs(f256): book the round 5 verdict and DECISION F256 D4
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +94 / -0 | C2: the `DECF256D4` slice appended |
| `.agent/live_review.md` | +14 / -0 | C2: the `GATEF256R5` slice appended, the R5 verdict |

### 4aea7ba2 test(diff-endpoint): measure the 10k fixture end to end
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_server/test_diff_endpoint.py` | +298 / -0 | C3: S1–S6 — four constants, the fixture generator, the new `TestDiffEndpointPerfBudget` class and its two tests |

### C4 (this commit) chore(f256): hand back round 6
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C4: this handback. A handoff cannot table the commit that writes it (R-0149) |

Every `+/-` cell above was compared cell by cell against G1's `git diff --numstat`
figures and agrees with them.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName` | `[]` — no open PR. No PR created, nothing merged. |
| `git worktree add .remedy-wt/f256-r6-redproof HEAD --detach` | created at `4aea7ba2` for G7 |
| `git worktree remove .remedy-wt/f256-r6-redproof --force` | removed; `git worktree list` shows the primary alone |
| `git push -u origin feature/f256-diff-viewer-completion` | run AFTER this commit, so its outcome cannot be written into the file it pushes; the branch tip equalling `origin/feature/f256-diff-viewer-completion` is the reading that proves it |

No `npm run build` and no `npx vite build`: this round edits no file under `apps/ui/`
and `apps/ui/dist` was already warm.

## Verification

**G1 HYGIENE AND STRUCTURE.** `.agent/STOP` read with `os.path.exists` before C0a →
`False`; read again before C3 → `False`. `git rev-parse HEAD` before C0a =
`08f6218a6d7d4f172589ab38ecb264ae128cc23e`, which equals the ordered base `08f6218a`.
`git branch --show-current` = `feature/f256-diff-viewer-completion`.
`git status --porcelain | wc -l` = **0** after each of C0a, C0b, C1, C2 and C3, and
**0** again after the worktree removal.

Over `08f6218a..4aea7ba2` — the range ending BEFORE this handback commit —
`git diff --name-only` returns exactly six paths: `.agent/authored/f256-r6.md`,
`.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `tests/ui_server/test_diff_endpoint.py`. Both residues against the
change set with `.agent/handoff.md` set aside are **empty**: changed − expected =
`[]`, expected − changed = `[]`.

Per-commit insertions from `git diff --numstat`, each under 500, each single-parent:

| Commit | + | − | parents |
|---|---|---|---|
| 250529ba C0a | 396 | 0 | 1 |
| b402da84 C0b | 322 | 271 | 1 |
| 221c1dd2 C1 | 12 | 14 | 1 |
| 1962f8ef C2 | 108 | 0 | 1 |
| 4aea7ba2 C3 | 298 | 0 | 1 |

Lines beginning `<<<SLICE ` / `<<<END ` at `4aea7ba2`: `.agent/plan.md` **0 / 0**,
`.agent/live_review.md` **0 / 0**, `.agent/decisions.md` **0 / 0**,
`tests/ui_server/test_diff_endpoint.py` **0 / 0**; the two authored controls,
`.agent/authored/f256-r6.md` and `.agent/last_block.md`, are **3 / 3** each by
construction. `git ls-files .remedy-wt | wc -l` = **0**. After the red-proof worktree
was removed, `git worktree list` shows only
`/home/decodeux/Repos/remedy  4aea7ba2 [feature/f256-diff-viewer-completion]`.

**G2 TRANSPORT.** One digest comparison. `git show 250529ba:.agent/authored/f256-r6.md`
and the reviewer's own original `.remedy-wt/f256-r6-block.md` both hash to
`9c873ffb6f5d31498d0305f4e7ebe10412a3d7e739ff59516882e5fc65516b67` at **27077 bytes** —
EQUAL. That original predates this worker, so the reading covers the EMISSION and not
merely the worker's self-consistency. At C0b,
`b402da84:.agent/authored/f256-r6.md` and `b402da84:.agent/last_block.md` are ONE blob
id, `2fd3a32f39c5b70ca4dd0d9257a2c03c411f0df6`.

**G3 THE PLAN AT C1.** `221c1dd2:.agent/plan.md` byte-equal to the `PLANF256R6` slice
including the trailing newline → **True**. `wc -l` = **35** (< 50). Lines exactly
`## Goal` = **1**; lines exactly `## Next Steps` = **1**.

**G4 THE RECORD AT C2**, two readers per appended file.

(a) the `08f6218a` blob + a newline + the slice == the C2 blob:
- `.agent/live_review.md` with `GATEF256R5` → **True**; 1352347 → 1356682 bytes; the
  pre-round blob is a byte PREFIX → **True**. NEGATIVE CONTROL: the script measured the
  FIRST appended paragraph as the leading 307 bytes of the slice and flipped the byte at
  slice offset **153** (`'D'`), inside it → equality now **False**.
- `.agent/decisions.md` with `DECF256D4` → **True**; 696427 → 702832 bytes; the
  pre-round blob is a byte PREFIX → **True**. NEGATIVE CONTROL: first appended paragraph
  168 bytes, byte at slice offset **84** (`'b'`) flipped → equality now **False**.

(b) N counted BY THE SCRIPT from each slice, empty trailing unit ignored:
- `GATEF256R5` → **N = 7**; the last 7 blank-line units of `.agent/live_review.md`
  match those paragraphs IN ORDER → **True**.
- `DECF256D4` → **N = 10**; the last 10 blank-line units of `.agent/decisions.md`
  match those paragraphs IN ORDER → **True**.

**G5 THE LEDGER AT C2.** The `1962f8ef` blob beside the `08f6218a` blob:

| Reader | base | C2 | delta |
|---|---|---|---|
| `^- R-\d+ — ` (registrations) | 293 | 293 | 0 |
| registrations all DISTINCT | True | True | — |
| `^Done: R-\d+ — ` | 43 | 43 | 0 |
| `^Landed: R-` | 11 | 11 | 0 |
| `^Gate: F\d+ R\d+ — ` | 101 | 102 | **+1** |
| OPEN SET, computed AS A SET | 252 | 252 | 0 |

Every figure UNMOVED except the gate count, which rises by exactly ONE, as a round that
registers and resolves nothing should. `Gate: F256 R5` occurs exactly **1** time.

**G6 THE MEASUREMENT AT C3.** Command
`python3 -m pytest tests/ui_server/test_diff_endpoint.py::TestDiffEndpointPerfBudget -q -s`,
exit **0**, `2 passed in 1.86s`, in the primary checkout. The class prints its figures;
this is the run they were read from:

| Figure | Acceptance count (10,000) | Linear reference (1,000) |
|---|---|---|
| median request time | **0.1331 s** | **0.0269 s** |
| minimum request time | **0.1282 s** | not printed separately |
| maximum request time | **0.1489 s** | not printed separately |
| serialised JSON response | **1,045,960 bytes** | — |

RATIO measured in `test_the_route_stays_linear_in_body_lines`, both medians from that
same run: `0.1339 s / 0.0269 s` = **4.97**, against the ceiling 20. (The 10,000-line
median differs between the two tests — 0.1331 s in the recording test, 0.1339 s in the
ratio test — because they are two independent sets of five requests; each test's
docstring records its own.)

The four pinned readings, asserted in `_pin_the_served_work` and therefore true of the
passing run: `status` **200**, `available` **True**, `truncated` **False**, exactly
**1** file entry, and the body lines summed across its hunks **10000**. The pins are
live rather than decorative: under G7 mutation (i) the very same assertions printed
`assert True is False` on `truncated` and served `@@ -1,5000 +1,5000 @@`.

`DIFF_VIEW_MAX_BODY_LINES` read from `packages/orchestration/diff_parser.py` is
**20_000**, and the Acceptance count 10,000 is strictly below it — asserted directly in
`test_the_acceptance_fixture_is_served_inside_the_hang_net`, not merely implied.

EVERY FIGURE WRITTEN INTO A DOCSTRING IS A FIGURE THAT RUN PRODUCED. The recording
test's docstring carries 0.1331 / 0.1282 / 0.1489 s and 1,045,960 bytes; the ratio
test's carries 0.0269 s, 0.1339 s and 4.97. The only edit made to the file after that
run was writing those very figures into the two docstrings, which cannot change what a
later run measures. No figure from the block's `DECF256D4` slice was transcribed into a
docstring; the docstrings' only borrowed number is the 0.105 s the EXISTING
`test_the_huge_diff_parses_inside_the_recorded_perf_budget` docstring already records
for the parser alone, quoted as that test's figure and attributed to it.

Reused from `TestDiffEndpoint`: `_get` (a `@staticmethod`, called unchanged) and the
module-level `_make_job`. Re-declared for the new class, per constraint 7: the autouse
fixture `_setup_perf_job`, the start helper `_start_perf_server`, the fixture generator
`_generated_huge_endpoint_diff` (the twin named in S3, with the comment S3 requires),
the request timer `_timed_diff_requests` and the shared pin `_pin_the_served_work`.
`TestDiffEndpoint` is neither edited nor subclassed.

`python3 -m ruff check tests/ui_server/test_diff_endpoint.py` → exit **0**,
`All checks passed!`.

**G7 THE RED-PROOF AT C3**, in the disposable worktree `.remedy-wt/f256-r6-redproof` at
`4aea7ba2`, never in the primary checkout. Command
`["python3","-B","-m","pytest","tests/ui_server/test_diff_endpoint.py","-q"]` with `cwd`
set to the WORKTREE; `__pycache__` purged inside the worktree before every run.

| Run | exit | result |
|---|---|---|
| UNMUTATED CONTROL (first) | 0 | 8 passed in 2.53s |
| (i) `DIFF_VIEW_MAX_BODY_LINES = 20_000` → `= 5_000` | **1** | 2 failed, 6 passed in 1.45s |
| (ii) one whole-input scan per line inserted after `stripped = line.strip()` | **1** | 1 failed, 7 passed in 13.97s |
| CONTROL AGAIN (after the last revert) | 0 | 8 passed in 2.51s |

(i) reddened BOTH new tests, and each names the right assertion:
`test_the_acceptance_fixture_is_served_inside_the_hang_net` at line 395 —
`AssertionError: the Acceptance fixture is 10000 body lines and DIFF_VIEW_MAX_BODY_LINES
is 5000: the fixture would be truncated` / `assert 10000 < 5000` — and
`test_the_route_stays_linear_in_body_lines` at line 359, the `truncated is False` pin —
`assert True is False`, with the served hunk header `@@ -1,5000 +1,5000 @@`.

(ii) THE EXACT LINE INSERTED, immediately after `        stripped = line.strip()` inside
`parse_unified_diff_to_view`:

    _quadratic_probe = diff_text.replace("body", "BODY")

indented to the loop body. It scans the WHOLE input on every iteration, so the pipeline
becomes quadratic in body lines while every answer is unchanged. THE RATIO THE MUTATED
RUN MEASURED: **42.38** — `AssertionError: 10000 body lines answered in 1.2630s against
0.0298s at 1000, a ratio of 42.38 against ceiling 20 for a size ratio of 10` /
`assert 42.38419809705108 < 20`, at `tests/ui_server/test_diff_endpoint.py:480`. The
assertion that went red is the RATIO assertion in
`test_the_route_stays_linear_in_body_lines`; the hang net did NOT trip (the 10,000-line
median was 1.2630 s against 5.0 s), which is exactly the separation DECISION F256 D4
designs for — a regression that changes no answer and only costs time is caught by the
ratio and not by the absolute bound.

Each mutation was applied ALONE and reverted before the next.
`git status --porcelain` inside the worktree was `''` after every revert, and the parser
file was restored byte-identical to its committed content → **True**.

**G8 THE SUITES AT C3**, one pytest process at a time, from the repository root, in the
PRIMARY checkout:

| Command | exit | result | wall clock |
|---|---|---|---|
| `python3 -m pytest tests/ui_server/ -q` | 0 | 497 passed in 30.43s | **30.71s** |
| `python3 -m pytest tests/orchestration/test_diff_parser.py -q` | 0 | 43 passed in 2.35s | 2.56s |
| `python3 -m pytest tests/orchestration/test_diff_view_source.py -q` | 0 | 15 passed in 0.26s | 0.46s |
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | 664 passed, 4 skipped in 5.61s | 5.87s |
| `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` | 0 | 16 passed in 0.29s | 0.51s |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | 42 passed in 20.69s | 20.90s |

`tests/ui_server/` COST OF THIS ROUND: 495 passed in about 30 s at `08f6218a` (the
reviewer's own reading) against **497 passed in 30.43 s** here — two tests added, and
the suite's wall clock is unchanged inside its own run-to-run spread. The whole new
class costs about 1.9 s when run alone. `apps/ui/dist` was already warm and was not
rebuilt.

**G-push.** `git push -u origin feature/f256-diff-viewer-completion` runs AFTER this
commit. Its outcome is not written here — a file cannot record the result of the push
that carries it — and is verified instead by `git rev-parse HEAD` equalling
`git rev-parse origin/feature/f256-diff-viewer-completion`.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| whole block | `.agent/authored/f256-r6.md` | sha256 equal to `.remedy-wt/f256-r6-block.md`, 27077 bytes (G2) |
| whole block | `.agent/last_block.md` | same blob id as the authored path (G2) |
| `PLANF256R6` | `.agent/plan.md` | byte-equal whole-file replacement, trailing newline included (G3) |
| `GATEF256R5` | `.agent/live_review.md` | base + newline + slice, negative control rejected (G4) |
| `DECF256D4` | `.agent/decisions.md` | base + newline + slice, negative control rejected (G4) |

Every slice was extracted from the COMMITTED `250529ba` blob by
`.remedy-wt/f256r6_extract.py`, never from the prompt (constraint 3).

## Deviations & assumptions

1. **MY FIRST MUTATION (ii) DID NOT REDDEN THE FILE, AND IS REPORTED AS A FAILED
   ATTEMPT.** The block leaves the exact inserted line to the worker. My first choice,
   `_quadratic_probe = diff_text.count(stripped)`, is a whole-input scan and is
   genuinely quadratic, but it is too CHEAP: the run came back exit **0**, `8 passed in
   4.21s`, because `str.count` added only about 0.17 s per 10,000-line request and the
   measured ratio stayed under 20. Nothing was weakened in response — no constant was
   changed and no assertion touched. I measured five candidate whole-input scans at both
   fixture sizes (`.remedy-wt/f256r6_scan_bench.py` and a follow-up one-liner) and chose
   `diff_text.replace("body", "BODY")`, which costs about 1.13 s per 10,000-line request
   and 0.010 s per 1,000-line one, and reddened at ratio 42.38. Reviewer note: the
   ceiling of 20 is therefore NOT tripped by every whole-input scan — a scan cheap
   relative to the parser's own per-line cost stays inside it. That is the guard being
   coarse, which is what `DECF256D4` argues for, but it is a real limit on its reach and
   is stated here rather than left implicit.
2. **Shell-guard re-expressions (constraint 6).** One command FORM was refused this
   round: `python3 -m ruff check … && echo "exit $?"` was rejected as "multiple
   operations". It was re-expressed, never skipped and never weakened, as a `python3 -c`
   `subprocess.run` that prints the real return code (reported under G6 as exit 0). To
   avoid the refused forms altogether, every multi-step check was written as a file under
   the gitignored `.remedy-wt/` and run with `python3`: `f256r6_extract.py` (slice
   extraction), `f256r6_append.py` (C2), `f256r6_gates.py` (G1 range half, G3, G4, G5),
   `f256r6_redproof.py` (G7), `f256r6_suites.py` (G8), plus the two throwaway probes
   `f256r6_probe_bytes.py` and `f256r6_scan_bench.py`. `git ls-files .remedy-wt` is **0**.
3. **The response byte length is reconstructed, and the reconstruction was verified
   byte-for-byte before it was written.** `TestDiffEndpoint._get` returns the DECODED
   body, so the test computes `len(json.dumps(body, default=str).encode())`. Probe
   `.remedy-wt/f256r6_probe_bytes.py` compared that value against the raw response bytes
   and the `Content-Length` header of a real 10,000-line response: all three are
   **1045960**, and the re-serialised bytes are IDENTICAL to the raw ones, because
   `_send_json` writes exactly `json.dumps(data, default=str).encode()`. The test carries
   a comment saying so.
4. **Both new tests `print` their measured figures.** "Recorded" is half of what F037's
   Acceptance asks for, so a run of the class reports the numbers its docstrings carry.
   pytest captures stdout, so a green suite run shows nothing and `tests/ui_server/`
   output is unchanged; `-s` or `-rP` surfaces it. A WHY comment above the first print
   says this. This is a choice, not an order: S4 only requires the figures in the
   docstring.
5. **One extra shared helper beyond the three constraint 7 names.**
   `_pin_the_served_work` is a `@staticmethod` on the new class holding the four pins S4
   requires, so both tests pin the same work in the same words. It is new code in the new
   class; nothing existing was touched.
6. **NO EXISTING ASSERTION WAS WEAKENED, DELETED OR RELAXED** (constraint 8). The C3
   diff is **+298 / −0** — zero deleted lines — so every one of `TestDiffEndpoint`'s six
   tests is byte-unchanged, and the module went from 6 tests to 8.
7. **No production file was edited.** `git diff --name-only 08f6218a..4aea7ba2` contains
   no path under `packages/`, `apps/` or `docs/`. `diff_parser.py` changed only inside
   the disposable worktree, and was restored byte-identical there before the worktree was
   removed.
8. **No `Done:` or `Gate:` paragraph of my own** appears anywhere. `GATEF256R5` and
   `DECF256D4` are reviewer-authored and were applied as slices, byte for byte, append
   only.
9. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 in that
   order, one commit each, nothing extra, nothing dropped, nothing reordered.
10. **The 4.97 ratio measured here is lower than the 7.42 `DECF256D4` records at the same
    base.** Nothing was changed to obtain it; the difference is run-to-run spread in the
    1,000-line median, which is tens of milliseconds and is where the fixed per-request
    overhead dominates. Both figures sit well under the ceiling and in the direction
    `DECF256D4`'s overhead paragraph predicts.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | `250529ba` |
| C0b mirror into `.agent/last_block.md` | done | `b402da84` |
| C1 advance `.agent/plan.md` | done | `221c1dd2` |
| C2 append the R5 verdict and DECISION F256 D4 | done | `1962f8ef` |
| C3 the end-to-end measurement | done | `4aea7ba2` |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene and structure | done | STOP `False` twice; base and branch as ordered; porcelain 0 six times; both residues empty; five single-parent commits, all under 500 |
| G2 transport | done | one digest, equal at 27077 bytes; C0b one blob id |
| G3 the plan at C1 | done | byte-equal True; 35 lines; 1 and 1 |
| G4 the record at C2 | done | both appends True, both negative controls False; N = 7 and N = 10 |
| G5 the ledger at C2 | done | only `^Gate:` moved, +1; `Gate: F256 R5` exactly once |
| G6 the measurement at C3 | done | 2 passed, exit 0; median 0.1331 s, ratio 4.97, 1,045,960 response bytes; `DIFF_VIEW_MAX_BODY_LINES` 20_000 |
| G7 the red-proof at C3 | done | control 0, both mutations exit 1, control again 0; mutation (ii) needed a second, heavier scan — see deviation 1 |
| G8 the suites at C3 | done | all six suites exit 0; `tests/ui_server/` 497 passed in 30.43s against 495 at base |
| push | done | run after C4; verified by the branch tip equalling `origin/feature/f256-diff-viewer-completion` |

## Next

Measure the CLIENT half of the same fixture in vitest — `buildDiffRowModels` and
`diffRowWindowForViewport` over a 10,000-row envelope — which is round 7. The recording
of every measured number into the Built State of `docs/roadmap/features/T5_F256.md` is
round 8.
