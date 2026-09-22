"""F114 T002 — the shared cost-preview confirmation helper.

Renders an upfront USD estimate band and confirms before an expensive
command runs. A SHARED module so a future expensive command reuses this
rather than growing a copy of the same shape.
No command calls this yet - wiring a real command to it is T003.
"""
from __future__ import annotations

import sys

from apps.cli.json_envelope import fail
from packages.orchestration.cost_preview import CostBandEstimate

EXIT_USAGE = 2


def _stdin_is_a_tty() -> bool:
    """Whether there is an operator on the other end who could answer a prompt."""
    return sys.stdin.isatty()


def render_estimate_line(estimate: CostBandEstimate) -> str:
    """The one-line preview text - always carries its basis (A9)."""
    if estimate.band_usd_low is None or estimate.band_usd_high is None:
        return f"estimated cost unavailable (basis: {estimate.basis})"
    return (
        f"estimated ${estimate.band_usd_low:.4f}-${estimate.band_usd_high:.4f} "
        f"(basis: {estimate.basis})"
    )


def confirm_cost_preview(
    estimate: CostBandEstimate,
    *,
    confirm_above_usd: float,
    yes: bool,
    command_name: str,
    json_output: bool = False,
) -> bool:
    """Show the estimate and decide whether the command may proceed.

    Returns True to proceed, False if the operator declined. An
    UNAVAILABLE estimate (``band_usd_high`` is None) is treated as
    expensive (A9) - it always requires confirmation, same as a real
    high estimate over the threshold.

    ``yes`` skips the prompt and proceeds, printing an audited line so
    the skip is visible in evidence. A non-tty stdin never blocks: it
    exits with the estimate and the --yes hint rather than hanging on a
    pipe. Below the threshold, no prompt either way - cheap commands
    never interrupt.

    DECISION F283 D2 — ``json_output`` keeps stdout the one parseable object
    a ``--json`` caller reads. With it off, nothing changes: the same lines
    on the same streams, the same exit code. With it on, every line this
    helper writes for a human — including the prompt ``input()`` would
    otherwise print to stdout — goes to stderr instead, byte for byte the
    same text, and the non-terminal refusal answers through ``fail()``
    rather than printing its own ``Error: `` line and exiting itself.
    """
    line = render_estimate_line(estimate)
    is_expensive = estimate.band_usd_high is None or estimate.band_usd_high > confirm_above_usd
    human = sys.stderr if json_output else sys.stdout
    if not is_expensive:
        print(line, file=human)
        return True

    if yes:
        print(f"{line} - proceeding without prompt (--yes)", file=human)
        return True

    if not _stdin_is_a_tty():
        message = (
            f"{line}. stdin is not a terminal, so there is nobody to "
            f"confirm. Pass --yes to run '{command_name}' without a prompt."
        )
        fail("confirmation_required", message, json_output=json_output, exit_code=EXIT_USAGE)

    print(line, file=human)
    prompt = f"Continue running '{command_name}'? [y/N] "
    if json_output:
        print(prompt, end="", file=sys.stderr)
        answer = input()
    else:
        answer = input(prompt)
    return answer.strip().lower() in ("y", "yes")
