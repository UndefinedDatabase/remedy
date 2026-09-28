# Handback — F038, round 10: book round 9, resolve R-1093, register and repair R-1094, the cockpit's chat route lands

## Session

SESSION 3 of feature F038 · round 10 · rounds so far 10. This session ran round 10 only,
continuing directly after round 9's handback. Context self-assessment: a comfortable margin of
context remained at the end of the round; the work was not near its limit.

For the operator, in plain words: the cockpit can now ask the same grounded question or type the
same request the command line already can, through a read-only route the panel will call next
round — `GET /api/jobs/<job_id>/chat?text=<line>&task=<task id>` runs one chat turn and answers it
in the exact same shape `remedy chat ask --json` already gives, so both doors show the same
citations, the same unsupported marks and the same card. The route itself never sends anything;
confirming a card still goes through the one write door the cockpit has always had. Six small test
gaps the previous round's review found — two live sessions for one job, two cards sent in a row to
one cockpit, the evidence numbering, the text form's evidence lines, an unsupported sentence, and a
padded `--task` — are all pinned now.

## Range

Review of `c1c3f636a`..`HEAD` (the commit that writes this file). Six commits: C1a, C1b, C2, C3,
C4, C5.

## Commits

### 406864100 F038 R10 C1a: copy round 10 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r10-block.md | 277/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f038-r10-plan.md | 29/0 | the plan payload, copied verbatim by `shutil.copyfile` |

### 9b4d5af08 F038 R10 C1b: copy round 10 records and landed diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r10-records.diff | 62/0 | the records payload, copied verbatim |
| .agent/authored/f038-r10-landed.diff | 10/0 | the landed-line payload, copied verbatim |

### af4f50c18 F038 R10 C2: book round 9, resolve R-1093, register R-1094, record DECISION F038 D11
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 40/0 | `git apply records.diff`: DECISION F038 D11 |
| .agent/live_review.md | 6/0 | `git apply records.diff`: round 9's Gate entry, R-1093's `Done:`, R-1094's registration |
| .agent/plan.md | 7/7 | rewritten to plan.md payload: round 10's goal and next steps |

### 43f48e7cf F038 R10 C3: answer one chat turn over the cockpit's read route
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_turn.py | 36/0 | S2: `chat_turn_view`, the one wire shape both doors give |
| apps/cli/commands/chat_cmd.py | 14/21 | S3: `remedy chat ask --json` now emits `chat_turn_view(turn)`; `_send_chat_card` is handed the whole turn |
| packages/orchestration/ui_server.py | 22/0 | S4: `_build_chat_turn_json` and the `chat` branch of `do_GET` |

(measured: `git show 43f48e7cf --numstat` reads `36 0`, `14 21`, `22 0` respectively — no insertion
count was expected by the block for C3, per WHAT TO REPORT.)

### ca1fbd4fe F038 R10 C4: test the chat route and repair R-1094
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_chat_route.py | 166/0 | NEW FILE, S5's TESTS section: 9 tests over the route |
| tests/cli/test_chat_ask.py | 69/0 | S1: 4 new tests — two live sessions, two cards to one cockpit, text/json evidence parity, a padded `--task` |
| tests/orchestration/test_chat_turn.py | 30/0 | S1: `test_chat_turn_view_numbers_evidence_and_marks_each_sentences_support` |
| tests/ui_server/test_command_channel.py | 1/0 | S5: the chat path added to `_walkable_paths` |
| .agent/live_review.md | 2/0 | `git apply landed.diff`: the `Landed: R-1094 —` line |
| .agent/authored/f038-r10-mutations.py | 158/0 | the G5 mutation tool, saved as its own commit per the block |

(measured: `git show ca1fbd4fe --numstat` reads `166 0`, `69 0`, `30 0`, `1 0`, `2 0`, `158 0` —
no insertion count was expected by the block for C4 either; total commit insertions 426, under the
500-line cap.)

### (this commit) F038 R10 C5: rewrite handoff for round 10
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, the session-end handback G6 orders |

## External actions

- `git worktree add --detach .remedy-wt/f038-r10-mut ca1fbd4fe` — created the G5 mutation worktree.
- `git worktree remove --force .remedy-wt/f038-r10-mut` — removed it after the tool ran; `git
  worktree prune` afterward.
- `git worktree list | wc -l` read 70 before and after, matching step 4's reading.
- `git push origin feature/f038-grounded-chat` after this commit — reported in the worker's reply.
- No PR created, edited or merged. No `gh pr` command run except the G6 open-PR read.

## Verification

BEFORE ANYTHING ELSE: `.agent/STOP` absent (`ls` exit 2, No such file or directory); `pwd` read
`/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current` read
`feature/f038-grounded-chat`; `git log --oneline -1` read `c1c3f636a`; block bytes measured 277
lines / sha256 `543f4db61745817f7382cf61a784e0996e7409e94c0bef3e045786948c9f7fb8`, both matching
the delegation message; `git worktree list | wc -l` read 70.

PAYLOADS: all three measured line count, byte count and sha256 exactly matching the PAYLOADS
table before use — `records.diff` 62 / 10502 /
`eea4a65fc9a5e2e64372bb027aafe50db944237191e02d334ca721daf3c13eb5`; `plan.md` 29 / 971 /
`2e291954bb13be542e2e0180ad9d1ae8e7795c17dda14f1e6a876322834b68ff`; `landed.diff` 10 / 2507 /
`3621f6841a99ebdab8dcf6e99e4f79ae87dc65a9f8d2140dc3b85d94b8b28e4a`.

G1 TRANSPORT: each `.agent/authored/f038-r10-*` copy, read with `git show <commit>:<path>`, compared
byte-identical (Python `==` over the raw bytes) against its source: block copy vs
`.remedy-wt/f038-r10/block.md` — True; plan copy vs the plan payload — True; records-diff copy vs
its payload — True; landed-diff copy vs its payload — True.

G2 THE RECORDS: sha256 at the named commit, read with `git show <commit>:<path>`, against the
reviewer's reading:
- C2 `.agent/decisions.md`: 2410035 bytes, sha256
  `d0c1611cfffb33f18d1268a6693b36a5827228fde2b9aeac595669bdc0129b08` — MATCH.
- C2 `.agent/live_review.md`: 339555 bytes, sha256
  `28651e704757f6cda3fdd3c5cd70059a7dfcd48e1d98485c49d528c6b257232c` — MATCH.
- C2 `.agent/plan.md`: 971 bytes, sha256
  `2e291954bb13be542e2e0180ad9d1ae8e7795c17dda14f1e6a876322834b68ff` — MATCH.
- C4 `.agent/live_review.md`: 339924 bytes, sha256
  `5a7565821894795a6987e52c5424106237e79c7ed9e4a22e965aa5bde31d5c92` — MATCH.
`open_finding_ids` (`scripts/rotate_live_review.py`) over the ledger's TEXT at C2 and at C4:
`['R-1094']` at both, matching the reviewer's reading. `git diff --name-only 9b4d5af08 af4f50c18`
(C1b..C2) named exactly: `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`.

G3 THE CODE:
```
$ python3 -m ruff check apps/cli/commands/chat_cmd.py packages/orchestration/chat_turn.py \
  packages/orchestration/ui_server.py tests/ui_server/test_chat_route.py \
  tests/ui_server/test_command_channel.py tests/cli/test_chat_ask.py \
  tests/orchestration/test_chat_turn.py .agent/authored/f038-r10-mutations.py
All checks passed!
REAL_EXIT=0
```
`chat_turn_view`, `_build_chat_turn_json` and the `chat` branch of `do_GET`, quoted from
`git show 43f48e7cf`, are reproduced verbatim in the worker's reply (see the reply's G3 section).

G4 THE TESTS — the block's selection, run serially in the primary checkout at C4:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <selection> 2>&1 | tail -12; \
  echo "REAL_EXIT=${PIPESTATUS[0]}"'
1259 passed in 144.72s (0:02:24)
REAL_EXIT=0
```
No `SKIPPED` line appeared (matching the reviewer's own primary-checkout reading of "1245 passed
with no skip"). `--collect-only -q` node counts at C4: `tests/ui_server/test_chat_route.py` 9 (NEW
FILE), `tests/cli/test_chat_ask.py` 17 (was 13, +4), `tests/orchestration/test_chat_turn.py` 10
(was 9, +1). Accounting for 1259 vs the reviewer's primary-checkout baseline of 1245: 9 + 4 + 1 =
14 new nodes; 1245 + 14 = 1259, exact. Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}
```
all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — whole tool output, `git worktree add --detach .remedy-wt/f038-r10-mut
ca1fbd4fe` then `python3 -B .agent/authored/f038-r10-mutations.py .../f038-r10-mut`:
```
control (before): exit=0 failed=0 nodes=[]
m1 (ui_server.py) a blank text runs a turn: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m2 (ui_server.py) a ChatTurnError is not caught: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m3 (ui_server.py) the task is dropped: exit=1 failed=5 nodes=[...5 nodes...] restored byte-identical: True
m4 (ui_server.py) the task is not stripped: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m5 (chat_turn.py) the view numbers evidence from 0: exit=1 failed=3 nodes=[...3 nodes...] restored byte-identical: True
m6 (chat_turn.py) every sentence is reported supported: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m7 (chat_turn.py) a card's args come back empty: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m8 (ui.py) the lookup returns the oldest session: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m9 (chat_cmd.py) every send uses one fixed nonce: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m10 (chat_cmd.py) the text form's evidence lines are dropped: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m11 (chat_cmd.py) --task is not stripped: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
m12 (chat_cmd.py) the --json answer's question is blanked: exit=1 failed=1 nodes=[...1 node...] restored byte-identical: True
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
(the worker's reply carries every node id in full). Every one of the twelve mutations was caught,
at least one failing node each, every restore byte-identical, both controls exit 0. Then
`git worktree remove --force .remedy-wt/f038-r10-mut`, `git worktree prune`, `git worktree list |
wc -l` read 70, matching step 4's reading.

## Authored-text proofs

The block itself and the plan, records-diff and landed-diff payloads were each copied verbatim
(`shutil.copyfile` for the block/plan, `git apply` for the two diffs) and compared byte-identical
against their sources under G1 above — all four MATCH. `.agent/plan.md` and the two ledger applies
(records.diff at C2, landed.diff at C4) were verified sha256-identical to the reviewer's own
simulation readings under G2 above — all four MATCH. No other reviewer-authored text was applied
this round (S1 to S5 are the worker's own code and tests against the block's specification, not
reviewer-authored payloads).

## Deviations & assumptions

None. Every commit, subject, expected insertion count and gate reading matched the block; no
payload was retyped or edited; the touched-path set (`git diff --name-only c1c3f636a` at the tip
after C5, reported in the worker's reply) equals constraint 3's list plus `.agent/handoff.md`
exactly, with no other file under `apps/`, `packages/` or `docs/` touched.

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 10. Then T003's next
part: the cockpit's chat panel, with citation chips, unsupported marks and cards confirmed through
the write door, and its DOM audit. Open findings in the ledger: 1, R-1094, landed and awaiting the
review. Operator questions open: 1.
