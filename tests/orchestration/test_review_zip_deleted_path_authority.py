"""R-0837, SECOND SITE — the review-zip coordinator must not refuse a branch that DELETES a file.

`_assert_authority_equality` in `scripts/build_review_zip.py` recomputes the attestable set
INDEPENDENTLY of the producer, and unguarded it keeps a deleted path — which has no current content
and so is absent from the producer's authority set — making the equality it then demands
unsatisfiable and refusing the whole package with
`authority set != attestable ReviewSubject paths`.

The deleted path loses NO coverage by leaving that set: it is attested by its tombstone,
`ReviewFileV1.base_sha256`, whose own docstring says recording a removed file is the POINT.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from packages.orchestration.archive_plan import ArchivePlanError
from packages.orchestration.review_subject import (
    KIND_DELETED,
    KIND_REGULAR,
    ReviewFileV1,
    ReviewSubjectV1,
)

#: `scripts/` is not on the suite's default import path, so the repository's own copy is put there
#: — derived from this file's location, never from a hard-coded absolute path.
_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

LIVE_A = "src_pkg/alpha.py"
LIVE_B = "src_pkg/beta.py"
DELETED = "src_pkg/gamma.py"


class _StagedWithoutReports:
    """A staged byte map holding NO optional report, so ONLY the attestable-subject comparison of
    `_assert_authority_equality` is exercised."""

    def load_json(self, name: str):
        return None


def _subject_with_one_deletion() -> ReviewSubjectV1:
    """Two MODIFIED source files that still have content, and one DELETED file that does not."""
    return ReviewSubjectV1(
        base_commit="a" * 40,
        head_commit="b" * 40,
        base_is_ancestor=True,
        files=(
            ReviewFileV1(path=LIVE_A, status="modified", base_sha256="1" * 64,
                         current_sha256="2" * 64, kind=KIND_REGULAR),
            ReviewFileV1(path=LIVE_B, status="modified", base_sha256="3" * 64,
                         current_sha256="4" * 64, kind=KIND_REGULAR),
            # The tombstone shape: a base hash to attest what it WAS, and no current content.
            ReviewFileV1(path=DELETED, status="deleted", base_sha256="5" * 64,
                         current_sha256=None, kind=KIND_DELETED),
        ),
    )


class TestDeletedPathIsNotDemandedOfTheAuthoritySet:
    def test_a_deleted_path_does_not_block_the_package(self):
        """THE REGRESSION: the producer's authority set holds only the two live paths, and the
        coordinator must AGREE rather than refuse. This is the assertion that fails unguarded."""
        import build_review_zip

        build_review_zip._assert_authority_equality(
            authority={LIVE_A, LIVE_B},
            subject=_subject_with_one_deletion(),
            content_proof=None,
            staged=_StagedWithoutReports(),
        )

    def test_a_genuinely_missing_live_path_still_blocks(self):
        """THE DISCRIMINATOR: a LIVE attestable path absent from the authority set is a real
        disagreement and must still be refused. Without this test the regression above is equally
        satisfied by deleting the check, and a guard that cannot tell a fix from a deletion proves
        nothing."""
        import build_review_zip

        with pytest.raises(ArchivePlanError) as excinfo:
            build_review_zip._assert_authority_equality(
                authority={LIVE_A},
                subject=_subject_with_one_deletion(),
                content_proof=None,
                staged=_StagedWithoutReports(),
            )

        assert "authority set != attestable ReviewSubject paths" in str(excinfo.value)
        # It names the LIVE path it actually missed. What the message says about the DELETED path
        # is the guard's business, not this test's: asserting on it here would make the
        # discriminator fail under the mutation too, and then it could no longer tell a repaired
        # guard apart from a deleted check.
        assert LIVE_B in str(excinfo.value)
