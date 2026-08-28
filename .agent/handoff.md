# Handback — F037 R8 (T002 preparation)

## Session

SESSION 2 of feature F037 · round 8 · rounds so far 8

## Range

Review of `996ffea91883543ad9b10d5aac621b12b6c71c15`..`HEAD` (base = `996ffea9`,
branch `feature/f037-rendered-diff-viewer`). Six commits: C0a, C0b, C1, C2, C3
and this handback commit C4.

## Commits

### 7f4c9af4 docs(agent): save the F037 R8 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r8.md | +331/-0 | C0a — the block saved verbatim, 26615 bytes |

### 6cddb842 docs(agent): mirror the F037 R8 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +252/-285 | C0b — the C0a blob mirrored; same blob hash |

### 1d53b2d2 docs(agent): point the plan at the F037 R8 preparation round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +24/-23 | C1 — whole-file replacement by slice PLANF037R8 |

### 345235ca docs(agent): book the R7 verdict, resolve R-0715 and register R-0719
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +5/-1 | C2 — pair DONE715PAIR, then appends GATER7 and R0719 |
| .agent/prose_slips.md | +9/-0 | C2 — append SLIPR8 |

### c60a7318 docs(f037): name the diff surface design authority in amendment A4
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T5_F037.md | +27/-0 | C3 — append AMEND4 |
| .agent/decisions.md | +31/-0 | C3 — append DECISION3 (F037 D3) |

### C4 (this commit) docs(agent): hand back F037 R8
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | n/a | C4 — a handback cannot table the commit that writes it |

Every `+/-` cell above is taken from `git diff --numstat <sha>^ <sha>` and
agrees cell for cell with the per-commit reading recorded under G8.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  (Open PR Gate; no PR created, nothing merged).
- `git push origin feature/f037-rendered-diff-viewer` — ordered AFTER C4 and
  deliberately outside every gate; its result is not named here, the reviewer
  reads the remote tip itself.
- No worktree added or removed. `git worktree list` = 1 line.

## Verification

**G1 hygiene — PASS.** `.agent/STOP` ABSENT before C0a and ABSENT again before
C4. `git rev-parse HEAD` before C0a = `996ffea91883543ad9b10d5aac621b12b6c71c15`
= the base. `git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain` line count after C0a 0, after C0b 0, after C1 0, after
C2 0, after C3 0.

**G2 transport, one digest comparison — PASS.** After C0a:
`.agent/authored/f037-r8.md` sha256
`08668ffb1740a26e53b777dca18582b2e2376d516a9705aad998bab49254ad37`, 26615 bytes,
331 lines. After C0b: `git rev-parse HEAD:.agent/authored/f037-r8.md` =
`9d388a211da7a2c6190f64a1eb33a315767f5f06` and
`git rev-parse HEAD:.agent/last_block.md` = `9d388a211da7a2c6190f64a1eb33a315767f5f06`
— the SAME blob hash. This chain covers the saved copy, its mirror and the
working copy only. It claims nothing whatever about the bytes of any prompt.

**G3 extraction and caps — PASS.** Every slice extracted from the COMMITTED C0a
blob by its marker lines: PLANF037R8 50, DONE715PAIR 4, GATER7 1, R0719 1,
SLIPR8 8, AMEND4 26, DECISION3 30. TOTAL 331, CONTENT 120, PROSE = 331 − 120 =
211. PROSE 211 ≤ 400 and TOTAL 331 ≤ 490.

**G4 the plan at C1 — PASS on byte equality, FAIL on the line-count clause; see
Deviations.** `.agent/plan.md` byte-equal to PLANF037R8 under the
newline-included convention: **True**. NEGATIVE CONTROL against the slice minus
its trailing newline: **False**. `^## Goal$` 1, `^## Next Steps$` 1.
`wc -l .agent/plan.md` = **50**, which is NOT strictly under 50 — the slice as
authored is exactly 50 lines and constraint 1 forbids editing it.

**G5 the record at C2 — PASS.**
- PAIR: FROM count before 1, after 0. TO count before 0, after 1.
- Base sizes measured: `.agent/live_review.md` 1166346 bytes (block states
  1166346 — MATCH); `.agent/prose_slips.md` 8424 bytes (block states 8424 —
  MATCH).
- GATER7: reader (a) BYTE IDENTITY `result == before + b"\n" + slice` → True,
  re-read FROM DISK after the commit. Reader (b), N counted by the script as 1
  blank-line unit, last 1 unit == the slice's unit in order → True. NEGATIVE
  CONTROL, one byte flipped inside the FIRST appended paragraph: reader (a)
  False AND reader (b) False.
- R0719: reader (a) byte identity → True (from disk). Reader (b) N=1 → True.
  NEGATIVE CONTROL: reader (a) False, reader (b) False.
- SLIPR8: reader (a) byte identity → True (from disk). Reader (b) N=1 → True.
  NEGATIVE CONTROL: reader (a) False, reader (b) False.
- Additional whole-file reading on the final `.agent/live_review.md`: the last
  TWO blank-line units are [GATER7, R0719] in that order → True.
- COUNTS after C2, line-anchored, measured: `^- R-\d+ — ` **280** (ordered 280);
  `^Done: R-\d+ — ` **28** (ordered 28); `^Landed: R-` **1** (ordered 1);
  `^Gate: F\d+ R\d+ — ` **78** (ordered 78).
- ids ADDED: exactly `R-0719`. ids newly RESOLVED: exactly `R-0715`. All ids
  DISTINCT: True. Maximum id: `R-0719`. Open set size: **252** (unmoved — one
  minted, one resolved). The `Landed: R-0711` line was not touched and no
  existing `Done:` paragraph was touched.

**G6 the two docs appends at C3 — PASS.**
- AMEND4 → `docs/roadmap/features/T5_F037.md`: base measured **7981** bytes
  (block states 7981 — MATCH). Reader (a) byte identity from disk → True.
  Reader (b), N counted by the script as **3** blank-line units, last 3 units ==
  the slice's 3 units in order → True. NEGATIVE CONTROL: reader (a) False,
  reader (b) False.
- DECISION3 → `.agent/decisions.md`: base measured **655420** bytes (block
  states 655420 — MATCH). Reader (a) byte identity from disk → True. Reader (b),
  N = **5** units → True. NEGATIVE CONTROL: reader (a) False, reader (b) False.
- `^## DECISION ` in `.agent/decisions.md`: **168** before C3, **169** after C3.
  `F037 D3` occurs exactly **1** time in that file after C3.
- `^<<<SLICE ` / `^<<<END ` after C3: 0 / 0 in
  `docs/roadmap/features/T5_F037.md` and 0 / 0 in `.agent/decisions.md`.

**G7 THE PROBE — ANSWERED. THE FRONTEND TEST RUNNER CANNOT BE EXECUTED IN THIS
ENVIRONMENT. All three routes were REFUSED; none ran; there is NO vitest result
for this round and none is claimed, estimated or inferred.**

| # | Exact command | RAN or REFUSED | Result / refusal, verbatim |
|---|---------------|----------------|----------------------------|
| 1 | `npx vitest run --root apps/ui` | REFUSED | `This command requires approval` |
| 2 | `npm --prefix apps/ui run test:unit` | REFUSED | `This command requires approval` |
| 3 | `apps/ui/node_modules/.bin/vitest run --root apps/ui` | REFUSED | `This command requires approval` |

No exit code exists for any of the three: the environment refused each before
execution. No other route to the runner was attempted, nothing was installed and
nothing was modified to make it run — as the block ordered. This matches the
reviewer's own three refusals, so the refusal is reproducible across both roles.

The two commands in this gate that DO run:
- `python3 -m pytest tests/docs/ -q` → exit code **0**, `295 passed in 0.44s`.
  Base figure 295 passed — MATCH, no difference to report. Required because this
  round's change set includes `docs/roadmap/**`.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → exit code **0**,
  `42 passed in 20.66s`. Base figure 42 passed — MATCH, no difference to report.

**G8 structure, artifacts and the Open PR Gate, at C3 — PASS.**
- `git diff --name-only 996ffea9..c60a7318` = `.agent/authored/f037-r8.md`,
  `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `docs/roadmap/features/T5_F037.md`. Residue actual − expected: **[]**.
  Residue expected − actual: **[]**.
- Restricted `git diff --stat`: `apps/` EMPTY, `packages/` EMPTY, `tests/`
  EMPTY; `docs/` holds only `docs/roadmap/features/T5_F037.md | 27 +++`.
- Per-commit `git diff --numstat`, single-parent and under 500 insertions:
  C0a `7f4c9af4` +331/-0, 1 parent, under 500 True;
  C0b `6cddb842` +252/-285, 1 parent, True;
  C1 `1d53b2d2` +24/-23, 1 parent, True;
  C2 `345235ca` +14/-1, 1 parent, True;
  C3 `c60a7318` +58/-0, 1 parent, True.
  C4 is deliberately not counted — its own count cannot exist while its text is
  being written.
- The `^<<<SLICE ` / `^<<<END ` counter over the C0a blob measures **7** and
  **7**, i.e. 14 marker lines, greater than zero — so the zero-counts reported
  in G5 and G6 come from a sweep that is demonstrably not blind.
- `git ls-files .remedy-wt` line count **0**. `git worktree list` line count
  **1** — no worktree was opened; this round runs no destructive verification.
- Open PR Gate, verbatim: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  → `[]`.

## Authored-text proofs

Every one of the seven authored texts was extracted IN PYTHON from the COMMITTED
C0a blob (`git show HEAD:.agent/authored/f037-r8.md`) by its marker LINES and
applied byte for byte; none was retyped and none was edited.

| Slice | Target | Proof |
|-------|--------|-------|
| PLANF037R8 | `.agent/plan.md` | whole-file byte equality True; negative control False (G4) |
| DONE715PAIR | `.agent/live_review.md` | FROM 1→0, TO 0→1; `TO contains FROM` False as stated (G5) |
| GATER7 | `.agent/live_review.md` | append byte identity from disk True; control False (G5) |
| R0719 | `.agent/live_review.md` | append byte identity from disk True; control False (G5) |
| SLIPR8 | `.agent/prose_slips.md` | append byte identity from disk True; control False (G5) |
| AMEND4 | `docs/roadmap/features/T5_F037.md` | append byte identity from disk True; control False (G6) |
| DECISION3 | `.agent/decisions.md` | append byte identity from disk True; control False (G6) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | 331 lines, sha256 `08668ffb…` |
| C0b mirror into last_block | done | same blob `9d388a21…` |
| C1 the plan | done | byte-equal to PLANF037R8 |
| C2 the record | done | pair + GATER7 + R0719 + SLIPR8, all four counts as ordered |
| C3 the two docs appends | done | AMEND4 and DECISION3 |
| C4 the handback | done | this file |
| Push after C4 | done | ordered outside every gate; result not named here |
| G1 hygiene | done | STOP ABSENT twice; base SHA matched; five clean-tree readings at 0 |
| G2 transport | done | one digest comparison; blob hashes identical |
| G3 extraction and caps | done | TOTAL 331, CONTENT 120, PROSE 211 |
| G4 the plan | deviated | byte equality and both header counts as ordered; `wc -l` = 50 is NOT strictly under 50 and the slice cannot be edited — see Deviations |
| G5 the record | done | every reading matched the ordered value exactly |
| G6 the docs appends | done | every reading matched the ordered value exactly |
| G7 the probe | done | ANSWERED: all three runner routes REFUSED; docs gate and canary both exit 0 at their base figures |
| G8 structure and Open PR Gate | done | both residues empty; `apps/`, `packages/`, `tests/` empty; PR list `[]` |

## Deviations & assumptions

1. **G4's `wc -l` strictly-under-50 clause could not be met, and was not
   worked around.** Slice PLANF037R8 is exactly **50** lines as authored. The
   gate orders BOTH byte equality with the slice AND `wc -l` strictly under 50,
   and those two cannot both hold; constraint 1 says "never retype a slice,
   never edit a slice". The worker kept the byte equality — it is the property
   that proves the plan on disk is the plan the reviewer wrote — and reports the
   line count as measured rather than trimming the reviewer's text to make a
   number green. Consequence on disk: `.agent/plan.md` is 50 lines, one line
   over the `<50` rule in AGENTS.md ("### plan.md → keep it short (<50 lines)").
   This is a one-line overage in a `.agent/` prose file; nothing else on disk is
   affected. REPAIR BELONGS TO THE NEXT BLOCK: cut one line from the next
   round's plan slice before it is emitted. No id was minted for it — no id was
   ordered, and per amend0827 rule 2 an authoring inaccuracy of the reviewer's
   own prose is not an R-id class — and no unordered line was added to
   `.agent/prose_slips.md`, whose only ordered append this round is SLIPR8.
2. **No commit was added, dropped or reordered.** The bundle ran exactly C0a,
   C0b, C1, C2, C3, C4 in the ordered sequence, one commit each.
3. **No assumption_log entry was needed.** Nothing under `apps/`, `packages/`,
   `tests/`, `docs/roadmap/ROADMAP.md` or `docs/roadmap/STATUS.md` was touched,
   and no TypeScript, TSX or CSS was written, exactly as constraints 7 and 8
   ordered.

## Next

**THE FRONTEND TEST RUNNER CANNOT BE EXECUTED IN THIS ENVIRONMENT: all three
ordered routes — `npx vitest run --root apps/ui`,
`npm --prefix apps/ui run test:unit` and
`apps/ui/node_modules/.bin/vitest run --root apps/ui` — were REFUSED by the
environment with the message `This command requires approval`, none of them ran,
and no vitest result exists for this round. Ordering `.ts`, `.tsx` or `.css`
under `apps/` in the next round would produce code that NEITHER the worker NOR
the reviewer can execute, and therefore cannot be verified or certified.**

The first action of the next round is to re-read `.agent/STOP` from disk
(Phase 1 rule 1 — the sentinel binds at any point, not only at session start).
Then the Open PR Gate:
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
returned `[]` at C3 of this round.

Then the reviewer decides the shape of the round on the G7 answer above. The
plan's step 1 states both branches: if the runner can be granted, T002's
rendering core lands as a pure `.ts` view-model beside its `.test.ts`; if it
cannot, the session hands off asking the operator to grant execution of the
frontend runner, and orders no UI code. Open findings: 252, with `R-0719` newly
registered and OPEN and `R-0715` resolved.
