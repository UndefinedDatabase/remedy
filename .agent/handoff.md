# Handback — F038, round 9: book round 8, resolve R-1092, register and repair R-1093, `remedy chat ask` lands

## Session

SESSION 3 of feature F038 · round 9 · rounds so far 9. This session ran round 9 only, delegated
after the operator lifted `.agent/STOP`. Context self-assessment: a comfortable margin of context
remained at the end of the round; the work was not near its limit.

For the operator, in plain words: the chat now has a command line. `remedy chat ask <job_id>
"<text>"` asks the same grounded question or types the same request the cockpit's own turn reads —
a question comes back with its scope, its checked answer and its numbered sources; a request comes
back as a card, and that card is sent through the job's own running cockpit only once it is
complete and you say yes, either with `--yes` or by typing `y` at the prompt. Nothing is sent
without your say-so, and nothing is sent at all unless a cockpit is actually running for that job.
Two small test gaps the previous round's review found are both closed now: the intent parser's two
blind spots are pinned, and the one that let a handed-in answer function be silently dropped is
pinned too.

## Range

Review of `7627663b7`..`HEAD` (the commit that writes this file). Six commits: C1a, C1b, C2, C3,
C4, C5.

## Commits

### 81bfa006d F038 R9 C1a: copy round 9 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r9-block.md | 288/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f038-r9-plan.md | 29/0 | the plan payload, copied verbatim by `shutil.copyfile` |

### d016127e0 F038 R9 C1b: copy round 9 records and landed diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r9-records.diff | 60/0 | the records payload, copied verbatim |
| .agent/authored/f038-r9-landed.diff | 10/0 | the landed-line payload, copied verbatim |

### c6f0085d9 F038 R9 C2: book round 8, resolve R-1092, register R-1093, record DECISION F038 D10
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 38/0 | `git apply records.diff`: DECISION F038 D10 |
| .agent/live_review.md | 6/0 | `git apply records.diff`: round 8's Gate entry, R-1092's `Done:`, R-1093's registration |
| .agent/plan.md | 7/7 | rewritten to plan.md payload: round 9's goal and next steps |

### fc7493187 F038 R9 C3: add remedy chat ask, one chat turn on the command line
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 26/0 | S3: the `chat.ask` catalog entry |
| apps/cli/commands/chat_cmd.py | 158/0 | S4-S6: `_cmd_chat_ask`, its answer and card renderers, the module docstring paragraph |
| apps/cli/commands/ui.py | 18/0 | S2: `live_ui_session_for_job`, the read-only registry lookup |
| docs/guides/exit-codes.md | 1/0 | S7: the `remedy chat ask` row |
| tests/orchestration/import_reachability_allowlist.txt | 6/0 | S7: the six `chat_*` modules now reachable from `chat_cmd.py`'s imports |
| tests/test_no_orphan_modules.py | 0/6 | S7: `chat_door.py` and `chat_turn.py` removed from `ALLOWED_UNWIRED` — `chat_cmd.py` wires them |

### d0cbeec86 F038 R9 C4: test remedy chat ask and repair R-1093
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_turn.py | 22/0 | S1: `test_a_handed_in_answer_call_fn_is_used_and_checked`, R-1093's repair |
| tests/cli/test_chat_ask.py | 238/0 | NEW FILE: 13 tests over the TESTS section's list |
| .agent/live_review.md | 2/0 | `git apply landed.diff`: the `Landed: R-1093 —` line |
| .agent/authored/f038-r9-mutations.py | 159/0 | the G5 mutation tool, saved as its own commit per the block |

### (this commit) F038 R9 C5: rewrite handoff for round 9
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, the session-end handback G6 orders |

## External actions

- `git worktree add --detach .remedy-wt/f038-r9-mut d0cbeec86` — created the G5 mutation worktree.
- `git worktree remove --force .remedy-wt/f038-r9-mut` — removed it after the tool ran.
- `git worktree prune` — pruned; `git worktree list | wc -l` read 68 before and after, matching
  step 4's reading.
- `git push origin feature/f038-grounded-chat` after this commit — reported in the worker's reply.
- No PR created, edited or merged. No `gh pr` command run except the G6 open-PR read.

## Verification

BEFORE ANYTHING ELSE: `.agent/STOP` absent (`ls` exit 2, No such file or directory); `pwd` read
`/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current` read
`feature/f038-grounded-chat`; `git log --oneline -1` read `7627663b7`; block bytes measured 288
lines / sha256 `c92089bb7c346f6fe4026308f14c52703d0cd0654573fd9c1976c3476e5c8818`, both matching
the delegation message; `git worktree list | wc -l` read 68.

PAYLOADS: all three measured line count, byte count and sha256 exactly matching the PAYLOADS
table before use — `records.diff` 60 / 9723 /
`5f5de100d2694da50402517b6b6b48c71c7d7f305bf5fd64f296a1b3a0bd1cb9`; `plan.md` 29 / 968 /
`4343ab72f525a060e53bfb517d52504b16fb982803abda5243c13f36a7c486e3`; `landed.diff` 10 / 2121 /
`caaea37932ac90fb6fca2e669685f81c45dab629cf17a3b020bf71f173286346`.

G1 TRANSPORT: each `.agent/authored/f038-r9-*` copy, read with `git show <commit>:<path>`, compared
byte-identical (Python `==` over the raw bytes) against its source: block copy vs
`.remedy-wt/f038-r9/block.md` — True; plan copy vs the plan payload — True; records-diff copy vs
its payload — True; landed-diff copy vs its payload — True.

G2 THE RECORDS: sha256 at the named commit, read with `git show <commit>:<path>`, against the
reviewer's reading:
- C2 `.agent/decisions.md`: 2406736 bytes, sha256
  `d5a308fc82bd2fbe14a2308f373fbd22eff8130ce578d1d8aa39fbada7f711a7` — MATCH.
- C2 `.agent/live_review.md`: 334333 bytes, sha256
  `03ab5768a1953e50dff041b574af6a1706482000f22151133c7a42b3da76356b` — MATCH.
- C2 `.agent/plan.md`: 968 bytes, sha256
  `4343ab72f525a060e53bfb517d52504b16fb982803abda5243c13f36a7c486e3` — MATCH.
- C4 `.agent/live_review.md`: 334559 bytes, sha256
  `a6a84ced9ac8f2ae3a9db612fa860e95fb5d267fe9bbd667add1172632ad8e67` — MATCH.
`open_finding_ids` (`scripts/rotate_live_review.py`) over the ledger's TEXT at C2 and at C4:
`['R-1093']` at both, matching the reviewer's reading. `git diff --name-only d016127e0 c6f0085d9`
(C1b..C2) named exactly: `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`.

G3 THE CODE:
```
$ python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/chat_cmd.py \
  apps/cli/commands/ui.py tests/cli/test_chat_ask.py tests/orchestration/test_chat_turn.py \
  tests/test_no_orphan_modules.py
All checks passed!
REAL_EXIT=0
```
`_cmd_chat_ask`, `live_ui_session_for_job` and the `chat.ask` catalog entry, quoted from
`git show fc7493187`, are reproduced verbatim in the worker's reply (too long to duplicate a second
time here; see the reply's G3 section). `git show fc7493187 -- \
tests/orchestration/import_reachability_allowlist.txt` shows the six-line insertion between
`change_set` and `checkpoints`, and nothing else changed in that file.

G4 THE TESTS — the block's selection, run serially in the primary checkout at C4:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <selection> 2>&1 | tail -12; \
  echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [6] tests/regression/test_named_bugs.py (F252 quarantine, six lines)
SKIPPED [3] tests/orchestration/test_model_routing.py:455 (covered by the violating fixture above)
3654 passed, 9 skipped, 1 warning in 554.05s (0:09:14)
REAL_EXIT=0
```
Accounting for 3654 vs the reviewer's primary-checkout baseline of 3637: `tests/cli/test_chat_ask.py`
collects 13 nodes (new file), `tests/orchestration/test_chat_turn.py` collects 9 (was 8, +1 for
S1's repair) — 14 new nodes from these two files — plus the three catalog-parametrized cases the
new `chat.ask` entry adds: `test_declared_codes_are_the_floor_plus_named_codes[chat.ask]`,
`test_declared_codes_equal_the_codes_the_handler_reaches[chat.ask]` (both
`tests/cli/test_exit_codes.py`) and
`TestInvalidArgumentSweep::test_an_unrecognised_option_answers_the_envelope[chat.ask]`
(`tests/cli/test_json_contract.py`) — confirmed present and collected by name. 3637 + 14 + 3 =
3654, exact. Skip count (9) and the skip reasons match the reviewer's primary-checkout reading
unchanged. Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}
```
all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — whole tool output, `git worktree add --detach .remedy-wt/f038-r9-mut d0cbeec86`
then `python3 -B .agent/authored/f038-r9-mutations.py .../f038-r9-mut`:
```
control (before): exit=0 failed=0 nodes=[]
r1 --yes is ignored: exit=1 failed=5 nodes=[...5 nodes...] restored byte-identical: True
r2 a card is sent with neither --yes nor a terminal: exit=1 failed=1 nodes=[...] restored byte-identical: True
r3 a card that is not confirmable is sent: exit=1 failed=1 nodes=[...] restored byte-identical: True
r4 an answer other than y sends: exit=1 failed=1 nodes=[...] restored byte-identical: True
r5 (ui.py) the lookup ignores the job id: exit=1 failed=1 nodes=[...] restored byte-identical: True
r6 (ui.py) the lookup ignores a dead pid: exit=1 failed=1 nodes=[...] restored byte-identical: True
r7 a refused card exits 0: exit=1 failed=1 nodes=[...] restored byte-identical: True
r8 no cockpit exits 0: exit=1 failed=3 nodes=[...3 nodes...] restored byte-identical: True
r9 a ChatTurnError is not caught: exit=1 failed=1 nodes=[...] restored byte-identical: True
r10 (chat_turn.py) a handed-in answer_call_fn is dropped (R-1093): exit=1 failed=1 nodes=[...] restored byte-identical: True
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
(the worker's reply carries every node id in full). Every one of the ten mutations was caught, at
least one failing node each, every restore byte-identical, both controls exit 0. Then
`git worktree remove --force .remedy-wt/f038-r9-mut`, `git worktree prune`, `git worktree list |
wc -l` read 68, matching step 4's reading.

## Authored-text proofs

The block itself and the plan, records-diff and landed-diff payloads were each copied verbatim
(`shutil.copyfile` for the block/plan, `git apply` for the two diffs) and compared byte-identical
against their sources under G1 above — all four MATCH. `.agent/plan.md` and the two ledger applies
(records.diff at C2, landed.diff at C4) were verified sha256-identical to the reviewer's own
simulation readings under G2 above — all four MATCH. No other reviewer-authored text was applied
this round (S1 to S7 are the worker's own code and tests against the block's specification, not
reviewer-authored payloads).

## Deviations & assumptions

None. Every commit, subject, expected insertion count and gate reading matched the block; no
payload was retyped or edited; the touched-path set (`git diff --name-only 7627663b7` at the tip
after C5, reported in the worker's reply) equals constraint 3's list plus `.agent/handoff.md`
exactly, with no other file under `apps/`, `packages/` or `docs/` touched.

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 9. Then T003's next
part: the cockpit panel asks the same chat turn through a route and confirms a card through the
write door. Open findings in the ledger: 1, R-1093, landed and awaiting the review. Operator
questions open: 1.
