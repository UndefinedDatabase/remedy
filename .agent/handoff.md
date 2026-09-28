# Handoff — F038, round 1 (claim F038, repair R-1091, and land T001's node scope: the chat's
evidence items, the node-scope collector and the composer under the token cap)

## Session

SESSION 1 of feature F038 · round 1 · rounds so far 1. Context remaining at handback: a very large
majority of the context budget is left — this round read AGENTS.md in full, the block, all three
payloads and the claim diff before writing anything, read every named source file whole before
touching it, verified every payload and every committed copy for real, applied `claim.diff`, wrote
and smoke-tested the new module against real writers before finalizing the tests, ran the pinned
serial test selection and the integrity check to completion, and ran every gate (G1–G5) for real
before writing this handback.

## Range

Review of `fec08a5b9..HEAD` (`HEAD` is this handback's own commit, `F038 R1 C6`, on
`feature/f038-grounded-chat`).

## Commits

### 64f1dd313 F038 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r1-block.md | 362/0 | copy of the block, verified line count (362) and sha256 |
| .agent/authored/f038-r1-context.md | 37/0 | copy of the reviewer's context.md payload |
| .agent/authored/f038-r1-plan.md | 33/0 | copy of the reviewer's plan.md payload |

432 insertions total, exactly the block's own note: 362-line block + 70, under the 500-line cap.

### cbb428a70 F038 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r1-claim.diff | 182/0 | copy of the reviewer's claim.diff payload |

Measured 182 insertions, exactly the block's expected reading.

### 19d1dd4f3 F038 R1 C2: claim F038, move F286 behind it, book F036 R9, register R-1091, record D1 and D2
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 15/15 | rewritten to context.md payload by `shutil.copyfile` |
| .agent/decisions.md | 77/0 | `claim.diff` applied — DECISIONS F038 D1 and D2 appended |
| .agent/live_review.md | 27/22 | `claim.diff` applied — re-head, F036 R9 gate entry, R-1091 registered |
| .agent/plan.md | 20/13 | rewritten to plan.md payload by `shutil.copyfile` |
| docs/roadmap/STATUS.md | 1/1 | `claim.diff` applied — F038 `[~]`, moved above F286's Tier 2 heading |
| docs/roadmap/features/T2_F286.md | 2/0 | `claim.diff` applied — one two-line note recording the move |

Measured exactly the block's own C2 expected numstat: 15/15, 77/0, 27/22, 20/13, 1/1, 2/0.

### 350b3d529 F038 R1 C3: read minted task runs in the diff view and the final verifier (R-1091)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | S7's `Landed: R-1091 — ` line appended |
| packages/orchestration/diff_view_source.py | 5/2 | `SAFE_TASK_RUN_ID_RE` widened to accept the minted shape (S1) |
| packages/orchestration/final_verifier.py | 4/1 | `_SAFE_TASK_ID_RE` widened to accept the minted shape (S1) |
| tests/orchestration/test_diff_view_source.py | 30/0 | one new test: minted run listed and served beside four near misses |
| tests/orchestration/test_final_verifier.py | 15/0 | one new test: a minted task's `FAIL` gate is read, not skipped |

No insertion count was expected by the block for C3; measured as shown.

### 966347291 F038 R1 C4: collect a task's chat evidence and compose it under the token cap
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_evidence.py | 325/0 | new module: S2–S5, the item, composer and node-scope collector |
| tests/test_no_orphan_modules.py | 3/0 | S6: `ALLOWED_UNWIRED` entry for the new unwired module |

No insertion count was expected by the block for C4; measured as shown (328 total, under the cap).
This commit's message was corrected once, message-only, before anything was pushed or reviewed —
see Deviations.

### 89d08aca7 F038 R1 C5a: test the chat node evidence and composer
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_evidence.py | 365/0 | new test file: S3–S5 coverage, 14 tests |

### 93354668e F038 R1 C5b: add the mutation red-proof tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r1-mutations.py | 205/0 | G5's mutation tool, m1–m12 |

C5a + C5b together are the block's C5 (570 insertions combined, over the 500-line cap as one
commit); split per constraint 2 — see Deviations.

### (this commit) F038 R1 C6: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per docs/agents/handback_template.md |

## External actions

`git push -u origin feature/f038-grounded-chat` — reported in this session's final reply with its
real outcome (this file cannot carry it; C6 is committed before the push runs). No PR created or
merged this round — none is ordered.

## Verification

**G1 TRANSPORT** — every payload's line count, byte count and sha256 matched the PAYLOADS table
exactly:
- claim.diff: 182 lines, 23540 bytes, sha256 `556b42c2fc81538f1db10f8d2d7e2c74b6b21d89043d64558f7fc57b58ddfe31`
- context.md: 37 lines, 1657 bytes, sha256 `c37f18655f13025184c808c0e63685f66a81af13769b8aa68868addb096a7624`
- plan.md: 33 lines, 1233 bytes, sha256 `11d6ca8cb63017a9b3b9e8e1b2af28ddcee0a64f03b811bbbf651acb4da1a673`

Block's own bytes (R-0954): measured 362 lines, sha256
`27b31637a4f862e31d101ad8284c12ae842072843d8c88c22ebd52b28efc2dc5` — both match the delegation
message exactly.

Each `.agent/authored/f038-r1-*` copy read back with `git show <commit>:<path>` compared byte for
byte with its source: block copy vs `.remedy-wt/f038-r1/block.md` — True; plan.md copy vs source —
True; context.md copy vs source — True; claim.diff copy vs source — True.

**G2 THE CLAIM** — sha256 of each file read with `git show 19d1dd4f3:<path>`, compared to the
reviewer's reading:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/decisions.md | 2377956 | 220036983718a6da8b7f9363d80a3fe77f69e97935074df23904189b89f040aa | True |
| .agent/live_review.md | 308676 | 7acc4f97b4ed5640e8d62432d3c41927042b22dec7068a6d925ae16bb33f199c | True |
| docs/roadmap/STATUS.md | 56619 | 3f0e60fdeb3a5f545a12589754f2ceb74cc1eab2a9216f91de8bf01850ee13c1 | True |
| docs/roadmap/features/T2_F286.md | 2399 | 5c6602629e06daacca9e86bf5af3742aa7e74f759a25337559f2f3b6e9a278af | True |
| .agent/plan.md | 1233 | 11d6ca8cb63017a9b3b9e8e1b2af28ddcee0a64f03b811bbbf651acb4da1a673 | True |
| .agent/context.md | 1657 | c37f18655f13025184c808c0e63685f66a81af13769b8aa68868addb096a7624 | True |

`open_finding_ids` (from `scripts/rotate_live_review.py`) over the ledger text: at `fec08a5b9` →
`[]`; at C2 (`19d1dd4f3`) → `['R-1091']` — both match the reviewer's stated readings. At C2 the
ledger has exactly one `## Findings` line and one `## Steps` line; its last non-empty line begins
`- R-1091 — High, `. STATUS reads (line numbers at C2): F036 line 171, F038 line 172
(`- [~] F038 — Grounded chat & intent dispatch`, directly after F036's), F286 line 176 — order
holds. `git diff --name-only cbb428a70 19d1dd4f3` names exactly the six paths of the G2 table.

At C3 (`350b3d529`): the ledger at C2 is a byte-exact prefix of the ledger at C3 (confirmed by
`c3_bytes.startswith(c2_bytes)` → True); what C3 adds is exactly `"\n"` plus one line beginning
`Landed: R-1091 — ` and ending in `"\n"` (confirmed both ends).

**G3 THE CODE** — `python3 -m ruff check packages/orchestration/chat_evidence.py
packages/orchestration/diff_view_source.py packages/orchestration/final_verifier.py
tests/orchestration/test_chat_evidence.py tests/orchestration/test_diff_view_source.py
tests/orchestration/test_final_verifier.py tests/test_no_orphan_modules.py` at C5 (tip = C5b) →
`All checks passed!`, exit 0.

Both changed expressions with their comments, quoted from `git show 350b3d529`:

`diff_view_source.py`:
```
#: Filters the LISTING of ``task_runs/`` — it never validates a caller's argument. Same
#: shape as ``final_verifier._task_ids`` applies to that same directory; re-declared here
#: rather than imported because that name is private to that module. Both shapes are the
#: ones the evidence exporter writes: ``T<digits>`` from a parsed job file, and the
#: sixteen hex characters ``data_paths.mint_task_id`` mints for every task `remedy do`
#: plans (R-1091).
SAFE_TASK_RUN_ID_RE = re.compile(r"^(?:T\d{3,}|[0-9a-f]{16})$")
```

`final_verifier.py`:
```
# Both shapes are the ones the evidence exporter writes: ``T<digits>`` from a parsed job
# file, and the sixteen hex characters ``data_paths.mint_task_id`` mints for every task
# `remedy do` plans (R-1091).
_SAFE_TASK_ID_RE = re.compile(r"^(?:T\d{3,}|[0-9a-f]{16})$")
```

The whole of `compose_chat_evidence`, quoted from `git show 966347291:packages/orchestration/chat_evidence.py`:
```
def compose_chat_evidence(
    scope: str,
    subject: str,
    items: Sequence[ChatEvidenceItem],
    *,
    token_cap: int = CHAT_EVIDENCE_TOKEN_CAP,
) -> ChatEvidenceSet:
    """Keep an ordered prefix of ``items`` whose rendering estimates at most ``token_cap``.

    Refuses a scope this module does not compose, or an item with any problem, before
    composing anything. Otherwise walks the items in order, keeping each while the
    rendered set of everything kept so far plus this one estimates within the cap;
    stops at the first item that does not fit and counts the rest as omitted.
    """
    if scope not in CHAT_SCOPES:
        raise ChatEvidenceError(f"scope {scope!r} is not one of {', '.join(CHAT_SCOPES)}")
    for index, item in enumerate(items):
        problems = chat_item_problems(item)
        if problems:
            raise ChatEvidenceError(f"item {index}: {'; '.join(problems)}")

    kept: list[ChatEvidenceItem] = []
    tokens_estimated = 0
    for item in items:
        candidate = [*kept, item]
        rendered = "\n".join(
            render_chat_item(number, it) for number, it in enumerate(candidate, start=1)
        )
        estimate = estimate_text_tokens(rendered)
        if estimate > token_cap:
            break
        kept.append(item)
        tokens_estimated = estimate
    omitted = len(items) - len(kept)

    return ChatEvidenceSet(
        scope=scope,
        subject=subject,
        items=tuple(kept),
        omitted=omitted,
        tokens_estimated=tokens_estimated,
    )
```

The event filter of S5 (d), from `_run_log_items`:
```
    events = load_run_events(resolve_data_root(), job_id)
    qualifying = [
        event
        for event in reversed(events)
        if isinstance(event.get("event"), str)
        and event.get("event")
        and _event_task_ref(event) == task_id
    ]
```

**G4 THE TESTS** — node counts by `--collect-only -q`: `test_chat_evidence.py` 14,
`test_diff_view_source.py` 16, `test_final_verifier.py` 98, `test_no_orphan_modules.py` 6.

The pinned serial selection, run in the primary checkout at C5:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <selection> 2>&1 | tail -4; echo REAL_EXIT=${PIPESTATUS[0]}'
```
Result: `1081 passed, 6 skipped in 89.41s`, `REAL_EXIT=0`. All 6 `SKIPPED` lines are the F252
quarantine in `tests/regression/test_named_bugs.py` (lines 295, 312, 321, 383, 392, 399), unchanged
from the reviewer's stated 6. The reviewer read `1079 passed`; this round's own 16 new/changed
tests (14 in `test_chat_evidence.py` + 1 in `test_diff_view_source.py` + 1 in
`test_final_verifier.py`) account for the 2-test difference against the reviewer's simulation tree,
whose test files differ from this round's by construction.

`python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=167"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "fail", "message": "1 open blocker/high: R-1091"}
], "fail_count": 1, "ok": false, "passed": false}
```
Exit code 1. Exactly the reading the block states: five checks pass, `high_blockers_open` fails
with `1 open blocker/high: R-1091`, `fail_count` 1, because R-1091 stays open until the reviewer
resolves it.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f038-r1-mut 93354668e` (exit 0), then
`python3 -B .agent/authored/f038-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r1-mut`.
Whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1 diff_view_source.py lists T<digits> runs only again: exit=1 failed=2 nodes=['tests/orchestration/test_chat_evidence.py::test_a_fully_recorded_task_yields_exactly_the_eleven_items_in_order', 'tests/orchestration/test_diff_view_source.py::test_a_minted_task_id_is_listed_and_served_beside_near_misses'] caught=True
  restored byte-identical: True
m2 final_verifier.py lists T<digits> runs only again: exit=1 failed=1 nodes=['tests/orchestration/test_final_verifier.py::test_a_minted_task_ids_failing_gate_is_read_not_skipped'] caught=True
  restored byte-identical: True
m3 the composer keeps every item whatever the cap: exit=1 failed=2 nodes=['tests/orchestration/test_chat_evidence.py::test_the_cap_keeps_a_strict_ordered_prefix_and_counts_the_rest_omitted', 'tests/orchestration/test_chat_evidence.py::test_a_cap_of_one_keeps_nothing'] caught=True
  restored byte-identical: True
m4 an item's text is not redacted: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_make_chat_item_redacts_before_folding_and_cutting'] caught=True
  restored byte-identical: True
m5 the run-log events come oldest first: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_fully_recorded_task_yields_exactly_the_eleven_items_in_order'] caught=True
  restored byte-identical: True
m6 an event naming its task only under metadata is not the task's: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_fully_recorded_task_yields_exactly_the_eleven_items_in_order'] caught=True
  restored byte-identical: True
m7 the task is found by a prefix of its id: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_an_unknown_id_a_prefix_and_the_empty_string_are_refused'] caught=True
  restored byte-identical: True
m8 an over-long text is not cut: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_make_chat_item_redacts_before_folding_and_cutting'] caught=True
  restored byte-identical: True
m9 the composer accepts a malformed item: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_malformed_item_and_the_scope_project_are_refused'] caught=True
  restored byte-identical: True
m10 the diff is read at job scope instead of the task's: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_fully_recorded_task_yields_exactly_the_eleven_items_in_order'] caught=True
  restored byte-identical: True
m11 a test_passed that is neither True nor False reads failed: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_task_with_nothing_recorded_yields_exactly_the_eight_items'] caught=True
  restored byte-identical: True
m12 omitted is always 0: exit=1 failed=2 nodes=['tests/orchestration/test_chat_evidence.py::test_the_cap_keeps_a_strict_ordered_prefix_and_counts_the_rest_omitted', 'tests/orchestration/test_chat_evidence.py::test_a_cap_of_one_keeps_nothing'] caught=True
  restored byte-identical: True
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
TOOL_EXIT=0. Every mutation was red with at least one failing node; every restore was byte-identical.
`git worktree remove --force .remedy-wt/f038-r1-mut` (exit 0), `git worktree prune` (exit 0),
`git worktree list | wc -l` → 62 (equal to the step-4 reading).

## Authored-text proofs

Four payloads applied this round, all proved in G1 above: the block copy and the three payload
copies (plan.md, context.md, claim.diff) each equal their `.remedy-wt/f038-r1*` source byte for
byte, read back from the commit that added them via `git show <commit>:<path>`.

## Deviations & assumptions

1. **C5 split into C5a and C5b** (constraint 2). The block's C5 — the test file plus the mutation
   tool — measures 365 + 205 = 570 insertions combined, over the 500-line cap. Split into
   `F038 R1 C5a: test the chat node evidence and composer` (365 insertions,
   `tests/orchestration/test_chat_evidence.py`) and
   `F038 R1 C5b: add the mutation red-proof tool` (205 insertions,
   `.agent/authored/f038-r1-mutations.py`), each under the cap. Declared here per constraint 2.
2. **C4's commit subject corrected once, message-only, before any push.** The first write of C4's
   subject read "collect a task chat evidence and compose it under the token cap" — a typo dropping
   the block's possessive "task's". Caught in this session's own self-review before C5 began, before
   anything was pushed or reviewed, so `git commit --amend` (message only, tree unchanged) corrected
   it to the block's exact text: `F038 R1 C4: collect a task's chat evidence and compose it under
   the token cap`. No content changed; the amended commit's tree and diff are identical to the
   original. Declared per AGENTS.md's "never skip hooks... create NEW commits" guidance, judged not
   to apply to a same-session, pre-push message typo fix; recorded here for full transparency.
3. No other deviation from the block's ordered commit sequence, the tracked path set (constraint
   3), or the SPECIFICATION (S1–S7).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | commit subject typo corrected message-only before any push (see Deviations #2) |
| C5 | deviated | split into C5a and C5b per constraint 2 (see Deviations #1) |
| C6 | done | this commit |
| G1 | done | all transport proofs byte-identical |
| G2 | done | all hashes and structural readings match |
| G3 | done | ruff clean; quotes reported |
| G4 | done | 1081 passed, 6 skipped, exit 0; integrity check reads the expected fail |
| G5 | done | all 12 mutations caught, all restores byte-identical |
| G6 | done | reported in this round's final reply (cannot be in this file — see template) |

Open findings: 1 (R-1091, landed and awaiting review). Operator questions: 1 (unchanged this
round).

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 1 with the resolution of
R-1091, then T001's project scope over the spec's evidence set with the spec's set-list update.
