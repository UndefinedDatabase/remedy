You are the WORKER for one round of a Remedy self-drive session. Read `/home/decodeux/Repos/remedy/AGENTS.md` first — it is the highest authority and binds you in full (commit gate, self-review loop before every commit, small commits, push after every commit, plan.md current). Work only in `/home/decodeux/Repos/remedy`.

State to verify, not assume: branch `feature/paydown0814-closure-debt` at `bc0f5223`, tree clean. Registered findings R-0359, R-0360, R-0361; none yet resolved on disk.

── STEP R3/4 — paydown0814: land the reviewer's R2 verdict and resolutions ──
Goal:        Put the reviewer's PASS verdict for R2 and its authored `Done:` resolutions for R-0359 and R-0360 onto disk, so the record is complete before PR #198 merges.
Bundle:      C0 save this block verbatim · C1 live_review.md (Steps rewrite + two Done: resolutions) · C2 plan.md + handoff.md.
Change:      Exactly these files: `.agent/authored/paydown0814-r3.md` (new), `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`. NOTHING else — no docs/, no tests/, no packages/, no apps/, no STATUS.md, no README.md.
Constraints: Do NOT merge PR #198 — the merge is R4 and runs at the Open PR Gate (docs/agents/self_drive_protocol.md G1). Never force-push. Do NOT write any `Done:` text of your own; every `Done:` byte below is reviewer-authored and is applied verbatim. Do NOT invent a new finding id — none is spent this round and the next free id stays R-0362.
──────────────────────────────────────────────────────────────

C0 — save this entire block verbatim to `.agent/authored/paydown0814-r3.md`. Commit alone: `chore(paydown0814): save the R3 block verbatim`. Push.

── C1 — apply the reviewer's verdict record and resolutions ──

Three exact-string replacements in `.agent/live_review.md`. Apply each byte for byte: do not reflow, re-wrap, re-indent or re-punctuate. The em dashes, arrows, backticks and `§` are intentional. Each `Done:` line is ONE long line — do not wrap it.

PAIR 1 — REWRITE shape (the TO does NOT contain the FROM).
FROM (verify it occurs exactly once before applying):
>>> STEPS-FROM >>>
R1 register the two candidates carried out of the F045 closure plus the gate
round's own finding, and empty `.agent/candidates.md` → R2 fix R-0359 and
R-0360, each in its own gated commit, with a red-proof for the new pin →
verdict, handoff, PR. The PR is NOT merged this session
(docs/agents/self_drive_protocol.md G1).
<<< STEPS-FROM <<<

TO:
>>> STEPS-TO >>>
R1 register the two candidates carried out of the F045 closure plus the gate
round's own finding, and empty `.agent/candidates.md` → R2 fix R-0359 and
R-0360, each in its own gated commit, with a red-proof for the new pin → R3
record the reviewer's verdict and its resolutions → R4 merge PR #198 at the
Open PR Gate, which is the round that finally turns `main` green.

R2 verdict, issued at `bc0f5223` by the second session's reviewer: PASS. Every
gate the R2 block ordered was re-run by the reviewer itself rather than read
out of the worker's report — the cap probe (`chars 3111 tokens 778 cap 800`),
`tests/orchestration/test_role_conventions.py` (`26 passed`), the content and
trailing-whitespace guards, the pair proof, the new pin by node id, the whole
`tests/docs/` suite (`295 passed`), ruff, a red-proof in the reviewer's own
disposable worktree, and the golden-path canary (`42 passed`). The change set
is exactly the five files the R2 block named; no `packages/`, `apps/`,
`STATUS.md` or `README.md` was touched. Both authored slices are byte-identical
on disk to what was applied. No block condition was hit.

inline clerical fix: the R2 handoff's Range header named `ad82b469..HEAD, 4
commits`, but that range holds 5 — it swept in `ff3f1273`, the already-reviewed
R1 handback. The reviewed R2 range is `ff3f1273..HEAD`, which is also the SHA
the R2 block itself names as the round's starting point. That header's own
per-commit table listed the correct four commits and the reviewer derived the
range mechanically, so nothing downstream was misled. Corrected here under the
ephemeral-artifact rule in docs/agents/reviewer_conventions.md; no finding id
spent, and the next free id stays R-0362.
<<< STEPS-TO <<<

PAIR 2 — APPEND shape (the TO contains the FROM verbatim, then adds).
FROM (verify it occurs exactly once before applying):
>>> D359-FROM >>>
 only prose, duplication and retold precedents are compressed. OPEN.
<<< D359-FROM <<<

TO:
>>> D359-TO >>>
 only prose, duplication and retold precedents are compressed. OPEN.

Done: R-0359 — Fixed at `2fce58c1`, verified by the reviewer at `bc0f5223`. `docs/agents/reviewer_conventions.md` was replaced in full by the authored slice; the reviewer re-ran the cap probe itself and measured `chars 3111 tokens 778 cap 800`, 22 tokens of headroom against `CONVENTIONS_TOKEN_CAP` in `packages/orchestration/prompt_segments.py`, then re-ran `python3 -m pytest tests/orchestration/test_role_conventions.py -q` → `26 passed`, exit 0, so the five ids that fail on `main` are green on this branch. Transport was proved disk to disk rather than by retype: sha256 over the CONVENTIONS slice of `.agent/authored/paydown0814-r2.md` and over the applied file are both `213b28e1c84b4b60dfc900c4dd43af32de2abb73b7dfe5f213680559a32218b8`. The content guards were re-run green — the three required headings present, `numbered 6` block conditions, no trailing whitespace, exactly one terminating newline. The reduction came from pointing the Discoverability section at AGENTS.md's Code Discoverability Conventions instead of restating them; every rule the pre-trim document carried survives, and `CONVENTIONS_TOKEN_CAP` was deliberately left alone, which is what keeps this a repair rather than a cap move. `main` itself only turns green when PR #198 merges.
<<< D359-TO <<<

PAIR 3 — APPEND shape (the TO contains the FROM verbatim, then adds).
FROM (verify it occurs exactly once before applying):
>>> D360-FROM >>>
 which runs only inside a disposable git worktree. OPEN.
<<< D360-FROM <<<

TO:
>>> D360-TO >>>
 which runs only inside a disposable git worktree. OPEN.

Done: R-0360 — Fixed at `02572f74`, verified by the reviewer at `bc0f5223`. `tests/docs/test_docs_consistency.py` gained one method, `TestPrimaryDocsAreHonest::test_the_readme_tier_table_done_column_matches_the_ledger`, which re-derives each tier's accepted count by resolving every `^- \[x\] F\d{3} — ` id in `docs/roadmap/STATUS.md` through its feature file's tier prefix via the module's existing `_feature_ids()` helper, then asserts EVERY tier row of the README table and that no accepted tier lacks a row. The reviewer re-ran the node id → `1 passed`, exit 0; `python3 -m pytest tests/docs/ -q` → `295 passed`, exit 0, exactly one more than R1's 294; `python3 -m ruff check` → `All checks passed!`, exit 0. Because the pin passes on arrival, the reviewer re-ran the RED-PROOF itself, inside its own disposable worktree at `bc0f5223` and never in the primary checkout: the import path was proved first — the probe printed `REPO /home/decodeux/Repos/remedy/.remedy-wt/reviewer_r2_red`, so the mutated copy is the one under test — and then Tier 2's `Done` cell was mutated 8 to 7 and the pin FAILED at its own assertion, `AssertionError: README Tier 2 Done=7; the ledger derives 8` with `assert 7 == 8` and the derived distribution `{0: 16, 1: 22, 2: 8}`. The worktree was removed and pruned; `git worktree list` returned to a single line and the primary checkout's `git status --porcelain` stayed empty. `README.md` was correctly NOT edited — its table already matched the ledger, so the fix is the pin, not a number change.
<<< D360-TO <<<

C1 gates — run each, report RAW output and exit code:
1. Pair proofs, counted with Python `str.count` and not grep (these strings contain backticks, braces, brackets and regex characters). After applying all three, in `.agent/live_review.md`: STEPS-FROM occurs 0 times and STEPS-TO occurs exactly 1 time (rewrite); D359-FROM occurs exactly 1 time and D359-TO exactly 1 time; D360-FROM exactly 1 time and D360-TO exactly 1 time (appends — the FROM surviving inside the TO is the expected shape here, not a failure).
2. The two added `Done:` lines each appear exactly once among the lines THIS commit's diff ADDS. Measure with `git show --numstat <sha> -- .agent/live_review.md` for the totals plus a per-line count over that diff's added lines.
3. `python3 -c "import re;t=open('.agent/live_review.md').read();o=set(re.findall(r'^- (R-\d+) — ',t,re.M));d=set(re.findall(r'^Done: (R-\d+) — ',t,re.M));print('OPEN',sorted(o-d),'DONE',sorted(d))"` → must print exactly `OPEN ['R-0361'] DONE ['R-0359', 'R-0360']`. If it prints anything else, do not adjust the text — report the output and stop.
4. `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` → must be green; it is the contract that reads this file and asserts it carries "Steps". Report the real count (it was `70 passed` before this round).

Commit C1 ALONE: `docs(paydown0814): record the R2 verdict and resolve R-0359 and R-0360`
Push.

── C2 — plan and handoff ──

Replace `.agent/plan.md` entirely with the text between the PLAN markers, byte for byte:

>>> PLAN >>>
# Plan — paydown0814 closure debt

Branch: feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the
F045 closure PR #197 merged. Next free finding id: R-0362. R-0359 and R-0360
are FIXED and RESOLVED by the reviewer at bc0f5223; R-0361 stays open as a
recorded reviewer-process finding whose counter-measure is already in force.

## Goal
Pay down the debt the F045 closure carried out on disk, so the next feature
starts on a green `main`: trim `docs/agents/reviewer_conventions.md` under its
800-token prompt-segment cap (R-0359), pin the README tier table's Done column
to the ledger (R-0360), and record the gate round's own finding (R-0361). A
paydown branch in the established shape of feature/paydown-0730, -0731, -0731b
and -0801 — it claims no STATUS line and closes no `[ ]`.

## Current Step
R3 complete: the reviewer re-ran every R2 gate itself, including its own
red-proof in a disposable worktree, issued PASS, and its authored `Done:`
resolutions for R-0359 and R-0360 are now on disk in `.agent/live_review.md`.
PR #198 is still NOT merged.

## Next Steps
1. R4 — Open PR Gate: merge PR #198 with
   `gh pr merge 198 --merge --delete-branch`, then `git checkout main` and
   `git pull --ff-only`. That merge is what finally turns `main` green, and it
   closes the operator's manual-review window.
2. Then F057 — Rate-limit-aware scheduler, per Rule A5 and STATUS order. New
   session, new branch, cut from the merged `main`.

## Risks
- `main` is RED until PR #198 merges. The five
  tests/orchestration/test_role_conventions.py ids are green on this branch,
  which is the fix's proof, but `main` itself only turns green at the merge.
- R-0361 remains open by design. Its counter-measure — a block may only order
  a command the reviewer has itself executed — was applied again in R3.
<<< PLAN <<<

Then rewrite `.agent/handoff.md` per AGENTS.md (rewrite not append; under 60 lines, or carry a "Deviations, declared" line naming the actual count and the mandated content that caused it; feature+round, branch, commit SHAs, per-commit changed-files table, REAL verification results, open-findings count, next expected action). State the reviewed range as `bc0f5223..HEAD` and give its real commit count. The next expected action is R4, the Open PR Gate merge of PR #198.

Commit C2: `chore(paydown0814): handback R3`. Push.

Final report — give me, with RAW output and exit codes: every gate 1-4 above, plus `git log --oneline -n 5`, `git show --numstat` for each of C0/C1/C2, `git status --porcelain` (say "empty" explicitly if it is), `git worktree list`, and `python3 -m pytest tests/cli/test_golden_path.py -q` (the canary, mandatory every handback).

Do NOT merge PR #198. Do NOT push to main. If anything blocks you, say exactly what blocked you and stop without improvising.
