# Proof Chain

The proof chain answers: **"Why did this change happen, and is it proven?"**

## CLI Usage

```
remedy change proof <job_id> [--path <file>] [--json]
```

Text output shows status icons per change:
- `[OK]` verified
- `[FAIL]` failed
- `[...]` incomplete
- `[?]` unverified
- `[N/A]` not applicable (rejected)

JSON output includes structured `next_safe_action_obj` with `label`, `command`, `reason`, `available`.

## Proof Statuses

| Status | Meaning |
|---|---|
| **verified** | Linked approval + apply event + apply proof + passed or not-required test evidence |
| **failed** | Linked test failed, or task execution blocked/failed |
| **incomplete** | Some chain links present but not all — approval pending, not applied, no proof, or no linked test |
| **unverified** | Change exists but required linkage cannot be established |
| **not_applicable** | Intent was rejected |

### Verified Requirements (strict)

A change is only `verified` when **all** of these are true:

1. Patch intent approved
2. Patch applied (apply event exists)
3. Apply proof recorded (before/after hash)
4. Test passed **and linked** to this change, OR explicit `test_not_required` evidence

Test absence is **never** treated as verified.

## Test Linking

Tests are linked to changes by priority:

1. **intent_linked** — test event has `intent_id` matching the change
2. **task_linked** — test event has `task_id` matching the change's task
3. **sole_change** — job has exactly one applied change, generic test ran
4. **explicit_not_required** — event with `test_not_required: true` for this intent
5. **none** — no linkage possible

A generic test in a multi-change job does **not** verify any individual change.

## Missing Links

The proof chain reports what's missing:

- `approval_pending` — intent awaits approval
- `not_applied` — approved but not applied
- `no_apply_event` — marked applied but no apply event found
- `no_apply_proof` — applied but no proof hash recorded
- `no_linked_test` — applied with proof but no test evidence
- `test_not_linked_to_change` — test ran but not linked to this specific change

## File Provenance

`remedy file why <job_id> <path>` includes `proof_status` derived from the same proof chain.
Both commands agree on status for the same path.
