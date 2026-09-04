"""CLI handlers for the self-repair command group."""

from __future__ import annotations

import argparse
import json
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def _cmd_proposal_create(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import (
        create_self_repair_proposal_from_replay,
        export_self_repair_proposal_json,
    )

    run_id = args.run_id
    use_json = getattr(args, "json", False)

    proposal = create_self_repair_proposal_from_replay(run_id)

    if use_json:
        json.dump(export_self_repair_proposal_json(proposal), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    print(f"Proposal {proposal.proposal_id} created.")
    print(f"  Status: {proposal.status}")
    print(f"  Title:  {proposal.title}")
    if proposal.evidence_refs:
        print(f"  Evidence refs: {len(proposal.evidence_refs)}")
    if proposal.suspected_files:
        print(f"  Suspected files: {len(proposal.suspected_files)}")


def _cmd_proposal_show(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import (
        export_self_repair_proposal_json,
        load_self_repair_proposal,
    )

    proposal_id = args.proposal_id
    use_json = getattr(args, "json", False)
    proposal = load_self_repair_proposal(proposal_id)

    if proposal is None:
        msg = f"Proposal {proposal_id} not found."
        if use_json:
            json.dump({"error": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if use_json:
        json.dump(export_self_repair_proposal_json(proposal), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    print(f"Proposal: {proposal.proposal_id}")
    print(f"  Status:  {proposal.status}")
    print(f"  Title:   {proposal.title}")
    print(f"  Run:     {proposal.run_id}")
    print(f"  Problem: {proposal.problem_summary[:200]}")
    if proposal.evidence_refs:
        print(f"  Evidence refs ({len(proposal.evidence_refs)}):")
        for ref in proposal.evidence_refs[:5]:
            print(f"    - {ref}")
    if proposal.operator_decision:
        print(f"  Decision: {proposal.operator_decision}")


def _cmd_proposal_list(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import list_self_repair_proposals

    run_id = getattr(args, "run_id", None)
    use_json = getattr(args, "json", False)
    proposals = list_self_repair_proposals(run_id=run_id or None)

    if use_json:
        json.dump(proposals, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if not proposals:
        print("No self-repair proposals found.")
        return

    for p in proposals:
        print(f"  {p.get('proposal_id', '?'):20s}  {p.get('status', '?'):25s}  {p.get('title', '')[:50]}"
              f"  (created={p.get('created_at', '')}, updated={p.get('updated_at', '')})")


def _cmd_proposal_approve(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import (
        approve_self_repair_proposal,
        export_self_repair_proposal_json,
    )

    proposal_id = args.proposal_id
    operator_id = args.operator_id
    use_json = getattr(args, "json", False)
    result = approve_self_repair_proposal(proposal_id, operator_id)

    if result is None:
        msg = f"Cannot approve proposal {proposal_id} (not found or terminal)."
        if use_json:
            json.dump({"error": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if use_json:
        json.dump(export_self_repair_proposal_json(result), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Proposal {proposal_id} approved by {operator_id}.")


def _cmd_proposal_deny(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import (
        deny_self_repair_proposal,
        export_self_repair_proposal_json,
    )

    proposal_id = args.proposal_id
    operator_id = args.operator_id
    reason = getattr(args, "reason", None) or ""
    use_json = getattr(args, "json", False)
    result = deny_self_repair_proposal(proposal_id, operator_id, notes=reason)

    if result is None:
        msg = f"Cannot deny proposal {proposal_id} (not found or terminal)."
        if use_json:
            json.dump({"error": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if use_json:
        json.dump(export_self_repair_proposal_json(result), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Proposal {proposal_id} denied by {operator_id}.")


def _cmd_proposal_edit(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import (
        edit_self_repair_proposal,
        export_self_repair_proposal_json,
    )

    proposal_id = args.proposal_id
    operator_id = args.operator_id
    text = args.text
    use_json = getattr(args, "json", False)
    result = edit_self_repair_proposal(proposal_id, operator_id, text)

    if result is None:
        msg = f"Cannot edit proposal {proposal_id} (not found or terminal)."
        if use_json:
            json.dump({"error": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if use_json:
        json.dump(export_self_repair_proposal_json(result), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Proposal {proposal_id} edited by {operator_id}. Status: awaiting_operator.")


def _cmd_worker_prompt(args: argparse.Namespace) -> None:
    from packages.orchestration.self_repair_proposal import (
        convert_self_repair_proposal_to_worker_prompt,
    )

    proposal_id = args.proposal_id
    use_json = getattr(args, "json", False)
    prompt = convert_self_repair_proposal_to_worker_prompt(proposal_id)

    if prompt is None:
        msg = f"Cannot convert proposal {proposal_id} (not found, not approved, or already converted)."
        if use_json:
            json.dump({"error": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if use_json:
        json.dump({"proposal_id": proposal_id, "worker_prompt": prompt}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(prompt)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "self-repair.proposal-create": _cmd_proposal_create,
    "self-repair.proposal-show": _cmd_proposal_show,
    "self-repair.proposal-list": _cmd_proposal_list,
    "self-repair.proposal-approve": _cmd_proposal_approve,
    "self-repair.proposal-deny": _cmd_proposal_deny,
    "self-repair.proposal-edit": _cmd_proposal_edit,
    "self-repair.worker-prompt": _cmd_worker_prompt,
}
