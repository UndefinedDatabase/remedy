# Handback — F085 R41 (record and protocol repair)

Branch feature/f085-sandbox-hardening · base 93226220 · no PR, no merge. Open findings 122.
Fortschritt: ~77 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R40 PASS
· T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 ab R42 migrierbar ·
T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Range
Review of 93226220..HEAD — 7 commits: C0a, C0b, C1, C2, C3, C4, C5.

## Commits
### 9cc4772c docs(f085): save the R41 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r41.md | +398/-0 | C0a — the block saved byte-for-byte |
### a66aa301 docs(f085): mirror the R41 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +361/-188 | C0b — same bytes as C0a |
### 1a29a77d docs(review): record the R40 PASS, register R-0533 and R-0534, resolve R-0530 to R-0532
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +102/-0 | C1 — RECORD9 appended |
### 01359f81 docs(agents): bind the append per-line count to prose and order equality for code
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +14/-0 | C2 — P49 pair, §4 item 9 |
### 247df04b docs(agents): narrow checklist item 20 and add items 21 and 22
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +49/-0 | C3 — CL20 pair, the §3 checklist |
### bb07a759 docs(f085): advance the plan to R41
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +4/-3 | C4 — PLANF9→PLANT9 over Current Step alone |
### this commit docs(f085): rewrite the handback for R41
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C5 — a handoff cannot table itself |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | landed after C2, per constraint 6 |
| C4 | done | |
| C5 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after this commit — the only one. No
worktree add or remove, no gh command, no PR, no merge.

## Verification
G1 STATE exit 0 — `.agent/STOP` absent before C0a and before C5; `git status --porcelain`
empty at round start and after all six preceding commits; `git worktree list` one line.
G2 TRANSPORT exit 0 — reviewer scratch, both committed copies and both working copies all
five byte-EQUAL disk to disk at sha256
a3716bdf9fa29892bbb6220a5b50bf6c73b057106e0465a28d71e3cd17febbba, 28265 B, 398 lines, 14
marker lines. Regions, trailing newlines included: 1-120 3a60710d… 8501 B, 121-240
784abc8e… 8690 B, 241-398 640caada… 11074 B; 8501+8690+11074 = 28265, the whole file.
G3 APPEND exit 0 — pre-commit 412143 B is a byte-exact PREFIX of the 420193 B post-commit
file; remainder 8050 B = one blank line + RECORD9; RECORD9 an exact suffix at sha256
cf21f13adb1535b6…, 8049 B, 101 lines. 0 LINES match `^(BEGIN|END)-[A-Z0-9]+$`, while 11
lines of that file's prose contain the regex text. Every non-empty RECORD9 line occurs 1x
among C1's 102 added lines, 0 violations; the slice holds 7 empty lines, exempt; 0
duplicate non-empty lines in it. numstat 102 0.
G4 ARITHMETIC exit 0 — 93226220 147 / 24 / 0, 123 open, max registered R-0532, max resolved
R-0527; HEAD 149 / 27 / 0, 122 open, max registered R-0534, max resolved R-0532. Registered
symmetric difference exactly R-0533 and R-0534; done difference exactly R-0530, R-0531 and
R-0532; landed difference empty; 0 duplicate ids; 0 resolutions naming an unregistered id;
next free R-0533 → R-0535.
G5 DOC EDITS exit 0 — P49FROM 1x, P49TO 1x, CL20FROM 1x, CL20TO 1x at HEAD; both TO-only
sets (14 and 49 lines) equal their own commit's added lines IN ORDER, each line 1x, 0
duplicates within either set. STRUCTURAL: the region from line 173 (`Pre-emission block
checklist`) to the `Why this is on disk and not a habit:` line yields item labels 1..22
contiguous, no gap, no repeat, against a base of 1..20; the UNSCOPED match reads 1..22 then
1,2,3,5. 0 marker lines. The file MEASURES 706 lines at HEAD against 643 at 93226220 (see
Deviations). numstat: C2 14 0, C3 49 0.
G6 PLAN exit 0 — PLANF9 1x before C4 and 0x at HEAD, PLANT9 1x; `.agent/plan.md` MEASURES
46 lines against the 50 cap, `## Goal` and `## Next Steps` present, 0 marker lines.
numstat 4 3.
G7 SUITES exit 0 each, both run in the PRIMARY checkout — `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf
-q` → `159 passed in 20.09s` against base 159; canary `python3 -m pytest
tests/cli/test_golden_path.py -q` → `42 passed in 21.97s` against base 42.
G8 HYGIENE exit 0 — `git diff --name-only 93226220..HEAD` before C5 is exactly
`.agent/authored/f085-r41.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`docs/agents/planner_reviewer_prompt.md`, `.agent/plan.md`. Walked with `git rev-list
--reverse`, one reading per commit: insertions 398, 361, 102, 14, 49, 4 (deletions 0, 188,
0, 0, 0, 3), none over 500; C5's own insertions are in the round report. Every commit
single-parent; `git reflog -10` holds only `commit:` entries.

## Authored-text proofs
RECORD9, P49FROM/P49TO, CL20FROM/CL20TO, PLANF9 and PLANT9 were extracted programmatically
by marker pair from the COMMITTED `.agent/authored/f085-r41.md`, never retyped and never
taken from the prompt; the disk-to-disk comparison against `.remedy-wt/f085-r41.md` is G2.
Pair shapes re-measured at 93226220, each matching constraint 2: P49 and CL20 both read `TO
contains FROM: true` (APPENDs, so each FROM still reads 1x at HEAD); PLANF9→PLANT9 reads
false (REWRITE, FROM 0x / TO 1x).

## Deviations & assumptions
Sequence followed exactly: C0a, C0b, C1, C2, C3, C4, C5 — none added, dropped or reordered;
C2 landed before C3 per constraint 6. No worktree created.
Declared under constraint 8 and NOT repaired per constraint 9. The sweep re-read all five
edited paths after C4 and measured:
1. TWO PRESENT-TENSE READINGS IN RECORD9 DIFFER FROM HEAD, each in a clause whose SHA
   qualifier attaches to an EARLIER reading in the same sentence — the shape R-0534
   registers two paragraphs above, in the same slice. (a) "`.agent/plan.md` 45 lines": 45 at
   1a29a77d, 46 at HEAD, falsified by C4 of this same round. (b) "next free R-0533": true at
   93226220, but already R-0535 at 1a29a77d, the commit that landed the sentence.
2. THREE LINE-COUNT PREDICTIONS IN THE BLOCK EACH READ +1. G5 states 707 at HEAD and 644 at
   93226220; measured 706 and 643. G6 states the dry run put the plan at 47 lines; measured
   46. G5 orders "report the number rather than asserting it", so the gate is met by the
   measurement. This is not a convention difference: RECORD9's own line counts reproduce
   exactly under `splitlines` (the R40 block 225 lines, `.agent/plan.md` 45 at base).
The sweep also re-measured what this round registers and records; all reproduce. R-0533's
walk of cbcb5c23..d3a707f5 gives 349, 295, 50, 66, 3, 147 with f31802f0 at 3 ins / 3 del.
R-0534's `.agent/last_block.md` hashes 32415af6 at 757be21c and fad599b4 at both 067fa3d2
and a5e240ca. RECORD9's R40 hygiene walk of d3a707f5..93226220 gives 225, 168, 70, 3, 81.
The three `Done:` claims are TRUE at HEAD: items 21 and 22 sit under `## 3. Planning
contract`, the P49 text under `## 4. Review loop` as its item 9, and items 11, 12 and 20
that the new text cites all exist with the cited subjects.
Length 144 lines under DECISION D15, stated cause: mandated content that does not fit 60 —
Commits 30 lines (seven per-commit tables), Item status 11, Verification 41 (eight gates
with real values), the constraint-8 measurement 26, Fortschritt 3 and the R42 note 8.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). R41's own verdict is NOT a §4.13 terminator,
because this branch continues; the next reviewed round records R41's gate entry.

  R42 migrates `packages/orchestration/ci_run.py` onto the seam, passing the per-stage
  budget through the `extra_env` overlay that landed at dce66faa. It still owes its own
  DECISION on where the stage output goes: at 93226220 `_run_via_subprocess` streams
  straight to the console and returns only the returncode, while the seam CAPTURES both
  streams, so the migration changes observable behaviour rather than preserving it. That
  decision is the round's own work and belongs in `.agent/decisions.md` before any line
  changes. `packages/orchestration/builder_bridge.py` follows it; then T002c-d, then T003
  and the integration gate.
