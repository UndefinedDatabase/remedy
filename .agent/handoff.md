# Handoff — F260 One world · round 13 · ONE SPELLING FOR THE RUN-LOG STORE

## Session

SESSION 4 of feature F260 · round 13 · rounds so far 13

Context self-assessment (amend0905-throughput): context is comfortable and was
never a constraint this round. WALL CLOCK was the whole cost —
`tests/orchestration/` alone ran 745.59 s and `tests/cli/` 304.93 s, so G6 spent
roughly seventeen minutes of serial suite time. The 25-round / 7-session soft
limit is not reached (13 rounds, 4 sessions).

## Range

Review of `4d13f5a02608a40081a7ebacf779124cc6318309`..`HEAD`.

Seven commits plus this one, all single-parent, in EXACTLY the Bundle's ordered
sequence C0a → C0b → C1 → C2 → C3 → C4 → C5 → C6. No extra commit, no dropped
commit, no reordering. Largest insertion count 318 (`.agent/authored/f260-r13.md`,
a single `.agent/**` state write, exempt under the AGENTS.md DECISION F104 D1
counting rule); largest CODE commit 22 insertions (`8ccd9309`, the sweep).
Nothing approached the 500-insertion cap.

## Commits

`+/-` taken from `git diff --numstat`, never re-derived by eye.

### a5039818 f260: save the round 13 step block verbatim under agent authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r13.md | +318 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r13-block.md`, proved by `filecmp.cmp(shallow=False)` = True and sha256 equal to the delegation digest BEFORE staging |

### 2f18e3c7 f260: mirror the round 13 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +285 / -267 | C0b — same source file, same copy route, same two proofs |

### 727b281f f260: point the plan at the one spelling for the run log store
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17 / -17 | C1 — whole-file replacement by the PLAN slice plus one trailing newline; 2664 bytes, 49 lines, under the 50-line cap |

### aaaff111 f260: book the round 12 PASS verdict and register finding R-0815
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | C2 — GATE_R12 then FIND815 appended in that order; 923356 → 931365 bytes |

### e1096fe6 f260: append the round 12 reviewer prose slip about the unreachable red proof
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | C3 — SLIP13 appended; 113984 → 115506 bytes |

### 97ced424 f260: give the live job-keyed run-log store one spelling in data_paths
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/data_paths.py | +13 / -0 | C4 — SPEC (1): the six-line WHY comment plus `run_log_dir`, inserted between `runs_dir` and `projects_dir` |
| tests/test_data_paths.py | +17 / -0 | C4 — SPEC (2): three tests in `TestDirectoryHelpers`, each a PATH EQUALITY — explicit root, process data root, `UUID` coercion |

### 8ccd9309 f260: move the nine hand-spelled run-log paths onto the data_paths accessors
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/cockpit.py | +2 / -1 | C5 — site 380 onto `run_log_dir(job.id, data_dir)`; one module-level import |
| packages/orchestration/patch_apply.py | +4 / -2 | C5 — sites 526 and 563 onto `runs_dir(data_dir)`; two FUNCTION-LOCAL imports, one per function |
| packages/orchestration/patch_revert.py | +2 / -2 | C5 — site 245 onto `runs_dir(actual_data_dir)`; `runs_dir` joined the EXISTING module-level `data_paths` import (deviation 3) |
| packages/orchestration/pingpong_job.py | +2 / -2 | C5 — site 3217 onto `run_log_dir(job_id)`; the function-local `runs_dir` import at 3215 became the `run_log_dir` import (constraint 5(b), deviation 5) |
| packages/orchestration/timeline.py | +5 / -4 | C5 — site 64 onto `runs_dir(Path(data_dir))`, site 75 onto `run_log_dir(job_id, data_dir)`; the local `runs_dir` renamed to `run_log_path` because the added module-level import WOULD have been shadowed (deviation 4) |
| packages/orchestration/trust_report.py | +3 / -2 | C5 — site 373 onto `run_log_dir(job.id, data_dir)`; the local renamed to `run_log_path` per constraint 5(a); printed text unchanged |
| packages/orchestration/worker_queue.py | +2 / -1 | C5 — site 488 onto `runs_dir(root)`; one FUNCTION-LOCAL import, because this file has NO module-level `packages.*` import at all (deviation 3) |

### C6 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6 — a handoff cannot table the commit that writes it (R-0149 pattern). Constraint 7: no gate reading is taken after this file exists; the reviewer measures C6's own insertion count at the next gate |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/g7-r13 8ccd9309 --detach` | created, detached HEAD at `8ccd9309` |
| `git worktree remove .remedy-wt/g7-r13 --force` | removed BY EXACT PATH, exit 0 |
| `git worktree prune` | exit 0; `git worktree list` then shows the primary checkout and the ELEVEN pre-existing `remedy/job-*` worktrees only, none of which this round created or touched, and no `g7-r13` row |
| `git push -u origin feature/f260-one-world` | runs after this file is committed; see the note under Verification |

No PR created. No PR merged. No `gh` command run. No force push. No branch
deleted. No file under `.remedy-wt/` was ever `git add`ed.

## Verification

ONE LINE PER GATE, with its REAL exit code. Every suite ran SERIALLY — never two
at once — captured to a file under `.remedy-wt/`, and read from the capture.

| Gate | Command / reading | Exit | Result |
|---|---|---|---|
| G1 | `sha256sum .agent/authored/f260-r13.md .agent/last_block.md` | 0 | both `ba81fed15e2173bd73d969458cd033910ef7af510ae99d5c40f392a1402e3adb`, equal to the digest the delegation names. One comparison, not a chain |
| G2(a) | exact-image equality of `.agent/live_review.md` | 0 | `post == pre + b"\n" + GATE_R12 + b"\n\n" + FIND815 + b"\n"` is True, and `post[:len(pre)] == pre`. 923356 → **931365** bytes, +8009. sha pre `986744520cd7fdc7a69afc309c9b9a051ad77ffcb2cff95862782c8c68786ff5`, sha post `2cd831ca9a2f71667acc8a8eadcd3c08ae61a11b1caff17a6cbf3583d1a81050` |
| G2(b) | structural, split on `"\n\n"` | 0 | units counted BY THE SCRIPT: **432 → 434**, a rise of two. The last two units, in order, EQUAL GATE_R12 and FIND815, and units `[:-2]` equal the pre-image's units exactly |
| G2(c) | negative control, IN MEMORY | 0 | byte at offset **923397** (`b'T'`, 40 bytes into the FIRST appended paragraph) XOR-flipped to `b't'`: reader (a) REJECTS and reader (b) REJECTS. After restore both ACCEPT. No bad bytes were ever written to the file (self-drive G5) |
| G2(d) | census after C2 | 0 | `^Gate: ` **22** · registrations **300** over **300** distinct ids · `^Done: ` **5** lines over **3** distinct ids · open set **297** BY DISTINCT ID. `R-0815` present in the registration set |
| G3 (plan) | `.agent/plan.md` | 0 | disk bytes `== PLAN slice + b"\n"` is True; **2664** bytes, **49 lines**, under the 50-line cap; carries `## Goal` and `## Next Steps` |
| G3 (slips) | `.agent/prose_slips.md` | 0 | `post == pre + b"\n" + SLIP13 + b"\n"` is True and the post-image begins with the pre-image byte for byte. Bytes **113984 → 115506**. Blank-line units **143 → 144**, a rise of exactly ONE |
| G4 (tests) | `python3 -m pytest tests/test_data_paths.py -q -p no:randomly` at C4 | 0 | **51 passed** in 0.63 s (48 at the base, plus the three new ones) |
| G4 (uniqueness) | occurrences of `    return runs_dir(root) / str(job_id)` in `data_paths.py` | 0 | **1**, verified BEFORE C4 was committed, as SPEC (1) requires for the G7 revert target |
| G4 (probe) | scratch probe under `.remedy-wt/`, run BEFORE any consumer was edited | 0 | five printed pairs, hand-spelled vs accessor-built, all EQUAL — see the transcript below |
| G5(a) | quoted token `"runs"` over **1030** tracked `.py` files under `packages/`, `apps/`, `tests/`, enumerated from `git ls-files` IN PYTHON | 0 | PATH-BUILDING lines **82 → 76**. All eight quoted-token swept sites ABSENT at C5; the ninth (`pingpong_job.py:3217`, `runs_dir() / job_id`, no quoted token) also ABSENT. NON-path (JSON-key) occurrences **60 → 60**, changed files: NONE |
| G5(b) | AST reading, calls to `run_log_dir` / `runs_dir` per swept module | 0 | timeline 0/0 → 1/1 · cockpit 0/0 → 1/0 · trust_report 0/0 → 1/0 · pingpong_job 0/2 → 1/1 · patch_apply 0/0 → 0/2 · patch_revert 0/0 → 0/1 · worker_queue 0/0 → 0/1. ALL SEVEN NON-ZERO at C5; six of the seven were ZERO at the base |
| G5(c) | `git diff --numstat 8ccd9309^ 8ccd9309` | 0 | SEVEN rows, exactly the SPEC (3) modules and nothing else: cockpit +2/−1 · patch_apply +4/−2 · patch_revert +2/−2 · pingpong_job +2/−2 · timeline +5/−4 · trust_report +3/−2 · worker_queue +2/−1 |
| G6 (1) | `pytest tests/orchestration/ -q -p no:randomly` | **0** | **12805 passed, 10 skipped**, 1 warning in 745.59 s. 0 FAILED lines, 0 ERROR lines. Identical pass count to the base reading round 12 recorded |
| G6 (2) | `pytest tests/cli/ -q -p no:randomly` | **0** | **1537 passed** in 304.93 s, 0 FAILED lines. Canary presence verified separately: `pytest tests/cli/test_golden_path.py --collect-only` exit 0, **42 tests collected**, so the canary is inside this selection |
| G6 (3) | `pytest tests/test_data_paths.py tests/test_timeline.py tests/test_cockpit.py tests/test_trust_report.py tests/test_patch_apply.py -q -p no:randomly` | **0** | **344 passed** in 1.73 s, 0 FAILED lines |
| G6 (4) | `python3 -m apps.cli.grouped integrity check --json` | 0 | `"passed": true`, `"fail_count": 0`, `"check_count": 5` |
| G7(i) | control in `.remedy-wt/g7-r13` at `8ccd9309`, `python3 -B`, the G6(3) selection | **0** | **344 passed** in 2.07 s. `__pycache__` dirs ENUMERATED after purge: **0**. Module resolution CONFIRMED before any colour was trusted: `data_paths.__file__` = `/home/decodeux/Repos/remedy/.remedy-wt/g7-r13/packages/orchestration/data_paths.py`; the LIVE body printed back as `return runs_dir(root) / str(job_id)`; `run_log_dir("J", Path("/R"))` = `/R/runs/J`. Revert target occurrences in that worktree: **1** |
| G7(ii) | the ordered mutation — `run_log_dir` appends `"_MUTATED"` to the job id | **1** | **IT WENT RED. 17 failed, 327 passed.** Mutation confirmed LIVE in the same process before the run: body `return runs_dir(root) / (str(job_id) + "_MUTATED")`, `run_log_dir("J", Path("/R"))` = `/R/runs/J_MUTATED`. Failing files: `tests/test_timeline.py` (**8**), `tests/test_patch_apply.py` (**6**), `tests/test_data_paths.py` (**3**). `tests/test_cockpit.py` and `tests/test_trust_report.py` contributed 0 — see deviation 7 |
| G7(iii) | restore | **0** | original line restored (original count 1, mutated count 0); `__pycache__` re-enumerated at 0; live body re-printed as the original; control re-run **344 passed**, exit 0. `git status --porcelain` in that worktree EMPTY (`''`), `git diff HEAD --stat` EMPTY (`''`). Worktree removed BY EXACT PATH, then `git worktree prune` |
| G8 (lint) | `python3 -m ruff check` over the edited `.py` paths of the change set — **NINE, not eight** (deviation 6) | **0** | `All checks passed!` |
| G8 (tree) | `git status --porcelain` / `git ls-files .remedy-wt` | 0 / 0 | both EMPTY (`''` each) |

G4 PROBE TRANSCRIPT — the printed pairs, not a summary of them. Run under
`.remedy-wt/` with `python3 -B`, BEFORE any consumer file was edited:

    SHAPE root/"runs"
       hand     = .remedy-wt/g4arg-hwu0c_nq/runs
       accessor = .remedy-wt/g4arg-hwu0c_nq/runs
       EQUAL    = True
    SHAPE root/"runs"/str(jid=str)
       hand     = .remedy-wt/g4arg-hwu0c_nq/runs/0123456789abcdef
       accessor = .remedy-wt/g4arg-hwu0c_nq/runs/0123456789abcdef
       EQUAL    = True
    SHAPE root/"runs"/str(jid=UUID)
       hand     = .remedy-wt/g4arg-hwu0c_nq/runs/0a3e0529-3c8c-46e1-8e5d-2ce1bd2d6bde
       accessor = .remedy-wt/g4arg-hwu0c_nq/runs/0a3e0529-3c8c-46e1-8e5d-2ce1bd2d6bde
       EQUAL    = True
    SHAPE resolve_data_root()/"runs"/str(jid)
       hand     = .remedy-wt/g4env-46gn2yvj/runs/0123456789abcdef
       accessor = .remedy-wt/g4env-46gn2yvj/runs/0123456789abcdef
       EQUAL    = True
    SHAPE runs_dir()/jid  [pingpong_job.py:3217 base spelling]
       hand     = .remedy-wt/g4env-46gn2yvj/runs/0123456789abcdef
       accessor = .remedy-wt/g4env-46gn2yvj/runs/0123456789abcdef
       EQUAL    = True
    ALL PAIRS EQUAL: True

The two `g4arg-`/`g4env-` scratch directories the probe created were removed BY
EXACT PATH afterwards. No glob was used.

THE RED-PROOF IS THE ROUND'S CENTRAL MEASUREMENT AND IT BEHAVED AS THE BLOCK
PREDICTED. Round 12's G7 could not fail because round 11 had already routed the
production writer AND every reader through one accessor. Here the writer moved
and the tests did NOT: `tests/test_timeline.py`, `tests/test_patch_apply.py` and
`tests/test_data_paths.py` still hand-spell `tmp_path / "runs" / <job id>`, so
they remain an INDEPENDENT OBSERVER of `run_log_dir`. Mutating the one function
body therefore reddens 17 of them. That observer is exactly what the plan's first
"Next Step" says the next round will consume, and consuming it is what will make
the NEXT round's red-proof unreachable in turn — the pre-sweep/post-sweep PAIR
that round 12's P3 supplied is the shape that round will need.

The push runs AFTER this file is committed, so its transcript cannot appear in
the commit that carries it (the R-0149 self-reference pattern, same reason the C6
row of the commit table has no `+/-`). Its outcome is verifiable directly:
`origin/feature/f260-one-world` points at the C6 commit.

## Authored-text proofs

| Slice | Target | Shape | Proof |
|---|---|---|---|
| the whole block | `.agent/authored/f260-r13.md` | file copy | `shutil.copyfile`, then `filecmp.cmp(shallow=False)` = True, then sha256 equal to the delegation digest |
| the whole block | `.agent/last_block.md` | file copy | same source, same route, same two proofs |
| PLAN | `.agent/plan.md` | whole-file REWRITE | disk bytes `== slice + b"\n"`, True (G3) |
| GATE_R12, FIND815 | `.agent/live_review.md` | APPEND, in that order | exact-image equality + structural reader + in-memory negative control (G2 a/b/c) |
| SLIP13 | `.agent/prose_slips.md` | APPEND | exact-image equality over the derived recipe, plus a unit reading (G3) |

Every slice was extracted from the COMMITTED `.agent/authored/f260-r13.md` — not
from a retype — by taking the lines strictly between its marker lines, joined by
`"\n"`, with no trailing newline. Each of the eight marker lines was verified to
occur EXACTLY ONCE (at file lines 256, 306, 308, 310, 312, 314, 316, 318), and
every extracted slice was asserted to contain none of the eight marker tokens. NO
MARKER LINE REACHED ANY TARGET FILE.

## Deviations & assumptions

**1. CONSTRAINT 6 MIS-STATES `.agent/prose_slips.md`'s TERMINAL BYTE, AND THE
CONSTRAINT'S OWN DERIVE-IT RULE WAS FOLLOWED INSTEAD.** The constraint says that
file "at the base ends with NO trailing newline". MEASURED at the base
`4d13f5a0`: it ends with EXACTLY ONE newline — last 40 bytes
`b' spent (amend0827-process-diet rule 2).\n'`, trailing-newline count 1, 113984
bytes. `.agent/live_review.md` also ends with exactly ONE newline, as the
constraint says. Because constraint 6 also orders "DERIVE EACH RECIPE FROM ITS
OWN TARGET'S TERMINAL BYTE, measured at the base", the derived recipe was used
for both files: `pre + "\n" + slice + "\n"` per appended paragraph. BOTH BASE
MEASUREMENTS ARE STATED IN G2/G3 ABOVE, as the constraint requires. Worth noting
for the reviewer: this is the SECOND consecutive round whose constraint 6 got
this file's terminal byte wrong, and in the opposite direction each time —
round 11's block claimed a trailing newline the file did not have, round 12's
`.agent/prose_slips.md` append then GAVE it one, and round 13's block still
carries round 11's description. The file's own SLIP for round 11 records the
first half of that story.

**2. THE BLOCK'S OWN LINE NUMBER FOR `pingpong_job.py` IS OFF BY ONE IN THE
BUNDLE LINE AND CORRECT IN SPEC (3).** The Bundle's C4/C5 prose and constraint
5(b) name `pingpong_job.py:3215` for the IMPORT and SPEC (3) names `:3217` for
the expression. Both are correct and they are different lines — 3215 is
`from packages.orchestration.data_paths import runs_dir`, 3217 is
`job_runs = runs_dir() / job_id`. Recorded only so the reviewer does not read
them as a contradiction. All nine SPEC (3) line numbers were RE-GREPPED at the
base before editing and all nine matched: timeline 64/75, cockpit 380,
trust_report 373, pingpong_job 3217, patch_apply 526/563, patch_revert 245,
worker_queue 488. Re-measured count: **NINE**.

**3. CONSTRAINT 4's PER-FILE MEASUREMENT IS WRONG FOR TWO FILES, AND THE
CONSTRAINT'S GOVERNING RULE — NOT ITS LIST — WAS FOLLOWED.** Constraint 4 states
the rule ("decided PER FILE, following what that file already does, and no second
convention is introduced") and then lists which files do what. The list is wrong
twice, measured at the base:
- `patch_revert.py` does NOT import `data_paths` function-locally. Line 33 is a
  MODULE-LEVEL `from packages.orchestration.data_paths import resolve_data_root`.
  Adding a function-local import would have introduced a SECOND convention in
  that file, which the governing rule forbids, so `runs_dir` joined line 33:
  `from packages.orchestration.data_paths import resolve_data_root, runs_dir`.
- `worker_queue.py` has NO module-level `packages.*` import AT ALL — every one of
  its `packages.*` imports (lines 187, 431-433, 487, 582-583 at the base) is
  function-local. The new import therefore went FUNCTION-LOCALLY, beside the
  existing `run_log` import inside the same `try:` block at line 487.
The other five files match the constraint's list: `timeline.py`, `cockpit.py` and
`trust_report.py` took a module-level import in isort order, `patch_apply.py` and
`pingpong_job.py` took function-local ones. `ruff check`'s `I001` accepted every
placement (G8, exit 0), which is the check constraint 4 itself names.

**4. `timeline.py`'s LOCAL `runs_dir` WAS RENAMED, WHICH SPEC (3) MADE
CONDITIONAL.** SPEC (3) says to keep the local name `runs_dir` at
`timeline.py:75` "if that does not shadow an import you added; rename it if it
does". It does: site 64 in the SAME module needs `runs_dir` the accessor, and the
per-file convention put that import at MODULE level, so the local binding at 75
would have shadowed it inside `load_run_events`. The local is now `run_log_path`
— the same spelling constraint 5(a) suggests for the `trust_report.py` collision,
so the two collisions resolve to ONE new name rather than two. Three references
moved (75, 76, 79); no printed or logged text changed.

**5. `pingpong_job.py`'s LOCAL IMPORT WAS REBOUND RATHER THAN DELETED.**
Constraint 5(b) anticipates that the `runs_dir` import at 3215 "becomes unused"
and says to remove it. In fact the enclosing function `_job_stopped_event_exists`
had exactly ONE use of `runs_dir`, the swept expression, so the import line was
REPLACED in place by `from packages.orchestration.data_paths import run_log_dir`
rather than deleted and a new line added. Net effect is identical and ruff `F401`
is clean; declared because the block's word was "remove", the way round 12
declared its `resolve_data_root` removal. The module's OTHER function-local
`runs_dir` import at line 3176 is untouched and still used at 3182 — it is one of
the two sites SPEC (3) explicitly excludes.

**6. G8 SAYS "THE EIGHT EDITED `.py` PATHS"; THE CHANGE SET HAS NINE.** Counting
the change set's own list: `data_paths.py`, `test_data_paths.py`, `timeline.py`,
`cockpit.py`, `trust_report.py`, `pingpong_job.py`, `patch_apply.py`,
`patch_revert.py`, `worker_queue.py` = **9**. The lint gate was run over all
nine, which is the wider reading and the one the gate's own words
("over exactly the ... edited `.py` paths of the change set") select. Exit 0,
`All checks passed!`. The two pre-existing errors the gate warns about
(`UP035` at `dag_schedule.py:36`, `F821` at `gauntlet_injection.py:286`) were not
approached: neither file is in the change set.

**7. TWO OF THE FIVE FILES IN THE G7 SELECTION CANNOT REDDEN UNDER THIS
MUTATION, AND THAT IS A PROPERTY OF THOSE TESTS.** Reported because the gate asks
for the failing files and the absences are informative. `tests/test_cockpit.py`
and `tests/test_trust_report.py` contributed ZERO failures. Their assertions on
this feature are `assert "run log" in out.lower() or "runs" in out`
(`test_cockpit.py:480`, `test_trust_report.py:660`) — a substring test against a
LABEL, which no change to the path's leaf can disturb. They are not evidence of a
surviving hand-spelling: G5(a) measures both modules at ZERO path-building
occurrences of the quoted token at C5, and G5(b) measures both at one
`run_log_dir` call. The gate's post-condition ("IT MUST GO RED") is about the
SELECTION and the selection went red at exit 1 with 17 failures.

**8. `cmp` IS DENIED IN THIS SANDBOX.** As constraint 9 directs, C0a and C0b were
proved with `filecmp.cmp(shallow=False)` — a full byte comparison, not a stat
comparison — plus sha256 on both files against the delegation's digest. `remedy`
was invoked as `python3 -m apps.cli.grouped` and `ruff` as `python3 -m ruff`.

**9. G2(c)'s NEGATIVE CONTROL RAN IN MEMORY.** The flip and restore were done on
`bytes` objects inside the checking process rather than by writing a corrupted
image to `.agent/live_review.md`, so the primary checkout never held known-bad
bytes (self-drive guardrail G5, and the block's own G2(c) wording). The property
measured is identical: offset 923397, one bit flipped inside the FIRST appended
paragraph, both readers reject, both accept after restore.

**10. G5(a)'s ENUMERATION IS IN PYTHON, AND ITS "BUILDS A PATH" PREDICATE IS
STATED SO THE REVIEWER CAN RE-RUN IT.** `git ls-files` was enumerated in Python
and filtered to `.py` under `packages/`, `apps/`, `tests/` — 1030 files — because
the shell glob `tests/**/*.py` silently misses `tests/test_data_paths.py` (round
12 deviation 7, promoted into this round's G5). A line COUNTS AS PATH-BUILDING
when the quoted token is joined with `/` (`/ "runs"`, `"runs" /`, `/"runs"`);
everything else — `"runs": [...]`, `["runs"]`, `.get("runs")` — is a JSON key and
is reported separately and unchanged at 60. The base side of every count was read
with `git show 4d13f5a0:<path>`, not from the working tree.

**Not a deviation, recorded because it was checked:** `packages/orchestration/run_log.py`
was NOT touched, per constraint 2. `RunLogWriter.__init__` still joins
`root / self._job_id` where `root` is the runs BASE, and `RunLogWriter`'s
signature is unchanged. `safe_points.py:671` and `pingpong_job.py:3178` already
call `runs_dir()` and were not swept. The eleven `remedy/job-*` worktrees under
`.remedy-wt/` pre-date this round and were neither created nor removed here; only
`.remedy-wt/g7-r13` was added and removed, by exact path.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | file copy, two proofs |
| C0b mirror the block | done | file copy, two proofs |
| C1 PLAN slice | done | 49 lines, 2664 bytes |
| C2 GATE_R12 + FIND815 append | done | in that order; open set 297 by distinct id |
| C3 SLIP13 append | done | units 143 → 144 |
| C4 accessor + its tests | done | `run_log_dir` added; revert target unique (count 1); 51 passed |
| C5 the nine-site sweep | done | 9 re-grepped at the base, 9 moved, 7 modules, no row outside SPEC (3) |
| C6 handback | done | this file |
| G1 transport | done | pass, exit 0 |
| G2 the record | done | pass, all four parts, exits 0 |
| G3 the prose files | done | pass, both targets, exits 0 |
| G4 accessor + no behaviour change | done | pass, exit 0; five printed pairs all equal |
| G5 sweep complete and non-vacuous | done | pass, all three parts, exits 0 |
| G6 the suites | done | pass, all four readings, exits 0 |
| G7 mutation red-proof | done | **MET AS WRITTEN** — control 0/344, mutation **exit 1, 17 failed**, restore 0/344, worktree clean and removed |
| G8 lint + clean tree | done | pass, exits 0; nine paths linted, not eight (deviation 6) |

## Open findings

**297** by DISTINCT ID, measured after C2: 300 registrations over 300 distinct
ids, minus 3 distinct ids carrying a `Done:` line. (The `^Done: ` LINE count is 5;
two findings, R-0721 and R-0725, were each resolved across two paragraphs, so a
line-based formula over-counts by two — the distinct-id reading is the correct
one.) This round REGISTERED `R-0815` from the FIND815 slice and resolved nothing;
authoring a `Done:` paragraph is the reviewer's, not the worker's.

## Next

**Rule order at session start is Phase 1 rule 1 BEFORE rule 2: re-read
`.agent/STOP` from disk first, then check for an open PR.** There is no open PR
for this branch and none may be created without an instruction.

**Immediate: review round 13.** Read `git diff 4d13f5a0..HEAD` bottom-up and
re-run the eight gates independently. Ten deviations are declared; the ones
wanting a RULING rather than an acknowledgement are 1, 3 and 6 — all three are
places where the BLOCK's own measured claim disagrees with the disk, and in each
the block's governing RULE was followed over its stated list. Deviations 4 and 5
are scope questions the constraints already anticipated. Nothing was reshaped to
make a gate pass and no gate went red.

**Then: THE TEST SIDE OF THE RUN-LOG SPELLING**, which is the plan's first Next
Step and is deliberately left standing by this round. Measured here, at
`8ccd9309`, so that round does not start blind:

- **76** path-building occurrences of the quoted token `"runs"` remain across
  1030 tracked `.py` files. ONE is the definition (`data_paths.py:73`); the rest
  are tests. Per-file counts are in the G5(a) capture.
- The heaviest are `tests/test_patch_apply.py` (6), `tests/test_agent_loop.py`
  (5), `tests/test_patch_intent_approval.py` (5), `tests/test_project_brain.py`
  (5), `tests/orchestration/test_worker_execution.py` (4),
  `tests/test_project_context_coverage.py` (4).
- **A ROUND THAT SWEEPS THOSE DESTROYS ITS OWN RED-PROOF OBSERVER.** This round's
  G7 went red only because 17 tests in three files still hand-spell the path. Once
  they route through `run_log_dir`, mutating that body moves writer and reader in
  lockstep and no test inside the system can see it — precisely round 12's
  finding. That round's gate must therefore order the PAIR: red against the
  pre-sweep bytes, green against the swept ones, which is what round 12's P3 did.
- Two of the five files in this round's G7 selection are useless as observers
  either way (deviation 7); a future selection should be chosen for its
  path-asserting tests, not its module names.

**Then THE RE-KEY ITSELF**, which is what all of this has been buying:
`run_log_dir` and `pingpong_run_dir` collapse onto `run_dir`, keyed by RUN id.
After this round that collapse touches `data_paths.py` plus ONE remaining
writer-side spelling — `RunLogWriter.__init__` (`run_log.py:114-115`), which joins
`root / self._job_id` onto a runs BASE it is handed and is deliberately outside
this round's change set (constraint 2). Its signature must change in the same
commit as the re-key, or `timeline.load_run_events` reads one directory keyed two
ways — DECISION F260 D0's collision, concretely.

After that, the rest of T002: the unified record's own fields and the Mission
extension (order, contract, mission plan, job refs). Then T003 consumer by
consumer; T004 the classic runner, the classic store and the resolver collapse
together (DECISION F260 D5); T005 the reachability test and the cluster deletion.
