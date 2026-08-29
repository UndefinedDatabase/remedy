# Handback — F033 round 14 · THE CLI COMMAND AND ITS HANDLER

## Session

SESSION 4 of feature F033 · round 14 · rounds so far 14

## Range

Review of `34d5e4e48418536bfcd21fd9403403b96ea66220`..`eec2cd4ab4388c1d62195d22317b38222274f927`
(BASE is the round 13 handback commit; C6, the commit carrying this file, is the tip).

Branch `feature/f033-hunk-approval-v2` throughout. `+/-` cells below are `git diff --numstat`,
read from the tool per commit, and they agree cell for cell with the walk G8 performed.

## Commits

### 54dbf6ce docs(f033): save the round 14 block — C0a
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f033-r14.md | +449 -0 | the reviewer's block, copied byte for byte with `shutil.copyfile` |

### 1207790f docs(f033): mirror the round 14 block — C0b
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +302 -261 | the same bytes, read back out of the C0a blob |

### fffa6647 docs(f033): open round 14 in the plan — C1
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16 -19 | PLANF033R14, whole-file |

### 096b8539 docs(f033): book the round 13 verdict and register R-0743 — C2
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | RECORDF033R14 appended: the R13 `Gate:` entry and the R-0743 registration |

### 0d2c98c0 docs(f033): record the round 13 prose slip — C3
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 -0 | SLIPSF033R14 appended |

### ca938ff4 feat(f033): add the approve-hunks command and its handler — C4
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +37 -0 | three arg shorthands and the `patch.approve-hunks` entry |
| apps/cli/commands/patch.py | +112 -0 | `_split_hunk_rejection`, `_cmd_approve_hunks`, the `COMMAND_HANDLERS` entry |
| tests/test_command_catalog.py | +3 -2 | the equality guard widened from 6 to 7 in the SAME commit as the entry |

### eec2cd4a test(f033): pin the evidence-dir precedence and the approve-hunks handler — C5
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_patch_cmd.py | +292 -0 | NEW — 11 tests over the handler, named after `apps/cli/commands/patch.py` |
| tests/orchestration/test_evidence_index.py | +14 -0 | the R-0743 precedence pin, one added test |
| .agent/live_review.md | +2 -0 | the one ordered `Landed: R-0743 — …` line |

### C6 docs(f033): hand back the round 14 CLI command
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | the handback; a handoff cannot table the commit that writes it (R-0149) |

## External actions

- `git worktree add --detach .remedy-wt/base-g6 34d5e4e4` — created, used ONLY to read G6(d)'s
  BASE catalog and handler counts.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/base-g6` then `git worktree prune`
  — removed by exact path; `git worktree list` back to the primary checkout alone.
- `git worktree add --detach .remedy-wt/g7-c5 eec2cd4a` — created for the G7 mutations.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/g7-c5` then `git worktree prune`
  — removed by exact path; `git worktree list` back to the primary checkout alone.
- `git push -u origin feature/f033-hunk-approval-v2` — the round's FINAL action, run immediately
  after C6. Its outcome cannot be recorded in the file it pushes (the write-once rule forbids a
  second handoff commit), so it is reported in the round report instead; a reader auditing it
  reads `git log origin/feature/f033-hunk-approval-v2 -1` and expects the C6 sha.
- No PR created, none merged, no `gh` command run. No force-push, no history rewrite, no branch
  deleted.

## Verification

ONE LINE PER GATE, real exit codes and real numbers.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a: absent; read again before C6:
  absent. `git status --porcelain` empty after every one of C0a, C0b, C1, C2, C3, C4, C5 and
  after both worktree removals. Branch `feature/f033-hunk-approval-v2` throughout;
  `git rev-parse feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
  unchanged; the branch reflog shows seven plain `commit:` entries and no forced update.
- **G2 TRANSPORT — PASS.** `54dbf6ce:.agent/authored/f033-r14.md` is 33129 bytes, sha256
  `9c373cd2076dc69440904aa2beb925afd1b139255655feca01e56ca7aec322ca`;
  `.remedy-wt/f033-r14-block.md` is 33129 bytes, same sha256; EQUAL = True.
  `git rev-parse 1207790f:.agent/authored/f033-r14.md` and
  `git rev-parse 1207790f:.agent/last_block.md` both print `9ef207de42099f7ceebaa64bf0bd084aa9943065`
  — ONE blob id.
- **G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob 1517848 bytes (== the ordered 1517848),
  plus one newline plus RECORDF033R14 at 7219 bytes = 1525068, and the C2 blob is 1525068 bytes
  and byte-EQUAL to that reconstruction; BASE is a byte PREFIX = True; ends in exactly one
  newline = True. (b) N COUNTED by the script = 2; the LAST 2 blank-line units of the C2 blob
  equal the slice's two paragraphs IN ORDER (unit 0 = 5164 bytes, `Gate: F033 R13 — …`; unit 1 =
  2052 bytes, `- R-0743 — Low, …`). First appended paragraph's BYTE span computed as
  [1517849, 1523013), length 5164 == len(first paragraph), and `C2[span] == first paragraph`.
  NEGATIVE CONTROL at byte offset 1520431, proved inside that span; reader 1 (byte
  reconstruction) rejects it and reader 2 (last-N paragraphs) rejects it — BOTH reject.
- **G4 THE LEDGER at C2 and C5 — PASS.** BASE: registered 303 (303 distinct), `Done:` 48 lines
  over 46 distinct, `Landed:` 15, `Gate:` 130, `^Gate: F033 R13 — ` 0, `DECISION F033 D` 4, open
  set 257. C2: registered 304 with the ADDED id exactly `R-0743`, `Done:` 48/46, `Landed:` 15,
  `Gate:` 131 with `^Gate: F033 R13 — ` exactly 1, `DECISION F033 D` 4, open set 258. C5:
  registered 304 (no id added), `Done:` 48/46, `Landed:` 16 with `^Landed: R-0743 — ` exactly 1,
  `Gate:` 131, `DECISION F033 D` 4, open set 258. Every ordered reading met.
- **G5 THE PROSE FILES — PASS.** `.agent/plan.md` at C1 is 2479 bytes over 46 lines, byte-EQUAL
  to PLANF033R14, and 46 < the 50-line cap AGENTS.md sets. `.agent/prose_slips.md`: BASE blob
  23793 bytes (== the ordered 23793), plus one newline plus SLIPSF033R14 at 472 bytes = 24266,
  and the C3 blob is 24266 bytes and byte-EQUAL; BASE a byte PREFIX = True; ends in exactly one
  newline = True. `^2026-\d\d-\d\d · F033 R13 · ` lines: 0 at BASE, 1 at C3. Lines beginning
  `- R-` in the whole file at C3: 0.
- **G6 THE CATALOG AND ITS GUARD at C4 — PASS.** (a) `python3 -m ruff check
  apps/cli/command_catalog.py apps/cli/commands/patch.py tests/test_command_catalog.py` — REAL
  exit 0, summary line `All checks passed!`. (b) `get_command("patch.approve-hunks")`:
  group_id `patch`, subcommand `approve-hunks`, action_class `approval_gate`, supports_json
  True, may_mutate_repo **False**, requires_permission **False**; args NAMES in order
  `['job_id', '--task-run', '--approve-hunk', '--reject-hunk', '--json']`; the args carrying
  `is_repeatable` are `['--approve-hunk', '--reject-hunk']`. (c)
  `len(get_commands_for_group("patch"))` = 7, sorted subcommand set
  `['apply', 'approve', 'approve-hunks', 'list', 'reject', 'revert', 'show']`, and
  `"patch.approve-hunks" in collect_all_handlers()` = True at THIS commit. (d) BASE:
  `len(CATALOG)` 340, `len(collect_all_handlers())` 340, catalog ids with NO handler 0. C4:
  `len(CATALOG)` 341, `len(collect_all_handlers())` 341, catalog ids with NO handler 0. (e)
  `sorted(UI_EXPOSED_COMMANDS)` at C4 = `['decision.resolve', 'job.stop']` — the write door is
  NOT opened this round.
- **G7 THE MUTATION RED-PROOFS at C5 — PASS, all four RED.** In the disposable worktree
  `.remedy-wt/g7-c5` at `eec2cd4a`, never in the primary checkout, every run `python3 -B` with
  `PYTHONDONTWRITEBYTECODE=1`. IMPORT PATH PROOF (exit 0):
  `apps.cli.commands.patch.__file__` = `…/.remedy-wt/g7-c5/apps/cli/commands/patch.py` and
  `packages.orchestration.evidence_index.__file__` = `…/.remedy-wt/g7-c5/packages/orchestration/evidence_index.py`
  — both under the worktree. UNMUTATED CONTROLS: `tests/cli/test_patch_cmd.py` REAL exit 0, 11
  passed; `tests/orchestration/test_evidence_index.py` REAL exit 0, 33 passed — 33 EXCEEDS the
  32 BASE gives. Each anchor asserted UNIQUE (count == 1) inside its named file before
  replacement, and each file restored to its exact pre-mutation sha256 afterwards with the
  control re-run returning to 11 / 33 passed.
  - (i) `save_job` on the refusal path too, in `apps/cli/commands/patch.py` — REAL exit 1, 1
    failed, 10 passed; failing test
    `tests/cli/test_patch_cmd.py::TestItMintsNoRefusalVocabularyOfItsOwn::test_a_refusal_never_persists_the_job`.
  - (ii) split each `--reject-hunk` value on its LAST `=` (`partition` → `rpartition`), in
    `apps/cli/commands/patch.py` — REAL exit 1, 3 failed, 8 passed; failing tests
    `TestTheHappyPath::test_a_mixed_decision_lands_under_the_envelope_derived_attempt_key`,
    `TestTheHappyPath::test_a_rejection_reason_survives_verbatim`,
    `TestItMintsNoRefusalVocabularyOfItsOwn::test_a_reject_value_with_no_equals_is_the_cores_missing_reason`.
  - (iii) `task_id` and `attempt` passed to the recorder the other way round, in
    `apps/cli/commands/patch.py` — REAL exit 1, 4 failed, 7 passed; failing tests
    `TestTheHappyPath::test_a_mixed_decision_lands_under_the_envelope_derived_attempt_key`,
    `TestTheHappyPath::test_a_rejection_reason_survives_verbatim`,
    `TestTheHappyPath::test_a_task_run_scope_keys_on_that_runs_own_artifact`,
    `TestTheHappyPath::test_json_output_is_the_exported_record`.
  - (iv) the relative-fallback branch moved ABOVE the `try` in
    `packages/orchestration/evidence_index.py`, so the CWD directory is consulted first — REAL
    exit 1, 1 failed, 32 passed; failing test
    `tests/orchestration/test_evidence_index.py::TestResolveJobEvidenceDir::test_the_index_record_beats_the_cwd_relative_fallback`.
    This is R-0743's proof: GREEN at `55c365d6`, RED now, and it kills exactly the one added test.
  Worktree removed BY EXACT PATH `/home/decodeux/Repos/remedy/.remedy-wt/g7-c5`, then
  `git worktree prune`; `git worktree list` shows the primary checkout alone.
- **G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, `-q -p no:randomly`,
  every REAL exit 0: `tests/cli/test_patch_cmd.py` 11 passed (NEW file, 0 at BASE);
  `tests/orchestration/test_evidence_index.py` 33 passed (32 at BASE, +1 = the R-0743 pin);
  `tests/test_command_catalog.py` 18 passed (18 at BASE, unmoved — the guard was WIDENED, not
  split); `tests/cli/test_command_catalog.py` 23 passed (23 at BASE, unmoved);
  `tests/test_grouped_cli.py` 511 passed at C5 — 511 at BASE, so it did NOT move, exactly as the
  block predicted from its parametrization over GROUPS rather than commands;
  `tests/ui_server/test_command_channel.py` 106 passed (106 at BASE, unmoved — the write door is
  untouched); canary `tests/cli/test_golden_path.py` 42 passed (42 at BASE, unmoved).
  COMMIT WALK `git rev-list --reverse BASE..C5` — seven commits, each with exactly ONE parent,
  each under 500 INSERTIONS counted from the `+` column of `git diff --numstat`:
  `54dbf6ce` 449, `1207790f` 302, `fffa6647` 16, `096b8539` 4, `0d2c98c0` 2, `ca938ff4` 152,
  `eec2cd4a` 308. PATH SET, both directions: touched-but-not-in-the-change-set = `[]`;
  in-the-change-set-but-not-touched = `['.agent/handoff.md']`, which C6 writes and no gate at C5
  can see (declared below). 10 paths touched. MARKER RESIDUE, `<<<SLICE ` / `<<<END `:
  `.agent/plan.md` 0/0, `.agent/prose_slips.md` 0/0, `apps/cli/command_catalog.py` 0/0,
  `apps/cli/commands/patch.py` 0/0, `tests/cli/test_patch_cmd.py` 0/0, against the non-zero
  CONTROL `.agent/authored/f033-r14.md` at 5/6. `git ls-files .remedy-wt` = 0 entries.
  DO-NOT-TOUCH, blob id at BASE vs C5, one line per path, all 13 of 13 identical:
  `hunk_decision_record.py` `0563c5a00660`, `hunk_ledger.py` `57c00fcfde62`,
  `hunk_approval.py` `25d1a8d0d08d`, `hunk_apply.py` `195f0d223210`,
  `hunk_subset_diff.py` `6c47c2083795`, `diff_view_source.py` `30a86b1b977d`,
  `diff_parser.py` `b6632f657426`, `ui_server.py` `068721f8adf0`,
  `apps/cli/grouped.py` `c9c5265d0b87`, `tests/ui_server/test_command_channel.py` `7ff931e2f005`,
  `docs/roadmap/STATUS.md` `a370be066b7a`, `packages/orchestration/evidence_index.py`
  `4d797b53312a`, `.agent/context.md` `4e3a3f2d9c3f`.

## What landed, in the block's own terms

THE CATALOG ENTRY, fields quoted from G6(b): `command_id` `patch.approve-hunks`, `group_id`
`patch`, `subcommand` `approve-hunks`, `description` "Record a hunk-level approve and reject
decision over a job's diff.", `action_class` `approval_gate`, `args`
`(_JOB_ID, _TASK_RUN_OPT, _APPROVE_HUNK_OPT, _REJECT_HUNK_OPT, _JSON_OPT)`, `supports_json`
True, `may_mutate_repo` False, `requires_permission` False, `related`
`("patch.approve", "patch.apply")`. `--task-run` is a valued option and NOT `_TASK_OPT`, with a
comment saying why: `build_diff_view` requires exact membership in the real `task_runs/` listing
and does no prefix resolution, so promising a prefix match would be worse than a second option
name. `--approve-hunk` and `--reject-hunk` are `is_repeatable=True`, and `--reject-hunk`'s help
states and SHOWS the shape `<hunk-id>=<reason>`. All five arg helps and the description were
checked against the list `TestCatalogSensitivity` actually holds in
`tests/test_command_catalog.py` — the eight `FORBIDDEN` terms and the three token-boundary
`FORBIDDEN_PREFIXES` — and that class passes as part of the 18.

THE HANDLER'S `COMMAND_HANDLERS` LINE, verbatim as shipped:

    "patch.approve-hunks": lambda args: _cmd_approve_hunks(
        args.job_id,
        task_run=getattr(args, "task_run", None),
        approve=getattr(args, "approve_hunk", None),
        reject=getattr(args, "reject_hunk", None),
        json_output=getattr(args, "json", False),
    ),

THE TESTS WRITTEN, with the property each pins:

`tests/cli/test_patch_cmd.py` (11):
- `TestItIsWiredIntoTheCli::test_the_command_id_resolves_in_the_catalog` — the entry exists under
  `patch` with `supports_json` and neither capability flag set.
- `TestItIsWiredIntoTheCli::test_the_handler_is_registered` — the discriminator for
  `Error: no handler for patch.approve-hunks`.
- `TestTheHappyPath::test_a_mixed_decision_lands_under_the_envelope_derived_attempt_key` — the
  key is `job:workspace.diff`, BOTH halves from the envelope; the three hunks land
  approved/rejected/pending; unrelated metadata survives; the record is read back with
  `load_job`, so `save_job` really persisted it. Kills mutations (ii) and (iii).
- `TestTheHappyPath::test_a_rejection_reason_survives_verbatim` — the split is on the FIRST `=`
  and both halves are kept verbatim; the reason itself carries an `=` and leading/trailing
  spaces. Kills mutations (ii) and (iii).
- `TestTheHappyPath::test_a_task_run_scope_keys_on_that_runs_own_artifact` — `--task-run` passes
  through UNCHANGED, so the key becomes `T001:task_runs/T001/safe.diff`. Kills mutation (iii).
- `TestTheHappyPath::test_json_output_is_the_exported_record` — `--json` prints parseable JSON on
  the SUCCESS path and it equals what is on the job. Kills mutation (iii).
- `TestItMintsNoRefusalVocabularyOfItsOwn::test_a_reject_value_with_no_equals_is_the_cores_missing_reason`
  — the refusal `code` is `hunk_approval.REFUSAL_MISSING_REASON`, not a handler-minted one; exit
  1; nothing recorded. Kills mutation (ii).
- `TestItMintsNoRefusalVocabularyOfItsOwn::test_an_unresolvable_evidence_directory_is_no_diff_available`
  — `no_diff_available`, the envelope's own `evidence_dir_unavailable` quoted into the message,
  and NOTHING written.
- `TestItMintsNoRefusalVocabularyOfItsOwn::test_a_refusal_never_persists_the_job` — THE
  discriminator for "a refused decision is not a decision": the on-disk record is unchanged
  either way, so the test watches `save_job` itself. Kills mutation (i).
- `TestItMintsNoRefusalVocabularyOfItsOwn::test_a_human_refusal_goes_to_stderr_with_the_offending_ids`
  — `Error: <message>` on stderr plus the offending ids.
- `TestItMintsNoRefusalVocabularyOfItsOwn::test_an_unknown_job_id_exits_1` — the
  `JobNotFoundError` branch.

`tests/orchestration/test_evidence_index.py` (+1, 32 → 33):
- `TestResolveJobEvidenceDir::test_the_index_record_beats_the_cwd_relative_fallback` — with BOTH
  an index record naming an existing directory AND a real `remedy-job-evidence-j7` directory in
  the CWD, the INDEX record wins. It is the first case in that suite to construct both sources at
  once, which is the only state in which precedence is observable. G7(iv) is its red-proof.

## Authored-text proofs

Three reviewer-authored slices applied, every one extracted from the COMMITTED C0a blob per
convention 4 and never retyped:

- PLANF033R14 → `.agent/plan.md` at C1: 2479 bytes, byte-EQUAL to the slice, disk-to-disk
  comparison against `54dbf6ce:.agent/authored/f033-r14.md` = True.
- RECORDF033R14 → `.agent/live_review.md` at C2: 7219 bytes, appended as base + one newline +
  slice, reconstruction byte-EQUAL to the C2 blob at 1525068, BASE a byte PREFIX.
- SLIPSF033R14 → `.agent/prose_slips.md` at C3: 472 bytes, reconstruction byte-EQUAL to the C3
  blob at 24266, BASE a byte PREFIX.

The block itself: `.remedy-wt/f033-r14-block.md` → `.agent/authored/f033-r14.md` by
`shutil.copyfile`, 33129 bytes, sha256 unchanged, and mirrored to `.agent/last_block.md` under
ONE blob id — see G2.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it | done | |
| C1 `.agent/plan.md` | done | |
| C2 the R13 verdict AND the R-0743 registration | done | |
| C3 one dated prose slip | done | |
| C4 catalog entry + widened guard + handler, ONE commit | done | |
| C5 the R-0743 precedence pin and the handler's tests | deviated | the ordered `Landed: R-0743` line cannot name C5's own sha; see D1 |
| C6 the handback | done | this file |
| G1 HYGIENE | done | |
| G2 TRANSPORT | done | |
| G3 THE RECORD APPEND at C2 | done | |
| G4 THE LEDGER at C2 and C5 | done | |
| G5 THE PROSE FILES | done | |
| G6 THE CATALOG AND ITS GUARD at C4 | done | |
| G7 THE MUTATION RED-PROOFS at C5 | done | all four RED |
| G8 SUITES AND STRUCTURE | deviated | `.agent/handoff.md` is in the change set but unreachable to a C5 path-set reading; see D2 |
| R-0743 fix | done | one added test; `evidence_index.py` byte-identical BASE→C5 |
| SPEC `apps/cli/command_catalog.py` | done | |
| SPEC `tests/test_command_catalog.py` | done | |
| SPEC `apps/cli/commands/patch.py` | deviated | the SPEC's step-3 argument; see D3 |
| SPEC `tests/orchestration/test_evidence_index.py` | done | |
| SPEC `tests/cli/test_patch_cmd.py` | done | 11 tests, idiom taken from `tests/cli/test_job_stop.py` and `tests/cli/test_decision_answers.py` |

## Deviations & assumptions

**D1 — the `Landed: R-0743` line cannot name its own commit.** The Bundle places that line IN
C5, and every existing `Landed:` line in `.agent/live_review.md` names a SHA. A commit cannot
carry its own id, so ordering one would be ordering an unknowable value. The line therefore names
the commit BY ROLE — "at C5 of F033 round 14 — the commit this line lands in, whose sha the round
14 handback names, because a commit cannot carry its own id" — and the sha is
`eec2cd4ab4388c1d62195d22317b38222274f927`, stated here. The GATE is satisfied exactly:
G4 orders `^Landed: R-0743 — ` and counts it at 1 at C5. The line also claims NO mutation result,
because G7 runs after C5 and an unmeasured claim has no business in the append-only record; the
mutation result is in this handback's G7 line instead.

**D2 — G8's path-set reading cannot see `.agent/handoff.md`.** G8 orders the range's path set
against the change set in BOTH directions, and it runs over `BASE..C5`. `.agent/handoff.md` is in
the change set and is written by C6, so the "in the change set but NOT touched" side reports it
and always will. Reported honestly in both directions rather than quietly excluded; nothing else
is missing on either side. This is checklist item 14's shape and was declared the same way at
round 13.

**D3 — the SPEC's step 3 passes the operator's RAW argument, not the resolved job id.** The SPEC
fixes `evidence_index.resolve_job_evidence_dir(job_id_str)`, and step 1 has by then already
resolved that same string to a UUID with `resolve_job_id`. I implemented the SPEC literally,
because names and signatures it fixes are binding and no gate reads this call. The CONSEQUENCE,
recorded so the next round decides rather than discovers it: a SHORT PREFIX job id
(`remedy patch approve-hunks abc123`) loads the job fine — `resolve_job_id` resolves prefixes —
but `resolve_job_evidence_dir` looks for an index file literally named `abc123.json`, finds none,
and the operator gets `no_diff_available` for a job whose diff exists. `str(job_id)` would resolve
both. This is a SPEC observation, not a gate/SPEC disagreement, and it was NOT silently fixed.

**D4 — no `docs/` update.** AGENTS.md's Documentation Updates rule fires on "a feature introduces
new behavior that is not yet documented", and `remedy patch approve-hunks` is new operator-facing
behaviour. The block's change set names eleven paths and no file under `docs/`, and scope control
forbids touching a path the block did not name. No docs file was edited; the obligation is
carried forward to the round that opens the write door or to F033's closure.

**D5 — mutations (ii) and (iii) each kill more than one test.** The block asks for "the NAME of
each failing test" and does not require a single-test kill, so this is reported as information
rather than as a problem: (ii) kills 3, (iii) kills 4, while (i) and (iv) each kill exactly 1.
Every listed name is a test whose property the mutation genuinely breaks.

No other deviation. The block's ordered commit sequence was followed exactly — seven commits,
C0a, C0b, C1, C2, C3, C4, C5, in that order, plus this C6 — with no extra commit, none dropped
and no reordering. I wrote NO `Done:` paragraph and NO verdict on this round's work.

## Next

SESSION 4 carries forward. The next session's first actions, in this order:

1. Read `.agent/STOP` from disk.
2. Run the Open PR Gate — `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Book this round's verdict into `.agent/live_review.md` and RESOLVE R-0743, replacing the
   `Landed: R-0743 — …` line at `eec2cd4a` with the reviewer's authored `Done:` text.
4. Then the plan's step 2 — the write door: expose `patch.approve-hunks` in
   `UI_EXPOSED_COMMANDS` (still exactly `["decision.resolve", "job.stop"]` today, measured by
   G6(e) at C4) and add its dispatch, widening the `DOOR_METHODS` and `ALLOWED_IMPORTS` equality
   guards in `tests/ui_server/test_command_channel.py` in the SAME commit, and adding
   `packages.orchestration.hunk_apply` to `FORBIDDEN_MODULES` so DECISION F033 D4's forbidden
   mistake cannot be made silently later.
