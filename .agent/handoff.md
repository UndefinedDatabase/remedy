# Handoff — operator amendment amend1026-go-live-and-ask (session 1, closing)

- Branch: `feature/amend1026-go-live-and-ask`, merged into `main` by its pull request.
- Feature: F318 (Fragen an ein Projekt, nur lesend), registered and accepted by this amendment.
- Open findings added: none. Finding of Part C2: the public API has no upload route, so the ask
  takes no `attachments` (DECISION amend1026 D4 (6)).

## Machine state (Part A)
- Supervisor: the user unit `remedy-serve-live` (systemd-run), port 8450, data root
  `~/Repos/remedy/.data`, code of `main` (editable install of `~/Repos/remedy`).
- `host_tools`: `orb-universe` and `orb-remedy` true, `luna` false (it was true and was revoked).
- Order `a5d65e5e50342eec` (key `luna-twmhd8`) cancelled with the ordered reason; the earlier order
  of that key, `048ff6987b7336bd`, was already cancelled on 2026-10-23.
- Remedy's own project: the slug `remedy`, not `remedy-backend`.

## Changed
| Area | Files |
|---|---|
| D1, D2 | `execution_options.py`, `scope_decision.py`, `client_story.py`, `order_story.py` |
| D3 | `order_review.py`, route, `remedy client order-review` |
| C1 | `client_projects.py`, route, `remedy client projects` |
| C2, C3 | `project_ask.py`, route, `remedy client ask`, `public_api_writes.py`, data-root class `evidence` |
| B | contract 1.30, `docs/system/public-http-api-v1.md`, `CHANGELOG.md`, release matrix |
| E | `evidence/current/amend1026_ask/`, `STATUS.md`, `T2_F318.md`, `README.md` |

## Verification
- First full run: 8 failed, 24,324 passed (guards: exit codes, release matrix, reachability,
  data-root class, file limit, context steps); all repaired.
- The final run's command, interpreter, tree and result are in the pull request's body.
- Real ask: 200, 2,199 tokens (10 in, 2,189 out), 1 call, 5 turns, `claude-opus-5-5`, repository
  unchanged; the answer names `scope_decision.py`.

## Next
The next session: Rule A5 reads F316.
