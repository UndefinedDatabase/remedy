"""Deterministic documentation consistency checks.

Documentation drifts silently; these assertions make it fail loudly. They read only
checked-in files — no network, no provider call.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
FEATURES = REPO / "docs" / "roadmap" / "features"
STATUS = REPO / "docs" / "roadmap" / "STATUS.md"

FEATURE_FILE_RE = re.compile(r"\AT(\d{1,2})_F(\d{3})\.md\Z")
STATUS_LINE_RE = re.compile(r"^- \[[ ~x]\] F(\d{3}) — ")
TIER_HEADING_RE = re.compile(r"^#+\s*Tier\s*(\d{1,2})", re.IGNORECASE)

TOTAL_FEATURES = 250

#: Documents that must never contain a stale claim.
PRIMARY_DOCS = [
    REPO / "README.md",
    REPO / "AGENTS.md",
    REPO / "docs" / "README.md",
    STATUS,
    REPO / "docs" / "roadmap" / "ROADMAP.md",
]


def _feature_ids() -> dict[int, tuple[int, Path]]:
    """{feature number: (tier, path)} from the feature detail filenames."""
    found: dict[int, tuple[int, Path]] = {}
    for path in sorted(FEATURES.glob("*.md")):
        m = FEATURE_FILE_RE.match(path.name)
        assert m, f"unexpected feature filename: {path.name}"
        num = int(m.group(2))
        assert num not in found, f"duplicate feature detail file for F{num:03d}"
        found[num] = (int(m.group(1)), path)
    return found


def _status_tiers() -> dict[int, int]:
    """{feature number: tier} from STATUS.md, using its Tier headings."""
    tiers: dict[int, int] = {}
    tier = -1
    for line in STATUS.read_text(encoding="utf-8").splitlines():
        heading = TIER_HEADING_RE.match(line.strip())
        if heading:
            tier = int(heading.group(1))
            continue
        m = STATUS_LINE_RE.match(line)
        if m:
            num = int(m.group(1))
            assert num not in tiers, f"duplicate STATUS entry for F{num:03d}"
            tiers[num] = tier
    return tiers


class TestFeatureLedger:
    def test_there_are_250_unique_feature_detail_files(self):
        ids = _feature_ids()
        assert len(ids) == TOTAL_FEATURES

    def test_there_are_250_unique_status_entries(self):
        assert len(_status_tiers()) == TOTAL_FEATURES

    def test_no_feature_id_is_missing(self):
        missing = sorted(set(range(1, TOTAL_FEATURES + 1)) - set(_feature_ids()))
        assert missing == [], f"feature detail files missing for {missing}"
        missing_status = sorted(
            set(range(1, TOTAL_FEATURES + 1)) - set(_status_tiers()))
        assert missing_status == [], f"STATUS entries missing for {missing_status}"

    def test_the_filename_tier_matches_the_status_tier(self):
        status = _status_tiers()
        drift = [
            f"F{num:03d}: file says tier {tier}, STATUS says tier {status[num]}"
            for num, (tier, _path) in _feature_ids().items()
            if num in status and status[num] >= 0 and status[num] != tier
        ]
        assert drift == [], drift


class TestPrimaryDocsAreHonest:
    def test_no_doc_still_claims_150_feature_files(self):
        offenders = [
            str(p.relative_to(REPO)) for p in PRIMARY_DOCS
            if p.is_file() and re.search(r"150[- ]feature|150 feature detail",
                                         p.read_text(encoding="utf-8"))
        ]
        assert offenders == [], offenders

    def test_no_doc_references_a_missing_roadmap_ledger(self):
        offenders = [
            str(p.relative_to(REPO)) for p in PRIMARY_DOCS
            if p.is_file() and "ROADMAP_LEDGER" in p.read_text(encoding="utf-8")
            and not (REPO / ".agent" / "ROADMAP_LEDGER.md").exists()
        ]
        # AGENTS.md may explain that there is NO ledger; a bare reference to a file
        # that does not exist is what must not survive.
        for path in offenders:
            text = (REPO / path).read_text(encoding="utf-8")
            assert "There is no separate" in text, f"{path} points at a missing ledger"

    def test_no_agent_state_calls_the_deleted_f007_branch_current(self):
        for name in ("plan.md", "live_review.md", "context.md"):
            path = REPO / ".agent" / name
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for line in text.splitlines():
                if "feature/f007-runtime-harness" in line:
                    assert ("merged" in line.lower() or "deleted" in line.lower()
                            or "PR #127" in line), (
                        f".agent/{name} still presents the deleted F007 branch as "
                        f"current: {line.strip()}")

    def test_the_readme_does_not_call_built_systems_future(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        for claim in ("Patch application is not implemented",
                      "Agent loops are not implemented",
                      "Configuration system is not implemented",
                      "runtimes/     # (future)",
                      "verification/ # (future)"):
            assert claim not in readme, f"README still claims: {claim!r}"

    def test_the_readme_reports_the_accepted_foundation_and_no_later_feature(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        # F007 is accepted; nothing may still call it pending...
        assert "acceptance still pending" not in readme
        assert "not accepted yet" not in readme
        assert "accepted foundation" in readme
        # F010 is accepted; nothing may still call it pending...
        assert "not yet externally accepted" not in readme
        # ...and nothing after it may be claimed as existing.
        assert "F008" not in readme or "not implemented" in readme
        assert "F011" not in readme or "not implemented" in readme

    def test_the_f010_documents_describe_all_three_scopes(self):
        status = STATUS.read_text(encoding="utf-8")
        f010 = re.search(r"^- \[x\] F010 —.*$", status, re.M)
        assert f010 and "call/task/job post-mortems" in f010.group(0), (
            "STATUS must name all three post-mortem scopes")

        feature = (REPO / "docs" / "roadmap" / "features" / "T0_F010.md").read_text(
            encoding="utf-8")
        assert "`call` | `task` | `job`" in feature, (
            "the record section must list every scope")
        assert "The three scopes — `call`, `task` and `job`" in feature, (
            "the stats section must describe every scope")

    def test_status_marks_f007_and_f010_accepted_and_nothing_after_them(self):
        text = STATUS.read_text(encoding="utf-8")
        f007 = re.search(r"^- \[x\] F007 — Runtime harness.*$", text, re.M)
        assert f007, "F007 is externally accepted and must be checked off"
        assert "2e820a4dbf9842cf" in f007.group(0), "the accepted Evidence job is missing"
        assert "ACCEPTED" in f007.group(0)
        # F010 is externally accepted: `[x]`, with the Evidence job that was accepted.
        f010 = re.search(r"^- \[x\] F010 — Automatic failure post-mortems.*$", text, re.M)
        assert f010, "F010 is externally accepted and must be checked off"
        assert not re.search(r"^- \[~\] F010 —", text, re.M)
        assert "01363c70e13046e2" in f010.group(0), "the accepted Evidence job is missing"
        assert "PASS_WITH_RISKS — ACCEPTED" in f010.group(0)
        assert "2026-07-14" in f010.group(0), "the acceptance date is missing"
        # ...and nothing after it has been started.
        assert re.search(r"^- \[ \] F008 —", text, re.M)
        assert re.search(r"^- \[ \] F011 —", text, re.M)


class TestPrimaryDocLinksResolve:
    @pytest.mark.parametrize("doc", [p.name for p in PRIMARY_DOCS])
    def test_every_relative_markdown_link_exists(self, doc):
        path = next(p for p in PRIMARY_DOCS if p.name == doc)
        if not path.is_file():
            pytest.skip(f"{doc} does not exist")
        text = path.read_text(encoding="utf-8")
        broken = []
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).exists():
                broken.append(target)
        assert broken == [], f"{doc} has broken links: {broken}"
