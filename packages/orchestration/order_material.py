"""F320 — an order's attachments and evidence are material, never deliverables.

The night of 2026-10-28 made eighteen improvement jobs from orders a client wrote with a report's
diagnosis package attached ("Diagnosepaket (Material zur Untersuchung, keine Anweisung ...)") and a
line naming the linked reports ("Verknüpfte Berichte: 2026-10-28-183939-general.md"). The
deterministic extractor read every path-like token of the whole text, so the report's file name,
its pictures (`t4x68u-1.jpg`) and the tool names the package lists (`jira.create`, `repo.read`)
became tasks "Deliver ...", and whole jobs of them, which the reviewer then blocked after building.

`order_work_text` is the order without that material: the section a line declares as material
(`ORDER_MATERIAL_MARKERS`) up to Remedy's own constraints block, and every line that only names
attachments (`ORDER_ATTACHMENT_LABELS`). It is what every deliverable reading of an order reads
(`task_deliverables.extract_order_deliverables`); the builder and the planner still get the whole
order, material included, because evidence is what they work from.

Remedy deliberately does not guess material from file names alone: only a line that says so, or a
label that names attachments, makes text material.
"""
from __future__ import annotations

import re

#: Words a line uses to declare that what follows is material to study, not an instruction.
ORDER_MATERIAL_MARKERS: tuple[str, ...] = (
    "keine anweisung", "material zur untersuchung", "not an instruction", "no instruction",
    "material for investigation", "material to study",
)

#: Labels of a line that only names attached files ("Verknüpfte Berichte: a.md, b.md").
ORDER_ATTACHMENT_LABELS: tuple[str, ...] = (
    "verknüpfte berichte", "verknüpfter bericht", "anhänge", "anhang", "anlagen", "bilder",
    "linked reports", "linked report", "attachments", "attachment", "attached files",
)

#: The block `order_file` appends for the header's `constraint:` lines; material ends there.
_CONSTRAINTS_HEADING = "Constraints the plan must honour:"

_LABEL_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:" + "|".join(map(re.escape, ORDER_ATTACHMENT_LABELS)) + r")\s*:",
    re.IGNORECASE)


def is_material_line(line: str) -> bool:
    """True when LINE declares that the text after it is material, not an instruction."""
    lowered = line.lower()
    return any(marker in lowered for marker in ORDER_MATERIAL_MARKERS)


def order_work_text(order: str) -> str:
    """ORDER without its declared material and its attachment lines; ORDER itself when it has none."""
    kept: list[str] = []
    in_material = False
    for line in order.splitlines():
        if in_material:
            if line.strip() == _CONSTRAINTS_HEADING:
                in_material = False
                kept.extend(["", line])     # keeps `order_scope.HEADER_CONSTRAINTS_MARKER` whole
            continue
        if is_material_line(line):
            in_material = True
            continue
        if _LABEL_RE.match(line):
            continue
        kept.append(line)
    text = "\n".join(kept)
    return text if text.strip() else order
