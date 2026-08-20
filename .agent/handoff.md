# Handoff — F086 Release capability, R8 (ledger separation repaired; session closed)

Branch: feature/f086-release-capability (continued; no branch created, no PR opened).
Base b769ccd7 · HEAD = the C7 commit · Open findings 160 (162 registered, 2 resolved),
and the paragraph and line-anchored extractions AGREE at HEAD, which is the property
this round existed to restore. The reviewer's own session verdict is appended below
by C7 and is the reviewer's text, not the worker's.

## Range

Review of b769ccd7..HEAD

## Commits

### 7119325c chore(state): save the F086 R8 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r8.md | +381/-0 | C0a, `shutil.copyfile` of `.remedy-wt/f086-r8.md` |

### f9cd229b chore(state): mirror the R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +257/-263 | C0b, whole-file mirror of the COMMITTED C0a blob |

### 9255aff8 chore(state): advance the plan to the F086 R8 round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-9 | C1, PLAN8 slice byte-verbatim, whole file |

### f75536c0 chore(review): register R-0578 and R-0579 in the finding ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2, FINDINGS2 EOF-append |

### 2ea6de4b fix(review): separate the R-0575 to R-0577 finding paragraphs
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +3/-0 | C3, THE REPAIR: three blank lines inserted programmatically |

### b665c5e0 chore(review): mark R-0578 resolved by the R8 separation repair
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C4, RESOLUTION EOF-append |

### 998b02e4 chore(review): record the F086 R7 verdict in the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C5, RECORD6 EOF-append |

### this commit, and the C7 commit that appends to it
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6, this commit; a handoff cannot table its own commit (R-0149) |
| .agent/handoff.md | +56/-0 | C7, the VERDICT slice appended after this commit; both counts are in the round report |

## External actions

- `git push origin feature/f086-release-capability` after C5 → `b769ccd7..998b02e4`; pushed again after C7.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, read-only at the handback. No PR created, none merged, none opened by this round.
- No worktree was added or removed this round; `git worktree list` stayed at one line throughout.

## Verification

G1 `git status --porcelain` empty; `git worktree list` 1 line; `.agent/STOP` absent (re-read from disk before C0a and again at the handback); branch feature/f086-release-capability.
G2 `.remedy-wt/f086-r8.md` == committed `.agent/authored/f086-r8.md` == committed `.agent/last_block.md`, all three byte-equal; sha256 4b90e4a1aef0ffe5066bfbb046a6f67422ceef9532545bddbd98f80c71b7d91d, 29943 B, 381 lines.
G3 `.agent/plan.md` at HEAD byte-equal to the PLAN8 slice of the COMMITTED block: True; sha256 7a9fa4dfbae21ea51142ffe7cfd9309c245c9f0292382a0430ed92b188ec32e6, 42 lines, under 50; contains `## Goal`, `## Next Steps` and `F086`.
G4 All three appends are byte-exact prefix-plus-remainder. b769ccd7 → post-C2 prefix True, remainder == FINDINGS2, sha256 ff12be01ad3bd7f0b0040572227979a668fd8dd7c4717732159067b965ca5b3d. C3 → C4 prefix True, remainder == RESOLUTION, sha256 44a7345bb082dd6b03733c925a4cabc77e474f43a64f3f217d89b8a41aed9d64. C4 → C5 prefix True, remainder == RECORD6, sha256 cb1fab009fdb80c4f70f177fe9b9153662854234ef4f9d74e83ab82f2f715c46.
G5 PASS, and the two readings AGREE at HEAD. At b769ccd7 — PARAGRAPH 157 registered / 1 resolved / 0 duplicates / 0 unregistered resolutions / 0 anchored `Landed:` / 156 open; LINE-ANCHORED 160 / 1 / 0 / 0 / 0 / 159. They disagree, and that disagreement is the control finding R-0578 records. At HEAD — PARAGRAPH 162 / 2 / 0 / 0 / 0 / 160 and LINE-ANCHORED 162 / 2 / 0 / 0 / 0 / 160, and the two id SETS are equal. Ids added over b769ccd7's LINE-ANCHORED set: PARAGRAPH `['R-0578','R-0579']`, LINE-ANCHORED `['R-0578','R-0579']` — the sets themselves, not only their sizes.
G6 The repair changed separation and nothing else. Measured ACROSS C3 (f75536c0..2ea6de4b, the commit that performs it): (a) the multiset of `^- R-\d+ — ` lines is IDENTICAL at 162 lines each side, symmetric difference EMPTY; (b) the file with all blank lines removed is byte-identical, sha256 ea17fd8087104c217130f09fe6fa501cd6db48ea1c4553d0c457b82b05a083b4 both sides: True; (c) bytes 302150 → 302153, delta exactly 3; (d) at 2ea6de4b `- R-0575 — `, `- R-0576 — ` and `- R-0577 — ` are each preceded by exactly one blank line, and finding lines NOT preceded by a blank line number 0 across the whole file, against 3 at b769ccd7 — the reviewer's control value, reproduced, so this check can fail. Clauses (a), (b) and (c) taken over the LITERAL b769ccd7..2ea6de4b range the gate names are RED and were not repaired: C2 lies inside that range and appends two finding lines, so (a) reports symmetric difference 2 — exactly `- R-0578 — ` and `- R-0579 — ` — (b) reports False, and (c) reports delta 2575. Both readings are recorded; no numstat shape was asserted for C3.
G7 `Done: R-0578 — ` occurs exactly 1x at HEAD. R-0578 is registered under BOTH extractions: True and True. Resolutions naming an unregistered id: none.
G8 `.agent/live_review.md` contains `Steps`: True. Lines beginning `<<<SLICE ` or `<<<END `: 0. Counted as marker LINES, not as `<<<` substrings.
G9 `.agent/handoff.md` as committed by C6 is a byte-exact PREFIX of the file at HEAD, and the remainder is exactly the VERDICT slice — the values are in the round report, because a handoff cannot measure the append that follows it. The seven mandated headings of docs/agents/handback_template.md are present, in order, and no line of this file begins `<<<SLICE ` or `<<<END `.
G10 CARRY INTACT. In the `76661dc1` blob: 184 finding paragraphs, 32 `^Done: R-\d+ — ` resolutions, 152 unresolved. The carried set — ids in the HEAD ledger AND in that blob — is 152 and equals that unresolved set. Fixed ONCE and compared against both blobs: vs `76661dc1` compared 152, equal 152; NEGATIVE CONTROL vs `25f7a5af`, read-only and no checkout, compared 152, equal 113 — strictly fewer, so the check can fail.
G11 `git diff --name-only b769ccd7..HEAD` measured at 998b02e4, before this commit exists: `.agent/authored/f086-r8.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. C6 adds `.agent/handoff.md` as the fifth, which C7 then only appends to; the post-C6 reading is in the round report, because a handoff cannot measure the range that contains it. `pyproject.toml` and every path under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` are ABSENT; `git ls-tree b769ccd7` shows all five of those directories and `pyproject.toml` exist there, so the clause forbids something real.
G12 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, `160 passed in 19.89s`, run in the PRIMARY checkout, never in a worktree.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.19s`. Run only after G12 had ended; the two never overlapped.
G14 Insertions, the `+` column of `git show --numstat` — 7119325c 381, f9cd229b 257, 9255aff8 8, f75536c0 4, 2ea6de4b 3, b665c5e0 2, 998b02e4 2. None exceeds 500 and no DECISION F104 D1 exemption is invoked. C6's own count, and C7's, are in the round report.
G15 One parent per commit: b769ccd7 ← 7119325c ← f9cd229b ← 9255aff8 ← f75536c0 ← 2ea6de4b ← b665c5e0 ← 998b02e4, linear. `git reflog` over this round shows only `commit:` entries, one per commit above, plus the two this handback adds — no amend, rebase, reset or force-push.
G16 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, read-only at the handback. Nothing merged whatever it said.

## Authored-text proofs

PLAN8, FINDINGS2, RESOLUTION, RECORD6 and VERDICT were extracted programmatically by their one-line `<<<SLICE …>>>` / `<<<END …>>>` markers from the COMMITTED `.agent/authored/f086-r8.md` and applied byte-verbatim; PLAN8 is re-verified byte-equal at HEAD under G3, the three ledger appends under G4, and VERDICT under G9. No marker line reached any target file: `.agent/plan.md`, `.agent/live_review.md` and `.agent/handoff.md` each contain 0 lines beginning `<<<SLICE ` or `<<<END ` at HEAD. The four EOF-appends were pure concatenation, each slice carrying its own leading blank line — nothing prepended, nothing stripped. C3 is not a slice and was applied as a programmatic read-insert-write, never by retyping a finding.

## Deviations & assumptions

1. NO DEPARTURE from the block's ordered commit sequence. C0a, C0b, C1, C2, C3, C4, C5, C6 and C7 were made in that order, one commit each, none dropped, none added, none reordered.
2. SIZE, declared under AGENTS.md DECISION D15: this file stands at 151 lines after C7, over the 100-line cap a >5-commit bundle allows, and over the template's 800-token thrift cap. Cause: this round carries the reviewer's authored session verdict, 56 lines of mandated content for the round that closes a session, on top of nine per-commit attributions and a sixteen-gate Verification section one of whose gates carries two readings because one of them is red. No section is dropped to meet the cap, nothing is trimmed after C7, and no trim commit follows.
3. G6 clauses (a), (b) and (c) are RED under the literal range the gate names, b769ccd7..2ea6de4b, because C2 sits inside that range and appends two findings; they are GREEN across C3 itself, f75536c0..2ea6de4b, which is the commit the gate describes. Both readings are recorded under G6 and nothing was edited to reconcile them.
4. Helper scripts were written under the gitignored `.remedy-wt/r8/` (`extract.py`, `c3_repair.py`, `gates.py`, `suites.py`, this draft) because this session's Bash guard rejects shell loops, `$( )` and env-prefix forms. `git status --porcelain` stayed empty throughout.
5. The worker wrote NO verdict anywhere. The `Reviewer's session verdict` section below is the VERDICT slice, applied byte-verbatim by C7, neither summarised nor reformatted.

## Next

Next session, in this order: (1) re-read `.agent/STOP` from disk, Phase 1 rule 1; (2) run the Open PR Gate, Phase 1 rule 2.

## Reviewer's session verdict — authored by the reviewer, applied by the worker

This section exists because finding R-0571, registered by this feature, is that a
verdict issued and never written to disk cannot be told apart from one never
issued. It is appended rather than written into the sections above so that the
next handback rewrite cannot silently destroy it.

Session of 2026-08-20, self-drive per docs/agents/self_drive_protocol.md, and the
SECOND session on this branch. The reviewer wrote nothing in the work tree; one
delegated worker per round made every commit; every verdict below rests on gates
the reviewer re-executed itself over the committed diff, never on a handback's
summary.

| Round | Range | Verdict |
|---|---|---|
| R5 | 655661b0..91459dc1 | PASS |
| R6 | 91459dc1..72e07381 | PASS |
| R7 | 72e07381..b769ccd7 | FAIL — R-0578 |

R5 was inherited unreviewed from the previous session, which ended immediately
after issuing its own verdict; reviewing it first was Phase 1 rule 4 and it
passed on every gate. R6 was ordered to choose the wheel carry mechanism by
measurement and could not: its red control was sited under `.remedy-wt/`, and
hatchling drops every VCS exclusion when the build root is itself gitignore-matched,
so the control read 3 where 0 was required. The worker obeyed the block's own halt
clause, left `pyproject.toml` untouched, found the cause in hatchling's source and
proved it — the right outcome from a broken order, and the defect is registered as
R-0574 against the reviewer. R7 then landed the carry for real, with the probe tree
moved OUTSIDE the repository: `artifacts = ["apps/ui/dist/**"]` is in
`pyproject.toml` at `b769ccd7`, a wheel built at that commit carries
`apps/ui/dist/index.html` and both asset bundles, and the control that must read 0
does read 0. R7 failed only on the layout of the reviewer's own findings slice,
which R8 repaired.

Every finding this session registered — R-0574 through R-0579 — is a defect in
the reviewer's own gates rather than in any worker's execution. That is the honest
summary of the session: the workers were not the weak link, and every round that
went wrong went wrong in the order, not in the obedience.

DECISION F086 D3 was ruled and is the session's other durable output. It withdraws
D1 part (c) — the dual-mode asset resolver — because the premise was false, and
measured false from an extracted wheel, from an independent wheel-root-shaped copy
and from the checkout: `_get_frontend_dist()`'s three `.parent` hops
land on the wheel ROOT, where `apps/` is a sibling of `packages/` exactly as in a
checkout, so the single existing expression already resolves in both modes. The
test per mode is KEPT. D1 part (b), the packaging-time guard, is still owed and no
release may be cut before it exists: with the carry applied and no `dist/` present
a build still exits 0 and ships a wheel with zero UI files.

The open set stands at 160 once this round's own C2 and C4 have landed, which is
what G5 requires and measures at HEAD, and the next free id is R-0580. By
docs/agents/planner_reviewer_prompt.md §4 item 13 the LAST round of a branch has no
on-disk gate entry, so R8's own verdict is the terminator and lives in the
reviewer's closing report rather than here. That absence is the rule, not an
omission — and it is precisely the hole R-0571 exists to close.
