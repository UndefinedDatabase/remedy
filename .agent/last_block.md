# STEP R2/F258 — T001 PART 1: THE QUEUE SCHEMA MOVES TO V2 (THE PROVENANCE FIELD)

Goal: bump the self-use queue schema to v2, adding a required `provenance`
field naming each item's source, migrate the four shipped items to carry one,
and keep both existing test files and the two docs that describe the format
in step — all in this one round, so the shipped file and its loader never
disagree at any commit. The generator itself (the source-priority search that
WRITES a generated item) is the NEXT round, not this one.

Base: `d3913f60`, round 1's handback commit and the tip of
`feature/f258-self-use-v2`. Stay on that branch. Open no pull request.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f258-r2.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN2
- C2  append slice RECORD2 to `.agent/live_review.md`
- C3  apply the six PAIR-Q* pairs to `packages/orchestration/self_use_queue.py`
- C4  apply the PAIR-TQ* pairs to `tests/orchestration/test_self_use_queue.py`
- C5  apply the three PAIR-TJ* pairs to `tests/orchestration/test_self_use_job.py`
- C6  apply the six PAIR-JSON* pairs to `scripts/self_use_queue.json`
- C7  apply the three PAIR-DOC* pairs to `docs/system/self-use-track-v1.md`
- C8  apply pair PAIR-F257AMEND to `docs/roadmap/features/T5_F257.md`
- C9  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f258-r2.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/self_use_queue.py
    tests/orchestration/test_self_use_queue.py
    tests/orchestration/test_self_use_job.py
    scripts/self_use_queue.json
    docs/system/self-use-track-v1.md
    docs/roadmap/features/T5_F257.md
    .agent/handoff.md

`.agent/context.md` is NOT touched this round — nothing in it (Active Branch,
Scope, Do-not-touch, Assumptions, Constraints) changed by this round's work;
both of its Assumptions from round 1 are still exactly true after this round.
No file under `apps/` changes. No NEW module is created this round —
`packages/orchestration/self_use_generator.py` is the next round's work.

## Constraints

1. Apply every slice and every pair BYTE FOR BYTE. Do not fix, rewrap, retitle
   or improve one. If something looks wrong, apply it as given and DECLARE the
   problem in the handback's deviations.
2. C0a is a COPY, never a retype: the block is at
   `.remedy-wt/f258-r2-block.md`. Use `shutil.copyfile` for C0a and again for
   C0b. Its sha256 is stated in gate G1; verify BEFORE saving.
3. C1 is the FIRST substantive commit, ahead of C2, per AGENTS.md's Commit Gate.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD2 and revises
   NOTHING already there.
5. Every PAIR below is applied with the SAME method: read the file as text,
   assert `text.count(FROM) == 1` (refuse and declare a deviation if it is not
   exactly 1 — never apply a pair that is not uniquely anchored), then
   `text.replace(FROM, TO, 1)`, then write the file back. Do this in a small
   script under `.remedy-wt/`, one script per target file is fine, and report
   each pair's before/after occurrence counts in the handback.
6. `.agent/plan.md` stays under 50 lines.
7. Every exit code you report is REAL, from `subprocess.run(...).returncode` in
   a script under the gitignored `.remedy-wt/`, never through a pipe.
8. The mutation red-proof (G5) runs ONLY inside a disposable `git worktree`,
   never in the primary checkout: purge every `__pycache__` under
   `packages/orchestration/` and `tests/orchestration/` inside that worktree
   and run with `python3 -B`. The primary checkout is `git status --porcelain`
   empty at every reading.
9. `packages/orchestration/self_use_queue.py` is an EXISTING module already
   swept by repo-wide guards (the `REMEDY_DATA_DIR` single-reader invariant,
   the path-utils single-implementation invariant, the bare-`except: pass`
   ban, the development-artifact boundary) — none of this round's six pairs
   introduces a new import, a new path reference, or a new exception handler,
   so no new guard surface is created, but confirm this by reading the diff
   yourself before committing rather than assuming it from this sentence.
10. `scripts/self_use_queue.json` must be valid JSON after C6 — parse it with
    `json.loads` immediately after writing and before committing; if it does
    not parse, STOP and declare rather than committing broken JSON.
11. The `remedy` console script is DENIED in this sandbox; use
    `python3 -m apps.cli.grouped ...` if needed and say so.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
13. Push after C9. No pull request, no merge, no force-push.
14. NO NEW R-ID IS MINTED THIS ROUND. Exactly one new `^DECISION F258 D\d+ — `
    id is minted: `D1`. `R-0570` stays OPEN.

## Slices

The authored units are PLAN2 and RECORD2, each between its own BEGIN/END
marker line. The markers are NOT part of the unit; the unit starts on the line
after BEGIN and ends with the newline before END.

<<<BEGIN PLAN2
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, round 2.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 closure candidate | done | round 1 |
| the F258 claim and the seam inventory | done | round 1 |
| T001 part 1 — schema v2, the provenance field | done | this round |
| T001 part 2 — the generator module | open | next round |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round bumps the self-use queue schema to v2 (DECISION F258 D1): a
   required `provenance` field joins the five existing keys, the shipped
   queue's four items are migrated in the same commit range, and both test
   files plus the two describing docs are kept in step.
2. The round after it builds `packages/orchestration/self_use_generator.py`,
   the source-priority search itself, using round 1's inventory finding that
   no code caller of `plan_next_self_use_item` exists today.
3. T002 depends on T001 producing a real item to run against; T003 wires
   existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- The version check stays an EXACT match, not a range (DECISION F258 D1): a
  v1-shaped file is refused after this round, by design, symmetric with the
  existing "a file from the future is refused" rule.
<<<END PLAN2

<<<BEGIN RECORD2
DECISION F258 D1 — THE QUEUE SCHEMA MOVES TO V2 BY EXACT-MATCH BREAK, ADDING A REQUIRED `provenance` FIELD; THE GENERATOR ITSELF IS THE NEXT ROUND, NOT THIS ONE. THE PROBLEM: F258's T001 needs a `provenance` field naming each item's source, but round 1's inventory measured that `_ITEM_KEYS` at `packages/orchestration/self_use_queue.py:69` validates an item's key set for EQUALITY against a fixed five-tuple, refusing anything else, and `load_self_use_queue`'s version check at `packages/orchestration/self_use_queue.py:134-136` is an EXACT match against `SELF_USE_QUEUE_SCHEMA_VERSION`, not a range — so a sixth key on any item is refused today regardless of `schema_version`. CHOSEN: bump `SELF_USE_QUEUE_SCHEMA_VERSION` 1 to 2; extend `_ITEM_KEYS` to six, adding `provenance`; require it as a non-blank string alongside `id`/`title`/`why`/`job_markdown` in the same validation loop; migrate all four shipped items (SU-001 through SU-004) to carry one in the SAME commit range that ships the code, so the shipped file and its loader never disagree at any commit. This is a HARD break, not a soft extension: a v1-shaped file (schema_version 1, five keys) is REFUSED after this round, exactly as `load_self_use_queue`'s own docstring already promises for "a file from the future" — here it is a file from the PAST that is refused, symmetric with that same exact-match discipline. `provenance` for the four existing items reads "operator-curated (F257, 2026-08-29)" for SU-001 (consumed, curated at F257's own session) and "operator-curated (amend0829-selfuse-v2, 2026-08-29)" for SU-002 through SU-004 (curated at the amend0829-selfuse-v2 session, already named in the file's own description), both dated, both naming the actual curating session rather than a placeholder. ALTERNATIVES CONSIDERED: (a) make `provenance` OPTIONAL, defaulting to `""` when absent, so `SELF_USE_QUEUE_SCHEMA_VERSION` would not need to move — rejected, because an optional field a human-curated item is free to skip is exactly the shape that lets a FUTURE generated item's provenance go missing silently too, and this module's own "deliberate absences" convention already treats a required field's absence as a raise, never a default; (b) accept BOTH schema_version 1 and 2 during a transition window — rejected as unnecessary complexity for a shipped file this feature branch itself controls and migrates atomically, with no external consumer of the v1 shape to support; (c) build the generator module in the SAME round as the schema bump — rejected on round-size grounds (AGENTS.md small-commits discipline): the schema change and its four-file ripple (the module, both test files, the shipped JSON) is a complete, independently reviewable unit on its own, and the generator's own source-priority logic deserves a round where it is the only new decision under review. HOW TO REVERSE: revert `SELF_USE_QUEUE_SCHEMA_VERSION` to 1, drop `provenance` from `_ITEM_KEYS` and the required-fields loop, drop the field from `SelfUseQueueEntry`, and revert the four migrated items and the two test files to their pre-round shape — independent, mechanical reversions, none of which touches any OTHER feature's code, since `self_use_job.py` constructs no `SelfUseQueueEntry` itself and needs no change either way. WHAT IT COSTS TO BE WRONG HERE: if `provenance`'s chosen wording convention turns out not to fit what the round-3 generator needs to write, only the STRING CONTENT changes — the field, the schema version and every validation rule stay exactly as this round ships them.
<<<END RECORD2

## PAIR-Q* — `packages/orchestration/self_use_queue.py` (six pairs)

Apply all six. Each FROM occurs exactly once in the file before C3; verify
that yourself and report it.

<<<BEGIN PAIRQ1-FROM
SELF_USE_QUEUE_SCHEMA_VERSION = 1
<<<END PAIRQ1-FROM
<<<BEGIN PAIRQ1-TO
SELF_USE_QUEUE_SCHEMA_VERSION = 2
<<<END PAIRQ1-TO

<<<BEGIN PAIRQ2-FROM
#: The five keys an item carries — no more, no fewer.  An unexpected key is a
#: curation mistake or a format drift, and either way it is refused.
_ITEM_KEYS: tuple[str, ...] = ("id", "title", "why", "job_markdown", "consumed_by")
<<<END PAIRQ2-FROM
<<<BEGIN PAIRQ2-TO
#: The six keys an item carries — no more, no fewer.  An unexpected key is a
#: curation mistake or a format drift, and either way it is refused.  Schema v2
#: (F258) added ``provenance``; every v1 item was migrated to carry one.
_ITEM_KEYS: tuple[str, ...] = ("id", "title", "why", "job_markdown", "consumed_by", "provenance")
<<<END PAIRQ2-TO

<<<BEGIN PAIRQ3-FROM
            object or whose keys are not exactly the five this module names,
<<<END PAIRQ3-FROM
<<<BEGIN PAIRQ3-TO
            object or whose keys are not exactly the six this module names,
<<<END PAIRQ3-TO

<<<BEGIN PAIRQ4-FROM
    id: str
    title: str
    why: str
    job_markdown: str
    consumed_by: str

    @property
<<<END PAIRQ4-FROM
<<<BEGIN PAIRQ4-TO
    id: str
    title: str
    why: str
    job_markdown: str
    consumed_by: str
    provenance: str

    @property
<<<END PAIRQ4-TO

<<<BEGIN PAIRQ5-FROM
        for field_name in ("id", "title", "why", "job_markdown"):
<<<END PAIRQ5-FROM
<<<BEGIN PAIRQ5-TO
        for field_name in ("id", "title", "why", "job_markdown", "provenance"):
<<<END PAIRQ5-TO

<<<BEGIN PAIRQ6-FROM
        entries.append(SelfUseQueueEntry(
            id=item_id,
            title=raw["title"],
            why=raw["why"],
            job_markdown=raw["job_markdown"],
            consumed_by=consumed_by,
        ))
<<<END PAIRQ6-FROM
<<<BEGIN PAIRQ6-TO
        entries.append(SelfUseQueueEntry(
            id=item_id,
            title=raw["title"],
            why=raw["why"],
            job_markdown=raw["job_markdown"],
            consumed_by=consumed_by,
            provenance=raw["provenance"],
        ))
<<<END PAIRQ6-TO

## PAIR-TQ* — `tests/orchestration/test_self_use_queue.py`

<<<BEGIN PAIRTQ1-FROM
_ONE_ITEM = {
    "id": "SU-001",
    "title": "A curated item",
    "why": "Because a reader would look here and find nothing.",
    "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
    "consumed_by": "",
}
<<<END PAIRTQ1-FROM
<<<BEGIN PAIRTQ1-TO
_ONE_ITEM = {
    "id": "SU-001",
    "title": "A curated item",
    "why": "Because a reader would look here and find nothing.",
    "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
    "consumed_by": "",
    "provenance": "operator-curated (fixture)",
}
<<<END PAIRTQ1-TO

<<<BEGIN PAIRTQ2-FROM
def _queue_body(items: list[dict], schema_version: int = 1) -> dict:
<<<END PAIRTQ2-FROM
<<<BEGIN PAIRTQ2-TO
def _queue_body(items: list[dict], schema_version: int = 2) -> dict:
<<<END PAIRTQ2-TO

<<<BEGIN PAIRTQ3-FROM
    def test_shipped_ids_are_unique_and_match_the_pattern(self):
        import re

        ids = [entry.id for entry in load_self_use_queue()]
        assert len(set(ids)) == len(ids), f"duplicate ids: {sorted(ids)}"
        for item_id in ids:
            assert re.match(r"^SU-\d{3}$", item_id), item_id


class TestShippedQueueParsesAsJobs:
<<<END PAIRTQ3-FROM
<<<BEGIN PAIRTQ3-TO
    def test_shipped_ids_are_unique_and_match_the_pattern(self):
        import re

        ids = [entry.id for entry in load_self_use_queue()]
        assert len(set(ids)) == len(ids), f"duplicate ids: {sorted(ids)}"
        for item_id in ids:
            assert re.match(r"^SU-\d{3}$", item_id), item_id

    def test_every_shipped_item_carries_a_non_blank_provenance(self):
        for entry in load_self_use_queue():
            assert entry.provenance.strip(), f"{entry.id}: blank provenance"


class TestEntryCarriesProvenance:
    """The loaded entry's provenance is the JSON value, verbatim."""

    def test_provenance_round_trips_from_the_file(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(provenance="a generator run")]))
        entry = next_self_use_item(path)
        assert entry is not None
        assert entry.provenance == "a generator run"


class TestShippedQueueParsesAsJobs:
<<<END PAIRTQ3-TO

<<<BEGIN PAIRTQ4-FROM
    def test_shipped_queue_declares_schema_version_one(self):
        body = json.loads(default_self_use_queue_path().read_text(encoding="utf-8"))
        assert body["schema_version"] == SELF_USE_QUEUE_SCHEMA_VERSION == 1
<<<END PAIRTQ4-FROM
<<<BEGIN PAIRTQ4-TO
    def test_shipped_queue_declares_schema_version_two(self):
        body = json.loads(default_self_use_queue_path().read_text(encoding="utf-8"))
        assert body["schema_version"] == SELF_USE_QUEUE_SCHEMA_VERSION == 2
<<<END PAIRTQ4-TO

<<<BEGIN PAIRTQ5-FROM
    def test_wrong_schema_version_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item()], schema_version=2))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)
<<<END PAIRTQ5-FROM
<<<BEGIN PAIRTQ5-TO
    def test_wrong_schema_version_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item()], schema_version=3))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_old_v1_shaped_file_is_refused(self, tmp_path: Path):
        v1_item = _item()
        del v1_item["provenance"]
        path = _write_queue(tmp_path, {
            "schema_version": 1,
            "description": "fixture queue",
            "items": [v1_item],
        })
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)
<<<END PAIRTQ5-TO

<<<BEGIN PAIRTQ6-FROM
    def test_id_not_matching_the_pattern_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(id="SU-1")]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_empty_queue_is_not_an_error(self, tmp_path: Path):
<<<END PAIRTQ6-FROM
<<<BEGIN PAIRTQ6-TO
    def test_id_not_matching_the_pattern_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(id="SU-1")]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_missing_provenance_raises(self, tmp_path: Path):
        broken = _item()
        del broken["provenance"]
        path = _write_queue(tmp_path, _queue_body([broken]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_blank_provenance_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(provenance="   ")]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_empty_queue_is_not_an_error(self, tmp_path: Path):
<<<END PAIRTQ6-TO

## PAIR-TJ* — `tests/orchestration/test_self_use_job.py`

<<<BEGIN PAIRTJ1-FROM
def _entry(**overrides) -> SelfUseQueueEntry:
    fields = {
        "id": "SU-042",
        "title": "A curated item",
        "why": "Because the track must run on something.",
        "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
        "consumed_by": "",
    }
    fields.update(overrides)
    return SelfUseQueueEntry(**fields)
<<<END PAIRTJ1-FROM
<<<BEGIN PAIRTJ1-TO
def _entry(**overrides) -> SelfUseQueueEntry:
    fields = {
        "id": "SU-042",
        "title": "A curated item",
        "why": "Because the track must run on something.",
        "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
        "consumed_by": "",
        "provenance": "operator-curated (fixture)",
    }
    fields.update(overrides)
    return SelfUseQueueEntry(**fields)
<<<END PAIRTJ1-TO

<<<BEGIN PAIRTJ2-FROM
def _write_queue(tmp_path: Path, items: list[dict]) -> Path:
    path = tmp_path / "self_use_queue.json"
    body = {
        "schema_version": 1,
        "description": "fixture queue",
        "items": items,
    }
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path
<<<END PAIRTJ2-FROM
<<<BEGIN PAIRTJ2-TO
def _write_queue(tmp_path: Path, items: list[dict]) -> Path:
    path = tmp_path / "self_use_queue.json"
    body = {
        "schema_version": 2,
        "description": "fixture queue",
        "items": items,
    }
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path
<<<END PAIRTJ2-TO

<<<BEGIN PAIRTJ3-FROM
        consumed = dict(
            id="SU-001",
            title="Already done",
            why="Every item here carries a consumer.",
            job_markdown="# Job: Demo\n\n## Task 1\nDo it.\n\nAcceptance:\n- done\n",
            consumed_by="F256",
        )
<<<END PAIRTJ3-FROM
<<<BEGIN PAIRTJ3-TO
        consumed = dict(
            id="SU-001",
            title="Already done",
            why="Every item here carries a consumer.",
            job_markdown="# Job: Demo\n\n## Task 1\nDo it.\n\nAcceptance:\n- done\n",
            consumed_by="F256",
            provenance="operator-curated (fixture)",
        )
<<<END PAIRTJ3-TO

## PAIR-JSON* — `scripts/self_use_queue.json` (six pairs, applied in this order)

<<<BEGIN PAIRJSON1-FROM
  "schema_version": 1,
<<<END PAIRJSON1-FROM
<<<BEGIN PAIRJSON1-TO
  "schema_version": 2,
<<<END PAIRJSON1-TO

<<<BEGIN PAIRJSON2-FROM
  "description": "F257 — the self-use queue Remedy runs against its own repository. Operator-curated DATA, not discovery: Remedy never invents an item and never appends one. Exactly one item is consumed per feature close, and an item is marked consumed by the closure round and NEVER by a job, because a run that can check itself off is not a gate. Mark an item consumed by setting its consumed_by to the feature id that consumed it; the loader packages/orchestration/self_use_queue.py reads this file and ships no writer. Dated note, 2026-08-29 (amend0829-selfuse-v2): items SU-002, SU-003 and SU-004 were curated in this session on operator authority — grepping the reviewer ledger for open self-contained Medium findings (SU-003, SU-004) and grepping docs/ for a page contradicting shipped code (SU-002) — exactly the research the future F258 generator will automate.",
<<<END PAIRJSON2-FROM
<<<BEGIN PAIRJSON2-TO
  "description": "F257 — the self-use queue Remedy runs against its own repository. Operator-curated DATA, not discovery: Remedy never invents an item and never appends one. Exactly one item is consumed per feature close, and an item is marked consumed by the closure round and NEVER by a job, because a run that can check itself off is not a gate. Mark an item consumed by setting its consumed_by to the feature id that consumed it; the loader packages/orchestration/self_use_queue.py reads this file and ships no writer. Dated note, 2026-08-29 (amend0829-selfuse-v2): items SU-002, SU-003 and SU-004 were curated in this session on operator authority — grepping the reviewer ledger for open self-contained Medium findings (SU-003, SU-004) and grepping docs/ for a page contradicting shipped code (SU-002) — exactly the research the future F258 generator will automate. Dated note, 2026-08-30 (F258 round 2): schema_version moved to 2, adding a required provenance field naming each item's source; every existing item below was migrated to carry one, each 'operator-curated' since none was yet generated by code.",
<<<END PAIRJSON2-TO

<<<BEGIN PAIRJSON3-FROM
      "consumed_by": "F257"
    },
<<<END PAIRJSON3-FROM
<<<BEGIN PAIRJSON3-TO
      "consumed_by": "F257",
      "provenance": "operator-curated (F257, 2026-08-29)"
    },
<<<END PAIRJSON3-TO

<<<BEGIN PAIRJSON4-FROM
- `python3 -m pytest tests/docs/ -q` stays green.\n",
      "consumed_by": ""
    },
<<<END PAIRJSON4-FROM
<<<BEGIN PAIRJSON4-TO
- `python3 -m pytest tests/docs/ -q` stays green.\n",
      "consumed_by": "",
      "provenance": "operator-curated (amend0829-selfuse-v2, 2026-08-29)"
    },
<<<END PAIRJSON4-TO

<<<BEGIN PAIRJSON5-FROM
- `npm run typecheck` and `npx vitest run` in `apps/ui` both still exit 0 (this job changes lint tooling only, not source).\n",
      "consumed_by": ""
    },
<<<END PAIRJSON5-FROM
<<<BEGIN PAIRJSON5-TO
- `npm run typecheck` and `npx vitest run` in `apps/ui` both still exit 0 (this job changes lint tooling only, not source).\n",
      "consumed_by": "",
      "provenance": "operator-curated (amend0829-selfuse-v2, 2026-08-29)"
    },
<<<END PAIRJSON5-TO

<<<BEGIN PAIRJSON6-FROM
- Existing failure-classification tests stay green.\n",
      "consumed_by": ""
    }
  ]
}
<<<END PAIRJSON6-FROM
<<<BEGIN PAIRJSON6-TO
- Existing failure-classification tests stay green.\n",
      "consumed_by": "",
      "provenance": "operator-curated (amend0829-selfuse-v2, 2026-08-29)"
    }
  ]
}
<<<END PAIRJSON6-TO

## PAIR-DOC* — `docs/system/self-use-track-v1.md` (three pairs)

<<<BEGIN PAIRDOC1-FROM
> **Status (2026-08-29):** built by F257. The queue, its loader, the job-path
> seam and the closure-protocol precondition are in place; consumption happens
> at feature close.
<<<END PAIRDOC1-FROM
<<<BEGIN PAIRDOC1-TO
> **Status (2026-08-29):** built by F257. The queue, its loader, the job-path
> seam and the closure-protocol precondition are in place; consumption happens
> at feature close. **Update (2026-08-30, F258 round 2):** the queue's schema
> moved to v2, adding a required `provenance` field naming each item's source;
> every shipped item was migrated. F258's self-replenishing generator is not
> yet built — this page still describes v1's discovery-free behaviour, which
> remains true until that round ships.
<<<END PAIRDOC1-TO

<<<BEGIN PAIRDOC2-FROM
    {
      "schema_version": 1,
      "description": "<what this queue is for>",
      "items": [
        {
          "id": "SU-001",
          "title": "<one line>",
          "why": "<why this job is worth a feature close>",
          "job_markdown": "# Job: ...\n\n## Task 1\n...\n\nAcceptance:\n- ...\n",
          "consumed_by": ""
        }
      ]
    }
<<<END PAIRDOC2-FROM
<<<BEGIN PAIRDOC2-TO
    {
      "schema_version": 2,
      "description": "<what this queue is for>",
      "items": [
        {
          "id": "SU-001",
          "title": "<one line>",
          "why": "<why this job is worth a feature close>",
          "job_markdown": "# Job: ...\n\n## Task 1\n...\n\nAcceptance:\n- ...\n",
          "consumed_by": "",
          "provenance": "<what found this item — a human curator, or a generator source>"
        }
      ]
    }
<<<END PAIRDOC2-TO

<<<BEGIN PAIRDOC3-FROM
| Rule | Detail |
|------|--------|
| `schema_version` | must equal 1; a file from the future is refused, not half-read |
| item keys | exactly the five above — no more, no fewer |
| `id` | must match `^SU-\d{3}$`, and must be unique across the file |
| `title`, `why`, `job_markdown` | non-empty strings |
| `consumed_by` | a string; empty means the item is still PENDING |
<<<END PAIRDOC3-FROM
<<<BEGIN PAIRDOC3-TO
| Rule | Detail |
|------|--------|
| `schema_version` | must equal 2 (v1 files, without `provenance`, are refused, not half-read) |
| item keys | exactly the six above — no more, no fewer |
| `id` | must match `^SU-\d{3}$`, and must be unique across the file |
| `title`, `why`, `job_markdown`, `provenance` | non-empty strings |
| `consumed_by` | a string; empty means the item is still PENDING |
<<<END PAIRDOC3-TO

## PAIR-F257AMEND — `docs/roadmap/features/T5_F257.md`

<<<BEGIN PAIRF257-FROM
registered in `.agent/live_review.md` as `R-0733`, `R-0734`, `R-0735` and
`R-0736`, of which `R-0734` and `R-0736` are deliberately left for branches of
their own.

**The integration gate.** Full suite at `2bb2db2c`: `18186 passed, 20 skipped`,
<<<END PAIRF257-FROM
<<<BEGIN PAIRF257-TO
registered in `.agent/live_review.md` as `R-0733`, `R-0734`, `R-0735` and
`R-0736`, of which `R-0734` and `R-0736` are deliberately left for branches of
their own.

**Amendment (2026-08-30, F258 round 2).** The queue's schema moved to v2: a
required `provenance` field was added naming each item's source, and every
item this feature shipped (`SU-001`) was migrated to carry one. This is a
data-shape extension only — F258's own self-replenishing generator, which will
be the first thing to populate `provenance` with something other than a human
curator's name, has not been built yet; this feature's "operator-curated DATA
— curation is where this feature's risk sits" property is unchanged until it
is.

**The integration gate.** Full suite at `2bb2db2c`: `18186 passed, 20 skipped`,
<<<END PAIRF257-TO

## Done when — the gates

Run each gate and report ONE line per gate in the handback with its REAL exit
code. Every gate below runs at a commit STRICTLY EARLIER than C9, which writes
the handback.

G1 TRANSPORT, at C0b. sha256 over THREE files — `.remedy-wt/f258-r2-block.md`,
   the committed `.agent/authored/f258-r2.md`, and the committed
   `.agent/last_block.md` — report the one digest and byte length, state all
   three equal.

G2 THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to PLAN2 (report both sha256),
   under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s byte length
   yourself immediately before C2 (do not trust a number from an earlier
   round). TWO readings: (a) WHOLE RECONSTRUCTION — base + `\n` + RECORD2
   equals the committed file exactly; (b) PARAGRAPH ORDER — the committed
   file's last `\n\n`-delimited unit equals RECORD2 exactly (N=1). NEGATIVE
   CONTROL inside a disposable worktree: flip one printable byte inside
   RECORD2 and show both readings reject the flip and accept the original;
   remove the worktree after.

G4 THE LEDGER, at C1 and at C2. Distinct `^- R-\d+ — ` ids and `^Done: R-\d+`
   ids, ADDED/REMOVED both empty for each. Distinct `^DECISION F258 D\d+ — `
   ids before and after: `[]` then `['D1']` — ADDED is exactly `['D1']`.
   `^Done: R-0570` stays 0.

G5 THE PRODUCTION CODE, THE TESTS AND THE DATA, at C6 (after the JSON
   migration lands, so the shipped-queue integration tests run against a
   consistent file). For EVERY PAIR in PAIR-Q*, PAIR-TQ*, PAIR-TJ* and
   PAIR-JSON* (twenty-one pairs total): report the FROM occurrence count
   immediately before its own commit (must be 1) and the TO occurrence count
   immediately after (must be 1), and confirm `scripts/self_use_queue.json`
   parses with `json.loads` after C6. Then, at C6, in the PRIMARY checkout:
   `python3 -m pytest tests/orchestration/test_self_use_queue.py
   tests/orchestration/test_self_use_job.py -q`, REAL exit code, all passing.
   The reviewer measured the base (round 1's tip, before this round's pairs)
   at 18 collected in each file, 36 combined; this round adds FIVE new tests
   to `test_self_use_queue.py` (`test_every_shipped_item_carries_a_non_blank_provenance`,
   `TestEntryCarriesProvenance::test_provenance_round_trips_from_the_file`,
   `test_old_v1_shaped_file_is_refused`, `test_missing_provenance_raises`,
   `test_blank_provenance_raises`) and renames one existing test
   (`test_shipped_queue_declares_schema_version_one` to `_two`, net zero),
   so `test_self_use_queue.py` goes to 23 and `test_self_use_job.py` stays at
   18 — 41 combined. Report YOUR collected counts for both files and confirm
   they match.
   THEN the mutation red-proof, in a disposable git worktree branched from
   C6, `__pycache__` purged, `python3 -B`: revert PAIRQ5 alone (the
   `field_name` tuple loses `"provenance"` again, so a PRESENT-but-blank
   `provenance` is no longer refused — PAIRQ2's `_ITEM_KEYS` still names the
   key, so a MISSING key is still caught by the separate key-set-equality
   check regardless of this one mutation) and re-run the same two test
   files. The reviewer verified this exact mutation directly before
   delegating: exactly ONE test goes RED,
   `test_blank_provenance_raises` (`Failed: DID NOT RAISE
   <class 'packages.orchestration.self_use_queue.SelfUseQueueError'>`);
   `test_missing_provenance_raises` and
   `test_every_shipped_item_carries_a_non_blank_provenance` stay GREEN under
   this specific mutation, for the reasons just given — they are not blind
   to every defect this round could ship, only to this ONE reverted pair.
   Report REAL exit code and the FAILED test name(s); if your own run shows a
   DIFFERENT set of failures than this one test, STOP and declare it as a
   deviation rather than silently reporting your own number as if it were
   expected — that mismatch would mean the round's code differs from what
   the reviewer verified. Then restore PAIRQ5's TO bytes and re-run once
   more: REAL exit 0, 41 passing again. Remove the worktree after;
   `git worktree list` shows the primary checkout alone.

G6 THE DOCS, at C8. For PAIR-DOC1/2/3 and PAIR-F257AMEND (four pairs): FROM/TO
   occurrence counts as in G5. Then, at C8: `python3 -m pytest tests/docs/ -q`
   and `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`
   (`docs/roadmap/features/T5_F257.md` is under `docs/roadmap/**`), each its
   own REAL exit code. The reviewer measured both green at the base, 295 and
   30 passed; report YOUR numbers.

G7 THE STATE READERS AND THE CANARY, at C9. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured these at the base at 515, 52, 21, 16 and 42 passed; report YOURS.

G8 THE TREE, at C9. `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, `git worktree list` shows the primary checkout
   alone, and the per-commit insertion counts for C0a through C8 from
   `git diff --numstat`, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
the state block, the `## Commits` table with `+/-` from `git diff --numstat`,
the deviations, the item-status table with every bundle item and every gate
appearing exactly once, and the next steps. It states `SESSION 1` of F258 and
round 2. It has NO length cap. Report every one of the twenty-five pairs by
name with its before/after occurrence count; a table is fine for this. Name
`R-0570` as OPEN and routed away, and `DECISION F258 D1` as the one id minted
this round.
