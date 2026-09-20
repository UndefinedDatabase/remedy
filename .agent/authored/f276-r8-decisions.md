
## DECISION F276 D9 (2026-09-20, reviewer, round 8) — the closure suite's three red nodes are a cold checkout, not this feature's defect, and the repair is one re-run against a warm `dist`

CONTEXT: operator amendment amend0917-throughput rule 1 gives a feature ONE full suite run,
in the closure sequence's integration-gate round. F276 spent it at round 7's C4 and the
transcript, committed at `a5193724`, is RED: `3 failed, 17636 passed, 20 skipped` at exit 1,
with a complete bad set of three node ids, all in `tests/ui_server/`, all failing at
`tests/ui_server/server_start.py` with `Server thread exited before publishing its info file`
under a captured `ERROR: React UI not built.`. Rule 2 makes every bad node the feature's to
fix unless main's hosted CI shows it red there, and caps repair at three rounds before an
`xfail(strict=True)` and a follow-up feature.

THE MEASUREMENT, taken by the reviewer with targeted tests and never the full suite, which is
what rule 1 permits a reviewer dry run to use. `apps/ui/dist` is gitignored and absent from a
cold checkout; the UI server's start path auto-builds it. Its `index.html` and its `assets/`
were written at 09:32:22 on 2026-09-20, while C3 was committed at 09:18:21 and the suite ran
after that — so the dist was built DURING the run, by the auto-build, while the `-n auto`
workers that had already reached a UI test were failing to reach a server. Re-run alone
against the now-present dist, in the primary checkout, those same three node ids read
`3 passed in 85.32s` at exit 0.

CHOSEN. (1) The three are attributed to the CHECKOUT's posture, not to F276 and not to a
defect in the tests. Nothing in this feature's change set reaches `tests/ui_server/`,
`apps/ui/` or the server start path, and the same three nodes pass unchanged once the artifact
they need exists. (2) The repair under rule 2 is ONE re-run of the full suite, in the primary
checkout, with `apps/ui/dist` already built before the run starts, and its transcript replaces
`.agent/authored/f276-closure-suite.txt` — one canonical file, as closure precondition 2 reads
it by name. That transcript states the PREVIOUS bad set of three explicitly beside its own, so
the shrinking rule is checkable on the file rather than across two files. (3) Nothing is
marked `xfail`, nothing is skipped, no assertion is weakened and no test is deleted. Rule 2
reserves the mark for what is still red after the third repair round, and a node that passes
on a re-run is not that. (4) If the re-run's bad set is NOT empty, the round records it and
stops; the next repair round is authored from that reading, and F276 still has two of its
three repair rounds left.

CONSEQUENCE: the integration-gate transcript this closure reads is green and was produced by a
run whose environment was made correct FIRST, rather than by a run whose result was
reinterpreted afterwards. The cost is one extra full-suite run beyond rule 1's single run; that
is precisely what rule 2 spends a repair round on, and it is spent once.

A STANDING NOTE, not a rule: the auto-build racing `-n auto` makes the FIRST full-suite run in
any cold checkout of this repository unreliable for `tests/ui_server/`, independently of what
the branch changed. Building `apps/ui` before the integration-gate run is the cheap
counter-measure, and the reason it is a note rather than a rule is that changing the
integration-gate procedure belongs to the operator, not to a feature's closure. It is carried
into `.agent/prose_slips.md` as a dated line so the next closure reads it.

ALTERNATIVES: marking the three `xfail(strict=True)` and registering a "Suite repair after
F276" follow-up under rule 2, rejected because rule 2 orders the mark only for what survives
three repair rounds and these survive none — it would register a feature for work already done
by an `npm run build`; closing PASS_WITH_RISKS on the red transcript, rejected for the same
reason and because precondition 2 would then be met by a transcript nobody believes; re-reading
the red run as green because the reviewer's targeted run passed, rejected outright — a
transcript is the artifact precondition 2 names, and a reviewer's own reading is not a
substitute for it.

REVERSE: this decision changes no code. To reverse it, restore
`.agent/authored/f276-closure-suite.txt` from `a5193724` and delete this paragraph.
