# The prototype-cluster deletion order — one COMPONENT per line, importers first.
#
# WHAT THIS IS. Operator ruling amend0908-f275-finish RULE 2 orders the deletion to
# proceed "in dependency order — leaf modules first, the modules they import last —
# so that each group commit leaves no dangling import", and orders that order derived
# from the map and written down BEFORE the first `git rm`. This file is that order.
#
# HOW TO READ IT. Each non-comment line is ONE deletion step. A line naming several
# modules is a cycle: those modules import each other, so no ordering can separate
# them and they are deleted in ONE commit together with their handlers, catalog
# entries, cockpit sections, tests and map lines. A line naming one module is the
# ordinary case operator RULE 1 describes. Lines are executed top to bottom.
#
# WHY COMPONENTS. The cluster's internal import graph is CYCLIC in three places, so
# RULE 2's "leaf modules first" is unsatisfiable at module granularity: whichever of
# two mutual importers goes first leaves the other importing a deleted module.
# DECISION F275 D2 rules the atomic unit to be the strongly connected component —
# one module wherever the graph is acyclic, the whole cycle where it is not — and
# records the measurement behind it.
#
# HOW IT IS MAINTAINED. This file is GENERATED from the live import graph, never
# typed, and `tests/orchestration/test_cluster_deletion_order.py` holds it against
# that graph. A group commit removes its modules from this file in the SAME commit
# that removes them from disk, exactly as it does for `cluster_deletion_map.txt`.
#
# Blank lines and lines beginning with `#` are ignored by the reader.
packages.orchestration.context_optimizer
packages.orchestration.review_bundle
packages.orchestration.dogfood_run, packages.orchestration.feature_planner, packages.orchestration.overnight_mission, packages.orchestration.progress_ledger, packages.orchestration.repair_loop_v2, packages.orchestration.self_repair_proposal
packages.orchestration.worker_recommend
packages.orchestration.builder_routing, packages.orchestration.candidate_quality, packages.orchestration.local_candidate_generator, packages.orchestration.model_route_tournament
packages.orchestration.context_pack
packages.orchestration.execution_approval_policy
packages.orchestration.external_builder_sandbox
packages.orchestration.local_model_advisor
packages.orchestration.managed_builder_execution
packages.orchestration.overnight_executor
packages.orchestration.worker_registry
packages.orchestration.main_builder_adapter
packages.orchestration.overnight_readiness
packages.orchestration.provider_trust, packages.orchestration.provider_trust_verification
