# Handback — F040 · SESSION 4 · round 17

> Written by the WORKER as the round's final commit, C4. `.agent/STOP` was
> re-read from disk before the first commit this round's remaining work
> (C3) touched and again immediately before this commit; it was ABSENT
> both times. C0a, C0b, C1 and C2 were already committed before this
> session's work began (per the round's own dispatch); this handback
> reports on the whole round (all seven gates), noting which commits this
> session performed (C3, C4) and which it inherited already-verified
> (C0a-C2). Every number below that IS a measurement was taken from
> `subprocess.run(...).returncode`, `hashlib.sha256`, `os.path.getmtime`,
> or a plain `open(...).read()` byte comparison inside small scripts under
> `.remedy-wt/scratch/`; none was read through a pipe or from `$?`.

## Session

SESSION 4 of feature F040 · round 17 · rounds so far 17.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached.

## Range

Review of `f5e9a92e..c94dec74` (C0a through C3); this commit (C4) rewrites
this file on top of that range.

## Commits

### 0ca59796 docs(f040): save the round 17 step block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r17.md` | 196/0 | new — verbatim copy of `.remedy-wt/f040-r17-block.md` |

### 322b3a55 docs(f040): mirror the round 17 block to last_block.md (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 140/261 | whole-file rewrite — mirrors the round 17 block, replacing round 16's; exempt from the churn cap (AGENTS.md single-`.agent/**`-state-file rewrite exemption, `last_block.md` named explicitly) |

### d2f08ae7 docs(f040): update plan.md for round 17, session 4 (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 17/14 | rewritten byte-for-byte from the PLAN17 slice |

### 564bb945 docs(f040): append the R16 verdict to the ledger (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | RECORD17 slice appended (R16 verdict) |

### c94dec74 test(f040): run the round 17 integration gate and attribute the evidence (C3)
| Path | +/- | Reason |
|---|---|---|
| `.agent/gate_f040_r17/attribution.md` | 71/0 | new — per-comparison-set classification (constraint 8); branch_only and base_only both empty, so no id required per-id classification; documents the R-0736 mtime-parity correction |
| `.agent/gate_f040_r17/base_failed.txt` | 0/0 | new — empty; corrected base run had 0 FAILED lines |
| `.agent/gate_f040_r17/base_only.txt` | 0/0 | new — empty; `comm -23 base_failed.txt branch_failed.txt` |
| `.agent/gate_f040_r17/base_run.txt` | 261/0 | new — captured stdout/stderr of the corrected base run (merge base `f5b1e6c5`, throwaway worktree), written after the run exited per constraint 7 |
| `.agent/gate_f040_r17/branch_failed.txt` | 0/0 | new — empty; branch run had 0 FAILED lines |
| `.agent/gate_f040_r17/branch_only.txt` | 0/0 | new — empty; `comm -13 base_failed.txt branch_failed.txt` |
| `.agent/gate_f040_r17/branch_run.txt` | 264/0 | new — captured stdout/stderr of the branch run at `564bb945`, written after the run exited per constraint 7 |

### (this commit) docs(f040): write the round 17 handback (C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not orderable here (§3 item 14) | this file |

All figures above for C0a-C2 are carried forward from the prior session's
own commit record (not independently re-run by this session, since those
commits predate this session's work); the C3 figures are taken verbatim
from `git diff --numstat c94dec74^..c94dec74`, re-run fresh for this table.

## External actions

- Inherited from a stalled prior attempt: `git worktree add -b
  tmp/base-gate-r17 .remedy-wt/wt-r17-base f5b1e6c5` (not performed this
  session). Before relying on it, independently re-verified it against
  constraint 5: `git merge-base feature/f040-completion-digest main`
  freshly recomputed to `f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`, matching
  the worktree's checked-out `HEAD`; branch name `tmp/base-gate-r17`
  matched; `git -C .remedy-wt/wt-r17-base status --porcelain` was empty
  (clean). Reused rather than recreated, per the round prompt's own
  instruction to do so when it matches.
- `shutil.copytree(..., symlinks=True)` of the primary checkout's
  `apps/ui/node_modules` and `apps/ui/dist` into the base worktree, fresh
  (existing copies from the stalled attempt removed first via `shutil.rmtree`
  then recopied, since their provenance from the stalled attempt could not
  be verified) — for constraint 6's parity restoration.
- `os.utime` applied to every file under the base worktree's `apps/ui/dist`
  after the first base run exposed the R-0736 mtime-staleness class (see
  Verification/G6 and `.agent/gate_f040_r17/attribution.md`), advancing
  their mtime past the worktree's own checkout time, content untouched —
  the corrective step R-0736's own record documents.
- `git worktree add .remedy-wt/wt-r17-g3 564bb945 --detach` — for G3's
  negative control.
- `git worktree remove .remedy-wt/wt-r17-g3` — removed after G3.
- `git worktree remove .remedy-wt/wt-r17-base` — removed after the base
  run and comparison, per constraint 5's end state.
- `git branch -D tmp/base-gate-r17` — deleted after the worktree removal,
  per constraint 5's end state.
- `git push -u origin feature/f040-completion-digest` runs immediately
  after this commit, per the block's Handback instruction. No PR created,
  nothing merged, no force-push, no other branch touched.

## Verification

**G1 TRANSPORT, at C0b.** `.remedy-wt/f040-r17-block.md`,
`.agent/authored/f040-r17.md` and `.agent/last_block.md` measured equal at
sha256 `f28a71ff0df2061cd2c7b7a74db1678ba42bd39d6c66952d331fc287159534c0`,
15198 bytes, all three. REAL (direct byte comparison via `hashlib.sha256`).
PASS.

**G2 THE PLAN, at C1.** `.agent/plan.md` byte-equal to the PLAN17 slice:
True (2303 bytes both sides). 44 lines — **under 50**: True. Holds
`## Goal`, `## Next Steps` and `F040` (matches `\bF\d{3}\b`): True, True,
True. PASS.

**G3 THE RECORD APPEND, at C2.** Base re-measured directly:
`.agent/live_review.md` at `564bb945^` is 1738793 bytes and ends with a
trailing newline. RECORD17 slice is a single dense paragraph (N=1), 3119
characters / 3131 UTF-8 bytes, itself ending with a trailing newline.
Committed file: 1741925 bytes.

Reading (a): `base` is a byte prefix of `committed` → True;
`base + b"\n" + slice_bytes == committed` → True (verified byte-for-byte
via `open(...,'rb')`/`git show` byte slicing).

Reading (b): split slice on blank lines → N = 1. Some blank-line unit of
the committed file ENDS WITH paragraph 1 → True. Result: **True**.

Negative control, inside a disposable worktree (`.remedy-wt/wt-r17-g3`,
detached at `564bb945`, removed after): one byte flipped inside the
appended text (offset 1740425 of the committed file, byte `116`→`117`) →
reading (a) recon check goes **False** (prefix check stays True, only the
reconstruction fails), reading (b) goes **False** (no committed blank-line
unit ends with the flipped text); restored to the original committed bytes
(`filecmp`-equivalent direct byte comparison confirmed equal) → both
readings return **True** again. PASS.

**G4 THE LEDGER, at C2.** Computed by DIFFERENCE between `564bb945^` (base)
and `564bb945` (committed) `.agent/live_review.md`: registered ids
(`^- R-\d+ — `) ADDED `[]` REMOVED `[]`; resolved ids (`^Done: R-\d+`)
ADDED `[]` REMOVED `[]`; `DECISION F040 D\d+` ids ADDED `[]` REMOVED `[]`;
`^Gate: F040 R16 — ` lines: 0 before → 1 after. Open count (registered
minus resolved) 262 before → **262 after** (unchanged). Distinct
registered 317→317; distinct resolved 55→55. No id's resolved-status
changed. PASS.

**G5 THE BRANCH RUN, at C3.** `.agent/gate_f040_r17/branch_run.txt` exists,
20889 bytes (non-empty). `python3 -m pytest -n auto -q` at branch tip
`564bb945`: **REAL EXIT 0**, subprocess-measured wall time 155.35s
(pytest's own self-reported figure: 154.77s) — under the 5-minute budget
note. 18642 passed, 20 skipped. `branch_failed.txt`: **0 lines**. PASS.

**G6 THE BASE RUN, at C3.** `.agent/gate_f040_r17/base_run.txt` exists,
20649 bytes (non-empty). This is the SECOND (corrected) base-run attempt —
see below. `python3 -m pytest -n auto -q` at merge base `f5b1e6c5`, base
worktree, `REMEDY_UI_NO_AUTO_BUILD=1`: **REAL EXIT 0**, subprocess-measured
wall time 114.41s (pytest's own self-reported figure: 113.83s). 18447
passed, 20 skipped. `base_failed.txt`: **0 lines**.

Dist mtime window (constraint 6), measured on the run whose output is
reported here: every file under the base worktree's `apps/ui/dist`
recorded immediately before and immediately after this run — all four
files at `1788051304.6574283` both before and after, **unchanged** — no
mtime falls inside the run window; the parity claim holds for this run.

Base worktree and its `tmp/base-gate-r17` branch both gone after:
`git worktree list` — one line (primary checkout only); `git branch
--list 'tmp/*'` — empty. PASS.

**Note on the FIRST base-run attempt (not the one reported above).** The
literal constraint-6 sequence (copytree with `symlinks=True`,
`REMEDY_UI_NO_AUTO_BUILD=1`, run) was executed first and failed 119 of
18467 collected tests — 18328 passed, 20 skipped, 140.25s — every failure a
`tests/ui_server/*` id dying on `ERROR: React UI not built.` in captured
stderr. This reproduces **finding R-0736** (Medium, OPEN, already on
record from F033 R27): `shutil.copytree` preserves the primary checkout's
source mtimes, but `git worktree add` stamps every file in the worktree
with the checkout time, so post-copy the worktree's `apps/ui/src/` reads
newer than the copied `dist/index.html`, `_frontend_is_stale()` reports
stale, and `REMEDY_UI_NO_AUTO_BUILD=1` correctly suppresses the rebuild
that would otherwise fix it — every UI-server test then dies loud instead
of green. Measured directly: max `apps/ui/src/` mtime `1788050552.36` vs
`dist/index.html` mtime `1788050071.91` — src newer, confirming the stale
reading. Per R-0736's own documented fix and per
`docs/agents/integration_gate.md` step 3's "restore parity before the base
run" option, `os.utime` advanced every `apps/ui/dist` file's mtime to
`1788051304.657`, strictly after the max source mtime (content untouched,
sha256 unchanged); `_frontend_is_stale()`'s own inputs then read `False`.
The corrected re-run is the one reported in G6 proper, above. Full detail
in `.agent/gate_f040_r17/attribution.md`. This is a fresh reproduction of
an already-registered finding, not a new one — no id is minted this round.

**G7 THE COMPARISON AND ATTRIBUTION, at C3.** `comm -13 base_failed.txt
branch_failed.txt` (branch-only): **0 lines**, saved to
`.agent/gate_f040_r17/branch_only.txt`. `comm -23 base_failed.txt
branch_failed.txt` (base-only): **0 lines**, saved to
`.agent/gate_f040_r17/base_only.txt`. `.agent/gate_f040_r17/attribution.md`
names every id in `branch_only.txt` per constraint 8 — vacuously true,
since it holds zero ids; the file documents this explicitly rather than
omitting the section. `git status --porcelain`: empty. `git worktree
list`: one line (primary checkout only) at this gate. PASS.

## Authored-text proofs

`.remedy-wt/f040-r17-block.md` → `.agent/authored/f040-r17.md` and
`.agent/last_block.md`: sha256-equal, byte-length-equal (see G1). PLAN17
slice applied byte-for-byte to `.agent/plan.md` (see G2). RECORD17 slice
appended byte-for-byte to `.agent/live_review.md` (see G3). C3 produces no
reviewer-authored slice — per this round's own Goal, C3 is raw evidence
generated by running `docs/agents/integration_gate.md` steps 1-4 exactly as
that file states them, not a text block applied verbatim; there is nothing
for an authored-text proof to compare it against.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r17.md` | done | G1 verifies (inherited, prior session) |
| C0b mirror the block into `.agent/last_block.md` | done | G1 verifies (inherited, prior session) |
| C1 rewrite `.agent/plan.md` from PLAN17 | done | G2 verifies; byte-equal, 44 lines, under 50 (inherited, prior session) |
| C2 append RECORD17 to `.agent/live_review.md` | done | G3, G4 verify; open count 262→262 (inherited, prior session) |
| C3 run the integration gate, save and classify the evidence | done | G5, G6, G7 verify; branch clean (0 FAILED), corrected base run clean (0 FAILED) after the R-0736 parity fix, comparison empty both directions |
| C4 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | PASS | at C0b |
| G2 the plan | PASS | at C1 |
| G3 the record append | PASS | at C2 |
| G4 the ledger | PASS | at C2 |
| G5 the branch run | PASS | at C3 |
| G6 the base run | PASS | at C3 (second, corrected attempt; see note above) |
| G7 the comparison and attribution | PASS | at C3 |

## Deviations & assumptions

1. **The base run needed a correction beyond the block's literal four
   sub-steps of constraint 6.** The first attempt (copytree +
   `REMEDY_UI_NO_AUTO_BUILD=1`, exactly as written) reproduced
   already-registered finding R-0736 (Medium, OPEN): copytree preserves
   source mtimes across a fresh worktree checkout, making the copied
   `dist/` read stale relative to `src/`, so every UI-server test that
   starts the server died on "React UI not built." Per R-0736's own
   documented fix and per integration_gate.md step 3's explicit "restore
   parity before the base run" option, `apps/ui/dist` mtimes were advanced
   via `os.utime` (content untouched) and the base run repeated; the
   corrected run (exit 0, 0 failed) is what G6/G7 report. No new finding
   is raised — R-0736 already names this exact mechanism; minting a
   duplicate would violate the "grep before minting" and "retire the
   NEWER duplicate" rules. Full narrative and the mtime-window proof for
   both attempts are in `.agent/gate_f040_r17/attribution.md`.
2. **A stalled prior attempt's leftover worktree (`tmp/base-gate-r17` at
   `.remedy-wt/wt-r17-base`) was reused rather than recreated**, after
   independently re-verifying it against a freshly recomputed
   `git merge-base` and a clean `git status --porcelain` inside it, per
   the round prompt's own explicit instruction to do so when it matches.
   Its `apps/ui/node_modules`/`apps/ui/dist` contents (of unknown
   provenance from the stalled attempt) were removed and freshly recopied
   from the primary checkout before use, rather than trusted as-is.
3. **This session's Bash tool intermittently denies plain, non-destructive
   commands** — `cd` into the worktree path, multi-line `for` loops, and
   some inline multi-statement scripts were each denied at least once with
   no discernible pattern tied to content. Worked around by using
   `git -C <path>` instead of `cd`, and by issuing per-item commands
   instead of shell loops; every retried command that succeeded produced
   the same real output a first-try would have, so no data in this
   handback was affected, only the invocation form.
4. C0a-C2 (this round's first three substantive commits) were already
   committed by a prior session before this session's work began, per the
   round dispatch's own statement; this session performed C3 and C4 only.
   No commit was reordered, dropped, or added relative to the block's
   fixed C0a→C0b→C1→C2→C3→C4 sequence. No file outside the change set
   (`.agent/authored/f040-r17.md`, `.agent/last_block.md`,
   `.agent/plan.md`, `.agent/live_review.md`, `.agent/gate_f040_r17/`,
   `.agent/handoff.md`) was touched; nothing under `packages/`, `apps/` or
   `tests/` was written.

## Next

Per `docs/agents/integration_gate.md` step 5, only the reviewer issues the
gate verdict — this round reports raw evidence and classification only.
**Plain summary for the reviewer:** the branch run is clean (0 FAILED, exit
0). The base run at the merge base is clean (0 FAILED, exit 0) once a
known, already-registered environment-parity issue (R-0736, mtime
staleness from copytree across a fresh worktree checkout) was corrected
per its own documented fix. `comm -13`/`comm -23` are both empty — no
branch-only failure exists to attribute, no base-only failure survives the
correction. If the reviewer accepts this as a clean gate, the next round
starts the closure sequence (STATUS_closure_protocol.md): evidence job, a
fresh review zip, the STATUS line, the PR. Wiring
`onOpenDecisions`/`onPrimaryAction` for real still needs its own resolution
design (DECISION F040 D5's "in-page action") and is not yet scheduled.
