# Cache-Optimal Prompt Ordering v1

> How every Remedy prompt is composed from ranked, named segments, and what
> that reordering actually bought — measured, not asserted. Built by F105
> (T001 registry, T002 conventions loaders, T003 the six builder migrations,
> T004 the stats view and this note). The target plan is
> [T2_F105.md](../roadmap/features/T2_F105.md); this page describes what is
> built. The provider-side cache-read share is **not** measured here and this
> page says why.

## What changed, and what did not

Prompt assembly stopped being ad hoc string concatenation.

- **A registry.** `packages/orchestration/prompt_segments.py` holds
  `PromptSegmentRegistry`: every part of a prompt is registered under a NAME,
  duplicates are rejected, and registration order is kept as the tie-break so
  composition is deterministic rather than dependent on dict iteration order.
- **Stability ranks.** `SegmentStabilityRank` is the documented scale —
  `SYSTEM=0`, `CONVENTIONS=1`, `DOSSIER=2`, `JOB_CONTEXT=3`, `TASK=4`,
  `STEERING=5`. `compose_prompt_segments` sorts by `(rank, registration index)`
  and joins with `PROMPT_SEGMENT_DELIMITER`, which is a plain blank line and
  nothing else (DECISION F105 D1).
- **A segment manifest.** Composition returns `ComposedPrompt(text, manifest)`;
  each manifest row is `name, rank, sha256, chars, tokens_estimated`. The rows
  reach evidence through `PromptTraceEntry.segment_manifest`, so a cache miss
  caused by a legitimately changed dossier is explainable after the fact
  instead of mysterious.

**Prompt CONTENT did not change — only its ORDER.** That is not a claim, it is
what the six T003 content-equality goldens assert, one per migrated role, each
freezing the pre-migration form and proving the composed segments carry the same
bytes. The table below shows the same thing from the other side: `before_total`
and `after_total` are equal in every row, because the composed prompt is a
permutation of the pre-migration one.

## What the reordering bought — MEASURED

Reproduce, from the repo root:

```bash
python3 -m tests.orchestration.test_prompt_cache_prefix
```

That prints the table below and nothing else. Its numbers come from
`measure_cacheable_prefixes()` in
`tests/orchestration/test_prompt_cache_prefix.py`, which is also the only source
the test assertions read — the figures here and the figures the suite checks
cannot drift apart.

Method, per role: two renders that differ ONLY in volatile input — the per-task
or per-round content carrying rank `TASK` or later — and are otherwise
identical. That is the situation a provider prompt cache is paid for: a second
round of the same job re-sending the same stable prefix. All four figures are in
CHARACTERS, not tokens; Remedy ships no tokenizer and would only be able to
estimate.

| Role | before_prefix | after_prefix | before_total | after_total |
|---|---|---|---|---|
| intake | 115 | 672 | 681 | 681 |
| plan | 227 | 1463 | 1548 | 1548 |
| mission | 207 | 1478 | 1576 | 1576 |
| builder | 458 | 620 | 1460 | 1460 |
| reviewer | 241 | 1134 | 1987 | 1987 |
| orchestrator | 3872 | 3872 | 3916 | 3916 |

`before_prefix` / `after_prefix` are the longest common prefix of the two
pre-migration and the two composed renders; `before_total` / `after_total` are
the length of the first render on each side.

Reading the rows:

- **intake, plan, mission** gain the most in relative terms: their rules blocks
  sat AFTER the volatile mission/intake/goal text, so the pre-migration
  cacheable prefix died a few characters into that text. Rank order puts the
  rules first and the prefix now runs to the end of them. As a share of the
  whole prompt that is 115/681 -> 672/681 for intake, 227/1548 -> 1463/1548 for
  plan, and 207/1576 -> 1478/1576 for mission: roughly a seventh of the prompt
  before, and all but the task tail after.
- **builder** gains least in relative terms, and the reason is structural
  rather than a weak result: the pre-migration builder prompt already led with
  its system block and repo facts, so 458 characters were already shared. The
  reorder moves the scope contract and the job-context blocks ahead of the task
  and carries the prefix to 620.
- **orchestrator does not move at all, and that is the expected result.** Its
  pre-migration order was ALREADY rank order, so the migration is byte-exact
  (its golden asserts `==`, not equality-modulo-ordering) and the two figures
  are identical by construction. An honest zero-delta is a result, not a gap.

The only numeric assertion the module makes is the DIRECTIONAL one the feature
file asks for, `after_prefix >= before_prefix`, per role. Exact byte counts are
deliberately not asserted: a legitimate later prompt change would then break a
test that is not about content, and the goldens already own content.

For `builder` and `reviewer` the goldens freeze RENDERS rather than templates,
so the pre-migration render for a varied fixture is reassembled from the
composed segments in the golden's own `_PRE_MIGRATION_ORDER`. That reassembly is
not invented for this note: it is exactly what those goldens assert equals their
frozen renders, and two guard tests in the measurement module re-prove it at the
parameterisation boundary.

## What is NOT measured: the provider-side cache-read share

**No ledger exists on disk in this checkout.** `ledger.sqlite` lives at
`<data_root>/projects/<project_id>/ledger.sqlite`
(`packages/orchestration/token_ledger.py`), and there is no such file anywhere
in this repository. So:

```
$ remedy stats cache
Cache-read share from the token ledger — project <id>, 0 ledger(s) read
Filters: since=-  job=-  by=-

No ledger on disk for this scope — nothing has been recorded yet.
Run 'remedy stats backfill-ledger <evidence-dir>' to mirror existing evidence.
```

and `remedy stats cache --json` reports `"cache_read_share": null` with
`"share_basis": "unmeasured"`. There are no actuals to read, so any provider-side
number on this page would be invented. The view exists and works; what it has
to work on is nothing.

### `unmeasured` is not `undefined`, and neither is `0`

The distinction is the whole point of the view, so both words are spelled out:

| Word | Meaning | When |
|---|---|---|
| `unmeasured` | **Nothing was reported.** No provider gave the inputs, so no share can be computed. | `cache_read` or `tokens_in` is NULL (`UNMEASURED`, `apps/cli/commands/stats_ledger_cmd.py`) |
| `undefined` | **The inputs WERE reported and were zero.** A real bucket that read nothing at all; a share of nothing has no value. | `tokens_in + cache_read == 0` (`UNDEFINED_SHARE`, same module) |

Neither ever renders as `0`, in the table or in `--json`. Calling an unreported
figure `unmeasured` blames nobody; calling a reported zero `unmeasured` would
blame a provider for a figure it did report; printing `0.0%` for either would
invent a measurement. `--json` keeps the two apart by carrying `share_basis`
alongside a `null` `cache_read_share`.

## Two known seams — stated, not worked around

Both were inventoried against the code before the view was written
(`.agent/t004_inventory.md` §1 and §3).

1. **A measured-looking zero the ledger cannot tell from a real one.**
   `UsageActuals.cache_read` is a plain `int` filled with `.get(..., 0) or 0`
   (`packages/orchestration/token_actuals.py`). A provider that reports usage
   but carries no cache field therefore leaves a `0`, that `0` is summed into
   the run total, written as `cache_read_input_tokens: 0`, and stored as a
   MEASURED zero rather than NULL. A provider that reports no usage at all
   leaves NULL, which is the honest value the whole `unmeasured` rendering rests
   on. The first case is indistinguishable from a genuine zero-cache run from
   the ledger alone, and this view does not pretend otherwise.

2. **The ledger's `role` is a hardcoded `builder` in production data.**
   `calls.role` is a real, indexed column and `--by role` groups on it, but the
   producer writes `"role": "builder"` unconditionally into
   `token_accounting.json` (`packages/orchestration/pingpong_loop.py`). So a
   per-role breakdown of production data would be a single bucket; every other
   bucket ever seen came from a hand-written accounting file in a fixture. The
   view prints that limit in its own output rather than burying it — the
   `role_limit` line in `--json`, and the matching note in the table — because
   presenting one bucket as a per-role breakdown would be the lie.

   The richer role vocabulary (`intake`, `flight_plan`, `orchestrator`,
   `mission_plan`, `planner`, …) exists on the PROMPT TRACE side, but five of
   those roles produce no ledger row at all: rows are only ever created from a
   task run's `provider_evidence.json`, and the intake, plan, mission and
   orchestrator call sites leave the identity fields empty. Closing that gap is
   a producer change, not a query change, and it is out of F105's scope.

## Related

- [T2_F105.md](../roadmap/features/T2_F105.md) — the target plan and its
  acceptance criteria.
- [token-economy-context-budget-optimizer-v0.md](token-economy-context-budget-optimizer-v0.md)
  — where the chars/4 token ESTIMATE comes from and why no tokenizer is vendored.
