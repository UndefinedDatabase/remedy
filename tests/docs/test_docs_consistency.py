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
        # F010 is accepted, and its own line must say so...
        f010_line = next((ln for ln in readme.splitlines()
                          if ln.startswith("| F010")), "")
        assert f010_line and "externally accepted" in f010_line
        assert "F010 (automatic failure post-mortems) is" not in readme
        # ...and nothing after it may be claimed as existing.
        assert "F008" not in readme or "not implemented" in readme
        # F011 is accepted; its own table line must say so.
        f011_line = next((ln for ln in readme.splitlines()
                          if ln.startswith("| F011")), "")
        assert f011_line and "externally accepted" in f011_line
        # No ACCEPTED feature's table row may call itself pending.
        for ln in readme.splitlines():
            if ln.startswith("| F0") and "✅" in ln:
                assert "not yet externally accepted" not in ln
        # F012 is implemented but must never be called accepted yet.
        if "F012" in readme:
            assert "not yet externally accepted" in readme
        # ...and nothing after it may be claimed as existing.
        assert "F017" not in readme or "not implemented" in readme

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
        # F012 is implemented and in progress; F017 is the next unchecked feature.
        f012 = re.search(r"^- \[~\] F012 — Deterministic runs.*$", text, re.M)
        assert f012, "F012 is built and must be in progress"
        assert not re.search(r"^- \[x\] F012 —", text, re.M)
        assert "remedy job rerun --check-manifest" in f012.group(0)
        assert re.search(r"^- \[ \] F017 —", text, re.M)

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
        # ...and nothing after F012 has been started.
        assert re.search(r"^- \[ \] F008 —", text, re.M)
        assert re.search(r"^- \[ \] F017 —", text, re.M)


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
        r = self._readme()
        assert "must be COMPLETE" in r
        assert "the order is\nthe claim" in r

    def test_the_readme_states_lexical_containment(self):
        assert "refused\nrather than walked" in self._readme()

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [~] F012" in status
        assert "- [ ] F017" in status


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
        r = self._readme()
        assert "frozen whole" in r
        assert "closed canonical grammar" in r
        assert "two different runs can never be\nbacked by one file" in r

    def test_f012_is_still_in_progress_and_f017_not_started(self):
        from pathlib import Path as _P
        status = _P("docs/roadmap/STATUS.md").read_text()
        assert "- [~] F012" in status
        assert "- [ ] F017" in status
