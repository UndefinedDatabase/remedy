
DECISION F277 D5 (2026-09-20, round 5) — THE QUARANTINE BECOMES THE RETIRED SET, AND ITS
FLOOR IS NOT ZERO.

CONTEXT. T001 declared `READ_ONLY_EVENT_NAMES` a QUARANTINE that "may only ever shrink" and
ruled every entry disposed of by giving it a writer or deleting its readers, "never by leaving
the dimension permanently absent". DECISION F277 D4 then disposed of four of the six names on
exactly that reading, and it was the right reading for all four. It is the wrong reading for
the two that remain, and the reason is on the record rather than in the code.

WHAT THE RECORD SAYS, read by the reviewer at `fa448bef`. `patch_intent_reverted` lost its
writer to DECISION F271 D3, which deleted `packages/orchestration/patch_revert.py` under
finding `R-0982` and ruled in as many words: "The four readers of `patch_intent_reverted` stay,
each reading run logs already on disk." `stop_reason_recorded` lost its scan to DECISION F031
D2 and D9, and `ui_server.py` carries that reading today in a comment above
`_count_open_decisions`. Neither name is an accident. Each is a name whose WRITER a dated
decision removed and whose READERS the same decision kept on purpose, so that run logs written
before the removal still render.

CHOSEN. `READ_ONLY_EVENT_NAMES` is renamed `RETIRED_EVENT_NAMES` and its contract is restated:
names nothing writes any more and live code still reads, on purpose, each entry citing the
decision that retired its writer and naming a module that still reads it. Both halves are
asserted from the source by
`tests/orchestration/test_event_names.py::TestEveryRetiredNameCitesTheDecisionThatRetiredIt`,
because the two ratchet tests cannot tell a retirement from a dead reader hiding in the set —
they only fire when a name gains a writer or loses its last reader, and a genuine accident does
neither. The citation is what makes the difference legible, and a guard is what keeps it
honest. `docs/roadmap/features/T2_F277.md` is amended in the same round, per
docs/agents/planner_reviewer_prompt.md §4 item 7: T001's design sentence and its Acceptance
line now read `read ⊆ declared` and `written ⊆ declared` over
`EVENT_NAMES | RETIRED_EVENT_NAMES`, and a second Acceptance line carries the citation guard.
The old rule stands unchanged for an ACCIDENT and simply does not reach a RETIREMENT.

ALTERNATIVES. Mint writers so the set empties — rejected: re-creating a writer a decision
deleted resurrects the mechanism that decision replaced, which AGENTS.md's "Replacing is
deleting" forbids outright, and it would make `remedy` emit events for the sole purpose of
satisfying a declaration. Delete the readers so the set empties — rejected: three modules
render revert history and three render stop reasons out of run logs already on disk, five test
files pin the second group, and deleting them would break exactly the rendering F271 D3 and
F031 D9 preserved. Leave the set named `READ_ONLY_EVENT_NAMES` and only widen its comment —
rejected under AGENTS.md's one-spelling-per-concept rule: the set no longer means
"quarantined, pending disposal", and a name that lies about its contents is what this feature
exists to remove.

THE TWO SETS TOGETHER ARE NOW STABLE, which is the property T001 was really after: every name
the code writes is in `EVENT_NAMES`, every name the code reads is in one of the two, no name is
in both, every retired name has a reader and no writer, and every retired entry cites its
ruling. The collector proves the first four from the source in every run; the citation guard
proves the fifth.

REVERSE: delete this paragraph, rename the set back and restore the two Acceptance lines from
git history at `fa448bef`. Reversing it does not restore the quarantine's emptiability — it
only stops the file saying why the two survivors are there.
