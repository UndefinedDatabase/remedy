# Handoff — F035, round 1 (claim F035, re-head the live review record, book F030 R7, record
DECISION F035 D1, and land the first half of T001: the ownership ledger module, its entry
schema and actor, and a pure pass over the records that already name who acted)

## Session

SESSION 1 of feature F035 · round 1 · rounds so far 1. Context remaining at handback:
comfortable — the round read AGENTS.md, the block, the reviewer's three payloads and the
handback template once, read every source module the block named (whole or by search),
wrote the module and its 33-test suite, ran the full gate selection three times and the
mutation tool once, and still has a healthy context budget left.

## Range

Review of `a0b287a55`..`HEAD` (`HEAD` is this handback's own commit, `F035 R1 C5`, on
`feature/f035-ownership-ledger`).

## Commits

### d7e741086 F035 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r1-block.md | 332/0 | verbatim copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f035-r1-context.md | 36/0 | verbatim copy of the context.md payload |
| .agent/authored/f035-r1-plan.md | 30/0 | verbatim copy of the plan.md payload |

Measured insertions: 398 (332+36+30). Block expected 332+66=398. Match, under the 500-line cap.

### cea469ff8 F035 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r1-claim.diff | 161/0 | verbatim copy of the claim.diff payload |

Measured insertions: 161. Block expected 161. Match.

### 35e1ad11c F035 R1 C2: claim F035, re-head the live review record, book F030 R7, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 14/14 | rewritten to context.md payload |
| .agent/decisions.md | 79/0 | DECISION F035 D1 appended by claim.diff |
| .agent/live_review.md | 23/20 | re-headed (heading + intro + Steps) and F030 R7's gate entry appended, by claim.diff |
| .agent/plan.md | 16/12 | rewritten to plan.md payload |
| docs/roadmap/STATUS.md | 1/1 | F035's line `[ ]` to `[~]`, by claim.diff |

Measured by `git show --numstat`: 14/14, 79/0, 23/20, 16/12, 1/1. Block expected exactly this.
Match. `git apply --check .remedy-wt/f035-r1-payloads/claim.diff` read exit 0, then the real
`git apply` also read exit 0.

### 69af2cb03 F035 R1 C3a: build the ownership ledger from the records that name who acted
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ownership.py | 499/0 | new module: S1-S5 — the ledger, the entry schema, the actor, the seven S4 readers, the build |

Measured insertions: 499. **Deviation**: the block's own C3 bundled this file with the
`ALLOWED_UNWIRED` line in one commit named `C3`; the module alone measured 508 lines on first
write, over the 500-line cap even before the second file's `+3` was added, so it was trimmed
(separator banners tightened from 3 lines to 1, one docstring paragraph break removed) to 499
and split into **C3a** (this commit, the module alone) and **C3b** (the guard line), per
constraint 2's own naming pattern. See Deviations below.

### 301550d7c F035 R1 C3b: allow-list ownership.py as unwired until round 2 wires it
| Path | +/- | Reason |
|---|---|---|
| tests/test_no_orphan_modules.py | 3/0 | S6 — `ALLOWED_UNWIRED` entry for `ownership.py`, between `hunk_apply.py` and `self_use_findings.py` |

Measured insertions: 3.

### 12398596b F035 R1 C4a: add the ownership ledger's mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r1-mutations.py | 178/0 | G5's mutation tool: 12 red proofs, a control run first and last, byte-identical restoration |

Measured insertions: 178. **Deviation**: the block named this commit's payload as part of `C4`
alongside the test file; the test file alone measured 658 lines, so the bundle was split three
ways instead of the block's own `C4a`/`C4b` pair — see Deviations below.

### d85741e46 F035 R1 C4b: test the ownership ledger per action class, part one
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_ownership_ledger.py | 445/0 | new file, first 445 lines: fixtures, builders, TestEmptyJob through TestSteering |

Measured insertions: 445. The file is syntactically complete and importable at this commit
(the cut lands after `TestSteering`'s closing blank line, before the next class); it is not
independently run as a gate step, since G4 runs at C4's tip (after C4c).

### ca8e00924 F035 R1 C4c: test the ownership ledger per action class, part two
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_ownership_ledger.py | 213/0 | remaining 213 lines appended: TestRunLog through TestIdempotence |

Measured insertions: 213. Together with C4b: 658 lines, 33 test functions (`--collect-only -q`
confirms 33 collected), covering every item the block's TESTS section orders.

### C5 (this commit) — the handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | rewritten per docs/agents/handback_template.md |

## External actions

- `git checkout -b feature/f035-ownership-ledger` from `main` at `a0b287a55` — succeeded.
- `git worktree add --detach .remedy-wt/f035-r1-mut ca8e00924` (G5) — succeeded, worktree
  created at C4's tip.
- `git worktree remove --force .remedy-wt/f035-r1-mut` — succeeded.
- `git worktree prune` — succeeded, no-op (nothing stale).
- `git push -u origin feature/f035-ownership-ledger` — reported below (after this commit).
- No `gh pr create`, no `gh pr merge`, no branch deletion, no force-push, no `git stash` — none
  ordered, none run.

## Verification

**Step 1** — `ls .agent/STOP`: `ls: cannot access '.agent/STOP': No such file or directory`,
`REAL_EXIT=2`. Does not exist; proceeded.

**Step 2** — `pwd`: `/home/decodeux/Repos/remedy`. `git status --porcelain`: empty.
`git branch --show-current`: `main`. `git log --oneline -1`: `a0b287a55 Merge pull request #289
from UndefinedDatabase/feature/f030-steering-messages`. All three matched. Then
`git checkout -b feature/f035-ownership-ledger` — branch created, reported above.

**Step 3** — block bytes: measured 332 lines (newline count), sha256
`18bd369622a14dd8f92b853357da870060b7a42dcfd4da49b3dd07421d2b0f04` against the delegation
message's stated 332 / `18bd369622a14dd8f92b853357da870060b7a42dcfd4da49b3dd07421d2b0f04`. Both
match.

**Step 4** — `git worktree list | wc -l`: 61 (found, before this round's own worktree
additions).

**Payloads** (G1's own table, verified before use):
| file | lines | bytes | sha256 | match |
|---|---|---|---|---|
| claim.diff | 161 | 19954 | c549edffa7281082a0e893096c0ecf58f25f70470e381787b1379d615932e8f3 | yes |
| context.md | 36 | 1538 | 516a4400e303e8fc913d8e1aec6f664ce0eacc725153fc4d1cd4e49eb67c10a1 | yes |
| plan.md | 30 | 1081 | 8d0f445c1e6dd1adc7ae81a95ef2e2cc7c4f872a61947681f844c95d9aa3242b | yes |

**G1 TRANSPORT** — each `.agent/authored/f035-r1-*` copy read back with `git show <commit>:<path>`
and compared byte for byte against its source:
- `f035-r1-block.md` (at `d7e741086`) == `.remedy-wt/f035-r1/block.md`: True (25818 == 25818 bytes)
- `f035-r1-plan.md` (at `d7e741086`) == `.remedy-wt/f035-r1-payloads/plan.md`: True (1081 == 1081)
- `f035-r1-context.md` (at `d7e741086`) == `.remedy-wt/f035-r1-payloads/context.md`: True (1538 == 1538)
- `f035-r1-claim.diff` (at `cea469ff8`) == `.remedy-wt/f035-r1-payloads/claim.diff`: True (19954 == 19954)

**G2 THE CLAIM** — every file's sha256, read with `git show 35e1ad11c:<path>`, against the
reviewer's simulation-tree reading:
| path | bytes (measured/expected) | sha256 match |
|---|---|---|
| docs/roadmap/STATUS.md | 55903/55903 | yes |
| .agent/live_review.md | 299354/299354 | yes |
| .agent/decisions.md | 2325681/2325681 | yes |
| .agent/plan.md | 1081/1081 | yes |
| .agent/context.md | 1538/1538 | yes |

Open finding set, `open_finding_ids` from `scripts/rotate_live_review.py`: `[]` at both
`a0b287a5` and `35e1ad11c` (C2). At C2 the ledger has exactly one line reading `## Findings`
and exactly one reading `## Steps`; its last line begins `Gate: F030 R7 — `. F035's STATUS line
at C2 reads back in full as `- [~] F035 — Ownership ledger`. `git diff --name-only cea469ff8
35e1ad11c` names exactly: `.agent/context.md`, `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/roadmap/STATUS.md` — the table above, nothing else.

**G3 THE CODE** —
```
python3 -m ruff check packages/orchestration/ownership.py tests/orchestration/test_ownership_ledger.py tests/test_no_orphan_modules.py
```
at C4c (`ca8e00924`): `All checks passed!`, `REAL_EXIT=0`.

Quoted from `git show 69af2cb03` (the file is byte-identical from C3a through the branch tip —
`git diff 69af2cb03 HEAD -- packages/orchestration/ownership.py` is empty):

`ownership_actor`, whole:
```python
def ownership_actor(recorded_as: Any, *, kind: str = "operator",
                    auto_approved: bool = False) -> dict[str, Any]:
    """One actor: `kind`, `door`, `recorded_as`, `token_number` (always 0 here — round 1
    numbers fingerprints over the whole sorted ledger, not per actor), `auto_approved`.

    `recorded_as` is `str(recorded_as)`, or "" for `None`, never otherwise changed — an
    operator's own token or channel name travels unaltered. A `kind` outside `ACTOR_KINDS`
    raises `OwnershipError`: nothing renders authorless or under an invented kind.
    """
    if kind not in ACTOR_KINDS:
        raise OwnershipError(f"unknown actor kind {kind!r}; must be one of {ACTOR_KINDS}")
    recorded = "" if recorded_as is None else str(recorded_as)
    if recorded.startswith("tf:") or recorded in ("cockpit", "ui"):
        door = "browser"
    elif recorded == "cli":
        door = "cli"
    else:
        door = ""
    return {
        "kind": kind,
        "door": door,
        "recorded_as": recorded,
        "token_number": 0,
        "auto_approved": bool(auto_approved),
    }
```

`build_ownership_ledger`'s sort and token-numbering lines:
```python
    entries.sort(key=lambda e: (e["ts"] == "", e["ts"], e["record_ref"]))

    fingerprint_numbers: dict[str, int] = {}
    next_number = 1
    for entry in entries:
        recorded_as = entry["actor"].get("recorded_as", "")
        if isinstance(recorded_as, str) and recorded_as.startswith("tf:"):
            if recorded_as not in fingerprint_numbers:
                fingerprint_numbers[recorded_as] = next_number
                next_number += 1
            entry["actor"]["token_number"] = fingerprint_numbers[recorded_as]
```

Reader (g)'s dedupe:
```python
        key = (name, request_id)
        if key in seen:
            continue
        seen.add(key)
```

**G4 THE TESTS** — in the primary checkout at C4c, the ordered selection ran serially:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <selection> 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Trimmed output:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
1201 passed, 1 skipped in 83.24s (0:01:23)
REAL_EXIT=0
```
The one `SKIPPED` line is exactly the F252 quarantine the block names, unchanged. Node count of
`tests/orchestration/test_ownership_ledger.py` by `--collect-only -q`: 33. Reviewer's baseline
(the same selection minus this file, at `a0b287a5`, before any change): `1168 passed, 1
skipped`, real exit 0. Account: 1168 + 33 = 1201 — exact match, no other difference.

Then `python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass"}, {"name": "live_review_verdict", "status": "pass"}, {"name": "plan_consistency", "status": "pass"}, {"name": "relevant_untracked", "status": "pass"}, {"name": "repo_root_hygiene", "status": "pass"}, {"name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true}
```
All six `pass`, `fail_count` 0.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f035-r1-mut ca8e00924` (exit 0),
then `python3 -B .agent/authored/f035-r1-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f035-r1-mut`, whole output:
```
control (before any mutation): exit=0 failed=0 failing=[]
m1 ownership_actor maps cli to the door "": exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestActorDoorMapping::test_door_mapping[cli-cli]']
m2 fingerprints numbered in sorted order of their text, not by first appearance: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestTokenNumbering::test_fingerprints_numbered_by_first_appearance_not_text_order']
m3 an injection's auto_approved is always false: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestInjection::test_applied_with_yes_is_auto_approved_and_verbatim_text_survives']
m4 a folded veto's consequence drops its unreachable ids: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestVeto::test_folded_and_control_only_entries_in_one_ledger']
m5 a veto only in the control files is skipped: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestVeto::test_folded_and_control_only_entries_in_one_ledger']
m6 an injection's own _edits entry is read as a plan_edited entry: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestInjection::test_applied_with_yes_is_auto_approved_and_verbatim_text_survives']
m7 a steering record's consequence ignores its marker: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestSteering::test_consumed_note_names_its_task_and_round']
m8 a resume's actor is read from the event's source: exit=1 failed=2 failing=['tests/orchestration/test_ownership_ledger.py::TestRunLog::test_job_resumed_entry_actor_has_no_door_and_names_the_pause_source_in_detail', 'tests/orchestration/test_ownership_ledger.py::TestRunLog::test_task_resumed_entry']
m9 a second pause event for one request id yields a second entry: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestRunLog::test_a_pause_event_written_twice_for_one_request_id_yields_one_entry']
m10 entries with an empty ts sort first: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestSortOrder::test_an_entry_with_empty_ts_sorts_after_every_dated_one']
m11 a veto reader error is swallowed and yields no veto entries: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestVeto::test_an_unreadable_control_file_raises_ownershiperror']
m12 ownership_entry_problems accepts an actor kind outside ACTOR_KINDS: exit=1 failed=1 failing=['tests/orchestration/test_ownership_ledger.py::TestOwnershipEntryProblems::test_an_actor_kind_outside_actor_kinds_is_reported']
control (after every mutation restored): exit=0 failed=0 failing=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every one of the 12 mutations was RED with at least one failing node; none stayed green, so no
test needed adding before C5. Then `git worktree remove --force .remedy-wt/f035-r1-mut` (exit
0), `git worktree prune` (exit 0, no-op), `git worktree list | wc -l`: 61 — equal to step 4's
reading.

**Constraint 3's tracked path set** — `git diff --name-only a0b287a5` at the branch tip after
C5 names: `.agent/authored/f035-r1-block.md`, `.agent/authored/f035-r1-claim.diff`,
`.agent/authored/f035-r1-context.md`, `.agent/authored/f035-r1-mutations.py`,
`.agent/authored/f035-r1-plan.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/handoff.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`,
`packages/orchestration/ownership.py`, `tests/orchestration/test_ownership_ledger.py`,
`tests/test_no_orphan_modules.py` — every one inside the block's constraint 3 list; nothing
under `apps/`, no other `packages/` path, and none of the six explicitly forbidden files.

**G6 TREE AND PUSH** — reported below, since C5 cannot contain its own readings.

## Authored-text proofs

`f035-r1-block.md`, `f035-r1-plan.md`, `f035-r1-context.md` (all copied at `d7e741086`) and
`f035-r1-claim.diff` (copied at `cea469ff8`): each compared disk-to-disk against its committed
`.agent/authored/` copy, read back with `git show`, per the fidelity protocol — all four
byte-identical (readings in G1 TRANSPORT above). `f035-r1-mutations.py` is this round's own
authored tool (not a reviewer payload); no reviewer-authored text applied for C3/C4c beyond
those four.

## Deviations & assumptions

1. **C3 split into C3a/C3b.** The block bundles `packages/orchestration/ownership.py` and the
   `ALLOWED_UNWIRED` line as one commit `C3`. `ownership.py` alone first measured 508 insertions
   — over the 500-line cap by itself, before the guard-file `+3` was even added. It was trimmed
   (four 3-line section banners shortened to 1 line each, one docstring paragraph break removed)
   to 499 insertions, still the same S1-S5 content, then committed alone as **C3a**; the guard
   line followed as **C3b**. Constraint 2 names exactly this split pattern (`C3a and C3b`) for
   this situation, so the split is not itself a rule violation, but the *reason* — the module
   read over the cap on first write and needed shrinking, not merely splitting — is declared
   here per constraint 2 ("say so").
2. **C4 split three ways instead of two.** The block bundles the test file and the mutation
   tool as one commit `C4`, naming `C4a`/`C4b` as the split pattern if it overflowed. The test
   file alone measured 658 insertions, itself over the cap, so it could not be rescued by a
   single split the way C3 was — trimming 658 lines of table-driven, per-class test coverage
   down to under 500 without cutting a test or an assertion was not attempted, since AGENTS.md's
   commit-size rule counts insertions, not test count, and the block's TESTS section orders
   every item this file covers. The bundle was instead split into three commits: **C4a** (the
   178-line mutation tool, standing alone under the cap), **C4b** (the test file's first 445
   lines, cut at a clean class boundary — `TestSteering`'s last blank line — so the file is
   syntactically valid, though not run, at that commit), and **C4c** (the remaining 213 lines,
   completing the file). No test's behaviour or assertions were changed by the split; only where
   the same bytes landed across two commits changed. G3, G4 and G5 all ran against C4c's tip,
   where the file is whole.
3. **Job-scope pause/resume/stop test records use `RunLogWriter.log(...)` directly** rather than
   driving `pingpong_job._append_job_paused_event` / `_append_job_resumed_event` /
   `_append_job_stopped_event` through a full `run_job` simulation. `RunLogWriter.log` is itself
   the real, single writer every one of those production callers uses; the kwargs passed in
   `TestRunLog` mirror, field for field, what each caller's own source (read in full before
   writing any code) passes it. Task-scope pause/resume use the real `pause_control
   .pause_job_command` / `unpause_job_command` end to end, since those do not require a running
   job loop. This keeps the round inside its own scope (round 1 reads records; it does not
   drive the pause/stop machinery, which belongs to F025/F011's own test suites already run in
   G4's selection) while still exercising `ownership.py`'s reader against the exact real event
   shape.
4. **Two veto-answer control files have their `answered_at` patched after a real
   `record_veto_answer()` write**, in `TestTokenNumbering` and `TestSortOrder`, so a fingerprint-
   ordering and a sort-order assertion do not depend on how far apart two real-clock calls land
   in microseconds. The record itself — every other field — is exactly what the real writer
   produced; only the timestamp is overwritten afterward, the same pattern
   `tests/orchestration/test_task_injection.py` already uses (patching a stored record's
   `job_id` directly to test a tamper path).
5. No existing test went red at any point; no correction of this round's own tests was needed
   before C5.

## Next

Per AGENTS.md Phase 1 rule 1 (read `.agent/STOP` from disk) and the block's ordering: review of
round 1, then T001's second half — hunk decisions, decision answers, clarification answers,
plan approval human and unattended, and the ledger written at every job terminal, per DECISION
F035 D1 (6). Open findings: 0. Operator questions: 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 (`.agent/STOP` check) | done | |
| Step 2 (primary checkout, branch cut) | done | |
| Step 3 (block byte verification) | done | |
| Step 4 (worktree count) | done | |
| Payload verification (3 payloads) | done | |
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | deviated | split into C3a/C3b — module alone was over the 500-line cap; see Deviations 1 |
| C4 | deviated | split into C4a/C4b/C4c — test file alone was over the 500-line cap; see Deviations 2 |
| G1 Transport | done | |
| G2 The claim | done | |
| G3 The code | done | |
| G4 The tests | done | |
| G5 The red proofs | done | |
| G6 Tree and push | done | |
| C5 (this handback) | done | |
