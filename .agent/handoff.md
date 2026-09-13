# Handback — F275 round 87

## Session

`SESSION 30 of feature F275 · round 87 · rounds so far 87`

Context self-assessment: this worker ran one generator over four scratch trees, one transform over one
detached worktree, one instrument five times over pinned transcripts, and one canary; it ran no suite and
has ample context left. Nothing about the session boundary is forced by this round.

## Range

Review of `bd2a75d5`..`HEAD` (the nine commits C0a–C7 plus this handback commit C8).

## Commits

### 19202ba3 F275 R87 C0a: save the round 87 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r87.md` | +300 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r87_block.md` at 29430 bytes |

### 2890f9ca F275 R87 C0b: mirror the round 87 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +214 / -205 | written from the COMMITTED C0a blob read back with `git show` |

### a67d18dc F275 R87 C1: make the plan current for round 87

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20 / -16 | slice PLAN87, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### 5123721f F275 R87 C2: book the round 86 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD87 appended |

### ec7a051f F275 R87 C3: append the round 86 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +6 / -0 | slice SLIPS87 appended |

### 09373353 F275 R87 C4: commit the residue instrument over the pinned transcripts

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r87-residue.py.md` | +203 / -0 | SPEC I: the worker's own instrument, one `python` fence of 5468 bytes, sha256 `d42fbd3c8b8c3048c31f877bef4f9ddc898a19c0522b4171745424fc94907317`; the carrier was generated from the scratch source and its extraction verified to round-trip before staging |

### 75afa4fa F275 R87 C5: land the flip residue reading at its own base

| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t003_flip_residue_r87.md` | +166 / -0 | SPEC A: scope paragraph, G4 generator and transform readings beside the reviewer's, the committed C4 fence's stdout verbatim |

### 7f242191 F275 R87 C6: record DECISION F275 D61

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +18 / -0 | slice DEC87 APPENDED after G4, G5 and G6 ran; deletion column ZERO |

### 9776de2f F275 R87 C7: file the operator question on how the flip lands

| Path | +/- | Reason |
|---|---|---|
| `.agent/operator_questions.md` | +9 / -1 | slice OPQ87, a full replacement, byte for byte; the one deleted line is `EMPTY — nothing is waiting on the operator.` |

### C8 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate runs after C8, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8:
C0a 300/0 = 300/0; C0b 214/205 = 214/205; C1 20/16 = 20/16; C2 8/0 = 8/0; C3 6/0 = 6/0; C4 203/0 = 203/0;
C5 166/0 = 166/0; C6 18/0 = 18/0; C7 9/1 = 9/1. Nine of nine pairs EQUAL, zero differ. Every commit staged
exactly ONE path; the largest insertion count is C0a at 300.

## External actions

| Command | Outcome |
|---|---|
| `git archive ef75e213` and `git archive bd2a75d5`, extracted by `tarfile` into `.remedy-wt/r87w/tree_base` and `tree_tip`, each `git init -q` + `git add -A -f .`; `tree_shift` and `tree_delete` by `shutil.copytree(..., symlinks=True)` and re-indexed | all exit **0**; plain directories, never registered worktrees |
| `git worktree add --detach .remedy-wt/r87w/wt bd2a75d5` (G4) | exit **0**, `HEAD is now at bd2a75d5`; `git worktree list` then showed two rows |
| `git checkout -- .` inside that worktree, then `git worktree remove .remedy-wt/r87w/wt`, then `git worktree prune -v` | exit **0**, **0**, **0**, all BEFORE C4 and WITHOUT `--force`; the worktree's `status --porcelain` read `''` before the remove; afterwards the path does not exist and `git worktree list` shows one row (deviation 2) |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C8; its result is in the round report |
| `gh` / `remedy` | NOT RUN. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite, NO SUITE RUN |

## Verification

Each gate ran through `.remedy-wt/r87w/run.py`, which saves the output to `.remedy-wt/r87w/<name>.out` and
appends `PROCESS_EXIT=` from the subprocess's own return code. No reading below differs from the reviewer's
figure.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C7 | 0 | `cmp` of `.remedy-wt/r87_block.md` against the COMMITTED C0a blob exit **0**, empty output, both 29430 bytes, sha256 `277ccb94…159697` (equal to the digest the delegation stated); `.agent/last_block.md` at C0b equals the C0a blob; slices FOUND **5**: PLAN87 2657 bytes / 45 lines, RECORD87 3278 / 8, SLIPS87 1352 / 6, DEC87 5854 / 18, OPQ87 2100 / 18, each MATCHING the sha256 on its BEGIN marker; TOTAL **300**, slice lines 95, PROSE **205**, as constraint 9 states; no line is a run of one repeated character; all 6 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C7 | 0 | `.agent/plan.md` at C1 byte-identical to PLAN87 from the committed C0a blob, 2657 bytes; **45** lines; one `## Goal`, one `## Next Steps`; unchanged at C7 |
| G3 the record | C7 | 0 | pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD87: **1119826** (MATCHES the block) + 3278 = 1123104; C6 DEC87: **1264216** (MATCHES the block) + 5854 = 1270070. READER A exact for both; READER B holds at N counted by the script as **4** and **9**, in order. Negative controls: a letter flipped in each FIRST appended paragraph (`G`→`g` at 1119827, `D`→`d` at 1264220) REJECTED by BOTH readers, both. Deletion columns **0 / 0**. prose_slips at C3 = its **296513**-byte pre-commit blob + SLIPS87 exactly (297865), deletion column 0. `.agent/operator_questions.md` at C7 byte-identical to OPQ87, 2100 bytes. Header pattern DERIVED from the pre-commit ledger (prefix to the first ` — `, digit runs generalised): one shape, `^Gate: F\d+ R\d+ — `, matching **108 of 108** `Gate:` heads (555 paragraphs); RECORD87's header matches it as `Gate: F275 R86 — `, no earlier head has that prefix, byte-duplicate first lines 0 |
| G4 the re-derivation | before C4 | 0 / 0 / 0 | three processes: `g4_trees` exit 0, `g4_gen` exit 0, `g4_flip` exit 0. FENCES from the carriers at `bd2a75d5`: re-key 5186 bytes `f56394e9…`, owner check 24253 `7be34374…`, generator 10580 `c50da973…`, transform part1+part2 29032 `075bc0dc…`, all four MATCH. DELETE: the line's count in `brain_detail.py` read **1** (line 142) before removal. GENERATOR (inner re-key and owner runs each REAL EXIT 0): **21** differing paths; **2183** ruled sites after the subtraction; recovered by the scope key **2183 / 2183 / 2183** at TIP / SHIFT / DELETE, UNRESOLVED **0 / 0 / 0**; line-key control **2157 / 2148 / 2148**; owner check at TIP **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED. TRANSFORM exit 0: PRECONDITION **2183** resolving, **0** not; **264** files rewritten; **6097** total rewrites; **0** broken. `git diff --numstat` in the worktree: **264** files, **5252** insertions, **5079** deletions, **4177** under `tests/`, **1075** elsewhere, largest **141** (`tests/orchestration/test_job_fulfillment.py`); untracked files 0. CENSUS by `ast` over 269 `.py` files under `packages/` at `bd2a75d5`: **55** `UUID(...)` calls, **29** of `load_job`, **4** of `load_job_safe` (the rest: 13 no call, 3 `str`, 2 `load_project`, 1 each `_lj`, `_mii`, `add`, `make_intent_id`) |
| G5 the residue | C5 | 0 | the three pinned digests MATCH. The committed C4 fence (5468 bytes, `d42fbd3c…`) ran TWICE, exit 0 / 0, no stderr, stdouts BYTE-IDENTICAL at 5266 bytes, sha256 `3752f7a1…775a53`. Tallies `1 failed, 18429 passed, 29 skipped, 1 warning`, `796 failed, 17603 passed, 29 skipped, 1 warning, 31 errors`, `795 failed, 17610 passed, 23 skipped, 1 warning, 31 errors`; distinct bad nodes **1 / 827 / 826**; flip-only **826**, control-only **0**; symmetric difference exactly `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes` (only in the one-line flipped run); **826** sections; AssertionError **233**, TypeError **142**, AttributeError **114**, ValueError **85**, `http.client.RemoteDisconnected` **80**, `<none>` **74**; deepest frames production **237**, test **589**, unattributable **0**; pairs `data_paths.py::job_dir` TypeError **80**, `job_fulfillment.py::run_job_fulfill` ValueError **46**, `pingpong_job.py::_persist_job` TypeError **31**, `flight_plan.py::map_flight_plan_to_tasks` TypeError **12**. All 22 compared figures MATCH. At C5, read from the COMMITTED blob `75afa4fa`: all **85** stdout lines found in the artefact in order, 0 missing |
| G6 the instrument can fail | C5 | 0 | scratch copies only. (a) the exact `FAILED …::test_staged_apply_has_staged_scope` line counted **1** in the flipped copy, removed: flip-only reads **825**, instrument exit 0. (b) the `FAILED tests/test_data_paths.py::TestLookupJobId::test_a_non_hex_string_raises_invalid` line appended after the control copy's last `FAILED` line (line 297): control-only reads **1**, exit 0. (c) lines ENDING `packages/orchestration/data_paths.py:201: in job_dir` removed from the short copy: **80** (equal to the reviewer's copy); no output row names `data_paths.py::job_dir`, the pair is ABSENT, exit 0 |
| G7 tree, canary, lint, path set, open set | C7 | 0 | `git status --porcelain` exit 0 `''`; `git worktree list` **1** row; CANARY `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit **0**, **42 passed**; `ruff check .` exit **1**, **26** `-->` rows against ruff's own `Found 26 errors.`; `.py` files under `.agent/` on the filesystem **0**; changed paths `bd2a75d5`..C7 **9** against the Bundle minus handoff **9**, MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `bd2a75d5` (112 registered − 24 Done) and **88** at C7 (112 − 24), membership IDENTICAL; `R-0809`, `R-0880` and `R-0883` OPEN at both |
| G8 insertion cap | C7 | 0 | C0a 300/0 1 path, C0b 214/205 1, C1 20/16 1, C2 8/0 1, C3 6/0 1, C4 203/0 1, C5 166/0 1, C6 18/0 1, C7 9/1 1; commits reaching 500 insertions **0**. Over `a5bf8949`..`bd2a75d5`, non-merge commits above 500 insertions: **8** — `8b02f1e8` 627, `75cc221e` 636, `dac50bcd` 609, `0d47205d` 551, `7ac6ec87` 553, `30072048` 515, `bf5ec6a4` 711, each `.agent/handoff.md` alone (**7**), and `78e5c18c` **529**, `.agent/authored/f275-r73-owner-stage.py.md` |

THE READINGS DEC87 STATES WERE CHECKED BEFORE C6 LANDED (`.remedy-wt/r87w/pre_c6.out`): beyond G4–G6, the 80
`RemoteDisconnected` sections' last captured server-side traceback line reads
`AttributeError: '_JobPlanAdapter' object has no attribute 'job_id'` **73** times and
`TypeError: unsupported operand type(s) for /: 'PosixPath' and 'UUID'` **7** times, and the eight oversize
commits above were listed by the same command G8 later ran. All matched.

STOP READINGS, per constraint 3: before C0a and before C8, `.agent/STOP` ABSENT at both — `test -e`
exit 1, `ls -la` exit 2, `os.path.exists` False — transcripts `.remedy-wt/r87w/stop_before_C0a.txt`
and `.remedy-wt/r87w/stop_before_C8.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r87.md` | `cmp` exit 0 against `.remedy-wt/r87_block.md`, 29430 bytes, sha256 `277ccb94802280d8e23b70d4680258c2f4e97ee81aa5b2345ddf36275e159697` |
| PLAN87 | `.agent/plan.md` | byte-identical, 2657 bytes, sha256 `12dfff71d180b560b1aa305c0e092e6766b9dfe7f07e8838ab97804ae4b00e3c` |
| RECORD87 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 3278 bytes, sha256 `770e942105badf349aea56de206a5dc223f6de5f8ead80b60f4755e9c3ab148f` |
| SLIPS87 | `.agent/prose_slips.md` | exact suffix at C3, 1352 bytes, sha256 `74e778bdb8e80c782a0abdbeeb816566ce67cde8f1f5f3f5fd8850ebbed39d86` |
| DEC87 | `.agent/decisions.md` | exact suffix at C6 under readers A and B, 5854 bytes, sha256 `435031a68f9b24c9392e857e234b1e30d10f570428821c101537efcc409421cf` |
| OPQ87 | `.agent/operator_questions.md` | byte-identical, 2100 bytes, sha256 `f009f1512642ce5d5950a08032e1bd58595b022ba071178ec8caa231c887b762` |

Every slice was applied by bytes from the COMMITTED C0a blob, and NO SLICE WAS EDITED. C4 and C5 are the
worker's own text, written from SPEC I and SPEC A.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 86 verdict | done | |
| C3 prose slips | done | |
| C4 SPEC I instrument | done | definitions stated in the carrier (deviation 3) |
| C5 SPEC A artefact | done | empty stdout lines left unindented (deviation 1) |
| C6 DECISION F275 D61 | done | after G4, G5 and G6 ran |
| C7 operator question | done | |
| C8 handback | done | this commit |
| G4 | done | exit 0 · 0 · 0, before C4 |
| G5 · G6 | done | exit 0, at C5 |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C7 |

## Deviations & assumptions

1. **SPEC A's "EVERY STDOUT LINE INDENTED BY ONE SPACE" IS MET FOR EVERY NON-EMPTY LINE ONLY.** The instrument's
   stdout has three empty lines, the separators between I1, I2, I3 and I4. In the artefact they stay empty
   rather than becoming a lone space, because a line of nothing but a space is trailing whitespace in a committed
   document. Round 82's generator made the same choice, and no `f275_t003_*` artefact from rounds 70 to 82 has a
   whitespace-only line. The artefact says so in the sentence before the stdout. The in-order check treats an
   empty stdout line as an empty artefact line, and the artefact's last 85 lines, unindented, EQUAL the stdout
   lines.

2. **THE G4 WORKTREE WAS RESTORED BEFORE IT WAS REMOVED.** The transform rewrites 264 tracked files, and
   `git worktree remove` refuses a modified worktree without `--force`. So `git checkout -- .` ran inside the
   detached worktree after the numstat was read. It left `status --porcelain` at `''` and 0 untracked files, and
   the remove and prune then ran without `--force`. No branch or commit was touched.

3. **INSTRUMENT DEFINITIONS SPEC I LEFT OPEN, STATED IN THE C4 CARRIER.** "Pytest's final tally line" is the LAST
   line that is a comma-separated run of `<n> <word>` counts followed by ` in <seconds>s (<clock>)`, and only the
   counts are printed. PREFIX and one `/` are stripped only when the frame path starts with PREFIX. The section
   region starts at the first line containing `= ERRORS =` or `= FAILURES =` and ends at the first later line
   containing `short test summary info`. Lines before the first section header in that region belong to no
   section. "Sorted" for a count listing means count descending and then key ascending, which is a total order.
   The symmetric difference is sorted by node id, and each row names the transcript it appears in.

4. **G4 CENSUS DEFINITION.** A `UUID(...)` call is an `ast.Call` whose callee is the bare `Name` `UUID`. The
   attribute form `<x>.UUID(...)` occurs 0 times under `packages/`. Each call is counted by the callee name,
   bare `Name` id or `Attribute` attr, of the call whose positional arguments contain it. Import aliases are NOT
   followed, so the one call into `_lj` and the one into `_mii` count under those names, not under
   `load_job` or `make_intent_id`. Under this definition the reviewer's 55 / 29 / 4 reproduce.

5. **ONE GATE READING WAS TAKEN LATER THAN THE DECISION THAT QUOTES IT.** DEC87 at C6 quotes the eight-commit
   oversize history, which constraint 10 assigns to G8 at C7. The same command ran before C6 as a scratch check
   (`pre_c6.py`), and G8 re-ran it at C7. The two listings are identical. The 73 / 7 split of the server-side
   tracebacks DEC87 states belongs to no gate. It was read from the pinned short transcript before C6 and
   matched.

6. **OBSERVED, NOT ACTED ON.** The generator's CROSS-CHECK lines "re-key BASE to TIP equals the subtracted set"
   read `False` as a set and in order. This is expected rather than a failure, because 21 paths differ between
   BASE and TIP and a line-keyed tuple moves when its file changes. The ordered reading is the scope-key
   recovery, and it is 2183 of 2183. The owner check over DELETE, which no gate asks for, read 1907 / 276 / 0.

7. **THE STATE-FILE ORDER.** C0a and C0b land before C1 updates `.agent/plan.md`, as the Bundle orders and as
   item 23 of §3 names C1 the first substantive commit.

8. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle. Nothing under `packages/`, `apps/`,
   `tests/`, `docs/` or `scripts/` was touched. No landed record was rewritten and no `.py` file was created
   under `.agent/`. Of the reviewer's `.remedy-wt/r87/`, only the three pinned transcripts were opened, plus one
   directory listing while their digests were checked. All of this worker's scratch is under `.remedy-wt/r87w/`,
   uncommitted.

## Next

The reviewer re-runs the gates and issues the round 87 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`: the `UUID(...)` parses under `packages/` that feed the job store, a SPLIT
production round with mutation red-proofs; then the flip's dry run again; then the flip as a series of commits
under the cap unless the operator answers Q1 otherwise; then the classic store and the closure sequence.
