# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 8

## Session

SESSION 4 of feature F277 · round 8 · rounds so far 8

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r8-payloads/block.md` and `docs/roadmap/features/T2_F277.md` in full,
verified the step block's own bytes before using it (R-0954: 245 lines, sha256
`a6c847eb1779d2447ab3242cae42f1535d2de341372d965f61072fcc0aed2f53`, matching the delegation
message's reading exactly), found no `.agent/STOP` on disk, verified the branch was already
`feature/f277-machine-contracts` clean at `a8e2e565`, then began the block's mandatory PAYLOADS
verification (line count + sha256 for all nine files) BEFORE using any of them. Eight of nine
payloads matched the block's table exactly. `decisions.md` did not: same line count (54) but a
different byte count and sha256. Per the block's own constraint 4 ("if a gate goes red, STOP...
do not guess which half of a disagreement is wrong") this is treated as gate G1(a) failing
before any commit was made. **No commit in the round's bundle (C1a-C6) was made.** This handback
and a small blocker note in `.agent/plan.md` are the only changes this round makes.

## Range

Review of `a8e2e565`..`HEAD` (HEAD is this round's single commit).

## Commits

### This commit: F277 R8 C-STOP: record the round 8 payload transport failure and stop
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +23/-19 | rewrite: record the round 8 blocker (decisions.md transport mismatch), no other content change |
| .agent/handoff.md | rewrite | this handback, per the write-once rule |

No other file was touched. C1a, C1b, C2, C3, C4, C5, C6 as ordered by the block were NOT
executed — see Deviations below. `.agent/live_review.md`, `.agent/decisions.md` and
`.agent/prose_slips.md` are untouched at their `a8e2e565` bytes; `.agent/authored/` gained no
new files this round.

## External actions

None. No push, no PR action, no worktree add/remove — the round stopped before any of C1a
through C7 in the block's sequence, and G5's disposable worktree is part of a gate that was
never reached. `git push -u origin feature/f277-machine-contracts` for THIS handback commit is
reported under Verification/G6 below (the one push this round does make, per this round's own
non-negotiable "last act" requirement).

## Verification

### Pre-flight (before PAYLOADS)

- `ls .agent/STOP` → `No such file or directory`. No stop file present.
- `git status --porcelain` → empty.
- `git branch --show-current` → `feature/f277-machine-contracts`.
- `git rev-parse --short HEAD` → `a8e2e565`. Matches the block's stated tip.
- Block self-verification (R-0954): `wc -l .remedy-wt/f277-r8-payloads/block.md` → `245`;
  `sha256sum .remedy-wt/f277-r8-payloads/block.md` →
  `a6c847eb1779d2447ab3242cae42f1535d2de341372d965f61072fcc0aed2f53`. Both match the delegation
  message's two readings exactly.

### G1(a) — PAYLOADS transport (the gate that went RED)

Nine readings, measured with `wc -lc` and `sha256sum` (cross-checked independently with Python's
`hashlib.sha256` for `decisions.md`, same result both ways):

| file | lines measured | lines expected | bytes measured | bytes expected | sha256 measured | sha256 expected | match |
|---|---|---|---|---|---|---|---|
| ledger.md | 2 | 2 | 5157 | 5157 | `38f2c5a3f58030cf4b3b3baeae875f13b42e73eb17c0b3f7c84bcf2bc362b600` | same | True |
| decisions.md | 54 | 54 | **4185** | 4192 | **`2b34e363aca0b6d02e7a61b9e8ac2e1e2dd7d5a7ae2c9db62c1b596a8682e627`** | `4145607740c22809893250005cd84f2dff2ca8b3d0b0bf4f2e3bb30d75bd12f2` | **False** |
| plan.md | 49 | 49 | 2597 | 2597 | `7f42b315bee37d9f74c68f22e41bcc68e1862573621cd1a03555d91b1555fc20` | same | True |
| slips.md | 2 | 2 | 1544 | 1544 | `0f26001c9a85dee6cee14085ae1bb2afde421f1d25296b7569517a8f9f0071f6` | same | True |
| s1-job-context.diff | 104 | 104 | 4620 | 4620 | `8708c77f153c62416992ceaf4466e0a10a712d61d6145174fe74344ebc1d0078` | same | True |
| s2-worker.diff | 105 | 105 | 4102 | 4102 | `3f128a0dbfd2579c1964795dd83d8ae2aff894b7129edcf961a792d5c6598dd2` | same | True |
| s3-change.diff | 136 | 136 | 6203 | 6203 | `e6f0d0dc080e1b5b97cba224872866554cad04bf144a23cbc747be70560503e3` | same | True |
| s4-blocker.diff | 112 | 112 | 4306 | 4306 | `97cac51840be4915cb7f0698daafd8c0bae6d18c91a89ba54a4901f86fda12b2` | same | True |
| s5-contract.diff | 91 | 91 | 3832 | 3832 | `ec46cc2b9ded1869ec9d739ca4388fd68dc0af1cd3f93f266483cb6c2c83ae3f` | same | True |

Eight of nine equal; `decisions.md` is not. `decisions.md`'s line count (54) matches, so no
whole line is missing or extra; the discrepancy is 7 bytes of content somewhere across 54
lines. The file itself parses as coherent, complete markdown prose (DECISION F277 D8, read in
full and quoted nowhere here to avoid retyping it) with no visible truncation, stray carriage
returns (`grep -c $'\r'` → 0), or BOM. The worker did not attempt to identify which specific
byte differs or which side (the file on disk vs. the block's table) is correct — that
determination requires the reviewer's original artifact, which is not something this round has
access to, and guessing is exactly what constraint 4 forbids.

Per the block: "Never retype a payload; never edit one." The worker did not edit, retype, or
otherwise attempt to repair `decisions.md`, and did not proceed to use it (or any payload after
it in the ordered bundle) in a commit.

### G1(b) through G6 — NOT RUN

Every gate from G1(b) onward depends on commits (C1a onward) that were not made, because they
are downstream of the failed G1(a) check in the block's own PAYLOADS section, which the block
states must be verified "BEFORE using" each file. Reporting a gate reading here would be
reporting output that does not exist. None were fabricated.

### G6 (the part that does apply: push and tree, for this round's own commit)

- `git push -u origin feature/f277-machine-contracts` → `a8e2e565..225445d7
  feature/f277-machine-contracts -> feature/f277-machine-contracts`, branch set to track the
  remote. Succeeded.
- `git status --porcelain` after commit and push: empty.
- `git worktree list` after push:
```
/home/decodeux/Repos/remedy                                  225445d7 [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
  Primary checkout plus the two pre-existing `remedy/job-*` worktrees, nothing else. No G5
  worktree was ever created this round.

## Authored-text proofs

None applied. C1a (the `.agent/authored/f277-r8-*` copy step) was not executed, because it
would have copied the unverified `decisions.md` into a second location before the mismatch
could be resolved.

## Deviations & assumptions

1. **The round's full commit bundle (C1a, C1b, C2, C3, C4, C5, C6) was not executed.** Only a
   single out-of-sequence commit was made: a rewrite of `.agent/plan.md` (blocker note) and
   `.agent/handoff.md` (this handback), following AGENTS.md's "If Blocked" protocol rather than
   the block's ordered sequence. Reason: `decisions.md`'s measured bytes/sha256 disagree with
   the block's PAYLOADS table while its line count agrees, and the block's own constraint 4
   requires stopping rather than guessing which side is wrong or repairing either one. Since
   `decisions.md` is consumed by both C1a (byte-copy into `.agent/authored/`) and C1b (append
   into `.agent/decisions.md`), and every later commit in the bundle is sequenced after C1b,
   the entire bundle was withheld rather than partially applied out of order.
2. **The five `.diff` files (s1-s5) and the other three state payloads (ledger.md, plan.md,
   slips.md) all verified byte-for-byte clean.** The worker considered applying C2-C6 alone
   (they do not read `decisions.md`), but did not, because doing so would reorder the block's
   fixed commit sequence (C1a/C1b before C2-C6) — itself a deviation the handback template
   flags (R-0485 pattern) — on top of an already-open integrity question, compounding rather
   than containing the uncertainty. This is a judgment call, recorded here for the reviewer to
   overturn if a different reading of "commit what is verified" is intended.
3. No payload was edited, retyped, or worked around. No file outside `.agent/plan.md` and
   `.agent/handoff.md` was modified.

## Next

Operator/reviewer investigates the `decisions.md` transport mismatch (regenerate the payload,
or correct the block's table entry, whichever is actually wrong) and issues a corrected round 8
(or a round 9) block; the worker re-verifies all nine payloads from scratch before making any
commit, then executes the bundle (C1a through C7) and all six gates as originally ordered.
