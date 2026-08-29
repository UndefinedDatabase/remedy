# Handback — F040 · SESSION 1 · round 1 — THE CLAIM, THE TWO CANDIDATES, THE SEAM INVENTORY

> Written by the WORKER in C7, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe.

## Session

SESSION 1 of feature F040 · round 1 · rounds so far 1.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed.

## Range

Review of `f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`..`HEAD` on branch
`feature/f040-completion-digest`, cut from `main` at that base — the merge commit
of pull request 222.

## Commits

### ed8fb753 docs(f040): save the round 1 step block verbatim

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r1.md` | +339 / -0 | C0a. The round's step block, copied with `shutil.copyfile` from `.remedy-wt/f040-r1-block.md`. Never retyped. |

### 0392be34 docs(f040): mirror the round 1 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +308 / -275 | C0b. The same bytes again, by a second `shutil.copyfile` from the same scratch original. |

### 05dca153 docs(f040): retarget the plan at the F040 claim round

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +25 / -28 | C1. Full rewrite from slice PLAN1. FIRST substantive commit, ahead of the ledger append, so the Commit Gate reads a plan that matches the work. |

### 249e648f docs(f040): record the two discharged closure candidates and decision D1

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | C2. APPEND-ONLY: one blank separator line plus RECORD1's two paragraphs. Zero deletions. No id minted, none resolved. |

### 7616a884 docs(f040): empty the closure candidates carrier

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/candidates.md` | +6 / -35 | C3. Full rewrite from slice CAND1. The block condition on the F040 claim lifts here. |

### 2ed1ba3d docs(f040): claim F040 in the roadmap ledger

| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1 / -1 | C4. Pair PAIR-STATUS, a REWRITE (`TO contains FROM: false`), applied once. `- [ ] F040` becomes `- [~] F040`. |

### 3ef0b5a0 docs(f040): retarget the context at the digest feature

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/context.md` | +19 / -20 | C5. Full rewrite from slice CONTEXT1, standing project constraints carried forward inside the slice. |

### 6149c7ac docs(f040): measure the four digest seams into the round 1 inventory

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/f040_inventory.md` | +499 / -0 | C6. THE WORKER'S OWN MEASUREMENT per the block's SPEC. 499 lines, 67 `file:line` citations over 28 distinct paths, every one resolving under `git ls-tree HEAD`. |

### C7 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | not tabled | A handback cannot table the commit that writes it. Full rewrite per docs/agents/handback_template.md. |

## External actions

| Command | Outcome |
|---------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — Open PR Gate passes, no open PR. PR 222 was already merged into `main` before this round began. |
| `git checkout -b feature/f040-completion-digest f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1` | `Switched to a new branch 'feature/f040-completion-digest'`; `git rev-parse HEAD` = `f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`; `git status --porcelain` empty. |
| `git worktree add --detach .remedy-wt/g3wt HEAD` (inside the G3 script) | returncode 0. The disposable worktree for the G3 negative control. |
| `git worktree remove --force .remedy-wt/g3wt` + `git worktree prune` | Removed; the script re-read `WT.exists()` as `False` and the PRIMARY checkout's `git status --porcelain` as `''`. |
| `git reset --mixed HEAD~1` once and `git commit --amend` three times, all on C6 | Local only, never pushed, no history rewrite of any published commit. Reason in Deviations, item 1. |
| `git push -u origin feature/f040-completion-digest` | Issued immediately after this commit. NO pull request is opened — the block forbids it; the PR is created at closure. |

`python3 -m apps.cli.grouped` was NOT needed this round: no CLI invocation was
required by any gate. The `remedy` console script is denied in this sandbox and
was not called.

## Verification

One line per gate, each with its REAL exit code.

    G1  TRANSPORT, at C0b .................................... REAL exit 0
        sha256 9c0c71913863c6f9c15bc648cc94ecf9aefed84fd55d474732a63e9e5ad3e276
        byte length 21083, and ALL THREE FILES ARE EQUAL:
          .remedy-wt/f040-r1-block.md   (the scratch original)
          .agent/authored/f040-r1.md    (committed at C0a)
          .agent/last_block.md          (committed at C0b)
        ONE digest comparison, not a chain.

    G2  THE PLAN, at C1 ...................................... REAL exit 0
        .agent/plan.md   sha256 7271c247fc0583dd41b71e65273e81efbe3392c2123f7e9731733c78e42d363c, 1805 bytes
        slice PLAN1      sha256 7271c247fc0583dd41b71e65273e81efbe3392c2123f7e9731733c78e42d363c, 1805 bytes
        BYTE-EQUAL True · 37 lines (< 50 True) · holds `## Goal` True · holds `## Next Steps` True

    G3  THE RECORD APPEND, at C2 ............................. REAL exit 0
        ARITHMETIC, base re-measured by this worker at the commit it appended at:
          1640101 + 1 + 3531 = 1643633 = the committed byte length. OK.
          (The reviewer's stated 1640101 at `f5b1e6c5` is confirmed, not assumed.)
        N COUNTED by the script from RECORD1's blank-line units = 2.
        UNFLIPPED committed file, sha256 709af495bff76fa5015ff57d9510976ebf2f2a7aec926f63fa76748f8f4021b1:
          (a) WHOLE RECONSTRUCTION — base + separator + slice compared to the ENTIRE
              committed file, not a prefix test .............. True
          (b) PARAGRAPH ORDER — last 2 blank-line units equal RECORD1's 2
              paragraphs IN ORDER ........................... True
        NEGATIVE CONTROL, inside the disposable worktree `.remedy-wt/g3wt`:
          absolute byte 1640202 flipped, b' ' -> b'\x00', INSIDE the FIRST appended
          paragraph (which spans bytes 1640102..1641721).
          flipped file sha256 5bba18c4461291184b375686fe432abb3d01bf05f2d1c2f6a3005cbb06fc9a7b
          (a) rejects the flip: True   (b) rejects the flip: True
          restored file: (a) accepts True, (b) accepts True
        Worktree removed; PRIMARY `git status --porcelain` = '' at the reading.

    G4  THE LEDGER, at C1 and at C2 .......................... REAL exit 0
        at C1 05dca153:  `^- R-\d+ — ` distinct 311 · `^Done: R-\d+ — ` distinct 53 · open 258
                         `^DECISION F040 D\d+ — ` ids []
        at C2 249e648f:  `^- R-\d+ — ` distinct 311 · `^Done: R-\d+ — ` distinct 53 · open 258
                         `^DECISION F040 D\d+ — ` ids ['D1']
        ADDED registered ids C1->C2 = []      (must be [], and is)
        ADDED resolved   ids C1->C2 = []      (must be [], and is)
        ADDED F040 DECISION ids     = ['D1']  (must be ['D1'], and is)
        `^Done: R-0570` line count at C2 = 0 — R-0570 STAYS OPEN.

    G5  THE CANDIDATES FILE, at C3 ........................... REAL exit 0
        byte length BEFORE (at C2 249e648f) 3024 · AFTER (at C3 7616a884) 796
        .agent/candidates.md sha256 bae384d32dfac4880dac561d9323dee202630288958053b22f815957271b2d89
        slice CAND1          sha256 bae384d32dfac4880dac561d9323dee202630288958053b22f815957271b2d89
        BYTE-EQUAL True, for BOTH the working tree and the committed blob.
        occurrences of `· F033 · 2026-08-29`: before 1, after 0.

    G6  THE CLAIM AND THE DOCS PINS, at C4 — four readings, four exit codes:
        G6 structural ........................................ REAL exit 0
          PAIRSTATUS-FROM occurs 0 · PAIRSTATUS-TO occurs 1
          `git diff --numstat 2ed1ba3d^ 2ed1ba3d` = exactly `1  1  docs/roadmap/STATUS.md`
          lines matching `^- \[~\] F\d{3} — ` in the whole file = 1
        G6 `python3 -m pytest tests/docs/ -q` ................ REAL exit 0 — 295 passed in 0.44s
        G6 `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`
                                                  ........... REAL exit 0 — 30 passed in 0.35s
        Both figures EQUAL the reviewer's base measurement (295 and 30).

    G7  THE STATE READERS AND THE CANARY, at C6 — five readings, five exit codes:
        `python3 -m pytest tests/ui_server/ -q` .............. REAL exit 0 — 508 passed in 31.22s
        `python3 -m pytest tests/orchestration/test_test_runner.py -q`
                                                  ........... REAL exit 0 —  52 passed in  5.35s
        `python3 -m pytest tests/regression/test_resource_safety.py -q`
                                                  ........... REAL exit 0 —  21 passed in 11.56s
        `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`
                                                  ........... REAL exit 0 —  16 passed in  0.28s
        `python3 -m pytest tests/cli/test_golden_path.py -q` . REAL exit 0 —  42 passed in 20.72s
        All five EQUAL the reviewer's base measurement (508, 52, 21, 16, 42).
        THE FOUR STATE READERS WERE RUN AS FOUR, NOT AS THREE.

    G8  THE INVENTORY AND THE TREE, at C6 .................... REAL exit 0
        `.agent/f040_inventory.md` exists, 27101 bytes over 499 lines.
        All six SPEC section headings present, in order:
          ## 1. The next-action rule table — the one-source seam for the digest's CTA
          ## 2. The decision inbox read path
          ## 3. The cost line and its basis
          ## 4. The ownership seam — ABSENT, and here is how it was searched
          ## 5. The server seam
          ## 6. The UI and CLI seams
        67 `file:line` citations over 28 distinct paths; EVERY path resolves under
        `git ls-tree HEAD -- <path>`; the not-resolving list is [].
        `git status --porcelain` EMPTY.
        `git ls-files --others --exclude-standard` count 0.
        Per-commit insertions, from `git diff --numstat <sha>^ <sha>`, every one
        under 500: C0a 339 · C0b 308 · C1 25 · C2 4 · C3 6 · C4 1 · C5 19 · C6 499.

## Authored-text proofs

Every authored unit was extracted MECHANICALLY from `.remedy-wt/f040-r1-block.md`
by `.remedy-wt/f040r1_extract.py`, which asserts that each `<<<BEGIN <NAME>` and
`<<<END <NAME>` marker line occurs exactly once and takes the bytes between them.
Nothing was retyped. The block original is committed byte-identical at
`.agent/authored/f040-r1.md` (G1), so each disk-to-disk comparison below is
against the committed authored file's own content.

| Slice | bytes | sha256 | applied to | result |
|-------|-------|--------|------------|--------|
| PLAN1 | 1805 | `7271c247…d363c` | `.agent/plan.md` (C1) | BYTE-EQUAL (G2) |
| RECORD1 | 3531 | `3217492364…c470c` | appended to `.agent/live_review.md` (C2) | WHOLE RECONSTRUCTION exact + PARAGRAPH ORDER exact (G3) |
| CAND1 | 796 | `bae384d32d…b2d89` | `.agent/candidates.md` (C3) | BYTE-EQUAL (G5) |
| CONTEXT1 | 3118 | `1e15d042e7…e1989` | `.agent/context.md` (C5) | BYTE-EQUAL, verified at write time by `.remedy-wt/apply_slice.py` |
| PAIRSTATUS-FROM | 40 | `915fc36c79…fddf` | `docs/roadmap/STATUS.md` | occurred exactly 1 before, 0 after (G6) |
| PAIRSTATUS-TO | 40 | `566c3c4728…fe8f` | `docs/roadmap/STATUS.md` | occurs exactly 1 after (G6) |

`TO contains FROM` measured as `false`, so PAIR-STATUS is a REWRITE and the
FROM-zero / TO-one count is the right reading of it, exactly as constraint 12
states.

## Item status

Every bundle item and every gate, each exactly once.

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f040-r1.md` | done | `shutil.copyfile`, ed8fb753 |
| C0b mirror the same bytes into `.agent/last_block.md` | done | second `shutil.copyfile`, 0392be34 |
| C1 rewrite `.agent/plan.md` from PLAN1 | done | 05dca153 |
| C2 append RECORD1 to `.agent/live_review.md` | done | 249e648f, append-only, 0 deletions |
| C3 rewrite `.agent/candidates.md` from CAND1 | done | 7616a884 |
| C4 apply PAIR-STATUS to `docs/roadmap/STATUS.md` | done | 2ed1ba3d |
| C5 rewrite `.agent/context.md` from CONTEXT1 | done | 3ef0b5a0 |
| C6 write `.agent/f040_inventory.md` per the SPEC | deviated | 6149c7ac. Written and measured in full; the commit was RESET once and AMENDED three times before push, see Deviations 1. |
| C7 rewrite `.agent/handoff.md` | done | this commit |
| G1 TRANSPORT at C0b | done | REAL exit 0 |
| G2 THE PLAN at C1 | done | REAL exit 0 |
| G3 THE RECORD APPEND at C2 | done | REAL exit 0 |
| G4 THE LEDGER at C1 and C2 | done | REAL exit 0 |
| G5 THE CANDIDATES FILE at C3 | done | REAL exit 0 |
| G6 THE CLAIM AND THE DOCS PINS at C4 | done | REAL exit 0 structural, 0 `tests/docs/`, 0 `test_roadmap_index.py` |
| G7 THE STATE READERS AND THE CANARY at C6 | done | REAL exit 0 × 5 |
| G8 THE INVENTORY AND THE TREE at C6 | done | REAL exit 0 |

## Deviations & assumptions

**1. C6 TOOK FOUR ATTEMPTS — ONE RESET AND THREE AMENDS — BEFORE IT WAS RIGHT.
DECLARED HERE BECAUSE A COMMIT-SEQUENCE DEPARTURE BELONGS IN THIS SECTION EVEN
WHEN IT IS CORRECT.** The FIRST C6 measured `+504` insertions on
`git diff --numstat` — over the AGENTS.md 500-line insertion cap, and over G8's
own "every one under 500". `.agent/f040_inventory.md` is NOT one of the five
state files the DECISION F104 D1 exemption names (`last_block.md`, `handoff.md`,
`live_review.md`, `plan.md`, `context.md`), so no exemption applied and the
oversize-with-declaration route was the wrong answer for a file I could simply
tighten. I reset it (`git reset --mixed HEAD~1`), condensed prose without
dropping a single measurement, and recommitted at 499. The SECOND attempt fell to
G8, which reported two cited paths that did NOT resolve — `decisionOrder.ts` and
`decision_inbox.py`, bare-filename shorthands in prose where the full path stood
a few lines above; I expanded both to full repository paths, which is what the
SPEC's "a `file:line` for every claim" actually asks for. The THIRD attempt
briefly went back to 500 insertions and was tightened again. The FOURTH fixed a
citation G8 could not catch and my own self-review did: the inventory cited
`.agent/plan.md:118-119` for the plan's second Risk, which are the line numbers
of that text IN THE BLOCK FILE, not in the 37-line `.agent/plan.md` it names. The
correct citation is `.agent/plan.md:36-37`. G8's path-resolution reading passes a
line number that does not exist, so I wrote `.remedy-wt/spotcheck.py`, which
opens 53 sampled citations and asserts the cited LINE contains what the inventory
says it does: 52 confirmed exactly, and the 53rd
(`docs/roadmap/features/T5_F040.md:57-58`) is a two-line quote my one-line probe
could not match and which I then read by hand and confirmed. Nothing was pushed
at any point, so no published history was rewritten. FINAL C6 IS `6149c7ac`; the
abandoned objects `8b62d172`, `a60a4448` and `34f74cc0` are unreferenced.

**2. THE BLOCK'S SLICE `PLAN1` CARRIES A CLAIM I APPLIED VERBATIM AND WOULD
OTHERWISE HAVE QUESTIONED.** `.agent/plan.md` line 99 marks "the seam inventory"
as `done` in the C1 commit, one commit BEFORE C6 writes the inventory. It is
false at C1 and true at C6, which is the ordinary shape of a plan that describes
the round rather than the commit — but it means a reader at `05dca153` reads a
`done` for a file that does not yet exist. Constraint 1 orders slices applied
byte for byte, so it is applied byte for byte and declared here instead of
improved.

**3. THE INVENTORY REPORTS A STALE COMMENT IN SHIPPED CODE, AND THE STALENESS IS
THE FINDING-SHAPED THING I DID NOT REGISTER.** `packages/orchestration/run_report.py:170`
documents `NEXT_ACTION_RULES` as `(rule id, condition, action template)` — three
elements — while the value at :175 is annotated `tuple[tuple[str, str], ...]` and
holds PAIRS. I did not mint an R-id for it: constraint 5 forbids minting one this
round, and it is recorded in the inventory (section 1) where the T001 order will
read it. Whoever writes that order decides whether it earns an id.

**4. THE OWNERSHIP SEAM IS ABSENT AND THE ABSENCE IS AS WIDE AS THE SEARCH.** Six
commands over all of `packages/` and all of `apps/` are quoted verbatim in
inventory section 4 with their exact results. The widest of them,
`git grep -l -i -E 'ownership' -- packages/ apps/`, matched 9 files; every one was
opened and classified, and all nine are PROCESS, FILE or REPO ownership, not the
human-attribution ledger F035 describes. `git grep` reads tracked files only, so
the claim does not reach untracked or ignored paths — stated so it is not read
wider than it was measured.

**5. THE URGENCY FORMULA IS NOT IMPORTABLE FROM PYTHON, WHICH THE FEATURE FILE
ASSUMES IT IS.** `docs/roadmap/features/T5_F040.md:57-58` orders digest
significance to be "one source with the inbox". The formula is
`apps/ui/src/api/decisionOrder.ts:21-39` — browser-side TypeScript, whose own
header comment at :3-5 says the rule "is written down nowhere else".
`git grep -i -E "urgency|significance" -- packages/ apps/` matches ZERO lines
under `packages/`. I recorded the three routes in inventory section 2 and chose
none: choosing is the T001 order's job, not this round's.

**6. NO OTHER DEPARTURE.** The bundle ran in the block's order, the change set is
exactly the nine declared paths and nothing else, no file under `packages/`,
`apps/`, `tests/`, `docs/guides/`, `docs/system/` or `docs/roadmap/features/` was
touched, no production code and no test was written, no R-id was minted or
resolved, and no pull request was opened.

## The two candidates, as discharged

Both entries the F033 closure gate left in `.agent/candidates.md` are settled and
the file now reads `EMPTY — no candidate is open.`, which lifts the block
condition on the F040 claim. NO ID WAS SPENT ON EITHER.

- The FIRST — the README's per-tier accepted list guarded in one direction only,
  now one feature short — went on the record as NEW EVIDENCE on the ALREADY-OPEN
  finding **`R-0570`**, per planner_reviewer_prompt.md §3 item 30. **R-0570 STAYS
  OPEN** and is **ROUTED AWAY FROM THIS BRANCH**: its fix edits `README.md` and
  `tests/docs/test_docs_consistency.py`, neither of which F040 owns, and AGENTS.md
  forbids mixing an unrelated fix into a feature branch. G4 confirms zero
  `^Done: R-0570` lines at C2. It is also carried as the first Risk in
  `.agent/plan.md`.
- The SECOND was settled as **DECISION F040 D1 — no defect, nothing edited**. G4
  confirms the added `^DECISION F040 D\d+ — ` id set is exactly `['D1']`.

## Next

The single expected next action: the reviewer re-runs G1 through G8 at
`f5b1e6c5..6149c7ac` plus this commit, reads `.agent/f040_inventory.md`, and
writes the T001 order — the endpoint composition, the `NEXT_ACTION_RULES` import
and the fixture goldens — WITH the decision inventory section 2 forces about the
urgency formula and the decision inventory section 4 forces about the unbuilt
ownership seam. No pull request is opened until closure.
