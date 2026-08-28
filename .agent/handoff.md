# Handback — F032 Evidence Triple — Round R18 (closure part one)

## Session

SESSION 4 of feature F032 · round R18 · rounds so far 18
(R1–R5 session 1, R6–R9 session 2, R10–R14 session 3, R15–R18 this one.)

## Range

Review of `12f28a42..c3cf408f`.

## State

- Branch: `feature/f032-evidence-triple`
- Base of this round: `12f28a424be48fc41602383e8844f694e408553d` (the R17 handback),
  measured with `git rev-parse HEAD` and equal to the base the block names.
- Merge base with `main`: `a399a3304f9d962cd920c251488c40c486b35fdc`
- Commits, in order: C0a `c89b867b`, C0b `b8d2e0cc`, C1 `c084172b`,
  C2 `02164346`, C3 `c3cf408f`, C4 the handoff.
- ACCEPTED HEAD: `c3cf408f537de393bb156e45feae46d5de9f63da` (C3).
- No pull request was created, no STATUS line was flipped, no README was
  touched and nothing was merged.

## Commits

### c89b867b docs(agent): save the R18 closure block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f032-r18.md | +452 / -0 | C0a, the block saved verbatim |

### b8d2e0cc docs(agent): mirror the R18 closure block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +332 / -287 | C0b, the same bytes mirrored |

### c084172b docs(agent): point the plan at the R18 closure round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18 / -20 | C1, slice PLANF032R18 applied whole |

### 02164346 docs(agent): book the R17 gate verdict, register R-0714 and the slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | C2, slices LEDGER18 then FINDING714 appended in order |
| .agent/prose_slips.md | +10 / -0 | C2, slice SLIP18 appended |

### c3cf408f docs(roadmap): record the F032 built state on disk
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F032.md | +40 / -0 | C3, slice BUILTSTATE appended; closure precondition 4; the ACCEPTED HEAD |

### C4 the handoff (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | not tabled | a handoff cannot table the commit that writes it |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  (Open PR Gate clear; no PR was created this round).
- `bash scripts/make_review_zip.sh --evidence-dir …/remedy-job-evidence-f032-closure`
  run TWICE from the clean tree at C3 — see Deviations 1. Both produced
  `READY_FOR_REVIEW`; the second is the package of record.
- `git push -u origin feature/f032-evidence-triple` is ordered by the block's
  constraint 6 and is executed immediately AFTER this commit. Its outcome
  cannot be recorded in the file it precedes and is reported in the round
  report instead.
- No worktree was added or removed; no merge; no force-push; no history rewrite.

## Verification

One line per gate, every number measured this round.

- **G1 HYGIENE, BASE, SENTINEL** — `git rev-parse HEAD` before C0a =
  `12f28a424be48fc41602383e8844f694e408553d`, equal in full to the base the
  block names; `git rev-parse --abbrev-ref HEAD` = `feature/f032-evidence-triple`;
  `git status --porcelain | wc -l` = `0` after each of C0a, C0b, C1, C2 and C3;
  `ls -la .agent/STOP` before C0a AND again before C4 both printed
  `ls: cannot access '.agent/STOP': No such file or directory` — the sentinel
  does not exist at either reading.
- **G2 TRANSPORT** — `sha256sum` equal across all three disk copies at
  `f2a2f0895d9032f7fd7441ca4f4bcc3253113b3f0664a501917c1451b0c2ec37`: the
  reviewer's gitignored scratch original `.remedy-wt/f032-r18.md`,
  `.agent/authored/f032-r18.md` at C0a and `.agent/last_block.md` at C0b; the
  two committed paths are ONE git blob `84d9a8137e5084055430557908761dc8a9d7e870`.
  No claim is made about any prompt's bytes.
- **G3 EXTRACTION AND CAPS** (measured on the committed C0a blob) — 5 slice
  regions found: PLANF032R18 42 content lines, LEDGER18 1, FINDING714 1,
  SLIP18 9, BUILTSTATE 39; content total 92; block TOTAL 452 lines; PROSE =
  452 − 92 = 360. PROSE < 400 `True`, TOTAL < 490 `True`.
- **G4 THE PLAN, at C1** — `.agent/plan.md` byte-equal to slice PLANF032R18
  extracted from the committed C0a blob → `True`; NEGATIVE CONTROL with the
  slice's trailing newline removed → `False`; `wc -l` = 42 (< 50); `^## Goal$`
  = 1; `^## Next Steps$` = 1.
- **G5 THE APPENDS, at C2 and C3** — `.agent/live_review.md` reader (a) `True`
  at 1112545 + 1 + 5207 + 1 + 4096 = 1121850 with the pre-commit blob a byte
  PREFIX `True`, reader (b) N = 2 in-order `True`; `.agent/prose_slips.md`
  reader (a) `True` at 2933 + 1 + 616 = 3550, PREFIX `True`, reader (b) N = 1
  `True`; `docs/roadmap/features/T5_F032.md` reader (a) `True` at 11728 + 1 +
  2291 = 14020, PREFIX `True`, reader (b) N = 6 `True`. NEGATIVE CONTROL for
  each — one byte flipped IN MEMORY inside the FIRST appended paragraph, at a
  BYTE offset proved to lie inside the slice — BOTH readers reject in all three
  cases (see Deviation 3 for the first, faulty control and its repair).
  Ledger counters, before C2 → after C2: `^Gate: F\d+ R\d+ — ` 69 → 69 (gate
  keys ADDED: `[]`), `^- R-\d+ — ` 274 → 275, `^Done: R-\d+ — ` 24 → 24,
  `^Landed: R-` 1 → 1; open set 250 → 251; maximum id `R-0713` → `R-0714`; ids
  ADDED `['R-0714']`; done-ids ADDED `[]`. The gate-key count is unmoved
  because the LEDGER18 slice opens `Gate: F032 R16 and R17 — `, which that
  pattern does not match — see Deviation 2.
- **G6 THE EVIDENCE BUNDLE, after C3** — the F031 `EVIDENCESCRIPT` slice was
  extracted programmatically from the committed `.agent/authored/f031-r68.md`
  (markers at lines 303 and 445, 141 body lines) and adapted by 9 anchored
  replacements, each anchor asserted unique; `diff -u` shows ONLY: the
  docstring `F031`→`F032`; `EVIDENCE_DIR` `f031_closure_evidence`/
  `remedy-job-evidence-f031-closure` → `f032_closure_evidence`/
  `remedy-job-evidence-f032-closure`; `BASE`
  `6325ac2fad76ca94e23f7bd02c80427d28e05f1f` →
  `a399a3304f9d962cd920c251488c40c486b35fdc`; the four `runs` entries →
  `vr-0001 tests/orchestration/test_decision_evidence.py 134`,
  `vr-0002 tests/orchestration/test_decision_inbox.py 35`,
  `vr-0003 tests/ui_contracts/test_decision_answer_wiring.py 55`,
  `vr-0004 tests/ui_server/test_decisions_endpoint.py 4`; `job_id`
  `f031-closure`→`f032-closure`; `job_title` `F031 Decision inbox - closure` →
  `F032 Approval with the evidence triple - closure`; `prior_job_ids`
  `["f022-closure"]`→`["f031-closure"]`; `note_prefix` `…F031 closure` →
  `…F032 closure`; `review_feature_id` `f031`→`f032`. `step_range="T001-T003"`
  and `num_tasks=3` were ALREADY correct for F032 and were not changed;
  `_tail`, `mkrun`, the `_unsafe_text` scan with its red control and the
  `output_hash` preimage check are byte-unchanged. FULL stdout, untruncated:
  `vr-0001 selected 134 node_ids 134 deselected 0 files 1 dur 0.35`;
  `vr-0002 selected 35 node_ids 35 deselected 0 files 1 dur 0.29`;
  `vr-0003 selected 55 node_ids 55 deselected 0 files 1 dur 0.31`;
  `vr-0004 selected 4 node_ids 4 deselected 0 files 1 dur 0.65`;
  `SCAN rejected strings: 0 []` with `SCAN red control: a local absolute path`
  (truthy, so the scanner is live); bundle result `job_id f032-closure`,
  `head_commit c3cf408f537de393bb156e45feae46d5de9f63da`, `manual_completion
  true`, `operator_attested_tasks T001 T002 T003`, `partition T001 4 / T002 4 /
  T003 2`, `authority_count 10`, `commit_count 134`, `total_passed 228`,
  `verdict PASS_WITH_RISKS`; `OUTPUT_HASH vr-0001 … True`, `vr-0002 … True`,
  `vr-0003 … True`, `vr-0004 … True`. Absolute `EVIDENCE_DIR`
  `/home/decodeux/Repos/remedy/.remedy-wt/f032_closure_evidence/remedy-job-evidence-f032-closure`.
  `git status --porcelain | wc -l` afterwards = `0` and `git ls-files
  .remedy-wt` = 0 lines, so nothing of the bundle entered the review subject.
- **G7 INTEGRITY AND THE ZIP** — `remedy integrity check --json` was ATTEMPTED
  and REFUSED verbatim with `Permission to use Bash has been denied.`, so the
  check was reached through its Python MODULE from the repository root:
  `packages.orchestration.integrity_gate.run_integrity_checks(collect_only=False)`
  exported with `export_integrity_json` → `"passed": true`, `"fail_count": 0`,
  `"check_count": 5`, all five checks `pass` (`handler_import handlers=340`,
  `live_review_verdict`, `plan_consistency unchecked=0`, `relevant_untracked
  untracked=0, relevant=0`, `high_blockers_open no open blocker/high
  findings`). ROUTE: the module, NOT the CLI. `git status --porcelain` 0 lines
  and `git ls-files .remedy-wt` 0 lines. ZIP: `bash scripts/make_review_zip.sh
  --evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f032_closure_evidence/remedy-job-evidence-f032-closure`,
  exit code 0 — observed by chaining `&& echo ZIP_EXIT_0_MARKER_PRINTED`, and
  the marker PRINTED. Printed package
  `remedy-review-20260828-032101-READY_FOR_REVIEW.zip`, `PACKAGE_STATUS=READY_FOR_REVIEW`,
  `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`, 3347 members.
  SHA-256 `a368e28c61381e17de4bb46a5b35ecc975046be85d456983adf469759c1e2cf4`,
  re-computed independently over the file on disk (17996334 bytes) and equal to
  the script's printed `final_sha256`. The package's
  `.review_zip_manifest.json` records `committed_review_subject` base
  `a399a3304f9d962cd920c251488c40c486b35fdc` → head
  `c3cf408f537de393bb156e45feae46d5de9f63da`, `base_is_ancestor true`,
  `commit_count 134` — the merge base to C3, as required.
- **G8 CANARY, DOCS, STRUCTURE, PR GATE, at C3** — `python3 -m pytest
  tests/cli/test_golden_path.py -q` → `42 passed in 20.72s`, exit 0 (marker
  `CANARY_EXIT_0` printed); `python3 -m pytest tests/docs/ -q` → `295 passed in
  0.44s`, exit 0 (marker `DOCS_EXIT_0` printed) — MEASURED, and equal to the
  reviewer's 295 at `a4a24663`, so the docs suite did not grow this round. Both
  ran BEFORE the evidence bundle. `git diff --name-only 12f28a42..c3cf408f` =
  `.agent/authored/f032-r18.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/prose_slips.md`, `docs/roadmap/features/T5_F032.md`
  — exactly the Change set less `.agent/handoff.md`; BOTH residues empty
  (extra `[]`, missing `[]`). `git diff --stat 12f28a42..c3cf408f -- packages/
  apps/ tests/` EMPTY; the same range over `docs/roadmap/STATUS.md` and
  `README.md` EMPTY, so both are untouched. Per-commit insertions, each
  single-parent and each under 500: C0a +452/−0, C0b +332/−287, C1 +18/−20,
  C2 +14/−0 (live_review +4, prose_slips +10), C3 +40/−0 — cell for cell equal
  to the `+/-` column of the `## Commits` table above. `^<<<SLICE ` and
  `^<<<END ` are 0 and 0 in every written file (`.agent/plan.md`,
  `.agent/live_review.md`, `.agent/prose_slips.md`,
  `docs/roadmap/features/T5_F032.md`) against a CONTROL of 5 and 5 over the
  committed C0a blob. `git ls-files .remedy-wt` 0 lines; `git worktree list`
  one line (`/home/decodeux/Repos/remedy c3cf408f [feature/f032-evidence-triple]`);
  `git branch --list "tmp/*"` empty; `gh pr list --state open --json
  number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

All five slices were extracted PROGRAMMATICALLY from the committed C0a blob
(`git show c89b867b:.agent/authored/f032-r18.md`) and never retyped.

| Slice | Target | Proof |
|---|---|---|
| PLANF032R18 | `.agent/plan.md` | whole-file byte equality `True`, trailing-newline control `False` |
| LEDGER18 | `.agent/live_review.md` | append reader (a) `True`, reader (b) N=2 in order, both controls reject |
| FINDING714 | `.agent/live_review.md` | same append, second in order |
| SLIP18 | `.agent/prose_slips.md` | append reader (a) `True`, reader (b) N=1, both controls reject |
| BUILTSTATE | `docs/roadmap/features/T5_F032.md` | append reader (a) `True`, reader (b) N=6 in order, both controls reject |

## Closure artifacts

Recorded here because R19 cannot author the STATUS line without them and this
file is the only channel that survives the round.

- **Evidence job id**: `f032-closure`
- **EVIDENCE_DIR (absolute)**:
  `/home/decodeux/Repos/remedy/.remedy-wt/f032_closure_evidence/remedy-job-evidence-f032-closure`
  — gitignored, NOT committed, and `git ls-files .remedy-wt` is 0 lines.
- **Package**: `remedy-review-20260828-032101-READY_FOR_REVIEW.zip`
- **SHA-256**: `a368e28c61381e17de4bb46a5b35ecc975046be85d456983adf469759c1e2cf4`
- **Archived path**: `/home/decodeux/Repos/remedy-history/zips`
  (DECISION amend0827 D1 — the absolute directory the package was written to,
  outside the repository; NOT the literal `NOT ARCHIVED`.)
- **Accepted HEAD (full)**: `c3cf408f537de393bb156e45feae46d5de9f63da`
- **Integrity route and result**: the CLI `remedy integrity check --json` was
  REFUSED by this session's command guard (`Permission to use Bash has been
  denied.`); the check ran through the Python MODULE
  `packages.orchestration.integrity_gate.run_integrity_checks` from the
  repository root and returned `passed: true`, `fail_count: 0`,
  `check_count: 5`. The route is the module, and no CLI PASS is claimed.
- **Suites recorded in the bundle**: `tests/orchestration/test_decision_evidence.py`
  134, `tests/orchestration/test_decision_inbox.py` 35,
  `tests/ui_contracts/test_decision_answer_wiring.py` 55,
  `tests/ui_server/test_decisions_endpoint.py` 4 — each exit 0, 0 failed,
  0 skipped, 0 deselected, node ids equal to selected, 0 strings rejected by
  the metadata scan. No full-suite node-id list is recorded (protocol pitfall
  (d)); the full-suite proof rides in R17's committed gate evidence.
- **Not done this round, by constraint 6**: no STATUS line was flipped, no
  README was touched, no pull request was created, and nothing was merged.

## Open findings

251 open (275 registered − 24 resolved), maximum id `R-0714`. This round
registered exactly `R-0714` and resolved nothing.

## Item status

Every ordered item appears exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `c89b867b`, digest equal to the scratch original |
| C0b mirror the block | done | `b8d2e0cc`, same git blob as C0a's path |
| C1 the plan | done | `c084172b`, slice PLANF032R18 applied whole |
| C2 the record | done | `02164346`, LEDGER18 then FINDING714 then SLIP18 |
| C3 the Built State | done | `c3cf408f`, slice BUILTSTATE appended; ACCEPTED HEAD |
| C4 the handback | done | this commit; rewritten once, then the branch is pushed |
| S1 the record moves first | done | C2 is the first commit after the plan |
| S2 nothing resolved | done | open set 250 → 251, `^Done:` unmoved at 24 |
| S3 Built State section | done | precondition 4 now holds; `## Built State (F032, 2026-08-28)` at line 196 |
| S4 the evidence bundle | done | F031 script adapted by 9 anchored constant edits; job `f032-closure` |
| S5 integrity | done | CLI refused verbatim; module route returned `passed: true` |
| S6 the review zip | done | `READY_FOR_REVIEW`, exit 0 by chained marker, subject spans merge base → C3 |
| S7 nothing else changes | done | both residues empty; `packages/`, `apps/`, `tests/`, STATUS.md, README.md untouched |
| S8 spec and bundle agree | done | S1–S2 in C2, S3 in C3, S4–S6 between C3 and C4 and reported in C4 |

## Deviations & assumptions

1. **The zip was built TWICE and the SECOND package is the one of record.** The
   first build's output was piped to `tail`, which masked its exit code, and G7
   orders the exit code reported rather than assumed. The build was therefore
   repeated from the same clean tree at C3 with `&& echo
   ZIP_EXIT_0_MARKER_PRINTED` chained per constraint 8; the marker printed. The
   FIRST package,
   `remedy-review-20260828-032005-READY_FOR_REVIEW.zip`, SHA-256
   `b72d245988d3ec60db3795527d5f33a40d00079068830315fdb1db4940dff787`, also
   built `READY_FOR_REVIEW` and still sits in the same archive directory; it is
   SUPERSEDED and nothing should reference it. Neither package was deleted —
   removing a READY artifact is not something this round was ordered to do.
   This is an extra ACTION, not an extra commit; the ordered commit sequence
   C0a→C0b→C1→C2→C3→C4 was followed exactly, with no extra, dropped or
   reordered commit.
2. **The `^Gate: F\d+ R\d+ — ` count did NOT move: 69 before C2, 69 after, gate
   keys ADDED `[]`.** The LEDGER18 slice opens `Gate: F032 R16 and R17 — `, and
   that pattern requires ` — ` directly after the round number, so the entry
   does not match it. The slice was applied BYTE FOR BYTE as constraint 1
   requires and was not corrected. Reported as measured, not as expected: prior
   rounds saw this counter grow by one, and this one did not.
3. **G5's reader (b) negative control was wrong on its first run and is
   reported with its repair.** The byte to flip was located with a CHARACTER
   index from `.decode()` and then applied to a BYTEARRAY; the file contains
   multi-byte em dashes, so the flip landed earlier in the file than intended —
   outside the appended region — and reader (b), which only inspects the last N
   paragraphs, did not reject it (reader (a) did). Re-run with a true BYTE
   offset, asserted to lie inside the first appended paragraph, BOTH readers
   reject in all three files. The first result was a defect of my control, not
   of the append; the appends themselves passed reader (a) byte identity
   unchanged throughout.
4. **Closure precondition 3's CLI is unreachable in this session.** `remedy
   integrity check --json` answered `Permission to use Bash has been denied.`
   The documented module substitute was used and the route is named everywhere
   the result appears. Note for the reviewer: the `high_blockers_open` check
   returned `pass`, and that check is separately known to be unable to parse
   the real ledger, so its PASS should not be read as evidence about the open
   set — the open-set numbers above were counted directly instead.
5. **The canonical zip sequence's step-1 `git push` was deferred.** Constraint 6
   orders the push AFTER C4, so the branch was not pushed before the zip. The
   package records only committed content and the manifest's
   `committed_review_subject` was verified against the local commits, so no
   reading depended on the remote.
6. **The adapted evidence script keeps F031 wording it does not use.**
   `mkrun`'s docstring still names "F031's scoped suites" and commit
   `44fd8df9`. S4 orders everything but the named constants kept AS IT IS, so
   it was kept. The script lives at `.remedy-wt/f032_evidence.py`, is
   gitignored and is not committed, so no stale claim entered the repository.
7. **Assumption, declared:** `step_range="T001-T003"`, `num_tasks=3` and the
   `_tail`/`mkrun`/scan/preimage machinery were left byte-unchanged because
   they were already correct for F032; S4 named no change to them.

No test was edited, no assertion weakened, no evidence directory or package was
committed, no branch was force-pushed and no history was rewritten. `git status
--porcelain` is 0 lines at the end of every commit in the bundle.

## Next

R19 — closure part two: the reviewer-authored STATUS `[x]` line for F032 and
the README capability sync in ONE commit, last on the branch, using the
Closure artifacts above verbatim; then the pull request, which is NOT merged in
this session (closure protocol step 6). Before authoring, re-read `.agent/STOP`
from disk (Phase 1 rule 1) and only then run the Open PR Gate (rule 2).
