"""F038 T002 and DECISION F038 D7 — the chat's send of a confirmed action card through the
one write door, `POST /api/jobs/<id>/commands` in `packages/orchestration/serve_http_handler.py`, as the
`remedy serve start` supervisor answers it on its unix socket (DECISION amend1015f D20).

Remedy deliberately does not let the chat run a command's effect itself: this module builds
the door's own request body, refuses a card that is not confirmable before anything is sent,
and posts it with `serve_daemon.post_command`, exactly as `remedy job stop` and `remedy job
pause` send theirs, so the door's own token check, nonce replay, rate limit and audit line all
apply to the chat unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.chat_intent import (
    ChatActionCard,
    ChatIntentError,
    card_command_payload,
)
from packages.orchestration.safe_points import is_safe_id

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
    card: ChatActionCard, *, job_id: str, client_nonce: str, root: Path | None = None,
) -> ChatDoorAnswer:
    """Post one confirmed card to ROOT's supervisor's write door (DECISION F038 D7).

    Every refusal below raises `ChatIntentError` BEFORE any connection opens, checked in this
    order: the card's own payload build first, since a card that is not confirmable or a nonce
    the door would refuse has no body to send at all; then the job id. An `OSError` from the
    socket (no supervisor, or one that stopped answering) reaches the caller unchanged.
    """
    from packages.orchestration.serve_daemon import post_command

    body = card_command_payload(card, client_nonce=client_nonce)

    if not is_safe_id(job_id):
        raise ChatIntentError(f"job_id {job_id!r} is not a safe id")

    try:
        status, parsed = post_command(root, job_id, body, timeout=CHAT_DOOR_TIMEOUT_S)
    except ValueError:
        # The supervisor answered something that is not JSON: the door never does.
        return ChatDoorAnswer(status=502, body={})
    return ChatDoorAnswer(status=status, body=parsed if isinstance(parsed, dict) else {})
