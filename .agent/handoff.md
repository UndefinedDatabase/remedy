# Handoff — F157 round 4

## Session

SESSION 2 of feature F157 · round 4 · rounds so far 4. This round booked round 3's verdict and
R-1452's repair, landed DECISION F157 D4, added `reviewer_schema_route` and `parked_resume_route`
beside the existing stream route, renamed `routed_stream_evidence` to `routed_claude_cli_build` so
one line now carries a build's whole set of decisions, and routed the claude-cli provider's own
reviewer-schema and resume readings through it — exactly as the block ordered, with every gate
green on its first run.

Fortschritt: ~65 % (T001 and T002 landed · T003: three routes landed, the report, the
command-line line and the end-to-end open) — Schätzung.

## Range

Review of `69e4b321b`..`35dd16c6b`.

## Commits

### 7796e0ef1 F157 R4 C1: book round 3, R-1451 resolved and R-1452, DECISION F157 D4, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r4.md` | +145/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | append DECISION F157 D4 |
| `.agent/live_review.md` | +7/-0 | book round 3's Gate verdict PASS and register R-1452 |
| `.agent/plan.md` | +5/-7 | rewritten: Current Step → round 4, Next Steps → D4 (1)/(2), the report line and the closure sequence |

### 17deb50bf F157 R4 C2: every decision of a claude-cli build recorded once, and the evidence line held by tests
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/capability_routes.py` | +54/-11 | adds `reviewer_schema_route`, `parked_resume_route`, `routed_reviewer_schema`, `routed_parked_resume`; renames `routed_stream_evidence` to `routed_claude_cli_build`, which now gathers every role's decisions and records one line only when something is not native (D4 (4)); the module docstring names the consumer guard (R-1452) |
| `packages/orchestration/role_provider_factory.py` | +2/-2 | one import and one call site renamed; `create_role_provider` unchanged otherwise, measured length still 98 lines |
| `tests/orchestration/test_capability_routes.py` | +107/-18 | the round-3 tests renamed onto `routed_claude_cli_build` and rewritten to D4 (4) (all-native writes nothing); new `_ResumeAndSchemaReducedAdapter` fixture; added tests for a reviewer build's two degraded decisions, a builder build carrying no `reviewer_schema_gate`, the append across two builds, a JSON-array line skipped (R-1452), and `routed_reviewer_schema`/`routed_parked_resume` under the registry and reduced adapters and the `REMEDY_REVIEWER_FREETEXT` switch |

### 35dd16c6b F157 R4 C3: the claude-cli provider asks the routes for its reviewer schema and its resume
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_provider.py` | +5/-5 | one import line for `routed_parked_resume`/`routed_reviewer_schema`; `ClaudeCliProvider.supports_resume` returns `routed_parked_resume(self._model)` behind one collapsed `# WHY:` line (net length unchanged by the import add); `review` and `_review_impl` read `routed_reviewer_schema(self._model)`; `ClaudeProvider.review`'s own `_reviewer_structured_enabled()` reading is untouched; file measured 1570 lines before and after |
| `tests/orchestration/test_capability_routes.py` | +44/-0 | `TestClaudeCliProviderRoutesResumeAndSchema`: `ClaudeCliProvider` built through `create_role_provider(..., with_failover=False)`; `supports_resume` true/false under the registry/reduced adapters; `resume_declined_reasons` names the reviewer for the reduced adapter; `review` prepares a `cli-native` input with the registry adapter and `cli-legacy` with the reduced one, `_review_impl` stubbed so no command runs |
| `docs/system/worker-adapter-contract-v2.md` | +16/-10 | the capability-matrix section's last paragraph rewritten with no round number: the three routes, that a route decides only a feature asked for, `routed_claude_cli_build` and what it records, that an all-native build writes nothing, the failover link's own line, the provider reading both new routes with the operator switch kept, and `read_capability_degradations` |

## External actions

`git push origin feature/f157-capability-matrix` — run once immediately after this commit; no PR
opened, per the block's constraint.

## Verification

1. `git -C <repo> status --porcelain` → empty.
   `python3 .remedy-wt/f157-r4/prep/verify.py .` → every line `True`; last line `ALL True`; the
   `C4` row read `absent` at the time this gate ran, before this commit existed.

2. `python3 .remedy-wt/f157-r4/prep/run_selection.py . .remedy-wt/f157-r4-worker/selection-output.txt`
   → `exit 0`; last pytest line `5706 passed, 2 skipped in 71.56s (0:01:11)`; no `FAILED`, no
   `ERROR`, no `process(es) behind` line anywhere in the output. The two `SKIPPED` lines: the
   pre-existing `test_install_smoke.py` (opt-in, needs network) and `test_agent_tooling.py` (a
   standing D12 quarantine). Run once, as the block's rule states.

3. `python3 -m ruff check packages/orchestration/capability_routes.py packages/orchestration/role_provider_factory.py packages/orchestration/pingpong_provider.py tests/orchestration/test_capability_routes.py`
   → `All checks passed!`, exit 0.

4. `python3 -m mypy packages/orchestration/capability_routes.py` → `Success: no issues found in 1
   source file`, exit 0.

5. `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, `"ok": true`, 6 of 6
   checks `pass`.
   An `ast`-based script under `.remedy-wt/f157-r4-worker/` printed `create_role_provider`'s length
   as `end_lineno - lineno + 1` → `98`, and `packages/orchestration/pingpong_provider.py`'s line
   count → `1570`.

6. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `9`.

## Authored-text proofs

`.agent/authored/f157-r4.md`, applied at C1, compared disk-to-disk against the committed prepared
file `c1-.agent__authored__f157-r4.md` (itself byte-equal to `block.md`): byte-equal, 145 lines,
sha256 `55ec1cb2b2d719c40bf542553fec7a5111ca8c839a629a961b1bebfdca31a5df` on both sides. The other
three C1 targets (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`) were each
compared disk-to-disk against their own prepared `c1-*` file before the commit and read byte-equal;
`verify.py`'s gate 1 re-confirms all four after the commit.

## Deviations & assumptions

None. Every commit landed as the block ordered — no split was needed (167, 163 and 65 insertions,
all under the 500-insertion cap) — and every gate passed on its first run.

For the operator: this round's own test run covered a selection chosen for it, not the full
collection the repository holds; that selection passed in full on its one run.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| R-1452 | done | repaired in C2 (`17deb50bf`): tests prove a line's role/provider/model, the append across two builds and a JSON-array line skipped; the module docstring now names the consumer guard |
| C3 | done | |
| C4 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Push | done | `git push origin feature/f157-capability-matrix` immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated.
3. Book round 4's verdict in the next round's first commit.
4. The report section, the run's `Degradations:` line and the reduced-capability end-to-end
   (DECISION F157 D3 (5) and (6)).
5. Operator questions open: 2.
6. Open findings count (gate 6): 9.
