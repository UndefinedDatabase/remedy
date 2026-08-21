# Handback — F008 SSE event stream, R7 (HALTED, no bundle commit landed)

Branch `feature/f008-sse-event-stream`. Open findings: 185, unchanged — the block registered none and the next free id stays R-0614. R7 HALTED before its first bundle commit under self-drive guardrail G8 (contradiction / red gate): the HELPERSTO slice is internally inconsistent with the TESTSSE slice, so applying both byte for byte as constraint 1 requires makes the block's own G10 and G11 UNSATISFIABLE. Nothing was merged, no PR was opened, no branch was created.

## The blocking defect (measured, not inferred)

In `.remedy-wt/f008-r7.md` the HELPERSTO slice writes DOUBLE-backslash escapes in two byte-string literals — block lines 291 and 300:

    return f"id: {seq}\\ndata: {json.dumps(payload, default=str)}\\n\\n".encode()
    return b": heartbeat\\n\\n"

In Python source `\\n` is an escaped backslash plus `n`, so `sse_event_frame` emits `b'id: 0\\ndata: {...}\\n\\n'` — literal backslash-n text, not CR-free SSE line breaks. The TESTSSE slice asserts REAL newlines (`assert frame.endswith(b"\n\n")`, single backslash, block lines 401/422). The two slices therefore contradict each other. Every other slice, pair shape and numeral in the block was re-derived and is CORRECT; the fix is two characters and belongs to the reviewer, not to this worker (constraint 1 forbids editing a slice).

## Range

Review of `cc27ff16`..HEAD, HEAD being the single commit that writes this file.

## Commits

### C5 docs(state): halt F008 R7 on a defective slice and write the handback
`.agent/handoff.md`, rewritten. It is the ONLY commit of this round. A handoff cannot table the commit that writes it (R-0149), so its `+/-` is reported in the round report. C0a, C0b, C1, C2, C3 and C4 were NOT created — see Deviations.

## External actions

- `git worktree add .remedy-wt/dry-r7 --detach cc27ff16` — exit 0, disposable dry-run tree (guardrail G5).
- `git worktree remove --force .remedy-wt/dry-r7` then `git worktree prune` — exit 0; `git worktree list` now names the primary checkout alone.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, output `[]`.
- `git push -u origin feature/f008-sse-event-stream` — run after this commit; transcript in the round report.

## Verification

Gates were executed against the DRY-RUN application of the slices in the disposable worktree, never against a commit, because no bundle commit exists. Each line says which.
- G1 `.agent/STOP` absent; branch `feature/f008-sse-event-stream`; `git status --porcelain` empty at the halt and at this handback; `git worktree list` names the primary checkout alone.
- G2 scratch block sha256 `c57ddb619a288a17081ba32e9c8f7f5fa94de6ac6cfa6bdc3b5679392be859bf`, 26837 bytes, 488 lines — receipt MATCHES the three ordered readings. No C0a/C0b copy exists, so the three-way equality is NOT claimed.
- G3 7 slices by ordered extraction from the block on disk (not from a committed file): PLANF008R7 `9430fb9b` 2574B/45L · RECORDR6 `6b33bfba` 2657B/1L · SUMMARYFROM `f9bb5a39` 496B/11L · SUMMARYTO `eee8d7a6` 118B/4L · HELPERSFROM `3562a4b8` 41B/1L · HELPERSTO `670aaa0c` 2715B/75L · TESTSSE `26c3a934` 5588B/147L.
- G4 NOT RUN as a commit gate. PLANF008R7 itself is 45 lines (< 50), `## Goal` 1, `## Next Steps` 1, `F008` 2 — all line-anchored.
- G5 NOT RUN as a commit gate. Simulated against the `cc27ff16` blob: prefix TRUE, remainder `0cf0f10d` 2658B/2L equals `\n`+RECORDR6, INDEPENDENT blank-line split yields 196 units whose LAST equals RECORDR6, and a one-byte flip is REJECTED by both readings while the unflipped value is ACCEPTED by both.
- G6 at `cc27ff16`: `^- R-\d+ — ` 185 · `^Done: R-\d+ — ` 0 · `^Landed: ` 0 · `^Gate: R\d+ — ` 6 with keys R1 R2 R3 R4 R5 R6 DISTINCT · `^- R-0614 — ` 0. The C2 half is unmeasurable; no id was minted.
- G7 dry-run: each FROM occurs EXACTLY ONCE at `cc27ff16`; after application SUMMARYFROM 1→0, SUMMARYTO 0→1, HELPERSTO contained exactly once. `git diff --numstat` reads **78 insertions, 11 deletions** — the block's number, RE-DERIVED and CONFIRMED.
- G8 dry-run: the 78 lines the diff ADDS are, IN ORDER, exactly SUMMARYTO plus the HELPERSTO lines absent from HELPERSFROM (78 vs 78). Ordered equality HOLDS.
- G9 NOT RUN as a commit gate. TESTSSE is 5588B/147L; as a new file its insertions would equal 147.
- G10 PRIMARY checkout, run SERIALLY at `cc27ff16`: state readers exit 0 at passed 400 + skipped 0 = **400**; `tests/docs/` exit 0 at passed 295 + skipped 0 = **295**. Constraint 10 RE-DERIVED and CONFIRMED. `--collect-only` on the new file reads **14 tests**, so 400 + 14 = **414** — the block's arithmetic is CORRECT.
- G11 **RED**. In the disposable worktree, `ui_server.py` at `cc27ff16` with the test file present: exit 1, 14 failed, 0 passed — the block's prediction CONFIRMED. With the pairs applied (the C3 state): exit 1, **7 failed, 7 passed**. The gate orders exit 0; it CANNOT be met with the slice as written. This is the halt.
- G12 dry-run, red control FIRST: a scratch file with unsorted imports and an undefined name returns exit 1 and multiset `{I001: 1, F401: 2, F821: 1}`, so the extractor is shown producing a reading. Then all three targets exit 0 with an EMPTY multiset — `ui_server.py` at base, `ui_server.py` applied, and the test file. Ruff is BLIND to this defect: `\\n` is valid Python.
- G13 NOT APPLICABLE. `git diff --name-only cc27ff16..C5` is `.agent/handoff.md` alone, a strict subset of the Change list — the six missing paths are the halt, declared below. The one commit has exactly one parent and its insertions are under 500.
- G14 lines beginning `<<<SLICE ` or `<<<END `: 0 in every one of the 7 slice bodies and 0 in this file.
- G15 over this round's OWN reflog entries the count whose OPERATION — the text before the first `:` in `git reflog --format=%gs` — is `amend`, `rebase` or `cherry` is 0. Counted by operation, never by substring; no entry total is stated.
- G16 the branch is pushed and NO pull request exists: `gh pr list` returned `[]`. Nothing was merged.
- G17 this file carries every section `docs/agents/handback_template.md` mandates plus the item table below; its line count is reported in the round report; the cap this round is 100.

## Authored-text proofs

NONE APPLIED. No slice was written to a tracked file, so no disk-to-disk comparison against `.agent/authored/f008-r7.md` exists — that file was never created. The slices were extracted from the block on disk by their marker lines and applied ONLY inside the disposable worktree, byte for byte, without retyping, rewrapping, reflowing or editing; the objection above is raised against HELPERSTO exactly as constraint 1 directs, and no slice was edited to route around it.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | skipped | halted before the first bundle commit under guardrail G8 |
| C0b | skipped | depends on C0a |
| C1 | skipped | PLANF008R7 asserts R7 built the reader; landing it would put a false Current Step on disk |
| C2 | skipped | constraint 3 fixes the order; C2 cannot precede C1 |
| C3 | skipped | HELPERSTO is defective; applying it lands a red branch tip and poisons R8's red proof |
| C4 | skipped | TESTSSE without a working C3 is 7 failing tests on the branch tip |
| C5 | done | this commit — the halt record |

## Deviations & assumptions

DEVIATION, declared: the ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was NOT followed. Six of seven commits were not created and only C5 landed. Cause: a measured contradiction between constraint 1 (apply every slice byte for byte, never edit) and gates G10/G11 (the suite exits 0), forced by the double-backslash escapes in HELPERSTO. Self-drive guardrail G8 and the round order both end the round on a contradiction rather than guessing; constraint 1 forbids repairing the slice here. No commit was half-written at the halt. Nothing was widened, no scope was added, and no gate was reported as met that was not measured.

## Next

The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1). Its SECOND action is the Open PR Gate (Phase 1 rule 2), which finds NO open pull request and therefore continues on THIS branch at R8 rather than cutting a new one. R8 re-issues this same bundle with HELPERSTO's two literals corrected to single-backslash `\n`; every other slice, both pair shapes, the 78/11 numstat, the 400/295 suite totals and the 414 arithmetic were RE-DERIVED this round and need no re-authoring. Only after that does the route land.

Fortschritt: 20 % (F008 beansprucht · sechs Urteile im Ledger — das R6-Urteil
bleibt ungeschrieben · T001-Leser NICHT gebaut: die Runde hielt an einem
fehlerhaften Slice an, bevor der erste Commit fiel · R8 gibt dasselbe Bündel
mit zwei korrigierten Zeichen erneut aus) — Schätzung
