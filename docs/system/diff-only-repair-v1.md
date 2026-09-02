# Diff-Only Repair v1

> Built state of F111 (`docs/roadmap/features/T2_F111.md`, Tier 2). A repair
> round in the BOUNDED repair loop sends only the failure-relevant hunks and
> accepts a unified diff back, falling back to the full-file round on any doubt.

## Where this applies — and where it deliberately does not

The path is `run_builder_bridge_loop` in
`packages/orchestration/builder_bridge.py`: the bounded
build → bridge → test → repair-context → rebuild cycle, whose bridge already
applies a `StructuredPatch` through the fenced applicator in
`packages/orchestration/source_apply.py`.

`packages/orchestration/pingpong_loop.py` is NOT on this path (DECISION F111
D1). Its builder is an agentic CLI that edits the staging tree itself, its
`BuilderOutput` carries no patch, and no applicator is invoked there — so there
is no seam for a diff channel to attach to. Remedy deliberately does not route
ping-pong repairs through the diff channel in v1.

## Knobs

| Parameter of `run_builder_bridge_loop` | Default | Effect |
|---|---|---|
| `diff_mode` | `True` | `False` ⇒ every repair round is full-file, reason `diff_mode_off` |
| `diff_margin_lines` | `3` | context lines added on each side of every selected range |

## Prompt side — what a repair round carries

`packages/orchestration/diff_repair.py` selects the source a repair prompt
sends:

    select_repair_hunks(repo_root, changed_line_ranges, *,
                        margin_lines=3, max_total_chars=20000)

The line ranges come from the PATCH THAT WAS APPLIED, through
`changed_line_ranges_from_patch` → `review_scope.parse_diff_line_ranges` — not
from the `source_patch_applied` timeline event, whose metadata carries file
lists and no line numbers at all (DECISION F111 D3).

Selected hunks reach the repair context as `diff_hunks`; every path that
carried none reaches it as `diff_hunks_omitted` with a reason — `missing`,
`binary`, `no_ranges`, `out_of_bounds` or `budget`. `out_of_bounds` is the
load-bearing one: lines WERE requested but none of them exist in the file,
which is how a stale diff becomes visible instead of being swallowed.

The prompt-side choice is recorded as `repair_mode`: `diff`, or `full_file`
with a reason (`no_patch`, `no_ranges`, `no_hunks_selected`, `diff_mode_off`).

## Response side

`packages/orchestration/diff_repair_response.py` accepts one versioned record:

    {"format": "unified_diff", "diff": "<unified diff>", "files": ["<path>"]}

`validate_diff_repair_response` rejects a diff touching any file outside the
declared `files` list, and `precheck_diff_repair_fences` asks the job's fences
BEFORE any file is opened — so a diff aimed at a fence-denied path never
reaches the applicator by construction, rather than by an exception raised
mid-apply. `diff_repair_response_to_patch` then converts the accepted answer
into the `StructuredPatch` the existing applicator already takes.

## Apply side — all-or-nothing, or full fallback

`apply_diff_repair` (`packages/orchestration/diff_repair_apply.py`) reports a
mode as data, never as an exception:

| Mode | Meaning |
|---|---|
| `diff` | the unified diff landed; the full-file round was skipped |
| `full_fallback` | nothing landed; `fallback_reason` names why |

`fallback_reason` is prefixed by the stage that refused: `validation:`,
`fence_denied:` or `apply_failed:`. Context matching is STRICT — no fuzz, no
offset search, and nothing shells out to `patch` or `git apply`.

All-or-nothing is `source_apply`'s durable snapshot, created and verified
before any mutation; this path adds no rollback and no second reading of
unified-diff syntax of its own. When the applicator's own restore fails it says
so — `rollback_incomplete (N file(s)): …` — and the result then carries
`rollback_incomplete=True` plus the real `files_modified` count instead of a
reassuring zero.

New-file creation and deletion both stay on the full-file path in v1 (DECISION
F111 D6): the applicator requires the target file to exist, so a creation diff
fails the apply and the round falls back, and the full-file round creates the
file under the same durable snapshot.

## Evidence

Timeline events on this path: `repair_mode_selected` (the prompt-side choice
plus the size pair below), `diff_repair_not_used` (the answer was not a valid
diff record), `diff_repair_applied` (mode, `fallback_reason`, `files_modified`,
`rollback_incomplete`) and `repair_round_fell_back_to_full_file`. The bridge
stop reason for a discarded attempt is `diff_repair_fell_back`.

`repair_mode_selected` carries the pair the saving is read from: `total_chars`,
what the diff path SENT, and `full_file_chars`, what the full-file path WOULD
have sent for the same paths. Both are CHARACTERS, never tokens (DECISION F111
D9) — calling them tokens turns a real measurement into a fabricated one.
Remedy deliberately does not record a derived `chars_saved` field: a derived
number can disagree with its own inputs, and the reader can subtract.

## Related

- [repair-loop-v1.md](repair-loop-v1.md) — the approval-gated repair PROPOSAL
  path. A different loop: it never applies code and never calls a provider.
- `docs/roadmap/features/T2_F111.md` — the target spec and its decisions.
- [session-resume-v1.md](session-resume-v1.md) — reuses `select_repair_hunks`/`render_repair_hunks` for a different purpose: shrinking a REPAIR PROMPT under an active resumed session, never applying a patch; DECISION F111 D1 (no diff-apply seam in `pingpong_loop.py`) is unchanged.
