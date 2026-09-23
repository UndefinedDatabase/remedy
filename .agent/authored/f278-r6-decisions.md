
DECISION F278 D5 (2026-09-23, round 6) — THE FIRST MARKING ROUND: HOW A REASON IS WRITTEN AND
CHECKED, AND THE ONE HANDLER THAT CHANGES BEHAVIOUR.

CONTEXT. DECISION F278 D4 orders the remaining blind handlers read and either narrowed or marked.
This round takes the three files with the most: `job_evidence.py` 29, `run_manifest.py` 23 and
`scripts/build_review_manifest.py` 27, measured at `4353fb9e` with `ruff check --select BLE001`.

CHOSEN. (1) A research agent read every one of the 79 handlers, without writing to the tree, and
proposed a reason per site with one sentence of evidence. It proposed no narrowing; for the
subprocess probes, the closest candidates, it reported that they run with `text=True`, whose
decoding failure is a `ValueError` the obvious narrowing would miss. The
reviewer read the proposals, checked the handlers whose reasons could hide a defect against the
code, and changed three: two lines that carried `# pragma: no cover` keep it after the noqa, and
one reason that quoted a round label is reworded. (2) A marking commit changes COMMENTS only.
`marking_check.py`, shipped with this round, proves it per commit: every changed line keeps its
code text up to the comment, gains `# noqa: BLE001 — ` and a reason, and the commit removes as
many lines as it adds; the fail-closed commit below is its negative control. (3) ONE HANDLER
CHANGES BEHAVIOUR. `run_manifest._contains_secret` asks the stream redactor whether a value
carries a secret, and on ANY exception answered False, so a detector that could not run cleared
the value it was asked about. Every caller refuses or flags a value when it answers True, so it
now answers True: a detector that failed cannot clear anything. A test pins it, and its red proof
restores the old answer.

ALTERNATIVES. Register the fail-open answer as a finding for the paydown feature — rejected: the
repair is one line inside a handler this round must read and mark anyway, and marking it with a
reason that describes a fail-open would put the defect into the record as a justification.
Narrow the subprocess probes to `(OSError, subprocess.TimeoutExpired)` — rejected for the
decoding case above.

REVERSE by deleting this paragraph and restoring `_contains_secret`'s `return False` from git
history at `4353fb9e`.
