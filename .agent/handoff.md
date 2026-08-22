# Handback — F009 R30 (closure preparation)

Fortschritt: ~99 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN: Branch-only-Menge leer, alle sechs
             Base-only-Ids per Einzelbeweis der Umgebung zugeordnet; offen
             bleiben nur die zwei Closure-Runden) — Schätzung

## Range
Review of `bcf295f951957ebdf0047fba315b344b1a2ce212`..HEAD — that SHA is the
round base, read at step 0.

## Commits
### e46e5d0c chore(state): save the F009 R30 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r30.md | 303/0 | C0a — transport copy of the emitted block |
### 1cabcfd5 chore(state): mirror the F009 R30 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 204/172 | C0b — written from the committed C0a blob |
### 41bdb583 docs(state): point the F009 plan at closure preparation
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 12/11 | C1 — PLANF009R30 slice, byte-equal |
### 55504d45 docs(review): register R-0645 against the integration gate inference
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — FINDING645 appended on the round base |
### 146d02a8 docs(review): record the R29 and integration gate verdicts
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C3 — LEDGER30 appended on **C2** |
### cc82ab44 docs(agents): make the parity check measure the rebuild event
| Path | +/- | Reason |
|---|---|---|
| docs/agents/integration_gate.md | 8/3 | C4 — the GATEDOC FROM/TO rewrite |
### d8d48b7f docs(roadmap): record the F009 built state
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F009.md | 59/0 | C5 — BUILTSTATE appended on the round base |
### C6 (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | C6 — this file; its numbers are in the round report |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |

## External actions
`git push -u origin feature/f009-single-write-channel` after C6; outcome in the
round report. One worktree, none added or removed. No `gh` command. NO pull
request created: F009 opens one at its own closure.

## Verification
Transcripts are in the round report (R-0582); one line per gate here.
- G1 PASS — STOP absent before C0a and before C6; branch correct; `git status --porcelain` 0 lines after each of C0a…C5.
- G2 PASS — emitted original, C0a and C0b all sha256 `8af694b2…24df7d`, 28915 bytes, 303 lines; disk-to-disk, negative control differs.
- G3 PASS — 6 slices, 111 CONTENT lines, from the committed C0a blob; TOTAL 303, PROSE 192 — constraint 9 reproduced.
- G4 PASS — `cmp` exit 0 against PLANF009R30, control exit 1; 40 lines vs the 50 cap; `^## Goal$` 1, `^## Next Steps$` 1.
- G5 PASS — all three appends ACCEPT under both readers and REJECT the equal-length flip; N counted 1, 1 and 4.
- G6 PASS — base entries 210, `Done:` 3, `Landed: ` 0, `Gate: R` 29/29 distinct, `Gate: R30` 0, `- R-0645` 0, max R-0644, open 207.
- G7 PASS — REWRITE confirmed; FROM 1→0 and TO 0→1, whole-line and indent-agnostic agreeing at both points.
- G8 PASS with a WEAK CLAUSE — numstat 8/3; the 18-line span reads as one sentence sequence; `^## ` is 0 at base AND at C4 (see Deviations).
- G9 PASS — `tests/docs/` exit 0, 295 passed; `tests/cli/test_golden_path.py` exit 0, 42 passed; run serially in the primary checkout.
- G10 PASS — declared path set matches, both differences empty; 0 `packages/` `apps/` `tests/` paths; every commit 1 parent; numstat agrees; 0 marker LINES; `git ls-files .remedy-wt` 0; amend/rebase/cherry 0.
- G11 — this file; its `wc -l` is in the round report.

## Authored-text proofs
The emitted original is still on disk at `.remedy-wt/f009-r30.md`, so this is a
real disk-to-disk comparison, not a recorded digest: `filecmp(shallow=False)` is
True for original↔C0a, original↔C0b and C0a↔C0b — all three sha256
`8af694b228cc5d3e10c0a1cb233c5ae9490962481be9f8289a00690be724df7d`, 28915 bytes,
303 lines — and False against `AGENTS.md` as control; both committed blobs re-read
to that digest. Every slice came out of the committed C0a blob by its marker
lines, applied by script; none was retyped.

## Deviations & assumptions
- NO departure from the ordered sequence C0a…C6: none extra, dropped or reordered.
- G8's `^## ` clause is SATISFIED BUT VACUOUS, for the reviewer to rule on:
  `docs/agents/integration_gate.md` has no `## ` heading at all, so the count is 0
  at the round base and 0 at C4 and the clause could not have gone red.
- G6's max-id reading does not discriminate this round — an unanchored scan at C3
  also reports R-0645. Anchoring shows elsewhere: unanchored sees 271 ids where 211
  are registered (60 never registered) and 32 `Gate: R` strings against 30 keys.
- Assumption: "no marker reaches a target file" is read LINE-anchored, as G10
  words it. LEDGER30 legitimately QUOTES `<<<SLICE ` and `<<<END ` twice mid-line;
  a substring guard would have made that slice unappliable.

## Next
The reviewer rules on R30; then the first closure round — the evidence job and a
FRESH review zip, whose values the later STATUS line quotes.
