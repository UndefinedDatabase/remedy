
DECISION F277 D10 (2026-09-21, round 12) — F277 REACHED THE SEVEN-SESSION SOFT LIMIT AND
CLOSES AT THE SCOPE IT HAS BUILT; THE REST BECOMES F283.

CONTEXT. Operator amendment amend0827-process-diet rule 6 sets the soft limit at 25 rounds
OR 7 sessions per feature, whichever is reached first, and
`docs/agents/planner_reviewer_prompt.md` §2 renders the second half as "at 7/7 the row is
followed by the scope report, not by another step". The handoff chain on this branch is
continuous and monotone — session 1 at round 1, session 2 at rounds 2 to 6, session 3 at
round 7, session 4 at round 8, session 5 at round 9, session 6 at rounds 10 and 11 — so the
session reading this handback is F277's SEVENTH and the limit is reached at round 11 of 25.
The round budget is not what ran out; the session budget is, because five of the six
sessions before this one delivered one or two rounds each.

Operator amendment amend0905-throughput makes the standing default at the soft limit
SPLIT-AND-CLOSE, executed by the session on its own authority, and reserves the old hard
stop with an operator question for the case where no self-consistent close is possible.

CHOSEN. Split and close. F277 closes on T001 and T002 complete and T003 in part, and its
remaining scope is registered as F283 — Machine contracts, part two: the refusal sweep, the
JSON gap and the exit-code taxonomy — placed directly after F277's own STATUS line inside
the same Tier 2 heading, per amend0906-split-placement, so Rule A5 proposes it next.

WHY THE CLOSE IS SELF-CONSISTENT, which is the only question the default leaves open.
Nothing F277 ships is half-built. T001 is a complete contract: `event_names.py` declares the
vocabulary, the AST test asserts read and written both subset of declared, every
`RETIRED_EVENT_NAMES` entry cites its ruling and names a living reader, and the four
accidents DECISION F277 D5 found are disposed of. T002 is a complete contract:
`json_envelope.py` carries one shape with `emit_ok`, `emit_error` and `fail`, and the error
boundary in `grouped.py` means no traceback reaches an operator. T003 is a MIGRATION onto
the helper T002 landed — nine of twenty-eight modules done — and a migration is the one
kind of slice that is coherent at any prefix, because every unmigrated site still behaves
exactly as it did before F277 opened. T004 is a sweep that measures T003's completion and
is meaningless before it. So the seam between F277 and F283 falls between two finished
declarations and their unfinished application, which is where a seam belongs.

WHAT MOVES. F277's T003 minus the nine applied modules, and F277's T004 whole, become
F283's T001 and T002, copied from F277's file rather than re-planned, with DECISIONs F277
D7, D8 and D9 travelling with them. Three of F277's seven Acceptance bullets move with
them and are struck from F277's list in the same commit that registers F283. Finding R-1014
moves to F283 for whatever half of its fix clause F277's own closure consolidation does not
land.

ALTERNATIVES CONSIDERED. (a) Row on and finish T003 and T004 in this session: forbidden in
as many words — "on reaching it the next obligation is NOT more work" — and dishonest about
the cost, since nineteen modules and a documented taxonomy is not one session's work at the
one-to-two rounds per session this feature has been managing. (b) The hard stop with an
operator question: reserved by amend0905-throughput for a scope that cannot close
self-consistently, and this one can, so taking it would spend a session waiting for a
ruling the default already supplies — which is the exact failure amend0905-throughput cites
F262's round 23 for. (c) Close F277 and carry the remainder with no feature file, as a
finding: that is the attic AGENTS.md's Scope Control forbids, and nineteen unmigrated
modules is not a defect to be paid down, it is planned work.

CONSEQUENCE. F277's STATUS line names the slices that moved, in the shape F261's and F280's
lines already use. F283 is registered THIN in the ledger-atomic sense — feature file,
STATUS line, `TOTAL_FEATURES` pin and README counters in ONE commit — and is filled at
claim, not now. The operator may reverse this by deleting F283's four registration edits and
re-opening F277's STATUS line; the work itself is untouched either way, because nothing in
this decision changes a line of product code.

REVERSE by deleting this paragraph, deleting `docs/roadmap/features/T2_F283.md`, removing
F283's STATUS line, restoring `TOTAL_FEATURES` to 282 with its comment, restoring the README
counters, restoring F277's three struck Acceptance bullets from git history at `67b0972d`,
and flipping F277's STATUS line back to `[~]`.
