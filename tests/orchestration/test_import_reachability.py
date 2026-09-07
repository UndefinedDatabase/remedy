"""The import-reachability ratchet over the six D11 (c) entry points.

WHAT THIS GUARDS. Operator amendment amend0905-vocab, DECISION D11 (c), requires
that no module outside an allowlist is importable from the six real entry points
of this product — the golden path, the job path, the mission path, the self-use
runner, the teacher and the cockpit read endpoints. F274's T003 names this test
as the proof that must be green around the prototype-cluster deletion. The
allowlist is the MEASUREMENT of today's reachable set, not a wish: it is
generated from the closure this module computes, so a deletion round shrinks it
and assertion (c) reds if it forgets to, and a new orphan module wired into the
graph reds assertion (b).

WHY THE WALK IS STATIC. The closure is computed by parsing each module with
`ast`, never by importing it. Importing the cockpit — `packages.orchestration.ui_server`
— runs module-level side effects, and a guard that has to boot the product in
order to describe it is not a guard.

WHY OVER-APPROXIMATION IS THE SAFE DIRECTION. Imports inside
`if TYPE_CHECKING:` blocks and inside function bodies ARE followed, and a
`from X import y` contributes both `X` and `X.y`. For a test whose job is to
guard a DELETION, counting a module as reachable when it might not be is the
harmless error; missing an edge and calling a live module an orphan is the
error that deletes working code. Names that resolve to no file on disk are
dropped, and relative imports are skipped — this repository has no first-party
relative imports.

DECISION F274 D1 rules this shape: a RATCHET against a generated allowlist,
rather than the precondition F260's Design paraphrased it as. Finding R-0830
records why that paraphrase is unmeetable — all twenty-four cluster modules are
reachable from the very entry points the proof measures.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

ALLOWLIST_PATH = Path(__file__).resolve().parent / "import_reachability_allowlist.txt"

# The six DECISION amend0905-vocab D11 (c) entry points, resolved to dotted modules.
ENTRY_POINTS = (
    "apps.cli.commands.do_cmd",          # the golden path
    "apps.cli.commands.job",             # the job path
    "apps.cli.commands.mission_cmd",     # the mission path
    "packages.orchestration.self_use_runner",  # the self-use runner
    "apps.cli.commands.teach_cmd",       # the teacher
    "packages.orchestration.ui_server",  # the cockpit read endpoints
)

# A dotted name is first-party when its first segment is one of these.
FIRST_PARTY_ROOTS = ("packages", "apps")


def resolve_module_path(dotted: str) -> Path | None:
    """Return the file backing a dotted first-party module, or None if there is none."""
    parts = dotted.split(".")
    if not parts or parts[0] not in FIRST_PARTY_ROOTS:
        return None
    module_file = REPO_ROOT.joinpath(*parts).with_suffix(".py")
    if module_file.is_file():
        return module_file
    package_file = REPO_ROOT.joinpath(*parts, "__init__.py")
    if package_file.is_file():
        return package_file
    return None


def first_party_imports(path: Path) -> set[str]:
    """Every first-party dotted name named by an import statement anywhere in the file."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    named: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                named.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            # Relative imports are skipped; this repository has none first-party.
            if node.level or node.module is None:
                continue
            named.add(node.module)
            for alias in node.names:
                # `from X import y` contributes both X and X.y; X.y is dropped
                # later if it names a function rather than a module.
                named.add(f"{node.module}.{alias.name}")
    return {name for name in named if name.split(".")[0] in FIRST_PARTY_ROOTS}


def reachable_closure() -> set[str]:
    """The transitive first-party import closure of ENTRY_POINTS, statically computed."""
    reached: set[str] = set()
    pending = list(ENTRY_POINTS)
    while pending:
        dotted = pending.pop()
        if dotted in reached:
            continue
        path = resolve_module_path(dotted)
        if path is None:
            continue
        reached.add(dotted)
        pending.extend(sorted(first_party_imports(path) - reached))
    return reached


def read_allowlist() -> set[str]:
    """The allowlist as a set; blank lines and hash-comment lines are ignored."""
    raw = ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines()
    stripped = (line.strip() for line in raw)
    return {line for line in stripped if line and not line.startswith("#")}


def _one_per_line(modules: set[str]) -> str:
    return "\n".join(sorted(modules))


def test_every_entry_point_resolves_to_a_file_on_disk():
    """Without this, a typo shrinks the measured set to nothing and the ratchet passes vacuously."""
    missing = {name for name in ENTRY_POINTS if resolve_module_path(name) is None}
    assert not missing, (
        "These D11 (c) entry points resolve to no file on disk, so the reachability "
        "measurement below would be taken over a smaller graph than the product has:\n"
        + _one_per_line(missing)
    )


def test_no_module_outside_the_allowlist_is_reachable_from_the_entry_points():
    """DECISION amend0905-vocab D11 (c) itself. A new orphan wired into the graph reds here."""
    unlisted = reachable_closure() - read_allowlist()
    assert not unlisted, (
        "These modules are reachable from the D11 (c) entry points but are not in "
        f"{ALLOWLIST_PATH.name}. Either the import that reached them is unwanted, or "
        "the allowlist is stale and this round grew the reachable set:\n"
        + _one_per_line(unlisted)
    )


def test_every_allowlist_entry_still_resolves_to_a_file_on_disk():
    """A deletion round that forgets to shrink the allowlist reds here."""
    stale = {name for name in read_allowlist() if resolve_module_path(name) is None}
    assert not stale, (
        f"These {ALLOWLIST_PATH.name} entries name modules with no file on disk. A "
        "deletion round must remove an entry in the same commit that removes its "
        "module, so the allowlist stays a measurement:\n"
        + _one_per_line(stale)
    )
