# Handback — F259 Vocabulary & concept model v1, round 8 (CLOSURE PART 1)

## Session

`SESSION 1 of feature F259 · round 8 · rounds so far 8`

Soft limit (25 rounds / 7 sessions) not reached — 8 rounds, 1 session. No scope
report is owed.

Context self-assessment: context is comfortable — roughly a third consumed by a
round whose heaviest reads (the 1239-line prompt document and one 107-second job
run) are already behind it, so nothing here argues for ending the session.

Fortschritt, verbatim as the block authored it:
`~97 % (T001–T004 ✅ · Integration Gate ✅ · Closure Teil 1 im Review · Teil 2 offen) — Schätzung`

## Range

Review of `e10cbc30..HEAD` — 7 content commits plus this handoff commit.
Branch `feature/f259-vocabulary`, pushed. **No pull request created** (`gh pr
list --state open` → `[]`); it belongs to part 2.

## Commits

### d2041b6b f259: save round 8 block to .agent/authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f259-r8.md | +400 / -0 | C0a — byte copy of the scratch block, never retyped |

### 6e0c648b f259: mirror round 8 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +349 / -215 | C0b — same bytes; completes the G1 transport chain |

### 6645854f f259: plan.md for round 8, closure part 1
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21 / -19 | C1 — whole rewrite from the PLANF259R8 slice |

### aca1d835 f259: book the round 7 integration-gate verdict and one prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — the GATE_R7 record appended |
| .agent/prose_slips.md | +3 / -1 | C2 — SLIP8 appended, no trailing newline |

### d393b76c f259: feature file Built State, registration-only banner retired
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F259.md | +48 / -1 | C3 — closure precondition 4: REGBANNER pair + BUILTSTATE append |

### db21957a f259: the one mandated section 3 consolidation, item 32 merged into 16
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +24 / -23 | C4 — the one amend0827 rule-4 consolidation: 37 items → 36 |

### dca20076 f259: self-use item SU-010 generated and run to the approval gate
| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f259/SU-010.md | +7 / -0 | C5 — the generated job markdown, byte-identical to the rendered file |
| .agent/selfuse_f259/run.txt | +118 / -0 | C5 — commands, JobPlan, defect strings, budgets |
| scripts/self_use_queue.json | +8 / -0 | C5 — SU-010 appended by the generator; `consumed_by` left empty |

### (this commit) f259: round 8 handback, closure part 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6 — a handoff cannot table the commit that writes it (R-0149) |

Every commit is single-parent. Insertions against the 500 cap: 400, 349, 21, 5,
48, 24, 133 — all under, largest 400 (C0a, the block copy).

Change-set check — the union of paths touched across `e10cbc30..HEAD` is exactly
the ten the block names, and **`docs/roadmap/STATUS.md` and `README.md` are
untouched** (measured, both `False`). Those two land in the same commit as each
other, in part 2.

## External actions

- `git push -u origin feature/f259-vocabulary` → `e10cbc30..dca20076`, branch set
  up to track. One push, after C5.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
  **No PR created, none merged, no branch deleted, no force-push, no history
  rewrite.**
- The self-use run created its own retained execution worktree
  `.remedy-wt/job-1cbb6972bf7c4ffc` on branch `remedy/job-1cbb6972bf7c4ffc` at
  base `db21957a` — created and managed by `run_job` itself, left untouched, as
  every prior self-use run has left its own. No `git worktree add` was issued by
  hand.

## Verification — one line per gate, real readings

**G1 TRANSPORT — PASS.** `sha256sum .remedy-wt/f259-r8-block.md
.agent/authored/f259-r8.md .agent/last_block.md` → one digest three times,
`481692ac503da0cc3a803fe8bf68bb414525f421aa15021571b6a310c236334b`, 30048 bytes
each; equal to the digest the order stated, verified before the block was read.

**G2 THE RECORD AND THE SLIP — PASS.** `.agent/live_review.md` 843886 → 848281
bytes; pre-bytes are a byte-exact prefix (`True`), remainder is exactly
`"\n" + GATE_R7 + "\n"` (`True`, 4395 bytes); `grep -c '^Gate: R7 — '` 0 before →
1 after. `.agent/prose_slips.md` 82415 → 83964 bytes; prefix-exact `True`,
remainder exactly `"\n\n" + SLIP8` (`True`, 1549 bytes), still no trailing
newline (`ends with newline: False`).

**G3 THE FEATURE FILE — PASS.** REGBANNER containment printed
`TO contains FROM: false` → **REWRITE**, matching the order's label. FROM count
1 before / 0 after; TO count 0 before / 1 after. Reconstruction run against the
**committed blobs** (`git show HEAD~1:` vs `git show HEAD:`): post == pre with
the pair applied plus exactly `"\n" + BUILTSTATE + "\n"` → `True`; 9401 → 12386
bytes (9413 after the pair, +2973 appended for a 2971-byte slice). `^## `
headings in order: Goal & Done · Why this exists · DECISIONs · Design · T001 ·
T002 · T003 · T004 · Acceptance · Do not touch · Orchestrator brief · **Built
State**. `REGISTRATION ONLY` occurs **0** times. One trailing newline.

**G4 THE CONSOLIDATION — PASS, and the answer is exactly one item, number 16.**
BEFORE: 37 items, numbers `1..37`, no gaps. AFTER: 36 items, numbers `1..31` and
`33..37` (`sorted == range(1,32)+range(33,38)` → `True`); 32 absent, retired, no
survivor renumbered. Item-32 block recomputed before deletion: 23 lines, 1703
bytes, sha256
`695759114c327d494d21e548170eeefd74e9263db04881dd9baa8de814d8000b` — **equal to
the value the order stated**, so the deletion proceeded rather than refusing.
Containment readings, each re-run here: `ITEM16 containment: TO contains FROM:
true` → **APPEND**; `FROZEN containment: TO contains FROM: false` → **REWRITE**.
Both labels match the order. Obligations met: ITEM16 FROM count stays **1** after
(append, never FROM-zero); FROZEN FROM 1→**0**, TO 0→**1**. Reconstruction from
the **committed blobs**: post == pre with exactly those three edits and nothing
else → `True`; 91681 → 92038 bytes; one trailing newline.

Per-item digest sweep, all 36 surviving items hashed before and after
(full table below): **items whose digest differs: `[16]`, count 1.** Item 31 is
byte-identical (`a3ee49f1…` both sides), so the newline trap the order warned
about was avoided — the block was removed together with the newline terminating
its last line, exactly once.

| item | before sha256 | after sha256 | same |
|---|---|---|---|
| 1 | dc53a806d7b5fc3da32a2ab69a99f3564cfdd25f391d6a7e773b4ec61a91cbd1 | dc53a806d7b5fc3da32a2ab69a99f3564cfdd25f391d6a7e773b4ec61a91cbd1 | yes |
| 2 | c831ac21dc05e79e168a38efd738ff71d5b385c363a40c11e6b00665359441b2 | c831ac21dc05e79e168a38efd738ff71d5b385c363a40c11e6b00665359441b2 | yes |
| 3 | 67e39e672fdee83b84f465504107ad086af84abcf2cb116aafdc9e8a492e7a07 | 67e39e672fdee83b84f465504107ad086af84abcf2cb116aafdc9e8a492e7a07 | yes |
| 4 | 1132e21bcc715d6797ead0aca71a3cb08e4e82a303c2e43d1b30725c9a0e3969 | 1132e21bcc715d6797ead0aca71a3cb08e4e82a303c2e43d1b30725c9a0e3969 | yes |
| 5 | 011330d9c8832384a0437464e39ec64f005089685a5584ef07d589b1fd31ee4d | 011330d9c8832384a0437464e39ec64f005089685a5584ef07d589b1fd31ee4d | yes |
| 6 | 3cf55673a7337700f3da71710bd8c535337e84f00c872d3328da54ea87840240 | 3cf55673a7337700f3da71710bd8c535337e84f00c872d3328da54ea87840240 | yes |
| 7 | 659e5212dbffb9502dcd8ecea177a3d759818ac8dcab485ded3b7905ac329797 | 659e5212dbffb9502dcd8ecea177a3d759818ac8dcab485ded3b7905ac329797 | yes |
| 8 | 0175de6313788cb5d742a7373a174fb4149d480b513092521e3b1c16f5f26f65 | 0175de6313788cb5d742a7373a174fb4149d480b513092521e3b1c16f5f26f65 | yes |
| 9 | dec675faa62a8c4d0b99f786ba92b731cbc34059a892eed5185eb4a9beb915a2 | dec675faa62a8c4d0b99f786ba92b731cbc34059a892eed5185eb4a9beb915a2 | yes |
| 10 | 8af03da1688fe8e76f44f0786e447d4fb349bd99deaecee4e54a78c823dcb8bd | 8af03da1688fe8e76f44f0786e447d4fb349bd99deaecee4e54a78c823dcb8bd | yes |
| 11 | 3ac45f46abd1f3d30d930a7c0b11455230c76d039f5b44485900904a3285e43a | 3ac45f46abd1f3d30d930a7c0b11455230c76d039f5b44485900904a3285e43a | yes |
| 12 | ebb57dbf72ba356792a3b3a8023be3b067e32ae88ac2adc9011c56a00794aeb2 | ebb57dbf72ba356792a3b3a8023be3b067e32ae88ac2adc9011c56a00794aeb2 | yes |
| 13 | bc959c2a1e67d58fe61bcd7d4051cf387fc441e6757575beaf3d679225e86bca | bc959c2a1e67d58fe61bcd7d4051cf387fc441e6757575beaf3d679225e86bca | yes |
| 14 | b61d1b370b42d39ed43f6fe7884e3543b6f244a063f37099a95b9151f4b9b551 | b61d1b370b42d39ed43f6fe7884e3543b6f244a063f37099a95b9151f4b9b551 | yes |
| 15 | 10b34961d566df13c1e9c94a7c781da40b413f71bf0ed6f34e0dae6f6ff6c678 | 10b34961d566df13c1e9c94a7c781da40b413f71bf0ed6f34e0dae6f6ff6c678 | yes |
| **16** | **22dbc279704540d1d25047127172196648c81947e1d7786df194d1a4e332c2a5** | **dd4348b06ac52d43567bec737967c1c08082373abc95f8cfa1db6080516fe9e9** | **NO** |
| 17 | 17c14f05fcfa38b8d113bcb67ad549f0f54ec10942c6a7f8812b3ce522a44671 | 17c14f05fcfa38b8d113bcb67ad549f0f54ec10942c6a7f8812b3ce522a44671 | yes |
| 18 | 2284d5aa473588c519380d69fcf21fa5f49fcada67f06dd650082dd3a7539c12 | 2284d5aa473588c519380d69fcf21fa5f49fcada67f06dd650082dd3a7539c12 | yes |
| 19 | 28b7c6272f87282844f3a9acfa14754667015baf8a614d2a6ac7f8ac4f320853 | 28b7c6272f87282844f3a9acfa14754667015baf8a614d2a6ac7f8ac4f320853 | yes |
| 20 | 87782f8ad7850e9d9992944da4f4921152adeae4881bd35eecdf2ee50c76b71b | 87782f8ad7850e9d9992944da4f4921152adeae4881bd35eecdf2ee50c76b71b | yes |
| 21 | 34afd5d6720a023f4c78190df78ff3f5e1ba9bcc23c2edf7d9e4b493032c20cf | 34afd5d6720a023f4c78190df78ff3f5e1ba9bcc23c2edf7d9e4b493032c20cf | yes |
| 22 | 7e0fd7ac0c176ca1fe8958fe0d7e5545ed20af072f38ab18339196eaae105654 | 7e0fd7ac0c176ca1fe8958fe0d7e5545ed20af072f38ab18339196eaae105654 | yes |
| 23 | b1c7eeddf56d4db13eabd1365358f39a63e72f49bbfe4c41c14391c9945b60c2 | b1c7eeddf56d4db13eabd1365358f39a63e72f49bbfe4c41c14391c9945b60c2 | yes |
| 24 | e2df135e8367f90b813aa4053989433ea999a427303bff4427688e3e47e5cef1 | e2df135e8367f90b813aa4053989433ea999a427303bff4427688e3e47e5cef1 | yes |
| 25 | 6b8f4e90e5051c8fbc5d00ae779d3a487fde6cdb499d3a4e24028905aaf114f0 | 6b8f4e90e5051c8fbc5d00ae779d3a487fde6cdb499d3a4e24028905aaf114f0 | yes |
| 26 | d1820aff1a49f6d12942eac13fd255dd7ac819eb2e309177309bf67a7f042235 | d1820aff1a49f6d12942eac13fd255dd7ac819eb2e309177309bf67a7f042235 | yes |
| 27 | 63e73c7a171f91bfcfa7b56f439b5f53b1a325701311d01534c0d3c0b5a6e093 | 63e73c7a171f91bfcfa7b56f439b5f53b1a325701311d01534c0d3c0b5a6e093 | yes |
| 28 | dd85e4388e650c0cb32f1a701d741cef894156ed14f29532cb25071e2a7221aa | dd85e4388e650c0cb32f1a701d741cef894156ed14f29532cb25071e2a7221aa | yes |
| 29 | b9de669f10a59e7695de24e2fa24351d8afb16bd278a2c92ef237f4e25b4894b | b9de669f10a59e7695de24e2fa24351d8afb16bd278a2c92ef237f4e25b4894b | yes |
| 30 | 0f5fb0125efdc28ca07f78c7da68923187c628d1368a331afe2cb877fdf12332 | 0f5fb0125efdc28ca07f78c7da68923187c628d1368a331afe2cb877fdf12332 | yes |
| 31 | a3ee49f1ac9ffe466ce96c1a7e34ac5adadf163e5dc50fe8fc266526b1dc1f62 | a3ee49f1ac9ffe466ce96c1a7e34ac5adadf163e5dc50fe8fc266526b1dc1f62 | yes |
| 33 | 13930e55472b7ef4c972a53ca1342445d0a5ea411341244c2be5a5cd5caa26d4 | 13930e55472b7ef4c972a53ca1342445d0a5ea411341244c2be5a5cd5caa26d4 | yes |
| 34 | 678824b6feeea7ee2d01cd4f1d4a4d97b583e02fa020c1d10581887eeb782083 | 678824b6feeea7ee2d01cd4f1d4a4d97b583e02fa020c1d10581887eeb782083 | yes |
| 35 | 50a09855e9fbf73ea21388c44a929cb74278b1fdb2f06d25b6ff69da9af336df | 50a09855e9fbf73ea21388c44a929cb74278b1fdb2f06d25b6ff69da9af336df | yes |
| 36 | c1faf5ba9e138735c07698bed92fa7ed1f068f603d906fbf54adecce56fbed25 | c1faf5ba9e138735c07698bed92fa7ed1f068f603d906fbf54adecce56fbed25 | yes |
| 37 | 4ad6999cd8d4747a1e834e14a1966439df86d7e70d7749b0fdddaf7f5a41de0a | 4ad6999cd8d4747a1e834e14a1966439df86d7e70d7749b0fdddaf7f5a41de0a | yes |

Sweep definition, stated so the reviewer can reproduce it exactly: an item's
block runs from its `^  \d+\. \*\*` line up to but not including the next line
matching that pattern, joined by newlines without a trailing one — the order's
own rule. The pattern matches **41** lines in the file, not 37: §4 carries its
own numbered list (`1.`, `2.`, `3.`, `5.`). The §3 checklist was therefore
bounded by ascending numbering, which stops at the first non-ascending match.
Item 37's block consequently extends to §4's `1.` line, which makes the sweep
strictly wider than the checklist — a superset, so it can only over-detect, and
it detected nothing there. The FROZEN paragraph sits at lines 226–230, i.e.
immediately **before** item 1, so it lies outside every item block and its edit
correctly does not appear in the sweep.

**G5 THE SELF-USE ITEM — PASS.** Full transcript in its own section below.

**G6 THE SUITES — PASS, all eight, run serially, every expected count matched.**

| suite | exit | passed | vs expected |
|---|---|---|---|
| `python3 -m pytest tests/docs/ -q` | 0 | 303 | matches 303 |
| `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` | 0 | 30 | matches 30 |
| `python3 -m pytest tests/ui_server/ -q` | 0 | 515 | matches 515 |
| `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 0 | 52 | matches 52 |
| `python3 -m pytest tests/regression/test_resource_safety.py -q` | 0 | 21 | matches 21 |
| `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` | 0 | 16 | matches 16 |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | 42 | matches 42 |
| `python3 -m pytest tests/test_agent_tooling.py -q` | 0 | 10 | no expectation given; **10 passed, 1 skipped** |

Last lines, real: `303 passed in 0.49s` · `30 passed in 0.36s` · `515 passed in
33.42s` · `52 passed in 5.54s` · `21 passed in 11.51s` · `16 passed in 0.28s` ·
`42 passed in 20.92s` · `10 passed, 1 skipped in 0.19s`. Zero failures, so there
are no failing node ids to quote. The four state readers were run as four.

**G7 THE INTEGRITY GATE — PASS.** Command actually run:
`python3 -m apps.cli.grouped integrity check --json` (the built `remedy` CLI is
denied to this session; this is the route constraint 5 names). Full JSON:

```json
{
  "version": 1,
  "passed": true,
  "fail_count": 0,
  "check_count": 5,
  "checks": [
    { "name": "handler_import",      "status": "pass", "message": "handlers=342" },
    { "name": "live_review_verdict", "status": "pass", "message": "> Round-by-round review record, re-headed at the F259 claim. The heading this" },
    { "name": "plan_consistency",    "status": "pass", "message": "unchecked=0, context_complete=False" },
    { "name": "relevant_untracked",  "status": "pass", "message": "untracked=0, relevant=0" },
    { "name": "high_blockers_open",  "status": "pass", "message": "no open blocker/high findings" }
  ]
}
```

`passed: true`, `fail_count: 0`. `git status --porcelain` → **empty**; there are
**no untracked paths at all**, so none to list. `git status --porcelain
--ignored` shows only gitignored entries (`.remedy-wt/`, `.data/**`,
`.coverage`, `.brain/`, …), none of them relevant.

**G8 THE PLAN AND THE STRUCTURE — PASS.** `wc -l .agent/plan.md` → **42**, under
50. `## Goal` count **1**, `## Next Steps` count **1**.
`filecmp.cmp(".agent/plan.md", <PLANF259R8 slice + one newline>, shallow=False)`
→ **True**. `git status --porcelain` **empty** immediately before C6 was staged.
`git ls-files .remedy-wt` → **nothing** (the scratch is untracked and ignored,
`.gitignore:235`). Every commit single-parent — verified per commit, parent
counts all 1. `git diff --numstat <parent> <commit>`, cell by cell:

| commit | path | + | - |
|---|---|---|---|
| d2041b6b | .agent/authored/f259-r8.md | 400 | 0 |
| 6e0c648b | .agent/last_block.md | 349 | 215 |
| 6645854f | .agent/plan.md | 21 | 19 |
| aca1d835 | .agent/live_review.md | 2 | 0 |
| aca1d835 | .agent/prose_slips.md | 3 | 1 |
| d393b76c | docs/roadmap/features/T2_F259.md | 48 | 1 |
| db21957a | docs/agents/planner_reviewer_prompt.md | 24 | 23 |
| dca20076 | .agent/selfuse_f259/SU-010.md | 7 | 0 |
| dca20076 | .agent/selfuse_f259/run.txt | 118 | 0 |
| dca20076 | scripts/self_use_queue.json | 8 | 0 |

Insertions per commit vs the 500 cap: 400, 349, 21, 5, 48, 24, 133 — all OK, no
oversize commit and none declared. Push: `e10cbc30..dca20076`, one push, exit 0.
**No pull request was created** — `gh pr list --state open` → `[]`.

## The complete self-use transcript (G5)

1. `packages.orchestration.self_use_queue.next_self_use_item()` **before** the
   generator → **`None`**. The queue held nine entries SU-001..SU-009, every one
   with a non-empty `consumed_by` (F257, F258, F106, F108, F109, F110, F112,
   F114, F262), so there was no pending item. Precondition 6's generator step
   was therefore required.
2. `packages.orchestration.self_use_generator.generate_and_append_if_empty()` →
   appended one `SelfUseQueueEntry`:
   - **id** `SU-010`
   - **title** `Address ledger finding R-0418`
   - **provenance** `generated (self-use-generator tier 1, ledger scan, R-0418)`
   - **consumed_by** `''` (empty)
   - **why / job_markdown** — the tier-1 pick, the oldest open Low finding
     R-0418 (the self-drive "Fortschritt line" defect)

   `next_self_use_item()` afterwards → **`SU-010`**, so the track is **not**
   exhausted.
3. The run. `run_next_self_use_item(Path(".remedy-wt/selfuse-f259-run"),
   repo_path=".")`, all three budget arguments left at the function's own
   defaults. **The runner did not raise.** Wall clock **107.832 s** (call start
   epoch 1788646916.114, end 1788647023.946).
   - returned **entry id** `SU-010`
   - returned **path** `.remedy-wt/selfuse-f259-run/SU-010.md`
   - **JobPlan id** `1cbb6972bf7c4ffc`
   - **JobPlan status** `blocked`
   - plan error `task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
   - budgets in force: `max_provider_calls=6`, `max_cost_usd=0.5`,
     `max_tasks=1` (source=invocation), `max_total_tokens=None`,
     `max_wall_clock_minutes=None`, `deadline=None`
   - providers: builder `ollama` (source=cli), reviewer `ollama` (source=cli),
     both models blank with source=default, i.e. the real product defaults
   - one task, T001: `final_status=repair_exhausted`, `reviewer_verdict=fail`,
     `status=blocked`, `test_passed=None`, `repair_rounds_used=2 of 2`
   - `result_diff_size_bytes` **0** — no production code moved by the run
   - retained worktree `.remedy-wt/job-1cbb6972bf7c4ffc` at base `db21957a`
   - **the run was taken to the approval gate and no further: nothing approved,
     nothing applied, nothing promoted.**
4. `packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)`
   → a **`tuple` of length 2 — NOT an empty tuple**. Both strings, verbatim and
   complete, in order:
   1. `job 1cbb6972bf7c4ffc (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
   2. `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
5. Files written under `.agent/selfuse_f259/`, with byte sizes:
   - `SU-010.md` — **1541 bytes**, byte-identical to the rendered job file
     (compared by Python byte read, `True`); sha256
     `6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd`, equal to
     the persisted plan's `job_file_sha256` in
     `.data/task_jobs/1cbb6972bf7c4ffc/job.json`
   - `run.txt` — **6680 bytes**, carrying the commands, the JobPlan id and
     status, the two defect strings and the budgets in force
6. **`consumed_by` for SU-010 is still `''`** — re-read from
   `scripts/self_use_queue.json` after the commit and confirmed empty. This round
   does not consume it; precondition 6 puts that edit in the closure commit,
   which is part 2's.
7. `git status --porcelain` names **nothing** under the runner's dest_dir — it is
   empty overall. `git status --porcelain --ignored -- .remedy-wt` prints
   `!! .remedy-wt/`, i.e. the whole scratch tree is ignored by `.gitignore:235`.

## Authored-text proofs

- Block transport: one digest across the scratch block, `.agent/authored/f259-r8.md`
  and `.agent/last_block.md` (G1).
- `.agent/plan.md`: `filecmp.cmp(..., shallow=False)` **True** against the
  PLANF259R8 slice plus one newline.
- `GATE_R7`, `SLIP8`: reconstruction from the pre-append bytes, both **True**
  (G2).
- `REGBANNER_FROM/TO`, `BUILTSTATE`: reconstruction from the **committed** blobs,
  **True** (G3).
- `ITEM16_FROM/TO`, `FROZEN_FROM/TO`, the item-32 block: reconstruction from the
  **committed** blobs, **True** (G4).

Every slice was extracted from the committed `.agent/authored/f259-r8.md` by
marker extraction in Python and applied byte for byte. Nothing was retyped.

## Item-status table (AGENTS.md)

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f259-r8.md`, `shutil.copyfile`, digest verified |
| C0b | done | `.agent/last_block.md`, same bytes |
| C1 | done | `.agent/plan.md` whole rewrite from PLANF259R8 |
| C2 | done | GATE_R7 + SLIP8 in one commit |
| C3 | done | REGBANNER pair then BUILTSTATE append |
| C4 | done | three edits, exactly one item's digest changed (16) |
| C5 | done | SU-010 generated and run; runner did not raise |
| C6 | done | this commit |

No item was skipped, none deviated, none reordered, and no extra commit was
added. The bundle ran C0a → C0b → C1 → C2 → C3 → C4 → C5 → push → gates → C6,
exactly as ordered.

## Deviations & assumptions

**No departure from the block's ordered commit sequence.** Seven content commits
in the ordered positions plus this handoff; no extra commit, none dropped, none
reordered.

1. **The order's prose misattributes the blank line at the deletion point; its
   instruction is nonetheless correct.** The block says the correct deletion
   "leaves item 31's own trailing blank line followed directly by item 33's first
   line". Measured: **item 31 has no trailing blank line.** Its block ends at the
   content line "reviewer who had registered it." on both sides of the edit. The
   blank line belonged to item **32** — which the same paragraph states correctly
   two sentences earlier — and removing the block together with its terminating
   newline removes that separator, so item 31's last content line now abuts item
   33 directly. The mechanical instruction was right and G4 confirms it (item 31
   byte-identical, exactly one item differs); only the attribution is wrong.
   Impact on disk: none worth repairing — **31 of the 35 adjacent item pairs in
   this list already have no blank separator** (only 34, 35, 36 and 37 are
   preceded by one), the file contains no code fences, so the result matches the
   dominant style rather than departing from it. Reviewer-prose class under
   amend0827 rule 2, not a product defect; no R-id spent by me.
2. **FROZEN_TO leaves a stale numeral standing beside its new one — applied
   verbatim per constraint 1 and declared here.** The paragraph's surviving
   sentence still reads "The list stood at 37 items on 2026-08-27, which is the
   number the next consolidation measures against", while the text just appended
   to the same paragraph reads "The next consolidation measures against 36." A
   reader now finds two present-tense answers to "what does the next
   consolidation measure against" in one paragraph. Read chronologically they
   agree (37 was this pass's baseline, 36 is the next one's), but the older
   sentence is now stale and a later reviewer may read the pair as a
   contradiction. I did not touch it: it is outside the three edits the order
   authorised, and the order forbids anything else changing.
3. **Shell-guard refusal, quoted verbatim.** `grep -n '^  [0-9]\+\. \*\*'
   docs/agents/planner_reviewer_prompt.md` (in a compound command with two
   further greps and a `wc -l`) was refused: *"Permission to use Bash has been
   denied. IMPORTANT: You *may* attempt to accomplish this action using other
   tools that might naturally be used to accomplish this goal, e.g. using head
   instead of cat. But you *should not* attempt to work around this denial in
   malicious ways… If you believe this capability is essential to complete the
   user's request, STOP and explain to the user what you were trying to do and
   why you need this permission."* Re-expressed in Python (`re.compile(r"^  (\d+)\. \*\*")`
   over the file's lines) — the enumeration, the heading list and the whole
   digest sweep were produced that way, and each Python snippet is reported
   beside its output above. Real exit codes for the suites were likewise
   collected in Python (`subprocess.run(...).returncode`), because `$?` in a
   compound command is refused.
4. **Gate route.** G7 used `python3 -m apps.cli.grouped integrity check --json`,
   not the built `remedy` CLI, which is denied to this session — the substitution
   constraint 5 prescribes.
5. **G6's eighth suite carried no expected count**, as the order intended
   ("report the number"): `tests/test_agent_tooling.py` → 10 passed, 1 skipped,
   exit 0. Reported as the number it is.
6. **SU-010's job markdown has the same sha256 as F262's SU-009** —
   `6d72d9c1…`, 1541 bytes both. Declared so it is not read as a copy error: both
   are tier-1 picks of the same oldest open Low finding R-0418, so the generator
   renders an identical job body; the id lives in the queue entry and the
   filename, not in the markdown.
7. **The two defect strings are NOT registered as R-ids this round.** The block
   ordered them reported, not registered, and it registered no id. Closure
   precondition 6 does require every string to be registered as a normal R-id
   finding **before the close** — so this is work still owed, and the reviewer
   decides at its gate whether they add evidence to the open R-0784 (the same
   two strings arrived from SU-009 in F262 R26) or mint a new id. Flagging it
   here so part 2 does not close over it.

Open findings: **294** — recomputed mechanically, 299 registration lines
(`^- R-\d{4}`) against 5 `Done:` lines (`^Done: R-\d{4}`). Unchanged by this
round; no id was spent, and the one prose-level lesson went to
`.agent/prose_slips.md` per amend0827 rule 2.

## Next

The reviewer's gate on this round. Then **CLOSURE PART 2**: the ledger rotation
via `scripts/rotate_live_review.py` as its own commit; the registration of the
self-use defect strings; the evidence job; the fresh review zip (a failing build
is a closure blocker); the STATUS `[x]` line and the README capability sync in
ONE commit together with the SU-010 `consumed_by` edit; then the pull request,
which is created but **not merged** in this session — it merges at the next
feature's Open PR Gate.

Phase 1 rule 1 first at the next session start: read `.agent/STOP` from disk
before anything else, then the Open PR Gate.
