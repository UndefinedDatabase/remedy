# Handback — F032 R13 (T003a: the card model learns the triple)

## Session

SESSION 3 of feature F032 · round R13 · rounds so far 13

Session 3 began at R10. Session 1 was R1 through R5; session 2 was R6 through
R9. Thirteen rounds across three sessions is inside the soft limit of 25 rounds
or 7 sessions, so no limit report is owed and none is emitted.

## Range

Review of `4b1b2e99`..`8694120b` (C5, the commit writing this file, is not in
that range and cannot table itself).

## State

- Feature: F032, the evidence triple. Round R13, task T003a.
- Branch: `feature/f032-evidence-triple`. Base of the round: `4b1b2e99`,
  confirmed by `git rev-parse HEAD` before C0a.
- `.agent/STOP`: ABSENT at both readings constraint 8 orders — once before C0a,
  once before C5.
- No pull request created, none merged. Open PR Gate reports `[]`.
- Open findings: 250 (unmoved; this round registered none and resolved none).
  Maximum id `R-0713`, unmoved.

## Commits

### 7f1da6e6 docs(agent): save the F032 R13 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f032-r13.md` | +321 / -0 | C0a, the byte-preserving copy of the block |

### 3bc7141f docs(agent): mirror the R13 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +252 / -288 | C0b, the same bytes written over the previous round's block |

### 03c6b9be docs(agent): open T003 in the plan
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +23 / -24 | C1, slice PLANF032R13 applied whole |

### 92ebbc4f docs(agent): book the R12 verdict and the close of T002
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C2, slice LEDGER13 appended; the only commit touching the record |

### 5284ba66 feat(ui): the card model carries the evidence triple
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/decisionCard.ts` | +225 / -5 | C3, spec items S2 through S7 |

### 8694120b test(ui): pin the triple on the card model and its answers
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/decisionCard.test.ts` | +407 / -17 | C4, spec item S8 |

### C5 docs(agent): hand back F032 R13
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | not tabled | A handoff cannot table the commit that writes it (R-0149 pattern). Its numstat is not read, not predicted and not stated here. |

The `+/-` cells above and the insertion counts reported under G8 are ONE
`git diff --numstat` reading written twice; they were compared cell by cell and
they agree.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it into `last_block` | done | |
| C1 the plan | done | |
| C2 the R12 verdict | done | |
| C3 the model and its types | done | |
| C4 its tests | done | |
| C5 the handback | done | this file |
| S1 read first | done | module, its tests and the producer read before any edit |
| S2 the copy rule | done | `scrubUiText` from `../copy/humanCopy` decides every chip's text |
| S3 the ref projection | done | `DecisionEvidenceRef` + `evidenceRefs`; blank target dropped |
| S4 the outcome reaches its answer | done | matched inside `decisionAnswers`, no `card.type` branch |
| S5 the status becomes a sentence | done | `evidenceNote`; no raw status on the model, no boolean beside it |
| S6 nothing else changes | done | no other field, function or type altered |
| S7 the three endpoint keys | done | `evidence_refs`/`outcomes`/`evidence_status`, optional and `unknown` |
| S8 the tests | done | 80 tests in `decisionCard.test.ts`, every listed case covered |

## External actions

- `git worktree add .remedy-wt/r13mut 8694120b --detach` — created for the G7
  mutation runs. Outcome: "HEAD is now at 8694120b".
- `git worktree remove .remedy-wt/r13mut` — outcome: `git worktree list` back to
  1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
  outcome `[]`. Nothing created, nothing merged.
- `git push -u origin feature/f032-evidence-triple` — run after C5.

## Verification

**G1 — hygiene, base and the sentinel.**
`git rev-parse HEAD` before C0a → `4b1b2e995aebe1e997a90e47f8008c8981f643b2`,
which IS the base of constraint 10. `git rev-parse --abbrev-ref HEAD` →
`feature/f032-evidence-triple`. `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2, C3, C4 → `0`, `0`, `0`, `0`, `0`, `0`. `.agent/STOP` at both
ordered readings → `ls: cannot access '.agent/STOP': No such file or directory`,
exit 2 both times, so ABSENT both times.

**G2 — transport.** All three artifacts carry sha256
`35bccbc815fdae5117a4c88155c7a26027bfc03c4695e87f7df32d0d29108119` over
`26943` bytes and `321` lines:

| Artifact | sha256 | bytes | lines |
|---|---|---|---|
| `.remedy-wt/f032-r13.md` (reviewer's scratch original) | `35bccbc8…08119` | 26943 | 321 |
| committed `.agent/authored/f032-r13.md` blob | `35bccbc8…08119` | 26943 | 321 |
| committed `.agent/last_block.md` blob | `35bccbc8…08119` | 26943 | 321 |

All three EQUAL. `git rev-parse HEAD:.agent/authored/f032-r13.md` and
`HEAD:.agent/last_block.md` both → `755261e837a5bcc99b1d9eda6e7072c7a749b315`,
so C0a and C0b are the SAME git blob. Plainly: this proves the reviewer's
scratch original, the saved copy and the mirror agree. It says NOTHING about the
bytes of any prompt — under docs/agents/self_drive_protocol.md there is no paste
relay, and the chain measured here runs scratch file → committed copy → mirror.

**G3 — extraction and caps.** From the COMMITTED C0a blob:

| Region | content lines |
|---|---|
| `PLANF032R13` | 48 |
| `LEDGER13` | 1 |

Regions: `2`. CONTENT total: `49`. Block TOTAL: `321`. PROSE = 321 − 49 = `272`.
PROSE under 400: TRUE. TOTAL under 490: TRUE. These are the numbers the
extraction measured, not numbers restated from the block.

**G4 — the plan.** `.agent/plan.md` at C1 byte-equal to slice PLANF032R13 under
constraint 2 → `True`. NEGATIVE CONTROL, the same comparison with the trailing
newline removed → `False`, as required. `wc -l` → `48`, under 50 → TRUE.
`^## Goal$` count → `1`. `^## Next Steps$` count → `1`.

**G5 — the ledger append.** Pre-commit blob read with
`git show 4b1b2e99:.agent/live_review.md`; the tracked file was never written
over to obtain it, and it was asserted equal to the on-disk file before the
append.

- Arithmetic: `1086751 + 1 + 5183 = 1091935` → holds.
- Base is a byte PREFIX of the result → `True`.
- READER 1 (exact byte identity, base + one newline + slice) → accepts.
- READER 2 (independent structural: split the whole file on blank lines, take
  the LAST N units against the slice's own N paragraphs in order), N = `1` →
  accepts.
- NEGATIVE CONTROL: one byte flipped in memory at offset `1086762`, inside the
  FIRST appended paragraph (`' '` → `'\x00'`). READER 1 rejects → `True`.
  READER 2 rejects → `True`. BOTH readers reject it.

Base measurements confirmed independently at `4b1b2e99`: `1086751` bytes over
`429` blank-line units — both equal to the reviewer's stated figures.

| Pattern | before | after |
|---|---|---|
| `^Gate: F\d+ R\d+ — ` | 64 | 65 |
| `^- R-\d+ — ` | 274 | 274 |
| `^Done: R-\d+ — ` | 24 | 24 |
| `^Landed: R-` | 1 | 1 |
| `^Gate: R\d+ — ` | 19 | 19 |
| open set | 250 | 250 |
| maximum id | `R-0713` | `R-0713` |

All five "before" counts equal the reviewer's stated 64, 274, 24, 1 and 19, with
the open set 250 and the maximum `R-0713`. Gate keys ADDED: `['F032 R12']`.
Ids ADDED to the resolved set: `[]` — this round registered no finding and
resolved none.

**G6 — the typecheck, and the model read back.**
`cd apps/ui && npx tsc --noEmit` → exit 0, NO output. Verbatim output: (empty).
That matches the reviewer's base reading exactly, so this round contributed
nothing. Re-run after C4 as `npm run typecheck` (script body `tsc --noEmit`) →
exit 0, no output beyond the two npm banner lines.

The four-card read-back is reported from ASSERTED tests rather than from an
ad-hoc script — see the deviation below for why. The describe block
"the T003a read-back the block's G6 orders" in `decisionCard.test.ts` builds
each card through `buildDecisionCardModel` and asserts exactly these tuples;
all four assertions pass in every green run reported under G7, and each fails
under the mutation that would break it.

Card A — two options, two KEYED outcomes:
- `answers` (kind, value, expectedOutcome, downside):
  `("option", "retry", "The export job runs again", "Costs another ten minutes")`,
  `("option", "skip", "The pipeline moves on", "The export stays stale")`
- `evidenceRefs` (kind, target, label):
  `("test_run", "tr-9", "Test result for the export job")`
- `evidenceNote`: `""`

Card B — one UNKEYED outcome, two next actions:
- `answers`:
  `("command", "remedy resume", "The run continues under the raised budget", "Spends more than planned")`,
  `("command", "remedy abort", "The run continues under the raised budget", "Spends more than planned")`
- `evidenceRefs`: none
- `evidenceNote`: `""`

Card C — NO triple at all:
- `answers`: `("option", "approve", "", "")`, `("option", "reject", "", "")`
- `evidenceRefs`: none
- `evidenceNote`: `"Recorded before receipts were required."`

Card D — a blank-target ref beside a valid one:
- `answers`: `("option", "approve", "", "")`
- `evidenceRefs`: `("escalation", "td:1", "Escalation raised by the worker")`
  — the `stop_record` ref whose target was `"   "` is DROPPED
- `evidenceNote`: `"Recorded before receipts were required."`

**G7 — the model's tests, green then red.** Every run below is the command
`vitest run src/api/decisionCard.test.ts` (plus the worktree flags where
stated), reached through `npm run test:unit --`, which echoes its script body in
the transcript. Runs were serial; never two test processes at once.

| Run | exit | count line |
|---|---|---|
| PRIMARY checkout at C4 | 0 | `Test Files 1 passed (1)` / `Tests 80 passed (80)` |
| WORKTREE control, unmutated | 0 | `Test Files 1 passed (1)` / `Tests 80 passed (80)` |
| mutation (a), unkeyed fallback removed | 1 | `Test Files 1 failed (1)` / `Tests 2 failed \| 78 passed (80)` |
| mutation (b), blank-target drop removed | 1 | `Test Files 1 failed (1)` / `Tests 3 failed \| 77 passed (80)` |
| mutation (c), `scrubUiText` replaced by the raw label | 1 | `Test Files 1 failed (1)` / `Tests 2 failed \| 78 passed (80)` |
| WORKTREE control again, after all three restorations | 0 | `Test Files 1 passed (1)` / `Tests 80 passed (80)` |

Worktree recipe used, exactly as constraint 9 orders: run from the PRIMARY
checkout's `apps/ui`, with
`--root /home/decodeux/Repos/remedy/.remedy-wt/r13mut/apps/ui` and
`--config /home/decodeux/Repos/remedy/apps/ui/vitest.config.ts`, SCOPED to
`src/api/decisionCard.test.ts`. Vitest confirms the root in its banner:
`RUN v2.1.9 /home/decodeux/Repos/remedy/.remedy-wt/r13mut/apps/ui`.

Every mutation was applied to the FILE
`.remedy-wt/r13mut/apps/ui/src/api/decisionCard.ts`. Each exact byte string was
counted IN THAT FILE before it was applied and the count was `1` in all three
cases; each was restored byte for byte before the next was applied. The
worktree's `git status --porcelain` was EMPTY after the restorations
(`wc -l` → `0`).

The failures name the right things. (a) → `applies ONE unkeyed outcome to EVERY
next-action answer of the card`, expected the budget sentence, received `''`.
(b) → `DROPS a ref whose target is blank after trimming`, the `stop_record` ref
with target `"   "` survives. (c) → `shows the fallback for a label that is a
bare hex id`, `expected 'a3f9c2e1b4d7' to be 'Receipt'` — the raw id reaches the
model, which is precisely the leak S2 exists to prevent.

**G8 — the guards, the canary and the PR gate.**
`python3 -m pytest tests/ui_contracts/ -q` → exit 0, `566 passed, 4 skipped in
5.60s`. That equals the reviewer's base reading exactly, so no other reading is
owed an explanation. `python3 -m pytest tests/cli/test_golden_path.py -q` →
exit 0, `42 passed in 20.73s`.

`git diff --name-only 4b1b2e99..8694120b` →
`.agent/authored/f032-r13.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `apps/ui/src/api/decisionCard.test.ts`,
`apps/ui/src/api/decisionCard.ts`. Against the Change set less
`.agent/handoff.md`: residue changed−ordered `[]`, residue ordered−changed `[]`
— BOTH EMPTY.

`git diff --stat 4b1b2e99..8694120b -- packages/` → `''` EMPTY. Same for
`-- tests/` → `''` EMPTY. Same for `-- docs/` → `''` EMPTY.
`git diff --name-only 4b1b2e99..8694120b -- 'apps/**/*.tsx' 'apps/**/*.css'` →
`''` EMPTY.

| Commit | insertions | parents | under 500 |
|---|---|---|---|
| `7f1da6e6` | +321 | 1 | TRUE |
| `3bc7141f` | +252 | 1 | TRUE |
| `03c6b9be` | +23 | 1 | TRUE |
| `92ebbc4f` | +2 | 1 | TRUE |
| `5284ba66` | +225 | 1 | TRUE |
| `8694120b` | +407 | 1 | TRUE |

Marker counts, each 0 as required, against a non-zero CONTROL:

| File | `^<<<SLICE ` | `^<<<END ` |
|---|---|---|
| `.agent/plan.md` | 0 | 0 |
| `.agent/live_review.md` | 0 | 0 |
| `apps/ui/src/api/decisionCard.ts` | 0 | 0 |
| `apps/ui/src/api/decisionCard.test.ts` | 0 | 0 |
| CONTROL: committed C0a blob | 2 | 2 |

`git ls-files .remedy-wt` → 0 lines. `git worktree list` → 1 line.
`git branch --list "tmp/*"` → 0 lines.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
Nothing merged, nothing created.

## Authored-text proofs

Two reviewer-authored slices were applied, plus the block itself.

- The BLOCK: `.remedy-wt/f032-r13.md` → committed `.agent/authored/f032-r13.md`
  → committed `.agent/last_block.md`. Disk-to-disk sha256 equal across all
  three (G2), and C0a/C0b are the same git blob `755261e8`.
- `PLANF032R13` → `.agent/plan.md`: byte-equal under constraint 2's convention
  (G4), with the no-trailing-newline negative control FALSE.
- `LEDGER13` → `.agent/live_review.md`: byte-equal as base + one newline +
  slice, proved by two independent readers, both of which reject a single
  flipped byte in the first appended paragraph (G5).

## Deviations & assumptions

1. **G7's ordered command could not be run verbatim; an equivalent was used and
   is declared.** `npx vitest run src/api/decisionCard.test.ts` is DENIED by
   this session's permission sandbox, as are `npx vite-node` and
   `node node_modules/vitest/vitest.mjs`. Every G7 run therefore went through
   `npm run test:unit -- <args>`, which is allowed. This is not a weaker gate:
   npm echoes the resolved script body into the transcript, so each run shows
   `> vitest run src/api/decisionCard.test.ts` (with the worktree flags where
   they apply) above its own result. Same binary, same arguments, same working
   directory.
2. **G6's read-back is reported at C4, not at C3, and from assertions rather
   than from a print.** The block orders the four cards' values reported "at
   C3". Producing them at C3 needs an ad-hoc TypeScript runner, and both
   available ones (`vite-node`, the vitest node entrypoint) are denied by the
   sandbox as above. The values are instead ASSERTED in `decisionCard.test.ts`
   and reported from the C4 run. The reported values are the model's behaviour
   at C3 unchanged: C4 touches only the test file, so `decisionCard.ts` is
   byte-identical at `5284ba66` and `8694120b`. This is arguably the stronger
   form — a read-back that the suite re-runs rather than a transcript a reader
   must trust — but it IS a departure from the ordered commit at which the
   measurement was to be made, so it is recorded here.
3. **No visual change, and nothing is owed to an assumption_log.** Stating
   constraint 12 plainly: this round adds no component, no element, no class and
   no token. It touches no `.tsx` and no CSS — proved EMPTY under G8. The
   canonical design reference therefore imposes no visual decision on this
   round, and NOTHING is owed to an assumption_log. The next round, T003b, is
   the one it binds.
4. **No slice was edited.** Both slices were applied byte for byte from the
   COMMITTED C0a blob rather than retyped, and neither looked wrong.
5. **The ordered commit sequence was followed exactly** — C0a, C0b, C1, C2, C3,
   C4, C5, in that order, with no commit between them and no extra commit. C2 is
   the only commit touching `.agent/live_review.md`.
6. **One naming choice the spec left to me.** S3 says to pass "a fallback of
   your choosing that reads as a receipt"; the chosen word is `Receipt`, held in
   `EVIDENCE_REF_FALLBACK_LABEL`. S5's sentence is likewise mine:
   `Recorded before receipts were required.` Both are asserted by name in the
   tests, so a reword is a visible change rather than a silent one.
7. **S4's unkeyed rule was implemented on its literal wording** — the fallback
   applies when the card carries exactly one outcome whose `option` is the empty
   string, found by filtering for that key rather than by requiring the card to
   carry exactly one outcome in total. The two readings coincide on every shape
   the eight producers emit, since rule (h) emits exactly one outcome and keys
   it `UNKEYED_OPTION`.

## Next

1. **Phase 1 rule 1 of docs/agents/self_drive_protocol.md, before anything
   else: re-read `.agent/STOP` FROM DISK.** It is one-shot at Phase 0 but binds
   at any point; never delete the sentinel.
2. Then the Open PR Gate:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then **T003b: the card component projects what this round's model now
   carries** — chips for `evidenceRefs`, and each option's `expectedOutcome` and
   `downside` under its own answer. That is the round which touches `.tsx` and
   CSS, so it IS bound by the canonical design reference, and it must FIRST read
   the source-counting guards in
   `tests/ui_contracts/test_decision_answer_wiring.py`.
