# F318 — a question to a project, read-only (operator amendment amend1026-go-live-and-ask, Part E)

Run on 2026-10-26 at 12:19 UTC on the operator's machine against the long-running supervisor
(`remedy-serve-live`, port 8450, data root `~/Repos/remedy/.data`), restarted on this branch's code,
with a real call of the Claude Code CLI 2.1.310. Collected by `.agent/authored/amend1026-e1-evidence.py`;
no client token is stored here.

| Acceptance | Evidence |
|---|---|
| The server speaks contract 1.30 | `interface_version.json`: `interface_version` `1.30` |
| `orb-universe` holds `host_tools`; claude-cli is every role's default and available | `execution_offer.json`: `host_tools` true, `default_provider` `claude-cli` and `claude_cli_available` true for planner, builder, reviewer and repair; `autonomy.push_allowed` true |
| The client sees its projects, Remedy's own among them | `projects.json`: the slug `remedy`, repository `~/Repos/remedy` (Universe's alias `remedy-backend` names no project here) |
| The question was asked over HTTP by `orb-universe` | `ask_request.json`: `POST /api/v1/projects/remedy/ask`, the question „Welche Datei entscheidet, ob ein Auftrag ein Job oder mehrere wird, und wie?“, `max_total_tokens` 150000 |
| The answer names `scope_decision.py` | `ask_answer.json` and `ask_evidence/answer.md`: `packages/orchestration/scope_decision.py` (the planner's question) together with `packages/orchestration/do_lane.py` (`settle_do_lane`, the last word) |
| Only reading tools were offered and called | `ask_evidence/question.json` `argv`: `--tools Read,Glob,Grep --allowedTools Read,Glob,Grep --restricted --strict-mcp-config --safe-mode`; `ask_evidence/tool_calls.jsonl`: Grep, Read, Grep, Read; `ask_evidence/result.json`: no permission denial |
| The repository is unchanged | `ask_evidence/result.json` `repo_unchanged` true (HEAD, status and diff digest equal before and after); `repository_state.json`: HEAD `1e7cc4462` before and after, an empty `git status` both times |
| Real provider calls, kept under the data root | `ask_answer.json`: 1 call, 5 turns, model `claude-opus-5-5`, 10 input, 2,189 output, 14,167 cache-written and 35,329 cache-read tokens (`tokens_used` 2,199); 25.1 s; the data root's `evidence/asks/ask-20261026T121928Z-59affd79/` is copied whole into `ask_evidence/` |

No manual operator repair: every file here was written by the supervisor's route and the script that called it.
