# Handback — F038, round 11: book round 10, resolve R-1094, register and repair R-1095, the evidence panel's Chat tab lands

## Session

SESSION 3 of feature F038 · round 11 · rounds so far 11. This session ran round 11 only,
continuing directly after round 10's handback. Context self-assessment: a comfortable margin of
context remained at the end of the round; the work was not near its limit.

For the operator, in plain words: the evidence panel's Chat tab is no longer a placeholder. A line
asks the chat route about the focused run's task, or about the whole project when "Ask about the
whole project" is ticked; an answer shows a scope chip, every sentence with numbered chips linking
to its evidence items, or a visible dashed "unsupported" mark; a card shows its title and lines
with a Confirm button that sends it through the same write door the cockpit has always had, only
while the card is complete and has not already been sent. A vitest DOM audit renders the real
component with `react-dom/server` and checks every mark. R-1095, last round's finding that
`chat_turn_view`'s six keys had no test naming them, is repaired with two literal-dictionary
comparisons.

## Range

Review of `9c7f5fad7`..`HEAD` (the commit that writes this file). Nine commits: C1a, C1b, C2, C3a
(1/2), C3a (2/2), C3b, C4 (1/2), C4 (2/2), C5 — two more than the block's seven because C3a and C4
each had to split under the 500-line insertion cap (constraint 2); see Deviations below.

## Commits

### b818956ba F038 R11 C1a: copy round 11 block, plan and assumption payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r11-block.md | 299/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f038-r11-plan.md | 29/0 | the plan payload, copied verbatim |
| .agent/authored/f038-r11-assumption_line.md | 1/0 | the assumption-row payload, copied verbatim |

(measured: `git show b818956ba --numstat` reads `1 0`, `299 0`, `29 0` — total 329, exactly the
block's own line count (299) plus 30, as C1a's line ordered.)

### 29ea11664 F038 R11 C1b: copy round 11 records and landed diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r11-landed.diff | 10/0 | the landed-line payload, copied verbatim |
| .agent/authored/f038-r11-records.diff | 66/0 | the records payload, copied verbatim |

(measured: total 76 insertions, exactly the block's expected reading.)

### d462b6966 F038 R11 C2: book round 10, resolve R-1094, register R-1095, record DECISION F038 D12
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 35/0 | `git apply records.diff`: DECISION F038 D12 |
| .agent/live_review.md | 6/0 | `git apply records.diff`: round 10's Gate entry, R-1094's `Done:`, R-1095's registration |
| .agent/plan.md | 7/7 | rewritten to plan.md payload: round 11's goal and next steps |
| .agent/prose_slips.md | 1/0 | `git apply records.diff`: the one prose-slip line |

(measured: `35 0`, `6 0`, `7 7`, `1 0` — exactly the block's G2 table.)

### 7aa360fee F038 R11 C3a (1/2): decode, mark and send a chat turn in the browser
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/chatTurn.ts | 332/0 | NEW FILE, S2: the pure chat-turn module — decoder, path, marks, card builder and send flow |
| apps/ui/src/api/remedyApi.ts | 24/0 | S2: `loadChatTurn`, shaped as `loadTourView` |

(measured: `332 0`, `24 0` — 356 insertions; no count was expected by the block for C3a beyond
"none is expected for C3a to C4 — report what you measure".)

### ea5add6a5 F038 R11 C3a (2/2): test the pure chat-turn module
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/chatTurn.test.ts | 237/0 | NEW FILE, THE TESTS: the decoder, the path, the two sentence helpers, the send request and `sendChatCard` |

(measured: 237 insertions. Split from C3a per constraint 2: C3a (1/2) + this part would have been
593 insertions, over the 500-line cap. See Deviations.)

### 3c1f292d0 F038 R11 C3b: the evidence panel's chat tab, with chips, marks and cards
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/EvidenceChatTab.tsx | 199/0 | NEW FILE, S3: `ChatTurnBlock` (pure) and `EvidenceChatTab` |
| apps/ui/src/components/graph/EvidenceChatTab.module.css | 158/0 | NEW FILE, S3: the tab's `--remedy-*` tokens only |
| apps/ui/src/components/graph/EvidencePanel.tsx | 3/2 | S4: the chat line becomes `<EvidenceChatTab .../>`, its import added |
| apps/ui/src/components/graph/evidencePanel.ts | 3/8 | S4: `EVIDENCE_CHAT_NOT_YET` deleted, header comment updated |
| apps/ui/src/components/graph/evidencePanel.test.ts | 1/7 | S4: its import and the one test pinning it deleted |
| tests/ui_contracts/test_evidence_panel_contract.py | 2/1 | S4: the one assertion naming it replaced by one asserting the new line |
| docs/ui/design_reference/assumption_log.md | 1/0 | S5: the assumption-row payload appended byte for byte |

(measured: total 367 insertions, 18 deletions; no count was expected by the block for C3b either.)

### 525b80209 F038 R11 C4 (1/2): test the chat tab and repair R-1095
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_turn.py | 87/3 | S1: two literal-dict tests (a hand-built answer, a hand-built card) plus the imports they need |
| tests/ui_contracts/test_chat_citations.py | 55/0 | NEW FILE, THE TESTS: the panel mounts the tab, no `fetch(`, the two doors, `CHAT_NOT_IN_EVIDENCE` parity, every key read by name |
| apps/ui/src/components/graph/evidenceChatAudit.test.ts | 128/0 | NEW FILE, THE DOM AUDIT: `ChatTurnBlock` via `renderToStaticMarkup` |
| .agent/live_review.md | 2/0 | `git apply landed.diff`: the `Landed: R-1095 —` line |

(measured: 272 insertions. Split from C4 per constraint 2: with the mutation tool this part would
have been 648 insertions. See Deviations.)

### 1bc00a302 F038 R11 C4 (2/2): save the round's mutation tool for G5
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r11-mutations.py | 376/0 | NEW FILE, G5's tool: 10 vitest mutations, 8 pytest mutations, two runners, two controls |

(measured: 376 insertions.)

### (this commit) F038 R11 C5: rewrite handoff for round 11
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, the session-end handback G6 orders |

## External actions

- `git worktree add --detach .remedy-wt/f038-r11-mut 1bc00a302` — created the G5 mutation worktree
  at C4's tip (the tip after C4 (2/2), since C4 was split).
- `git worktree remove --force .remedy-wt/f038-r11-mut` — removed it after the tool ran; `git
  worktree prune` afterward.
- `git worktree list | wc -l` read 72 before and after, matching step 4's reading.
- `git push origin feature/f038-grounded-chat` after this commit — reported in the worker's reply.
- No PR created, edited or merged. No `gh pr` command run except the G6 open-PR read.

## Verification

BEFORE ANYTHING ELSE: `.agent/STOP` absent (`ls` exit 2, No such file or directory); `pwd` read
`/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current` read
`feature/f038-grounded-chat`; `git log --oneline -1` read `9c7f5fad7`; block bytes measured 299
lines / sha256 `c3d5cc4acf3307b88e1dd2d3a528ca07a0f821ea45984943276a2eedd667b085`, both matching the
delegation message exactly; `git worktree list | wc -l` read 72.

PAYLOADS: all four measured line count, byte count and sha256 exactly matching the PAYLOADS table
before use — `records.diff` 66 / 11701 /
`852ab5380b11f9c10fff9850355d31b580595788e4dab692ddc5da04bad9663a`; `plan.md` 29 / 944 /
`fa4a665b38e00af292b2fd638fa494d46220a32a366887b11883693bd70cd3b0`; `landed.diff` 10 / 2557 /
`e92df1b3bb0ac537759769b6a735dfee9ee033ce1e087485f0eb00440d0d5b31`; `assumption_line.md` 1 / 1053 /
`645f581584453b7679ec10b3ba6bc02bad3069878ad554bd280a1e425d046fa9`.

G1 TRANSPORT: each `.agent/authored/f038-r11-*` copy, read with `git show <commit>:<path>`,
compared byte-identical (Python `==` over raw bytes) against its source: block copy vs
`.remedy-wt/f038-r11/block.md` — True; plan copy vs the plan payload — True; assumption-line copy
vs the assumption payload — True; records-diff copy vs its payload — True; landed-diff copy vs its
payload — True. `docs/ui/design_reference/assumption_log.md` at C3b (`3c1f292d0`) equals its bytes
at `9c7f5fad7` followed by `assumption_line.md`'s bytes — True.

G2 THE RECORDS: sha256 at the named commit, read with `git show <commit>:<path>`, against the
reviewer's reading:
- C2 `.agent/decisions.md`: 2413085 bytes, sha256
  `e8041d41ed46ddde35c6126f33b0b18e9caac36a19f7b8b6f55bd45be3a4857c` — MATCH.
- C2 `.agent/live_review.md`: 344554 bytes, sha256
  `0b46aef726922f00c580374ccee73b7fde0ccf54ad8c85085f19e559ee7533d7` — MATCH.
- C2 `.agent/prose_slips.md`: 376658 bytes, sha256
  `6ba91163114a4ae2e881afd928669566f7749dd89ae8c97d6ccfdd1976cb3313` — MATCH.
- C2 `.agent/plan.md`: 944 bytes, sha256
  `fa4a665b38e00af292b2fd638fa494d46220a32a366887b11883693bd70cd3b0` — MATCH.
- C4 `.agent/live_review.md` (read at `525b80209`, C4 (1/2), which carries `git apply
  landed.diff`): 344808 bytes, sha256
  `e62a2b54cc6e0e1e823dcf366a7b5f678cb04b583353e4452ed5ee541cd7de4a` — MATCH.
`open_finding_ids` (`scripts/rotate_live_review.py`) over the ledger's TEXT at C2 (`d462b6966`) and
at C4 (`525b80209`): `['R-1095']` at both, matching the reviewer's reading. `git diff --name-only
29ea11664 d462b6966` (C1b..C2) named exactly: `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md`.

G3 THE CODE:
```
$ python3 -m ruff check tests/ui_contracts/test_chat_citations.py \
  tests/ui_contracts/test_evidence_panel_contract.py tests/orchestration/test_chat_turn.py \
  .agent/authored/f038-r11-mutations.py
All checks passed!
REAL_EXIT=0
```
`decodeChatTurn`, `chatSentenceText`, `chatSentenceMark` and `buildChatCardSendRequest`, quoted
from `git show 7aa360fee` (C3a (1/2)), and `ChatTurnBlock` and the EvidencePanel line, quoted from
`git show 3c1f292d0` (C3b), are reproduced verbatim in the worker's reply (see the reply's G3
section).

G4 THE TESTS — the block's selection, run serially in the primary checkout at C4 (`1bc00a302`):
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <selection> 2>&1 | tail -60; \
  echo "REAL_EXIT=${PIPESTATUS[0]}"'
1561 passed, 5 skipped in 94.93s (0:01:34)
REAL_EXIT=0
```
Every `SKIPPED` line: `tests/ui_contracts/test_graph_architecture.py:441` and `:484`,
`tests/ui_contracts/test_ux_quality.py:507` and `:543` (all four D3 quarantine, F252), and
`tests/test_agent_tooling.py:43` (D12 quarantine, F252) — the same five the block's own baseline
names. `--collect-only -q` node counts at C4: `tests/ui_contracts/test_chat_citations.py` 4 (NEW
FILE), `tests/orchestration/test_chat_turn.py` 12 (was 10 at `9c7f5fad7`, +2). Accounting for 1561
vs the block's reviewer-baseline reading of 1555 passed: 4 + 2 = 6 new nodes; 1555 + 6 = 1561,
exact. Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}
```
all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — whole tool output, `git worktree add --detach .remedy-wt/f038-r11-mut
1bc00a302` then `python3 -B .agent/authored/f038-r11-mutations.py .../f038-r11-mut` (full output,
including every failing test name, is reproduced in the worker's reply's G5 section):
```
=== CONTROL (pre) — VITEST === exit=0 failed=0
=== CONTROL (pre) — PYTEST === exit=0 failed=0
v1..v10 (chatTurn.ts, EvidenceChatTab.tsx): each exit=1, failed>=1, restored=True
c1, c2 (chatTurn.ts, EvidencePanel.tsx): each exit=1, failed>=1, restored=True
p1..p6 (packages/orchestration/chat_turn.py): each exit=1, failed=1, restored=True
=== CONTROL (post) — VITEST === exit=0 failed=0
=== CONTROL (post) — PYTEST === exit=0 failed=0
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
All 18 mutations caught, at least one failing name each, every restore byte-identical, both
controls exit 0 pre and post. Then `git worktree remove --force .remedy-wt/f038-r11-mut`, `git
worktree prune`, `git worktree list | wc -l` read 72, matching step 4's reading.

## Authored-text proofs

The block itself and the plan, records-diff, landed-diff and assumption-line payloads were each
copied or applied verbatim (`shutil.copyfile` for the block/plan/assumption-line, `git apply` for
the two diffs) and compared byte-identical against their sources under G1 above — all five MATCH.
`.agent/plan.md` and the two ledger applies (records.diff at C2, landed.diff at C4 (1/2)) were
verified sha256-identical to the reviewer's own simulation readings under G2 above — all five
MATCH. No other reviewer-authored text was applied this round (S1 to S5 are the worker's own code
and tests against the block's specification, not reviewer-authored payloads).

## Deviations & assumptions

1. C3a was split into C3a (1/2) (production: `chatTurn.ts`, `remedyApi.ts`, 356 insertions) and
   C3a (2/2) (`chatTurn.test.ts`, 237 insertions), because the two together would have been 593
   insertions, over the 500-line cap (constraint 2). Both parts carry declared split messages
   naming each other.
2. C4 was split into C4 (1/2) (S1's repair, `test_chat_citations.py`,
   `evidenceChatAudit.test.ts`, `landed.diff`'s apply — 272 insertions) and C4 (2/2) (the mutation
   tool, 376 insertions), because the two together would have been 648 insertions, over the cap.
3. A grouping mistake, declared rather than amended (constraint 5): while splitting C3a I placed
   `chatTurn.test.ts` — one of the block's "three new test files" the block orders into C4 — into
   C3a (2/2) instead. Its CONTENT matches the block's THE TESTS section for `chatTurn.test.ts`
   exactly (the decoder, the path, both sentence helpers, the send request, `sendChatCard`'s two
   cases); only its commit GROUPING differs from the block's C3a/C4 split. No commit was amended
   or rewritten to fix this; it is declared here, in the C4 (1/2) commit message, and via the
   two-extra-commits note in Range above. The round's whole tracked path set (below) is unaffected.
4. No payload was retyped or edited; every payload's `git apply --check` was run before its real
   `git apply` and read exit 0 (see the worker's reply for both readings).

`git diff --name-only 9c7f5fad7` at the tip after C5 names exactly the round's whole tracked path
set (constraint 3's list, 23 paths, plus `.agent/handoff.md` itself — 24 total): no other file
under `apps/`, `packages/` or `docs/` was touched. The full list is reported in the worker's reply.

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3a (1/2) | deviated | split from C3a per constraint 2; see Deviations |
| C3a (2/2) | deviated | split from C3a per constraint 2, and grouped a C4 file in here by mistake; see Deviations |
| C3b | done | |
| C4 (1/2) | deviated | split from C4 per constraint 2; see Deviations |
| C4 (2/2) | deviated | split from C4 per constraint 2; see Deviations |
| C5 | done | this commit |
| G1 TRANSPORT | done | all readings MATCH |
| G2 THE RECORDS | done | all readings MATCH, open set `['R-1095']` at both commits |
| G3 THE CODE | done | ruff exit 0, every named function quoted in the reply |
| G4 THE TESTS | done | 1561 passed, 5 skipped, exit 0; integrity check 6/6 pass |
| G5 THE RED PROOFS | done | all 18 mutations caught, restored byte-identical, controls clean |

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 11. Then T003's
end-to-end proof: ask, a cited answer, a stop card confirmed, the job stopping with its audit
line; then closure. Open findings in the ledger: 1, R-1095, landed and awaiting the review.
Operator questions open: 1.
