## What

F291 — Self-use sources v2. At every feature's close, Remedy runs one small maintenance job on its
own code, and the generator that picks that job read "queue exhausted" at nine of the last thirteen
closes. It now has two more sources, tried after the four it had:

- T001, Tier 4 — an excused blind exception handler. The generator reads the same roots and the same
  mark pattern `tests/test_ble001_ratchet.py` counts, and offers the first `except Exception`
  handler carrying a BLE001 excuse mark, in file order, that no queue entry has named. The job
  narrows the handler, deletes the mark and lowers `MAX_EXCUSED` by one in the same change. An
  item's key is the file, the ordinal of the line's text and the line itself, so a mark that only
  moves is never offered twice. The generator's own source never spells the mark.
- T002, Tier 5 — a test-less module. The first module under `packages/` or `apps/cli/` that no
  `import` statement under `tests/` binds, with the functions and classes to test named in the job
  (the public ones, or every one when none is public, since all fifteen such modules define only
  private names).
- T003 — three requests on a queue dry for tiers 0 to 3 give three different items, and the first
  runs to the approval gate within the default budget: proved by tests, and live at this close.

The closure's own self-use item, `SU-037`, was the first Tier 4 item on the real tree. It ran on
`claude-cli` with Sonnet for builder and reviewer in two calls ($0.66), narrowed the handler around
`load_project_constitution` in `apps/cli/commands/brain.py` to `OSError`, lowered `MAX_EXCUSED` to
289, and is landed here with two reviewer tests (DECISION F291 D3).

## Why

`docs/roadmap/features/T5_F291.md`: the operator's second priority is that Remedy is used on itself
continuously, and a self-use track whose queue is usually empty meets that only on paper.

## Key decisions (in `.agent/decisions.md`)

- F291 D1 — the two tiers, their order after Tier 3, "oldest" read as first in file order, the
  content key, the fallback to private names, and raising on an unreadable file.
- F291 D2 — T003's run half as a runner test under the default budget; both tiers documented in
  `docs/system/self-use-track-v1.md` and closure precondition 6.
- F291 D3 — `SU-037` landed as its job's own diff with two tests.
- F291 D4 — a file under `tests/` that vanishes mid-read is skipped by Tier 5 and by the
  parametrize-id guard (R-1114, the closure suite's one red node, repaired in round 4).

The README's Tier 5 total now reads 37: F291's registration raised the overall total to 291 but left
the Tier 5 cell at 36.

## How to review / test

- `python3 -m pytest -q tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/test_brain_viewer.py tests/test_parametrize_ids_stable.py tests/test_ble001_ratchet.py`
- The one full suite: `.agent/authored/f291-closure-suite.txt` (`20976 passed, 20 skipped`, exit 0).
- Evidence job `f291r5e1001`; package `remedy-review-20260929-230028-READY_FOR_REVIEW.zip`, SHA-256
  `445966ec71a0b64f30be65c8082e7819f43a060bfdb80a8505ca9aa0dc62ca33`, accepted head `5f4cebf3`.
- Round-by-round review record: `.agent/live_review.md` and its archive.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
