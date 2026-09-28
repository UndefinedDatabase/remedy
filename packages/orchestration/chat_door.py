"""F038 T002 and DECISION F038 D7 — the chat's send of a confirmed action card through the
cockpit's one write door, `POST /api/jobs/<id>/commands` in
`packages/orchestration/ui_server.py`, over the same loopback connection the browser uses.

Remedy deliberately does not let the chat run a command's effect itself: this module builds
the door's own request body, refuses a card that is not confirmable before anything is sent,
and posts it exactly as a browser command would, so the door's own token check, nonce replay,
rate limit and audit line all apply to the chat unchanged.
"""

from __future__ import annotations

import http.client
import json
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.chat_intent import (
    ChatActionCard,
    ChatIntentError,
    card_command_payload,
)
from packages.orchestration.safe_points import is_safe_id

#: The write door only ever binds `127.0.0.1` — `start_ui_server`'s own security check.
CHAT_DOOR_HOST = "127.0.0.1"
CHAT_DOOR_TIMEOUT_S = 10.0


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
