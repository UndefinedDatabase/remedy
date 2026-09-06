# Handoff — amend0906-triage-throughput

Branch `feature/amend0906-triage-throughput`, cut from main at `b18fad57` (the fork
point, by `git merge-base`). Loop stopped: `pgrep -af 'build[-]remedy[-]self'` empty.
`.agent/STOP` present, untouched. Open PR Gate: `gh pr list --state open` → `[]`, so
F260's PR #242 was already merged and nothing was owed.

## A.4 — the open set, measured twice by the A.1 method

| reading | before (`b18fad57`) | after (HEAD) |
|---|---:|---:|
| canonical `count_open_findings` | 296 | 53 |
| distinct ids (set difference) | 298 | 55 |

fixed 39 · deletion-bound 1 (R-0767 → F261) · process-only 204 · product 54 (= F273).

The readings differ by 2 at both ends and always will: `R-0721` and `R-0725` each
carry two `Done:` lines, so the LINE formula subtracts them twice. R-0778 registers
that; `rotate_live_review.py`'s docstring anticipates it. 55 after = 54 + R-0767.

## Commits

`e0fc5c6b` triage table, before any resolution line · `d0a708db` 243 resolutions in
the ledger (39 fixed, 204 process-only) · `0682f6b7` eight process-only classes in
prose_slips · `6edd14fd` R-0767 tagged deletion-bound, with the F272 T005 and F261
T003 sentences · `624a183b` F273 registered with its pins and the product routing
lines · `fc64df5f` the protocol paragraph and DECISION amend0906-triage-throughput.
Commit 2 was first written at 504 insertions, over the AGENTS.md cap and not exempt
(two files), so it was split into 2 and 3 before anything was pushed.

## Gates

- `grep -c 'amend0906-triage-throughput' docs/agents/self_drive_protocol.md` → 1
- F273 present once, directly after F271 (STATUS.md:39-40)
- `pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q` → 333 passed
- four state-file contract readers → 154 passed; canary → 42 passed
- `rotate_live_review.py --dry-run` round-trips, open 53 both sides; 244 pairs now
  rotatable (next rotation: ledger 1.05 MB → 0.33 MB)
- `git diff --check` clean; no force-push anywhere

## Deviations

1. A resolution is written `Done: R-XXXX — RESOLVED 2026-09-06 (triage amend0906): …`.
   The order gave the `RESOLVED …` wording but not the `Done:` prefix, and without it
   the canonical function cannot see the resolution, so A.4's "open after" would not
   move. The order's wording is the line's content.
2. Two readings the order left open are settled in the DECISION rather than assumed:
   `fixed` is scoped to durable artifacts (a round-local `.agent/` file is rewritten
   every round and would trivially qualify), and the process-only line is the review
   process's own artifacts: a feature file and `integration_gate.md` are product.
3. F272's `Findings carried: R-0816 (open, owned here)` was corrected in commit 4:
   the triage resolved R-0816, and running the shipped `timeline.append_run_event`
   for five events of one job in one process writes ONE file under ONE `run_id`.

## Next

Push, PR, merge on green hosted CI, verify main, then Part C: merge `origin/main`
into `feature/f272-one-world-completion` with `--no-ff`, keeping BOTH sides of every
append-only conflict, main's block first. F272 IS claimed on that branch, so Part C
is not skipped.
