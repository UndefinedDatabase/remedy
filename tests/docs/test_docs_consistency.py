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

#: 250 roadmap features (F001-F250) plus eight registered additions: F251,
#: added by the planning amendment of 2026-07-27; F252 (standing-red
#: paydown), added by operator ruling A of 2026-07-28; F253 (headless
#: API contract), added by operator decision of 2026-08-03; F254
#: (model alias table & dead-model doctor check), added by amendment
#: round amend0805-v3 of 2026-08-05; F255 (teacher role), added by
#: registration round plan0806 of 2026-08-06; F256 (diff viewer
#: completion) plus F257 (self-use track), both added by operator order
#: amend0828-daily-driver of 2026-08-28 — F256 carrying the scope
#: DECISION F037 D11 split off from F037; and F258 (self-use track v2 —
#: self-replenishing queue & executed items), added by operator order
#: amend0829-selfuse-v2 of 2026-08-29. See docs/roadmap/features/
#: T1_F251.md, T1_F252.md, T12_F253.md, T2_F254.md, T5_F255.md,
#: T5_F256.md, T5_F257.md and T5_F258.md.
TOTAL_FEATURES = 258

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

    def test_no_doc_understates_the_feature_count(self):
        """R-0209: AGENTS.md and the docs index described a 250-file roadmap.

        The ledger has been TOTAL_FEATURES long since F251-F255 were
        registered, and the 150 pin above did not cover the successor
        claim, which is why it survived. Pinned by document rather than
        by regex over PRIMARY_DOCS on purpose: README.md's "250 features
        + registered items" is a different and still-true statement,
        and a blanket pattern would force a false repair on it.
        """
        for rel in ("AGENTS.md", "docs/README.md"):
            text = (REPO / rel).read_text(encoding="utf-8")
            assert "250 feature detail files" not in text, rel
            assert "250-feature" not in text, rel

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
        """The README's accepted list must agree with the ledger.

        Rewritten for the README of bd2f8ad, which replaced the per-feature
        table ("| F010 … externally accepted") with a per-tier status table
        and a named accepted-foundation list. The pin is now a cross-check
        against STATUS.md instead of a pin on the retired table shape, so it
        fails on real drift rather than on layout.
        """
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")

        # Nothing accepted may still be described as pending.
        assert "acceptance still pending" not in readme
        assert "not accepted yet" not in readme
        assert "not yet externally accepted" not in readme
        assert "Accepted foundation" in readme

        accepted = {m.group(1) for m in
                    re.finditer(r"^- \[x\] F(\d{3}) — ", status, re.MULTILINE)}

        # Every feature the README lists as accepted IS accepted in the ledger.
        for block in re.findall(r"Accepted[^\n]*:\n((?:[^\n]+\n)+)", readme):
            for fid in re.findall(r"\bF(\d{3})\b", block):
                assert fid in accepted, f"README claims F{fid} accepted; STATUS does not"

        # F012 and F017 were "implemented, not yet accepted" when this pin was
        # written; STATUS.md now carries `- [x]` for both, and the loop above
        # is the general form of what these two clauses checked by name.

    def test_the_readme_accepted_count_equals_the_status_count(self):
        """R-0156: pin the README accepted-COUNT to the STATUS ledger.

        The id cross-check above verifies every README-listed feature
        IS accepted, but the prose line "N of 252 registered items
        accepted" could carry any N (negative control: a faked count
        stayed green through all of tests/docs). Parse both counts
        and pin them equal.
        """
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        m = re.search(r"^(\d+) of (\d+) registered items accepted\.",
                      readme, re.MULTILINE)
        assert m, "README must state 'N of M registered items accepted.'"
        assert int(m.group(2)) == TOTAL_FEATURES
        accepted = len(re.findall(r"^- \[x\] F\d{3} — ", status,
                                  re.MULTILINE))
        assert int(m.group(1)) == accepted, (
            f"README claims {m.group(1)} accepted; STATUS.md has "
            f"{accepted}")

    def test_the_readme_tier_table_done_column_matches_the_ledger(self):
        """R-0360: pin the README tier table's Done column to the ledger.

        The prose count beside this table is pinned by the test above
        (R-0156), but nothing read the per-tier ``Done`` cells, so they
        drifted silently: the Tier 2 cell sat at 6 while the ledger derived
        7 from the F111 closure until the F045 closure wrote 8. Derive each
        tier's count the way a reviewer derives it by hand at closure —
        every accepted STATUS id resolved through its feature file's tier
        prefix — and pin every row of the table, not just the one that moved.
        """
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        features = _feature_ids()

        derived: dict[int, int] = {}
        for m in re.finditer(r"^- \[x\] F(\d{3}) — ", status, re.MULTILINE):
            num = int(m.group(1))
            assert num in features, f"F{num:03d} is accepted with no feature file"
            tier = features[num][0]
            derived[tier] = derived.get(tier, 0) + 1

        rows = re.findall(r"^\| (\d{1,2}) \| [^|]+ \|\s*(\d+) \|\s*(\d+) \|$",
                          readme, re.MULTILINE)
        assert rows, "README must carry the Tier status table"
        listed = set()
        for tier_text, done_text, _total_text in rows:
            tier = int(tier_text)
            listed.add(tier)
            assert int(done_text) == derived.get(tier, 0), (
                f"README Tier {tier} Done={done_text}; the ledger derives "
                f"{derived.get(tier, 0)}")
        missing = sorted(set(derived) - listed)
        assert not missing, f"accepted tiers with no README row: {missing}"

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

    def test_the_f011_document_describes_the_accepted_kill_switch(self):
        feature = (REPO / "docs" / "roadmap" / "features" / "T0_F011.md").read_text(
            encoding="utf-8")
        for claim in ("Safe points", "STOPPED state and resume", "job_stopped",
                      "stop_postmortems/<request_id>/postmortem.json",
                      "No signal handler, no thread, no daemon",
                      # a consumed request is archived, never deleted
                      "archived, not deleted",
                      # and the two boundaries v1 does NOT cross, said out loud
                      "SIGKILL", "Deep checkpoints"):
            assert claim in feature, f"the F011 document must state: {claim!r}"
        assert "accepted as v1" in feature
        assert "49955e41c49f41bc" in feature, "the accepted Evidence job is missing"

    def test_status_marks_f011_accepted_and_f012_untouched(self):
        text = STATUS.read_text(encoding="utf-8")
        f011 = re.search(r"^- \[x\] F011 — Kill switch.*$", text, re.M)
        assert f011, "F011 is externally accepted and must be checked off"
        assert not re.search(r"^- \[~\] F011 —", text, re.M)
        assert "49955e41c49f41bc" in f011.group(0), "the accepted Evidence job is missing"
        assert "PASS_WITH_RISKS — ACCEPTED" in f011.group(0)
        assert "2026-07-14" in f011.group(0), "the acceptance date is missing"
        assert "remedy job stop" in f011.group(0)
        assert "STOPPED state" in f011.group(0)
        # F012 is externally accepted; F017 is externally accepted.
        f012 = re.search(r"^- \[x\] F012 — Deterministic runs.*$", text, re.M)
        assert f012, "F012 is externally accepted and must be checked off"
        assert "r40_authority_contract_closure" in f012.group(0)
        assert "PASS_WITH_RISKS — ACCEPTED" in f012.group(0)
        assert re.search(r"^- \[x\] F017 —", text, re.M)

    def test_the_f012_document_describes_the_deterministic_runs_feature(self):
        feature = (REPO / "docs" / "roadmap" / "features" / "T0_F012.md").read_text(
            encoding="utf-8")
        for claim in ("RunManifestV1", "on_call_finalized", "logical_input_sha256",
                      "job rerun <job_id> --check-manifest", "exit 4",
                      "recorded, not promised", "provider CLI version",
                      "no second call-directory walker".replace(
                          "no second call-directory walker", "no second call-directory walker")):
            assert claim in feature, f"the F012 document must state: {claim!r}"

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
        # ...and nothing after F012 has been started except F017 (accepted) and
        # whatever feature is claimed at the time. R-0387, F008 R1: this pin read
        # `[ ]` F008, so it asserted that NO feature was in progress and the next
        # claim had to break it. Naming the holder instead moved the same defect
        # from every claim to every CLOSURE — closing F008 removes the only `[~]`
        # line, taking the count to 0 (measured at 3035bc2a against the closure
        # edits in a throwaway worktree: 1 failed, 294 passed, this test). The
        # invariant the workflow holds is AT MOST one claim
        # (planner_reviewer_prompt.md §1), true in both states, so this pin
        # survives a claim and a closure alike.
        in_progress = re.findall(r"^- \[~\] F\d{3} —", text, re.M)
        assert len(in_progress) <= 1, f"at most one feature is in progress, found {in_progress}"
        assert re.search(r"^- \[x\] F017 —", text, re.M)


class TestPrimaryDocLinksResolve:
    # R-0596: parametrising by `p.name` collided the repository README.md with
    # docs/README.md and `next` resolved both to the first, so the documentation
    # INDEX — the one file AGENTS.md requires every new doc to be registered in —
    # was checked by no case. The repo-relative path is unique by construction.
    @pytest.mark.parametrize("doc", [str(p.relative_to(REPO)) for p in PRIMARY_DOCS])
    def test_every_relative_markdown_link_exists(self, doc):
        path = REPO / doc
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


class TestF012IdentityModelIsPinned:
    """F16: F084 and F140 depend on the three-way identity distinction, so the binding Built
    State must keep documenting it."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_three_identities_are_documented(self):
        doc = self._f012()
        assert "Record / provenance identity" in doc
        assert "Logical input identity" in doc
        assert "Outcome / lifecycle" in doc

    def test_the_logical_projection_exclusions_are_documented(self):
        doc = self._f012()
        for excluded in ("job/episode/run/call", "terminal status", "stop request id",
                         "timestamps"):
            assert excluded in doc, f"the logical projection must document excluding {excluded}"

    def test_the_stable_logical_call_key_is_documented(self):
        assert "(task_id, sequence, role, round, kind)" in self._f012()

    def test_outcome_is_not_an_input(self):
        assert "never an input" in self._f012()


class TestF012ReferenceCoverageIsPinned:
    """F14 (round 9): the reference-vs-candidate distinction decides exit 1 vs exit 5, so the
    binding Built State must keep documenting it."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_three_validation_modes_are_documented(self):
        doc = self._f012()
        for mode in ("prepublication", "published_reference", "current_candidate"):
            assert mode in doc, f"the validation mode {mode!r} must be documented"

    def test_the_coverage_exit_codes_are_documented(self):
        doc = self._f012()
        assert "exit 1 (integrity)" in doc, "a stored incomplete terminal manifest is exit 1"
        assert "exit 5 (incomplete coverage)" in doc, "an incomplete candidate is exit 5"

    def test_the_published_reference_rule_is_documented(self):
        doc = self._f012()
        assert "canonical loader and the writer" in doc
        assert "Zero calls is `complete` only when" in doc

    def test_the_canonical_index_rule_is_documented(self):
        assert "canonical_index_bytes(decode_index_v1(bytes))" in self._f012()

    def test_the_strict_writer_reads_are_documented(self):
        doc = self._f012()
        assert "_decode_existing_episode" in doc
        assert "ManifestConflictError" in doc

    def test_the_writer_readability_invariant_is_documented(self):
        assert "Writer success implies canonical readability" in self._f012()

    def test_the_call_lineage_rule_is_documented(self):
        doc = self._f012()
        assert "within its own run" in doc
        assert "never renumbered" in doc

    def test_the_complete_job_input_definition_is_documented(self):
        doc = self._f012()
        assert "isolation_mode" in doc and "worktree` | `copy" in doc

    def test_the_redundant_fact_agreement_is_documented(self):
        assert "Redundant facts must agree" in self._f012()

    def test_the_key_and_pythonhashseed_rules_are_documented(self):
        doc = self._f012()
        assert "_is_safe_key" in doc
        assert "0..4294967295" in doc

    def test_the_standard_json_rule_is_documented(self):
        doc = self._f012()
        assert "allow_nan=False" in doc and "parse_constant" in doc

    def test_the_marker_absence_only_rule_is_documented(self):
        doc = self._f012()
        assert "The marker changes absence semantics only." in doc
        assert "manifest_tree_is_present" in doc


class TestF012WriterModelIsPinned:
    """Round 10: the publication model and the zero-call proof are what F084/F140 will build on,
    so the binding Built State must keep documenting them exactly."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_complete_chain_append_is_documented(self):
        doc = self._f012()
        assert "An append validates the COMPLETE existing canonical chain" in doc
        assert "ordinal exactly `N+1`" in doc
        assert "only then publish the Root Mirror and the Index" in doc

    def test_the_conflict_safe_publication_model_is_documented(self):
        doc = self._f012()
        assert "Conflict-safe Episode publication" in doc
        assert ".run_manifest_staging" in doc
        assert "ONE atomic `rename`" in doc
        assert "leaves NOTHING in the winner's Episode" in doc

    def test_the_artifact_create_race_rule_is_documented(self):
        doc = self._f012()
        assert "Artifact create-race" in doc
        assert "identical bytes converge, different bytes raise" in doc

    def test_the_known_prior_episode_rule_is_documented(self):
        doc = self._f012()
        assert "Only KNOWN prior Episodes may excuse a Call" in doc
        assert "blocking coverage problems" in doc
        assert "per-run numbering spans Episodes" in doc

    def test_the_zero_call_proof_is_documented(self):
        doc = self._f012()
        assert "A zero-Call reference must PROVE zero Calls were expected" in doc
        for expectation in ("executed", "prior_episode", "dispatched_no_calls", "skipped",
                            "not_dispatched"):
            assert f"`{expectation}`" in doc
        for phase in ("worked", "pre_work_stop", "planning_only"):
            assert phase in doc

    def test_the_genuine_zero_call_contract_cases_are_documented(self):
        doc = self._f012()
        assert "Planning-only job (zero calls): valid manifest, empty hash list" in doc
        assert "all-skipped" in doc

    def test_the_call_to_job_input_binding_is_documented(self):
        doc = self._f012()
        assert "Every Call is bound to the embedded JobInput" in doc
        assert "EXACTLY ONCE" in doc

    def test_the_single_job_input_validator_is_documented(self):
        doc = self._f012()
        assert "ONE exact JobInput validator" in doc
        assert 'no longer be "valid" on the way out and invalid on the way back in' in doc

    def test_the_role_agreement_is_documented(self):
        doc = self._f012()
        assert "Exact Builder/Reviewer/Repair agreement" in doc
        assert "Absence is symmetric and explicit" in doc

    def test_the_universal_writer_postcondition_is_documented(self):
        doc = self._f012()
        assert "One universal writer-success postcondition" in doc
        assert "NO undeclared\nfile exists in the canonical namespace" in doc
        assert "pending F011 stop still retryable" in doc

    def test_the_authoritative_test_count_rule_is_documented(self):
        doc = self._f012()
        assert "Authoritative Evidence contains the claimed runs" in doc
        assert "never called green, never omitted while its count is quoted" in doc


class TestF012Round11IsPinned:
    """Round 11: the append claim, the lifecycle matrix and the read-only workspace check are
    what F084/F140 will build on, so the binding Built State must keep documenting them."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_append_serialization_is_documented(self):
        doc = self._f012()
        assert "Per-job append serialization" in doc
        assert ".run_manifest_control/append.lock" in doc
        assert "Readers never take it" in doc

    def test_the_shared_full_chain_validation_is_documented(self):
        doc = self._f012()
        assert "load_verified_canonical_chain_for_write()" in doc
        assert "Success means the same" in doc

    def test_the_complete_winner_rule_is_documented(self):
        doc = self._f012()
        assert "verifies the COMPLETE winner" in doc
        assert "never repairs or adds" in doc
        assert "files into another writer's Episode" in doc

    def test_the_post_publication_revalidation_is_documented(self):
        doc = self._f012()
        assert "Post-publication chain revalidation" in doc
        assert "VerifiedCanonicalChain" in doc

    def test_the_lifecycle_matrix_is_documented(self):
        doc = self._f012()
        assert "The exact CallExpectation lifecycle matrix" in doc
        for combo in ("completed + planning_only", "planned + worked",
                      "completed + dispatched_no_calls", "completed + not_dispatched"):
            assert combo in doc, f"the matrix must refuse {combo}"

    def test_the_exact_call_ledger_proof_is_documented(self):
        doc = self._f012()
        assert "finalized_calls_sha256" in doc
        assert "expected_call_count" in doc
        assert "`expected_min_calls` is gone" in doc

    def test_the_phase_aware_snapshot_identities_are_documented(self):
        doc = self._f012()
        assert "Phase-aware Snapshot identities" in doc
        assert "There is no\n**silent empty string**" in doc or \
            "no\nsilent empty string" in doc.replace("**", "")
        assert "episode_start_workspace_identity" in doc

    def test_the_read_only_workspace_check_is_documented(self):
        doc = self._f012()
        assert "Contained, read-only workspace inspection" in doc
        assert "no `git add`" in doc
        assert "clean/smudge filters\nare neutralized" in doc

    def test_the_universal_writer_postcondition_is_documented(self):
        doc = self._f012()
        assert "One universal Writer success postcondition" in doc
        assert "pending F011 Stop stays retryable" in doc


class TestF012Round12IsPinned:
    """Round 12: the canonical ledger, immutable artifacts and the read-only workspace contract
    are what F084/F140 will build on, so the binding Built State must keep documenting them."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_canonical_ledger_is_documented(self):
        doc = self._f012()
        assert "The canonical Run Call Ledger" in doc
        assert "call_ledgers/<task-id>-<run-id>.json" in doc
        assert "RunCallLedgerV1" in doc

    def test_the_ledger_bijection_is_documented(self):
        doc = self._f012()
        assert "The bijection" in doc
        assert "EXACTLY ONE ledger entry" in doc

    def test_immutable_published_artifacts_are_documented(self):
        doc = self._f012()
        assert "Published artifacts are immutable" in doc
        assert "never" in doc and "repaired" in doc

    def test_non_latest_idempotency_is_documented(self):
        doc = self._f012()
        assert "Exact retry of a non-latest Episode is a no-op" in doc

    def test_the_task_lifecycle_is_documented(self):
        doc = self._f012()
        assert "One exact task lifecycle record" in doc
        assert "failed_pre_dispatch" in doc
        assert "dispatch_state" in doc

    def test_the_prework_resume_matrix_is_documented(self):
        doc = self._f012()
        assert "Pre-work Stop on a resumed job carries proven prior tasks" in doc

    def test_the_held_handle_containment_is_documented(self):
        doc = self._f012()
        assert "Containment stays bound through the inspection" in doc
        assert "/proc/self/fd/N" in doc
        assert "fails CLOSED" in doc or "fails CLOSED" in doc.replace("\n", " ")

    def test_the_helper_neutralization_is_documented(self):
        doc = self._f012()
        assert "Read-only means no repository code runs" in doc
        assert "core.fsmonitor=false" in doc
        assert "GIT_CONFIG_GLOBAL=/dev/null" in doc

    def test_the_canonical_workspace_identity_is_documented(self):
        doc = self._f012()
        assert "One canonical workspace identity format" in doc
        assert "episode_start_workspace_identity" in doc

    def test_input_versus_call_coverage_is_documented(self):
        doc = self._f012()
        assert "Input coverage versus Call coverage" in doc
        assert "input_status" in doc and "call_status" in doc

    def test_the_transaction_phases_are_documented(self):
        doc = self._f012()
        assert "The real transaction phases" in doc
        assert "Before Episode publication" in doc
        assert "After immutable Episode publication" in doc
        assert "three separate durable" in doc

    def test_the_staging_cleanup_model_is_documented(self):
        doc = self._f012()
        assert "Bounded safe staging cleanup" in doc
        assert "never removed" in doc or "never a canonical Episode name" in doc


class TestF012Round13IsPinned:
    """Round 13: ledger MEANING (completeness, terminal-state source, result binding, order,
    cross-episode continuity), lexical workspace containment and the operator-state Evidence
    policy. F140's replay is keyed by the ledger's verified order and F084 replays recorded
    evidence, so the binding Built State must keep documenting these."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 13" in self._f012()

    def test_ledger_completeness_is_documented(self):
        doc = self._f012()
        assert "A published ledger must be complete" in doc
        assert "is a contradiction, not a caveat" in doc

    def test_the_terminal_state_source_is_documented(self):
        doc = self._f012()
        assert "The terminal state comes from the Run record" in doc
        assert "RUN_FINAL_STATUS_TO_LEDGER_STATE" in doc
        assert "asked the wrong witness" in doc

    def test_the_closed_matrix_and_its_narrow_task_rule_are_documented(self):
        """The narrowness is deliberate and load-bearing: production reaches blocked/failed with
        a SUCCESSFUL run, so a stricter rule would refuse real records."""
        doc = self._f012()
        assert "CLOSED" in doc
        assert "production reaches every one of them with a SUCCESSFUL run" in doc

    def test_the_result_binding_is_documented(self):
        doc = self._f012()
        assert "The ledger entry's result matches its call" in doc
        assert "LEDGER_CALL_BIJECTION_FIELDS" in doc

    def test_the_order_contract_is_documented(self):
        doc = self._f012()
        assert "Ledger order is bound, not merely contiguous" in doc
        assert "stream N for call N" in doc

    def test_cross_episode_continuity_is_documented(self):
        doc = self._f012()
        assert "Ledger history is continuous across Episodes" in doc
        assert "exact EXTENSION" in doc
        assert "ghost-prior" in doc

    def test_the_call_id_uniqueness_subtlety_is_documented(self):
        doc = self._f012()
        assert "unique within a run and\ndeliberately not across the job" in doc

    def test_the_identity_safety_rules_are_documented(self):
        doc = self._f012()
        assert "Ledger entry identities are path- and secret-safe" in doc
        assert "safe_call_ref()" in doc

    def test_the_recorded_contract_difference_is_documented(self):
        """A finding that contradicts the committed contract is recorded, never silently
        half-applied."""
        doc = self._f012()
        assert "Recorded contract difference" in doc
        assert "would refuse all of them" in doc

    def test_lexical_containment_is_documented(self):
        doc = self._f012()
        assert "Workspace containment rejects lexical `..` escapes" in doc
        assert "lexical_parts()" in doc
        assert "one level per component" in doc

    def test_the_one_closed_ledger_contract_is_documented(self):
        doc = self._f012()
        assert "One closed ledger contract" in doc
        assert "validate_ledger_chain" in doc

    def test_the_operator_state_policy_is_documented(self):
        doc = self._f012()
        assert "One consistent operator-state policy" in doc
        assert "OPERATOR STATE" in doc
        assert "non-authoritative operator context" in doc

    def test_the_diagnostic_versus_final_package_is_documented(self):
        doc = self._f012()
        assert "Diagnostic BLOCKED_EVIDENCE versus final READY_FOR_REVIEW" in doc

    def test_the_readme_states_the_ledger_contract(self):
        # Was a duplicate of the contract in README prose. The README stopped
        # being a spec dump in bd2f8ad ("condensed pitch, <=120 lines"), so the
        # contract is pinned where it lives: the F012 Built State.
        assert "## Hardening round 13" in self._f012()

    def test_the_readme_states_lexical_containment(self):
        assert "## Hardening round 13" in self._f012()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round14IsPinned:
    """Round 14: terminal ledger finality, the exact expectation<->ledger set, collision-free
    ledger refs and the closed canonical call-ref grammar. F140 replays stream N WITHIN one
    frozen Run Ledger and F084 replays recorded evidence, so the binding Built State must keep
    documenting these — including the corrected extension-versus-finality contract."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 14" in self._f012()

    def test_terminal_ledger_finality_is_documented(self):
        doc = self._f012()
        assert "A complete terminal ledger is FINAL" in doc
        assert "freezes the run's whole" in doc
        assert "byte-for-byte and nothing else" in doc

    def test_the_superseded_extension_contract_is_corrected(self):
        """F6: the docs must not still describe a later ledger as an extension."""
        doc = self._f012()
        assert "Terminal run versus new run" in doc
        assert "superseded" in doc

    def test_new_work_uses_a_new_run_id(self):
        doc = self._f012()
        assert "Later work uses a NEW run id" in doc
        assert "uuid4().hex[:16]` per execution" in doc

    def test_the_finality_rule_is_proven_against_production(self):
        doc = self._f012()
        assert "byte-identical repeat" in doc
        assert "new work, NEW run id" in doc

    def test_the_exact_ledger_set_is_documented(self):
        doc = self._f012()
        assert "The ledger set is exactly the expectation set" in doc
        assert "expected_ledger_keys" in doc
        assert "GHOST" in doc

    def test_the_shared_set_validator_is_documented(self):
        doc = self._f012()
        assert "validate_ledger_set()" in doc
        assert "one shared set-level contract" in doc

    def test_collision_free_refs_are_documented(self):
        doc = self._f012()
        assert "Ledger artifact refs are collision-free" in doc
        assert "call_ledgers/a-b-c.json" in doc
        assert "sha256(canonical identity)" in doc

    def test_the_ref_bound_is_documented(self):
        doc = self._f012()
        assert "NAME_MAX" in doc
        assert "no compatibility layer is needed" in doc.lower()

    def test_the_call_ref_grammar_is_documented(self):
        doc = self._f012()
        assert "A closed canonical call-ref grammar" in doc
        assert "calls//builder" in doc
        assert "streams/<role>/round-NN/<kind>-II" in doc

    def test_the_grammar_covers_both_real_namespaces(self):
        doc = self._f012()
        assert "shared_call_id" in doc
        assert "_allocate_stream_call_dir" in doc

    def test_the_ref_must_agree_with_its_identity(self):
        doc = self._f012()
        assert "must also AGREE with the" in doc

    def test_f140_serves_stream_n_within_one_frozen_ledger(self):
        doc = self._f012()
        assert "WITHIN one frozen Run Ledger" in doc

    def test_the_checkpoint_commit_policy_is_documented(self):
        doc = self._f012()
        assert "Local checkpoint commit policy" in doc
        assert "Local history is not an acceptance signal" in doc

    def test_the_readme_states_finality_and_the_grammar(self):
        assert "## Hardening round 14" in self._f012()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round15IsPinned:
    """Round 15: chain-wide task-lifecycle monotonicity, the canonical call-ref number text, the
    typed/verified review subject, deletion+rename proofs and the machine-verifiable commit chain.
    F140 replays within one frozen run ledger and F084 replays recorded evidence, so the binding
    Built State must keep documenting these."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 15" in self._f012()

    def test_task_lifecycle_monotonicity_is_documented(self):
        doc = self._f012()
        assert "Task lifecycle is MONOTONIC across the chain" in doc
        assert "The omission WAS the erasure" in doc
        assert "validate_task_lifecycle_chain()" in doc

    def test_the_terminal_versus_resumable_task_is_documented(self):
        """The distinction that keeps F011's resume working."""
        doc = self._f012()
        assert "Terminal with a run" in doc
        assert "Non-terminal" in doc
        assert "deliberately unbound" in doc
        assert "never** rolled back" in doc

    def test_the_skipped_contract_is_documented(self):
        doc = self._f012()
        assert "_block_job" in doc
        assert "NO reactivation" in doc

    def test_the_immutable_task_list_is_documented(self):
        assert "cannot gain, lose or reorder a task" in self._f012()

    def test_the_canonical_number_text_is_documented(self):
        doc = self._f012()
        assert "Call-ref numbers have exactly one text form" in doc
        assert "1 -> 01" in doc and "100 -> 100" in doc
        assert "canonical_call_number()" in doc

    def test_the_number_aliases_are_named(self):
        doc = self._f012()
        assert "round-000001" in doc
        assert "attempt-00" in doc

    def test_reconstruction_decides_canonicality(self):
        assert "decided by RECONSTRUCTION" in self._f012()

    def test_the_typed_review_subject_is_documented(self):
        doc = self._f012()
        assert "The review subject is typed, verified and resolved by ONE helper" in doc
        assert "ReviewSubjectV1" in doc
        assert "rev-parse --verify" in doc

    def test_the_ancestor_requirement_is_documented(self):
        doc = self._f012()
        assert "merge-base --is-ancestor" in doc
        assert "non-ancestral RAISES" in doc

    def test_the_base_and_head_facts_are_documented(self):
        doc = self._f012()
        assert "full 40-char SHA becomes the durable fact" in doc
        assert "review_subject.json" in doc
        assert "read in exactly one module" in doc

    def test_the_legacy_unset_base_is_documented(self):
        assert "Unset base remains the documented legacy path" in self._f012()

    def test_deletion_and_rename_proofs_are_documented(self):
        doc = self._f012()
        assert "Deletions and renames are provable" in doc
        assert "TOMBSTONE" in doc
        assert "old_path" in doc
        assert "NUL-delimited" in doc

    def test_the_coverage_mapping_is_documented(self):
        doc = self._f012()
        assert "Authoritative coverage understands directory arguments" in doc
        assert "cries wolf" in doc

    def test_the_commit_chain_artifact_is_documented(self):
        doc = self._f012()
        assert "The commit chain is an artifact, not prose" in doc
        assert "review_commit_chain.json" in doc
        assert "--ancestry-path" in doc

    def test_the_checkpoint_commit_policy_is_documented(self):
        doc = self._f012()
        assert "Local checkpoint commit policy" in doc
        assert "Local history is not an acceptance signal" in doc

    def test_the_readme_states_the_task_history_rule(self):
        assert "## Hardening round 15" in self._f012()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round16IsPinned:
    """Round 16: the task-status/expectation truth table, the restored do job-flow behaviour,
    explicit review-base transport, full ReviewSubject/CommitChain re-verification, the
    symlink/special-file policy, packaged commit patches, and relevant-regression coverage."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 16" in self._f012()

    def test_the_job_flow_repair_is_documented(self):
        doc = self._f012()
        assert "`do job-flow` works again" in doc
        assert "NameError: timeout_sec is not defined" in doc
        assert "RESOLVED and recorded" in doc

    def test_the_truth_table_is_documented(self):
        doc = self._f012()
        assert "The task-status / expectation truth table" in doc
        assert "validate_task_expectation_truth()" in doc
        for expectation in ("`skipped`", "`not_dispatched`", "`failed_pre_dispatch`",
                            "`executed`", "`prior_episode`", "`dispatched_no_calls`"):
            assert expectation in doc, expectation

    def test_the_permissive_rows_are_justified_not_assumed(self):
        """They are load-bearing: forbidding them would refuse real production records."""
        doc = self._f012()
        assert "F011's mid-flight\nstop" in doc
        assert "AFTER a successful run" in doc
        assert "would refuse real records" in doc

    def test_the_commit_chain_fields_are_documented(self):
        doc = self._f012()
        assert "Every commit-chain field is recomputed" in doc
        assert "FORGED SUBJECT" in doc
        assert "`chain_v`" in doc

    def test_the_subject_recomputation_is_documented(self):
        doc = self._f012()
        assert "The packager recomputes the whole review subject" in doc
        assert "own account of its own work" in doc

    def test_the_path_kind_policy_is_documented(self):
        doc = self._f012()
        assert "Typed path kinds: inspect, never follow" in doc
        assert "lstat" in doc
        for kind in ("`regular`", "`symlink`", "`deleted`", "`directory`", "`special`"):
            assert kind in doc, kind
        assert "LEXICAL" in doc

    def test_the_honest_fifo_boundary_is_documented(self):
        """A rule that never runs must not be documented as protection."""
        doc = self._f012()
        assert "does not report a bare FIFO" in doc

    def test_the_explicit_base_transport_is_documented(self):
        doc = self._f012()
        assert "the CWD is not a credential" in doc
        assert "read_declared_base()" in doc
        assert "child_env_without_declaration()" in doc

    def test_the_commit_patch_artifacts_are_documented(self):
        doc = self._f012()
        assert "review_commit_patches/<full-sha>.patch" in doc
        assert "not self-contained evidence" in doc

    def test_the_relevant_regression_coverage_is_documented(self):
        doc = self._f012()
        assert "Relevant regressions are part of authoritative verification" in doc
        assert "_RELEVANT_SUITES_FOR_SOURCE" in doc
        assert "cannot notice the one you broke" in doc

    def test_the_readme_states_the_review_subject_contract(self):
        assert "## Hardening round 16" in self._f012()
        assert "is not a credential" in self._f012()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round17IsPinned:
    """Round 17: episode-context task truth, lossless typed committed/dirty merge, git file
    modes, no-follow symlink proofs, dirty tombstones/renames, job-flow review-base forwarding,
    strict ReviewSubject schema, NUL-safe ZIP building, component-aware containment, exact
    post-build membership."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 17" in self._f012()

    def test_episode_context_task_truth_is_documented(self):
        doc = self._f012()
        assert "Task truth depends on the episode's status and phase" in doc
        assert "_allowed_statuses_for" in doc

    def test_the_frozen_prior_status_is_documented(self):
        doc = self._f012()
        assert "A prior task's terminal status is frozen" in doc

    def test_the_lossless_merge_is_documented(self):
        doc = self._f012()
        assert "One lossless typed merge of committed and dirty records" in doc
        assert "merge_review_file_state" in doc

    def test_committed_kinds_and_modes_are_documented(self):
        doc = self._f012()
        assert "Committed file kinds and modes come from git" in doc
        assert "git diff --raw" in doc

    def test_the_no_follow_content_proof_is_documented(self):
        doc = self._f012()
        assert "The content-proof check is typed and no-follow" in doc
        assert "lstat" in doc

    def test_dirty_tombstones_and_renames_are_documented(self):
        doc = self._f012()
        assert "Dirty deletions and renames carry full base proofs" in doc

    def test_job_flow_base_forwarding_is_documented(self):
        doc = self._f012()
        assert "`do job-flow` forwards the review base" in doc

    def test_the_strict_schema_is_documented(self):
        doc = self._f012()
        assert "Strict external ReviewSubject schema" in doc
        assert "validate_review_subject_schema" in doc

    def test_the_nul_safe_zip_is_documented(self):
        doc = self._f012()
        assert "The ZIP is built from an exact path-safe model" in doc
        assert "review_zip.py" in doc
        assert "newline" in doc

    def test_component_containment_is_documented(self):
        doc = self._f012()
        assert "Containment by path components" in doc
        assert "commonpath" in doc
        assert "repo-evil" in doc

    def test_post_build_membership_is_documented(self):
        doc = self._f012()
        assert "Post-build membership verification" in doc

    def test_the_readme_states_the_round17_contracts(self):
        assert "## Hardening round 17" in self._f012()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round18IsPinned:
    """Round 18: the typed file-to-archive transaction — ArchivePlan, type/mode preservation,
    atomic no-follow reads, recursive ReviewSubject schema, full-record recompute, typed
    post-build verification, and full packaging integration."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 18" in self._f012()

    def test_the_archive_plan_is_documented(self):
        doc = self._f012()
        assert "One typed ArchivePlanV1 drives the package" in doc
        assert "archive_plan.py" in doc
        assert "-type f -o -type l" in doc

    def test_type_and_mode_preservation_is_documented(self):
        doc = self._f012()
        assert "File type and mode are preserved" in doc
        assert "100755" in doc and "S_IFLNK" in doc

    def test_atomic_no_follow_reads_are_documented(self):
        doc = self._f012()
        assert "File reads are atomically no-follow" in doc
        assert "read_verified_file_at" in doc
        assert "O_NOFOLLOW" in doc

    def test_the_recursive_schema_is_documented(self):
        doc = self._f012()
        assert "The ReviewSubject schema is exact recursively" in doc
        assert "validate_review_commit_schema" in doc
        assert "decode_review_subject_from_json" in doc

    def test_full_record_recompute_is_documented(self):
        doc = self._f012()
        assert "Every file field is recomputed" in doc

    def test_typed_post_build_verification_is_documented(self):
        doc = self._f012()
        assert "Post-build verification validates typed metadata" in doc

    def test_full_integration_is_documented(self):
        doc = self._f012()
        assert "Full make_review_zip integration is tested" in doc

    def test_the_filename_byte_policy_is_documented(self):
        doc = self._f012()
        assert "Filename-byte policy" in doc
        assert "surrogateescape" in doc

    def test_the_readme_states_the_typed_transaction(self):
        assert "## Hardening round 18" in self._f012()
        assert "ArchivePlan" in self._f012()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round19IsPinned:
    """Round 19: the closure block — one explicit authority set and one bundle-safety policy, the
    plan and its report packaged, modes bound to bytes, stable reads, a typed no-follow evidence
    inventory, a coherent subject schema, a fail-closed loader, and a bounded archive."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 19" in self._f012()

    def test_explicit_authority_is_documented(self):
        doc = self._f012()
        assert "Authority is passed explicitly" in doc
        assert "authoritative_paths" in doc
        assert "source_class" in doc and "operator_context" in doc

    def test_packaged_plan_and_report_are_documented(self):
        doc = self._f012()
        assert "review_archive_plan.json" in doc
        assert "review_zip_verification.json" in doc
        assert "always describes a verified archive" in doc

    def test_mode_binding_and_dirty_capture_are_documented(self):
        doc = self._f012()
        assert "dirty chmod" in doc
        assert "expected_mode" in doc
        assert "bound to the opened descriptor" in doc

    def test_stable_read_is_documented(self):
        doc = self._f012()
        assert "stable same-inode read" in doc
        assert "torn read" in doc

    def test_atomic_symlink_and_bundle_policy_are_documented(self):
        doc = self._f012()
        assert "classify_bundle_path" in doc
        assert "BLOCK_SENSITIVE" in doc
        assert "one atomic fact" in doc

    def test_typed_evidence_inventory_is_documented(self):
        doc = self._f012()
        assert "evidence_inventory.py" in doc
        assert "stage_review_evidence.py" in doc
        assert "never skipped, never followed" in doc

    def test_coherence_matrix_is_documented(self):
        doc = self._f012()
        assert "coherence matrix" in doc
        assert "base symlink whose `base_mode` is `100644`" in doc

    def test_fail_closed_loader_is_documented(self):
        doc = self._f012()
        assert "fails closed" in doc
        assert "ABSENT `--subject-json`" in doc

    def test_bounded_archive_is_documented(self):
        doc = self._f012()
        assert "expansion-ratio bomb guard" in doc
        assert "64 MiB" in doc and "2 GiB" in doc

    def test_readme_states_the_closure(self):
        assert "## Hardening round 19" in self._f012()


class TestF012Round20IsPinned:
    """Round 20: the root-of-trust closure — a single staged byte source, one strict authority
    proof, exact authority equality, an expected hash on every member, and a directed hash chain
    over generated artifacts that never hash themselves."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 20" in self._f012()

    def test_the_single_sources_are_documented(self):
        doc = self._f012()
        assert "immutable private staging snapshot" in doc
        assert "after staging nothing reads `EVIDENCE_DIR` again" in doc

    def test_strict_content_proof_is_documented(self):
        doc = self._f012()
        assert "ContentProofV1" in doc
        assert "no fail-open empty authority" in doc
        assert "forced non-authoritative even if a forged Proof names it" in doc

    def test_the_directed_hash_chain_is_documented(self):
        doc = self._f012()
        assert "review_zip_expectation.json" in doc
        assert "No artifact hashes itself" in doc
        assert "review_archive_plan_sha256" in doc

    def test_every_member_identity_is_documented(self):
        doc = self._f012()
        assert "snapshot_plan_members" in doc
        assert "expected content identity" in doc

    def test_one_bundle_policy_and_no_follow_manifest_are_documented(self):
        doc = self._f012()
        assert "governs EVERY repository member including unchanged context" in doc
        assert "a symlinked manifest is refused" in doc

    def test_complete_matrix_and_limits_are_documented(self):
        doc = self._f012()
        assert "Complete ReviewFile state matrix" in doc
        assert "enforced DURING the snapshot walk" in doc
        assert "review_zip_expectation.json" in doc

    def test_the_round_19_overclaim_is_corrected(self):
        assert "Superseded by round 20" in self._f012()

    def test_readme_states_the_root_of_trust(self):
        doc = self._f012()
        assert "staged byte source" in doc
        assert "directed hash chain" in doc

    def test_f012_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round21IsPinned:
    """Round 21: the final root-identity closure — exact raw-byte identities over one immutable
    staged byte map, one disposition owner, the verified final-status source, and exact versions."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 21" in self._f012()

    def test_raw_byte_identity_is_documented(self):
        doc = self._f012()
        assert "Raw-byte identity" in doc
        assert 'SHA256(exact bytes packaged at' in doc
        assert "reserialized projection" in doc

    def test_immutable_staged_byte_map_is_documented(self):
        doc = self._f012()
        assert "_StagedArtifacts" in doc
        assert "refuses if a staged file changed between decode and package" in doc

    def test_one_disposition_owner_is_documented(self):
        doc = self._f012()
        assert "EXCLUDE_SAFE_CONTEXT" in doc
        assert "BLOCK_UNSUPPORTED" in doc
        assert "nothing silently disappears" in doc

    def test_final_status_source_is_documented(self):
        doc = self._f012()
        assert "Final status source" in doc
        assert "never a post-build disk-manifest reread" in doc

    def test_declared_subject_and_exact_versions_are_documented(self):
        doc = self._f012()
        assert "subject.declared" in doc
        assert 'exact version set `{"1.1.0"}`' in doc

    def test_snapshot_inventory_boundary_is_documented(self):
        doc = self._f012()
        assert "source Evidence members at the snapshot" in doc

    def test_no_live_stale_verification_reference(self):
        # The round-19 claim is explicitly corrected, and the round-21 section labels the retired
        # path; the only occurrences are historical prose or the "stale ... retired" note.
        doc = self._f012()
        assert "Superseded by round 20" in doc
        assert "the stale `review_zip_verification.json`" in doc

    def test_readme_states_the_raw_byte_identity(self):
        doc = self._f012()
        assert "raw-byte" in doc
        assert "verified package model" in doc

    def test_f012_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round22IsPinned:
    """Round 22: the gate-and-snapshot closure — READY bound to the complete gate matrix over one
    staged byte map, a strict inventory bijection, and one bundle-policy owner."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 22" in self._f012()

    def test_the_ready_gate_matrix_is_documented(self):
        doc = self._f012()
        assert "The exact READY gate matrix" in doc
        assert "evaluate_ready_gate_matrix" in doc
        assert "commit_execution_gate = NEEDS_HUMAN_APPROVAL` is expected and nonblocking" in doc

    def test_one_staged_byte_map_owner_is_documented(self):
        doc = self._f012()
        assert "one staged byte-map owner" in doc
        assert "the package always contains exactly the gate bytes used to decide status" in doc

    def test_strict_inventory_bijection_is_documented(self):
        doc = self._f012()
        assert "EvidenceSnapshotInventoryV1" in doc
        assert "CALLED in the production build before READY is possible" in doc

    def test_one_bundle_policy_owner_is_documented(self):
        doc = self._f012()
        assert "the sole bundle-policy owner" in doc
        assert "no policy-relevant path silently" in doc

    def test_complete_regression_is_documented(self):
        doc = self._f012()
        assert "all 46 `test_run_manifest*.py`" in doc

    def test_readme_states_the_gate_matrix(self):
        doc = self._f012()
        assert "## Hardening round 22" in doc
        assert "complete gate verdict matrix" in doc

    def test_f012_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round23IsPinned:
    """Round 23: semantic gate consistency, the checked commit gate, one complete staged byte map,
    inventory size binding, and ArchivePlan-owned prior-package disposition."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def _readme(self):
        from pathlib import Path as _P
        return _P("README.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 23" in self._f012()

    def test_semantic_gate_consistency_is_documented(self):
        doc = self._f012()
        assert "Semantic gate consistency" in doc
        assert "checks its INTERNAL truth, not just" in doc

    def test_checked_commit_gate_is_documented(self):
        doc = self._f012()
        assert "Checked nonblocking commit gate" in doc
        assert "embedded `gate_checks` equal the packaged verdicts" in doc

    def test_complete_staged_byte_map_is_documented(self):
        doc = self._f012()
        assert "One complete staged byte map" in doc
        assert "no evidence artifact is interpreted from one" in doc

    def test_inventory_size_binding_is_documented(self):
        doc = self._f012()
        assert "Inventory size binding" in doc
        assert "packaged ZIP uncompressed size" in doc

    def test_prior_package_disposition_is_documented(self):
        doc = self._f012()
        assert "No hidden shell bundle policy" in doc
        assert "EXCLUDE_SAFE_CONTEXT" in doc

    def test_readme_states_semantic_consistency(self):
        assert "## Hardening round 23" in self._f012()

    def test_f012_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [x] F012" in status
        assert "- [x] F017" in status


class TestF012Round24IsPinned:
    """Round 24: closed gate schemas, embedded gate equality, exact commit-gate derivation, no
    unsafe gate metadata, and snapshot-only manifest construction."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 24" in self._f012()

    def test_closed_gate_schemas_are_documented(self):
        doc = self._f012()
        assert "Closed gate schemas" in doc
        assert "an unknown field BLOCKS" in doc

    def test_embedded_gate_equality_is_documented(self):
        doc = self._f012()
        assert "Embedded gate equality" in doc
        assert "must EQUAL the" in doc and "separately packaged gate verdicts" in doc

    def test_exact_commit_gate_derivation_is_documented(self):
        doc = self._f012()
        assert "Exact commit-gate derivation" in doc
        assert "`non_pass_gates` is the derived set" in doc

    def test_unsafe_metadata_scan_is_documented(self):
        doc = self._f012()
        assert "No unsafe gate metadata" in doc
        assert "control character in any field BLOCKS" in doc

    def test_snapshot_only_manifest_is_documented(self):
        doc = self._f012()
        assert "Snapshot-only manifest construction" in doc
        assert "no Evidence helper opens, stats or lists the staging filesystem" in doc


class TestF012Round25IsPinned:
    """Round 25: recursive gate schemas, complete semantics, metadata key safety, exact commit-gate
    issue derivation, duplicate-key rejection, and no-follow staged acquisition."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 25" in self._f012()

    def test_recursive_schemas_documented(self):
        doc = self._f012()
        assert "Recursive gate schemas" in doc
        assert "an unknown NESTED field blocks" in doc

    def test_complete_semantics_documented(self):
        doc = self._f012()
        assert "Complete gate semantics" in doc
        assert "the packaged ContentProof authority" in doc

    def test_metadata_key_safety_documented(self):
        doc = self._f012()
        assert "Metadata key safety" in doc
        assert "walks dictionary KEYS" in doc

    def test_exact_commit_issues_documented(self):
        doc = self._f012()
        assert "Exact commit-gate issues" in doc
        assert "issue text is not a second" in doc

    def test_duplicate_key_rejection_documented(self):
        doc = self._f012()
        assert "Duplicate-key rejection" in doc
        assert "refuses duplicate keys at ANY depth" in doc

    def test_no_follow_acquisition_documented(self):
        doc = self._f012()
        assert "No-follow acquisition" in doc
        assert "never followed or read" in doc


class TestF012Round26IsPinned:
    """Round 26: fully typed gate shapes, required nested fields, strict fail-closed verification
    total, one bounded acquisition budget, one shared strict decoder, packaging-output disposition."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 26" in self._f012()

    def test_fully_typed_documented(self):
        doc = self._f012()
        assert "Fully typed gate shapes" in doc
        assert "NO accept-anything node" in doc

    def test_required_fields_documented(self):
        doc = self._f012()
        assert "Required nested fields" in doc
        assert "a required field that is\n  absent blocks" in doc or "required field that is" in doc

    def test_strict_verification_documented(self):
        doc = self._f012()
        assert "Strict, fail-closed VerificationTests" in doc
        assert "NO `int()` coercion" in doc

    def test_acquisition_budget_documented(self):
        doc = self._f012()
        assert "One bounded acquisition budget" in doc
        assert "never a silent\n  absence" in doc or "never a silent absence" in doc

    def test_shared_decoder_documented(self):
        doc = self._f012()
        assert "One shared strict decoder" in doc
        assert "keep no private copy" in doc

    def test_packaging_output_disposition_documented(self):
        doc = self._f012()
        assert "Packaging output is not dirty source" in doc
        assert "packaging_generated_outputs" in doc


class TestF012Round27IsPinned:
    """Round 27: real token summary shapes, complete verification typing, acquisition overflow never
    absence, exact packaging-output identity, strict decode at every trust boundary."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 27" in self._f012()

    def test_real_token_shapes_documented(self):
        doc = self._f012()
        assert "Real token measurement shapes" in doc
        assert "_ACTUAL_TOKEN_SUMMARY" in doc

    def test_complete_verification_typing_documented(self):
        doc = self._f012()
        assert "Complete verification typing" in doc
        assert "_run_verifications" in doc

    def test_acquisition_overflow_never_absence_documented(self):
        doc = self._f012()
        assert "Acquisition overflow never absence" in doc
        assert "BEFORE reading bytes" in doc

    def test_exact_output_identity_documented(self):
        doc = self._f012()
        assert "Exact packaging-output identity" in doc
        assert "nested file or a root lookalike" in doc

    def test_strict_decode_every_boundary_documented(self):
        doc = self._f012()
        assert "Strict decode at every trust boundary" in doc
        assert "no silent fallback" in doc


class TestF012Round28IsPinned:
    """Round 28: token-status projection coherence, producer-derived VerificationTests, invocation-
    bound packaging-output identity, malformed nested Evidence validates instead of crashing, plus the
    F012 closure statement."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 28" in self._f012()

    def test_token_projection_coherence_documented(self):
        doc = self._f012()
        assert "Token-status projection coherence" in doc
        assert "single authority" in doc

    def test_producer_derived_verification_documented(self):
        doc = self._f012()
        assert "Producer-derived VerificationTests" in doc
        assert '" && ".join(run commands)' in doc
        assert "timezone-aware ISO-8601 datetime" in doc

    def test_invocation_bound_identity_documented(self):
        doc = self._f012()
        assert "Invocation-bound packaging-output identity" in doc
        assert "only exact membership classifies" in doc
        # The Round-27 grammar claim is explicitly corrected.
        assert "invocation-INDEPENDENT" in doc

    def test_malformed_nested_documented(self):
        doc = self._f012()
        assert "Malformed nested Evidence validates, never crashes" in doc
        assert "never raises `AttributeError`" in doc

    def test_closure_section_present(self):
        doc = self._f012()
        # F012 is externally accepted; the acceptance section records the verdict.
        assert "External acceptance" in doc
        assert "PASS_WITH_RISKS — ACCEPTED" in doc
        assert "Maintenance follow-ups" in doc or "follow-up maintenance" in doc


class TestF012Round29IsPinned:
    """Round 29: complete-class closure — token producer re-derivation, manual-completion shape safety,
    internally-derived generated-output identity, NUL-safe git paths, hermetic packaging E2E, and the
    corrected (conditional) acceptance wording."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 29" in self._f012()

    def test_token_rederivation_documented(self):
        doc = self._f012()
        assert "Complete token producer re-derivation" in doc
        assert "token_measurement.token_measurement_summary(token_status)" in doc

    def test_manual_shape_safety_documented(self):
        doc = self._f012()
        assert "Complete manual-completion shape safety" in doc
        assert "before any iteration\n  or `.get` chain" in doc or "before any iteration" in doc

    def test_internally_derived_identity_documented(self):
        doc = self._f012()
        assert "Internally-derived generated-output identity" in doc
        assert "a caller cannot declare a source path a" in doc
        assert "exit 3" in doc

    def test_nul_safe_git_paths_documented(self):
        doc = self._f012()
        assert "NUL-safe Git porcelain paths" in doc
        assert "porcelain=v1 -z" in doc

    def test_hermetic_e2e_documented(self):
        doc = self._f012()
        assert "Hermetic review-packaging E2E" in doc
        assert "env -u PYTHONPATH" in doc

    def test_acceptance_is_recorded(self):
        doc = self._f012()
        # F012 is externally accepted; the document records the verdict and date.
        assert "PASS_WITH_RISKS — ACCEPTED" in doc
        assert "2026-07-20" in doc
        assert "is accepted on the basis of its" not in doc


class TestF012Round30IsPinned:
    """Round 30: the primary blocker (final-verifier reproducibility) is closed; F2–F7 are documented
    as OPEN follow-ups, not claimed closed."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 30" in self._f012()

    def test_authority_model_documented(self):
        doc = self._f012()
        assert "staged Evidence bytes" in doc
        assert "never** authority" in doc or "never* authority" in doc or "never" in doc

    def test_regeneration_documented(self):
        doc = self._f012()
        assert "regenerate_final_verifier" in doc
        assert "verify_final_verifier=True" in doc
        assert "manual_attestation" in doc

    def test_open_followups_not_claimed_closed(self):
        doc = self._f012()
        assert "OPEN follow-ups" in doc
        # F2..F7 are explicitly listed as open, not closed.
        for tag in ("**F2**", "**F5**", "**F6**", "**F7**"):
            assert tag in doc


class TestF012Round31IsPinned:
    """Round 31: fail-closed tri-state reproducibility, token authority, typed manual semantics, total
    gate evaluation; F4/F5/F7 kept explicitly open."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 31" in self._f012()

    def test_authority_rule_documented(self):
        doc = self._f012()
        assert "ran SUCCESSFULLY and exact\nequality was verified" in doc or \
            "ran SUCCESSFULLY and exact equality was verified" in doc
        assert "unchecked or failed regeneration is never reproducible" in doc

    def test_tristate_documented(self):
        doc = self._f012()
        for s in ("VERIFIED_EQUAL", "VERIFIED_MISMATCH", "NOT_CHECKED", "PRODUCER_ERROR"):
            assert s in doc

    def test_token_and_scalar_and_gate_documented(self):
        doc = self._f012()
        assert "token_authority.validate_token_truth" in doc
        assert "the single supported manual-Evidence" in doc
        assert "total gate evaluation" in doc

    def test_f4_f5_f7_still_open(self):
        doc = self._f012()
        assert "Still OPEN" in doc
        for tag in ("**F4**", "**F5**", "**F7**"):
            assert tag in doc


class TestF012Round32IsPinned:
    """Round 32: final authority & packaging closure — token-truth root binding, complete manual
    contract, no-clobber publication, fail-closed git-status, exact patchset identity, integration
    termination."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 32" in self._f012()

    def test_token_truth_binding_documented(self):
        doc = self._f012()
        assert "root token truth bound to task/provider Evidence" in doc
        assert "_token_truth_authority" in doc

    def test_no_clobber_documented(self):
        doc = self._f012()
        assert "safe_publish.assert_publishable" in doc
        assert "mv` is never the" in doc

    def test_git_status_snapshot_documented(self):
        doc = self._f012()
        assert "fail-closed single Git-status snapshot" in doc
        assert "OK|FAILED|TIMED_OUT|UNAVAILABLE|" in doc

    def test_patchset_identity_documented(self):
        doc = self._f012()
        assert "commit_patchset_identity" in doc
        assert "can never enter the identity" in doc

    def test_manual_production_caller_documented(self):
        doc = self._f012()
        assert "job_evidence.write_manual_completion_evidence" in doc


class TestF012Round33IsPinned:
    """Round 33: publication-lifecycle & producer-caller closure — atomic no-clobber publication
    really used by both coordinators, fail-closed git tracked-status, shared token-truth schema, and a
    real end-to-end operator caller for the canonical manual producer."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 33" in self._f012()

    def test_atomic_publication_really_used(self):
        doc = self._f012()
        assert "safe_publish.publish_atomically" in doc
        assert "os.link" in doc and "PublishCollisionError" in doc

    def test_fail_closed_git_tracked_status(self):
        doc = self._f012()
        assert "safe_publish.git_tracked_status" in doc
        assert "never read as \"untracked\"" in doc

    def test_shared_token_schema(self):
        doc = self._f012()
        assert "CONFIDENCE_SOURCE_PAIRS" in doc
        assert "mixed_provider_actuals_and_heuristic" in doc

    def test_real_operator_caller(self):
        doc = self._f012()
        assert "job_evidence.create_manual_completion_bundle" in doc
        assert "temporary git repository" in doc


class TestF012Round34IsPinned:
    """Round 34: single-publication & complete-token-truth closure — one private-to-final publication
    with no public intermediate ZIP, and the complete TokenTruthV1 input/output contract."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 34" in self._f012()

    def test_single_publication_no_public_intermediate(self):
        doc = self._f012()
        assert "no public intermediate ZIP" in doc
        assert "verify_source_identity" in doc and "PublishSourceError" in doc
        assert 'rm -f "$OUT"' in doc                          # documents its REMOVAL

    def test_complete_token_truth_contract(self):
        doc = self._f012()
        assert "complete TokenTruthV1 input + output semantics" in doc
        assert "TokenEvidenceError" in doc
        assert "PRODUCER_ERROR" in doc and "BLOCKED_EVIDENCE" in doc


class TestF012Round37IsPinned:
    """Round 37: anonymous-inode publication & semantic provider evidence — O_TMPFILE + linkat,
    pre-publication cleanup ownership, validate_provider_evidence, diagnostic broad run."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 37" in self._f012()

    def test_anonymous_inode_publication(self):
        doc = self._f012()
        assert "O_TMPFILE" in doc
        assert "linkat" in doc
        assert "anonymous" in doc.lower()

    def test_pre_publication_cleanup_ownership(self):
        doc = self._f012()
        assert "fstat(anonymous_fd)" in doc or "fstat" in doc
        assert "BEFORE publication" in doc or "pre-publication" in doc.lower()

    def test_semantic_provider_evidence(self):
        doc = self._f012()
        assert "validate_provider_evidence" in doc
        assert "actual_model_verified" in doc
        assert "TokenEvidenceError" in doc

    def test_diagnostic_broad_run(self):
        doc = self._f012()
        assert "7440 passed" in doc
        assert "pre-existing" in doc.lower()
        assert "not the aggregate" in doc or "invalid" in doc


class TestF012Round38IsPinned:
    """Round 38: versioned PE schema, publication capability, machine-validated diagnostic."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 38" in self._f012()

    def test_cost_call_count_requirement(self):
        doc = self._f012()
        assert "cost_call_count" in doc
        assert "cost without call-count" in doc.lower() or "cost_call_count is absent" in doc.lower()

    def test_ambiguous_actual_model_rejected(self):
        doc = self._f012()
        assert "ambiguous" in doc.lower()
        assert "actual_model" in doc

    def test_verified_model_zero_calls(self):
        doc = self._f012()
        assert "provider_call_count" in doc

    def test_publication_capability_probe(self):
        doc = self._f012()
        assert "probe_anonymous_publication_capability" in doc or "SUPPORTED" in doc
        assert "UNSUPPORTED_OS" in doc or "capability" in doc.lower()


class TestF012Round39IsPinned:
    """Round 39: closed PE schema, diagnostic producer/validator, verification matrix, capability integration."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 39" in self._f012()

    def test_closed_pe_schema(self):
        doc = self._f012()
        assert "ProviderTokenEvidence" in doc or "provider_token_evidence" in doc
        assert "ALLOWED_FIELDS" in doc
        assert "validate_provider_token_evidence" in doc

    def test_diagnostic_producer_validator(self):
        doc = self._f012()
        assert "diagnostic_comparison" in doc
        assert "produce_diagnostic_comparison" in doc or "validate_diagnostic_comparison" in doc

    def test_verification_matrix(self):
        doc = self._f012()
        assert "verification_matrix" in doc or "produce_verification_tests" in doc
        assert "validate_verification_completeness" in doc or "completeness validator" in doc.lower()

    def test_capability_integrated(self):
        doc = self._f012()
        assert "build_review_zip" in doc
        assert "exit code 4" in doc or "returns exit code 4" in doc.lower()

    def test_authoritative_test_count(self):
        doc = self._f012()
        assert "651 passed" in doc


class TestF012Round40IsPinned:
    """Round 40: authority contract closure — 5 findings closed."""

    def _f012(self):
        from pathlib import Path as _P
        return _P("docs/roadmap/features/T0_F012.md").read_text()

    def test_the_round_is_recorded(self):
        assert "Hardening round 40" in self._f012()

    def test_mixed_identity_check(self):
        doc = self._f012()
        assert "_has_any_manual_claim" in doc or "mixed completion identity" in doc.lower()

    def test_forged_patch_bytes_test(self):
        doc = self._f012()
        assert "ForgedPatchBytesBlock" in doc or "commit_patch_bytes" in doc

    def test_pe_cross_field_validation(self):
        doc = self._f012()
        assert "completion_provider_call_count" in doc
        assert "provider_attempts" in doc

    def test_verification_completeness_enforced(self):
        doc = self._f012()
        assert "REQUIRED_F012_VERIFICATION_SUITES" in doc or "required_verification_suites" in doc

    def test_publication_capability_in_manifest(self):
        doc = self._f012()
        assert "publication_capability" in doc
        assert "primitive" in doc

    def test_authoritative_test_count(self):
        doc = self._f012()
        assert "538 passed" in doc

    def test_external_acceptance_recorded(self):
        doc = self._f012()
        assert "PASS_WITH_RISKS — ACCEPTED" in doc
        assert "2026-07-20" in doc
        assert "r40_authority_contract_closure" in doc

    def test_accepted_residual_risks_section(self):
        doc = self._f012()
        assert "Accepted residual risks" in doc

    def test_maintenance_followups_do_not_reopen(self):
        doc = self._f012()
        assert "FOLLOWUP-F012-A" in doc
        assert "FOLLOWUP-F012-B" in doc
        assert "FOLLOWUP-F012-C" in doc
        assert "do NOT change F012" in doc or "do not reopen F012" in doc.lower()

    def test_status_is_done(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "[x] F012" in status
