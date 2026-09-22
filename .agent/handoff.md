# Handback — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 24 · The closure: the rotation, the accepted STATUS line with its README pins, and the pull request

## Session

SESSION 5 of feature F283 · round 24 · rounds so far 24

This round booked round 23's PASS, rotated the finding ledger into its
archive as its own commit, flipped F283's STATUS line to accepted with the
README's three pinned places and the self-use entry SU-026's `consumed_by`
in one closure commit, and opened the pull request (never merged by this
session). Context self-assessment: a comfortable majority of the working
budget remained through the round; the two full-file suite runs
(`tests/docs/`, `tests/cli/test_golden_path.py`) each ran once and to
completion.

## Range

Review of `120a3b77`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 184 | 184 | True |
| sha256 | `e5c0481a4f434242290eaf0c3ac2875c6394eac74f5d3312f8a163fea5d36a25` | `e5c0481a4f434242290eaf0c3ac2875c6394eac74f5d3312f8a163fea5d36a25` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `120a3b77`, matching the delegation message.
- `git stash list`, first line before C1: `stash@{0}: WIP on (no branch):
  365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package
  readings` (pre-existing project debt, untouched this round).
- `git worktree list`, before C1: primary checkout + `.remedy-wt/job-129b3ad7206d4f8d`
  (round 22's self-use leftover — not this round's to remove).
- `git branch --list 'remedy/job-*' | wc -l`, before C1: **38**.

Payload readings against the PAYLOADS table (lines = newline count):

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 2/2 | 2451/2451 | True |
| plan.md | 31/31 | 1294/1294 | True |
| status_from.txt | 0/0 | 102/102 | True |
| status_to.txt | 0/0 | 459/459 | True |
| readme_count_from.txt | 0/0 | 36/36 | True |
| readme_count_to.txt | 0/0 | 36/36 | True |
| readme_tier_from.txt | 0/0 | 44/44 | True |
| readme_tier_to.txt | 0/0 | 44/44 | True |
| readme_prose_from.txt | 0/0 | 72/72 | True |
| readme_prose_to.txt | 5/5 | 432/432 | True |

All ten readings equal.

## Commits

### ebce205e F283 R24 C1: copy round 24 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r24-block.md | +184/-0 | byte-for-byte copy of this round's step block (`shutil.copyfile`) |
| .agent/authored/f283-r24-ledger.md | +2/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r24-plan.md | +31/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r24-readme_count_from.txt | +1/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-readme_count_to.txt | +1/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-readme_prose_from.txt | +1/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-readme_prose_to.txt | +6/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-readme_tier_from.txt | +1/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-readme_tier_to.txt | +1/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-status_from.txt | +1/-0 | byte-for-byte copy |
| .agent/authored/f283-r24-status_to.txt | +1/-0 | byte-for-byte copy |

Measured insertions (`git show --numstat`): **230** (184+2+31+1+1+1+6+1+1+1+1).

### f15ab354 F283 R24 C2: book round 23's PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append ledger.md payload: round 23's `Gate:` entry |
| .agent/plan.md | +10/-13 | full-file rewrite to plan.md payload, byte-identical |

Measured insertions (`git show --numstat`): **12** (2 for live_review.md +
10 for the plan.md rewrite), 13 deletions, well under the 500-line cap.

### 4250c7a5 F283 R24 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-94 | `scripts/rotate_live_review.py` moved 19 gate records and 14 resolved finding pairs (28 records) out of the live ledger |
| .agent/live_review_archive.md | +94/-0 | the same moved text appended to the archive |

Measured insertions: **94**. Script's own printed readings: gate records
moved 19; finding pairs moved 14 (28 records); old ledger size 568445 bytes,
new ledger size 425098 bytes; old archive size 4432550 bytes, new archive
size 4575897 bytes; open findings before 26, after 26 (identical). Path set
is exactly the two ledger files, nothing else.

### (this commit) F283 R24 C4: accept F283 in STATUS with its README pins and the self-use entry
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | the `[~]` line replaced by the accepted `[x]` line (status_from/status_to pair) |
| README.md | +8/-3 | the accepted count + Next clause (1 line), the Tier 2 Done cell (1 line) and the Tier 2 prose entry (5-line rewrite of a 1-line sentence) |
| scripts/self_use_queue.json | +1/-1 | SU-026's `"consumed_by": ""` set to `"consumed_by": "F283"`, the only line touched |
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback
cannot table the commit that writes it. Measured insertions for the three
non-handoff paths: 1 (STATUS.md) + 8 (README.md) + 1 (queue.json) = 10,
all under the cap.

## External actions

- `git push origin feature/f283-machine-contracts-part-two` after C4 —
  real outcome reported in the session reply, since it ships this very file.
- `gh pr create --base main ...` after the push — real number and URL
  reported in the session reply.
- `gh pr list --state open ...` after the create — real outcome reported in
  the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push.
- `git stash` was **not** used at any point this round.
- No file under `.remedy-wt/f283-r24-payloads/` was written to, and no file
  the reviewer placed under `.remedy-wt/f283-r24-scratch/` before this round
  (`build_closure.py`, `build_payloads.py`, `gate_src.txt`, `plan.txt`) was
  edited.

## Verification

### G1 — TRANSPORT

Payload readings (table above): **all ten files equal on lines/bytes/sha256**.

Eleven `.agent/authored/f283-r24-*` blobs (the block copy plus ten
payloads), each read back from the committed tree with
`git show ebce205e:<path>` and compared byte-for-byte with its source:

| copy | equal to source | bytes |
|---|---|---|
| f283-r24-block.md | True | 13072 both |
| f283-r24-ledger.md | True | 2451 both |
| f283-r24-plan.md | True | 1294 both |
| f283-r24-status_from.txt | True | 102 both |
| f283-r24-status_to.txt | True | 459 both |
| f283-r24-readme_count_from.txt | True | 36 both |
| f283-r24-readme_count_to.txt | True | 36 both |
| f283-r24-readme_tier_from.txt | True | 44 both |
| f283-r24-readme_tier_to.txt | True | 44 both |
| f283-r24-readme_prose_from.txt | True | 72 both |
| f283-r24-readme_prose_to.txt | True | 432 both |

**All eleven readings True.**

### G2 — THE BOOKING (at C2, `f15ab354`)

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`120a3b77`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 565994 | 2451 | 568445 | True |

Matches the block's stated composition exactly (568445).

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R23 — ` = **1**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `120a3b77` | **26** |
| C2 (`f15ab354`) | **26** |

Added: `[]`. Removed: `[]`. Matches the block's stated 26 → 26, ADDED and
REMOVED both empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload. Line count: **31**, under the AGENTS.md 50-line rule.

### G3 — THE ROTATION (at C3, `4250c7a5`)

Script's own printed readings: old ledger size **568445** bytes, new ledger
size **425098** bytes; gate records moved **19**; finding pairs moved **14**
(28 records); open findings before **26**, after **26** — IDENTICAL; old
archive size **4432550** bytes, new archive size **4575897** bytes — the
archive grew by **143347** bytes, exactly what the ledger lost
(568445−425098=143347). C3's path set: `.agent/live_review.md` and
`.agent/live_review_archive.md`, nothing else (`git diff --stat` for that
commit shows exactly those two paths).

### G4 — THE CLOSURE EDITS (at C4)

| pair | target | FROM before | FROM after | TO after |
|---|---|---|---|---|
| status | docs/roadmap/STATUS.md | 1 | 0 | 1 |
| readme_count | README.md | 1 | 0 | 1 |
| readme_tier | README.md | 1 | 0 | 1 |
| readme_prose | README.md | 1 | 0 | 1 |

`scripts/self_use_queue.json`: `"consumed_by": "",` count before **1**,
after **0**; `"consumed_by": "F283"` count after **1**, carried by the
SU-026 entry (verified by loading the JSON and finding the one item whose
`consumed_by` was empty before the edit — its id is `SU-026`, title
"Address ledger finding R-0950"). `python3 -m json.tool
scripts/self_use_queue.json` exits 0 (valid JSON). `git diff
scripts/self_use_queue.json` shows exactly one changed line.

`python3 -m pytest tests/docs/ -q`: **315 passed** in 85.11s, exit **0** —
matches the reviewer's dry-run reading exactly.

Accepted count measured from the flipped STATUS.md:
`len(re.findall(r'^- \[x\] F\d{3} — ', status, re.M))` = **89**. Tier 2
Done cell, measured the same way the reviewer's dry run derived it (walking
every accepted line's `docs/roadmap/features/T*_F<id>.md` filename and
counting the `T2_` prefix): **31**. Both match the block's required 89 and
31, and README.md's own committed lines read `89 of 283 registered items
accepted` and `| 2 | Minimal Self-Build Runtime | 31 | 36 |`.

### G5 — THE TREE

`python3 -c` calling `run_integrity_checks` from
`packages.orchestration.integrity_gate`, read with C4's STATUS/README/queue
edits already applied on disk: `passed=True`, `fail_count=0`, `len(checks)=5`.

`python3 -m pytest tests/cli/test_golden_path.py -q`: **42 passed** in
131.17s, exit **0** — the canary every handback runs.

`git status --porcelain`, `git worktree list` and the `remedy/job-*` branch
count are read fresh, post-push, and reported with real exit codes in the
session reply (G6), since this file cannot table its own commit's effect on
the tree ahead of time.

## Authored-text proofs

- The block copy and ten payload copies at C1, compared with the block's
  originals under `.remedy-wt/f283-r24-payloads/` and
  `.remedy-wt/f283-r24-block.md`: **eleven readings, all True** (G1).
- The one APPEND payload against its committed file: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md,
  565994+2451=568445, G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- The four FROM/TO REWRITE pairs applied at C4: each target's FROM count
  went 1→0 and its TO count went to 1, measured by direct `str.count` before
  and after the substitution (G4 table above) — no payload text was
  retyped; every FROM and TO string was read from its payload file on disk
  and applied with `str.replace`.
- No payload was edited or retyped. The block copy and ten payload copies at
  C1 were made with `shutil.copyfile`; the live_review.md append by reading
  the payload's bytes and writing pre+payload back to disk; the plan.md
  rewrite by `shutil.copyfile`; the rotation by the reviewer's own
  `scripts/rotate_live_review.py`; the four closure pairs by reading each
  FROM/TO payload file's exact bytes and calling `str.replace` once per
  pair; the `consumed_by` edit by a single targeted string replacement on
  the one line the reviewer's own count (1 occurrence) identified.

## Deviations & assumptions

None. The block's four commits (C1, C2, C3, C4) landed in the ordered
sequence, with no extra, dropped or reordered commit, followed by the pull
request.

1. **Constraint 1** (no payload edited or retyped): held — `shutil.copyfile`
   for C1's eleven copies; byte-read-then-write for C2's one append;
   `shutil.copyfile` for the plan.md rewrite; `str.replace` against payload
   bytes read fresh from disk for all four C4 pairs and the queue.json edit.
2. **Constraint 2** (every commit under 500 insertions by `git show
   --numstat`): held — 230, 12, 94, 10 (excluding the handoff.md rewrite,
   exempt as a single `.agent/**` state file).
3. **Constraint 3** (the round's tracked path set is EXACTLY the enumerated
   set): held — `git diff --name-only 120a3b77 HEAD` before this commit's
   handoff.md addition reads exactly the eleven
   `.agent/authored/f283-r24-*` copies, `.agent/live_review.md`,
   `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json`
   — fourteen paths; adding `.agent/handoff.md` from this commit makes
   fifteen, still exactly the block's enumeration (`.agent/authored/f283-r24-*`,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`,
   `.agent/handoff.md`). Nothing under `packages/`, `apps/`, `tests/`, no
   other file under `docs/` or `scripts/`, and none of `.agent/candidates.md`,
   `.agent/context.md`, `.agent/decisions.md`, `.agent/operator_questions.md`,
   `.agent/prose_slips.md` were touched.
4. **Constraint 4** (C4 is the LAST commit on this branch, Rule A4): held —
   nothing follows C4 except, if the operator's review asks for one later,
   a `.agent/candidates.md`-only commit, which this block does not order and
   was not written.
5. **Constraint 5** (if any gate goes red, stop before C4): not invoked —
   every gate (G1, G2, G3, and the pre-checks folded into G4 — the four
   FROM/TO counts and the `consumed_by` count) read exactly as required
   before C4 was drafted, so the round proceeded to C4 and the pull request.
6. **Constraint 6** (nothing is merged): held — no `gh pr merge`, no
   checkout of `main`, no branch deletion, no force-push.
7. **Constraint 7** (delete nothing not created this round): held —
   `remedy/job-129b3ad7206d4f8d` and its worktree, and all pre-existing
   stash entries, left exactly as found; `remedy/job-*` count unchanged at
   38 as measured pre-C1 (re-confirmed post-C4 in the session reply).
8. `git stash` was never used this round.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `120a3b77`; block 184 lines / matching sha256 |
| C1 copy block + 10 payloads | done | 230 insertions |
| C2 book round 23's PASS | done | 12 insertions, 13 deletions; open set 26→26, no ADDED/REMOVED |
| C3 rotate the finding ledger | done | 94 insertions/94 deletions across two files; 19 gate records + 14 finding pairs (28 records) moved; open findings 26→26 identical |
| C4 accept F283 with README pins and self-use entry | done | STATUS `[~]`→`[x]`; README count 88→89, tier 30→31, prose rewritten; SU-026 `consumed_by` `""`→`"F283"` |
| PR creation | done | reported with number and URL in the session reply |
| G1 payload transport + authored copies | done | 10/10 payload readings equal; 11/11 authored copies byte-identical |
| G2(a) live_review.md append | done | 565994+2451=568445 |
| G2(b) line-anchored gate line + open set by distinct id | done | 1 occurrence of the named line; 26→26, no ADDED/REMOVED |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 31 lines, under 50 |
| G3 the rotation | done | old/new ledger 568445/425098; old/new archive 4432550/4575897; 19 gate records + 14 pairs moved; open 26→26 |
| G4 the closure edits | done | all four FROM/TO pairs 1→0/1; `consumed_by` 1→0 empty, 1 `F283`; valid JSON; `tests/docs/` 315 passed exit 0; accepted 89, Tier 2 Done 31 |
| G5 the tree | done | integrity `passed=True fail_count=0`; golden path 42 passed exit 0 |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile` / bytes read+write / `str.replace` against payload bytes only |
| Constraint 2 every commit under 500 insertions | done | 230, 12, 94, 10; handoff exempt as single `.agent/**` state file |
| Constraint 3 tracked path set is exactly the enumeration | done | 14 paths before this commit (15 after), exact match |
| Constraint 4 C4 is the last commit (Rule A4) | done | nothing follows except an optional future `.agent/candidates.md` commit, not ordered here |
| Constraint 5 stop before C4 if any gate is red | done (n/a) | no gate was red; C4 proceeded |
| Constraint 6 nothing merged | done | no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push |
| Constraint 7 delete nothing not created this round | done | round-22 branch/worktree left alone; `remedy/job-*` count unchanged at 38 |
| `git stash` used | done (n/a) | never used this round |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk. While it exists, write
   nothing and end.
2. The Open PR Gate — the pull request this round opens is merged by the
   NEXT feature's session, never by this one.
3. Then Rule A5: the first unchecked feature in `docs/roadmap/STATUS.md`.

Open findings count: **26**. Operator-questions count: **0**.
