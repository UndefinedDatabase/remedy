# Handback — F274 ROUND 7 — round 6's G6 red is repaired, and the blindness that hid it is closed

This file supersedes the round 6 handback. It is written by the delegated worker on the reviewer's
authored block `.agent/authored/f274-r7.md`.

EVERY GATE G1 THROUGH G8 IS GREEN. One deviation is declared, D1, and it is a NUMERAL in the block
rather than anything on disk: G2(c)'s `^Landed: ` clause names a LINE pattern but states the
DISTINCT-ID number. Both readings were measured and both move by exactly +2. Nothing was adjusted
to make a gate agree.

## Session

SESSION 4 of feature F274 · round 7 · rounds so far 7

Soft limit 25 rounds / 7 sessions: 7 rounds and 4 sessions used. The session opened with
`.agent/STOP` ABSENT — re-checked at every commit boundary and still absent at C7 — and
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returning `[]`, so the
Open PR Gate is clear. No branch was created or switched; no PR was created.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): this round consumed a modest share of
context — an eight-commit bundle, four slice applications, eight FROM/TO pairs across three files
each read before editing, and the eight gates run in full across two disposable worktrees — and
ample headroom remains for a further delegated round in this session.

## Range

Review of `450365a7214b3d6c04c394a645a5fee65cc00867`..HEAD, where HEAD is C7, the commit that
writes this file. Seven commits precede it, every one single-parent, in exactly the block's ordered
sequence C0a, C0b, C1, C2, C3, C4, C5, C6.

## Commits

### b7b88ee9 F274 R7 C0a: save the round 7 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f274-r7.md | +380 / -0 | the block's 31076 bytes copied verbatim by `shutil.copyfile`, never retyped |

### 68e6b0db F274 R7 C0b: mirror the round 7 block into the last-block pointer
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +304 / -226 | the same bytes mirrored by `shutil.copyfile`; the round 6 block it replaced was shorter |

### 58085c38 F274 R7 C1: point the plan at the round 6 repair and the widened walker
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +18 / -18 | full replacement by the PLAN7 slice |

### f40a94d2 F274 R7 C2: book round 6 FAIL and register R-0833 and R-0834
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6 / -0 | RECORD7 appended: the `Gate: F274 R6` FAIL entry and the two new findings |

### 09bb3959 F274 R7 C3: append round 6 two reviewer prose slips
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4 / -0 | SLIPS7 appended: two dated lines, no ids |

### a81aef39 F274 R7 C4: cut the context_budget half of smoke section 12ai
| Path | +/- | Reason |
|------|-----|--------|
| scripts/remedy_smoke.sh | +5 / -11 | pairs P1-P4: the comment, the banner, the import tuple's two names, and the six `context_budget` node/edge/order assertions plus the success line. THE REPAIR ONLY — the map test is untouched by this commit, per constraint 7 |

### a3082c28 F274 R7 C5: widen the deletion map walker to embedded python and record the edge
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_cluster_deletion_map.py | +29 / -3 | pairs P5-P7: `import re`, the `_EMBEDDED_IMPORT` regex with its WHY comment and `embedded_first_party_imports`, and `measured_edges` widened from `rglob("*.py")` to every file with an `ast`/regex split |
| tests/orchestration/cluster_deletion_map.txt | +1 / -0 | pair P8: the `context_optimizer <- scripts/remedy_smoke.sh` edge the widened walk newly sees, placed by the file's sort. THE GUARD ONLY — the smoke script is untouched by this commit, per constraint 7 |

### 685af2ab F274 R7 C6: mark R-0833 and R-0834 landed
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | LANDED7 appended: the two reviewer-authored `Landed:` paragraphs, applied verbatim |

### HEAD F274 R7 C7: hand back round 7 (self-reference exception, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file; a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — Open PR Gate clear |
| `git worktree add --detach .remedy-wt/r7-g5 a3082c28` | created for G5 and G6; 14 -> 15 entries |
| `git worktree remove --force .remedy-wt/r7-g5` | removed after `git -C .remedy-wt/r7-g5 status --porcelain` came back EMPTY |
| `git worktree prune` | ran; `git worktree list` back to 14 entries |
| `git worktree add --detach .remedy-wt/r7-lint 450365a7…` | created for G7's base lint; 14 -> 15 entries |
| `git worktree remove --force .remedy-wt/r7-lint` | removed |
| `git worktree prune` | ran; `git worktree list` back to 14 entries |
| `git push` | see below |

No PR was created. No branch was created or switched. Nothing was force-pushed. No file was deleted
by glob: both mutated files were restored by exact path with a sha256 identity check.

## Verification

G1 TRANSPORT, at C0b — **PASS.** `git cat-file blob HEAD:.agent/authored/f274-r7.md | sha256sum`
and `git cat-file blob HEAD:.agent/last_block.md | sha256sum` both give
`fef320ac5fb35964459f808402ed4f61f5d3718e8232aff6b987d168a1bb6e70`, and `git cat-file -s` gives
31076 for both. That is the digest and the byte count the delegation states, measured on
`.remedy-wt/f274-r7-block.md` BEFORE the file was used and again on both committed blobs.

G2 THE TWO RECORD APPENDS, re-derived from the COMMITTED blobs — **PASS in all three parts.**
(a) AT C2 `f40a94d2`: `.agent/live_review.md` 543921 -> 554047 bytes; pre-image a byte-exact
PREFIX and post-image equal to pre plus the 10126-byte RECORD7 slice with NO separator added —
byte reader True. Structural reader over the whole appended region, unit = a maximal run of
consecutive non-empty lines, N counted FROM THE SLICE = 3: units 217 -> 220, the file's last 3
units equal the slice's 3 units IN ORDER and everything before them is unchanged — True.
NEGATIVE CONTROL: the post-image byte at ZERO-INDEXED offset 543922 reads as `G`, the `G` opening
the first appended paragraph; flipped to `g` IN MEMORY, the byte reader REJECTS and the structural
reader REJECTS. The primary checkout was never touched.
(b) AT C6 `685af2ab`: 554047 -> 554669 bytes against the 622-byte LANDED7 slice; byte reader True,
structural reader True, N from the slice = 2, units 220 -> 222. NEGATIVE CONTROL at zero-indexed
offset 554048, which reads as `L`, the `L` opening the first appended `Landed:` paragraph; flipped
to `l`, BOTH readers REJECT.
(c) COUNTS at C6, base `450365a7` -> C6, all from the committed blobs:
registrations 66 -> 68, resolutions 3 -> 3 BY DISTINCT ID, **OPEN SET 63 -> 65 BY DISTINCT ID**,
`^Gate: ` 37 -> 38, `^Gate: F274 R6` 0 -> 1, `^- R-0833 — ` exactly 1, `^- R-0834 — ` exactly 1.
`^Landed: ` — see deviation D1: measured 35 -> 37 as LINES, 31 -> 33 as DISTINCT IDS. The block's
numeral is the distinct-id reading and it holds exactly; the line reading moves by the same +2.

G3 THE STATE PROSE FILES — **PASS.**
(a) `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN7 slice, sha256
`ab2fd8b46fcdcf1e6efddf66142eee5be02edb133073f7557a88cdf97d4b5576`, 2512 bytes, **43 lines**
against the cap of 50, and carries both `## Goal` (line 7) and `## Next Steps` (line 22).
(b) `.agent/prose_slips.md` at C3 `09bb3959`: 158733 -> 159553 bytes, pre-image a byte-exact
PREFIX, post-image pre plus the 820-byte SLIPS7 slice with no separator, and each of the two
appended lines occurs EXACTLY ONCE in the post-image.

G4 THE REPAIR PROVES ITSELF BY RUNNING, at C4 — **PASS.**
Section 12ai's embedded python was EXTRACTED FROM THE COMMITTED BLOB, not retyped:
`git cat-file blob a81aef39:scripts/remedy_smoke.sh`, then the bytes between that section's
`python3 -c "` line and the next line that is exactly `"` — 961 bytes, 30 lines. Executed with
`python3 -B` from the repo root:

    EXIT CODE = 0
    stdout: '    brain nodes: OK (decision_queue)\n'
    stderr: ''

The import block it now carries is `NT_DECISION_QUEUE, / ET_HAS_DECISION_QUEUE, / _NODE_TYPE_ORDER,
build_project_brain,` — the `decision_queue` node, edge and `_NODE_TYPE_ORDER` assertions all
survive and all pass. THE SWEEP ROUND 6 COULD NOT PASS, over the 1313 tracked files under
`packages/`, `apps/`, `tests/` and `scripts/`, ALL FILE TYPES and not only python:
`NT_CONTEXT_BUDGET` 0, `ET_HAS_CONTEXT_BUDGET` 0, `_build_context_budget_node` 0,
`_detail_context_budget` 0, `has_context_budget` 0 — **TOTAL = 0**, against the 5 round 6 measured.

G5 THE EXTENDED GUARD IS LOAD-BEARING, BOTH WAYS — **PASS.** All four runs in the disposable
worktree `.remedy-wt/r7-g5` at C5, never in the primary checkout; `__pycache__` purged before
every run and every run under `python3 -B`. The worktree's own copy was confirmed to be what
pytest imports: `m.__file__` = `.remedy-wt/r7-g5/tests/orchestration/test_cluster_deletion_map.py`.
Command for every run: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q`.
(a) CONTROL before mutations — **EXIT 0**, `3 passed in 1.42s`.
(b) RED ONE, the new walker is what produces the new edge: `    return set(_EMBEDDED_IMPORT.findall(text))`
occurs EXACTLY ONCE in that file at C5 (measured, 1) and was replaced with `    return set()`.
**EXIT 1**, `1 failed, 2 passed in 1.20s`, output carries `DISAPPEARED (1)` and names
`packages.orchestration.context_optimizer <- scripts/remedy_smoke.sh`; `APPEARED (0)`. Restored BY
EXACT PATH, byte-identical True by sha256.
(c) RED TWO, the new walker sees a NEW embedded consumer: appended
`from packages.orchestration.review_bundle import build_review_bundle` to `scripts/remedy_smoke.sh`.
**EXIT 1**, `1 failed, 2 passed in 1.18s`, output carries `APPEARED (1)` and names
`packages.orchestration.review_bundle <- scripts/remedy_smoke.sh`; `DISAPPEARED (0)`. Restored BY
EXACT PATH, byte-identical True by sha256.
(d) CONTROL after both restorations — **EXIT 0**, `3 passed in 1.17s`, and
`git -C .remedy-wt/r7-g5 status --porcelain` EMPTY before removal.
So the regex walker is not decoration: neutering it loses the edge, and a new embedded import
gains one.

G6 THE EDGE TRUTH, at C5 — **PASS, and it is the reading that corrects round 6.** All four
readings, taken in the worktree at C5:
 - measured edges 38, recorded edges 38, `measured == recorded` True, APPEARED `[]`,
   DISAPPEARED `[]`;
 - measured consumers of `packages.orchestration.context_optimizer` = **`['scripts/remedy_smoke.sh']`**,
   so that module is NOT deletable and round 6's zero-edge reading is corrected ON DISK by the
   guard itself;
 - modules with NO edge = **`['context_pack', 'review_bundle', 'self_repair_proposal']`**, exactly
   three, `context_optimizer` no longer among them;
 - non-`.py` consumers the widened walk finds = **`['scripts/remedy_smoke.sh']`**, exactly one, so
   the widening added one real edge and no noise — in particular `cluster_deletion_map.txt` did NOT
   become its own consumer, which is what the import-form-only regex exists to prevent.
NO CLUSTER MODULE WAS DELETED THIS ROUND.

G7 THE SUITES AND THE CEILING, run SERIALLY in the primary checkout at C6 — **PASS.** Every suite
was re-run at C6 itself, not carried over from C5.
| Command | Exit | Count |
|---------|------|-------|
| `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` | 0 | **3 passed** in 4.18s |
| `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` | 0 | **3 passed** in 1.28s |
| `python3 -B -m pytest tests/test_remedy_smoke_script.py -q` | 0 | **191 passed** in 0.45s |
| `python3 -B -m pytest tests/orchestration/test_project_brain.py -q` | 0 | **82 passed** in 0.84s |
| `python3 -B -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | **42 passed** in 21.05s |
| `python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q` | 0 | **10 passed** in 0.28s |
Every number equals the number the block states. THE LINT CEILING HELD: `python3 -m ruff check .`
run FROM THE WORKTREE'S OWN ROOT in a disposable worktree checked out at
`450365a7214b3d6c04c394a645a5fee65cc00867` gives `Found 26 errors.`; the same command in the
primary checkout at C6 gives `Found 26 errors.` DECISION F083 D5's frozen ceiling is untouched —
the 29 inserted lines of C5 added no lint error.

G8 THE TREE, at C6 — **PASS.**
`git status --porcelain` EMPTY, and empty at every commit boundary of the round.
`git ls-files .remedy-wt` EMPTY — nothing under the gitignored scratch dir was ever staged.
`git worktree list` 14 entries before the first `worktree add` and 14 after the last `prune`.
`git diff --name-only 450365a7214b3d6c04c394a645a5fee65cc00867..685af2ab` names exactly 8 paths —
the 9 of the change set minus `.agent/handoff.md`, which C7 writes — and nothing else:
`.agent/authored/f274-r7.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/prose_slips.md`, `scripts/remedy_smoke.sh`,
`tests/orchestration/cluster_deletion_map.txt`, `tests/orchestration/test_cluster_deletion_map.py`.
Every commit C0a through C6 is SINGLE-PARENT.
INSERTIONS ONLY, the `+` column, per AGENTS.md DECISION F104 D1:
C0a **380**, C0b **304**, C1 **18**, C2 **6**, C3 **4**, C4 **5**, C5 **30**, C6 **4**.
Every one is under the 500 cap; no oversize commit was declared or needed. Each figure was
cross-checked cell by cell against the `+/-` column of the Commits table above, taken from
`git diff --numstat`. C7's own numbers are deliberately not quoted; that commit does not exist
while this file is being written.

## Authored-text proofs

| Slice | Bytes | sha256 (measured) | Result |
|-------|-------|-------------------|--------|
| PLAN7 | 2512 | `ab2fd8b4…7d4b5576` | verified against its BEGIN marker before applying; committed `.agent/plan.md` at C1 is BYTE-EQUAL |
| RECORD7 | 10126 | `fc0342be…0a071078c`* | verified before applying; committed `.agent/live_review.md` at C2 is pre + slice exactly, no separator |
| LANDED7 | 622 | `935ddc6d…f9191901a04`* | verified before applying; committed `.agent/live_review.md` at C6 is pre + slice exactly, no separator |
| SLIPS7 | 820 | `f1745333…240fdceed`* | verified before applying; committed `.agent/prose_slips.md` at C3 is pre + slice exactly, no separator |
| whole block | 31076 | `fef320ac…8a1bb6e70`* | measured on `.remedy-wt/f274-r7-block.md` BEFORE use, and again on both committed copies |

(*abbreviated head…tail of the full 64-hex digest; each full digest was compared in full against
its BEGIN marker, and the whole-block digest against the delegation message.)

All four slices were extracted from the block's own bytes by marker line and written byte for byte.
All eight FROM/TO pairs were extracted the same way and each FROM was measured to occur EXACTLY
ONCE in its target before being applied: P1 1, P2 1, P3 1, P4 1, P5 1, P6 1, P7 1, P8 1. The eight
`TO contains FROM` readings measured independently match the block's printed values exactly —
false for P1, P2, P3, P4, P5, P7 and P8, true for P6. Nothing was reflowed, re-indented, retyped or
"fixed". `.agent/authored/f274-r7.md` and `.agent/last_block.md` were produced by
`shutil.copyfile`, never by re-emission.

## Deviations & assumptions

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |
| G1 | done | PASS |
| G2 | done | PASS; one clause's numeral is a pattern mismatch — D1 |
| G3 | done | PASS |
| G4 | done | PASS — EXIT 0, sweep total 0 |
| G5 | done | PASS — 0 / 1 / 1 / 0 |
| G6 | done | PASS — all four readings exact |
| G7 | done | PASS |
| G8 | done | PASS |

No departure from the block's ordered commit sequence: eight commits, C0a, C0b, C1, C2, C3, C4, C5,
C6 then C7, in that order, none added, none dropped, none reordered. Constraint 7 was honoured:
C4's diff touches only `scripts/remedy_smoke.sh` and C5's touches only the two map files, so the
repair and the guard are separately revertible.

**D1 — G2(c)'s `^Landed: ` CLAUSE NAMES A LINE PATTERN BUT STATES A DISTINCT-ID NUMBER.** The block
orders `^Landed: ` 31 -> 33. Measured against the committed blobs, `grep -c '^Landed: '` gives
**35 at the base and 37 at C6**. The block's 31 -> 33 is the DISTINCT-ID reading:
`grep -o '^Landed: R-[0-9]*' | sort -u | wc -l` gives **31 at the base and 33 at C6**. The gap is
four ids that each carry two `Landed:` lines in the record — R-0725, R-0727, R-0730 and R-0749.
Both readings move by exactly +2, which is the fact the clause exists to check, and the two new
lines are LANDED7's own. Nothing was adjusted: the slice was applied verbatim and the real numbers
are reported here. This is the same class as round 6's `resolutions 3 -> 3` note, where the block's
numeral was also the distinct-id reading of a line pattern.

**D2 — THE R-0833 PARAGRAPH'S "ordering weight 25" IS NOT ON DISK, AND THE PAIR IS STILL RIGHT.**
RECORD7's fix clause says the `decision_queue` assertions are unchanged "including the one pinning
the ordering weight 25". Section 12ai carries no numeral 25: its ordering assertion is
`chk(NT_DECISION_QUEUE in _NODE_TYPE_ORDER, 'missing dq in order')`, a MEMBERSHIP check. Pair P4
keeps that line verbatim, so the intended site set was never ambiguous and the specified text was
applied unchanged. Declared, not repaired; nothing on disk is wrong because of it, and the slice
was applied byte for byte as constraint 1 requires.

No assumption_log entry was needed. **No `Done:` paragraph was written anywhere** — the two
`Landed:` paragraphs at C6 are reviewer-authored text applied verbatim, and only the reviewer
writes `Done:`, at the next gate. `.agent/STOP` was absent throughout.

## Open findings

**65, measured** — the G2(c) count over the committed post-image of `.agent/live_review.md` at C6,
BY DISTINCT ID: 68 distinct `^- R-\d+ — ` registrations minus 3 distinct `^Done: R-\d+ — `
resolutions. R-0833 (Medium) and R-0834 (High) are the two newest and both are open, both now
carrying a `Landed:` line. The open High findings remain R-0803, R-0804, R-0806 and R-0807 — all
F273's per DECISION F272 D12 — with R-0834 joining them.

## Next

The reviewer re-runs G1 through G8 against this committed diff, rules D1 and D2, and writes the
`Done:` paragraphs for R-0833 and R-0834 if the Landed work is accepted. The substantive next round
cuts section 12ah of `scripts/remedy_smoke.sh`, the last recorded consumer of `context_optimizer`,
which is the round that takes that module to zero edges for real — this time with the widened
walker watching.
