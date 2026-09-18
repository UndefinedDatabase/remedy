
## DECISION F269 D9 (2026-09-18, reviewer, round 8) — the remainder proposal: when it is raised, what it carries, and what a one-word "yes" does
CONTEXT: T2_F269.md T005 rules "at budget end with blocking criteria open, a decision in the F031
inbox carrying the open criteria as a prefilled follow-up order; the operator answers with one
word", and its Acceptance wants a fixture with one unfulfillable criterion to end blocked with a
remainder decision naming that criterion; F031's inbox contract is this feature's Do-not-touch.
Measured at `5fac20d6`: a decision is an escalation record raised by
`escalation.enqueue_task_decision` on a job's task, and its type in the inbox is always
`task_decision`, so a new record changes no pinned type set; `escalate_repeated_refusal` and the
watchdog attach theirs to the mission's latest linked job's first task and dedupe by a marker at
the start of the question; answering is `remedy decision resolve <job> <id> --reason <answer>` or
the cockpit's `_dispatch_decision_resolve`, both calling `answer_task_decision`, which records and
never acts, while the CLI's `plan:` branch already creates a mission under `--as-mission`; the
cockpit door's imports are the closed set `TestCommandDoorImportGuard.ALLOWED_IMPORTS` pins, which
a ruled DECISION may widen in its own commit; `run_mission` ends at its budget with the terminal
`iteration_limit`, and a `do` job stopped by its budget ends `stopped` with `stop_source` budget;
no mission records a link to another.
CHOSEN: (1) THE DECISION. One function in `mission_contract.py` raises it: when the mission's
contract has blockers (D4 (5)) and no OPEN remainder decision exists on the mission's jobs, it
enqueues one on the latest linked job's first task — the question starting with the marker
`[contract remainder]` and naming the mission and every blocker by id and text, options `yes` and
`no`, no safe default (a human answers), and `impact` = the prefilled follow-up order: `Meet the
acceptance criteria mission <id> left unmet: <text>; <text>.` It returns the decision id, or None
when there are no blockers, an open one exists, or the mission has no job with a task. (2) WHEN.
`run_mission`, on reaching `iteration_limit` with blockers, raises it and names its id in the
result's detail; `remedy do`, when a job it ran ended stopped by its budget with blockers, raises
it and names it, with its answer command, in the Next lines. "Ends blocked" in the Acceptance is
that state: the run stopped at its budget, the achieve move is held by the contract, and the
remainder decision is open naming each blocker. (3) THE ANSWER. Both answer doors, after a
successful answer of a `td:` record, call one function in `mission_contract.py` that acts only on a
remainder decision answered exactly `yes`: it creates the follow-up mission — goal and order = the
prefilled order; contract = the blockers copied in order, renumbered from `C001`, with their text,
blocking, origin and check, whole-mission, `open`, no evidence — and returns its id, which the CLI
prints with `remedy mission plan <id>` as the next step and the cockpit returns in its command
result. Any other answer records only. The cockpit door's `ALLOWED_IMPORTS` gains exactly that
function, under this DECISION.
ALTERNATIVES: a new decision type, rejected because the inbox pins its type sets and F031 is not
this feature's to change; creating the follow-up when the decision is raised, rejected because the
operator's answer is the order to start it; acting only in the CLI, rejected because a cockpit
"yes" would then be recorded and silently do nothing. REVERSE: delete the two functions, their
calls in the loop, `do` and both doors, the widened import, their tests, and this paragraph.
