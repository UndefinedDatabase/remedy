── STEP T002 (last item) / F272 — round 15 ──
Goal:   Give the Mission record the last two fields DECISION F260 D1 names — the
        ORDER it came from and its CONTRACT — both ADDITIVE and OPTIONAL, so
        every mission record already on disk stays byte-identical.
Base:   `998151b8`. Branch `feature/f272-one-world-completion`. SESSION 8.

THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED: C4 is a numbered SPECIFICATION
and you write the code. The marker-delimited slices are byte-verbatim.

## Provenance, and the one failure that is not yours

The reviewer APPLIED this whole change in a disposable worktree at `998151b8`,
ran the suites, and removed the worktree by exact path before authoring this
block; every figure below is measured, not predicted. IF YOU RUN ANY SUITE IN A
WORKTREE, `test_test_runner.py::TestVitestFrontendTestFoundation::
test_vitest_passes` fails with `ERR_MODULE_NOT_FOUND` from `vitest.config.ts` —
the missing-`node_modules` artifact, not this change. In the primary checkout,
where G6 runs, it passes.

The feature files' "D9 shape" reference resolves to `DECISION amend0905-vocab D9`
at `docs/system/vocabulary.md:233`, NOT to a missing F260 decision as the round
14 handback concluded; under it F269 builds the contract, so this round invents
no shape and lands the field RESERVED. DECISIONR15 carries the full ruling.

## Bundle (ordered; commit in this order, nothing added or reordered)

- C0a save this block to `.agent/authored/f272-r15.md` by `shutil.copyfile`
- C0b mirror the same source to `.agent/last_block.md` by `shutil.copyfile`
- C1  `.agent/plan.md` REPLACED by the PLANF272R15 slice
- C2  `.agent/live_review.md` APPEND the RECORDR15 slice
- C3  `.agent/prose_slips.md` APPEND SLIPSR15; `docs/roadmap/features/T2_F272.md`
      APPEND DECISIONR15 — both in this one commit
- C4  the extension, spec S1 through S8 below, over `mission_state.py` ONLY
- C5  `tests/orchestration/test_mission_state.py` — the two import pairs P1 and
      P2, then APPEND the TESTSR15 slice, all in this one commit
- C6  rewrite `.agent/handoff.md`

C4 and C5 are separate because C5's tests are NEW guards, not the extension, and
because C4 alone leaves the tree GREEN — nothing asserts the new fields until C5
adds them, so there is no knowingly-red intermediate. C5's import pairs and its
append are ONE commit because the appended class references `MissionOrder`,
`set_mission_order` and `set_mission_contract`: splitting them would commit a
tree that fails to import.

## Change set — these paths and no others

    .agent/authored/f272-r15.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/roadmap/features/T2_F272.md
    packages/orchestration/mission_state.py
    tests/orchestration/test_mission_state.py
    .agent/handoff.md

## C4 — the specification, over `packages/orchestration/mission_state.py`

Write this yourself, in the file's own idiom: two-space sentence gaps in
docstrings, `dataclass(frozen=True)` records with `to_json` / `from_json` pairs,
a one-line WHY above each definition. Every name below is public surface and is
spelled EXACTLY as given, because TESTSR15 imports them. No new import is
needed: `dataclass`, `replace`, `Any` and `Path` are already imported at
`mission_state.py:48-60`.

S1 — a new frozen record `MissionOrder`, placed directly ABOVE `class Mission`
and below `class MissionJobLink`. Fields, in this order, all defaulting to the
empty string: `text`, `source_path`, `source_sha256`. DECISION F260 D1 words the
order as "text, or file path + sha256"; carry all three rather than a union,
because they answer different questions — the text is what Remedy acted on, the
path and digest are what a later reader checks the file against. Its WHY comment
says that. The digest field is spelled to match `JobPlan.job_file_sha256`, which
the vocabulary page's Order row names as the same concept under another name.

S2 — `MissionOrder.to_json()` returns exactly those three keys. Its `from_json`
classmethod raises `ValueError("mission order must be an object")` for anything
that is not a dict, and otherwise coerces each of the three through `str()` with
`""` as the default, which is what `MissionJobLink.from_json` already does.

S3 — two new fields on `Mission`, declared immediately after `mission_plan` so
the dataclass field order stays stable: `order: MissionOrder | None = None` and
`contract: dict[str, Any] | None = None`.

S4 — `Mission.to_json` writes EACH of the two keys ONLY when its value is not
None, in the same shape and for the same stated reason as the `mission_plan`
block directly above it. `order` is written as `self.order.to_json()`. THIS IS
THE ADDITIVE PROPERTY AND IT IS WHAT G5 MUTATES: a mission that has neither
field must produce a body with neither key, so that records written before this
round stay byte-identical.

S5 — `Mission.from_json` reads both back and passes them to the constructor. A
present `order` becomes a `MissionOrder` via its `from_json`, an absent one stays
None; a `contract` that is present and not a dict raises `ValueError("mission
contract must be an object")`, mirroring the `mission_plan` check above it.

S6 — the `Mission` class docstring gains a paragraph documenting both fields
where it already documents `dossier_ref` and `mission_plan`. It must state that
both are additive and optional on `mission_plan`'s terms, and that `contract` is
RESERVED for F269 per DECISION amend0905-vocab D9 in
`docs/system/vocabulary.md`, exactly as `dossier_ref` is reserved for the
dossier. A reader who searches this class for "contract" must land on that.

S7 — two setters, `set_mission_order` and `set_mission_contract`, placed
directly below `set_mission_plan` and above `resolve_mission_id`. Each takes
`(project_id, mission_id, <value>, root=None)`, validates its argument type and
raises `MissionError` on a bad one, then loads, `replace`s the single field,
saves and returns the updated `Mission` — the exact body shape `set_mission_plan`
already has. They touch nothing else: not the goal, which stays immutable, not
the status, not the job chain. `set_mission_contract`'s docstring names F269 and
D9 as the owner of what goes in it.

S8 — `MISSION_SCHEMA_VERSION` IS NOT TOUCHED; it stays `1`. The additive design
exists so it need not move, and `test_mission_compiler.py:649` asserts it.

## C5 — the two import pairs, over `tests/orchestration/test_mission_state.py`

Both keep the existing alphabetical order of that import block, which is what
ruff's `I` rules check. Each FROM occurs EXACTLY 1x, measured at `998151b8`.
Both are APPEND-shaped; the containment test prints `TO contains FROM: true` for
each, so neither gets a FROM-zero count. Apply them at the indentation shown —
these fenced blocks add nothing to any content line.

P1 FROM:

```
    MissionNotFoundError,
    MissionVerifyFirstError,
```

P1 TO:

```
    MissionNotFoundError,
    MissionOrder,
    MissionVerifyFirstError,
```

P2 FROM:

```
    save_mission,
    set_mission_status,
```

P2 TO:

```
    save_mission,
    set_mission_contract,
    set_mission_order,
    set_mission_status,
```

## Constraints

1. EVERY MARKER-DELIMITED SLICE IS APPLIED BYTE FOR BYTE, extracted
   PROGRAMMATICALLY from `.agent/authored/f272-r15.md` between its BEGIN and END
   marker lines. Never retype, reflow or fix one: if a slice looks wrong, APPLY
   IT ANYWAY and say so in the handback — the reviewer rules. Report how many
   you extracted; this block deliberately states no count of its own parts.
2. No marker line reaches any file but the two C0 copies.
3. No file outside the change set is edited, and no existing test is edited,
   deleted or weakened. C5 only ADDS: two import lines and one appended class.
4. TESTSR15 begins with its own TWO blank lines, so C5's append is
   `pre + slice` with NO separator inserted. Assert the pre-image's terminal
   byte is exactly one newline before writing.
5. NO FINDING ID IS MINTED this round. The round 14 deviations and the D9
   mis-resolution are reviewer-prose matters under amend0827 rule 2; SLIPSR15
   carries them. The next free id remains R-0822.
6. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C6,
   and report all three readings. Stop and hand off if it ever exists.
7. Every commit boundary runs `git status --porcelain` and its REAL output is
   reported. Destructive verification (G5 only) runs in a disposable worktree and
   NEVER in the primary checkout; remove it BY EXACT PATH, never by glob.

## Done when — the eight gates

Run each and record its REAL exit code. "Green" as a word is a finding. G1-G4
and G6-G8 run in the PRIMARY checkout; G5 runs only in its own worktree. All
eight run BEFORE C6, so the handback can quote them.

G1 TRANSPORT — one digest comparison: `.agent/authored/f272-r15.md`,
`.agent/last_block.md` and `.remedy-wt/f272-r15-block.md` share one sha256, one
byte length and one line count. Report all three.

G2 THE RECORD — the append into `.agent/live_review.md`, four readers.
(a) BYTE: pre is 1145308 bytes, terminal bytes `b'ally.\n'`, exactly one
newline; `post == pre + b"\n" + slice`; pre is a byte-exact PREFIX of post.
(b) STRUCTURAL: N is COUNTED BY YOUR SCRIPT from the slice's own blank-line
paragraphs, never taken from this block; the LAST N units of the whole file
equal the slice's N paragraphs IN ORDER, and everything before is unchanged.
(c) NEGATIVE CONTROL: flip one byte inside the FIRST appended paragraph, in
memory and never on disk; both (a) and (b) must REJECT, and both must ACCEPT
once restored.
(d) COUNTS, before -> after: `^- R-\d{4}` distinct 305 -> 305; `^Done: R-\d{4}`
distinct 248 -> 248; open set BY DISTINCT ID 57 -> 57; `^Gate: ` 36 -> 37;
`^Gate: F272 R14 ` 0 -> 1.

G3 THE PLAN — `.agent/plan.md` byte-equals the PLANF272R15 slice. Report byte
count, line count, that it is under the AGENTS.md cap of 50, and that `## Goal`
and `## Next Steps` are present.

G4 THE EXTENSION IS REAL — measured by IMPORTING the shipped module and printing
its resolved `__file__`, never by grepping the diff. Report all seven readings:

    (i)   a mission created with neither field: "order" and "contract" are both
          ABSENT from to_json()
    (ii)  a legacy record (schema_version 1, no order, no contract) loads, gives
          order None and contract None, and re-exports BYTE-IDENTICALLY
    (iii) set_mission_order round-trips a MissionOrder through disk unchanged
    (iv)  set_mission_contract round-trips a dict through disk unchanged
    (v)   MISSION_SCHEMA_VERSION is still 1
    (vi)  Mission.from_json refuses a non-object order and a non-object contract
    (vii) writing an order leaves the immutable goal unchanged

G5 MUTATION RED-PROOF — in a disposable worktree at THIS round's C5 commit,
never in the primary checkout. Purge `__pycache__` and use `python3 -B`. FIRST
probe provenance by printing `mission_state.__file__` and confirming it resolves
INSIDE the worktree, because an editable install can shadow it.
  - UNMUTATED CONTROL, reported beside the mutated run:
    `python3 -B -m pytest tests/orchestration/test_mission_state.py -q -p no:randomly`
    The reviewer measured EXIT 0 at 88 passed.
  - MUTATION, in `packages/orchestration/mission_state.py` — that exact path.
    THE MUTATION IS ORDERED AS A PROPERTY, not as bytes, because you wrote the
    code: make `Mission.to_json` write the `"order"` key UNCONDITIONALLY, so it
    is present even when `self.order` is None, changing nothing else. Report the
    exact lines you replaced and the count of that span in that file before
    replacing — it must be 1. Re-run the same command. The reviewer measured
    EXIT 1 at 2 failed, 86 passed.
  - ORDERED COLOUR: control green THEN mutated red, and report WHICH tests fell
    by name. The reviewer measured exactly
    `test_a_mission_that_has_neither_writes_neither_key` and
    `test_a_record_written_before_this_round_re_exports_byte_identically`.
    If a different set falls, report it rather than adjusting anything.
    Remove the worktree BY EXACT PATH and show `git worktree list` after.

G6 THE SUITES — run SERIALLY, each its own invocation, each `-q -p no:randomly`,
all in the primary checkout. The four state readers are run AS FOUR:

    python3 -B -m pytest tests/orchestration/ -q -p no:randomly
    python3 -B -m pytest tests/ui_server/ -q -p no:randomly
    python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly
    python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly
    python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly
    python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
    python3 -B -m pytest tests/docs/ -q -p no:randomly
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly

`tests/orchestration/` base is 12850 passed and 10 skipped. COUNT the tests C5
adds with `ast` over that file before and after — do not take a number from this
block — and RECONCILE as 12850 + <your count>, reporting the arithmetic and any
difference rather than adjusting it. The reviewer's own AST count was 6.
`test_roadmap_index` and `tests/docs/` are ordered because C3 writes
`docs/roadmap/**`.

G7 LINT AND INTEGRITY:

    python3 -m ruff check packages/orchestration/mission_state.py tests/orchestration/test_mission_state.py
    python3 -m apps.cli.grouped integrity check --json

Bare `ruff` is denied to this environment; the `python3 -m` spelling is ordered.
Report both exit codes and, for integrity, `passed` and `fail_count`.

G8 THE TREE — `git status --porcelain` empty at every commit boundary and at the
end; `git ls-files .remedy-wt` empty; `git worktree list` showing the primary
plus the twelve pre-existing `remedy/job-*` entries and nothing else. Then the
per-commit insertions from `git diff --numstat <parent> <commit>`, EXCLUDING C6,
which cannot count its own insertions. Each must be under the DECISION F104 D1
cap of 500 and match the `## Commits` table of the handback cell for cell. For
scale only, the reviewer's worktree run produced 90 insertions for C4's file and
88 for C5's; yours will differ if you write S1-S8 differently, and a difference
is a fact to report, not a target to hit.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md, carrying
SESSION 8, the changed-files table with real `+/-` from `git diff --numstat`,
ONE LINE PER GATE with its real exit code, and an item-status table covering C0a
through C6 exactly once each. No length cap applies (amend0827 rule 3). Declare
every deviation. Push `feature/f272-one-world-completion`; create NO PR, merge
nothing, force-push nothing.

<<<BEGIN PLANF272R15>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 14 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE.
T002 has landed the eight administrative fields, widened `RunState`, renamed
`JobPlan.status` to `state`, retyped that field onto `RunState`, given `blocked`
and `stopped` their place in the cockpit, and now completes the Mission record.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

The Mission extension, T002's last item: `Mission.order` and `Mission.contract`,
the two fields of DECISION F260 D1 that had no counterpart on the record. Both
are ADDITIVE and OPTIONAL on the terms `mission_plan` already set, so
`MISSION_SCHEMA_VERSION` does not move and every mission record already written
stays byte-identical. The contract lands RESERVED and empty for F269, per
DECISION amend0905-vocab D9, which DECISION F272 D11 resolves the feature files'
"D9 shape" reference to.

## Next Steps

1. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
2. T004, the classic runner and the resolver collapse.
3. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- T002 completes here, so the next round opens T003, whose eleven consumers are
  measured in F260's file by line citation rather than listed here. Read that
  list from `T2_F260.md` before scoping, never from memory: DECISION F272 D7
  records what a site set inferred rather than measured cost this branch.
<<<END PLANF272R15>>>

<<<BEGIN RECORDR15>>>
Gate: F272 R14 — the F272 round 14 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `6c2225b8`..`0554bb5f`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the change set exactly the eleven ordered paths and nothing else. G1 TRANSPORT is a REAL chain and not merely self-consistent: the reviewer's own scratch original `.remedy-wt/f272-r14-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r14.md` and `.agent/last_block.md` are all 27108 bytes at 399 lines and all hash to `ad0f32b61f0488c27d0752f058fbe49a1faf1b7cec0e6b89b38ebfb209a78a87`; per §3 item 37 that covers the saved copy and its mirror, not the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte: `.agent/live_review.md` 1138931 to 1145308, pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE; registrations 305 unchanged, resolutions 248 unchanged, open set BY DISTINCT ID 57 unchanged, `^Gate: ` 35 to 36, `^Gate: F272 R13 ` 0 to 1. G3 THE PLAN is 1850 bytes byte-equal to its slice at 38 lines against the cap of 50. G4 THE RETYPE reproduces against the SHIPPED module: every construction path — default, raw literal, `JOB_*` constant and imported record — yields `RunState`; `JOB_BLOCKED` is a `RunState` and still equals `"blocked"`; the nine members are unchanged; `type(_export_job(job)["status"]) is str` is True; and a legacy record whose status is `complete` still loads and exports back unchanged, so DECISION F272 D5 holds. G5 THE RED-PROOF was re-run by the reviewer in its own disposable worktree, removed afterwards by exact path: the unmutated control is EXIT 0 at 12 passed, and with `_export_job`'s `.value` removed the run is EXIT 1 with ELEVEN TESTS STILL PASSING and only `test_the_exported_status_is_a_plain_str_and_not_a_run_state` failing — every pre-existing guard is blind to the missing `.value`, and only the new discriminator sees it. G6 THE SUITES, re-run serially: `tests/orchestration/` EXIT 0 at 12850 passed and 10 skipped, being the reviewer's own base of 12847 plus exactly the three tests C5 adds; `tests/ui_contracts/` EXIT 0 at 809 passed and 4 skipped; `tests/docs/` EXIT 0 at 303; the canary EXIT 0 at 42. G7 ruff EXIT 0 over the four changed `.py` files, integrity EXIT 0 with `"passed": true` and `"fail_count": 0`. G8 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, thirteen worktree entries, and per-commit insertions 399, 375, 17, 4, 41, 34 and 29, each under the DECISION F104 D1 cap of 500.

Gate: F272 R14 deviations — BOTH UPHELD, NEITHER SPENDING AN ID. Deviation 1 is THE REVIEWER'S DEFECT, NOT THE WORKER'S: the round 14 block rendered its C4 pairs inside markdown code blocks without a consistent rule for the fence indent, so P5's FROM appeared with 4 leading spaces where the file has 8, while P6 and P7's appeared with 4 where the file also has 4 — the same convention giving the right answer in one pair and the wrong one in another. The worker resolved it from the block's own count assertions, which only the 8-space reading can satisfy, applied every pair at the file's real indentation, and reported that every pre-edit FROM count matched. Nothing wrong reached disk, so no id is spent, and the round 15 block adds no indent to any fenced content line. Deviation 2 is accepted and confirmed: the two marker substrings in `.agent/live_review.md` are pre-existing and mid-line, the line-anchored count is 0 before and after, and RECORDR14 contributed neither. THE WORKER'S TWO CLOSING NOTES ARE CONFIRMED AND BINDING: C4 inserted 19 lines above them, so the two record boundaries are now `packages/orchestration/pingpong_job.py:686` and `:2987` and the protected f-string is at `:3045`, untouched byte for byte; a later block citing 667, 2968 or 3026 would cite the wrong lines.
<<<END RECORDR15>>>

<<<BEGIN SLIPSR15>>>
2026-09-07 — F272 R14 — the round 14 block rendered its C4 FROM/TO pairs inside markdown code fences at an indentation unrelated to the target line's own, so P5's FROM was shown with 4 leading spaces where `pingpong_job.py` has 8 while P6 and P7 were shown correctly at 4; the worker resolved it from the block's own count assertions, applied every pair at the file's real indentation, and declared it, so nothing wrong reached disk.

2026-09-07 — F272 R14 — the round 14 handback recorded that the "D9 shape" reference in `docs/roadmap/features/T2_F260.md:23` "resolves to no DECISION that exists", having searched only the F260 and F272 DECISION lists, and the round 15 reviewer carried that reading forward until it grepped the binding vocabulary page and found `DECISION amend0905-vocab D9` at `docs/system/vocabulary.md:233` giving the contract to F269 — the A1 trap docs/agents/planner_reviewer_prompt.md §0 names, since a reviewer verdict written into a handback is not thereby a measurement. Nothing was built on the wrong reading; DECISION F272 D11 records the resolution.
<<<END SLIPSR15>>>

<<<BEGIN DECISIONR15>>>

### DECISION F272 D11 (2026-09-07, F272 round 15) — the "D9 shape" the Mission contract is owed is `DECISION amend0905-vocab D9` in the binding vocabulary page, and under it the contract lands RESERVED

CONTEXT. This file's T002 line and `docs/roadmap/features/T2_F260.md:23` both
describe the Mission contract as "(D9 shape; may be empty until F269 fills it)".
Neither names the document D9 lives in. F260's own DECISIONs run D-A and D0
through D8, and F272's own D9 is the unrelated run-state phrase guard of round
12, so a reader searching either feature file finds nothing — which is what the
round 14 handback concluded, in those words, and it is wrong.

MEASURED at `998151b8` by grep over `docs/` and `.agent/decisions.md`: `DECISION
amend0905-vocab D9 (2026-09-05, operator order amend0905-vocab-rebuild) —
contract and templates` exists at `docs/system/vocabulary.md:233`. That page is
BINDING — F259 made it so and `tests/docs/test_vocabulary.py` enforces it. Its
Contract row at line 32 defines the concept, and D9 rules that the contract is
compiled from the order by the planner, that its two halves today are
`PlannedTask.acceptance` and `packages/orchestration/dod_compiler.py`, that four
templates ship first, and — in its own words — that **F269 builds the contract**.

CHOSEN. The reference resolves to that decision, and this round therefore INVENTS
NO SHAPE. `Mission.contract` lands as `dict[str, Any] | None = None`: ADDITIVE,
OPTIONAL and RESERVED, written to the record only when a value exists, so
`MISSION_SCHEMA_VERSION` does not move and every record already on disk stays
byte-identical. `None` and an absent key both mean "no contract compiled yet",
which is the truth for every mission today. F269 fills it. That is exactly the
precedent `dossier_ref` set in this same dataclass and `mission_plan` followed,
and it is what both feature files already asked for; the pointer was the only
thing missing.

`Mission.order` is ruled by DECISION F260 D1 directly — "text, or file path +
sha256" — and lands as a small frozen `MissionOrder` record carrying all three,
because they answer different questions: the text is what Remedy acted on, the
path and digest are what a later reader checks the file against. The digest
spelling follows `JobPlan.job_file_sha256`, which the vocabulary page's Order row
already names as the same concept under another name.

ALTERNATIVES CONSIDERED. Rule a contract shape here on F272's own authority —
rejected: D9 already rules it and gives it to F269, so a second ruling would be
two decisions over one concept, the exact defect this feature exists to remove.
Leave the field out until F269 — rejected: both feature files name it as part of
THIS task, and adding it later would change the record shape twice for one
concept. Edit the two feature-file sentences to name the document — rejected for
`T2_F260.md`, whose sections are kept UNEDITED on purpose so this feature can
copy from them; this decision is the pointer instead, in the file a reader of
F272 already opens.

CONSEQUENCE. No production line differs from what the reference already implied;
what changes is that the next reader finds the shape instead of concluding it
does not exist. No id is spent — nothing wrong reached disk, so the handback's
mis-resolution is a `.agent/prose_slips.md` line under amend0827 rule 2.

REVERSE by deleting this section, at which point "D9 shape" is once again a
reference resolving to nothing in either feature file.
<<<END DECISIONR15>>>

<<<BEGIN TESTSR15>>>


class TestTheMissionCarriesItsOrderAndItsContract:
    """F272 T002 — the last two Mission fields DECISION F260 D1 names.

    Both are ADDITIVE and OPTIONAL, exactly as ``mission_plan`` already is: the
    key is written only when there is a value, so every record written before
    this round stays byte-identical and every reader that predates it keeps
    working.  That is why ``MISSION_SCHEMA_VERSION`` does not move for them.
    """

    def test_a_mission_that_has_neither_writes_neither_key(self, tmp_path):
        """The additive property, stated as the absence it actually is."""
        mission = create_mission("proj", "ship the thing", root=tmp_path)

        body = mission.to_json()

        assert "order" not in body
        assert "contract" not in body

    def test_a_record_written_before_this_round_re_exports_byte_identically(self):
        """A pre-F272 record must survive a load/save cycle unchanged."""
        legacy = {
            "schema_version": MISSION_SCHEMA_VERSION,
            "id": "abc",
            "project_id": "proj",
            "goal": "an older goal",
            "status": MISSION_STATUS_ACTIVE,
            "job_links": [],
            "dossier_ref": "",
            "created_at": "2026-01-01T00:00:00+00:00",
        }

        loaded = Mission.from_json(legacy)

        assert loaded.order is None
        assert loaded.contract is None
        assert loaded.to_json() == legacy

    def test_the_order_round_trips_through_disk(self, tmp_path):
        mission = create_mission("proj", "ship the thing", root=tmp_path)
        order = MissionOrder(text="build a cli",
                             source_path="orders/cli.md",
                             source_sha256="deadbeef")

        set_mission_order("proj", mission.id, order, root=tmp_path)

        assert load_mission("proj", mission.id, root=tmp_path).order == order

    def test_the_contract_round_trips_through_disk(self, tmp_path):
        """RESERVED for F269 per DECISION amend0905-vocab D9; empty until then."""
        mission = create_mission("proj", "ship the thing", root=tmp_path)

        set_mission_contract("proj", mission.id, {"criteria": ["tests pass"]},
                             root=tmp_path)

        loaded = load_mission("proj", mission.id, root=tmp_path)
        assert loaded.contract == {"criteria": ["tests pass"]}

    def test_writing_an_order_leaves_the_immutable_goal_alone(self, tmp_path):
        mission = create_mission("proj", "ship the thing", root=tmp_path)

        updated = set_mission_order("proj", mission.id,
                                    MissionOrder(text="ship the thing"),
                                    root=tmp_path)

        assert updated.goal == "ship the thing"
        assert updated.schema_version == MISSION_SCHEMA_VERSION

    def test_a_body_that_is_not_an_object_is_refused_on_both_fields(self):
        base = {
            "schema_version": MISSION_SCHEMA_VERSION,
            "id": "abc",
            "project_id": "proj",
            "goal": "g",
            "status": MISSION_STATUS_ACTIVE,
            "job_links": [],
            "dossier_ref": "",
            "created_at": "",
        }

        with pytest.raises(ValueError):
            Mission.from_json(dict(base, order="just a string"))
        with pytest.raises(ValueError):
            Mission.from_json(dict(base, contract=["not", "an", "object"]))
<<<END TESTSR15>>>
