You are the worker (Window 2). Round id: paydown0730-r1. Read AGENTS.md
first; it wins on any conflict. Operator standing approval exists for a
same-session merge of this round's PR — but ONLY the reviewer's PASS
triggers it; you never merge this round's PR yourself. Save THIS ENTIRE
block verbatim to .agent/last_block.md before doing anything else, with a
final line "OUTCOME: pending"; flip it to "OUTCOME: executed" at handback.

STEP 0 — OPEN PR GATE (F051 closure PR)
Run: gh pr list --state open --json number,headRefName,baseRefName,isDraft
Expected: exactly one PR — #165, feature/f051-escalate-instead-of-block
-> main, not draft. Anything else -> STOP, hand back.
Then:
  gh pr merge 165 --merge --delete-branch
  git checkout main && git pull --ff-only
  git branch -D feature/f051-escalate-instead-of-block
Record the merge commit sha in the handback.

STEP 1 — BRANCH
git checkout -b feature/paydown-0730

STEP 2 — RECEIVE AUTHORED TEXTS (fidelity protocol)
Eight authored texts follow at the end of this block. Save each BODY (the
bytes between its BEGIN and END marker lines, exclusive; every file ends
with a trailing newline) verbatim to .agent/authored/<name>.md and verify
sha256sum equals the hash in the BEGIN marker BEFORE any use. Long lines
may arrive hard-wrapped by the relay: rejoin wrapped fragments with a
single space and re-hash (known recoverable fault). A hash that still
mismatches = STOP and hand back; never apply unverified bytes.

STEP 3 — COMMIT A (findings persist FIRST)
Copy paydown0730-r1-1.md over .agent/live_review.md and
paydown0730-r1-2.md over .agent/plan.md (byte-identical; prove with
cmp -> 0 in the handback). Commit .agent/live_review.md, .agent/plan.md,
.agent/authored/paydown0730-r1-*.md and .agent/last_block.md as:
chore(paydown0730): persist round state + authored texts

STEP 4 — COMMIT B (Item 1 — docs/agents/planner_reviewer_prompt.md)
In §2, the paste-block-format paragraph ends with the sentence ending
"broke an authored hash unrecoverably)." Insert the BODY of
paydown0730-r1-3.md as its OWN paragraph directly after that paragraph
(one blank line before and after), i.e. before the paragraph that starts
"**(4) Feature-done banner**". Commit:
docs(agents): hash-stamp-everything transport rule (operator ruling 2026-07-30)

STEP 5 — COMMIT C (Items 2+5 — docs/roadmap/STATUS_closure_protocol.md)
(a) Insert the BODY of paydown0730-r1-4.md as a new section between the
end of "## Algorithm" (after item 7, "End Window 1 ...") and the
"## Canonical zip build sequence" heading (one blank line before/after).
(b) In Algorithm step 1, the pitfall passage ends with the line ending
"missing values surface only at zip time." Insert the BODY of
paydown0730-r1-5.md directly after that line (the 3-space list
indentation is already inside the payload). Commit both edits as:
docs(roadmap): closure-candidate ledger rule + F051 producer pitfalls
Record nothing else in this commit.

STEP 6 — COMMIT D (Item 3 — tests/docs/test_docs_consistency.py)
Pre-proof: python3 -m pytest tests/docs/ -q -> record raw tail + exit
code (expect 292 passed, exit 0 — the count gap is invisible without the
pin; that IS the finding).
In class TestPrimaryDocsAreHonest, insert the BODY of
paydown0730-r1-6.md as a new method directly after the end of
test_the_readme_reports_the_accepted_foundation_and_no_later_feature
(after its closing "# ... checked by name." comment lines), separated by
one blank line from both neighbors. No README/STATUS edit is needed —
the counts agree at 27, so the pin lands green (R-0151 satisfied).
Post-proof: python3 -m pytest tests/docs/ -q -> expect 293 passed,
exit 0.
Negative control (red proof, throwaway only): git worktree add
/tmp/paydown-negctl HEAD; in the WORKTREE edit README.md "27 of 252" ->
"28 of 252"; run only the new test there — it MUST fail; record the raw
assertion line; then git worktree remove --force /tmp/paydown-negctl and
git worktree prune (git worktree list as proof). Never touch the primary
checkout for this. Commit (test file only):
test(docs): pin README accepted-count to STATUS [x] count (R-0156)
Record this commit's short sha as SHA_R0156.

STEP 7 — COMMIT E (Item 4 — docs/agents/integration_gate.md)
Step 3 ("Compare.") ends with the line ending "failures the branch
fixed." Insert the BODY of paydown0730-r1-7.md directly after that line,
as continuation lines of list item 3 (indentation already in the
payload). Commit:
docs(agents): integration gate — environment-coupled base-failure rule (R-0155)
Record this commit's short sha as SHA_R0155.

STEP 8 — COMMIT F (ledger resolutions)
Substitute <SHA_R0155> and <SHA_R0156> in a COPY of paydown0730-r1-8.md
(each placeholder occurs exactly once; grep -c proof: 1 before, 0 after,
per placeholder; the original authored file stays untouched). Then in
.agent/live_review.md replace the ENTIRE "- Open: R-0155 ..." bullet
(all of its lines) with the first bullet of the substituted copy, and
the ENTIRE "- Open: R-0156 ..." bullet with the second. cmp the applied
region against the substituted copy. Commit:
chore(paydown0730): resolve R-0155 + R-0156 in the ledger

STEP 9 — GATES (clean tree, all content committed)
python3 -m pytest tests/docs/ -q                    -> expect 293, exit 0
python3 -m pytest tests/cli/test_golden_path.py -q  -> expect 42, exit 0
Raw tails + exit codes into the handback. Any red: STOP after recording
the raw output; no further commits except the handback itself.

STEP 10 — PUSH + PR (no merge)
git push -u origin feature/paydown-0730
gh pr create --base main --title "chore: paydown micro-round 2026-07-30
(R-0155/R-0156 fixes + transport/ledger rules)" with an AGENTS.md-
conforming body (what/why, per-commit table, gate outputs, verdict
PENDING, open-findings count 0 after this round, next free ID R-0158).
DO NOT merge — the merge happens only on the reviewer's PASS.

STEP 11 — HANDBACK
Rewrite .agent/handoff.md per docs/agents/handback_template.md: range
main..HEAD, per-commit changed-files tables, verbatim sha256sum output
of all eight .agent/authored/paydown0730-r1-*.md files, cmp proofs, both
gate transcripts, the negative-control red proof, the #165 merge sha,
PR number, deviations (honest, including "none"). Flip OUTCOME in
.agent/last_block.md to "executed". Commit:
chore(paydown0730): handback R1
Push. Done — await the reviewer.

--- BEGIN paydown0730-r1-1 sha256=269bab2c143ee8a98bc471b5de3c470eee0a67e82bec44ef137b606890d4a59b ---
# Live Review — Paydown micro-round 2026-07-30 (F051→F052 boundary)

Branch: feature/paydown-0730
Scope: docs/process paydown — codify the sha256-everything transport
rule (planner_reviewer_prompt.md) and the closure-candidate ledger
rule (STATUS_closure_protocol.md); add the F051 producer pitfalls;
fix R-0155 (integration-gate baseline gap) and R-0156 (README
accepted-count pin). Same-session merge on PASS (standing operator
approval, 2026-07-30).

## Steps
- R1: Open PR Gate (#165) → Items 1–5 → gates (tests/docs + canary)
  → handback.

## Findings
- Open: R-0155 (process, Low, carried from F051; REFINED
  2026-07-30): the integration-gate base worktree lacks the ROOT
  node_modules and apps/ui/dist, so ~20 environment-coupled ids
  (vitest/tsc/ui-server classes) land in comm -23 on every gate run
  and could mask a genuine base failure in those files. Fix: this
  round's integration_gate.md amendment (Item 4).
- Open: R-0156 (process, Medium, carried from F051): the
  README/STATUS accepted-count cross-check is unenforced in
  tests/docs (negative control: a faked count still passed all 292).
  Fix: this round's count-pin test (Item 3; same-commit rule
  R-0151).
- Next free ID: R-0158.

## Verdicts
- R1: PENDING (reviewer).
--- END paydown0730-r1-1 ---

--- BEGIN paydown0730-r1-2 sha256=59f9de7b5ecbeed94f84f529854890ec5df1de326937b41ce24f5a93e7f641a4 ---
# Plan — Paydown micro-round 2026-07-30

## Goal
One reviewer-gated docs/process paydown round at the F051→F052
boundary: codify the sha256-everything transport rule and the
closure-candidate ledger rule, add the F051 producer pitfalls, fix
R-0155 (integration-gate baseline gap) and R-0156 (README
accepted-count pin). Same-session merge on PASS (standing operator
approval, 2026-07-30).

## Next Steps
- R1 handback → reviewer verdict → merge on PASS.
- Then Rule A5: F052 — Self-healing test rounds (fresh window).
--- END paydown0730-r1-2 ---

--- BEGIN paydown0730-r1-3 sha256=0dd842d6c45a0ee7e231c058c9f84f33023d0ecf61956445917b669745e9aa8f ---
**Hash-stamp everything (operator ruling 2026-07-30, F050 truncation
lesson):** EVERY string the worker applies to a file — however
short, including single-line FROM→TO replacement pairs and README
edit snippets — travels inside a sha256-stamped authored block and
is hash-verified before use. Bare procedure text may describe
actions but never carries appliable content; transport truncates
silently (the F050 closure block lost a bare README FROM-string in
transit and the edit had to be reconstructed). Until now this rule
lived only in reviewer session memory — exactly the A1 trap (§0)
this rule class keeps falling into; from here the disk carries it.
--- END paydown0730-r1-3 ---

--- BEGIN paydown0730-r1-4 sha256=bc1972aec19b5325fad8ceee0a9faeeb2e0cdaff29d465f9f525db1e8b933a78 ---
## Closure-candidate findings

Operator ruling 2026-07-30 (F050→amend0730 precedent): findings
raised DURING a closure review are recorded in the closure brief as
CANDIDATES only — no R-id is spent, nothing is registered in the
already-final live_review. The NEXT session's first reviewed round
then either registers each candidate (spending the next free ID) or
resolves it inline as a DECISION per planner_reviewer_prompt.md §4
item 7. This keeps the ledger monotonic across the session boundary
and keeps the operator-facing narrative in agreement with the disk.
--- END paydown0730-r1-4 ---

--- BEGIN paydown0730-r1-5 sha256=d81c78d0dc1d6f59901e21b7673f58fafa745429ce09c688bd174f314cd99920 ---
   Two more, from the F051 BLOCKED_EVIDENCE attempt (both caught by
   the packaging validator — catch them at authoring time instead):
   (a) verification records must carry non-empty test node ids with
   `len(node_ids) == selected` (run `--collect-only` for real ids);
   (b) `test_files` entries are files, never directories (expand
   `tests/docs/` to the actual file paths).
--- END paydown0730-r1-5 ---

--- BEGIN paydown0730-r1-6 sha256=253f733da566ca890633091efb838d49b54028780e671ce981caa0cea236ab50 ---
    def test_the_readme_accepted_count_equals_the_status_count(self):
        """R-0156: pin the README accepted-COUNT to the STATUS ledger.

        The id cross-check above verifies every README-listed feature
        IS accepted, but the prose line "N of 252 registered items
        accepted" could carry any N (negative control: a faked count
        stayed green through all of tests/docs). Parse both counts
        and pin them equal.
        """
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        m = re.search(r"^(\d+) of (\d+) registered items accepted\.",
                      readme, re.MULTILINE)
        assert m, "README must state 'N of M registered items accepted.'"
        assert int(m.group(2)) == TOTAL_FEATURES
        accepted = len(re.findall(r"^- \[x\] F\d{3} — ", status,
                                  re.MULTILINE))
        assert int(m.group(1)) == accepted, (
            f"README claims {m.group(1)} accepted; STATUS.md has "
            f"{accepted}")
--- END paydown0730-r1-6 ---

--- BEGIN paydown0730-r1-7 sha256=2b4612f6b425e69b416242c2d5d18dec607834a8768ad34911fe0082499de1ef ---
   Environment-coupled base failures (R-0155 amendment, operator
   approved 2026-07-30): the throwaway base worktree lacks build
   outputs the suite needs (the ROOT `node_modules`, `apps/ui/dist`),
   so environment-coupled ids (vitest/tsc/ui-server classes) fail at
   base and land in `comm -23` on every gate run — where a GENUINE
   base failure in those same files would be masked. Therefore:
   either restore parity before the base run (share or copy the
   primary checkout's root `node_modules` and `apps/ui/dist` into
   the base worktree, or run the same install/build there), or
   attribute EVERY `comm -23` id to the environment class by direct
   evidence (the missing artifact named per id). An unattributed
   `comm -23` id counts as a genuine base failure and blocks the
   gate verdict.
--- END paydown0730-r1-7 ---

--- BEGIN paydown0730-r1-8 sha256=3afe410d4f93339ee4ff1662b58e306e8a02ace87e98834c88947ebaadbddc95 ---
- Resolved: R-0155 (process, Low) 2026-07-30: integration_gate.md
  now requires base-environment parity (root node_modules +
  apps/ui/dist) or per-id direct-evidence attribution; an
  unattributed comm -23 id counts as a genuine base failure and
  blocks the gate verdict.
  Done: R-0155 (commit <SHA_R0155> — the doc diff is the evidence).
- Resolved: R-0156 (process, Medium) 2026-07-30: tests/docs now pins
  the README accepted-count against the STATUS [x] count; the pin
  landed green (counts agree at 27) with a red negative control
  proving it bites.
  Done: R-0156 (commit <SHA_R0156> — test + red-proof transcript).
--- END paydown0730-r1-8 ---

OUTCOME: pending
