"""Guard: the apply fold can emit `partial` beside its three confident labels (finding R-0738).

`fold_task_apply_states` in `packages/orchestration/proof_chain.py` folds a task's changes to ONE
apply label. These checks read the SHIPPED fold's AST rather than a recollection of it: the
emitted labels are derived from every string literal it assigns to `state_by_task[...]`, and the
fold must not answer by membership of its `apply_states` list. The half of this guard that read
the old cockpit's popover and tasks card went with the old face (amend1015f D27); this half moved
here from `tests/ui_contracts/test_apply_state_partial.py`.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
# The fold's home: it lives beside the `ProofChange.apply_state` field it reads so the run
# report can import it too.
FOLD_MODULE = REPO_ROOT / "packages" / "orchestration" / "proof_chain.py"

FOLD_FUNCTION = "fold_task_apply_states"
FOLD_MAP = "state_by_task"
# The local list of per-change apply states the fold decides from.
FOLD_STATE_LIST = "apply_states"


def fold_apply_function() -> ast.FunctionDef:
    """The AST of the shipped fold, or an assertion naming what is missing."""
    tree = ast.parse(FOLD_MODULE.read_text())
    fold = next(
        (
            node for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == FOLD_FUNCTION
        ),
        None,
    )
    assert fold is not None, (
        f"{FOLD_MODULE.name} defines no function named {FOLD_FUNCTION}; this guard would "
        f"measure the popover against an empty backend set and could not fail"
    )
    return fold


def fold_apply_labels() -> set[str]:
    """Every string literal the SHIPPED fold can assign to `state_by_task[...]`.

    Derived from the AST rather than listed, so a fifth state added on the Python side
    alone widens this set and reddens the agreement test below instead of reaching an
    operator as "Unknown".
    """
    labels: set[str] = set()
    for node in ast.walk(fold_apply_function()):
        if not isinstance(node, ast.Assign):
            continue
        if not (isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == FOLD_MAP
            ):
                labels.add(node.value.value)
    return labels


def fold_membership_tests_over_apply_states() -> set[str]:
    """Every literal the fold tests for MEMBERSHIP of its `FOLD_STATE_LIST` local.

    An AST predicate, not a text search: the fold's WHY comment quotes the membership
    test it replaced, so a grep over the source would be answered by the prose that
    explains the repair rather than by code (the R-0584 class, on the Python side).
    The agreement fold compares each state one at a time and so puts nothing here;
    `s in ("applied", "reverted")` inside a generator is a membership test over a
    TUPLE, not over the list, and is deliberately out of scope.
    """
    found: set[str] = set()
    for node in ast.walk(fold_apply_function()):
        if not isinstance(node, ast.Compare):
            continue
        for op, comparator in zip(node.ops, node.comparators):
            if (
                isinstance(op, ast.In)
                and isinstance(comparator, ast.Name)
                and comparator.id == FOLD_STATE_LIST
                and isinstance(node.left, ast.Constant)
                and isinstance(node.left.value, str)
            ):
                found.add(node.left.value)
    return found


class TestTheDerivationIsNotVacuous:
    def test_the_ast_derivation_finds_labels_at_all(self):
        assert fold_apply_labels(), (
            f"no label found in {FOLD_FUNCTION}; the walk names its own file and function, "
            f"and a moved fold would leave every check below measuring an empty set")


class TestTheBackendCanReallyEmitPartial:
    """Asserted against the SOURCE of the fold, not against a recollection of it."""

    def test_the_fold_assigns_the_partial_label(self):
        labels = fold_apply_labels()
        assert "partial" in labels, (
            f"{FOLD_FUNCTION} in {FOLD_MODULE.name} assigns {sorted(labels)} to {FOLD_MAP} "
            f"and never 'partial', so a task whose changes disagree is folded to one of "
            f"the confident answers again — the whole of finding R-0738"
        )

    def test_the_three_confident_labels_survive_beside_it(self):
        labels = fold_apply_labels()
        for expected in ("applied", "reverted", "not_applied"):
            assert expected in labels, (
                f"{FOLD_FUNCTION} no longer emits '{expected}'; the partial state was "
                f"added to model a case the three confident answers could not, never to "
                f"replace one of them"
            )

    def test_the_fold_no_longer_answers_by_membership(self):
        # Read as an AST PREDICATE rather than as a text grep, for the reason every
        # guard in this directory strips comments before asserting: the fold's own WHY
        # comment QUOTES the membership test it replaced, so `'if "applied" in
        # apply_states' not in source` fails on the prose that explains the repair.
        offenders = sorted(fold_membership_tests_over_apply_states())
        assert not offenders, (
            f"{FOLD_FUNCTION} in {FOLD_MODULE.name} still tests {offenders} for MEMBERSHIP "
            f"of apply_states; that reports 'applied' when a single change of many "
            f"applied, which is the exact reading the agreement fold replaced"
        )
