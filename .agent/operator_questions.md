# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q25 — One hosted test run, please (2026-10-24, F314, round 6)

**What needs deciding.** Two of the open problems of this clean-up concern the copy of Remedy's
tests that runs on GitHub's machines rather than on yours. I repaired what I could reproduce here:
one test failed there only because GitHub's machine has no name and e-mail address for git, and
another took too long because it searched a large Python installation that only GitHub's machines
carry. To prove both repairs, and to close the problem that the whole GitHub test run was red, the
test run on GitHub has to be started once on this branch. Your permission settings do not let this
session start it, so it has not run.

**Why it matters.** Until one such run is green, the two problems stay open and move to the next
clean-up. Nothing else waits on it.

**My recommendation.** Start the GitHub test run once for this branch, from the Actions page of the
repository or with the GitHub command line, or allow sessions to start it. The next clean-up then
reads the result and closes both problems when it is green.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise: the two problems are carried to the next clean-up, which asks again.

### Q26 — Let sessions run the claude command (2026-10-24, F152, round 2)

**What needs deciding.** The current work makes sure that a worker run by Remedy never picks up your own personal settings for the Claude command line, such as your instructions file, your extra tool servers or your plugins. To prove this properly, Remedy has to run the real command line twice: once with a planted marker in a fake personal settings folder, and once isolated, and show that the marker only appears the first time. The permission settings of these sessions refuse every run of the command line, even just asking it for its version or its help text, and they also refuse reading the public documentation on the web. So the research is written from a saved copy of the help text, and some points stay marked as unverified.

**Why it matters.** Without one real run, Remedy can prove that it hides your settings from the worker, but not that the command line itself honours the switches it is given. One real run costs one very small paid call.

**My recommendation.** Allow sessions to run the claude command for version and help, allow one small paid call for the proof, and allow reading the public Claude documentation. Until then, the proof runs against a stand-in program and the real run sits behind a switch that is off by default.

**What happens if you say nothing.** The recommendation is already executed and stands until you say otherwise: everything is built and tested with the stand-in, the real run stays switched off, and the work closes with that one point named as an open risk for a later clean-up.

### Q27 — Let sessions read the Codex tool (2026-10-24, F158, round 1)

**What needs deciding.** The next planned piece of work was to teach Remedy to use OpenAI's Codex command-line tool as a second kind of worker, beside the Claude tool it uses today. That work must begin with research on the exact tool installed on your machine: its version, the switches it accepts, the shape of what it prints, and a few recorded example runs. The plan forbids guessing any of this. The tool is installed, but the permission settings of these sessions refuse every way of finding out about it: running it even just to ask for its version or its help text, reading its installed files, and searching or reading the web. So the research cannot be done, and nothing about that tool can be built honestly.

**Why it matters.** The Codex worker is the template that the later Gemini worker and other vendors copy, so it waits until the research is possible. The work on cost comparison, the clean-up of open problems and several other features do not depend on it and go ahead.

**My recommendation.** Allow these sessions to run the Codex tool for its version and its help texts, to read its installed files, and to make a handful of very small paid example runs so that real recorded output can be saved as test material. Reading the public Codex documentation on the web would help too. Alternatively, run those few commands once yourself and save their output in the repository, and a session will work from that copy.

**What happens if you say nothing.** The recommendation is already executed and stands until you say otherwise: the Codex worker has been moved behind the next clean-up of open problems, the work on comparing costs across vendors is being done now instead, and when its turn comes again a session that still cannot read the tool moves it back once more and asks again, rather than building it from guesses.

### Q28 — Park the rest of the list too? (2026-10-24, amend1024-one-real-order, Part F2)

**What needs deciding.** Your order asked to park 55 open features until F317 has worked three times in a row on Luna: the second-worker adapters, the post-mortem miner, the idea engine and every open feature of Tiers 4, 6 and 7. Twenty-two of them are parked now. The other thirty-three stay in the active list, because a feature that stays there names them in its own "Depends on" line, and your order said to write such a case down instead of improvising. The whole of Tier 4 stays because F250 depends on F117 to F128; F073, F063, F064 and F066 stay because F230 and F250 depend on them; F129, F131, F134, F135, F138, F139 and F140 of Tier 7 and F087, F089, F090, F094, F096 and F098 of Tier 6 stay because F164, F187, F192 to F196, F224 to F232 and F244 depend on them, directly or through each other.

**Why it matters.** Until this is decided, the active list still holds those thirty-three features after F316, so a later session could start one of them before F317 has proved itself three times.

**My recommendation.** Park the dependents too: F164, F187, F192, F193, F194, F195, F196, F224, F225, F226, F227, F228, F229, F230, F231, F232, F244 and F250, and with them the thirty-three. None of them serves the one goal of a real order landing, and parking them keeps every dependency whole.

**What happens if you say nothing.** Nothing more moves. The thirty-three stay active behind F316, the twenty-two stay parked, and no dependency is torn.
