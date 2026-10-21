"""The names of the providers a role may run on, spelled once (R-1288, DECISION F307 D4).

`create_provider` in `packages/orchestration/pingpong_provider.py` builds four of them by name and
`create_role_provider` in `packages/orchestration/role_provider_factory.py` builds `pi` per role.
A `remedy do` provider option and a failover chain's link both refuse any other name.
"""

from __future__ import annotations

# WHY: one spelling, so a command-line option and a failover link refuse the same typo.
ROLE_PROVIDER_NAMES: frozenset[str] = frozenset({"fake", "claude", "claude-cli", "ollama", "pi"})
