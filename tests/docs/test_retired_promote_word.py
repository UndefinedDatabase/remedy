"""The retired job-result verb `promote` stays out of the tree, by file and token.

DECISION amend0905-vocab D5 made `apply` replace `promote` as the verb for moving a job's or a
run's reviewed changes into the target repository, and kept the word in its OTHER senses: a
memory card promoted between scopes, a model promoted into a task class, a non-blocking check
promoted to blocking by config, and a finding promoted into a checklist. DECISION F261 D11
renamed the job-result words that were left and ruled the rest by sense: the names that
committed accepted evidence carries (`promote_ready`, the final verifier's recommended actions)
stay, and so do the lines that quote the decision or guard the retired word.

This module reads every file `git ls-files` lists under `apps/`, `packages/`, `scripts/`,
`tests/`, `docs/` and `README.md`, except
`docs/roadmap/` (accepted history and the feature files that name the retired word) and this
file, and skips a file whose bytes contain NUL. It reads each listed path's CURRENT bytes from
the working tree, so an edit to a tracked file counts at once and a new file counts once it is
staged. Every line matching `promot` in any case contributes its tokens, lowercased, and those
tokens are held against `KEPT_BY_SENSE`.

WHEN A NEW LEGITIMATE USE APPEARS: decide its sense first. If it is the job-result verb, write
it with an apply word instead. If it is one of the senses below, add the token to its file's
entry, creating the entry with the sense label when the file has none, and keep the tokens
sorted. A sense that is none of these needs a new `K5:` label added to `SENSES` by a decision.
WHEN AN OCCURRENCE GOES AWAY: remove its token from the file's entry, and the entry once it lists
no token, because every listed token must still occur in its file.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCOPE = ("apps", "packages", "scripts", "tests", "docs", "README.md")
HISTORY = "docs/roadmap/"
THIS_FILE = "tests/docs/test_retired_promote_word.py"
WORD = re.compile(r"promot", re.IGNORECASE)
TOKEN = re.compile(r"[A-Za-z0-9_\-]*promot[A-Za-z0-9_\-]*", re.IGNORECASE)

K1 = "K1: a model promoted into a task class (F110)"
K2 = "K2: a memory card promoted between scopes (F125, F211)"
K3 = "K3: a non-blocking check promoted to blocking by config"
K4 = "K4: a finding promoted into a checklist"
K5_NODE = "K5: a run-log event raised into a brain graph node"
K5_STAGE = "K5: a pytest marker made a CI stage"
K5_STORAGE = "K5: a storage area moved into data_paths resolution"
K5_API = "K5: a private helper made public API"
K5_MILESTONE = "K5: a milestone marked done"
K5_RUNTIME = "K5: a dev-server runtime moved from starting to running"
E = "E: accepted evidence"
H = "H: history or a retired-word guard"

#: The closed set of senses a kept occurrence may have.
SENSES = frozenset({K1, K2, K3, K4, K5_NODE, K5_STAGE, K5_STORAGE, K5_API, K5_MILESTONE, K5_RUNTIME, E, H})

#: path -> (sense, the lowercase tokens that file may carry).
KEPT_BY_SENSE: dict[str, tuple[str, frozenset[str]]] = {
    "docs/README.md": (K1, frozenset({
        "promotion",
    })),
    "docs/agents/model_routing_policy.md": (K1, frozenset({
        "promoted", "promotion",
    })),
    "docs/agents/planner_reviewer_prompt.md": (K4, frozenset({
        "promoted", "promotion",
    })),
    "docs/system/architecture.md": (K5_NODE, frozenset({
        "promoted",
    })),
    "docs/system/remedy-toml-configuration-system-v0.md": (K1, frozenset({
        "promoting", "promotion", "promotion_evidence",
    })),
    "docs/system/vocabulary.md": (H, frozenset({
        "job-promote", "promote", "promoted",
    })),
    "packages/orchestration/brain_detail.py": (K5_NODE, frozenset({
        "promoted",
    })),
    "packages/orchestration/ci_stages.py": (K5_STAGE, frozenset({
        "promoting",
    })),
    "packages/orchestration/commit_execution_gate.py": (E, frozenset({
        "promote_ready",
    })),
    "packages/orchestration/config.py": (K1, frozenset({
        "promotion", "promotion-evidence", "promotion_evidence", "remedy_model_routing_promotion_evidence",
        "resolve_promotion_evidence",
    })),
    "packages/orchestration/final_verifier.py": (E, frozenset({
        "promote", "promoting",
    })),
    "packages/orchestration/manual_attestation.py": (E, frozenset({
        "promote_ready",
    })),
    "packages/orchestration/mission_dossier.py": (K5_MILESTONE, frozenset({
        "promote",
    })),
    "packages/orchestration/model_routing.py": (K1, frozenset({
        "_promotion_assertion_results_from_mapping", "_promotion_evidence_from_entry",
        "_promotion_evidence_reading", "check_promotion_backed_by_evidence", "is_task_class_promotion",
        "promoted", "promoted_by", "promotes", "promotion", "promotion-evidence", "promotion-rule",
        "promotion_evidence", "promotion_evidence_below_threshold",
        "promotion_evidence_compound_field_separator", "promotion_evidence_document_fields",
        "promotion_evidence_entry_field_types", "promotion_evidence_from_mapping",
        "promotion_evidence_incomplete", "promotion_evidence_nested_field",
        "promotion_minimum_block_assertion_pass_rate", "promotion_minimum_overall_pass_rate",
        "promotion_minimum_runs_per_fixture", "promotion_rule_names", "promotion_run_reference",
        "promotion_without_evidence", "promotionassertionresults", "promotionevidence",
        "resolve_promotion_evidence", "rule_promotion_evidence_below_threshold",
        "rule_promotion_evidence_incomplete", "rule_promotion_without_evidence",
    })),
    "packages/orchestration/pingpong_job.py": (H, frozenset({
        "promoted",
    })),
    "packages/orchestration/project_brain.py": (K5_NODE, frozenset({
        "promoted",
    })),
    "packages/orchestration/role_config.py": (K1, frozenset({
        "promoted", "promoted_by", "promotion", "promotion-evidence", "promotion_evidence",
        "promotion_evidence_config_key", "promotion_evidence_from_mapping", "promotion_without_evidence",
        "promotionevidence", "resolve_promotion_evidence", "rule_promotion_without_evidence",
    })),
    "packages/runtimes/dev_server.py": (K5_RUNTIME, frozenset({
        "promote", "promotes",
    })),
    "scripts/build_observability_index.py": (E, frozenset({
        "promote_ready",
    })),
    "scripts/build_review_manifest.py": (E, frozenset({
        "promote_ready",
    })),
    "tests/docs/test_vocabulary.py": (H, frozenset({
        "promote",
    })),
    "tests/orchestration/fixtures/dod/docs_site.json": (K3, frozenset({
        "promoted",
    })),
    "tests/orchestration/test_commit_execution_gate.py": (E, frozenset({
        "promote_ready",
    })),
    "tests/orchestration/test_config.py": (K1, frozenset({
        "_promotion_evidence_record", "_promotion_evidence_toml", "promotion", "promotion_evidence",
        "promotion_evidence_config_key", "promotion_evidence_entry_field_types",
        "promotion_evidence_nested_field", "promotionassertionresults",
        "testthepromotionevidencetableresolveswhole",
    })),
    "tests/orchestration/test_final_verifier.py": (E, frozenset({
        "promote", "promoting",
    })),
    "tests/orchestration/test_job_apply.py": (H, frozenset({
        "promot",
    })),
    "tests/orchestration/test_job_state_field.py": (H, frozenset({
        "promoted",
    })),
    "tests/orchestration/test_job_task_runner.py": (H, frozenset({
        "job-promote",
    })),
    "tests/orchestration/test_mission_dossier.py": (K5_MILESTONE, frozenset({
        "test_a_compression_cannot_promote_a_milestone_to_done",
    })),
    "tests/orchestration/test_model_routing.py": (K1, frozenset({
        "_parse_promotion_bars", "_promoted_table", "_promotion_evidence", "_promotion_rule_bullets",
        "check_promotion_backed_by_evidence", "first_promotion", "golden_promoted_call",
        "is_task_class_promotion", "promotable", "promotable_class", "promote", "promoted", "promoted_by",
        "promoted_tier", "promotion", "promotion-evidence", "promotion-rule", "promotion_evidence",
        "promotion_evidence_compound_field_separator", "promotion_evidence_document_fields",
        "promotion_evidence_entry_field_types", "promotion_evidence_from_mapping",
        "promotion_evidence_nested_field", "promotion_heading", "promotion_minimum_block_assertion_pass_rate",
        "promotion_minimum_overall_pass_rate", "promotion_minimum_runs_per_fixture", "promotion_rule_names",
        "promotion_run_reference", "promotion_without_evidence", "promotionassertionresults",
        "promotionevidence", "promotions", "rule_promotion_evidence_below_threshold",
        "rule_promotion_evidence_incomplete", "rule_promotion_without_evidence",
        "test_a_cheaper_tier_than_the_seed_is_a_promotion",
        "test_a_class_the_seed_table_does_not_name_is_never_a_promotion",
        "test_a_promoted_class_carries_the_run_that_promoted_it",
        "test_a_promoted_class_names_the_run_that_promoted_it",
        "test_a_promotion_with_no_evidence_is_refused_with_its_own_rule",
        "test_a_promotion_without_evidence_is_refused_with_the_rule_named",
        "test_a_stronger_tier_than_the_seed_is_not_a_promotion",
        "test_an_override_restating_a_seed_tier_is_not_a_promotion",
        "test_an_override_restating_the_seed_tier_reports_the_seed_reason_and_no_promotion",
        "test_an_undeclared_class_is_a_schema_fault_and_never_a_promotion_rule",
        "test_an_unpromoted_class_reports_no_promoting_evidence",
        "test_evidence_clears_the_promotion_name_and_never_the_orchestration_rule",
        "test_evidence_for_another_class_does_not_discharge_this_promotion",
        "test_no_promotion_rule_name_is_in_hard_rule_names",
        "test_no_promotion_rule_name_is_in_the_schema_tuple",
        "test_the_builder_accepts_the_same_promotion_with_evidence",
        "test_the_builder_refuses_a_promotion_without_evidence",
        "test_the_golden_promoted_call_is_exactly_this_mapping",
        "test_the_hard_rule_names_are_reported_before_the_promotion_rule_names",
        "test_the_promotion_is_accepted_and_routed_with_what_promoted_it",
        "test_the_promotion_rule_names_are_in_the_declared_order",
        "test_the_same_promotion_with_sufficient_evidence_is_accepted",
        "test_the_same_promotion_with_sufficient_evidence_is_not_refused",
        "test_the_seed_table_is_not_mutated_by_an_evidenced_promotion",
        "test_the_seed_tier_restated_is_not_a_promotion", "testpromotioncheck", "testpromotionpredicate",
        "testpromotionrefusedbytheoverridemap", "testpromotionrulesynctest",
        "testtheparsedrecordlicensesarealpromotion",
        "testthepromotionevidenceparserroundtripsacompleterecord",
        "testthepromotionevidenceparserskipswhatitcannotread",
    })),
    "tests/orchestration/test_review_authoritative_e2e.py": (E, frozenset({
        "promote_ready",
    })),
    "tests/orchestration/test_review_commit_gate_consistency.py": (E, frozenset({
        "promote_ready", "test_promote_ready_true_blocks",
    })),
    "tests/orchestration/test_review_commit_gate_exact_derivation.py": (E, frozenset({
        "promote_ready", "test_promote_ready_true_blocks",
    })),
    "tests/orchestration/test_review_package_status.py": (E, frozenset({
        "promote_ready",
    })),
    "tests/orchestration/test_role_config.py": (K1, frozenset({
        "_configure_promotion_tables", "_evidence_promotable_role", "is_task_class_promotion", "promote",
        "promoted", "promoted_by", "promoted_tier", "promotion", "promotion-evidence",
        "promotion_evidence_config_key", "promotion_evidence_entry_field_types",
        "promotion_evidence_nested_field", "promotion_minimum_block_assertion_pass_rate",
        "promotion_minimum_overall_pass_rate", "promotion_minimum_runs_per_fixture",
        "promotionassertionresults", "resolve_promotion_evidence", "rule_promotion_without_evidence",
        "test_a_promotion_with_evidence_is_accepted_end_to_end", "test_a_routed_call_names_what_promoted_it",
        "test_an_evidenced_worker_promotion_is_routed_and_still_pairs",
        "test_evidence_discharges_the_promotion_rule_but_never_the_pairing_rule",
        "test_the_promotable_role_and_class_are_derived",
        "test_the_same_promotion_without_evidence_is_still_refused",
        "test_the_same_role_records_no_promoter_without_evidence",
        "testmalformedpromotionevidenceisnotacrash", "testpromotableroleisreadfromtheshippedtables",
        "testpromotionevidencereachestheseam", "testpromotionevidencereachesthetablebuilder",
        "testunsetpromotionevidencechangesnothing",
    })),
    "tests/runtimes/test_runtime_state_machine.py": (K5_RUNTIME, frozenset({
        "promoted",
    })),
    "tests/test_command_catalog.py": (H, frozenset({
        "job-promote", "promote",
    })),
    "tests/test_observability_index.py": (E, frozenset({
        "promote_ready",
    })),
    "tests/test_project_brain.py": (K5_NODE, frozenset({
        "test_non_key_event_not_promoted_to_run_event",
    })),
}


def _occurrences() -> dict[str, set[str]]:
    """path -> the lowercase tokens of every line matching `promot`, for each file that has one."""
    listing = subprocess.run(
        ["git", "ls-files", "-z", "--", *SCOPE],
        cwd=REPO_ROOT, capture_output=True, check=True,
    ).stdout
    found: dict[str, set[str]] = {}
    for path in listing.decode("utf-8").split("\0"):
        if not path or path.startswith(HISTORY) or path == THIS_FILE:
            continue
        full = REPO_ROOT / path
        if not full.is_file():
            continue
        data = full.read_bytes()
        if b"\0" in data:
            continue
        tokens = {
            token.lower()
            for line in data.decode("utf-8", errors="replace").splitlines()
            if WORD.search(line)
            for token in TOKEN.findall(line)
        }
        if tokens:
            found[path] = tokens
    return found


def test_no_file_outside_the_map_carries_the_word():
    assert sorted(set(_occurrences()) - set(KEPT_BY_SENSE)) == []


def test_no_kept_file_carries_a_token_outside_its_set():
    extra = {
        path: sorted(tokens - KEPT_BY_SENSE[path][1])
        for path, tokens in _occurrences().items()
        if path in KEPT_BY_SENSE and tokens - KEPT_BY_SENSE[path][1]
    }
    assert extra == {}


def test_every_token_listed_for_a_file_still_occurs_in_it():
    found = _occurrences()
    stale = {
        path: sorted(allowed - found.get(path, set()))
        for path, (_, allowed) in KEPT_BY_SENSE.items()
        if allowed - found.get(path, set())
    }
    assert stale == {}


def test_every_sense_label_is_one_of_the_named_senses():
    assert sorted({sense for sense, _ in KEPT_BY_SENSE.values()} - SENSES) == []
