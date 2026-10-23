# Handback — F133 round 3

## Session

SESSION 1 of feature F133 · round 3 · rounds so far 3.

Context self-assessment: every production and test file this round touched was read whole before
editing (the module, the view, both test files, the docs page, `config_keys_model_routing.py`,
`token_ledger.py`'s cost-basis constants, `pingpong_job.py`'s status constants, `FailureClass`),
every registration and DECISION this round specifies was read after C1 from the committed file
rather than the prepared snapshot, and every number reported below (golden unchanged, test counts,
gate readings) was produced by running the thing, not recalled.

Fortschritt: ~60 % (T001, T002 and the trust view with its recommendation landed · the routing
note in the plan view, the one-home guard and the end-to-end open) — Schätzung

For the operator: this round closed the three small gaps the previous round's reviewer found and
then finished the trust view's last planned piece. The view now reads a call's actual price basis
from the ledger instead of guessing it, and names a label for a mix of price sources rather than
calling it something more certain than it is. The cost figure now also states how many successful
attempts it is averaged over, the same way the other figures already did. Seven small behaviours
that were already correct but had no test proving it now each have one, so a future change that
breaks any of them will be caught. Last, the view now ends with a short recommendation for each
role shown: when one model clearly out-performs the others by a wide enough margin, the view names
it and says adopting it is a configuration and documentation step for a person to take, never
something the system does by itself. A role with too few comparable models, or no model far enough
ahead, says so instead of guessing. The design decision to drop a second, separate per-tier summary
that an earlier plan had sketched was also made and recorded, because the function that would have
fed it writes to the database on every read and keeps no time window, which this view's whole point
is to avoid.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical, then committed |
| C2 | done | cost basis read from the ledger, cost-per-pass passes added to the module's result, settings' keys imported from the registry |
| C3 | done | one test per surviving mutation (seven), plus three cost-basis tests — 20 new tests across both files, all green |
| C4 | done | `TRUST_LEADER_MARGIN`, `trust_leader`, `TrustRecommendation`, and the view's recommendation line/JSON |
| C5 | deviated | the recommendation's tests and the docs page, plus a declared, necessary fix outside the named paths — see Deviations 1 |
| C6 | done | this handback |
| C7 | done | this handback (its own commit) |
| R-1429 | done | repaired in C3: one test per survivor, each red under its named mutation |
| R-1430 | done | repaired in C2, tested in C3: `cost_basis` read from the ledger, `price_table` and `mixed` labels |
| R-1431 | done | repaired in C2, tested in C3: the cost cell names its passes |
| Gate 1 | deviated | `verify.py` read one `False` line, on a stray path `tests/docs/test_retired_promote_word.py`; every other line read `True` — see Deviations 1 |
| Gate 2 | done | ruff over the 5 touched `.py` files: exit 0, `All checks passed!` |
| Gate 3 | done | exit 0, `10243 passed, 5 skipped`, no FAILED/ERROR, no "process(es) behind" line |
| Gate 4 | done | `fail_count` 0 |
| Gate 5 | done | `14` |
| Push | done | `git push origin feature/f133-provider-trust-score` run immediately after this commit |

## Range

Review of `c1804c605`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `402fe452b` F133 R3 C1: book round 2, register R-1429 to R-1431, DECISION F133 D3, the plan, the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f133-r3.md` | +120/-0 (new) | byte copy of the block, proved equal to it |
| `.agent/decisions.md` | +12/-0 | DECISION F133 D3 appended |
| `.agent/live_review.md` | +8/-0 | round 2's FAIL Gate entry and R-1429 to R-1431 appended |
| `.agent/plan.md` | +4/-5 | rewritten for round 3 |

Every one of the four is a byte-for-byte copy of its prepared `c1-*` file under
`.remedy-wt/f133-r3/prep/`, each proved equal by a sha256 comparison before staging.

### `85e8154f7` F133 R3 C2: the cost basis read from the ledger, the cost per pass with its passes, and the settings' keys spelled once

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_trust_score.py` | +45/-22 | R-1430: `_CALL_QUERY` selects `cost_basis`; `_RowAccumulator` tracks `all_priced`/`priced_bases` instead of a bare `cost_known`; `_finalize_row` labels `price_table`/`mixed`; `resolve_trust_settings` reads the three `TRUST_*_CONFIG_KEY` constants (D3 (4)); docstring updated for the cost basis and to withdraw the `tier_outcomes` claim (D3 (3)) |
| `apps/cli/commands/stats_trust_cmd.py` | +16/-7 | R-1431: `_format_cost` names the passes its figure rests on |

### `c8ab61ebd` F133 R3 C3: tests for the seven surviving mutations, the cost bases and the passes

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_model_trust_score.py` | +106/-7 | `TestSettlement` (blocked-as-fail, applied/completed-as-pass); two new `TestFormatErrors` cases (cross-round retry, non-parse post-mortem); three new `TestCostBases` cases (`price_table`, `mixed`, figure-with-`unknown`-basis); `_call`/`_postmortem`/`_one_pass` helpers extended with an optional override, never changed in meaning for an existing caller |
| `tests/cli/test_stats_trust_cmd.py` | +63/-0 | the text-view `--role` test; the no-settled-task dash test; the cost-cell-names-its-passes test; the signed-delta test |

### `758e4ded7` F133 R3 C4: the clear leader and the recommendation line per role

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_trust_score.py` | +69/-1 | `TRUST_LEADER_MARGIN`, the three `TRUST_RECOMMENDATION_*` reason constants, `TrustRecommendation` and `trust_leader(table, role)` (D3 (1)); docstring sentence added |
| `apps/cli/commands/stats_trust_cmd.py` | +49/-1 | `_shown_roles`, `_format_recommendation` (the three wordings, exactly), `_recommendations_payload`; wired into `render_trust_text` and the JSON output |

### `c29ffab08` F133 R3 C5: the recommendation's tests and the trust score page brought up to date

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_model_trust_score.py` | +54/-0 | `TestTrustLeader`: the leader at exactly the margin, just below it, a thin row, fewer than two eligible rows, a tie |
| `tests/cli/test_stats_trust_cmd.py` | +70/-1 | the three wordings each asserted as the whole line; the JSON's `recommendations`; round 2's `test_the_text_shows_each_row_with_its_columns_dashes_and_thin_marker` extended (not loosened) for the matrix's new trailing line |
| `docs/system/model-trust-score-v1.md` | +53/-19 | the cost basis read from the ledger, the cost cell's passes, a new "The clear leader and its recommendation" section, the per-tier withdrawal (D3 (3)), the routing note moved to round 4, the status banner rewritten |
| `docs/README.md` | +1/-1 | the page's index row brought up to date |
| `tests/docs/test_retired_promote_word.py` | +9/-0 | declared deviation — see Deviations 1 |

### `3ee401769` F133 R3 C6: Landed lines for R-1429 to R-1431

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6/-0 | three `Landed:` paragraphs, each naming what changed and its commit; no `Done:` line |

## External actions

- Open PR Gate was re-run at session start: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  returned `[]`, and the branch was already `feature/f133-provider-trust-score`, so no new branch
  was created and no merge was needed.
- `git push origin feature/f133-provider-trust-score` → run immediately after this commit.
- No pull request created (the block orders none this round). No worktree added or removed.

## Verification

Interpreter: the repository's configured Python 3. All five gates were taken once, on `3ee401769`
(this commit's parent), after C6 and before this commit, per the block.

| Command | Exit | Decisive output |
|---|---|---|
| `git -C <repo> status --porcelain` | 0 | empty |
| `python3 .remedy-wt/f133-r3/prep/verify.py .` | 0 | one line `False` — `c29ffab08 touches only the block's change set; stray: ['tests/docs/test_retired_promote_word.py']`; every other line `True`; last line `ALL False` |
| `python3 .remedy-wt/f133-r3/prep/ruff_touched.py .` | 0 | `ruff over 5 files: exit 0` / `All checks passed!` |
| `python3 .remedy-wt/f133-r3/prep/run_selection.py . .remedy-wt/f133-r3-worker/selection-output.txt` | 0 | `paths 211` / `10243 passed, 5 skipped, 1 warning in 103.40s (0:01:43)`; no FAILED, no ERROR, no "process(es) behind" line |
| `python3 -m apps.cli.main integrity check --json` | 0 | `"fail_count": 0, "ok": true, "passed": true` |
| `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` | 0 | `14` |

Gate 3's three `SKIPPED` lines, printed as they are:
```
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

## Authored-text proofs

C1's four paths are all reviewer-authored text applied this round. Each was copied from its
prepared `c1-*` file under `.remedy-wt/f133-r3/prep/` and proved byte-identical by a sha256
comparison immediately after the copy, before `git add`; all four read `OK`. The new file
`.agent/authored/f133-r3.md` was separately checked: `wc -l` reads 120 and its sha256 is
`f47b01239b1648590d3cc72619828e23c18bdd67cd9c3c941fae2eba4d5d2d5d`, identical to
`.remedy-wt/f133-r3/prep/block.md`'s own `wc -l` and sha256 — confirmed by `verify.py`'s own
"the saved block equals block.md" check, which read `True`.

## Deviations & assumptions

1. **Gate 1 reads one `False` line; the cause is declared, not hidden.** DECISION F133 D3 (1)
   fixes three wordings verbatim for the recommendation line, one of which reads "Adopt it through
   config and an ADR, as the promotion rule of `docs/agents/model_routing_policy.md` requires" —
   copied letter for letter from the decision, because the block says these wordings go in
   "exactly," and the cited section really is titled that in the policy document. That exact
   phrase, once it exists in `apps/cli/commands/stats_trust_cmd.py` (C4) and the test asserting the
   whole line in `tests/cli/test_stats_trust_cmd.py` (C5), is read by a repo-wide guard,
   `tests/docs/test_retired_promote_word.py`, that scans every tracked file for a retired verb and
   fails closed on any occurrence it has not been told the sense of; the round's own gate 3
   selection names the whole `tests/docs` directory, so that guard is one of the tests gate 3 runs.
   Leaving it unregistered would have left gate 3 red with no file named in any commit's path list
   that could fix it; the three-entry registration (the sense this occurrence actually has, a model
   promoted into a task class, already has a label in that guard) is the smallest fix, and it was
   folded into C5 because two of the three occurrences land there. The guard file itself is not a
   path C4 or C5 was named for, so `verify.py`'s static allow-list, which was written before this
   wording existed, reads the registration as a stray path on commit `c29ffab08` and fails that one
   check. Per this round's own instruction that the registrations and DECISION F133 D3 win over the
   block where they seem to differ, the decision's verbatim wording was kept and the guard was kept
   green; this is the difference being reported, in gate 1's own reading above, not smoothed over.
2. The three new `TRUST_RECOMMENDATION_*` reason values, `leader`/`too_few_eligible`/`no_margin`,
   and the extra `leader_settled_tasks` field on `TrustRecommendation`, are not named in the block
   or D3 (1) by these exact identifiers; D3 (1) only says "the reason" and lists the three
   situations in prose. The names were chosen to match the module's existing naming style
   (`TRUST_COST_BASIS_*`) and the settled-tasks figure was added because wording 1 needs `<n>` and
   nothing else on `ModelTrustRow` or `TrustRecommendation` carried it without a second lookup.
3. `TRUST_COST_BASIS_PRICE_TABLE` duplicates the ledger's own `COST_BASIS_PRICE_TABLE` string as a
   second constant (as `COST_BASIS_PROVIDER_REPORTED`/`COST_BASIS_UNKNOWN` already did before this
   round), rather than importing it, because a plain top-level import of it was flagged
   `F401 imported but unused` by ruff (nothing in this module referenced the alias directly, only
   re-exported it for the view); the existing equality test,
   `test_cost_basis_constants_match_the_ledgers_own_vocabulary`, was extended to also assert this
   constant equals the ledger's, keeping "one spelling" enforced by a test rather than by import.
4. No golden change: `tests/orchestration/fixtures/model_trust/golden.json` was re-derived from the
   new cost-basis logic by running `TestGoldenHistory` and it still passes unchanged, because every
   call in the golden's constructed history already carried a cost and the `provider_reported`
   basis, which is still `all_priced` and a single shared basis under the new rule. `git status`
   confirms the file was never touched this round.
5. No difference was found between the block and DECISION F133 D3 on anything this round built; D3
   is more detailed than the block everywhere the two overlap, never in conflict with it.
6. No change outside the paths named per commit, except the one declared in item 1 above. No
   `Done:` line was written anywhere, only `Landed:`. No mutation red-proof was run (the
   reviewer's). The full suite was not run; only the ordered selection plus every `tests/test_*.py`
   and `tests/docs/`, once, after C6.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 3's verdict in the next round's first commit.
4. Round 4: the informational routing note, the one-home guard, the end-to-end.

Operator questions open: 0. Open findings: 14.
