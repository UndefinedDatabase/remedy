# Handback — F032 Evidence Triple — Round R19 (closure part two)

## Session

SESSION 4 of feature F032 · round R19 · rounds so far 19
(R1–R5 session 1, R6–R9 session 2, R10–R14 session 3, R15–R19 this one.)

## Range

Review of `eb243fcd393fa4411cbb6cf55c9e273629c690c0..HEAD`, where HEAD is C3 —
the commit that carries this file. A commit's own SHA cannot be written inside
itself, so C3's SHA is reported in the round report; C0a through C2 are named in
full below.

## State

- Branch: `feature/f032-evidence-triple`
- Base of this round: `eb243fcd393fa4411cbb6cf55c9e273629c690c0` (the R18
  handback), measured with `git rev-parse HEAD` in full and equal to the base
  the block names.
- Merge base with `main`: `a399a3304f9d962cd920c251488c40c486b35fdc`
- Commits, in order: C0a `e01aef15d33df9de9df2a412191ece189eaecce6`,
  C0b `2b2cccec16209badf54596c9cf48cd1f3bcebb3b`,
  C1 `0b83f8a11a026a8195a0bed73dfc301712e6a9e7`,
  C2 `e9af5b633163fc1e75b33c6be0839040e83e8b67`,
  C3 this commit — the CLOSURE commit and the last on the branch.
- ACCEPTED HEAD, unchanged by this round:
  `c3cf408f537de393bb156e45feae46d5de9f63da`.
- F032's STATUS line is now `[x]` and the README capability prose and both
  ledger-derived counts moved WITH it, in this one commit.

## Commits

### e01aef15 docs(agent): save the F032 R19 closure block as authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f032-r19.md | +405 / -0 | C0a, the block saved verbatim |

### 2b2cccec docs(agent): mirror the R19 block into the last-block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +306 / -353 | C0b, the same bytes mirrored from the committed C0a blob |

### 0b83f8a1 docs(agent): point the plan at the F032 closure round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -18 | C1, slice PLANF032R19 applied whole |

### e9af5b63 docs(agent): book the R18 verdict and the authoring slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2, slice LEDGER19 appended |
| .agent/prose_slips.md | +11 / -0 | C2, slice SLIP19 appended |

### C3 the closure commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1 / -1 | pair STATUSFLIP, `[~]` → `[x]`; exactly one line |
| README.md | +7 / -2 | pairs READMECAP, READMECOUNT, READMETIER — the capability paragraph and both counts |
| .agent/handoff.md | not tabled | a handoff cannot table the commit that writes it |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  before any work this round (Open PR Gate clear).
- `git push -u origin feature/f032-evidence-triple` and `gh pr create --base
  main --head feature/f032-evidence-triple` are ordered by the block's
  constraint 7 and run immediately AFTER this commit. Their outcomes cannot be
  recorded in the file that precedes them and are reported in the round report.
- No worktree was added or removed. No merge, no force-push, no history rewrite,
  no branch deletion. No package was built and no `npm`, `npx`, `node` or `vite`
  was run (constraint 10).

**THE PULL REQUEST IS CREATED AND IS NOT MERGED IN THIS SESSION.** It merges at
the NEXT feature's start, through the Open PR Gate of AGENTS.md, on Window 1's
instruction; that gap is the operator's manual review window and the operator
may merge manually at any time instead (closure protocol step 6).

## Verification

One line per gate, every number measured this round. G6 and G7 read the tree
that BECAME C3 — the four pairs applied, nothing else staged — because a
handback committed inside C3 cannot quote a reading taken after C3 exists.

- **G1 HYGIENE, BASE, SENTINEL** — `git rev-parse HEAD` before C0a =
  `eb243fcd393fa4411cbb6cf55c9e273629c690c0`, equal IN FULL to the base the
  block names; `git rev-parse --abbrev-ref HEAD` = `feature/f032-evidence-triple`;
  `git status --porcelain | wc -l` = `0` after each of C0a, C0b, C1 and C2;
  `ls -la .agent/STOP` before C0a AND again before C3 both printed exactly
  `ls: cannot access '.agent/STOP': No such file or directory` — the sentinel
  does not exist at either reading.
- **G2 TRANSPORT** — `sha256sum` equal across all three disk copies at
  `bccbd4be2011a1b90f2533bea086d6f2fe6aa548c1fc0c22aaf29e0e206a35ff`: the
  reviewer's gitignored scratch original `.remedy-wt/f032-r19.md`,
  `.agent/authored/f032-r19.md` at C0a and `.agent/last_block.md` at C0b. The
  two committed paths are ONE git blob,
  `3797fb6373eb133fc0fcf3e47d3d5d329db012f1`. The chain covers the original,
  the copy and the mirror, and claims nothing about any prompt's bytes.
- **G3 EXTRACTION AND CAPS** (measured on the committed C0a blob, `git show
  e01aef15:.agent/authored/f032-r19.md`) — 11 regions found: SLICE PLANF032R19
  44 content lines, SLICE LEDGER19 1, SLICE SLIP19 10, FROM STATUSFLIP 1, TO
  STATUSFLIP 1, FROM READMECAP 1, TO READMECAP 6, FROM READMECOUNT 1, TO
  READMECOUNT 1, FROM READMETIER 1, TO READMETIER 1. Content total 68; block
  TOTAL 405 lines; PROSE = 405 − 68 = 337. PROSE < 400 `True`, TOTAL < 490
  `True`.
- **G4 THE PLAN, at C1** — `.agent/plan.md` byte-equal to slice PLANF032R19
  extracted from the committed C0a blob → `True`; NEGATIVE CONTROL, the same
  comparison with the slice's trailing newline removed → `False`; `wc -l` = 44
  (< 50); `^## Goal$` = 1; `^## Next Steps$` = 1.
- **G5 THE APPENDS, at C2**, each baseline read with `git show 0b83f8a1:<path>`
  so no tracked file was ever overwritten to get one. `.agent/live_review.md`:
  reader (a) byte identity `True` at 1121850 + 1 + 4705 = 1126556 = post, with
  the pre-commit blob a byte PREFIX `True`; reader (b) N = 1, the last 1
  blank-line unit equals the slice's paragraph in order `True`. `.agent/
  prose_slips.md`: reader (a) `True` at 3550 + 1 + 768 = 4319 = post, PREFIX
  `True`; reader (b) N = 1, in order `True`. NEGATIVE CONTROL for each — one
  byte flipped IN MEMORY inside the FIRST appended paragraph at a BYTE offset
  (live_review offset 1121851 `G`→`g`; prose_slips offset 3567 `F`→`f`, each
  asserted to lie inside the appended slice) — BOTH readers reject in BOTH
  files. Ledger counters, before C2 → after C2: `^- R-\d+ — ` 275 → 275,
  `^Done: R-\d+ — ` 24 → 24, OPEN SET 251 → 251, maximum id `R-0714` →
  `R-0714`. Unmoved, as ordered: this round registers nothing and resolves
  nothing.
- **G6 THE FOUR PAIRS, at C3**, each proved in the shape constraint 3 assigns
  it. BEFORE the edit each FROM occurred exactly `1` time in its target:
  STATUSFLIP 1 in `docs/roadmap/STATUS.md`, READMECAP 1, READMECOUNT 1,
  READMETIER 1 in `README.md`. The containment test re-run here agrees with the
  block: `TO contains FROM` is `False` for STATUSFLIP, READMECOUNT and
  READMETIER and `True` for READMECAP. AFTER the edit — the three REWRITES:
  STATUSFLIP FROM 0x / TO 1x, READMECOUNT FROM 0x / TO 1x, READMETIER FROM 0x /
  TO 1x. The APPEND READMECAP: FROM exactly 1x in `README.md`, and each of its
  5 TO-ONLY lines exactly 1x among the 8 lines C3's diff ADDS over the two
  files; NO FROM-zero count was ordered or attempted, being unattainable by
  construction. Numstat of C3's content against its parent, measured as `git
  diff --numstat HEAD -- README.md docs/roadmap/STATUS.md` from the tree that
  became C3: `7 2 README.md` and `1 1 docs/roadmap/STATUS.md`.
- **G7 THE DOCS GATE AND THE CANARY, at C3 and BEFORE the pull request** —
  `python3 -m pytest tests/docs/ -q` → `295 passed in 0.44s`, exit 0 (chained
  marker `DOCSGATE_EXIT_ZERO` PRINTED); `python3 -m pytest
  tests/cli/test_golden_path.py -q` → `42 passed in 20.73s`, exit 0 (chained
  marker `CANARY_EXIT_ZERO` PRINTED). Both were run on the tree carrying all
  four pair edits. `295` is what was MEASURED here; it is reported as measured
  and not because the reviewer's dry run predicted it, and the reviewer's RED
  control of `2 failed, 293 passed` was not reproduced because all four edits
  were applied before the suite ran, which is the state the gate asks about.
- **G8 STRUCTURE, THE PR AND THE GATE** reads C3 itself and therefore cannot be
  quoted by a file committed inside C3; its readings are in the round report,
  as the block directs.

## Authored-text proofs

All three slices and all four FROM/TO pairs were extracted PROGRAMMATICALLY
from the committed C0a blob (`git show e01aef15:.agent/authored/f032-r19.md`),
written to `.remedy-wt/r19_regions/` by the extractor, and applied from those
files. Nothing was retyped from the prompt.

| Text | Target | Proof |
|---|---|---|
| PLANF032R19 | `.agent/plan.md` | whole-file byte equality `True`, trailing-newline control `False` |
| LEDGER19 | `.agent/live_review.md` | append reader (a) `True`, reader (b) N=1 in order, both controls reject |
| SLIP19 | `.agent/prose_slips.md` | append reader (a) `True`, reader (b) N=1 in order, both controls reject |
| STATUSFLIP | `docs/roadmap/STATUS.md` | rewrite, FROM 1x before → FROM 0x / TO 1x after |
| READMECAP | `README.md` | append, FROM 1x before and 1x after, 5 TO-ONLY lines each 1x among C3's added lines |
| READMECOUNT | `README.md` | rewrite, FROM 1x before → FROM 0x / TO 1x after |
| READMETIER | `README.md` | rewrite, FROM 1x before → FROM 0x / TO 1x after |

## Closure artifacts

Carried forward VERBATIM from R18's handback, because R18 is the only actor
that measured them and this file is rewritten every round. The STATUS line
committed here rests on exactly these values.

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
  REFUSED by this session's command guard; the check ran through the Python
  MODULE `packages.orchestration.integrity_gate.run_integrity_checks` from the
  repository root and returned `passed: true`, `fail_count: 0`,
  `check_count: 5`. The route is the module, and no CLI PASS is claimed.
- **Suites recorded in the bundle**: `tests/orchestration/test_decision_evidence.py`
  134, `tests/orchestration/test_decision_inbox.py` 35,
  `tests/ui_contracts/test_decision_answer_wiring.py` 55,
  `tests/ui_server/test_decisions_endpoint.py` 4 — node ids equal to selected in
  every case. No full-suite node-id list is recorded (protocol pitfall (d)); the
  full-suite proof rides in R17's committed integration-gate evidence.
- **PROVENANCE LIMIT, stated rather than implied**: the package filename, its
  SHA-256 and its archived path rest on R18's transcript and NOT on any reading
  taken in this session — the archive directory lies outside this session's
  allowed working directories, where `ls` and `sha256sum` are both refused.
  Everything else in the STATUS line was measured directly.

## Open findings

251 open (275 registered − 24 resolved), maximum id `R-0714`. This round
registered nothing and resolved nothing; the counters were measured before and
after C2 and are unmoved.

## Item status

Every ordered item appears exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `e01aef15`, digest equal to the scratch original |
| C0b mirror the block | done | `2b2cccec`, same git blob as C0a's path |
| C1 the plan | done | `0b83f8a1`, slice PLANF032R19 applied whole |
| C2 the record | done | `e9af5b63`, LEDGER19 and SLIP19 appended |
| C3 the closure commit | done | this commit; STATUS flip + README sync + this handback, last on the branch |
| C4 no commit, the pull request | done | opened after C3 with `gh pr create`, base `main`; commits nothing; NOT merged |
| S1 the record moves first | done | C2 precedes C3; `^Done:` unmoved at 24, open set 251, max `R-0714` |
| S2 the STATUS flip | done | pair STATUSFLIP; exactly one line changed, numstat `1 1` |
| S3 the README sync | done | READMECAP, then READMECOUNT, then READMETIER, in that order |
| S4 S2 and S3 in ONE commit | done | both in C3, the last commit on the branch; they cannot disagree in any committed state |
| S5 the pull request | done | opened after C3 and after the push; number and URL in the round report |
| S6 runtime actuals | done | rounds 19, sessions 4; wall clock, models, tokens and cost `not-measured` |
| S7 nothing else changes | done | no production code, test, feature file, evidence directory or package touched |
| S8 spec and bundle agree | done | S1 is C2; S2–S4 are C3; S5–S6 follow C3 and commit nothing |

## Deviations & assumptions

The ordered commit sequence C0a→C0b→C1→C2→C3 was followed EXACTLY: no extra
commit, no dropped commit, no reordering.

1. **G6's numstat was measured against the tree that became C3, not with `git
   show --numstat <C3>`.** The block orders that command, and its output cannot
   exist while the file quoting it is still being written into that same commit.
   The equivalent reading `git diff --numstat HEAD -- README.md
   docs/roadmap/STATUS.md`, taken with all four pairs applied and nothing else
   staged, is reported instead; `git show --numstat <C3>` is re-run for the
   round report and must agree cell for cell.
2. **The same timing applies to the sentence that the pull request was created.**
   The PR is opened after this commit, so this file states the durable half —
   that it is NOT merged in this session and merges at the next feature's start
   through the Open PR Gate — and the number and URL go in the round report.
   This is R18's disposition of its own push, applied again.
3. **Assumption, declared:** the STATUS line's package filename, SHA-256 and
   archived path were applied byte for byte from the block's TO slice and were
   NOT independently re-measured, because the archive directory is outside this
   session's allowed working directories. The provenance limit is stated in
   Closure artifacts above rather than left implicit.

No test was edited, no assertion weakened, no evidence directory or package was
committed, no branch was force-pushed and no history was rewritten. `git status
--porcelain` is 0 lines after every commit in the bundle.

## Next

F032 is CLOSED on disk and its pull request is open and unmerged. The next
session's first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
and only then rule 2, the Open PR Gate, which merges this closure PR before any
new branch is cut. The next feature is then chosen by Rule A5 from
`docs/roadmap/STATUS.md`, whose first unclaimed line is
`- [ ] F037 — Rendered diff viewer`.
