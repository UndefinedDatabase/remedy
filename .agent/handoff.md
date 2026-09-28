# Handback — F038, round 6 (book round 5, record DECISION F038 D7, and send a confirmed
chat card through the cockpit's write door)

## Session

SESSION 2 of feature F038 · round 6 · rounds so far 6. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, both
payloads and the records diff before writing anything, read every named source file whole
(`chat_intent.py`, `is_safe_id` in `safe_points.py`, `COMMAND_CSRF_HEADER`,
`_handle_command_submission`, `_bearer_token_accepted` and `start_ui_server` in `ui_server.py`,
`AUDIT_FILENAME` in `command_audit.py`, `pause_requested` in `pause_control.py`,
`tests/ui_server/test_steer_task_door.py`, `tests/ui_server/server_start.py` and
`tests/test_no_orphan_modules.py`), verified every payload and every committed copy for real,
applied `records.diff`, wrote the new `chat_door.py` module from the specification, wrote 12
tests, wrote an 8-mutation red-proof tool, ran it for real in a disposable worktree, ran the
pinned serial test selection and the integrity check to completion, and ran every gate (G1–G5)
for real before writing this handback.

## Range

Review of `8b01ece36..HEAD` (`HEAD` is this handback's own commit, `F038 R6 C5`, on
`feature/f038-grounded-chat`).

## Commits

### b9ac83aa9 F038 R6 C1a: copy round 6 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r6-block.md | 271/0 | copy of the block, verified line count (271) and sha256 |
| .agent/authored/f038-r6-plan.md | 29/0 | copy of the reviewer's plan.md payload |

300 insertions total, exactly the block's own note: 271-line block + 29, under the 500-line cap.

### e2f5b6f93 F038 R6 C1b: copy round 6 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r6-records.diff | 56/0 | copy of the reviewer's records.diff payload |

Measured 56 insertions, exactly the block's expected reading.

### e57b06701 F038 R6 C2: book round 5 and record DECISION F038 D7
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 38/0 | `git apply records.diff` — appends DECISION F038 D7 |
| .agent/live_review.md | 2/0 | `git apply records.diff` — books round 5's Gate entry |
| .agent/plan.md | 7/7 | rewritten to plan.md payload by `shutil.copyfile` |

Measured numstat matches the block's table exactly: 38/0, 2/0, 7/7.

### 23d5920bf F038 R6 C3: send a confirmed chat card through the cockpit's write door
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_door.py | 86/0 | NEW FILE — S1 module docstring/imports/constants, S2 `ChatDoorAnswer`, S3 `send_card_through_door` (payload build, job id/port/token checks, one `HTTPConnection`, JSON answer), S4 no file opened or written |
| tests/test_no_orphan_modules.py | 3/3 | S5 — `ALLOWED_UNWIRED` entry for `chat_intent.py` replaced in place by the `chat_door.py` entry |

No insertion count was expected by the block for C3; measured 89 total (86 insertions, 3
insertions/3 deletions for the replaced entry), under the cap.

### 6e9100493 F038 R6 C4: test the door send, its refusals and its audit line
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_door.py | 163/0 | NEW FILE — 12 tests: audit absent before any send, an accepted pause with its exact audit line and `pause_requested`, a replayed nonce, a focused steer naming the task, an unfocused chat.send, a wrong token 403, an unconfirmable card raising with the audit still absent, and job_id/port(0)/port(70000)/port(True)/empty-token each raising with the audit still absent |
| .agent/authored/f038-r6-mutations.py | 148/0 | the G5 tool: 8 mutations (r1–r8) against `chat_door.py`, run with `-rf` against `tests/orchestration/test_chat_door.py` |

311 insertions total, under the 500-insertion cap.

### \<C5-sha\> F038 R6 C5: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r6-mut 6e9100493` — added the disposable G5
  worktree at C4. Outcome: `Preparing worktree (detached HEAD 6e9100493)`, exit 0.
- `python3 -B .agent/authored/f038-r6-mutations.py .../.remedy-wt/f038-r6-mut` — outcome: all 8
  mutations exit 1 with real failed counts (1–4) and real failing node ids, both controls exit
  0, `restored byte-identical: True`, `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove --force .remedy-wt/f038-r6-mut` — outcome: exit 0.
- `git worktree prune` — outcome: exit 0.
- `git push origin feature/f038-grounded-chat` — reported under G6 in the round reply (run
  after this file's own commit, so its outcome is reported there rather than tabled here, per
  the handback template's self-reference exception).

## Verification

### BEFORE ANYTHING ELSE
1. `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2. Absent.
2. `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty, exit 0.
   `git branch --show-current` → `feature/f038-grounded-chat`. `git log --oneline -1` →
   `8b01ece36 F038 R5 C5: rewrite handoff for round 5`.
3. Block bytes: measured line count 271, sha256
   `9d6c9c76571af82bee3213baab3c6702faa074b8066fccca339249a0ba7dd3b5`; both equal the two
   readings the delegation message stated.
4. `git worktree list | wc -l` → `62`.

### PAYLOADS
| file | measured lines | measured bytes | measured sha256 | matches table |
|---|---|---|---|---|
| records.diff | 56 | 11850 | ac3a728650801700d78140df6647bd36af764b32e09d23defd0fd6ef6f703e65 | yes |
| plan.md | 29 | 974 | 070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d | yes |

### G1 TRANSPORT
`git apply --check .remedy-wt/f038-r6-payloads/records.diff` → exit 0. Real `git apply` → exit 0.
Each `.agent/authored/f038-r6-*` copy compared byte-for-byte against its source, read back with
`git show <commit>:<path>`:
- `b9ac83aa9:.agent/authored/f038-r6-block.md` == `.remedy-wt/f038-r6/block.md` — MATCH (sha256
  `9d6c9c76571af82bee3213baab3c6702faa074b8066fccca339249a0ba7dd3b5` both).
- `b9ac83aa9:.agent/authored/f038-r6-plan.md` == `.remedy-wt/f038-r6-payloads/plan.md` — MATCH
  (sha256 `070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d` both).
- `e2f5b6f93:.agent/authored/f038-r6-records.diff` == `.remedy-wt/f038-r6-payloads/records.diff`
  — MATCH (sha256 `ac3a728650801700d78140df6647bd36af764b32e09d23defd0fd6ef6f703e65` both).

### G2 THE RECORDS
sha256 of each file read with `git show e57b06701:<path>`:
| path | bytes | sha256 | matches reviewer's reading |
|---|---|---|---|
| .agent/decisions.md | 2397195 | 00c4a36ebadb5091bb5ea9b910668eb3def49f8e6c7c2ff56f5e2605d66d68fd | yes |
| .agent/live_review.md | 323385 | 2e6b9eed1c6354f9a04842acfb10093e1a10d84ecd6b701a8d8e38269fd724e0 | yes |
| .agent/plan.md | 974 | 070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d | yes |

`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text at
`e57b06701` → `[]`, matching the reviewer's stated reading.

`git diff --name-only e2f5b6f93 e57b06701` →
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Names exactly the three paths of the table above.

### G3 THE CODE
`python3 -m ruff check packages/orchestration/chat_door.py
tests/orchestration/test_chat_door.py tests/test_no_orphan_modules.py` at C4 →
`All checks passed!`, exit 0.

Quoted from `git show 23d5920bf` (C3), the whole of `ChatDoorAnswer` and
`send_card_through_door`:

```python
@dataclass(frozen=True)
class ChatDoorAnswer:
    """What the write door answered: its HTTP status and its JSON body."""

    status: int
    body: dict[str, Any] = field(default_factory=dict)

    @property
    def accepted(self) -> bool:
        return self.status == 200


def send_card_through_door(
    card: ChatActionCard, *, job_id: str, client_nonce: str, port: int, token: str,
) -> ChatDoorAnswer:
    """Post one confirmed card to a running cockpit's write door (DECISION F038 D7).

    Every refusal below raises `ChatIntentError` BEFORE any connection opens, checked in this
    order: the card's own payload build first, since a card that is not confirmable or a nonce
    the door would refuse has no body to send at all; then the job id; then the port; then the
    token.
    """
    from packages.orchestration.ui_server import COMMAND_CSRF_HEADER

    body = card_command_payload(card, client_nonce=client_nonce)

    if not is_safe_id(job_id):
        raise ChatIntentError(f"job_id {job_id!r} is not a safe id")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        raise ChatIntentError(f"port {port!r} is not a usable port")
    if not token:
        raise ChatIntentError("token must not be empty")

    connection = http.client.HTTPConnection(
        CHAT_DOOR_HOST, port, timeout=CHAT_DOOR_TIMEOUT_S)
    try:
        connection.request(
            "POST", f"/api/jobs/{job_id}/commands",
            body=json.dumps(body),
            headers={
                "Authorization": f"Bearer {token}",
                COMMAND_CSRF_HEADER: token,
                "Content-Type": "application/json",
            },
        )
        response = connection.getresponse()
        status = response.status
        raw = response.read()
    finally:
        connection.close()

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        parsed = None
    response_body = parsed if isinstance(parsed, dict) else {}
    return ChatDoorAnswer(status=status, body=response_body)
```

### G4 THE TESTS
Serial run, at C4, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py 2>&1 | tail -9; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Output:
```
623 passed, 6 skipped in 74.40s (0:01:14)
REAL_EXIT=0
```
The six `SKIPPED` lines are exactly the F252 quarantine (`tests/regression/test_named_bugs.py`
lines 295, 312, 321, 383, 392, 399), matching the reviewer's own primary-checkout baseline.

Node count of `tests/orchestration/test_chat_door.py` by `--collect-only -q` at C4: 12 tests.

Accounting for the difference from the reviewer's base 611 passed at `8b01ece36`: this round
added exactly 12 new nodes in `tests/orchestration/test_chat_door.py` and touched no other test
file's collection. 611 + 12 = 623, exactly the measured total. The skip count is unchanged at 6
because the round added no new skip.

`python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0, exit 0.

### G5 THE RED PROOFS
`git worktree add --detach .remedy-wt/f038-r6-mut 6e9100493` → exit 0
(`Preparing worktree (detached HEAD 6e9100493)`).

```
control (unmutated, first): exit=0 failed=0 nodes=[]
r1 the CSRF header is not sent: exit=1 failed=4 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_pause_card_is_accepted_and_audited', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_the_same_card_and_nonce_sent_twice_replays', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_focused_note_is_a_steer_naming_the_task', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_an_unfocused_note_is_a_chat_send']
r2 the Authorization header is not sent: exit=1 failed=4 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_pause_card_is_accepted_and_audited', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_the_same_card_and_nonce_sent_twice_replays', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_focused_note_is_a_steer_naming_the_task', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_an_unfocused_note_is_a_chat_send']
r3 a card that is not confirmable is sent anyway, its body built without card_command_payload: exit=1 failed=1 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_an_unconfirmable_card_raises_and_writes_nothing']
r4 the job id is not checked: exit=1 failed=1 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_an_unsafe_job_id_raises_before_any_send']
r5 the port is not checked: exit=1 failed=3 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_port_of_zero_raises', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_port_of_70000_raises', 'tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_port_of_true_raises']
r6 the token is not checked: exit=1 failed=1 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_an_empty_token_raises']
r7 every answer reads as accepted: exit=1 failed=1 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_wrong_token_is_403_and_not_accepted']
r8 the nonce sent is a fixed string rather than the one given: exit=1 failed=1 nodes=['tests/orchestration/test_chat_door.py::TestChatDoorSend::test_a_pause_card_is_accepted_and_audited']
control (unmutated, last): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation caught with at least one real failing node; both unmutated controls read exit 0;
every mutation restored byte-identical. No mutation stayed green, so constraint 4's "add the
test that catches it" branch never fired.
`git worktree remove --force .remedy-wt/f038-r6-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list | wc -l` → `62`.

## Authored-text proofs

- `.agent/authored/f038-r6-block.md` (added at `b9ac83aa9`) == `.remedy-wt/f038-r6/block.md`,
  byte for byte (sha256 `9d6c9c76571af82bee3213baab3c6702faa074b8066fccca339249a0ba7dd3b5`
  both). MATCH.
- `.agent/authored/f038-r6-plan.md` (added at `b9ac83aa9`) ==
  `.remedy-wt/f038-r6-payloads/plan.md`, byte for byte (sha256
  `070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d` both). MATCH.
- `.agent/authored/f038-r6-records.diff` (added at `e2f5b6f93`) ==
  `.remedy-wt/f038-r6-payloads/records.diff`, byte for byte (sha256
  `ac3a728650801700d78140df6647bd36af764b32e09d23defd0fd6ef6f703e65` both). MATCH.
- `.agent/plan.md` after C2 (`e57b06701`) == `.remedy-wt/f038-r6-payloads/plan.md`, byte for
  byte (sha256 `070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d` both,
  confirmed under G2). MATCH.
- `records.diff` applied via `git apply` (not retyped); `.agent/decisions.md` and
  `.agent/live_review.md` after C2 match the reviewer's stated sha256 exactly (G2 table above).
  MATCH.

## Deviations & assumptions

1. No payload was repaired, edited or retyped. No existing test was touched, and no existing
   assertion in any file was changed. No file outside the round's tracked path set (constraint
   3) was touched — confirmed by `git diff --name-only 8b01ece36` at the branch tip before this
   commit (see below).
2. No product-code gate went red at any point this round. No mutation stayed green on its
   first application; the tool's 8 mutations all caught real behaviour changes on the first
   run, so no correction commit was needed.
3. No commit exceeded the block's ordered BUNDLE (C1a, C1b, C2, C3, C4, C5); all six commits
   landed in that exact order with no split and no extra commit.
4. Every commit's insertion count stayed well under the 500-insertion cap; no split was needed.

## Tracked path set (constraint 3)

`git diff --name-only 8b01ece36` at the branch tip before this commit:
```
.agent/authored/f038-r6-block.md
.agent/authored/f038-r6-mutations.py
.agent/authored/f038-r6-plan.md
.agent/authored/f038-r6-records.diff
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
packages/orchestration/chat_door.py
tests/orchestration/test_chat_door.py
tests/test_no_orphan_modules.py
```
Exactly the block's constraint-3 set (this file, `.agent/handoff.md`, is added by this commit
itself and so does not appear in a diff taken before it).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1 (STOP check) | done | |
| BEFORE ANYTHING ELSE 2 (repo state) | done | |
| BEFORE ANYTHING ELSE 3 (block bytes) | done | |
| BEFORE ANYTHING ELSE 4 (worktree count) | done | |
| PAYLOADS verification | done | |
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | all 8 mutations caught on the first run; no correction needed |
| G6 TREE AND PUSH | done | reported in the round reply, not tabled here (cannot precede this commit) |

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk. (2) The
review of round 6. (3) T002's last part: a model-written parse for the exposed commands a
sentence cannot fill, behind `chat.model_written`, off by default. Open-findings count: 0.
Operator-questions count: 1.
