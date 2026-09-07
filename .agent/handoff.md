# Handback — F274 ROUND 8 — a DELETION ROUND: smoke section 12ah is cut and `context_optimizer` reaches zero edges

This file supersedes the round 7 handback. It is written by the delegated worker on the reviewer's
authored block `.agent/authored/f274-r8.md`.

THE CUT LANDED AND THE EDGE TRUTH IS EXACTLY WHAT THE BLOCK PREDICTED: measured edges 37, the
consumers of `packages.orchestration.context_optimizer` are THE EMPTY LIST, the zero-edge modules
are the four the block names, and the non-`.py` consumers the widened walk finds are THE EMPTY LIST.
G1, G2, G3, G5 and G6 are GREEN in every clause with every stated numeral matching on the nose.

TWO DEVIATIONS ARE DECLARED AND NEITHER WAS REPAIRED INTO AGREEMENT. **D1: gate G4(d)'s ruff clause
is RED, and it is RED AT THE BASE COMMIT TOO** — `python3 -m ruff check` on an explicitly-named `.sh`
path is unmeetable by construction. **D2: gate G4(b), the full suite, is INTERMITTENT** — 6 of 8 runs
green, 2 runs red on the same two node ids, whose cause is the already-registered OPEN finding
R-0569. Both are reported with the real commands, the real exit codes and the real output below.
Nothing was adjusted to make a gate agree, and no number in the block was edited.

## Session

SESSION 4 of feature F274 · round 8 · rounds so far 8

Soft limit 25 rounds / 7 sessions: 8 rounds and 4 sessions used. `.agent/STOP` was ABSENT at session
start, re-checked at every commit boundary, and still absent at C5. The Open PR Gate is clear:
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]`. No branch was
created or switched, nothing was force-pushed, and NO PR WAS CREATED — the block orders a push and
nothing more.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): this round consumed a moderate share of
context — a six-commit bundle, three slice applications, one 49-line excision and six gates, of which
G4 alone cost eight full-suite runs and a base-commit worktree to characterise two red readings
honestly — and enough headroom remains for one more delegated round in this session.

## Range

Review of `b7b954b0c50f311ea74403eaaf9e43fef5192835`..HEAD, where HEAD is C5, the commit that writes
this file. Five commits precede it, every one single-parent, in exactly the block's ordered sequence
C0a, C0b, C1, C2, C3, C4.

## Commits

### 32b8da42 F274 R8 C0a: save the round 8 step block verbatim as authored text
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f274-r8.md | +235 / -0 | the block's 23487 bytes copied by `shutil.copyfile`, never retyped |

### e2450957 F274 R8 C0b: mirror the round 8 block into the last-block state file
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +148 / -293 | the same bytes mirrored by `shutil.copyfile`; the round 7 block it replaced was longer, hence the negative net |

### 3ecacc94 F274 R8 C1: point the plan at round 8, the context_optimizer deletion round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +17 / -19 | full replacement by the PLAN8 slice |

### 6fd13516 F274 R8 C2: book round 7 PASS and resolve R-0833 and R-0834 in the record
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6 / -0 | RECORD8 appended: the `Gate: F274 R7` PASS entry and the two reviewer-authored `Done:` paragraphs |

### cfde9141 F274 R8 C3: append the two round 7 prose slips to the slips log
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4 / -0 | SLIPS8 appended: two dated lines, no ids |

### 0064898b F274 R8 C4: cut smoke section 12ah and its context_optimizer map edge
| Path | +/- | Reason |
|------|-----|--------|
| scripts/remedy_smoke.sh | +0 / -49 | section 12ah excised entire: the banner, the heading comment, the `_SMOKE_SECTION` assignment, the `echo`, the whole `python3 -c` body with its closing quote and the trailing blank line |
| tests/orchestration/cluster_deletion_map.txt | +0 / -1 | the `packages.orchestration.context_optimizer <- scripts/remedy_smoke.sh` line, deleted in the SAME commit as the edge it records |

A PURE DELETION: this commit's `+` column is ZERO across both files, which is the reading G6 asks
for. Section 12ai SURVIVES UNTOUCHED — `12ai` still occurs 3 times in the script.

### HEAD F274 R8 C5: hand back round 8 (self-reference exception, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file; a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — Open PR Gate clear |
| `git worktree add --detach .remedy-wt/r8-base b7b954b0…` | created to measure D1's ruff behaviour AT THE BASE; 14 -> 15 entries |
| `git worktree remove --force .remedy-wt/r8-base` | removed |
| `git worktree prune` | ran; `git worktree list` back to 14 entries |
| `git worktree add --detach .remedy-wt/r8-c4 0064898b` | created for G5; 14 -> 15 entries |
| `git worktree remove --force .remedy-wt/r8-c4` | removed after `git -C .remedy-wt/r8-c4 status --porcelain` came back EMPTY |
| `git worktree prune` | ran; `git worktree list` back to 14 entries |
| `git push` | see below |

No PR was created. No branch was created or switched. Nothing was force-pushed. NO FILE WAS DELETED
BY GLOB: the one file mutated for a red-proof was restored by exact path with a sha256 identity
check, and the one scratch probe written into the disposable worktree
(`.remedy-wt/r8-c4/probe_g5.py`) was removed by exact path with `os.remove` before that worktree's
porcelain was read.

## Verification

**G1 TRANSPORT, at C0b — PASS.** Re-derived from the COMMITTED blobs with `git show`:
`.agent/authored/f274-r8.md` and `.agent/last_block.md` are both **23487 bytes** at sha256
**`2f9c169e3416cd9d528e5957b4547456510cc95146231fa87675bc3ff6d5f5c9`**, byte-equal to each other and
equal to the digest the delegation message states. The same digest was measured on
`.remedy-wt/f274-r8-block.md` BEFORE the file was used. Both copies were produced by
`shutil.copyfile`, never by re-emission.

**G2 THE RECORD APPEND, at C2 `6fd13516`, re-derived from the COMMITTED blobs — PASS in all four
clauses.**
(a) BYTES: `.agent/live_review.md` **554669 -> 563333**, exactly as ordered. Pre-image is a byte-exact
PREFIX (True) and the post-image equals pre plus the **8664-byte** RECORD8 slice with NO separator
added (`post == pre + slice` True).
(b) STRUCTURE over the whole appended region, unit = a maximal run of consecutive non-empty lines,
**N counted FROM THE SLICE = 3** (not taken from the block): units **222 -> 225**; the file's last 3
units equal the slice's 3 units IN ORDER (True) and everything before them is unchanged (True).
(c) NEGATIVE CONTROL: the post-image byte at ZERO-INDEXED offset **554670** reads as **`G`** — the `G`
opening the first appended paragraph, exactly as the block says. Flipped IN MEMORY to `F`, the byte
reader REJECTS and the structural reader REJECTS. The primary checkout was never touched.
(d) COUNTS, base -> C2, all by the stated patterns: registrations **68 -> 68**, resolutions
**3 -> 5**, **OPEN SET 65 -> 63 BY DISTINCT ID**, `^Gate: ` **38 -> 39**, `^Gate: F274 R7` **0 -> 1**,
`^Done: R-0833 — ` **exactly 1**, `^Done: R-0834 — ` **exactly 1**. THE TWO `Landed:` LINES ROUND 7
WROTE SURVIVE BESIDE THE RESOLUTIONS: `^Landed: ` is **unchanged at 37 lines**. Every numeral matches
the block exactly; unlike round 7 there is no line-vs-distinct-id gap to declare here, because this
clause is stated as a line count and was measured as one.

**G3 THE STATE PROSE FILES — PASS.**
`.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN8 slice (2376 bytes, sha256
`01c2d47f6880255f2a44a6eb22decbd756190d2127e33d2925cb80b32cec0f71`), is **41 lines** against the cap
of 50, and carries both `## Goal` and `## Next Steps`.
`.agent/prose_slips.md` at C3 `cfde9141` goes **159553 -> 160319**, pre-image a byte-exact prefix
(True), post-image equal to pre plus the 766-byte SLIPS8 slice with no separator (True), and each of
the two appended lines occurs **EXACTLY ONCE** in the post-image.

**G4 THE DELETION ROUND'S FOUR MEASUREMENTS, at C4 — (a) PASS, (b) INTERMITTENT (D2), (c) PASS,
(d) SPLIT: `bash -n` PASS, `ruff` RED and unmeetable (D1).**

(a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` — **EXIT 0**,
`3 passed in 1.27s`.

(b) `python3 -m pytest -q -n auto` in the PRIMARY CHECKOUT per constraint 7 — **8 runs, 6 green and
2 red on the same two node ids.** See D2. The green reading is **EXIT 0, `19791 passed, 23 skipped,
1 warning`**; the red reading is **EXIT 1, `2 failed, 19789 passed, 23 skipped, 1 warning`**, the two
failures being
`tests/orchestration/test_product_smoke.py::TestAppStartsGreen::test_a_clean_app_passes` and
`tests/orchestration/test_product_smoke.py::TestBrokenStartHoldsTheJob::test_the_job_is_held_open`.
Exit code by run, in order: run 1 NOT CAPTURED (the command was piped to `tail`, though its summary
line reads `19791 passed, 23 skipped`), then **1, 0, 0, 0, 0, 0, 1**.

(c) A sweep over **every tracked file** under `scripts/`, `packages/`, `apps/` and `tests/` — **1313
files, ALL FILE TYPES, no extension filter**, read as bytes:
 - the token `12ah` **TOTALS ZERO**, against 3 at the base, all three inside the deleted section;
 - the string `packages.orchestration.context_optimizer` **TOTALS ZERO UNDER `scripts/` ALONE**,
   against 1 at the base, in the deleted section.
Both scopes are the ones the block states and the block's reasons were checked rather than taken on
trust. The `12ah` sweep excludes `.agent/` because this very block names the section and C0a and C0b
commit this block, so a repo-wide zero is unmeetable BY CONSTRUCTION. The `context_optimizer` clause
is scoped to `scripts/` because the string legitimately SURVIVES elsewhere, and the survivors were
enumerated and match the block's list exactly: **3 in `apps/cli/commands/context_optimizer_cmd.py`,
5 in `tests/orchestration/test_project_brain.py`, 1 in
`tests/orchestration/import_reachability_allowlist.txt` and 1 in
`tests/orchestration/test_cluster_deletion_map.py`** — the MODULE is not deleted this round, only its
last consumer edge.

(d) `bash -n scripts/remedy_smoke.sh` — **EXIT 0.** The script STILL PARSES after the 49-line
excision, which is what this clause exists to test.
`python3 -m ruff check scripts/remedy_smoke.sh` — **EXIT 1**, and **EXIT 1 at the base commit too**.
See D1.

**G5 THE EDGE TRUTH AND THE RATCHET, at C4, in the disposable worktree `.remedy-wt/r8-c4` — PASS in
all three clauses.** `__pycache__` was purged first (0 directories present) and every run used
`python3 -B`. The primary checkout was never mutated.
(a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` — **EXIT 0**,
`3 passed in 1.39s`.
(b) THE FOUR READINGS, taken through the shipped module's own `measured_edges()` and `CLUSTER_MODULES`
rather than by grep:
 - measured edges **37**, recorded edges **37**, `measured == recorded` **True**;
 - measured consumers of `packages.orchestration.context_optimizer` = **`[]`, THE EMPTY LIST** — the
   module now has zero consumer edges under the WIDENED walker, which is what this round existed to
   produce;
 - modules with NO edge = **`['context_optimizer', 'context_pack', 'review_bundle',
   'self_repair_proposal']`**, exactly the four the block names, `context_optimizer` newly among them;
 - non-`.py` consumers the widened walk finds = **`[]`, THE EMPTY LIST** — round 7's single non-python
   consumer was the section just deleted, and no other file embeds a first-party import.
(c) RED: the deleted line `packages.orchestration.context_optimizer <- scripts/remedy_smoke.sh` was
appended back to `tests/orchestration/cluster_deletion_map.txt` (4038 -> 4106 bytes). The command of
(a) is then **EXIT 1**, `1 failed, 2 passed in 1.42s`, its output carrying **`DISAPPEARED (1)`** and
naming **`packages.orchestration.context_optimizer <- scripts/remedy_smoke.sh`**, with
`APPEARED (0)`. So the map guard is load-bearing in this direction and a line left behind is as red
as a new edge. RESTORED BY EXACT PATH
(`.remedy-wt/r8-c4/tests/orchestration/cluster_deletion_map.txt`), back to 4038 bytes at sha256
`b0501ec816fd3a50a90862c230d6a1da0eed8132796fb21355274d1cdf59f0c3`, **byte-identical True**, and the
control of (a) RETURNS TO **EXIT 0**, `3 passed in 1.28s`.

**G6 THE TREE, at C4 — PASS in every clause.**
`git status --porcelain` **EMPTY**, and empty at every commit boundary of the round.
`git ls-files .remedy-wt` **EMPTY** — nothing under the gitignored scratch dir was ever staged.
`git worktree list` **14 entries** before the first `worktree add` and **14** after the last `prune`.
`git diff --name-only b7b954b0c50f311ea74403eaaf9e43fef5192835..0064898b` names **exactly 7 paths** —
the 8 of the change set minus `.agent/handoff.md`, which C5 writes — and nothing else:
`.agent/authored/f274-r8.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/prose_slips.md`, `scripts/remedy_smoke.sh`, `tests/orchestration/cluster_deletion_map.txt`.
Set equality against constraint 3 was asserted, not eyeballed: **True**.
Every commit C0a through C4 is **SINGLE-PARENT** (parent count 1 for each).
INSERTIONS ONLY, the `+` column, per AGENTS.md DECISION F104 D1:
**C0a 235, C0b 148, C1 17, C2 6, C3 4, C4 0.**
**C4's insertion count is ZERO**, as a deletion round's cut must be. Every figure is under the 500
cap, no oversize commit was needed or declared, and each was cross-checked cell by cell against the
`+/-` column of the Commits table above, taken from `git diff --numstat`. C5's own numbers are
deliberately not quoted; that commit does not exist while this file is being written.

## Authored-text proofs

| Slice | Bytes | sha256 (measured) | Result |
|-------|-------|-------------------|--------|
| PLAN8 | 2376 | `01c2d47f…2cec0f71` | verified against its BEGIN marker BEFORE applying; committed `.agent/plan.md` at C1 is BYTE-EQUAL |
| RECORD8 | 8664 | `dff683cb…80a2f19d` | verified before applying; committed `.agent/live_review.md` at C2 is pre + slice exactly, no separator added |
| SLIPS8 | 766 | `d30b0fca…6b3c7f3ff` | verified before applying; committed `.agent/prose_slips.md` at C3 is pre + slice exactly, no separator added |
| whole block | 23487 | `2f9c169e…3ff6d5f5c9` | measured on `.remedy-wt/f274-r8-block.md` BEFORE use, and again on both committed copies |

Every slice was extracted from the block's own bytes by its BEGIN/END marker lines and written byte
for byte; each measured length and digest matched its BEGIN marker before a single byte was applied.
RECORD8 and SLIPS8 each CARRY THEIR OWN LEADING NEWLINE and no separator of any kind was added — both
were confirmed to begin with `\n`, and PLAN8 was confirmed to begin with `#` since it replaces rather
than appends. Nothing was reflowed, re-indented, retyped or "fixed". Marker lines were never written
to any file.

**NO `Done:` PARAGRAPH OF THE WORKER'S OWN WAS WRITTEN ANYWHERE.** The two `Done:` paragraphs now in
the record — R-0833 and R-0834 — are reviewer-authored text carried inside the RECORD8 slice and
applied verbatim as part of it; nothing was added beside them.

THE CUT WAS VERIFIED BEFORE IT WAS MADE, and every figure the block states was confirmed
independently: the run is **49 lines and 2011 bytes**, it occurs **exactly once** in the file at the
base commit (`raw.count(run) == 1`), it BEGINS at the banner line immediately preceding
`    # 12ah. Context Optimizer (Step 71)` and ENDS immediately before the banner line preceding
`    # 12ai. Brain nodes: decision_queue (Step 69)`, and the excision removed exactly 2011 bytes
(111867 -> 109856) and 49 lines (2725 -> 2676). The map line occurred **exactly once** (53 -> 52
lines). No figure the block states differed from what was measured.

## Deviations & assumptions

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| G1 | done | PASS |
| G2 | done | PASS — all four clauses, every numeral exact |
| G3 | done | PASS |
| G4(a) | done | PASS — EXIT 0, 3 passed |
| G4(b) | deviated | INTERMITTENT: 6 green / 2 red in 8 runs — D2 |
| G4(c) | done | PASS — both totals ZERO |
| G4(d) | deviated | `bash -n` EXIT 0 PASS; `ruff` EXIT 1, red at the base too — D1 |
| G5 | done | PASS — control 0, four readings exact, red 1 with `DISAPPEARED (1)`, restore byte-identical, control back to 0 |
| G6 | done | PASS — porcelain empty, 7 paths, all single-parent, C4 insertions ZERO |

NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE: six commits, C0a, C0b, C1, C2, C3, C4 then
C5, in that order, none added, none dropped, none reordered. The path set of C0a through C4 is
exactly the change set minus `.agent/handoff.md`, as constraint 3 requires.

**D1 — G4(d)'s RUFF CLAUSE IS RED, AND IT IS RED AT THE BASE COMMIT TOO, SO IT IS UNMEETABLE BY
CONSTRUCTION RATHER THAN BROKEN BY THIS ROUND.** The block orders
`python3 -m ruff check scripts/remedy_smoke.sh` EXIT 0. The real result:

    $ python3 -m ruff check scripts/remedy_smoke.sh          # primary checkout, at C4
    EXIT 1 — 1199 `invalid-syntax` diagnostics, beginning
    invalid-syntax: Simple statements must be separated by newlines or semicolons
      --> scripts/remedy_smoke.sh:22:16
       |
    22 | remedy_smoke() {
       |                ^

    $ python3 -m ruff check scripts/remedy_smoke.sh          # worktree at b7b954b0, THE BASE
    EXIT 1 — 1204 `invalid-syntax` diagnostics, the same first diagnostic at the same line 22:16

MECHANISM, measured rather than argued: ruff is a PYTHON linter and selects its parser by file type
during directory traversal, so `ruff check .` never picks up a `.sh` file — but naming the path
EXPLICITLY bypasses that discovery and forces bash source through the Python parser, which cannot
parse `remedy_smoke() {`. The count moves 1204 -> 1199 only because the excision removed 49 lines of
bash that were themselves being mis-parsed; it is not a lint improvement and must not be read as one.
THE FROZEN CEILING IS UNTOUCHED, which is the reading that actually matters here:
`python3 -m ruff check .` gives **`Found 26 errors.`** in a worktree at the BASE and **`Found 26
errors.`** in the primary checkout at C4 — identical, so DECISION F083 D5's ceiling holds.
The other half of G4(d), `bash -n scripts/remedy_smoke.sh`, is **EXIT 0** at both the base and C4, and
that is the clause that tests the property the block names ("the script must still PARSE after a
49-line excision"). NOTHING WAS REPAIRED: no lint config was touched, no `# noqa` added, no ruff
exclusion written, and the block's text was not edited to match. The reviewer may wish to restate this
clause as `bash -n` alone, or as `ruff check .` against the 26-error ceiling, since a python linter
pointed at a shell script can never return 0.

**D2 — G4(b), THE FULL SUITE, IS INTERMITTENT, AND THE CAUSE IS THE ALREADY-REGISTERED OPEN FINDING
R-0569 RATHER THAN THIS ROUND'S CUT.** Eight `python3 -m pytest -q -n auto` runs in the primary
checkout at C4: **6 green at `19791 passed, 23 skipped`, 2 red at `2 failed, 19789 passed, 23
skipped`**, exit codes in order — run 1 not captured (piped to `tail`, summary line green), then
1, 0, 0, 0, 0, 0, 1. The two red node ids are identical on both red runs:

    FAILED tests/orchestration/test_product_smoke.py::TestAppStartsGreen::test_a_clean_app_passes
    FAILED tests/orchestration/test_product_smoke.py::TestBrokenStartHoldsTheJob::test_the_job_is_held_open

THIS IS R-0569 — Low, OPEN, registered in `.agent/live_review.md` and explicitly NOT FIXED IN THIS
FEATURE — which states that `tests/orchestration/test_product_smoke.py` "builds its app fixtures with
a `port` parameter defaulting to 5273" inside a suite that runs under `-n auto`, so a second xdist
worker holding 5273 produces exactly this failure. VERIFIED AGAINST THE FILE RATHER THAN TAKEN FROM
THE FINDING'S PROSE: line 90 carries `port: int = 5273` as a default in the fixture builder's
signature, and both failing tests reach it through
`project()` without an explicit port. THE DISCRIMINATOR IS SERIALISATION, which is decisive:

| Selection | Command | Result |
|-----------|---------|--------|
| the two red node ids, SERIALLY | `python3 -m pytest -q <two node ids>` | **EXIT 0, `2 passed in 0.59s`** |
| the whole file, SERIALLY | `python3 -m pytest -q tests/orchestration/test_product_smoke.py` | **EXIT 0, `76 passed in 8.83s`** |
| the whole file, under `-n auto` | `python3 -m pytest -q -n auto tests/orchestration/test_product_smoke.py` | EXIT 1 on all 4 runs — `7 failed`, `6 failed`, `12 failed`, `10 failed`, each in ~2.6s |

The last row is the same mechanism amplified rather than a second one: concentrating 76 tests that all
default to port 5273 across parallel workers maximises the collision, and the file's own docstring
says "a port already in use is reported as a start failure", which is why those runs fail in 2.6s
instead of timing out.
NOT COUPLED TO THIS ROUND'S CUT, measured three ways: (i) `tests/orchestration/test_product_smoke.py`
is NOT in this round's change set and is byte-unchanged across
`b7b954b0..0064898b`; (ii) that file contains **ZERO** occurrences of `remedy_smoke`, `12ah`,
`context_optimizer` or `cluster_deletion`, so the cut cannot reach it textually; (iii) this round's
entire production diff is one excised bash section and one deleted data line, neither of which is
imported by any python module. NO TEST WAS DELETED, NO ASSERTION WEAKENED AND NO CEILING RAISED to
make this green — the intermittency is reported as it was measured.

No assumption_log entry was needed. `.agent/STOP` was absent throughout, re-checked at every commit
boundary.

## Open findings

**63, measured** — the G2(d) count over the committed post-image of `.agent/live_review.md` at C2,
BY DISTINCT ID: 68 distinct `^- R-\d+ — ` registrations minus 5 distinct `^Done: R-\d+ — `
resolutions, down from 65 because R-0833 and R-0834 both resolved this round. The open High findings
remain R-0803, R-0804, R-0806 and R-0807, all F273's rather than this feature's per DECISION F272
D12; R-0834 has left that set. R-0832 — the deletion map's blindness to event-name coupling — is
still OPEN and still binds the round that drafts DECISION F260 D3. R-0569, the fixed-port flake D2
names, is likewise still open and unrepaired here.

## Next

The reviewer re-runs G1 through G6 against this committed diff and rules D1 and D2 — D1 wanting a
restatement of G4(d)'s ruff clause, since a python linter aimed at a `.sh` path cannot return 0 at
any commit, and D2 wanting only a note that R-0569 is the cause, since it is already registered and
already routed away from this feature. The substantive next round is the first item of the plan's
Next Steps: `worker_recommend`'s three edges in `agent_loop.py`, `autonomy_loop.py` and
`dashboard.py`, which are LIVE RUNTIME CALLS rather than read-only views and so need a DECISION
naming what inherits worker recommendation authored BEFORE the cut.
