# Handoff — F276 Data-root hygiene & disk budget · Round 12

## Session

SESSION 3 of feature F276 · round 12 · rounds so far 12

Context self-assessment: the worker read AGENTS.md in full, verified the step
block's bytes before using it — 234 lines, sha256
`c2622cefbeb914c41652bbf9ffd82f2c806a208a15cd65189a3e66184d816789`, both
readings identical to the digest and line count the delegation message named
(R-0954) — then read `docs/agents/handback_template.md` and
`docs/roadmap/STATUS_closure_protocol.md`, found no `.agent/STOP` on disk,
verified all four payloads under `.remedy-wt/f276-r12/` byte-for-byte against
their stated line counts and digests, applied C1, and is writing this
handoff (C2) before running the integrity check, the evidence job and the
review package, all three of which the block's own Bundle places AFTER C2
with the tree clean and nothing further committed — so this file cannot and
does not carry their outputs; those go to the round report instead, exactly
as the block already orders for the package's own name and hash.

## Range

Review of 7625d967..HEAD.

## Commits

### 0365de33 f276-r12: book round 11 verdict, correct round 10 ledger clause (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r12-block.md | 234/0 | shutil.copyfile of P1 (this block) |
| .agent/authored/f276-r12-ledger.md | 2/0 | shutil.copyfile of P2 |
| .agent/authored/f276-r12-plan.md | 49/0 | shutil.copyfile of P3 |
| .agent/authored/f276-r12-prose-slips.md | 2/0 | shutil.copyfile of P4 |
| .agent/live_review.md | 2/0 | append P2: round 11 PASS verdict + correction to the round 10 entry |
| .agent/plan.md | 29/27 | rewrite with P3 |
| .agent/prose_slips.md | 2/0 | append P4: two round-11 reviewer-authoring prose slips |

Insertions by `git show --numstat` sum to 320 (also the `git diff --stat`
"+"-column total, which is the AGENTS.md-designated reading). Well under the
500-line cap; no exception is spent this round.

### This handoff (C2, self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewritten | a handoff cannot table the commit that writes it |

## External actions

- `git push origin feature/f276-data-root-hygiene` — after C2, per G6. Outcome
  reported in the round report (postdates this file by construction).
- No `gh` command was run this round. No pull request was opened, edited or
  merged. No branch was created or deleted. No history was rewritten. No
  force-push.
- No worktree was added or removed. The job worktrees under `.remedy-wt/`
  belong to earlier jobs and were left alone per the block's constraint 4.
  `.remedy-wt/` scratch (rounds 10, 11 and 12's own payload directories) was
  left intact; no `git clean -x` was run.

## Verification

**R-0954 — THE SAVED BLOCK'S OWN BYTES, two readings side by side.**
```
delegation message stated for P1 : lines 234  sha256 c2622cefbeb914c41652bbf9ffd82f2c806a208a15cd65189a3e66184d816789
worker's own reading on disk     : lines 234  sha256 c2622cefbeb914c41652bbf9ffd82f2c806a208a15cd65189a3e66184d816789
EQUAL on both readings: True
```

**ALL FOUR PAYLOADS, verified byte-for-byte before use.**
```
wc -l                            sha256sum
  2 ledger.md                    65a1eced7d05643184c4030dd8043b71a5fd7bea022590462cd46e52f8daf05b
 49 plan.md                      015b73764077a69ae7c7b5e1fb1862af50bfba967a7721bb6387269de0658cdd
  2 prose_slips.md               0183f995c9400e366c261db802b25ba7c544b2d95de1dfccffff094e25073ba3
147 create_f276_evidence.py      6c4b1d91a30557a586ac7e4ade05840b07092f80475264392937d61195f46608
```
Every line count and digest matches the block's P2-P5 statement exactly
(P1's are the R-0954 pair above).

**G1 — TRANSPORT AND STATE, at C1 (0365de33). Command: an on-disk python
check using `git show`. Exit 0.**
```
G1(a) — four authored copies, each == its payload byte for byte: True, True, True, True
G1(a) files measured: 4

G1(b) — live_review.md record append, full byte forensics:
  reading (a) at C1 == 7625d967 bytes + P2 bytes:              True
  reading (b) structural, last 1 paragraph-unit == payload's 1: True (N=1, counted from payload)
  negative control (byte flip in first appended paragraph) rejected by BOTH readings: True

G1(c) — byte equality only:
  .agent/prose_slips.md at C1 == 7625d967 bytes + P4 bytes:    True
  .agent/plan.md at C1 == P3 bytes:                             True

TOTAL READINGS TAKEN: 9
ALL TRUE: True
```

**G2, G3, G4, G5 — necessarily postdate this file.** The block's own Bundle
places the integrity check, the evidence job and the review package "AFTER
C2 and with the tree clean, and committing nothing," and G3's base-commit
readings are explicitly taken "at the commit C2 creates." None of the four
can be run before this file exists, so none of their real output is in this
file; all four are reported in full, with real output and exit codes, in
the round report to the reviewer. G6 (push and the post-push tree checks)
is likewise reported there.

## Authored-text proofs

Four files copied via `shutil.copyfile`, each verified byte-identical to its
source payload immediately after copy (see G1(a) above): `.agent/authored/
f276-r12-block.md`, `-ledger.md`, `-plan.md`, `-prose-slips.md`. The
record-append fidelity for `.agent/live_review.md` is proven in G1(b) above
by two independent readings plus a negative control; the byte-equality
readings for `.agent/prose_slips.md` and `.agent/plan.md` are in G1(c).

## Open findings

19 open by distinct id, unchanged from `c6a519d1` (round 11's own C1) —
this round registers and resolves nothing. The exact set and the
`Owner: F282.`/`Owner: F282 — Findings paydown v2` split are not
re-measured this round since neither the ledger's content nor its byte
count changed on the open-findings dimension (only round 11's verdict and
the round-10 correction were appended, which touch no `Owner:` line and no
severity marker); the count carried forward from round 11's own G5 is 19.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 the bookkeeping (4 payload copies + 2 appends + 1 rewrite) | done | commit 0365de33 |
| C2 the handoff | done | this file |
| G1 transport and state | done | 9 readings, all True |
| G2 the integrity check | pending | runs after C2 per the block's Bundle; reported in the round report |
| G3 the base commit | pending | runs after C2 per the block's Bundle; reported in the round report |
| G4 the evidence job | pending | runs after C2 per the block's Bundle; reported in the round report |
| G5 the review package | pending | runs after C2 per the block's Bundle; reported in the round report |
| G6 push and tree | pending | runs after C2 per the block's own text; reported in the round report |
| STATUS line, README edit, `consumed_by`, pull request | not done | explicitly out of scope for this round per the block's Goal — belongs to the closure round after this one |

## Deviations & assumptions

1. **The pre-commit `git diff --numstat --cached` reading for C1 (320
   insertions, 27 deletions) and the post-commit `git commit` terminal
   summary line (which read 340 insertions, 47 deletions, with `.agent/
   plan.md` reported as a "rewrite (74%)")** disagree, exactly the same
   class of diff-alignment/rewrite-detection artifact round 11's handoff
   declared as its deviation 2. `git show --numstat HEAD` and `git diff
   --stat` on the committed range both independently confirm 320/27; the
   AGENTS.md counting rule names "the `+` column of `git diff --stat`" as
   authoritative, so 320 is the reading used above and in this round's
   commit-size accounting. The block's own pre-computed insertion estimate
   (this block's 234 lines + 106 = 340) matches the commit-time summary's
   340 rather than the `git diff --stat`/`git show --numstat` reading of
   320; both are reported here rather than silently reconciled. Either
   reading is comfortably under the 500-line cap, so nothing turns on which
   one governs this round.
2. **G2, G3, G4, G5 and G6 are reported in the round report rather than in
   this handoff file**, declared above under Verification and in the item-
   status table. This is not a departure from the block: the Bundle section
   places all of them after C2 with nothing further committed, and G3's own
   text requires the commit C2 creates to already exist. It is declared
   here anyway because the block's C2 instruction, read in isolation, asks
   for "every gate below with its real output and exit code," which is
   physically impossible for a gate that has not yet run at the moment this
   file is written and committed.
3. **No destructive verification, no disposable worktree** — none was
   ordered by this round's gates, consistent with constraint 4.
4. **Open-findings count (19) is carried forward from round 11's own G5
   rather than re-measured this round** — declared above under Open
   findings, since neither payload applied this round touches a `Owner:`
   line, a severity marker, or registers/resolves any R-id.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: there
was none at the point this file is written. The sequence executed so far is
exactly C1 then C2, in that order, with no extra commit and none dropped or
reordered. Whether anything after C2 leaves a tracked file modified — which
constraint 3 would make a finding — is checked and reported in the round
report's G5/G6 readings.

## Next

Run, without committing anything: the integrity check (`remedy integrity
check --json`), the evidence job
(`python3 .remedy-wt/f276-r12/create_f276_evidence.py`), and the review
package (`bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f276_evidence_closure`) from the clean tree at this commit. Push
the branch. Report every gate's real output, the package's filename,
SHA-256 and archived path to the reviewer, and write those four readings to
`.remedy-wt/f276-r12/package.txt`. The reviewer then authors the STATUS
line and DECISION F276 D11's closure round applies it, the README
paragraph and counters, `consumed_by`, the final `.agent/` state and the
pull request.
