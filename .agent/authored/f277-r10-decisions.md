
DECISION F277 D9 (2026-09-20, round 10) — A CATCH-ALL EXCEPTION GETS A CATCH-ALL TOKEN,
NAMED FOR THE LAYER THAT REFUSED AND NOT FOR THE CONDITION IT WILL NOT NAME.

CONTEXT. DECISION F277 D8 rules that an error token is named for the CONDITION, so that the
same condition reads the same in every group. `mission_cmd.py` is the first module where that
rule meets a wall. Four of its twelve refusal sites are `except MissionError as exc:` with the
message `str(exc)`, and `MissionError` is the mission layer's single base: it is raised for a
mission already achieved, a mission with no plan, a status transition the record forbids, a
goal too short, and roughly a dozen other conditions, each distinguished only by the prose it
carries. There is no condition to name, because the code that raises it did not keep one.

CHOSEN. The token is `mission_error`, at all four sites. It is named for the layer that
refused, and it is honest about exactly what it tells a consumer: the mission layer rejected
this call, and the sentence is in `message`. A consumer that branches on `mission_error` learns
which SUBSYSTEM failed, which is real information and is more than the bare `Error:` line it
replaces, and it learns no more than the product currently knows. The alternative to naming it
is inventing a condition the raise site never recorded — a token derived by matching on the
message text would be a parser over prose, which is the defect this whole slice exists to end,
and it would go stale the first time a sentence was reworded.

THE RULE THIS SETS for the rest of T003 and for T004's sweep: where a module's refusals come
from a SINGLE exception whose instances are distinguished only by prose, the token is
`<layer>_error` and the layer is the module's own subsystem — `mission_error` here. Where the
raise sites are distinguishable — a not-found, a usage error, a state conflict — they keep
their own tokens, and this round does that too: `mission_not_found`,
`mission_plan_in_progress`, `invalid_status`, `invalid_argument`, `no_project`,
`invalid_list_option`. A `<layer>_error` token is therefore a statement that the layer below
does not classify its own failures, and it is the right place to look when someone later wants
it to.

ALTERNATIVES. Give each `except MissionError` site a token named for its call site — rejected:
`mission_show_error` and `mission_plan_error` name the COMMAND and not the condition, so two
commands hitting the same underlying refusal would report two tokens, which is the drift D8
forbids in the other direction. Classify by matching the message text — rejected above: a
parser over prose. Widen `MissionError` into a hierarchy first — the right long-term answer
and explicitly out of scope: it is a refactor of `packages/orchestration/mission_state.py`
inside a slice whose change set is CLI call sites, and `fail()` can adopt the finer tokens
later without any call site moving, because the token is an argument and not a shape.

ALSO IN THIS ROUND, AND IT IS WHY `contract_cmd.py` IS TOUCHED AGAIN. `_resolve_project_id`
and `_load_mission_or_exit` live in `mission_cmd.py` and are imported by `contract_cmd.py`,
which round 9 migrated. Threading `json_output` into the two helpers changes nothing for the
contract group unless the flag is threaded at the two call sites THERE as well. The reviewer's
first mutation set did not cover those two lines and both stayed GREEN under mutation, which
is what a red proof is for: the round would have shipped two threaded arguments no test
watches. Two tests were added in `tests/cli/test_contract_cmd.py` before emission and both
mutations now redden.

REVERSE: delete this paragraph and rename the four `mission_error` tokens. Reversing the rule
means the next module with a single-base exception layer either invents conditions or leaves
its refusals untokenised.
