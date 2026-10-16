# Face v1: Remedy as a backend, its face as the universe's edition `remedy`

Written 2026-10-15 for operator amendment amend1015-face-migration (decisions `amend1015f D0` and
up in `.agent/decisions.md`). This file and the universe's `docs/universe/REMEDY.md` are the plan
of the amendment; there is no further roadmap for it.

## The idea in plain sentences

Remedy is a backend. It is a command line and a versioned, documented HTTP API. Any developer can
write a client for that API, and Remedy is fully usable without anything else. Remedy has no web
page of its own any more.

The face that a person uses is the universe's edition `remedy`: an Orb on the same brain, app, kit
and front door that Luna and Sol use. It has the same chat window, the same five tabs, the same job
page and the same approval card. There is no second job engine and no copied chat code.

The one contract between the two is the run story: a read-only route that tells, in a fixed shape
with closed keys, what one job is doing, what it changed, what it measured and what the next step
is. The face translates every key into German itself. Remedy sends no prose, no secrets, no private
paths and no shell commands through it.

Who may do what with which token:

- Remedy's operator holds the admin token; nothing of this amendment uses it.
- The Orb holds one client token (`remedy client`) scoped to the projects decodeux allows. It lives
  only on the workstation, in the Orb's own environment file. It never reaches a browser, a
  browser's storage or a URL.
- The phone holds the Orb's device token, which the universe pairs as for Luna. With it the phone
  reads jobs and stories through the Orb; the Orb's apply, decline and retry operations need a
  paired device token too, and the gate's and the voice's service tokens cannot call them.

## The inventory (2026-10-15)

| Function | Remedy API route | Orb adapter (universe) | App place | Missing before this amendment |
| --- | --- | --- | --- | --- |
| Start an order | `POST /api/v1/orders`, `GET /api/v1/orders/{order}` | `luna_operator.remedy`: `POST /v1/remedy/orders` (new, luna-api 47) | «Remedy» tab: "Was soll Remedy tun?" | The Orb's route and the tab's field |
| See runs | `GET /api/v1/digest`, `GET /api/v1/changes` | `RemedyLink` view, jobs of kind `remedy` in `GET /v1/jobs` (new, luna-api 11.2) | Live board, «Remedy» tab's last five runs | Remedy jobs as Orb jobs |
| What one run does | `GET /api/v1/jobs/{job}/story` (new) | `story` field of the Orb's job | Job page: status sentence, steps, changes, numbers | The story route, its German texts |
| The log | `GET /api/v1/jobs/{job}/logs` | the Orb's job log | Job page, below the story | Wiring the log of a remedy job |
| Approve or decline | `POST /api/v1/jobs/{job}/apply`, `/decline` | `POST /v1/jobs/{id}/apply`, `/decline` (new) | Job page: "Nächster Schritt" | The Orb's two actions |
| Try again | `POST /api/v1/jobs/{job}/run`, `GET .../run` | `POST /v1/jobs/{id}/retry` (new) | Job page: "Noch einmal versuchen" | The Orb's action |
| Answer a question | `POST /api/v1/jobs/{job}/decisions/{decision}` | questions `q-r-<n>` (existing, luna-api 14) | Eingang | nothing |
| What Remedy offers | `GET /api/v1/interface` | `GET /v1/remedy` `cli` (new) | Job page: the command in small type | The Orb's summary |
| Is Remedy there | `GET /api/v1/health`, every call's failure | `GET /v1/remedy` `state` and `sentence` (new) | «Remedy» tab, job page | One German sentence instead of a spinner |
| What a change rests on | `GET /api/v1/jobs/{job}/proof` | not used in v1 | not shown in v1 | registered for Face v2 |
| Steering note | none in `/api/v1` | none | none | registered as a finding for F307 |

## What is deleted, and when

Only after the three gates of the amendment are green in the same run: the React app `apps/ui`,
its static serving and auto-build in the supervisor, its bundle guard in the wheel build, the `ui`
step of `remedy do`, and the tests whose subject is the deleted app. The public API, its
authentication and project scopes, every JSON route a client still reads, the tests of those, the
history and the contracts stay.

## The way back

Everything deleted stays in git history. Restoring the face means reverting the Phase 4 commits of
the amendment's pull request; the API needs nothing for it.
