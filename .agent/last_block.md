OUTCOME: executed
── STEP amend0730-R1/1 — docs amendment micro-round ─────────────────────
Goal:        Merge PR #163 (Open PR Gate), then apply the operator's
             2026-07-30 docs amendments (AGENTS.md discoverability
             section, F105 Design addition, closure-protocol step-2
             wording fix) on a fresh branch, gated, as an open PR.
Bundle:      1 Open PR Gate · 2 branch · 3 authored-text save+verify ·
             4 state commit · 5–7 the three docs commits · 8 gate ·
             9 handback commit · 10 push + PR · 11 handback
Change:      ONLY these paths: AGENTS.md,
             docs/roadmap/features/T2_F105.md,
             docs/roadmap/STATUS_closure_protocol.md, .agent/**.
Constraints: Docs only — no code, no tests, no other files. AGENTS.md
             rules win on any conflict. Never edit a test to make the
             gate pass. Your F050-R3 handback is ACCEPTED (D1); your
             R-0156 candidate is registered in the authored live_review;
             the zip-ordering conflict you flagged is resolved by D2
             (item 7 below).
Done when:   All verification commands below green, PR open, PR NOT
             merged.
Handback:    Completion report + rewrite .agent/handoff.md (per-commit
             changed-files tables, all five sha256sum outputs verbatim,
             raw gate output, deviations).

AUTHORED-TEXT PROTOCOL (applies to all five blocks below): the text's
bytes are the lines strictly BETWEEN the BEGIN and END marker lines,
joined with LF, plus one final LF. Save each to
.agent/authored/<name>.md, run sha256sum, and compare against the hash
in the BEGIN marker BEFORE any use. On mismatch: if a long line arrived
hard-wrapped, rejoin with a single space and re-verify (known transport
fault, recoverable); if still mismatched, STOP that item, record the
received bytes and computed hash in the handoff, complete the remaining
items, hand back. Never apply an unverified text.

1. Open PR Gate (AGENTS.md):
   gh pr list --state open --json number,headRefName,baseRefName,isDraft
   Expected: exactly one PR — #163, feature/f050-dag-scheduling -> main,
   not draft. Anything else: STOP, report, hand back.
   gh pr merge 163 --merge --delete-branch
   git checkout main
   git pull --ff-only
   Verify: gh pr list --state open  -> empty.

2. git checkout -b feature/docs-discoverability-amend

3. Save and verify the five authored texts per the protocol above to:
   .agent/authored/amend0730-r1-1.md … amend0730-r1-5.md
   Record all five sha256sum output lines verbatim for the handoff.

4. Commit 1 — state first, own commit:
   - .agent/live_review.md  := full replace with the bytes of
     .agent/authored/amend0730-r1-4.md (verify: cmp, disk-to-disk).
   - .agent/plan.md         := full replace with amend0730-r1-5.md (cmp).
   - .agent/last_block.md   := guard entry: block amend0730-r1 received
     (note any transport faults), OUTCOME pending.
   git add .agent/authored/amend0730-r1-*.md .agent/live_review.md \
     .agent/plan.md .agent/last_block.md
   Commit message: chore(amend0730): persist micro-round state + authored texts

5. Commit 2 — AGENTS.md:
   Insert the exact bytes of .agent/authored/amend0730-r1-1.md, followed
   by ONE empty line, immediately BEFORE the line:
   ## 🧩 Documentation Structure
   (The authored text ends with its own 72-dash separator, so the file's
   section rhythm is preserved.)
   Verify:
   sed -n '/^## 🔎 Code Discoverability Conventions$/,/^-\{72\}$/p' AGENTS.md | sha256sum
   -> must equal e87772f4c4e28fffac2c329620b496096857d686d4caba2d70a21e1e53ba1bad
   git diff --stat -> only AGENTS.md.
   Commit message: docs(agents): add Code Discoverability Conventions (operator ruling 2026-07-30)

6. Commit 3 — F105:
   In docs/roadmap/features/T2_F105.md insert the exact bytes of
   .agent/authored/amend0730-r1-2.md, followed by ONE empty line,
   immediately BEFORE the line:
   ## Task slicing
   Verify:
   sed -n '/^- \*\*Operator addition 2026-07-30/,/including Remedy itself\.$/p' docs/roadmap/features/T2_F105.md | sha256sum
   -> must equal 85bc6b5d6e57a756ac6879ac67b299ade62de821078fdc3e8d2064dd049a76c9
   Commit message: docs(roadmap): F105 — distilled discoverability block for builder/reviewer segments (operator addition 2026-07-30)

7. Commit 4 — closure-protocol wording (D2):
   In docs/roadmap/STATUS_closure_protocol.md, first verify the FROM
   block is byte-identical to what was reviewed:
   sed -n '/^   Build order: the closure zip is the LAST action/,/^   always\.$/p' docs/roadmap/STATUS_closure_protocol.md | sha256sum
   -> must equal 240a60c98303b5e0aed79c8f8f3679cac1c8e8a8a25fe6ec29b499800a43acaf
   (mismatch: STOP this item, report, continue with item 8).
   Then replace exactly those lines (the 5-line block from "   Build
   order: …" through "   always.") with the exact bytes of
   .agent/authored/amend0730-r1-3.md.
   Verify:
   sed -n '/^   Build order (wording aligned/,/^   handback, always\.$/p' docs/roadmap/STATUS_closure_protocol.md | sha256sum
   -> must equal 933265297b8af85a4560028d0b1340b034adb57e23bade37e2f84c5ad5e78d03
   grep -c "LAST action after ALL commits" docs/roadmap/STATUS_closure_protocol.md -> 0
   Commit message: docs(roadmap): closure protocol step 2 — align zip build-order wording with accepted practice (amend0730 D2)

8. Round gate (docs-round tier + canary) — raw output goes in the
   handoff, exit codes included:
   python3 -m pytest tests/docs/ -q                      (expect exit 0)
   python3 -m pytest tests/cli/test_golden_path.py -q    (expect exit 0)
   Any failure: report the raw output and hand back — do not repair.

9. Commit 5 — handback state:
   Rewrite .agent/handoff.md (range, per-commit changed-files tables,
   the five sha256sum lines verbatim, raw gate tails, deviations).
   Set OUTCOME executed in .agent/last_block.md.
   Commit message: chore(amend0730): handback R1

10. git push -u origin feature/docs-discoverability-amend
    gh pr create --base main \
      --title "docs: operator amendments 2026-07-30 (discoverability conventions, F105 segment rule, closure-protocol wording)" \
      --body per AGENTS.md PR workflow: what/why (three operator
      amendments; note Amendment 1 skipped as already codified and
      Amendment 2 had nothing to clean), changed-files table, gate
      results, verdict PENDING (R1), note "reviewer-gated; merges on
      reviewer PASS under standing operator approval (same session)".
    Do NOT merge the PR.

11. Hand back with the completion report.

TRANSPORT NOTES (worker, amend0730-R1):
(1) The five authored texts arrived CLEAN. All five sha256sum outputs
    matched their BEGIN-marker hashes on the first computation, before
    any use — no rejoin needed.
(2) Cosmetic wraps in the block's own instruction text (not in authored
    bytes): the five BEGIN marker lines each had their trailing "-----"
    pushed to the next line; the sed commands in items 6 and 7 and the
    commit-message lines in items 6, 7 and the --title in item 10 were
    hard-wrapped. All are unambiguous and are recorded above rejoined.
    No authored bytes are affected.
