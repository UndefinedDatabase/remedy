STEP T002/4 - F262 List commands v2, ROUND 6
FEATURE F262 - List commands v2 (Tier 2) - SESSION 2, ROUND 6

Goal
  Ship T002 batch 4: `project.list` gains its first `--json` support
  (it had NONE before this round - no `_JSON_OPT` in its catalog args,
  no `json_output` param on its handler, unlike every other list
  command this feature has touched so far, which already had --json
  and only needed a date field added to it). This round adds the flag
  end to end (catalog args + supports_json, handler signature +
  json branch, dispatch lambda), plus `created_at` in --json and a
  `created=` field in text mode. `RemyProject` has no second/updated
  timestamp field, so neither surface shows one - same precedent as
  round 5's tournament/external-builder records. Two production files
  (apps/cli/command_catalog.py, apps/cli/commands/project.py), one
  test file (tests/test_grouped_cli.py, a new class appended at the
  end). No model or store change.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r6.md
  C0b mirror it to .agent/last_block.md
  C1  append GATE5 to .agent/live_review.md - books round 5's PASS
      verdict (the reviewer's own, independently re-verified)
  C2  apply CODE PAIR C1 to apps/cli/command_catalog.py; apply CODE
      PAIR H1 and CODE PAIR H2 to apps/cli/commands/project.py; add
      the TEST SPEC class below to tests/test_grouped_cli.py (one
      commit, three files)
  C3  apply PLAN7 to .agent/plan.md
  C4  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r6.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - apps/cli/command_catalog.py (C2) -
  apps/cli/commands/project.py (C2) - tests/test_grouped_cli.py (C2) -
  .agent/plan.md (C3) - .agent/handoff.md (C4)

CODE PAIR C1 (apps/cli/command_catalog.py) - REWRITE (TO does NOT
contain FROM verbatim: two new keyword args are inserted before the
closing paren). FROM is the ENTIRE `project.list` CommandEntry
literal, unique in the file (the only entry whose command_id is
"project.list").
<<<BEGIN PAIR_C1_FROM>>>
    CommandEntry(
        command_id="project.list",
        group_id="project",
        subcommand="list",
        description="List all projects.",
        action_class="read_only",
    ),
<<<END PAIR_C1_FROM>>>
<<<BEGIN PAIR_C1_TO>>>
    CommandEntry(
        command_id="project.list",
        group_id="project",
        subcommand="list",
        description="List all projects.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),
<<<END PAIR_C1_TO>>>
`_JSON_OPT` is already defined and imported at module level in this
same file (it is what `project.show`'s own entry a few lines below
already uses) - do not add a new import or definition, just reference
the existing name. `_with_list_options()` (defined later in the same
file) runs over every catalog entry afterward and adds the shared
`--sort/--desc/--since/--until/--limit` flags to any list-shaped entry
missing them - `project.list` already gained those in round 2 (T001)
regardless of this round's change, so nothing else needs to touch that
mechanism.

CODE PAIR H1 (apps/cli/commands/project.py) - REWRITE, the entire
`_cmd_list_projects` function body, unique in the file (grep confirms
exactly one `def _cmd_list_projects` in the module).
<<<BEGIN PAIR_H1_FROM>>>
def _cmd_list_projects() -> None:
    from packages.orchestration.project_registry import _list_projects_readonly
    projects = _list_projects_readonly()
    if not projects:
        print("No projects found.")
        return
    for p in projects:
        slug = p.slug or "-"
        desc = f"  {p.description}" if p.description else ""
        print(f"{p.id}  {slug:<20s}  {p.name}{desc}")
<<<END PAIR_H1_FROM>>>
<<<BEGIN PAIR_H1_TO>>>
def _cmd_list_projects(*, json_output: bool = False) -> None:
    from packages.orchestration.project_registry import _list_projects_readonly
    projects = _list_projects_readonly()
    if json_output:
        print(_json.dumps({
            "version": 1,
            "project_count": len(projects),
            "projects": [{"id": str(p.id), "slug": p.slug or "", "name": p.name,
                          "description": p.description or "",
                          "created_at": p.created_at.isoformat()} for p in projects],
        }, sort_keys=True))
        return
    if not projects:
        print("No projects found.")
        return
    for p in projects:
        slug = p.slug or "-"
        desc = f"  {p.description}" if p.description else ""
        print(f"{p.id}  {slug:<20s}  {p.name}  (created={p.created_at.isoformat()}){desc}")
<<<END PAIR_H1_TO>>>
`import json as _json` is already present at the top of this file
(used by `_cmd_show_project` a few lines below and other handlers in
the same module) - do not add a second import.

CODE PAIR H2 (apps/cli/commands/project.py) - REWRITE, the
`COMMAND_HANDLERS["project.list"]` dispatch line, unique in the file.
<<<BEGIN PAIR_H2_FROM>>>
    "project.list": lambda args: _cmd_list_projects(),
<<<END PAIR_H2_FROM>>>
<<<BEGIN PAIR_H2_TO>>>
    "project.list": lambda args: _cmd_list_projects(json_output=args.json),
<<<END PAIR_H2_TO>>>

TEST SPEC for C2 - ONE new test class appended at the very END of
tests/test_grouped_cli.py (it is currently the LAST class in the
file, `TestMemoryCLIContract`, ending with `test_approved_absent_is_
false_in_argparse`), written BY HAND (not marker-extracted) matching
`TestMemoryCLIContract`'s own established style: monkeypatch
`REMEDY_DATA_DIR` to `tmp_path`, redirect `sys.stdout` to a `StringIO`
via `monkeypatch.setattr`, import the handler function locally inside
the test body (not at module top), call it, parse/inspect the buffer.

  class TestProjectListCLI:
      """project.list JSON must include version: 1, project_count and created_at."""

      def test_catalog_has_json_flag(self) -> None:
          from apps.cli.command_catalog import get_command
          cmd = get_command("project.list")
          assert cmd.supports_json is True
          assert any(a.name == "--json" for a in cmd.args)

      def test_list_json_has_created_at(self, tmp_path, monkeypatch) -> None:
          monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
          from packages.orchestration.project_registry import RemyProject, save_project
          save_project(RemyProject(name="p1", slug="p1"))
          from apps.cli.commands.project import _cmd_list_projects
          buf = StringIO()
          monkeypatch.setattr("sys.stdout", buf)
          _cmd_list_projects(json_output=True)
          data = json.loads(buf.getvalue())
          assert data["version"] == 1
          assert data["projects"][0]["created_at"]

      def test_list_text_shows_created(self, tmp_path, monkeypatch) -> None:
          monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
          from packages.orchestration.project_registry import RemyProject, save_project
          save_project(RemyProject(name="p2", slug="p2"))
          from apps.cli.commands.project import _cmd_list_projects
          buf = StringIO()
          monkeypatch.setattr("sys.stdout", buf)
          _cmd_list_projects(json_output=False)
          text = buf.getvalue()
          assert "created=" in text

  `json`, `StringIO`, `sys` are already imported at the top of
  tests/test_grouped_cli.py - no new imports needed for the class
  itself (only the two local `from packages.orchestration.
  project_registry import ...` / `from apps.cli.commands.project
  import _cmd_list_projects` lines inside each test body, per the
  spec above).

Constraints
  1. C1's append to .agent/live_review.md is applied BYTE FOR BYTE:
     extract GATE5 from the COMMITTED .agent/authored/f262-r6.md by its
     BEGIN/END markers (excluded) and apply with a script, never by
     retyping. GATE5 carries ZERO internal newlines and NO trailing
     newline of its own. The base file (measured by the reviewer before
     this round) is 2428711 bytes with NO trailing newline, last byte
     `.`; the applied file must equal base + one newline byte + GATE5's
     own bytes. Report the arithmetic and a byte comparison against a
     script-extracted copy of GATE5, both directions, plus a negative
     control (flip GATE5's first byte in a scratch copy, confirm it
     does NOT match the real tail).
  2. All three PAIRs (C1, H1, H2) are extracted from the COMMITTED
     .agent/authored/f262-r6.md by marker index and applied with
     str.replace(FROM, TO, 1) via a script, never by hand-retyping.
     Before editing, confirm each FROM occurs EXACTLY ONCE in its
     target file (report the count; if it is not exactly 1, STOP and
     report rather than editing). All three are REWRITEs: report FROM
     count before (1), FROM count after (0), TO count after (1) for
     each.
  3. The new test class is written by hand from the TEST SPEC above
     (not extracted from a marker slice), placed at the true end of
     the file, after the last line of the existing
     `TestMemoryCLIContract` class.
  4. `python3 -m py_compile apps/cli/command_catalog.py
     apps/cli/commands/project.py tests/test_grouped_cli.py` must exit
     0 for all three (ruff is denied this session per prior rounds -
     attempt it anyway and report the exact refusal or the real
     result, never assume).
  5. C2 is ONE commit covering all three files.
  6. PLAN7 REPLACES .agent/plan.md whole-file, ending WITHOUT a
     trailing newline, same as every prior round.
  7. Before writing PAIR C1, confirm no other CommandEntry in
     command_catalog.py shares this exact literal text (grep for
     `command_id="project.list"` must return exactly 1 hit). Before
     writing PAIR H1/H2, confirm `_cmd_list_projects` and the
     `"project.list":` dispatch key each appear exactly once in
     project.py. Report each count explicitly.
  8. A sentence OUTSIDE the change set that earlier rounds already
     found stale (docs/roadmap/features/T2_F262.md line 5,
     "REGISTRATION ONLY") remains outside this round's change set too -
     re-declare it in the handback, do not repair it.
  9. Read .agent/STOP from disk before the first commit and again
     before C4. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C4 (git push origin feature/f262-list-commands-v2). No
      pull request, no merge.
  11. `git rev-parse HEAD` before C0a must read
      `5918d1be844c5581f0f13b252a45a032f214d026` (report the full SHA);
      `git branch --show-current` must read
      `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r6.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND, FULL FORENSICS. Report:
       base size immediately before C1 (bytes, trailing-newline byte)
       GATE5 own byte length and internal-newline count
       base + 1 + GATE5_length, compared against the post-C1 file's
         real byte length - state match True/False
       tail slice (last GATE5_length bytes of the post-C1 file)
         compared against GATE5 - state equal True/False
       negative control: flip the first byte of a COPY of GATE5,
         confirm the flipped copy does NOT match the real tail - state
         rejected True/False
  G3 THE THREE PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES.
     Then read the FULL diff of apps/cli/command_catalog.py and
     apps/cli/commands/project.py and confirm nothing beyond the named
     insertions changed in EACH file (every other CommandEntry and
     every other handler function/dispatch line byte-for-byte
     untouched). `python3 -m py_compile` on all three touched/added
     files, reported individually, each exit 0.
  G4 THE TESTS, BEFORE AND AFTER. Report
       python3 -m pytest tests/test_grouped_cli.py -q
     BOTH before C2 (baseline: 513 passed) and after C2 (516 passed -
     base + 3, fully green, nothing else in the file touched).
  G5 THE STATE READERS AND THE CANARY (this round rewrites `.agent/`
     state):
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count; a moved count against this session's own
     prior readings (515/52/21/16/42) is itself a finding.
  G6 THE PLAN. Extract PLAN7 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G7 THE TREE, THE COMMITS AND THE SWEEP. `git status --porcelain`
     immediately before C4 is staged -> empty. `git ls-files
     .remedy-wt` -> no output. For C0a, C0b, C1, C2 and C3 (every
     commit before the handback), report each one's insertion count
     from `git show --numstat`, the '+' column only, compared cell by
     cell against the handback's Commits table. Then the staleness
     sweep, one line per file this round touched, plus the constraint-8
     check.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md.
  SESSION 2, ROUND 6 of F262. Item-status table with every ordered item
  (C0a through C4, G1 through G7) exactly once, Commits table, one line
  per gate followed by its real transcript, Deviations (apply anything
  that looks wrong exactly as specified and declare it - never silently
  correct the block), Next (round 7: job.list and queue.list, same
  new-flag shape as this round now that it is proven once - per PLAN7's
  Next Steps).

<<<BEGIN GATE5>>>
Gate: R5 — the F262 R5 entry. R5 SHIPPED T002 BATCH 3, tournament.list and external-builder.submission-list gain a first per-row TEXT format (previously count-only) plus their own single date field in --json (`created_at` for tournament reports, `received_at` for external-builder submissions — each record's own field name, neither has a second/updated timestamp), AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r5.md`/`.agent/last_block.md` share one sha256 digest, `821c2b83fb55529d9068dc5d2b66ad2d14d4d8c748658a838e98fef690c4aa8a`, over 293 lines. THE LEDGER APPEND (booking R4) IS PROVEN IN FULL: base immediately before C1 was 2424986 bytes with no trailing newline, GATE4 measured at 3724 bytes with 0 internal newlines, base plus one newline plus GATE4 equals 2428711 against an actual post-C1 size of 2428711 — match True; the tail slice equals GATE4 byte for byte — equal True; a negative control flipping GATE4's first byte was correctly rejected — rejected True. THE FOUR PAIRS WERE READ, NOT ONLY GATED: `apps/cli/commands/tournament_cmd.py`'s diff is exactly PAIR T1 (rewrite: the json dict comprehension's last field moves to add `"created_at": r.get("created_at", "")`) and PAIR T2 (append-shaped: the count-only print gains a per-row for-loop), nothing else changed in the file — the other three handlers (`report`, `show`, `integrity`) confirmed byte-for-byte untouched by reading the full diff. `apps/cli/commands/external_builder_cmd.py`'s diff is exactly PAIR E1 (rewrite: the json dict comprehension's last field moves to add `"received_at": s.get("received_at", "")`) and PAIR E2 (append-shaped: the count-only print gains a per-row for-loop), nothing else changed in the file — the other seven handlers confirmed byte-for-byte untouched. `python3 -m py_compile` exited 0 on all four touched files, run individually by the reviewer. THE FOUR NEW TESTS MATCH THE TEST SPEC: `test_list_json_has_created_at` and `test_list_text_shows_per_row` in `tests/cli/test_tournament_cli.py`, `test_submission_list_json_has_received_at` and `test_submission_list_text_shows_per_row` in `tests/cli/test_external_builder_cli.py`, each read in full against the block's own TEST SPEC. THE TESTS MOVED EXACTLY AS EXPECTED: `tests/cli/test_tournament_cli.py` read 6 passing before C2 and 8 after; `tests/cli/test_external_builder_cli.py` read 7 passing before C2 and 9 after — both reproduced by the reviewer independently, base plus 2 exactly, nothing else in either file touched. THE STATE READERS AND THE CANARY WERE UNMOVED FROM THIS SESSION'S OWN BASELINE, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty at HEAD `5918d1be844c5581f0f13b252a45a032f214d026`, `git ls-files .remedy-wt` empty, and every commit's insertion counts match the handback's Commits table cell for cell, each measured independently via `git show --numstat`: `c8324d9237e33e170cc5c7c3f8ad043f69ebcc67` 293 new, `28f9f452848767ae96ed14706ec29e4c58b87c84` 212 plus 165 deleted (mirror), `134153db25101ec09fcae0e2157e391da925125d` 2 plus 1 deleted, `fad10b21a4cbd04b93929dbf5339e159fd20b73b` 5 plus 1 deleted on `external_builder_cmd.py`, 6 plus 1 deleted on `tournament_cmd.py`, 24 new on `test_external_builder_cli.py`, 16 new on `test_tournament_cli.py`, and `61d80b65fb6709bc9f28fef3b950ae8d5e42be56` 10 plus 11 deleted. THE PLAN HELD BYTE-EXACT: PLAN6 extracted from the committed authored file compares equal to `.agent/plan.md`, last byte `.`. THE PUSH DISCHARGED — `git ls-remote origin refs/heads/feature/f262-list-commands-v2` and the local `git rev-parse HEAD` both read `5918d1be844c5581f0f13b252a45a032f214d026`, and nothing was created or merged; the branch carries R1 through R5 unmerged. THE DECLARED DEVIATIONS ARE ALL TOOLING OR PRE-EXISTING STALENESS, NONE A DEFECT ON DISK: `git commit`'s own rewrite-detected stat line disagreed with `git show --numstat` for the whole-file C0b mirror, the same substitution already declared every prior round; several Bash compound-command rejections re-expressed as single invocations; ruff's exact denial text varied slightly in wording from round 4's but was equally a refusal, not a run; `docs/roadmap/features/T2_F262.md` line 5's "REGISTRATION ONLY" sentence remains stale since round 2, outside this round's declared change set, correctly declared and left unrepaired again. THE VERDICT IS PASS.
<<<END GATE5>>>

<<<BEGIN PLAN7>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 6, session 2 — T002 batch 4: `project.list` gains its first
`--json` support (it had none before this round - no other list
command in this feature has needed to add `--json` from scratch, only
extend an existing one) plus a `created_at` field and a text-mode
`created=` field. `RemyProject` has no second/updated timestamp, so
neither surface shows one.

## Next Steps

- Round 7: `job.list` (text already prints an ISO date; needs --json
  added) and `queue.list` (text prints an age, derived from
  created_at, not raised as a gap; needs --json added) - same new-flag
  shape as this round, now proven once.
- `loop.list`/`patch.list` have no timestamp on their own model and
  need a design decision before any date can appear (round 3's
  handback carries the full 28-command audit).
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN7>>>
