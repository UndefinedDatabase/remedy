# Handback — F297 round 2: book round 1, structural step, T005 to T009 landed

## Session

SESSION 1 of feature F297 · round 2 · rounds so far 2

Context self-assessment: the worker's context is comfortable; the session continues.

Fortschritt: ~32 % (T001 to T009 landed · T010 to T025 open) — Schätzung

## Range

Review of `0a5acfc08`..`HEAD`.

## Commits

### b6b2666a6 F297 R2 C1: book round 1 and the resolutions of R-1172, R-1243 and R-1242, DECISION F297 D3

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r2.md` | +167/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r2/prep/block.md` |
| `.agent/live_review.md` | +8/-0 | appended the `Gate: F297 R1` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1172, R-1243, R-1242 |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D3: how round 2 repairs R-1143, R-1176, R-1196, R-1138 and R-1162, and that R-1196's structural step comes first |
| `.agent/prose_slips.md` | +2/-0 | two dated lines for F297's round 1 |
| `.agent/plan.md` | +13/-13 | rewritten in full for F297 round 2 |

### 163424d1a F297 R2 C2: the run-log reader skips a line that is not an object and sorts timestamps as text (R-1143)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/timeline.py` | +8/-4 | `load_run_events` now skips a parsed line whose JSON is not a `dict` and sorts by `str(timestamp)` instead of the raw value (R-1143) |
| `tests/test_timeline.py` | +27/-0 | new coverage for a non-object JSON line and for timestamp values that are not strings |
| `tests/orchestration/test_client_digest.py` | +9/-7 | the damaged-log test now expects both jobs' decisions listed rather than a degraded digest, because the reader no longer raises |

### ff993ac9a F297 R2 C3: a supervisor restart passes over a run whose end is recorded (R-1176)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | +4/-3 | `reconcile_open_runs` now skips a record whose `ended_at` is set, in addition to `exit_code` (R-1176) |
| `tests/orchestration/test_serve_runs.py` | +32/-0 | new coverage for a record with `ended_at` set but `exit_code` still None |

### a2bca3d11 F297 R2 C4: structural step, the sr branch of the decision resolve command becomes a function of its own

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/decision.py` | +19/-11 | the `sr:` branch of `_cmd_decision_resolve` extracted verbatim into `_resolve_stop_reason_decision`; no behaviour change |
| `docs/system/structure-ledger-v1.md` | +1/-1 | row updated for the new function boundary |
| `tests/test_structure_ratchet.py` | +1/-1 | ratchet pin lowered to match the new row |
| `tests/cli/test_client_interface.py` | +3/-1 | the answer-tree-naming test now also reads `_resolve_stop_reason_decision` |

### c672ef482 F297 R2 C5: a stop-reason decision resolves its job before reading any file (R-1196)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/decision.py` | +4/-1 | `_resolve_stop_reason_decision` now calls `resolve_job_id_or_fail` and uses the resolved `job_id` before it reads any stop-reasons file (R-1196) |
| `tests/cli/test_decision_cmd.py` | +15/-1 | new coverage for a job-id value that resolves to failure before any file read |

### 0f2c4ad13 F297 R2 C6: a round whose builder changed no file is described as exactly that (R-1138)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | +1/-1 | the no-changes diff summary now reads "(no changes — the builder changed no file)" |
| `packages/orchestration/pingpong_evidence.py` | +2/-2 | the tests-text and review-json summaries for `builder_no_changes` now state exactly that nothing was checked; the `no_changes_verified` verdict word is unchanged |
| `tests/orchestration/test_pingpong_cli.py` | +51/-0 | new coverage for the updated diff summary and review text |
| `tests/orchestration/test_evidence_bundle.py` | +8/-0 | new coverage for the updated bundle text |

### 254ddcda1 F297 R2 C7: a claude-cli call with no model set is fingerprinted under a fixed name (R-1162)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/claude_cli_command.py` | +5/-0 | new constant `CLAUDE_CLI_UNSET_MODEL = "claude-cli-default"`, the fingerprint name for a call with no model set (R-1162) |
| `packages/orchestration/pingpong_provider.py` | +4/-4 | the three `prepare_call_input` call sites now pass `self._model or CLAUDE_CLI_UNSET_MODEL`; no net growth |
| `tests/orchestration/test_claude_cli_resume.py` | +8/-4 | coverage updated for the fixed fingerprint name |
| `tests/orchestration/test_job_stop_integration.py` | +36/-0 | new coverage: a `claude-cli` job with no model set, stopped during its first builder call, now ends `stopped` rather than left `running` |

### this commit F297 R2 C8: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

None during the round. `git push origin feature/f297-findings-paydown-v7` after this commit, reported below with the post-push `git rev-parse HEAD origin/feature/f297-findings-paydown-v7`. No PR created or touched; no other `gh` command run. The Open PR Gate is Phase 1 rule 2 of the self-drive protocol and is listed in `## Next` for whoever starts the next cycle.

## Verification

**Preconditions (before C1):** `git status --porcelain` empty; `git rev-parse HEAD` read `0a5acfc0801b725c8cfdc3526a4991dc436f62cd`, the required base; `git branch --show-current` read `feature/f297-findings-paydown-v7`.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r2/prep/block.md` read `167`; `sha256sum` read `a077106f61d1bc8bbe259f561baca793d8c1ed16256923c62031481b388e7dff` — both equal to the values the prompt delivered. All 30 Bundle-listed prepared files (`block.md`, 23 `dry-*`/`c4-decision.py` files, 3 `append-*.txt` files, `verify.py`, `run_selection.py`, `selection.txt`) hashed via a python3 script under `.remedy-wt/f297-r2-worker/check_digests.py`: every one read `OK`, final line `ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the block and the four `dry-*` whole files; each printed `cmp_equal=True`. `git branch --show-current` read `feature/f297-findings-paydown-v7` before staging. `git diff --cached --numstat` read exactly `167 0 .agent/authored/f297-r2.md`, `12 0 .agent/decisions.md`, `8 0 .agent/live_review.md`, `13 13 .agent/plan.md`, `2 0 .agent/prose_slips.md` — matching the block's required readings. The staged diff of `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` was read in full and matched the block's "For the record" description exactly (the `Gate: F297 R1` paragraph, the three `Done:` paragraphs, DECISION F297 D3, the two prose-slip lines).

**C2:** `python3 -I c2_copy.py` copied the three files; each printed `cmp_equal=True`. `git diff --cached --numstat` read `8 4 packages/orchestration/timeline.py`, `9 7 tests/orchestration/test_client_digest.py`, `27 0 tests/test_timeline.py` — matching the block exactly. The staged diff of `timeline.py` was read in full: `load_run_events` now `continue`s past non-JSON lines, drops a parsed value that is not a `dict`, and sorts by `str(e.get("timestamp", ""))`.

**C3:** `python3 -I c3_copy.py` copied the two files; each printed `cmp_equal=True`. `git diff --cached --numstat` read `4 3 packages/orchestration/serve_runs.py`, `32 0 tests/orchestration/test_serve_runs.py` — matching the block exactly. The staged diff was read in full: `reconcile_open_runs` now skips a record when `record.exit_code is not None or record.ended_at is not None`.

**C4:** `python3 -I c4_copy.py` copied the four files (`c4-decision.py` for `decision.py`, the three `dry-*` files); each printed `cmp_equal=True`. `git diff --cached --numstat` read `19 11 apps/cli/commands/decision.py`, `1 1 docs/system/structure-ledger-v1.md`, `3 1 tests/cli/test_client_interface.py`, `1 1 tests/test_structure_ratchet.py` — matching the block exactly. The staged diff of `decision.py` was read in full: a verbatim extraction of the `sr:` branch's body into `_resolve_stop_reason_decision`, called from the original site; no other line changed.

**C5:** `python3 -I c5_copy.py` copied the two files; each printed `cmp_equal=True`. `git diff --cached --numstat` read `4 1 apps/cli/commands/decision.py`, `15 1 tests/cli/test_decision_cmd.py` — matching the block exactly. The staged diff was read in full: `_resolve_stop_reason_decision` now resolves `job_id` via `resolve_job_id_or_fail` before building `stop_id` and calling `resolve_stop_reason`, passing the resolved `job_id` rather than the raw string.

**C6:** `python3 -I c6_copy.py` copied the four files; each printed `cmp_equal=True`. `git diff --cached --numstat` read `2 2 packages/orchestration/pingpong_evidence.py`, `1 1 packages/orchestration/pingpong_loop.py`, `8 0 tests/orchestration/test_evidence_bundle.py`, `51 0 tests/orchestration/test_pingpong_cli.py` — matching the block exactly. The staged diff was read in full: only the three described strings changed; the `no_changes_verified` verdict word is untouched.

**C7:** `python3 -I c7_copy.py` copied the four files; each printed `cmp_equal=True`. `git diff --cached --numstat` read `5 0 packages/orchestration/claude_cli_command.py`, `4 4 packages/orchestration/pingpong_provider.py`, `8 4 tests/orchestration/test_claude_cli_resume.py`, `36 0 tests/orchestration/test_job_stop_integration.py` — matching the block exactly. The staged diff was read in full: the new `CLAUDE_CLI_UNSET_MODEL` constant, its import, and `self._model or CLAUDE_CLI_UNSET_MODEL` at the three `prepare_call_input` call sites; no `--model` argument added to any command line.

Every `git branch --show-current` run immediately before a commit (C1 through C7) read `feature/f297-findings-paydown-v7`.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then `python3 .remedy-wt/f297-r2/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (23 file-equality checks and the three ledger/decisions/prose_slips base-plus-slice checks), last line `ALL True`, exit 0.

**Gate 2:** `python3 -m ruff check` over the 17 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r2/prep/run_selection.py /home/decodeux/Repos/remedy` → 6 SKIPPED lines (`tests/orchestration/test_real_ollama_smoke.py` ×3 opt-in Ollama smoke, `tests/test_agent_tooling.py:43` D12 quarantine, `tests/test_install_smoke.py:175` opt-in install smoke, `tests/test_repair_context_reviewer_memory.py:257` UI source not found), no FAILED or ERROR line, no `process(es) behind` line, summary `7309 passed, 6 skipped in 76.12s (0:01:16)`, `exit 0` — identical to the reviewer's dry-tree reading, no UI-toolchain variance this round.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` → `{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass` (`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency` unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean, `high_blockers_open` none open), exit 0.

**Gate 5:** `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` → `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235', 'R-1236', 'R-1237', 'R-1238', 'R-1239', 'R-1240', 'R-1241', 'R-1246', 'R-1247', 'R-1248', 'R-1249', 'R-1250']` — the 26 ids in the required order, exit 0. (R-1143, R-1176, R-1196, R-1138 and R-1162 are landed by this round's code but stay in the open set until their `Done:` lines are booked in the next round's first commit, per operator amendment amend0827-process-diet rule 1 — the same pattern this round's own C1 applied to round 1's three resolutions.)

**Gate 6:** `git log --format=%s 0a5acfc08..HEAD` → the seven subjects of C1 to C7, newest first, exactly as required, exit 0.

No mutation red-proof was run (the reviewer ran its seven in its dry tree per amend0930-test-load rule 4). No full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by `filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 30-file digest pre-check (above) additionally confirmed every prepared source's sha256 against the Bundle's stated values before any copy:

1. `.remedy-wt/f297-r2/prep/block.md` → `.agent/authored/f297-r2.md`: 167 lines both, sha256 `a077106f61d1bc8bbe259f561baca793d8c1ed16256923c62031481b388e7dff` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256 `2bb08a3c83115c4c7156bf492cbeb392006613ec0f7a45aef79eea08b6c731af` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256 `877225d96e43499d51e0261d6908d0d039f83f31289f9bec901f4608e0d5c108` both.
4. `dry-prose_slips.md` → `.agent/prose_slips.md`: cmp equal, sha256 `dbbfffc0a0e3d73039e811fdd310ff0722ae1ffc6915636e6c068c1e3ebcd02d` both.
5. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256 `00e4d5e46051f89fb22f5b8ebe49282346c3f5229054136837c01d4662b88527` both.
6. `dry-timeline.py` → `packages/orchestration/timeline.py`: cmp equal, sha256 `69de489162d184406fa6a24335044d7e7bf35123c3ef5ca5a82daae0447f9fae` both.
7. `dry-test_timeline.py` → `tests/test_timeline.py`: cmp equal, sha256 `396c2b37299108cfa720f518b8084b0b84bd9f9e4c83249cff302feabbf53e06` both.
8. `dry-test_client_digest.py` → `tests/orchestration/test_client_digest.py`: cmp equal, sha256 `e7b6850669fc5a64d0da46fdb4bc20070e1ec6c61b6aebd3d319b2221eb8c591` both.
9. `dry-serve_runs.py` → `packages/orchestration/serve_runs.py`: cmp equal, sha256 `aedd90654225277ad2249a9d0c3198d361ce46cfed87e72b347f78afc293a541` both.
10. `dry-test_serve_runs.py` → `tests/orchestration/test_serve_runs.py`: cmp equal, sha256 `2e4733e9dd63a11f519d5ef2dd6d70d6f8d74b40cb4e6ac083d4d41eef14e50f` both.
11. `dry-structure-ledger-v1.md` → `docs/system/structure-ledger-v1.md`: cmp equal, sha256 `8d69e7d9e66478ec62fe7306b8803130daf81340d7897c3d7ba659754c906432` both.
12. `dry-test_structure_ratchet.py` → `tests/test_structure_ratchet.py`: cmp equal, sha256 `81b51e6032aa41bc1ef6decf3e7960b75e80850bfd63b0249a092f77eec583af` both.
13. `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: cmp equal, sha256 `2422731b5f769a0720ad6b4ed4fb94feea669c5e567b3a8058ccb64c78659b73` both.
14. `c4-decision.py` → `apps/cli/commands/decision.py` (at C4): cmp equal, sha256 `78027193e0e45bc3219213ccf9b8e1787bb9c3beaeaed589fed2335d6c1edc63` both.
15. `dry-decision.py` → `apps/cli/commands/decision.py` (at C5): cmp equal, sha256 `874d579581a3ef903d84f6e8f6cb99268948265bb1e899f76dcdfdc4005fb1a5` both.
16. `dry-test_decision_cmd.py` → `tests/cli/test_decision_cmd.py`: cmp equal, sha256 `3c246478ea13d898981889ef084131d31649c0398e7b0a6fefee45c53bbb7665` both.
17. `dry-pingpong_loop.py` → `packages/orchestration/pingpong_loop.py`: cmp equal, sha256 `4836a27f1bf037da7b576815af572dec16d0d9067f73b4c931436ec35bf251fe` both.
18. `dry-pingpong_evidence.py` → `packages/orchestration/pingpong_evidence.py`: cmp equal, sha256 `f6c4e1c8954d12e2d430246f86b6f2902cecb09043b283a4bed472ef814377d8` both.
19. `dry-test_pingpong_cli.py` → `tests/orchestration/test_pingpong_cli.py`: cmp equal, sha256 `6d192b2de761fe07b0839145ff39ecacb7f11bd55bba48e2b5aad86be7ce12ee` both.
20. `dry-test_evidence_bundle.py` → `tests/orchestration/test_evidence_bundle.py`: cmp equal, sha256 `fd79c6228b8a77008b34186174088ee07e0ce731e3c3e8ce00fb9b1d27350380` both.
21. `dry-claude_cli_command.py` → `packages/orchestration/claude_cli_command.py`: cmp equal, sha256 `23609bb95a4944714aeb1ac3189d54a6017b90def0b53c8090772f6edc1c787e` both.
22. `dry-pingpong_provider.py` → `packages/orchestration/pingpong_provider.py`: cmp equal, sha256 `63e0c1233160f1437be6f5388b5c530ba68b054401fd739d8b304efd4e33b117` both.
23. `dry-test_claude_cli_resume.py` → `tests/orchestration/test_claude_cli_resume.py`: cmp equal, sha256 `c1d7c2c360f8cc7e23bb145b1b940ca70b9c16254add70c442840975dd80891a` both.
24. `dry-test_job_stop_integration.py` → `tests/orchestration/test_job_stop_integration.py`: cmp equal, sha256 `d13aa4f2ada3fdf0845d88a3ae34e42fda276f7694f0a1b108bd3f15618abda3` both.

The three `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`, `append-prose_slips.txt`) were listed in the Bundle and digest-checked (all `OK`), but C1 orders copying the four whole `dry-*.md` files, which already carry that content baked in; the `append-*.txt` files were not applied separately, and nothing in the block calls for that.

## Deviations & assumptions

1. **"Operator questions open" count in `## Next`.** The block's C8 instructions order the `## Next` section to state literally `"Operator questions open: 2"`. Checked against disk: `.agent/operator_questions.md` reads `EMPTY — nothing is waiting on the operator.` (10 lines, no `## Q` heading), because DECISION F297 D2 — already present in this round's own base commit `0a5acfc08`, which the block's own preamble describes as "the operator's answers to Q11 and Q12" — answered and deleted both entries before this round began. Writing the literal "2" into a durable handback would state something false that the block's own preamble already contradicts. This handback's `## Next` states the verified count, `0`, instead of the block's literal text. Nothing on disk is wrong; this is a stale digit in the block's authored prose of the kind `.agent/prose_slips.md` exists to record (a worker-declared wording contradiction), not a defect this round introduced, and not treated as a guardrail-G8 stop because no gate, digest or numstat was involved.
2. **`git add -A -- <paths>`.** Each commit's staging used `git add -A -- <explicit path list>` rather than naming the paths without `-A`. The pathspec restricted staging to exactly the named files in every case (confirmed by the `git diff --cached --numstat` readings quoted above), so no unintended file was staged; AGENTS.md's caution is against `git add -A` or `git add .` with no restricting pathspec, which this is not, but the literal flag was present and is noted for completeness (same note as F297 round 1's handback).
3. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`, `wc -l`, `sha256sum`, the ruff and pytest-wrapper invocations) were run as `cd /home/decodeux/Repos/remedy && <one command>` rather than `git -C ... <command>` as the top-level task instructions prefer; none were refused by the sandbox. All copy/hash steps needing more than one operation used the mandated python3 scripts under `.remedy-wt/f297-r2-worker/` (same note as F297 round 1's handback).
4. **C4's "no behaviour change" claim.** The block states C4 "changes no behaviour" and that "the reviewer runs its tests on the commit itself" — read as a note about the reviewer's own dry-run verification, not an instruction for this worker to run tests between C4 and C5; the block's gates run once, after C7. No test command ran between C4 and C5; the behaviour-preservation claim was instead checked by reading the staged diff in full (a verbatim extraction, confirmed above).

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file written outside the paths each commit names; no write under `.remedy-wt/f297-r2/`; no pull request opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 2's verdict and the resolutions of R-1143, R-1176, R-1196, R-1138 and R-1162 in the next round's first commit.
5. T010 to T014: R-1237, R-1239, R-1238, R-1247 and R-1250.

Operator questions open: 0.
Open findings: 26, all owned by F297 except R-1248, owned by F305.

## For the operator, in plain sentences

This round first wrote last time's results permanently into the project's record. It then made five small repairs to parts of the system that read run history, watch background jobs for ones that have already finished, answer certain operator decisions, describe a round where nothing changed, and remember which automated model answered a call when none was chosen. Before the decision repair, the code it touches was tidied into a smaller piece without changing what it does, so a separate rule about keeping pieces of code small stays satisfied. Every one of the five repairs is backed by a test that fails without it and passes with it. This round's own results will be written permanently into the record at the start of next time's work, which will then take on five more items from the remaining list. Nothing is waiting on you right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 1, resolutions of R-1172/R-1243/R-1242, DECISION F297 D3; numstat matched exactly |
| C2 | done | T005 (R-1143) landed; numstat and diff content matched exactly |
| C3 | done | T006 (R-1176) landed; numstat and diff content matched exactly |
| C4 | done | structural step for T007 (R-1196); no behaviour change; numstat matched exactly |
| C5 | done | T007 (R-1196) landed; numstat and diff content matched exactly |
| C6 | done | T008 (R-1138) landed; numstat and diff content matched exactly |
| C7 | done | T009 (R-1162) landed; numstat and diff content matched exactly |
| C8 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `7309 passed, 6 skipped`, exit 0, identical to the dry tree |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 26 ids, exact order |
| Gate 6 | passed | seven subjects, newest first |
| T005 (R-1143) | done | `load_run_events` skips a non-object JSON line and sorts timestamps as text |
| T006 (R-1176) | done | `reconcile_open_runs` skips a record whose `ended_at` is set |
| T007 (R-1196) | done | stop-reason decision resolves its job before reading any file, after its structural step |
| T008 (R-1138) | done | a round whose builder changed no file is described as exactly that |
| T009 (R-1162) | done | a `claude-cli` call with no model set is fingerprinted under `CLAUDE_CLI_UNSET_MODEL` |
