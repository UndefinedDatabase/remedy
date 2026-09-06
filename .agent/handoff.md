# Handoff — F260 One world · round 9 · THE RECORD MOVE

## Session

SESSION 3 of feature F260 · round 9 · rounds so far 9

Context self-assessment (amend0905-throughput): context is comfortable — this
round read four protocol files, one 400-line block and roughly 1,500 lines of
target source, and spent no rounds on rework. Several more delegated rounds fit
in this session.

## Range

Review of `1523fde1b26892ee2c38166e2fad573f0569e397`..`01c8c69251a3fda33a8388a9b2a02931c0b8e4ac`.

Seven commits, all single-parent, in the block's ordered sequence C0a → C5. No
reordering, no extra commit, no dropped commit. C6 is this file. Largest
insertion count 400 (`.agent/authored/f260-r9.md`, a single `.agent/**` state
write and exempt under the AGENTS.md counting rule); largest CODE commit 76.
Nothing approached the 500-insertion cap.

## Commits

### 24538e0c f260: save the round 9 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r9.md | +400 / -0 | C0a — the block copied byte-for-byte with `shutil.copyfile`, verified by `cmp` (silent) before staging |

### 4977258d f260: mirror the round 9 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +370 / -319 | C0b — same bytes again by `copyfile`, verified by `cmp` |

### a0754a6c f260: point the plan at the record move
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21 / -21 | C1 — whole-file replacement from the PLAN slice; 48 lines, under the AGENTS.md 50-line cap |

### f77d3ddd f260: book the round 8 PASS verdict into the record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — the GATE_R8 slice appended; 898817 → 902842 bytes |

### 7ef03f27 f260: append the three round 8 and 9 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +6 / -0 | C3 — SLIP1/2/3 appended; 97989 → 101682 bytes |

### 6eefc0ee f260: move the ping-pong record under the one jobs root
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/data_paths.py | +17 / -52 | `task_jobs_dir`, `task_job_dir`, `task_job_record_path` and the mirror-pair comment block DELETED; `_task_job_id_matches` globs `jobs_dir()`; `job_record_path` and `resolve_any_job_id` docstrings corrected; `Public API::` block trimmed |
| packages/orchestration/pingpong_job.py | +13 / -13 | five call sites onto `job_record_path` / `job_dir`; the local `job_dir` in `_finalize_job_workspace` renamed `job_root` at all three lines; the `resume_job_plan` docstring corrected |
| packages/orchestration/job_evidence.py | +3 / -3 | `job_result_diff_source` onto `job_dir`; the `mirror_job_run_into_ledger` docstring corrected |
| apps/cli/commands/teach_cmd.py | +2 / -2 | the two comments naming the second store; no code change |
| tests/test_data_paths.py | +6 / -53 | `_task_layout` and the two task-job tests deleted with their comment block; four stale prose sites corrected (two of them beyond the block's list — see deviation D4) |
| tests/orchestration/test_job_worktree_handoff.py | +8 / -8 | six call sites; the local `job_dir` at the shadowing site renamed `job_root` |
| tests/orchestration/test_pingpong_integration.py | +4 / -4 | four call sites |
| tests/orchestration/test_job_stop_integration.py | +4 / -4 | three hard-coded `task_jobs` literals now built from `job_record_path`, which is imported at module scope |
| tests/cli/test_teach_cmd.py | +9 / -5 | the `_write_task_job` helper and `test_a_directory_without_a_job_file_is_not_a_job` build from `job_dir`; the class docstring corrected; helper local renamed `job_root` |
| tests/orchestration/test_failure_wiring.py | +2 / -2 | two call sites |
| tests/orchestration/test_job_promote_consistency.py | +2 / -2 | two call sites |
| tests/orchestration/test_job_worktree_integration.py | +2 / -2 | two call sites |
| tests/orchestration/test_job_worktree_integrity.py | +2 / -2 | two call sites |
| tests/orchestration/test_job_budgets.py | +2 / -2 | one hard-coded literal now built from `job_record_path` |

### 01c8c692 f260: prove the record move and land R-0814
| Path | +/- | Reason |
|---|---|---|
| tests/test_data_paths.py | +69 / -0 | C5 — the two SPEC tests, in `TestJobAndRunLayout` |
| .agent/live_review.md | +2 / -0 | C5 — the one `Landed: R-0814` line; 902842 → 904283 bytes |

### C6 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | the round-9 handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/f260-r9-wt 01c8c692` | created, detached at `01c8c692`, for G7 only |
| `git worktree remove .remedy-wt/f260-r9-wt --force` | removed; `git status --porcelain` inside it was EMPTY before removal, so both mutations were fully reverted |
| `git push -u origin feature/f260-one-world` | pushed after C6 |

No pull request created, none merged, no force-push, no work on `main`.

## Verification

ONE LINE PER GATE, each with its REAL exit code.

| Gate | Exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | `sha256sum` over `.agent/authored/f260-r9.md` and `.agent/last_block.md` both return `746c9953166920d3a6304bb115e47334ab07fb1db3916a0c9f658b83272c71c7`, equal to the digest supplied with the delegation and to the scratch original. One reading, not a chain. See deviation D1: the block says "the digest in this block's BEGIN marker" and no BEGIN marker in the block carries a digest. |
| G2(a) BYTE | 0 | C2: 898817 + 1 + 4023 + 1 = 902842, measured 902842; the pre-image is a byte-exact PREFIX. C5: second growth 1441 = 1 + 1439 + 1 for the `Landed` line I measured; prefix again exact. |
| G2(b) STRUCTURAL | 0 | split on `"\n\n"`: 426 → 427 at C2 → 428 at C5; the LAST unit with the file's terminating newline stripped equals GATE_R8 byte-for-byte. |
| G2(c) NEGATIVE CONTROL | 1 | **UNMEETABLE AS WORDED.** Flipping byte 898868 (`O`→`P`, 50 bytes into the appended paragraph) gives reading (a)=True, reading (b)=False. The gate orders BOTH to reject. Reading (a) is length-arithmetic plus a pre-image-prefix test, and a one-byte SUBSTITUTION inside the appended region changes neither, so (a) accepts by construction in any round. (b) rejects, and both accept again after restore, so the protection is intact. Deviation D2. |
| G2(d) POPULATIONS | 0 | after C5: `^Gate: ` headers 18, all 18 distinct; `^- R-\d{4} — ` registrations 299; `^Done: R-\d{4} — ` lines 4 over TWO distinct ids (`R-0721`, `R-0725`); `^Landed: R-0814 — ` exactly 1. |
| G3 THE SLIPS | 0 | 97989 + 1 + 1102 + 2 + 1183 + 2 + 1402 + 1 = 101682, measured 101682; pre-image a byte-exact PREFIX; blank-line units 131 → 134, a rise of exactly THREE, one per slip. Not 132, not 133 — the separators did not fuse. |
| G4 THE PLAN | 0 | `.agent/plan.md` equals the PLAN slice plus exactly one trailing newline (2585 + 1 = 2586 bytes, byte-equality True); 48 lines, under 50. |
| G5(a) hasattr | 0 | False for `task_jobs_dir`, `task_job_dir`, `task_job_record_path`; True for `jobs_dir`, `job_dir`, `job_record_path`, `job_evidence_dir`, `run_dir` — the non-vacuity half, proving `hasattr` finds anything at all. |
| G5(b) AST | 0 | over 1031 `.py` files under `packages/`, `apps/`, `tests/`: references resolving to exactly `task_jobs_dir`, `task_job_dir`, `task_job_record_path` = 0, 0, 0. NON-VACUITY CONTROL: the same reading over `job_dir` = 75, non-zero. Zero unparseable files. |
| G5(c) LITERAL | **1** | **RED, AND IT CONTRADICTS SPEC C5(A).** The literal `task_jobs` occurs 3 times over the 1234 tracked files under `packages/`, `apps/`, `tests/`, ALL THREE in `tests/test_data_paths.py` (lines 396, 414, 415), inside the very test SPEC C5(A) ordered. Occurrences OUTSIDE that file: 0. One gitignored build artifact (`tests/__pycache__/test_data_paths.cpython-310-pytest-9.0.3.pyc`) carries a compiled copy of the same three strings. Deviation D3 — the headline. |
| G5(d) VALUE | 0 | with `REMEDY_DATA_DIR` at a scratch dir: `job_dir(j) == jobs_dir()/j`; `job_record_path(j) == job_dir(j)/"job.json"`; `job_evidence_dir(j) == job_dir(j)/"evidence"`; and all four honour an explicit `root` against an env root set to a DIFFERENT directory, with `env_root not in p.parents` for each, so a function dropping `root` cannot pass by coincidence. |
| G6 suites, group 1 | 0 | `pytest tests/test_data_paths.py tests/orchestration/test_mint_call_sites.py tests/cli/test_golden_path.py -q -p no:randomly` → **93 passed** (base 93; two tests deleted, two added). Carries the canary. |
| G6 suites, group 2 | 0 | the six worktree/promote/failure/pingpong files → **165 passed** (base 165). |
| G6 suites, group 3 | 0 | `test_job_stop_integration.py test_job_budgets.py test_teach_cmd.py` → **186 passed** (base 186). |
| G6 integrity | 0 | `python3 -m apps.cli.grouped integrity check --json` → `"passed": true`, `"fail_count": 0`, `"check_count": 5` (handler_import handlers=342, live_review_verdict, plan_consistency, relevant_untracked, high_blockers_open). |
| G7 MUTATION | 0 | see the block below. |
| G8 LINT + CLEAN | 0 | `ruff check` over exactly the fourteen change-set paths under `packages/`, `apps/`, `tests/` → "All checks passed!". `git status --porcelain` EMPTY. `git ls-files .remedy-wt` EMPTY. |

The three suite groups were run SERIALLY, each through `subprocess.run` so its
own `returncode` is read — never piped into another process, which would report
the pipe's last status instead (the F260 R3 lesson).

### G7 — mutation red-proof, in the disposable worktree at `01c8c692`

Every run purged `__pycache__` and used `python3 -B`. Module resolution was
re-confirmed before each colour: `packages.orchestration.data_paths` resolved to
`.remedy-wt/f260-r9-wt/packages/orchestration/data_paths.py` every time, inside
the worktree and never the primary checkout — checked because `remedy==0.1.0` is
installed in this environment and an installed copy can shadow a worktree. Each
mutation target was verified UNIQUE in its file (occurrence count 1) before the
edit; each revert was by exact path from the original bytes held in memory.

| Step | Exit | Reading |
|---|---|---|
| (i) unmutated control | 0 | **46 passed** — the baseline every colour below is measured against |
| (ii) `_task_job_id_matches` pointed back at a literal `task_jobs` directory (`tdir = jobs_dir().parent / "task_jobs"`) | 1 | 1 failed, 45 passed. Failing node id: `tests/test_data_paths.py::TestJobAndRunLayout::test_a_pingpong_record_in_the_jobs_dir_is_still_resolvable_beside_a_classic_one` |
| (iv) control after (ii) | 0 | 46 passed |
| (iii) `_persist_job` writes `jobs_dir() / job.job_id / "record.json"` | 1 | 2 failed, 44 passed. Failing node id: `tests/test_data_paths.py::TestJobAndRunLayout::test_a_persisted_pingpong_job_writes_its_record_under_its_own_job_dir`, plus an UNPREDICTED second — see deviation D7 |
| (iv) control after (iii) | 0 | 46 passed |

## Authored-text proofs

| Text | Proof |
|---|---|
| the whole block | `.agent/authored/f260-r9.md` and `.agent/last_block.md` are byte-identical to `.remedy-wt/f260-r9-block.md` — `cmp` silent for both, and all three sha256 to `746c9953…`. Applied by `shutil.copyfile`, never re-typed and never text-extracted. |
| PLAN | `.agent/plan.md` == PLAN slice + exactly one `\n`, byte-equality True (2586 bytes) |
| GATE_R8 | the last blank-line unit of `.agent/live_review.md`, terminating newline stripped, == the slice byte-for-byte |
| SLIP1 / SLIP2 / SLIP3 | appended at 1102 / 1183 / 1402 bytes with `"\n\n"` separators; total arithmetic exact and unit rise exactly 3 |

All five slices applied BYTE FOR BYTE. None was repaired, reflowed or reworded.

## Deviations & assumptions

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4,
C5, C6, in that order, one commit each. No path outside the block's change set
was written.

**D1 — G1 names a referent the block does not contain.** G1 orders the digest to
equal "the digest in this block's BEGIN marker". The block has five `<<<BEGIN …>>>`
markers and every one of them names a SLICE (`GATE_R8`, `SLIP1`, `SLIP2`,
`SLIP3`, `PLAN`); none carries a digest. The digest reached me only in the
delegation prompt. Applied against that digest; all three artifacts match, so
the gate's substance is satisfied and only its pointer is wrong. Reviewer-prose
defect, nothing wrong on disk.

**D2 — G2(c) is unmeetable as worded, in this round and in any round.** It orders
a one-byte flip inside the first appended paragraph to be rejected by readings
(a) AND (b). Reading (a), as G2(a) defines it, is total-length arithmetic plus a
pre-image-prefix test. A single-byte SUBSTITUTION inside the appended region
changes neither the total length nor the pre-image, so (a) cannot reject it —
not through a bad choice of byte, but by construction. Measured at offset 898868:
a=True, b=False; after restore both accept. Recorded RED as worded rather than
narrowed to the half that works, per constraint 1. The protection the clause
exists for is fully delivered by (b).

**D3 — SPEC C5(A) and gate G5(c) directly contradict each other; no worker can
satisfy both.** SPEC C5(A) orders, verbatim: "Assert the record is NOT under any
path containing a `task_jobs` component." Any assertion of that shape must
contain the literal `task_jobs`. G5(c) orders that same literal to occur ZERO
times under `packages/`, `apps/` and `tests/` — the roots that contain the file
the test goes in. I applied the SPEC as given and ran the gate as given: G5(c) is
RED at 3 occurrences, all three inside `tests/test_data_paths.py` in the ordered
test (line 396 its docstring, line 414 the ordered assertion, line 415 that
assertion's message), and ZERO occurrences anywhere else under those three roots.
So the MOVE is complete and only the guard for it still names the old spelling.
I did NOT reword the test to shrink the count: the count is 3 rather than 1
because the docstring and the failure message also name the old path, and
rewording ordered prose to move a metric on a gate that fails either way is
optimizing the measurement, not repairing the defect. The block's own carve-out
sentence — "`docs/roadmap/features/` is deliberately OUT of scope: the feature
files record the history and are not rewritten" — is exactly the reasoning that
was needed one clause further along: a guard test asserting the OLD layout is
gone must name the old layout, for the same reason a history file does. The fix
is to G5(c)'s scope, not to the test.

**D4 — two stale sites outside the block's enumeration, both inside change-set
files, both changed.** (a) `tests/test_data_paths.py:392` (base numbering) read
"``jobs_dir``, ``_jobs_dir``, ``task_jobs_dir`` and ``_resolve_jobs_dir`` are
FOUR DIFFERENT names". `task_jobs_dir` is deleted this round and the string
carries the literal G5(c) sweeps, so the list is now the three surviving names
and the numeral moved FOUR → THREE with it. (b) `tests/test_data_paths.py:566`
(base numbering), the docstring of
`test_no_migrated_module_names_the_deleted_jobs_dir_helper`, read "``_jobs_dir()
/ job_id`` was EQUAL to what ``task_job_dir`` returns"; corrected to `job_dir`.
The block named the two ASSERTION MESSAGES carrying that same deleted name
(lines 555 and 583) for exactly this reason and missed the docstring sitting
above them.

**D5 — SPEC(7)'s deletion confirmation, as ordered, with one correction.** Before
deleting `test_the_task_job_record_is_job_json_under_the_task_job_dir` and
`test_the_root_override_is_honoured_by_both_task_job_helpers` I confirmed every
reading survives. It does — but across FOUR tests, not the two the block names.
`.name == "job.json"` → `test_the_record_is_named_job_json`; the root override
for both helpers → `test_the_root_override_is_honoured_by_all_four`; the
`.parent` reading → `test_the_record_and_the_evidence_share_one_root`; and
`task_job_dir(jid) == task_jobs_dir() / jid`, which the block attributes to
neither survivor → `test_job_dir_is_jobs_dir_keyed_by_the_job_id`. No reading was
lost, so the deletion is safe and nothing was kept back; the block's survivor
list was incomplete rather than wrong.

**D6 — the `Landed` line's byte length, which the block asks me to report because
it did not write it: 1439 bytes, one line.** Its second growth reading is
therefore 1 + 1439 + 1 = 1441, measured 1441.

**D7 — G7(iii) produced a second failure the block did not predict, and it is a
guard working.** Mutating `_persist_job` to `jobs_dir() / job.job_id /
"record.json"` introduces a `jobs_dir` reference into `pingpong_job`, so
`test_no_module_that_owns_job_evidence_spells_the_path_itself[packages.orchestration.pingpong_job]`
fails beside test A. This independently confirms the block's DO-NOT-TOUCH
paragraph from the other side: that guard is live and can fail, and C4 does not
trip it because `job_dir` and `job_record_path` are DIFFERENT names under its AST
reading, exactly as the block predicted.

**D8 — G5(c) scope note.** The sweep as worded also matches
`tests/__pycache__/test_data_paths.cpython-310-pytest-9.0.3.pyc`, a gitignored
build artifact holding a compiled copy of the same three source strings. It is
not an independent occurrence and it is not tracked; the gate is reported over
the 1234 TRACKED files, with the artifact disclosed rather than silently
excluded.

**Assumption, stated because it is load-bearing:** the `remedy` console script is
denied in this sandbox, so G6's CLI reading was taken through
`python3 -m apps.cli.grouped integrity check --json`, which is the invocation the
block itself orders.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 plan.md ← PLAN | done | |
| C2 live_review.md ← GATE_R8 | done | |
| C3 prose_slips.md ← 3 slips | done | |
| C4 the move | done | |
| C5 the two tests + Landed line | done | |
| C6 handback | done | this file |
| G1 transport | done | PASS; pointer defect declared (D1) |
| G2 the record | deviated | (a) (b) (d) PASS; (c) RED and unmeetable as worded (D2) |
| G3 the slips | done | PASS |
| G4 the plan | done | PASS |
| G5 the move is complete | deviated | (a) (b) (d) PASS; (c) RED, contradicts SPEC C5(A) (D3) |
| G6 the suites | done | PASS — 93 / 165 / 186, integrity 5 checks, 0 fail |
| G7 mutation red-proof | done | PASS — both mutations red at the named node ids, control green throughout |
| G8 lint and clean tree | done | PASS |

## Open findings

**297 open by DISTINCT ID**, not 295. `.agent/live_review.md` holds 299
registration paragraphs carrying 299 distinct ids, against 4 `Done:` lines
carrying only TWO distinct ids (`R-0721`, `R-0725`). The §3 item 10 formula
subtracts one population from the other and returns 295; SLIP3, appended this
round in C3, records that double-count. `R-0814` is LANDED this round but not yet
`Done:` — the reviewer authors that paragraph at the next gate — so it is still
inside the 297.

## Next

Reviewer gates round 9 against the committed diff `1523fde1..01c8c692`,
re-running every gate itself. Two clauses are RED BY CONSTRUCTION and need a
ruling rather than a repair round on the product: G2(c)'s "BOTH readings reject"
and G5(c)'s zero-literal sweep versus SPEC C5(A)'s ordered assertion. If the
verdict is PASS, the next round is T002's remaining work: the ONE resolver —
`resolve_job_id` and `resolve_any_job_id` collapsing into one `str`-returning
function over `storage.load_job`'s signature and its forty call sites across nine
`apps/cli/commands/` modules (DECISION F260 D4), where finding R-0809 belongs.
Before authoring it, re-read `.agent/STOP` from disk (self-drive Phase 1 rule 1,
before rule 2).
