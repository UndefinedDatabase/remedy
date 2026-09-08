── STEP T001/4 — F275 ────────────────────────────────
Goal:        Land the SECOND carry-over. `mission report` stops being a facade over the cluster module `dogfood_run` and becomes the carried report view, and the handler holding that name DIES IN THE SAME COMMIT — DECISION F274 D2 rules the name is not free until its current holder does.
Bundle:      C0a save block · C0b mirror block · C1 plan · C2 book round 3 PASS, register R-0840, append two prose slips · C3 the carry-over and the death (one commit) · C4 the tests · C5 gates (writes no file) · C6 handback
Change:      EXACTLY these eleven paths and nothing else —
             `.agent/authored/f275-r4.md`, `.agent/last_block.md`, `.agent/plan.md`,
             `.agent/live_review.md`, `.agent/prose_slips.md`,
             `apps/cli/command_catalog.py`, `apps/cli/commands/mission_cmd.py`,
             `apps/cli/commands/worker_facade_cmd.py`, `tests/cli/test_worker_facade_cmd.py`,
             `tests/cli/test_mission_cmd.py`, `.agent/handoff.md`.
Constraints: below, numbered 1 to 10.
Done when:   the eight gates G1 to G8 below all report exit 0, with G8 last.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────

WHAT THIS ROUND IS. Round 3 wired the readiness half of the carry-over and took
`packages.orchestration.overnight_readiness` to zero edges. This round does the report half.
`remedy mission report` today is a facade in `apps/cli/commands/worker_facade_cmd.py` over
`packages.orchestration.dogfood_run.build_mission_morning_report`, keyed on a dogfood RUN id;
after this round it is the carried `build_overnight_report` in
`packages/orchestration/mission_readiness.py`, keyed on a JOB id. That is a user-observable
change, so operator RULE 3 requires a FINDING naming the behaviour and who inherits the idea —
R-0840, authored in C2. It is NOT a deletion round: no module is `git rm`-ed. The reviewer
applied every production edit in a disposable worktree at `280fd101` and ran every gate before
authoring; the numerals in G4 to G7 are that run's.

THE ONE THING A READER WILL EXPECT AND NOT GET: this round does NOT cut the deletion map's
`packages.orchestration.dogfood_run <- apps/cli/commands/worker_facade_cmd.py` edge, and it must
not appear to. `_cmd_mission_run` in that same file imports `run_mission_loop` from `dogfood_run`
at two more sites, so the edge survives on `mission run`, which belongs to a later module group.
The dotted name goes from THREE occurrences to TWO in that file and the map is UNCHANGED. G5
gates exactly that, because a round that quietly shrank the map here would be hiding a live edge.

────────────────────────── CONSTRAINTS ──────────────────────────

1. NO SLICE IS EDITED. Every authored text below is applied byte for byte. If a slice looks
   wrong, apply it anyway and DECLARE it in the handback's deviations.

2. C0a and C0b are `shutil.copyfile` from the reviewer's scratch original
   `.remedy-wt/f275-r4-FINAL.md` — NEVER retyped — to `.agent/authored/f275-r4.md` and
   `.agent/last_block.md`. Both are whole-file writes of a single `.agent/**` state file, which
   AGENTS.md DECISION F104 D1 exempts from the 500-insertion cap by name.

3. C1 IS THE FIRST SUBSTANTIVE COMMIT; only C0a and C0b may precede it. This round touches the
   finding ledger, so `.agent/plan.md` advances before the ledger commit (§3 item 23).

4. C3 IS ONE COMMIT AND IS INDIVISIBLE, because DECISION F274 D2 rules that the carry-over and
   the death of the name's current holder are one commit. A commit that added the new handler
   before removing the old one would have two live claims on `mission.report`, and a commit that
   removed the old one first would leave the catalog naming a handler nothing provides.

5. `packages/orchestration/dogfood_run.py` IS NOT TOUCHED, and neither is
   `packages/orchestration/mission_readiness.py`. `build_mission_morning_report` keeps its
   module-level tests in `tests/orchestration/test_dogfood_run.py`; only the CLI path to it goes.
   The module dies later, with its own group commit. G4 and G7 gate both halves.

6. THE CARRIED SYMBOLS KEEP THEIR `overnight_` SPELLING — `build_overnight_report` and
   `render_overnight_report_markdown` are imported under those names. DECISION F275 D1 ruled the
   move renames nothing, and F261 owns renames.

7. THE NEW HANDLER MIRRORS THE ORIGINAL'S FLAG PRECEDENCE EXACTLY: `--markdown` first, then
   `--json`, then markdown as the default. The reviewer checked this against
   `_cmd_overnight_report` in `apps/cli/commands/overnight_cmd.py` at `280fd101`, where the two
   flags are tested in that order. Reversing them would silently change what
   `--markdown --json` prints, which is the one input where the order is observable.

8. `mission.report` STAYS IN THE CATALOG THROUGHOUT. Its entry is REWRITTEN, never removed and
   re-added. `tests/cli/test_product_spine.py` asserts the id is present and read-only, and the
   reviewer confirmed at `280fd101` that both assertions still pass after the rewrite — this
   round is not permitted to red the product-spine pins and does not.

9. PAIR SHAPES, CLASSIFIED BY A MECHANICAL CONTAINMENT TEST AND NOT BY EYE (§3 items 4 and 15).
   The reviewer ran the test per pair and records its OUTPUT; the label derives from that output:
     pair (a) catalog entry rewrite ..... TO contains FROM: false -> REWRITE
     pair (b) handler registration ...... TO contains FROM: true  -> APPEND
     pair (d) registry expectation ...... TO contains FROM: false -> REWRITE
     pair (e) facade count pin .......... TO contains FROM: false -> REWRITE
   Edits (c), (f) and (g) are DELETIONS and are not pairs. No gate orders a "FROM occurs 0 times"
   reading for pair (b), whose FROM legitimately survives inside its TO.

10. EVERY SEPARATOR LINE IN THIS BLOCK'S FRAME IS A RUN OF EXACTLY 54 `─` CHARACTERS (§3 item 37),
    stated because a run has no length a reader recovers by eye. Nothing appliable travels in the
    frame: every appliable byte is a slice, proved against its own target.

────────────────────────── C1 — THE PLAN ──────────────────────────

Replace the WHOLE of `.agent/plan.md` with the text between the markers. 41 lines and 2362 bytes,
under the AGENTS.md cap of 50 lines. The marker lines themselves are NOT part of the file.

<<<BEGIN PLAN4>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared, with one module group as the atomic unit.

## Current Step

ROUND 4 books round 3's PASS verdict, registers R-0840 for the behaviour operator RULE 3
requires a finding for, and lands the SECOND carry-over: `mission report` stops being a facade
over the cluster module `dogfood_run` and becomes the carried report view over a job's
evidence, while the handler holding that name dies in the SAME commit, as DECISION F274 D2
rules. The map is deliberately UNCHANGED — `mission run` keeps the `dogfood_run` edge.

## Next Steps

1. The route-policy knobs checked against F110's config keys — R-0831 already records that none
   has an equivalent, so this is a finding update and not a rebuild. It rides with substantive
   work, because amend0827 rule 1 forbids a round that is only bookkeeping.
2. `.agent/f275_deletion_order.md`, derived from the deletion map in dependency order, leaf
   modules first, written BEFORE the first `git rm`.
3. The module groups, one commit each, in that order, under the four measurements
   amend0906-triage-throughput names for a deletion round, until the map holds zero cluster
   lines and every module F260's Design lists is gone from disk.
4. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831 and
   R-0840 named among the ideas deleted rather than inherited.

## Risks

- 66 findings are open by distinct id once R-0840 lands, four of them High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12. The
  integrity gate's `high_blockers_open` check is WRONG about them, which is R-0648 and open.
- `packages/orchestration/overnight_readiness.py` has zero consumer edges and is DELETABLE but
  not deleted; only its group commit removes it. A half-deleted module is the state operator
  RULE 1 forbids.
<<<END PLAN4>>>

────────────────────────── C2 — THE RECORD AND THE SLIPS ──────────────────────────

ONE commit, two files.

(i) APPEND the two paragraphs between the RECORD4 markers to `.agent/live_review.md`, followed
by exactly one newline. They are TWO blank-line units — the round 3 gate entry, then the R-0840
registration. The file is 519228 bytes before this commit and ends with a newline; append a
single `\n` FIRST so the new units are separated from the current last one by a blank line.

(ii) APPEND the two paragraphs between the SLIPS4 markers to `.agent/prose_slips.md`, the same
way: one leading `\n`, then the text, then one newline. That file is 168030 bytes before this
commit. Both are reviewer-prose defects of ROUND 3 that left nothing wrong on disk, so under
amend0827 rule 2 they are dated lines here and NOT ids.

Do not renumber, reflow or edit anything already in either file.

<<<BEGIN RECORD4>>>
Gate: F275 R3 — the F275 round 3 entry. VERDICT PASS, booked by round 4 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 3 handback committed at `8325f20c` with the verdict appended at `280fd101`. Range `3068e9c1`..`8325f20c`, seven commits — C0a, C0b, C1, C2, C3, C4, C6 — every one single-parent, with no C5 commit because C5 is the measurement step and writes no file. THE CHANGE SET IS EXACTLY THE TWELVE PATHS the block named, by `git diff --name-status`, and the reviewer re-ran every gate itself against the COMMITTED blobs rather than reading the worker's report. THIS IS THE ROUND THAT MADE THE FIRST CARRY-OVER REAL: `packages/orchestration/mission_readiness.py` had been dead code since round 1, and round 3 gave it two consumers — the new `mission readiness` command and the cockpit's readiness section — while taking both away from `packages.orchestration.overnight_readiness`, which now has ZERO surviving consumer edges and is DELETABLE. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37, and NOT the emitted bytes: the reviewer's scratch original `.remedy-wt/f275-r3-FINAL.md`, the committed `.agent/authored/f275-r3.md` and the committed `.agent/last_block.md` are all 34166 bytes at `7e7d8cdc7fdfea446b5a1e01c03ab8fe07ab172bc82205cb27c0aca779d31d3b`. G2: `.agent/plan.md` byte-identical to its slice at 2425 bytes and 43 lines. G3 THE RECORD: `.agent/live_review.md` 515349 to 519228, the pre-blob an exact PREFIX, the slice plus one newline an exact SUFFIX, the new unit blank-line separated, units 215 to 216, `^Gate: ` 24 to 25, `^Gate: F275 R2 ` 0 to 1, and the OPEN SET UNCHANGED AT 65 BY DISTINCT ID — 68 distinct registrations against 3 distinct resolutions, subtracted over DISTINCT ids and never over the 5 `Done:` LINES. G4 THE WIRING: C3's real `git diff --numstat` columns are 12, 33, 6, 2, 0, 1 across six files, `ruff` exit 0 over all five touched python files, and `packages/orchestration/mission_readiness.py` is proved changed in its DOCSTRING ALONE by the strongest available reading — every byte after the closing triple quote is IDENTICAL to the base blob at `3068e9c1`, which subsumes the twenty-nine-definition count and does not depend on how a definition is counted. G5 THE RATCHETS ARE REAL AND THE REVIEWER PROVED BOTH DIRECTIONS AT `3068e9c1` BEFORE THE BLOCK WAS EMITTED: green with the round's edits, then RED on restoring the deleted map line, reporting `DISAPPEARED (1)` and naming that exact edge, and RED on removing the allowlist entry, naming `packages.orchestration.mission_readiness` as reachable-but-unlisted — which is the round's independent proof that the wiring really made the module reachable, since a module nothing imports cannot red that test. G6 THE CARRY-OVER IS BEHAVIOUR-PRESERVING, measured through the SHIPPED dispatch table rather than by importing the module: `apps.cli.grouped.build_parser()` parses the command path, and the `overnight.readiness` and `mission.readiness` handlers each emit 1097 characters differing in `generated_at` ALONE — the differing-key list with that key removed is EMPTY. G7 THE SUITES, each run alone: 48 · 645 · 506 · 42, all exit 0, and the discriminating count moved 639 to 645 exactly as predicted, which is the six new tests being real and collected rather than asserted. G8 THE TREE: the dotted path `packages.orchestration.overnight_readiness` occurs ZERO times in `packages/orchestration/ui_server.py` and ZERO times in `tests/orchestration/cluster_deletion_map.txt`, the map holds 19 recorded edges across 10 modules, and `packages/orchestration/overnight_readiness.py` is BYTE-IDENTICAL to its base blob; tree clean, no `.agent/STOP`, one worktree, branch pushed. FOUR DEVIATIONS WERE DECLARED AND ALL FOUR ARE SUSTAINED. The one that matters is the SECOND, and it is the REVIEWER'S ERROR: G3(a)'s formula `515349 + len(RECORD3) + 1` omits the LEADING newline that the same block's C2 operation requires, so it predicts 519227 where the correct result is 519228. The worker followed the OPERATION rather than the formula, landed the right bytes, and DECLARED the conflict instead of silently choosing one — which is exactly what constraint 1 asks of it. The reviewer re-measured: gain 3879 = 1 + 3877 + 1, prefix and suffix both exact. The first deviation is a reviewer anchor written short — edit (a)'s FIND text ended at `    # ── doctor` while the real line carries a banner tail — which the worker resolved by measuring both readings and using the only one that resolves; the committed diff shows the banner intact. The third is that "twenty-nine definitions" needs module-level bindings counted, not only `def` and `class`: 25 plus 4 equals 29, and the docstring-only proof is stronger either way. The fourth is the worker's own two gate readers being defective on first pass and corrected before reporting — reader bugs only, no disk state changed, and declaring them is the behaviour this workflow wants. NO FINDING IS MINTED BY THIS GATE and none is resolved; the two reviewer-prose defects are dated lines in `.agent/prose_slips.md`, per amend0827 rule 2, because nothing wrong reached disk.

- R-0840 — Medium, `remedy mission report` LOSES ITS RUN-KEYED DOGFOOD REPORT WHEN THE NAME IS HANDED TO THE CARRIED VIEW, AND THE LOST FIELDS HAVE NO HOME IN THE SURVIVING TREE. Raised by the reviewer at the F275 round 4 authoring, and registered because operator ruling amend0908-f275-finish RULE 3 orders it: "Where that removal takes away a behaviour a user could observe, the round REGISTERS a finding naming the behaviour and the feature that inherits the idea." THE RULE. DECISION F274 D2 rules that `mission report` is not free for the second carry-over until its current holder dies, so the carry-over and that deletion are one commit; RULE 3 then requires the observable loss to be recorded rather than discovered from a deleted file, exactly as R-0831 records the route-policy knobs. THE MEASUREMENT, taken at `280fd101`. `_cmd_mission_report` in `apps/cli/commands/worker_facade_cmd.py` reads `packages.orchestration.dogfood_run.build_mission_morning_report(run_id, job_id=job_id)`, is addressed by a dogfood RUN id, and prints five fields the carried view does not produce: `mission_status`, `final_status`, `stopped_because`, `steps_completed` and `operator_summary`. The catalog entry's positional argument is `run_id` and its options are `--job-id` and `--json`. After this round the same command name is addressed by a JOB id and answers from `build_overnight_report` in `packages/orchestration/mission_readiness.py`, whose payload the reviewer measured as byte-equal to `overnight report`'s but for `generated_at`. So the IDEA of a morning report survives and is inherited by `mission report` itself in its carried form; what is lost is the RUN-KEYED ADDRESSING and those five dogfood-run fields. WHAT IS NOT LOST HERE: `build_mission_morning_report` stays on disk in `dogfood_run` with its module-level tests in `tests/orchestration/test_dogfood_run.py`, and this round removes only the CLI path to it — the function dies later, with its own module group, which is why this id is registered now and resolved then. WHY THIS IS A FINDING AND NOT A REPAIR: AGENTS.md Scope Control forbids a stub, a shim, a copy or a compatibility reader by name, and RULE 3 repeats the prohibition, so nothing is rebuilt to preserve the run-keyed form. WHAT WOULD RESOLVE IT: the module group commit that deletes `dogfood_run` deleting these five fields with it, while DECISION F260 D3 names the run-keyed mission report among the ideas deleted rather than inherited and names this id. That paragraph is owed before the first `git rm` and is not written yet.
<<<END RECORD4>>>

<<<BEGIN SLIPS4>>>
2026-09-08 · F275 R3 · The round 3 block's gate G3(a) stated the post-append byte count as `515349 + len(RECORD3) + 1`, omitting the leading newline the same block's C2 operation orders, so it predicted 519227 against a correct 519228; the worker followed the operation, landed the right bytes and declared the conflict.

2026-09-08 · F275 R3 · The round 3 block's edit (a) gave its FIND anchor as `    # ── doctor`, a prefix of the real banner line rather than the whole line, so the anchor resolved only under the unterminated-prefix reading; the worker measured both readings before applying and used the one that resolves.
<<<END SLIPS4>>>

────────────────────────── C3 — THE CARRY-OVER AND THE DEATH (SPEC) ──────────────────────────

SEVEN labelled edits across FOUR files, ONE commit. The reviewer applied all seven in a
disposable worktree at `280fd101` and measured `git diff --numstat` as 7/4, 28/0, 0/27 and
2/38 — 37 insertions in total, far under the DECISION F104 D1 cap of 500.

(a) `apps/cli/command_catalog.py` — REWRITE the `mission.report` entry. FIND these lines, which
occur exactly once, and replace them with the block beneath:

  FROM:
        description="Generate a safe morning report — what happened, is it done, what to do next (read-only; no execution; no raw logs).",
        action_class="read_only",
        args=(
            ArgDef("run_id", "Run ID"),
            ArgDef("--job-id", "Job UUID", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.run", "dogfood.morning-report"),

  TO:
        description="Read-only morning-style report built from the job's current evidence.",
        action_class="read_only",
        args=(
            _JOB_ID,
            ArgDef("--markdown", "Render the report as markdown",
                   required=False, is_option=True, default="false"),
            _JSON_OPT,
        ),
        supports_json=True,
        may_mutate_repo=False,
        may_execute_commands=False,
        related=("mission.readiness", "mission.show"),

The `command_id`, `group_id` and `subcommand` lines above this region are NOT touched, which is
what keeps `mission.report` continuously present in the catalog per constraint 8.

(b) `apps/cli/commands/mission_cmd.py` — INSERT the carried handler and register it. FIND the
single line

COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {

and REPLACE it with the handler, two blank lines, that same line, and the registration:

def _cmd_mission_report(job_id: str, *, markdown: bool = False,
                        json_output: bool = False) -> None:
    """Read-only morning-style report built from the job's current evidence.

    The second of the two carry-overs F260's Design orders before the cluster
    deletion, landing on the name DECISION F274 D2 reserved for it. It reads
    ``packages/orchestration/mission_readiness.py`` — the module rounds 1 and 2
    carried — and never the cluster.
    """
    from packages.orchestration.mission_readiness import (
        build_overnight_report,
        render_overnight_report_markdown,
    )
    data = build_overnight_report(str(job_id))
    if markdown:
        print(render_overnight_report_markdown(data))
        return
    if json_output:
        print(_json.dumps(data, indent=2))
        return
    print(render_overnight_report_markdown(data))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "mission.report": lambda args: _cmd_mission_report(
        args.job_id,
        markdown=getattr(args, "markdown", False),
        json_output=getattr(args, "json", False),
    ),

The module already imports `json as _json`. The flag order is constraint 7's and is not a choice.

(c) `apps/cli/commands/worker_facade_cmd.py` — DELETE the old handler together with the banner
that titles it: the region beginning with the line

# ---------------------------------------------------------------------------

that carries `# mission report facade (Step 2625)` on its second line, through the last line of
`_cmd_mission_report`, which is

    print(f"  summary: {report.operator_summary}")

and the two blank lines that follow it. The next surviving line is the `# ----` banner opening
`# doctor core (Step 2665)`. Dropping the banner with the class it titles is the same reading
round 2 took for `# Plan (1256)` and the reviewer sustained.

(d) `apps/cli/commands/worker_facade_cmd.py` — DELETE the single registry line

    "mission.report": _cmd_mission_report,

(e) `tests/cli/test_worker_facade_cmd.py` — the registry expectation loses the moved id.

  FROM:        expected = {"worker.doctor", "worker.add", "worker.disable",
                    "mission.run", "mission.report", "doctor.core",
  TO:          expected = {"worker.doctor", "worker.add", "worker.disable",
                    "mission.run", "doctor.core",

(f) `tests/cli/test_worker_facade_cmd.py` — the facade count pin.

  FROM:        assert len(facade_cmds) == 12
  TO:          assert len(facade_cmds) == 11

(g) `tests/cli/test_worker_facade_cmd.py` — DELETE the deleted handler's own tests: the `# ----`
banner carrying `# mission report facade`, the whole of `class TestMissionReport` with its two
test methods, and the two blank lines after it; the next surviving line is the `# ----` banner
opening `# collect_all_handlers includes facade`. ALSO delete the single line

_MORNING_REPORT = "packages.orchestration.dogfood_run.build_mission_morning_report"

which is that class's only user — the reviewer measured it at 2 occurrences in the file at
`280fd101`, the definition and the one `@patch` that goes with the class. Under operator RULE 1
a handler's tests die in the commit that deletes the handler; leaving them would red the suite.
`patch`, `MagicMock` and `pytest` all keep other users in that file, so no import is removed —
the reviewer confirmed this by running `ruff` over the file after the deletion.

────────────────────────── C4 — THE TESTS (SPEC) ──────────────────────────

APPEND to `tests/cli/test_mission_cmd.py`, after its final newline, exactly two blank lines and
then the class below. It joins the class round 3 added, which is the last thing in that file.

class TestMissionReportIsTheCarriedReportView:
    """F275 T001: the second carry-over, and the death of the name's old holder.

    DECISION F274 D2 rules that `mission report` is not free until its current
    holder dies, so the two happen in one commit. These tests pin both halves:
    the name now resolves to the carried view in `mission_cmd`, and the facade
    in `worker_facade_cmd` no longer provides it.
    """

    JOB_ID = "11111111-2222-3333-4444-555555555555"

    def test_the_catalog_entry_is_job_keyed_now(self):
        from apps.cli.command_catalog import get_command

        names = [a.name for a in get_command("mission.report").args]

        assert names == ["job_id", "--markdown", "--json"]

    def test_the_facade_no_longer_provides_the_command(self):
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS

        assert "mission.report" not in COMMAND_HANDLERS

    def test_the_dispatch_table_still_reaches_it(self):
        from apps.cli.commands import collect_all_handlers

        assert "mission.report" in collect_all_handlers()

    def test_the_real_cli_answers_with_the_carried_report(self, project):
        data_root, _project_id = project

        body = json.loads(_run(["mission", "report", self.JOB_ID, "--json"],
                               data_root).stdout)

        assert "report" in body
        for key in ("completed_checklist", "blocked_checklist", "completed_count",
                    "blocked_count"):
            assert key in body["report"], f"the carried report lost {key}"

    def test_the_facade_module_no_longer_names_the_cluster_builder(self):
        """The CLI path to the cluster builder is what this round removed."""
        source = (REPO_ROOT / "apps" / "cli" / "commands" / "worker_facade_cmd.py").read_text(
            encoding="utf-8")

        assert "build_mission_morning_report" not in source
        assert "_cmd_mission_report" not in source

`json`, `Path` and `REPO_ROOT` are already imported at the top of that file, and `project` is its
existing fixture. The last test's two tokens were measured at 2 occurrences each at `280fd101`
and are 0 after edits (c) and (d); the file still imports `dogfood_run` for `mission run`, which
is why the assertion names these two symbols and NOT the module.

────────────────────────── C5 — THE GATES ──────────────────────────

Run ALL EIGHT at C5, after C4 and STRICTLY BEFORE the C6 handback commit, so the handback can
quote every one of them (§3 item 31). C5 writes no file and has no commit. Report ONE LINE PER
GATE with the REAL exit code. A gate that cannot be run is reported as not run — never as green.

EVERY GATE BELOW WAS RUN BY THE REVIEWER AT THE BASE `280fd101` BEFORE EMISSION, and each carries
its BASE reading beside its expected one, per the procedure finding R-0819's recurrence paragraph
strengthened from a clause. Readings that are deliberately NON-DISCRIMINATING are labelled as
such. The open fix clause R-0741 carries — a grep-derived leave-alone set naming each hit by file,
line and enclosing symbol — is DECLINED AS NOT APPLICABLE on its own terms: it binds "the next
block that orders such a set", and this block orders none.

G1 TRANSPORT. sha256 and byte count of the scratch original `.remedy-wt/f275-r4-FINAL.md`, of the
committed `.agent/authored/f275-r4.md`, and of the committed `.agent/last_block.md`. All three
must be ONE value. Per §3 item 37 this proves the chain this workflow can walk — saved copy,
mirror, working copy — and NOT the bytes the reviewer emitted; do not claim more.

G2 THE PLAN. `.agent/plan.md` byte-identical to PLAN4. Report its sha256, byte count, line count
(under the AGENTS.md cap of 50), and that `^## Goal$` and `^## Next Steps$` occur once each.

G3 THE RECORD. Six parts over `.agent/live_review.md`, plus one byte-equality reading for
`.agent/prose_slips.md`, which is a `.agent/` prose file and earns no more under the gate budget.
  (a) BYTES: 519228 before; after = 519228 + 1 + len(RECORD4) + 1. State the operation's result
      and both the before and after counts. If any formula in this block disagrees with the
      OPERATION ordered in C2(i), THE OPERATION WINS and the disagreement is declared — round 3
      lost a deviation to exactly this and the reviewer would rather be told twice.
  (b) EXACT EDGES: the pre-commit blob is a byte-exact PREFIX of the post-commit blob, and
      RECORD4 is a byte-exact SUFFIX of it. Report both booleans.
  (c) ORDERED EQUALITY by an independent paragraph reader: compare the LAST N blank-line units of
      the whole file against RECORD4's N paragraphs IN ORDER, where N is COUNTED FROM THE SLICE by
      your script and is NEVER taken from this block. Report N and the per-unit sha256 pairs.
  (d) NEGATIVE CONTROL on the FIRST appended paragraph, in scratch or memory only: flip one byte
      inside it and confirm BOTH the reader of (b) and the reader of (c) REJECT it. Re-read the
      tracked file afterwards and report its byte count to show the mutation never touched it.
  (e) COUNTS: blank-line units 216 → 218; `^Gate: ` 25 → 26; `^Gate: F275 R3 ` 0 → 1;
      `^- R-0840 — ` 0 → 1.
  (f) THE OPEN SET GAINS EXACTLY ONE: distinct `^- R-\d+ — ` ids 68 → 69, distinct
      `^Done: R-\d+ — ` ids 3 → 3, OPEN SET BY DISTINCT ID 65 → 66. Subtract DISTINCT IDS, never
      the 5 `Done:` LINES. This round mints R-0840 and resolves none.
  (g) `.agent/prose_slips.md`: 168030 before; after = 168030 + 1 + len(SLIPS4) + 1; the pre-blob
      an exact PREFIX and SLIPS4 an exact SUFFIX. Two readings, no arithmetic proof beyond them.

G4 THE CARRY-OVER AND THE DEATH. Over the C3 commit: `git diff --numstat` must read 7/4, 28/0,
0/27 and 2/38 for the four files in the order (a)/(b)/(c,d)/(e,f,g) — report the real columns
whatever they are. `python3 -m ruff check` exit 0 over `apps/cli/command_catalog.py`,
`apps/cli/commands/mission_cmd.py`, `apps/cli/commands/worker_facade_cmd.py` and
`tests/cli/test_worker_facade_cmd.py`; `ast.parse` clean on all four. Then the death, measured in
`apps/cli/commands/worker_facade_cmd.py`: `_cmd_mission_report` occurs ZERO times (BASE 2) and
`build_mission_morning_report` occurs ZERO times (BASE 2). Then the survival, in the SAME file:
`packages.orchestration.dogfood_run` occurs TWO times (BASE 3) — `mission run` keeps its import,
and a reading of 0 here would mean the round deleted more than it was asked to.
`packages/orchestration/dogfood_run.py` and `packages/orchestration/mission_readiness.py` are
BYTE-IDENTICAL to their blobs at `280fd101`; read them with `git show 280fd101:<path>` into
memory or gitignored scratch, never by overwriting the tracked file (§3 item 29, guardrail G5).

G5 THE MAP DOES NOT MOVE, AND THAT IS THE POINT. `python3 -m pytest
tests/orchestration/test_cluster_deletion_map.py tests/orchestration/test_import_reachability.py
-q` exit 0. Then, through the shipped reader `recorded_edges()`: the edge set still holds
`('packages.orchestration.dogfood_run', 'apps/cli/commands/worker_facade_cmd.py')`, and the total
is 19 edges over 10 modules — IDENTICAL to round 3's close. BASE reading: 19 and 10, with that
edge present. This gate is deliberately an EQUALITY rather than a decrease: the discrimination is
carried by G4's 3 → 2 occurrence count, which proves one of the three import sites really went
while the edge legitimately survived on the other two. A round that reported a shrinking map here
would have deleted something it was not asked to.

G6 THE CARRY-OVER IS BEHAVIOUR-PRESERVING. Through the SHIPPED dispatch table, not by importing
the module: build the parser with `apps.cli.grouped.build_parser()` and parse
`["mission","report","11111111-2222-3333-4444-555555555555","--json"]`; then call BOTH
`collect_all_handlers()["overnight.report"]` and `collect_all_handlers()["mission.report"]` on
that namespace, capture each one's stdout, and compare the two JSON payloads. They must differ in
`generated_at` ALONE — report the full differing-key list and the list with `generated_at`
removed, which must be EMPTY. The reviewer measured 1225 characters from each and
`['generated_at']` as the only difference. BASE reading at `280fd101`: the same parse raises
`SystemExit` because the old entry's positional is `run_id` and `--markdown` is not a flag it
declares, and the two handlers' payloads are not comparable at all — so this gate is UNMEETABLE
at the base and fully discriminating.

G7 THE SUITES, each run ALONE and serially, in this order. Report the real exit code and passed
count for each:
  1. `python3 -m pytest tests/cli/test_worker_facade_cmd.py tests/cli/test_product_spine.py
     tests/orchestration/test_cluster_deletion_map.py
     tests/orchestration/test_import_reachability.py -q`
     BASE 148, expected 146 — DISCRIMINATING DOWNWARD: edit (g) deletes exactly two tests, and
     this is the reading that separates "the tests died with their handler" from "a test was left
     behind" and from "something else was deleted too".
  2. `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py
     tests/cli/test_mission_cmd.py -q`
     BASE 645, expected 650 — DISCRIMINATING UPWARD: C4 adds exactly five tests, counted from the
     class above and not asserted from memory.
  3. `python3 -m pytest tests/orchestration/test_dogfood_run.py -q`
     BASE 135, expected 135 — NO-REGRESSION, and it is the gate for constraint 5: the cluster
     builder keeps every one of its module-level tests because only the CLI path to it went.
  4. `python3 -m pytest tests/cli/test_golden_path.py -q`
     BASE 42, expected 42 — the canary, NO-REGRESSION.

G8 THE TREE. All of: `.agent/STOP` does not exist; `git status --porcelain` is EMPTY; the branch
is `feature/f275-one-world-completion-part-three`; `git worktree list` shows ONLY the primary
checkout; and `git log --oneline` over this round's range shows C0a, C0b, C1, C2, C3, C4 in that
order, each single-parent. C6's OWN numbers are ordered NOWHERE: under
docs/agents/self_drive_protocol.md there is no second window, so a value routed to a "round
report" is written to a channel that ends with the session (§3 item 31). The REVIEWER measures
C6's commit and its numstat columns itself at the next gate and records them in that round's
ledger entry. Do not guess them and do not leave a blank where they would go.

────────────────────────── C6 — THE HANDBACK ──────────────────────────

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. NO length cap (amend0827 rule
3); valid when its mandated sections are present. It MUST carry: the state block naming FEATURE
F275, ROUND 4, SESSION 2, the branch, the base `280fd101` and every commit SHA; the changed-files
table with the REAL `git diff --numstat` columns per commit, taken from the tool and not
re-derived (§3 item 28); ONE LINE PER GATE with its real exit code, plus the G3, G4, G5, G6 and
G7 transcripts; the open-findings count (66 by distinct id after R-0840); the item-status table
covering C0a, C0b, C1, C2, C3, C4, C5, C6 and G1 to G8 exactly once each; the deviations; the
Fortschritt line below verbatim; ONE SENTENCE of context self-assessment per amend0905-throughput;
and the next expected action — the route-policy knob check against F110's config keys updating
R-0831, riding with `.agent/f275_deletion_order.md`, which operator RULE 2 requires written before
the first `git rm`. Write NO verdict: the verdict is the reviewer's and is written after this
commit.

Fortschritt: ~28 % (T001: Claim ✅ · Record ✅ · D1 ✅ · Carry-over readiness ✅ · Carry-over
report ✅ · Kante geschnitten ✅ · Löschreihenfolge offen · F260 D3 offen · Löschung offen ·
T002 offen · T003 offen) — Schätzung
