# Live Review — F254 Model alias table & dead-model doctor check

Branch: feature/f254-model-alias-table
Feature file: docs/roadmap/features/T2_F254.md
Tier 2 · registered by amendment round amend0805-v3 (2026-08-05, the
F232 core pulled forward) · depends on nothing · blocks F232 (model
upgrade playbook) and F110 (routing).

Goal & Done, quoted from the feature file: every hardcoded default
model id moves behind ONE alias table in a single module, and
`remedy doctor` gains a check that every configured/default model id is
not on a known-dead list. DONE when doctor flags a dead id in a fixture
and no hardcoded dated model string remains outside the alias module.

This feature is also the S4 rehearsal of the self-drive protocol
(docs/agents/self_drive_protocol.md): the first feature built end to
end inside ONE session, with the planner/reviewer in the main session
and a delegated worker subagent per round (DECISION D6 of the S1+S2
build). The rehearsal is under test as much as the feature is — a gap
the protocol cannot resolve is a finding against the protocol, never a
licence to improvise.

## Steps
- R1 (SPLIT): Open PR Gate — merge PR #185, the S1+S2 self-drive skill
  — then cut the branch, claim the STATUS line, and reset the three
  .agent state files to this feature — PASS.
- R2 (SPLIT): persist the R1 verdict, register R-0211, record DECISION
  D10; then the alias module packages/orchestration/model_aliases.py
  with the five built-in default model ids relocated behind it and its
  own unit test — PASS.
- R3 (SPLIT): persist the R2 verdict, register R-0212, record DECISION
  D11, amend the feature file's Acceptance, and route the last three
  built-in ids — the two Ollama providers and the `ollama.model`
  config default — through the alias table — PASS.
- R4 (current, SPLIT): persist the R3 verdict and register R-0213;
  then the known-dead model list — a shipped data file, a loader
  module that merges it with an operator config extension, and its
  unit tests. No `remedy doctor` wiring in this round: the doctor's
  JSON contract is a separate risk and gets its own round.
- R5: wire the check into `remedy doctor core`, whose output names the
  offending id, where it came from (config vs built-in default) and
  the alias to update.
- R6: the repo-scan test that no built-in model id survives outside
  the alias module, plus the docs/ update this feature owes.
- R7: the integration gate (docs/agents/integration_gate.md).
- R8: closure per docs/roadmap/STATUS_closure_protocol.md — evidence
  job and a fresh review zip are mandatory.

## Findings
- R-0211 (reviewer authoring, Low): F254 was claimed ahead of F103,
  which Rule A5 names as the first unchecked STATUS line, on the
  strength of a previous session's plan note rather than a recorded
  DECISION. docs/agents/planner_reviewer_prompt.md §4 item 7 requires
  a re-plan to be loud, persisted and reversible — chosen option,
  alternatives considered, how to reverse — and the authored
  .agent/context.md stated the ordering as a fact with none of that.
  The worker flagged the gap in its handback instead of proceeding
  silently, which is exactly the behaviour the rule exists to produce.
  It is NOT a block condition: nothing was fabricated and the ordering
  itself is sound. Fix: record it as DECISION D10 below, in the same
  commit that registers this finding.
  Done: R-0211 — D10 recorded.
- R-0212 (reviewer authoring, Low): the R2 step block's "Done when"
  ordered an `rg` over three model strings — including the UNDATED
  `qwen3-coder-next` — and required hits only in model_aliases.py,
  while the same block's Change list forbade touching the four files
  that hold the remaining occurrences. The criterion was unsatisfiable
  inside its own scope. The worker did the right thing and the record
  should say so: it declared the criterion unmet, printed the real
  `rg` output, refused to widen scope, and refused to adjust anything
  to make the check look green. Not a block condition — nothing was
  fabricated and no false completion was claimed. Fix: R3 routes the
  three remaining built-in ids, and the scan test is authored in R5
  against the amended Acceptance rather than against an ad-hoc
  command.
  Done: R-0212 — routed in R3, Acceptance amended in the same round.
- R-0213 (reviewer authoring, Low): the R3 receipt f254-r3-2 rewrote
  .agent/plan.md's Next Steps but its FROM block stopped one bullet
  short, leaving the old "Then the integration gate, then closure per
  …STATUS_closure_protocol.md" line orphaned below the new R6/R7
  bullets that already say the same thing. The worker reported the
  duplication and refused to delete text no authored FROM covered,
  which is exactly right — improvising a deletion is how authored
  state silently drifts. Third finding in a row raised against the
  reviewer's own authoring rather than the worker's execution; the
  pattern is worth naming, and the countermeasure is to extend a
  Next-Steps FROM to the end of its list rather than to the last line
  being changed. Fix: an authored receipt in R4 removes the orphan.
  Done: R-0213 — removed by receipt f254-r4-2.
- Next free ID: R-0214.

## Decisions
- D10 (work-item order): F254 runs before F103. Chosen because F254 is
  the designated S4 rehearsal of the self-drive protocol
  (docs/agents/self_drive_protocol.md), and the operator's SSH-only
  constraint carries a hard date of 2026-08-12 — the rehearsal has to
  finish first. F254 is small, dependency-free and touches production
  code under packages/ and apps/, which is precisely what a rehearsal
  must exercise: the SPLIT round type that forbids self-certified
  production code. Alternatives considered: claiming F103 (Token
  ledger, SQLite) first per Rule A5, which would rehearse the protocol
  on a far larger feature with four days left; or rehearsing on a
  docs-only item, which never exercises SPLIT at all and would prove
  nothing about the round type the operator actually depends on. How
  to reverse: any later relay flips the F254 line in
  docs/roadmap/STATUS.md back to `[ ]` and claims F103 instead —
  nothing else on this branch depends on the ordering. F103 remains
  the next roadmap feature after F254.
- D11 (spec tension, routed to planning per
  docs/agents/planner_reviewer_prompt.md §4 item 7): T2_F254's Goal
  says "every hardcoded default model id moves behind ONE alias
  table", while its Acceptance says "no hardcoded dated model string
  remains outside the alias module". They disagree about the undated
  built-in default `qwen3-coder-next`, which R2 left in
  packages/providers/ollama_builder/provider.py,
  packages/providers/ollama_planner/provider.py and the `ollama.model`
  ConfigKeySpec in packages/orchestration/config.py. Chosen: the GOAL
  is binding — those three are built-in defaults and get routed
  through the alias table in R3, and the feature file's Acceptance is
  amended in the same round to say so, so the spec and the build stop
  disagreeing. Alternatives considered: follow the Acceptance
  literally and leave three copies of the default model of the
  provider Remedy actually ships as its default, which preserves
  exactly the rot this feature exists to stop; or amend the feature
  file to drop the Goal sentence, which weakens a spec to match a
  half-done implementation. How to reverse: revert the three routing
  hunks and the one-line Acceptance amendment — the alias table is
  valid under either reading, so nothing else depends on the choice.
  Out of scope under either reading and deliberately untouched:
  illustrative ids inside comments and the sample-TOML prose in
  packages/orchestration/config.py, and the docstring mention in
  packages/orchestration/role_config.py — none of those is a default,
  they are documentation of one.
- The S1+S2 build's decisions D5 through D9 are the same numbering
  series, continued here rather than restarted, and stay in that
  branch's history, now on main.

## Verdicts
- R1: PASS (2026-08-07). Range fc023265..5fed2fca, two commits. Open
  PR Gate: `gh pr list` returned exactly the predicted single entry;
  `gh pr merge 185 --merge --delete-branch` produced merge commit
  fc023265; and because that command printed no explicit confirmation
  line, the worker verified independently with `gh pr view 185`, which
  reports state MERGED, mergedAt 2026-08-07T14:26:32Z. Refusing to
  read silence as success is the right instinct and is recorded here
  as such. `gh pr list --state open` is now empty. The branch is
  feature/f254-model-alias-table, cut from main at the merge commit;
  main was never committed to. Transport, PRIMARY proof: all four
  receipts cmp 0 against the reviewer's scratchpad originals — no
  digest fallback — and the three full-file applications cmp 0 against
  .agent/live_review.md, .agent/plan.md and .agent/context.md. The
  STATUS pair is REWRITE-shaped: FROM 0x, TO 1x, the hunk is exactly
  +1/-1 on line 66, and `grep -c` over the whole ledger finds exactly
  one `[~]` line. Scope is the nine instructed paths and nothing else:
  no file under packages/, apps/, scripts/, tests/ or .claude/
  changed, and ROADMAP.md was not touched. Reviewer re-runs at
  5fed2fca: tests/docs/ 294 · dashboard contract 70 · test_test_runner
  51 · resource safety 21 · golden path 42 — every count equal to the
  worker's report, all exit 0. Primary checkout clean, `git worktree
  list` shows the primary only, no force-push. One finding, R-0211,
  raised against the reviewer's own authoring rather than the worker's
  execution. Tier: docs-round gate + canary; no full-suite claim is
  made. LAST_REVIEWED_SHA = 5fed2fca.
- R2: PASS (2026-08-07). Range 5fed2fca..807e3df7, three commits.
  Ordering respected and verified against the diff, not the report:
  4254503b carries ONLY the two receipts, .agent/live_review.md and
  .agent/plan.md, so the finding and the decision were on disk before
  a line of code moved. Transport, PRIMARY proof: both receipts cmp 0
  against the reviewer's scratchpad originals — no digest fallback —
  and all six pairs applied REWRITE-clean. The relocation is faithful:
  `rg` over packages/, apps/ and scripts/ finds
  `claude-opus-4-20250514` and `claude-sonnet-4-20250514` ONLY in
  packages/orchestration/model_aliases.py. ClaudeProvider's evaluated
  default is unchanged because the module-level constant is resolved
  at import time and used as the signature default — the worker chose
  that shape over `model: str = ""`, which would have changed
  behaviour in a round that promised none. role_config's table is the
  same five provider→id pairs it always was. The alias module imports
  nothing from packages.orchestration, so no import cycle is
  possible, and it documents its three deliberate absences (no config
  read, no provider probe, no id modernisation) where a reader would
  search for them. Reviewer re-runs at 807e3df7: test_model_aliases
  18 · test_role_config 32 · test_pingpong 33 · test_provider_mode 24
  · test_token_truth 37 · test_final_verifier 97 · test_do_job_flow
  178 · dashboard contract 70 · test_test_runner 51 · resource safety
  21 · golden path 42 — every count equal to the worker's report, all
  exit 0. Independent spot-check of the reviewer's own choosing, on
  five reader files the round did NOT gate: test_pingpong_integration
  10 · test_job_task_runner 191 · test_task_plan_evidence 10 ·
  test_execution_config_evidence 17 · test_worker_facade_cmd 49 — all
  green, so the relocation broke nothing outside the gated set. No
  existing test was edited. Primary checkout clean, `git worktree
  list` shows the primary only, no force-push, no PR. One finding,
  R-0212, raised against the reviewer's own step block rather than
  the worker's execution. Tier: round gate + canary; no full-suite
  claim is made. LAST_REVIEWED_SHA = 807e3df7.
- R3: PASS (2026-08-07). Range 807e3df7..513451b4, four commits.
  Ordering verified against the diff: 1816f0a0 carries only receipts
  and .agent state, d8294663 only the feature file, and code appears
  first in 9a45a99a — the finding and the decision were on disk before
  the spec was amended, and the spec before the code. Transport,
  PRIMARY proof: all three receipts cmp 0 against the reviewer's
  scratchpad originals, no digest fallback. Both append-shaped pairs
  were reported under their own shape with no 0x claimed (R-0207
  honoured in practice, not just in the rule). The relocation is now
  complete and was checked by the reviewer's own `rg`, not the
  report's: every surviving `qwen3-coder-next` occurrence is
  documentation prose — the two provider docstring precedence lists,
  the role_config.py docstring, and three commented sample-TOML lines
  — plus the alias table entry itself; the two dated Claude ids appear
  only in model_aliases.py. That is exactly the boundary DECISION D11
  drew, so the amended Acceptance and the built state agree. No import
  cycle: `import packages.orchestration.config` in a fresh interpreter
  exits 0, which matters because config.py now resolves an alias at
  module import. Reviewer re-runs at 513451b4: test_model_aliases 21 ·
  test_config 62 · test_role_config 32 · test_provider_mode 24 ·
  tests/docs/ 294 · dashboard contract 70 · test_test_runner 51 ·
  resource safety 21 · golden path 42 — all exit 0, every count equal
  to the worker's report. Independent spot-check of the reviewer's own
  choosing on files the round did not gate: test_config_cmd 14 ·
  test_budget_guard 52 · test_ollama_builder 18 · test_ollama_provider
  19 · test_ollama_patch_reliability 18 — all green. The two Ollama
  counts confirm the worker's numbers exactly; the reviewer's first
  attempt looked for those files under tests/orchestration/ and found
  nothing, which was the reviewer's path error and not a discrepancy
  in the handback. Two declared items, both accepted: the test module
  docstring was updated to name the sources it now covers, which keeps
  an in-scope file honest rather than drifting scope; and the handoff
  ran to 119 lines because this block ordered two verbatim `rg`
  transcripts and 21 test results into it — accepted under the same
  reasoning as the S1+S2 R2 handoff, cause named, no section dropped,
  and the fix belongs to the reviewer's authoring, not the worker's.
  One finding, R-0213. Primary checkout clean, no worktree, no
  force-push, no PR. Tier: docs-round gate + canary; no full-suite
  claim is made. LAST_REVIEWED_SHA = 513451b4.
- R4: PENDING — awaiting the worker handback.
