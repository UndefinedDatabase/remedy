# Handback — F041, round 1: claim, book F286 R4, land T001's pipeline — COMPLETE after amendment

## Session

SESSION 1 of feature F041 · round 1 · rounds so far 1. This session claimed F041, re-headed the
live review record, booked F286's round 4 (C1a-C1c, C2), wrote and validated S1-S6 in full, then
hit C3's own "stop and report rather than split it" clause at 542 insertions and wrote a blocked
handback (C7, pushed). The reviewer's amendment (A1) withdrew that clause, ruled it an authoring
error, and ordered C3 split into C3a/C3b; this session then copied the amendment (A0), landed C3a,
C3b, C4, C5, C6 exactly as ordered, ran every gate for real, and rewrites this handback as C8.
Context self-assessment: a comfortable amount of context remains; the round completed inside one
session, across one blocked handback and its amendment.

For the operator, in plain words: F041's round 1 is now COMPLETE. The sanitized markdown renderer,
the artifact-root path gate, and the artifacts route are committed, pass the reviewer's whole
attack corpus and traversal fixtures unedited, and are red-proved against all 9 named mutations in
a real worktree. Nothing is merged; no pull request exists yet — the branch is pushed and waits for
review.

## Range

Review of 45c584e6e..HEAD (bc8be7d66 before this commit)

## Commits

### f690d984d F041 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r1-block.md | +311/-0 | verbatim copy of this round's block |
| .agent/authored/f041-r1-context.md | +33/-0 | verbatim copy of the context.md payload |
| .agent/authored/f041-r1-plan.md | +31/-0 | verbatim copy of the plan.md payload |

Measured: 375 insertions (311+33+31), matching "this block's line count plus 64" (311+64=375).

### bd6c2bd3b F041 R1 C1b: copy round 1 claim, allowlist and roots diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r1-allowlist.diff | +13/-0 | verbatim copy of the allowlist.diff payload |
| .agent/authored/f041-r1-claim.diff | +130/-0 | verbatim copy of the claim.diff payload |
| .agent/authored/f041-r1-roots.diff | +279/-0 | verbatim copy of the roots.diff payload |

Measured: 422 insertions, matching the block's expected 422 exactly.

### 2c21ea309 F041 R1 C1c: copy round 1 corpus diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r1-corpus.diff | +296/-0 | verbatim copy of the corpus.diff payload |

Measured: 296 insertions, matching the block's expected 296 exactly.

### f87ab2917 F041 R1 C2: claim F041, re-head the live review record, book F286 R4, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +11/-9 | rewritten to the round's context.md payload |
| .agent/decisions.md | +51/-0 | DECISION F041 D1 appended, via claim.diff |
| .agent/live_review.md | +21/-20 | re-headed for F041; F286 R4's Gate entry appended, via claim.diff |
| .agent/plan.md | +17/-9 | rewritten to the round's plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F041's line `[ ]` to `[~]`, via claim.diff |

Measured: 11/9, 51/0, 21/20, 17/9, 1/1 — matches the block's expected table exactly.

### 91839c9ad F041 R1 C7: rewrite handoff for round 1 (BLOCKED handback, since withdrawn as current)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | +231/-136 | rewritten to report the C3 stop |
| .agent/plan.md | +15/-9 | Current Step/Next Steps updated to the blocked state |

Measured: 231/136, 15/9. Pushed before the amendment arrived; per the amendment, "C7 stays as it
is" — not rewritten, not reset. This handback (C8) supersedes it as the current state.

### c007f5d2f F041 R1 A0: copy the reviewer's amendment into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r1-amend.md | +46/-0 | verbatim copy of the amendment |

Measured: 46 insertions, matching the amendment's own line count.

### 6c3f562ee F041 R1 C3a: render a README to a sanitized fragment on the server
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/artifact_markdown.py | +398/-0 | S1-S4: constants, `safe_url`, `sanitize_fragment`, `render_markdown` |

Measured: 398 insertions. Under the 500 cap alone.

### 416f41ce7 F041 R1 C3b: serve the artifacts view from derived roots through one path gate
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/artifact_preview.py | +134/-0 | S5: roots, `resolve_artifact_path`, `artifacts_view` |
| packages/orchestration/ui_server.py | +8/-0 | S6: `_build_artifacts_json` and the `handlers` dict entry |
| tests/orchestration/import_reachability_allowlist.txt | +2/-0 | `artifact_markdown` and `artifact_preview` added |

Measured: 134/0, 8/0, 2/0 — total 144 insertions. Under the 500 cap.

### 549bdf345 F041 R1 C4: add the reviewer's attack corpus for the markdown pipeline
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_artifact_markdown.py | +290/-0 | NEW FILE, the reviewer's attack corpus |

Measured: 290 insertions.

### 6a57aa0e8 F041 R1 C5: add the reviewer's traversal fixtures and artifacts route tests
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_artifact_preview.py | +147/-0 | NEW FILE, the traversal fixtures |
| tests/ui_server/test_artifacts_route.py | +120/-0 | NEW FILE, the route tests |

Measured: 267 insertions.

### bc8be7d66 F041 R1 C6: add the round 1 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r1-mutations.py | +115/-0 | the G4 mutation tool, m1-m9 |

Measured: 115 insertions.

### (this commit) F041 R1 C8: rewrite handoff for round 1 after the amendment
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |
| .agent/plan.md | Current Step/Next Steps put back to round 1 complete, round 2 next |

## External actions

- `git reset --soft HEAD^` × 3, each on my OWN just-made, UNPUSHED commit, each corrected and
  immediately recommitted (see Deviations): once for the premature C7 (before this session's
  amendment arrived — see Deviations), and twice for a commit-subject apostrophe typo (A0, then
  C4). No pushed commit was ever reset, rewritten or force-pushed.
- `git worktree add --detach .remedy-wt/f041-r1-mut bc8be7d66` (at C6): exit 0. Mutation tool run
  (see Verification, G4). `git worktree remove --force .remedy-wt/f041-r1-mut` then `git worktree
  prune`: exit 0. `git worktree list | wc -l`: 62 before and after, matching the step-4 reading.
- `git push -u origin feature/f041-artifact-preview` (earlier, for C7): succeeded, new branch.
  `git push` (this commit, C8): outcome reported in the reply.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`.

## Verification

**G1 TRANSPORT** — unchanged from C7's reading (all 6 payloads matched; all 7 `.agent/authored/`
copies byte-identical), PLUS the amendment's added reading:

`.agent/authored/f041-r1-amend.md` read via `git show c007f5d2f:.agent/authored/f041-r1-amend.md`:
3336 bytes, sha256 `9e835729cf329f4cf6203f02e372a0b70e84774e37252fb3bc281a7500884bd9` — matches the
delegation message's digest exactly, and is byte-identical to `.remedy-wt/f041-r1/amend.md`.

**G2** — already met at C2 (see C7's handback for the full derivation: all 5 file hashes, the
`open_finding_ids` empty-set reading at `45c584e6e` and at C2, the ledger's structural checks, the
STATUS line, and `git diff --name-only` C1c..C2). Nothing new to report.

**G3 THE CODE AND THE TESTS**

`python3 -m ruff check` on all 7 files (both new modules, all three new test files, the mutation
tool): `All checks passed!`, REAL_EXIT=0.

`git show --numstat` at C3a: `398 0 packages/orchestration/artifact_markdown.py`. At C3b: `134 0
packages/orchestration/artifact_preview.py`, `8 0 packages/orchestration/ui_server.py`, `2 0
tests/orchestration/import_reachability_allowlist.txt`. `ui_server.py`'s diff at C3b is exactly the
`_build_artifacts_json` function (placed directly after `_build_tour_json`) and the `"artifacts":
_build_artifacts_json,` handlers-dict entry (directly after `"tour"`) — nothing else in the file
changes.

AT C3a (the amendment's added reading): `python3 -m pytest -q -p no:cacheprovider
tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py` → **9 passed,
REAL_EXIT=0 — no orphan failure.** This is a DEVIATION from the amendment's stated expectation
("reads the new module as an orphan by construction"): both guards scan the LIVE FILESYSTEM at
`REPO_ROOT`, not git history, and `packages/orchestration/artifact_preview.py` — C3b's own payload
— was already sitting on disk at that moment (staged for the next commit, in this one persistent
primary checkout, never removed or stashed between commits) with its production import `from
packages.orchestration.artifact_markdown import render_markdown` already satisfying the
reachability scan. No other guard was red at C3a either way, so the amendment's "no other guard may
be red" condition holds; only the orphan window it predicted did not materialize, for the reason
just given.

At C6, in the primary checkout, serially, the full ordered selection:
```
python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_artifact_markdown.py tests/orchestration/test_artifact_preview.py tests/ui_server/test_artifacts_route.py tests/ui_server/test_command_channel.py tests/ui_server/test_tour_route.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_development_artifact_boundary.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
```
`SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine`, then `661 passed, 1 skipped in
81.54s`. REAL_EXIT=0 — matches the reviewer's stated reading exactly (`661 passed, 1 skipped`),
same one SKIPPED line.

`--collect-only -q` node counts: `test_artifact_markdown.py` 106, `test_artifact_preview.py` 20,
`test_artifacts_route.py` 5 — match the reviewer's stated 106/20/5 exactly.

`python3 -m apps.cli.main integrity check --json`, at C6: **all six checks `pass`**, `fail_count:
0`, `ok: true`. REAL_EXIT=0.

**G4 THE RED PROOFS** — run per the amendment, in a worktree ADDED at C6 (not populated by
copying, unlike the informal check in the withdrawn C7):

`git worktree add --detach .remedy-wt/f041-r1-mut bc8be7d66`: exit 0.
`python3 -B .agent/authored/f041-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r1-mut`,
whole output:
```
CONTROL (unmutated, first):
  tests/orchestration/test_artifact_markdown.py: exit=0 failed=0
  tests/orchestration/test_artifact_preview.py: exit=0 failed=0
  tests/ui_server/test_artifacts_route.py: exit=0 failed=0
m1: exit=1 failed=1 caught=True
restored byte-identical: True
m2: exit=1 failed=3 caught=True
restored byte-identical: True
m3: exit=1 failed=3 caught=True
restored byte-identical: True
m4: exit=1 failed=19 caught=True
restored byte-identical: True
m5: exit=1 failed=17 caught=True
restored byte-identical: True
m6: exit=1 failed=3 caught=True
restored byte-identical: True
m7: exit=1 failed=1 caught=True
restored byte-identical: True
m8: exit=1 failed=1 caught=True
restored byte-identical: True
m9: exit=1 failed=2 caught=True
restored byte-identical: True
CONTROL (unmutated, last):
  tests/orchestration/test_artifact_markdown.py: exit=0 failed=0
  tests/orchestration/test_artifact_preview.py: exit=0 failed=0
  tests/ui_server/test_artifacts_route.py: exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 9 mutations caught (nonzero exit), all 9 restorations byte-identical. `git worktree remove
--force .remedy-wt/f041-r1-mut` then `git worktree prune`: exit 0; `git worktree list | wc -l`: 62.

**G5** — reported in the reply (this file cannot contain the push outcome per the block).

## Authored-text proofs

All eight reviewer-authored texts applied this round, each compared disk-to-disk against its
committed `.agent/authored/f041-r1-*` blob (read via `git show <sha>:<path>`):

| authored file | applied as | result |
|---|---|---|
| f041-r1-block.md | (verification copy of this block, at f690d984d) | IDENTICAL |
| f041-r1-plan.md | rewrote `.agent/plan.md` at C2 | IDENTICAL |
| f041-r1-context.md | rewrote `.agent/context.md` at C2 | IDENTICAL |
| f041-r1-claim.diff | `git apply`'d at C2 | applied clean, exit 0 |
| f041-r1-allowlist.diff | `git apply`'d, committed at C3b | applied clean, exit 0, IDENTICAL |
| f041-r1-roots.diff | `git apply`'d, committed at C5 | applied clean, exit 0, IDENTICAL |
| f041-r1-corpus.diff | `git apply`'d, committed at C4 | applied clean, exit 0, IDENTICAL |
| f041-r1-amend.md | (verification copy of the amendment, at c007f5d2f) | IDENTICAL |

## Deviations & assumptions

1. **The C3 stop.** C3's original clause ("stop and report rather than split it") was triggered
   honestly: S1-S6 plus `allowlist.diff` measured 542 insertions in one commit, over the 500 cap.
   The reviewer's amendment (A1) ruled this the reviewer's own authoring error (sized from a
   shorter draft), not a deviation of mine, withdrew the clause, and replaced C3 with C3a/C3b —
   executed above.
2. **The premature C7.** Round 1's first handback (`91839c9ad`) was written and pushed while
   genuinely believing the round was blocked; the amendment shows the block itself was in error,
   not the stop. Per the amendment, "C7 stays as it is" — it was never reset, rewritten or
   force-pushed; this handback (C8) is the new current state, and C7's own commit table entry above
   is marked superseded rather than removed.
3. **The soft reset of my own unpushed commit(s).** Three times this round I ran `git reset --soft
   HEAD^` on a commit I had JUST created and had NOT yet pushed: once mid-C7 (before this
   amendment) to remove an accidental staging leak, once on A0 and once on C4, both to fix a
   commit-subject apostrophe typo before it reached the remote. All three are corrections of my own
   local, unpushed work; no pushed commit was ever touched.
4. **G3's orphan check at C3a did not fail**, contrary to the amendment's stated expectation — see
   the full explanation under G3 above (a filesystem-scanning guard sees C3b's not-yet-committed
   but already-on-disk file in this persistent primary checkout).

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk at the start of the next session.
2. Round 1 is COMPLETE. Round 2 is next: the file route for screenshot bytes and the full README,
   with its headers, and the start of T002.

Open findings: 0. Operator-questions count: 1 (`.agent/operator_questions.md`, unanswered, carried
forward unchanged by this round).
