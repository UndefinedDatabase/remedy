# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q2 — Narrower safety check before rename (2026-09-14, F275, round 101)

What needs deciding. An earlier ruling said that before the big rename lands, the loop must measure again, across the whole test suite, how many tests exercise each line the rename changes without having confirmed that line's type, and must stop if any line has lost every test. Eleven of those lines were each exercised by exactly one test. Doing that measurement the way it was first done needs a full run of the test suite with coverage recording, and your newest rule allows exactly one full run per round, after the rename. I decided to check only the eleven named lines, each by running its one test on its own with coverage before the rename, and to stop if any of them is no longer reached. When I checked before handing the work over, all eleven were reached, and the worker checks again before the rename.

Why it matters. The narrower check cannot see a line that used to be exercised by several tests and has since lost all of them. Such a line would only show up if the rename broke it and some other test happened to notice. The full test run after the rename remains the main safety net either way.

My recommendation. Keep the narrower check. The lines most exposed were the eleven with a single test, and repeating the whole measurement would add a second full run, with coverage recording, to a round your rule limits to one.

What happens if you say nothing. The rename lands after the narrower check, and the remaining work continues under one full test run per round.
