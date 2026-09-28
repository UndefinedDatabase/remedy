# Handback — F039, round 7: book round 6's PASS and R-1101's resolution, repair R-1102, land T003's data half

## Session

SESSION 1 of feature F039 · round 7 · rounds so far 7. This session ran round 7 only: booking
round 6's PASS gate and R-1101's resolution into the ledger, registering and repairing R-1102 —
the cockpit's dashboard mapping replacing every minted task id with `task-<n>`, so a finished
`remedy do` job never reached Finalized — and landing T003's data half: the story payload
builder (`packages/orchestration/story_export.py`) and its TypeScript reader
(`apps/ui/src/components/story/storyExport.ts`). Context self-assessment: a comfortable margin
remained through the round, including the full G4 pytest selection (~3 minutes, 2276 passed),
the vitest run of the touched files, and the mutation tool's one complete run over 9 mutations;
the work was not near its limit.

For the operator, in plain words: round 6 is booked PASS and R-1101 is booked resolved. A new
High finding, R-1102, was registered and repaired this round — the cockpit's dashboard used to
replace every task's real id with a synthetic `task-0`, `task-1`, ... label, so a job's own
finished tasks could never be matched against the lists that mark a job "paused", "vetoed" or
"finalized" — the phase bar and the story stalled at Review forever, even after the job
actually finished. The fix keeps a task's own id untouched (it is an identifier, not text a
person reads) while still scrubbing its visible label. Separately, the story feature's DATA
half landed: a new module builds one job's whole "story" (its task list, live state, story
pacing, every event, and who-did-what) entirely from the same builders the live cockpit already
uses, and a new TypeScript module reads that data back, refusing to guess at a story exported by
a future or past version of Remedy. R-1102 stays open, awaiting the reviewer's own review of
this fix.

## Range

Review of 622ec0451..2922e5855

## Commits

### 9fb6a0a06 F039 R7 C1a: copy round 7 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r7-block.md | +254/-0 | verbatim copy of the block |
| .agent/authored/f039-r7-plan.md | +30/-0 | verbatim copy of the plan payload |

### 3ef77bcc5 F039 R7 C1b: copy round 7 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r7-records.diff | +61/-0 | verbatim copy of the records payload |

### d5b8d9ae2 F039 R7 C2: book round 6 and R-1101, register R-1102, record D7
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +39/-0 | DECISION F039 D7 (the export is one HTML file) |
| .agent/live_review.md | +6/-0 | F039 R6 gate entry (PASS), R-1101's `Done:` line, R-1102's registration |
| .agent/plan.md | +9/-8 | rewritten to round 7's current step |

### 87890b366 F039 R7 C3: keep a task's own id in the dashboard mapping (R-1102)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Landed: R-1102 — ` line, appended per S1 |
| apps/ui/src/api/remedyApi.ts | +3/-1 | S1: the id is kept raw, never scrubbed |
| apps/ui/src/api/remedyApi.test.ts | +11/-0 | test: minted id kept, hex label still scrubbed |
| apps/ui/src/components/graph/brainView.test.ts | +39/-0 | R-1102 describe: seeds under the raw id, readPhases reads finalized |

### d45a07db7 F039 R7 C4: build a job's story payload from the cockpit's own builders
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/story_export.py | +58/-0 | NEW: S2, `build_story_payload` |
| tests/orchestration/test_story_export.py | +111/-0 | NEW: S4's Python half |

### 1f34be28c F039 R7 C4b: register story_export.py in ALLOWED_UNWIRED
| Path | +/- | Reason |
|---|---|---|
| tests/test_no_orphan_modules.py | +2/-0 | S2's own ALLOWED_UNWIRED entry, split out of C4 (declared below) |

### 95aeaccc8 F039 R7 C5: read an exported story back, refusing another schema
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyExport.test.ts | +73/-0 | NEW: S4's TypeScript half, hand-derived from the demo recording |
| apps/ui/src/components/story/storyExport.ts | +81/-0 | NEW: S3, `decodeStoryExport` |

### 116f65940 F039 R7 C4c: strengthen the dashboard-sections test with a literal expectation
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_story_export.py | +4/-0 | correction, declared below: a literal assertion so mutation m4 is caught |

### 2922e5855 F039 R7 C6: add the mutation tool for R-1102 and the story payload
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r7-mutations.py | +181/-0 | NEW: mutation tool for m1-m9 |

## External actions

- `git worktree add --detach .remedy-wt/f039-r7-mut 2922e5855` — created for G5. Outcome:
  success, `HEAD is now at 2922e5855`.
- `git worktree remove .remedy-wt/f039-r7-mut` — outcome: success (no output).
- `git worktree prune` — outcome: success (no output).
- `git push origin feature/f039-story-replay-mode` — outcome reported in the reply (per the
  block, G6's readings, including this one, go in the reply rather than this file).
- No PR created (the block forbids it this round).

## Verification

### BEFORE ANYTHING ELSE (block steps 1-4)
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f039-story-replay-mode
$ git log --oneline -1
622ec0451 F039 R6 C6: rewrite handoff for round 6
```
Block bytes (R-0954): measured line count 254 / given 254; measured sha256
`855fcf99f82da7ea92e290c47d1983a8f9bdd2f1c745fc6b1c866b114357a86b` / given the same — MATCH.
`git worktree list | wc -l` at step 4: 62.

### PAYLOADS table
| file | lines measured/given | bytes measured/given | sha256 match |
|---|---|---|---|
| plan.md | 30/30 | 1074/1074 | match |
| records.diff | 61/61 | 11701/11701 | match |

### G1 TRANSPORT
- plan.md: 30 lines, 1074 bytes, sha256 `a88fd3959b4387bf4984f6f060982c8e22e9022cf57c86d0e38c506921559667` — matches PAYLOADS table.
- records.diff: 61 lines, 11701 bytes, sha256 `ef131c1b4fd720e0622122eba37122a2793c1dbcf9de58cc625088425ee47968` — matches PAYLOADS table.
- `git show 9fb6a0a06:.agent/authored/f039-r7-block.md` == `.remedy-wt/f039-r7/block.md`: byte-identical (sha256 `855fcf99...` both sides).
- `git show 9fb6a0a06:.agent/authored/f039-r7-plan.md` == `.remedy-wt/f039-r7-payloads/plan.md`: byte-identical (sha256 `a88fd395...` both sides).
- `git show 3ef77bcc5:.agent/authored/f039-r7-records.diff` == `.remedy-wt/f039-r7-payloads/records.diff`: byte-identical (sha256 `ef131c1b...` both sides).

### G2 THE RECORDS
```
$ git apply --check .remedy-wt/f039-r7-payloads/records.diff
REAL_EXIT=0
$ git apply .remedy-wt/f039-r7-payloads/records.diff
REAL_EXIT=0
```
At C2 (`d5b8d9ae2`):
| path | bytes | sha256 | matches table |
|---|---|---|---|
| .agent/decisions.md | 2437905 | 567b16b449ad759474723ef38a0a888e99a459c5aaa5819b8385f8651ee10edb | yes |
| .agent/live_review.md | 352058 | c2098229bc892b0572ac38cac005842ab10020f811220e583fe3776a0976235f | yes |
| .agent/plan.md | 1074 | a88fd3959b4387bf4984f6f060982c8e22e9022cf57c86d0e38c506921559667 | yes |

`open_finding_ids(text)` over the ledger at C2 = `['R-1102']`; `latest_gate_verdict(text)` = `PASS` — both match the reviewer's stated readings.

`git diff --name-only 3ef77bcc5 d5b8d9ae2`:
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Exactly the table's three paths.

At C3 (`87890b366`): the ledger at C2 is confirmed a byte-exact prefix of the ledger at C3
(`c3[:len(c2)] == c2` → True), and the added bytes are exactly `"\n"` followed by one line
beginning `Landed: R-1102 — ` and ending in `"\n"` (verified: `added.startswith(b"\nLanded:
R-1102")` → True, `added.endswith(b"\n")` → True).

### G3 THE CODE
```
$ python3 -m ruff check packages/orchestration/story_export.py tests/orchestration/test_story_export.py tests/test_no_orphan_modules.py .agent/authored/f039-r7-mutations.py
All checks passed!
REAL_EXIT=0
```

The id line of S1 with its comment, quoted from the commit:
```ts
      // R-1102: the id is an IDENTIFIER every seed, focus rule and door
      // compares with a raw task id — never text a person reads, so it is never scrubbed.
      id: t.id ? String(t.id) : `task-${idx}`,
```

The whole of `story_export.py`, quoted from the commit:
```python
"""F039 T003 (DECISION F039 D7) — the story's DATA half: one job's story payload,
built from the cockpit's own builders and nothing else. Remedy deliberately
exports nothing the cockpit's own routes do not already serve: the dashboard
section, the event frames and the ownership view are each read through the
exact function the browser already calls, so a story file can never diverge
from what the live cockpit would have shown for the same job.

`build_story_payload` is the ONE function here. It imports `ownership_view`
(`packages/orchestration/ownership_phrases.py`) and `_build_dashboard`,
`_load_events` and `_safe_event_summary` (`packages/orchestration/ui_server.py`)
function-scoped, exactly as `ownership_phrases.py`'s own `ownership_view`
imports `build_ownership_ledger` function-scoped — the pattern this module
mirrors rather than reinvents.
"""
from __future__ import annotations

from typing import Any

__all__ = [
    "STORY_EXPORT_SCHEMA",
    "STORY_DASHBOARD_SECTIONS",
    "build_story_payload",
]

#: The one schema string both language halves pin: this module's writer and
#: `apps/ui/src/components/story/storyExport.ts`'s reader
#: (`tests/orchestration/test_story_export.py` guards the two stay equal).
STORY_EXPORT_SCHEMA = "remedy.story.v1"

#: The dashboard keys a story carries — the task list, the live state and the
#: story pacing section — never the whole dashboard, which holds figures (proof
#: chain paths, evidence directories) a self-contained export has no business
#: repeating.
STORY_DASHBOARD_SECTIONS = ("tasks", "live", "story")


def build_story_payload(job: Any) -> dict[str, Any]:
    """S2 — one job's story payload: `{"schema", "job_id", "dashboard", "frames",
    "ownership"}`. `dashboard` is `STORY_DASHBOARD_SECTIONS` of `_build_dashboard(job)`;
    `frames` is every event `_load_events(job)` holds, each through
    `_safe_event_summary`, with `seq` counted from 0; `ownership` is `ownership_view(job)`
    unchanged. Every part comes from the cockpit's own builders, so a story file holds
    nothing the cockpit does not already serve.
    """
    from packages.orchestration.ownership_phrases import ownership_view
    from packages.orchestration.ui_server import _build_dashboard, _load_events, _safe_event_summary

    dashboard = _build_dashboard(job)
    return {
        "schema": STORY_EXPORT_SCHEMA,
        "job_id": str(job.job_id),
        "dashboard": {key: dashboard[key] for key in STORY_DASHBOARD_SECTIONS},
        "frames": [
            {"seq": seq, "event": _safe_event_summary(seq, event)}
            for seq, event in enumerate(_load_events(job))
        ],
        "ownership": ownership_view(job),
    }
```

The whole of `decodeStoryExport`, quoted from the commit:
```ts
/** Decode one exported story payload. NEVER THROWS: every failure — a payload
 *  that is not a plain object, one naming another schema, one missing a
 *  required field, or one whose frames are malformed — answers `{ ok: false,
 *  message }` with a fixed line rather than propagating a parse error to the
 *  player. */
export function decodeStoryExport(raw: unknown): { ok: true; story: StoryExport } | { ok: false; message: string } {
  if (!isPlainObject(raw)) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  const schema = raw["schema"];
  if (typeof schema === "string" && schema !== STORY_EXPORT_SCHEMA) {
    return { ok: false, message: storyExportVersionLine(schema) };
  }
  const jobId = raw["job_id"];
  const dashboard = raw["dashboard"];
  const frames = raw["frames"];
  if (
    typeof schema !== "string"
    || typeof jobId !== "string"
    || !isPlainObject(dashboard)
    || !Array.isArray(frames)
  ) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  if (!frames.every(isFrame)) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  return {
    ok: true,
    story: {
      dashboard: normalizeDashboardPayload(jobId, dashboard),
      rows: frames.map((frame) => feedRowOf(frame, 0)),
      ownership: decodeOwnershipView(raw["ownership"]),
    },
  };
}
```

### G4 THE TESTS
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_story_export.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
2276 passed, 5 skipped in 179.44s (0:02:59)
REAL_EXIT=0
```
None of the 5 skips names `node_modules`, `dist` or `vitest` — all five are the pre-existing D3/D12
quarantine skips unrelated to a toolchain node; every toolchain-node skip the reviewer's fresh
simulation tree read (it read `2267 passed, 10 skipped`) PASSES here in the primary checkout, as
the block requires. `tests/orchestration/test_story_export.py` node count: 7 tests (collected via
`--collect-only`).
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=168"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "fail", "message": "1 open blocker/high: R-1102"}
], "fail_count": 1, "ok": false, "passed": false}
REAL_EXIT=1
```
Five checks pass, `high_blockers_open` fails with exactly `1 open blocker/high: R-1102` at
`fail_count` 1 — as expected, since R-1102 stays open until the reviewer resolves it.

### G5 THE RED PROOFS
```
$ git worktree add --detach .remedy-wt/f039-r7-mut 2922e5855
Preparing worktree (detached HEAD 2922e5855)
HEAD is now at 2922e5855 F039 R7 C6: add the mutation tool for R-1102 and the story payload
REAL_EXIT=0

$ python3 -B .agent/authored/f039-r7-mutations.py .remedy-wt/f039-r7-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r7-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=145 | guard exit=0 failed=0 passed=7
m1 (the task's id goes through scrubUiText again): vitest exit=1 failed=4 passed=141 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m2 (the frames' seqs are counted from 1): vitest exit=0 failed=0 passed=145 | guard exit=1 failed=1 passed=6 | caught=True restored byte-identical=True
m3 (each frame carries the raw event instead of _safe_event_summary's envelope): vitest exit=0 failed=0 passed=145 | guard exit=1 failed=2 passed=5 | caught=True restored byte-identical=True
m4 (STORY_DASHBOARD_SECTIONS gains metrics): vitest exit=0 failed=0 passed=145 | guard exit=1 failed=1 passed=6 | caught=True restored byte-identical=True
m5 (decodeStoryExport no longer refuses another schema by name): vitest exit=1 failed=1 passed=144 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m6 (a frame is taken as a row without feedRowOf): vitest exit=1 failed=1 passed=144 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m7 (the ownership view is taken without decodeOwnershipView): vitest exit=1 failed=2 passed=143 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m8 (the TypeScript constant reads remedy.story.v2): vitest exit=1 failed=1 passed=144 | guard exit=1 failed=1 passed=6 | caught=True restored byte-identical=True
m9 (a frame with no number seq is accepted): vitest exit=1 failed=1 passed=144 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=145 | guard exit=0 failed=0 passed=7
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ git worktree remove .remedy-wt/f039-r7-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
$ git worktree list | wc -l
62
$ git status --porcelain
(empty)
```
All 9 mutations caught (every one red in at least one runner), all restored byte-identical, no
skip.

## Authored-text proofs

| payload | committed at | disk-to-disk vs source | result |
|---|---|---|---|
| block.md copy | 9fb6a0a06 | `.agent/authored/f039-r7-block.md` vs `.remedy-wt/f039-r7/block.md` | byte-identical |
| plan.md copy | 9fb6a0a06 | `.agent/authored/f039-r7-plan.md` vs `.remedy-wt/f039-r7-payloads/plan.md` | byte-identical |
| records.diff copy | 3ef77bcc5 | `.agent/authored/f039-r7-records.diff` vs `.remedy-wt/f039-r7-payloads/records.diff` | byte-identical |
| records.diff application | d5b8d9ae2 | `git apply` of the reviewer's diff, C2's three files' sha256 vs the G2 table | all three match |

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | split into C4/C4b/C4c, declared below |
| C4b | done | added to cover an omission from C4 (S2's ALLOWED_UNWIRED entry) |
| C4c | done | test correction declared below (constraint 4) |
| C5 | done | |
| C6 | done | |
| C7 | done | this handback |
| G1 transport | done | |
| G2 records | done | |
| G3 code (ruff) | done | |
| G4 tests | done | |
| G5 red proofs | done | all 9 mutations caught |
| G6 tree and push | done | reported in the reply |

## Deviations & assumptions

1. **C4 was split into C4 / C4b / C4c, none of them under the 500-line cap.** C4b
   (`1f34be28c`) registers `story_export.py` in `tests/test_no_orphan_modules.py`'s
   `ALLOWED_UNWIRED`, which S2 itself specifies ("`ALLOWED_UNWIRED` gains..."). It was
   omitted from the original C4 commit by oversight; rather than amend a commit already made
   (AGENTS.md: a commit made out of order is declared, not rewritten), it was committed
   separately as C4b, immediately after C4. C4c (`116f65940`) strengthens a C4 test
   (`test_the_dashboard_equals_the_three_sections_of_build_dashboard`) with a literal
   `set(payload["dashboard"]) == {"tasks", "live", "story"}` assertion: the original
   assertion derived its expectation from `STORY_DASHBOARD_SECTIONS` itself, so mutation m4
   (that tuple gaining `"metrics"`) would have agreed with itself on both sides of the
   comparison and gone uncaught. This is a correction of a test this round itself wrote,
   made before C7 and declared here, per the block's constraint 4.
2. No other departure from the block's ordered commit sequence (C1a, C1b, C2, C3, C4/C4b/C4c,
   C5, C6, C7).

## Next

Phase 1 rule 1: read `.agent/STOP` from disk before anything else. Then the review of round 7
— R-1102's repair (the dashboard mapping keeping a task's own id) and T003's data half (the
story payload and its reader) — followed, once R-1102 is resolved, by T003 continued: the
story player as a second page of the UI build, and `remedy job story <id> --export <file>`
with its size budget. Open-findings count: 1 (R-1102, High, landed and awaiting review).
Operator-questions count: 1.
