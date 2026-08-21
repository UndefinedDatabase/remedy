── STEP R1/1 — F008 SSE event stream ─────────────────────────
Goal:        Open the F008 branch: merge pull request #208 at the Open PR
             Gate, claim F008 in the roadmap ledger, reset the live-review
             record for the new branch while carrying the open set forward
             by id, and record the F255 R21 verdict — the closing round of
             the previous branch, whose gate entry can only be written by
             the next reviewed round (DECISION F085 D9). No production
             code is written this round.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 reset the live-review record and record the R21 verdict ·
             C3 claim F008 in the ledger and rewrite the branch context ·
             C4 write the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r1.md   (C0a, new file)
             - .agent/last_block.md         (C0b, full rewrite)
             - .agent/plan.md               (C1, full rewrite)
             - .agent/live_review.md        (C2, rebuilt by the script)
             - docs/roadmap/STATUS.md       (C3, the F008 pair)
             - .agent/context.md            (C3, full rewrite)
             - .agent/handoff.md            (C4, full rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r1.md, extracted by its marker lines. No slice is
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R1,
    CONTEXTF008, LRHEADER, GATE1 and RESETSCRIPT are applied with their
    trailing newline INCLUDED. STATUSFROM and STATUSTO are single lines
    applied WITHOUT a trailing newline, so the surrounding file structure
    is untouched.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, and the Open PR
    Gate runs BEFORE C0a. .agent/plan.md is advanced at C1, the first
    substantive commit of the round — only the two block-save commits may
    precede it (checklist item 23).
 4. Pair shape, from a containment test the reviewer ran before emission.
    STATUSFROM/STATUSTO: `TO contains FROM: false` — therefore a REWRITE,
    so the obligation is FROM 1x→0x and TO 0x→1x in docs/roadmap/STATUS.md
    and NO append reading is owed for it.
 5. The live-review reset is performed by RESETSCRIPT, applied byte for
    byte and run UNEDITED. If any of its assertions fires, STOP, report the
    exact assertion text and the values it printed, and do not repair the
    script — that is the reviewer's defect to fix in the next block.
 6. Destructive checks run in memory or inside a disposable worktree under
    .remedy-wt/, never against a tracked file. `git status --porcelain` is
    empty after every commit and at the handback.
 7. Two pytest processes never run at once, and every suite runs in the
    PRIMARY checkout — it is the only tree holding apps/ui/node_modules.
 8. No production code. No path under packages/, apps/, tests/ or
    docs/roadmap/features/ is touched this round.
 9. The reviewer's base readings, taken at `8e08c0da` before this block was
    emitted, so a pre-existing red is not read as this round's: tests/docs/
    plus tests/orchestration/test_roadmap_index.py exit 0 at 325 passed;
    the state-reader four exit 0 at 160 passed; the canary exits 0 at 42
    passed; repository-wide `ruff check .` is RED at 26 errors (20 I001,
    4 F401, 1 UP035, 1 F821) and is NOT a gate for this round, whose change
    set holds no Python file.

Done when:
 G1  `.agent/STOP` is absent, checked immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback; `git worktree list` names the primary
     checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of
     .remedy-wt/f008-r1.md, of .agent/authored/f008-r1.md at C0a and of
     .agent/last_block.md at C0b, and state whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     .agent/authored/f008-r1.md by their marker lines, take the COUNT from
     that listing, and report per slice its newline-INCLUDED sha256, byte
     count and line count.
 G4  Plan. Report the sha256, byte count and line count of .agent/plan.md at
     C1, and whether it is byte-equal to PLANF008R1. Its line count is under
     50. In that file `## Goal` and `## Next Steps` each occur exactly once
     as line-anchored headings and `F008` occurs at least once. C1 is the
     first commit after C0a and C0b.
 G5  The reset, measured three ways. In .agent/live_review.md at C2:
     (a) the file BEGINS with LRHEADER byte for byte and ENDS with GATE1
         byte for byte — report both as the boolean the test printed;
     (b) line-anchored counts: `^- R-\d+ — ` is 183, `^Done: R-\d+ — ` is 0,
         `^Landed: ` is 0, and `^Gate: R\d+ — ` is 1;
     (c) the SET of ids registered at C2 equals exactly the set of ids that
         were registered and NOT resolved in .agent/live_review.md at
         `8e08c0da`. Report both set sizes and the symmetric difference,
         which is empty.
 G6  Carried text is verbatim. For every carried id, compare its paragraph at
     C2 against the paragraph with the same id at `8e08c0da`. Report the
     number of ids compared and the number byte-EQUAL; the two agree. Then
     run a NEGATIVE CONTROL: flip one byte of one carried paragraph in
     memory and report that the same comparison now reports a mismatch.
 G7  Contract shape. In .agent/live_review.md at C2, `## Steps` occurs
     exactly once as a line-anchored heading and `## Findings` exactly once.
 G8  The claim pair. In docs/roadmap/STATUS.md, count STATUSFROM and
     STATUSTO as WHOLE LINES at `8e08c0da` and at C3: FROM reads 1 then 0,
     TO reads 0 then 1. Separately report that the count of
     `^- \[x\] F\d{3} — ` lines in that file is 53 at both `8e08c0da` and
     C3 — the claim moves no feature into the accepted set — and that
     README.md is NOT in this round's change set.
 G9  Context. Report the sha256, byte count and line count of
     .agent/context.md at C3 and whether it is byte-equal to CONTEXTF008. In
     that file `## Active Branch` occurs exactly once, the token `feature/`
     occurs at least once, and the substrings `Steps`, `F008`, `pytest` and
     `resource` each occur at least once — those are the four assertions the
     live state readers make about this path.
 G10 Docs gate, in the primary checkout, run SERIALLY:
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
     Report each exit code and each passed count. Both exit 0.
 G11 State-reader gate and canary, in the primary checkout, run SERIALLY and
     never alongside G10:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     Report each exit code and each passed count. Both exit 0.
 G12 The Open PR Gate, reported as a transcript of real exit codes:
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     before the merge; the exact merge command
     `gh pr merge 208 --merge --delete-branch` and its exit code; then
     `git checkout main`, `git pull --ff-only`, `git rev-parse main`, and
     `git checkout -b feature/f008-sse-event-stream`. After the merge,
     `gh pr list --state open` returns an empty list. Report the SHA
     `git rev-parse main` printed and confirm with
     `git merge-base --is-ancestor <that sha> feature/f008-sse-event-stream`
     that the new branch descends from it.
 G13 Range. With BASE the SHA G12 reported, run
     `git diff --name-only BASE..C4` and report that its output equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C4 has exactly one parent. Report each commit's INSERTION count
     from `git show --numstat`, all under 500, and compare those numbers
     cell by cell against the `+/-` column of the handback's `## Commits`
     table, reporting that the two readings agree.
 G14 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` — the
     line-anchored reading, because GATE1 legitimately quotes both markers
     mid-line — in .agent/plan.md at C1, .agent/live_review.md at C2,
     docs/roadmap/STATUS.md at C3, .agent/context.md at C3 and
     .agent/handoff.md at C4. Every count is 0.
 G15 History. Over this round's OWN reflog entries only, report the count
     containing `amend`, `rebase` or `cherry`; it is 0. Do not order that
     every entry read `commit:` — this round performs a checkout, a pull and
     a branch creation, so that reading is unmeetable by construction
     (finding R-0601), and an unstage is not a history rewrite (R-0608).
 G16 Handback. .agent/handoff.md at C4 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3 and C4 exactly once each. Report its line
     count; the cap for this round is 100, this round having more than five
     commits. C4's own insertion count belongs to the round report, not to
     that table's own cell (finding R-0149).

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 2 % (F008 claimed · the previous feature's pull
            request merged and its closing verdict recorded · the review
            record reset with 183 findings carried forward · the stream
            inventory R2 measures is not yet started) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R1
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at the merge commit of
pull request #208, which THIS round merged at the Open PR Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat, and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the client transcript byte-equals the
ledger's envelope sequence, the heartbeat holds cadence, and the fallback
engages on a disabled EventSource and recovers to live.

## Current Step
R1 opens the feature. It merges pull request #208 at the Open PR Gate, claims
F008 in `docs/roadmap/STATUS.md`, resets `.agent/live_review.md` for the new
branch while carrying the open set forward by id, and records the F255 R21
verdict — the closing round of the previous branch, whose gate entry can only
be written by the next reviewed round. No production code is written here.

## Next Steps
1. R2 inventories the ground the feature file's "How it fits" section names,
   MEASURED in the source rather than read off the feature file: whether
   ledger entries already carry a monotonic index, how the UI server serves a
   long-lived response and whether it is threaded, what the Part E envelope
   contract fixes, and how the existing state endpoint authenticates.
2. R3 records R2 and rules the stream's shape as a DECISION — threading, the
   heartbeat cadence, the max-connections guard and the fallback's contract —
   before any endpoint is written.
3. R4 onward builds T001, T002 and T003 in the feature file's own order.

## Risks
- The server-capability finding gates everything: the feature file's
  Orchestrator brief dispatches it first, and a stream built on an unthreaded
  stdlib server would block every other request the cockpit makes.
- 183 findings are open at this reset and none is a code defect of F008.
  R-0403, R-0607, R-0608, R-0609 and R-0611 are routed to a paydown branch
  and are deliberately not fixed here.
<<<END PLANF008R1

<<<SLICE LRHEADER
# Live Review — F008 SSE event stream

> Round-by-round review record for the F008 branch, reset at the feature claim.
> The F255 record closed with pull request #208, merged into `main` at this
> feature's Open PR Gate. That branch's LAST round, R21, has no gate entry in
> its own record by construction, because a round's verdict is written by the
> NEXT reviewed round (DECISION F085 D9) and R21 was the last round F255 had;
> its entry is therefore the first `Gate:` paragraph below. Finding ids continue
> the monotonic R-XXXX series across the reset.
> Next free id: R-0612.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when
> the F255 record closed are reproduced verbatim below, extracted BY ID out of
> the previous record by script and never retyped, never rewrapped and never
> summarised. The pre-reset record held no `Landed:` line.

## Steps
R1 merge #208 at the Open PR Gate, claim F008 in the ledger, reset this record
carrying the F255 open set forward and gate R21 → R2 the stream inventory:
whether ledger entries already carry a monotonic index, how the UI server
serves a long-lived response and whether it is threaded, what the Part E
envelope contract fixes and how the existing state endpoint authenticates —
each MEASURED in the source rather than read off the feature file → R3 record
R2 and rule the stream's shape as a DECISION: threading, the heartbeat
cadence, the max-connections guard and the fallback's contract → R4 onward the
built work, in the T001/T002/T003 order the feature file's Task slicing names.

## Findings
<<<END LRHEADER

<<<SLICE GATE1
Gate: R1 — the F255 R21 entry. R21 PASSED and F255 IS CLOSED. NO finding is registered against it: the round did exactly what its block ordered, declared no deviation beyond the two observations named at the end of this entry, and every gate it reported was RE-EXECUTED by the reviewer off disk rather than read back out of the handback. THE CLOSURE VALUES ARE REAL AND THE REVIEWER MEASURED THEM ITSELF: `remedy-review-20260821-051015-READY_FOR_REVIEW.zip` is present at 60194458 bytes and sha256 f142a9935d2730c01a80d98a619d2b297899c144f29ad16fd5c01aa1f493fcc2, which is exactly the digest the `[x]` line committed at `7d601c94` quotes, and the `accepted HEAD` value that same line carries, c96f82c3372520bfd0545c7ce640886479197a08, is an ancestor of the branch tip `8e08c0da` — so the STATUS line names a package that exists on disk and a commit that is really on the branch, rather than two values that merely agree with each other. TRANSPORT HELD THREE WAYS: `.remedy-wt/f255-r21.md`, `.agent/authored/f255-r21.md` at `779a8318` and `.agent/last_block.md` at `027537d1` are all sha256 a7d4a09cf30f997a78ca12409831f2f00ebba4b9995567e63ce407be6398afbb over 23516 B and 308 lines, and all three are EQUAL. ELEVEN SLICES, a count taken from the reviewer's own ordered extraction out of the committed C0a file and not from the handback, every newline-included digest matching: PLAN255R21 b46418e7, RECORDR20 0cab00fb, STATUSFROM 09dba254, STATUSTO 2c0c835f, COUNTFROM 93c8221e, COUNTTO b4eace4e, TIERFROM 06f358c5, TIERTO 1cc9fdd3, ACCEPTEDFROM 2413c959, ACCEPTEDTO 4246b906 and CANDIDATES c335c96a. THE PLAN LANDED FIRST at `2df7eab5`, byte-equal to PLAN255R21 at b46418e7 over 2046 B and 36 lines, under the 50-line cap, which is checklist item 23 met rather than merely claimed. THE R20 VERDICT IS RECORDED at `32401303` as a byte-exact prefix-plus-remainder append: the base blob is a prefix of the result, the remainder is 4133 B and equals a newline plus RECORDR20 exactly, and an INDEPENDENT blank-line split of the whole file into 216 units ends in that same paragraph — two extractors agreeing, with a deliberate one-byte mutation REJECTED by both readings, which is the negative control that makes the agreement worth stating. THE SETS DID NOT MOVE: 187 registered, 4 resolved, 183 open and 0 line-anchored `Landed:` at `a4f0fafd`, and the same four numbers at `32401303`, a `Gate:` paragraph being neither kind of line; 21 line-anchored `Gate: R` headers, all keys distinct, R21's last. ONE READING NEEDED ITS OWN SCOPE AND THE ROUND'S CLAUSE HAD IT RIGHT: the string `Gate: R21 — the R20 entry.` occurs once at `a4f0fafd` and twice at `32401303` as a bare SUBSTRING, because finding R-0587 quotes that header inside its own body, while the LINE-ANCHORED count the gate actually names reads 0 and then 1 — the R-0584 shape, in which a guard that cannot tell a quotation from a use is satisfied by the quotation, and the handback's sentence names the anchored reading rather than the substring one. THE FOUR PAIRS ARE ALL REWRITES, measured and not asserted: each FROM occurs once at `a4f0fafd` and zero times at `7d601c94` while each TO goes from zero to one, and the containment test prints `TO contains FROM: false` for all four, so none of them owes an append reading. THE COUNTS AGREE ACROSS TWO FILES: `docs/roadmap/STATUS.md` at `7d601c94` holds exactly one line-anchored `- [x] F255 — ` and zero `- [~] F255`, its total of line-anchored `- [x] F` entries is 53, README.md's stated N is 53, the two are EQUAL, and the README Tier 5 Done cell reads 1 against the single accepted id carrying a `T5_` feature file. THE SUITES ARE GREEN AND SERIAL, re-run by the reviewer in the primary checkout rather than read back: `tests/docs/` together with `tests/orchestration/test_roadmap_index.py` exit 0 at 325 passed, which is the 295 and the 30 the handback reported separately; the state-reader four exit 0 at 160 passed; the canary `tests/cli/test_golden_path.py` exits 0 at 42 passed. THE RANGE HOLDS: six single-parent commits over eight paths, with insertions 308, 240, 17, 2, 17 and 73, every one under the 500 cap; `docs/roadmap/features/T5_F255.md`, `.agent/decisions.md`, `apps/cli/commands/teach_cmd.py` and `packages/orchestration/teacher_model.py` are all PRESENT at `a4f0fafd` and ABSENT from the range, so the closure commit reached none of them; zero marker lines leaked into any target; the round's own six reflog entries carry no amend, rebase or cherry operation; and the tree is clean with `git worktree list` naming the primary checkout alone. TWO OBSERVATIONS ARE NOT DEVIATIONS and the worker was right to state both rather than pick a reading: C0b reads 240/333 under plain `git diff --numstat` and 308/401 under break-rewrite detection, both under the cap; and the review package contains `.remedy-wt/` scratch, which is the already-open R-0403 rather than a new condition of this closure. WHAT THIS ROUND PROVES ABOUT THE PROCESS is worth keeping beside what it shipped: R21 is the LAST round of the F255 branch, so the terminator of §4 item 13 applies and its verdict has no gate entry inside its own record — this paragraph, the first of the F008 record, IS that entry, written by the next reviewed round exactly as DECISION F085 D9 requires, and it is the concrete reason a branch may not end at a verdict without a following round to carry it.
<<<END GATE1

<<<SLICE STATUSFROM
- [ ] F008 — SSE event stream
<<<END STATUSFROM

<<<SLICE STATUSTO
- [~] F008 — SSE event stream
<<<END STATUSTO

<<<SLICE CONTEXTF008
# Context — F008 SSE event stream

## Active Branch
feature/f008-sse-event-stream, cut from `main` at the merge commit of pull
request #208, which this round merged at the Open PR Gate. Self-drive session
per docs/agents/self_drive_protocol.md: the main session plans and reviews and
writes nothing in the work tree, one delegated worker per round makes every
commit.

## Scope
In: a per-job SSE endpoint served by the existing UI server, carrying the
Part E envelope with the ledger's own monotonic seq as the event id, a 15 s
heartbeat frame, Last-Event-ID resume replaying the missed span out of the
ledger, 404 for an unknown job and a max-connections-per-job guard answering
429 beyond it; plus a client hook with reconnect backoff, gap detection, a
polling fallback on the same interface, and the status surface live,
reconnecting or delayed.

Out, per the feature file's Do not touch: command and write paths, the event
content and schema (Part E owns them) and the ledger format. Any POST surface
belongs to the NEXT feature and is rejected here.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, and a round
  rewriting `.agent/` state also gates the four files that read that state
  live: tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- THE SERVER-CAPABILITY FINDING GATES EVERYTHING: the feature file's
  Orchestrator brief dispatches it first, so R2 measures in the source whether
  ledger entries already carry a monotonic index and whether the UI server can
  hold a long-lived response without blocking every other request, and no
  endpoint is written before R3 rules the shape as a DECISION.
- This is a UI feature: docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority. Any deviation needs an
  assumption_log entry carrying a technical reason.
- Repository-wide `ruff check .` is RED at the claim and is NOT a gate
  (R-0364): the reviewer measured 26 errors at `8e08c0da` — 20 I001, 4 F401,
  1 UP035 and 1 F821. Ruff is gated scoped to the files a round touches,
  measured against the SAME files at the claim, so a pre-existing error is
  never read as a new one.
- 183 findings are open at this reset, all carried forward per DECISION F057
  D1, and none is a code defect of F008. R-0403, R-0607, R-0608, R-0609 and
  R-0611 stay routed to a paydown branch and are deliberately not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXTF008

<<<SLICE RESETSCRIPT
import hashlib
import pathlib
import re

LR = pathlib.Path(".agent/live_review.md")
AUTH = pathlib.Path(".agent/authored/f008-r1.md")
PRE_SHA = "4758a379bc258f1672ff76101b6c389ea1bf999dd25d49d6a89f913277768c0a"

src = LR.read_bytes()
got = hashlib.sha256(src).hexdigest()
print("pre-reset:", got, len(src), "B", src.count(b"\n"), "lines")
assert got == PRE_SHA, ("pre-reset record is not the expected bytes", got)


def slice_of(name):
    body = []
    keep = False
    for line in AUTH.read_text().splitlines(keepends=True):
        if line.startswith("<<<SLICE " + name):
            keep = True
        elif line.startswith("<<<END " + name):
            keep = False
        elif keep:
            body.append(line)
    assert body, ("empty slice", name)
    return "".join(body)


text = src.decode()
paras = text.split("\n\n")
assert "\n\n".join(paras) == text, "paragraph split does not round-trip"

registered = {}
order = []
for para in paras:
    m = re.match(r"^- (R-\d+) — ", para)
    if m:
        assert m.group(1) not in registered, ("duplicate id", m.group(1))
        registered[m.group(1)] = para
        order.append(m.group(1))

resolved = set(re.findall(r"^Done: (R-\d+) — ", text, re.M))
carried = [i for i in order if i not in resolved]
print("registered:", len(registered), "resolved:", len(resolved), "carried:", len(carried))
assert len(registered) == 187, len(registered)
assert len(resolved) == 4, len(resolved)
assert len(carried) == 183, len(carried)

out = slice_of("LRHEADER") + "\n" + "\n\n".join(registered[i] for i in carried)
out = out + "\n\n" + slice_of("GATE1")
data = out.encode()
LR.write_bytes(data)
print("post-reset:", hashlib.sha256(data).hexdigest(), len(data), "B", data.count(b"\n"), "lines")
<<<END RESETSCRIPT
