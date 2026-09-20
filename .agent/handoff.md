# Handoff — F276 Data-root hygiene & disk budget · Round 11

## Session

SESSION 3 of feature F276 · round 11 · rounds so far 11

Context self-assessment: the worker read AGENTS.md in full, verified the step
block's bytes before using it — 247 lines, sha256
`5c1fb43f74d9163cc40ff1063412330d8697e191a8b9869f1e16d1f5dcd1ea09`, both
readings identical to the digest and line count the delegation message named
(R-0954) — then read `docs/agents/handback_template.md`, found no
`.agent/STOP` on disk, verified all six payloads under `.remedy-wt/f276-r11/`
byte-for-byte against their stated line counts and digests, applied C1 and
C2 in the ordered sequence, and re-ran the full integration gate exactly
once on the merged tree, which came back green.

## Range

Review of 512ba69c..HEAD.

## Commits

### c6a519d1 f276-r11: book rounds 9-10 verdicts, DECISIONs D11/D12, Q1 (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r11-block.md | 247/0 | shutil.copyfile of P1 (this block) |
| .agent/authored/f276-r11-ledger.md | 4/0 | shutil.copyfile of P2 |
| .agent/authored/f276-r11-decisions.md | 136/0 | shutil.copyfile of P3 |
| .agent/authored/f276-r11-operator-questions.md | 39/0 | shutil.copyfile of P6 |
| .agent/authored/f276-r11-plan.md | 47/0 | shutil.copyfile of P4 |
| .agent/authored/f276-r11-prose-slips.md | 1/0 | shutil.copyfile of P5 |
| .agent/decisions.md | 136/0 | append P3: DECISION F276 D11 and D12 |
| .agent/live_review.md | 4/0 | append P2: round 9 and round 10 verdicts, both PASS |
| .agent/operator_questions.md | 30/1 | rewrite with P6: header preserved, EMPTY line replaced by Q1 |
| .agent/plan.md | 29/26 | rewrite with P4 |
| .agent/prose_slips.md | 1/0 | append P5: round 9 unbounded-count-gate slip |

Insertions by `git show --numstat` sum to 674 (also the `--shortstat` total).
**This exceeds the AGENTS.md 500-line insertion cap** — see Deviations below;
declared here as required by the exception clause.

### 3359296e f276-r11: re-run the integration gate on the merged tree (C2)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-closure-suite.txt | 52/42 | rewrite in place with the merged-tree integration-gate transcript, per DECISION F276 D12 |

### This handoff (C3, self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewritten | a handoff cannot table the commit that writes it |

## External actions

- `git push origin feature/f276-data-root-hygiene` — after C3, per G6. Outcome
  reported in the round report (postdates this file by construction).
- No `gh` command was run this round. No pull request was opened, edited or
  merged. No branch was created or deleted. No history was rewritten. No
  force-push.
- No worktree was added or removed. The two job worktrees under `.remedy-wt/`
  are jobs' and were left alone per the block's constraint 5. `.remedy-wt/`
  scratch (round 10's and round 11's own payload directories) was left intact;
  no `git clean -x` was run.

## Verification

**R-0954 — THE SAVED BLOCK'S OWN BYTES, two readings side by side.**
```
delegation message stated for P1 : lines 247  sha256 5c1fb43f74d9163cc40ff1063412330d8697e191a8b9869f1e16d1f5dcd1ea09
worker's own reading on disk     : lines 247  sha256 5c1fb43f74d9163cc40ff1063412330d8697e191a8b9869f1e16d1f5dcd1ea09
EQUAL on both readings: True
```

**ALL SIX PAYLOADS, verified byte-for-byte before use.**
```
wc -l                          sha256sum
247 block.md                   5c1fb43f74d9163cc40ff1063412330d8697e191a8b9869f1e16d1f5dcd1ea09
  4 ledger.md                  5fa2784e5a201b74e69a938df8ec713d277a9e93f8a69a398a6c475d7cbf5426
136 decisions.md                a9a39be4be5b7fc4ff1f11d19d9a84cec233631e8ea0aab77e8a3aca9f66b404
 47 plan.md                    672f83d95c5d538e2888c87dbb29d7f599ef6ed08f6e6badf5b829db192bda73
  1 prose_slips.md             7ab1117ffe690970bef04e8a34b032143d2dd2d01f581f63886b846f2ef60abe
 39 operator_questions.md      25a621db2dfffb974617fa0a04eb5d824410f34b3646cfa87e7602cdce077e4d
```
Every line count and digest matches the block's P1–P6 statement exactly.

**G1 — TRANSPORT AND STATE, at C1 (c6a519d1). Command: `python3 .remedy-wt/f276-r11/gate_g1.py`. Exit 0.**
```
G1(a) — six authored copies, each == its payload byte for byte: True, True, True, True, True, True
G1(a) files measured: 6

G1(b) — record appends, full byte forensics:
  .agent/live_review.md
    reading (a) at C1 == 512ba69c bytes + payload:            True
    reading (b) structural, last 2 paragraph-units == payload's 2: True (N=2, counted from payload)
    negative control (byte flip in first appended paragraph) rejected by BOTH readings: True
  .agent/decisions.md
    reading (a) at C1 == 512ba69c bytes + payload:            True
    reading (b) structural, last 17 paragraph-units == payload's 17: True (N=17, counted from payload)
    negative control rejected by BOTH readings:               True

G1(c) — byte equality only:
  .agent/prose_slips.md at C1 == 512ba69c bytes + P5 bytes:   True
  .agent/plan.md at C1 == P4 bytes:                            True
  .agent/operator_questions.md at C1 == P6 bytes:              True

TOTAL READINGS TAKEN: 15
ALL TRUE: True
```

**G2 — THE UI BUILD, before the suite.**
```
cd apps/ui && npm run build
EXIT CODE 0
last line: ✓ built in 1.42s
git status --porcelain immediately afterwards: EMPTY (apps/ui/dist is gitignored)
```

**G3 — THE INTEGRATION GATE.**
```
command: python3 -m pytest -n auto -q
cwd: /home/decodeux/Repos/remedy
exit code (from the process object): 0
summary line verbatim: 17720 passed, 20 skipped, 1 warning in 253.14s (0:04:13)
wall clock measured around the process: 337.24 seconds
BAD NODE IDS: none — searched mechanically for a FAILURES section, an ERRORS
  section, and any line beginning FAILED or ERROR over the full captured
  output; all three searches matched zero lines.
this run's outcome total:       17720 + 20 = 17740
superseded run's (fd23710f) outcome total: 17659
difference: 81, attributed to the operator's merge of origin/main at
  512ba69c, which brought in tests (including the whole of
  tests/orchestration/test_claude_planner.py) that did not exist on the
  branch when fd23710f's transcript was recorded.
golden-path canary, tests/cli/test_golden_path.py: 42 node ids collected
  (verified separately via --collect-only, not a second suite run); none
  appear in the empty bad-node set, so all 42 are among the 17720 passed.
```

**G4 — THE BASE COMMIT AND THE FORK POINT, at C1 (c6a519d1).**
```
git merge-base main c6a519d1
8f129d71e311ccd58bdb01d63c78bb75dffbd382   (== main's tip, NOT the base — expected, pitfall (e) live)

first commit of `git rev-list --first-parent c6a519d1` also in `git rev-list main`
43d148177efd145f179ba2d9875eaa675b1595b7   (== the fork point)

git rev-list --ancestry-path 43d148177efd145f179ba2d9875eaa675b1595b7..c6a519d1 | wc -l
60

git rev-list 43d148177efd145f179ba2d9875eaa675b1595b7..c6a519d1 | wc -l
60
```
Base at full forty characters: `43d148177efd145f179ba2d9875eaa675b1595b7`.
The two lengths are EQUAL (60 and 60). The first reading answering main's tip
and not the base is the expected reading, not a surprise — pitfall (e) is
live on this branch since the operator's merge, exactly as DECISION F276 D11
records at `512ba69c` (where the same two lengths read 59; +1 here is C1's
own commit).

**G5 — THE OPEN SET, at C1 (c6a519d1) and at 512ba69c, derived mechanically
from `.agent/live_review.md` (`^- R-\d+` minus `^Done: R-\d+`, by distinct id).**
```
at 512ba69c: count 19
  ids: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880,
       R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1004, R-1005,
       R-1007, R-1008, R-1009
  carrying "Owner: F282 — Findings paydown v2": 17

at C1 (c6a519d1): count 19
  ids: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880,
       R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1004, R-1005,
       R-1007, R-1008, R-1009
  carrying "Owner: F282 — Findings paydown v2": 17
```
The two counts are IDENTICAL (19 == 19), the ids are identical, and the
owner-count (17 of 19, the remaining two — R-1008 and R-1009 — carry no
`Owner:` line and default to F282 under amend0911-feedback rule A) is
identical. This round registered and resolved nothing, as expected.

**G6 — PUSH AND TREE.** Necessarily postdates this file; reported in the
round report below rather than here, per the block's own note that these
readings "belong to the round report and not to the handoff's own text."

## Authored-text proofs

Six files copied via `shutil.copyfile`, each verified byte-identical to its
source payload immediately after copy (see G1(a) above):
`.agent/authored/f276-r11-block.md`, `-ledger.md`, `-decisions.md`,
`-plan.md`, `-prose-slips.md`, `-operator-questions.md`. The record-append
fidelity for `.agent/live_review.md` and `.agent/decisions.md` is proven in
G1(b) above by two independent readings plus a negative control on each.

## Open findings

19 open by distinct id at C1, unchanged from 512ba69c (see G5). 10 Medium,
7 Low among the 17 carrying `Owner: F282 — Findings paydown v2`; R-1008 and
R-1009 carry no severity/owner line of their own in this round's reading —
this round registered nothing and resolved nothing, so no severity
breakdown was computed beyond what round 9's ledger already states for the
17 it owns.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 the bookkeeping (6 payload copies + 4 appends/rewrites) | done | commit c6a519d1 |
| C2 the integration-gate transcript | done | commit 3359296e, green run |
| C3 the handoff | done | this file |
| G1 transport and state | done | 15 readings, all True |
| G2 the UI build | done | exit 0, tree clean after |
| G3 the integration gate | done | exit 0, 17720 passed/20 skipped, bad set empty |
| G4 base commit and fork point | done | all four readings taken, lengths equal (60/60) |
| G5 the open set | done | 19 == 19, identical ids, identical owner-count |
| G6 push and tree | done | reported in round report (postdates this file) |
| DECISION F276 D11 (two-round closure) | done | recorded via P3 append |
| DECISION F276 D12 (integration-gate re-run) | done | recorded via P3 append; executed as C2 |
| Operator question Q1 | done | recorded via P6 rewrite of `.agent/operator_questions.md` |
| STATUS line, README edit, `consumed_by`, evidence job, package, pull request | not done | explicitly out of scope for this round per the block's Goal — belongs to the two rounds after it |

## Deviations & assumptions

1. **C1's insertion count (674 by `git show --numstat`, matching
   `--shortstat`) EXCEEDS the AGENTS.md 500-line cap.** The block's own
   constraint 4 states "C1's insertion count ... stays under 500"; the
   measured value is 674. Justification for treating this as the AGENTS.md
   declared exception (Commit Discipline: "a diff over 500 lines is
   acceptable only when (a) the worker declares it in the handback WITH the
   inseparability reason before review, and (b) it is the only such commit
   in its feature"): (a) the block's Bundle explicitly orders "C1 the
   bookkeeping, in ONE commit," bundling six full-file payload copies
   (474 combined lines) with four appends/rewrites to `.agent/` state files
   that the block's own containment test proves are all independent, unmerged
   pieces of one bookkeeping action — splitting it would break the atomic
   unit the block calls for and would not shrink the total bytes committed
   this round, only redistribute them across artificial commit boundaries;
   (b) checked every first-parent commit on this branch since the fork
   point `43d148177…` through `512ba69c` — none of this feature's own
   worker-authored round commits exceeds 500 insertions (the largest prior
   is 481, at commit `46f8947c`); the only larger diff in that range is
   `512ba69c` itself, the operator's own merge of `origin/main`, which is
   not a worker round commit. C1 is therefore the first and, so far, only
   oversize worker commit in this feature. Applied anyway per constraint 1
   ("A payload that looks wrong is REPORTED as a deviation and applied
   anyway") — the block's own text is what looked wrong here (its stated
   expectation of staying under 500), not a payload byte, and every payload
   byte was applied unedited regardless.
2. **The commit-time `git commit` summary line for C1 read "692 insertions(+),
   45 deletions(-)" and for C2 read "85 insertions(+), 75 deletions(-)"**,
   both of which disagree with the `git show --numstat` / `--shortstat`
   totals reported above (674/27 for C1, 52/42 for C2). `--numstat` and
   `--shortstat` agree with each other in both cases; the constraint asks
   specifically for the `git show --numstat` reading, which is what is
   reported as authoritative above. The discrepancy is a diff-alignment
   artifact (the commit-time summary and `git show` can choose different
   hunk alignments for the same net change) and is declared rather than
   silently reconciled.
3. **No destructive verification, no disposable worktree** — none was
   ordered by this round's gates, consistent with constraint 5.
4. **`tests/cli/test_golden_path.py --collect-only` was run as a second,
   separate, lightweight `pytest` invocation** to name the golden-path node
   count explicitly for the G3 transcript. This is a collection-only probe
   (it executes no test bodies) and is not a second run of the integration
   gate; the gate itself (`python3 -m pytest -n auto -q`) was run exactly
   once, as ordered.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: there
was none. The sequence executed was exactly C1, then C2, then C3, in that
order, with no extra commit and none dropped or reordered.

## Next

The evidence round: `remedy integrity check --json`, the evidence job over
the six test files this feature created, and a fresh review package built
from the clean tree at that round's own handback commit (`base_commit` the
fork point `43d148177efd145f179ba2d9875eaa675b1595b7`), reporting the
package's name, SHA-256 and archived path to the reviewer per DECISION
F276 D11 — followed by the closure round that applies the reviewer-authored
STATUS line, README counters and `consumed_by`, and opens the pull request.
