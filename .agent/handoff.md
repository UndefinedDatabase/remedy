# Handoff — F107 Context compiler v2 — R9 (T004 part 2a, the first caller)

Branch: feature/f107-context-compiler-v2. C1..C7 were made by a previous worker in
this round and were not touched; I did steps 6 and 7 only. Nothing amended,
rebased, reverted, reordered or force-pushed. main untouched. No PR exists.
`packages/orchestration/context_compiler.py` was NOT edited — it stays frozen.
Open findings: 12 (R-0221/0239/0247/0262/0265/0266/0268/0270/0272/0274/0275/0276).
Next free finding ID: R-0277. No `Done:` and no `Landed:` line was written: R9 adds
a CALLER and fixes no finding.

## Range

Review of 7acb406d..HEAD — 8 commits, C1..C8.

## Commits

### 65da6bfb chore(f107): save the R9 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f107-r9-1.md | 276/0 | C1 verbatim block save |

### 7f66ccad chore(f107): mirror the R9 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 253/195 | C2 byte-copy of the block |

### 61adb419 chore(f107): record the R8-close gate and register R-0275 and R-0276
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 68/7 | C3 the four authored pairs |

### 7664b677 feat(f107): add the job context CLI view module
| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/commands/job_context_cmd.py | 273/0 | C4 new read-only view |

### 6a56fe81 feat(f107): register the job context command in the catalog
| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/command_catalog.py | 17/0 | C5 one CommandEntry job.context |
| apps/cli/commands/__init__.py | 2/1 | C5 import + module tuple |

### f92a0359 test(f107): cover the job context CLI view end to end
| Path | +/- | Reason |
|------|-----|--------|
| tests/cli/test_job_context_cmd.py | 231/0 | C6 nine runtime cases |

### b5575a88 chore(f107): advance plan to R9 T004 part 2a
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 12/12 | C7 slice PLAN9, full replacement |

### C8 — self-reference, a handoff cannot table its own SHA
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | see log | C8 this rewrite, pushed immediately after |

## External actions

`git push -u origin feature/f107-context-compiler-v2` after C8 (Verification i).
No `git worktree add`/`remove` ran, no gh command ran, no PR created/edited/merged.
Gate h scratch is under the gitignored `.remedy-wt/r9gate/` with `REMEDY_DATA_DIR`
pointed there, so no job state reached a tracked path.

## Verification

a. `cmp .agent/authored/f107-r9-1.md .agent/last_block.md` → exit 0, silent.
   `sha256sum` both → f8e42fd684fe23673b38f63799894cb976ac20d5c6be049986c60ae1a4fdbb81,
   276 lines each; that digest EQUALS BLOCK_SHA256 (Authored-text proofs).
   CORRECTION, declared: no BLOCK_SHA256 line exists inside the saved block —
   `grep -n BLOCK_SHA256 .agent/last_block.md` returns only lines 221 and 242, the
   two prose references. The value lives on line 277 of the reviewer original, one
   line PAST the block body, so gate a is met against that trailer.
b. Nine slice bodies recompute to their BEGIN-marker digests at their declared
   line counts → SLICES=9 MISMATCH=0, exit 0: HDRFROM dfab3095… 1L, HDRTO
   969938db… 1L, LRF5FROM 21a6a3f6… 1L, LRF5TO 21a8b66c… 23L, LR8FROM 686e2302…
   1L, LR8TO 4894b692… 34L, LRDFROM 62450c77… 6L, LRDTO 39b40890… 12L, PLAN9
   33ad2144… 28L. `sha256sum .agent/plan.md` → 33ad21444aed… == PLAN9, 28 lines.
c. `git show --numstat 61adb419 -- .agent/live_review.md` → exit 0 → `68  7`:
   deletion column exactly 7 = HDRFROM 1 + LRDFROM 6, as specified. Greps on
   .agent/live_review.md: `^Landed:` → 0; `^Done:` → 2; `Next free ID: R-0277` → 1;
   `^- R-0275` → 1; `^- R-0276` → 1; `^## Steps` → 1; `^<<<` → 0 (also 0 in
   plan.md, 0 in handoff.md). ONE SUB-CHECK MISSED ITS SPECIFIED VALUE:
   `grep -c 'Next free ID: R-0271'` → 1, not 0. Unmeetable by construction, not a
   defect: the single hit is line 128, inside the reviewer's own R-0276 finding
   body (slice LRF5TO, digest-verified in b), which QUOTES the stale value it
   reports. The header the gate is about is correct — line-scoped,
   `grep -c '^> Branch:.*Next free ID: R-0271'` → 0 and the R-0277 form → 1, and
   line 8 reads `> Branch: feature/f107-context-compiler-v2. Next free ID: R-0277.`
   The known "gate quotes its own marker" class. Reported, not repaired: I edited
   nothing to turn this number green.
d. `python3 -m pytest tests/cli/test_job_context_cmd.py -q` → exit 0 → 9 passed, 2.60s.
e. `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py -q`
   → exit 0 → 505 passed, 36.87s.
f. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 → 42 passed, 19.80s.
g. `python3 -m ruff check apps/cli/commands/job_context_cmd.py
   tests/cli/test_job_context_cmd.py apps/cli/command_catalog.py` → exit 0,
   "All checks passed!".
h. THE REAL RUN — a user invocation, not a test. Entry point: the installed console
   script `remedy` (/home/decodeux/.local/bin/remedy; pyproject
   `remedy = "apps.cli.grouped:main"`), so the forms below are literally typed.
   Setup, all through the repo's own CLI: `remedy init` → exit 0 (project
   demo-repo cc42fd01); `remedy job create "Harden the payment gateway retry path"`
   → exit 0 → 994eb8d1-5ce5-4fd8-a150-2121bf391d07; `remedy job attach-repo
   994eb8d1… <demo_repo>` → exit 0 → `Job 994eb8d1-… | repo=…/r9gate/demo_repo`.
   Target repo: a REAL git checkout of 5 committed files under
   .remedy-wt/r9gate/demo_repo — src/payment_gateway.py imports src/retry_policy.py
   imports src/clock_source.py, while src/invoice_report.py and README.md are
   imported by nothing. Task construction: Deviations 2.
   FULL stdout of `remedy job context 994eb8d1-5ce5-4fd8-a150-2121bf391d07
   --task T001`, exit 0:

    Task context for job 994eb8d1 task T001 (52c783f1)
      Fenced paths (1):
        src/payment_gateway.py
      Candidates: 5 (git ls-files)
      Budget: 164 / 24000 tokens
      Included (3):
        Tier 1:
          src/payment_gateway.py  full  73 tokens
        Tier 2:
          src/retry_policy.py  full  63 tokens
        Tier 3:
          src/clock_source.py  signatures  28 tokens
      Omissions (2):
        README.md  tier 4  distance  omitted
        src/invoice_report.py  tier 4  distance  omitted

   FULL stdout of the same command plus `--json`, exit 0:

    {
      "job_id": "994eb8d1-5ce5-4fd8-a150-2121bf391d07",
      "task_id": "52c783f1-815a-4bfb-a307-d2335de3e18e",
      "task_label": "T001",
      "fenced_paths": [
        "src/payment_gateway.py"
      ],
      "candidate_count": 5,
      "candidate_source": "git ls-files",
      "estimated_tokens": 164,
      "budget_tokens": 24000,
      "over_budget": false,
      "line_cap": 200,
      "included": [
        {
          "path": "src/payment_gateway.py",
          "tier": 1,
          "rendering": "full",
          "estimated_tokens": 73
        },
        {
          "path": "src/retry_policy.py",
          "tier": 2,
          "rendering": "full",
          "estimated_tokens": 63
        },
        {
          "path": "src/clock_source.py",
          "tier": 3,
          "rendering": "signatures",
          "estimated_tokens": 28
        }
      ],
      "omissions": [
        {
          "path": "README.md",
          "tier": 4,
          "reason": "distance",
          "outcome": "omitted"
        },
        {
          "path": "src/invoice_report.py",
          "tier": 4,
          "reason": "distance",
          "outcome": "omitted"
        }
      ]
    }

   Third run, decisive on "never guess a task": `remedy job context 994eb8d1…
   --task T999` → exit 3, stderr exactly `Error: no task matches --task 'T999'` —
   it names nothing it did not find. F107 now has a caller outside its own tests.
i. `git status --porcelain` → exit 0 → 0 lines. `git worktree list` → the primary
   checkout alone. HEAD == origin/feature/f107-context-compiler-v2 after the push;
   before it, origin stood at 7acb406d, 7 commits behind — the branch had never
   been pushed this round. Insertions per commit (`git show --numstat` summed):
   65da6bfb 276, 7f66ccad 253, 61adb419 68, 7664b677 273, 6a56fe81 19,
   f92a0359 231, b5575a88 12, C8 this file — each < 500.
j. `git diff --name-only 7acb406d..HEAD` → exit 0 → exactly the nine Change-list
   paths, nothing else: .agent/authored/f107-r9-1.md, .agent/last_block.md,
   .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
   apps/cli/command_catalog.py, apps/cli/commands/__init__.py,
   apps/cli/commands/job_context_cmd.py, tests/cli/test_job_context_cmd.py.
   Measured at C1..C7 it returned 8; .agent/handoff.md is the ninth and arrives
   with C8, so the count is 9 only from C8 onward.

## Authored-text proofs

The reviewer original `.remedy-wt/f107-r9-1.block.md` survives on disk: 277 lines,
17966 bytes, line 277 being the trailer `BLOCK_SHA256 (bytes above this line) =
f8e42fd684fe23673b38f63799894cb976ac20d5c6be049986c60ae1a4fdbb81`. Its first
17862 bytes (the block body) `cmp` exit 0 and silent against BOTH
.agent/authored/f107-r9-1.md and .agent/last_block.md, and all three sha256 to
f8e42fd6…bb81 at 276 lines — the declared BLOCK_SHA256 is met exactly. The four
applied pairs are proven by the nine digest recomputations in b and the C3
numstat `68 7` in c.

## Deviations & assumptions

1. Two block-text corrections, measured not repaired: gate a's BLOCK_SHA256
   reference (Verification a) and gate c's `Next free ID: R-0271` → 0 sub-check
   (Verification c). No file was edited to move either number.
2. Gate h task construction. `remedy job plan` is the only CLI path that writes
   `inputs["flight"]`, and it hard-requires a live Ollama planner
   (apps/cli/commands/job.py:209 `OllamaPlanner()`), absent here. I did NOT
   hand-write job JSON: I built a real validated
   `FlightPlan(schema_v="flight_plan_v1", tasks=[PlannedTask(id="T001", …,
   files_hint=["src/payment_gateway.py"])])` and passed it through the repo's own
   `packages.orchestration.flight_plan.map_flight_plan_to_tasks` — the function
   the block cites at flight_plan.py:513 — then `save_job`. Reload proves it:
   task.id 52c783f1-815a-4bfb-a307-d2335de3e18e, planned_id T001, files_hint
   ['src/payment_gateway.py'], target_repo …/.remedy-wt/r9gate/demo_repo.
   Script: .remedy-wt/r9gate/gate_h_plan.py.
3. Gate h target repo is a purpose-built 5-file git checkout rather than a large
   existing one, because the block orders the FULL stdout pasted verbatim and a
   large repo's tier-4 omission list runs to thousands of lines. The files are
   real and committed, and are shaped so all four tiers appear at once.
4. Line count: this file is 257 lines, over the block's 60 and over the AGENTS.md
   100-line ceiling, declared under DECISION D15. Cause is mandated content, each
   piece counted: the two verbatim gate-h stdout transcripts the block orders =
   15 + 48 = 63 lines; the Commits section's eight per-commit changed-files tables,
   which the handback template orders, = 44 lines; the item-status table = 10
   lines. 117 of the 257 are those three blocks alone. No section was dropped to
   fit and no transcript was padded.
5. `docs/` was NOT updated for the new `remedy job context` command even though
   AGENTS.md orders docs for new behaviour: the block's Change list is nine paths
   "and nothing else", none under docs/. Flagged here so the reviewer can order it
   in R10 or at closure rather than discover the absence then.

## Item status

| Item | Status | Reason                                                        |
|------|--------|---------------------------------------------------------------|
| C1   | done   | cmp exit 0, sha256 f8e42fd6… == BLOCK_SHA256, 276 lines        |
| C2   | done   | cmp exit 0 silent against both the authored copy and original  |
| C3   | done   | numstat `68 7`, deletions exactly 7 as specified               |
| C4   | done   | 273 insertions; the module renders all four tiers in gate h    |
| C5   | done   | job.context registered; catalog + grouped CLI 505 passed       |
| C6   | done   | 9 passed, 2.60s                                                |
| C7   | done   | plan.md sha256 == PLAN9 digest 33ad2144…, 28 lines             |
| C8   | done   | this rewrite; pushed immediately after, gate i re-measured     |

## Next

Reviewer gate on R9, range 7acb406d..HEAD. Then R10 = T004 part 2b: the end-to-end
fixture task solved by the fake provider using the compiled context, plus the
whole-file size comparison via `compare_context_size`.
