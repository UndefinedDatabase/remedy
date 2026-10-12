## F058 — Model failover chain

**What.** Each role may carry a failover chain in `remedy.toml` under `model_failover.chains`: a
list of links, each naming exactly `provider`, `model` and `tier`.
`packages/orchestration/model_failover.py` parses the chains and checks every link against the
three hard rules of `docs/agents/model_routing_policy.md` and a fourth, `core_role_on_local_provider`
(a local link only for roles routed to the cheap tier); a refused table gives one warning naming
every violation and no failover. When a role's provider is unavailable after the transport retries,
`FailoverProvider`, wrapped around the role's provider by
`packages/orchestration/role_provider_factory.py`, walks the chain. Every call the walk reached
carries a `failover` key in the run record with the intended and the used provider and model and
the reason `failover:provider_unavailable`, and `remedy run show` prints one `Failover:` line. A
timeout, a rate limit and an unreadable answer never fail over. After a backup has served, the
backups are tried first for `model_failover.cooldown_s` (default 300) and the usual provider again
after it; a backup is never offered a session another model opened. Page:
`docs/system/model-failover-v1.md`.

**Why.** An unattended mission must survive a provider that is down without hiding a timeout or a
rate limit behind a more expensive model, and must say plainly when a different model served.

**Key decisions.** DECISIONS F058 D1 to D5 in `.agent/decisions.md`: a link declares its tier,
because Remedy maps no model name to a tier, and the routing keys moved to
`packages/orchestration/config_keys_model_routing.py` first (D1); the walk wraps the provider where
a run builds it, after a structural step moved that construction out of `pingpong_loop.py` (D2); the
disclosure sits beside each call's session in the run record (D3); the cooldown runs on an injected
clock and is not kept between runs (D4); after pull request 331 merged into `main`, the branch took
`main` in one merge commit and repaired the two guards that merge had turned red on `main` (D5):
the structure ratchet, by moving the `ui` keys to `packages/orchestration/config_keys_ui.py` and the
UI server's launch helpers to `packages/orchestration/ui_server_launch.py` without changing what they
do, and the vocabulary guard, by rewording the help of `ui.start --host`.

**How to review.** `docs/roadmap/features/T3_F058.md` (its amendment and Built State), then the
round entries `Gate: F058 R1` to `R9` and the `Done:` paragraphs of R-1257 to R-1265 in
`.agent/live_review.md` and its archive; `tests/orchestration/test_model_failover.py` drives a down
primary, an exhausted chain, the three non-triggers and the cooldown through `run_pingpong`.

**Changed files.** Ten rounds over four sessions; each round's prepared files are in its
`.agent/authored/f058-r<N>.md`, and the review package's manifest lists every path.

**Verdict.** Rounds 1 to 9 booked in the ledger, round 1 FAIL and repaired, round 7 stopped by an
outside switch of the checkout and superseded by the merge, the rest PASS; round 10's verdict is
the reviewer's and is booked in the next feature's first commit. Live review PASS_WITH_RISKS: four
Low findings carried, all owned by F306.

**Open findings.** 4 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the merged tree at `895152727` after `vite
  build`: `22826 passed, 22 skipped, 1 warning in 399.98s`, exit 0
  (`.agent/authored/f058-closure-suite.txt`).
- The evidence job `f058r9e1001`, `python3 .agent/authored/f058-r9-create_f058_evidence.py`, on the
  accepted head `78a10d8eedb04e65af0ea44f6f0d20408dbee673`: 4751 passed, 4 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261013-011933-READY_FOR_REVIEW.zip`, SHA-256
  `39a31421f1a8d8cf0fbd28b3d2036b9010e729ef5fd65142a688425fbbbc2621`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 10 delegated rounds over four sessions; wall clock and model tokens not
measured for the rounds themselves; the closure's self-use run, item `SU-059`, ran to its approval
gate in round 6 and was never applied.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
