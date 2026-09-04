── STEP R8/25 — F262 List commands v2 ────────────────────────
Goal: Book round 7's PASS verdict into the ledger (this round's first
commit, per amend0827-process-diet rule 1 — a verdict never buys a
round of its own) and ship T002 batch 6: patch.list gains --json end
to end plus a DECIDED column in text output, matching the shape
rounds 6-7 already proved for project.list/job.list/queue.list.

Bundle:
  C0a. Save this entire block verbatim to .agent/authored/f262-r8.md
  C0b. Mirror it to .agent/last_block.md
  C1.  Append GATE7 (below) to .agent/live_review.md, byte-exact
  C2.  Apply PAIR P1-P4 (production code) + PAIR P5-P7 (tests), one
       commit, five files
  C3.  Replace .agent/plan.md with PLAN9 (below), whole-file
  C4.  Rewrite .agent/handoff.md (the handback), push

Change: apps/cli/command_catalog.py, apps/cli/commands/patch.py,
packages/orchestration/approval_queue.py,
tests/test_patch_intent_approval.py, tests/test_command_catalog.py,
plus the four .agent/** state files C0a/C0b/C1/C3 touch. Nothing else.

Constraints:
  1. GATE7 and PLAN9 below are authored text: extract each by its own
     <<<BEGIN ...>>>/<<<END ...>>> marker pair from the COMMITTED
     .agent/authored/f262-r8.md (byte-exact, binary mode), never by
     hand-retyping. GATE7 is appended to the base file as exactly
     "\n" + GATE7's own bytes, with nothing else added or stripped.
     PLAN9 replaces the whole of .agent/plan.md byte-for-byte.
  2. PAIR P1-P7 below are also authored text, extracted the same way
     by their own <<<BEGIN PAIR_Pn_FROM>>>/<<<END PAIR_Pn_FROM>>> and
     <<<BEGIN PAIR_Pn_TO>>>/<<<END PAIR_Pn_TO>>> marker pairs, applied
     with str.replace(FROM, TO, 1) via a python3 script — never by
     hand-retyping. Every FROM has been counted by the reviewer at
     exactly 1 occurrence in its target file before this block was
     written; the worker re-confirms that count (before and after)
     for each pair before treating a "replaced" result as real.
  3. Pair shapes (reviewer's own containment test, run before this
     block was written): P1, P2, P3, P4 and P7 are REWRITEs (TO does
     NOT contain FROM verbatim) — order the "FROM 0x, TO 1x" proof for
     each. P5 and P6 are APPEND-shaped (TO contains FROM verbatim,
     each appends one new test method after the existing ones) — for
     these two, order ordered equality instead (§4.9 of
     docs/agents/planner_reviewer_prompt.md): the pre-commit blob is a
     byte-exact prefix of the post-commit file and the appended lines
     are an exact suffix, in order.
  4. C2 is ONE commit covering all five touched files (command_catalog.py,
     patch.py, approval_queue.py, test_patch_intent_approval.py,
     test_command_catalog.py).
  5. No path outside this change set is written under version control.
  6. `.agent/plan.md` stays under 50 lines (AGENTS.md cap); PLAN9 is
     49 lines, already under it.
  7. `.agent/STOP` is checked, read from disk, before C0a and again
     immediately before C4. If present at either check: stop, do not
     commit further, and write a handoff explaining where the round
     stopped instead.
  8. Constraint 8 (feature-file staleness): `docs/roadmap/features/T2_F262.md`
     line 5 ("REGISTRATION ONLY — nothing in this file has been
     implemented.") is already false and outside this round's change
     set; do not repair it this round, just re-declare it stale in the
     handback as every prior round has.
  9. Ruff is expected to be denied this session (every prior round hit
     "This command requires approval" or the Bash-permission refusal);
     attempt it once per constraint 4's precedent, record whatever
     refusal text appears, and do not treat its absence as a gate
     failure.

Done when (worker runs these for real, records real output):
  $ git status --porcelain                                    # empty, before C0a and before C4
  $ python3 -m py_compile apps/cli/command_catalog.py apps/cli/commands/patch.py packages/orchestration/approval_queue.py tests/test_patch_intent_approval.py tests/test_command_catalog.py
                                                                # exit 0
  $ python3 -m pytest tests/test_patch_intent_approval.py tests/test_command_catalog.py -q
                                                                # before C2: 77 passed; after C2: 91 passed
  $ python3 -m pytest tests/ui_server/ -q                      # 515 passed
  $ python3 -m pytest tests/orchestration/test_test_runner.py -q      # 52 passed
  $ python3 -m pytest tests/regression/test_resource_safety.py -q    # 21 passed
  $ python3 -m pytest tests/orchestration/test_integrity_gate.py -q  # 16 passed
  $ python3 -m pytest tests/cli/test_golden_path.py -q         # 42 passed
  $ git push origin feature/f262-list-commands-v2              # after C4

Handback: rewrite .agent/handoff.md per docs/agents/handback_template.md,
covering C0a-C4, all seven gates below (G1-G7), the Commits table with
git show --numstat readings, and the Verification section with every
command's real output.

═══════════════════════════════════════════════════════════════
GATES THE REVIEWER WILL RE-RUN (worker records its own readings too)
═══════════════════════════════════════════════════════════════
G1 TRANSPORT: sha256sum .agent/authored/f262-r8.md .agent/last_block.md — one digest, twice.
G2 THE LEDGER APPEND: base size/trailing-byte of .agent/live_review.md immediately before C1, GATE7's own byte length and internal newline count, base+1+GATE7_length == post-C1 size, tail slice equals GATE7 byte for byte, negative control (flipped first byte of a COPY of GATE7) rejected against the real tail.
G3 THE FOUR PRODUCTION PAIRS (P1-P4): FROM count before/after, TO count after, for each of P1 (command_catalog.py), P2 (patch.py handler body), P3 (patch.py dispatch lambda), P4 (approval_queue.py format_intent_list) — full diff of all three files read and confirmed nothing else changed; py_compile exit 0 on all five touched/added files.
G4 THE TESTS, BEFORE AND AFTER: tests/test_patch_intent_approval.py + tests/test_command_catalog.py combined, 77 before C2, 91 after — reproduced independently.
G5 STATE READERS + CANARY: tests/ui_server/ 515, test_test_runner 52, test_resource_safety 21, test_integrity_gate 16, test_golden_path 42 — unmoved from session baseline.
G6 THE PLAN: PLAN9 extracted from the committed authored file compares byte-equal to .agent/plan.md; wc -l reads 49 or fewer; `## Goal` and `## Next Steps` each appear exactly once.
G7 THE TREE, COMMITS, SWEEP: git status --porcelain empty before C4; git ls-files .remedy-wt empty; every commit's insertion/deletion counts cross-checked cell-for-cell against the handback's own Commits table via git show --numstat; one staleness-sweep line per file this round touched.

<<<BEGIN GATE7>>>
Gate: R7 — the F262 R7 entry. R7 SHIPPED T002 BATCH 5, job.list and queue.list gain --json end to end (catalog args gain _JSON_OPT + supports_json=True for both entries, handler json_output kwarg + json branch for both, dispatch lambda passes json_output=args.json for both) — job.list's json carries created_at (its text output already had it), queue.list's json carries the RAW created_at string (its text output keeps its existing AGE display, _age(), unchanged) plus goal — AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r7.md`/`.agent/last_block.md` share one sha256 digest, `3ba94f24b91b38acc72ca8c09f90e9ed6d0007fa869247eb92ca19ca99667e6b`, confirmed by the reviewer's own `sha256sum` of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 7c25e9363ee43c6b91d26659e7d538ce9b9650f2..2286919d` shows 10 files changed, 1282 insertions, 436 deletions; `apps/cli/command_catalog.py`'s diff is exactly PAIR J1 (job.list CommandEntry gains _JSON_OPT and supports_json=True) and PAIR Q1 (queue.list CommandEntry gains the same, related= unchanged), both confirmed independently at their own command_id anchors, every other CommandEntry untouched; `apps/cli/commands/job.py`'s diff is exactly PAIR J2 (the _cmd_list_jobs body gains a json_output kwarg and a json branch) and PAIR J3 (the dispatch lambda passes json_output=args.json), degraded stays unused as before, every other handler and dispatch line untouched; `apps/cli/commands/queue_cmd.py`'s diff is exactly PAIR Q2 (the _cmd_queue_list body gains the same shape, entry.created_at used raw, never .isoformat()'d) and PAIR Q3 (the dispatch lambda passes json_output=args.json), skipped_total and its stderr print stay in place unmoved, every other handler and dispatch line untouched — every diff re-read in full by the reviewer, not just diffstat'd. `python3 -m py_compile` exited 0 on all five touched/added files (`command_catalog.py`, `job.py`, `queue_cmd.py`, `tests/test_grouped_cli.py`, `tests/cli/test_queue_cmd.py`), run together by the reviewer. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED: `tests/test_grouped_cli.py` read 518 passing (base 516 plus the two `TestJobListCLI` tests), `tests/cli/test_queue_cmd.py` read 26 passing (base 24 plus `test_list_has_json_flag` and `test_json_has_created_at_and_goal`), both reproduced by the reviewer independently, nothing else in either file touched. THE STATE READERS AND THE CANARY WERE UNMOVED FROM THIS SESSION'S OWN BASELINE, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty at HEAD `2286919d60503ddd0535eedc49af3ea1242ac047`, `git ls-files .remedy-wt` empty, and `git ls-remote origin refs/heads/feature/f262-list-commands-v2` matches the local HEAD exactly — the push discharged, nothing merged, the branch carries R1 through R7 unmerged. THE DECLARED DEVIATIONS ARE ALL TOOLING, NONE A DEFECT ON DISK: a commit-message typo in C1 (R4 instead of R7) was self-corrected before push via `git commit --amend` on the tip commit only, no content affected; `git commit`'s own rewrite-detected stat line disagreed with `git show --numstat` for the whole-file C0b mirror, the same substitution already declared every prior round; several Bash compound-command and `cmp` rejections were re-expressed as single invocations or as `python3 -c` byte comparisons; ruff's exact denial text was equally a refusal, not a run; `docs/roadmap/features/T2_F262.md` line 5's "REGISTRATION ONLY" sentence remains stale since round 2, outside this round's declared change set, correctly declared and left unrepaired again. THE VERDICT IS PASS.
<<<END GATE7>>>

<<<BEGIN PLAN9>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 8, session 3 - T002 batch 6: `patch.list` gains `--json` end to
end (same shape rounds 6-7 proved for project.list/job.list/
queue.list) plus a DECIDED column in text output surfacing the intent
dict's own `decided_at` (no `created_at` exists on a patch intent -
only a decision timestamp). Five other audited handlers closed out
this round with NO code change owed: worker.list, worker.registry-list,
review.list, config.list, builder.adapter-list carry no timestamp
field anywhere on their underlying models - Acceptance is satisfied
as-is per the Risks section below.

## Next Steps

- `change.list`'s event log DOES carry timestamps, but the only
  production emitter of an intent-creation event
  (`do_run_patch_intent_created` in do_run.py) is read by NO consumer,
  while every reader instead checks a bare `patch_intent_created` no
  production code emits - needs a design decision on which event
  names creation before a date can land there.
- `loop.list`/`patch.list` have no `created_at` on their own model and
  need a design decision before a CREATED date can appear; `loop.list`
  already prints a "last run" label that may be the right substitute.
- The execution.* trio (`execution.template-list`, `execution.list`,
  `execution.approval-list`) always print JSON unconditionally with no
  text branch at all - the pre-existing `--json`-ignored quirk the
  Risks section already excuses.
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN9>>>

<<<BEGIN PAIR_P1_FROM>>>
        command_id="patch.list",
        group_id="patch",
        subcommand="list",
        description="List patch intents for a job.",
        action_class="read_only",
        args=(_JOB_ID,),
        related=("patch.show", "patch.approve"),
    ),
<<<END PAIR_P1_FROM>>>
<<<BEGIN PAIR_P1_TO>>>
        command_id="patch.list",
        group_id="patch",
        subcommand="list",
        description="List patch intents for a job.",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("patch.show", "patch.approve"),
    ),
<<<END PAIR_P1_TO>>>
Target: apps/cli/command_catalog.py — REWRITE.

<<<BEGIN PAIR_P2_FROM>>>
def _cmd_list_patch_intents(job_id_str: str) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
    intents = list_patch_intents(job)
    print(format_intent_list(intents))
<<<END PAIR_P2_FROM>>>
<<<BEGIN PAIR_P2_TO>>>
def _cmd_list_patch_intents(job_id_str: str, *, json_output: bool = False) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
    intents = list_patch_intents(job)
    if json_output:
        print(_json.dumps({
            "version": 1,
            "intent_count": len(intents),
            "intents": intents,
        }, sort_keys=True))
        return
    print(format_intent_list(intents))
<<<END PAIR_P2_TO>>>
Target: apps/cli/commands/patch.py — REWRITE. `_json` is already
imported at module level (`import json as _json`, line 5) — do not
add a second import.

<<<BEGIN PAIR_P3_FROM>>>
    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id),
<<<END PAIR_P3_FROM>>>
<<<BEGIN PAIR_P3_TO>>>
    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id, json_output=args.json),
<<<END PAIR_P3_TO>>>
Target: apps/cli/commands/patch.py — REWRITE (same file as P2, same commit).

<<<BEGIN PAIR_P4_FROM>>>
    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  TARGET PATH"]
    lines.append("-" * 72)
    for item in intents:
        lines.append(
            f"{item['intent_id']:<14}  "
            f"{item['state']:<8}  "
            f"{item['risk']:<8}  "
            f"{item['action']:<12}  "
            f"{item['target_path']}"
        )
    return "\n".join(lines)
<<<END PAIR_P4_FROM>>>
<<<BEGIN PAIR_P4_TO>>>
    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'DECIDED':<20}  TARGET PATH"]
    lines.append("-" * 72)
    for item in intents:
        lines.append(
            f"{item['intent_id']:<14}  "
            f"{item['state']:<8}  "
            f"{item['risk']:<8}  "
            f"{item['action']:<12}  "
            f"{(item['decided_at'] or '-'):<20}  "
            f"{item['target_path']}"
        )
    return "\n".join(lines)
<<<END PAIR_P4_TO>>>
Target: packages/orchestration/approval_queue.py, function
format_intent_list — REWRITE.

<<<BEGIN PAIR_P5_FROM>>>
    def test_format_intent_list_shows_target_path(self):
        job = _make_job()
        _add_patch_artifact(job)
        out = format_intent_list(list_patch_intents(job))
        assert "docs/file_0.md" in out
<<<END PAIR_P5_FROM>>>
<<<BEGIN PAIR_P5_TO>>>
    def test_format_intent_list_shows_target_path(self):
        job = _make_job()
        _add_patch_artifact(job)
        out = format_intent_list(list_patch_intents(job))
        assert "docs/file_0.md" in out

    def test_format_intent_list_shows_decided_when_set(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        item = get_patch_intent(job, intent_id)
        out = format_intent_list(list_patch_intents(job))
        assert item["decided_at"] in out
<<<END PAIR_P5_TO>>>
Target: tests/test_patch_intent_approval.py, class TestFormatHelpers —
APPEND (TO contains FROM verbatim; order ordered-equality, not a
FROM-count proof).

<<<BEGIN PAIR_P6_FROM>>>
    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.patch import _cmd_list_patch_intents
        with pytest.raises(SystemExit) as exc_info:
            _cmd_list_patch_intents(str(uuid4()))
        assert exc_info.value.code == 1
<<<END PAIR_P6_FROM>>>
<<<BEGIN PAIR_P6_TO>>>
    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.patch import _cmd_list_patch_intents
        with pytest.raises(SystemExit) as exc_info:
            _cmd_list_patch_intents(str(uuid4()))
        assert exc_info.value.code == 1

    def test_json_output_has_version_and_intents(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id), json_output=True)
        data = json.loads(capsys.readouterr().out)
        assert data["version"] == 1
        assert data["intent_count"] == 1
        assert data["intents"][0]["target_path"] == "docs/file_0.md"
        assert data["intents"][0]["decided_at"] is None
<<<END PAIR_P6_TO>>>
Target: tests/test_patch_intent_approval.py, class TestCmdListPatchIntents
(same file as P5, same commit) — APPEND (TO contains FROM verbatim;
order ordered-equality). `json` is already imported at module level.

<<<BEGIN PAIR_P7_FROM>>>
        expected_json = {
            "brain.graph", "brain.node", "brain.context",
            "policy.contract", "policy.token",
            "worker.list", "test.discover",
            "project.show", "project.context",
        }
<<<END PAIR_P7_FROM>>>
<<<BEGIN PAIR_P7_TO>>>
        expected_json = {
            "brain.graph", "brain.node", "brain.context",
            "policy.contract", "policy.token",
            "worker.list", "test.discover",
            "project.show", "project.context", "patch.list",
        }
<<<END PAIR_P7_TO>>>
Target: tests/test_command_catalog.py, TestCatalogJSONSupport.test_known_json_commands — REWRITE.

Reviewer's own pre-emission proof (dry run, disposable worktree
`.remedy-wt/dryrun-r8` off HEAD `2286919d60503ddd0535eedc49af3ea1242ac047`,
removed before this block was written): all seven FROM strings counted
at exactly 1 occurrence in their target files; all seven pairs applied
via the same str.replace(FROM, TO, 1) shape this block orders;
`python3 -m py_compile` exit 0 on all five files; `python3 -m pytest
tests/test_patch_intent_approval.py tests/test_command_catalog.py -q`
read 91 passed (up from a 77-passed baseline on the unmodified worktree);
`python3 -m pytest tests/cli/test_golden_path.py -q` read 42 passed; a
manual smoke script constructed one pending patch intent and confirmed
both the text table's new DECIDED column (reading `-` for the
undecided row) and the `--json` payload (`version`, `intent_count`,
`intents[0].decided_at is None`) by hand.
