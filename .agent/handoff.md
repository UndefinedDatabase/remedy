# Handoff — F273 Findings paydown v1 · Round 20

## Session

SESSION 3 of feature F273 · round 20 · rounds so far 20

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D20, the handback template, round 19's handoff as the template's instance and every hunk of the four diffs as it applied them, and held all of it without loss; every figure below comes from a command run in this round.

## Range

Review of fdece9ab..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 20 books round 19's verdict and fourteen resolutions, registers T015's three ids, lands DECISION F273 D20, and builds T015 as the reviewer's dry run built it.
- C1 books Gate F273 R19 (VERDICT PASS) and fourteen `Done:` lines (R-0831, R-0832, R-0850, R-0941, R-0867, R-0863, R-0884, R-0828, R-0826, R-0937, R-0851, R-0852, R-0856, R-0860); registers R-0994, R-0995 and R-0996; lands DECISION F273 D20; rewrites the plan; saves the four payload copies.
- C2 (R-0994): `ClaudeProvider._call` returns the CLI provider's shape with the SDK usage in `usage_actuals`; `ComposedPrompt.stable_prefix()` and the loop's `_offer_stable_prefix` let the direct-API provider send the prefix as a cached `system` block; failures map most-specific-first to a kind with HTTP status and a redacted, capped message; `pyproject.toml` gains the `anthropic` extra.
- C3 (R-0995): `tests/orchestration/test_ci_stage_coverage.py` collects the suite once and asserts every node is selected by a CI stage or by the stage CI deliberately excludes; it runs in the `budgets` stage, whose re-measured maximum (24.40 s) still yields a 300 s budget.
- C4 (R-0996): the vitest test's docstring records three measured runs (1.01 s to 1.09 s), the machine and the rule; the 30 s ceiling stays.
- C5: T015 in `docs/roadmap/features/T2_F273.md` records its ids and D20's narrowing of item (b).
- C6 is this handoff.

Landed: R-0994 — `e6ddf73d` (C2)
Landed: R-0995 — `a22e805f` (C3)
Landed: R-0996 — `7dba86b9` (C4)

## Commits

### 8a591882 F273 R20 C1: bookkeeping — round 19's verdict and fourteen resolutions booked, T015's ids R-0994, R-0995 and R-0996 registered, DECISION F273 D20 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r20-block.md` | +116 / -0 | Byte copy of the block |
| `.agent/authored/f273-r20-decisions.md` | +26 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r20-ledger.md` | +36 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r20-plan.md` | +31 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +26 / -0 | `fdece9ab` bytes + decisions.md (DECISION F273 D20) |
| `.agent/live_review.md` | +36 / -0 | `fdece9ab` bytes + ledger.md (Gate F273 R19, fourteen `Done:` lines, R-0994 to R-0996) |
| `.agent/plan.md` | +15 / -14 | := plan.md |

286 insertions, 14 deletions (`git show --numstat`).

### e6ddf73d F273 R20 C2: R-0994 — the direct-API provider returns its usage through usage_actuals, sends the stable prefix as a cached system block, maps failures to a kind with status and message, and pyproject names an anthropic extra
All by `git apply .remedy-wt/f273-proto-g10a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +18 / -0 | `_offer_stable_prefix` before each builder and reviewer call |
| `packages/orchestration/pingpong_provider.py` | +130 / -19 | Usage via `usage_actuals`, cached `system` prefix, error chain |
| `packages/orchestration/prompt_segments.py` | +17 / -0 | `ComposedPrompt.stable_prefix()` |
| `pyproject.toml` | +1 / -0 | `anthropic` extra |
| `tests/orchestration/test_pingpong_provider_claude_api.py` | +264 / -0 | New: usage, prefix, error kinds, extra |

430 insertions, 19 deletions.

### a22e805f F273 R20 C3: R-0995 — one guard collects the suite once and proves every collected test is selected by a CI stage or by the stage CI deliberately excludes, run in the budgets stage whose re-measured budget still yields 300 s
All by `git apply .remedy-wt/f273-proto-g10b.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/ci_stages.py` | +1 / -0 | The guard joins the `budgets` stage |
| `tests/orchestration/test_ci_stage_coverage.py` | +84 / -0 | New: the coverage guard |
| `tests/orchestration/test_ci_stages.py` | +5 / -3 | `budgets` re-measured at 24.40 s |

90 insertions, 3 deletions.

### 7dba86b9 F273 R20 C4: R-0996 — the vitest ceiling of 30 s is measured, three runs of 1.01 s to 1.09 s, and the test's docstring records the numbers, the machine and the rule
All by `git apply .remedy-wt/f273-proto-g10c2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_test_runner.py` | +14 / -1 | Docstring records the measurement |

14 insertions, 1 deletion.

### d6690f9e F273 R20 C5: T015 records its ids R-0994, R-0995 and R-0996 and DECISION F273 D20's narrowing of its item (b) to coverage
All by `git apply .remedy-wt/f273-s3/r20_docs.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F273.md` | +5 / -0 | T015 names its ids and D20's narrowing |

5 insertions, 0 deletions.

### C6 (this commit) F273 R20 C6: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C2, with 430.

## External actions

- `git worktree add --detach .remedy-wt/f273-r20-g5 d6690f9e` for G5, then `git worktree remove --force .remedy-wt/f273-r20-g5` as the step's last action (exit 0; the tree's `git status --porcelain` read `''` after the reverts). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                         d6690f9e [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-s3-r20  9e6bb7b9 (detached HEAD)
  ```
  `.remedy-wt/f273-s3-r20` is the reviewer's; the worker did not touch it.
- The branch `remedy/job-81ec65896729405c` still exists in this repository. A research helper's probe created it before round 16; nobody may delete it without the operator. `git branch --list 'remedy/job-*'` reads 37 branches after the gates.
- After C6: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C5 `d6690f9e` with a clean tree. Every script ran with an explicit `cwd`; a gate's exit code is the process's own (the tool reports a non-zero exit as an error, and none was reported).

- **Transport**, before any write: `sha256sum` of the block, the five payloads and the four diffs each equalled the block's digest; the block file read 116 lines.
- **Block copy**, before C1: `.remedy-wt/f273-r20/wk_c1.py`:
  ```
  saved block sha256 52a3c1556223bd7bfbd989cc32a2712705702ff9ffcbf22d10fd499f45af4eb9
  saved block lines 116
  ```
  Both equal the given block's digest and line count.
- **G1 and G2**: `python3 .remedy-wt/f273-r20/wk_g1g2.py`, exit 0:
  ```
  G1 transport
  digest .remedy-wt/f273-r20/plan.md True
  digest .remedy-wt/f273-r20/ledger.md True
  digest .remedy-wt/f273-r20/decisions.md True
  digest .remedy-wt/f273-r20/next.md True
  digest .remedy-wt/f273-r20/block.md True
  digest .remedy-wt/f273-s3/r20_targets.txt True
  digest .remedy-wt/f273-proto-g10a.diff True
  digest .remedy-wt/f273-proto-g10b.diff True
  digest .remedy-wt/f273-proto-g10c2.diff True
  digest .remedy-wt/f273-s3/r20_docs.diff True
  plan.md equals payload True
  live_review.md equals base + ledger True
  decisions.md equals base + decisions True
  authored f273-r20-plan.md equals payload True
  authored f273-r20-ledger.md equals payload True
  authored f273-r20-decisions.md equals payload True
  authored f273-r20-block.md equals payload True
  C2 e6ddf73d paths equal True ['packages/orchestration/pingpong_loop.py', 'packages/orchestration/pingpong_provider.py', 'packages/orchestration/prompt_segments.py', 'pyproject.toml', 'tests/orchestration/test_pingpong_provider_claude_api.py']
  C3 a22e805f paths equal True ['packages/orchestration/ci_stages.py', 'tests/orchestration/test_ci_stage_coverage.py', 'tests/orchestration/test_ci_stages.py']
  C4 7dba86b9 paths equal True ['tests/orchestration/test_test_runner.py']
  C5 d6690f9e paths equal True ['docs/roadmap/features/T2_F273.md']
  G2 code transport
  6f36fc30471e00a9386dfae2ae930066bf5b2513 tests True
  d11bd01647593af33f1184ce7978e6846e6b76e8 packages True
  39a6be279a37193ae0ebcf00d97cadb542da960f apps True
  84b927c29a16a08a98ab396bc690011037d89d01 docs True
  866c1b06bafcedd6f4cca87b588dccae60d37531 scripts True
  ef1bd103cd0c13235a1e8dfd3cc4c40734d3da62 pyproject.toml True
  ```
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r20/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over the lines of `r20_targets.txt`, `env=` without `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST`:
  ```
  targets 108
  3892 passed in 779.10s (0:12:59)
  R-0803 lines 0
  exit 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root, exit 0:
  ```
  All checks passed!
  ```
- **G5** (`python3 .remedy-wt/f273-r20/wk_g5.py`, exit 0): one detached worktree at `d6690f9e`; `python3 -B -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM counted as a whole line with its newline; each file reverted from its saved bytes.
  ```
  import path /home/decodeux/Repos/remedy/.remedy-wt/f273-r20-g5/packages/orchestration/pingpong_provider.py
  CONTROL exit 0 | 50 passed in 20.82s
  (a) packages/orchestration/pingpong_provider.py FROM count 1
    exit 1 | 1 failed, 23 passed in 0.63s | failed ids 1
      tests/orchestration/test_pingpong_provider_claude_api.py::TestTheStablePrefixIsACachedSystemBlock::test_an_offered_prefix_is_sent_as_a_cached_system_block
    reverted True
  (b) packages/orchestration/pingpong_provider.py FROM count 1
    exit 1 | 10 failed, 14 passed in 0.66s | failed ids 10
      ...::TestEachFailureKeepsItsKindStatusAndMessage::test_a_status_error_maps_to_its_kind_and_keeps_the_status[AuthenticationError-401-authentication_failed]
      ...::TestEachFailureKeepsItsKindStatusAndMessage::test_a_status_error_maps_to_its_kind_and_keeps_the_status[PermissionDeniedError-403-permission_denied]
      ...::TestEachFailureKeepsItsKindStatusAndMessage::test_a_status_error_maps_to_its_kind_and_keeps_the_status[NotFoundError-404-not_found]
      ...::TestEachFailureKeepsItsKindStatusAndMessage::test_a_status_error_maps_to_its_kind_and_keeps_the_status[RateLimitError-429-rate_limited]
      ...::TestEachFailureKeepsItsKindStatusAndMessage::test_a_status_error_maps_to_its_kind_and_keeps_the_status[BadRequestError-400-bad_request]
      ...::TestEachFailureKeepsItsKindStatusAndMessage::test_a_status_error_maps_to_its_kind_and_keeps_the_status[InternalServerError-500-server_error]
    reverted True
  (c) packages/orchestration/pingpong_provider.py FROM count 1
    exit 1 | 2 failed, 22 passed in 0.64s | failed ids 2
      tests/orchestration/test_pingpong_provider_claude_api.py::TestTheSdkUsageIsRecorded::test_build_records_all_four_usage_fields
      tests/orchestration/test_pingpong_provider_claude_api.py::TestTheSdkUsageIsRecorded::test_review_records_all_four_usage_fields
    reverted True
  (d) packages/orchestration/prompt_segments.py FROM count 1
    exit 1 | 2 failed, 47 passed in 0.74s | failed ids 2
      tests/orchestration/test_pingpong_provider_claude_api.py::TestTheStablePrefixIsACachedSystemBlock::test_the_composed_stable_prefix_ends_before_the_first_task_segment
      tests/orchestration/test_pingpong_provider_claude_api.py::TestTheStablePrefixIsACachedSystemBlock::test_a_prompt_that_opens_with_its_task_has_no_stable_prefix
    reverted True
  (e) tests/orchestration/test_ci_stage_coverage.py FROM count 1
    exit 1 | 1 failed in 20.30s | failed ids 1
      tests/orchestration/test_ci_stage_coverage.py::test_every_collected_test_is_selected_by_a_stage
    reverted True
  status after reverts: ''
  ```
  In (b) the `...` stands for `tests/orchestration/test_pingpong_provider_claude_api.py`; the first six of ten ids are shown, as the block allows. Every mutation went red in the file the block names; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit comes before it.
- Full suite: not run in this round (the integration-gate round follows).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r20/wk_c1.py` from `git show fdece9ab:<path>` bytes and the payload bytes, with no hand edit. G1 re-proves every C1 file and every `.agent/authored/f273-r20-*` copy against its payload.
- The code and docs arrived only by `git apply` of the four reviewer-verified diffs, in the block's order; before each commit `git status --porcelain` listed exactly the paths the apply touched, all staged (the new test files included), and nothing untracked. G1 proves each commit's path set equals its diff's; G2's object ids equal the reviewer's dry-run objects.
- The `## Next` body below is `next.md` byte for byte, appended by `.remedy-wt/f273-r20/wk_c6.py`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping (Gate F273 R19, fourteen `Done:` lines, R-0994 to R-0996 registered, D20) | done | `8a591882` |
| R-0994 | done | `e6ddf73d` (C2) |
| R-0995 | done | `a22e805f` (C3) |
| R-0996 | done | `7dba86b9` (C4) |
| C5 T015 records its ids | done | `d6690f9e` |
| G1 to G5 | done | All green / red-proofs red as above |
| C6 handoff + push | done | This commit, then the push |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r20/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registers it in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `8a591882` (C1 onwards; C2 to C5 do not touch it; the same at `d6690f9e`): **16 open**;
- at `fdece9ab`: 27 open.

C1's fourteen `Done:` lines close fourteen distinct ids and its three registrations open three: 27 - 14 + 3 = 16. The three ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C6, then the push. No extra commit.
- **An attempted `$?`:** one Bash call tried `echo "exit=$?"` after the G1/G2 script; the shell refused the call before anything ran, and the script was then run alone. Its exit code is the process's own, and the tool reported no error.
- **G5 worktree removal:** `worktree remove` was given `--force` as a precaution against ignored bytecode; the tree's `git status --porcelain` was empty beforehand, so nothing tracked was discarded. Made with `--detach`, so no branch was created.
- **G5 runs:** pytest ran as `python3 -B -m pytest` so that no bytecode is written between the purges; the control ran A, P and V together (50 passed); each mutation ran only the files the block names for it.
- **Payload copies:** the four files the block names for C1 went to `.agent/authored/` as `f273-r20-<name>`. `next.md` is not copied; it lives in this handoff's `## Next`.
- **Operator questions:** the count below is the number of `### Q<n>` headings in `.agent/operator_questions.md` (Q1, Q2, Q4, Q5, Q7), unchanged this round.
- **Scratch:** gitignored under `.remedy-wt/f273-r20/`: `wk_c1.py`, `wk_g1g2.py`, `wk_g3.py`, `wk_g5.py`, `wk_count.py`, `wk_c6.py`, `handoff_head.md`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 20 over `fdece9ab`..the round 20
   handoff commit, booked as `Gate: F273 R20` with `Done:` lines for R-0994, R-0995 and R-0996 in
   the next round's first commit.
2. The integration-gate round (the Built State and the one full suite), then closure rounds A and B
   of `docs/roadmap/STATUS_closure_protocol.md`.

Operator questions open: 5
