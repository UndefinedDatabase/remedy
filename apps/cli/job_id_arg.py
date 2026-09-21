"""F283 T001 — resolve a job-id argument, or refuse in the shape the caller asked for.

Finding R-1020.  ``packages.orchestration.data_paths.resolve_job_id`` is the EXITING form
of the lookup: it prints a prose line to stderr and calls ``sys.exit`` itself, one call
above the handler's own failure path.  A command that declares ``supports_json`` and takes
a job id therefore answered a bad id with prose and an empty stdout however carefully its
own refusals had been migrated onto :func:`apps.cli.json_envelope.fail` — which is the
defect the envelope exists to remove.

The fix is a LAYER, not a rewrite of the resolver.  ``lookup_job_id`` already raises rather
than exits, and its own docstring names this as the intended shape: "A handler that guards
its parse calls :func:`lookup_job_id` and catches the ``ValueError``."  This module is that
guard, written once for every CLI caller instead of once per command group.

Remedy deliberately does not put ``fail()`` inside ``data_paths``.  The envelope is a CLI
contract and ``packages/`` is the layer beneath it; pushing the envelope down would make
the storage layer depend on the shape of a command's stdout.  The exiting
``resolve_job_id`` therefore stays exactly as it is, for the callers that have no failure
path of their own, and the ``--json`` callers move up to this one.

The TEXT branch is byte-identical to what the exiting helper printed: ``fail()`` writes
``Error: `` itself, and the ambiguous message reproduces the helper's header line and its
one indented line per match, so an operator's terminal does not change.
"""

from __future__ import annotations

from typing import NoReturn

from apps.cli.json_envelope import fail
from packages.orchestration.data_paths import JobIdAmbiguous, JobIdError, lookup_job_id


def refuse_ambiguous_job_id(raw: str, matches: list[str], *, json_output: bool) -> NoReturn:
    """Refuse in the envelope: ``raw`` is a prefix more than one job matches.

    The shared body of the ambiguous branch, split out so a caller that reaches
    :func:`lookup_job_id` itself — rather than through :func:`resolve_job_id_or_fail` —
    can still answer the SAME refusal. `apps/cli/commands/job_stop_cmd.py` is that
    caller: it needs `job_id` in the envelope's own payload, which
    :func:`resolve_job_id_or_fail` does not carry.

    Exit 2, always — the code the exiting resolver already used. Under ``--json`` the
    envelope additionally carries ``matches``, the full job ids it could have meant, so
    a machine can disambiguate without re-running the command and parsing a prose list.
    """
    matches = sorted(matches)
    listed = "\n".join(f"  {m[:8]}" for m in matches)
    fail(
        "ambiguous_job_id",
        f"ambiguous job id prefix '{raw}' matches {len(matches)} jobs:\n{listed}",
        json_output=json_output,
        exit_code=2,
        matches=matches,
    )


def resolve_job_id_or_fail(raw: str, *, json_output: bool) -> str:
    """The job id ``raw`` names, or a refusal in the envelope and an exit.

    Exit 1 when the string names no job, exit 2 when a prefix names more than one —
    the two codes the exiting resolver already used, unchanged, because renumbering
    them belongs to F283's T002 taxonomy and not to this repair.
    """
    try:
        return lookup_job_id(raw)
    except JobIdAmbiguous as exc:
        refuse_ambiguous_job_id(raw, exc.matches, json_output=json_output)
    except JobIdError:
        fail(
            "invalid_job_id",
            f"No job matches {raw!r}. Try: remedy job list.",
            json_output=json_output,
        )
