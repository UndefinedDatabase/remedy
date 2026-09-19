
## DECISION F273 D19 (2026-09-19, reviewer, round 19) — the open ids F273 did not list are measured, the moot ones are booked, the dead residue goes, and DECISION F260 D3 gains the sentences four findings asked of it
CONTEXT: amend0911-feedback rule A gives every open finding one owner. F273's third session measured every
open id outside F273's own list at `f445a2c0` and again at `17c7f169`: a group is moot or already met,
a group waits only on DECISION F260 D3, which F275 round 23 wrote on 2026-09-10 and DECISION F275 D20
amended, and a group is live dead code or a small defect.
CHOSEN: (1) The moot and met ids are booked in this round's first commit, each with its evidence: R-0830,
R-0846, R-0849, R-0854, R-0857, R-0868, R-0869, R-0883, and R-0840, R-0842, R-0844, R-0845, R-0848, R-0853
and R-0865, whose FIX binds only D3 and which D3 names. (2) Dead residue goes, with its tests:
the three route-policy flags `apps/cli/grouped.py` still wired (R-0831); the readers of
`context_budget_optimized`, which nothing emits, so `KNOWN_DEAD_EVENT_COUPLINGS` empties and
`_COUPLING_CEILING` falls to 0 (R-0832); `_job_with_repo` (R-0850); the test-only functions of
`proposed_tasks.py` and the three helpers only they called (R-0941);
`packages/orchestration/provider_patch_material.py`, which no module imports, with the self-dogfood
roadmap rule that tested for its file (R-0867); the two `REVIEW_FINDINGS_OPEN` members nothing sets
(R-0863); and `AcceptanceCheck` with the `Verifier` protocol nothing implements (R-0884), because a task's
acceptance criteria are text, by this ruling. (3) Small repairs: a job `_stop_job` moves to `stopped` gets
its `finished_at` (R-0828), while a stop whose run manifest failed to write keeps the state it had and
records the error, as `tests/cli/test_job_rerun_manifest.py` pins against a false clean stop; the
self-use defect reporter also answers a stop that never finalized, a run-manifest error and a task that
did not pass with a blank error (R-0826); and the smoke script's messages name the keyword arguments
rather than retired flags (R-0937). (4) Amending DECISION F260 D3, as D20 did: Remedy deliberately ships
without an automated execution-approval policy, and every execution is approved by a person (R-0851);
Remedy deliberately accepts no candidate produced outside it (R-0852); Remedy deliberately runs no
external builder until a later feature provides one, and the deleted `execution` surface took the
fourteen `ContractAction` members EXECUTION_TEMPLATE_SHOW, EXECUTION_TEMPLATE_CREATE,
EXECUTION_TEMPLATE_ENABLE, EXECUTION_TEMPLATE_DISABLE, EXECUTION_TEMPLATE_UPDATE, EXECUTION_APPROVE,
EXECUTION_RUN, EXECUTION_SHOW, EXECUTION_DEBUG_BUNDLE, EXECUTION_APPROVAL_SHOW,
EXECUTION_APPROVAL_VALIDATE, EXECUTION_APPROVAL_LIST, EXECUTION_OPERATOR_RUNBOOK and
EXECUTION_CLAUDE_DOCTOR, removed at `795e4080` (R-0856); and the deleted `builder` surface took the six
members BUILDER_ADAPTER_SHOW, BUILDER_ADAPTER_ENABLE, BUILDER_PACKAGE_CREATE, BUILDER_SESSION_CREATE,
BUILDER_SESSION_SHOW and BUILDER_SESSION_INTAKE, removed at `3384dd53` (R-0860). The inheritors D3 names
are closed features, so no feature inherits any of these today. `docs/system/core-product-spine-v0.md`
stops listing the deleted groups as commands. (5) Carried to the next paydown, not ruled here: R-0819
and R-0820, whose counter-measures wait for the checklist consolidation pass; R-0866, which DECISION
F275 D12 (a) keeps open until a feature reopens the external-candidate route; R-0880, which D75 and D78
of F275 keep open; R-0829, because this feature's own closure runs the packer it would change; R-0984,
which the closure pull request's hosted CI decides.
ALTERNATIVES: resolving the D3 group by a second D3, rejected because D3 exists; giving the dead
functions callers, rejected because nothing needs them.
REVERSE: restore the touched files from `17c7f169`, and delete this paragraph.
