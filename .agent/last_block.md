── STEP R11/n — F280 ────────────────────────────────────
Goal: book round 10's independently-reviewed PASS (Gate: F280 R10, one prose slip, no new
R-id), and author DECISION F280 D6, naming the persisted-literal spellings the second half of
DECISION F280 D5's rename needs. This round is DECISION-ONLY — no file under `apps/`,
`packages/`, `tests/`, or `scripts/` changes; only `.agent/` prose carriers and one feature-file
amendment move.

Bundle:
  1. Copy this block to `.agent/authored/f280-r11.md` and mirror to `.agent/last_block.md`.
  2. Append the Gate:F280 R10 entry to `.agent/live_review.md`, append the prose-slip line to
     `.agent/prose_slips.md`, append DECISION F280 D6 to `.agent/decisions.md`, insert the
     feature-file amendment into `docs/roadmap/features/T2_F280.md`, and replace `.agent/plan.md`
     — all five pre-built and pre-verified by the reviewer.
  3. Run the done-when gates, write the handoff, commit, push.

Change — exact files, exact source:
  All five source files below live under `/home/decodeux/Repos/remedy/.remedy-wt/` (repo-root
  scratch, NOT a git ref — plain files on disk in the primary checkout's own working tree).
  Copy each BYTE-FOR-BYTE with `shutil.copyfile` or equivalent; do not retype.

  (a) `.agent/live_review.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/gate_r10_entry.txt` (sha256
           `d0b7a869251e57fa3a305602746593a6f1d896328455357ed458d7e69cd2c7ce`, 4583 bytes,
           already ends in its own single `\n`)
      i.e. `new_bytes = old_bytes + b"\n" + gate_r10_entry`. There is no new R-id to register.
  (b) `.agent/prose_slips.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/prose_slip_r10.txt` (sha256
           `cb473c01b4f2db0a30ef6a35777962614a5ae7e7a867c03456dc26b7fecad733`, 412 bytes,
           already ends in its own single `\n`)
  (c) `.agent/decisions.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/decision_f280_d6.txt` (sha256
           `ce7db4b956bc5c6f4639db5dc56c77ac26e571341762aa657505a3435124eac6`, 6464 bytes,
           already ends in its own single `\n`)
  (d) `docs/roadmap/features/T2_F280.md` — INSERT the exact bytes of
      `.remedy-wt/t2_f280_amendment.txt` (sha256
      `b195259cce88ee9f23b1a2f073775c0285d85a61390886996eb00a35ab0baa04`, 895 bytes, starts with
      its own leading `\n` and ends in its own single trailing `\n`) immediately after the
      byte sequence ending `...with no\noperator-facing heir.\n` (the end of DECISION F280 D5's
      amendment paragraph) and immediately before the pre-existing blank line that precedes the
      `## T002` heading. Locate the exact splice point yourself by reading the file — do not
      guess a line number; the insertion is `prefix + amendment_bytes + suffix` where `prefix`
      ends in `operator-facing heir.\n` and `suffix` begins with the existing blank line then
      `## T002 — Descriptions, role labels, help wrapping, tests`.
  (e) `.agent/plan.md` — REPLACE THE WHOLE FILE with the exact bytes of
      `.remedy-wt/f280-r11-plan.md` (sha256
      `7d1127891876f42bbc9d4baeeb3c77fde30f68582af9f127522c6d9c3f1372b5`, 2534 bytes, 44 lines).

Constraints:
  - Do not touch any file this block does not name. In particular: no file under `apps/`,
    `packages/`, `tests/`, or `scripts/` changes this round — if your own diff shows one, STOP,
    that is a block condition.
  - Do not edit DECISION F280 D5's own paragraph, or any other existing paragraph in
    `.agent/decisions.md` or `T2_F280.md` — this round only APPENDS/INSERTS.
  - Commit order: C0a (authored carrier) -> C0b (last_block mirror) -> C1 (all five
    appends/inserts (a)-(e), ONE commit) -> C2 (handoff). Do not split C1 further — the total
    is 6464+4583+412+895+(plan.md delta) bytes, far under the 500-line insertion cap by any
    reasonable line count.
  - `git status --porcelain` empty before your first commit and after your last.

Done when (run every command from the repo root, primary checkout):
  G1 TRANSPORT — five digest/byte comparisons: `sha256sum .agent/authored/f280-r11.md` equals
     `sha256sum .agent/last_block.md`; `cmp` each of the five source files under `.remedy-wt/`
     against the corresponding section it produced in the committed target (for (d), `cmp` the
     inserted span, not the whole file) — report PASS/FAIL, not a re-typed diff.
  G2 THE RECORD — after C1:
     `python3 -c "import re; d=open('.agent/live_review.md').read(); print(len(re.findall(r'^Gate: F\d+ R\d+ — ', d, re.M)), len(set(re.findall(r'^- (R-\d{4}) — ', d, re.M))), len(set(re.findall(r'^Done: (R-\d{4}) — ', d, re.M))))"`
     must read exactly `37 136 7` (unchanged open/done — no new finding). `grep -c "^## DECISION F280 D" .agent/decisions.md` must read `6`. `wc -l .agent/prose_slips.md` must read one more line-count than base (a single-paragraph append). `.agent/plan.md` must be exactly 44 lines with exactly one `## Goal`, one `## Current Step`, one `## Next Steps` and one `## Risks`.
  G3 THE SPLICE — after C1, `git diff --numstat HEAD~1..HEAD -- docs/` reads exactly
     `docs/roadmap/features/T2_F280.md` with `11` insertions and `0` deletions (a pure insert,
     no line touched or removed); `git diff HEAD~1..HEAD -- docs/roadmap/features/T2_F280.md`
     shows the new paragraph landing between D5's amendment and the `## T002` heading, with
     every other line of the file unchanged.
  G4 THE BOUNDARY — after C1, confirm no other file changed:
     `git diff --stat HEAD~1..HEAD` reads exactly five paths — `.agent/live_review.md`,
     `.agent/prose_slips.md`, `.agent/decisions.md`, `docs/roadmap/features/T2_F280.md`,
     `.agent/plan.md`.
  G5 DOCS SUITE — `python3 -m pytest tests/docs/ -q` reads `310 passed` (unchanged — this round
     adds a decision paragraph, not a new command, group or catalog claim).

Handback: completion report (state block, deviations, next steps) + rewrite
`.agent/handoff.md`. Attribute commits `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
Session number: this is SESSION 5 of F280, round 11.
──────────────────────────────────────────────────────────────
