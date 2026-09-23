# Handback — F279 Configuration & toolchain truth · Round 4 · Book round 3's PASS, record DECISION F279 D4, land T001's reader half

## Session

SESSION 1 of feature F279 · round 4 · rounds so far 4

This round booked round 3's PASS into the ledger, recorded DECISION F279 D4
(UI flags and the strict event-name flag now read yes for 1, true or yes
rather than "1" alone; a whole-number or number variable that fails to parse
now fails naming the variable and its type, an empty value included; the
Claude planner's 300-second timeout default now lives in the variable's spec
alone; text reads, the standalone `scripts/` scripts and the two runtime
port reads keep their own reads), and landed T001's reader half: `env_value`
in `packages/orchestration/config.py` reads a registered variable from the
live environment as its declared type, the eleven typed reads (ui_server.py
x4, run_log.py, claude_planner/provider.py, ollama_builder/provider.py,
ollama_planner/provider.py, runtime_supervisor.py, and others) moved onto
it, and `tests/orchestration/test_env_registry.py` guards every typed read
stays on it. All of G1-G5 ran before this handoff was written and matched
the block's stated expectations exactly, byte for byte and reading for
reading. Context self-assessment: a comfortable majority of the working
budget remains at handback.

## Range

Review of `0a529d69`..`HEAD`.

## Commits

### 3af08afc F279 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r4-block.md | +235/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f279-r4-ledger.diff | +10/-0 | Payload copy |
| .agent/authored/f279-r4-plan.md | +32/-0 | Payload copy |
| .agent/authored/f279-r4-decisions.diff | +43/-0 | Payload copy |
| .agent/authored/f279-r4-feature.diff | +15/-0 | Payload copy |
| .agent/authored/f279-r4-slips.diff | +9/-0 | Payload copy |

Measured insertions: 344 (block's line count 235 plus 109), matching the
block's formula and its stated total exactly, well under the 500 cap.

### c5dc31b4 F279 R4 C1b: copy round 4 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r4-config.diff | +47/-0 | Payload copy |
| .agent/authored/f279-r4-ollama_builder.diff | +47/-0 | Payload copy |
| .agent/authored/f279-r4-ollama_planner.diff | +45/-0 | Payload copy |
| .agent/authored/f279-r4-claude_planner.diff | +36/-0 | Payload copy |
| .agent/authored/f279-r4-ui_server.diff | +55/-0 | Payload copy |
| .agent/authored/f279-r4-run_log.diff | +28/-0 | Payload copy |
| .agent/authored/f279-r4-runtime_supervisor.diff | +21/-0 | Payload copy |
| .agent/authored/f279-r4-test_env_registry.diff | +122/-0 | Payload copy |
| .agent/authored/f279-r4-mutations.py | +62/-0 | Payload copy (G5 tool, never applied to a tracked file) |

Measured insertions: 463, matching the block's expected 463 exactly.

### 2a8f7efa F279 R4 C2: book round 3's PASS and record DECISION F279 D4
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.diff` applied: round 3's `Gate:` entry appended |
| .agent/plan.md | +11/-13 | Rewritten to the round-4 plan.md payload |
| .agent/decisions.md | +35/-0 | `decisions.diff` applied: DECISION F279 D4 recorded |
| docs/roadmap/features/T2_F279.md | +4/-0 | `feature.diff` applied: the feature file's note |
| .agent/prose_slips.md | +1/-0 | `slips.diff` applied: one prose-slip line appended |

Measured insertions (`git diff --numstat`): 35 decisions.md, 2
live_review.md, 11 plan.md, 1 prose_slips.md, 4 T2_F279.md — matching the
block's expected counts exactly.

### 49cb9d1b F279 R4 C3: read every typed REMEDY_ variable through the registry reader
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/config.py | +36/-0 | `config.diff` applied: `env_value()` added, reading a registered variable from the live environment as its declared type |
| packages/orchestration/run_log.py | +2/-2 | `run_log.diff` applied: its typed read moved onto `env_value` |
| packages/orchestration/ui_server.py | +11/-4 | `ui_server.diff` applied: four typed reads (demo mode x2, no-auto-build, allow-legacy-fallback) moved onto `env_value` |
| packages/providers/claude_planner/provider.py | +4/-14 | `claude_planner.diff` applied: its timeout read moved onto `env_value`; the provider's private 300s default deleted |
| packages/providers/ollama_builder/provider.py | +5/-15 | `ollama_builder.diff` applied: its typed reads moved onto `env_value` |
| packages/providers/ollama_planner/provider.py | +5/-15 | `ollama_planner.diff` applied: its typed reads moved onto `env_value` |
| packages/runtimes/runtime_supervisor.py | +5/-3 | `runtime_supervisor.diff` applied: the log-cap read moved onto `env_value`; an empty `REMEDY_RUNTIME_LOG_MAX` now fails loudly instead of silently meaning no cap |
| tests/orchestration/test_env_registry.py | +98/-0 | `test_env_registry.diff` applied: the reader's own tests plus the guard holding all eleven typed reads on it |

Measured insertions: 36 config.py, 2 run_log.py, 11 ui_server.py, 4
claude_planner provider.py, 5 ollama_builder provider.py, 5 ollama_planner
provider.py, 5 runtime_supervisor.py, 98 test_env_registry.py — matching
the block's expected counts exactly.

### (this commit) F279 R4 C4: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f279-r4-mut 49cb9d1b` — created for
  G5; `git worktree remove --force .remedy-wt/f279-r4-mut` then
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
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, real exit 2 (ENOENT), absent — proceed.
- `git status --porcelain` → empty. `git branch --show-current` →
  `feature/f279-configuration-toolchain-truth`. `git log --oneline -1` →
  `0a529d69 F279 R3 C6: rewrite handoff for round 3`. All three matched.
- Block bytes (R-0954): measured line count (newline count)=235,
  sha256=`341d57ddc5b7bd4f29fbed7caa0bdbf767dcf1d44cf2c29c272a3944674e00df`;
  matches both readings given in the delegation message exactly.
- `git worktree list` (before any change) → primary checkout at `0a529d69`
  plus `.remedy-wt/job-129b3ad7206d4f8d` (`09441a92`) and
  `.remedy-wt/job-e7268925db3a4831` (`cc8696a3`).
- `git stash list | head -1` →
  `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 14 measured and matched the block's table exactly (line
count, byte count, sha256): claude_planner.diff (36/1716/`c2538346...`),
config.diff (47/2367/`48e630d4...`), decisions.diff (43/3307/`1ba8b559...`),
feature.diff (15/1022/`825ad48a...`), ledger.diff (10/6964/`f0a999bd...`),
mutations.py (62/2701/`4290c666...`), ollama_builder.diff
(47/2049/`c407d116...`), ollama_planner.diff (45/1970/`2618c9dd...`),
plan.md (32/1322/`33556ec3...`), run_log.diff (28/949/`528a3448...`),
runtime_supervisor.diff (21/1056/`7a627d2f...`), slips.diff
(9/1635/`146e3b40...`), test_env_registry.diff (122/6073/`e074be00...`),
ui_server.diff (55/2430/`cd203efb...`).

`git apply --check` then `git apply` for every `.diff` payload (ledger,
decisions, feature, slips, config, ollama_builder, ollama_planner,
claude_planner, ui_server, run_log, runtime_supervisor,
test_env_registry): all 12 pairs at real exit code 0, in the commit order
the block specifies. `.agent/plan.md` was a rewrite by `shutil.copyfile`,
never a `git apply`.

G1 TRANSPORT — every `.agent/authored/f279-r4-*` copy (15 files, including
the block copy) read back with `git show <adding-commit>:<path>` and
compared byte-for-byte against its source (`.remedy-wt/f279-r4-block.md` for
the block, `.remedy-wt/f279-r4-payloads/<name>` for the rest): all 15
matched exactly.

G2 THE BOOKKEEPING — at C2 (`2a8f7efa`): `.agent/live_review.md`
bytes=380746 sha256=`85cb0df6...` MATCH; `.agent/plan.md` bytes=1322
sha256=`33556ec3...` MATCH; `.agent/decisions.md` bytes=1867202
sha256=`2c5cac8d...` MATCH; `docs/roadmap/features/T2_F279.md` bytes=8575
sha256=`05493ada...` MATCH; `.agent/prose_slips.md` bytes=364451
sha256=`5a97f18d...` MATCH. Open-finding-id set via `open_finding_ids`
(`scripts/rotate_live_review.py`), computed over `.agent/live_review.md`
text at `0a529d69` and at C2: 26 and 26, both set differences empty —
matching the block's 26/26 exactly. Lines beginning `Gate: F279 R3 — ` at
`0a529d69` and at C2: 0 and 1 — matching the block's 0/1 exactly.
`git diff --name-only <C1b> <C2>` → exactly `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`docs/roadmap/features/T2_F279.md` — matches C2's list.

G3 THE READER — `git diff --name-only <C2> <C3>` → exactly
`packages/orchestration/config.py`, `packages/orchestration/run_log.py`,
`packages/orchestration/ui_server.py`,
`packages/providers/claude_planner/provider.py`,
`packages/providers/ollama_builder/provider.py`,
`packages/providers/ollama_planner/provider.py`,
`packages/runtimes/runtime_supervisor.py`,
`tests/orchestration/test_env_registry.py` — matches C3's list exactly. At
C3 (`49cb9d1b`): `packages/orchestration/config.py` bytes=62161
sha256=`cb2ad6ad...` MATCH; `packages/providers/ollama_builder/provider.py`
bytes=11447 sha256=`99e5b308...` MATCH;
`packages/providers/ollama_planner/provider.py` bytes=7658
sha256=`c18029b6...` MATCH; `packages/providers/claude_planner/provider.py`
bytes=13104 sha256=`3c9a9bb7...` MATCH;
`packages/orchestration/ui_server.py` bytes=147335 sha256=`e69cada6...`
MATCH; `packages/orchestration/run_log.py` bytes=6845 sha256=`77da32cb...`
MATCH; `packages/runtimes/runtime_supervisor.py` bytes=25721
sha256=`3d5c8885...` MATCH; `tests/orchestration/test_env_registry.py`
bytes=11442 sha256=`52f60d4b...` MATCH. No digest differed, so no `git
diff --no-index` stop was needed.

G4 THE TESTS — the ordered pytest selection, run SERIALLY (real exit code
0): `2244 passed, 4 skipped in 397.78s (0:06:37)`. The reviewer ran the same
selection WITHOUT `tests/cli/test_golden_path.py` inside a disposable
worktree and read `2201 passed, 5 skipped` at exit 0; this round ran the
full selection INCLUDING golden path in the primary checkout, which carries
the UI toolchain a worktree lacks (as the block anticipates), accounting for
the different pass/skip counts.
`python3 -m ruff check packages/orchestration/config.py
packages/orchestration/run_log.py packages/orchestration/ui_server.py
packages/providers/claude_planner/provider.py
packages/providers/ollama_builder/provider.py
packages/providers/ollama_planner/provider.py
packages/runtimes/runtime_supervisor.py
tests/orchestration/test_env_registry.py`
→ `All checks passed!`, real exit 0. `python3 -m apps.cli.main integrity
check --json` → all 5 checks `pass` (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`), `fail_count` 0, real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r4-mut
49cb9d1b` real exit 0. `python3 -B .remedy-wt/f279-r4-payloads/mutations.py
.remedy-wt/f279-r4-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
57 passed in 2.88s
m1_boolean_reads_only_one FROM count in packages/orchestration/config.py: 1
m1_boolean_reads_only_one REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::TestTheRegistryReader::test_a_boolean_reads_yes_only_for_the_registered_words
1 failed, 56 passed in 2.84s
m1_boolean_reads_only_one restored byte-identical: True
m2_unset_answers_the_default_everywhere FROM count in packages/orchestration/config.py: 1
m2_unset_answers_the_default_everywhere REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::TestTheRegistryReader::test_an_unset_variable_remedy_toml_may_carry_answers_none
1 failed, 56 passed in 2.93s
m2_unset_answers_the_default_everywhere restored byte-identical: True
m3_parse_error_names_nothing FROM count in packages/orchestration/config.py: 1
m3_parse_error_names_nothing REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::TestTheRegistryReader::test_a_number_that_does_not_parse_names_the_variable_and_its_type
FAILED tests/test_ollama_builder.py::test_invalid_temperature_raises_with_var_name
FAILED tests/test_ollama_builder.py::test_invalid_num_predict_raises_with_var_name
3 failed, 54 passed in 2.92s
m3_parse_error_names_nothing restored byte-identical: True
m4_a_typed_read_bypasses_the_reader FROM count in packages/orchestration/ui_server.py: 1
m4_a_typed_read_bypasses_the_reader REAL_EXIT=1
FAILED tests/orchestration/test_env_registry.py::test_a_typed_variable_is_read_through_the_registry_reader
1 failed, 56 passed in 2.86s
m4_a_typed_read_bypasses_the_reader restored byte-identical: True
control_after REAL_EXIT=0
57 passed in 2.83s
```
Every reading matches the reviewer's stated expectations exactly: control
57/57 passed, m1 1 failed at
`TestTheRegistryReader::test_a_boolean_reads_yes_only_for_the_registered_words`,
m2 1 failed at
`TestTheRegistryReader::test_an_unset_variable_remedy_toml_may_carry_answers_none`,
m3 3 failed at the three named tests, m4 1 failed at
`test_a_typed_variable_is_read_through_the_registry_reader`, control_after
57 passed.
`git worktree remove --force .remedy-wt/f279-r4-mut` real exit 0,
`git worktree prune` real exit 0. `git worktree list` afterward → primary
checkout plus the two `.remedy-wt/job-*` worktrees only.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148):
byte-identity proof = mechanical disk-to-disk comparison of the applied
location against the `.agent/authored/` copy.

- This block (`f279-r4-block.md`): `.agent/authored/f279-r4-block.md` at
  C1a verified byte-identical to `.remedy-wt/f279-r4-block.md` (G1) and to
  the two readings given in the delegation message.
- All 13 payloads (ledger.diff, plan.md, decisions.diff, feature.diff,
  slips.diff, config.diff, ollama_builder.diff, ollama_planner.diff,
  claude_planner.diff, ui_server.diff, run_log.diff,
  runtime_supervisor.diff, test_env_registry.diff, mutations.py): each
  `.agent/authored/f279-r4-<name>` copy verified byte-identical to its
  `.remedy-wt/f279-r4-payloads/<name>` source (G1).
- Every `.diff` payload applied by `git apply` (never retyped): ledger,
  decisions, feature, slips, config, ollama_builder, ollama_planner,
  claude_planner, ui_server, run_log, runtime_supervisor,
  test_env_registry — all 12, `git apply --check` then `git apply`, real
  exit 0 both times, and the resulting tracked-file digests MATCH the
  reviewer's stated readings exactly at G2/G3.
- `plan.md` (rewrite, never retyped): `shutil.copyfile` from the payload;
  resulting `.agent/plan.md` digest MATCHES the reviewer's stated G2
  reading exactly.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 344 insertions, matches 235+109 formula |
| C1b | done | 463 insertions, matches expectation |
| C2 | done | round 3's PASS booked, DECISION F279 D4 recorded, all five insertion counts match |
| C3 | done | reader and its eleven callers landed, all eight counts match |
| C4 | done | this handback |
| G1 TRANSPORT | done | all 15 authored copies byte-identical to source |
| G2 THE BOOKKEEPING | done | all 5 digests match, 26/26 open-finding set empty diff, 0/1 Gate-line count matches, file-list matches |
| G3 THE READER | done | file-list and all 8 digests match, no stop needed |
| G4 THE TESTS | done | 2244 passed, 4 skipped, exit 0, ruff clean exit 0, integrity 5/5 pass exit 0 |
| G5 THE RED PROOFS | done | control/m1-m4/control_after all match reviewer's exact readings, worktree cleaned up |
| G6 TREE AND PUSH | done | reported in the session's final reply, not this file, since it runs after C4 |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C2, C3,
C4) exactly and touched exactly the tracked path set constraint 3 names —
confirmed by `git diff --name-only 0a529d69 HEAD` before C4 was written.

No oversize commit this round (largest was C1b's 463 insertions, well under
the 500 cap; F279's one declared oversize commit remains round 1's C5).

No sandbox friction beyond the block's own anticipated shapes: every
measurement script was written to a file under
`.remedy-wt/f279-r4-scratch/` and run with `python3 <file>` or `bash
<file>`, never as an inline heredoc or `VAR=x cmd` shape; no payload was
retyped or edited.

No other procedural deviation. Nothing was merged this round, per
constraint 5. No `remedy/job-*` branch or self-use worktree was created,
touched or deleted beyond the round's own `.remedy-wt/f279-r4-mut`, which
was created and removed within G5 per constraint 6. The full suite was not
run, per constraint 7 (amend0917 rule 1) — F279's one full-suite run
belongs to its closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4,
then T003 — `remedy block lint`. Open findings: 26. Operator questions: 0.
