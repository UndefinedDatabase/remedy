# STEP R4/F040 — T001 PART 2: THE DIGEST ENDPOINT

Goal: serve the composition round 3 built. One line in the server's per-job
handlers dict, one builder beside its siblings, and the route tests that pin the
wiring — after which `GET /api/jobs/<job_id>/digest` answers the digest envelope
and T001 is complete.

Base: `2b063387`, the round-3 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r4.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN4
- C2  append slice RECORD4 to `.agent/live_review.md`
- C3  add `_build_digest_json` and apply pair PAIRHANDLERS to
      `packages/orchestration/ui_server.py` per the SPEC below
- C4  create `tests/ui_server/test_digest_route.py` per the SPEC below
- C5  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r4.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/ui_server.py
    tests/ui_server/test_digest_route.py
    .agent/handoff.md

`packages/orchestration/job_digest.py` is NOT edited this round — round 3 built
it and its tests pin it; the endpoint is a caller and nothing about the
composition changes to serve it. Nothing under `apps/` changes.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. If one looks wrong, apply it as
   given and DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r4-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` is APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. The red proof runs ONLY in a disposable `git worktree`; purge `__pycache__`
   and use `python3 -B`. The primary checkout is `git status --porcelain` empty
   at every reading.
8. C3 IS ONE COMMIT holding both the builder and the handlers line. They are not
   separable: a builder no dict references is dead code, and a dict line naming
   a function that does not exist is a NameError at import. Landing them apart
   would put a red commit on the branch.
9. THE ROUTE ADDS NO BEHAVIOUR OF ITS OWN. It loads events the way its siblings
   do and returns `build_job_digest(...)`. No filtering, no defaulting, no
   reshaping — a route that edited the envelope would be a second home for the
   composition round 3 made single.
10. The word `digest` already occurs seven times in `ui_server.py`, every one a
    hash digest (`hexdigest`, `compare_digest`). Any count you report is scoped
    to an exact string — the route key or the builder name — and never to the
    bare word.
11. The `remedy` console script is DENIED; use `python3 -m apps.cli.grouped ...`
    if needed and say so.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
13. Push after C5. No pull request, no merge, no force-push.
14. Pair shape, measured: PAIRHANDLERS `TO contains FROM: true` — APPEND-shaped,
    so its obligation is FROM exactly 1x plus the ONE TO-only line exactly 1x
    among the lines C3's diff ADDS, and NEVER a FROM-zero count.

## Slices

The authored units are PLAN4, RECORD4 and the two halves of PAIRHANDLERS, each
between its own BEGIN and END marker line. The markers are NOT part of the unit.

<<<BEGIN PLAN4
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, round 4.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D5 | done | rounds 2 and 3 |
| the one-source urgency and R-0751 | done | round 2, PASS |
| T001 the composition module and its tests | done | round 3, PASS |
| T001 the endpoint and its route tests | done | this round |
| T002 the hero card, triggers, the TS retirement | open | next session |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round serves the composition: one handlers line, one builder, and the
   route tests that pin the wiring. T001 is complete when it lands.
2. T002 builds the hero card against the design reference, wires the trigger,
   dismiss and last-seen mechanics, and retires the TypeScript urgency copy per
   DECISION F040 D2.
3. T003 adds `remedy job digest` and the end-to-end, then the integration gate
   and closure.

## Risks
- R-0570, R-0752 and R-0753 stay OPEN. The first two are routed to the paydown
  branch; R-0753 is a documented risk this feature carries, because the persisted
  actuals record has no money field for the digest's cost basis to read.
- Two homes for the urgency formula exist until T002, pinned equal by
  `tests/ui_contracts/test_decision_urgency_parity.py` rather than trusted.
<<<END PLAN4

<<<BEGIN RECORD4
Gate: F040 R3 — T001 PART 1, THE COMPOSITION MODULE. VERDICT PASS. Reviewed by re-running every gate against the reviewer's own scratch original. TRANSPORT is REAL: both committed copies equal `.remedy-wt/f040-r3-block.md` at sha256 `f43b5ab338bf700e879df1a1c3ab1cb00e918051dbaa20f82ff7c51e03a0ab8f` over 24441 bytes. THE PLAN is byte-equal to PLAN3 at 38 lines. THE RECORD APPEND reconstructs at 1655733 + 1 + 6933 = 1662667, N counted as 3, paragraph order holding. THE SLIPS APPEND is exact: the committed file EQUALS the pre-commit bytes followed by SLIP3 with no separator of its own, 284 lines to 290, and the blank-line convention the R1 entry lost is restored going forward. THE LEDGER moved as ordered — registered 312 to 313 with ADDED `['R-0752']`, resolved ADDED `[]`, `DECISION F040` ADDED `['D5']`, one `^Gate: F040 R2 — ` line. THE MODULE IS PURE, measured rather than asserted: over comment- and docstring-stripped source, `open(`, `subprocess`, `socket`, `requests`, `urllib` and `except:` each occur ZERO times, and the single purity-grep hit the worker reported is prose in the module docstring. It calls `build_report_sources` at line 95 and names `collect_report_sources` only in the comment at line 84 explaining why it does not use it — which is the trap that would have made the `open-decision` rule unreachable. THE ONE-SOURCE PROPERTY WAS RE-PROVED BY THE REVIEWER IN ITS OWN WORKTREE, control first: unmutated 40 passed at REAL exit 0; replacing the `recommended_next_action` call with a hard-coded `NextAction` gave REAL exit 1 at 6 failed and 34 passed; the restored bytes gave 40 passed again. Six tests bite on that one line, so the property is pinned rather than merely described. NINE SUITES were re-run serially in the primary checkout, every one REAL exit 0: `test_run_report.py` 81, `test_decision_inbox.py` 43, `test_job_digest.py` 40, `tests/ui_server/` 508, `tests/ui_contracts/` 699 passed with 4 skipped, `test_integrity_gate.py` 16, `test_resource_safety.py` 21, `tests/docs/` 295 and the canary 42. EIGHT COMMITS, one path each, insertions 321, 263, 18, 6, 6, 239, 492 and — the reading the handback cannot take of itself — 365 for the handback commit, every one under 500. THE WORKER'S SEVEN DEVIATIONS WERE ALL CORRECTLY DECLARED. Two deserve naming. Its C5 first landed at 501 insertions, one over the AGENTS.md cap, and it unwound the commit before any push and re-made it at 492 by deleting a test whose propositions the assertion beside it already implied — the right repair, and declared rather than quietly amended. And its G4 draft used a resolved-id pattern matching zero lines in the record, which it caught and corrected mid-gate to the file's real `^Done: R-\d+` convention: that is a gate that could not fail, found and fixed by the worker rather than by the reviewer, which is the outcome the whole gate discipline exists to produce.

- R-0753 — Medium, THE DIGEST'S COST BASIS HAS THREE VALUES AND ONLY ONE OF THEM IS REACHABLE IN PRODUCTION, BECAUSE THE PERSISTED ACTUALS RECORD CARRIES NO MONEY AT ALL. Raised by the WORKER of F040 R3 as deviation 2, from its own reading while building the cost branch, and CONFIRMED INDEPENDENTLY by the reviewer at `2b063387`. THE MEASUREMENT: `_PERSISTED_ACTUALS_FIELDS` at `packages/orchestration/budget_guard.py:674-677` is a CLOSED set of seven names — `schema_version`, `provider_call_count`, `actual_call_count`, `unmeasured_call_count`, `total_tokens`, `actual_sources`, `started_at` — and `decode_persisted_budget_actuals` REJECTS any field outside it (:700-703, "persisted actuals has unknown fields"), while `counters_from_persisted` at :793-813 constructs `BudgetCounters` from seven values and sets NONE of the three F104 money fields. `measured_cost_usd` therefore takes its `None` default on every counters object built from persisted state, so DECISION F040 D4's mapping can only ever answer `absent`: `lower_bound` and `actual` are unreachable through the one route production uses. Medium rather than Low because it is not the digest's defect and does not stop at the digest — `run_report._evidence_sources` reads the same route at `packages/orchestration/run_report.py:829-845` and takes only `token_description`, `cost_basis` and `elapsed_seconds` from it, so the REPORT has never rendered a persisted money figure either, and F104's money actuals reach no reader that survives a process boundary. WHAT IT COSTS F040: the hero card's cost line will always draw the `~` and say `, estimated`, which is HONEST — the figure genuinely is not measured — but the basis treatment DECISION F040 D4 specifies is only demonstrable in tests until the persisted record carries money. The round did the right thing rather than the convenient one: it pinned the measurement in `test_the_persisted_cost_route_carries_no_money_today` so the test stand-in is deleted when the route learns to price a run, instead of asserting a reachability the code does not have. NOT F040's TO FIX — the repair widens a persisted schema and its decoder, which is F104's surface and needs its own round — so it is CARRIED as this feature's documented risk, in the manner precondition 1 of docs/roadmap/STATUS_closure_protocol.md admits. The open set was searched for the defect before this id was minted, per §3 item 30, and no finding describes the persisted money gap.
<<<END RECORD4

<<<BEGIN PAIRHANDLERS-FROM
                "diff": _build_diff_json,
<<<END PAIRHANDLERS-FROM

<<<BEGIN PAIRHANDLERS-TO
                "diff": _build_diff_json,
                "digest": _build_digest_json,
<<<END PAIRHANDLERS-TO

## SPEC for C3 — the builder in `packages/orchestration/ui_server.py`

Read `_build_decisions_json` first — it begins at line 2771 and is the sibling
this endpoint is modelled on, chosen because it is the same shape: a pure
composition over one job that owns no storage.

Add `_build_digest_json` immediately beside the decisions builder, following the
two conventions that sibling demonstrates:

- the package import is LOCAL to the function, not module-level, exactly as
  `_build_decisions_json` imports `build_decision_inbox` inside its own body;
- the version field is owned by the COMPOSED MODULE — `JOB_DIGEST_VERSION` lives
  in `job_digest.py` and the server adds nothing to the payload. `_send_json`
  does not wrap: the builder's dict IS the response body.

The function:

    def _build_digest_json(job: Any) -> dict[str, Any]:

with a one-line docstring in the siblings' voice, loading events through the same
`_load_events(job)` helper the decisions builder uses and returning
`build_job_digest(job, events)` — nothing else. Per constraint 9 it adds no
behaviour: no key is added, removed, defaulted or renamed here.

Then apply PAIRHANDLERS, which registers the route. The dict at line 3467 is the
one the path guard at :3445 dispatches through, so registration is the whole
wiring — `handlers.get(endpoint)` finds it and `_send_json(200, handler(job))`
serves it. A route that cannot load its job returns the loader's error before any
handler runs (:3449-3451), so the builder never sees a missing job.

## SPEC for C4 — `tests/ui_server/test_digest_route.py`

Read a sibling route test in `tests/ui_server/` first and follow its conventions
for standing the server up and issuing a request; do not invent a new harness.

Cover, at least:

- `GET /api/jobs/<job_id>/digest` answers **200** with `Content-Type`
  `application/json`, for a job with a real plan;
- THE ROUTE IS A PASS-THROUGH, asserted directly: the decoded response body
  EQUALS `build_job_digest(job, events)` computed in the test for the same job.
  This is the assertion that makes constraint 9 enforceable rather than
  aspirational — a route that reshaped the envelope fails here;
- the body's top-level key set is exactly the eight `job_digest` specifies, and
  `version` equals `JOB_DIGEST_VERSION` imported from the module — never a
  literal `1`, so a version bump that forgets a consumer reddens here;
- an unknown job id answers the same status its sibling routes answer for one —
  MEASURE what that is from the loader at :3449-3451 rather than assuming 404,
  and assert the measured value;
- an unknown endpoint under the same job path is still unhandled, so adding this
  route did not widen the dispatch: assert a request to a neighbouring
  nonexistent endpoint does not answer 200.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C5, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — `.remedy-wt/f040-r4-block.md`,
   the committed `.agent/authored/f040-r4.md` and `.agent/last_block.md` — with
   the byte length, all three EQUAL. This block states no expected digest.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN4 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1662667 at `2b063387`. Base + one separator newline + RECORD4
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION against
   the entire committed file; (b) PARAGRAPH ORDER — the last N blank-line units
   equal RECORD4's N paragraphs IN ORDER, N COUNTED by your script. NEGATIVE
   CONTROL in a disposable worktree: flip one byte inside the FIRST appended
   paragraph and report that BOTH readings reject it and accept the unflipped
   bytes.

G4 THE LEDGER, at C2. Distinct `^- R-\d+ — ` ids before and after with ADDED
   exactly `['R-0753']`; ADDED resolved `[]`; exactly one `^Gate: F040 R3 — `
   line; `^Done: R-0570`, `^Done: R-0752` and `^Done: R-0753` all 0. Report the
   open count.

G5 THE WIRING, at C3. PAIRHANDLERS is APPEND-shaped: report FROM occurring
   exactly 1x in the committed file and the ONE TO-only line occurring exactly 1x
   AMONG THE LINES C3's DIFF ADDS — do NOT count FROM to zero. Then: the exact
   string `"digest": _build_digest_json,` occurs exactly 1x; `_build_digest_json`
   occurs exactly 2x in the whole file, its definition and its registration;
   the handlers dict now holds 16 entries, reported by counting the keys of that
   literal rather than by asserting the number. Then
   `ruff check packages/orchestration/ui_server.py` and
   `python3 -m compileall -q packages/orchestration/ui_server.py`. Confirm
   `packages/orchestration/job_digest.py` is NOT in this round's path set.

G6 THE ROUTE AND ITS RED PROOF, at C4. First
   `python3 -m pytest tests/ui_server/test_digest_route.py -q` — REAL exit 0
   with the passed count. Then, INSIDE A DISPOSABLE WORKTREE at C4: report the
   UNMUTATED control's exit code over that file FIRST — it must be 0 — then
   DELETE the single line `                "digest": _build_digest_json,` from
   `<worktree>/packages/orchestration/ui_server.py`, having first COUNTED that
   those exact bytes occur exactly once in that file, and report the exit code
   and failing count with the route unregistered. That removes the wiring and
   nothing else, so it proves the tests pin the registration rather than the
   builder. Restore, re-run, and report the restored exit code. Name the
   worktree path, remove it, and report that `git worktree list` no longer holds
   it.

G7 THE SUITES AND THE TREE, at C4. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_job_digest.py -q`,
   `python3 -m pytest tests/ui_contracts/ -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured 508, 40, 699 passed with 4 skipped, 16, 21 and 42 at the base; the
   `tests/ui_server/` count MUST rise by the number of tests C4 adds, so report
   both numbers and the difference. Then `git status --porcelain` EMPTY,
   `git ls-files --others --exclude-standard` count 0, and the per-commit
   insertion counts for C0a through C4, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat` and never from file line counts, the deviations, the
item-status table with every bundle item and every gate appearing exactly once,
and the next steps. State `SESSION 1` of F040 and round 4. No length cap. Record
that T001 is COMPLETE with this round, and name R-0570, R-0752 and R-0753 as
OPEN, the first two routed to paydown and the third carried as this feature's
documented risk.
