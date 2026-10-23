# Handback — F315 "The loop runs through the adapter," round 3

## Session

SESSION 1 of feature F315 · round 3 · rounds so far 3. Context self-assessment: this session
continued directly from round 2's handback, landed T003 in full (the usage of a call that is not
streamed from the installed adapter, the re-export's deletion, the docs), and carries no backlog
into the closure sequence.

**Fortschritt:** ~75 % (T001 ✅ · T002 ✅ · T003 landed · closure open) — Schätzung.

## Range

Review of `30cd588dc`..`f4c485787`.

## Commits

### 3ee6fab75 F315 R3 C1: book round 2, DECISION F315 D3, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r3.md` | +101/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/decisions.md` | +10/-0 | DECISION F315 D3: usage of a call that is not streamed comes from the installed adapter; the stream and error classes stay with the loop's evidence; the re-export is deleted |
| `.agent/live_review.md` | +2/-0 | books round 2's VERDICT PASS |
| `.agent/plan.md` | +7/-10 | rewritten for round 3's current step (T003, DECISION F315 D3) and the next steps (the closure sequence) |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### 916284f4f F315 R3 C2: delete the command-line builder re-export and point its readers at its module
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +1/-1 | ratchet row for `pingpong_provider.py` falls 1573→1572 |
| `packages/orchestration/pingpong_provider.py` | +2/-3 | the `build_claude_cli_args` re-export and its `noqa: F401` are deleted; the import comment is rewritten |
| `packages/providers/claude_planner/provider.py` | +2/-1 | imports `build_claude_cli_args` directly from `claude_cli_command.py` instead of through the provider module |
| `tests/orchestration/test_claude_cli_resume.py` | +1/-2 | same re-point |
| `tests/orchestration/test_pingpong_cli.py` | +1/-1 | same re-point |
| `tests/orchestration/test_provider_mode.py` | +2/-2 | both of this file's `build_claude_cli_args` imports re-pointed |
| `tests/orchestration/test_stream_evidence_integration.py` | +1/-1 | same re-point |
| `tests/orchestration/test_structured_outputs.py` | +1/-1 | same re-point |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 63050→63049, matching the shrink |

All nine paths are byte copies of the reviewer's prepared `c2-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### a800b48f6 F315 R3 C3: the usage of a call that is not streamed comes from the installed adapter
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +1/-1 | ratchet row for `pingpong_provider.py` falls 1572→1570 |
| `packages/orchestration/pingpong_provider.py` | +4/-6 | `_call` reads a non-streamed call's actuals and reason through `adapter_usage_actuals`; the direct `parse_cli_result_detailed` import is dropped |
| `packages/orchestration/worker_adapter_slot.py` | +12/-0 | `adapter_usage_actuals(adapter_ref, raw, **settings)` added: the installed adapter's mapped actuals with `"ok"`, or the reason `parse_cli_result_detailed` gives when the adapter maps none |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 63049→63047, matching the shrink |

All four paths are byte copies of the reviewer's prepared `c3-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### f693ae35c F315 R3 C4: the usage tests of the slot
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_worker_adapter_slot.py` | +45/-0 | tests `adapter_usage_actuals` for a mapped call and for each of the four reasons (`is_error`, `usage_missing`, `parse_failed`, `empty_input`), and replaces the installed adapter with one whose `map_usage` changes the counts, proving the provider's usage follows it |

Byte copy of the reviewer's prepared `c4-*` file; gate 1's `verify.py` confirms the equality.

### f4c485787 F315 R3 C5: the docs page, the two docstrings and the worker note
| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v2.md` | +14/-3 | status banner updated for F315 T003; new paragraph states `adapter_usage_actuals` and names the two absences (the stream capture, the failure post-mortem) that stay with the loop |
| `packages/orchestration/worker_adapter_slot.py` | +1/-1 | module docstring extended to name the usage mapping (DECISION F315 D3) |
| `packages/orchestration/worker_adapters.py` | +2/-2 | the claude-cli spec's note now says the adapter maps the usage of every call that is not streamed |
| `packages/providers/adapters/claude_cli_reference.py` | +2/-1 | module docstring updated: the loop takes the command line and the non-streamed usage from the adapter (DECISIONs F315 D2 and D3) |

All four paths are byte copies of the reviewer's prepared `c5-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `3ee6fab75`, four paths, byte-equal to prepared files |
| C2 | done | `916284f4f`, nine paths, byte-equal to prepared files |
| C3 | done | `a800b48f6`, four paths, byte-equal to prepared files |
| C4 | done | `f693ae35c`, one new test file, byte-equal to prepared file |
| C5 | done | `f4c485787`, four paths, byte-equal to prepared files |
| Gate 1 | done | `verify.py` exit 0, every line `True` (`C6` read `absent` as expected before this commit), `ALL True` |
| Gate 2 | done | selection + every `tests/test_*.py`, exit 0, `4878 passed, 2 skipped` |
| Gate 3 | done | `ruff check .`, `All checks passed!` |
| Gate 4 | done | `integrity check --json`, `fail_count` 0 |
| Gate 5 | done | open finding ids: `11` |
| C6 | done | this file |
| Push | done | see External actions |

## External actions

- `git push origin feature/f315-loop-through-adapter` — run after this handback's own commit,
  carrying `3ee6fab75`, `916284f4f`, `a800b48f6`, `f693ae35c`, `f4c485787` and the handback commit
  itself; see the reply for the push's own result.
- No pull request opened (the block orders none).
- No worktree created or removed; one scratch directory was used,
  `.remedy-wt/f315-r3-worker/`, holding only python helper scripts and gate output, never written
  under `.remedy-wt/f315-r3/` (the reviewer's prepared tree, left untouched).

## Verification

Gate order per the block: run once each, after C5 and before C6.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f315-r3/prep/verify.py .` → exit 0. Every line `True`, including each
   commit's single-parent and insertions-under-500 check, the subject check (`5 of 5`), the branch
   check, each commit's path-set-exactly check and every per-path byte-equality check against the
   prepared `c<n>-*` files, `C6` → `absent` (as the block states, before this commit exists), `the
   saved block equals block.md` `True`, final line `ALL True`.
2. `python3 .remedy-wt/f315-r3/prep/run_selection.py . .remedy-wt/f315-r3-worker/selection-output.txt`
   → exit 0. `paths 111`, `4878 passed, 2 skipped in 52.04s`. No `FAILED`, no `ERROR`, no
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

`.agent/authored/f315-r3.md` (this round's committed copy of the block) against
`.remedy-wt/f315-r3/prep/block.md`: `wc -l` 101 on both; sha256
`9f9bfda05aa880d621c5d2a7519144868d87260cf09577725dadc6b4830a536b` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f315-r3/prep/digests.txt` was checked against its own
stated sha256 (`ebfb76023c747592d88ff47877b88deeb99fcbd7fcae13e549ce18635ba7413b`, matched), then
every one of its twenty-five listed entries was recomputed and matched (`ALL_FILES_OK`), before any
prepared file was copied or read for C1 through C5.

## Deviations & assumptions

- No deviation from the block's ordered commit sequence (C1, C2, C3, C4, C5, gates 1–5, C6, push);
  nothing was added, dropped or reordered. Every `c<n>-*` prepared byte was copied verbatim and
  proved equal by a direct comparison before being added to the index.
- `LAST_REVIEWED_SHA` in the Range line above is taken as `30cd588dc`, round 2's handback commit,
  the base this round's block names.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Phase 1 rule 2: the next session runs the Open PR Gate before opening any new branch.
3. Round 3's verdict gets booked into the next round's first commit, once a reviewer has read this
   handback.
4. The closure sequence: the integration gate round with the one full suite.

Operator questions open: 0. Open findings (gate 5): 11.

For the person reading this and not the next worker: this round took the second piece of a
claude-cli call's answer, the usage it reports, from the same replaceable piece that already
builds what goes out, for every call that is not streamed. The loop itself still watches a
streamed call while it runs and still decides what a failure means, because those two pieces
belong with the evidence the loop already keeps, not with the piece that only talks to the
assistant. A leftover shortcut that let five other files reach that piece through the wrong door
was removed, and each of those files now goes through the door that was always meant for it. The
round's own selection of tests ran, a subset chosen to match what this round touched, not the
whole collection.
