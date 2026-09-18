
## DECISION F269 D7 (2026-09-18, reviewer, round 6) — the contract binds a job to its repository and grants it, and `job attach-repo` and `job permit` are deleted
CONTEXT: DECISIONs amend0917-throughput D2 and F280 D4 keep `remedy job attach-repo` and `remedy job
permit` until F269's contract writes a job's repository binding and grants. Measured at `c93d117d`:
`test run` requires `metadata["target_repo"]` and the grant `repo_test_run`; `test discover` and
`self execute` require `target_repo`; `patch apply` requires `target_repo` and `repo_generated_write`;
`patch revert` requires `target_repo` and `repo_revert`; grants live in `metadata["permissions"]`
and are written by `permissions.set_permission`; no job-creation path writes `target_repo`, and no
production code outside the two handlers writes `repo_test_run` or `repo_revert`; a `do` job
carries `repo_path`, a job made by `continue_mission` carries neither; the orchestrator's dispatch
and `do`'s shape step both call `mission_contract.merge_contract_slice_into_dod` for every job of a
mission.
CHOSEN, FIRST — THE WRITER. `mission_contract.py` gains one function, called beside
`merge_contract_slice_into_dod` at both sites, that does nothing for a mission with no contract,
and otherwise writes on the job record: `metadata["target_repo"]` := the job's `repo_path` when it
has one, else the project's `canonical_repo_path` when it has one, else nothing; and the grants
`repo_test_run`, `repo_generated_write` and `repo_revert` allowed. Those three are exactly what the
five surviving commands check, and a contract is the operator's accepted order for that
repository. It never denies a grant and never overwrites a `target_repo` already set.
CHOSEN, SECOND — THE DELETION. `job.attach-repo` and `job.permit` go: their catalog entries,
handlers and dispatch entries; `TestRequiredCommands.REQUIRED` loses them and
`TestDeletedCommands.DELETED` gains them; tests that asserted the commands themselves are deleted;
tests that used them to set up a job write the binding and grants directly on the job record
instead; every production, script and `docs/system` or `docs/guides` string that tells a reader to
run either command names the heir instead: a job gets its repository and grants from its mission's
contract, shown by `remedy job contract <id>`, and tests asserting that guidance follow it.
THE HEIR: the contract writer above, for every job of a mission that has a contract, which is every
mission `plan_mission` planned and every `remedy do` walk. WHAT IS LOST: a job of a mission with no
contract — a mission never planned — has no command left that binds or grants it; the five commands
refuse such a job with their existing reasons. No stub, alias or compatibility reader is left.
ALTERNATIVES: a `grants` field on the contract compiled per template, rejected because nothing today
reads a grant other than the five commands and they all need the same three; keeping `job permit`
for denials, rejected because the grants default to denied and nothing but these commands ever
reads them. REVERSE: revert the round's writer and deletion commits and delete this paragraph.
