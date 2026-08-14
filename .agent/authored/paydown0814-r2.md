You are the WORKER for one round of a Remedy self-drive session. Read `/home/decodeux/Repos/remedy/AGENTS.md` first — it is the highest authority and binds you in full (commit gate, self-review loop before every commit, small commits, push after every commit, plan.md current). Work only in `/home/decodeux/Repos/remedy`.

State to verify, not assume: branch `feature/paydown0814-closure-debt` at `ff3f1273`, tree clean. Open findings R-0359, R-0360, R-0361.

── STEP R2/2 — paydown0814: land both fixes ──────────────────
Goal:        Fix R-0359 (conventions document over its token cap, which is why `main` is red) and R-0360 (unpinned README tier table), each in its own gated commit, and open the PR.
Bundle:      C0 save this block verbatim · C1 R-0359 · C2 R-0360 + red-proof · C3 plan + handoff, PR.
Change:      Exactly these files: `.agent/authored/paydown0814-r2.md` (new), `docs/agents/reviewer_conventions.md` (full replacement), `tests/docs/test_docs_consistency.py` (one method inserted), `.agent/plan.md`, `.agent/handoff.md`. NOTHING else — no packages/, no apps/, no STATUS.md, no README.md.
Constraints: Do NOT edit `README.md` — R-0360 is fixed by pinning the table, and the table is already correct. Do NOT change `CONVENTIONS_TOKEN_CAP`; the cap is production code and a P4 principle, and moving it would defeat the fix. Never force-push. Do NOT merge the PR (docs/agents/self_drive_protocol.md G1).
──────────────────────────────────────────────────────────────

C0 — save this block verbatim to `.agent/authored/paydown0814-r2.md`. Commit alone: `chore(paydown0814): save the R2 block verbatim`. Push.

── C1 — R-0359: trim the conventions document under its cap ──

Replace the ENTIRE contents of `docs/agents/reviewer_conventions.md` with the text between the CONVENTIONS markers below, EXCLUDING the marker lines. Byte for byte: do not reflow, re-wrap, re-indent, re-punctuate, or restore anything you think was lost. The em dashes, the `§`, and the pipe characters in `Blocker|High|Medium|Low` are all intentional. End the file with exactly one newline.

This text is 3111 characters. `token_economy.estimate_text_tokens` is `math.ceil(len(text) / 4)`, so it estimates 778 tokens against the cap of 800 — 22 tokens of headroom, deliberately, because a repair that lands at 799 re-breaks `main` on the next clause anyone adds. If your applied file does not measure 3111 characters, you have altered the text; re-apply it rather than adjusting the number.

>>> CONVENTIONS >>>
# Reviewer Conventions (stable prompt segment)

> The F105 "conventions" segment for the review role: the CONTENT rules only.
> Verdict FORMAT is the F005 review_verdict schema. Cap 800 tokens, estimated
> as chars/4 (P4) — keep headroom, and point at a rule rather than restate it.

## Stance

Independent track. The reviewer verifies; it never fixes, refactors or
implements. Distrust the worker summary: verify bottom-up — diff, verification
commands, rendered output vs. docs/ui/design_reference/ — never from memory.

## Findings

Stable numbered IDs (R-XXXX, continuing the series). Each carries severity per
.agent/review_protocol.md's scale (Blocker|High|Medium|Low; legacy
BLOCK=Blocker, MAJOR=High, MINOR=Medium/Low), evidence (file:line or a
reproduction step), and the violated criterion. A finding without evidence is
dropped or upgraded.

## Block conditions — any single one forces FINDINGS (blocking)

1. Data fabrication: a displayed value not traceable to a real source
2. False live indicators: implied live state over static or mocked data
3. Design-fidelity violation vs. docs/ui/design_reference/ with no
   assumption_log entry (A8/F101)
4. Missing changed-files table in the worker report (R-0070 class)
5. Unverified completion claims (assertion without reproducible evidence)
6. Silent scope change vs. the task/mission

## Specified route exercised

A feature whose spec names a runtime route (executor, provider call, gate
invocation) is not accepted until evidence shows that route EXECUTED
end-to-end; unit tests of its parts do not suffice. Precedent: R-0184, the
F075 R4 diagnosis of F070.

## Verdict

Per A2/F005: PASS or FINDINGS (PASS_WITH_RISKS only where the schema allows and
no block condition is hit). A wrong spec is its own finding routed to planning,
never a reason to pass non-conforming work. No new feature starts while
findings are open (A2).

## Discoverability, checked

Raise AGENTS.md's Code Discoverability Conventions as findings on new or
touched code: an exported name of one generic word or one greping to unrelated
hits; two spellings of one concept in a diff; a test file not named after its
source; a plausible argument swap left untyped; a non-obvious definition with
no one-line WHY comment above it; a deliberate absence the change relies on but
never states in prose. A mass rename of untouched code is itself a finding —
churn is the enemy.

## Inline clerical correction

A Low defect made BY the reviewer or worker IN an ephemeral coordination
artifact — handoff, plan, a live_review entry's wording, an authored block not
yet applied — MAY be fixed in the same round without spending an ID, provided
ALL of: (1) it lands in that round's own commit; (2) the round record carries
one line, 'inline clerical fix: <what>'; (3) no product code, test, evidence
file, gate result or AGENTS.md rule is involved — those ALWAYS take an ID;
(4) it was caught before anything downstream consumed the artifact. IDs measure
substance. Precedent: the inline DECISION path, planner_reviewer_prompt.md §4
item 7. Motivation: F105 (30 of 35 findings clerical).
<<< CONVENTIONS <<<

C1 gates — run each, report RAW output and exit code:
1. `python3 -c "from packages.orchestration.token_economy import estimate_text_tokens as e; t=open('docs/agents/reviewer_conventions.md').read(); print('chars',len(t),'tokens',e(t),'cap',800,'headroom',800-e(t))"`
   → must print `chars 3111 tokens 778 cap 800 headroom 22`.
2. `python3 -m pytest tests/orchestration/test_role_conventions.py -q` → must be fully GREEN, 0 failed. Report the real counts. These five ids were FAILING before this commit; their going green IS the proof.
3. Content guards, run explicitly rather than trusted to the suite:
   `python3 -c "import re;t=open('docs/agents/reviewer_conventions.md').read();print([a for a in ('## Stance','## Findings','## Block conditions') if a not in t]);s=t.split('## Block conditions',1)[1].split(chr(10)+'## ',1)[0];print('numbered',len([l for l in s.split(chr(10)) if re.match(r'^\d+\. ',l)]))"`
   → must print `[]` then `numbered 6`.
4. No trailing whitespace in the applied file (same one-liner shape you used in R1) → `[]`.

Commit C1 ALONE: `fix(paydown0814): trim the reviewer conventions under its token cap`
Push.

── C2 — R-0360: pin the README tier table ──

Insert ONE new test method into `tests/docs/test_docs_consistency.py`, immediately after `test_the_readme_accepted_count_equals_the_status_count` and before `test_the_f010_documents_describe_all_three_scopes`. This is a REWRITE-shaped pair, not an append: apply it with an exact-string replacement.

FROM (occurs exactly once in the file — verify that before applying):
>>> PIN-FROM >>>
            f"{accepted}")

    def test_the_f010_documents_describe_all_three_scopes(self):
<<< PIN-FROM <<<

TO:
>>> PIN-TO >>>
            f"{accepted}")

    def test_the_readme_tier_table_done_column_matches_the_ledger(self):
        """R-0360: pin the README tier table's Done column to the ledger.

        The prose count beside this table is pinned by the test above
        (R-0156), but nothing read the per-tier ``Done`` cells, so they
        drifted silently: the Tier 2 cell sat at 6 while the ledger derived
        7 from the F111 closure until the F045 closure wrote 8. Derive each
        tier's count the way a reviewer derives it by hand at closure —
        every accepted STATUS id resolved through its feature file's tier
        prefix — and pin every row of the table, not just the one that moved.
        """
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        features = _feature_ids()

        derived: dict[int, int] = {}
        for m in re.finditer(r"^- \[x\] F(\d{3}) — ", status, re.MULTILINE):
            num = int(m.group(1))
            assert num in features, f"F{num:03d} is accepted with no feature file"
            tier = features[num][0]
            derived[tier] = derived.get(tier, 0) + 1

        rows = re.findall(r"^\| (\d{1,2}) \| [^|]+ \|\s*(\d+) \|\s*(\d+) \|$",
                          readme, re.MULTILINE)
        assert rows, "README must carry the Tier status table"
        listed = set()
        for tier_text, done_text, _total_text in rows:
            tier = int(tier_text)
            listed.add(tier)
            assert int(done_text) == derived.get(tier, 0), (
                f"README Tier {tier} Done={done_text}; the ledger derives "
                f"{derived.get(tier, 0)}")
        missing = sorted(set(derived) - listed)
        assert not missing, f"accepted tiers with no README row: {missing}"

    def test_the_f010_documents_describe_all_three_scopes(self):
<<< PIN-TO <<<

C2 gates — run each, report RAW output and exit code:
5. Pair proof (REWRITE shape): after applying, the FROM string occurs 0 times and the TO string occurs exactly 1 time in `tests/docs/test_docs_consistency.py`. Count with Python `str.count`, not grep — these strings contain braces, quotes and regex characters.
6. `python3 -m pytest tests/docs/test_docs_consistency.py::TestReadmeStatus -q` if that is the enclosing class, otherwise run the new test by node id. Report the node id you ran and the result.
7. `python3 -m pytest tests/docs/ -q` → report the count. It must be exactly ONE more than the 294 that passed at R1, i.e. 295. If it is not, do not adjust anything — report the number and stop.
8. `python3 -m ruff check tests/docs/test_docs_consistency.py` → report output and exit code. If ruff is unavailable, say so.

9. RED-PROOF — MANDATORY, and it runs ONLY inside a disposable git worktree, never in the primary checkout (docs/agents/self_drive_protocol.md G5). The new pin PASSES on arrival, so without this it proves nothing.
   a. `git worktree add .remedy-wt/paydown0814_r2_red HEAD`
   b. Inside that worktree ONLY, edit its `README.md` tier row for Tier 2 from `| 2 | Minimal Self-Build Runtime | 8 | 14 |` to `| 2 | Minimal Self-Build Runtime | 7 | 14 |`.
   c. Prove the probe imports the WORKTREE's copy and not the primary checkout's (finding R-0337): from inside the worktree run
      `python3 -c "import sys;sys.path.insert(0,'tests/docs');import test_docs_consistency as m;print('REPO',m.REPO)"`
      and report the printed path. It MUST be under `.remedy-wt/paydown0814_r2_red`. If it is not, the red-proof is void — say so and stop.
   d. From inside the worktree run the new test by node id. It MUST FAIL, and it must fail at its OWN assertion — report the full assertion message. A failure with a different message (import error, collection error) does not count.
   e. `git worktree remove --force .remedy-wt/paydown0814_r2_red` then `git worktree prune`. Report `git worktree list` afterwards — it must be ONE line.

Commit C2 ALONE: `test(paydown0814): pin the README tier table to the ledger`
Push.

── C3 — plan, handoff, PR ──

Replace `.agent/plan.md` entirely with the text between the PLAN markers, byte for byte:

>>> PLAN >>>
# Plan — paydown0814 closure debt

Branch: feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the
F045 closure PR #197 merged at this session's Open PR Gate. Next free finding
id: R-0362. Findings R-0359, R-0360 and R-0361 are registered; R-0359 and
R-0360 are FIXED on disk and awaiting the reviewer's authored resolution.

## Goal
Pay down the debt the F045 closure carried out on disk, so the next feature
starts on a green `main`: trim `docs/agents/reviewer_conventions.md` under its
800-token prompt-segment cap (R-0359), pin the README tier table's Done column
to the ledger (R-0360), and record the gate round's own finding (R-0361). A
paydown branch in the established shape of feature/paydown-0730, -0731, -0731b
and -0801 — it claims no STATUS line and closes no `[ ]`.

## Current Step
R2 complete: both fixes committed, gated and pushed, the new pin red-proved in
a disposable worktree, and the PR opened. The PR is NOT merged this session
(docs/agents/self_drive_protocol.md G1); it merges at the next session's Open
PR Gate, which is the operator's manual-review window.

## Next Steps
1. The reviewer re-runs every gate, authors the `Done:` resolutions for R-0359
   and R-0360, and issues the round verdict. R-0361 stays OPEN as a recorded
   reviewer-process finding whose counter-measure is already in force.
2. Next roadmap feature per Rule A5 and STATUS order: F057 — Rate-limit-aware
   scheduler. New session, new branch, after this PR merges.

## Risks
- `main` stays RED until this PR merges. The five
  tests/orchestration/test_role_conventions.py ids are green ON THIS BRANCH,
  which is the fix's proof, but `main` itself only turns green at the merge.
- The conventions trim is a content decision: every rule survives, and the
  Discoverability section now POINTS at AGENTS.md instead of restating it.
  Reversing that choice means restoring the prose and re-breaking the cap.
<<< PLAN <<<

Then rewrite `.agent/handoff.md` per AGENTS.md (rewrite not append; under 60 lines, or carry a "Deviations, declared" line naming the actual count and the mandated content that caused it; feature+round, branch, commit SHAs, per-commit changed-files table, REAL verification results, open-findings count, next expected action). Include the red-proof result and the worktree cleanup proof.

Commit C3: `chore(paydown0814): handback R2`. Push.

Then create the PR (do NOT merge it):
`gh pr create --base main --head feature/paydown0814-closure-debt --title "paydown0814 — pay down the F045 closure debt: conventions token cap, README tier pin" --body-file <a file you write under .remedy-wt/>`
The body must carry: what changed and why, the two findings fixed with their ids, key decisions (headroom over a minimal trim; Discoverability now points at AGENTS.md rather than restating it; the cap itself deliberately untouched), how to review/test (the exact commands), the changed-files table, the red-proof result, and the open-findings count. Report the PR number and URL.

Final report — give me, with RAW output and exit codes: every gate 1-9 above, plus
`git log --oneline -n 5`, `git show --numstat` for each of C0/C1/C2/C3, `git status --porcelain` (say "empty" explicitly if empty), `git worktree list`, `git branch --list 'tmp/*'`, `python3 -m pytest tests/cli/test_golden_path.py -q` (the canary, mandatory every handback), and the mechanical open-finding derivation:
`python3 -c "import re;t=open('.agent/live_review.md').read();o=set(re.findall(r'^- (R-\d+) — ',t,re.M));d=set(re.findall(r'^Done: (R-\d+) — ',t,re.M));print('OPEN',sorted(o-d))"`

Do NOT write any `Done:` paragraph into `.agent/live_review.md` — `Done:` is reserved for reviewer-authored text. If a fix has landed but the reviewer has not yet resolved it, you may add a single `Landed: R-XXXX — <one line: what changed, which commit>` line, and nothing else. Do NOT merge the PR. If anything blocks you, say exactly what and stop without improvising.
