# Context — paydown0814 closure debt

## Active Branch
feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the F045
closure PR #197 merged at this session's Open PR Gate. No STATUS line is
claimed: this is a paydown branch, not a roadmap feature. The next roadmap
feature is F057, Rate-limit-aware scheduler, and it starts in a new session.

## Scope
In: `docs/agents/reviewer_conventions.md`, trimmed under the 800-token
prompt-segment cap with headroom (R-0359); a new pin in
`tests/docs/test_docs_consistency.py` deriving the README tier table's Done
column from the ledger (R-0360); `.agent/**` state, including emptying
`.agent/candidates.md` now that both carried candidates are registered.

Out: every RULE the conventions document states — the trim compresses prose,
duplication and retold precedents, never a rule; `CONVENTIONS_TOKEN_CAP`
itself, which is production code and a P4 principle; `docs/roadmap/STATUS.md`
and `README.md`, which no paydown branch touches; F057 and all feature work.

## Constraints
- No production code: this branch touches docs/, tests/ and .agent/ only, so
  no packages/ or apps/ file is in scope.
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate, and never a PR this session created (G1);
  never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. Destructive and red-proof checks run only
  inside a disposable git worktree, so resource safety stays intact and no
  background pytest process is ever left running.
- A round pushes after EVERY commit, not once at its last step (R-0289).

## Steps
R1 state reset and candidate registration → R2 the two fixes, each gated, the
new pin red-proved → handoff and PR. The PR stays unmerged this session.
