# Handoff — F276 Data-root hygiene & disk budget · Round 9

## Session

SESSION 2 of feature F276 · round 9 · rounds so far 9

Context self-assessment: the worker verified the step block's bytes before doing anything else — 221 lines, sha256 `eb5c1c4e41bb0b86916f1f13fa4d1f851c9ae0e1f7d5bde23a038c2fed73608b`, both readings identical to the digest the delegation message named — then read AGENTS.md in full, `docs/agents/handback_template.md` and `docs/roadmap/STATUS_closure_protocol.md` step 5 word for word, then the four remaining payloads with their digests checked before use; every numeral below is the output of a command run in this round, never a recollection, and G5's two exit codes were taken from a subprocess object rather than from a pipeline.

## Range

Review of 8da83220..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 9 is the closure sequence's third part: the bookkeeping, and the three steps that must precede the evidence package. It flips no STATUS line, touches no README, builds no package and opens no pull request; those are round 10's.
- C1 books round 8's PASS over the four commits ending at `8da83220`, registers R-1007 from the self-use run closure precondition 6 consumed, appends DECISION F276 D10, rewrites the plan, and saves byte copies of the four reviewer payloads.
- C2 spends this feature's ONE §3 checklist consolidation pass: item 17 merged into item 15, the number 17 retired, the list left at 34, and the prompt's consolidation paragraph amended to say that no free number remained.
- C3 is the ledger rotation, run by `scripts/rotate_live_review.py` and by nothing else: 25 gate records and 4 finding pairs moved, open findings 17 before and 17 after.
- C4 re-assigns every still-open finding to F282 by APPENDING one line per paragraph — 14 ids, ZERO deletions.
- C5 is this handoff.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | 4 payload copies + 3 state files; 445 insertions over 7 paths |
| C2 the consolidation | done | one path; blob `073486a2`, 34 items, 17 absent |
| C3 the rotation | done | script-run only; two ledger paths; 68 lines moved, byte-conserving |
| C4 the re-assignment | done | one path; 14 insertions, 0 deletions |
| C5 handoff | done | this file |
| G1 transport + state | done | 7 readings, every one True; saved block matches the delegation digest |
| G2 the consolidation | done | (a) blob EQUAL, (b) 34 items and 17 absent, (c) exactly one path |
| G3 the rotation | done | every printed line below; open findings 17 → 17; exactly the two ledger paths |
| G4 the re-assignment | done | (a) deletions ZERO, (b) 14 appended / 3 skipped, (c) 17 = 17, (d) 20/20 and 3/3 |
| G5 the canary + docs | done | `42 passed`, exit 0; `314 passed`, exit 0 |
| G6 push and tree | done | pushed; tree EMPTY; no `.agent/STOP`; 3 worktrees, two of them jobs' |
| R-1007 | **registered** | Medium; the reviewer's text in P2, applied at C1, never the worker's |
| R-1003, R-1006 | resolved in earlier rounds | untouched this round |
| R-1004, R-1005 | open | already carried the F282 owner string; skipped by C4 by design |
| STATUS flip | not done | round 10's, per the block's Goal |
| README sync | not done | round 10's |
| evidence job + package | not done | round 10's |
| `consumed_by` for SU-024 | not set | round 10's closure commit |

## Commits

### f1ea73a7 F276 R9 C1: the round 9 bookkeeping
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r9-block.md | +221/-0 | byte copy of P1, the step block |
| .agent/authored/f276-r9-decisions.md | +74/-0 | byte copy of P3 |
| .agent/authored/f276-r9-plan.md | +44/-0 | byte copy of P4 |
| .agent/authored/f276-r9-ledger.md | +4/-0 | byte copy of P2 |
| .agent/decisions.md | +74/-0 | DECISION F276 D10 appended |
| .agent/live_review.md | +4/-0 | round 8's PASS verdict and the R-1007 registration appended |
| .agent/plan.md | +24/-23 | rewritten to round 9 |

Insertions 445, deletions 23, 7 paths — under the 500 cap.

### 319ae0f0 F276 R9 C2: the §3 checklist consolidation
| Path | +/- | Reason |
|------|-----|--------|
| docs/agents/planner_reviewer_prompt.md | +24/-14 | item 17 merged into item 15; 17 retired; item 35's cross-reference repointed; the consolidation paragraph amended to 34 |

Insertions 24, deletions 14, 1 path. Applied from P5 with `git apply`, never retyped.

### 649ce611 F276 R9 C3: the ledger rotation
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +0/-68 | 25 gate records and 4 finding pairs left the live ledger |
| .agent/live_review_archive.md | +68/-0 | the same 68 lines arrived, sha256-verified by the script |

Insertions 68, deletions 68, 2 paths. NO SIZE EXEMPTION IS NEEDED and none is claimed: the block anticipated a wholesale rewrite, and the measured diff is a 68-line move whose insertion count is far under 500. The byte readings agree — the ledger lost 77108 bytes and the archive gained exactly 77108.

### 6bbd8771 F276 R9 C4: the finding re-assignment to F282
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +14/-0 | one new final line in each of 14 open findings' paragraphs |

Insertions 14, deletions 0, 1 path. The ZERO is the gate.

### C5 — this handoff (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewritten | a handoff cannot table the commit that writes it |

## External actions

- `git push origin feature/f276-data-root-hygiene` — after C5, G6. No `gh` command was run, no pull request was opened or edited, nothing was merged, no branch was deleted and no history was rewritten.
- No worktree was added or removed. The two job worktrees under `.remedy-wt/` are jobs', left alone per the block's constraint 5.

## Verification

**G1 — TRANSPORT AND STATE, at C1.** 7 readings, every one True, 0 False.

```
R1  .agent/authored/f276-r9-block.md         == payload block.md     : True
R2  .agent/authored/f276-r9-ledger.md        == payload ledger.md    : True
R3  .agent/authored/f276-r9-decisions.md     == payload decisions.md : True
R4  .agent/authored/f276-r9-plan.md          == payload plan.md      : True
R5  .agent/live_review.md   == 8da83220 bytes + ledger.md    : True
R6  .agent/decisions.md     == 8da83220 bytes + decisions.md : True
R7  .agent/plan.md          == payload plan.md               : True
readings: 7 | every one True: True | False count: 0
```

The saved block beside the delegation's own numbers, two readings side by side (R-0954):

```
saved  .agent/authored/f276-r9-block.md : lines 221  sha256 eb5c1c4e41bb0b86916f1f13fa4d1f851c9ae0e1f7d5bde23a038c2fed73608b
delegation message stated for P1        : lines 221  sha256 eb5c1c4e41bb0b86916f1f13fa4d1f851c9ae0e1f7d5bde23a038c2fed73608b
```

This covers the chain `.remedy-wt/f276-r9/` originals → the committed `.agent/authored/` copies → the committed state files. It makes no claim about the bytes that reached the worker's prompt, which this workflow cannot measure.

**G2 — THE CONSOLIDATION, at C2.** Three readings.

```
(a) git rev-parse C2:docs/agents/planner_reviewer_prompt.md
    exit 0 -> 073486a24b07721fa6364368cc573f8313c1ed52
    expected 073486a24b07721fa6364368cc573f8313c1ed52
    EQUAL: True
(b) first '  N. **' line (1-indexed): 251
    numbers: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37]
    length: 34 | must be 34 | EQUAL: True
    17 among them: False | must be absent | ABSENT: True
(c) git diff --name-only C1 C2
    exit 0 -> ['docs/agents/planner_reviewer_prompt.md']
    exactly the one path: True
```

(b) was bounded TWO independent ways and the two agree, which is why it is a cross-check and not a partition that cannot fail: BOUND A takes the region from the first `  N. **` line to the line before the exact string `- Verification tiers (operator decision 2026-07-26):`, which introduces the next numbered list in the file at line 1031; BOUND B ignores line numbers entirely and cuts the numbering run at the first item whose number does not exceed its predecessor. Both yield the same 34 numbers. The whole-file count without a bound reads 38, because the verification-tiers list contributes 1, 2, 3 and 5 — so an unbounded count would have passed nothing and is recorded here to show the bound is load-bearing.

**G3 — THE ROTATION, at C3.** Every line the script printed, and it was run with no arguments from the repository root; neither ledger was edited by hand.

```
gate records moved: 25
finding pairs moved: 4 (8 records)
old ledger size: 411123 bytes
new ledger size: 334015 bytes
old archive size: 4284047 bytes
new archive size: 4361155 bytes
open findings before: 17
open findings after: 17
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```

Exit 0; the script did not refuse. THE SAFETY PROPERTY HELD: open findings 17 before and 17 after, identical, which is the invariant the script prints so that a rotation can never be mistaken for a resolution. The two size deltas are 77108 bytes each and opposite, so every byte that left one file arrived in the other. F276's own `Gate:` records stayed, because F276 is `[~]` at this commit.

```
git diff --name-only C2 C3
.agent/live_review.md
.agent/live_review_archive.md
```

**G4 — THE RE-ASSIGNMENT, at C4.** Four readings.

```
(a) git show --numstat C4 -- .agent/live_review.md
    exit 0 -> 14	0	.agent/live_review.md
    insertions 14 | deletions 0 | DELETIONS ARE ZERO: True
(c) open findings                        : 17
    open findings whose paragraph holds  : 17
    repr of the string counted           : 'Owner: F282 — Findings paydown v2'
    the two counts are equal             : True
    open findings WITHOUT it             : []
(d) registered: C3 20 | C4 20 | identical set: True
    resolved  : C3  3 | C4  3 | identical set: True
    four numbers: 20 20 3 3
```

(b) The open set was computed from `.agent/live_review.md` AS IT STANDS AFTER C3. APPENDED TO, 14 ids: `R-0499`, `R-0622`, `R-0662`, `R-0819`, `R-0820`, `R-0829`, `R-0866`, `R-0880`, `R-0892`, `R-0950`, `R-0984`, `R-0998`, `R-0999`, `R-1000`. SKIPPED, 3 ids, each for the one reason the block names — the paragraph already contains the exact string `Owner: F282 — Findings paydown v2` and was therefore left completely untouched: `R-1004`, `R-1005`, `R-1007`. 14 + 3 = 17, the open count.

**G5 — THE CANARY, after C4, in the primary checkout.** Each exit code read off the `subprocess` object, no pipeline.

```
python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 130.92s (0:02:10)
exit 0

python3 -m pytest tests/docs -q
314 passed in 85.16s (0:01:25)
exit 0
```

**G6 — PUSH AND TREE, after C5.**

```
git push origin feature/f276-data-root-hygiene
git status --porcelain   -> EMPTY
ls .agent/STOP           -> No such file or directory (ABSENT)
git worktree list
/home/decodeux/Repos/remedy                                  [feature/f276-data-root-hygiene]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Three entries: the primary checkout and the two job worktrees, which are jobs' and are expected. No disposable worktree was created this round — no destructive verification was ordered.

## Authored-text proofs

All four reviewer-authored payloads applied this round compare EQUAL disk-to-disk against their committed `.agent/authored/` copies; those are readings R1 to R4 of G1 above, and readings R5 to R7 carry each applied text through to the state file it landed in. Digests verified BEFORE use, each against the number the block states:

| Payload | Lines | sha256 | Verified before use |
|---------|-------|--------|---------------------|
| P1 block.md | 221 | `eb5c1c4e…608b` | yes |
| P2 ledger.md | 4 | `a31d4ed9…4e2a` | yes |
| P3 decisions.md | 74 | `fdcaa54f…2055` | yes |
| P4 plan.md | 44 | `f3602a4d…f5fa` | yes |
| P5 f276-r9.diff | 77 | `1bc99001…0eb4` | yes |

The containment tests the block states were re-run mechanically before emission and reproduce its three readings: `.agent/live_review.md` contains P2 — false; `.agent/decisions.md` contains P3 — false; `.agent/plan.md` contains P4 — false. All three are new bytes and no FROM-count proof is owed.

## Open findings

17 by both readings at HEAD: `scripts/rotate_live_review.py::count_open_findings` answers 17, and `open_finding_ids` answers 17 entries over 17 distinct ids. By severity: 10 Medium, 7 Low, NONE High. Registered ids number 20 distinct over 21 paragraphs — `R-0809` appears twice and is resolved — against 3 distinct resolved ids.

The count reads 17 where round 8 measured 16 because C1 registered `R-1007`; nothing was resolved and nothing vanished, and the rotation's own before/after pair proves it.

Every one of the 17 now carries `Owner: F282 — Findings paydown v2`, counted at C4 as 17 of 17. No finding leaves this feature unowned.

## Deviations & assumptions

1. **G5 was run twice, and the numbers reported are the SECOND, wrapped run's.** The first invocation went through the tool directly, where a non-zero exit surfaces as an error but the exit code itself could only be inferred. The two suites were therefore re-run inside a `subprocess.run` wrapper that prints `p.returncode`, and G5's figures above are that run's: `42 passed in 130.92s` and `314 passed in 85.16s`, both exit 0. The first run read `42 passed in 130.50s` and `314 passed in 85.30s` — same counts, different wall clock, no contradiction.
2. **G6's push and its three post-commit readings necessarily postdate this file.** The write-once rule forbids a second handoff commit, so the push of C5 and the `git status` / `.agent/STOP` / `git worktree list` readings taken after it cannot be written into the commit that carries them. The worktree list and the STOP absence above were measured at C4, and the push and the empty tree are performed and read immediately after C5 and reported in full in the round report. Nothing else in this file is forward-looking.
3. **G2(b)'s bound is the worker's, not the block's.** The block orders the count "within the pre-emission checklist" without fixing that region's boundary, and the file holds a SECOND `  N. **` list — the verification tiers at line 1031 — which an unbounded count folds in, yielding 38 rather than 34. Two independent bounds were therefore computed and shown to agree, and the unbounded 38 is reported beside them so the reader can see which number the bound is responsible for. The block's substantive claim is confirmed either way for 17, which is absent under every reading.
4. **C3 needed no size exemption and none is claimed.** The block's constraint 4 pre-authorises one, reading the rotation as a wholesale ledger rewrite. Measured, it is a 68-line move at 68 insertions, so the AGENTS.md counting rule is satisfied outright and the single-state-file exemption is left unspent.
5. **No finding was registered by the worker.** `R-1007` is the reviewer's text, arriving in P2 and applied byte for byte at C1.
6. **The commit sequence ran C1, C2, C3, C4, C5 in that order** — no extra commit, none dropped, none reordered — and no path outside the block's change set was written. `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`, `scripts/self_use_queue.json`, `.agent/candidates.md` and `.agent/prose_slips.md` were not touched.

## Next

Round 10, the closure's last: `remedy integrity check --json` reading PASS, the evidence job through `job_evidence.create_manual_completion_bundle`, a FRESH review package whose `base_commit` is the fork point `43d14817` with the two `rev-list` readings agreeing, and then the closure commit — STATUS `[x]`, the README counters, SU-024's `consumed_by` and the final `.agent/` state — followed by the pull request into `main`.
