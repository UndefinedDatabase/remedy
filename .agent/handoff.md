# Handoff — F260 One world · round 12 · THE TEST SIDE OF THE ONE SPELLING

## Session

SESSION 3 of feature F260 · round 12 · rounds so far 12

Context self-assessment (amend0905-throughput): context is comfortable, but this
was declared the LAST round of the session by the delegation, so the "Next"
section below is written to be the ONLY channel that reaches the next session.
Wall clock, not context, was this round's cost: `tests/orchestration/` alone ran
708 seconds.

## Range

Review of `2ad2d1534ff53a202dc6965909391849b2dd2ca0`..`HEAD`.

Six commits plus this one, all single-parent, in EXACTLY the Bundle's ordered
sequence C0a → C5. No extra commit, no dropped commit, no reordering. Largest
insertion count 300 (`.agent/authored/f260-r12.md`, a single `.agent/**` state
write, exempt under the AGENTS.md DECISION F104 D1 counting rule); largest CODE
commit 22 insertions (`326fe67a`, the sweep). Nothing approached the
500-insertion cap.

## Commits

`+/-` taken from `git diff --numstat`, never re-derived by eye (§3 item 28).

### 24c5dd03 f260: save the round 12 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r12.md | +300 / -0 | C0a — the block copied byte-for-byte with `shutil.copyfile`, verified by `filecmp.cmp(shallow=False)` and sha256 before staging |

### b20e62aa f260: mirror the round 12 step block into the last block file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +201 / -300 | C0b — same bytes, same copy route, same two proofs |

### 58ff92d3 f260: point the plan at the test side of the one spelling
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15 / -13 | C1 — whole-file replacement by the PLAN slice plus one trailing newline; 49 lines, 2611 bytes, under the 50-line cap |

### 4097ddf3 f260: book the round 11 PASS verdict into the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — GATE_R11 appended; 918017 → 923356 bytes |

### 4fc2b546 f260: append the four round 11 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +8 / -0 | C3 — SLIP9 through SLIP12 appended; 108734 → 113984 bytes |

### 326fe67a f260: move the hand-spelled ping-pong run paths in the tests onto the accessors
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_task_input.py | +4 / -2 | C4 — sites 146 and 155 onto `pingpong_run_dir(run_id, tmp_path / "data")`; two FUNCTION-LOCAL imports, because this file has no module-level `packages.*` import at all |
| tests/orchestration/test_evidence_bundle.py | +3 / -2 | C4 — sites 201 and 209 onto `pingpong_run_dir(run_id, data_dir)`; one module-level import added |
| tests/orchestration/test_failure_postmortem.py | +2 / -1 | C4 — site 687 ONLY, onto `pingpong_run_dir("r1", tmp_path / "data")`; one module-level import added. Lines 669, 688 and 689 UNTOUCHED |
| tests/orchestration/test_failure_wiring.py | +5 / -5 | C4 — sites 351, 359, 623, 631 onto `pingpong_runs_dir(<explicit root>)`; `pingpong_runs_dir` joined the existing module-level `data_paths` import |
| tests/orchestration/test_job_stop_integration.py | +3 / -3 | C4 — sites 248 and 250 onto `pingpong_runs_dir()`; `resolve_data_root` DROPPED from the import because it became unused (ruff F401) |
| tests/orchestration/test_manual_completion_bundle.py | +2 / -1 | C4 — site 142 onto `pingpong_run_dir(run_id, data_root)`; one module-level import added |
| tests/orchestration/test_pingpong_cli.py | +3 / -3 | C4 — sites 281 and 283 onto `pingpong_runs_dir(demo_repo / ".data")` and `pingpong_run_dir(result.run_id, isolate_data_root)`; `pingpong_runs_dir` joined the existing module-level import |

### C5 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/f260-r12-g7 326fe67a` | created, detached HEAD at `326fe67a` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f260-r12-g7` | removed |
| `git worktree prune` | exit 0; `git worktree list` then shows only the primary checkout and the ELEVEN pre-existing `remedy/job-*` worktrees, none of which this round created or touched |
| `git push -u origin feature/f260-one-world` | runs after this file is committed; see the note under Verification |

No PR created. No PR merged. No `gh` command run. No force push. No branch
deleted. No file under `.remedy-wt/` was ever `git add`ed.

## Verification

ONE LINE PER GATE, with its REAL exit code. Every suite ran SERIALLY, captured
to a file under `.remedy-wt/`, and was read from the capture — never piped.

| Gate | Command / reading | Exit | Result |
|---|---|---|---|
| G1 | `sha256sum .agent/authored/f260-r12.md .agent/last_block.md` | 0 | both `203cd3fc75b5c639947d1ace5a7a93197a8fe4ca18b60ab9296051e242d6410a`, equal to the digest named in the delegation that carried this block |
| G2(a) | exact-image equality of `.agent/live_review.md` | 0 | `post == pre + b"\n" + GATE_R11 + b"\n"` is True; 918017 + 1 + 5337 + 1 = **923356** measured bytes |
| G2(b) | structural, split on `"\n\n"` | 0 | units **431 → 432**; the last unit with its terminating newline stripped EQUALS GATE_R11, and it carries exactly one newline |
| G2(c) | negative control | 0 | byte at offset **918118**, inside the appended paragraph, XOR-flipped: reading (a) REJECTS and reading (b) REJECTS; after restore both ACCEPT |
| G2(d) | counts after C2 | 0 | `^Gate: ` **21**, all distinct · registrations **299** over **299** distinct ids · `^Done: ` **5** lines over **3** distinct ids · open set **296** BY DISTINCT ID |
| G3 | exact-image equality of `.agent/prose_slips.md` | 0 | `post == pre + b"\n" + SLIP9 + b"\n\n" + SLIP10 + b"\n\n" + SLIP11 + b"\n\n" + SLIP12 + b"\n"` is True; 108734 → **113984** bytes; blank-line units **139 → 143**, a rise of exactly FOUR |
| G4 | `.agent/plan.md` | 0 | disk bytes `== PLAN slice + b"\n"` is True; **2611** bytes, **49 lines**, under the 50-line cap |
| G5(a) | quoted token over **1030** tracked `.py` files under `packages/`, `apps/`, `tests/` | 0 | EXACTLY THREE sites, full list: `packages/orchestration/data_paths.py:216`, `tests/test_data_paths.py:406`, `tests/test_data_paths.py:407`. Per-file counts `{data_paths.py: 1, test_data_paths.py: 2}`, which is the gate's named pair exactly. Base reading re-measured before the sweep: **17** sites in **9** files |
| G5(b) | AST non-vacuity per swept file | 0 | failure_wiring **9** · pingpong_cli **6** · job_stop_integration **3** · evidence_bundle **3** · task_input **4** · failure_postmortem **2** · manual_completion_bundle **2**. All seven NON-ZERO; all seven were ZERO at the base |
| G5(c) | `git diff --numstat 326fe67a^ 326fe67a` | 0 | seven rows, every one both-non-zero and within two: task_input +4/−2 · evidence_bundle +3/−2 · failure_postmortem +2/−1 · failure_wiring +5/−5 · job_stop_integration +3/−3 · manual_completion_bundle +2/−1 · pingpong_cli +3/−3. No row outside the swept set |
| G6 (1) | `pytest tests/orchestration/ -q -p no:randomly` | **0** | **12805 passed, 10 skipped**, 1 warning in 708.19s — identical to the base reading the block quotes |
| G6 (2) | `pytest tests/cli/ -q -p no:randomly` | **0** | **1537 passed** in 303.14s. Canary presence verified separately: `pytest tests/cli/test_golden_path.py --collect-only` reports **42 tests collected**, so the canary is inside this selection |
| G6 (3) | `pytest tests/test_data_paths.py -q -p no:randomly` | **0** | **48 passed** in 0.59s |
| G6 (4) | `python3 -m apps.cli.grouped integrity check --json` | 0 | `"passed": true`, `"fail_count": 0`, `"check_count": 5` |
| G7(i) | control in `.remedy-wt/f260-r12-g7` at `326fe67a`, `python3 -B`, whole seven-file selection | **0** | **544 passed** in 16.34s. Module resolution CONFIRMED from that worktree before any colour was trusted: `data_paths.__file__` = `/home/decodeux/Repos/remedy/.remedy-wt/f260-r12-g7/packages/orchestration/data_paths.py`, and the live function BODY printed back as `return (root if root is not None else resolve_data_root()) / "pingpong_runs"`. `__pycache__` dirs in that worktree: **0**, enumerated not assumed |
| G7(ii) | the ordered mutation — `pingpong_runs_dir` returns `.../"pingpong_runs_MUTATED"` | **0** | **544 passed, ZERO failed.** THE GATE IS NOT MET AS WRITTEN. Mutation confirmed live in the same run (`BODY ... / "pingpong_runs_MUTATED"`). Failures per swept file: failure_wiring **0** · pingpong_cli **0** · job_stop_integration **0** · evidence_bundle **0** · task_input **0** · failure_postmortem **0** · manual_completion_bundle **0**. See deviation 1 — the cause is NOT a surviving hand-spelling, and it is measured, not argued |
| G7(iii) | restore | 0 | mutated bytes verified to occur exactly once before reverting; original line restored; `git status --porcelain` AND `git diff HEAD --stat` in that worktree both EMPTY; control re-run **544 passed**, exit 0 |
| G8 (lint) | `python3 -m ruff check` over exactly the seven swept files | **0** | `All checks passed!` |
| G8 (tree) | `git status --porcelain` / `git ls-files .remedy-wt` | 0 / 0 | both EMPTY (0 bytes of output each) |

SUPPLEMENTARY PROBES, run because G7(ii) produced no colour and the delegation
asks for the report rather than a green word. Both ran in the same disposable
worktree, both were reverted, both left it clean.

| Probe | Reading | Exit | Result |
|---|---|---|---|
| P2 — discriminating mutation | `pingpong_runs_dir` made to IGNORE its `root` argument (`return resolve_data_root() / "pingpong_runs"`) | **1** | **3 failed, 541 passed.** `test_failure_wiring.py::TestTargetGuardExemptionIsStrict::test_data_root_inside_the_repo_exempts_only_what_is_inside_it`, `test_failure_wiring.py::TestDataRootSymlinksExemptNothing::test_a_real_data_directory_inside_the_repo_still_works`, `test_pingpong_cli.py::TestExternalRunStorage::test_storage_outside_target`. Those are the only swept sites whose explicit root DIFFERS from the process data root |
| P3 — negative control on the ORDERED mutation | the ordered `_MUTATED` mutation applied, AND the seven test files checked out at `326fe67a^` (their PRE-sweep, hand-spelled bytes) | **1** | **30 failed, 514 passed**, across FOUR files: `test_evidence_bundle.py` (25), `test_task_input.py` (2), `test_manual_completion_bundle.py` (2), `test_pingpong_cli.py` (1) |

P3 is the measurement that settles G7. The SAME mutation reddens 30 tests
against the PRE-sweep files and 0 against the POST-sweep files. The gate's
direction is inverted: this round's whole purpose is that the tests FOLLOW the
store when it moves, so the correct post-condition is that they stay GREEN under
a rename of the leaf, and it is the OLD hand-spelled text that goes red.

The push runs AFTER this file is committed, so its transcript cannot appear in
the commit that carries it (the R-0149 self-reference pattern, same reason the C5
row of the commit table has no `+/-`). Its outcome is verifiable directly:
`origin/feature/f260-one-world` points at the C5 commit.

## Authored-text proofs

| Slice | Target | Shape | Proof |
|---|---|---|---|
| the whole block | `.agent/authored/f260-r12.md` | file copy | `shutil.copyfile`, then `filecmp.cmp(shallow=False)` = True, then sha256 equal to the delegation digest |
| the whole block | `.agent/last_block.md` | file copy | same route, same two proofs |
| PLAN | `.agent/plan.md` | whole-file REWRITE | disk bytes `== slice + b"\n"`, True (G4) |
| GATE_R11 | `.agent/live_review.md` | APPEND | exact-image equality + structural + negative control (G2 a/b/c) |
| SLIP9, SLIP10, SLIP11, SLIP12 | `.agent/prose_slips.md` | APPEND | exact-image equality over the whole four-slice recipe (G3) |

Every slice was extracted from the COMMITTED `.agent/authored/f260-r12.md` by
taking the lines strictly between its marker lines, joined by `"\n"`, with no
trailing newline. Each BEGIN and each END marker was verified to occur exactly
once. No marker line reached any file.

## Deviations & assumptions

**1. G7(ii) CANNOT REDDEN, AND ITS STATED INFERENCE IS FALSE FOR THIS ROUND.
DECLARED, NOT REPAIRED. Nothing was reshaped to make it go green.**
The gate says tests in the swept files "must now FAIL — because they read the
accessor rather than a hand-spelled string", and that a file which does not
redden "is still hand-spelling its path somewhere the token reading missed".
Measured: **544 passed, 0 failed**, all seven files at zero. The cause is the
opposite of the one the gate names. Round 11 already moved PRODUCTION onto the
same accessor — G5(a) this round measures the quoted token `"pingpong_runs"` at
**exactly one** site under `packages/` and `apps/`, the definition itself — so
mutating that one function moves the WRITER and the READER in lockstep and no
observer inside the system can see it. That is not a leak; it is the property the
one-spelling work exists to produce. P3 proves the direction empirically: the
identical mutation reddens **30** tests against the pre-sweep bytes of the same
seven files and **0** against the swept bytes. A future gate of this shape should
assert the pre-sweep redness and the post-sweep greenness as a PAIR, which is
what P3 does, rather than demanding redness from the swept side.

**2. THREE OF THE SEVEN FILES CANNOT REDDEN UNDER ANY MUTATION OF THE ACCESSOR,
AND THAT IS A PROPERTY OF THE TESTS, NOT OF THE SWEEP.** Reported because the
gate asks which files produce no failure and why, and because the reason is worth
a look. In `test_failure_wiring.py` all four swept sites only `mkdir` a directory
and write a file into it, after which the assertion is
`any("remedy_data" in o for o in operational)` — the LEAF name is never
cross-checked, so renaming it changes nothing. In `test_failure_postmortem.py`
site 687 is a bare `mkdir`; the assertion on the next two lines is about
`FP.safe_text` applied to a hand-written string. In
`test_job_stop_integration.py` sites 248/250 sit inside
`run = json.loads(...) if (...).is_file() else None` followed by
`if run is not None:` — when the path is wrong the read yields `None` and the
assertion is SILENTLY SKIPPED rather than failing. That last one is a latent weak
assertion that predates this round and survives it unchanged; it is offered as a
candidate, not registered, because this round's change set forbids widening.
(These three are also why P2 reddens only two files: the other five pass an
explicit root that EQUALS the process data root, so a root-ignoring mutation is a
no-op there by construction — which is exactly the "no behaviour change"
requirement being honoured.)

**3. `cmp` IS DENIED IN THIS SANDBOX.** The delegation names `cmp` and supplies
the substitute; recorded so the substitution is visible in the audit trail. C0a
and C0b were proved with `filecmp.cmp(shallow=False)` — a full byte comparison,
not a stat comparison — plus sha256 on both files. `remedy` was invoked as
`python3 -m apps.cli.grouped` and `ruff` as `python3 -m ruff`, as directed.

**4. G2(c)'S NEGATIVE CONTROL WAS RUN IN MEMORY.** The flip and the restore were
performed on `bytes` objects inside the checking process rather than by writing a
corrupted image to `.agent/live_review.md` and back, so the primary checkout was
never left holding known-bad bytes (self-drive G5). The property measured is
identical: offset 918118, one bit flipped, inside the appended paragraph;
readings (a) and (b) both reject the flipped image and both accept the restored
one.

**5. `resolve_data_root` WAS REMOVED FROM AN IMPORT LINE THE SPEC DID NOT NAME.**
In `tests/orchestration/test_job_stop_integration.py` the only two uses of
`resolve_data_root` were the two swept sites, so leaving the import would have
been a ruff F401 and G8 would have gone red. The import line now reads
`from packages.orchestration.data_paths import job_record_path, pingpong_runs_dir`.
This is inside the change set and is behaviour-neutral, but it is a line the SPEC
did not describe, so it is declared.

**6. PATH EQUALITY WAS MEASURED, NOT REASONED.** Per the delegation, a scratch
probe under `.remedy-wt/` printed BOTH the hand-built and the accessor-built path
for all five shapes this sweep uses, before any file was edited:
`root/"pingpong_runs"` vs `pingpong_runs_dir(root)`; `root/"pingpong_runs"/rid`
vs `pingpong_run_dir(rid, root)`; `resolve_data_root()/"pingpong_runs"` vs
`pingpong_runs_dir()`; and the two longer joins used by `test_task_input.py` and
`test_job_stop_integration.py`. All five printed identical and compared equal.
NO TEST CHANGES WHICH DIRECTORY IT READS.

**7. A MEASUREMENT GOTCHA WORTH RECORDING.** The git pathspec
`tests/**/*.py` does NOT match `tests/test_data_paths.py`, only files at least
one directory deeper. A first grep written that way returned 15 sites and would
have made the base look like 15-in-8 rather than the block's 17-in-9. The G5(a)
reading above therefore enumerates `git ls-files` and filters in Python instead
of relying on a shell glob. The block's count of seventeen is correct.

**Assumption, stated — the import convention, decided per file.** SPEC says to
follow each file's existing convention and not to introduce a second one.
`test_failure_wiring.py` and `test_pingpong_cli.py` already carry a MODULE-LEVEL
`from packages.orchestration.data_paths import pingpong_run_dir`, so the second
name joined that line. `test_job_stop_integration.py`, `test_evidence_bundle.py`,
`test_failure_postmortem.py` and `test_manual_completion_bundle.py` import every
`packages.*` name they use at module level, so the new import went there, placed
in isort order (`data_paths` sorts before `failure_postmortem`, `job_evidence`
and `pingpong_evidence`, and after the bare
`from packages.orchestration import failure_postmortem as FP`). `test_task_input.py`
has NO module-level `packages.*` import at all — every one of its ~30 imports is
function-local — so it received two FUNCTION-LOCAL imports, one per edited test.
That is the only file where the insertion count exceeds the deletion count by
two, and it is why.

**Not a deviation, recorded because it was checked:** the eleven
`remedy/job-*` worktrees under `.remedy-wt/` pre-date this round. They were
neither created nor removed here; only `.remedy-wt/f260-r12-g7` was added and
removed, by exact path.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 PLAN slice | done | |
| C2 GATE_R11 append | done | |
| C3 SLIP9–SLIP12 append | done | |
| C4 THE SWEEP — 14 sites, 7 files | done | 14 measured at the base, 14 re-grepped before editing, 14 moved |
| C5 handback | done | this file |
| G1 transport | done | pass, exit 0 |
| G2 the record | done | pass, all four parts, exit 0 |
| G3 the slips | done | pass, exit 0 |
| G4 the plan | done | pass, exit 0 |
| G5 hand-spelled paths gone | done | pass, all three parts, exit 0 |
| G6 the suites | done | pass, all four readings, exit 0 |
| G7 mutation red-proof | deviated | (i) and (iii) pass; (ii) produced ZERO failures and is NOT MET AS WRITTEN — deviation 1, with P2 and P3 supplied in its place |
| G8 lint + clean tree | done | pass, exit 0 |

## Open findings

**296** by DISTINCT ID, measured after C2 (299 registrations over 299 distinct
ids, minus 3 distinct ids carrying a `Done:` line). No finding was registered or
resolved by this round. One CANDIDATE is offered in deviation 2 and deliberately
not registered: the guarded read at
`tests/orchestration/test_job_stop_integration.py:248-251` skips its assertion
instead of failing when the path is wrong.

## Next

**Rule order at session start is Phase 1 rule 1 BEFORE rule 2: re-read
`.agent/STOP` from disk first, then check for an open PR.** There is no open PR
for this branch and none may be created without an instruction.

**Immediate: review round 12.** Read `git diff 2ad2d153..HEAD` bottom-up, re-run
the eight gates independently, and rule on the seven declared deviations.
Deviation 1 is the only one needing a VERDICT rather than an acknowledgement:
G7(ii) as written cannot fail, and the reviewer should decide whether to accept
P3 (the pre-sweep/post-sweep pair) as the round's red-proof or to order a
different one. Deviations 2 and 5 want an acknowledgement and a ruling on whether
the `test_job_stop_integration` guarded read becomes a finding.

**Then: THE RUN MOVE, and it is the round this session deliberately did not
start.** It needs a fresh reading of `packages/orchestration/run_log.py` and
`packages/orchestration/timeline.py`, which no round of F260 has touched. What
was measured THIS round, at `326fe67a`, so the next session does not start blind:

- `data_paths.runs_dir` (line 71) and `data_paths.run_dir` (line 198) ALREADY
  EXIST. The plan's phrasing "collapse into `runs_dir` and `run_dir`" is a MERGE
  of two live pairs, not a rename into a free name. `data_paths` says so in its
  own comment: `run_dir` is "the TARGET spelling and this pair is the LIVE one".
  Whoever writes that block must state which of the two directories survives.
- `runs_dir` today means `<data_root>/runs/`, the RUN LOG store keyed by JOB id.
  `pingpong_runs_dir` means `<data_root>/pingpong_runs/`, the run RESULT store
  keyed by RUN id. Two directories, two keys. That is DECISION F260 D0's
  collision, concretely.
- `run_log.py:34` imports `data_paths.runs_dir as _runs_dir_default` and uses it
  at line 114 — that file is already on the accessor.
- `timeline.py` is NOT. It hand-spells the component twice:
  `timeline.py:64` `RunLogWriter(jid, runs_root=Path(data_dir) / "runs")` and
  `timeline.py:75` `runs_dir = data_dir / "runs" / str(job_id)`, read by
  `load_run_events(data_dir, job_id)` at line 68. Line 75 is the exact reader
  D0 warns about: it keys `<data_root>/runs/` by JOB id, so it must move in the
  SAME commit as any writer that re-keys that directory by RUN id.
- Twelve modules under `packages/` and `apps/` mention `runs_dir`:
  `data_paths`, `job_evidence`, `overnight_executor`, `pingpong_job`,
  `pingpong_loop`, `run_log`, `safe_points`, `test_execution_service`,
  `test_runner`, `timeline`, `ui_server`, `worktree_resume`. That is the reach
  of the move and it is much wider than round 11's or round 12's.
- A gate for that round should read the quoted token `"runs"` the way G5(a) here
  read `"pingpong_runs"` — enumerate `git ls-files` and filter in Python, not a
  `tests/**/*.py` shell glob (deviation 7).

After the run move, the rest of T002: the unified record's own fields and the
Mission extension (order, contract, mission plan, job refs). Then T003 consumer
by consumer; T004 the classic runner, the classic store and the resolver
collapse together (DECISION F260 D5); T005 the reachability test and the cluster
deletion.
