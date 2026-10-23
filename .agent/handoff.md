# Handback — F315 "The loop runs through the adapter," round 2

## Session

SESSION 1 of feature F315 · round 2 · rounds so far 2. Context self-assessment: this session
continued directly from round 1's handback, landed T002 in full (the slot, the wiring, the
provider's three call sites, the ratchet and the proof test), and carries no backlog into round 3.

**Fortschritt:** ~50 % (T001 ✅ · T002 landed · T003 open) — Schätzung.

## Range

Review of `052edbf10`..`828521d0b`.

## Commits

### eb95f8d77 F315 R2 C1: book round 1, DECISION F315 D2, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r2.md` | +96/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/decisions.md` | +10/-0 | DECISION F315 D2: the worker adapter slot and the provider's three call sites |
| `.agent/live_review.md` | +2/-0 | books round 1's VERDICT PASS |
| `.agent/plan.md` | +9/-8 | rewritten for round 2's current step and next steps |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### 4dcf75c07 F315 R2 C2: the worker adapter slot, filled by the command line, builds every claude-cli command line
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/grouped.py` | +4/-0 | `main` installs `WORKER_ADAPTERS_BY_REF` into the slot before any command parses |
| `docs/system/structure-ledger-v1.md` | +2/-2 | ratchet rows for `_call_reviewer_structured` (133→130) and the file total (1574→1573) |
| `packages/orchestration/pingpong_provider.py` | +21/-22 | `_adapter_argv` helper; `_call`, `_call_streamed` and the reviewer's non-streamed branch ask the slot; `role` plumbed to each |
| `packages/orchestration/worker_adapter_slot.py` | +58/-0 | NEW FILE; `install_worker_adapters`, `installed_worker_adapter`, `adapter_cli_argv`, `WorkerAdapterNotInstalled` |
| `tests/conftest.py` | +5/-0 | `pytest_configure` installs the same registry once per test process |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | the new slot module joins the allowlist |
| `tests/test_structure_ratchet.py` | +2/-2 | `MAX_FUNCTION_LINES` 28516→28513, `MAX_FILE_LINES` 63051→63050, matching the shrink |

All seven paths are byte copies of the reviewer's prepared `c2-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### 7ae963322 F315 R2 C3: the slot's tests and the loop that follows the installed adapter
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_worker_adapter_slot.py` | +217/-0 | NEW FILE; replaces the installed adapter and proves the provider's builder/reviewer, streamed/non-streamed and a whole `run_pingpong` all take their command line from it, plus the empty-slot error and the argv-equals-`build_claude_cli_args` property |

Byte copy of the reviewer's prepared `c3-*` file; gate 1's `verify.py` confirms the equality.

### 828521d0b F315 R2 C4: the docs page, the adapter docstring and the worker note
| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v2.md` | +17/-2 | new "The worker adapter slot" section; status banner updated for F315 T002 |
| `packages/orchestration/worker_adapters.py` | +2/-2 | the claude-cli spec's note no longer says the loop calls the CLI provider directly |
| `packages/providers/adapters/claude_cli_reference.py` | +4/-4 | module docstring updated: the loop now takes the command line from the slot (DECISION F315 D2), not direct calls |

All three paths are byte copies of the reviewer's prepared `c4-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `eb95f8d77`, four paths, byte-equal to prepared files |
| C2 | done | `4dcf75c07`, seven paths, byte-equal to prepared files |
| C3 | done | `7ae963322`, one new test file, byte-equal to prepared file |
| C4 | done | `828521d0b`, three paths, byte-equal to prepared files |
| Gate 1 | done | `verify.py` exit 0, every line `True` (C5 read `absent` as expected before this commit), `ALL True` |
| Gate 2 | done | selection + every `tests/test_*.py`, exit 0, `4872 passed, 2 skipped` |
| Gate 3 | done | `ruff check .`, `All checks passed!` |
| Gate 4 | done | `integrity check --json`, `fail_count` 0 |
| Gate 5 | done | open finding ids: `11` |
| C5 | done | this file |
| Push | done | see External actions |

## External actions

- `git push origin feature/f315-loop-through-adapter` — run after this handback's own commit,
  carrying `eb95f8d77`, `4dcf75c07`, `7ae963322`, `828521d0b` and the handback commit itself; see
  the reply for the push's own result.
- No pull request opened (the block orders none).
- No worktree created or removed; one scratch directory was used,
  `.remedy-wt/f315-r2-worker/`, holding only python helper scripts and gate output, never written
  under `.remedy-wt/f315-r2/` (the reviewer's prepared tree, left untouched).

## Verification

Gate order per the block: run once each, after C4 and before C5.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f315-r2/prep/verify.py .` → exit 0. Every line `True`, including each
   commit's single-parent and insertions-under-500 check, the subject check (`4 of 4`), the branch
   check, each commit's path-set-exactly check and every per-path byte-equality check against the
   prepared `c<n>-*` files, `C5` → `absent` (as the block states, before this commit exists), `the
   saved block equals block.md` `True`, final line `ALL True`.
2. `python3 .remedy-wt/f315-r2/prep/run_selection.py . .remedy-wt/f315-r2-worker/selection-output.txt`
   → exit 0. `paths 111`, `4872 passed, 2 skipped in 51.22s`. No `FAILED`, no `ERROR`, no
   `process(es) behind` anywhere in the output. The two skips, reported as the block asks:
   `tests/test_agent_tooling.py:43` (D12 quarantine, pre-existing, unrelated to this round) and
   `tests/test_install_smoke.py:175` (opt-in, needs network).
3. `python3 -m ruff check .` → exit 0, `All checks passed!`.
4. `python3 -m apps.cli.main integrity check --json` → exit 0,
   `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}`, every one of the
   six named checks `"status": "pass"`.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → exit 0, printed `11`, matching the block's required value.

## Authored-text proofs

`.agent/authored/f315-r2.md` (this round's committed copy of the block) against
`.remedy-wt/f315-r2/prep/block.md`: `wc -l` 96 on both; sha256
`0a505fe2ccb08fed887da5e2c6c385e199d61bfeb159fdd7976082e43b995abd` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f315-r2/prep/digests.txt` was checked against its own
stated sha256 (`d5872957f18be80f948b22e0694935e3dea25877ff327ea5368909be361b5b18`, matched), then
every one of its nineteen listed entries was recomputed and matched (`ALL_MATCH: True`), before any
prepared file was copied or read for C1 through C4.

## Deviations & assumptions

- No deviation from the block's ordered commit sequence (C1, C2, C3, C4, gates 1–5, C5, push);
  nothing was added, dropped or reordered. Every `c<n>-*` prepared byte was copied verbatim and
  proved equal by a direct comparison before being added to the index.
- `LAST_REVIEWED_SHA` in the Range line above is taken as `052edbf10`, round 1's handback commit,
  the base this round's block names.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Phase 1 rule 2: the next session runs the Open PR Gate before opening any new branch.
3. Round 2's verdict gets booked into the next round's first commit, once a reviewer has read this
   handback.
4. T003: usage and error mapping through the adapter, the re-export's readers re-pointed, the docs.

Operator questions open: 0. Open findings (gate 5): 11.

For the person reading this and not the next worker: this round built the piece that lets a
different program stand in for the assistant the system calls today, without touching the part
that decides what to ask it or what to do with the answer. Every one of today's calls to that
assistant now goes out through one small, replaceable piece instead of being built in three
different places, and a new test file proves that swapping that piece changes what goes out.
Nothing about how answers are read back, or how errors are handled, has changed yet; that is next
round's work. The round's own selection of tests ran, a subset chosen to match what this round
touched, not the whole collection.
