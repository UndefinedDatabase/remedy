"""F114 T002 — the shared cost-preview confirmation helper.

Renders an upfront USD estimate band and confirms before an expensive
command runs. A SHARED module (unlike loop_cmd.py's own local
`_confirm_materialization`/`_stdin_is_a_tty` copy) so a future expensive
command reuses this rather than growing a third copy of the same shape.
No command calls this yet - wiring a real command to it is T003.
"""
from __future__ import annotations

import sys

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
    """
    line = render_estimate_line(estimate)
    is_expensive = estimate.band_usd_high is None or estimate.band_usd_high > confirm_above_usd
    if not is_expensive:
        print(line)
        return True

    if yes:
        print(f"{line} - proceeding without prompt (--yes)")
        return True

    if not _stdin_is_a_tty():
        print(
            f"Error: {line}. stdin is not a terminal, so there is nobody to "
            f"confirm. Pass --yes to run '{command_name}' without a prompt.",
            file=sys.stderr,
        )
        sys.exit(EXIT_USAGE)

    print(line)
    return input(f"Continue running '{command_name}'? [y/N] ").strip().lower() in ("y", "yes")
