# Handback — F058 round 4: book round 3 (PASS), repair R-1261, move `parked_session_refs`, and T003 — the cooldown, the session guard and the three non-triggers through a run

## Session

SESSION 3 of feature F058 · round 4 (resumed) · rounds so far 4

Session 2 ended after C4 with a partial C5 (one test file, uncommitted) in the tree; session 3
(this one) verified the block's digest and line count, kept that partial file, finished C5 and ran
the gates and this handback.

Context self-assessment: this session read the block, the walk, the factory, the call record and
the run seam before writing any test, and wrote every test against values it had read or measured
by a one-off introspection script, so the one open risk is that the three run fixtures were
proved only by gate 3, the single permitted run.

Fortschritt: ~75 % (T001, T002 and T003 landed · the documentation page and the closure open) — Schätzung

## Range

Review of `f7ca54efe`..HEAD.

## Commits

### 0c39746a1 F058 R4 C1: book round 3 (PASS, R-1261; R-1259 and R-1260 resolved), DECISION F058 D4 (made by session 2)

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-r4.md` | +224/-0 | NEW FILE, copy of the round's block (224 lines, sha256 `484a9eac5087175d9e13e038946acd9900a5eddea73062f5038c1e0da8b8dd18`) |
| `.agent/decisions.md` | +12/-0 | DECISION F058 D4 |
| `.agent/live_review.md` | +8/-0 | round 3's verdict, R-1261, the resolutions of R-1259 and R-1260 |
| `.agent/plan.md` | +11/-17 | rewritten for round 4 |
| `.agent/prose_slips.md` | +1/-0 | one prose-slip line |

### 27635158f F058 R4 C2: repair R-1261 (the call record's docstring) (made by session 2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_call_record.py` | +4/-3 | `_session_fields` docstring: every call the walk reached carries `failover` |

### cc9e206a4 F058 R4 C3: parked_session_refs moves to pingpong_call_record.py (structural, DECISION F058 D4) (made by session 2)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +3/-2 | `pingpong_loop.py` row and bullet |
| `packages/orchestration/pingpong_call_record.py` | +17/-1 | `parked_session_refs` moved here |
| `packages/orchestration/pingpong_loop.py` | +5/-17 | function removed, imported back by name |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` falls by what the file lost |

### 35de9362f F058 R4 C4: the cooldown, the sticky window and the session guard (T003, DECISION F058 D4) (made by session 2)

| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | +1/-0 | regenerated from the registry |
| `packages/orchestration/config_keys_model_routing.py` | +14/-0 | `model_failover.cooldown_s` key |
| `packages/orchestration/model_failover.py` | +170/-26 | cooldown names, `primary_skipped`, the held walk, the session guard |
| `packages/orchestration/pingpong_call_record.py` | +10/-2 | `parked_session_refs` clears a role a backup served |
| `packages/orchestration/role_provider_factory.py` | +7/-1 | wrapper built with `cooldown_s=resolve_failover_cooldown_s()` |

### 267f94b62 F058 R4 C5: the cooldown's, the session guard's and the non-triggers' tests (T003)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_model_failover.py` | +307/-2 | existing-test changes, `TestResolveFailoverCooldown`, registry test, `TestStickyWindow`, `TestSessionGuard`, `_ScriptedProvider`, the three non-trigger run fixtures |
| `tests/orchestration/test_pingpong_call_record.py` | +29/-1 | `TestParkedSessionRefsFailover` (three cases) |
| `tests/orchestration/test_role_provider_factory.py` | +46/-1 | `TestCooldownIsConfigured` |

### this commit F058 R4 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |
| `.agent/plan.md` | +5/-4 | Current Step rewritten from forward-looking to what landed (see Deviations 3) |

## External actions

No pull request opened (`gh pr list --state open --json number` read `[]` at the start of the
session). No worktree added or removed. Scratch under `.remedy-wt/f058-r4-worker/` (gate 3 output,
integrity JSON), gitignored. The push that follows this commit is reported in the final reply only.

## Verification

**Resume preconditions:** branch `feature/f058-model-failover-chain`; HEAD `35de9362f`; open PRs
`[]`; only dirty path `tests/orchestration/test_model_failover.py`. Block: 224 lines, sha256
`484a9eac5087175d9e13e038946acd9900a5eddea73062f5038c1e0da8b8dd18`, both as ordered.
`run_selection.py` sha256 `45e942f1...f96`, `selection.txt` sha256 `aaf44217...116f`, both as ordered.

**C5:** the partial file was kept. The only `to_json()` compared with a literal anywhere in
`tests/` is the one in `test_primary_unavailable_first_link_serves_discloses_one_attempt` (grep of
`primary_error"` found two other lines, both subscripts, not literals). `ruff check tests/orchestration/`:
`All checks passed!`. No test was run before gate 3.

**Gates (after C5):**

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. PASS.
2. `python3 -m ruff check <the nine files of the block>` → `All checks passed!`. PASS.
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f058-r4/prep/run_selection.py /home/decodeux/Repos/remedy`
   → exit 0, `5081 passed, 3 skipped in 47.54s`. SKIPPED lines: `tests/test_agent_tooling.py:43`
   (D12 quarantine, F252); `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`);
   `tests/test_repair_context_reviewer_memory.py:257` ("UI source not found"). A grep of the output
   for `FAILED`, `ERROR`, `absent in tree:` and `process(es) behind` counted 0. PASS.
4. `python3 -m apps.cli.main integrity check --json` → `fail_count` 0. PASS.
5. `open_finding_ids` → `['R-1235', 'R-1246', 'R-1251', 'R-1252', 'R-1261']`. PASS.
6. `git log --format=%s f7ca54efe..HEAD` →
   `F058 R4 C5: the cooldown's, the session guard's and the non-triggers' tests (T003)`,
   `F058 R4 C4: the cooldown, the sticky window and the session guard (T003, DECISION F058 D4)`,
   `F058 R4 C3: parked_session_refs moves to pingpong_call_record.py (structural, DECISION F058 D4)`,
   `F058 R4 C2: repair R-1261 (the call record's docstring)`,
   `F058 R4 C1: book round 3 (PASS, R-1261; R-1259 and R-1260 resolved), DECISION F058 D4`. PASS.

## Authored-text proofs

C1 (session 2) copied the prepared files; the block's own copy reads 224 lines and the digest above,
equal to the delivering prompt. Session 3 applied no reviewer-authored text. `None applied` in C5 and C6.

## Deviations & assumptions

1. **Resumed session.** C1 to C4 were made by session 2 and C5 was finished by session 3; the block's
   "before any write" preconditions were replaced as the resume prompt states. No commit was amended.
2. **Existing tests changed (C5):** `test_primary_unavailable_first_link_serves_discloses_one_attempt`
   (call passes `resume=None`, primary recorded with `None`, literal `to_json()` gains
   `"primary_skipped": False`). No other existing test was changed.
3. `.agent/plan.md`'s Current Step was forward-looking and is rewritten by this handback to what
   landed (the Commit Gate requires the step be accurate).
4. `SeamFakeClock`, `_seam_governor` and `RATE_LIMITED_RETRYABLE_ERROR` are IMPORTED from
   `tests/orchestration/test_provider_retry.py` (not copied); other tests already import across
   `tests.orchestration.*`.
5. The factory test reads the hold through the wrapper's read-only `held_until` property (added in
   C4), bracketed by `time.monotonic()` readings, because the factory leaves the clock at its default.
6. The run fixtures use a `_ScriptedProvider` stub placed through `pingpong_loop.create_provider`
   (the real function answers every other name); each fixture asserts the chain resolves, that
   `("stub", "primary-model")` was asked for, that `("fake", "stand-in")` was not, and that no round
   entry carries `failover`. The reviewer-role chain uses tier `mid`, which the hard rules admit
   (checked with `validate_failover_chains`).
7. No mutation proofs and no second test run were made, as ordered. No gate 3 re-run was needed.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): check first.
2. Phase 1 rule 2, the Open PR Gate: check for open pull requests before starting new work.
3. The next round's first commit books round 4's verdict.
4. The documentation page and the closure's integration gate.

Operator questions open: 0.
Open findings: 5 — R-1235, R-1246, R-1251 and R-1252, owned by F306; R-1261, owned by F058,
repaired this round and awaiting the reviewer's verdict.

## For the operator, in plain sentences

After a backup model has answered once in a run, that role's next calls go straight to the backups
for five minutes, a time the operator can change in the settings, and then the usual service is
tried again. A conversation a backup model began is never continued by a different model. Checks
now run whole runs to show that a slow answer, a rate limit and an unreadable answer never switch
to a backup.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | made by session 2 |
| C2 | done | made by session 2 |
| C3 | done | made by session 2 |
| C4 | done | made by session 2 |
| C5 | done | one commit, 382 insertions; partial file from session 2 kept and completed |
| C6 | done | this handback |
| Gate 1 | passed | `git status --porcelain` empty |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | `5081 passed, 3 skipped`, exit 0, no FAILED/ERROR/absent/behind line |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | open-id list matched exactly |
| Gate 6 | passed | C1 to C5 subjects, newest first |
| R-1261 | repaired | C2; awaiting the reviewer's verdict |
