## F313 — Contract 1.22 for the Orb

### What changed
- **The version and the words (T001).** `PUBLIC_API_VERSION` and `CLIENT_INTERFACE_VERSION` read
  `1.22`. `docs/system/api-release-matrix-v1.json` reads `current` `1.22` with one `1.22` entry
  that names every addition of F310, F311 and F312 (the two routes, the interface's `insight`
  words, each provider's `class` and `budgets.profiles`, the decision route's `resumed` and
  `resume_refused`, the digest's `blockers`) and their value changes (`extend` without an answer,
  the run that starts by itself, the one question of a budget stop, the profile limits, the working
  wall clock, a cancelled job's remainder question, an order with no file name). The two routes
  moved from `1.21` to `1.22`, and five `insight.*` categories joined the inventory the matrix test
  reads from the code.
- **R-1390.** Every decision of the digest, of `remedy client changes` and of the public API's
  digest carries `blockers`: a budget stop's open blocking criteria, an empty list for any other
  decision. Before, a machine client saw the one question of a budget stop without what was left.
- **The documents (T002).** `docs/system/public-http-api-v1.md` gained "Budget stops", "What runs
  now, and why a job hangs", "Budget profiles (since 1.22)" and "Recorded answers";
  `docs/system/machine-client-contract-v1.md` describes `extend` without an answer, drops the
  remainder decision a budget stop no longer raises, and gained "Watching what runs". Both
  generated sections are regenerated.
- **The recorded answers (T003).** `scripts/record_client_answers.py` seeds a scratch data root
  with two running Pi jobs, serves a stub of the local model server, runs the real client commands
  with no model and none of the machine's data or configuration, and writes five answers to
  `docs/system/client-answers-v1/`; `--check` records them again and compares, and
  `tests/orchestration/test_record_client_answers.py` runs it. The universe's kit copies the
  folder.

### Why
The universe's kit client is written only from the contract Remedy ships over its API, so the
routes and words of F310, F311 and F312 reach the Orb only through this release.

### Key decisions
DECISIONs F313 D1 to D3 in `.agent/decisions.md`. D1: the change lines of 1.22 and where each is
written; `resumed` and `resume_refused` stay out of the command's answer keys because only the HTTP
route adds them; its addendum adds the digest's `blockers` (R-1390). D2: the recorded answers live
in this repository and the kit copies them; its addendum adds the stub of the local model server,
the five cases and the keys compared by type. D3: no ledger rotation in this closure (R-1376,
owned by F307).

### How to review and test
Read `docs/roadmap/features/T12_F313.md` (Built State) and the round entries in
`.agent/live_review.md`. Every file of rounds 1 to 3 was prepared by the reviewer in a disposable
worktree and applied byte for byte, and every production change was mutation-proven there. The
closure's one full suite: `python3 -m pytest -n auto -q` → `22100 passed, 11 skipped` on
`64249f32b` (`.agent/authored/f313-closure-suite.txt`), 0.4 percent less CPU time than F311's.
`python3 scripts/record_client_answers.py --check` compares the recorded answers with a fresh
recording.

### Evidence
- Evidence job `f313r5e1001` (9547 passed, 0 failed); package
  `remedy-review-20261021-053728-READY_FOR_REVIEW.zip`, SHA-256
  `31eee0bfb465651bc3c04ca6c383fd230ba7c1d8ace53fcff3250a7d2fad4848`, in
  `~/Repos/remedy-history/zips`; accepted head `da2e6ebe8e2d53f6f36f13527b259481fdf16029`.
- Self-use item SU-068, narrowing an excused error handler of `remedy test discover`, ran
  to its approval gate through `claude-cli`, passed review and was never applied.

### Verdict and findings
Live review PASS_WITH_RISKS: the integrity check fails only on twelve High findings F313 does not
own (DECISION F310 D7). Resolved inside the feature: R-1390. Open: 87 findings by the ledger's
reader; F313 owns none.

### Runtime actuals
One session, six delegated rounds; reviewer Claude Opus 5.5, workers Claude Sonnet; tokens and cost
of the session: not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
