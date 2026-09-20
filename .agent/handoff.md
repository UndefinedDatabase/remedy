# Handoff — F276 Data-root hygiene & disk budget · Round 15 (THE REPAIR THAT COMPLETES THE CLOSURE)

## Session

SESSION 3 of feature F276 · round 15 · rounds so far 15

Context self-assessment: the worker read `AGENTS.md` in full, verified the
step block's bytes before using it — 233 lines, sha256
`a11e206561a7f9193053fae4df29faa12448bd59d54e791e8b2292da87b9963b`, both
readings identical to the digest and line count the delegation message
named (R-0954) — read `docs/agents/handback_template.md`, found no
`.agent/STOP` on disk, verified all six payloads P2-P6 (plus the P7
README pairs) byte-for-byte against the block's stated line counts and
digests, ran G2's base reading at `b07a2eda` BEFORE C1 (`2 failed, 312
passed`, exit 1, matching the block's own reading), applied C1 (bookkeeping,
`0c048ce9`), applied and committed C2 (the repair, `692dbaba`), re-ran G2 and
read `314 passed`, exit 0, applied and committed C3 (the resolution,
`c48d903a`), ran G1's full transport and record-append forensics (including
both negative controls) plus G4 and G5, and is now writing this handoff as
C4. G6 (push and tree) necessarily postdates this commit and is reported in
the round report only, per the block's own instruction (item 31).

## Range

Review of `b07a2eda`..`HEAD` (HEAD after this commit is C4, the handoff).

## Commits

### 0c048ce9 f276-r15: book round 14 verdict, register R-1011, save round 15 payloads (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r15-block.md | 233/0 | shutil.copyfile of P1 (this block) |
| .agent/authored/f276-r15-candidates.md | 41/0 | shutil.copyfile of P5 |
| .agent/authored/f276-r15-ledger-done.md | 2/0 | shutil.copyfile of P6 |
| .agent/authored/f276-r15-ledger.md | 4/0 | shutil.copyfile of P2 |
| .agent/authored/f276-r15-plan.md | 40/0 | shutil.copyfile of P3 |
| .agent/authored/f276-r15-prose-slips.md | 1/0 | shutil.copyfile of P4 |
| .agent/candidates.md | 1/17 | rewrite with P5: F276 closure-gate entry retired to a resolved pointer |
| .agent/live_review.md | 4/0 | append P2: round 14 PASS verdict + registration of R-1011 |
| .agent/plan.md | 18/21 | rewrite with P3: round 15 plan |
| .agent/prose_slips.md | 1/0 | append P4: the three-README-places rule |

`git show --numstat 0c048ce9` insertions sum to 345
(233+41+2+4+40+1+1+4+18+1). Well under the 500-line cap; no exception spent
(constraint 4 — the AGENTS.md oversize exception is already spent by
`c6a519d1` and unavailable here). `git commit`'s own terminal summary read
"367 insertions(+), 60 deletions(-)" for this commit, which applies rename
detection and is NOT the DECISION F104 D1 reading — declared per constraint
4 so the discrepancy is not mistaken for a miscount.

### 692dbaba f276-r15: repair README's accepted-count and Tier 2 Done cell (C2)
| Path | +/- | Reason |
|------|-----|--------|
| README.md | 2/2 | COUNT pair: "86 of 282 registered items accepted." → "87 of 282 registered items accepted."; TIER pair: Tier 2 Done cell 28 → 29. Each FROM measured to occur exactly once before replacing. No other path touched. |

`git show --numstat 692dbaba` reads `2	2	README.md` — one path, insertion
count 2, matching G3's requirement exactly.

### c48d903a f276-r15: book Done R-1011, resolved by this round's C2 (C3)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 2/0 | append P6: the `Done: R-1011` resolution paragraph, committed after C2 as its own text requires |

`git show --numstat c48d903a` reads `2	0	.agent/live_review.md` — the whole
change set of C3, as ordered.

### THIS COMMIT (C4, self-reference, R-0149 pattern — the handoff)
| Path | Reason |
|------|--------|
| .agent/handoff.md | rewritten — a handoff cannot table the commit that writes it |

## External actions

`git push origin feature/f276-data-root-hygiene` happens AFTER this commit
(Bundle ordering); its outcome is reported in the round report (G6's own
instruction), which necessarily postdates this file. No `gh` command is run
this round — pull request 262 exists, needs no edit, and must not be merged
(constraint 6). No branch was created or deleted, no history was rewritten,
no force-push, no worktree added or removed.

## Verification

**R-0954 — THE SAVED BLOCK'S OWN BYTES, two readings side by side.**
```
delegation message stated for P1 : lines 233  sha256 a11e206561a7f9193053fae4df29faa12448bd59d54e791e8b2292da87b9963b
worker's own reading on disk     : lines 233  sha256 a11e206561a7f9193053fae4df29faa12448bd59d54e791e8b2292da87b9963b
EQUAL on both readings: True
```

**PAYLOADS P2-P6 and the P7 README pairs, verified byte-for-byte before use.**
```
wc -l   file                sha256sum
  4     ledger.md            e176aae18f87910d135a2b90d5c5b73573c33ab251184b00b014a938d9683b62
 40     plan.md              e7e24f0cb61c4e7633e7127e3f35be90e852ecbf7f6e94702a98848f328cff84
  1     prose_slips.md       2ace9662326e849b58b5ab6cecf5f9e744e46ea05c95532afc395ee69400b85d
 41     candidates.md        5f1aebbb0b6986e3aac2f03eba03678dda45e7e425c0b8df2f6fde90e2eefd1f
  2     ledger_done.md       a1dc6ca2b12beadd8235f89bec9ba0b506c595d5fd86df77f21389352a9b598f
  0     count_from.txt       dc48d8dc77d9db3efcc8887739e2942c58aadd6a9518d679b3adf27329fbe0ac
  0     count_to.txt         a5e2f0fffaa19e04848397ba5652c35d0351b40dda0806f3817a11da80dd30dc
  1     tier_from.txt        026199e6213868b437bab492e3f512d676637214f2b6536c8727240f88da0a2f
  1     tier_to.txt          8200810be780cc382e98b58dfd0acc9a1162eb3c65f816fdf01110c171994a51
```
Every line count and digest matches the block's P2-P6/P7 statement exactly
(P1's is the R-0954 pair above). The COUNT pair's FROM/TO carry no trailing
newline (verified: both end `pted.`); the TIER pair's FROM/TO each end with
one (verified: both end `35 |\n`) — exactly as the block describes, and
neither was added nor stripped.

**Containment test (mechanical, at `b07a2eda`):** all seven pairs the block
lists read `false` for "target contains payload" — P2/P6 into
`.agent/live_review.md`, P4 into `.agent/prose_slips.md`, P3 into
`.agent/plan.md`, P5 into `.agent/candidates.md`, and each README TO into
its own FROM — so every one is NEW bytes and no FROM-count proof was owed
beyond the two README anchor counts below.

**ANCHOR UNIQUENESS, measured before replacing:**
```
grep -c "86 of 282 registered items accepted." README.md   -> 1
grep -c "| 2 | Minimal Self-Build Runtime | 28 | 35 |" README.md -> 1
```
Both FROM texts occur exactly once, as the block requires.

**G1 — TRANSPORT AND STATE.**
```
(a) six authored copies, each == its payload byte for byte: True x6
    (f276-r15-block.md, -ledger.md, -plan.md, -prose-slips.md,
     -candidates.md, -ledger-done.md)
    files measured: 6

(b) .agent/live_review.md record append, full byte forensics, AT C1:
    reading (a) byte equality (b07a2eda bytes + P2 bytes):          True
    reading (b) structural, independent paragraph-split reader,
      N=2 computed from P2's own paragraph count,
      last 2 units == P2's 2 contributed paragraphs, in order:      True
    negative control (byte flip into the middle of the first
      appended paragraph) rejected by BOTH readings:                True

    .agent/live_review.md record append, full byte forensics, AT C3:
    reading (a) byte equality (C1 bytes + P6 bytes):                True
    reading (b) structural, independent paragraph-split reader,
      N=1 computed from P6's own paragraph count,
      last 1 unit == P6's 1 contributed paragraph, in order:        True
    negative control (byte flip into the middle of the first
      appended paragraph) rejected by BOTH readings:                True

(c) byte equality only, at C1:
    .agent/prose_slips.md at C1 == b07a2eda bytes + P4 bytes:       True
    .agent/plan.md at C1 == P3 bytes exactly:                       True
    .agent/candidates.md at C1 == P5 bytes exactly:                 True

TOTAL READINGS TAKEN: 15 — six file-equality readings in (a), three
  booleans in (b) at C1 (reading-a, reading-b, negative-control-rejected),
  three booleans in (b) at C3 (reading-a, reading-b,
  negative-control-rejected), and three booleans in (c) (prose_slips, plan,
  candidates).
ALL TRUE: True
```

**G2 — THE GATE THAT FOUND THE DEFECT, RUN AGAIN.**
```
BEFORE C1, at b07a2eda: python3 -m pytest tests/docs/ -q
  -> 2 failed, 312 passed in 85.17s, exit 1
  failing node ids:
    tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_accepted_count_equals_the_status_count
    tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_tier_table_done_column_matches_the_ledger

AFTER C2: python3 -m pytest tests/docs/ -q
  -> 314 passed in 91.78s, exit 0
```

**G3 — THE REPAIR IS CONFINED AND EXACT.**
```
FROM occurrence count before replacing, in README.md:
  "86 of 282 registered items accepted."                 -> 1
  "| 2 | Minimal Self-Build Runtime | 28 | 35 |"          -> 1

git show 692dbaba:README.md:
  "87 of 282 registered items accepted."                  -> 1 (TO present)
  "86 of 282 registered items accepted."                  -> 0 (FROM absent)
  "| 2 | Minimal Self-Build Runtime | 29 | 35 |"           -> 1 (TO present)
  "| 2 | Minimal Self-Build Runtime | 28 | 35 |"           -> 0 (FROM absent)

git show --numstat 692dbaba:
  2	2	README.md
  (one path, insertion count 2)
```

**G4 — THE LEDGER AND THE CANDIDATES.**
```
open findings by distinct id at C1 (0c048ce9): 20, R-1011 among them: True
open findings by distinct id at C3 (c48d903a): 19, R-1011 among them: False
count of the 19 (at C3) carrying "Owner: F282" (short spelling): 19

git show 0c048ce9:.agent/candidates.md:
  contains "went RED against the closure commit": 0 times
  contains "R-1011": at least once (True)
```

**G5 — THE CANARY AND THE INTEGRITY CHECK, after C3.**
```
python3 -m pytest tests/cli/test_golden_path.py -q
  -> 42 passed in 131.84s, exit 0

python3 -m apps.cli.main integrity check --json
  -> exit 0
  {
    "version": 1,
    "passed": true,
    "fail_count": 0,
    "check_count": 5,
    "checks": [
      {"name": "handler_import", "status": "pass", "message": "handlers=145"},
      {"name": "live_review_verdict", "status": "pass", "message": "Owner: F282 — Findings paydown v2 (re-assigned at F276's closure, 2026-09-20; this line supersedes a"},
      {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
      {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
      {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
    ]
  }
```

**G6 — necessarily postdates this file**, because this file is committed AS
C4 and G6 reads the push and the post-commit tree. It is run for real, with
real output and exit codes, and reported in full in the round report.

## Authored-text proofs

Six files copied via `shutil.copyfile` at C1, each verified byte-identical
to its source payload immediately after copy (see G1(a) above):
`.agent/authored/f276-r15-block.md`, `-ledger.md`, `-plan.md`,
`-prose-slips.md`, `-candidates.md`, `-ledger-done.md`. The record-append
fidelity for `.agent/live_review.md` at C1 and C3, and for
`.agent/prose_slips.md` at C1, is proven in G1(b)/(c) above, each including
a negative control that both readings reject. `.agent/plan.md` and
`.agent/candidates.md` are REWRITES, proven byte-equal to P3 and P5
respectively in G1(c). The two README pairs are direct FROM/TO literal
replacements, not copies from `.agent/authored/`; their fidelity proof
(FROM count before, TO-present/FROM-absent after, read out of the C2
commit) is G3's, above.

## Open findings

By distinct id: 20 at C1 (`0c048ce9`, with `R-1011` newly registered among
them) and 19 at C3 (`c48d903a`, with `R-1011` resolved and no longer among
them) — both readings reported per the block's instruction. All 19 carry
`Owner: F282` (the short spelling; all 19 counted, per G4 above). The set at
C3: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892,
R-0950, R-0984, R-0998, R-0999, R-1000, R-1004, R-1005, R-1007, R-1008,
R-1009. R-1010 and R-1011 were both raised and repaired inside this feature
and are not among them.

## Closing-round durable facts (this round completes F276's closure)

- Accepted HEAD: `03e72f77fd74e72d6cdc8b2d2f00e3efe76e0315`
- Package: `remedy-review-20260920-150902-READY_FOR_REVIEW.zip`
- Package SHA-256: `b36e23f1e04adf64f953ba9fbc5825ff5a9942af97a8133616646417d6cd01f3`
- Package archived path: `/home/decodeux/Repos/remedy-history/zips`
- Evidence job id: `f276r13e1001`
- Pull request: 262, OPEN and UNMERGED. It is the next session's Open PR
  Gate business; no `gh` command was run this round and none will be by
  this worker.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 the bookkeeping (6 payload copies + 2 appends + 2 rewrites) | done | commit `0c048ce9` |
| C2 the repair (README.md, two counter pairs) | done | commit `692dbaba` |
| C3 the resolution (`Done: R-1011` append) | done | commit `c48d903a`, after C2 |
| C4 the handoff | done | this commit |
| G1 transport and state | done | 15 readings, all True; two negative controls, both rejected by both readings |
| G2 the gate that found the defect, run again | done | base `2 failed, 312 passed` exit 1 at `b07a2eda`; after C2, `314 passed` exit 0 |
| G3 the repair is confined and exact | done | FROM=1 both pairs before; TO present/FROM absent after; numstat names only README.md at 2 insertions |
| G4 the ledger and the candidates | done | 20 at C1 (R-1011 in), 19 at C3 (R-1011 out), all 19 `Owner: F282`; candidates.md at C1 carries R-1011 and not the old phrase |
| G5 the canary and the integrity check | done | 42 passed exit 0; integrity `passed: true`, 0 fail, 5/5 checks pass |
| G6 push and tree | pending | runs after C4; reported in round report |
| Pull request | unchanged | 262 remains OPEN and UNMERGED; not touched this round |

## Deviations & assumptions

None. The commit sequence executed is exactly C1, C2, C3, C4, in that
order, with no extra commit and none dropped or reordered. Every payload
was applied byte for byte via `shutil.copyfile` or an explicit byte
write/append, never by retyping. Both README replacements were single
literal string replacements after the FROM was measured to occur exactly
once. No path outside the change set was touched: `docs/roadmap/STATUS.md`,
`scripts/self_use_queue.json` and `docs/roadmap/features/T2_F276.md` were
left untouched per constraint 2. No `gh` command was run. No destructive
verification was ordered and none was performed; no worktree was created
or removed, and the two job worktrees under `.remedy-wt/` were left alone.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: there
was none.

## Next

Run, after this commit, without committing anything further except the
push the Bundle permits: G6 (`git push origin feature/f276-data-root-hygiene`,
then `git status --porcelain` which must be empty, `ls .agent/STOP` which
must be absent, and `git worktree list` in full). Report all four in the
round report. Run NO `gh` command. Pull request 262 remains OPEN and
UNMERGED; merging it is the next session's Open PR Gate business, not this
round's.
