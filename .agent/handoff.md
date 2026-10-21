# Handback — F303 round 1: claim, the inventory and the contract's two missing proofs

## Session

SESSION 1 of feature F303 · round 1 · rounds so far 1

Context self-assessment: this worker verified every prepared digest, byte-copied the nine C1
files, wrote the two new contract proofs and widened the 404 parametrization from the block's
own specification, ran every gate once, and wrote this handback with ample context margin left.

Fortschritt: ~15 % (claim, inventory and the contract's proofs landed · note route and MCP facet open) — Schätzung

## Range

Review of `2621bbe2e`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### ef978b9c6 F303 R1 C1: claim F303, book F060 R7, the inventory and DECISION F303 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r1.md` | 142/0 | this round's block, byte copy (142 lines, sha256 `52ad16a12b355e0a07c2583a2dcddca5529a05cc3b25cf501869a6626450cd71`, equal to `block.md`) |
| `.agent/f303_inventory.md` | 60/0 | T001's inventory of what the public API already publishes (prepared file, byte copy) |
| `docs/roadmap/STATUS.md` | 1/1 | F303 claimed, `[ ]` to `[~]` (prepared file, byte copy) |
| `docs/roadmap/features/T12_F303.md` | 4/0 | Acceptance line for R-1329, moved here by DECISION F303 D1 (prepared file, byte copy) |
| `docs/roadmap/features/T2_F307.md` | 1/1 | names R-1329's move to F303 (prepared file, byte copy) |
| `.agent/live_review.md` | 17/13 | re-headed at F303's claim, the Owner line moving R-1329, F060 round 7's gate booked (prepared file, byte copy) |
| `.agent/decisions.md` | 14/0 | DECISION F303 D1 appended (prepared file, byte copy) |
| `.agent/plan.md` | 14/11 | rewritten for F303 round 1 (prepared file, byte copy) |
| `.agent/context.md` | 8/10 | rewritten for F303 (prepared file, byte copy) |

### 6fbbfab16 F303 R1 C2: the route served outside the public API is named, and the contract's served set and the logs order are proved
| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 9/0 | hand-written section "Served outside the public API" naming the socket's command door (DECISION F303 D1 (3)) |
| `tests/ui_server/test_public_api.py` | 75/0 | three new tests: the logs route's order over one run proved through the route, not only below it (DECISION F303 D1 (4)); the contract page's served-outside-the-API set pinned to the one door; the socket's refusal set over eight method/path pairs plus a sibling case proving the door itself refuses an unauthenticated caller |
| `tests/orchestration/test_serve_daemon.py` | 4/3 | `test_the_api_port_answers_every_cockpit_only_path_404` widened to every pair of the four methods and six paths the block names (its own name and body unchanged) |

### C3 F303 R1 C3: handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | new | this handback |

## External actions

- `git push -u origin feature/f303-face-public-api` follows this commit; its outcome is reported
  in the session reply.
- No pull request is opened this round (the block orders none).
- No merge. No worktree was added or removed. No provider call.

## Verification

Preconditions: `block.md` (142 lines), `verify.py`, `run_selection.py`, `selection.txt` and
`digests.txt` matched the digests given in the prompt; the nine `c1-` files matched the digests
in `digests.txt`. Before the first write, `HEAD` read `2621bbe2e`, the tree was clean,
`.agent/STOP` was absent, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
answered `[]`.

1. Gate 1: `git status --porcelain` — empty. `python3 .remedy-wt/f303-r1/prep/verify.py .` — every
   line `True` (17 checks), `absent	C3`, last line `ALL True`.
2. Gate 2: `python3 -m ruff check tests/ui_server/test_public_api.py tests/orchestration/test_serve_daemon.py`
   — `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f303-r1/prep/run_selection.py . .remedy-wt/f303-r1-worker/selection-output.txt`
   — `paths 77`, `exit 0`, `3832 passed, 2 skipped in 81.79s`; no FAILED or ERROR line, no
   `process(es) behind` line. SKIPPED lines: `tests/test_agent_tooling.py:43` (D12 quarantine F252,
   the reviewer agent file deleted deliberately); `tests/test_install_smoke.py:175` (install smoke
   is opt-in, needs REMEDY_INSTALL_SMOKE=1 and network).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 1, `fail_count` 1, only
   `high_blockers_open`, naming the same twelve findings as before this round: `R-1335, R-1336,
   R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`.
5. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   — `88`.
6. Gate 6: `git -C . diff --stat 2621bbe2e HEAD -- packages apps` — prints nothing.

## Authored-text proofs

C1's `.agent/authored/f303-r1.md`: byte copy of `c1-.agent__authored__f303-r1.md`, itself
byte-equal to `block.md` (142 lines, sha256
`52ad16a12b355e0a07c2583a2dcddca5529a05cc3b25cf501869a6626450cd71`), both readings matching before
the commit. The other eight C1 paths: prepared files, proven equal over bytes at copy time and
again by `verify.py` (every `equals` line `True`). C2 applied no reviewer-authored text; its two
tests and the contract section are this worker's own, written from the block's specification in
`## Change set — C2` of `block.md`.

## Deviations & assumptions

None. The change set, the paths touched per commit and the gate order all follow the block
exactly.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created at `2621bbe2e` |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 3832 passed, 2 skipped |
| Gate 4 | done | fail_count 1, high_blockers_open only |
| Gate 5 | done | 88 |
| Gate 6 | done | prints nothing |
| Push | pending | reported in the session reply |

## Next

In order: Phase 1 rule 1 (`.agent/STOP`); the Open PR Gate; book round 1's verdict in the next
round's first commit; round 2: the steering-note route.

Operator questions open: 3
Open findings: 88

## For the operator, in plain sentences

This round claims the feature that makes sure everything the edition needs is already published,
with nothing else answered outside what is written down. It records what the interface already
offers today, and then closes two small gaps in the written description rather than in the
running system: it names the one local channel that still answers something outside the
published list, and it proves that a job's log lines come back in the order they really
happened, not the order they happened to land on disk. Nothing that runs a command changed this
round; only the written description and its tests did. Three questions are still waiting for a
decision, each with a recommendation already attached.
