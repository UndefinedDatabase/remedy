# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). The closure pull request
is created by this round and is NOT merged in this session — it merges at the
next feature's start through the AGENTS.md Open PR Gate, which is the
operator's manual-review window.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`). F277 closes on the first two complete
and the third half applied; DECISION F277 D10 moved the rest to F283.

## Current Step

THE CLOSURE ROUND. Round 17's package is READY_FOR_REVIEW and every
precondition holds: the integration gate is green at 17813 passed, the
self-use item SU-025 was run to the approval gate, `integrity check` passes
on all five checks, the feature file's Built State is current, and the tree
is clean. This round books round 17's PASS, resolves R-1014 through the
checklist consolidation, rotates the ledger, and flips STATUS to `[x]` with
the README sync and the SU-025 `consumed_by` edit in one commit.

## Next Steps

F277 has nothing after this round. What follows belongs to the next session:

1. The Open PR Gate merges this feature's pull request before any new branch
   is cut — not this session, by guardrail G1.
2. Rule A5 then proposes F283, which stands directly behind F277 in the
   ledger: the refusal sweep over the nineteen unmigrated CLI modules, the
   read-only-without-`supports_json` set, and the exit-code taxonomy.
3. F283's first round fills its file at claim; the three Acceptance bullets
   and the T-slices it carries are already copied there verbatim.

## Risks

Twenty-two findings stay open at this close and every one is Low or Medium
with an owner, which is why the verdict is PASS_WITH_RISKS. Three were raised
by this closure itself — the self-use generator writing a retired word into a
tracked file, the run that returned nothing without saying why, and the two
producers that disagree about one sorted field — and all three belong to the
next findings-paydown feature, not to F283.
