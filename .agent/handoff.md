# Handoff — F114 Cost preview per command, round 10 (books R9's PASS; adds the cost-preview user guide, T003 continued)

## Session

SESSION 3 of feature F114 · round 10 · rounds so far 10.

This round books round 9's PASS verdict into the ledger (RECORD9) and
adds T003's docs item: a new user guide,
`docs/guides/cost-preview-user-guide-v0.md`, documenting `job.run`'s
cost-preview behavior end to end — the estimate line, the mandatory
basis label, the `cost_preview.confirm_above_usd` config key, `--yes`,
`--unattended`, and the non-tty exit-2-with-hint path — and registers
it in `docs/README.md` (Quick-Find Table + Guides section). No
production code or test file changes this round.

## Range

Review of `91e4ad64..HEAD` (HEAD is `a2a24339` before this handback
commit).

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this handback |
| G1 TRANSPORT | done | PASS |
| G2 THE LEDGER APPEND | done | PASS |
| G3 THE PLAN | done | PASS, one wording deviation declared below |
| G4 THE NEW FILE | done | PASS |
| G5 THE README PAIRS | done | PASS |
| G6 THE SUITES | done | PASS (all six measured) |
| G7 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### ab68a385 F114 R10 C0a: save step block verbatim to .agent/authored/f114-r10.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r10.md` | +293/-0 | transport proof — verbatim save of the supplied step block, new file |

### fc141a63 F114 R10 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +293/-287 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### bb3bc3f8 F114 R10 C1: append RECORD9 to live_review.md, replace plan.md with PLAN10
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD9 (round 9's PASS verdict) — exactly one `\n` then RECORD9's 3264 bytes, no blank-line separator |
| `.agent/plan.md` | +14/-21 | whole-file replace with PLAN10 (first substantive commit, per constraint 2) |

### a2a24339 F114 R10 C2: add cost-preview user guide, register in docs/README.md (T003 continued)
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/cost-preview-user-guide-v0.md` | +88/-0 | GUIDE, new file — user guide for `job.run`'s cost-preview behavior (estimate line, basis label, config key, `--yes`/`--unattended`, non-tty exit-2 path) |
| `docs/README.md` | +2/-0 | QUICKFIND PAIR (cost preview row, Quick-Find Table) and GUIDESROW PAIR (Guides section row), both applied via `str.replace(FROM, TO, 1)` |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created,
  edited or merged this round; constraint 10 states explicitly that a
  docs-only addition does not by itself trigger the Open PR Gate, which
  waits for the remaining T003 acceptance items (marking further
  expensive commands, the integration gate).
- No git worktree was created or used this round — constraint 11 states
  no mutation red-proof applies since no production code changed, and
  none was created.

## Verification

Preconditions, checked before C0a and again before C3:

```
$ test -f .agent/STOP && echo EXISTS || echo ABSENT
ABSENT (checked twice: before the first commit, and again before C3)
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git log --oneline -n 5
91e4ad64 F114 R9 C3: rewrite .agent/handoff.md - round 9 handback
c18a416c F114 R9 C2: add acceptance tests for job.run cost-preview behavior (T003 continued)
947a1474 F114 R9 C1: append RECORD8 to live_review.md, replace plan.md with PLAN9
cab855b8 F114 R9 C0b: mirror block to .agent/last_block.md
a871cd4f F114 R9 C0a: save step block verbatim to .agent/authored/f114-r9.md
```
Step block was supplied directly in this round's delegation prompt
(no relay path this session); saved verbatim to
`.agent/authored/f114-r10.md` via the Write tool, delimiter lines
excluded, never retyped for any downstream use — every applied slice
was extracted from the COMMITTED file by script (constraint 1).

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r10.md .agent/last_block.md
fc00c33f38b4c17083c476110e1a520fb21b90bf3f7cc32ca4e8e69f08636dee  .agent/authored/f114-r10.md
fc00c33f38b4c17083c476110e1a520fb21b90bf3f7cc32ca4e8e69f08636dee  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2379181 bytes
Base ends with trailing newline: False
RECORD9 own byte length (extracted from committed authored file): 3264 bytes, 0 internal newlines
base + 1 + len(RECORD9) = 2379181 + 1 + 3264 = 2382446
post-C1 file byte length: 2382446
Match: True (also matches the round instructions' own stated
2382446/2379181/3264 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2379181) to end-of-file and compared against
`"\n" + RECORD9` directly:
```
tail (base..end) == "\n" + RECORD9: True
```
Negative control, scratch copy only (never the tracked file — a
throwaway file under `.remedy-wt/`, removed immediately after) — one
byte flipped (XOR 0xFF) at an offset inside RECORD9's own text (10
bytes into the RECORD9 region), then re-compared against the real
`"\n" + RECORD9`:
```
second reader REJECTS the mutated copy: True (mutated tail != "\n" + RECORD9)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN10 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
39 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0 — PASS. `wc -l` reads 39, one less than the gate's own
stated "expect 40" — DEVIATION, declared below, not silently
corrected. Both grep counts 1 — PASS. 39 is under 50 either way.

**G4 THE NEW FILE**:
```
$ cmp <GUIDE + its own trailing newline, extracted from committed authored file> docs/guides/cost-preview-user-guide-v0.md
(no output — exit 0)
$ wc -c docs/guides/cost-preview-user-guide-v0.md
3666 docs/guides/cost-preview-user-guide-v0.md
```
`cmp` exit 0 (written as a whole-file copy — GUIDE's 3665 extracted
bytes plus its own true trailing `\n` — a "copyfile", never a
text-extraction-and-reflow, per constraint 5), byte length 3666 —
matches the round instructions' own stated expectation exactly — PASS.

**G5 THE README PAIRS**:
```
QUICKFIND PAIR FROM count in docs/README.md immediately before C2: 1
GUIDESROW PAIR FROM count in docs/README.md immediately before C2: 1
QUICKFIND PAIR TO contains QUICKFIND PAIR FROM: True
GUIDESROW PAIR TO contains GUIDESROW PAIR FROM: True
```
Both applied via `str.replace(FROM, TO, 1)`, then re-checked present
in the file — both True. PASS.
```
$ git show --numstat a2a24339 -- docs/README.md
2	0	docs/README.md
```
+2/-0, matching the diff (one Quick-Find Table row, one Guides section
row, both pure insertions) — PASS.

**G6 THE SUITES, EACH ITS OWN INVOCATION, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/docs/ -q
295 passed in 0.45s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.73s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.57s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.51s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.29s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.91s
```
All six counts — 295, 515, 52, 21, 16, 42 — are IDENTICAL to round 9's
own stated figures in RECORD9, exactly as expected since this round
touches only `.agent/**` and `docs/`. `tests/docs/` in particular
still reads 295: the new guide file is not itself a member of
`PRIMARY_DOCS` in `tests/docs/test_docs_consistency.py`, so its links
are checked as part of the existing parametrized case for
`docs/README.md` rather than as a new case — no new test was added by
this round, confirmed by the unchanged count. These are the REAL,
measured counts, not assumed.

**G7 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| ab68a385 (C0a) | `.agent/authored/f114-r10.md` | 293 | 293 | yes |
| fc141a63 (C0b) | `.agent/last_block.md` | 293 | 293 | yes |
| bb3bc3f8 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| bb3bc3f8 (C1) | `.agent/plan.md` | 14 | 14 | yes |
| a2a24339 (C2) | `docs/guides/cost-preview-user-guide-v0.md` | 88 | 88 | yes |
| a2a24339 (C2) | `docs/README.md` | 2 | 2 | yes |

C3's own numbers go to neither this table nor a round report, per this
gate's own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r10.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 11 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD9 books round 9's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 10's actual current step and real next steps |
| `docs/guides/cost-preview-user-guide-v0.md` | NOT stale | documents the real, already-gated round 8/9 behavior; its own Risks-section note in PLAN10 already flags that a future behavior change must update it in the same round |
| `docs/README.md` | NOT stale | both new rows point at the real new file; no existing row was altered or removed |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
Searched `docs/` for other references to `cost-preview-user-guide` or
`cost_preview` outside the change set — found only
`docs/roadmap/features/T3_F114.md`'s own pre-existing lines (the
`cost_preview.py` design line and the suggested-tests line), neither
made stale by this round's docs addition. Rounds 2 and 3's own
`.agent/context.md` declarations (lines 29 and 36) stand and are not
repeated here, per constraint 8's explicit instruction.
`docs/roadmap/STATUS.md`'s F114 line (`- [~] F114`) is untouched and
still correctly claimed (in progress).

## Authored-text proofs

- `.agent/authored/f114-r10.md` written verbatim via the Write tool
  from the step block supplied in this round's delegation prompt
  (delimiter lines `═══ BLOCK BEGINS ═══` / `═══ BLOCK ENDS ═══`
  excluded, exactly as instructed), sha256
  `fc00c33f38b4c17083c476110e1a520fb21b90bf3f7cc32ca4e8e69f08636dee`,
  confirmed identical to `.agent/last_block.md` after C0b (G1). Two of
  its slices' independently-measured byte lengths matched the round
  instructions' own stated expectations exactly before any writing
  happened — RECORD9 at 3264 bytes and GUIDE at 3665+1=3666 bytes —
  which is itself strong evidence the file was transcribed correctly.
- All seven slices (RECORD9, PLAN10, GUIDE, QUICKFIND PAIR FROM/TO,
  GUIDESROW PAIR FROM/TO) were extracted from the COMMITTED
  `.agent/authored/f114-r10.md` by a Python script
  (`.remedy-wt/extract_slices.py`, gitignored scratch) reading
  delimiter indices (`<<<BEGIN ...>>>` / `<<<END ...>>>`), taking the
  exact substring strictly between each pair of markers — never by
  hand-retyping (constraint 1).
- Per constraint 4: RECORD9 and PLAN10 each had no trailing `\n` of
  their own carried into the target file (the byte separating the
  slice's last content line from its own `<<<END ...>>>` marker line
  belongs to marker-line formatting, not the slice). GUIDE's own
  trailing `\n` was ADDED as its true last byte — a real markdown
  file's own structural suffix, not marker-line formatting, per
  constraint 4's explicit statement (same class as round 9's own
  TESTMODULE).
- RECORD9: 3264 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD9 (G2, above).
- PLAN10: 1744 bytes, 40 logical lines, no trailing newline (matches
  `.agent/plan.md`'s own pre-round no-trailing-newline convention,
  same as round 9's PLAN9); `.agent/plan.md` reproduces it
  byte-identical (`cmp` exit 0).
- GUIDE: 3665 bytes extracted, 3666 bytes written (own trailing `\n`
  added), matches the round instructions' own stated expectation
  exactly; written as a whole-file copy (never a
  text-extraction-and-reflow) then verified byte-identical against the
  extracted-plus-newline slice with `cmp` (G4, above).
- QUICKFIND PAIR FROM (93 bytes) / TO (190 bytes) and GUIDESROW PAIR
  FROM (103 bytes) / TO (244 bytes): each TO verified to contain its
  own FROM before application (constraint 6), each FROM verified to
  occur exactly once in `docs/README.md` before C2, each applied via
  `str.replace(FROM, TO, 1)`, and each TO verified present in the file
  after (G5, above).

## Deviations & assumptions

One deviation. G3's gate text states "wc -l .agent/plan.md -> report;
expect 40, must be under 50". The real, measured `wc -l` output is 39,
not 40. This is not a transcription error: PLAN10 as extracted has 40
logical lines (39 `\n` characters joining them) and carries no
trailing newline of its own, per constraint 4 — `wc -l` counts `\n`
bytes, so a file with N logical lines and no final newline reports
N-1. This is the identical pattern round 9's own PLAN9 hit (46 lines,
also under the 50 cap) and is not a defect in `.agent/plan.md`; it is
the gate's own prose stating a logical-line count that a literal
`wc -l` invocation cannot produce once the no-trailing-newline
convention (constraint 4) is honored. Reported as measured, not
corrected, per constraint 1's "if anything ... looks wrong, apply it
as written and declare the concern" and self_drive_protocol.md's G4
("gates run, never assumed"). Either reading — 39 or 40 — is well
under the 50-line cap, so nothing about the plan's compliance is in
question.

No other deviations. The slice extraction, the newline-convention
handling (constraint 4), the whole-file copyfile-and-cmp for GUIDE
(constraint 5), and the README pairs' containment-then-replace
sequence (constraint 6) all matched the round instructions exactly. No
slice's content looked wrong, so nothing else needed declaring under
constraint 1's "apply as written... declare" clause. `.agent/STOP` was
absent at both checkpoints (before the first commit and again before
C3). No path outside the change set was written: only
`.agent/authored/f114-r10.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`,
`docs/guides/cost-preview-user-guide-v0.md`, `docs/README.md` and this
handback were touched — `packages/`, `apps/` and `tests/` were never
opened for writing, per constraint 7. The bundle's commit order (C0a,
C0b, C1, C2, C3) was followed exactly. No git worktree was created,
per constraint 11. No pull request or merge action was taken this
round.

## Next

T003 continuation (round 11 or later, no fixed round assigned yet):
consider marking other "rerunning subtrees" / "long explanations"
commands `is_expensive` — only `job.run` carries it so far; real cost
bands for `job.run` still do not exist and a future round needs real
task-class data to replace the unavailable estimate. Then acceptance
fixtures continue, the integration gate, then the closure sequence
(PR, Open PR Gate) — no PR exists yet and none is expected until
enough of the feature lands to warrant one. Session note: round 10,
session 3 — this is the 1st delegated round of session 3, at the
operator's 4-5 default; more rounds may follow in this same session
unless context runs low.
