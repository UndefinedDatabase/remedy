── STEP T-CLOSURE/1 — F111 Diff-only repair · Round 22 ───────────────
Goal:        Close F111 under docs/roadmap/STATUS_closure_protocol.md: record
             the R21 integration-gate verdict, make the feature file current,
             build the evidence job and a FRESH review zip, apply the authored
             STATUS line, and open the PR without merging it.
Bundle:      C1a save this block · C1b mirror it · C2 record the R21 gate and
             resolve R-0319 · C3 feature-file Built State · C4 evidence job ·
             C5 review zip · C6 closure commit · C7 push + PR
Change:      EXACTLY these paths:
               .agent/authored/f111-r22-1.md   (new, C1a)
               .agent/last_block.md            (rewrite, C1b)
               .agent/live_review.md           (C2: one pair + one append)
               docs/roadmap/features/T2_F111.md (C3: one appended section)
               docs/roadmap/STATUS.md          (C6: one line)
               README.md                       (C6: one line)
               .agent/plan.md                  (C6: full rewrite)
               .agent/candidates.md            (C6: full rewrite)
               .agent/handoff.md               (C6: full rewrite)
             NO source file and NO test changes this round. The evidence dir is
             NEVER committed.
Constraints:
  - TEXT-A … TEXT-G are AUTHORED text. Apply them byte for byte. Do not reword,
    rewrap or re-punctuate. If one looks wrong, apply it anyway and report it as
    a declared deviation. TEXT-D carries three <PLACEHOLDER> slots and is the
    ONLY authored text you substitute into; substitute nothing else anywhere.
  - Do NOT write a `Done:` paragraph of your own. This round's authored `Done:`
    text is TEXT-A and it resolves the only unreviewed-fix marker on disk.
  - C1 is SPLIT into two commits on purpose (authored file, then last_block):
    combined they exceed the AGENTS.md 500-insertion cap.
  - The evidence dir lives under `.remedy-wt/` (gitignored) — NEVER inside the
    tracked tree and NEVER `/tmp` (writes there are denied on this machine). A
    pre-committed evidence dir puts evidence files into the base..HEAD review
    subject and the package builds BLOCKED_EVIDENCE.
  - The zip is built from a CLEAN tree after ALL content commits (C1-C5) and
    BEFORE the closure commit C6. A package built from a dirty tree is invalid.
  - A failing zip build is a closure BLOCKER: do not close, do not invent a
    package name, record the raw error in the handoff and hand back. Same for a
    failing `remedy integrity check`.
  - The STATUS edit is the LAST content of the closure commit C6, and C6 touches
    exactly the five paths listed for it — README and STATUS may never disagree
    in any committed state.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding.
  a. `cmp .agent/authored/f111-r22-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2, in `.agent/live_review.md`: `grep -c '^Done:'` prints 13,
     `grep -c '^Landed:'` prints 0, `grep -c '^### R21 — PASS'` prints 1,
     `grep -c '^- R-0'` prints 44 (this round registers nothing).
  c. The R-0319 fix is proved SCOPED, not file-wide. Extract the `### R19 —
     PASS` entry — from its heading up to but excluding the next line starting
     `### ` — and count inside that slice only: `are byte-identical` 0 times,
     `WERE byte-identical` 1 time. Record both numbers and the slice's line
     count. Do NOT count over the whole file: fifteen earlier entries carry the
     phrase legitimately and the R-0319 bullet quotes it on purpose.
  d. After C3: `python3 -m pytest tests/docs/ -q` — record the tail and exit
     code (the change set includes docs/roadmap/**, so this gate is mandatory).
     Also `grep -c 'diff-only-repair-v1.md' docs/roadmap/features/T2_F111.md`
     prints 1.
  e. `remedy integrity check --json` → PASS, with no relevant untracked files.
     Record the real JSON verdict. If it is not PASS, STOP and hand back.
  f. Evidence job: use the canonical producer
     `packages.orchestration.job_evidence.create_manual_completion_bundle`
     with `review_feature_id='f111'` and the job id `f111-closure`. READ that
     module before calling it — do not guess its signature. Honour the four
     producer pitfalls the closure protocol lists: sha256-hex `output_hash`,
     valid VerificationTests totals, FULL-LENGTH base_commit SHA, non-empty
     node ids with `len(node_ids) == selected` taken from a real
     `--collect-only`, `test_files` entries that are FILES and never
     directories, and a `run_id` matching `^vr-\d{4,}$`. Never record a
     FULL-SUITE node-id list — record the clean SCOPED suites
     (`tests/orchestration/test_diff_repair.py`,
     `test_diff_repair_apply.py`, `test_diff_repair_response.py`,
     `test_builder_repair_loop.py`) and let the full-suite proof ride in the
     committed `.agent/gate_f111_r21/` evidence. Record the real job id.
  g. Review zip: `bash scripts/make_review_zip.sh --evidence-dir <path>` from a
     clean tree. Record the package filename, its SHA-256, and confirm the
     manifest's `committed_review_subject` spans BASE..HEAD with
     BASE = 4e0b762e and HEAD = the head at zip time. Record that head SHA in
     FULL — it is the `accepted HEAD` value.
  h. C6 substitutions, and only these three, into TEXT-D:
       <PACKAGE>       → the package filename from (g)
       <SHA256>        → its SHA-256 from (g)
       <ACCEPTED_HEAD> → the full 40-char head SHA from (g)
     Then prove the applied STATUS line is byte-identical to the authored text
     outside those three slots, and that exactly ONE line in
     `docs/roadmap/STATUS.md` starts `- [x] F111 — ` and ZERO start `- [~]`.
  i. README/STATUS agreement: `grep -c '^- \[x\] F[0-9][0-9][0-9] — ' docs/roadmap/STATUS.md`
     prints 44, and README.md's "N of 255 registered items accepted." line reads
     44. Both land in the SAME commit (C6).
  j. After C6: `python3 -m pytest tests/docs/ -q` again — the ledger pins read
     both files and this is the commit that could break them. Record tail and
     exit code. Then `python3 -m pytest tests/cli/test_golden_path.py -q`.
  k. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real number.
     Do not pad or trim the authored text to hit a count.
  l. `git status --porcelain` empty, `git diff --name-only 35329dec..HEAD`
     lists only the ordered paths (and NO evidence dir, NO zip),
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     prints 0 and 0 after the final push.
  m. C7: `gh pr create` targeting main from this branch. Record the PR number
     and URL. Do NOT merge it. Do NOT mark it draft.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C1a, C1b, C2, C3, C4, C5, C6, C7 — each exactly once), commit table
           with real SHAs and insertions, changed-files table, every result a-m
           as a REAL value, and the grep proof (h) that the applied STATUS line
           matches the authored one. Repeat the Fortschritt line verbatim. Over
           60 lines ⇒ carry a "Deviations, declared" line naming the count and
           the mandated content that caused it (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f111): save the R22 step block verbatim` — write the block bytes to
    `.agent/authored/f111-r22-1.md`.
C1b `chore(f111): mirror the R22 block into last_block` — copy that file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f111): record the R21 integration gate and resolve R-0319`
    Two edits to `.agent/live_review.md`, in this order: apply the TEXT-A pair
    (REWRITE: the single `Landed: R-0319 …` line at the end of the file becomes
    the authored `Done: R-0319 …` line), then append TEXT-B after it. Run gates
    (b) and (c).

C3 `docs(f111): record the shipped shape in the feature file`
    Append TEXT-C to the END of `docs/roadmap/features/T2_F111.md`, after the
    D6 section, separated by one blank line. Run gate (d).

C4 (no commit) Evidence job per gate (f). The evidence dir goes under
    `.remedy-wt/`. Nothing from it is committed, now or later.

C5 (no commit) Review zip per gate (g), from the clean tree at the C3 head.

C6 `chore(f111): close F111 in the ledger`
    ONE commit touching exactly `docs/roadmap/STATUS.md`, `README.md`,
    `.agent/plan.md`, `.agent/candidates.md`, `.agent/handoff.md`:
      - STATUS: replace the single `- [~] F111 — Diff-only repair` line with
        TEXT-D, substituted per gate (h). Touch no other STATUS line.
      - README: apply the TEXT-E pair.
      - `.agent/plan.md` ← TEXT-F in full. `.agent/candidates.md` ← TEXT-G in
        full. `.agent/handoff.md` ← your own rewrite.
    Run gates (h), (i), (j), (k).

C7 Push, then `gh pr create` per gate (m). Title:
    `F111 — Diff-only repair (T001-T003, closure)`
    The body carries: what changed and why; the key decisions (F111 D1, D3, D6,
    D9) each in one line; how to review (the ist-doc first, then
    `.agent/gate_f111_r21/attribution.txt`); a changed-files summary; the latest
    verdict (R21 PASS, integration gate green relative to base); the
    open-findings count (32, none High, each an accepted risk); and the runtime
    actuals you can observe (rounds, wall clock) with `not-measured` wherever
    the ledger has no number — never a guess. The body says in one line that the
    saving is measured in CHARACTERS, not tokens. Do NOT merge.

TEXT-A — one REWRITE pair for .agent/live_review.md
  FROM (the single last line of the file, whatever its exact wording, which
  begins `Landed: R-0319 —`). TO (1 line):
Done: R-0319 — the `### R19 — PASS` transport sentence now reads "WERE byte-identical at the R19 gate" and says why `last_block.md` has moved on, so a later reader cannot mistake a dated record for a live claim about a file every round rewrites. Verified at the R21 gate by the reviewer's own scoped greps over that entry alone: `are byte-identical` 0 times inside it, `WERE byte-identical` once, and the sha256, byte count and line count the sentence carries all unchanged. The scope is deliberate: fifteen EARLIER gate entries carry the same present-tense phrasing and are left exactly as they are, because each sits under its own dated heading and rewriting the archive of record to correct a tense would be churn against the file this repository trusts most. RESOLVED.

TEXT-B — append to the END of .agent/live_review.md

### R21 — PASS (2026-08-13) — INTEGRATION GATE

Reviewed by the main session over 1e90e89f..35329dec: seven commits, sixteen
paths, not one of them source, test or doc. Transport:
`.agent/authored/f111-r21-1.md` and `.agent/last_block.md` WERE byte-identical
at this gate under `cmp`, 16911 bytes, 273 lines, sha256
42ba3e6e0480b28c64959023ff1fd9e6397661fec293f5c992ff8268382e041b. Markers at
gate time: twelve resolution paragraphs, one unreviewed-fix marker, 44
registered findings, one R20 gate heading, and `.agent/plan.md` at 44 lines.

THE GATE. The suite ran twice for the gate and a third time for the reviewer.
  BRANCH  (worker, at 863b3d3e)   5 failed, 16634 passed, 19 skipped in 134.16s
  BASE    (worker, at 4e0b762e)   5 failed, 16537 passed, 19 skipped in 153.37s
  BRANCH  (reviewer, at 35329dec) 5 failed, 16634 passed, 19 skipped in 180.78s
`comm -13` branch-only failures: ZERO. `comm -23` base-only failures: ZERO. The
same five ids fail in both trees — every `[reviewer]` parametrization in
`tests/orchestration/test_role_conventions.py`, each raising
`PromptSegmentError: prompt segment 'reviewer_conventions' is over its token
cap: 954 tokens estimated, cap 800` before any assertion in the test runs. That
is R-0286 unchanged; it fails at the merge base, where no F111 commit exists,
and F111 correctly does not repair it, because AGENTS.md bars mixing an
unrelated fix into a feature branch. No branch-only id existed, so no serial
re-run was needed — and the worker recorded that step as not-needed rather than
omitting it, which is the difference between a gate and a summary.

The reviewer's third run has a specific job. The worker's branch run was taken
at 863b3d3e, and two later commits rewrote `.agent/plan.md` and
`.agent/handoff.md` — files the `.agent` contract tests actually read — so that
run did not cover the head being closed. The reviewer re-ran the whole suite at
35329dec and measured the same 5 failed, 16634 passed, 19 skipped and the same
five ids. The gap is closed by measurement, not by argument.

COLLECTED-TEST DELTA. Branch collects 16658, base 16561: a delta of 97 with an
empty base-only side, so pure addition — no id renamed, moved or dropped. All 97
branch-only ids live in the six F111 test files (32 + 30 + 11 + 9 + 8 + 7 = 97),
the inverse grep against the permitted patterns returns zero, and both
`--collect-only` totals equal their own run's passed+skipped+failed arithmetic,
so this is a real test delta and not a selection difference.

UI PARITY. All four aggregate content hashes of `apps/ui/dist` are the same
value fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0 — base
before and after, primary before and after — with `cp -a` restoration, zero
symlinks and dist newer than src. Nothing wrote through into the primary
checkout during the base run. Wall clock 135 s and 154 s, both inside the
five-minute budget, so no perf pass is indicated. Cleanup is proven rather than
asserted: one worktree, no `tmp/*` branch, `.remedy-wt/base-gate` absent, and a
clean tree.

Four deviations were declared and all four are upheld. (1) Gate (c) was
unmeetable as the reviewer wrote it: `grep -c 'are byte-identical'` over the
WHOLE file counts 16, because fifteen earlier gate entries carry the phrase and
the R-0319 bullet quotes it deliberately. That is the DECISION F105 D8 item 6
class — a count scoped to a file when it should have been scoped to the change —
and the error is the reviewer's, not the worker's, who applied the ordered bytes,
met the second clause, and reported the true number instead of a convenient one.
No finding is registered: the countermeasure already exists on disk as the §3
pre-emission checklist and was simply not run, and re-registering a written rule
teaches nothing. The closure block replaces it with a gate scoped to the R19
entry, which is what it should have said. (2) The `Landed: R-0319` line could
not name its own SHA, because the fix and the line ship in one commit; naming
the commit by subject was the only honest form available. (3) C5 landed in two
commits: the first carried gate (m) as a forward reference, the second replaced
it with measured values — a correction made visible rather than quietly. (4) The
77-line handoff carries its DECISION D15 stated-cause line with no section
dropped.

TEXT-C — append to the END of docs/roadmap/features/T2_F111.md

## Built State — the shipped shape (2026-08-13)
F111 is built, gated and closed. The ist-doc is
`docs/system/diff-only-repair-v1.md`, registered in `docs/README.md`; read it
first — it carries the two knobs (`diff_mode`, `diff_margin_lines`), the
prompt-side hunk selection with its five omission reasons, the
`{format, diff, files}` response record and its fence precheck, the `diff` /
`full_fallback` modes with their `validation:` / `fence_denied:` /
`apply_failed:` reason prefixes, and the timeline events that carry the
evidence. The code is `packages/orchestration/diff_repair.py` (selection),
`diff_repair_response.py` (schema, validation, fence precheck),
`diff_repair_apply.py` (apply-or-fall-back) and the wiring in
`builder_bridge.py` (`run_builder_bridge_loop`). The saving is the pair
`total_chars` and `full_file_chars` on the `repair_mode_selected` event, in
CHARACTERS and never tokens (DECISION F111 D9). The integration gate that
cleared it is committed at `.agent/gate_f111_r21/`: zero branch-only failures
against the merge base, with the five pre-existing `test_role_conventions.py`
`[reviewer]` failures attributed to R-0286 in both trees.

TEXT-D — the STATUS line (substitute the three placeholders, nothing else)

- [x] F111 — Diff-only repair (T001–T003 complete; accepted 2026-08-13 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f111-closure · package <PACKAGE> · SHA-256 <SHA256> · accepted HEAD <ACCEPTED_HEAD>)

TEXT-E — one REWRITE pair for README.md
  FROM (1 line, occurs exactly once):
43 of 255 registered items accepted. Next: F111 (Diff-only repair).
  TO (1 line):
44 of 255 registered items accepted. Next: F115 (Prompt breakdown & cost report).

TEXT-F — the complete new .agent/plan.md

# Plan — F111 Diff-only repair (CLOSED)

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Last reviewed SHA: 35329dec (R21 PASS, integration gate). Next free
finding ID: R-0320. Open findings: 32 — 44 registered minus 12
resolved. None is High; each is an accepted risk at closure.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md). DONE.

## Current Step
Closed. T001, T002 and T003 are complete and gated; the ist-doc
`docs/system/diff-only-repair-v1.md` is registered in docs/README.md;
the integration gate in `.agent/gate_f111_r21/` shows zero branch-only
failures against the merge base; STATUS.md carries the `[x]` line and
the closure PR is open and UNMERGED by design.

## Next Steps
1. The closure PR merges at the NEXT feature's start via the AGENTS.md
   Open PR Gate — that gap is the operator's manual-review window. The
   operator may also merge it manually at any time.
2. Next feature per Rule A5 and STATUS order: F115 — Prompt breakdown
   & cost report. New session, new branch, nothing carried over but
   `.agent/candidates.md`.
3. That first reviewed round MUST register or resolve every entry in
   `.agent/candidates.md` and empty the file
   (docs/roadmap/STATUS_closure_protocol.md).

## Risks
- The suite is RED at the merge base with five known ids (R-0286),
  unrelated to F111 and unfixed here on purpose.
- The saving is measured in CHARACTERS, not tokens (DECISION F111 D9).
- All-or-nothing rests entirely on source_apply's durable snapshot;
  a failed rollback is reported, not hidden (R-0316).

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate ✅ · Closure ✅) — Schätzung

TEXT-G — the complete new .agent/candidates.md

# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- A stop reason no code can ever emit. `STOP_REASONS` in
  `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file
  finds that string in exactly one place: the frozenset itself. Nothing
  raises it, nothing tests it, nothing reads it. It predates this
  branch — it is present at the merge base 4e0b762e — so it is NOT an
  F111 defect and was deliberately not fixed here, because AGENTS.md
  bars mixing an unrelated fix into a feature branch. It is recorded
  because F111 is the feature that put a stale-diff CONCEPT into the
  codebase (`out_of_bounds` in `diff_repair.py` is how a stale diff
  actually becomes visible), so the next reader will reasonably expect
  the two to be connected and find that one of them is dead. Either
  wire it to the condition it names or delete it. · source F111 ·
  2026-08-13
