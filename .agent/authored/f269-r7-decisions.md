
## DECISION F269 D8 (2026-09-18, reviewer, round 7) — an amendment's shape, its round of effect, its recompile and its acknowledgement
CONTEXT: T2_F269.md T004 rules that every later operator message is an amendment "recorded on the
mission, DoD recompiled, acknowledged with what was understood and from which round it applies",
that F264 builds the channel and this feature owns the data shape and the recompile, and its
Acceptance wants an amendment sent between rounds to change the DoD of the next round and be
acknowledged in the run log with the round it applies from. DECISION F269 D2 stored
`amendments[]` entries verbatim and left their fields to T004. Measured at `c4bd55c1`: a mission's
rounds are the orchestrator loop's iterations, numbered per mission by
`orchestrator_loop.next_iteration_index`, and its run log is the append-only
`ledger.jsonl` that `append_ledger_entry` writes and `render_ledger` prints; each dispatched job's
DoD takes its contract slice at dispatch (D4 (3), D6 (1)).
CHOSEN: (1) SHAPE. An amendment entry is `{"id", "text", "received_at", "applies_from",
"criteria", "understood", "acknowledged_in"}`: `id` is `A` plus three digits, unique; `text` is
the operator's message, non-empty; `received_at` is an ISO timestamp; `applies_from` is the round
it takes effect from, an integer of at least 1; `criteria` lists the ids of the criteria it added,
each present in the contract with origin `amendment`; `understood` is the sentence that says what
was understood; `acknowledged_in` is null until acknowledged, then the round it was acknowledged
in, never before `applies_from`. D2's validation now applies these rules on read and on write.
(2) AMEND. One function in `mission_contract.py` amends a mission's contract from a message: it
creates the contract when the mission has none; adds one criterion — the message as its text,
origin `amendment`, whole-mission unless milestones are given, blocking unless told otherwise —
compiled by D4 (1)'s compiler; and appends the entry with `applies_from` = the mission's next
round, `understood` = "adds blocking criterion <id>: <text>" (or "advisory"). It never edits an
existing criterion or entry. No command is added: F264 owns the route. (3) THE NEXT ROUND. Because
a job's DoD takes its slice at dispatch, every job dispatched from `applies_from` on carries the
amendment's check and every job dispatched before it does not. (4) ACKNOWLEDGEMENT. At the start of
each loop round, before its move, every amendment whose `applies_from` is at most that round and
whose `acknowledged_in` is null gets one ledger entry in that round — move kind
`acknowledge_amendment` with the amendment id, outcome status `acknowledged` and detail
`<understood>; applies from round <n>` — and its `acknowledged_in` set to that round. (5) The
contract renderers list the amendments after the criteria, each with its round of effect, its
acknowledgement and the criteria it added.
ALTERNATIVES: acknowledging at the moment the message is received, rejected because the run log
is the loop's and nothing runs between rounds to write it; changing an existing criterion's text,
rejected because the record is the audit and an amendment adds, so a replaced wording is a new
criterion; a command to send amendments, rejected because F264 owns the channel. REVERSE: delete
the amend function, the acknowledgement in the loop, the entry rules and their tests, and this
paragraph.
