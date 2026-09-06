# Handoff — F260 One world · round 14 · ONE SPELLING FOR THE RUN-LOG JOIN

## Session

SESSION 5 of feature F260 · round 14 · rounds so far 14

Context self-assessment (amend0905-throughput): context is comfortable and was
never a constraint. WALL CLOCK was again the whole cost — `tests/orchestration/`
alone ran 738.68 s and `tests/cli/` 303.30 s, so G7 spent roughly seventeen
minutes of serial suite time on top of G6's three worktree runs. The 25-round /
7-session soft limit is NOT reached (14 rounds, 5 sessions), but the plan's
remaining scope is larger than the eleven rounds left, so split-and-close is the
likely endgame and this round leaves a self-consistent tree.

## Range

Review of `4f265f91cbdf2f4c327e9dd303b8cd78c146618d`..`HEAD`.

NINE commits plus this one, all single-parent. Eight of the nine are EXACTLY the
Bundle's ordered sequence C0a → C0b → C1 → C2 → C3 → C4 → C5 → C6. There is ONE
EXTRA COMMIT, `c296ee97`, inserted after C6 and before this handback; it is
deviation 3 below and it is the only departure from the ordered sequence. No
commit was dropped and nothing was reordered. Largest insertion count 397
(`.agent/authored/f260-r14.md`, a single `.agent/**` state write, exempt under
the AGENTS.md DECISION F104 D1 counting rule); largest CODE commit 35 insertions
(`dcfe7a36`). Nothing approached the 500-insertion cap.

## Commits

`+/-` taken from `git log --numstat`, never re-derived by eye.

### 11fa257b f260: save the round 14 step block verbatim under agent authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r14.md | +397 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r14-block.md`, proved by `filecmp.cmp(shallow=False)` = True and sha256 equal to the delegation digest BEFORE staging |

### 755b0a98 f260: mirror the round 14 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +319 / -240 | C0b — same source file, same copy route, same two proofs |

### a7a47473 f260: rewrite the plan for round 14, the run-log join
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21 / -22 | C1 — whole-file replacement by the PLAN slice plus one trailing newline; 2530 bytes, 48 lines, under the 50-line cap |

### f5f959d0 f260: book the round 13 PASS verdict and record DECISION F260 D6
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — GATE_R13 appended; 931365 → 937682 bytes |
| .agent/decisions.md | +3 / -0 | C2 — DEC_D6 appended in the SAME commit, after the live_review append; 839361 → 842038 bytes |

### 24596473 f260: append the four round 13 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +8 / -0 | C3 — SLIP14, SLIP15, SLIP16, SLIP17 appended IN ORDER, blank-line separated; 115506 → 117457 bytes |

### dcfe7a36 f260: give RunLogWriter a data root and build its directory with run_log_dir
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_log.py | +5 / -5 | C4 — SPEC (1): the import at 34, the class docstring at 97, the one-line WHY comment above `__init__`, `runs_root` → `data_root`, and the three path lines collapsed to two |
| tests/test_run_log.py | +30 / -23 | C4 — SPEC (2): all 21 `runs_root=tmp_path` → `data_root=tmp_path`, the two constraint-3 observers re-spelled LITERALLY as `tmp_path / "runs" / str(job_id)`, plus ONE new default-root test |

### 3126d0cc f260: move the seven production run-log call sites onto the data root
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/timeline.py | +2 / -2 | C5 — site 65 → `data_root=Path(data_dir)`; `runs_dir` left the module-level import (now unused), `run_log_dir` stays for site 76 |
| packages/orchestration/worker_queue.py | +1 / -2 | C5 — site 489 → `data_root=root`; the function-local `runs_dir` import removed (F401) |
| packages/orchestration/patch_apply.py | +2 / -6 | C5 — BOTH pairs (527-528 and 565-566): the `runs_root` local deleted, `data_root=data_dir` passed, and each function's local `runs_dir` import removed |
| packages/orchestration/patch_revert.py | +2 / -3 | C5 — site 245-246: the local deleted, `data_root=actual_data_dir` passed; `runs_dir` left the module-level import at 33 |
| packages/orchestration/safe_points.py | +1 / -2 | C5 — site 675: the `runs_root` argument DROPPED entirely; the function-local `runs_dir` import removed |
| packages/orchestration/pingpong_job.py | +1 / -2 | C5 — site 3182: the `runs_root` argument DROPPED entirely; the function-local `runs_dir` import removed |
| packages/orchestration/prompt_trace.py | +1 / -1 | C5 — COMMENT ONLY at 215: `<runs_root>/<job_id>/` → `<data_root>/runs/<job_id>/`. No code in this file changed |

### 34b14577 f260: move the last two run-log test call sites onto the data root
| Path | +/- | Reason |
|---|---|---|
| tests/test_test_runner.py | +1 / -1 | C6 — site 344 → `data_root=tmp_path`; the written path is unchanged by construction |
| tests/cli/test_propose_cli.py | +1 / -2 | C6 — site 340 → `data_root=tmp_path`; the local `runs_dir` at 339 WAS unused afterwards and was deleted, as SPEC (4) permits |

### c296ee97 f260: stop respelling the deleted runs-dir alias in a new test comment
| Path | +/- | Reason |
|---|---|---|
| tests/test_run_log.py | +1 / -1 | EXTRA COMMIT, deviation 3 — the C4 comment on the new test spelled `_runs_dir_default`, which made G5(a)'s word-bounded reading 1 instead of 0. Reworded to "the deleted module-level runs-dir alias" |

### C7 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C7 — a handoff cannot table the commit that writes it (R-0149 pattern). Constraint 9: no gate reading was taken after this file existed; the reviewer measures C7's own insertion count at the next gate |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f260-r14-mut HEAD` | exit 0; detached HEAD at `c296ee97` |
| `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f260-r14-mut` | exit 0; removed BY EXACT PATH. No glob was used anywhere |
| `git worktree prune` | exit 0; `git worktree list` then shows the primary checkout and the ELEVEN pre-existing `remedy/job-*` worktrees only, no `f260-r14-mut` row |
| `git push -u origin feature/f260-one-world` | runs after this file is committed; see the note under Verification |

No PR created. No PR merged. No `gh` command run. No force push. No branch
deleted. No file under `.remedy-wt/` was ever `git add`ed. `.agent/STOP` was
checked at the start of the round and did not exist.

## Verification

ONE LINE PER GATE, with its REAL exit code. Every suite ran SERIALLY — never two
at once — captured to a file under `.remedy-wt/`, and read from the capture.
Because the sandbox guard rejects `$?` and shell loop forms, every exit code was
taken from a Python `subprocess.run(...).returncode` and written into the capture
as a trailing `__EXIT_CODE__` line; no exit code in this table was inferred from
output text.

| Gate | Command / reading | Exit | Result |
|---|---|---|---|
| G1 | `sha256sum .agent/authored/f260-r14.md .agent/last_block.md` | 0 | BOTH `59fb3c47a421fa4e14fe13f8afa6761a3a97caebc764ca0101bf8b22935e0d57`, equal to the digest the delegation names. ONE comparison, not a chain |
| G2(a) live_review | exact-image byte equality | 0 | `post == pre + b"\n" + GATE_R13 + b"\n"` is **True**, and `post[:len(pre)] == pre` is True. **931365 → 937682** bytes. Recipe derived from the target's own terminal byte, measured at the base |
| G2(b) live_review | structural, whole file split on `"\n\n"` | 0 | N counted BY THE SCRIPT = **1**; total blank-line units **434 → 435**; the last 1 unit EQUALS the slice's 1 paragraph. Marker lines in the file: **0** |
| G2(c) live_review | negative control, IN MEMORY | 0 | byte at offset **931371**, inside the FIRST appended paragraph, XOR-flipped `b' '` → `b'\x00'`: reader (a) REJECTS, reader (b) REJECTS. After restore both ACCEPT and the restored image equals the disk image |
| G2(a) decisions | exact-image byte equality | 0 | `post == pre + b"\n" + DEC_D6 + b"\n"` is **True**, prefix check True. **839361 → 842038** bytes |
| G2(b) decisions | structural, whole file split on `"\n\n"` | 0 | N counted BY THE SCRIPT = **1**; total units **1892 → 1893**; last 1 unit EQUALS the slice's 1 paragraph (DEC_D6 is a heading line plus a body line with no blank between them). Marker lines: **0** |
| G2(c) decisions | negative control, IN MEMORY | 0 | byte at offset **839367** flipped `b'E'` → `b'e'`: both readers REJECT, both ACCEPT after restore |
| G2(d) | census after C2 | 0 | `.agent/live_review.md`: `^Gate: ` **23** (base 22) · registrations **300** over **300** DISTINCT ids · `^Done: ` **5** lines over **3** DISTINCT ids · **open set 297 BY DISTINCT ID**. `.agent/decisions.md`: `### DECISION F260 D5` headings **1** (unchanged from base 1), `### DECISION F260 D6` headings **1** (base 0) |
| G3 (plan) | `.agent/plan.md` | 0 | disk bytes `== PLAN slice + b"\n"` is **True**; **2530** bytes, **48 lines**, under the 50-line cap; carries `## Goal` and `## Next Steps`. Marker lines: 0 |
| G3 (slips) | `.agent/prose_slips.md` | 0 | `post == pre + b"\n" + SLIP14 + b"\n\n" + SLIP15 + b"\n\n" + SLIP16 + b"\n\n" + SLIP17 + b"\n"` is **True**. Bytes **115506 → 117457**. Blank-line units **144 → 148**, a rise of exactly FOUR; the last four units EQUAL SLIP14…SLIP17 IN ORDER. Marker lines: 0 |
| G4 | scratch probe under `.remedy-wt/`, run BEFORE C4 while `run_log.py` still held the old join | 0 | three printed pairs, all EQUAL — full transcript below. `_runs_dir_default is runs_dir` printed **True**, which is the identity the equality rests on |
| G5(a) | bytes `root / self._job_id` in `run_log.py` | 0 | base **1** → C6 **0** |
| G5(a) | word-bounded `_runs_dir_default` over the file set | 0 | base **2** (both in `run_log.py`) → C6 **0**. Intermediate reading of **1** at `34b14577`, in a comment, is deviation 3 |
| G5(b) | AST reading, calls to `run_log_dir` in `run_log.py` | 0 | base **0** → C6 **1**, exactly as ordered |
| G5(c) | word-bounded `runs_root` over the file set | 0 | base **41 in 11 files** (the block says 37 — deviation 1) → C6 **0 in 0 files**. NO SURVIVOR. Enumeration: `git ls-files` IN PYTHON, filtered to `.py` under `packages/`, `apps/`, `tests/` = **1030** files; `tests/test_data_paths.py` confirmed present in the set |
| G6(i) | control, disposable worktree, `python3 -B`, the four-file selection | **0** | **261 passed** in 2.12 s, 0 FAILED. `__pycache__` dirs purged then RE-ENUMERATED as **0**. Module resolution CONFIRMED to the worktree: `data_paths.__file__` = `/home/decodeux/Repos/remedy/.remedy-wt/f260-r14-mut/packages/orchestration/data_paths.py`, live body printed as `return runs_dir(root) / str(job_id)` |
| G6(ii) | revert-target uniqueness, then the mutation | **1** | exact bytes `    return runs_dir(root) / str(job_id)` occur **EXACTLY 1** time before mutating. After replacing with `    return runs_dir(root) / (str(job_id) + "_MUTATED")` the live body re-printed WITH `_MUTATED`. **IT WENT RED: exit 1, 32 failed, 229 passed.** Failing files: `tests/test_patch_apply.py` **18**, `tests/test_timeline.py` **8**, `tests/test_data_paths.py` **3**, `tests/test_run_log.py` **3**. BOTH constraint-3 observers are AMONG the failures: `test_creates_job_directory` True, `test_path_is_inside_job_directory` True |
| G6(iii) | restore + clean worktree + removal | **0** | original line restored (mutated count 1 → 0), `__pycache__` re-enumerated at 0, live body re-printed as the original, control re-run **261 passed exit 0**. That worktree's `git status --porcelain` EMPTY (`''`) and `git diff HEAD --stat` EMPTY (`''`). Worktree removed BY EXACT PATH, then `git worktree prune` |
| G7(1) | `pytest tests/test_run_log.py tests/test_data_paths.py tests/test_timeline.py tests/test_patch_apply.py tests/test_test_runner.py -q -p no:randomly` | **0** | **304 passed** in 3.17 s, 0 FAILED |
| G7(2) | `pytest tests/orchestration/ -q -p no:randomly` | **0** | **12805 passed, 10 skipped**, 1 warning in 738.68 s. `^FAILED` lines **0**, `^ERROR` lines **0**. Same pass count as round 13's reading |
| G7(3) | `pytest tests/cli/ -q -p no:randomly` | **0** | **1537 passed** in 303.30 s, 0 FAILED. Canary presence verified separately: `pytest tests/cli/test_golden_path.py --collect-only` exit 0, **42 tests collected**, so the canary is inside this selection |
| G7(4) | `python3 -m apps.cli.grouped integrity check --json` | **0** | `"passed": true`, `"fail_count": 0`, `"check_count": 5`; all five checks `"status": "pass"` |
| G8 (lint) | `python3 -m ruff check` over the edited `.py` paths — **COUNTED MYSELF: ELEVEN** | **0** | `All checks passed!` |
| G8 (tree) | `git status --porcelain` / `git ls-files .remedy-wt` | 0 / 0 | both EMPTY (`''` each) |

THE ELEVEN EDITED `.py` PATHS, counted rather than recalled: `run_log.py`,
`timeline.py`, `worker_queue.py`, `patch_apply.py`, `patch_revert.py`,
`safe_points.py`, `pingpong_job.py`, `prompt_trace.py`, `tests/test_run_log.py`,
`tests/test_test_runner.py`, `tests/cli/test_propose_cli.py`. The two
pre-existing errors G8 warns about (`UP035` at `dag_schedule.py:36`, `F821` at
`gauntlet_injection.py:286`) were not approached; neither file is in the change
set.

G4 PROBE TRANSCRIPT — the printed pairs, not a summary of them. Run under
`.remedy-wt/` with `python3 -B`, BEFORE `run_log.py` was edited:

    data_paths module   : /home/decodeux/Repos/remedy/packages/orchestration/data_paths.py
    _runs_dir_default is runs_dir: True
    CASE1 lhs runs_dir(R)/str(J) : /tmp/f260r14-explicit-ezir4rmu/runs/11111111-2222-3333-4444-555555555555
    CASE1 rhs run_log_dir(J, R)  : /tmp/f260r14-explicit-ezir4rmu/runs/11111111-2222-3333-4444-555555555555
    CASE1 equal                  : True
    CASE2 REMEDY_DATA_DIR        : /tmp/f260r14-datadir-gjnogtan
    CASE2 lhs _runs_dir_default()/str(J): /tmp/f260r14-datadir-gjnogtan/runs/11111111-2222-3333-4444-555555555555
    CASE2 rhs run_log_dir(J, None)     : /tmp/f260r14-datadir-gjnogtan/runs/11111111-2222-3333-4444-555555555555
    CASE2 equal                  : True
    CASE3 lhs run_log_dir(UUID, R)      : /tmp/f260r14-explicit-ezir4rmu/runs/11111111-2222-3333-4444-555555555555
    CASE3 rhs run_log_dir(str(UUID), R) : /tmp/f260r14-explicit-ezir4rmu/runs/11111111-2222-3333-4444-555555555555
    CASE3 equal                  : True
    G4 ALL THREE PAIRS EQUAL: True

"NO LAYOUT CHANGE" IS THEREFORE A MEASUREMENT AND NOT A CLAIM.
`<data_root>/runs/<job_id>/<run_id>.jsonl` is where a run log lived before this
round and where it lives after it; only WHO SPELLS THE JOIN moved. The re-key to
`<run_id>` is DECISION F260 D1's own work and was NOT performed here.

THE RED-PROOF COULD FAIL AND DID. The two tests constraint 3 names still assert
the writer's directory against a HAND-SPELLED right-hand side — now
`tmp_path / "runs" / str(job_id)` — and the three `run_log_dir` tests in
`tests/test_data_paths.py` are literal for the same reason and were not touched.
Mutating the one function body reddens 32 tests across four files, both named
observers among them. That is 32 rather than round 13's 17 because the selection
changed (`tests/test_run_log.py` replaces `test_cockpit.py` and
`test_trust_report.py`) AND because `RunLogWriter` itself now routes through the
accessor, so every `patch_apply` test that reads a run-log path moved from 6
failures to 18.

The push runs AFTER this file is committed, so its transcript cannot appear in
the commit that carries it (the R-0149 self-reference pattern, same reason the C7
row of the commit table has no `+/-`). Its outcome is verifiable directly:
`origin/feature/f260-one-world` points at the C7 commit.

## Authored-text proofs

| Slice | Target | Shape | Proof |
|---|---|---|---|
| the whole block | `.agent/authored/f260-r14.md` | file copy | `shutil.copyfile`, then `filecmp.cmp(shallow=False)` = True, then sha256 equal to the delegation digest |
| the whole block | `.agent/last_block.md` | file copy | same source, same route, same two proofs |
| PLAN | `.agent/plan.md` | whole-file REWRITE | disk bytes `== slice + b"\n"`, True (G3) |
| GATE_R13 | `.agent/live_review.md` | APPEND | exact-image equality + structural reader + in-memory negative control (G2 a/b/c) |
| DEC_D6 | `.agent/decisions.md` | APPEND, same commit, after live_review | exact-image equality + structural reader + in-memory negative control (G2 a/b/c) |
| SLIP14, SLIP15, SLIP16, SLIP17 | `.agent/prose_slips.md` | APPEND, IN ORDER | exact-image equality over the derived recipe, plus the four-unit reading (G3) |

Every slice was extracted from the COMMITTED `.agent/authored/f260-r14.md` — not
from a retype — by taking the lines strictly between its marker lines, joined by
`"\n"`, with no trailing newline. Each of the FOURTEEN marker lines was verified
to occur EXACTLY ONCE, at file lines 323, 372, 374, 376, 378, 381, 383, 385, 387,
389, 391, 393, 395 and 397, and each target file was re-read afterwards and
contains **ZERO** lines beginning `BEGIN ` or `END `. NO MARKER LINE REACHED ANY
TARGET FILE.

## Deviations & assumptions

**1. G5(c)'s BASE COUNT IS 41, NOT THE 37 THE GATE STATES; THE ELEVEN FILES ARE
EXACTLY AS STATED.** Measured at the base with the gate's own word-bounded reading
over the same 1030-file enumeration: `\bruns_root\b` occurs **41** times in
**11** files — `patch_apply.py` 6, `run_log.py` 4, `patch_revert.py` 3,
`test_run_log.py` 21, and 1 each in `pingpong_job.py`, `prompt_trace.py`,
`safe_points.py`, `timeline.py`, `worker_queue.py`, `tests/cli/test_propose_cli.py`,
`tests/test_test_runner.py`. The eleven files ARE the code files of the change
set, exactly as constraint 4 says. The gap of four is four LINES that carry the
token TWICE: `patch_apply.py:528` and `:566` and `patch_revert.py:246` each read
`runs_root=runs_root`, and `run_log.py:114` reads
`runs_root if runs_root is not None`. 41 − 4 = 37, so the block's number is a
LINE count where its own words order an OCCURRENCE count. Nothing on disk is
affected: the C6 reading is **0** under either reading, and the gate's binding
clause — "any survivor FAILS the gate" — is met with no survivors. Recorded per
constraint 1: the gate was executed as written and the discrepancy declared, not
edited away. SPEC (2)'s own sub-count of TWENTY-ONE in `tests/test_run_log.py`
re-measured at exactly **21**.

**2. SPEC (3) SAYS "EIGHT CONSTRUCTIONS PASS `runs_root`"; THERE ARE SEVEN
CONSTRUCTIONS AND ONE COMMENT.** Re-grepped at the base before editing, all line
numbers matched the block: `timeline.py:65`, `worker_queue.py:489`,
`patch_apply.py:527-528`, `patch_apply.py:565-566`, `patch_revert.py:245-246`,
`safe_points.py:675`, `pingpong_job.py:3182` — **SEVEN** `RunLogWriter(...)`
constructions — plus `prompt_trace.py:215`, which is a COMMENT and constructs
nothing. Eight SITES, seven CONSTRUCTIONS. The block's own enumeration is seven
bullets, so the numeral disagrees with the list beside it. All eight sites moved;
the count I re-measured and report is SEVEN constructions. The PLAN slice
inherits the same numeral ("Eight production call sites") and was applied BYTE FOR
BYTE anyway, per constraint 1.

**3. ONE EXTRA COMMIT, `c296ee97`, OUTSIDE THE BLOCK'S ORDERED SEQUENCE.** The
WHY comment SPEC (2) does not order but which I wrote above the new default-root
test read "the deleted `_runs_dir_default` alias". G5(a) is a WORD-BOUNDED
identifier search that does not strip comments, so at `34b14577` it read **1**,
not the ordered **0** — the single occurrence being that comment, in
`tests/test_run_log.py`. I did not reshape any code, any test or any assertion:
I reworded MY OWN comment to "the deleted module-level runs-dir alias", which
removes the re-spelling of a symbol this round deletes and is precisely what the
gate measures. Both readings are reported in the table (1 at `34b14577`, 0 at
`c296ee97`). Declared here because ANY departure from the ordered commit sequence
belongs in this section even when it is correct (finding R-0485).

**4. THE `patch_apply.py` `None` PASS-THROUGH IS INTENTIONAL AND UNGUARDED, AS
SPEC (3) DIRECTS.** Both `_emit_run_log` and `_emit_proof_run_log` now call
`RunLogWriter(job_id=job.id, data_root=data_dir)` where `data_dir` may be `None`.
`run_log_dir(job_id, None)` resolves the process data root through `runs_dir` →
`resolve_data_root`, which is EXACTLY what `RunLogWriter` did with a `None`
`runs_root` before — G4's CASE2 measures that equality. No guard was added and
the two `runs_root = ... if data_dir is not None else None` locals are gone.

**5. TWO CALL SITES DROPPED THE ARGUMENT ENTIRELY RATHER THAN RE-SPELLING IT.**
`safe_points.py:675` and `pingpong_job.py:3182` both passed `runs_root=runs_dir()`
— the process data root, spelled at the call site. SPEC (3) orders the argument
DROPPED, so it is: `RunLogWriter(job_id, run_id=BUDGET_TICK_RUN_ID)` and
`RunLogWriter(job.job_id)`. The resolution now happens INSIDE `run_log_dir`
instead of at the call site; the resulting path is identical (G4 CASE2). Both
files' function-local `runs_dir` imports became unused and were removed.

**6. IMPORT REMOVALS, PER FILE, AS CONSTRAINT 7 REQUIRES.** This round mostly
REMOVED `runs_dir` calls, so six imports went unused and all six were deleted
(`F401`), each following what its own file already does and introducing no second
convention: `timeline.py:43` MODULE-level, `runs_dir` dropped from the pair, and
`run_log_dir` KEPT because site 76 still uses it; `patch_revert.py:33`
MODULE-level, `runs_dir` dropped, `resolve_data_root` kept; and four FUNCTION-LOCAL
single-name import lines deleted outright — `worker_queue.py:487`,
`patch_apply.py:524` and `:562`, `safe_points.py:671`, `pingpong_job.py:3176`
(five lines across four files). `run_log.py:34` is the only ADDITION: the same
module-level line, its imported name changed from `runs_dir as _runs_dir_default`
to `run_log_dir`. `ruff check` accepted every placement including `I001` (G8,
exit 0). `pingpong_job.py`'s OTHER function-local `runs_dir` import, outside this
function, is untouched — constraint 4's five other modules with their own run
stores (`job_evidence.py`, `pingpong_loop.py`, `worktree_resume.py`,
`local_candidate_generator.py`, `local_model_advisor.py`) were never opened.

**7. SPEC (2) ASKED WHAT ELSE ASSERTS A PATH RELATIVE TO `tmp_path`; I MEASURED
FIVE LINES, OF WHICH THREE ARE WRITER-DIRECTORY ASSERTIONS AND TWO ARE NOT.**
`grep -n "tmp_path /" tests/test_run_log.py` at C6 returns lines **128**, **134**,
**175**, **340** and **358**. The reviewer measured two; the two it measured are
128 and 134, the constraint-3 observers, and BOTH keep a literal right-hand side.
The third, line 175, is the NEW test this round adds — also literal, also a
writer-directory assertion, and it did not exist when the reviewer counted. Lines
340 and 358 are `tmp_path / "nonexistent.jsonl"` and `tmp_path / "empty.jsonl"`:
standalone files handed straight to `read_run_events`, never produced by
`RunLogWriter`, so the root's meaning changing from runs-base to data-root cannot
disturb them. The binding count is therefore THREE writer-layout assertions after
this round, two of them pre-existing.

**8. THE `runs_dir` LOCAL IN `tests/cli/test_propose_cli.py` WAS UNUSED AND WAS
DELETED, AS SPEC (4) ASKED ME TO REPORT.** Line 339 read `runs_dir = tmp_path / "runs"`
and its ONLY consumer was line 340. With the construction taking `data_root=tmp_path`
the local had no reader left, so the line went. `tests/test_test_runner.py:344`
needed no such deletion — it built `tmp_path / "runs"` inline.

**9. CONSTRAINT 8's THREE TERMINAL-BYTE MEASUREMENTS, TAKEN AT THE BASE AND
STATED HERE AS ORDERED.** At `4f265f91`, counted by trailing-`\n` enumeration on
the raw bytes: `.agent/live_review.md` ends with **exactly ONE** newline (931365
bytes), `.agent/decisions.md` with **exactly ONE** (839361 bytes),
`.agent/prose_slips.md` with **exactly ONE** (115506 bytes). The block is CORRECT
for all three this round. Each recipe was nonetheless derived from its own
target's measured terminal byte, not from the block's sentence, and each append
asserted the count was 1 before writing.

**10. `cmp` IS DENIED IN THIS SANDBOX (constraint 11).** C0a and C0b were proved
with `filecmp.cmp(shallow=False)` — a full byte comparison, not a stat comparison
— plus sha256 on both files against the delegation's digest. `remedy` was invoked
as `python3 -m apps.cli.grouped` and `ruff` as `python3 -m ruff`. Every mutation
reading ran under `python3 -B` with `PYTHONDONTWRITEBYTECODE=1` and `__pycache__`
purged and re-enumerated at 0.

**11. G2(c)'s NEGATIVE CONTROLS RAN IN MEMORY, ONE PER FILE.** The flip and
restore were done on `bytes` objects inside the checking process rather than by
writing a corrupted image to `.agent/live_review.md` or `.agent/decisions.md`, so
the primary checkout never held known-bad bytes — the block's own G2(c) wording
and self-drive guardrail G5. The property measured is identical, and the restored
image was asserted equal to the disk image in both cases.

**12. EXIT CODES WERE CAPTURED THROUGH A PYTHON RUNNER, NOT `$?`.** The sandbox's
bash guard rejects `$?`, `$( )` and shell loop forms by FORM, so every gate ran
through `.remedy-wt/f260_r14_run.py`, which executes the command with
`subprocess.run`, writes stdout+stderr plus a trailing `__EXIT_CODE__ <n>` line to
a capture file under `.remedy-wt/`, and prints the real return code. Reported so
the reviewer can reproduce the readings the same way. None of those scratch files
is tracked — `git ls-files .remedy-wt` is empty (G8).

**Not a deviation, recorded because it was checked:** `scripts/` and
`tests/test_remedy_smoke_script.py` were NOT touched (constraint 5); the shell
smoke script's `RUNS_ROOT=".data/runs"` pin is a different convention and is
untouched. `tests/test_data_paths.py` was NOT touched (constraint 3); its three
`run_log_dir` tests remain literal and are part of the G6 selection.
`RunLogWriter(job_id=...)` calls that pass NO root were left alone (constraint 6).
`new_run_id`, the `path` and `run_id` properties, `append`, `log` and the event
shape are unchanged (SPEC 1). The module docstring at `run_log.py:5` already read
`<REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl` and was deliberately NOT "fixed".
The eleven `remedy/job-*` worktrees pre-date this round and were neither created
nor removed; only `.remedy-wt/f260-r14-mut` was added and removed, by exact path.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | file copy, `filecmp` True + sha256 equals the delegation digest |
| C0b mirror the block | done | same source, same route, same two proofs |
| C1 PLAN slice | done | 2530 bytes, 48 lines, under the 50-line cap |
| C2 GATE_R13 + DEC_D6 append | done | both in ONE commit, live_review first then decisions |
| C3 four SLIP appends | done | units 144 → 148, in order |
| C4 writer takes a data root + its tests | done | SPEC (1) and SPEC (2); 21 kwargs moved, 2 observers kept literal, 1 new test |
| C5 seven production sites + one comment | done | SPEC (3); re-grepped at the base, all eight line numbers matched |
| C6 the other two test files | done | SPEC (4); the unused `runs_dir` local deleted and reported |
| — extra commit `c296ee97` | deviated | not in the ordered sequence; reworded my own C4 comment so G5(a) reads 0 — deviation 3 |
| C7 handback | done | this file |
| G1 transport | done | exit 0; both digests equal the delegation's, one comparison |
| G2 the two records | done | exit 0; a/b/c/d for BOTH files, negative controls reject and restore |
| G3 the prose files | done | exit 0; plan byte-equal at 48 lines, slips byte-equal at 144 → 148 units |
| G4 the fallback equality | done | exit 0; taken BEFORE C4, three printed pairs all equal |
| G5 the join is gone | done | exit 0; 1→0, 2→0, 0→1 AST, 41→0 word-bounded, no survivor. Base count is 41 not 37 — deviation 1 |
| G6 mutation red-proof | done | **MET AS WRITTEN** — control exit 0 / 261 passed, mutation **exit 1 / 32 failed**, both named observers among the failures, restore exit 0 / 261 passed, worktree clean and removed by exact path |
| G7 the suites | done | exit 0 on all four; 304 / 12805+10s / 1537 / integrity `passed:true`; canary 42 collected |
| G8 lint + clean tree | done | exit 0; ELEVEN paths linted, `All checks passed!`; both tree readings EMPTY |

## Open findings

**297** by DISTINCT ID, measured after C2: 300 registrations over 300 distinct
ids, minus 3 distinct ids carrying a `Done:` line. (The `^Done: ` LINE count is 5;
two findings were each resolved across two paragraphs, so a line-based formula
over-counts by two — the distinct-id reading is the correct one.) This round
registered NOTHING and resolved NOTHING: GATE_R13 is a `Gate:` record, not a
registration, so the open set is unchanged from the base. No `Done:` paragraph was
authored here; that is the reviewer's to write. Nothing this round is marked
`Landed:` either, because no finding was repaired by it.

## Next

**Rule order at session start is Phase 1 rule 1 BEFORE rule 2: re-read
`.agent/STOP` from disk first, then check for an open PR.** There is no open PR
for this branch and none may be created without an instruction.

**Immediate: review round 14.** Read `git diff 4f265f91..HEAD` bottom-up and
re-run the eight gates independently. Twelve deviations are declared; the ones
wanting a RULING rather than an acknowledgement are **1**, **2** and **3**.
Deviations 1 and 2 are the block's own numerals disagreeing with the disk and with
the block's own lists — the shape of checklist item 16 — and in both cases the
gate's binding clause was met and nothing on disk is wrong, so both look like
`.agent/prose_slips.md` lines under amend0827-process-diet rule 2 rather than
R-ids. Deviation 3 is the only departure from the ordered commit sequence and is
the one place where I edited something to make a gate read as ordered; the edit
was to MY OWN comment, not to any code, test or assertion, and both readings are
reported. Nothing was reshaped to make a gate pass and no gate went red.

**Then: THE RE-KEY ITSELF**, which is what rounds 11-14 have been buying.
`run_log_dir` and `pingpong_run_dir` collapse onto `run_dir`, keyed by RUN id —
DECISION F260 D1. After this round the WRITER side of that collapse is ONE
function body, `data_paths.run_log_dir`, plus `RunLogWriter`'s own run-id
plumbing: no production module joins a job id onto a runs base any more (G5, four
independent readings). The READER side is the open problem, and it is the reason
the step below is its prerequisite.

**Its prerequisite: `Job.run_refs`**, the plural run list D1 names and nothing on
disk carries yet. Once `<data_root>/runs/` is keyed by run id, no reader can find
a job's runs — `timeline.load_run_events` reads `run_log_dir(job_id, data_dir)`
today and would have nothing to read.

**The test-side sweep is DECLINED, not forgotten** — DECISION F260 D6, appended to
`.agent/decisions.md` this round, records the measurement and the ruling: 75
path-building occurrences of the quoted token `"runs"` survive under `tests/` in
34 files, 65 of the 69 non-contract ones supply a JOB id, and D1's re-key makes
each a SEMANTIC change rather than a spelling change. The re-key round inherits
those sites and touches them ONCE. That ruling also means the re-key round must
plan its own red-proof carefully: this round's G6 could fail only because
`tests/test_run_log.py`, `tests/test_data_paths.py`, `tests/test_timeline.py` and
`tests/test_patch_apply.py` still hand-spell the path, and a round that sweeps
them consumes its own observer — round 12's finding, and the pre-sweep/post-sweep
PAIR is the shape that round will need.

After that, the rest of T002: the unified record's own administrative fields —
measured at `4f265f91`, eight of D1's eleven have no counterpart in `JobPlan` —
and the Mission extension. Then T003 consumer by consumer; T004 the classic
runner, the classic store and the resolver collapse together (DECISION F260 D5);
T005 the reachability test and the cluster deletion.
