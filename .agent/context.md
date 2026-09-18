# Context — F266 remedy study (repo comprehension pass)

## Active Branch
feature/f266-remedy-study, cut from `main` at the merge commit of pull
request 254 (F281's closure).

## Scope
F266 (Tier 4; depends on F255 teacher role and the memory cards, both
built). Per `docs/roadmap/features/T4_F266.md`: `study` is a bounded,
read-only comprehension pass that writes auto-approved memory cards with
provenance `machine-study`; `teacher ask` answers from those cards
afterward. F268 (`remedy do`, not yet built) will later invoke `study`
automatically — this feature ships `study` as its own standalone command
regardless, since F268 does not exist yet to invoke it.

## Do not touch
The approval duty for cards of any other provenance (D-C is scoped to
`machine-study` only). The scope-fence deny list (F017). The teacher's
existing read-only stance. `docs/roadmap/features/T5_F265.md` also carries
DECISION D-C's identical text for its own future provenance value(s) —
F266 does not touch that file or claim its provenance value.
`apps/cli/commands/memory.py` (the human-facing `remedy memory store` CLI
path) is untouched this round — `study` writes cards through
`store_memory()` directly, in Python, not through the CLI.

## Assumptions
- `provenance` is a plain `str` field on `MemoryEntry`, not a `Literal`,
  because F265 is already registered with DECISION D-C's identical text
  for its own future provenance value and a closed `Literal` would force
  this feature to predict F265's spelling.
- `study`'s default model is not a new "cheap model" choice: F110
  (`model_routing.py`, `role_config.py`) deliberately maps no tier to a
  concrete model id, so every role resolves to the same provider-aware
  default absent an override. DECISION F266 D1 records that `study`
  inherits that same default, tiered `summarize` for routing/promotion
  bookkeeping only.

## Constraints
- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- Adding a role to `role_config.KNOWN_ROLES` requires the SAME commit to
  add it to `model_routing.ROLE_TASK_CLASSES` (or
  `TASK_CLASS_INHERITING_ROLES`), or `tests/orchestration/test_model_routing.py`'s
  inventory coverage test goes red — measured this round.
- A production `resolve_role_config("study", ...)` call site (landing in a
  later round, with T001) must be added to
  `model_routing.ROLE_CONFIG_CALL_SITES` in the SAME commit, or the
  AST-sweep inventory test goes red.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check
  <path>` is the spelling every gate of this feature orders.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full suite
  runs exactly once per feature, in the closure sequence's
  integration-gate round; no round block may order it. A round's
  verification is targeted tests plus `tests/cli/test_golden_path.py`,
  `tests/docs/` when `docs/roadmap/**` changed, and `ruff check` on
  touched files. A round orders at most six gates; the plan slice, verdict
  booking, prose-slip lines and any DECISION land in ONE commit.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
