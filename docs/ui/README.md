# Remedy has no page of its own

Since 2026-10-15 Remedy ships no web page. Its old cockpit, the React app under `apps/ui`, was
deleted (amend1015f D3 and D19). Remedy's face is now the universe's edition `remedy`, described in
[the edition's README](../../../universe/remedy/README.md), which lives in the universe workspace
beside this repository.

What Remedy serves is its public HTTP API under `/api/v1`, started by `remedy serve start`. Every
route, answer and refusal is listed on [the public HTTP API's page](../system/public-http-api-v1.md),
and [the HTTP clients guide](../guides/http-clients.md) walks a program through it with `curl`,
from its token to an applied change.

The old cockpit's guides and design references are kept for history in `docs/archive/`.
