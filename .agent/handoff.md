# Handback — F009 R34 (closure round two, the last round of this branch)

Round base: `06aeb7494ff47dae77764303dbbb3d4aace48158`

Fortschritt: ~100 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidenz-Bundle und Review-Zip gebaut
             und verifiziert; diese Runde schreibt die STATUS-Zeile, den
             README-Sync und den Pull Request) — Schätzung

## Range

Review of `06aeb749`..C3, the closure commit this file is written inside; C3's
own SHA cannot exist when its content is written, so it is named by role here
and its value is in the round report (R-0371).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   |        |
| C0b  | done   |        |
| C1   | done   |        |
| C2   | done   |        |
| C3   | done   |        |

## Commits

### 744b7c97 docs(state): save the F009 R34 closure block as authored text (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f009-r34.md | 327/0 | the received R34 block, byte for byte |

### ac0f0bcc docs(state): mirror the F009 R34 block into last_block (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 241/376 | mirrored from the committed C0a blob |

### 7a54eb1a docs(state): point the F009 plan at closure round two (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 13/14 | PLANF009R34 in full |

### 6413f223 docs(review): record the R33 verdict as PASS (C2)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 2/0 | LEDGER34 appended on the round base |

### C3 (SHA in the round report) docs(roadmap): close F009 with the STATUS line, the README sync and the closure candidate
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | 1/1 | the authored `[x] F009` ledger line |
| README.md | 5/2 | capability sync, same commit as STATUS (R-0154) |
| .agent/candidates.md | 27/5 | CANDIDATES34: one candidate, no id spent |
| .agent/handoff.md | 150/61 | this file; a handoff cannot table the commit that writes it (R-0149), so this cell was measured on the staged content |

## External actions

Ordered after C3 and reported with their real values in the round report,
because none of them can exist while C3's content is written (R-0371):
`git push` of `feature/f009-single-write-channel`, then `gh pr create` and
`gh pr list --state open`. NO `gh pr merge` is run in this session. No worktree
was added or removed this round; every off-HEAD read used `git show` (G5, R-0594).

## Verification

Every gate below was executed with its real exit code; the transcripts are in
the round report (R-0582). One line per gate:

- G1 `.agent/STOP` ABSENT before C0a and before C3; branch
  `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after
  each of C0a, C0b, C1, C2; after C3 in the round report (self-reference).
- G2 TRANSPORT: `.agent/authored/f009-r34.md` at C0a, `.agent/last_block.md` at
  C0b and the received bytes are all sha256
  `cc6873fa1a5a3e1215b8f479bf7c08b1787ca7cc2100e4737ef53a7b7b6f1bfc`, 26081
  bytes, 327 lines. C0b was written from the committed C0a blob.
- G3 SLICES: the extractor over the committed C0a blob printed 11 slices over 87
  CONTENT lines; re-measured from that same blob, TOTAL 327 lines against
  DECISION F085 D6's 490 and PROSE (TOTAL minus slice-CONTENT lines) 240 against
  D5's 400 — both agree with constraint 10.
- G4 `.agent/plan.md` at C1 `cmp` exit 0 against PLANF009R34, both sha256
  `4d7fc193f3102b9602e0b171fdd03afaaf4679219bec54499e4a3078b919eb1b`, negative
  control exit 1; `wc -l` 36 against the 50-line cap; `^## Goal$` 1 and
  `^## Next Steps$` 1. `.agent/candidates.md` at C3 `cmp` exit 0 against
  CANDIDATES34, both sha256
  `3ce7d0550c4f12e9de830df8811243bedfac67dd2574ca04ce4ecd1fd8bb9e80`, negative
  control exit 1; line-anchored a leading `- ` 0 at the round base and 1 at C3,
  `^EMPTY\.` 1 at the base and 0 at C3, `^NON-EMPTY\.` 0 at the base and 1 at
  C3 — six anchored numbers, because the unanchored substring discriminates
  nothing (R-0646).
- G5 THE APPEND at C2 under two independent readers: (a) the round-base blob is
  a byte-exact PREFIX and the 5463-byte remainder is exactly one newline plus
  LEDGER34, sha256
  `1be2426d44fbdc30e18311e1b6d8104f297850977496bd05b56828de8dcc8ce7`, 5462
  bytes, 1 line; (b) N counted by the script as 1 and the last blank-line
  separated unit equals the slice's paragraph. 589646 to 595109 bytes, 1146 to
  1148 lines. NEGATIVE CONTROL: one printable byte of the FIRST appended
  paragraph replaced at equal length is REJECTED by both readers while both
  ACCEPT the true file (R-0631).
- G6 THE FOUR PAIRS at C3, FROM occurrences measured BEFORE each replacement and
  each applied with count=1: STATUS 1, READMEA 1, READMEB 1, READMEC 1. AFTER
  C3, the three REWRITES read FROM 0x and TO 1x in their target; the APPEND
  READMEC reads FROM exactly 1x and each of its TO-only lines exactly 1x among
  the lines C3's diff ADDS to `README.md` — never a whole-file count (§4.9,
  R-0253). `git show --numstat` at C3: `README.md` 5/2,
  `docs/roadmap/STATUS.md` 1/1. Readings in the round report.
- G7 line-anchored over `.agent/live_review.md`, round base then C2: `- R-`
  entries 213 all DISTINCT then 213 all DISTINCT; `Done: R-` 3 then 3;
  `Landed: ` 0 then 0; `Gate: R` keys 33 over 33 DISTINCT then 34 over 34
  DISTINCT; `Gate: R34` 0 then 1 (R-0494).
- G8 max REGISTERED id `R-0647` at the round base and `R-0647` at C2; open by
  DECISION F009 D10's rule — line-anchored `- R-` entries minus line-anchored
  `Done: R-` lines — 210 at the round base and 210 at C2. Nothing was minted:
  the next free id is R-0648.
- G9 THE STATUS LEDGER, line-anchored, round base then C3: `^- \[x\] ` 54 then
  55; `^- \[~\] ` 1 then 0; `^- \[x\] F009 — ` 0 then 1; `^- \[~\] F009 — ` 1
  then 0. The C3 F009 line carries the literal evidence job `f009-closure`, the
  package `remedy-review-20260822-085607-READY_FOR_REVIEW.zip`, the SHA-256
  `ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f` and the
  accepted HEAD `97d028980b5781cbf22a0f651f7e879eea1a0485`; the package on disk
  is 72237000 bytes, recomputes to that same SHA-256, and the `head_commit`
  read OUT OF its in-zip `.review_zip_manifest.json` is that same accepted HEAD
  at `package_status` READY_FOR_REVIEW.
- G10 DOCS GATE `python3 -m pytest tests/docs/ -q -rf` in the primary checkout,
  serially: exit 0, 295 passed.
- G11 CANARY `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the
  primary checkout, run after the docs gate had finished: exit 0, 42 passed.
- G12 RANGE, executed after C3 because it reads C3: the seven declared paths
  with the set difference empty both ways, 0 paths under `packages/`, `apps/`
  or `tests/`, single-parent commits, `git show --numstat` and
  `git diff --numstat` agreeing cell by cell with the table above, every
  insertion under the 500 cap, leading `<<<SLICE ` and `<<<END ` 0 LINES in all
  five slice targets, `git ls-files .remedy-wt` 0, and this round's reflog rows
  classified with `amend`, `rebase` and `cherry` each 0. Readings in the round
  report (R-0371).
- G13 THE PULL REQUEST, created after C3 is pushed and NEVER merged; its number
  and URL are in the round report because they cannot exist here (R-0371).
- G14 this file: every mandated section of docs/agents/handback_template.md, an
  item-status row for each of C0a, C0b, C1, C2 and C3, the round base SHA, one
  line per gate, and the block's `Fortschritt:` line verbatim across all four of
  its lines; its own `wc -l` is in the deviations line below.

## Authored-text proofs

Every applied text was extracted programmatically from the COMMITTED C0a blob
`.agent/authored/f009-r34.md` at `744b7c97` by its `<<<SLICE `/`<<<END ` marker
lines and applied byte for byte — nothing was retyped or reflowed. Disk to disk:
PLANF009R34 equals `.agent/plan.md` at C1 and CANDIDATES34 equals
`.agent/candidates.md` at C3, both `cmp` exit 0 with a negative control at exit
1 (G4); LEDGER34 is the exact appended remainder at C2 under two readers (G5);
the four FROM/TO pairs each matched exactly once before replacement and were
applied with count=1 (G6). 11 of 11 slices applied; none deviated.

## Deviations & assumptions

Deviations, declared (DECISION D15): this file is 177 lines against the 60-line
cap a five-commit round allows. The overage is mandated content, not prose
padding — five per-commit changed-files tables, an item-status table, fourteen
gate lines several of which carry a reading at TWO points (R-0494), and the
closure values G9 requires as literal substrings. No section is dropped.

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3 were
committed in that order, five commits, no extra and none dropped. THIS ROUND
MINTS NO FINDING ID AND RESOLVES NOTHING (constraint 3): no `- R-` entry, no
`Done:` line and no `Landed:` line was written, and the one defect found during
the closure review is recorded in `.agent/candidates.md` as an un-idded
CANDIDATE, per the closure protocol. Assumption: none beyond the block.

## Next

F009 is CLOSED. `docs/roadmap/STATUS.md` carries the `[x] F009` line, README
agrees with it in the same commit, and C3 is the LAST commit on this branch
(AGENTS.md Rule A4). The pull request is OPEN and UNMERGED by design — the gap
is the operator's manual-review window. The single expected next action: the
NEXT session's Open PR Gate merges that pull request before any new feature is
claimed, and that session's first reviewed round must register or resolve the
candidate now sitting in `.agent/candidates.md`, which is non-empty and is
therefore itself a block condition at feature-claim time.
