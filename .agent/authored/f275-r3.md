── STEP T001/3 — F275 ────────────────────────────────
Goal:        Wire the carried readiness module into the CLI and the cockpit as `mission readiness`, cut the ONE surviving consumer edge the deletion map records for `packages.orchestration.overnight_readiness`, and remove that map line in the SAME commit — which takes that module to ZERO edges and makes it deletable.
Bundle:      C0a save block · C0b mirror block · C1 plan · C2 book round 2 PASS · C3 the wiring (one commit) · C4 the CLI test · C5 gates (writes no file) · C6 handback
Change:      EXACTLY these twelve paths and nothing else —
             `.agent/authored/f275-r3.md`, `.agent/last_block.md`, `.agent/plan.md`,
             `.agent/live_review.md`, `apps/cli/command_catalog.py`,
             `apps/cli/commands/mission_cmd.py`, `packages/orchestration/mission_readiness.py`,
             `packages/orchestration/ui_server.py`, `tests/orchestration/cluster_deletion_map.txt`,
             `tests/orchestration/import_reachability_allowlist.txt`,
             `tests/cli/test_mission_cmd.py`, `.agent/handoff.md`.
Constraints: below, numbered 1 to 11.
Done when:   the eight gates G1 to G8 below all report exit 0, with G8 last.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────

WHAT THIS ROUND IS. Rounds 1 and 2 moved twenty-nine definitions out of
`packages/orchestration/overnight_readiness.py` into `packages/orchestration/mission_readiness.py`
byte-identically and left it UNWIRED — dead code for two rounds. This round gives it its two
consumers and takes them off the cluster module in the same breath. It is NOT a deletion round:
nothing is `git rm`-ed, and operator ruling amend0908-f275-finish orders the carry-overs done
BEFORE the first `git rm`. The reviewer applied every production edit in a disposable worktree at
`3068e9c1` and ran every gate before authoring; the numerals in G4 to G8 are that run's.

────────────────────────── CONSTRAINTS ──────────────────────────

1. NO SLICE IS EDITED. Every authored text below is applied byte for byte. If a slice looks wrong,
   apply it anyway and DECLARE it in the handback's deviations. Repairing a reviewer's text
   silently is the one thing that makes a gate meaningless.

2. C0a and C0b are `shutil.copyfile` from the reviewer's scratch original
   `.remedy-wt/f275-r3-FINAL.md` — NEVER retyped, never re-wrapped — to `.agent/authored/f275-r3.md`
   and `.agent/last_block.md`. Both are whole-file writes of a single `.agent/**` state file, which
   AGENTS.md DECISION F104 D1 exempts from the 500-insertion cap by name.

3. C1 IS THE FIRST SUBSTANTIVE COMMIT; only C0a and C0b may precede it. This round touches the
   finding ledger, so `.agent/plan.md` advances before the ledger commit (§3 item 23).

4. C3 IS ONE COMMIT AND IS INDIVISIBLE. `tests/orchestration/test_cluster_deletion_map.py` reds
   BOTH when an edge appears and when a cut edge's line is left behind, so the import switch in
   `packages/orchestration/ui_server.py` and the removal of the map line MUST land together.
   `tests/orchestration/import_reachability_allowlist.txt` gains its line in that same commit for
   the same reason: wiring the module makes it reachable, and
   `tests/orchestration/test_import_reachability.py` reds on a reachable module the allowlist does
   not name. The reviewer confirmed both reds by control — see G5.

5. `packages/orchestration/overnight_readiness.py` IS NOT TOUCHED. Not one byte. It stays on disk
   with all its definitions and is deleted later, with its cluster group. G8 gates that.

6. NO COMMAND IS RENAMED. `overnight readiness` still exists and still works after this round; this
   round ADDS `mission readiness` beside it. F261 owns renames, and the feature file's "Do not
   touch" forbids one here. The old command dies by DELETION with its handler, in a later round.

7. THE CARRIED SYMBOLS KEEP THEIR `overnight_` SPELLING. `build_overnight_readiness` and
   `export_readiness_json` are imported under those names from the new module. DECISION F275 D1
   ruled the move renames nothing, and rounds 1 and 2 are byte-identical moves on that basis.

8. C4's append goes at the END of `tests/cli/test_mission_cmd.py`, whose last byte at `3068e9c1`
   is a single `\n` closing the line `        assert body["watchdog_trips"] == []`. The appended
   region begins with exactly two blank lines, which is how that file separates its classes.

9. NOTHING UNDER `docs/` CHANGES this round, so the docs gate does not apply. No pull request is
   created: under `docs/roadmap/STATUS_closure_protocol.md` the PR belongs to the closure sequence.

10. PAIR SHAPES, CLASSIFIED BY A MECHANICAL CONTAINMENT TEST AND NOT BY EYE (§3 items 4 and 15).
    The reviewer ran the test per pair and records its OUTPUT here; the label is derived from that
    output on the same line:
      pair (a) catalog entry ........ TO contains FROM: false -> REWRITE
      pair (b) handler registration . TO contains FROM: true  -> APPEND
      pair (c) cockpit import ....... TO contains FROM: false -> REWRITE
      pair (d) cockpit source ....... TO contains FROM: false -> REWRITE
      pair (f) allowlist line ....... TO contains FROM: true  -> APPEND
      pair (g) module docstring ..... TO contains FROM: false -> REWRITE
    Edit (e) is a DELETION and is not a pair. No gate orders a "FROM occurs 0 times" reading for
    the two APPEND pairs, because their FROM legitimately survives inside their TO.

11. EVERY SEPARATOR LINE IN THIS BLOCK'S FRAME IS A RUN OF EXACTLY 54 `─` CHARACTERS (§3 item 37),
    stated because a run has no length a reader recovers by eye. Nothing appliable travels in the
    frame: every appliable byte is a slice, proved against its own target.

────────────────────────── C1 — THE PLAN ──────────────────────────

Replace the WHOLE of `.agent/plan.md` with the text between the markers. 43 lines and 2425 bytes,
under the AGENTS.md cap of 50 lines. The marker lines themselves are NOT part of the file.

<<<BEGIN PLAN3>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared, with one module group as the atomic unit.

## Current Step

ROUND 3 books round 2's PASS verdict into the record and then WIRES the carried readiness
module. `mission readiness` joins the catalog and `apps/cli/commands/mission_cmd.py`, the
cockpit's readiness section switches its import from the cluster module to the carried one,
and the deletion map loses the one line it recorded for
`packages.orchestration.overnight_readiness` in that same commit. That module ends the round
with ZERO surviving consumer edges, which is what makes it deletable.

## Next Steps

1. The `mission report` carry-over, which DECISION F274 D2 couples to the death of the current
   holder of `mission.report` in `apps/cli/commands/worker_facade_cmd.py`: the carry-over and
   that deletion are ONE commit.
2. The route-policy knobs checked against F110's config keys — R-0831 already records that none
   has an equivalent, so this is a finding update and not a rebuild.
3. `.agent/f275_deletion_order.md`, derived from the map in dependency order, leaf modules
   first, written BEFORE the first `git rm`.
4. The module groups, one commit each, under the four measurements
   amend0906-triage-throughput names for a deletion round.
5. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831
   named among the ideas deleted rather than inherited.

## Risks

- 65 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check is WRONG about them, which is R-0648 and itself open.
- `packages/orchestration/overnight_readiness.py` keeps its own tests and its own cluster
  consumers after this round. It is deletable, not deleted, and only its GROUP commit removes
  it — a half-deleted module is the state operator RULE 1 forbids.
<<<END PLAN3>>>

────────────────────────── C2 — THE RECORD ──────────────────────────

APPEND the text between the markers to `.agent/live_review.md`, followed by exactly one newline.
It is ONE blank-line unit, 3877 bytes. The file is 515349 bytes before this commit and ends with a
newline; append a single `\n` FIRST so the new unit is separated from the current last one by a
blank line. Do not renumber, reflow or edit anything already in the file.

<<<BEGIN RECORD3>>>
Gate: F275 R2 — the F275 round 2 entry. VERDICT PASS, booked by round 3 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 2 handback committed at `2a2f2b5b` and pushed, with the verdict appended at `09086390`. Range `b382ab02`..`2a2f2b5b`, and the reviewer re-ran the round's verification itself against the COMMITTED blobs rather than reading the worker's report. THE CHANGE SET IS EXACTLY THE EIGHT PATHS the block named, by `git diff --name-status`. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37, and NOT the emitted bytes: the scratch original, the committed `.agent/authored/f275-r2.md` and the committed `.agent/last_block.md` are all 25131 bytes at `dd9532377da9b2e460e83618b56a776d395b96e548b88679c61856812e040d3f`. G2 THE PLAN: `.agent/plan.md` byte-equal to its slice at 2368 bytes and 41 lines. G3 THE RECORD: `.agent/live_review.md` 510121 to 515349 and `.agent/prose_slips.md` 166737 to 168030, each gain the slice's bytes plus one newline, each pre-blob an exact PREFIX and each slice an exact SUFFIX, blank-line units 214 to 215 and 229 to 233, `^Gate: ` 23 to 24, and the OPEN SET UNCHANGED AT 65 BY DISTINCT ID — 68 distinct registrations against 3 distinct resolutions, the subtraction taken over DISTINCT ids and never over the 5 `Done:` LINES. G4 THE MODULE: all twenty-nine carried definitions BYTE-IDENTICAL to their spans in `packages/orchestration/overnight_readiness.py` at `a5bf894946ab6de053a4232109d6341a63533768`, the round-1 blob an exact PREFIX of the round-2 blob, `ast.parse` clean, and all five deliberately excluded names absent from the module and present in the source — checked in BOTH directions. G6: `tests/orchestration/test_mission_readiness.py` collects 20 and passes 20, holds no `class TestPlan`, no `build_overnight_plan` and no `export_plan_json`, and its twelve `overnight_readiness` occurrences are every one of them the CARRIED symbol `build_overnight_readiness` or `select_overnight_next_action`, never an import of the old module. G7: 506 · 51 · 21 · 16 · 28 · 42, six suites each run ALONE, every count the one predicted, and run 5 includes the ORIGINAL module's own test, which still passes because round 2 COPIED its subject and did not move it. G8 WAS RED and the round is a PASS ANYWAY: its only failing clause was that `.agent/STOP` existed and therefore `git status --porcelain` was not empty. The reviewer confirmed the sentinel independently — 0 bytes, UNTRACKED, created 10:10 while the gates ran, and the single occurrence of that path in a tracked file is a READ-ONLY assertion in `tests/test_agent_tooling.py`, inside `test_self_drive_protocol_states_its_guardrails`, measured at `3068e9c1`, so nothing in this repository writes it. It was an EXTERNAL signal arriving mid-round, not a product of the change set; every other G8 clause passed, including the dotted-import search returning exactly one file with NOTHING under `packages/` or `apps/`. Grading the round down for a sentinel the operator placed would grade the worker for the operator's action, and the worker did exactly what guardrail G6 orders: finished the one owed commit, left the sentinel untouched, and stopped. The operator has since cleared it and committed amend0908-f275-finish at `3068e9c1`. THREE DEVIATIONS WERE DECLARED AND NONE IS A FINDING: the `# Plan (1256)` banner dropped with the class it titled; the module docstring left reading "STAGED BATCH 1 OF 2" because constraint 3 required the round-1 bytes to stay an exact prefix, which round 3 repairs in the commit that wires the module; and the docstring's "655 lines" CHECKED rather than assumed and found exact. Under amend0827 rule 2 none of the three put anything wrong on disk that a round must repair, so none earns an id.
<<<END RECORD3>>>

────────────────────────── C3 — THE WIRING (SPEC) ──────────────────────────

SEVEN labelled edits across SIX files, ONE commit — (c) and (d) are two edits to the same file.
The reviewer applied all seven in a disposable worktree at `3068e9c1` and measured
`git diff --numstat` as 12, 33, 6, 2, 0, 1 insertions — 54 in total, far under the DECISION F104
D1 cap of 500 insertions per commit.

(a) `apps/cli/command_catalog.py` — INSERT a catalog entry. The anchor is the END of the
`mission.resume` entry, which is the last entry before the doctor group's comment banner. FIND
this text, which occurs exactly ONCE in the file:

        related=("mission.pause", "mission.watchdog"),
    ),

    # ── doctor

REPLACE it with the same text carrying the new entry between the `),` and the blank line:

        related=("mission.pause", "mission.watchdog"),
    ),
    CommandEntry(
        command_id="mission.readiness",
        group_id="mission",
        subcommand="readiness",
        description="Read-only: is this job safe to run unattended?",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("mission.show", "mission.watchdog"),
    ),

    # ── doctor

The reviewer checked this entry against every invariant `tests/test_command_catalog.py` asserts
over the whole catalog — unique id, unique (group, subcommand) path, known group, id format, a
valid `action_class`, `is_expensive` a bool with only `job.run` marked, a `--json` arg because
`supports_json` is True, no forbidden term in the description. `mission.readiness` is FREE;
`mission.report` is NOT, which is what DECISION F274 D2 is about and why report is a later round.

(b) `apps/cli/commands/mission_cmd.py` — INSERT a handler and register it. FIND the single line

COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {

and REPLACE it with the handler, two blank lines, that same line, and the registration:

def _cmd_mission_readiness(job_id: str, *, json_output: bool = False) -> None:
    """Read-only: is this job safe to run unattended?

    The readiness view carried out of the prototype cluster into
    ``packages/orchestration/mission_readiness.py`` by DECISION F275 D1. The
    JSON payload is the carried module's own export, unwrapped, so the view
    survives the cluster deletion byte for byte rather than being redesigned.
    """
    from packages.orchestration.mission_readiness import (
        build_overnight_readiness,
        export_readiness_json,
    )
    data = export_readiness_json(build_overnight_readiness(str(job_id)))
    if json_output:
        print(_json.dumps(data, indent=2))
        return
    print(f"Mission readiness: {str(job_id)[:8]}")
    print(f"  level: {data['readiness_level']}  ready: {data['ready']}  "
          f"unattended: {data['can_run_unattended']}")
    if data["blockers"]:
        print("  blockers: " + ", ".join(data["blockers"]))
    top_risks = [r for r in data["risks"] if r["severity"] in ("blocker", "high")]
    if top_risks:
        print("  top risks: " + "; ".join(r["summary"] for r in top_risks[:3]))
    na = data.get("next_action")
    if na:
        print(f"  next: {na['label']} -> {na['command']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "mission.readiness": lambda args: _cmd_mission_readiness(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),

The module already imports `json as _json`, so no import is added. The handler is the body of
`_cmd_overnight_readiness` in `apps/cli/commands/overnight_cmd.py` with its module swapped and
its header changed from `Overnight readiness:` to `Mission readiness:` — the payload is
byte-for-byte the old one, which G6 measures rather than assumes.

(c) `packages/orchestration/ui_server.py` — the EDGE CUT, inside `_build_overnight_section`.
Each line below occurs exactly once in the file; replace FROM with TO, keeping the indentation:

  FROM:         from packages.orchestration.overnight_readiness import (
  TO:           from packages.orchestration.mission_readiness import (

(d) `packages/orchestration/ui_server.py`, second edit, SAME commit:

  FROM:             "source": "overnight_readiness",
  TO:               "source": "mission_readiness",

The reviewer searched the whole repository for that string as a VALUE before ordering this: no
test, no `apps/ui` source, no doc and no JSON fixture reads it, so the relabel breaks no
consumer, and leaving it saying `overnight_readiness` after the import moved would make the
field name a module that no longer produces it.

(e) `tests/orchestration/cluster_deletion_map.txt` — DELETE the whole line

packages.orchestration.overnight_readiness <- packages/orchestration/ui_server.py

and its newline. It occurs exactly once. The file goes from 20 recorded edges to 19, and the
number of cluster modules still carrying any edge goes from 11 to 10.

(f) `tests/orchestration/import_reachability_allowlist.txt` — INSERT the single line

packages.orchestration.mission_readiness

directly BEFORE the existing line `packages.orchestration.mission_state`. That is its sorted
position: `mission_plan_schema` < `mission_readiness` < `mission_state`. The file is generated
and sorted; an entry out of order is a defect even when the test passes.

(g) `packages/orchestration/mission_readiness.py` — the stale docstring sentence round 2
declared and could not repair. FIND the paragraph beginning `STAGED BATCH 1 OF 2, AND UNWIRED.`
and ending `not touched by either batch.` — five lines — and REPLACE all five with these six:

COMPLETE AND WIRED. The carry-over is 655 lines, which exceeds the DECISION F104 D1
cap of 500 insertions for one commit, so it landed across two commits in two rounds.
`remedy mission readiness` and the cockpit readiness section both read it, and those
two consumers are why `packages/orchestration/overnight_readiness.py` has no
surviving consumer left. That module is still on disk and is deleted with its
cluster group; it was never touched by this move.

This is the ONLY edit this round makes to that module and it touches the docstring alone: all
twenty-nine carried definitions stay byte-identical, which G4 gates.

────────────────────────── C4 — THE TEST (SPEC) ──────────────────────────

APPEND to `tests/cli/test_mission_cmd.py`, after its final newline, exactly two blank lines and
then the class below. This file runs the REAL grouped CLI in a subprocess against a tmp data
root, which is why the wiring is proven end to end here rather than by importing the handler.

class TestMissionReadinessIsWiredToTheCarriedModule:
    """F275 T001: the readiness view carried out of the prototype cluster.

    `packages/orchestration/mission_readiness.py` was moved definition by
    definition in rounds 1 and 2 and left deliberately UNWIRED, so for two
    rounds it was dead code. These are the tests that stop it being dead: the
    catalog carries the command, the dispatch table reaches the handler, the
    real CLI answers with the carried payload, and the cockpit no longer
    imports the cluster module it was carried out of.
    """

    JOB_ID = "11111111-2222-3333-4444-555555555555"

    def test_the_catalog_registers_mission_readiness_exactly_once(self):
        from apps.cli.command_catalog import CATALOG

        assert len([c for c in CATALOG if c.command_id == "mission.readiness"]) == 1

    def test_the_dispatch_table_reaches_the_handler(self):
        from apps.cli.commands import collect_all_handlers

        assert "mission.readiness" in collect_all_handlers()

    def test_the_real_cli_answers_with_the_carried_payload(self, project):
        data_root, _project_id = project

        body = json.loads(_run(["mission", "readiness", self.JOB_ID, "--json"],
                               data_root).stdout)

        for key in ("readiness_level", "ready", "can_run_unattended", "blockers",
                    "risks", "checklist"):
            assert key in body, f"the carried payload lost {key}"

    def test_the_text_view_names_the_mission_command(self, project):
        data_root, _project_id = project

        out = _run(["mission", "readiness", self.JOB_ID], data_root).stdout

        assert out.startswith("Mission readiness:")

    def test_the_cockpit_reads_the_carried_module_and_says_so(self):
        from packages.orchestration.ui_server import _build_overnight_section

        class _Job:
            id = "11111111-2222-3333-4444-555555555555"

        section = _build_overnight_section(_Job(), Path(".data"))

        assert section["source"] == "mission_readiness"

    def test_the_cockpit_no_longer_imports_the_cluster_readiness_module(self):
        """The edge this round cut. The map ratchet proves the graph; this names the file.

        The token is the DOTTED MODULE PATH, never the bare word: the carried
        symbol `build_overnight_readiness` keeps its spelling by DECISION F275
        D1, so a substring check would red on the very names the move preserves.
        """
        source = (REPO_ROOT / "packages" / "orchestration" / "ui_server.py").read_text(
            encoding="utf-8")

        assert "packages.orchestration.overnight_readiness" not in source
        assert "from packages.orchestration.mission_readiness import" in source

`json`, `Path` and `REPO_ROOT` are already imported at the top of that file, and `project` is its
existing fixture returning `(data_root, project_id)`. The reviewer ran the fifth test's body in
the worktree with that exact `Path(".data")` argument — which did NOT exist there, and the section
still reported `mission_readiness`, so it does not depend on a data root being present.

WHY THAT TEST READS A DOTTED PATH, measured at `3068e9c1`: `ui_server.py` holds the substring
`overnight_readiness` FOUR times — the import, the `source` value, and TWICE inside the carried
symbol `build_overnight_readiness`, which constraint 7 keeps. Edits (c) and (d) remove two, the
other two legitimately survive, and the dotted path occurs ONCE at base and ZERO times after (c).
A bare-word assertion would have landed RED on a correct change.

────────────────────────── C5 — THE GATES ──────────────────────────

Run ALL EIGHT at C5, after C4 and STRICTLY BEFORE the C6 handback commit, so the handback can
quote every one of them (§3 item 31). C5 writes no file and has no commit. Report ONE LINE PER
GATE with the REAL exit code. A gate that cannot be run is reported as not run — never as green.

EVERY GATE BELOW WAS RUN BY THE REVIEWER AT THE BASE `3068e9c1` BEFORE EMISSION, and each carries
its BASE reading beside its expected one — the procedure finding R-0819's recurrence paragraph
strengthened from a clause, so that a gate which cannot discriminate is visible on this page.
Readings that are deliberately NON-DISCRIMINATING are labelled: they are no-regression gates, and
G5's two red controls carry the discrimination. The other open fix clause read before emission is
R-0741's grep-derived leave-alone set; it is DECLINED AS NOT APPLICABLE on its own terms — it
binds "the next block that orders such a set", and this block orders none.

G1 TRANSPORT. sha256 and byte count of the scratch original `.remedy-wt/f275-r3-FINAL.md`, of
the committed `.agent/authored/f275-r3.md`, and of the committed `.agent/last_block.md`. All
three must be ONE value. Per §3 item 37 this proves the chain this workflow can walk — saved
copy, mirror, working copy — and NOT the bytes the reviewer emitted; do not claim more.

G2 THE PLAN. `.agent/plan.md` byte-identical to PLAN3. Report its sha256, its byte count, its
line count (must be under the AGENTS.md cap of 50), and that `^## Goal$` and `^## Next Steps$`
each occur exactly once.

G3 THE RECORD. Six parts, over `.agent/live_review.md` only.
  (a) BYTES: 515349 before, and after = 515349 + len(RECORD3) + 1. State both numbers.
  (b) EXACT EDGES: the pre-commit blob is a byte-exact PREFIX of the post-commit blob, and
      RECORD3 is a byte-exact SUFFIX of it. Report both booleans.
  (c) ORDERED EQUALITY by an independent paragraph reader: compare the LAST N blank-line units
      of the whole file against RECORD3's N paragraphs IN ORDER, where N is COUNTED FROM THE
      SLICE by your script and is never taken from this block. Report N and the per-unit
      sha256 pairs.
  (d) NEGATIVE CONTROL on the FIRST appended paragraph, in scratch only: flip one byte inside
      it and confirm BOTH the reader of (b) and the reader of (c) REJECT it. Re-read the
      tracked file afterwards and report its byte count to show the mutation never touched it.
  (e) COUNTS: blank-line units 215 → 216; `^Gate: ` 24 → 25; `^Gate: F275 R2 ` 0 → 1.
  (f) THE OPEN SET DOES NOT MOVE: distinct `^- R-\d+ — ` ids 68 → 68, distinct `^Done: R-\d+ — `
      ids 3 → 3, OPEN SET BY DISTINCT ID 65 → 65. Subtract DISTINCT IDS, never the 5 `Done:`
      LINES. This round mints no id and resolves none.

G4 THE WIRING. Over the C3 commit: `git diff --numstat` must read 12, 33, 6, 2, 0, 1 insertions
for the six files in the order (a)/(b)/(g)/(c,d)/(e)/(f) — report the real columns whatever they
are. `python3 -m ruff check` exit 0 over `apps/cli/command_catalog.py`,
`apps/cli/commands/mission_cmd.py`, `packages/orchestration/ui_server.py` and
`packages/orchestration/mission_readiness.py`. `ast.parse` clean on all four. And the docstring
edit is the ONLY change to `packages/orchestration/mission_readiness.py`: every one of its
twenty-nine top-level definitions is byte-identical to its span in the file at `3068e9c1`.
READ THE BASE BLOB WITH `git show 3068e9c1:packages/orchestration/mission_readiness.py` INTO
MEMORY OR INTO GITIGNORED SCRATCH — never by overwriting and restoring the tracked file, which
guardrail G5 forbids outright (§3 item 29). BASE reading, measured by the reviewer: ruff exit 0
on all four files, and all twenty-nine definitions identical to themselves, so the definition
half of this gate is a no-regression reading; the numstat columns are what discriminate.

G5 THE RATCHETS, WITH BOTH RED CONTROLS. Green first, in the primary checkout:
`python3 -m pytest tests/orchestration/test_import_reachability.py
tests/orchestration/test_cluster_deletion_map.py -q` must be exit 0. Then, in a DISPOSABLE
`git worktree` and NEVER in the primary checkout, per guardrail G5:
  control 1 — put the deleted map line back and re-run the map test ALONE. It must FAIL, and its
  message must name `DISAPPEARED (1)` with that exact edge.
  control 2 — remove `packages.orchestration.mission_readiness` from the allowlist and re-run
  the reachability test ALONE. It must FAIL naming `packages.orchestration.mission_readiness`
  as reachable-but-unlisted, which is the round's independent proof that the wiring REALLY made
  the module reachable.
Report all four exit codes, then remove the worktree BY ITS EXACT PATH and show
`git worktree list` holding only the primary checkout. BASE readings, measured by the reviewer at
`3068e9c1`: both ratchets GREEN with the map line present and the allowlist entry absent — which
is the untouched base — and then, with this round's edits applied, GREEN again, and both controls
RED with exactly those two messages. So both halves can fail and both halves can pass, which is
what makes this gate evidence rather than decoration.

G6 THE CARRY-OVER IS BEHAVIOUR-PRESERVING. Through the SHIPPED dispatch table, not by importing
the module: build the parser with `apps.cli.grouped.build_parser()` and parse
`["mission","readiness","11111111-2222-3333-4444-555555555555","--json"]`; then call BOTH
`collect_all_handlers()["overnight.readiness"]` and `collect_all_handlers()["mission.readiness"]`
on that namespace, capture each one's stdout, and compare the two JSON payloads. They must
differ in `generated_at` ALONE — report the full list of differing keys and the list with
`generated_at` removed, which must be empty. `generated_at` is a timestamp that differs between
two consecutive calls to the SAME module, which round 2's G5 already measured. Also report
`_build_overnight_section` returning `source` == `mission_readiness`. The reviewer measured
1097 characters from each handler and `['generated_at']` as the only difference.
BASE reading at `3068e9c1`: `"mission.readiness" in collect_all_handlers()` is FALSE and the
lookup raises `KeyError`, while `overnight.readiness` is registered — so this gate is UNMEETABLE
at the base and fully discriminating.

G7 THE SUITES, each run ALONE and serially, in this order. Report the real exit code and the
passed count for each:
  1. `python3 -m pytest tests/orchestration/test_import_reachability.py
     tests/orchestration/test_cluster_deletion_map.py
     tests/orchestration/test_overnight_readiness.py
     tests/orchestration/test_mission_readiness.py -q`
     BASE 48, expected 48 — NO-REGRESSION, this reading does not discriminate.
  2. `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py
     tests/cli/test_mission_cmd.py -q`
     BASE 639, expected 645 — DISCRIMINATING: C4 adds exactly six tests, counted from the class
     above and not asserted from memory. Report what you measure.
  3. `python3 -m pytest tests/ui_server/ -q`
     BASE 506, expected 506 — NO-REGRESSION. This is the suite the edge cut could break.
  4. `python3 -m pytest tests/cli/test_golden_path.py -q`
     BASE 42, expected 42 — the canary, NO-REGRESSION.

G8 THE TREE AND THE UNTOUCHED MODULE. All of:
  - `.agent/STOP` does not exist;
  - `git status --porcelain` is EMPTY;
  - the branch is `feature/f275-one-world-completion-part-three`;
  - `git worktree list` shows ONLY the primary checkout;
  - `packages/orchestration/overnight_readiness.py` is BYTE-IDENTICAL to its blob at
    `3068e9c1`, read with `git show 3068e9c1:packages/orchestration/overnight_readiness.py`
    into scratch and never by touching the tracked file — report both sha256 values;
  - `tests/orchestration/cluster_deletion_map.txt` contains the DOTTED PATH
    `packages.orchestration.overnight_readiness` ZERO times (BASE reading: exactly 1), and its
    recorded-edge count read through `recorded_edges()` is 19 (BASE reading: 20);
  - `git log --oneline` over this round's range shows the commits C0a, C0b, C1, C2, C3, C4 in
    that order, each single-parent.
C6's OWN numbers are deliberately ordered NOWHERE. Under docs/agents/self_drive_protocol.md there
is no second window, so a value routed to a "round report" or a "completion message" is written to
a channel that ends with the session (§3 item 31). The REVIEWER measures C6's commit and its
numstat columns itself at the next gate and records them in that round's ledger entry. Do not
guess them, and do not leave a blank where they would go.

────────────────────────── C6 — THE HANDBACK ──────────────────────────

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. NO length cap (amend0827 rule
3); valid when its mandated sections are present. It MUST carry: the state block naming FEATURE
F275, ROUND 3, SESSION 2, the branch, the base `3068e9c1` and every commit SHA; the changed-files
table with the REAL `git diff --numstat` columns per commit, taken from the tool and not
re-derived (§3 item 28); ONE LINE PER GATE with its real exit code, plus the G3, G5, G6 and G7
transcripts; the open-findings count (65 by distinct id, unchanged); the item-status table
covering C0a, C0b, C1, C2, C3, C4, C5, C6 and G1 to G8 exactly once each; the deviations; the
Fortschritt line below verbatim; ONE SENTENCE of context self-assessment per amend0905-throughput;
and the next expected action — the `mission report` carry-over, which DECISION F274 D2 couples to
the deletion of the current holder of `mission.report` in
`apps/cli/commands/worker_facade_cmd.py`, carry-over and deletion in ONE commit. Write NO verdict:
the verdict is the reviewer's and is written after this commit.

Fortschritt: ~20 % (T001: Claim ✅ · Record ✅ · D1 ✅ · Carry-over Batch 1 ✅ · Batch 2 ✅ ·
Testdatei ✅ · Verdrahtung ✅ · Kante geschnitten ✅ · mission report offen · F260 D3 offen ·
Löschung offen · T002 offen · T003 offen) — Schätzung
