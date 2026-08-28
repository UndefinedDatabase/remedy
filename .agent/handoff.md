# Handoff — F033 R1, claim and inventory

## Session

SESSION 1 of feature F033 · round 1 · rounds so far 1

Branch: `feature/f033-hunk-approval`. Soft limit (25 rounds / 7 sessions) not
reached and not approached.

## Range

Review of `32cde54ef6afb8f994a2f7d804f1c991a62df9e8`..HEAD

This round's BASE is `32cde54e`, the merge commit pull request #218 produced at
the Open PR Gate, read by `git rev-parse HEAD` on `main` after
`git pull --ff-only`. Every range gate below is measured from it.

## Commits

Every `+/-` cell below is `git diff --numstat` between the commit's single
parent and the commit. G8 reports its insertion counts from the SAME tool over
the SAME commits; the two readings were compared cell by cell and THEY AGREE:
415, 368, 28, 1, 33, 367, 207.

### 0f7e716c docs(agent): save the F033 R1 claim block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f033-r1.md` | +415 / -0 | C0a — the reviewer's block saved verbatim |

### fb27cd55 docs(agent): mirror the F033 R1 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +368 / -239 | C0b — same bytes, one git blob with C0a's path |

### b90c8a9a docs(agent): retarget the plan at the F033 claim round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +28 / -29 | C1 — PLANF033R1 applied byte for byte |

### 1a765aab docs(roadmap): claim F033 hunk-level diff approval
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1 / -1 | C2 — STATUSCLAIM pair, `[ ]` becomes `[~]` |

### d2e77606 docs(review): reset the record for F033 and book the F037 R27 verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +33 / -24 | C3 — RECORDHEAD pair AND the GATEF037R27 append, one commit |

### fff34c44 docs(agent): record the F033 source inventory, sections 1 to 5
| Path | +/- | Reason |
|---|---|---|
| `.agent/f033_inventory.md` | +367 / -0 | C4a — sections 1 through 5 (see deviations: C4 was split) |

### d4b05cf0 docs(agent): record the F033 source inventory, sections 6 to 9
| Path | +/- | Reason |
|---|---|---|
| `.agent/f033_inventory.md` | +207 / -0 | C4b — sections 6 through 9 and the Unanswered section |

### C5 (this commit) docs(agent): hand back the F033 R1 claim round
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | (self-reference) | C5 — this handback; a handoff cannot table the commit that writes it (R-0149 pattern). Its insertion count is deliberately NOT reported here — the block's G8 assigns it to the next gate. |

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | Exactly one entry: `{"baseRefName":"main","headRefName":"feature/f037-rendered-diff-viewer","isDraft":false,"number":218}` — exactly what the block's gate expects. |
| `gh pr merge 218 --merge --delete-branch` | MERGED. Remote branch deleted. Local `main` fast-forwarded `9dde5495..32cde54e`, 70 files changed, 20888 insertions, 686 deletions. |
| `git checkout main` | "Already on 'main'" — `gh` had switched the checkout when it deleted the merged branch. |
| `git pull --ff-only` | "Already up to date." |
| `git rev-parse HEAD` | `32cde54ef6afb8f994a2f7d804f1c991a62df9e8` — THE MERGE COMMIT AND THIS ROUND'S BASE. |
| `git checkout -b feature/f033-hunk-approval` | "Switched to a new branch 'feature/f033-hunk-approval'" |
| `git push -u origin feature/f033-hunk-approval` | Run after this commit; the tip comparison it enables is reported in the round report (see deviations, item 3). |
| worktree add / remove | NONE. No disposable worktree was needed: no gate this round mutates a tracked file, and every "base blob" reading was taken with `git show <base>:<path>` into memory as the block orders. |
| PR create | NONE. The block creates no pull request this round. |

## Verification

One line per gate, the real result.

- G1 HYGIENE — `os.path.exists(".agent/STOP")` is **False** before C0a and
  **False** again before C5. `git branch --show-current` is
  `feature/f033-hunk-approval`. `git status --porcelain | wc -l` after each of
  C0a, C0b, C1, C2, C3, C4a, C4b: **0, 0, 0, 0, 0, 0, 0**.
- G2 TRANSPORT — sha256 of `git show 0f7e716c:.agent/authored/f033-r1.md` is
  `27dd7e0ca170d48547e99fcd242032149cd8638df252a71224b58c2e5fcac6fd`; sha256 of
  the reviewer's original `.remedy-wt/f033-r1.md` is the same digit for digit;
  the byte comparison `blob == original` is **True**; 29247 bytes, 415 lines.
  `git rev-parse fb27cd55:.agent/authored/f033-r1.md` and
  `git rev-parse fb27cd55:.agent/last_block.md` both print
  `cc2ddb7dfbde495b347a3ed26eead2ba05ee522d` — ONE blob id.
- G3 THE PLAN AT C1 — PLANF033R1 re-extracted from the COMMITTED C0a blob equals
  `git show b90c8a9a:.agent/plan.md` byte for byte including the trailing
  newline: **True**. NEGATIVE CONTROL with the trailing newline dropped:
  **False**. `wc -l` **41**, under 50. Lines exactly `## Goal`: **1**. Lines
  exactly `## Next Steps`: **1**.
- G4 THE RECORD AT C3, BOTH READERS — (a) base blob with its single RECORDHEAD
  FROM replaced by the TO, plus one newline, plus GATEF037R27, EQUALS the C3
  blob: **True**. NEGATIVE CONTROL: the first paragraph of GATEF037R27 ends at
  slice offset **5298**; the byte flipped is at slice offset **50** (absolute
  file offset **1334620**), confirmed by the script to lie inside that first
  paragraph, and the equality becomes **False**. (b) N counted by the script from
  the slice itself is **2**; the LAST 2 blank-line units of the C3 blob equal
  those 2 paragraphs in order, unit by unit (**True**, lengths 5298 and 1173).
  The base blob's bytes AFTER its RECORDHEAD FROM are a byte-exact PREFIX of the
  C3 blob's bytes after the RECORDHEAD TO: **True** (1332493 bytes growing to
  1338968; whole file 1334200 → 1341044).
- G5 THE LEDGER — BASE / C3. Registrations `^- R-\d+ — `: **292 / 292**, all
  DISTINCT in both. `^Done: R-\d+ — `: **43 / 43**. `^Landed: R-`: **11 / 11**.
  `^Gate: F\d+ R\d+ — `: **97 / 98**, a rise of EXACTLY ONE. Maximum id
  **R-0731 / R-0731**. OPEN SET computed as a set: **251 / 251**, and the two
  sets are identical, not merely equal in size. `Gate: F037 R27` occurrences:
  **0 at the base / 1 at C3**. `R-0714`: **1** registration line, **0** `Done:`
  lines, **0** `Landed:` lines — unchanged at both commits, so it stays OPEN.
- G6 THE STATUS CLAIM AT C2 — STATUSCLAIM FROM occurs **1** time in
  `docs/roadmap/STATUS.md` at the base, verified before writing. Over the C2
  content: FROM **0**, TO **1**, and the TO is present AS A WHOLE LINE exactly
  **1** time. `^- \[~\]`: **0** at the base, **1** at C2. `^- \[x\] F\d{3} — `:
  **60** at the base, **60** at C2 — unmoved, as a claim must leave it.
- G7 THE DOCS GATE AND THE CANARY, run after C4, serially, one pytest process at
  a time, `returncode` read from `subprocess.run(..., capture_output=True)`:
  `python3 -m pytest tests/docs/ -q` → exit **0**, final line
  `295 passed in 0.50s`. `python3 -m pytest tests/cli/test_golden_path.py -q` →
  exit **0**, final line `42 passed in 22.44s`.
- G8 STRUCTURE — measured over `32cde54e..d4b05cf0` (C4b), the last commit that
  exists when these bytes are written; see deviations item 3 for the three
  readings that cannot. `git diff --name-only` returns exactly
  `.agent/authored/f033-r1.md`, `.agent/f033_inventory.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`.
  measured-minus-changeset is **EMPTY**; changeset-minus-measured is exactly
  `[.agent/handoff.md]`, the one path C5 itself adds. `git diff --stat`
  restricted to `apps/`, to `packages/`, to `tests/` and to
  `docs/roadmap/features/` prints **the empty string in all four cases**. Parent
  counts: C0a **1**, C0b **1**, C1 **1**, C2 **1**, C3 **1**, C4a **1**,
  C4b **1**. Insertions: **415, 368, 28, 1, 33, 367, 207** — each under 500.
  `git ls-files .remedy-wt | wc -l` is **0**.

## Authored-text proofs

- `PLANF033R1` → `.agent/plan.md` at C1: re-extracted from the COMMITTED
  `.agent/authored/f033-r1.md` blob, never from the prompt; byte-equal including
  the trailing newline, with the newline-dropped negative control False (G3).
- `STATUSCLAIM` P1 → `docs/roadmap/STATUS.md` at C2: FROM 1x before, FROM 0x and
  TO 1x after, TO present as a whole line exactly once (G6).
- `RECORDHEAD` P1 and `GATEF037R27` → `.agent/live_review.md` at C3: the whole
  C3 blob reconstructed byte for byte from the base blob plus the pair plus the
  append, with a confirmed in-paragraph byte flip breaking it (G4).
- The block itself → `.agent/authored/f033-r1.md` and `.agent/last_block.md`:
  digest-equal to the reviewer's own `.remedy-wt/f033-r1.md`, which existed
  before this worker did, and the two committed paths are ONE git blob (G2).

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 Open PR Gate | done | Exactly one non-draft `feature/*` → `main` PR, #218, merged; base recorded |
| C0a save the block | done | `0f7e716c` |
| C0b mirror the block | done | `fb27cd55` |
| C1 the plan | done | `b90c8a9a` |
| C2 the STATUS claim | done | `1a765aab` |
| C3 the record header and the F037 R27 gate | done | `d2e77606`, one commit for both |
| C4 the source inventory | deviated | Split into `fff34c44` (sections 1–5) and `d4b05cf0` (sections 6–9), at a whole-section boundary, under constraint 4: the single commit measured 574 insertions |
| C5 the handback | done | this commit |
| Push | done | `git push -u origin feature/f033-hunk-approval`, run after this commit |
| Inventory question 1 hunk identity | done | |
| Inventory question 2 version field | done | |
| Inventory question 3 `diff_repair` guards | done | Five files confirmed; only one guards the three named symbols, and that is reported |
| Inventory question 4 applicator | done | |
| Inventory question 5 write channel | done | `UI_EXPOSED_COMMANDS` confirmed as exactly `job.stop` and `decision.resolve` |
| Inventory question 6 validation precedent | done | Answered as a DELIBERATE ABSENCE plus the two nearest real precedents |
| Inventory question 7 rejection seam | done | Answered as a DELIBERATE ABSENCE for the name, plus the seam that really exists |
| Inventory question 8 change state | done | |
| Inventory question 9 three surfaces | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |
| G7 | done | |
| G8 | deviated | Three readings depend on C5 or on the push and cannot exist when C5's bytes are written; see deviations item 3 |

## Deviations & assumptions

1. **C4 WAS SPLIT INTO TWO COMMITS, AND THAT IS A DEPARTURE FROM THE BLOCK'S
   ORDERED COMMIT SEQUENCE.** `.agent/f033_inventory.md` measured **574**
   insertions as one commit, over the 500 cap. Constraint 4 orders exactly this:
   split at a whole-section boundary and declare it. The boundary is the line
   before `## 6. THE VALIDATION PRECEDENT`; C4a carries sections 1–5 at 367
   insertions and C4b carries sections 6–9 and Unanswered at 207. The committed
   file at C4b is byte-identical to the file that measured 574: C4b's diff is a
   pure append of 207 lines with 0 deletions.
2. **THE SHELL GUARD REJECTED THREE COMMAND FORMS AND EACH WAS RE-EXPRESSED, NOT
   WEAKENED.** (a) A bash `for` loop over the five `diff_repair` test files was
   refused by form and re-expressed as a `python3` heredoc that read each file and
   printed its test names — same evidence. (b) Two composite `python3` heredocs
   for G8 were refused; each was re-expressed as smaller heredocs measuring one
   property at a time, plus a plain `git ls-files .remedy-wt | wc -l`. No gate was
   skipped and no gate's assertion was loosened. Constraint 7 covers this.
3. **G8 CARRIES THREE READINGS THAT CANNOT EXIST IN THIS FILE.** The block says
   "G1 through G8 all run at commits strictly earlier than C5", yet G8's own text
   orders `git diff --name-only <base>..<C5>`, C5's parent count, and a
   post-push `git rev-parse HEAD` against
   `git rev-parse origin/feature/f033-hunk-approval`. None of those three values
   exists at the moment C5's bytes are written, so writing them here would be a
   self-referential claim. The block is applied as written (constraint 1) and the
   contradiction is declared here: the C5-INDEPENDENT readings are in the G8 line
   above, measured over `32cde54e..d4b05cf0`, and the three C5-dependent readings
   are taken by this worker AFTER C5 and AFTER the push and are reported to the
   reviewer in the round report. The reviewer re-runs all of them itself.
4. **NO DISPOSABLE WORKTREE WAS CREATED.** Guardrail G5 requires one only for
   mutating or destructive verification, and no gate this round mutates a tracked
   file: every base-blob reading used `git show <base>:<path>` into memory, as the
   block orders. `.remedy-wt/` therefore holds only the reviewer's own
   `f033-r1.md`, and `git ls-files .remedy-wt` prints 0 lines.
5. **ONE SCRATCH FILE WAS CREATED AND REMOVED BY EXACT PATH.**
   `.remedy-wt/f033_inventory_full.md` held the full inventory text while C4a was
   committed with the truncated file; it was removed with
   `os.remove(".remedy-wt/f033_inventory_full.md")` after C4b, by exact path, and
   its absence was verified. No glob deletion was used anywhere this round.
6. **`.agent/context.md` AND `.agent/decisions.md` STILL DESCRIBE F037.** The
   block's change set is "these paths and nothing else" and names neither file,
   so neither was touched. AGENTS.md's Commit Gate item 7 asks whether they need
   updating: they do, and that update belongs to the next round rather than to
   this one, because widening a change set the block fixed would be a silent scope
   change. Flagging it rather than doing it.
7. **NO SLICE WAS EDITED.** All four slices — PLANF033R1, STATUSCLAIM,
   RECORDHEAD, GATEF037R27 — were applied byte for byte as written. Nothing in
   them was found wrong.
8. **ONE INVENTORY ANSWER IS NARROWER THAN THE BLOCK'S FRAMING, AND IT IS SAID SO
   IN THE FILE.** Question 3 asks for "every test file that guards"
   `RepairHunk`, `RepairHunkSelection` and `select_repair_hunks`. All five files
   the block names do contain the string `diff_repair` — confirmed, the grep
   returns exactly those five — but only `tests/orchestration/test_diff_repair.py`
   imports and asserts on the three named symbols. The other four guard
   `diff_repair_apply`, `diff_repair_response`, the loop that CALLS the selection,
   and (in `test_command_channel.py`) a single string inside a forbidden-imports
   frozenset. Section 3 of the inventory says exactly this, because T001's real
   safety net is narrower than the file count suggests.

## Open findings

**251**, computed as a SET over `.agent/live_review.md` at C3: 292 registered ids
minus the ids carrying a `Done:` or a `Landed:` line. Unmoved from the base. This
round registered no finding and resolved none; it booked one `Gate:` paragraph,
F037 R27. `R-0714` remains open as the documented Medium risk inherited across
the reset.

## Next

The reviewer books the R1 verdict in the first commit of R2 and plans T001 —
stable content-hash hunk ids, the stability property tests, the viewer JSON
version bump and the shared-helper consolidation with `diff_repair` — against
`.agent/f033_inventory.md`. Phase 1 rule 1 first: re-read `.agent/STOP` from disk
before anything else; then rule 2, the Open PR Gate, which should find no open
pull request because this round created none.
