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
- R4 (SPLIT): persist the R3 verdict, register R-0213, then the
  known-dead model list — shipped data file, loader, config extension
  and unit tests — PASS.
- R5 (SPLIT): persist the R4 verdict, register R-0214, record D12 and
  D13, file the handoff-cap closure candidate, and wire the dead-model
  check into `remedy doctor core` as an advisory warning — PASS. The
  feature's first acceptance criterion is met against the real shipped
  list, not a fixture.
- R6 (SPLIT): persist the R5 verdict, register R-0215, fix the doctor
  warning's text-mode verbosity and its miscounted detail line, add
  the repo-scan test that closes the second acceptance criterion, and
  write the docs, registered in the docs/README.md index — PASS. Both
  of the feature file's acceptance criteria are now met and pinned.
- R7 (SPLIT): persist the R6 verdict, register and fix R-0216, then
  the integration gate — PASS. Zero branch-only failures; the
  reviewer's own independent full-suite run at the same HEAD was
  16016 passed, 19 skipped, 0 failed.
- R8 (SPLIT): persist the R7 verdict and register R-0217 — PASS. The
  S4 rehearsal session reached its capacity limit here, with the
  feature built, both acceptance criteria pinned and the integration
  gate green, but NOT closed. A second session resumes at R9.
- R9 (current, SPLIT): closure PREPARATION — persist the R8 verdict,
  record DECISION D14, write the feature file's Built State section,
  and re-produce the integration-gate evidence INTO the repo, which
  is what R-0217c owes. Deliberately NOT in this round: the evidence
  job, the review zip, the STATUS edit and the PR — a closure that
  packages its own preparation cannot be reviewed before it lands.
- R10: closure per docs/roadmap/STATUS_closure_protocol.md — evidence
  job and a fresh review zip are mandatory, a zip failure is a closure
  blocker, the STATUS `[x]` line lands in the SAME commit as the
  README capability sync (R-0154), that commit is LAST on the branch,
  and the PR that follows is NOT merged in the session that creates
  it.

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
- R-0214 (rule vs practice, Low): AGENTS.md caps .agent/handoff.md at
  60 lines, or 100 when a per-commit table of more than five commits
  needs it, with sections never dropped. Three handbacks running have
  exceeded it — S1+S2 R2, F254 R3 at 119 lines, F254 R4 at 122 — and
  each time the reviewer accepted the overage ad hoc because the cause
  was content the round's own step block mandated: transport proofs,
  pair counts under two shapes, a generated changed-files table, an
  item-status table and a verification table. R4 exceeded it even
  after the block explicitly forbade verbatim transcripts, which rules
  out worker verbosity as the cause. A rule that is correctly
  overridden every time it binds is not a rule, and accepting it in
  session memory three times over is the A1 trap
  (docs/agents/planner_reviewer_prompt.md §0) this project keeps
  falling into. NOT a block condition: no section was dropped and
  every overage was declared with its cause. Fix: the amendment
  belongs to AGENTS.md, which is out of this feature's scope —
  AGENTS.md Core Workflow forbids mixing an unrelated fix into a
  feature branch — so it is filed in .agent/candidates.md under the
  disk-vehicle rule (docs/roadmap/STATUS_closure_protocol.md) and
  becomes a block condition at the next feature claim until resolved.
  Done: R-0214 — filed as a closure candidate in R5.
- R-0215 (doctor output, Low): two defects in what the new warning
  prints, both found by the reviewer running `remedy doctor core`
  rather than by reading the diff. (a) In text mode each warning is a
  single ~700-character line, because the entry's whole recorded
  reason is embedded; two warnings turn the readable check list into a
  wall. Worse, the detail ends "…choosing the successor is F232's job
  (the model upgrade playbook). No replacement id is recorded." — the
  recorded reason already said that, so the appended sentence is
  redundant in exactly the case that fires today. (b) The
  `dead_model_list` check detail reads "N shipped + M configured dead
  ids", but M is computed as `len(dead_ids) - len(shipped_entries)`,
  which is the number of configured ids NOT already shipped, not the
  number configured. An operator who adds an id Remedy already ships
  sees it counted as zero. Neither is a block condition: nothing is
  fabricated, the honesty clause about operator-maintained data is
  present and correct, and `ready` is unaffected. Fix: text mode
  prints one compact line per warning — id, origin, the alias or key
  to change, and the provenance clause, which stays in BOTH modes
  because it is the honesty requirement — while the full recorded
  reason stays in `--json`; the redundant trailing sentence is dropped
  when the reason already covers it; and the count is labelled for
  what it counts.
  Done: R-0215 — both fixed in R6.
- R-0216 (reviewer authoring, Low): receipt f254-r6-1 PAIR 1 rewrote
  the R5 step bullet and added an R6 bullet, but its FROM stopped
  before the pre-existing "- R6: the repo-scan test…" line, so the
  Steps list carried two R6 entries. Identical in shape to R-0213 and
  with the same countermeasure, which was written down after R-0213
  and then not applied: a FROM that edits a LIST extends to the end of
  that list, not to the last line whose wording is changing. Fourth
  reviewer-authoring finding of this feature and the second of exactly
  this kind, so the pattern is now the finding: authored list edits in
  this project need the whole list in the FROM, every time. The worker
  again reported the duplicate and refused to delete text no authored
  FROM covered, which is correct and is why the defect surfaced at all
  rather than being quietly normalised. Not a block condition — a
  duplicated planning bullet misleads no verification. Fix: receipt
  f254-r7-1 PAIR 1 takes the whole tail of the list.
  Done: R-0216 — the duplicate is gone.
- R-0217 (reviewer authoring, Low): three defects in the R7 step
  block, all in what the reviewer ordered rather than in what the
  worker did. (a) Its "Done when" required
  `grep -c '^- R6' .agent/live_review.md` to be 1, which is
  unsatisfiable while an R6 VERDICT line exists — verdict lines share
  the `- R6:` prefix with step lines. The worker reported the
  mismatch instead of deleting a verdict line to satisfy a check, and
  the substantive test — exactly one R6 bullet inside `## Steps` —
  passes. (b) The authored plan.md text pushed the file to 54 lines,
  past the AGENTS.md sub-50 cap that the reviewer enforces on
  everyone else. (c) The block's Change list forbade any sixth path,
  which blocked integration_gate.md §2's own instruction to copy the
  gate logs into a `.agent/gate_*` directory; the logs therefore live
  only in the session scratchpad and die with the session. Not a
  block condition: the gate's real numbers are recorded in the R7
  verdict from two independent runs, and the closure protocol
  requires a full-suite confirmation anyway, so the evidence is
  reproducible rather than lost. Fix: (a) and (b) in this round's
  receipts; (c) is carried into the closure round, which must produce
  the gate evidence into the repo before flipping the STATUS line.
  Done: R-0217a and R-0217b — fixed here. R-0217c — carried to R9,
  named in the handoff as a closure precondition.
- Next free ID: R-0218.

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
- D12 (where the handoff-cap fix goes): the R-0214 amendment is filed
  as a closure candidate rather than applied on this branch. Chosen
  because AGENTS.md is not F254's subject and the Core Workflow rule
  "never mix unrelated features or fixes in the same branch" binds the
  reviewer's authoring exactly as it binds the worker's editing; the
  candidates file is the vehicle this project already built for a
  finding that outlives its feature, and a non-empty candidates file
  is itself a block condition at the next feature claim, so the fix
  cannot be forgotten. Alternatives considered: amending AGENTS.md
  here, which mixes a process fix into a model-alias feature and
  makes the F254 PR harder to review honestly; or carrying it as an
  open finding, which dies with the branch — the exact F056 loss the
  disk vehicle exists to prevent. How to reverse: delete the entry
  from .agent/candidates.md; the finding text stays in this file
  either way.
- D13 (dead-model check severity): the doctor's dead-model finding is
  a WARNING, not a blocker, and `ready` keeps its current meaning.
  Chosen because Remedy's own shipped defaults are on the dead list
  today, so a blocker would make `remedy doctor core` report NOT READY
  on a freshly cloned repo until F232 lands — which teaches operators
  that NOT READY is normal and destroys the signal the command exists
  to carry. A stale-but-working default does not stop Remedy running,
  and that is precisely what a readiness check answers. Failing to
  READ the shipped list is different and stays a hard check: "no dead
  models" and "I could not open the file" must never look alike
  (packages/orchestration/dead_model_list.py says the same in code).
  Alternatives considered: making it a blocker, which is louder but
  false about readiness; or shipping an empty dead list so nothing
  fires, which makes the check decorative and leaves the actual rot
  unflagged. How to reverse: move the warning into the `checks` list
  and it becomes a blocker again — one call site.
- D14 (closure gate evidence, reviewer): R9's gate evidence is a
  BRANCH-ONLY re-run at the final content head, with its raw log,
  FAILED list, exit code and wall time committed to
  `.agent/gate_f254_r9/`. No second base run at the merge base is
  ordered. Chosen because R7 already performed the dedicated
  integration-gate round the closure protocol requires — branch run,
  base run in a disposable worktree, and a third independent
  reviewer run — and found ZERO branch-only failures; R-0217c is a
  finding about the LOGS not reaching the repo, not about the
  measurement being absent or doubted. The closure protocol's
  precondition 2 asks this round to RE-CONFIRM a gate that already
  PASSed, which a branch run at the head being packaged does.
  Alternatives considered: repeating the full branch+base comparison,
  which costs a second worktree, the apps/ui/node_modules and dist
  parity restoration and roughly five more minutes to reproduce a
  comparison whose answer is already recorded and was already
  independently re-run; or committing the R7 numbers as prose, which
  is exactly the "green as a word" that G4 calls a finding. How to
  reverse: order a base run in the repair round and drop
  `base_run.txt`, `base_failed.txt` and the `comm` outputs into the
  same `.agent/gate_f254_r9/` directory — nothing about this round's
  layout has to change to accept them.
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
- R4: PASS (2026-08-07). Range 513451b4..2504a560, three commits.
  Ordering verified against the diff: 74baaa7b carries only receipts
  and .agent state, code appears first in 5ecd0197, and that commit's
  diff is 438 lines — under the 500 limit, so no oversize declaration
  was owed. Transport, PRIMARY proof: both receipts cmp 0 against the
  reviewer's scratchpad originals, no digest fallback; all six pairs
  REWRITE-clean; and the R-0213 repair landed — the orphaned bullet is
  gone (`grep -c` 0) and .agent/plan.md is 46 lines. The data file is
  the part that most deserved distrust and it holds up: both entries
  name ids that exist in model_aliases.py, both reasons cite
  T2_F254.md's own "How it fits" for the staleness claim, and both
  `superseded_by` fields are EMPTY with the reason saying the
  successor is F232's to choose. Nothing was invented, and
  `qwen3-coder-next` is correctly absent because no source in this
  repository calls it dead. The loader refuses to degrade an
  unreadable file to an empty list, refuses a schema_version it does
  not understand, and lets config extend but never replace — the
  three properties that decide whether a check like this can be
  trusted at all, and each is documented as a deliberate absence
  where a reader would search for it. Reviewer re-runs at 2504a560:
  test_dead_model_list 23 · test_model_aliases 21 · test_config 62 ·
  test_config_cmd 14 · tests/docs/ 294 · dashboard contract 70 ·
  test_test_runner 51 · resource safety 21 · golden path 42 — all
  exit 0, every count equal to the worker's report. Independent
  spot-check of the reviewer's own choosing on registry consumers the
  round did not gate: test_command_catalog 23 · test_run_manifest_schema
  13 — green. Fresh-interpreter imports of dead_model_list and config
  both exit 0, which matters because config.py now resolves an alias
  at import and the loader imports config lazily inside a function to
  keep that direction one-way. Five items declared, all accepted: the
  self-corrected config-key placement, four public names beyond the
  ordered surface (each earns its place — one spelling per concept),
  the two loader assumptions about config unavailability and an absent
  `superseded_by`, and the handoff length, which becomes finding
  R-0214 rather than another silent acceptance. Primary checkout
  clean, no worktree, no force-push, no PR. Tier: round gate + canary;
  no full-suite claim is made. LAST_REVIEWED_SHA = 2504a560.
- R5: PASS (2026-08-07). Range 2504a560..c77dfc0d, three commits.
  Ordering verified against the diff: fd601931 carries only receipts
  and .agent state — including the candidates.md entry — and code
  appears first in 885c64f0, 289 lines. Transport, PRIMARY proof: all
  three receipts cmp 0 against the reviewer's scratchpad originals, no
  digest fallback; the candidates.md full-file application cmp 0; the
  append-shaped pair was again reported under its own shape with no 0x
  claimed. The block condition this round actually risked was a false
  live indicator, and the code does not commit it: every warning says
  Remedy calls the id dead "only because the shipped list …says so —
  that list is operator-maintained data, no provider was queried", and
  the helper that builds that sentence carries the reason for it in a
  docstring. D13 holds in the built artifact, verified by the reviewer
  running the command rather than trusting the report: `ready` is
  true, `blockers` is empty, both dead ids surface as advisory
  warnings, and the JSON gained exactly one key — `warnings` — with
  `ready`, `checks` and `blockers` unchanged in meaning. The alias
  names in the warnings are derived from MODEL_ALIASES and the config
  keys from the key registry, so neither goes stale when the tables
  change. Reading the list is a hard check and its failure is a
  blocker; what the list SAYS is advisory — the distinction the whole
  design turns on, and it is implemented where it was designed. One
  event deserves the record: `test_development_artifact_boundary`
  went red 3/18 mid-round because the new docstring cited
  .agent/live_review.md, and shipped product code may not name a
  development artifact. The worker fixed its own docstring and edited
  no assertion — the rule caught a real leak on its first exposure,
  which is what it is for. Reviewer re-runs at c77dfc0d:
  worker_facade_cmd 59 · product_spine 72 · command_catalog 23 ·
  development_artifact_boundary 18 · dead_model_list 23 ·
  model_aliases 21 · cli_ux 57 · dashboard contract 70 ·
  test_test_runner 51 · resource safety 21 · golden path 42 — all exit
  0, every count equal to the worker's report. Reviewer's own
  execution of `remedy doctor core` in both forms confirmed the
  contract independently. Four items declared, all accepted; the
  700-character text line and the miscounted detail become finding
  R-0215 rather than a silent acceptance, and the handoff's 131 lines
  are the measurement R-0214 asked for, not a new offence. Primary
  checkout clean, no worktree, no force-push, no PR. Tier: round gate
  + canary; no full-suite claim is made. LAST_REVIEWED_SHA = c77dfc0d.
- R6: PASS (2026-08-07). Range c77dfc0d..ac54592c, five commits.
  Ordering verified against the diff: 08dcdd3b carries only receipts
  and .agent state; the fix, the pin and the docs land in three
  separate commits, none mixed. Transport, PRIMARY proof: both
  receipts cmp 0 against the reviewer's scratchpad originals, no
  digest fallback; all six pairs REWRITE-clean. R-0215 is fixed and
  measured, not asserted: the reviewer ran `remedy doctor core` and
  the longest warning line is 220 and 224 characters against 839
  before, the provenance clause survives in the short form word for
  word in meaning ("per the shipped list scripts/dead_models.json —
  operator data, no provider queried"), the full recorded reason moved
  to `--json` with a printed pointer saying so, and the count now
  reads "2 shipped + 0 config-only dead ids (2 total)" — a label that
  matches what it counts. The repo scan is the part that had to be
  distrusted hardest, because a scan that never bites is worse than no
  scan. The reviewer proved it independently, in a disposable
  worktree at this HEAD, not by reading the worker's transcript:
  adding a real assignment of claude-sonnet-4-20250514 to
  role_config.py turns the test RED and the message names
  packages/orchestration/role_config.py:151 with the offending id;
  putting the SAME id in a `#` comment on the same file leaves it
  green, which is DECISION D11's boundary falling out of the `ast`
  mechanism rather than out of an allow-list. The worktree was removed
  and pruned before this verdict and the primary checkout was clean
  throughout. Zero violations at HEAD and no exclusion was added to
  reach that. The docs decision is sound and evidenced: a grep of
  docs/system, docs/guides and docs/agents for the concepts returned
  nothing, so a new doc was correct, and it is registered in both the
  quick-find and system tables of docs/README.md. One declared item
  needs naming rather than burying: implementing R-0215's
  de-duplication inverted an assertion this reviewer authored in R5,
  which now reads "not repeated after the reason". That is the R5
  test being corrected by the R6 finding, not an assertion weakened to
  fit — the `ready`/`blockers` contract of D13 is untouched, and the
  reviewer confirmed it by running the command. B3 was solved by
  relabelling rather than recomputing because the real configured
  count sits behind a private function in a module this round was
  forbidden to edit; the label is honest, so the finding is closed
  correctly, if not at its root. Reviewer re-runs at ac54592c:
  worker_facade_cmd 63 · model_aliases 24 · dead_model_list 23 ·
  product_spine 72 · cli_ux 57 · development_artifact_boundary 18 ·
  tests/docs/ 294 · dashboard contract 70 · test_test_runner 51 ·
  resource safety 21 · golden path 42 — all exit 0, every count equal
  to the worker's report. One finding, R-0216. Primary checkout
  clean, `git worktree list` shows the primary only, no force-push, no
  PR. Tier: docs-round gate + canary. No full-suite claim is made —
  that is R7's job and nothing before it may claim it.
  LAST_REVIEWED_SHA = ac54592c.
- R7: PASS (2026-08-07), and the integration gate is GREEN. Range
  ac54592c..a310cd13, two commits, both .agent-only — no source, test,
  docs or STATUS file was touched in the gate round, which is what
  keeps the gate a measurement rather than a negotiation. Transport,
  PRIMARY proof: both receipts cmp 0 against the reviewer's scratchpad
  originals; all six pairs REWRITE-clean; the R-0216 duplicate is gone
  and `## Steps` holds exactly one R6 bullet. The gate itself: the
  worker ran `python3 -m pytest -n auto -q` at 0ea95c88 → exit 1, 1
  failed / 16015 passed / 19 skipped in 128s, and at the merge-base
  fc023265 in a disposable worktree → exit 1, 5 failed / 15950 passed
  / 19 skipped in 147s. BRANCH-ONLY FAILURES: ZERO. The single shared
  failure, test_product_smoke.py::test_no_zombie_processes_after_
  every_outcome, is present at the base too and passes on a serial
  re-run — the xdist-flake class, not this branch. The four base-only
  failures were not waved away as noise: the worker measured the cause
  and showed that the full suite rebuilt apps/ui/dist mid-run (the
  primary's dist mtime falls inside the branch-run window while the
  base worktree's dist hash was unchanged), which is the R-0155/R-0158
  build-output class. That asymmetry means the two runs were not
  perfectly comparable, and the honest answer to it is a third
  measurement rather than an argument — so the reviewer ran the full
  suite independently at a310cd13: `python3 -m pytest -n auto -q` →
  16016 passed, 19 skipped, 0 FAILED, 124s. Zero failures at this
  HEAD, in the reviewer's own hands. Both runs sit well under the
  five-minute budget, so no perf pass is owed. Worktree cleanup
  verified by the reviewer, not the report: `git worktree list` shows
  the primary alone, no `tmp/*` branch survives, `git status
  --porcelain` is empty and no pytest, vite or npm process is left
  running. Three deviations were declared and all three are the
  reviewer's, becoming finding R-0217. This is the ONLY round of this
  feature permitted to claim "full suite green", and it claims it:
  16016 passed, 0 failed, at a310cd13. LAST_REVIEWED_SHA = a310cd13.
- R8: PASS (2026-08-07). Range a310cd13..d8dd8c18, two commits, both
  .agent-only — no source, test, docs or STATUS file was touched, so
  the session-closing round changed nothing it then certified.
  Transport: the prior session's scratchpad originals died with that
  session, so the DIGEST FALLBACK of planner_reviewer_prompt.md §4.9
  applies and is declared here rather than implied. What this
  reviewer proved with its own hands, disk to disk: `.agent/plan.md`
  is byte-identical to the committed receipt f254-r8-2 (`cmp` exit
  0), and all three of receipt f254-r8-1's pairs are REWRITE-shaped
  with FROM 0x and TO 1x in the applied file. The receipts' sha256
  values recompute to
  fb7cb6a83e21a368432fa16510bdda3389e657c1295c58a09422c0486e6ea85d
  and
  50c6c2fb9729aea88e629378ded93423f47757b66028a8ce9d8337283d2ab55b,
  matching what the handoff records — a weaker link than
  cmp-against-scratchpad, because the digests and the files now share
  one custodian, and it is named as weaker instead of dressed up.
  State contracts hold: plan.md is 43 lines, under the AGENTS.md
  sub-50 cap the reviewer enforces on everyone else (R-0217b fixed,
  measured not asserted), with `## Goal` and `## Next Steps` present;
  live_review.md keeps `## Steps`, `## Findings`, `## Decisions` and
  `## Verdicts` once each and exactly one `- R6` bullet inside
  `## Steps`, which is R-0217a's real test rather than the
  unsatisfiable whole-file grep the R7 block asked for. The round
  gate was RE-RUN by the reviewer, not read out of the report:
  tests/ui_server/test_dashboard_contract.py 70 ·
  tests/orchestration/test_test_runner.py 51 ·
  tests/regression/test_resource_safety.py 21 ·
  tests/cli/test_golden_path.py 42 — 184 tests, every file exit 0 and
  every count equal to the worker's. One correction the reviewer owes
  its own record: the first re-run reached for tests/test_test_runner.py
  (43 tests) instead of the orchestration file the worker meant, and
  the per-file breakdown above is the settled reading. R-0217 is
  registered with all three sub-items and its resolution is split
  honestly rather than rounded up — a and b Done in this round's
  receipts, c CARRIED with a named closure precondition. The 116-line
  handoff is over the cap, declared as R-0214's fifth measurement with
  no section dropped, and the amendment is already filed in
  .agent/candidates.md — the same override for the fifth time is not a
  new finding, it is evidence for the one already filed. Primary
  checkout clean, `git worktree list` shows the primary alone, no
  force-push, no PR, STATUS untouched at `[~]`. Tier: round gate plus
  canary — this round makes no full-suite claim and none is owed until
  the closure re-confirmation. LAST_REVIEWED_SHA = d8dd8c18.
- R9: PENDING — awaiting the worker handback.
