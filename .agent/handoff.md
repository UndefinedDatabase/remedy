# Handback — F286, round 1: claim F286 and land T001 (R-1104)

## Session

SESSION 1 of feature F286 · round 1 · rounds so far 1. This session ran round 1 only: verified the
block and every payload byte-exact, cut `feature/f286-findings-paydown-v5` from `6ba1f4be8`,
applied the claim diff (re-heading `.agent/live_review.md`, booking F039's round 13 gate entry,
recording DECISION F286 D1, flipping F286's STATUS line to `[~]`, and writing F286's slice list),
landed T001's repair in `packages/orchestration/doc_staleness.py` (S1–S3), added the fixture test
and live guard (S4–S5) plus the mutation tool, and ran G1–G4. Context self-assessment: a
comfortable margin remained through the whole round — every payload and the block matched its
table on the first read, `git apply --check` passed clean, every numstat and hash gate matched its
expected reading on the first try, the targeted pytest selection and the mutation tool both passed
on the first run with no repair needed, and the work was not near its limit.

For the operator, in plain words: this round claimed the fifth findings paydown, F286, and repaired
its one open finding, R-1104 — the documentation-staleness catalog was misreading a guide's
backticked file name (`story.html`) as an unregistered config key, because the name happens to
start with a registered key's namespace (`story`). The check now leaves out any backticked span
whose last segment is a known file extension, while it still correctly reports a genuinely
unregistered key like `story.speed` in the same namespace. Four targeted mutations to the fix each
broke a test and were each cleanly caught and reverted. The next round starts F286's closure
sequence: the one full-suite integration-gate run, the evidence bundle and review package, then the
close, which registers the next paydown.

## Range

Review of 6ba1f4be8..HEAD

## Commits

### 60109f5e8 F286 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f286-r1-block.md | +242/-0 | verbatim copy of this round's block |
| .agent/authored/f286-r1-context.md | +31/-0 | verbatim copy of the context payload |
| .agent/authored/f286-r1-plan.md | +26/-0 | verbatim copy of the plan payload |

Measured insertions: 299 (242 + 31 + 26), matching the block's expectation "this block's line count
plus 57" (242 + 57 = 299) exactly. Under the 500-line cap.

### e4accbc10 F286 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f286-r1-claim.diff | +136/-0 | verbatim copy of the claim diff payload |

Measured: 136 insertions, matching the block's expected 136 exactly.

### 5f4e1e635 F286 R1 C2: claim F286, re-head the live review record, book F039 R13, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +9/-13 | rewritten to F286's context (`context.md` payload) |
| .agent/decisions.md | +37/-0 | DECISION F286 D1 appended |
| .agent/live_review.md | +22/-21 | re-headed for F286; F039 R13 gate entry appended |
| .agent/plan.md | +13/-13 | rewritten to F286's plan (`plan.md` payload) |
| docs/roadmap/STATUS.md | +1/-1 | F286's line `[ ]` → `[~]` |
| docs/roadmap/features/T2_F286.md | +7/-0 | Task slicing section (T001) added |

Measured: 9/13, 37/0, 22/21, 13/13, 1/1, 7/0 — matching the block's expected table exactly, per
file. `git apply --check` on `claim.diff` exited 0 before the real `git apply`, which also exited 0.

### 5d761c433 F286 R1 C3: leave a backticked file name out of the config-key check (R-1104)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/doc_staleness.py | +10/-1 | S1 `_FILE_EXTENSIONS` + comment, S2 the skip in `_run_c07`, S3 the catalog claim text |

Measured: 10 insertions, 1 deletion. The block states none is expected for C3; this is what was
measured.

### fe2521ea2 F286 R1 C4: hold story.html out of the config-key check and add the mutation tool
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_doc_staleness.py | +28/-0 | S4 the fixture test, S5 the live guard |
| .agent/authored/f286-r1-mutations.py | +114/-0 | the G4 mutation tool |

Measured: 28 + 114 = 142 insertions. The block states none is expected for C4; this is what was
measured.

### (this commit) F286 R1 C5: rewrite handoff for round 1
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f286-r1-mut fe2521ea2` — succeeded, used for G4.
- `git worktree remove --force .remedy-wt/f286-r1-mut` then `git worktree prune` — succeeded;
  `git worktree list | wc -l` read 62 both before (step 4) and after removal.
- `git push -u origin feature/f286-findings-paydown-v5` — run after this commit; its real outcome
  is reported in the reply (this file cannot contain it, per the block).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`.

## Verification

**G1 TRANSPORT** — payload readings against the PAYLOADS table (all matched before use):

| file | lines | bytes | sha256 match |
|---|---|---|---|
| claim.diff | 136 | 14751 | match |
| plan.md | 26 | 837 | match |
| context.md | 31 | 1188 | match |

Block self-verification (BEFORE ANYTHING ELSE step 3): lines 242 (expected 242), bytes 17634
(expected 17634), sha256 matched exactly. No difference found.

Committed-copy-vs-source, read back with `git show <commit>:<path>`, byte for byte:
```
60109f5e8 .agent/authored/f286-r1-block.md   == .remedy-wt/f286-r1/block.md            -> True
60109f5e8 .agent/authored/f286-r1-plan.md    == .remedy-wt/f286-r1-payloads/plan.md    -> True
60109f5e8 .agent/authored/f286-r1-context.md == .remedy-wt/f286-r1-payloads/context.md -> True
e4accbc10 .agent/authored/f286-r1-claim.diff == .remedy-wt/f286-r1-payloads/claim.diff -> True
```

**G2 THE CLAIM** — sha256 of each file, read with `git show 5f4e1e635:<path>`, against the
reviewer's reading:

| path | bytes | sha256 match |
|---|---|---|
| .agent/context.md | 1188 | match |
| .agent/decisions.md | 2447895 | match |
| .agent/live_review.md | 319065 | match |
| .agent/plan.md | 837 | match |
| docs/roadmap/STATUS.md | 57372 | match |
| docs/roadmap/features/T2_F286.md | 3248 | match |

`open_finding_ids` (from `scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text:
- at `6ba1f4be8`: `['R-1104']`
- at `5f4e1e635` (C2): `['R-1104']`

At C2: exactly one line reads `## Findings` (count 1) and exactly one reads `## Steps` (count 1);
the last non-empty line begins `Gate: F039 R13 — ` (True). F286's STATUS line at C2 read back in
full: `- [~] F286 — Findings paydown v5` (exact match). `git diff --name-only e4accbc10 5f4e1e635`
named exactly: `.agent/context.md`, `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F286.md` — exactly the table above, no more, no
less.

**G3 THE CODE AND THE TESTS**

`python3 -m ruff check packages/orchestration/doc_staleness.py tests/orchestration/test_doc_staleness.py .agent/authored/f286-r1-mutations.py`
at C4: `All checks passed!`, REAL_EXIT=0.

`_FILE_EXTENSIONS` with its comment and the whole of `_run_c07`, quoted from `git show 5d761c433`:
```python
# No config key ends in a file extension, so a span whose last segment is one is a file
# name that begins with a key prefix, not a key (R-1104).
_FILE_EXTENSIONS = frozenset({
    "css", "html", "js", "json", "md", "py", "sh", "toml", "ts", "tsx", "txt", "yaml", "yml",
})


def _run_c07(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "doc_config_keys"
    items: list[tuple[int, int, StaleClaim]] = []
    prefixes = truth.key_prefixes
    documents = [_README, _INDEX] + _guide_documents(root)
    for order, document in enumerate(documents):
        text = _read(root, document)
        if text is None:
            continue
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _SPAN_RE.finditer(line):
                span = m.group(1)
                if not _KEY_NAME_WHOLE_RE.match(span):
                    continue
                first = span.split(".", 1)[0]
                if first not in prefixes:
                    continue
                last = span.rsplit(".", 1)[-1]
                if last in _FILE_EXTENSIONS:
                    continue
                if span in truth.command_ids:
                    continue
                if span not in truth.config_keys:
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"backticks the config key `{span}`",
                        f"`{span}` is not a registered config key",
                    )))
    return _sorted_claims(items)
```

`[c for c in run_staleness_checks() if c.check_id == "doc_config_keys"]` in the primary checkout at
C4: `[]` — matches the reviewer's reading of `[]` in its simulation tree. The block's own text
states the same call at `6ba1f4be` answers the one claim about `story.html`; this round did not
independently re-run that call at `6ba1f4be` (see Deviations).

Targeted pytest selection, run serially (`-p no:cacheprovider -rs`), tail:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
576 passed, 1 skipped in 57.03s
```
REAL_EXIT=0 — matches the reviewer's reading of `576 passed, 1 skipped` at exit 0 exactly, and the
one `SKIPPED` line matches exactly.

`tests/orchestration/test_doc_staleness.py --collect-only -q`: `33 tests collected` — matches the
reviewer's reading of 33 exactly.

`python3 -m apps.cli.main integrity check --json`: `check_count: 6`, `fail_count: 0`, `ok: true`,
`passed: true`, all six checks `"status": "pass"` (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`). REAL_EXIT=0.

**G4 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f286-r1-mut fe2521ea2`, then
`python3 -B .agent/authored/f286-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f286-r1-mut`,
whole output:
```
control (before, unmutated): exit=0 failed=0
m1 the skip of S2 is deleted: exit=1 failed=1
restored byte-identical: True
m2 html is removed from _FILE_EXTENSIONS: exit=1 failed=1
restored byte-identical: True
m3 the skip reads the span's FIRST segment instead of its last: exit=1 failed=1
restored byte-identical: True
m4 host is added to _FILE_EXTENSIONS, which hides the registered key ollama.host: exit=1 failed=1
restored byte-identical: True
control (after, unmutated): exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. Every mutation exited non-zero with failed count 1; no test needed to be added. Then
`git worktree remove --force .remedy-wt/f286-r1-mut`, `git worktree prune`; `git worktree list | wc -l`
read 62, equal to the step-4 reading.

**Constraint 3 (tracked path set)** — `git diff --name-only 6ba1f4be8` at the branch tip after C5
is reported in the reply (cannot be measured before this commit exists). Before C5 it read exactly:
`.agent/authored/f286-r1-block.md`, `.agent/authored/f286-r1-claim.diff`,
`.agent/authored/f286-r1-context.md`, `.agent/authored/f286-r1-mutations.py`,
`.agent/authored/f286-r1-plan.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`,
`docs/roadmap/features/T2_F286.md`, `packages/orchestration/doc_staleness.py`,
`tests/orchestration/test_doc_staleness.py` — exactly the block's declared set. None of the six
forbidden paths (`docs/guides/story-user-guide-v1.md`, `scripts/self_use_queue.json`,
`.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`) were
touched.

## Authored-text proofs

Every reviewer-authored text applied this round, disk-to-disk against the committed
`.agent/authored/` file:
- `.agent/authored/f286-r1-block.md` (C1a) == `.remedy-wt/f286-r1/block.md`: byte-identical.
- `.agent/authored/f286-r1-plan.md` (C1a) == `.remedy-wt/f286-r1-payloads/plan.md`: byte-identical.
- `.agent/authored/f286-r1-context.md` (C1a) == `.remedy-wt/f286-r1-payloads/context.md`:
  byte-identical.
- `.agent/authored/f286-r1-claim.diff` (C1b) == `.remedy-wt/f286-r1-payloads/claim.diff`:
  byte-identical.

`.agent/plan.md` and `.agent/context.md` were rewritten from the same verified `plan.md` and
`context.md` payloads via `shutil.copyfile` (C2); `claim.diff` was applied via `git apply` only
(C2), never retyped or edited.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| G1 | done | all transport reads matched byte-exact |
| G2 | done | all claim hashes, open-set reads and structural checks matched |
| G3 | done | ruff clean, live check reads `[]`, targeted suite 576 passed/1 skipped at exit 0, integrity all-pass |
| G4 | done | all 4 mutations caught, all restores byte-identical |

## Deviations & assumptions

1. **Assumption, not a deviation from the bundle or gates**: G3's prose states "the same call at
   `6ba1f4be` answers the one claim about `story.html`" as background from DECISION F286 D1. The
   block orders the `run_staleness_checks()` call to be run "in the primary checkout at C4" only;
   it does not order a second worktree at `6ba1f4be` to re-verify the pre-repair reading, and
   constraint 7 sanctions only the one worktree G4 adds. This round took the DECISION's own
   measurement (made by the reviewer at `c5eb695b`, referencing the pre-existing R-1104 finding
   text) as given rather than independently reproducing it. If this reading should have been
   independently reproduced, that is a gap to flag at review.
2. No other deviation: the bundle ran C1a, C1b, C2, C3, C4, C5 in the block's exact order; no gate
   went red; no payload was edited or retyped; no forbidden path was touched; no full-suite run was
   made (amend0917 rule 1 reserved); no provider call and no self-use job were run.

## Next

Per the block's `## Next` order: Phase 1 rule 1 — read `.agent/STOP` from disk before anything
else. Then the review of this round (round 1). Then the closure sequence's integration-gate round
(the one full-suite run, per amend0917-throughput). Open-findings count: 1 (R-1104, owned by F286,
not yet resolved — its resolution line is authored by the reviewer, not this round, per constraint
4). Operator-questions count: 1 (Q6, open in `.agent/operator_questions.md`).
