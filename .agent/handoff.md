# Handoff — F276 Data-root hygiene & disk budget · Round 14 (THE CLOSING ROUND)

## Session

SESSION 3 of feature F276 · round 14 · rounds so far 14

Context self-assessment: the worker read `AGENTS.md` in full, verified the
step block's bytes before using it — 221 lines, sha256
`bd2bab1081780ffb3ae2f45889c15d8fa1849fa51379e397dc6b0403950794fd`, both
readings identical to the digest and line count the delegation message
named (R-0954) — then read `docs/agents/handback_template.md` and
`docs/roadmap/STATUS_closure_protocol.md`, found no `.agent/STOP` on disk,
verified all five reviewer-authored payloads under `.remedy-wt/f276-r14/`
(P2-P6, the ledger append, the plan rewrite, the prose-slip append and the
STATUS/README FROM-TO pairs) byte-for-byte against their stated line counts
and digests, applied C1 (committed as `945b9e93`), ran G1's full transport
and record-append forensics against that commit, and is now applying and
committing C2 — the closure commit, the LAST on this branch — which is the
commit that writes this very file. G2 through G6 all read or postdate C2
(each reads `git show <C2>:<path>` or the working tree after C2, or the
push/PR that follow it), so none of their outputs can exist inside a file
committed AS PART OF C2; they are reported in full, with real output and
exit codes, in the round report instead — exactly the constraint the round
13 handoff already documented for its own G4-G6.

One explicit note on the Handback section's instruction that this file
additionally state "that the pull request is OPEN and UNMERGED": the
Bundle orders C2 (which commits this file) BEFORE the pull request is
opened ("Then, AFTER C2 and committing nothing further: the pull
request"), so no committed byte of this file can truthfully assert an
OPEN PR at the moment it is written — doing so would be recording a future
fact as already true. This file states everything precommit-known (the
accepted HEAD, the package, the evidence job id, the open-findings count);
the PR's number, URL and its OPEN/UNMERGED status are stated in the round
report, which is written after the PR exists and is the artifact that
necessarily carries them.

## Range

Review of 03e72f77..HEAD (HEAD after this commit is the closure commit).

## Commits

### 945b9e93 f276-r14: book round 13 verdict, save round 14 payloads (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r14-block.md | 221/0 | shutil.copyfile of P1 (this block) |
| .agent/authored/f276-r14-ledger.md | 2/0 | shutil.copyfile of P2 |
| .agent/authored/f276-r14-plan.md | 43/0 | shutil.copyfile of P3 |
| .agent/authored/f276-r14-prose-slips.md | 1/0 | shutil.copyfile of P4 |
| .agent/authored/f276-r14-readme-to.txt | 8/0 | shutil.copyfile of P6's TO |
| .agent/authored/f276-r14-status-to.txt | 1/0 | shutil.copyfile of P5's TO |
| .agent/live_review.md | 2/0 | append P2: round 13 PASS verdict |
| .agent/plan.md | 23/29 | rewrite with P3 |
| .agent/prose_slips.md | 1/0 | append P4: numeral-provenance rule |

Insertions by `git show --numstat 945b9e93` sum to 302 (221+2+43+1+8+1+2+23+1).
Well under the 500-line cap; no exception spent this round (constraint 4 —
the AGENTS.md oversize exception is already spent by `c6a519d1` and
unavailable here). `git commit`'s own terminal summary read "322
insertions(+), 49 deletions(-)" for this commit, which applies rename
detection and is NOT the DECISION F104 D1 reading — declared here per
constraint 4 so the discrepancy is not mistaken for a miscount.

### THIS COMMIT (C2, self-reference, R-0149 pattern — the closure commit and the LAST on this branch)
| Path | Reason |
|------|--------|
| docs/roadmap/STATUS.md | P5 applied: FROM (1 line) replaced by TO (1 line), single literal replacement, FROM measured to occur exactly once before replacing |
| README.md | P6 applied: FROM (2 lines) replaced by TO (8 lines), single literal replacement, FROM measured to occur exactly once before replacing |
| scripts/self_use_queue.json | the one `consumed_by` field of the item whose `id` is `SU-024` set from `""` to `"f276"`; no other field of that item and no other item touched; 24 items before and after, non-empty `consumed_by` count 23 before and 24 after |
| .agent/handoff.md | rewritten — a handoff cannot table the commit that writes it |

A handoff cannot know its own commit's `git show --numstat` reading before
it exists; that reading, and the confirmation that these are the ONLY four
paths in C2, are taken with `git show --numstat <C2-sha>` after the commit
and reported in the round report (G2's own instruction).

## External actions

None yet at the time this file is written. `git push
origin feature/f276-data-root-hygiene` and `gh pr create` both happen
AFTER C2 with nothing further committed (Bundle ordering); their outcomes —
including the PR number and URL, and the explicit statement that it is
NOT merged — are reported in the round report, which necessarily postdates
this file (G6's own instruction). No `gh pr merge` is run this round or
ever will be by this worker (guardrail G1 of the delegation). No branch was
created or deleted, no history was rewritten, no force-push.

## Verification

**R-0954 — THE SAVED BLOCK'S OWN BYTES, two readings side by side.**
```
delegation message stated for P1 : lines 221  sha256 bd2bab1081780ffb3ae2f45889c15d8fa1849fa51379e397dc6b0403950794fd
worker's own reading on disk     : lines 221  sha256 bd2bab1081780ffb3ae2f45889c15d8fa1849fa51379e397dc6b0403950794fd
EQUAL on both readings: True
```

**PAYLOADS P2-P6, verified byte-for-byte before use.**
```
wc -l   file                sha256sum
  2     ledger.md            20fe134c152516e2fd5b933634eb409eff3db959884580abe971c8b8cd627acc
 43     plan.md               607dd750ff17c96a363513030fd061cc088abe56d41ddaaab4f2480cf42ddd56
  1     prose_slips.md       2176701a7502aa673c0a1727546ad0a1cbc862de53e09bc11fb0c428f9584b85
  1     status_from.txt      1f9b47ef799e660fe82255feb20fc9680f05b15b322942386f962d505435d627
  1     status_to.txt        e7b14e0407b647cad562ef630e0b903f9ba9dd1a90bea312187368ea53f90c01
  2     readme_from.txt      0d0f0e899b4e31ddc722dbaf61b2b2ea1ef031718528bb33ac9cc9e881a7daef
  8     readme_to.txt        8f288cf168449ef2e4ef8e6e0c8ba86101b0881beb817863427c5c5c1049a556
```
Every line count and digest matches the block's P2-P6 statement exactly
(P1's is the R-0954 pair above).

**G1 — TRANSPORT AND STATE, at C1 (945b9e93). Command: on-disk python
checks against `git show 03e72f77:<path>`.**
```
(a) five authored copies, each == its payload byte for byte: True x6
    (block.md, ledger.md, plan.md, prose_slips.md, status_to.txt, readme_to.txt)
    files measured: 6

(b) .agent/live_review.md record append, full byte forensics:
    reading (a) byte equality (03e72f77 bytes + P2 bytes):        True
    reading (b) structural, independent paragraph-split reader,
      N=1 computed from the merged-vs-before paragraph delta,
      last 1 unit == P2's 1 contributed unit, in order:            True
    negative control (byte flip 5 bytes into the first appended
      paragraph) rejected by BOTH readings:                        True

(c) byte equality only:
    .agent/prose_slips.md at C1 == 03e72f77 bytes + P4 bytes:      True
    .agent/plan.md at C1 == P3 bytes exactly:                      True

TOTAL READINGS TAKEN: 6 (a-all-files, b-reading-a, b-reading-b,
  b-negative-control, c-prose-slips, c-plan)
ALL TRUE: True
```

**G2 through G6 — necessarily postdate this file**, because this file is
committed AS PART OF C2 and every one of those gates reads `git show
<C2>:<path>` or the tree/push/PR state that follows C2. All are run for
real, with real output and exit codes, and reported in full in the round
report to the reviewer.

## Authored-text proofs

Six files copied via `shutil.copyfile` at C1, each verified byte-identical
to its source payload immediately after copy (see G1(a) above):
`.agent/authored/f276-r14-block.md`, `-ledger.md`, `-plan.md`,
`-prose-slips.md`, `-status-to.txt`, `-readme-to.txt`. The record-append
fidelity for `.agent/live_review.md` and `.agent/prose_slips.md` at C1 is
proven in G1(b) and G1(c) above. P5 and P6's application to
`docs/roadmap/STATUS.md` and `README.md` is a direct FROM/TO literal
replacement, not a copy from `.agent/authored/`; its own fidelity proof
(FROM count before, TO-present/FROM-absent after, read out of the C2
commit) is G2's, reported in the round report because it requires C2 to
already exist.

## Open findings

By distinct id, at C1 (945b9e93) and unchanged through C2 (neither the
STATUS/README/queue edits nor this file touch `.agent/live_review.md`): 19
open — `- R-id` registrations (23 distinct) minus `Done: R-id` resolutions
(4 distinct). The set: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829,
R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1004,
R-1005, R-1007, R-1008, R-1009 — every one of them carrying `Owner: F282`
(the short spelling; all 19 counted).

## Closing-round durable facts

- Accepted HEAD: `03e72f77fd74e72d6cdc8b2d2f00e3efe76e0315`
- Package: `remedy-review-20260920-150902-READY_FOR_REVIEW.zip`
- Package SHA-256: `b36e23f1e04adf64f953ba9fbc5825ff5a9942af97a8133616646417d6cd01f3`
- Package archived path: `/home/decodeux/Repos/remedy-history/zips`
- Evidence job id: `f276r13e1001`
- Open-findings count: 19, all `Owner: F282`
- Pull request: not yet opened as of this commit (opens immediately after,
  per Bundle ordering); its number, URL, and the explicit statement that
  it is NOT merged are in the round report.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 the bookkeeping (6 payload copies + 2 appends + 1 rewrite) | done | commit 945b9e93 |
| C2 the closure commit (STATUS, README, queue, handoff) | done | this commit |
| G1 transport and state | done | 6 readings, all True |
| G2 the closure edit is exact | pending | runs after C2; reported in round report |
| G3 the ledger pins (tests/docs) | pending | runs after C2; reported in round report |
| G4 the canary and the queue | pending | runs after C2; reported in round report |
| G5 the integrity check and the open set | pending | runs after C2; reported in round report |
| G6 push, pull request and tree | pending | runs after C2; reported in round report |
| Pull request | pending | opened after C2, per Bundle ordering; not merged (guardrail) |

## Deviations & assumptions

1. **The Handback section's literal instruction that this file state the
   PR is OPEN and UNMERGED could not be honored inside the committed
   file**, because the Bundle orders the PR strictly after C2 and commits
   nothing further with it. This file states every other closing-round
   fact the section orders (accepted HEAD, package, evidence job id,
   open-findings count) and defers the PR's number/URL/unmerged status to
   the round report, which is written after the PR exists. Declared as a
   deviation from the letter of the instruction, not from its intent.
2. **G1(b)'s N is 1 here** (P2 carries exactly one paragraph: the round
   13 verdict), computed mechanically from the merged-vs-before paragraph
   delta rather than asserted from the block's prose.
3. **`git commit`'s own terminal summary for C1** read 322/49, not the
   302/29 the `git show --numstat` DECISION F104 D1 reading gives (rename
   detection); declared per constraint 4, the numstat reading is the one
   that governs the 500-line cap and it is well clear at 302.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: there
was none. The sequence executed is exactly C1 then C2, in that order, with
no extra commit and none dropped or reordered. C2 is the last commit on
the branch, as ordered.

## Next

Run, after this commit, without committing anything further except the
push and the PR the Bundle explicitly permits: G2 (the closure-edit
exactness readings via `git show <C2>:<path>`), G3 (`python3 -m pytest
tests/docs/ -q`), G4 (`python3 -m pytest tests/cli/test_golden_path.py -q`
plus the queue counts), G5 (`python3 -m apps.cli.main integrity check
--json` plus the open-set/owner counts), then G6 (push, `gh pr create`
against `main`, `git status --porcelain`, absence of `.agent/STOP`, `git
worktree list`). Report every gate's real output and exit code, the pull
request's number and URL, and an explicit statement that it was not
merged. The merge itself is deferred to the next feature's Open PR Gate.
