# Handoff — F036, round 9 (the closing round: book round 8, rotate the ledger, and accept F036 in
STATUS with its README pins, then open the pull request)

## Session

SESSION 2 of feature F036 · round 9 · rounds so far 9. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, all seven
payloads and the handback template before writing anything, verified every payload and every
committed copy for real, applied `closure.diff`, ran the full serial test selection and the
integrity check to completion, and ran every gate (G1–G4) for real before writing this handback;
G5 runs after this write and before C4 is committed.

## Range

Review of `405538726..HEAD` (`HEAD` is this handback's own commit, `F036 R9 C4`, on
`feature/f036-guided-result-tour`).

## Closure record

F036 is accepted in `docs/roadmap/STATUS.md` this round on the round 8 evidence, unchanged by
round 9: evidence job `f036r8e1001`, accepted head
`153537dc8e5a6bb7061f220cdeaffbc1829d3067`, package
`remedy-review-20260928-094901-READY_FOR_REVIEW.zip` (SHA-256
`e2bd771b3f1c1a52fcc7e73cdae50c4fd4a837107ee5e46b76d79d8b8dffc2f4`) in directory
`/home/decodeux/Repos/remedy-history/zips`, and `self-use NONE (queue exhausted)` — no self-use
item was consumed, because round 8 read the queue exhausted. No pull request number is named here:
none exists yet when this handback is written; the round's final reply carries it after C4 pushes
and `gh pr create` runs.

## Commits

### b7d8397c5 F036 R9 C1: copy round 9 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r9-block.md | 157/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r9-build.py | 108/0 | copy of the reviewer's build.py payload — never run |
| .agent/authored/f036-r9-closure.diff | 52/0 | copy of the reviewer's closure.diff payload |
| .agent/authored/f036-r9-ledger.md | 2/0 | copy of the reviewer's ledger.md payload |
| .agent/authored/f036-r9-plan.md | 26/0 | copy of the reviewer's plan.md payload |
| .agent/authored/f036-r9-pr_body.md | 98/0 | copy of the reviewer's pr_body.md payload |
| .agent/authored/f036-r9-readme_para.txt | 9/0 | copy of the reviewer's readme_para.txt payload |
| .agent/authored/f036-r9-status_line.txt | 1/0 | copy of the reviewer's status_line.txt payload |

453 insertions total, exactly the block's own C1 note (157-line block + 296), under the 500-line
cap.

### e73c546b7 F036 R9 C2: book round 8's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | round 8's `Gate:` entry appended, byte for byte, from ledger.md |
| .agent/plan.md | 5/6 | rewritten to the reviewer's plan.md payload by `shutil.copyfile` |

Measured exactly the block's own C2 expected numstat: 2/0, 5/6.

### 571e8bc63 F036 R9 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 0/36 | rotated out by `scripts/rotate_live_review.py` |
| .agent/live_review_archive.md | 36/0 | rotated in by `scripts/rotate_live_review.py` |

Measured exactly the block's own C3 expected numstat: 0/36, 36/0. Path set: exactly these two
files, nothing else.

### <this commit> F036 R9 C4: accept F036 in STATUS with its README pins
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | 1/1 | `closure.diff` flips F036's STATUS line to `[x]` with its pins |
| README.md | 12/2 | `closure.diff` moves the accepted count, Tier 5 Done cell and prose |
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |

## External actions

- `git push -u origin feature/f036-guided-result-tour` — run immediately after this commit, per
  the bundle order. Its real outcome is reported in the round's reply (G6), not here, because this
  file is written before the push happens.
- `gh pr create --base main --head feature/f036-guided-result-tour --title "F036 — Guided result
  tour" --body-file .remedy-wt/f036-r9/pr_body.md` — run after the push. Its number and URL are
  reported in the round's reply only, per the block, because neither exists when this file is
  written.
- No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no `git stash`, no
  `git worktree add`/`remove` — none of these were run, per constraints 6 and 7.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use), all MATCH:
```
build.py:          108 lines, 5591 bytes, sha256 f8e200da22b5726c4ec9caca0356f9da67d71567bf15164e621ed9768d86519e
closure.diff:        52 lines, 3997 bytes, sha256 61dc87ac75b43cf6435b02b40dc580f858c040f2bc1d7107b5485f7cc49b60d0
ledger.md:            2 lines, 2498 bytes, sha256 ac9633a41624c232e66afc67fd4ddb39300315923f75c2e752c4d12e08632197
plan.md:             26 lines,  813 bytes, sha256 0b11b61b4c0c68237e11b1d05ebf6b78c84d3b109f0ff8cef8644f0e5105fe58
pr_body.md:          98 lines, 5804 bytes, sha256 9d8dbf6a6c2756912b0fc1ecfd16cfd511fab25be8f2009f3756992d45a1e1e9
readme_para.txt:      9 lines,  780 bytes, sha256 0bdbf52b808dc5a3e7f91d0fbc5129454106115f0a1709d9ad391c1407b68dba
status_line.txt:      1 line,   392 bytes, sha256 ced0285376fa9cb89fc5fa64d0c2eea8c490261d71a66bbde260cd903fc8f629
```
Block self-check: 157 lines, sha256
`0a360ba843596c1520a286ae86ec10f2436e10b43b06e89901de4d9b3f8fef27` — MATCH on both readings given
in the delegation message. `.agent/authored/f036-r9-*` copies vs. sources, read back via
`git show b7d8397c5:<path>`, all byte-identical (sha256-verified):
```
f036-r9-block.md          vs .remedy-wt/f036-r9/block.md          MATCH
f036-r9-build.py          vs .remedy-wt/f036-r9/build.py          MATCH
f036-r9-closure.diff      vs .remedy-wt/f036-r9/closure.diff      MATCH
f036-r9-ledger.md         vs .remedy-wt/f036-r9/ledger.md         MATCH
f036-r9-plan.md           vs .remedy-wt/f036-r9/plan.md           MATCH
f036-r9-pr_body.md        vs .remedy-wt/f036-r9/pr_body.md        MATCH
f036-r9-readme_para.txt   vs .remedy-wt/f036-r9/readme_para.txt   MATCH
f036-r9-status_line.txt   vs .remedy-wt/f036-r9/status_line.txt   MATCH
```
Insertions at C1: 453 (measured via `git diff --cached --stat` before commit), equal to the
block's 157 + 296, under the 500-line cap.

**G2 THE BOOKING** — at C2 (`e73c546b7`), `git show <C2>:<path>`:
```
.agent/live_review.md   344469 bytes  sha256 610eb75199aec2d06fb2f895292cf1d05c8ba8392d1f1c500503ffc16eb87151
.agent/plan.md              813 bytes  sha256 0b11b61b4c0c68237e11b1d05ebf6b78c84d3b109f0ff8cef8644f0e5105fe58
```
Both MATCH the block's G2 table exactly. `open_finding_ids` (`scripts.rotate_live_review`) over
`.agent/live_review.md` at C2 read `[]`, matching the reviewer's simulation.

**G3 THE ROTATION** — `python3 scripts/rotate_live_review.py`, printed in full:
```
gate records moved: 10
finding pairs moved: 4 (8 records)
old ledger size: 344469 bytes
new ledger size: 303959 bytes
old archive size: 5340260 bytes
new archive size: 5380770 bytes
open findings before: 0
open findings after: 0
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
MATCH, line for line, against the block's G3 table apart from the final `written:` line, which
names this checkout's own paths as the block anticipates. Resulting file readings:
```
.agent/live_review.md            303959 bytes  sha256 bfede5e874f5b3bc89137538b38c2d89d3e41958839d559c286b4c7cc4c63a70
.agent/live_review_archive.md   5380770 bytes  sha256 db9bea9d7c9c79cb58c6303a3fde89782f9f49e3cc52ab199ade1a90e8713792
```
Both MATCH the block's G3 table exactly. C3's path set (`git status --porcelain` before staging):
exactly `.agent/live_review.md` and `.agent/live_review_archive.md`, nothing else.

**G4 THE CLOSURE EDITS AND THE TREE** — `closure.diff` applied via `git apply --check` (exit 0)
then `git apply` (exit 0), touching exactly `README.md` and `docs/roadmap/STATUS.md`. Readings:
```
docs/roadmap/STATUS.md   56619 bytes  sha256 3b77eec91532077b3a8b494bf64231517e263ebb1f2cc03d8375cd159ad6c80d
README.md                42469 bytes  sha256 af8845034d3c23d2bd4532418454b7383eb9cdec373300d51a261a7ee45b0671
```
Both MATCH the block's G4 table exactly. The status line in `status_line.txt` occurs exactly once
in `docs/roadmap/STATUS.md` (count = 1). `pending_self_use_items()` from
`packages.orchestration.self_use_queue` read `()` — empty. Then, serially:
```
python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py
512 passed in 47.15s
REAL_EXIT=0
```
Matches the reviewer's simulation reading (`512 passed`, exit 0) exactly. Then:
```
python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0, `ok` true — each check's status is the reading, not
the exit code, and the exit code is also 0.

**G5 THE HANDBACK'S PINS** — read after this section is written, before C4 is committed; its
readings go in the round's final reply, not here, per the block's own sequencing (G5 runs after
the handback is written).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit, closure.diff applied, STATUS/README/handoff committed together |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | read after this write, reported in the final reply |
| Pull request | done | opened after C4's push; number and URL reported in the final reply only |

## Authored-text proofs

`closure.diff` was applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never
edited, never retyped. All seven payloads (`build.py`, `closure.diff`, `ledger.md`, `plan.md`,
`pr_body.md`, `readme_para.txt`, `status_line.txt`) were verified line count/byte count/sha256
against the PAYLOADS table before use, and the committed `.agent/authored/f036-r9-*` copies read
back byte-identical to their sources via `git show` (G1, above). `.agent/plan.md` was REWRITTEN to
the payload file by `shutil.copyfile`, never hand-edited; its post-write bytes/sha256 equal the
payload table's own row and C2's resulting file hash matched the reviewer's G2 table exactly.
`ledger.md` was appended to `.agent/live_review.md` byte for byte via a binary-mode read and
append, never retyped. `build.py` and `readme_para.txt` were copied into `.agent/authored/` for
the transport record only (C1) — `build.py` was never run, per constraint 1, because doing so
would reset the reviewer's tree.

## Deviations & assumptions

None. The round's commit sequence (C1, C2, C3, C4) followed the block's ordered bundle exactly,
with no split commit, no extra commit, and no reordering. Every gate ran for real, to completion,
with no summarized "green". A scratch directory `.remedy-wt/f036-r9-worker/` (git-ignored, outside
the tracked path set) was created to hold small Python verification scripts, as the block
authorizes ("which is yours") for shapes the sandbox refuses inline; nothing under it was
committed or is part of this round's tracked path set.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The Open PR Gate — the pull request this round opens is merged by the NEXT feature's
session, never by this one. (3) Rule A5 — the first unchecked feature in `docs/roadmap/STATUS.md`.
Open-findings count: 0, as `scripts/rotate_live_review.py` reads at C3 ("open findings after: 0").
Operator questions open: 1.
