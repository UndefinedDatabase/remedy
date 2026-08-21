── STEP R1/1 — F009 The single write channel ────────────────────────
Goal:        Open the F009 branch: merge pull request #209 at the Open PR Gate,
             claim F009 in the roadmap ledger, reset `.agent/live_review.md` for
             this branch carrying the open findings forward BY SCRIPT, record the
             F008 R36 verdict as this record's first `Gate:` paragraph, register
             the closure candidate F008 carried, resolve R-0406, and empty
             `.agent/candidates.md`. No production code is touched this round.

Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the live-review reset · C3 the STATUS claim · C4 the candidates
             carrier emptied · C5 the context file · C6 the handback.

Change set:  `.agent/authored/f009-r1.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md`,
             `.agent/candidates.md`, `.agent/context.md`, `.agent/handoff.md`.
             Nothing else. No path under `packages/`, `apps/`, `tests/` or
             `docs/roadmap/features/` is edited this round.

## Step 0 — the Open PR Gate, BEFORE any commit
Run, in this order, and record each exit code and its real output:

    ls -la .agent/STOP
    git rev-parse --abbrev-ref HEAD
    git status --porcelain
    gh pr list --state open --json number,headRefName,baseRefName,isDraft
    gh pr merge 209 --merge --delete-branch
    git checkout main
    git pull --ff-only
    git rev-parse HEAD
    git checkout -b feature/f009-single-write-channel

`.agent/STOP` MUST be absent; if it exists, stop, write the handoff and end.
Pull request 209 is `feature/f008-sse-event-stream` into `main`, not a draft,
and its CI run 32511286935 concluded `success` — the reviewer read that
conclusion itself. It was created by a PREVIOUS session, so merging it here is
the Open PR Gate and not a same-session merge. If `gh pr list` shows anything
other than exactly that one pull request, stop and report.

The SHA that `git rev-parse HEAD` prints after the pull is the BRANCH POINT.
Record it in the handback; every gate below that says "at the branch point"
means that value. It is the merge commit of pull request 209 and it cannot be
named in this block, because it does not exist while this text is written.

## Transport
This block lives at `.remedy-wt/f009-r1.md`. Its sha256, byte count and line
count are stated in the task prompt that handed you that path — a file cannot
carry its own digest, so the digest travels beside it rather than inside it.
Verify it BEFORE using any byte of it. Save it byte for byte as
`.agent/authored/f009-r1.md` (C0a). Then mirror it to `.agent/last_block.md`
(C0b) FROM THE COMMITTED C0a BLOB — `git show <C0a>:.agent/authored/f009-r1.md`
— never from this file again and never by retyping.

## Slice convention
The authored units below are delimited by one-line markers, `<<<SLICE <NAME>`
opening and `<<<END <NAME>` closing. Extract every slice from the COMMITTED C0a
BLOB by its marker lines, never from this message and never by hand. The marker
lines are NOT part of any slice. Every slice is newline-terminated, none begins
with a blank line, and none carries trailing whitespace on any line — report
those three readings as your script measured them. Marker lines never reach a
target file: gate `^<<<SLICE ` and `^<<<END ` at 0 lines in every committed
target.

## C1 — the plan, the FIRST substantive commit
This round registers, resolves and renumbers findings, so `.agent/plan.md`
advances first (checklist item 23). Apply PLANF009R1 as the WHOLE file.

<<<SLICE PLANF009R1
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at the merge commit of
pull request #209, which R1 merges at the Open PR Gate. `.agent/live_review.md`
is the source of truth for the open set, the next free finding id and the round
map.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI command catalog, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through queue
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R1 opens the feature. It merges pull request #209 at the Open PR Gate, claims
F009 in the roadmap ledger, resets this branch's review record while carrying the
open findings forward by script, records the F008 R36 verdict as that record's
first `Gate:` paragraph, registers the closure candidate F008 carried, resolves
R-0406 by dropping the stale next-free-id line the reset is the fix for, and
empties `.agent/candidates.md`.

## Next Steps
1. R2 the write-channel inventory, MEASURED in the source rather than read off
   the feature file: where the UI command catalog lives and which subset it
   exposes, how `_RemedyHandler` authenticates today, and which module owns each
   effect backend — the kill-switch control file, the decision queue and the
   approval consumption.
2. R3 records R2 and rules the channel's shape as a DECISION: the auth pair, the
   nonce replay window, the rate-limit configuration and the audit record fields.
3. R4 onward the built work, in the T001/T002/T003 order the feature file names.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  configuration installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
<<<END PLANF009R1

## C2 — the live-review reset
One commit, one file. It is the verbatim rewrite of a single `.agent/**` state
file, which AGENTS.md DECISION F104 D1 exempts from the 500-line commit cap;
declare that exemption in the handback rather than splitting the file.

Extract LRHEADER, R0630, DONE0406 and GATE1 from the committed C0a blob into
`.remedy-wt/f009r1_slices/LRHEADER.txt`, `R0630.txt`, `DONE0406.txt` and
`GATE1.txt`. Then run RESETSCRIPT from the repository root and record every line
it prints.

<<<SLICE RESETSCRIPT
import hashlib
import re
from pathlib import Path

SL = Path(".remedy-wt/f009r1_slices")
LR = Path(".agent/live_review.md")

old = LR.read_text(encoding="utf-8")
print("INPUT sha256", hashlib.sha256(old.encode("utf-8")).hexdigest())
print("INPUT bytes", len(old.encode("utf-8")), "lines", old.count("\n"))

units = old.rstrip("\n").split("\n\n")
reg = [u for u in units if re.match(r"^- R-\d+ — ", u)]
done = set(re.findall(r"^Done: (R-\d+) — ", old, re.M))
carried = [u for u in reg if re.match(r"^- (R-\d+) — ", u).group(1) not in done]
ids = [re.match(r"^- (R-\d+) — ", u).group(1) for u in carried]
print("REGISTERED", len(reg), "RESOLVED", len(done), "CARRIED", len(carried))
print("CARRIED IDS DISTINCT", len(set(ids)))
print("R-0406 CARRIED", "R-0406" in ids)
print("MAX ID", max(ids))

absent = [i for i in ids if u"- " + i + u" — " not in old]
print("CARRIED IDS NOT PRESENT IN THE OLD RECORD", len(absent))
notbytes = [i for i, u in zip(ids, carried) if u not in old]
print("CARRIED PARAGRAPHS NOT BYTE-PRESENT IN THE OLD RECORD", len(notbytes), notbytes)

header = SL.joinpath("LRHEADER.txt").read_text(encoding="utf-8").rstrip("\n")
r0630 = SL.joinpath("R0630.txt").read_text(encoding="utf-8").rstrip("\n")
done406 = SL.joinpath("DONE0406.txt").read_text(encoding="utf-8").rstrip("\n")
gate1 = SL.joinpath("GATE1.txt").read_text(encoding="utf-8").rstrip("\n")

new = "\n\n".join([header] + carried + [r0630, done406, gate1]) + "\n"
LR.write_text(new, encoding="utf-8")
print("OUTPUT sha256", hashlib.sha256(new.encode("utf-8")).hexdigest())
print("OUTPUT bytes", len(new.encode("utf-8")), "lines", new.count("\n"))

back = new.rstrip("\n").split("\n\n")
mid = back[len(back) - len(carried) - 3:len(back) - 3]
print("CARRIED ORDER PRESERVED", mid == carried)
print("REGISTERED AFTER", len(re.findall(r"^- R-\d+ — ", new, re.M)))
print("RESOLVED AFTER", len(re.findall(r"^Done: R-\d+ — ", new, re.M)))
print("LANDED AFTER", len(re.findall(r"^Landed: ", new, re.M)))
print("GATE LINES AFTER", len(re.findall(r"^Gate: R\d+ — ", new, re.M)))
print("NEXT FREE ID HEADER LINES", len(re.findall(r"^> Next free id", new, re.M)))
<<<END RESETSCRIPT

<<<SLICE LRHEADER
# Live Review — F009 The single write channel

> Round-by-round review record for the F009 branch, reset at the feature claim.
> The F008 record closed with pull request #209, merged into `main` at this
> feature's Open PR Gate. That branch's LAST round, R36, has no gate entry in its
> own record by construction, because a round's verdict is written by the NEXT
> reviewed round (DECISION F085 D9) and R36 was the last round F008 had; its
> entry is therefore the first `Gate:` paragraph below. Finding ids continue the
> monotonic R-XXXX series across the reset.
>
> This header carries NO next-free-id sentence, and its absence is the fix for
> R-0406 rather than an omission. That finding ruled the stored value a second
> source of truth for a number
> `docs/agents/planner_reviewer_prompt.md` §3 item 10 already requires every
> emission to recompute mechanically from this record, and named the next
> feature's reset as the place to drop it. Derive the ceiling with `max` over the
> line-anchored `^- R-\d+ — ` entries below.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when the
> F008 record closed are reproduced verbatim below, extracted BY ID out of the
> previous record by script and never retyped, never rewrapped and never
> summarised. The pre-reset record held no `Landed:` line.

## Steps
R1 merge #209 at the Open PR Gate, claim F009 in the ledger, reset this record
carrying the F008 open set forward, gate R36 and register the candidate F008
carried → R2 the write-channel inventory: where the UI command catalog lives and
which subset it exposes, how `_RemedyHandler` authenticates today, and which
module owns each effect backend — the kill-switch control file, the decision
queue and the approval consumption — each MEASURED in the source rather than read
off the feature file → R3 record R2 and rule the channel's shape as a DECISION:
the auth pair, the nonce replay window, the rate-limit configuration and the
audit record's fields → R4 onward the built work, in the T001/T002/T003 order the
feature file's Task slicing names.

## Findings
<<<END LRHEADER

<<<SLICE R0630
- R-0630 — Low — A UNIQUENESS OR COUNT GATE OVER `.agent/live_review.md` MUST NAME THE ANCHOR IT IS READ UNDER, BECAUSE THAT FILE LEGITIMATELY QUOTES ITS OWN GATE HEADERS. Carried in `.agent/candidates.md` as a closure candidate of F008, raised by the reviewer during the R35 gate, and registered here because this is F009's first reviewed round; the open set was searched for the DEFECT before the id was minted (§3 item 30), and the only neighbouring entries — R-0584 on a guard satisfied by a quotation and R-0587 on a slice's header shape — describe the token-stripping rule and the header-comparison rule rather than the anchor a count is read under. THE INSTANCE: the F008 R35 block's G6 ordered "the R35 pair occurs EXACTLY ONCE" for the entry header `Gate: R35 — the R34 entry.` without saying LINE-ANCHORED. Measured by the reviewer at `c5ebf179`, that byte string occurs TWICE in the file, the second occurrence inside finding R-0600, which quotes the F086 record's identically-worded round-35 header. The worker read the gate line-anchored over `^Gate: ` lines, which is the entry-key reading §3 item 26 exists for, reported 1, and was right; NOTHING FALSE LANDED and the ledger was healthy at that commit, 35 `Gate: ` lines under 35 distinct keys. WHY IT IS STILL A DEFECT: header strings repeat across features by construction — this record's own R1 header will one day be quoted by a finding — so any round whose header a finding has quoted inherits an unmeetable gate the moment the count is read as a substring, and the two readings differ silently. WHY LOW: the failure mode is a gate that cannot be satisfied rather than a claim that is false, and the worker's reading was the correct one both times it arose. THE FIX, beside §3 item 26 which produced this gate class: a uniqueness or count gate over a file that quotes its own record format STATES the anchor it is read under, and a block ordering such a count orders BOTH readings and labels each — as R-0586 already requires backtick-quoted spans to be deleted before a token is counted. That edit lands in `docs/agents/planner_reviewer_prompt.md`, which F009 does not own and AGENTS.md forbids mixing into a feature branch, so it routes to the paydown branch already carrying R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613, together with promoting the fix clauses of R-0387 and R-0573 into the §3 checklist. OPEN.
<<<END R0630

<<<SLICE DONE0406
Done: R-0406 — Resolved by this commit, which is the reset R-0406's own fix clause named: "the header sentence naming a next free id is removed at the next feature's reset". The F008 header carried `Next free id: R-0612.` while that record's highest registered entry was R-0629, so the stored value understated the ceiling by seventeen and a session trusting it would have reused an id seventeen times over. The F009 header this commit writes carries no such sentence, and RESETSCRIPT's `NEXT FREE ID LINE` reading is the measurement that it does not: consumers derive the ceiling with `max` over the line-anchored `^- R-\d+ — ` entries, which is what `docs/agents/planner_reviewer_prompt.md` §3 item 10 has always required. The finding's own conduct ruling stands and is not weakened by this resolution: no round rewrote that header mid-feature, because doing so would have broken the append-only property for a cosmetic gain, and the R2 worker that noticed the staleness and declined to touch it did the right thing.
<<<END DONE0406

<<<SLICE GATE1
Gate: R1 — the F008 R36 entry. R36 PASSED AND F008 IS CLOSED. NO finding is registered against it: every value it reported reproduced, and every gate below was RE-EXECUTED by the reviewer off disk rather than read back out of the handback. THE CLOSURE VALUES ARE REAL AND THE REVIEWER MEASURED THEM ITSELF: `remedy-review-20260821-193052-READY_FOR_REVIEW.zip` is present in the repository root and recomputes to sha256 1d827ac756433f3be73f02947d9b1410e7759c4fc9ef6dfd95f5032924b9a366, which is exactly the digest the `[x]` line committed at `e20fe420` quotes, and that same line's `accepted HEAD` value, 870f198ea9c0e4b51075f3386d1025cce805811a, is a real commit — `git cat-file -t` prints `commit` — and an ancestor of the branch tip `7be4cfba`, so the STATUS line names a package that exists on disk and a commit that is really on the branch rather than two values that merely agree with each other. TRANSPORT HELD: `.agent/authored/f008-r36.md` and `.agent/last_block.md` are both sha256 188502199d1931b706c9f016fcf990f435e4754e6f087658d721352576d0fdd9 over 34965 bytes and 490 lines, equal as bytes and equal to the digest carried at delegation, and 490 is exactly the budget DECISION F085 D6 rules rather than a line under it. THE RANGE HOLDS, walked by the reviewer over `3035bc2a`..`7be4cfba`: SEVEN single-parent commits over exactly the eight declared paths plus the handback's own, insertions 490, 402, 13, 2, 10 and 24 for the six pre-handback commits — every one under the 500 cap, 490 the maximum — and each cell equal to the `+/-` column of the handback's `## Commits` table, which is the second derivation §3 item 28 exists to catch and it agreed. Zero lines beginning `<<<SLICE ` or `<<<END ` leaked into any of the six committed targets. THE LEDGER APPEND at `65c9e315` is two lines, a blank separator and one paragraph headed `Gate: R36 — the R35 entry.`, and that header matches the shape of the entries it joins with the second numeral one less than the first — §3 item 26 met by comparison rather than by eye. THE SETS ARE WHAT THE ROUND CLAIMED: 201 registered entries, ALL DISTINCT, 6 line-anchored `Done:` lines naming R-0620, R-0621, R-0623, R-0624, R-0626 and R-0627, 0 `Landed:` lines, 36 `Gate:` lines, and `^- R-0630 — ` reading 0 — the round minted no id, so R-0630 was still free for this record to spend on F008's closure candidate. THE COUNTS AGREE ACROSS TWO FILES at the closure commit: `docs/roadmap/STATUS.md` holds 54 line-anchored `- [x] F` entries, zero `- [~] ` and zero `- [!] `, and `README.md` states 54 in its prose and 2 in the Tier 5 Done cell against the two accepted ids carrying a `T5_` feature file. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at the branch tip: `python3 -m pytest tests/docs/ -q -rf` EXITS 0 at 295 passed, and the canary `python3 -m pytest tests/cli/test_golden_path.py -q -rf` EXITS 0 at 42 passed — the same two numbers the handback reported. THE DOCS PIN R36 REPLACED IS STRICTLY STRONGER THAN THE ONE IT RETIRED, which is the one thing a repair of this shape must prove, and the reviewer proved it in its OWN disposable worktree at `7be4cfba` with the primary checkout never written to: with F009 claimed and nothing else changed the suite EXITS 0 at 295 passed, with a SECOND claim injected on the F021 line it EXITS 1 at 1 failed and 294 passed, failing exactly `TestPrimaryDocsAreHonest::test_status_marks_f007_and_f010_accepted_and_nothing_after_them` and naming both claims in its message, and `tests/orchestration/test_roadmap_index.py` EXITS 0 at 30 passed with the claim in place. The retired sentence pinned the HOLDER of the claim, so it went red at every closure; the sentence that replaced it pins AT MOST one claim, which is true at a claim and true at a closure alike, and the worktree was removed and pruned before this verdict with `git worktree list` naming the primary checkout alone. THE HANDBACK'S OWN NUMERAL IS CORRECT: it declares itself 90 lines and `wc -l` reads 90, under the 100 its seven commits allow, and `.agent/plan.md` reads 35 lines under the 50-line cap. THE PULL REQUEST IS REAL AND WAS NOT SELF-MERGED: 209, `feature/f008-sse-event-stream` into `main`, OPEN, MERGEABLE and not a draft when this verdict was written, its CI run 32511286935 concluded `success`, and it was merged at THIS round's Open PR Gate by the next session rather than by the one that created it. WHAT THIS PAIR OF ROUNDS SETTLES is worth recording once: R36 is the LAST round of the F008 branch, so the terminator of §4 item 13 applies and its verdict has no gate entry inside its own record — this paragraph, the first of the F009 record, IS that entry, written by the next reviewed round exactly as DECISION F085 D9 requires, and it is the concrete reason a branch may not end at a verdict without a following round to carry it.
<<<END GATE1

## C3 — the STATUS claim
One line, in `docs/roadmap/STATUS.md`. The reviewer's containment test printed
`STATUS pair — TO contains FROM: False`, and the REWRITE label is derived from
that output: this pair owes the FROM-0x reading rather than the append obligation
of §4.9.

<<<SLICE STATUSFROM
- [ ] F009 — The single write channel
<<<END STATUSFROM

<<<SLICE STATUSTO
- [~] F009 — The single write channel
<<<END STATUSTO

## C4 — the candidates carrier, emptied
`.agent/candidates.md` becomes CANDIDATES as the WHOLE file. Its single entry is
registered as R-0630 by C2, so the file empties in the same round that registers
it, which is what docs/roadmap/STATUS_closure_protocol.md requires.

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

EMPTY. The one entry F008 carried — the line-anchoring rule for uniqueness gates
over `.agent/live_review.md` — is registered as R-0630 in this branch's review
record, by the same round that empties this file.
<<<END CANDIDATES

## C5 — the context file
`.agent/context.md` becomes CONTEXTF009 as the WHOLE file. Its readers span
several test modules: the dashboard contract asserts the substring "Steps" and a
`## Active Branch` heading with a `feature/` slug, `test_test_runner.py` asserts a
roadmap F-id, and `tests/regression/test_resource_safety.py` asserts "resource" or
"pytest" — validate the applied file against ALL of them, not only the one you
happen to run.

<<<SLICE CONTEXTF009
# Context — F009 The single write channel

## Active Branch
feature/f009-single-write-channel, cut from `main` at the merge commit of pull
request #209, which R1 merged at the Open PR Gate. Self-drive session per
docs/agents/self_drive_protocol.md: the main session plans and reviews and writes
nothing in the work tree, one delegated worker per round makes every commit. The
branch is fresh and carries no pull request.

## Scope
In: ONE authenticated POST door for UI-initiated change —
`/api/jobs/<job_id>/commands` taking {command, args, client_nonce}, validated
against the UI-exposed subset of the command catalog, authenticated by bearer
token plus an X-Remedy-CSRF double-submit, rate-limited per token and job,
deduplicated by nonce so a replay returns the ORIGINAL result, audited per job,
and ENQUEUEING into the decision, approval and control machinery that already
exists. Also in: the `command.accepted` event on the F008 stream, and the
route-walking proof that every other POST, PUT and DELETE answers 405.

Out, per the feature file's Do not touch: the effect backends' semantics, the
catalog's CLI half, and any file or shell access from a handler — forbidden by
the P3 contract and enforced by an import guard rather than by convention.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py — the second by
  R-0493, tests/docs/ asserting nothing about a feature file's body — and a round
  rewriting `.agent/` state or touching the UI server also gates
  tests/ui_server/, tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource safety
  stays intact. Two pytest processes never run at once.
- COUNT BY PASSED-PLUS-SKIPPED. Data-dependent `pytest.skip(...)` calls in
  tests/ui_server/ make the split vary run to run at an unchanged tree, so a bare
  passed count is not a stable gate value and a skip is not a failure.
- This is a UI-facing feature: docs/ui/design_reference/ is binding for every
  visual surface and assets_spec.md is the asset authority. Any deviation needs
  an assumption_log entry carrying a technical reason.
- Repository-wide `ruff check .` is RED at base and is NOT a gate (R-0364). Ruff
  is gated scoped to the files a round touches, measured against the SAME files
  at the base, so a pre-existing error is never read as a new one. `npm run lint`
  in `apps/ui` is likewise red at base and is R-0622.
- 196 findings are open after this round's reset and registration, and none is a
  code defect of F009. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613 and the new
  R-0630 stay routed to a paydown branch, together with promoting the fix clauses
  of R-0387 and R-0573 into the §3 checklist.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXTF009

## Constraints
1. Apply every slice BYTE FOR BYTE out of the committed C0a blob. Do not retype,
   rewrap, reflow, reindent or whitespace-adjust any of them. If a slice looks
   wrong to you, apply it as written and say so in the handback under
   "Deviations & assumptions" — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and nothing else comes
   between them. C1 is the first substantive commit.
3. The change set is the eight paths named above. Touch no other path. In
   particular do not edit `tests/docs/test_docs_consistency.py`: the reviewer
   dry-ran this round's STATUS claim against that suite and it stays GREEN, so
   there is nothing to repair there. If any suite named below goes red, STOP,
   record the raw output, and write the handoff — do not repair a test to buy a
   green.
4. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there and runs from there; `git status --porcelain` prints 0 lines after each
   commit, so nothing from that directory is ever committed.
5. Push with `git push -u origin feature/f009-single-write-channel` after C5, and
   do NOT create a pull request this round — F009 opens its pull request at its
   own closure.

## Done when
- G1 `.agent/STOP` ABSENT, read immediately before C0a. `git rev-parse
  --abbrev-ref HEAD` prints `feature/f009-single-write-channel` from C0a onward.
  `git status --porcelain` prints 0 lines after each of C0a through C6.
- G2 Transport EQUAL: `.remedy-wt/f009-r1.md` as received, `.agent/authored/
  f009-r1.md` at C0a and `.agent/last_block.md` at C0b all carry the same sha256,
  byte count and line count, and that digest EQUALS the one stated above.
- G3 Report, per slice, the newline-included sha256, byte count and line count,
  the COUNT of slices taken from your own ordered extraction out of the committed
  C0a blob, and the three aggregate readings: any trailing whitespace, any
  leading blank line, all newline-terminated.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R1; report its line count
  against the 50-line cap; `Steps` occurs; `^## Goal$` and `^## Next Steps$` each
  match exactly 1 line; and its first `\bF\d{3}\b` match is `F009`.
- G5 The reset at C2: report every line RESETSCRIPT prints. `CARRIED PARAGRAPHS
  NOT BYTE-PRESENT IN THE OLD RECORD` MUST read 0 and `CARRIED IDS NOT PRESENT`
  MUST read 0 — that pair is what makes "extracted by script, never retyped" a
  measurement instead of a promise. NEGATIVE CONTROL, in scratch and never over
  the tracked file: flip ONE printable ASCII byte in ONE carried paragraph and
  re-run the byte-presence check, which MUST then report 1; report both readings
  and confirm the unflipped value reports 0.
- G6 At C2, line-anchored: `^- R-\d+ — ` reads 196, all ids DISTINCT;
  `^Done: R-\d+ — ` reads 1 and names R-0406; `^Landed: ` reads 0; `^Gate: R\d+
  — ` reads 1; `^- R-0630 — ` reads 1; and `^> Next free id` reads 0 lines —
  anchored at the header's own form, because DONE0406 QUOTES the retired sentence
  and a bare substring count would be unmeetable by construction. Report the max
  id the file carries.
- G7 The claim at C3. Read the branch-point bytes with `git show <branch
  point>:docs/roadmap/STATUS.md` into `.remedy-wt/` scratch — never by writing
  that blob over the tracked file, which guardrail G5 of
  docs/agents/self_drive_protocol.md forbids. STATUSFROM reads 1 at the branch point and 0 at C3,
  STATUSTO reads 0 then 1, and the branch-point blob with that substitution
  applied ONCE is BYTE-EQUAL to the C3 blob — which is also the proof no other
  line of that file changed. `^- \[~\] ` reads 0 at the branch point and 1 at C3;
  `^- \[x\] F\d{3} — ` reads 54 at BOTH, so claiming F009 moved nothing into the
  accepted set. `README.md` is correctly ABSENT from this round's change set.
- G8 The carrier at C4 is BYTE-EQUAL to CANDIDATES, and `^- ` reads 0 in it.
  `.agent/context.md` at C5 is BYTE-EQUAL to CONTEXTF009; report the four reader
  assertions of constraint C5 as four readings taken over the APPLIED file.
- G9 In the PRIMARY checkout, SERIALLY, one process at a time, at C5:
  `python3 -m pytest tests/docs/ -q -rf`, then `python3 -m pytest
  tests/orchestration/test_roadmap_index.py -q -rf`, then `python3 -m pytest
  tests/ui_server/ tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  -q -rf`, then the canary `python3 -m pytest tests/cli/test_golden_path.py -q
  -rf`. Report each exit code and its passed-plus-skipped sum. The reviewer
  measured the first two at the F008 branch tip with this round's claim applied
  in a throwaway worktree: 295 passed and 30 passed, both exit 0.
- G10 The range from the branch point to C5: `git diff --name-only` lists
  EXACTLY the seven paths of the change set other than `.agent/handoff.md`, the
  set difference empty in both directions. Walk `git rev-list --reverse` and
  report, per commit, that it has ONE parent and its `git show --numstat`
  insertions, with `git diff --numstat` AGREEING on every cell; every cell must
  equal the `+/-` column of your `## Commits` table. Name the C2 exemption
  explicitly. `^<<<SLICE ` and `^<<<END ` read 0 lines in each of
  `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md`,
  `.agent/candidates.md` and `.agent/context.md`. Classify this round's own
  reflog entries by the operation before the first `:` in `%gs` and report the
  counts of `amend`, `rebase` and `cherry`, which must each be 0; assert no total
  over the whole reflog (R-0601).
- G11 The Open PR Gate transcript of Step 0, one line per command with its exit
  code, plus the branch point SHA and the merge commit `gh pr merge` reported.
- G12 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4, C5 and C6, the branch point SHA, and one
  line per gate — the raw transcripts belong in the round report, not here
  (R-0582). Report its line count against the 100 that eight commits allow.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 0 % (T001 offen · T002
             offen · T003 offen — R1 hat das Feature beansprucht, den
             Review-Record zurückgesetzt und das F008-R36-Urteil eingetragen;
             gebaut wurde noch nichts) — Schätzung
──────────────────────────────────────────────────────────────
