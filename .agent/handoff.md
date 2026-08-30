# Handoff — F106 Session resume instead of rebuild

## Session

SESSION 1 of feature F106 · round 1 · rounds so far 1

## Range

Review of `811c2d7e..HEAD`.

## State

Branch `feature/f106-session-resume`, cut from `main` at `811c2d7e`
(current tip at round start, top commit "fix(ci): sort self_use_runner
test import, restore lint ceiling"). Phase-0 checks before branching:
`git status --porcelain` empty, `gh pr list --state open --json number,
headRefName,baseRefName,isDraft` returned `[]`, `.agent/STOP` absent,
`.agent/candidates.md` EMPTY. This is round 1 of a fresh feature claim — no
code changes ordered or made; only `.agent/` state, `docs/roadmap/
STATUS.md`, and the new measurement file `.agent/f106_inventory.md`.
Nothing under `packages/`, `apps/`, `tests/` or `docs/roadmap/features/`
was touched, matching the block's Change set exactly (8 named paths).

C0a/C0b saved and mirrored the round's block via `shutil.copyfile` (never
`cp`), byte-equal (18597 bytes each, `cmp` confirmed). C1 rewrote
`.agent/plan.md` from slice PLAN1 (sha256-equal, 39 lines, under the
50-line cap). C2 appended slice RECORD1 to `.agent/live_review.md` — base
measured at 1809603 bytes (matching the reviewer's own base reading),
append arithmetic and both G3 readings (whole reconstruction, paragraph
order) confirmed, negative control run inside a disposable `git worktree`
(removed after) rejected a one-byte-flipped copy on both readings and
accepted the unflipped one. C3 applied PAIR-STATUS to
`docs/roadmap/STATUS.md`: `[ ] F106` → `[~] F106`, exactly one insertion
and one deletion, FROM now occurs 0×, TO occurs 1×, and the whole file
holds exactly 1 line matching `^- \[~\] F\d{3} — `. C4 rewrote
`.agent/context.md` from slice CONTEXT1 (sha256-equal). C5 wrote
`.agent/f106_inventory.md`, the SPEC-driven measurement (not a slice) —
every citation in it was independently verified against the repository
(grep/read), not transcribed from the block's hypotheses; section 5 (the
repair loop's call sites) DRIFTED from a naive one-site reading —
`reviewer_provider.review(` actually has two call sites
(`pingpong_loop.py:3227` and `:3284`), not one — and is reported corrected
in the file itself. An unordered extra commit (`44c6847c`, declared under
Deviations) then corrected that file's own closing citation-count section
from a partial hand-count (19) to a complete, mechanically-extracted
enumeration (30 `file:line` pairs across 9 files) after I noticed the
hand-count had silently dropped several citations mentioned in the prose
(worker_registry.py:168/169, pingpong_loop.py:3284, etc.). This file (C6)
rewrites `.agent/handoff.md`.

Open findings count in `.agent/live_review.md`, measured before and after
C2: 318 registered `R-` ids (UNMOVED), 55 distinct resolved (`Done:`,
UNMOVED), open set = 263 (UNMOVED). No id was minted — constraint 5 held.
`DECISION F\d+ D\d+ — ` count: 19 before and after C2 (UNMOVED).

## Commits

All `+/-` figures are `git diff --numstat` against each commit's own
parent — NOT the number `git commit`'s own terminal summary prints (see
Deviations: that summary uses a rewrite-detection heuristic and printed
different, larger numbers for two of these commits).

### 3f712642 chore(f106): save round 1 authored block verbatim (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f106-r1.md | +344/-0 | `shutil.copyfile` from `.remedy-wt/f106-r1-block.md`, never retyped |

### 30960577 chore(f106): mirror round 1 block into last_block (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +328/-268 | `shutil.copyfile` from the committed `.agent/authored/f106-r1.md`; byte-equal to it (18597 bytes both, G1) |

### 4f5eec7a chore(f106): rewrite plan.md for round 1 (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +27/-22 | rewritten byte-for-byte from slice PLAN1 (sha256-equal, G2) |

### 335c2282 docs(f106): record F106 claim shape measurement in live review (C2)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | RECORD1 appended (base 1809603B + `\n` + 1164B slice = 1810768B, G3) |

### b603c9e3 docs(f106): claim F106 in STATUS.md (C3)
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | +1/-1 | PAIR-STATUS applied: F106's line `[ ]` → `[~]` (G5) |

### b33f5c4d chore(f106): rewrite context.md for round 1 (C4)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/context.md | +38/-47 | rewritten byte-for-byte from slice CONTEXT1 (sha256-equal, G6) |

### 11ccdb32 docs(f106): write round 1 shape inventory measurement (C5)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/f106_inventory.md | +206/-0 | new file, the SPEC-driven measurement, all 7 sections (G8) |

### 44c6847c docs(f106): correct inventory citation count to a mechanical enumeration (deviation — not in the block's bundle, see Deviations)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/f106_inventory.md | +37/-10 | replaced a hand-counted, incomplete 19-citation closing list with a mechanically-extracted, complete 30-citation one |

C6 (this commit, rewriting `.agent/handoff.md`) is not self-tabled, per
the handback template's self-reference exception.

## External actions

- `git checkout main && git pull --ff-only && git checkout -b
  feature/f106-session-resume` — branch created cleanly from `811c2d7e`.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  → `[]` (Open PR Gate satisfied, run before branching).
- `git worktree add .remedy-wt/negctl-wt HEAD` then `git worktree remove
  .remedy-wt/negctl-wt --force` — used only for G3's negative control (one
  printable byte flipped inside the appended RECORD1 region: space →
  `!`); both readings rejected the flipped copy and accepted the unflipped
  one; `git worktree list` afterward shows only the primary checkout.
- `git push -u origin feature/f106-session-resume` (after C6) — outcome
  reported to the operator in the round's completion report; not re-run
  here to respect the handback's write-once rule.
- No PR created this round, per constraint 11 (round 1 of the feature; PR
  at closure).

## Verification

Every exit code below is a real `subprocess.run(...).returncode` from a
script under `.remedy-wt/`, or a directly-observed shell exit from a
single Bash invocation — never inferred from piped output.

**G1** (at C0b) — `.agent/authored/f106-r1.md` and `.agent/last_block.md`
both 18597 bytes; `cmp` exits 0 (byte-equal). PASS.

**G2** (at C1) — sha256 of `.remedy-wt/PLAN1.txt` and `.agent/plan.md`:
both `9bf3e19d7613ed9d7557be6b65cca3e4c55fe3c37591fccc8dafb815da9f3251`.
Line count 39 (< 50). Contains `## Goal` and `## Next Steps`. PASS.

**G3** (at C2) — base pre-commit `.agent/live_review.md` measured
1809603 bytes (matches the reviewer's own `811c2d7e` reading exactly).
1809603 + 1 (separator `\n`) + 1164 (RECORD1) = 1810768 = the committed
file's actual size. (a) Whole reconstruction: `base + "\n" + RECORD1 ==
committed` → `True`. (b) Paragraph order: `committed.split(b"\n\n")[-1]
== RECORD1` → `True` (786 total paragraphs, N=1 dense paragraph appended).
Negative control inside a disposable worktree: unflipped copy accepted by
both readings (`True`, `True`); one printable byte flipped inside the
appended region (offset 10 into RECORD1, a space → `!`) — both readings
rejected it (`False`, `False`). Worktree removed after; `git status
--porcelain` empty throughout. PASS.

**G4** (at C1 and C2) — registered `R-` ids: 318 at both. Resolved
(`Done:`) ids: 55 at both. Open: 263 at both. Added registered: `set()`.
Added resolved: `set()`. `DECISION F\d+ D\d+ — ` ids: 19 at both. PASS.

**G5** (at C3) — PAIRSTATUS-FROM occurs 0×, PAIRSTATUS-TO occurs 1× in
`docs/roadmap/STATUS.md`. `git diff --numstat` for C3 alone: `1  1
docs/roadmap/STATUS.md`. Whole file holds exactly 1 line matching
`^- \[~\] F\d{3} — `.
`python3 -m pytest tests/docs/ -q` → 295 passed, exit 0.
`python3 -m pytest tests/orchestration/test_roadmap_index.py -q` → 30
passed, exit 0. Both match the reviewer's base reading exactly. PASS.

**G6** (at C4) — sha256 of `.remedy-wt/CONTEXT1.txt` and
`.agent/context.md`: both
`a35653587f2bd603f8007b76143028f8f5cbd894253d315ea8505146ea3f5107`.
Contains `## Active Branch`, `feature/f106-session-resume`, `F106`,
`Steps`. PASS.

**G7** (at C5) — each its own real exit code:
`python3 -m pytest tests/ui_server/ -q` → 515 passed, exit 0.
`python3 -m pytest tests/orchestration/test_test_runner.py -q` → 52
passed, exit 0.
`python3 -m pytest tests/regression/test_resource_safety.py -q` → 21
passed, exit 0.
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → 16
passed, exit 0.
`python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → 42 passed,
exit 0.
All five match the reviewer's base readings (515, 52, 21, 16, 42) exactly.
PASS.

**G8** (at C5) — `.agent/f106_inventory.md` exists and carries all 7 SPEC
section headings: "1. THE PROVIDER PROTOCOL AND ITS CONCRETE ADAPTERS",
"2. THE SESSION-ID FIELD IN CALL EVIDENCE", "3. THE CALL-ENTRY SIGNATURE —
THE ADDITIVE TARGET FOR `resume`", "4. CAPABILITY-FLAG PRECEDENT ELSEWHERE
IN THE REPO", "5. THE REPAIR LOOP'S CALL SITES — LOCATE ONLY", "6. THE
DIFF-REPAIR / DELTA MECHANISM", "7. TEST CONVENTIONS FOR PROVIDER-ADAPTER
TESTS" (rendered as `## 1. ...` through `## 7. ...` — the literal case in
the file is sentence case with the section topic capitalized, matching
the SPEC's own numbering exactly). After the `44c6847c` correction, the
file cites 30 distinct `file:line` locations plus 2 file-level (no single
line) existence checks; every `.py`/`.md` path resolves with
`git ls-tree HEAD -- <path>` (verified across all 9 distinct files the 30
lines sit in — every one returned a `100644 blob <sha>` line). `git status
--porcelain` empty. `git ls-files --others --exclude-standard` empty
(count 0). Per-commit insertion counts, `git diff --numstat`, C0a through
the `44c6847c` correction: 344, 328, 27, 2, 1, 38, 206, 37 — every one
under 500. PASS.

## Authored-text proofs

- PLAN1 → `.agent/plan.md`: sha256-equal
  (`9bf3e19d7613ed9d7557be6b65cca3e4c55fe3c37591fccc8dafb815da9f3251` both
  sides).
- RECORD1 → appended to `.agent/live_review.md`: whole-reconstruction and
  paragraph-order readings both `True` against the committed file;
  negative control (disposable worktree, one byte flipped) rejected by
  both readings, restored/removed after.
- CONTEXT1 → `.agent/context.md`: sha256-equal
  (`a35653587f2bd603f8007b76143028f8f5cbd894253d315ea8505146ea3f5107` both
  sides).
- PAIRSTATUS-FROM/PAIRSTATUS-TO → `docs/roadmap/STATUS.md`: measured, not
  asserted — FROM 0× / TO 1× post-C3, exactly 1 insertion + 1 deletion in
  `git diff --numstat`, matching constraint 12's stated pair shape
  (`TO contains FROM: false`, a REWRITE).
- C0a/C0b transport (`.agent/authored/f106-r1.md` /
  `.agent/last_block.md`): byte-equal, 18597 bytes each (G1).

## Deviations & assumptions

1. **Extra commit beyond the block's C0a-C6 bundle.** After committing C5
   (`11ccdb32`), I noticed its own closing "Citation count" section had
   hand-counted only 19 `file:line` pairs while the body prose actually
   cited more (e.g. `worker_registry.py:168`/`:169`,
   `pingpong_loop.py:3284`, `pingpong_provider.py:138`/`146`/`235`,
   `model_route_tournament.py:145`) — an undercount, not a fabrication,
   but sloppy self-auditing against the SPEC's own "cite every claim"
   instruction. I committed a follow-up fix (`44c6847c`) rather than
   amending C5, per AGENTS.md's "always create NEW commits rather than
   amending." This is a real deviation from the block's exact bundle shape
   (C0a-C6, 8 named commits) — the branch now carries 9 commits before C6,
   i.e. C5 plus one correction. I judged this preferable to shipping a
   self-reported measurement I knew to be an undercount, but it is not
   what constraint 3's implicit "one commit per bundle item" shape orders,
   so it is declared here rather than silently folded into the C5 entry.
2. **`git commit`'s terminal summary disagreed with `git diff --numstat`
   for two commits.** For C0b, the auto-printed summary read "344
   insertions(+), 284 deletions(-)"; `git diff --numstat 3f712642
   30960577` reads `328  268`. For C1, the auto-printed summary read "39
   insertions(+), 34 deletions(-)"; `git diff --numstat 30960577
   4f5eec7a` reads `27  22`. Both commits are `.agent/`-file rewrites that
   git's commit-summary path detects as "rewrite" (>50% changed) and
   diffstats with a different heuristic (whole-file replace) than a plain
   `git diff`/`git diff --numstat`, which do a real line-level diff and
   agree with each other and with `git show --numstat`. I used
   `git diff --numstat` throughout this handback because (a) AGENTS.md's
   Commit Discipline section states the cap counts "the `+` column of
   `git diff --stat`" by name, and (b) the block's own Handback section
   says the `+/-` column is "taken from `git diff --numstat`." A reviewer
   who reads only the terminal transcript of the `git commit` calls will
   see different, larger numbers than this table reports; both are
   internally consistent (verified via `git diff --stat` too), the
   discrepancy is git's own dual diffstat code paths, not an error in
   either reading.
3. Two `grep` invocations (checking `## Goal`/`## Next Steps` line counts
   in `.agent/plan.md`, and later a `for` loop over `git ls-tree` calls)
   were denied by the sandbox's Bash permission layer without an obvious
   single-cause pattern. Worked around by using the `Read` tool or a
   single non-looping `git ls-tree HEAD -- <path1> <path2> ...` call, and
   by moving repeated logic into one-shot `python3` scripts under
   `.remedy-wt/`, consistent with constraint 7 anyway (every reported exit
   code is a real `subprocess.run(...).returncode`).
4. `remedy` the console binary was not needed this round — no gate or SPEC
   item in this block calls the orchestrator or `plan next`; constraint 9
   is noted for completeness but not triggered.
5. No production code, test, or `docs/roadmap/features/` file was touched,
   matching the block's Change set exactly (verified: `git diff
   --stat main...HEAD` touches only the 8 named paths plus the one
   undeclared-in-advance but same-file `44c6847c` correction to
   `.agent/f106_inventory.md`, already covered by deviation 1).

## Next

Round 2 orders T001: add `supports_resume: bool = False` to the
`PingPongProvider` protocol and all three adapters (`FakeProvider`,
`ClaudeProvider`, `ClaudeCliProvider`), an additive `resume` keyword
parameter on `build`/`review` (default `None`, unused this round), and
`resume_used`/`resume_session_ref` fields on `BuilderOutput`/
`ReviewerOutput` (both False/"" by construction — zero behavior change),
plus `tests/orchestration/test_session_resume.py`. `.agent/f106_inventory.
md` (this round's measurement) is the shape T001 builds directly on.
