# Handback — F151 round 1

## Session

SESSION 1 of feature F151 · round 1 · rounds so far 1.

Context self-assessment: every prepared file this round (`block.md` and the ten `c1-*`/other files
under `.remedy-wt/f151-r1/prep/`) was checked against `digests.txt`'s sha256 before use, and
`digests.txt`'s own sha256 was checked against the value given in the prompt, both with a `python3`
script under `.remedy-wt/f151-r1-worker/`; the whole block, `AGENTS.md`, `docs/agents/handback_template.md`
and the feature file were read in full before acting; T001's inventory was written by reading the named
modules directly at `4232c579e` and citing `path:line` for every factual sentence, never recalled; and
every gate reading below was produced by running the thing.

Fortschritt: ~15 % (T001 inventory landed · T002 and T003 open) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created from clean `main` at `4232c579e`; HEAD confirmed before any write |
| C1 | done | seven prepared paths copied and proved byte-identical, `.agent/authored/f151-r1.md` confirmed equal to `block.md` by `wc -l` (123) and `sha256sum`, staged and committed alone |
| C2 | done | `.agent/f151_inventory.md` written by reading the code at `4232c579e` (244 lines, under 400), committed alone, no other file touched |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C3` read `absent`, last line `ALL True` |
| Gate 2 | done | `run_selection.py` → exit 0, `3763 passed, 2 skipped in 27.56s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 3 | done | `integrity check --json` → `fail_count` 0, six checks all `pass` |
| Gate 4 | done | `open_finding_ids` → `11` |
| C3 | done | this handback written and committed |
| Push | done | `git push -u origin feature/f151-worker-adapter-contract` succeeded on the first attempt, no HTTP 500 |

## Range

Review of `4232c579e`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `336b7484c` F151 R1 C1: claim F151, book F133 R7, re-head the ledger, DECISION F151 D1, the slice list

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r1.md` | +123/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/context.md` | +9/-9 | rewritten for F151's branch, scope, do-not-touch and assumptions |
| `.agent/decisions.md` | +10/-0 | DECISION F151 D1 appended: the contract is reconciled with what survives, not with the file's named (now-deleted) modules |
| `.agent/live_review.md` | +23/-20 | re-headed from F133 to F151; F133 R7's verdict booked at the end |
| `.agent/plan.md` | +12/-9 | rewritten: goal, current step (T001), next steps (T002, T003, closure) |
| `docs/roadmap/STATUS.md` | +1/-1 | F151's line `[ ]` → `[~]` |
| `docs/roadmap/features/T8_F151.md` | +16/-0 | the Slice list section added, per DECISION F151 D1 |

### `d0625928d` F151 R1 C2: T001, the inventory of the worker call path and its owners

| Path | +/- | Reason |
|---|---|---|
| `.agent/f151_inventory.md` | +244/-0 (new) | T001's findings pass: what was deleted, the surviving call path, the contract's five faces mapped, the error taxonomy, the ownership table, the v1 list and import-guard candidates, the `adapter` name survey, and the proposal for DECISION F151 D2 |

Plus, in this commit (self-reference exception, R-0149 pattern — a handback cannot table the commit
that writes it):

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- Open PR Gate was run before the branch was created: `gh pr list --state open --json
  number,headRefName,baseRefName,isDraft` returned `[]` — no open pull request, so no merge was needed.
- `git checkout -b feature/f151-worker-adapter-contract` from `main` at `4232c579e`, confirmed by
  `git rev-parse HEAD` before any write.
- `git push -u origin feature/f151-worker-adapter-contract` → run once, after this commit, succeeded on
  the first attempt; no HTTP 500, no retry needed.
- No pull request was opened (the block orders none). No worktree was added or removed by this worker.
  No merge, no rebase, no amend. No provider call.

## Verification

Interpreter: the repository's configured Python 3. All four gates were run once each, after C2 and
before C3, per the block.

Gate 1 — `git status --porcelain` → empty. `python3 .remedy-wt/f151-r1/prep/verify.py .` → every line
`True`: both C1 and C2 single-parent and under 500 insertions (194 and 244), both carry an `F151 R1 Cn`
subject, on `feature/f151-worker-adapter-contract`, C1's seven paths exact and byte-equal to their
`c1-*` snapshots, C2's one path holds no machine path and is 244 lines (under 400); `C3` read `absent`
(not yet committed at gate time); last line `ALL True`.

Gate 2 — `python3 .remedy-wt/f151-r1/prep/run_selection.py . .remedy-wt/f151-r1-worker/selection-output.txt`
→ `paths 82`, `exit 0`, `3763 passed, 2 skipped in 27.56s`; the two SKIPPED lines printed verbatim:
`tests/test_agent_tooling.py:43` (D12 quarantine, F252, a deliberately deleted reviewer contract file)
and `tests/test_install_smoke.py:175` (install smoke is opt-in, no network access set). No FAILED, no
ERROR, no `process(es) behind` line.

Gate 3 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, six checks all `pass`
(`handler_import` `handlers=197`, `live_review_verdict` `last Gate verdict PASS`, `plan_consistency`
`unchecked=0, context_complete=False`, `relevant_untracked` `untracked=0, relevant=0`,
`repo_root_hygiene` `no reviewer scratch, evidence dir or archive at the root`, `high_blockers_open`
`no open blocker/high findings`).

Gate 4 — `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
→ `11`.

## Authored-text proofs

C1's seven paths are reviewer-authored or reviewer-produced text applied this round. Each was copied
from its prepared `c1-*` file under `.remedy-wt/f151-r1/prep/` by a dedicated `python3` script under
`.remedy-wt/f151-r1-worker/` (`c1_copy.py`), then proved byte-identical by direct bytes equality
immediately after (`c1_prove.py`); all seven pairs read `True`. `block.md` itself (saved as
`.agent/authored/f151-r1.md`) was separately confirmed equal to the prepared `block.md` by its sha256
(given in the prompt, checked before any file was used) and again by `wc -l` (123) and `sha256sum`
directly against `block.md`, and a third time by `verify.py`'s own check for that path.
`.agent/f151_inventory.md` (C2) is NOT reviewer-authored text — it was written by this worker from
reading the code — so no disk-to-disk comparison applies to it; its own correctness is the gate and
self-review-loop checks recorded above.

## Deviations & assumptions

None. `git branch --show-current` was run as a standalone command, never joined to another, immediately
before the C1 and C2 commits, and read `feature/f151-worker-adapter-contract` every time. Two commits
this round — C1 and C2 — exactly as the block orders, plus this handback as C3. No file outside the
paths the block names per commit was touched. No production or test file was edited; T001 is a
read-only investigation. `.agent/context.md`, `.agent/decisions.md` and `.agent/plan.md` were all
rewritten in C1 as reviewer-prepared byte copies, so no further change to them was needed in C2 or C3.
No mutation red-proof was run. No full suite was run; the selection gate ran pytest once. No two test
commands ran at the same time. No merge, no rebase, no amend, no stash, no provider call.

## For the operator, in plain sentences

This round claimed the next roadmap feature, which gives Remedy's builder and reviewer backends a
single, typed way to describe what they can do and how they are called, so that adding a new vendor
backend later never requires touching the orchestration code that runs today's jobs. Two things it
reconciles with turned out to already be gone: an older declarative worker list and an older external
builder session feature were both deleted by an earlier cleanup feature, so this round recorded that
fact as a formal decision and pointed the new work at what actually runs jobs today instead. Before any
new code is written, this round produced a plain-language map of exactly how a builder or reviewer call
works right now — which piece of code builds the request, which piece retries a failed attempt, which
piece switches to a backup model when one is unreachable, and which piece counts the tokens spent — so
that the people reviewing the next round's design can check it against how the system actually behaves,
not against guesswork. No code that runs a job was changed. The whole test selection this round ordered
passed, and a built-in health check of the project's own record-keeping passed cleanly as well.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. The Open PR Gate, run at the start of the next session before any new branch.
3. Book round 1's verdict in the next round's first commit.
4. T002: the contract and its kit, DECISION F151 D2.

Operator questions open: 0. Open findings: 11, gate 4 printed (`R-1246`, `R-1281`, `R-1326`, `R-1351`,
`R-1353`, `R-1418`, `R-1421`, `R-1425`, `R-1426`, `R-1427` and `R-1428`, all owned by F314).
