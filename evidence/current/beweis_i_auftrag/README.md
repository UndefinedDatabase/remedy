# The proof of the operator order beweis (U752): the (i) order through Remedy, three tries

Run on 2026-10-29 on the operator's machine against the live supervisor (`remedy-serve-live`,
interface 1.34), with real provider calls of the Claude Code CLI. The order was sent through
Universe's own code path: the edition Universe's order body (`universe_operator.improve.remedy`:
`order_text`, `constraints_of`, the size „Normal“ 400,000 tokens, 60 calls, 120 minutes) and the
kit's `RemedyClient.submit_order` as the client `orb-universe`, with planner, builder and reviewer
`claude-cli` and `unattended: true`. No token is stored here. The order's text: „Das (i) in
Gedächtnis bekommt denselben Namen und dasselbe Verhalten wie jedes andere (i) der App.“, project
universe-chat. The operator allowed at most three tries; each stop's cause was fixed in Remedy
before the next.

| Try | Order, job | How it ended | Cause | Fixed as |
|---|---|---|---|---|
| 1 (`try1.jsonl`) | `dcec082d2d7ce552`, `6c4564622e87457e` | blocked after 8 minutes, `no_file_changed` | task 2 changed the call site task 3 named; task 3 had nothing left | F332 (PR #401) |
| 2 (`try2.jsonl`) | `7373acec386af86a`, `de04ce7d2bed47b0` | blocked after 5 minutes, review high | the change was built; the test task stopped on a test already red on the job's base commit | F333 (PR #402) |
| 3 (`try3.jsonl`, `try3-job-3f80bd014da944e2/`) | `63047a4d5990625c`, `3f80bd014da944e2` | blocked after 5 minutes, `no_file_changed` | task 1 did the whole change; the merged task 2 had nothing left and F332 missed a lone path and the merge; the builder gave up testing after one refused `echo` | F334 (PR #403) |

None of the three reached „wartet auf Übernahme“. Every try asked the operator nothing. Every stop
came after real work: the (i) change itself was built in each try (task 1's commit in the job's
worktree). The three causes are fixed and tested on main, but no fourth try was made, because the
order allowed three. The next real order (a report or a night run) is the next proof.

`try3-job-3f80bd014da944e2/` is `remedy job evidence 3f80bd014da944e2`, exported into this folder,
so the evidence index points here and `scripts/make_review_zip.sh --job-id 3f80bd014da944e2`
selects it.
