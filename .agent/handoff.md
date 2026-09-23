# Handback — F279 Configuration & toolchain truth · Round 2 · Book round 1's PASS, record DECISION F279 D2, land T001's registry half

## Session

SESSION 1 of feature F279 · round 2 · rounds so far 2

This round booked round 1's PASS into the ledger, recorded DECISION F279 D2
(config.py is the registry, not a new module) with the feature file's T001
amendment, and landed T001's registry half: the fifteen `REMEDY_` names
production code spelled without a spec are now registered as env-only keys
in `packages/orchestration/config.py`'s `_CONFIG_KEY_SPECS`, and a new
`tests/orchestration/test_env_registry.py` holds every such name to the
registry, each guard backed by a red-proof (`mutations.py`) run against a
disposable `--detach` worktree at C3. All of G1-G5 ran before this handoff
was written and matched the block's stated expectations exactly, byte for
byte and reading for reading. Context self-assessment: a comfortable
majority of the working budget remains at handback.

## Range

Review of `62c689e1`..`HEAD`.

## Commits

### ce2bf78e F279 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r2-block.md | +214/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f279-r2-ledger.diff | +10/-0 | Payload copy |
| .agent/authored/f279-r2-plan.md | +37/-0 | Payload copy |
| .agent/authored/f279-r2-decisions.diff | +38/-0 | Payload copy |
| .agent/authored/f279-r2-feature.diff | +17/-0 | Payload copy |

Measured insertions: 316 (214+10+37+38+17 = 316), matching the block's "this
block's line count plus 102" formula (214+102=316) exactly, under the 500 cap.

### 1b0eb1ac F279 R2 C1b: copy round 2 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r2-config.diff | +174/-0 | Payload copy |
| .agent/authored/f279-r2-test_env_registry.py | +93/-0 | Payload copy |
| .agent/authored/f279-r2-mutations.py | +67/-0 | Payload copy (G5 tool, never applied to a tracked file) |

Measured insertions: 334, matching the block's expected 334 exactly.

### a52bc565 F279 R2 C2: book round 1's PASS, record DECISION F279 D2 and amend T001
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.diff` applied: round 1's `Gate:` entry appended |
| .agent/plan.md | +15/-12 | Rewritten to the round-2 plan.md payload |
| .agent/decisions.md | +30/-0 | `decisions.diff` applied: DECISION F279 D2 recorded |
| docs/roadmap/features/T2_F279.md | +6/-0 | `feature.diff` applied: T001 amended to match the decision |

Measured insertions (`git diff --numstat`): 30 decisions.md, 2
live_review.md, 15 plan.md, 6 T2_F279.md — matching the block's expected
counts exactly.

### aa5d90a2 F279 R2 C3: register every REMEDY_ name production code spells, and guard it
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/config.py | +163/-0 | `config.diff` applied: 15 unregistered `REMEDY_` names added to `_CONFIG_KEY_SPECS` as env-only |
| tests/orchestration/test_env_registry.py | +93/-0 | New file, copied whole from the payload, `git add`ed |

Measured insertions: 163 config.py, 93 test_env_registry.py — matching the
block's expected counts exactly.

### (this commit) F279 R2 C4: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f279-r2-mut aa5d90a2` — created for
  G5; `git worktree remove --force .remedy-wt/f279-r2-mut` then
  `git worktree prune` removed it as G5's last action. `git worktree list`
  afterward showed only the primary checkout and the two pre-existing
  `.remedy-wt/job-*` worktrees.
- `git push origin feature/f279-configuration-toolchain-truth` — see the
  session's final reply for the real outcome; it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no
  checkout of `main` or any other branch/commit in the primary checkout: none
  run, per constraint 5.
- `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their
  branches and every existing stash were left untouched.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '/home/decodeux/Repos/remedy/.agent/STOP': No such file or directory`, real exit 2 (ENOENT), absent — proceed.
- `git status --porcelain` → empty. `git branch --show-current` →
  `feature/f279-configuration-toolchain-truth`. `git log --oneline -1` →
  `62c689e1 F279 R1 C7: rewrite handoff for round 1`. All three matched.
- Block bytes (R-0954): measured line count (newline count)=214,
  sha256=`806ea9daafef8068f2fd744417c310e3a5376014bed51c868c7aa182de1d9d8d`;
  matches both readings given in the delegation message exactly.
- `git worktree list` (before any change) → primary checkout at `62c689e1`
  plus `.remedy-wt/job-129b3ad7206d4f8d` (`09441a92`) and
  `.remedy-wt/job-e7268925db3a4831` (`cc8696a3`).
- `git stash list | head -1` →
  `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 7 measured and matched the block's table exactly (line count,
byte count, sha256): config.diff (174/5717/`386cc4f5...`), decisions.diff
(38/2697/`1d7420e4...`), feature.diff (17/1046/`6ae3410b...`), ledger.diff
(10/7685/`c5d50428...`), mutations.py (67/2592/`6a4db126...`), plan.md
(37/1599/`87ef5e1b...`), test_env_registry.py (93/3883/`16ae49f0...`).

`git apply --check` then `git apply` for every `.diff` payload (ledger,
decisions, feature, config): all 4 pairs at real exit code 0, in the commit
order the block specifies.

G1 TRANSPORT — every `.agent/authored/f279-r2-*` copy (8 files, including
the block copy) read back with `git show <adding-commit>:<path>` and
compared byte-for-byte against its source (`.remedy-wt/f279-r2-block.md` for
the block, `.remedy-wt/f279-r2-payloads/<name>` for the rest): all 8 matched
exactly.

G2 THE BOOKKEEPING — at C2 (`a52bc565`): `.agent/live_review.md`
bytes=376430 sha256=`01c7cc95...` MATCH; `.agent/plan.md` bytes=1599
sha256=`87ef5e1b...` MATCH; `.agent/decisions.md` bytes=1861590
sha256=`87e7757e...` MATCH; `docs/roadmap/features/T2_F279.md` bytes=8234
sha256=`7eba8a4c...` MATCH. Open-finding-id set via `open_finding_ids`
(`scripts/rotate_live_review.py`), computed over `.agent/live_review.md`
text at `62c689e1` and at C2: 26 and 26, both set differences empty —
matching the block's 26/26 exactly. Lines beginning `Gate: F279 R1 — ` at
`62c689e1` and at C2: 0 and 1 — matching the block's 0/1 exactly.
`git diff --name-only <C1b> <C2>` → exactly `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T2_F279.md` — matches C2's list.

G3 THE REGISTRY — `git diff --name-only <C2> <C3>` → exactly
`packages/orchestration/config.py`, `tests/orchestration/test_env_registry.py`
— matches C3's list. At C3 (`aa5d90a2`): `packages/orchestration/config.py`
bytes=51844 sha256=`d69f3d33...` MATCH; `tests/orchestration/test_env_registry.py`
bytes=3883 sha256=`16ae49f0...` MATCH.

G4 THE TESTS — the ordered pytest selection (real exit code 0):
`1025 passed in 294.25s (0:04:54)`. The reviewer ran the same selection
WITHOUT `tests/cli/test_golden_path.py` inside a disposable worktree and
read `981 passed, 2 skipped` at exit 0; this round ran the full selection
INCLUDING golden path in the primary checkout, which carries the UI toolchain
a worktree lacks (as the block anticipates), accounting for the different
pass/skip counts.
`python3 -m ruff check packages/orchestration/config.py tests/orchestration/test_env_registry.py`
→ `All checks passed!`, real exit 0. `python3 -m apps.cli.main integrity check --json`
→ all 5 checks `pass` (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `high_blockers_open`), `fail_count`
0, real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r2-mut aa5d90a2`
real exit 0. `python3 -B .remedy-wt/f279-r2-payloads/mutations.py .remedy-wt/f279-r2-mut`
real exit 0, full output:
```
control_before REAL_EXIT=0
4 passed in 1.87s
m1_unregistered_literal_read FROM count in packages/orchestration/run_log.py: 1
m1_unregistered_literal_read REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::test_every_literal_env_read_names_a_registered_variable
FAILED tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered
2 failed, 2 passed in 1.89s
m1_unregistered_literal_read restored byte-identical: True
m2_unregistered_name_in_a_constant FROM count in packages/runtimes/runtime_config.py: 1
m2_unregistered_name_in_a_constant REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered
1 failed, 3 passed in 1.89s
m2_unregistered_name_in_a_constant restored byte-identical: True
m3_spec_removed FROM count in packages/orchestration/config.py: 1
m3_spec_removed REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::test_every_literal_env_read_names_a_registered_variable
FAILED tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered
2 failed, 2 passed in 1.89s
m3_spec_removed restored byte-identical: True
m4_env_var_registered_twice FROM count in packages/orchestration/config.py: 1
m4_env_var_registered_twice REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::test_every_literal_env_read_names_a_registered_variable
FAILED tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered
FAILED tests/orchestration/test_env_registry.py::test_every_registered_variable_is_a_remedy_name_and_registered_once
3 failed, 1 passed in 1.89s
m4_env_var_registered_twice restored byte-identical: True
control_after REAL_EXIT=0
4 passed in 1.87s
```
Every reading matches the reviewer's stated expectations exactly: control
4/4 passed, m1 2 failed at the two named tests, m2 1 failed at the named
test, m3 2 failed at the same two tests as m1, m4 3 failed at the three
named tests, control_after 4 passed.
`git worktree remove --force .remedy-wt/f279-r2-mut` real exit 0,
`git worktree prune` real exit 0. `git worktree list` afterward → primary
checkout plus the two `.remedy-wt/job-*` worktrees only.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148):
byte-identity proof = mechanical disk-to-disk comparison of the applied
location against the `.agent/authored/` copy.

- This block (`f279-r2-block.md`): `.agent/authored/f279-r2-block.md` at C1a
  verified byte-identical to `.remedy-wt/f279-r2-block.md` (G1) and to the
  two readings given in the delegation message.
- All 6 payloads (ledger.diff, plan.md, decisions.diff, feature.diff,
  config.diff, test_env_registry.py, mutations.py): each
  `.agent/authored/f279-r2-<name>` copy verified byte-identical to its
  `.remedy-wt/f279-r2-payloads/<name>` source (G1).
- Every `.diff` payload applied by `git apply` (never retyped): ledger,
  decisions, feature, config — all 4, `git apply --check` then `git apply`,
  real exit 0 both times, and the resulting tracked-file digests MATCH the
  reviewer's stated readings exactly at G2/G3.
- `plan.md` (rewrite, never retyped): `shutil.copyfile` from the payload;
  resulting `.agent/plan.md` digest MATCHES the reviewer's stated G2 reading
  exactly.
- `test_env_registry.py` (new file, copied whole, never retyped):
  `shutil.copyfile` from the payload to `tests/orchestration/`; resulting
  digest MATCHES the reviewer's stated G3 reading exactly.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 316 insertions, matches 214+102 formula |
| C1b | done | 334 insertions, matches expectation |
| C2 | done | round 1's PASS booked, DECISION F279 D2 recorded, T001 amended, all four insertion counts match |
| C3 | done | registry + guard landed, both counts match |
| C4 | done | this handback |
| G1 TRANSPORT | done | all 8 authored copies byte-identical to source |
| G2 THE BOOKKEEPING | done | all 4 digests match, 26/26 open-finding set empty diff, 0/1 Gate-line count matches, file-list matches |
| G3 THE REGISTRY | done | file-list and both digests match |
| G4 THE TESTS | done | 1025 passed exit 0, ruff clean exit 0, integrity 5/5 pass exit 0 |
| G5 THE RED PROOFS | done | control/m1-m4/control_after all match reviewer's exact readings, worktree cleaned up |
| G6 TREE AND PUSH | done | reported in the session's final reply, not this file, since it runs after C4 |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C2, C3, C4)
exactly and touched exactly the tracked path set constraint 3 names —
confirmed by `git diff --name-only 62c689e1 HEAD` before C4 was written,
which listed precisely the 8 `.agent/authored/f279-r2-*` copies,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T2_F279.md`, `packages/orchestration/config.py` and
`tests/orchestration/test_env_registry.py`.

No oversize commit this round (largest was C2's 53 insertions net, well
under the 500 cap; F279's one declared oversize commit remains round 1's C5).

No other procedural deviation. Nothing was merged this round, per
constraint 5. No `remedy/job-*` branch or self-use worktree was created,
touched or deleted beyond the round's own `.remedy-wt/f279-r2-mut`, which
was created and removed within G5 per constraint 6. The full suite was not
run, per constraint 7 (amend0917 rule 1) — F279's one full-suite run belongs
to its closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 2,
then T001's doctor and docs half — `remedy doctor core` naming unknown and
unparsable `REMEDY_*` variables, and the generated
`docs/guides/environment.md` with its drift test. Open findings: 26.
Operator questions: 0.
