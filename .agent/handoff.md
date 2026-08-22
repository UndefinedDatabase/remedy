# F021 R40 handback — closure round one, the evidence bundle and the review zip

Fortschritt: ~100 % (T001, T002 und T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidence-Job und Review-Zip in dieser
             Runde; danach bleiben nur STATUS-Zeile, README-Sync und der Pull
             Request) — Schaetzung

## Range
Review of 68df0d8992f276eac1e032f3686cb14d720b3a08..HEAD — ROUND BASE `68df0d89`
resolved with `git rev-parse`, branch `feature/f021-live-activity-feed`. Open
findings 227 by `planner_reviewer_prompt.md` §3 item 10 — canonical
`^- R-\d+ — ` 228 minus `^Done: R-` 1 — 227 at the base and 227 at C2. NO id
minted, NOTHING resolved; the next free id is R-0666, as it was at the start.
NO BLOCKER: no gate went red and `PACKAGE_STATUS` is `READY_FOR_REVIEW`.

## Closure values
| Field | Value |
|---|---|
| Evidence job | f021-closure |
| package | remedy-review-20260823-005026-READY_FOR_REVIEW.zip |
| SHA-256 | be70b65dd4a397ac7697a3c37b2f5cfb1a52197c9434cde67dec4a0a502e3dd8 |
| accepted HEAD | a0a883f7bf47e92bd3c084d127bf56f5f4feaad2 |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `f9a649fd` | done | |
| C0b `9f5eb4d8` | done | |
| C1 `b268188f` | done | |
| C2 `a0a883f7` | done | the ACCEPTED HEAD both artefacts record |
| C3 (this file) | done | its own SHA and insertions are unnameable from inside it |

## Commits

### f9a649fd chore(agent): save the F021 R40 closure step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r40.md | +420/-0 | the block copied byte for byte (C0a) |

### 9f5eb4d8 chore(agent): mirror the R40 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +377/-138 | written FROM the committed C0a blob (C0b) |

### b268188f docs(state): point the F021 plan at R40, closure round one
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-23 | PLANF021R40 whole-file write (C1) |

### a0a883f7 docs(review): record the R39 PASS and the accepted head for closure
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | RECORD40 appended, ONE blank line at the join (C2) |

### C3 docs(state): hand back F021 R40 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to the next round | the handback itself (C3) |

Every `+/-` cell above is the `git diff --numstat` reading and equals the number
the G7 line reports, compared cell by cell (block constraint 2, §3 item 28).

## External actions
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` exit 0,
output `[]`. NO `gh pr create`, NO `gh pr merge`, NO worktree added or removed.
`git push -u origin feature/f021-live-activity-feed` after C2 (`68df0d89..a0a883f7`)
and again after C3. `bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f021_closure_evidence/remedy-job-evidence-f021-closure` exit 0.

## Verification — one line per gate
G1 `.agent/STOP` ABSENT before C0a and again before C3; branch `feature/f021-live-activity-feed` at both; `git status --porcelain` 0 lines after EACH of C0a, C0b, C1 and C2, 0 again immediately before the evidence run, 0 immediately before the zip build and 0 after it. ROUND BASE resolved to `68df0d8992f276eac1e032f3686cb14d720b3a08`. C3's own reading is left to the next session (§3 item 31).
G2 sha256 `458138df2c127076752cf655d7f55015f5b4f1869fe4b131650cb1456df667be`, 29048 bytes, 420 lines — EQUAL over the bytes I read, `.remedy-wt/f021-r40.md`, `.agent/authored/f021-r40.md` at C0a and `.agent/last_block.md` at C0b, the last written FROM the committed C0a blob.
G3 My extractor read the COMMITTED C0a blob by marker line and printed 3 whole texts beside 6 marker lines: PLANF021R40 `d42548a7a582edd27e6fa0065f59c63a897505c86392bab473a358953dc116d7` 2208 bytes 39 lines; RECORD40 `c75bfbb73202062440a246376eb29b5118b5d3e598a3f6ac04d04b5dba0df62e` 4466 bytes 1 line; EVIDENCESCRIPT `369a3cc57e33bd51a47997dcd004df3260e2fad4668a53b67e9ff1643c3b70ca` 5712 bytes 139 lines. Summed slice CONTENT 179, so TOTAL 420 against DECISION F085 D6's 490 and PROSE 241 against D5's 400 — both equal to constraint 11.
G4 `cmp .agent/plan.md` vs PLANF021R40 plus one terminating newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1 (`cmp: EOF on .remedy-wt/r40_plan_bare after byte 2208, in line 39`); 2209 bytes, last byte `0xa`; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 39, under AGENTS.md's 50, untrimmed.
G5 THE APPEND at C2 under TWO readers, both ACCEPTING the true file: (a) the `68df0d89` blob is a byte-exact PREFIX and the remainder is EXACTLY one newline plus RECORD40 plus one newline, 4468 bytes; (b) N counted BY MY SCRIPT is 1 and the last 1 blank-line-separated unit equals RECORD40's 1 paragraph. The FIRST appended paragraph opens with the bytes `Gate: R40 — the R39 `. NEGATIVE CONTROL: flipping offset 0 of that first paragraph, `G` -> `Z`, at equal file length, is REJECTED by reader (a) AND by reader (b).
G6 base then C2, every count anchored: canonical `^- R-\d+ — ` 228 then 228, ALL DISTINCT at both, maximum R-0665 at both — this round minted nothing; loose `^- R-` 229 then 229; `^Done: R-` 1 then 1; `^Landed: ` 0 then 0; `^Gate: R` 38 then 39, DISTINCT at both; `^Gate: R40` 0 then 1; `^Recurrence: ` 16 then 16. OPEN = canonical minus `^Done: R-` = 227 at base and 227 at C2.
G7 `git diff --name-only 68df0d89..HEAD` I COUNT FOUR paths at C2 — `.agent/authored/f021-r40.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — and FIVE at C3, those plus `.agent/handoff.md`; BOTH set differences against the `Change:` list are EMPTY at BOTH points; `docs/roadmap/STATUS.md` and `README.md` are BOTH ABSENT. 4 commits before C3 — as many as `Bundle:` names — every one single-parent; `git show --numstat` (no `--` before the SHA) and `git diff --numstat` agree cell by cell on all four; insertions 420, 377, 19 and 2, each under 500, C3's own left to the next round. Marker sweep LINE-ANCHORED 0 for each of `^<<<SLICE ` and `^<<<END ` over `.agent/plan.md` and `.agent/live_review.md`. `git ls-files .remedy-wt` reads 0. Reflog BY OPERATION over THIS ROUND's four rows: every one `commit`, with `amend`, `rebase` and `cherry` 0 each in that field; no total is asserted over the whole reflog. `gh pr list --state open` printed `[]` verbatim.
G8 CANARY `python3 -m pytest tests/cli/test_golden_path.py -q -rf` REAL exit 0, `42 passed in 20.83s` — 42, EQUAL to the block's base reading. Serial, in the PRIMARY checkout, no other pytest process alive. No docs gate owed: no `docs/` path is in the change set.
G9 EVIDENCE JOB at C2, tree 0 lines before it and after `git push`. `.remedy-wt/r40_evidence.py` sha256 `369a3cc57e33bd51a47997dcd004df3260e2fad4668a53b67e9ff1643c3b70ca` EQUALS the slice's. `python3 .remedy-wt/r40_evidence.py` REAL exit 0, stderr 0 bytes. Bundle dir did NOT pre-exist (read BEFORE the run) and holds 27 entries after. Per-run lines: `vr-0001 selected 9 node_ids 9 deselected 0 files 1 dur 1.29`, `vr-0002 selected 67 node_ids 67 deselected 0 files 1 dur 0.26`, `vr-0003 selected 66 node_ids 66 deselected 0 files 1 dur 0.22`, `vr-0004 selected 51 node_ids 51 deselected 0 files 1 dur 0.21`. `OUTPUT_HASH` True for each of vr-0001..vr-0004, re-derived from `verification_tests.json` on disk. `SCAN rejected strings: 0 []` and `SCAN red control: a local absolute path` — NOT `None`. Producer summary: authority_count 39, commit_count 248, head_commit `a0a883f7bf47e92bd3c084d127bf56f5f4feaad2`, job_id `f021-closure`, manual_completion true, operator_attested_tasks `["T001", "T002", "T003"]`, partition T001 13 / T002 13 / T003 13, total_passed 193, verdict `PASS_WITH_RISKS`. head_commit EQUALS C2's SHA.
G10 INTEGRITY CHECK at C2 via `from packages.orchestration.integrity_gate import run_integrity_checks` then `run_integrity_checks()`: `passed` True, `fail_count` 0, FIVE checks — handler_import pass, live_review_verdict pass, plan_consistency pass, relevant_untracked pass, high_blockers_open pass. The high-blocker precondition's blindness is the already-registered R-0648.
G11 REVIEW ZIP at C2, tree 0 lines immediately before the build, branch already pushed, run from the repository root and NOT through a pipe. REAL exit code 0 — and exit 0 is NOT the reading: `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`. Package `remedy-review-20260823-005026-READY_FOR_REVIEW.zip`, script `final_sha256` `be70b65dd4a397ac7697a3c37b2f5cfb1a52197c9434cde67dec4a0a502e3dd8`, and a FRESH sha256 over the file on disk RECOMPUTES the same value. `member_count` 13921 EQUALS `zipfile.namelist()` 13921. From `.review_zip_manifest.json` INSIDE the package: `committed_review_subject.base_commit` `4548995de3e46dc5304d3584dc249262d54edac9` (full 40), `head_commit` `a0a883f7bf47e92bd3c084d127bf56f5f4feaad2` EQUALS C2, `base_is_ancestor` true, `commit_count` 248, `file_count` 99, `packaged_evidence_job_id` `f021-closure`, `ready_gate_matrix.ok` true over `blocking_reasons` `[]`, `review_subject_evidence_alignment.verdict` `PASS` with `issues` 0 and `hash_mismatches` 0.
G12 This handback carries every mandated section, a row per `Bundle:` item, the round base SHA, one line per gate, both points of every multi-point reading, the `## Closure values` table and the verbatim `Fortschritt:` block. `wc -l` is declared in Deviations item 5.

## Authored-text proofs
All three texts were extracted BY MARKER LINE from the COMMITTED C0a blob
`f9a649fd:.agent/authored/f021-r40.md`, never retyped. `plan.md`: `cmp` exit 0
against PLANF021R40 plus one terminating newline, exit 1 against the bare slice.
`live_review.md`: the committed `68df0d89` blob is a byte-exact PREFIX of the
committed C2 blob and the remainder is EXACTLY one newline plus RECORD40 plus one
terminator; no landed paragraph, `Gate:` or `Recurrence:` entry was edited.
`.remedy-wt/r40_evidence.py`: sha256 EQUAL to the EVIDENCESCRIPT slice, and it is
NOT committed — `git ls-files .remedy-wt` reads 0.

## Deviations & assumptions
1. No departure from the ordered commit sequence: exactly C0a, C0b, C1, C2, C3 —
   none extra, dropped or reordered. Nothing under `apps/`, `packages/`, `docs/`
   or `tests/` was touched; `docs/roadmap/STATUS.md` and `README.md` are
   untouched and belong to the next round. No formatter or linter ran, `npm run
   lint` was NOT run, no PR was created or merged, NO worktree was created, and
   two pytest processes never ran at once. No artefact build went through a pipe:
   each ran under a wrapper that captured the REAL exit code.
2. NEWLINE CONVENTION, stated because the two slices differ: `.agent/plan.md` is
   PLANF021R40 plus ONE terminating newline, exactly as G4 orders, whereas
   `.remedy-wt/r40_evidence.py` is the EVIDENCESCRIPT slice with NO added byte,
   because G9 orders its sha256 to EQUAL the slice's. A first write of that file
   with a terminating newline hashed `cab95e54…`; it was overwritten with the
   exact slice bytes BEFORE the script was ever executed.
3. READER (b) DEFINITION, stated so it is auditable: a unit is a blank-line
   separated run of lines with its own trailing newlines stripped. Under it the
   true file is ACCEPTED and the equal-length one-byte flip in the FIRST appended
   paragraph is REJECTED, so the reader is not vacuous.
4. OBSERVATIONS, no id spent — closure-round findings are CANDIDATES per the
   closure protocol, and the next session's first reviewed round registers them.
   (a) `review_subject_evidence_alignment.dirty_file_count_total` reads 1 while
   `dirty_source_test_files` and `uncovered_source_test_files` are both empty and
   `issues` is 0; the verdict is PASS. (b) `gate_verdicts.commit_execution_gate`
   reads `NEEDS_HUMAN_APPROVAL` while `ready_gate_matrix.ok` is true over empty
   blocking reasons. (c) 10646 of the package's 13921 members are `.remedy-wt/`
   scratch — the already-registered R-0403, NOT a new condition.
5. DECISION D15, size: this handback measures 139 lines against the ≤60-line
   tier. Mandated cause: five commit tables, the item-status table, the
   `## Closure values` table G12 requires, and twelve gate lines that must carry
   BOTH points of every two-point reading (G6's base-then-C2 ledger, G7's C2-then
   -C3 path sets) plus the full producer summary and the full zip manifest field
   set. No section is dropped and no transcript is restated here.
6. No `.agent/context.md` or `.agent/decisions.md` update is owed: scope,
   assumptions and constraints are unchanged and no new technical decision was
   made — this round produces artefacts and records R39's verdict.

## Next
CLOSURE ROUND TWO: the reviewer-authored STATUS `[x]` line and the README
capability sync in ONE commit (R-0154), then the pull request. NO pull request
exists yet and none was created here. That round's STATUS line is authored from
the `## Closure values` table above and from nothing else. The PR is NOT merged
in this session; it merges at the next feature's start via the Open PR Gate. The
next session's FIRST action is Phase 1 rule 1 of
`docs/agents/self_drive_protocol.md` — re-reading `.agent/STOP` from disk —
BEFORE rule 2. Owed to the next round, because C3 cannot state them about itself:
C3's SHA, C3's insertion count and the `git status --porcelain` reading after C3.
