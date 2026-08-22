# Handback — F021 R3 (decision + specification-repair round)

Feature F021 Live activity feed + now-card, round R3, branch
feature/f021-live-activity-feed, round base `4a7b5cbf85f76b5c7f1aec9c12108788bdf2b3b9`.
Fortschritt: ~10 % (T001 offen · T002 offen · T003 offen; R1 beansprucht, R2
             vermessen, R3 entscheidet und korrigiert die Spezifikation —
             gebaut wird ab R4) — Schätzung

## Range
Review of `4a7b5cbf85f76b5c7f1aec9c12108788bdf2b3b9..HEAD` (6 commits).

## Commits
### a0fa3380 docs(state): save the F021 R3 decide block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r3.md | 274/0 | C0a, the R3 block saved verbatim, NEW |
### 12e0c51d docs(state): mirror the F021 R3 decide block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 222/174 | C0b, written FROM the committed C0a blob |
### 4e6d5539 docs(state): point the F021 plan at the R3 decision round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 23/25 | C1, PLANF021R3 applied in full |
### d49cad70 docs(review): record the R2 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2, RECORD2 appended after the round-base blob |
### 14060467 docs(state): rule DECISIONS F021 D1 and D2 on the measured ground
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 20/0 | C3, DECIDE1 appended after the round-base blob |
### C4 (SHA ABSENT BY CONSTRUCTION — C4 is the final commit and it writes this very file, so it cannot carry its own identifier, the R-0149 pattern; its SHA is in the round report) docs(roadmap): amend the F021 feature file to match the measured source and hand back R3
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F021.md | 21/9 | C4, the three pairs AMENDA, AMENDB, AMENDC |
| .agent/handoff.md | 86/63 | C4, this handback, measured on staged content |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions
`git worktree add .remedy-wt/g5wt HEAD --detach` for G5's destructive half, then
`git worktree remove --force .remedy-wt/g5wt` and `git worktree prune` — `git
worktree list` afterwards shows the primary checkout only. `gh pr list --state
open --json number,headRefName` printed `[]`. `git push -u origin
feature/f021-live-activity-feed` runs after C4 as the block's last step; its
outcome is in the round report. No PR created, none merged, no `gh pr create`
and no `gh pr merge` run.

## Verification
- G1 STOP absent immediately before C0a and again immediately before C4; branch feature/f021-live-activity-feed; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3; C4's own reading is in the round report (checklist item 14).
- G2 TRANSPORT: `.agent/authored/f021-r3.md` at C0a, `.agent/last_block.md` at C0b and the received bytes are all sha256 e25b8baffc8537e2de1d849e8320ede2c32355bc71d5471ce58fa11e5feb808d over 23380 bytes and 274 lines; C0b was written FROM the committed C0a blob.
- G3 SLICES: the marker-line extractor over the committed C0a blob printed 9 slices over 94 CONTENT lines; constraint 9 re-measures from that same blob as TOTAL 274 against DECISION F085 D6's 490 and PROSE 180 against D5's 400.
- G4 PLAN: `cmp` of `.agent/plan.md` against PLANF021R3 exit 0, negative control `cmp` against RECORD2 exit 1; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 42 under the 50 cap.
- G5 reader (a), BOTH appends ACCEPT: the round-base blob is a byte-exact PREFIX and the remainder is exactly one newline plus the slice — live_review.md remainder sha256 27f3e4871bb7c3ce98ff2e418b54f653d9b01b8428c23bf19b3e318f94f083f4 over 4339 bytes and 2 lines, file 426777 bytes / 1072 lines to 431116 / 1074; decisions.md remainder sha256 37fbff5a6882ba72aa0f630e5be8fdf74237556a627048809a1ebd2fed31c852 over 4316 bytes and 20 lines, file 485030 / 6959 to 489346 / 6979.
- G5 reader (b), blank-line units: N 217 then 218 at live_review.md and N 1210 then 1220 at decisions.md; every carried unit elementwise equal at both files, and the appended units equal the slice's OWN units (1 for RECORD2, 10 for DECIDE1) while neither base tail already held them.
- G5 reader (b) IS RED AS LITERALLY ORDERED AND IS NOT PATCHED — the clause "the LAST unit equals the slice" is unmeetable for DECIDE1, which spans 10 units, and it ACCEPTS the live_review.md first-paragraph mutant because it inspects only the last unit; that is finding R-0631 live in this block's own G5 text. See Deviations.
- G5 NEGATIVE CONTROL, one printable ASCII byte of the FIRST paragraph swapped in case at equal length, run in the disposable worktree `.remedy-wt/g5wt` since removed and pruned: reader (a) REJECTS both mutants and ACCEPTS both true files; the carried-unit reader REJECTS both mutants at index 0 and ACCEPTS both true files.
- G6 LEDGER SETS, line-anchored, base then C2: `- R-` entries 211 then 211, DISTINCT 211 then 211; `Done: R-` 0 then 0; `Landed: ` 0 then 0; `Gate: R` keys 2 then 3, DISTINCT 2 then 3; `Gate: R3` 0 then 1; MAXIMUM registered id R-0648 at BOTH points, as constraint 3 requires.
- G7 DECISION HEADINGS, line-anchored over `.agent/decisions.md`, base then C3: `^## DECISION ` 110 then 112; `^## DECISION F021 D1 ` 0 then 1; `^## DECISION F021 D2 ` 0 then 1 — each append landed once and not twice.
- G8 THE THREE PAIRS at C4 over `docs/roadmap/features/T5_F021.md`, applied with count=1 in the order AMENDA, AMENDB, AMENDC: each FROM measured BEFORE its own replacement reads 1, 1, 1; after C4 each FROM reads 0 and each TO reads 1; `git show --numstat` for that path is 21/9.
- G9 DOCS GATES, serial, on the tree C4 commits: `python3 -m pytest tests/docs/ -q -rf` exit 0, 295 passed; `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf` exit 0, 30 passed.
- G10 CONTRACT SUITES, primary checkout, serial after G9: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed plus skipped (511 passed, 0 skipped), 40.86s.
- G11 CANARY, serial and after G10 finished: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed, 20.54s.
- G12 NO PRODUCTION FILE CHANGED: 0 paths beginning `apps/`, `packages/` or `tests/` in the base-to-C4 range; `git ls-files .remedy-wt` reads 0.
- G13 RANGE, measured base-to-tree with C4 fully staged and re-run after C4: the path set EQUALS the block's seven-path `Change:` list with BOTH set differences EMPTY; every commit single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the table above; maximum insertions 274 under the 500 cap; leading `<<<SLICE ` and `<<<END ` read 0 LINES in all four files a slice lands in; this round's reflog rows classify with `amend` 0, `rebase` 0, `cherry` 0.
- G14 NO PULL REQUEST: `gh pr list --state open --json number,headRefName` printed `[]`; this round ran neither `gh pr create` nor `gh pr merge`.
- G15 THIS HANDBACK carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, ONE LINE PER GATE with transcripts kept in the round report (R-0582), the block's `Fortschritt:` line verbatim across all three of its lines, and a FULL subject in every `## Commits` heading with C4's unavailable SHA explained inside that heading itself rather than in a channel that ends with this session.

## Authored-text proofs
All nine slices were extracted programmatically from the COMMITTED C0a blob by
their `<<<SLICE `/`<<<END ` marker LINES and never retyped. PLANF021R3 to
`.agent/plan.md` at C1 — `cmp` exit 0, negative control against RECORD2 exit 1
(G4). RECORD2 to `.agent/live_review.md` at C2 and DECIDE1 to
`.agent/decisions.md` at C3 — appended, not replaced, each proved under reader
(a) plus the carried-unit reader with a first-paragraph mutant both reject (G5).
The three pairs AMENDA, AMENDB and AMENDC applied to
`docs/roadmap/features/T5_F021.md` at C4 as byte-substring replacements of the
FROM slice by the TO slice; all three are REWRITES per constraint 5, so no §4.9
append obligation attaches and the FROM-zero reading is the one reported (G8).

## Deviations & assumptions
No commit was added, dropped or reordered: C0a, C0b, C1, C2, C3, C4 exactly as
the block ordered them. Constraint 3 held — this round minted no finding id,
wrote no `- R-` entry, no `Done:` and no `Landed:` line; R-0648 stays the
maximum and R-0649 is the next free id. No file under `apps/`, `packages/` or
`tests/` was created, modified or deleted and no in-place formatter was run.
ONE DECLARED DEVIATION, and it is a defect of the block's own gate text rather
than of the execution: G5's reader (b) as written orders "confirm the LAST unit
equals the slice". DECIDE1 spans 10 blank-line units, so that clause cannot be
satisfied for C3 by construction; and for C2 the clause is satisfied by the
first-paragraph MUTANT as well as by the true file, so the ordered reader (b)
FAILS its own mandated negative control. The clause was NOT weakened and no
expected value was adjusted. It is reported RED as written, and beside it the
strictly stronger property was measured and passed: the new unit list equals the
base unit list followed by exactly the slice's own units, elementwise, which
subsumes the ordered clause when a slice is one unit and rejects both mutants at
carried index 0. AMENDATO leaves the paragraph wrapped raggedly ("The steering
input\nis a design\nelement of this surface"); it was applied byte for byte and
NOT reflowed, per constraint 1. DECISION D15 OVERAGE DECLARED: this file exceeds
the 100-line cap a six-commit round allows. The cause is mandated
content only — per-commit tables for six commits, the six-row item-status table,
the authored-text proofs, and G15's ONE LINE PER GATE over fifteen gates of
which G5 needs four (two readers, the ordered reader's red result, and the
negative control). No section was dropped to reach the cap and no transcript was
moved into this file. Its own `wc -l` reads 120.

## Next
Reviewer gates this handback against the source and, on PASS, authors R4: build
T001 headless-first — the humanize catalog module, the coverage test DECISION
F021 D1 rules, the honest generic line for an unrecognised kind, and goldens,
per `.agent/plan.md` Next Steps item 1.
