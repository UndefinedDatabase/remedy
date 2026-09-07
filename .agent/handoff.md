# Handback — F274 round 5 — `context_pack` reaches ZERO edges

The round cut the last recorded edge of `packages.orchestration.context_pack` by DELETING the
cockpit `context-budget` read endpoint that was built on it: the builder
`_build_context_budget_json` in `packages/orchestration/ui_server.py`, its single route-table
line, and its two tests. Nothing replaces it — no stub, no alias, no 404 route. The deletion is
ruled as DECISION F274 D3, written in C3 BEFORE the cut in C4, because the plan's own rule is
that nothing is deleted before the decision recording the deletion exists.

THE HEADLINE MEASUREMENT: the deletion map falls from 39 edges to 38, and
`packages.orchestration.context_pack` now has an EMPTY recorded-consumer list and an EMPTY
measured-consumer list. It becomes the THIRD cluster module the deletion may take, beside
`review_bundle` and `self_repair_proposal`. The count of cluster modules carrying at least one
edge falls from 22 to 21. No module was deleted this round.

THE NAME COLLISION DID NOT CLAIM A VICTIM. `context_budget` names two different concepts here.
The deleted one is `_build_context_budget_json`, built on the cluster module
`packages.orchestration.context_pack`. The surviving one is `estimate_context_budget` /
`export_context_budget_estimate_json` in `packages/orchestration/token_economy.py`, surfaced
through the key `context_budget_estimate` that `packages/orchestration/ui_server.py` reads at
line 1001. `token_economy.py` is not in the change set and has no diff in this range; the
`context_budget_estimate` read at line 1001 is present and unmodified after the cut.

Round 4's PASS verdict is booked into `.agent/live_review.md` in this round's C2, under operator
amendment amend0827-process-diet rule 1.

## Session

SESSION 3 of feature F274 · round 5 · rounds so far 5 (soft limit 25) · sessions 3 of 7.

`.agent/STOP` was ABSENT at the start of the round and was re-checked before the cut. No pull
request was created and nothing was merged.

## Range

Review of `0d68507bd5b794109db45d6d5765798fa87f7b97`..`<C5>` (this handoff commit).

## Commits

### 2df66b58 F274 R5 C0a: save the round 5 block as the authored original

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f274-r5.md | +324/-0 | the round 5 block saved by `shutil.copyfile` from `.remedy-wt/f274-r5-block.md` |

### 5795e396 F274 R5 C0b: mirror the round 5 block into the last block slot

| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +230/-233 | same file mirrored by `shutil.copyfile`; the +/- is against round 4's block |

### 9a4107a1 F274 R5 C1: advance the plan to round 5

| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-18 | whole-file replacement by the authored text PLANF274R5 |

### 5e2a9e07 F274 R5 C2: book the round 4 PASS verdict into the record

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | the authored slice RECORD5 appended at the end (its own leading blank line plus one paragraph) |

### 97403515 F274 R5 C3: rule the cockpit context-budget endpoint deletion as D3

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +46/-0 | the authored slice D3SLICE274 appended at the end — DECISION F274 D3 |

### 72ca7740 F274 R5 C4: cut the context_pack edge by deleting the context-budget endpoint

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +0/-21 | `_build_context_budget_json` with its docstring, its `except` fallback and the blank lines separating it from its neighbours (20 lines), plus the one route-table line |
| tests/ui_server/test_live_state.py | +0/-8 | the test method `test_context_budget_endpoint` and its separating blank line |
| tests/orchestration/test_test_runner.py | +0/-11 | the test method `test_context_budget_returns_degraded_signal`, which imported the deleted function by name |
| tests/orchestration/cluster_deletion_map.txt | +0/-1 | the recorded edge `packages.orchestration.context_pack <- packages/orchestration/ui_server.py`, removed in the SAME commit that cuts it |

### `<C5>` F274 R5 C5: hand back round 5 with its real gate results

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-reference) | this handback; a handoff cannot table the commit that writes it (R-0149 pattern). The reviewer measures it at the next gate. |

Every +/- cell above is taken from `git diff --numstat <sha>^ <sha>` and was compared cell by
cell against the per-commit figures G8 reports. They agree.

## External actions

| Action | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f274-r5-g5 72ca7740` | created; worktree count 14 → 15 |
| `git worktree add --detach .remedy-wt/f274-r5-g6base 0d68507b` | created; worktree count 15 → 16 |
| `git worktree remove --force .remedy-wt/f274-r5-g5` | removed |
| `git worktree remove --force .remedy-wt/f274-r5-g6base` | removed |
| `git worktree prune` | exit 0; worktree count back to 14 |
| `git push -u origin feature/f274-one-world-completion-part-two` | run after C5 — see the push line at the end of this section |
| PR create / PR merge / any `gh` command | NONE. No pull request was created; nothing was merged. |

Push: `git push -u origin feature/f274-one-world-completion-part-two` — exit 0, branch up to
date with the six commits C0a..C5.

## Verification

One line per gate, with its REAL exit code.

- **G1 TRANSPORT — EXIT 0.** `.remedy-wt/f274-r5-block.md`, `.agent/authored/f274-r5.md` and
  `.agent/last_block.md` are all **26865 bytes** and all hash to
  `086b486a775911164ac34029a7583a6e556aba9d11c439334950e8c3cc8ab301`; `filecmp.cmp(shallow=False)`
  is True for both pairs. Per §3 item 37 this chain covers those three artefacts and claims
  nothing about the bytes emitted into the worker's prompt.
- **G2 THE RECORD APPEND — EXIT 0.** (a) BYTE: `.agent/live_review.md` 528978 → 535659, pre-image
  a byte-exact PREFIX of the post-image, post-image == pre-image + the 6681-byte RECORD5 slice
  exactly, `len(post) == len(pre) + len(slice)` so no separator newline was added. (b) STRUCTURAL,
  unit = *a maximal run of consecutive non-empty lines, as the tuple of those lines*: units 214 →
  215, **N counted from the slice = 1**, the last unit equals the slice's one paragraph in order,
  and every unit before it is unchanged. (c) NEGATIVE CONTROL: byte 528984, inside the FIRST
  appended paragraph, XOR-flipped — BOTH readers reject it, and the file on disk is unchanged
  afterwards (the flip is done in memory, as in round 4, so the primary checkout is never dirtied).
  (d) COUNTS before→after: registrations 65 → 65, resolutions 3 → 3, **OPEN SET 62 → 62 BY
  DISTINCT ID**, `^Gate: ` 35 → 36, `^Gate: F274 R4` 0 → 1. Base figures 65/3/62/35/0 reproduced
  exactly.
- **G3 THE DECISION APPEND — EXIT 0.** (a) BYTE: `.agent/decisions.md` **886003 → 889313**,
  pre-image a byte-exact PREFIX of the post-image, post-image == pre-image + the 3310-byte
  D3SLICE274 exactly. (b) STRUCTURAL, same unit definition as G2: units 1951 → 1959, **N counted
  from the slice = 8**, the last 8 units equal the slice's 8 paragraphs IN ORDER, every unit
  before them unchanged. (c) NEGATIVE CONTROL: byte 886009, inside the FIRST appended paragraph
  (index 0 of 8, not the last) — BOTH readers reject it, disk unchanged. (d) `^## DECISION F274 D`
  2 → 3, and `^## DECISION F274 D3 ` heads exactly ONE section.
- **G4 THE PLAN — EXIT 0.** `.agent/plan.md` is byte-equal to PLANF274R5 (`filecmp.cmp`
  shallow=False True), 2462 bytes, **44 lines against the cap of 50**, and it carries both
  `## Goal` and `## Next Steps`.
- **G5 THE EDGE IS CUT AND THE RATCHET IS PROVED BOTH WAYS — EXIT 0**, in the disposable worktree
  `.remedy-wt/f274-r5-g5` at C4 `72ca7740`.
  (a) UNMUTATED CONTROL, both suites in ONE command: `python3 -B -m pytest
  tests/orchestration/test_cluster_deletion_map.py tests/orchestration/test_import_reachability.py
  -q` → **EXIT 0, 6 passed**.
  (b) Through the SHIPPED readers `measured_edges()` and `recorded_edges()`: **measured 38,
  recorded 38, EQUAL** (APPEARED 0, DISAPPEARED 0); cluster modules carrying at least one recorded
  edge **21 of 24**; the three with ZERO are `packages.orchestration.context_pack`,
  `packages.orchestration.review_bundle`, `packages.orchestration.self_repair_proposal`. The
  reading this round exists for, printed as a LIST and not as a claim — recorded consumers of
  `packages.orchestration.context_pack`: **`[]`** (0), measured consumers: **`[]`** (0).
  (c) RED, map direction: appending the deleted edge line back to
  `tests/orchestration/cluster_deletion_map.txt` → **EXIT 1**, `DISAPPEARED (1)` naming exactly
  `packages.orchestration.context_pack <- packages/orchestration/ui_server.py`, `APPEARED (0)`;
  restored by exact path with `git checkout -- tests/orchestration/cluster_deletion_map.txt`,
  worktree porcelain empty, control back to **EXIT 0, 3 passed**.
  (d) RED, import direction: appending `from packages.orchestration import context_pack` to
  `packages/orchestration/ui_server.py` (0 occurrences beforehand) → **EXIT 1**, `APPEARED (1)`
  naming exactly that same edge, `DISAPPEARED (0)`; restored by exact path with `git checkout --
  packages/orchestration/ui_server.py`, worktree porcelain empty, control back to **EXIT 0, 3
  passed**. This is what proves the map still SEES `ui_server.py` as a consumer, so the cut was a
  real cut and not a hidden exclusion.
- **G6 THE LINT CEILING AND THE BUDGETS — both readings 26.** BASE mechanism: `python3 -m ruff
  check .` run from the root of the disposable worktree `.remedy-wt/f274-r5-g6base`, checked out
  at `0d68507bd5b794109db45d6d5765798fa87f7b97`, so `pyproject.toml` and its `per-file-ignores`
  resolve against the same paths — **Found 26 errors**, tool exit 1. HEAD mechanism: the same
  command in the PRIMARY checkout at C4 — **Found 26 errors**, tool exit 1. The two agree, so
  DECISION F083 D5's frozen ceiling is untouched; `ruff`'s own exit code is 1 by construction
  because the ceiling is 26 and not 0, and that is declared below rather than smoothed over.
  `python3 -m pytest tests/orchestration/test_ci_budgets.py -q` → **EXIT 0, 10 passed**.
  `ruff --fix` was NOT run.
- **G7 THE SUITES, run SERIALLY in the PRIMARY CHECKOUT — every one EXIT 0.** The four state
  readers, run as FOUR: `tests/ui_server/` **EXIT 0, 514 passed**;
  `tests/orchestration/test_test_runner.py` **EXIT 0, 51 passed**;
  `tests/regression/test_resource_safety.py` **EXIT 0, 21 passed**;
  `tests/orchestration/test_integrity_gate.py` **EXIT 0, 16 passed**. Then
  `tests/regression/test_named_bugs.py` **EXIT 0, 64 passed / 6 skipped**;
  `tests/orchestration/test_cluster_deletion_map.py` **EXIT 0, 3 passed**;
  `tests/orchestration/test_import_reachability.py` **EXIT 0, 3 passed**; and the canary
  `tests/cli/test_golden_path.py` **EXIT 0, 42 passed**.
  THE TWO COUNTS THE BLOCK ORDERED CHECKED, stated explicitly: `tests/ui_server/` went **515 → 514
  — it fell by EXACTLY ONE**; `tests/orchestration/test_test_runner.py` went **52 → 51 — it fell
  by EXACTLY ONE**. Neither stayed level and neither fell by more than one.
- **G8 THE TREE AND THE COMMITS — EXIT 0.** `git status --porcelain` was EMPTY at every commit
  boundary (checked after each of C0a, C0b, C1, C2, C3, C4 and again after the worktree teardown)
  and is `''` at C4. `git ls-files .remedy-wt` is `''`. `git worktree list` counted **14 before,
  15 and then 16 while the two disposable worktrees existed, and 14 after `remove --force` ×2 plus
  `prune`**. `git diff --name-only 0d68507bd5b794109db45d6d5765798fa87f7b97..72ca7740` names
  exactly NINE paths, every one in the declared change set and nothing else: `.agent/authored/
  f274-r5.md`, `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `packages/orchestration/ui_server.py`,
  `tests/orchestration/cluster_deletion_map.txt`, `tests/orchestration/test_test_runner.py`,
  `tests/ui_server/test_live_state.py`. The tenth declared path, `.agent/handoff.md`, arrives with
  C5. Per-commit insertions against the DECISION F104 D1 cap of 500: **324, 230, 19, 2, 46, 0** for
  C0a..C4 — every one far under the cap, and every commit single-parent.

Supporting measurements taken while executing the SPEC, reported because the block asked for the
count:

- The bytes `"context-budget": _build_context_budget_json,` occur **EXACTLY ONCE** in
  `packages/orchestration/ui_server.py` at the base. Count reported: **1**.
- `grep -rn "_build_context_budget_json\|context-budget" apps/ packages/ tests/ scripts/` after
  the cut returns **ZERO hits**.
- `python3 -m py_compile` on the three edited Python files: **exit 0**.
- The surviving concept after the cut: `context_budget_estimate` still read at
  `packages/orchestration/ui_server.py:1001`; `estimate_context_budget` and
  `export_context_budget_estimate_json` still defined in
  `packages/orchestration/token_economy.py`, a file this range does not touch.
- `_load_events`, the helper the deleted function called, still has 21 occurrences in
  `ui_server.py`, so the deletion left no orphan.

## Authored-text proofs

Three reviewer-authored texts were applied this round. All three were extracted PROGRAMMATICALLY
from `.agent/authored/f274-r5.md` by matching the `<<<BEGIN <NAME> ` prefix line and the
`<<<END <NAME>>>` line, inclusive of the newline ending the last content line
(`.remedy-wt/extract.py`). None was hand-typed.

| Text | Bytes | Disk-to-disk result |
|---|---|---|
| PLANF274R5 | 2462 | `filecmp.cmp('.remedy-wt/PLANF274R5.txt', '.agent/plan.md', shallow=False)` → **True** (G4) |
| RECORD5 | 6681 | post-image of `.agent/live_review.md` == pre-image + slice, byte for byte (G2 a) |
| D3SLICE274 | 3310 | post-image of `.agent/decisions.md` == pre-image + slice, byte for byte (G3 a) |

Each slice's own leading blank line was preserved as authored: PLANF274R5 begins `# Plan —` with
no leading blank, RECORD5 and D3SLICE274 each begin with their own `\n`, and no separator newline
was added to either append.

## Deviations & assumptions

1. **Every gate ran as a Python script under `.remedy-wt/`, not as a shell one-liner.** This
   shell's guard refuses `$?` inside a compound command, shell loops and `$(...)`, and an agent
   thread's cwd is reset between bash calls, so `cd <dir> && cmd; echo $?` is unavailable in all
   three of its parts. Re-expression: `.remedy-wt/g1_transport.py`, `g2_record.py`,
   `g3_decision.py`, `g4_plan.py`, `g5b_edges.py`, `g8_tree.py` and the runner
   `.remedy-wt/run_in.py`, all executed with `python3 -B`; `run_in.py` supplies the working
   directory via `subprocess.run(cwd=...)` and prints the real exit code. No gate's meaning
   changed — only the way the command was spelled. `.remedy-wt/` is gitignored and
   `git ls-files .remedy-wt` is empty.
2. **G2's structural reader went RED on its first run because of a defect in MY OWN gate script,
   not in the file it was reading.** The first implementation split the images on blank lines with
   a regex, which leaves boundary newlines attached asymmetrically: the pre-image's last unit kept
   its trailing `\n` while the post-image's did not, and the slice's single unit kept its own
   leading `\n`, so the tail and head comparisons both read False while the BYTE reader read True
   on every clause. Redefining a unit as *a maximal run of consecutive non-empty lines, as the
   tuple of those lines* fixed it and the gate then read EXIT 0. Declared because the first run's
   real exit code was 1 and this handback reports real exit codes. Nothing on disk was written or
   reverted by that run — it is a pure reader — and no production file was involved. The corrected
   definition is stated in the G2 and G3 lines above and both gates use it.
3. **The block quotes the route line with FOUR MORE LEADING SPACES than the file carries, and I
   deleted the file's line rather than the block's literal string.** The block's "The cut" renders
   the line as `                    "context-budget": _build_context_budget_json,` (20 spaces); on
   disk it carries 16. That is the block's own presentation convention for quoted file content —
   it does the same to the map line, which the block indents by 4 and which sits at column 0 in
   `cluster_deletion_map.txt` — so this is markdown code-block indentation, not a disagreement
   about the file. I resolved it by measurement rather than by assumption: the identifying bytes
   `"context-budget": _build_context_budget_json,` occur **EXACTLY ONCE** in the file, at
   indentation 16, so the SPEC has one and only one referent. Reported rather than silently
   normalised, because the block ordered the count and because "The cut" is a SPEC I implement,
   not authored bytes I copy.
4. **`python3 -m ruff check .` exits 1 in BOTH G6 readings.** The gate's demand is that both read
   26 errors, and both do; but 26 is a frozen non-zero ceiling, so the tool's own exit code cannot
   be 0 and reporting it as 0 would be false. Both readings are 26 and the ceiling is intact.
5. **The `__pycache__` purge was satisfied by construction rather than by a purge command.** The
   guard refused `find ... -exec rm -rf {} +`. Both worktrees were created fresh by
   `git worktree add` in this round and contained no `__pycache__` at any point, and every
   mutation run and every control run used `python3 -B`. No stale cache could have been read.
6. **G8's `git diff --name-only` names NINE paths, not the change set's ten.** The tenth,
   `.agent/handoff.md`, is written by C5 itself, which is the commit G8 runs before. The block
   anticipates this — "C5's own numbers go in the handback's `## Commits` table" — so this is the
   ordered behaviour and not an omission; it is listed here because a reader auditing the change
   set against G8's output would otherwise count a path missing.

NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. The commits are exactly C0a, C0b, C1, C2,
C3, C4, C5, in that order, with no extra commit, no dropped commit and no reordering. C3 precedes
C4 as the block requires, so DECISION F274 D3 exists on disk before the bytes it rules are
removed.

NO FINDING WAS MINTED AND NONE WAS RESOLVED. No `Done:` paragraph and no `Landed:` line was
written; only the reviewer's authored text resolves a finding. **Open findings: 62 by distinct
id**, unchanged from the base, as G2 (d) measures before and after. R-0830 and R-0831 remain open;
the next free id is R-0832. The open High findings are R-0803, R-0804, R-0806 and R-0807, all
F273's rather than this feature's, per DECISION F272 D12.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block as `.agent/authored/f274-r5.md` | done | `shutil.copyfile`, 26865 bytes |
| C0b mirror to `.agent/last_block.md` | done | `shutil.copyfile`, same 26865 bytes |
| C1 `.agent/plan.md` = PLANF274R5 | done | byte-equal, 44 lines |
| C2 `.agent/live_review.md` append RECORD5 | done | +6681 bytes, both readers green |
| C3 `.agent/decisions.md` append D3SLICE274 | done | +3310 bytes, DECISION F274 D3 heads one section |
| C4 the cut, to the SPEC | done | 4 files, 41 lines deleted, 0 inserted |
| C5 `.agent/handoff.md` full rewrite | done | this file |
| G1 transport | done | EXIT 0 |
| G2 the record append | done | EXIT 0 (first run EXIT 1 on a defect in the gate script — deviation 2) |
| G3 the decision append | done | EXIT 0 |
| G4 the plan | done | EXIT 0 |
| G5 the edge cut and the ratchet both ways | done | EXIT 0; reds at EXIT 1 as ordered, restored to EXIT 0 |
| G6 the lint ceiling and the budgets | done | 26 base / 26 head; `test_ci_budgets.py` EXIT 0 (deviation 4) |
| G7 the suites | done | 8 suites, every one EXIT 0; both ordered counts fell by exactly one |
| G8 the tree and the commits | done | EXIT 0 |
| Push the branch | done | `git push -u origin feature/f274-one-world-completion-part-two` |
| Create a pull request | skipped | the block forbids it |
| Merge anything | skipped | the block forbids it |
| Touch `tests/orchestration/import_reachability_allowlist.txt` | skipped | this round adds no module, so the block excludes it from the change set |
| Mint or resolve a finding | skipped | block constraint 4: no `Done:`, no `Landed:`, open set 62 → 62 |
| Run `ruff --fix` | skipped | block constraint 5: the 26 errors are a frozen ceiling |
| Delete `packages/orchestration/context_pack.py` | skipped | the block forbids it; the module survives at zero edges until the deletion round under DECISION F260 D3 |

## Next

The reviewer reads the committed diff of
`0d68507bd5b794109db45d6d5765798fa87f7b97..<C5>` and re-runs G1 through G8 itself before any
verdict. On PASS, the next round is the one `.agent/plan.md` names first:
`context_optimizer`'s last edge — the `context_budget` BRAIN NODE that
`packages/orchestration/project_brain.py` builds, which also reaches `brain_detail.py`,
`brain_viewer.py`, `brain_viewer_theme.py`, `ui_view_model.py` and `ui_copy.py`, and which is
deliberately its own round. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
