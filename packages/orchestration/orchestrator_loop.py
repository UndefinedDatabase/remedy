"""F070 — the orchestrator loop: Remedy running its own missions.

The external orchestrator's working style — read the state, decide the next
order, dispatch it, evaluate the result, write everything down — internalized.
Per iteration: assemble the context, take ONE schema-validated
:class:`~packages.orchestration.orchestrator_move_schema.OrchestratorMove` from
the orchestrator-role provider, execute it through Remedy's EXISTING verbs,
evaluate, update the mission, and append a ledger entry a human can audit.

**This module is a POLICY layer (Rule A6).** It sequences verbs; it does not
reimplement them. Every verb it calls is named in `.agent/decisions.md`'s F070
verb map: `mission_state.continue_mission` dispatches, `long_run_executor`
executes, `dod_gate` evaluates, `run_report` reports, `escalation` escalates,
`safe_points` stops. A diff here that grows its own intake, executor, DoD
mechanism, reporter or escalator is a defect, not a feature.

Remedy deliberately does NOT let this loop grant itself new goals. That is not
a rule written in the prompt — it is the shape of the move schema, which has no
kind for creating a mission or editing a goal. See
``orchestrator_move_schema`` for the boundary and why it lives there.

Three disciplines this module holds to:

* **Cache-stable prefix.** The dossier is assembled FIRST and is byte-stable
  while the mission does not change, so a provider's prompt cache survives
  across iterations. Volatile sections come after it, never before.
* **Human overrides win instantly.** A stop request and the mission's open
  decisions are read EVERY iteration, at the safe point between iterations —
  so a stop lands within one iteration rather than at the end of a run.
* **The ledger is the account.** One append-only entry per iteration — added
  in the next commit of this slice, together with the milestone bookkeeping.
"""
from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# The protocol document — read, never written
# ---------------------------------------------------------------------------

#: Bump together with any change to what the protocol document ASKS the
#: orchestrator to do. Every ledger entry records the version it ran under, so
#: an audit can tell which contract a past decision was made against.
PROTOCOL_VERSION = "v1"

#: Where the protocol document lives, relative to the repo root. The location
#: is recorded in `.agent/decisions.md`; keeping it under ``docs/agents/``
#: puts the orchestrator's job description beside the human roles' own.
PROTOCOL_DOC_RELATIVE = "docs/agents/orchestrator_protocol.md"


def _repo_root() -> Path:
    """This repository's root, derived from this file's own location."""
    return Path(__file__).resolve().parents[2]


def protocol_document_path(repo_root: Path | None = None) -> Path:
    """Absolute path of the versioned protocol document."""
    return (repo_root or _repo_root()) / PROTOCOL_DOC_RELATIVE


def orchestrator_protocol_text(repo_root: Path | None = None) -> str:
    """The protocol document's text.

    Remedy deliberately does NOT provide a writer for this file. Runtime
    self-modification of the protocol is in F070's Do-not-touch list, so the
    absence of a write path here is the enforcement, not an omission: the loop
    reads its job description and cannot edit it.
    """
    return protocol_document_path(repo_root).read_text(encoding="utf-8")


def build_orchestrator_system_prompt(repo_root: Path | None = None) -> str:
    """The orchestrator role's system-prompt block, GENERATED from the document.

    Nothing about the orchestrator's instructions is authored in code — change
    the document and the prompt changes with it, as a reviewable diff.
    """
    return (
        f"# Orchestrator protocol {PROTOCOL_VERSION}\n"
        f"# Source: {PROTOCOL_DOC_RELATIVE} (versioned in the repository)\n\n"
        f"{orchestrator_protocol_text(repo_root)}"
    )
