"""
Human Copy Dictionary — centralized product language for the Remedy UI.

Maps internal node types, edge types, and concepts to human-readable labels.
Default UI must use this dictionary; raw internal names are forbidden in
default surfaces.

Public API::

    human_label(node_type) -> str
    human_subtitle(node_type) -> str
    human_state(state) -> str
    journey_kind(node_type) -> str
    is_diagnostics_only(node_type) -> bool
    is_default_visible(node_type) -> bool
    FORBIDDEN_DEFAULT_WORDS -> frozenset[str]
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Node type → human label + subtitle
# ---------------------------------------------------------------------------

_NODE_LABELS: dict[str, tuple[str, str]] = {
    "job":                  ("Goal",               "What you asked Remedy to do"),
    "task":                 ("Task",               "A step toward the goal"),
    "artifact":             ("Output",             "Content produced by a task"),
    "patch_intent":         ("Proposed change",    "A code change waiting for review"),
    "approval_decision":    ("Approval",           "Your approval or rejection"),
    "patch_apply":          ("Applied change",     "A code change that was written"),
    "patch_apply_proof":    ("Apply proof",        "Evidence the change was applied"),
    "test_run":             ("Test result",        "Automated test outcome"),
    "verification":         ("Verification",       "Quality check result"),
    "permission_blocker":   ("Needs permission",   "Blocked until you grant access"),
    "decision_queue":       ("Needs your decision","Something requires your attention"),
    "stop_reason":          ("Blocker",            "Why work cannot continue"),
    "run_event":            ("Event",              "A logged workflow event"),
    "agent_loop":           ("Agent cycle",        "One automation loop cycle"),
    "context_coverage":     ("Context check",      "How much context is available"),
    "context_budget":       ("Context budget",     "Token budget for this job"),
    "context_pack":         ("Context snapshot",   "Compact context for providers"),
    "constitution":         ("Project rules",      "Rules from your project config"),
    "project_placeholder":  ("Project",            "Project configuration"),
    "memory_placeholder":   ("Memory",             "Learned facts (future)"),
    "memory":               ("Memory",             "Learned facts (future)"),
    "mcp_placeholder":      ("Tool",               "External tool integration (future)"),
    "run_contract":         ("Run rules",          "Execution boundary contract"),
    "token_policy":         ("Token budget",       "Token routing policy"),
    "worker_adapter":       ("Worker",             "Provider connection spec"),
    "event_ledger":         ("Event summary",      "Aggregate event counts"),
    "git_status":           ("Repository status",  "Git state snapshot"),
    "change_set":           ("Change tracker",     "Full change lifecycle"),
    "patch_revert":         ("Reverted change",    "A change that was undone"),
    "guidance_summary":     ("Guidance",           "Suggestions for next steps"),
    "autonomy_readiness":   ("Readiness check",    "Autonomy level assessment"),
}

# ---------------------------------------------------------------------------
# Journey kind mapping (for story/journey items)
# ---------------------------------------------------------------------------

_JOURNEY_KINDS: dict[str, str] = {
    "job":                  "goal",
    "task":                 "task",
    "artifact":             "change",
    "patch_intent":         "change",
    "approval_decision":    "approval",
    "patch_apply":          "apply",
    "patch_apply_proof":    "proof",
    "test_run":             "test",
    "verification":         "proof",
    "permission_blocker":   "decision",
    "decision_queue":       "decision",
    "stop_reason":          "decision",
    "memory_placeholder":   "memory",
    "memory":               "memory",
}

# ---------------------------------------------------------------------------
# State → human readable
# ---------------------------------------------------------------------------

_STATE_LABELS: dict[str, str] = {
    "completed":       "Done",
    "passed":          "Passed",
    "approved":        "Approved",
    "running":         "In progress",
    "active":          "In progress",
    "pending":         "Waiting",
    "blocked":         "Blocked",
    "failed":          "Failed",
    "rejected":        "Rejected",
    "needs_decision":  "Needs your decision",
    "needs_approval":  "Needs approval",
    "informational":   "Info",
    "loaded":          "Loaded",
    "idle":            "Idle",
    "unknown":         "Unknown",
    "suggested":       "Suggested",
}

# ---------------------------------------------------------------------------
# Diagnostics-only node types (hidden from default journey)
# ---------------------------------------------------------------------------

_DIAGNOSTICS_ONLY: frozenset[str] = frozenset({
    "context_coverage", "context_budget", "context_pack",
    "constitution", "run_contract", "token_policy",
    "worker_adapter", "event_ledger", "agent_loop",
    "run_event", "autonomy_readiness", "git_status",
    "mcp_placeholder", "project_placeholder",
    "guidance_summary",
})

# Node types visible in default journey
_DEFAULT_VISIBLE: frozenset[str] = frozenset({
    "job", "task", "artifact",
    "patch_intent", "approval_decision",
    "patch_apply", "patch_apply_proof",
    "test_run", "verification",
    "permission_blocker", "decision_queue", "stop_reason",
    "memory_placeholder", "memory",
    "change_set", "patch_revert",
})

# ---------------------------------------------------------------------------
# Forbidden words in default UI (debug/internal concepts)
# ---------------------------------------------------------------------------

FORBIDDEN_DEFAULT_WORDS: frozenset[str] = frozenset({
    "rank", "importance", "node_type", "context coverage",
    "present signals", "missing signals", "zone", "metadata",
    "connected_to", "edge_type",
})

# ---------------------------------------------------------------------------
# Layer definitions
# ---------------------------------------------------------------------------

LAYERS = [
    {"id": "journey",      "label": "Journey",      "default": True},
    {"id": "proof",        "label": "Proof",         "default": False},
    {"id": "files",        "label": "Files",         "default": False},
    {"id": "review",       "label": "Review",        "default": False},
    {"id": "memory",       "label": "Memory",        "default": False},
    {"id": "tokens",       "label": "Tokens",        "default": False},
    {"id": "diagnostics",  "label": "Diagnostics",   "default": False},
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def human_label(node_type: str) -> str:
    """Get human-readable label for a node type."""
    entry = _NODE_LABELS.get(node_type)
    if entry:
        return entry[0]
    return node_type.replace("_", " ").title()


def human_subtitle(node_type: str) -> str:
    """Get human-readable subtitle for a node type."""
    entry = _NODE_LABELS.get(node_type)
    if entry:
        return entry[1]
    return ""


def human_state(state: str | None) -> str:
    """Get human-readable state label."""
    if not state:
        return "Unknown"
    return _STATE_LABELS.get(state, state.replace("_", " ").title())


def journey_kind(node_type: str) -> str:
    """Get journey kind for a node type."""
    return _JOURNEY_KINDS.get(node_type, "task")


def is_diagnostics_only(node_type: str) -> bool:
    """Is this node type hidden from default journey?"""
    return node_type in _DIAGNOSTICS_ONLY


def is_default_visible(node_type: str) -> bool:
    """Is this node type visible in default journey?"""
    return node_type in _DEFAULT_VISIBLE
