# F319 — build orders with Claude Code end green (operator amendment amend1027-green-builds, Part F)

Run on 2026-10-27 against the live supervisor (`remedy-serve-live`, port 8450, data root
`~/Repos/remedy/.data`) with the code of `main` at `014ff71de`, real Claude Code CLI calls and the
clients' own tokens. Collected by `.agent/authored/amend1027-f-orders.py`; no token is stored here.
The jobs' raw streams stay under the data root; `GET /api/v1/jobs/{job}/evidence` answers them.
Nothing was applied: the operator applies in the app.

## F1 — universe-chat, client orb-universe: `f1-universe-chat-run1/`

Order `2318f04b3a65e952`, header `max-total-tokens: 400000`, `max-provider-calls: 60`,
`max-wall-clock-minutes: 120`, text „Das (i) in Gedächtnis bekommt denselben Namen und dasselbe
Verhalten wie jedes andere (i) der App."

| Acceptance | Evidence |
|---|---|
| One job | `summary.json`: shape `one job`, job `967b13a7bbb44b9c`; `scope` `single_job: true` |
| Ended green, awaiting the apply | `order_poll.json`: state `ended`, phase `awaiting_apply`, exit 0; the story's state `done` |
| The builder ran the tests | `967b13a7bbb44b9c/evidence/builder_test_runs.json`: `npx vitest run tests/unit/memory-info-605.test.tsx` 2 passed, then the whole suite |
| The final check ran them and passed | `967b13a7bbb44b9c/evidence/dod_result.json`: `npm test` blocking, `passed`, reason `preexisting_failures` |
| Who tested | the story's `verification.tested_by`: `builder`, `final_check` |
| Used | 46,593 tokens in 15 calls, 10.0 minutes (`order_budget_used`) |

The final check passed with the reason `preexisting_failures`: universe-chat's own `main` failed the
same three Vitest tests (`motion-588.test.ts` twice, `text-golden.test.ts`) before the job, from
Universe merges of that afternoon. Every other test of the 2,099 passed (DECISION amend1027 D1).

## F2 — remedy-edition, client orb-remedy: `f2-remedy-edition-run5/` (the accepted run)

Order `67f912f1e5b9ab21` ended `awaiting_apply`, one job `98c1f2692d004e3e`, the final check (the
edition's 24 tests under the brain's Python, in the sandbox) passed, 1,311 tokens in 2 calls. The
change creates `CHANGELOG.md` with Unreleased and a three-sentence amend1024 entry.

The runs before it, kept as the record of why the order text grew (DECISION amend1027 D2):

- `run1` (`5a42873746467117`, the operator's words alone): blocked honestly; the edition has no
  `CHANGELOG.md` and the builder would not invent one.
- `run2` (`62f50ba6831ca68d`): stopped before planning; „leg sie … an" was not read as asking for a
  new file. Repaired in `do_lane._CREATES` (PR 395).
- `run3` (`f97733cb176ec835`): blocked; the builder could not read what amend1024 was.
- `run4` (`f72f138b0f2a9e76`): the facts named a file, and the job delivered that file; declined.

## Also

- `a3_probe.json`: a real builder call with `--permission-mode dontAsk` ran `python3 -m pytest -q`
  (1 passed) and was refused `curl --version` without being asked.
- `interface_version.json`: the server answers `interface_version` 1.31.
