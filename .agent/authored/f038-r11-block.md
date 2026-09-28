STEP F038 R11 — BOOK ROUND 10, RESOLVE R-1094, REGISTER AND REPAIR R-1095, THEN THE EVIDENCE PANEL'S CHAT TAB: answers with citation chips or the unsupported mark, cards confirmed through the write door, and the DOM chip audit

GOAL
Round 10 is reviewed PASS at `9c7f5fad`, with R-1094 resolved and one Low finding, R-1095. Book
them with one prose-slip line, record DECISION F038 D12, repair R-1095 with two tests, and replace
the evidence panel's chat placeholder with the grounded chat: a line asks the chat route about the
focused run's task, or the whole project; an answer shows every sentence with numbered chips
linking to its evidence items, or a visible unsupported mark; a card is sent through the write door
only when Confirm is pressed. A vitest DOM audit renders the real component and checks the marks.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS
SPECIFIED, NOT SLICED: you write the code and its tests yourself against S1 to S5 below. Only the
`.agent/` records and the assumption row travel as payloads. Read R-1095 and DECISION F038 D12 in
the records diff before you write code. Before you write anything, read whole:
`apps/ui/src/components/graph/EvidencePanel.tsx`, `evidencePanel.ts`, `evidencePanel.test.ts` and
`EvidencePanel.module.css` beside them; `apps/ui/src/api/resultTour.ts` (the decoder idiom you
follow); `loadTourView` in `apps/ui/src/api/remedyApi.ts`; `apps/ui/src/api/pauseSend.ts` and the
send chain it composes: `jobCommandsPath` and `isUsableCommandNonce` in `decisionAnswer.ts`,
`mintDecisionClientNonce` in `decisionNonce.ts`, `submitDecisionSendRequest` in
`decisionSubmit.ts`, `DecisionOutcomeMessage` in `decisionOutcome.ts`; `chat_turn_view` in
`packages/orchestration/chat_turn.py` and `CHAT_NOT_IN_EVIDENCE` in `chat_answer.py`;
`apps/ui/vitest.config.ts`; `tests/ui_contracts/test_evidence_panel_contract.py`,
`tests/ui_contracts/test_raw_colour_ratchet.py` and `tests/ui_contracts/test_tour_overlay_contract.py`;
and the last three rows of `docs/ui/design_reference/assumption_log.md`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r11-payloads/` READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r11/`          READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r11-worker/`   YOURS for logs, scripts and the vitest scratch; create it if
                                  absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace or a brace next to a quote is refused: write such a script to a file under your own
directory and run the file. Never run npm or npx: vitest, `tsc` and eslint run through the pytest
wrappers G4 names, and G5's tool runs the primary's own `vitest` binary.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `9c7f5fad7`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r11/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r11-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 66 | 11701 | 852ab5380b11f9c10fff9850355d31b580595788e4dab692ddc5da04bad9663a |
| plan.md | 29 | 944 | fa4a665b38e00af292b2fd638fa494d46220a32a366887b11883693bd70cd3b0 |
| landed.diff | 10 | 2557 | e92df1b3bb0ac537759769b6a735dfee9ee033ce1e087485f0eb00440d0d5b31 |
| assumption_line.md | 1 | 1053 | 645f581584453b7679ec10b3ba6bc02bad3069878ad554bd280a1e425d046fa9 |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `9c7f5fad` into which it wrote the edits.
`records.diff` appends round 10's gate entry, R-1094's `Done:` and R-1095's registration to
`.agent/live_review.md`, DECISION F038 D12 to `.agent/decisions.md` and one line to
`.agent/prose_slips.md`. `landed.diff` appends one `Landed: R-1095 — ` line on top of C2's ledger
and goes in with C4. `assumption_line.md` is appended byte for byte to
`docs/ui/design_reference/assumption_log.md`, which ends in a newline, in C3b.

THE SPECIFICATION. No `except Exception`, no `any`, no raw colour literal (the ratchet requires
zero in a new file), and no new dependency.
S1 R-1095's REPAIR. In `tests/orchestration/test_chat_turn.py`, two tests: `chat_turn_view` of a
   hand-built answer turn (`ChatAnswer`, `ChatAnswerSentence`, `ChatEvidenceSet`,
   `ChatEvidenceItem`) and of a hand-built card turn (`ChatActionCard`) each equals a LITERAL
   dictionary written out in the test, whose values are distinct and none a default: two
   sentences, one cited and supported, one uncited, unsupported, with a non-empty `problem`; two
   evidence items; `omitted` above 0; a non-empty `question`; a card with two `lines`, an `args`
   entry and a non-empty `missing`. Nothing else in that file changes.
S2 THE PURE HALF. A new `apps/ui/src/api/chatTurn.ts`, opening no socket, exporting:
   the types of the view (an answer, a card, and `{kind: "unavailable", reason}`);
   `CHAT_NOT_IN_EVIDENCE = "Not in evidence."`, spelled as `chat_answer.py` spells it;
   `decodeChatTurn(raw)`, which answers the unavailable kind for `available` false with a string
   `reason`, and for `available` true an answer or a card only when every key of the view is
   present with its type, the evidence numbered 1 to n in order, every citation an integer from 1
   to n, at least one sentence, and every card arg a string; otherwise `null`, never a partial
   view, never a throw; `chatTurnPath({jobId, token, text, taskId, baseUrl?})`, every value
   URL-encoded, with no `task` parameter when `taskId` is `""`; `chatSentenceText(sentence)`, the
   text with every inline `[n]` marker and the space before it removed, since the chips carry
   them; `chatSentenceMark(sentence)`, `unsupported` when not supported, `cited` when supported
   with a citation, `absence` only for `CHAT_NOT_IN_EVIDENCE` with none, and `unsupported`
   otherwise; `chatScopeLabel(answer)`, a sentence naming the task, the project, or no registered
   project; `chatEvidenceTab(kind)`, `diff` for a diff item, `prompt` for a prompt item, else
   `null`; `buildChatCardSendRequest(target, card, clientNonce)`, the door request with the
   bearer and `X-Remedy-CSRF` headers and the body `{command: verb, client_nonce, args}`, or
   `null` for an empty job id or token, a card not confirmable, with a `missing` entry or an
   empty verb, or an unusable nonce; `describeChatCardResult(result, verb)` and
   `describeUnsendableChatCard()`, one plain sentence each; and `sendChatCard(target, card,
   deps?)`, which mints, builds, submits once and describes, touching no network on a `null`.
   `remedyApi.ts` gains `loadChatTurn(request, fetchPayload = fetchJson)`, shaped as
   `loadTourView`, never throwing.
S3 THE TAB. A new `apps/ui/src/components/graph/EvidenceChatTab.tsx` with its
   `EvidenceChatTab.module.css` (the panel's `--remedy-*` tokens only), exporting a pure
   `ChatTurnBlock({question, view, turnKey, outcome, onConfirm, onOpenTab})`, where `view`
   `undefined` is pending and `null` unreadable, and `EvidenceChatTab({jobId, token, taskId,
   onTab})`. An answer renders a scope chip; each sentence as `chatSentenceText` inside an element
   with `data-ui="chat-sentence"` and `data-mark`, followed by one link per citation,
   `data-ui="chat-chip"`, text `[n]`, `href="#chat-<turnKey>-ev-<n>"`, or by
   `data-ui="chat-unsupported"` reading "unsupported" with the `problem` as its title; then the
   evidence items without list numbering, each `id="chat-<turnKey>-ev-<n>"`,
   `data-ui="chat-evidence-item"`, reading `[n] kind ref` and its text, with a button opening the
   diff or prompt trace tab for an item `chatEvidenceTab` maps. A card renders `data-ui="chat-card"`
   with its title and lines, a Confirm button `data-ui="chat-card-confirm"` only while it is
   confirmable, misses nothing and has not been sent with tone `ok`, and the outcome sentence with
   `role="status"`. The form holds a checkbox "Ask about the whole project", the input and Ask; a
   blank line asks nothing. It reads only through `loadChatTurn` and sends only through
   `sendChatCard`; no `fetch(` appears in it.
S4 THE WIRING, WHICH RETIRES THE PLACEHOLDER. `EvidencePanel.tsx`'s chat line becomes exactly
   `{tab === "chat" && <EvidenceChatTab jobId={jobId} token={token} taskId={detail.taskId} onTab={onTab} />}`
   with its import; `EVIDENCE_CHAT_NOT_YET` is deleted from `evidencePanel.ts` and its header
   comment no longer mentions it; in `evidencePanel.test.ts` its import and the one test pinning
   it are deleted; and in `tests/ui_contracts/test_evidence_panel_contract.py` the one assertion
   naming it is replaced by one asserting the new line. These two existing-test edits are ORDERED
   by this retirement and land in C3b with it; no other existing test is edited.
S5 THE ASSUMPTION ROW. `assumption_line.md` appended to the assumption log, in C3b.

THE TESTS. vitest collects `src/**/*.test.ts` in a node environment with no DOM library, so:
`apps/ui/src/api/chatTurn.test.ts` — at least, one each: the decoder reads an answer, a card
exactly, and an unavailable turn; refuses a citation beyond the evidence and a misnumbered item;
the path quotes the text and omits the task for the project; `chatSentenceText` drops `[1]` and
`[1][2]`; `chatSentenceMark` reads cited, unsupported without a citation, unsupported WITH a
citation, and absence; the send request's path and whole parsed body; an incomplete card sends
nothing (a counting submit stub) and a complete one sends once with the accepted sentence.
`apps/ui/src/components/graph/evidenceChatAudit.test.ts` — THE DOM AUDIT: `renderToStaticMarkup`
from `react-dom/server` over `createElement(ChatTurnBlock, ...)`, for an answer of three sentences
(one cited once, one unsupported, one cited twice): every sentence carries a chip or the
unsupported mark, no sentence's own text keeps an `[n]` marker, each chip's link number equals its
label, each chip's target id is rendered; the absence sentence alone carries neither; and Confirm
renders for a complete card and not for one unconfirmable or missing an argument.
`tests/ui_contracts/test_chat_citations.py` — the panel mounts the tab; the tab holds no `fetch(`
and calls `loadChatTurn(` and `sendChatCard(`; the TS `CHAT_NOT_IN_EVIDENCE` equals the Python
one; and every key of the view, `available` and `reason` is read by the decoder as `["<key>"]`.

BUNDLE — the commits are C1a, C1b, C2, C3a, C3b, C4 and C5, in this order.

C1a — `.agent/authored/f038-r11-block.md` := this block, `.agent/authored/f038-r11-plan.md` :=
  plan.md and `.agent/authored/f038-r11-assumption_line.md` := assumption_line.md, by
  `shutil.copyfile`. Subject: `F038 R11 C1a: copy round 11 block, plan and assumption payloads into .agent/authored/`
  Its insertions are this block's line count plus 30. STOP rather than commit at 500 or more.
C1b — `.agent/authored/f038-r11-records.diff` := records.diff and
  `.agent/authored/f038-r11-landed.diff` := landed.diff. Expected insertions: 76.
  Subject: `F038 R11 C1b: copy round 11 records and landed diffs into .agent/authored/`
C2 — `git apply` records.diff, then `.agent/plan.md` := plan.md. Expected by `git show --numstat`:
  35/0 decisions.md, 6/0 live_review.md, 7/7 plan.md, 1/0 prose_slips.md.
  Subject: `F038 R11 C2: book round 10, resolve R-1094, register R-1095, record DECISION F038 D12`
C3a — S2. Subject: `F038 R11 C3a: decode, mark and send a chat turn in the browser`
C3b — S3, S4, S5. Subject: `F038 R11 C3b: the evidence panel's chat tab, with chips, marks and cards`
C4 — S1, the three new test files, `git apply` landed.diff, and your mutation tool (G5) saved as
  `.agent/authored/f038-r11-mutations.py`. Subject: `F038 R11 C4: test the chat tab and repair R-1095`
C5 — `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R11 C5: rewrite handoff for round 11`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r11-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `apps/ui/src/api/chatTurn.ts`, `apps/ui/src/api/chatTurn.test.ts`,
   `apps/ui/src/api/remedyApi.ts`, `apps/ui/src/components/graph/EvidenceChatTab.tsx`,
   `apps/ui/src/components/graph/EvidenceChatTab.module.css`,
   `apps/ui/src/components/graph/EvidencePanel.tsx`, `apps/ui/src/components/graph/evidencePanel.ts`,
   `apps/ui/src/components/graph/evidencePanel.test.ts`,
   `apps/ui/src/components/graph/evidenceChatAudit.test.ts`,
   `docs/ui/design_reference/assumption_log.md`,
   `tests/ui_contracts/test_evidence_panel_contract.py`, `tests/ui_contracts/test_chat_citations.py`,
   `tests/orchestration/test_chat_turn.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 9c7f5fad7` at the branch tip after C5. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong, or this round's own mutation tool, may be corrected before C5 in a
   new commit, and the correction is declared. An EXISTING test that goes red, other than the two
   S4 orders edited, is never edited to pass; report it and stop.
5. NOTHING IS MERGED, SENT OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no `git stash`, no request to any server this
   round's tests did not start themselves or to any model, and no `git commit --amend` or any
   other rewrite of a commit, pushed or not: a wrong commit subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure. G4's selection takes about two minutes; run it once.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r11-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r11/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it, and show that
 `docs/ui/design_reference/assumption_log.md` at C3b equals its bytes at `9c7f5fad7` followed by
 `assumption_line.md`'s. Report one reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 named, equals the reviewer's reading, printed from its simulation tree. Report each beside the
 hash you read:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2413085 | e8041d41ed46ddde35c6126f33b0b18e9caac36a19f7b8b6f55bd45be3a4857c |
 | C2 | .agent/live_review.md | 344554 | 0b46aef726922f00c580374ccee73b7fde0ccf54ad8c85085f19e559ee7533d7 |
 | C2 | .agent/prose_slips.md | 376658 | 6ba91163114a4ae2e881afd928669566f7749dd89ae8c97d6ccfdd1976cb3313 |
 | C2 | .agent/plan.md | 944 | fa4a665b38e00af292b2fd638fa494d46220a32a366887b11883693bd70cd3b0 |
 | C4 | .agent/live_review.md | 344808 | e62a2b54cc6e0e1e823dcf366a7b5f678cb04b583353e4452ed5ee541cd7de4a |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show` at C2 and at C4 (the
 reviewer read `['R-1095']` at both); and `git diff --name-only <C1b> <C2>`, which must name
 exactly the four C2 paths of the table.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_chat_citations.py
 tests/ui_contracts/test_evidence_panel_contract.py tests/orchestration/test_chat_turn.py
 .agent/authored/f038-r11-mutations.py` at C4, with its real exit code. Then report, quoted from
 `git show <C3a>` and `git show <C3b>`, the whole of `decodeChatTurn`, `chatSentenceText`,
 `chatSentenceMark`, `buildChatCardSendRequest` and `ChatTurnBlock`, and the EvidencePanel line.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/orchestration/test_test_runner.py tests/orchestration/test_chat_turn.py tests/ui_server/test_chat_route.py tests/ui_server/test_dashboard_contract.py tests/docs tests/test_agent_tooling.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/cli/test_golden_path.py 2>&1 | tail -9; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 It runs the whole vitest suite (`test_vitest_passes`), `tsc` (`test_typescript_compiles`) and
 eslint (`tests/ui_contracts/test_ui_lint.py`) over `apps/ui`. The reviewer ran it serially in the
 primary checkout at `9c7f5fad7` and read `1555 passed, 5 skipped` at exit code 0, the skips being
 four F252 quarantines in `tests/ui_contracts/` and the one in `tests/test_agent_tooling.py`; over
 its simulation tree, whose own versions added 6 pytest nodes, it read 1556 passed and 10 skipped,
 the five further skips being the toolchain tests a worktree without `apps/ui/node_modules` cannot
 run. Report every `SKIPPED` line and the node counts of `tests/ui_contracts/test_chat_citations.py`
 and `tests/orchestration/test_chat_turn.py` (10 at `9c7f5fad7`) at C4, and account for any
 difference from 1555 passed by them. Then `python3 -m apps.cli.main integrity check --json`, all
 six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r11-mutations.py` takes a worktree path and
 has two runners. VITEST runs the PRIMARY's `apps/ui/node_modules/.bin/vitest run` with a scratch
 config the tool writes under `.remedy-wt/f038-r11-worker/`: a plain object with `root` the
 worktree's `apps/ui`, a cache directory under `.remedy-wt/`, `test.environment` `"node"` and
 `test.include` the worktree's two new vitest files by absolute path, `--reporter=json` into a
 file it reads for the failed names; before its first run the tool symlinks the worktree's
 `apps/ui/node_modules` to the primary's, so `react` resolves there. PYTEST runs `python3 -B -m
 pytest -q -p no:cacheprovider -rf tests/ui_contracts/test_chat_citations.py
 tests/ui_contracts/test_evidence_panel_contract.py tests/orchestration/test_chat_turn.py` from the
 worktree's root after purging its `__pycache__` directories. Each mutation asserts its FROM text
 occurs once in the worktree's file, runs its runner, restores the bytes, and prints its label, the
 exit code, the failed count and the failing names; controls of both runners run first and last,
 then `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
 VITEST, in `chatTurn.ts`: v1 an unsupported sentence with a citation marked cited; v2 a citation
 beyond the evidence decoded; v3 a card with a `missing` entry sendable; v4 the path drops the
 task; v5 the body drops the args. VITEST, in `EvidenceChatTab.tsx`: v6 the unsupported mark not
 rendered; v7 no chip rendered; v8 Confirm rendered for any card; v9 a chip linking to the next
 item; v10 the raw sentence text shown instead of `chatSentenceText`. PYTEST: c1 the TS absence
 sentence spelled otherwise; c2 the panel's chat line without the tab; and in `chat_turn.py`, p1
 a sentence's `problem` blanked, p2 an item's `text` blanked, p3 `missing` emptied, p4 `omitted`
 zeroed, p5 `question` blanked, p6 `lines` dropped.
 Run it: `git worktree add --detach .remedy-wt/f038-r11-mut <C4>`, then
 `python3 -B .agent/authored/f038-r11-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r11-mut`
 and report its whole output. EVERY mutation must be red with at least one failing name; a green
 one is reported as green, never papered over, and you then add the test that catches it in a
 commit before C5 and re-run. Then `git worktree remove --force .remedy-wt/f038-r11-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3b, C3a, C2, C1b, C1a and `9c7f5fad7` in that
 order (more lines if a commit was split or a declared correction added); `git worktree list |
 wc -l`, which must equal your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3a to C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 3
of feature F038, round 11, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 11, then T003's end-to-end proof: ask, a cited answer, a stop card confirmed, the job
stopping with its audit line; then closure. State the open-findings count, 1 (R-1095, landed and
awaiting the review), and the operator-questions count, 1.
