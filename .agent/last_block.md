Round paydown0731-r1 — operator directive 2026-07-31 (micro-round at
the F052→F053 boundary, single-session, standing approval for
same-session merge on PASS). Items: (1) codify the digest fallback
for transport proofs in planner_reviewer_prompt.md §4; (2) add the
practice-requires-pointer rule to §2; (3) fix R-0159 — the dogfood
branch guard must accept both `.git` forms (directory and linked
worktree gitfile pointer), additive and default-preserving, with a
minimal worktree-form test — then drop the non-restorable
`.git`-directory class from integration_gate.md. Candidate pass:
resolve the carried VerificationTests run_id pitfall in
STATUS_closure_protocol.md per the closure-candidate rule. Gates:
tests/docs + canary + the test files touched by Item 3. Expected
ledger effect: R-0159 RESOLVED; candidate resolved inline as a
DECISION; next free ID stays R-0160. Authored texts
paydown0731-r1-{1..8} (sha256 in .agent/authored/, cmp-verified
against the reviewer scratchpad originals at apply time).
OUTCOME: pending
