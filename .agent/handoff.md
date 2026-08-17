# Handback — F085 R40 (session-closing round)

Branch feature/f085-sandbox-hardening · base d3a707f5 · no PR, no merge.
Fortschritt: ~76 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R39
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 ab R41
migrierbar · T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

## Range
Review of d3a707f5..HEAD — 5 commits: C0a, C0b, C1, C2, C3.

## Commits
### fc5d957a docs(f085): save the R40 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r40.md | +225/-0 | C0a — the block saved byte-for-byte |
### 067fa3d2 docs(f085): mirror the R40 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +168/-292 | C0b — same bytes as C0a |
### a5e240ca docs(review): record the R39 PASS and register R-0531 and R-0532
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +70/-0 | C1 — RECORD8 appended |
### 8ab228ca docs(f085): advance the plan to R40
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3/-3 | C2 — PLANF8→PLANT8 over Current Step alone |
### this commit docs(f085): rewrite the handback for R40
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C3 — a handoff cannot table itself |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after this commit — the only one. No
worktree add or remove, no gh command, no PR.

## Verification
G1 STATE exit 0 — `.agent/STOP` absent before C0a and before C3; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.
G2 TRANSPORT exit 0 — reviewer scratch, both committed copies and both working copies all
five byte-EQUAL disk to disk at sha256
fad599b49902bd898feca72a990ba03061af4ba6598135570e7028ff797c41ed, 15082 B, 225 lines, 6
marker lines. Regions, trailing newlines included: 1-100 74617c1c… 6391 B, 101-end
8c417993… 8691 B; the two reassemble to the whole.
G3 APPEND exit 0 — pre-commit 406554 B is a byte-exact PREFIX of the 412143 B post-commit
file; remainder 5589 B = one blank line + RECORD8; RECORD8 an exact suffix; its first line
1x among C1's 70 added lines; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` in the file; every
non-empty RECORD8 line 1x among the added lines, 0 violations, the slice holding 3 empty
lines, exempt; added = one empty line then RECORD8's 69 lines IN ORDER. numstat 70 0.
G4 ARITHMETIC exit 0 — d3a707f5 145 / 24 / 0, 121 open, max registered R-0530, max resolved
R-0527; HEAD 147 / 24 / 0, 123 open, max registered R-0532, max resolved R-0527. Registered
symmetric difference exactly R-0531 and R-0532, done and landed differences empty, 0
duplicate ids, 0 resolutions naming an unregistered id, next free R-0531 → R-0533.
G5 PLAN exit 0 — PLANF8 1x before C2 and 0x at HEAD, PLANT8 1x; plan.md 45 lines against
the 50 cap, `## Goal` and `## Next Steps` present, 0 marker lines. numstat 3 3.
G6 SUITES exit 0 each, both in the primary checkout — four state readers `159 passed`
against base 159; canary `42 passed` against base 42.
G7 HYGIENE exit 0 — the path set before C3 is exactly `.agent/authored/f085-r40.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. Insertions 225, 168, 70,
3, none over 500; every commit single-parent; `git reflog -10` holds only `commit:` entries.

## Authored-text proofs
RECORD8, PLANF8 and PLANT8 were extracted programmatically by marker pair from the
COMMITTED `.agent/authored/f085-r40.md`, never retyped and never taken from the prompt;
the disk-to-disk comparison against `.remedy-wt/f085-r40.md` is G2. RECORD8 hashes
d6ce71700bafa738218c94e573b2470bfefc0532953f679234604721dc3b96af, 5588 B, 69 lines.

## Deviations & assumptions
Sequence followed exactly: C0a, C0b, C1, C2, C3 — none added, dropped or reordered.
Declared under constraint 8, applied as written and NOT repaired per constraint 9 — two
defects in RECORD8's own text, both quantifying over commits:
1. It reads R39's "per-commit insertions are 349, 295, 50, 66, 6". Measured over
   cbcb5c23..d3a707f5: 349, 295, 50, 66, 3 and 147. f31802f0 is 3 insertions / 3 deletions,
   so 6 is the insertions+deletions churn reading AGENTS.md DECISION F104 D1 excludes. The
   clause's conclusion, none over 500, still holds.
2. Its five-way transport sentence and closing "origin and local agree at d3a707f5" are
   present-tense claims this round's OWN earlier commits falsified before the sentence
   landed: at C1 four of the five R39 artifacts still hash 32415af6…1181a, but the WORKING
   `.agent/last_block.md` hashed fad599b4… because C0b overwrote it two commits earlier,
   and local HEAD was a5e240ca. R-0520's shape — a working-copy claim about a file the same
   block rewrites, carrying no SHA.
The same sweep re-measured what this round registers; both reproduce exactly: R-0531's
counts (SEAMTESTS 47 lines; empty 12x, `    )` 4x, the argument line 3x,
`@pytest.mark.subprocess` 2x among dce66faa's added lines) and R-0532's premise (`git
ls-tree origin/main` empty for both paths). Re-read after C2: the four paths in G7.
Length 114 lines under DECISION D15, stated cause: the mandated content does not fit 60 —
five per-commit tables (20 lines), the item-status table (8), the seven-gate verification
table with real values (23), the verbatim Fortschritt line (4) and the verbatim R41 note
(8). R39's handback measures 185 lines at d3a707f5.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). R40's own verdict is NOT a §4.13 terminator,
because this branch continues; the next reviewed round records R40's gate entry.

  R41 migrates `packages/orchestration/ci_run.py` onto the seam, passing the per-stage
  budget through the `extra_env` overlay that landed at dce66faa. It still owes its own
  DECISION on where the stage output goes: at d3a707f5 `_run_via_subprocess` streams
  straight to the console and returns only the returncode, while the seam CAPTURES both
  streams, so the migration changes observable behaviour rather than preserving it. That
  decision is the round's own work and belongs in `.agent/decisions.md` before any line
  changes. `packages/orchestration/builder_bridge.py` follows it; then T002c-d, then
  T003 and the integration gate.
