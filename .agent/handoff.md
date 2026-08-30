# Handoff — F258 Self-use track v2

## Session

SESSION 1 of feature F258 · round 1 · rounds so far 1.

## State

Branch `feature/f258-self-use-v2`, cut from `main` at `18ae71293cde9b1157aca35d3d02c3a8f4265813`
(the merge commit of pull request 225, F040's closure). Last commit on this
branch before the handback write is `b7da7f3db6589c80bdff02207b1b3a76a701ccb2`
("measure F258 queue/planner/execution/budget/ledger seams"). This round
opens the feature: it discharges the one closure candidate F040's closure
gate left, claims F258 `[~]` in progress on the STATUS ledger, and measures
the queue/planner/job-execution/budget/approval seams T001-T003 will compose
over, in `.agent/f258_inventory.md`. No production code and no test changed —
the change set is `.agent/**` plus one line of `docs/roadmap/STATUS.md`.
Open findings count in `.agent/live_review.md`: 317 registered, 55 distinct
resolved (`Done:`), 262 open. R-0570 stays OPEN (0 `Done: R-0570` lines) and
is routed to the paydown branch, not to this feature.

## Range

Review of `18ae71293cde9b1157aca35d3d02c3a8f4265813..b7da7f3db6589c80bdff02207b1b3a76a701ccb2`.

## Item status

Every bundle item and every gate, each appearing exactly once:

| Item | Status | Reason |
|------|--------|--------|
| C0a save block to `.agent/authored/f258-r1.md` | done | `shutil.copyfile`, sha256-verified |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`, sha256-verified |
| C1 rewrite `.agent/plan.md` from PLAN1 | done | byte-equal, 44 lines |
| C2 append RECORD1 to `.agent/live_review.md` | done | append-only, proved by reconstruction |
| C3 rewrite `.agent/candidates.md` from CAND1 | done | byte-equal, candidate discharged |
| C4 apply PAIR-STATUS to `docs/roadmap/STATUS.md` | done | exactly one FROM→TO |
| C5 rewrite `.agent/context.md` from CONTEXT1 | done | byte-equal |
| C6 write `.agent/f258_inventory.md` | done | measurement, six SPEC sections, 60 citations |
| C7 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | done | exit n/a (sha256 comparison), all three equal |
| G2 the plan | done | byte-equal, 44 lines |
| G3 the record append | done | reconstruction + paragraph order + negative control, all as expected |
| G4 the ledger | done | added registered/resolved both empty, DECISION F258 empty, R-0570 Done count 0 |
| G5 the candidates file | done | byte-equal, stale marker count 0 |
| G6 the claim and the docs pins | done | numstat 1/1, two suites exit 0 (295, 30 passed) |
| G7 the state readers and the canary | done | five suites exit 0 (515, 52, 21, 16, 42 passed) |
| G8 the inventory and the tree | done | six headings present, 60 citations, tree clean, all commits under 500 |

## Commits

All `+/-` figures are `git diff --numstat` against each commit's own parent,
per this round's own re-measurement (see Deviations — the message `git commit`
echoed at commit time for C1 read differently and the numstat reading below is
the one this handback uses, per the block's own instruction to source the
Commits table from `git diff --numstat`).

### e2e9724c add authored block for F258 round 1
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f258-r1.md` | 365/0 | C0a — verbatim copy of the round's step block, `shutil.copyfile` |

### a81cbe43 mirror F258 round 1 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 365/127 | C0b — verbatim copy of the same block, `shutil.copyfile`, into the mirror slot |

### 03e73a28 open F258 self-use track v2 plan
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | 32/38 | C1 — rewritten from slice PLAN1, byte-equal, 44 lines |

### 1d57ee0b append F258 record on R-0570 third occurrence
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 2/0 | C2 — RECORD1 appended verbatim; nothing earlier revised |

### 13e6fc24 discharge F040 closure candidate as R-0570 evidence
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/candidates.md` | 5/21 | C3 — rewritten from slice CAND1, byte-equal, candidate file emptied |

### 7b188ae0 claim F258 in progress on STATUS ledger
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | 1/1 | C4 — PAIR-STATUS applied, F258's line `[ ]` → `[~]` |

### fdb74bc2 rewrite context for F258 self-use track v2
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/context.md` | 27/19 | C5 — rewritten from slice CONTEXT1, byte-equal |

### b7da7f3d measure F258 queue/planner/execution/budget/ledger seams
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/f258_inventory.md` | 250/0 | C6 — new file, the round's own six-section measurement (SPEC), not an authored slice |

Not tabled per the template's self-reference exception: the commit that writes
this handback (C7, `.agent/handoff.md`) — its own numbers are the reviewer's
to measure at the next gate.

## External actions

- `git checkout -b feature/f258-self-use-v2` at `18ae71293cde9b1157aca35d3d02c3a8f4265813` — branch created.
- `git worktree add .remedy-wt/g3-check HEAD` — disposable worktree for the G3 negative control, detached at `b7da7f3d`.
- `git worktree remove .remedy-wt/g3-check --force` — removed after the negative control ran; `git worktree list` afterward shows only the primary checkout.
- `git push -u origin feature/f258-self-use-v2` — pushed after this handback's commit (see below). No pull request opened, per constraint 11 (round 1 of the feature; the PR is created at closure).
- No `gh pr` command run this round beyond the Open PR Gate check (`gh pr list --state open ...` → `[]`, empty, before branch creation).

## Verification

Every gate below ran with a REAL exit code captured via `subprocess.run(...).returncode`
inside `.remedy-wt/run_gates.py`, `.remedy-wt/g4_ledger.py`, `.remedy-wt/g6_check.py`,
`.remedy-wt/g3_negative_control.py` and `.remedy-wt/check_paths.py` on disk under
the gitignored `.remedy-wt/`. `remedy` the console script was not needed this
round (no CLI invocation was required by any gate); where a CLI surface was
cited it was read as source, not run.

**G1 — TRANSPORT, at C0b.** sha256
`4285092d765124f143b48f3ec791eaa7eac8cf4e266c4c31fcfc72e424c5f11c` over 20439
bytes, computed identically over all three files: the scratch original
`.remedy-wt/f258-r1-block.md`, the committed `.agent/authored/f258-r1.md`, and
the committed `.agent/last_block.md`. All three equal.

**G2 — THE PLAN, at C1.** `.agent/plan.md` sha256
`86dad5fe0fa993cb96ca60b9a195562849ef20579837b7cbf12393ef7fc49265` and the
scratch slice `.remedy-wt/slice_PLAN1.txt` sha256
`86dad5fe0fa993cb96ca60b9a195562849ef20579837b7cbf12393ef7fc49265` — equal.
Line count 44 (< 50). Carries `## Goal` and `## Next Steps`.

**G3 — THE RECORD APPEND, at C2.** Base (measured at commit `03e73a28`, i.e.
C1) is 1751668 bytes — matches the reviewer's stated reading at `18ae7129`.
RECORD1 is 1375 bytes. 1751668 + 1 + 1375 = 1753044, and the committed
`.agent/live_review.md` after C2 is 1753044 bytes — equal.
(a) WHOLE RECONSTRUCTION: `base + b'\n' + record == committed` → `True`.
(b) PARAGRAPH ORDER: the committed file's last `\n\n`-delimited unit equals
RECORD1 exactly (both 1363 chars after removing the shared trailing newline
convention) → `True`, N=1, one dense paragraph.
NEGATIVE CONTROL, run inside the disposable worktree `.remedy-wt/g3-check`
(detached at `b7da7f3d`): flipped the `T` in "THIRD" inside the appended
paragraph to `X`. Both readings on the UNFLIPPED committed file: `True`,
`True`. Both readings on the FLIPPED file: `False`, `False` — both readings
correctly reject the flip and accept the original. Worktree removed after;
`git worktree list` now shows only the primary checkout.

**G4 — THE LEDGER, at C1 and at C2.**
- At C1 (`03e73a28`): 317 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+ — ` ids, open count 262.
- At C2 (`1d57ee0b`): 317 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+ — ` ids, open count 262.
- ADDED registered (C2 − C1): `[]`. ADDED resolved (C2 − C1): `[]`.
- Distinct `^DECISION F258 D\d+ — ` ids before and after: `[]`, `[]` — both empty.
- `^Done: R-0570` count: 0 before, 0 after.

**G5 — THE CANDIDATES FILE, at C3.** `.agent/candidates.md` sha256
`454ac5f45f58bb1662523e77a95b902704b3d2662bec80a2c30d53f0172579ed`, matching
the scratch slice `.remedy-wt/slice_CAND1.txt`'s sha256
`454ac5f45f58bb1662523e77a95b902704b3d2662bec80a2c30d53f0172579ed` — equal.
The string `· F040 · 2026-08-30` occurs 0 times in the committed file. Byte
length before C3: 1960. Byte length after C3: 695.

**G6 — THE CLAIM AND THE DOCS PINS, at C4.** In `docs/roadmap/STATUS.md`:
PAIRSTATUS-FROM (`- [ ] F258 — Self-use track v2 (self-replenishing queue &
executed items)`) occurs 0 times after C4; PAIRSTATUS-TO occurs exactly 1
time. `git diff --numstat` for C4 alone: `1  1  docs/roadmap/STATUS.md` —
exactly one insertion, one deletion. Count of lines matching
`^- \[~\] F\d{3} — ` in the whole file: 1.
- `python3 -m pytest tests/docs/ -q` → exit 0, `295 passed`.
- `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` → exit 0, `30 passed`.
Both match the reviewer's stated base reading (295, 30).

**G7 — THE STATE READERS AND THE CANARY, at C6.** All re-run at HEAD = `b7da7f3d` (C6):
- `python3 -m pytest tests/ui_server/ -q` → exit 0, `515 passed`.
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → exit 0, `52 passed`.
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → exit 0, `21 passed`.
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → exit 0, `16 passed`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed`.
All five match the reviewer's stated base readings (515, 52, 21, 16, 42) exactly.

**G8 — THE INVENTORY AND THE TREE, at C6.** `.agent/f258_inventory.md` exists
and carries all six SPEC sections, headings in order: `## 1. The queue schema
and its v1 contract`, `## 2. The planner seam`, `## 3. The closure consumption
point today — search for it and report the result`, `## 4. The job execution
path to "a real run"`, `## 5. The budget machinery for "a small dedicated
budget"`, `## 6. The finding ledger's own shape, for T003` (plus one extra,
non-mandated `## Absences, summarized` section). It cites 60 `file:line`
tokens (counted mechanically with a regex over backtick-quoted
`path:line[-line]` tokens); every one of the twelve distinct source paths it
cites resolves with `git ls-tree HEAD -- <path>`, checked individually for
each. `git status --porcelain` is empty; `git ls-files --others
--exclude-standard` has count 0. Per-commit insertion counts for C0a-C6 from
`git diff --numstat`: 365, 365, 32, 2, 5, 1, 27, 250 — every one under 500.

## Authored-text proofs

Five slices were applied this round, all via disk-to-disk `shutil`/exact-slice
copy rather than retyping, each verified byte-equal against the scratch
original at `.remedy-wt/f258-r1-block.md` before commit:

- C0a/C0b: the whole block, sha256
  `4285092d765124f143b48f3ec791eaa7eac8cf4e266c4c31fcfc72e424c5f11c`,
  20439 bytes — three-way equal (scratch original, `.agent/authored/f258-r1.md`,
  `.agent/last_block.md`).
- PLAN1 → `.agent/plan.md`: sha256
  `86dad5fe0fa993cb96ca60b9a195562849ef20579837b7cbf12393ef7fc49265` both sides.
- CAND1 → `.agent/candidates.md`: sha256
  `454ac5f45f58bb1662523e77a95b902704b3d2662bec80a2c30d53f0172579ed` both sides.
- CONTEXT1 → `.agent/context.md`: sha256
  `facf378f2ecb946e402baffbf440bd6082a71259a736ecf1dd4d6759bfa788ef` both sides.
- RECORD1 → appended to `.agent/live_review.md`: proved by reconstruction and
  paragraph-order equality, not by whole-file sha256 (it is an append, not a
  rewrite) — see G3 above.
- PAIR-STATUS (FROM/TO) → `docs/roadmap/STATUS.md`: proved by exact-string
  occurrence counts, not sha256 (a one-line pair inside a large file) — see G6
  above.

`.agent/f258_inventory.md` (C6) is NOT an authored slice — it is this round's
own measurement per the block's SPEC, so no fidelity comparison applies to it.

## Deviations & assumptions

1. **Commit-time diffstat vs. `git diff --numstat` for C1.** The text `git
   commit` echoed at the moment of the C1 commit read "44 insertions(+), 50
   deletions(-)" for `.agent/plan.md`. A fresh, independent `git diff
   --numstat 03e73a28~1 03e73a28` (and `git diff --stat` over the same range)
   both read `32  38` instead. I could not identify the cause — no
   `diff.algorithm` or `core.autocrlf` override is set in this repo's git
   config — and did not investigate further since the block's own gates (G8)
   specify `git diff --numstat` as the authoritative source for the Commits
   table, which is what this handback reports. Flagging it rather than
   silently picking one number, per §3's "recount on FINAL bytes" and "count
   mechanically" lessons. Not a finding against the content of `.agent/plan.md`
   itself — the file is confirmed byte-equal to PLAN1 by sha256 (G2), so the
   RESULT is not in question, only which of two diffstat readings for the
   same commit is trustworthy for the Commits table's `+/-` column.
2. **The `remedy` console script was not exercised this round.** No gate in
   this round's block required running it — every G6/G7 gate is a `pytest`
   invocation, and the C6 inventory's CLI citations were read as source
   (`apps/cli/command_catalog.py`, `apps/cli/commands/job.py`), not executed.
   Recording this per the task brief's standing instruction to declare the
   `remedy` sandbox-denial workaround whenever it would otherwise matter; this
   round never needed to invoke it either way.
3. **Slice content applied as given, not fixed.** Per constraint 1, several
   authored slices were applied byte-for-byte without correction even where
   something could be read as slightly odd — e.g. RECORD1's prose repeats
   "R-0570" and its own routing rationale at length, and CONTEXT1 restates
   standing constraints verbatim from a template comment about "an earlier
   round['s] red CI run" that is not this round's own history. Neither was
   altered; both are exactly the authored bytes.
4. **`.agent/f258_inventory.md`'s two Absences beyond the SPEC's six
   sections.** The SPEC asked for six sections and I added one extra
   "Absences, summarized" section at the end, restating the three most
   load-bearing absences already stated inline in sections 1, 3 and 4. This
   is additive, not a substitution for anything the SPEC required, and every
   one of the six mandated headings is present and in order (checked
   mechanically, reported in G8 above) — flagging the extra section so it
   is not mistaken for a missing one.
5. **Two ids in `.agent/live_review.md` carry a second `Done:` line.** G4's
   measurement noticed 57 raw `^Done: R-\d+` lines against only 55 DISTINCT
   ids — i.e., two ids already had a correction-round `Done:` line duplicated
   before this round started. This round did not touch `Done:` lines at all
   (ADDED resolved is `[]` both times measured), so it is pre-existing state,
   not something this round introduced; noted in `.agent/f258_inventory.md`
   §6 and here so it is not silently absorbed into "55" without the caveat.

## Next

Order T001 — the self-replenishing generator's source-priority logic and its
`provenance` field — from what `.agent/f258_inventory.md` measured this round:
there is no code caller of `plan_next_self_use_item` at any closure point
today, so T001's design starts from what precondition 6's manual step
currently does by hand (§3 of the inventory) rather than from an existing
hook. Push and Open PR Gate housekeeping for round 2 apply as usual; no PR is
open on this branch yet (none is created before closure, per constraint 11).
