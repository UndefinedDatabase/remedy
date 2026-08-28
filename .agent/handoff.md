# Handback — F037 R7 (T001 read-endpoint part two)

## Session

SESSION 2 of feature F037 · round 7 · rounds so far 7

## Range

Review of `6b778634`..`HEAD` (base SHA `6b778634e7b952ef2cb5fff6c3e02634249405ae`,
branch `feature/f037-rendered-diff-viewer`).

## Commits

### 36832de5 docs(agent): save the F037 R7 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f037-r7.md | +364 -0 | C0a — the block saved verbatim, 24804 bytes, 364 lines |

### 7d5d8733 docs(agent): mirror the F037 R7 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +283 -326 | C0b — mirror written from the committed C0a blob, same blob hash |

### 402677f6 docs(agent): point the plan at the F037 R7 route round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22 -21 | C1 — whole-file replacement by PLANF037R7 |

### a89b6cd6 docs(agent): book the F037 R6 gate verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 -0 | C2 — GATER6 appended at EOF |

### 7a83d3ba feat(ui-server): serve the F037 diff envelope on two GET routes
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +35 -0 | C3 — S1 dict key, S2/S3 the two thin builders, S4 the structural route, S5 the import style |

### 23b9ab39 test(ui-server): walk the task-run diff route and drop the stale endpoint count
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_channel.py | +3 -2 | C4 — WALKPAIR registers the new route, DOCPAIR deletes the numeral (`R-0715`) |
| .agent/live_review.md | +2 -0 | C4 — LANDED715 appended at EOF |

### 995b42cd test(ui-server): cover the two F037 diff routes over real HTTP
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_diff_endpoint.py | +188 -0 | C5 — new file, S6 to S12, six tests |

### C6 (this commit) docs(agent): hand back F037 R7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | not measurable | C6 — a handback cannot table the commit that writes it; G8's per-commit reading deliberately stops at C5 |

## External actions

- `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/f037r7wt HEAD` — created at `995b42cd` (detached).
- `git worktree remove … --force` then `git worktree prune` — removed; `git worktree list` back to 1 line, primary `git status --porcelain` 0 lines.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. No PR created, nothing merged.
- `git push origin feature/f037-rendered-diff-viewer` — ordered AFTER this commit and deliberately not part of any gate; its result is not named here, the reviewer reads the remote tip itself.

## Verification

**G1 hygiene — PASS.** `.agent/STOP` read from disk before C0a: ABSENT. Read again
before C6: ABSENT. `git rev-parse HEAD` before C0a =
`6b778634e7b952ef2cb5fff6c3e02634249405ae`, equal to the base.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain` line count after C0a 0, C0b 0, C1 0, C2 0, C3 0, C4 0, C5 0.

**G2 transport, one digest comparison — PASS.** After C0a:
`.agent/authored/f037-r7.md` sha256
`a2b07da54d9a81408f8d10e4a6dc7bb5703d897ef9a3555b2c6a4ad45186ec55`, 24804 bytes,
364 lines. After C0b: `git rev-parse HEAD:.agent/authored/f037-r7.md` and
`git rev-parse HEAD:.agent/last_block.md` are BOTH
`a4bee2a8a2a989270d0366fd193d9c2303e02fd7` — the same blob. This chain covers the
saved copy, its mirror and the working copy, and it claims nothing whatever about
the bytes of any prompt.

**G3 extraction and caps — PASS.** Every slice extracted from the COMMITTED C0a
blob by its marker lines: PLANF037R7 49 lines, GATER6 1, LANDED715 1, WALKPAIR 17,
DOCPAIR 8. TOTAL 364, CONTENT 76, PROSE = 364 − 76 = 288. PROSE 288 ≤ 400 and
TOTAL 364 ≤ 490.

**G4 the plan at C1 — PASS.** `.agent/plan.md` byte-equal to PLANF037R7 under the
newline-included convention: **True**. NEGATIVE CONTROL against the slice minus its
trailing newline: **False**. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49
(strictly under 50).

**G5 the record, full byte forensics — PASS.**
At C2, GATER6: base `.agent/live_review.md` measured **1162114 bytes**, which is the
figure the block named. Reader (a): 1162114 + 1 + 3583 = 1165698 = measured
post-append length, and the base IS a byte prefix of the result — True. Reader (b),
independent and structural: the script counted N = 1 blank-line unit in GATER6 and
compared the LAST 1 unit of the file against the slice's 1 unit in order — True.
NEGATIVE CONTROL, one byte flipped inside the FIRST appended paragraph (offset
1162119, `b':'` → `b'\x1a'`): reader (a) **False**, reader (b) **False**.
At C4, LANDED715: base measured 1165698 (the length after C2). Reader (a):
1165698 + 1 + 647 = 1166346 = measured post-append length, base is a byte prefix —
True. Reader (b), N = 1 — True. NEGATIVE CONTROL at offset 1165703
(`b'e'` → `b'E'`): reader (a) **False**, reader (b) **False**.
COUNTS after C4, line-anchored, each as measured:
`^- R-\d+ — ` **279** (ordered 279, unchanged — no id minted);
`^Done: R-\d+ — ` **27** (ordered 27, unchanged);
`^Landed: R-` **2** (ordered 2 — the surviving `R-0711` line plus LANDED715);
`^Gate: F\d+ R\d+ — ` **77** (ordered 77).
Open set = 279 distinct registered − 27 distinct resolved = **252**, and `R-0715`
IS still in it (registered True, resolved False), exactly as constraint 6 requires.

**G6 the red-proofs — PASS, all three mutations red.** Run only inside the
disposable worktree `/home/decodeux/Repos/remedy/.remedy-wt/f037r7wt` at the C5
tree, never in the primary checkout; `__pycache__` purged and `python3 -B` used
before EVERY run; the file restored with `git checkout --` between mutations
(`git status --porcelain` in the worktree 0 lines after each restore).

UNMUTATED CONTROL: `python3 -B -m pytest tests/ui_server/test_diff_endpoint.py -q`
→ real exit code **0**, `6 passed in 5.43s`.

(a) remove the `"diff"` key from the `handlers` dict — occurrences of the FROM
string before the edit: **1**.
FROM:
```
                "diagnostics": _build_diagnostics_json,
                "diff": _build_diff_json,
```
TO:
```
                "diagnostics": _build_diagnostics_json,
```
→ real exit code **1**, `2 failed, 4 passed in 0.89s`. Failing node ids:
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_job_route_serves_the_workspace_diff`,
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_job_without_evidence_names_the_absence_at_status_200`.
The job route falls through to the 404, as the mutation's property predicts.

(b) make the structural route ignore `parts[5]` and pass `task_id=None` —
occurrences of the FROM string before the edit: **1**.
FROM:
```
            self._send_json(200, _build_task_run_diff_json(job, parts[5]))
```
TO:
```
            self._send_json(200, _build_task_run_diff_json(job, None))
```
→ real exit code **1**, `2 failed, 4 passed in 0.90s`. Failing node ids:
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_task_run_route_serves_only_that_runs_diff`,
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_unknown_task_run_is_a_named_absence_at_status_200`.
The reported body confirms the mutant served the JOB diff
(`'path': 'packages/orchestration/job_scope_only.py'`, `'scope': 'job'`), which is
what S7's different-file-paths design exists to catch.

(c) make the unknown-task-run case answer 404 instead of 200 with the named
absence — occurrences of the FROM string before the edit: **1**.
FROM:
```
            self._send_json(200, _build_task_run_diff_json(job, parts[5]))
```
TO:
```
            _view = _build_task_run_diff_json(job, parts[5])
            if _view.get("reason") == "unknown_task_run":
                self._send_json(*_safe_error(404, "not found"))
                return
            self._send_json(200, _view)
```
→ real exit code **1**, `1 failed, 5 passed in 0.90s`. Failing node id:
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_unknown_task_run_is_a_named_absence_at_status_200`
(`AssertionError: {'error': 'not found'}` / `assert 404 == 200`). The mutation was
made in the ROUTE, which is the code this round wrote;
`packages/orchestration/diff_view_source.py` was never touched, in the worktree or
out of it.

The guard C4 edits, UNMUTATED and in the SAME worktree:
`python3 -B -m pytest tests/ui_server/test_command_channel.py -q` → real exit code
**0**, `106 passed in 11.26s`. No mutation came back green.
After removal and prune: `git worktree list` **1** line,
`git status --porcelain` in the primary checkout **0** lines.

**G7 suite, lint and canary at C5 — PASS.** One pytest process at a time
throughout; no two suites ran in parallel.
`python3 -m pytest tests/ui_server/test_diff_endpoint.py tests/ui_server/test_command_channel.py tests/orchestration/test_diff_view_source.py -q`
→ real exit code **0**, `121 passed in 12.11s`, lines matching `^FAILED`: **0**.
Extractor-blindness control: the SAME counter over a control string containing
`FAILED tests/ui_server/test_diff_endpoint.py::test_control_string` returns **1**,
so the 0 above is a measurement and not a blind spot.
`tests/ui_server/test_command_channel.py` alone: real exit code **0**,
`106 passed in 11.01s` — the count measured is 106, equal to the base reading the
block named; no difference to report.
Node-id inventory of the new file from
`python3 -m pytest tests/ui_server/test_diff_endpoint.py --collect-only -q` —
**6 tests collected**, never derived from `-v` output:
- `tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_job_route_serves_the_workspace_diff`
- `tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_task_run_route_serves_only_that_runs_diff`
- `tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_unknown_task_run_is_a_named_absence_at_status_200`
- `tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_job_route_refuses_a_bad_token`
- `tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_task_run_route_refuses_a_bad_token`
- `tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_job_without_evidence_names_the_absence_at_status_200`

`python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_diff_endpoint.py tests/ui_server/test_command_channel.py`
under the repository's own configuration, no `--isolated` → real exit code **0**,
verbatim output `All checks passed!`.
Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → real exit code **0**,
`42 passed in 20.58s`.

**G8 structure, artifacts and the Open PR Gate at C5 — PASS.**
`git diff --name-only 6b778634..995b42cd` returns exactly:
`.agent/authored/f037-r7.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `packages/orchestration/ui_server.py`,
`tests/ui_server/test_command_channel.py`, `tests/ui_server/test_diff_endpoint.py`.
Residue actual-minus-expected: **[]**. Residue expected-minus-actual: **[]**.
Restricted `git diff --stat`: `apps/` **empty**, `docs/` **empty**, `packages/`
holds only `ui_server.py` (1 file changed, 35 insertions), `tests/` holds only
`test_command_channel.py` and `test_diff_endpoint.py` (2 files changed, 191
insertions, 2 deletions).
Per-commit INSERTION counts from `git diff --numstat`, each single-parent and each
under 500: C0a `36832de5` **364** (parents 1), C0b `7d5d8733` **283** (1), C1
`402677f6` **22** (1), C2 `a89b6cd6` **2** (1), C3 `7a83d3ba` **35** (1), C4
`23b9ab39` **5** (1), C5 `995b42cd` **188** (1). C6 is deliberately not measured:
its own count cannot exist while its text is being written.
Line-anchored `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` at C1 **0 / 0**,
`.agent/live_review.md` at C4 **0 / 0**. The SAME counter over the C0a blob
measures **5 / 5**, greater than zero, so the sweep is shown not to be blind.
Count of the string `thirteen` in `tests/ui_server/test_command_channel.py` after
C4: **0** — that is `R-0715`'s repair, done by DELETING the numeral. The
counter-measure was checked against substitution too: `twelve` 0, `fourteen` 0,
`fifteen` 0, `sixteen` 0, so no other numeral word took its place.
`git ls-files .remedy-wt` line count **0**.
Open PR Gate, verbatim:
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

Every reviewer-authored text was extracted from the COMMITTED C0a blob by its
marker lines in Python and applied without retyping.

| Slice | Proof |
|---|---|
| PLANF037R7 | whole-file replacement; disk byte-equal to the slice **True**, negative control (slice minus trailing newline) **False** |
| GATER6 | append at EOF; reader (a) True, reader (b) True, negative control both False (G5) |
| LANDED715 | append at EOF; reader (a) True, reader (b) True, negative control both False (G5) |
| WALKPAIR | FROM measured at **1** occurrence before the edit; `TO contains FROM: False`; after C4 FROM **0x**, TO **1x** |
| DOCPAIR | FROM measured at **1** occurrence before the edit; `TO contains FROM: False`; after C4 FROM **0x**, TO **1x** |

## Deviations & assumptions

1. **G5 reader (a) is the byte identity, not only its two reported facts.** The
   block names reader (a) by two properties — post-append length equals base + 1 +
   slice length, and the base is a byte prefix of the result — and then orders a
   NEGATIVE CONTROL that flips one byte INSIDE the appended paragraph to come back
   False for reader (a) as well as reader (b). Those two properties alone are blind
   to such a flip: neither the length nor the prefix changes. Reader (a) was
   therefore implemented as the full byte identity
   `result == base + b"\n" + slice`, which ENTAILS both named properties, and all
   three components are reported separately above for both appends (real:
   length True, prefix True, tail-identity True; control: length True, prefix True,
   tail-identity False). This is the only reading under which the ordered control
   result is achievable; no gate was weakened.
2. **Assumption, S5 import style.** The neighbouring `_build_*_json` builders in
   `ui_server.py` all use FUNCTION-LOCAL imports
   (`from packages.orchestration.ui_view_model import …` inside the body), so both
   new builders import `build_diff_view` function-locally rather than at module
   top. `_resolve_evidence_dir` was neither redefined nor moved.
3. **Assumption, S3 annotation.** `_build_task_run_diff_json(job: Any, task_id: str)`
   is annotated `str` for `task_id`, matching the neighbouring
   `_build_node_detail_json(job: Any, node_id: str)` shape; the spec gave no
   annotation. `build_diff_view` itself accepts `str | None`.
4. **Assumption, S8/S9 "files naming the path".** Asserted as an exact ordered list
   of `f["path"]` values, so the job route naming the task file (or the reverse) is
   a red rather than a permissive superset check.
5. No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4,
   C5, C6 were committed in that order, one commit each, with no extra commit, no
   dropped commit and no reordering.
6. No finding id was minted. `R-0715` was REPAIRED and carries a `Landed:` line
   only; no `Done:` paragraph was written for it, per constraint 6 — the reviewer
   authors that at the next gate. The `Landed: R-0711` line and every existing
   `Done:` paragraph are untouched.
7. `packages/orchestration/diff_view_source.py` and
   `packages/orchestration/diff_parser.py` were not touched, in the primary
   checkout or in the worktree.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `36832de5`, 364 lines, sha256 `a2b07da5…` |
| C0b mirror the blob | done | `7d5d8733`, same blob hash as C0a |
| C1 plan from PLANF037R7 | done | `402677f6`, byte-equal True |
| C2 live_review append GATER6 | done | `a89b6cd6` |
| C3 ui_server routes | done | `7a83d3ba` |
| C4 WALKPAIR + DOCPAIR + LANDED715 | done | `23b9ab39` |
| C5 test_diff_endpoint.py | done | `995b42cd`, 6 tests |
| C6 handback | done | this commit |
| S1 `"diff"` key in the handlers dict | done | added to that dict and nowhere else |
| S2 `_build_diff_json(job)` | done | thin caller, one-line WHY above it |
| S3 `_build_task_run_diff_json(job, task_id)` | done | same shape, `task_id=` passed through |
| S4 structural task-run route | done | after `debug-detail`, before the 404; WHY comment names the `_walkable_paths` hand-registration |
| S5 import style + 200-on-unknown | done | function-local import matching the neighbours; unknown run answers 200 with `unknown_task_run` |
| S6 harness matched to `TestUIServerIntegration` | done | autouse fixture, `REMEDY_DATA_DIR`, port 0 daemon thread, info-file wait, `HTTPConnection` on `127.0.0.1`; nothing imported from `test_command_channel.py` |
| S7 evidence index + two different-path diffs | done | `job_evidence_index/<job_id>.json` with `evidence_dir_local`; `workspace.diff` names `…/job_scope_only.py`, `task_runs/T001/safe.diff` names `…/task_scope_only.py` |
| S8 job route 200 | done | `test_job_route_serves_the_workspace_diff` |
| S9 task-run route 200, files ONLY the task path | done | `test_task_run_route_serves_only_that_runs_diff` |
| S10 unknown run, explicit 200 | done | `test_unknown_task_run_is_a_named_absence_at_status_200` |
| S11 bad token 403 on both routes | done | two tests, one per route |
| S12 absent evidence index | done | `test_job_without_evidence_names_the_absence_at_status_200` |
| G1 hygiene | done | STOP ABSENT twice, HEAD = base, 7 clean readings of 0 |
| G2 transport | done | one digest comparison, identical blob hash |
| G3 extraction and caps | done | PROSE 288 ≤ 400, TOTAL 364 ≤ 490 |
| G4 the plan | done | True / False / 1 / 1 / 49 |
| G5 the record | done | both appends, both readers, both controls False; four counts as ordered; open set 252 with `R-0715` in it |
| G6 red-proofs | done | control exit 0; three mutations exit 1; guard suite exit 0; worktree removed |
| G7 suite, lint, canary | done | 121 passed, `^FAILED` 0 with a control of 1, ruff exit 0, canary exit 0 |
| G8 structure and Open PR Gate | done | both residues empty, all insertion counts under 500, `thirteen` 0, `[]` |

## Next

The first action of the next round is to re-read `.agent/STOP` from disk
(self-drive Phase 1 rule 1), and only then run the Open PR Gate
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

T001 is COMPLETE: the parser, the resolver and both read routes are on disk and
exercised over real HTTP. T002 is next — the rendering core (lines, intraline
emphasis, hunk heads, hunk collapse) against the binding CSS in
`docs/roadmap/features/T5_F037.md`, with goldens per fixture shape. That is the
first UI work of this feature, so `docs/ui/design_reference/` becomes binding from
the next round on.

Open findings: 252. `R-0715` is repaired on disk and carries a `Landed:` line; it
stays OPEN until reviewer-authored `Done:` text resolves it at the next gate.
