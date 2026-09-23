
DECISION F278 D6 (2026-09-23, round 7) — A HANDLER THAT FAILS OPEN IS REPAIRED, NEVER EXCUSED,
AND THE THREE THE MARKING FOUND ARE REGISTERED AND TAKEN IN THIS ROUND AND THE NEXT.

CONTEXT. The research for the second and third marking groups read 178 handlers and flagged four
where catching everything hides a defect; the reviewer confirmed each against the code at
`ead4ec77`. One, in `pingpong_job.run_job`, drops a failed final job review in silence and the
final verifier reads the missing file as not blocked. Two, in `do_sequence`, drop a job's budgets
or fences when they fail to validate. One, in `review_subject._metadata_is_safe`, clears a value
when its scanners raise. A noqa reason on any of them would write the defect into the source as
its justification.

CHOSEN. (1) Each is registered with Owner F278 — R-1036, R-1037 and R-1038 — in this round's
booking commit, before any repair. (2) R-1036 is repaired in this round, in its own commit ahead
of the marking group that holds its file; the marking skips that line. (3) R-1037 and R-1038 sit
in the third marking group's files and are repaired in the next round, ahead of that group's
marking, which is the round that turns BLE001 on. (4) Every other handler the research read is
marked with the reason it proposed, which the reviewer read in full for this group; its two
handlers that assume a state on failure, in `job_apply`'s cleanup, were checked against the code
and fail toward the conservative answer.

ALTERNATIVES. Repair all three here — rejected: R-1037 and R-1038 live in files the next round
marks, and repairing them there keeps each file's change in one round. Register them for the
findings paydown feature — rejected: each is inside T003's own subject, a failure that must be
loud, and the feature that found them is the one reading the handlers.

REVERSE by deleting this paragraph; the R-1036 repair reverses from git history at `ead4ec77`.
