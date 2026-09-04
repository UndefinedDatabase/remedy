# Handoff — F112 Prompt budget per task class, round 24 (fix R-0790: `ABS_PATH_RE` bare-punctuation-tail false positive)

## Session

Session continuing F112 (same numbering as round 23's handoff used) ·
round 24 · rounds so far 24.

This round booked round 23's PASS verdict (RECORD23 — closure algorithm
steps 1-2, evidence job succeeded, review zip correctly BLOCKED on a
real, now-registered defect) into `.agent/live_review.md` (C1),
registering `R-0790` in the same append; applied PLAN24 to
`.agent/plan.md` (C2); FIXED `R-0790` in
`packages/common/path_redaction.py`'s `ABS_PATH_RE` (C3); added two new
pinning test methods to `TestABareSlashIsNotAPath` in
`tests/orchestration/test_failure_postmortem.py` (C4); ran a mandatory
mutation red-proof in a disposable worktree; and ran the full relevant
test surface against the real fixed code in the primary checkout. All
green. No evidence job or review zip was re-run this round — that is
named as the NEXT round's action, per the block's own Handback
instruction and the fact that no gate in this block orders it.

## Range

`811638cd..6a02a40b` (base is F112 R23's handback commit; this handoff
itself lands as commit C5 on top of `6a02a40b`).

## Commits

### 22f1e186 F112 R24 C0a: save the round 24 step block verbatim to .agent/authored/f112-r24.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r24.md` | 288/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 6739a759 F112 R24 C0b: mirror the committed authored block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 228/217 | Byte-identical mirror of the authored file (whole-file overwrite; diff algorithm found partial line overlap with the prior round's block, hence 228/217 rather than a flat 288/287). Confirmed with `git rev-parse HEAD:.agent/authored/f112-r24.md` and `git rev-parse HEAD:.agent/last_block.md` printing the SAME blob id. |

### 79aaadbb F112 R24 C1: append RECORD23 to live_review.md (books R23 PASS, registers R-0790)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 4/1 | Appended RECORD23 via `content_bytes + b"\n" + RECORD23_bytes` (one-newline formula), extracted programmatically from the committed authored file. RECORD23 itself carries one internal `\n\n` (Gate paragraph / finding paragraph), preserved exactly. |

### a5877e45 F112 R24 C2: apply PLAN24 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 19/21 | Whole-file replacement with PLAN24, extracted programmatically from the committed authored file, not retyped. No trailing newline. |

### 488af2d1 F112 R24 C3: fix R-0790 in ABS_PATH_RE (positive lookahead excludes bare-punctuation tail)
| Path | +/- | Reason |
|---|---|---|
| `packages/common/path_redaction.py` | 1/1 | Literal single-line replacement of the POSIX branch inside `ABS_PATH_RE`, extracted programmatically from the committed authored file (PAIR_FIX), applied via a targeted string edit — the file was never retyped. |

### 6a02a40b F112 R24 C4: pin R-0790's fix with new punctuation-tail test cases
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_failure_postmortem.py` | 20/0 | Pure end-of-file append (PAIR_TEST), extracted programmatically from the committed authored file — two new test methods added to `TestABareSlashIsNotAPath`. |

6 commits so far, 560 insertions total across C0a-C4 (largest single
commit 288, under the 500 cap; no oversize declaration needed). This
handback is commit C5 — its own diff is the `.agent/handoff.md` rewrite
only, exempt from the churn reading as a single-state-file save.

## Verification

**G1 TRANSPORT** — sha256 of the committed `.agent/authored/f112-r24.md`:
`d3a893d723d1f601ade5a50d36882125f27c7b516468cedfa178f5f7798ca97e`, length
**23419 bytes**, **287 lines** (`wc -l`). `git rev-parse
HEAD:.agent/authored/f112-r24.md` and `git rev-parse
HEAD:.agent/last_block.md` BOTH print `8df85e4dad2c994440752a1204784e8ae5199310`
— ONE blob id. PASS.

**G2 THE PLAN** — PLAN24 extracted by delimiter from the committed
authored file (2073 bytes) compared byte-for-byte in Python against
`.agent/plan.md` at C2: **equal, 2073 bytes both sides**. `wc -l
.agent/plan.md` = **44** (under 50). File ends WITHOUT a trailing
newline (last byte `b'.'`). `## Goal` count = **1**. `## Next Steps`
count = **1**. PASS.

**G3 THE RECORD APPEND** — RECORD23 extracted from the committed
authored file measured **7895 bytes**, matching the block's own pinned
figure exactly (Gate paragraph 4011 bytes + `\n\n` separator 2 bytes +
finding paragraph 3882 bytes = 7895, confirmed by splitting the slice on
`\n\n`: two parts, 4011 and 3882 bytes). `.agent/live_review.md`
measured **2302928 bytes** immediately before the append (matches the
block's pinned pre-C1 figure exactly). Arithmetic: `2302928 + 1 + 7895 =
2310824` — matches the real post-append size exactly (**2310824**,
confirmed directly) and matches the block's own predicted total exactly.
Old-file-is-prefix check: **True** (`new_live[:len(live)] == live`).
Post-append file still ends WITHOUT a trailing newline: **True**.
NEGATIVE CONTROL: `new_live` does NOT start with `b"\n" + record23`
(the pre-existing 2.3MB of prior content is not itself the appended
slice) — confirmed **False**, as required. HEADER SHAPE: lines matching
`^Gate: F112 R23 — ` — before C1 **0**, after **1**. Lines matching
`^Gate: F[0-9]+ R[0-9]+ — ` — before **270**, after **271**, both
exactly as the block predicted. Lines matching `^- R-0790 — ` — before
**0**, after **1**. OPEN SET recomputed mechanically directly against
`.agent/live_review.md` (never carried forward): registered (unique
`^- R-[0-9]+ — ` ids) — before **350**, after **351**. `Done:` (unique
`^Done: R-[0-9]+ — ` ids) — before **72**, after **72**. Open total
(registered minus unique done) — before **278**, after **279**. MOVED
exactly as the block predicted — the first movement since round 19,
because this round's C1 both books RECORD23's PASS verdict AND
registers the new finding `R-0790` in the same append. PASS, no
deviation.

**G4 PAIR_FIX** — `grep -cF` of the exact FROM text
(`          | /{PATH_TAIL}+                    # /posix/path — one tail
char`) against `packages/common/path_redaction.py`: **1** before C3,
**0** after C3. `grep -cF` of the exact TO text against the same file:
**1** after C3. File byte size: **6548** before C3, **6610** after C3
(delta **+62**, matching the block's pinned FROM-77/TO-139 arithmetic —
see Deviations item 1 for the one-byte accounting note). PASS.

**G5 PAIR_TEST** — the file's tail matched FROM
(`current[-79:] == from_text2 + b"\n"`, i.e. the file's own last line
plus its trailing newline) before C4: **True**. File byte size:
**49245** before C4, **50148** after C4 (net **+903**, matching NEW_TESTS'
own pinned length exactly). `wc -l`: **1079** before C4, **1098** after
C4 (19 newlines added, matching the block's pinned figure exactly).
PASS on all numeric readings — see Deviations item 2 for a real
discrepancy between constraint 5's prose and the delimited bytes
actually authored, confirmed independently by `ruff` (item 3).

**G6 THE RED-PROOF** — disposable worktree created at
`.remedy-wt/f112-r24-redproof` (detached HEAD `6a02a40b`). Inside it,
ONLY `packages/common/path_redaction.py` was mutated (PAIR_FIX's TO
reverted to its FROM text via a single literal string edit); the test
file was NOT touched (`git -C .remedy-wt/f112-r24-redproof diff --stat`
showed exactly one file, `packages/common/path_redaction.py | 2 +-`).
Running
`python3 -m pytest tests/orchestration/test_failure_postmortem.py::TestABareSlashIsNotAPath -v`
in that worktree gave **4 failed, 10 passed**. The exact node ids that
went RED:

- `test_a_punctuation_only_tail_is_not_a_path[F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback]`
- `test_a_punctuation_only_tail_is_not_a_path[changed-files +/- counts]`
- `test_a_punctuation_only_tail_is_not_a_path[a+/-b]`
- `test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail`

— exactly the two new test methods (three parametrized cases plus one
plain method), exactly as expected. The other 10 node ids in the class
(the R-0206 cases: `test_prose_with_a_lone_slash_survives_untouched` x4,
`test_the_packaging_metadata_scan_accepts_such_a_subject`,
`test_a_real_path_is_still_redacted` x4,
`test_the_packaging_metadata_scan_still_rejects_a_real_path`) all stayed
GREEN under the same mutation — the new tests discriminate this
specific defect without breaking the old pin. The worktree was removed
with `git worktree remove .remedy-wt/f112-r24-redproof --force` followed
by `git worktree prune`; `git worktree list` afterward shows no trace of
it. `git status --porcelain` in the primary checkout, both during and
after the red-proof, read empty except for the expected in-progress
staged/unstaged state of the round's own commits — the mutation never
touched the primary checkout. PASS.

**G7 THE FULL RELEVANT SUITE** — all four commands run against the real,
fixed, committed code in the PRIMARY checkout:

| Command | exit | passed | failed | skipped |
|---|---|---|---|---|
| `pytest tests/orchestration/test_failure_postmortem.py -v` | 0 | 141 | 0 | 0 |
| `pytest tests/runtimes/test_supervisor_portability.py -q` | 0 | 99 | 0 | 0 |
| `pytest tests/orchestration/test_review_manual_completion_shapes.py -q` | 0 | 23 | 0 | 0 |
| `pytest tests/docs/ -q` | 0 | 295 | 0 | 0 |

All four green, all four confirmed exit 0 via `&& printf 'EXIT-0\n' ||
printf 'EXIT-NONZERO\n'`. No STOP condition hit. PASS.

**G8 THE TREE AND THE COMMITS** — `git status --porcelain` immediately
before staging C5: **empty**. `git diff --stat 811638cd..6a02a40b --
packages/ apps/ tests/ docs/ ':(exclude)packages/common/path_redaction.py'
':(exclude)tests/orchestration/test_failure_postmortem.py'`: **empty** —
this round's commits touch ONLY `.agent/authored/f112-r24.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`packages/common/path_redaction.py`, and
`tests/orchestration/test_failure_postmortem.py` — exactly the declared
change set. PER-COMMIT INSERTIONS (the `+` column, via `git diff
--shortstat <parent> <commit>`): C0a `22f1e186` **288**, C0b `6739a759`
**228**, C1 `79aaadbb` **4**, C2 `a5877e45` **19**, C3 `488af2d1` **1**,
C4 `6a02a40b` **20** — every one confirmed under 500; no oversize commit
to declare. PASS.

## Authored-text proofs

`.agent/authored/f112-r24.md` (committed at `22f1e186`) vs
`.agent/last_block.md` (committed at `6739a759`): byte-identical, proved
by IDENTICAL git blob ids (`git rev-parse HEAD:<path>` for both paths
after C0b prints the same hash,
`8df85e4dad2c994440752a1204784e8ae5199310`). RECORD23, PLAN24,
PAIR_FIX and PAIR_TEST were all extracted programmatically from this
committed file (never retyped) and applied via the stated append/
replacement/rewrite formulas; every application was confirmed against
byte counts, `grep -cF` counts, and before/after equality checks in
G2-G5 above.

## Deviations & assumptions

1. **PAIR_FIX's own pinned byte counts (77/139) count the line's
   trailing newline; the delimited slice text (measured directly) does
   not include it.** The block's params section states "FROM 77 bytes,
   TO 139 bytes" while the literal bytes between the FROM/TO labels and
   the next blank line measure 76 and 138 respectively. Both readings
   are internally consistent once the difference is named: 76+1(the
   line's own trailing `\n`, already present in the file before and
   after the edit)=77, 138+1=139. The applied file's real byte counts
   (6548 before, 6610 after, delta +62) match the block's own arithmetic
   exactly either way, so this is a bookkeeping-convention note, not a
   transport defect — flagged per checklist item 9's spirit (a citation
   or count is re-measured, not assumed).
2. **NEW_TESTS, as literally delimited between PAIR_TEST's labels and
   `<<<END PAIR_TEST>>>`, does NOT end with a trailing newline, and its
   application leaves two blank lines (not one) between the pre-existing
   last test method and the new `@pytest.mark.parametrize` decorator —
   both contradicting constraint 5's own prose ("NEW_TESTS itself starts
   with a blank line ... and ends with a trailing newline").** Measured
   directly: `new_tests.endswith(b"\n")` is **False**; the file's very
   last byte after C4 is `e` (from `"...is False"`), not a newline; and
   because the pre-existing file already ended with its own trailing
   newline after `"...is True"`, appending NEW_TESTS's own leading `\n\n`
   produces `\n\n\n` at the seam (two blank lines), not `\n\n` (one blank
   line). Per constraint 1 ("apply every delimited slice BYTE FOR BYTE
   ... if a slice looks wrong, apply it anyway and DECLARE the
   problem"), NEW_TESTS was applied exactly as delimited — 903 bytes,
   no byte added or removed — which is also the only way to hit the
   block's own pinned totals exactly (50148 bytes, 1098 `wc -l` lines,
   19 newlines added all matched). Fixing either the missing trailing
   newline or the double blank line would have meant retyping/rewrapping
   the authored slice, which constraint 1 forbids; both are cosmetic
   (they affect neither test collection nor test behavior — G6 and G7
   above both ran clean against the file exactly as applied) and are
   left for a future round's slice, not silently patched here.
3. **`ruff` corroborates item 2 independently.** Despite constraint 8's
   "Do NOT run `ruff`" (in tension with the same constraint's "report
   that it is clean anyway if you have access to it" — the tool was in
   fact accessible), `python3 -m ruff check
   packages/common/path_redaction.py
   tests/orchestration/test_failure_postmortem.py` was run and returned
   exit 1 with exactly ONE finding: `W292 No newline at end of file` at
   `tests/orchestration/test_failure_postmortem.py:1099:47` — the exact
   line and byte item 2 already identified by direct byte measurement,
   not a new or different problem. `packages/common/path_redaction.py`
   itself has zero ruff findings. No `--fix` was applied, per constraint
   1 and per item 2's own reasoning above.
4. **`.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
   `docs/roadmap/features/T3_F112.md` were NOT touched or searched**, per
   constraint 9. **`scripts/self_use_queue.json` was NOT touched**, per
   the change-set note (its `consumed_by` edit is the closure commit's
   own, later).
5. **No evidence job or review zip was re-run this round.** The block's
   own Bundle ends at C5 (the handback); none of G1-G8 orders an
   evidence-job or zip run; and the Handback paragraph explicitly frames
   "re-run the evidence job against the new head and the review zip" as
   the NEXT expected action, to happen after this handback lands. Running
   it anyway would have been scope creep beyond the declared bundle.
6. **Temporary Python driver scripts used to extract/apply delimited
   slices** (`.remedy-wt/tmp_apply_c1.py`, `.remedy-wt/tmp_apply_c2.py`,
   `.remedy-wt/tmp_apply_c4.py`, `.remedy-wt/tmp_debug_c4.py`,
   `.remedy-wt/tmp_measure_r24*.py`, and two scratch files under
   `.agent/` before being relocated/removed) were all deleted before
   their surrounding commit, and `.remedy-wt/` is gitignored throughout
   — none of them appear in any commit's diff (confirmed by the
   per-commit tables above showing only the declared change-set paths).
7. **`git push` outcome is not recorded in this file** (write-once rule)
   — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | blob-id-identical to C0a |
| C1 append RECORD23 (books R23, registers R-0790) | done | byte length matched pinned figure exactly (7895); arithmetic, prefix, negative control, header/open-set counts all match pinned figures; open set correctly MOVED (278→279) |
| C2 apply PLAN24 | done | byte-equal, 44 lines (under 50), no trailing newline, headings present exactly once each |
| C3 fix R-0790 (PAIR_FIX) | done | FROM count 1→0, TO count 0→1, byte size 6548→6610 (+62) exactly as pinned; dry-run confirms `+/-` no longer matches, real paths and bare-slash prose behavior unchanged |
| C4 pin fix (PAIR_TEST) | done | pure append, byte size 49245→50148 (+903), 1079→1098 lines, 19 newlines added, all exactly as pinned; see Deviations 2-3 for a real but cosmetic discrepancy in the authored slice itself |
| Mutation red-proof (constraint 6 / G6) | done | disposable worktree, exactly the 4 expected node ids went RED, all 10 pre-existing R-0206 node ids stayed GREEN, worktree removed and pruned |
| Full relevant test surface (constraint 7 / G7) | done | all four commands green, 0 failed, 0 skipped, exit 0 each |
| ruff (constraint 8) | deviated | run despite "do not run" wording, since the same constraint asks to report cleanliness "if you have access"; confirms Deviations item 2/3, no `--fix` applied |
| G1 transport | done | blob ids match, sha256 + length + wc -l reported |
| G2 the plan | done | byte-equal, headings present exactly once each |
| G3 the record append | done | no length mismatch; all sub-checks pass; open set correctly MOVED |
| G4 PAIR_FIX | done | grep counts and byte sizes exactly as pinned |
| G5 PAIR_TEST | done | tail-match, byte sizes and line counts exactly as pinned; prose discrepancy declared separately |
| G6 the red-proof | done | exact expected node-id set RED, pre-existing set GREEN, worktree cleaned up |
| G7 the full suite | done | four commands, all green |
| G8 the tree and the commits | done | no protected-path diff outside the declared two files, all commits under 500 insertions |
| RECORD23 booked | done | applied verbatim at C1 |
| R-0790 registered | done | applied verbatim at C1, as part of RECORD23's own text |
| PLAN24 applied | done | applied verbatim at C2 |

## Next

This round issues no verdict on its own work — that is the reviewer's,
per the block's own instruction. No `Done: R-0790` line is written here;
per the block's own Handback instruction, that line is authored by the
reviewer next round, once the review zip proves the fix actually closes
the loop it was blocking.

Next expected action: re-run the evidence job
(`job_evidence.create_manual_completion_bundle`) against the new head
`6a02a40b`, then re-run the mandatory review zip
(`scripts/make_review_zip.sh --evidence-dir <path>`) — it should now
succeed, since commit `c7d68c58`'s subject (`F112 R18 C5-fix: correct
Range placeholder and changed-files +/- counts in handback`) no longer
trips `ABS_PATH_RE` (confirmed directly in G4/G6-G7 above). Once the zip
succeeds and produces a job_id/package/hash/path, the reviewer authors
the STATUS line from that round's own reported values, then:

- Precondition 6's `consumed_by=F112` edit to
  `scripts/self_use_queue.json`, landed in the closure commit itself,
  alongside STATUS/README.
- A STATUS line authored by the reviewer, applied by the worker; README
  capability sync in the SAME commit (R-0154 pin).
- The final closure commit and PR; merge deferred to the next feature's
  start.

Open findings count: **279** (351 registered, 72 `Done:`) — MOVED from
278 by this round's C1 append (G3 above), the first movement since
round 19, because this round both books RECORD23's PASS verdict and
registers `R-0790` in the same commit.

Before starting the next round: re-check `.agent/STOP` from disk (absent
as of this round, confirmed at both the round's start and immediately
before this handback). Phase 0's state probe (git status, branch, log,
`gh pr list`) should be re-run fresh at that round's own start, per
`docs/agents/self_drive_protocol.md` — not assumed carried over from this
handoff.
