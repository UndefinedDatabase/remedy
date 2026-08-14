You are the WORKER for one round of a Remedy self-drive session. Read `/home/decodeux/Repos/remedy/AGENTS.md` first — it is the highest authority and binds you in full (commit gate, self-review loop before every commit, push discipline, scope control). Work only in `/home/decodeux/Repos/remedy`.

Current state you may verify but must not assume: on `main` at `1e7f7bca`, tree clean, no open PRs, F045 closed and merged.

── STEP R1/2 — paydown0814: branch, state reset, candidate registration ──
Goal:        Open the paydown branch and PERSIST the three findings first, so nothing is lost if this session dies before the fixes land.
Bundle:      C0 save this block verbatim · C1 branch + state reset + register R-0359/R-0360/R-0361 + empty candidates.md.
Change:      A new branch `feature/paydown0814-closure-debt`. Exactly these files: `.agent/authored/paydown0814-r1.md` (new), `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md`, `.agent/candidates.md`. NOTHING else — no docs/, no tests/, no packages/, no apps/. The two fixes are the NEXT round's, not this one's.
Constraints: This is a paydown branch, not a roadmap feature — do NOT touch `docs/roadmap/STATUS.md` or `README.md`. Do not create a PR this round. Never force-push. Never commit on `main`.
──────────────────────────────────────────────────────────────

BRANCH FIRST:
`git checkout main && git pull --ff-only && git checkout -b feature/paydown0814-closure-debt`
Confirm `git branch --show-current` before any edit.

C0 — save this block verbatim.
Write the ENTIRE text of this prompt, byte for byte, to `.agent/authored/paydown0814-r1.md`. Commit alone:
`chore(paydown0814): save the R1 block verbatim`
Push.

C1 — state reset and candidate registration. Four files, ONE commit.

Apply each authored text below EXACTLY as written between its markers, EXCLUDING the marker lines. Full-file replacement for all four. Do not reflow, re-wrap, re-indent, re-punctuate, or "improve" any of them. Do not add a trailing blank line beyond the single newline ending the last line. Each file is a complete replacement of the file that is there now.

>>> LIVE-REVIEW >>>
# Live Review — paydown0814 closure debt

> Round-by-round review record for the paydown0814 branch, reset at the branch
> claim. The F045 record closed with PR #197, merged 2026-08-14 at this
> session's Open PR Gate; that round's verdict lives in the PR's closure
> comment, per docs/agents/planner_reviewer_prompt.md §4 item 13. Finding ids
> continue the monotonic R-XXXX series across the reset. Next free id: R-0362.

## Steps
R1 register the two candidates carried out of the F045 closure plus the gate
round's own finding, and empty `.agent/candidates.md` → R2 fix R-0359 and
R-0360, each in its own gated commit, with a red-proof for the new pin →
verdict, handoff, PR. The PR is NOT merged this session
(docs/agents/self_drive_protocol.md G1).

## Findings

- R-0359 — Medium — the reviewer conventions document is over its prompt-segment token cap, and `main` is red because of it. `docs/agents/reviewer_conventions.md` is 3813 characters, which `token_economy.estimate_text_tokens` — documented as `chars/4` and implemented as `math.ceil(len(text) / _CHARS_PER_TOKEN)` — turns into 954 tokens against the `CONVENTIONS_TOKEN_CAP` of 800 in `packages/orchestration/prompt_segments.py`, so the registry's `register` raises `PromptSegmentError: prompt segment 'reviewer_conventions' is over its token cap: 954 tokens estimated, cap 800` and five ids in `tests/orchestration/test_role_conventions.py` fail on `main` itself. The reviewer reproduced this at `1e7f7bca` with a full `pytest -n auto`: `5 failed, 16769 passed, 19 skipped in 132.23s`, the five being exactly those ids. Present since `a85e82f5` (2026-08-12); F115 and F045 both closed over it under DECISION F045 D8, which routes the repair to its own branch because AGENTS.md forbids mixing an unrelated fix into a feature branch. Carried out of the F045 closure as candidate 1 and registered here with the next free id. Fix by trimming the document under the cap WITH headroom: the worker conventions document sits at 740 tokens, and a repair landing at 799 re-breaks `main` on the next clause anyone adds. Every RULE in the document survives the trim — only prose, duplication and retold precedents are compressed. OPEN.

- R-0360 — Low — the README tier table's `Done` column is unpinned and silently drifted. `tests/docs/test_docs_consistency.py` pins the prose count beside it with `test_the_readme_accepted_count_equals_the_status_count` (R-0156), but no assertion reads the per-tier `Done` cells of the `## Status` table, so the Tier 2 cell sat at 6 while the ledger derived 7 from the F111 closure (`98a49b5c`, 2026-08-13) until the F045 closure corrected it to 8. The reviewer re-derived the true distribution at `1e7f7bca` by resolving every `^- \[x\] F\d{3} — ` id in `docs/roadmap/STATUS.md` through its feature file's tier prefix: tier 0 = 16, tier 1 = 22, tier 2 = 8, every other tier 0, total 46 — which the README's eighteen tier rows currently match, so the pin passes on arrival. Carried out of the F045 closure as candidate 2 and registered here. Fix by adding a pin that performs that derivation and asserts EVERY tier row, reusing the module's existing `_feature_ids()` helper rather than writing a second spelling of it. Because the pin passes on arrival it is worthless without a red-proof, which runs only inside a disposable git worktree. OPEN.

- R-0361 — Low — a gate round ordered a proof command the session cannot execute, and asserted an exit code the fetch tool contradicts. The R1 gate block ordered the posted F045 verdict fetched back with `gh api --paginate ... --jq '.[-1].body'` and `cmp`-ed against the authored file, expecting exit 0. `gh api` is denied by this session's permission layer, so the ordered command never ran at all; the worker's substitute, `gh pr view 197 --json comments --jq`, exited 1 because the `--jq` writer appends a newline to a body that already ends in one, leaving the fetched file exactly one byte longer with no differing byte in the common prefix. The worker proved equality the honest way instead — extracting the raw JSON body with no jq in the path, where the sha256 of the posted bytes and of the authored file are both `b9db4e4c41cf59c0c4adcfa8368c83843e2c0ee4e29ceab0b324864ebc19f5ff` and `cmp` exits 0 — declared both deviations in its report, and proceeded rather than burning the round on a tooling artifact. The reviewer re-verified that byte equality independently at `1e7f7bca` and agrees the merge was safe; nothing landed wrong. This is the R-0252/R-0336/R-0350 family — an ordered gate whose expected value the reviewer never computed from the tool that produces it — plus a second failure the existing counter-measures do not reach: ordering a command the permission layer denies makes the gate UNREACHABLE rather than merely wrong, and an unreachable gate cannot fail honestly. Counter-measure, applied from R2 on: a block may only order a command the reviewer has itself executed in this session, and a byte-equality claim over any transport that may normalise trailing newlines is stated as a sha256 comparison over extracted bytes, never as a `cmp` exit code. OPEN.
<<< LIVE-REVIEW <<<

>>> PLAN >>>
# Plan — paydown0814 closure debt

Branch: feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the
F045 closure PR #197 merged at this session's Open PR Gate. Next free finding
id: R-0362. Open findings: 3 — R-0359 (Medium), R-0360 (Low), R-0361 (Low).

## Goal
Pay down the debt the F045 closure carried out on disk, so the next feature
starts on a green `main`: trim `docs/agents/reviewer_conventions.md` under its
800-token prompt-segment cap (R-0359), pin the README tier table's Done column
to the ledger (R-0360), and record the gate round's own finding (R-0361). A
paydown branch in the established shape of feature/paydown-0730, -0731, -0731b
and -0801 — it claims no STATUS line and closes no `[ ]`.

## Current Step
R1: the state reset, the three registered findings and the emptied
`.agent/candidates.md`, committed and pushed. No fix lands this round — the
findings persist FIRST so nothing is lost if the session dies.

## Next Steps
1. R2 — trim the conventions document under the cap WITH headroom, and add the
   README tier pin, each in its own gated commit.
2. R2 — red-proof the new pin inside a disposable git worktree, rewrite the
   handoff, push, open the PR. The PR is NOT merged this session
   (docs/agents/self_drive_protocol.md G1).
3. Next roadmap feature per Rule A5 and STATUS order: F057 — Rate-limit-aware
   scheduler. New session, new branch, after this PR merges at that session's
   Open PR Gate.

## Risks
- `main` is RED until this branch merges: five
  `tests/orchestration/test_role_conventions.py` ids fail at 1e7f7bca. Round
  gates are therefore scoped, and those five going GREEN is R-0359's own proof.
- The README pin passes on arrival, so it proves nothing without a red-proof;
  that proof runs only in a disposable worktree (self_drive_protocol.md G5).
- Trimming a reviewer-facing rules document is a content decision. The trim
  keeps every rule and is recorded as such; a lost rule would be a finding.
<<< PLAN <<<

>>> CONTEXT >>>
# Context — paydown0814 closure debt

## Active Branch
feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the F045
closure PR #197 merged at this session's Open PR Gate. No STATUS line is
claimed: this is a paydown branch, not a roadmap feature. The next roadmap
feature is F057, Rate-limit-aware scheduler, and it starts in a new session.

## Scope
In: `docs/agents/reviewer_conventions.md`, trimmed under the 800-token
prompt-segment cap with headroom (R-0359); a new pin in
`tests/docs/test_docs_consistency.py` deriving the README tier table's Done
column from the ledger (R-0360); `.agent/**` state, including emptying
`.agent/candidates.md` now that both carried candidates are registered.

Out: every RULE the conventions document states — the trim compresses prose,
duplication and retold precedents, never a rule; `CONVENTIONS_TOKEN_CAP`
itself, which is production code and a P4 principle; `docs/roadmap/STATUS.md`
and `README.md`, which no paydown branch touches; F057 and all feature work.

## Constraints
- No production code: this branch touches docs/, tests/ and .agent/ only, so
  no packages/ or apps/ file is in scope.
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate, and never a PR this session created (G1);
  never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. Destructive and red-proof checks run only
  inside a disposable git worktree, so resource safety stays intact and no
  background pytest process is ever left running.
- A round pushes after EVERY commit, not once at its last step (R-0289).

## Steps
R1 state reset and candidate registration → R2 the two fixes, each gated, the
new pin red-proved → handoff and PR. The PR stays unmerged this session.
<<< CONTEXT <<<

>>> CANDIDATES >>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

(empty — both F045 candidates were registered as findings R-0359 and R-0360 in
`.agent/live_review.md` on the paydown0814 branch, 2026-08-14.)
<<< CANDIDATES <<<

Commit all four in ONE commit:
`chore(paydown0814): persist round state, register the carried candidates`
Push.

Done when — run each and report the RAW output with its exit code:
a. `git branch --show-current` → `feature/paydown0814-closure-debt`
b. `cmp .agent/authored/paydown0814-r1.md` against nothing is not possible, so instead prove the save is faithful by reporting `wc -l .agent/authored/paydown0814-r1.md` and `sha256sum` of it, plus the FIRST and LAST line of the file.
c. No trailing whitespace in any of the five written files:
   `python3 -c "import sys;[print(p,[i+1 for i,l in enumerate(open(p).read().split(chr(10))) if l!=l.rstrip()]) for p in sys.argv[1:]]" .agent/authored/paydown0814-r1.md .agent/live_review.md .agent/plan.md .agent/context.md .agent/candidates.md`
   Every list must be `[]`.
d. `wc -l .agent/plan.md` → must be under 50.
e. Open-finding set derived MECHANICALLY from the record, not from this block:
   `python3 -c "import re;t=open('.agent/live_review.md').read();o=set(re.findall(r'^- (R-\d+) — ',t,re.M));d=set(re.findall(r'^Done: (R-\d+) — ',t,re.M));print('OPEN',sorted(o-d))"`
   → must print `OPEN ['R-0359', 'R-0360', 'R-0361']`
f. `grep -c "^## Steps" .agent/live_review.md` → 1
g. `grep -c "## Active Branch" .agent/context.md` → 1
h. State-file contract tests still green:
   `python3 -m pytest tests/docs/ -q`
   `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/ui_server/test_dashboard_contract.py -q`
   Report the real pass/fail counts. If ANY of these goes red, STOP and report the exact failure — do not improvise a fix to the authored text; the reviewer authored it and will repair it.
i. `git status --porcelain` → must be EMPTY. Say "empty" explicitly.
j. `git log --oneline -n 3` and, for EACH of the two commits, `git show --numstat <sha>`.
k. `git rev-list --left-right --count origin/feature/paydown0814-closure-debt...HEAD` → `0	0` after pushing.

Handback: rewrite `.agent/handoff.md` (AGENTS.md rules: rewrite not append, under 60 lines unless a stated-cause line names the overage, feature+round, branch, commit SHAs, changed-files table, real verification results, open-findings count, next expected action) and commit it as a third commit `chore(paydown0814): handback R1`, then push. Also give me the same content as your completion report, with the RAW command output for every check above. Report `git status --porcelain` even when empty.

Do NOT create a PR. Do NOT merge anything. Do NOT write any `Done:` paragraph into `.agent/live_review.md` — `Done:` is reserved for reviewer-authored text; if you fix something before the reviewer has authored its resolution, mark it `Landed: R-XXXX — <one line>` instead. If anything blocks you, say exactly what and stop.
