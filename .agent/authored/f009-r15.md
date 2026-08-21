── STEP T003 (round 1 of the five DECISION F009 D17 rules) — F009 ────────────
Goal:        Put the two package-level prerequisites of the dispatch on disk —
             the nonce store's publication bound (finding R-0637) and the audit
             vocabulary's `accepted` and `replayed` tokens — with their tests,
             and change the door not at all. The 501 seam still stands when this
             round ends, and `tests/ui_server/test_command_channel.py` is
             untouched by design.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R14 verdict ·
             C3 DECISION F009 D17 · C4 the publication bound and its tests ·
             C5 the audit vocabulary and its pin · C6 the `Landed:` line ·
             C7 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r15.md` (NEW, C0a)
             `.agent/last_block.md` (C0b)
             `.agent/plan.md` (C1)
             `.agent/live_review.md` (C2, C6)
             `.agent/decisions.md` (C3)
             `packages/orchestration/command_nonce.py` (C4)
             `tests/orchestration/test_command_nonce.py` (C4)
             `packages/orchestration/command_audit.py` (C5)
             `tests/orchestration/test_command_audit.py` (C5)
             `.agent/handoff.md` (C7)
             NOTHING under `apps/`, `docs/`, `tests/ui_server/` or
             `tests/cli/` is touched. `packages/orchestration/ui_server.py` is
             NOT edited this round: the dispatch is round 2.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it — an objection is cheaper than a silent edit.
 2. Every FROM/TO pair below was classified MECHANICALLY by the reviewer before
    emission, by testing whether the TO contains the FROM verbatim. The script
    printed `TO contains FROM: false` for ALL SIX pairs, so all six are
    REWRITES and each carries the FROM-0x / TO-1x obligation. NONE of them is
    an append, including `NONCE_TESTIMPORT`, whose TO keeps its anchor line but
    does not contain its FROM contiguously. `NONCE_TESTAPPEND` is not a pair at
    all: it is a code APPEND to the end of its file and carries the §4.9
    ordered-equality obligation instead.
 3. Each FROM below occurs EXACTLY ONCE in its target file at the round base;
    the reviewer counted each one. Replace that single occurrence.
 4. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and is not negotiable.
    C1 is the first substantive commit because this round writes the finding
    ledger and the plan must be current before it (§3 item 23).
 5. The reviewer's own dry run of C4 and C5 ran in a disposable worktree at the
    round base and is already green; the two red controls below were run there
    too. Reproduce the gates, do not trust this sentence.
 6. This round is SPLIT type: it changes `packages/`, so nothing here is
    self-certified.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C7: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a through C7. Report the round base SHA you read at
     step 0.
 G2  TRANSPORT: `.agent/authored/f009-r15.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received. Report
     sha256, byte count and line count for both. C0b is written FROM the
     committed C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its
     `<<<SLICE ` and `<<<END ` marker lines with a script, and apply them
     programmatically. Report each slice's sha256, bytes and lines, plus the
     aggregate count your script printed. Do not state a slice count you have
     not counted.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R15 — report `cmp` exit
     and both sha256 — and `wc -l` reads it against the 50-line cap of
     AGENTS.md. Line-anchored, `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, each under TWO independent readers with a negative control on its
     FIRST appended paragraph (finding R-0631). For C2 over
     `.agent/live_review.md` with the round base as base, and for C3 over
     `.agent/decisions.md` with the C2 commit's blob of that file as base:
     (a) the base blob is a byte-exact PREFIX and the remainder equals a
     newline plus the slice — report the remainder's sha256, bytes and lines;
     (b) N is counted BY YOUR SCRIPT, not asserted, and the last N blank-line
     units of the file equal the slice's N paragraphs IN ORDER. Then flip one
     printable byte in the FIRST appended paragraph and report that BOTH
     readers REJECT the flip while both accept the true file. Report the
     before/after byte and line counts. Nothing already in either file is
     edited.
 G6  Line-anchored over `.agent/live_review.md` at the round base and at C6
     (finding R-0630 — state that the anchor is line-start): `^- R-\d+ — ` with
     every captured id DISTINCT at each reading; `^Done: R-\d+ — `;
     `^Landed: R-\d+ — `; `^Gate: R\d+ — ` over that many DISTINCT keys; and
     `^Gate: R15 — `. Report each pair of readings and the max id. Report the
     open count by DECISION F009 D10's rule — line-anchored entries minus
     line-anchored `Done:` lines — at C6.
 G7  Line-anchored over `.agent/decisions.md` at the round base and at C3:
     `^## DECISION F009 D\d+ — ` with every captured number DISTINCT at each,
     `^## DECISION F009 D17 — `, and the `^## DECISION ` total.
 G8  PAIRS: for each of the six REWRITE pairs report, in the file it targets
     and at the commit that applies it, the FROM count reading 0 and the TO
     count reading 1, with the whole-line and the indent-agnostic counts BOTH
     taken and AGREEING. Then show that applying the three
     `command_nonce.py` pairs to the round-base blob in the order NONCE_CONST,
     NONCE_DOC, NONCE_PUB yields a file BYTE-EQUAL to what C4 landed, so no
     byte of that file changed beyond the authored pairs; do the same for
     `command_audit.py` with its single pair at C5.
 G9  APPEND, ordered equality (§4.9, finding R-0531), scoped to ONE path and
     read against BOTH changes C4 makes to it (finding R-0615). C4 changes
     `tests/orchestration/test_command_nonce.py` in two ways — the
     NONCE_TESTIMPORT rewrite and the NONCE_TESTAPPEND append — so the
     round-base blob is NOT a prefix of the result and this gate does not claim
     it is; the reviewer measured that and it reads false. Prove instead, in
     three separate readings: take the round-base blob of that path, apply
     NONCE_TESTIMPORT to it ALONE, and show (i) the result is a byte-exact
     PREFIX of the file C4 landed, (ii) NONCE_TESTAPPEND is an exact SUFFIX of
     that landed file, and (iii) the landed file EQUALS that prefix followed by
     that slice with NOTHING between them. Report all three.
 G10 SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes
     at once, and never in a worktree. Report each command's REAL exit code and
     the count IT printed — predict no number:
       `python3 -m ruff check packages/orchestration/command_nonce.py
        packages/orchestration/command_audit.py
        tests/orchestration/test_command_nonce.py
        tests/orchestration/test_command_audit.py`
       `python3 -m pytest tests/orchestration/test_command_nonce.py
        tests/orchestration/test_command_audit.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The canary is unconditional and the four-path group is owed because this
     round's change set holds `.agent/` state files (finding R-0607). The
     reviewer measured the first two at the round base before ordering them:
     ruff exits 0 and the pair of suites exits 0, so both can fail honestly.
 G11 RED CONTROLS, in a DISPOSABLE worktree only, never in the primary
     checkout, removed and pruned afterwards — report `git worktree list`:
     (a) Run this control at C4, NOT at the round base: the bytes it removes do
         not exist before C4 creates them. In
         `packages/orchestration/command_nonce.py` delete the two lines
         `    if len(raw) > MAX_NONCE_RECORD_BYTES:` and `        return None`
         that directly follow the line `    raw = _record_bytes(record)`. The
         reviewer measured that three-line sequence AS C4 LANDS IT at exactly
         1 occurrence in that file, whole-line and indent-agnostic readings
         both reading 1 (§3 item 25); the bare line `    return None` occurs 14
         times there, which is why the control names the three-line sequence
         and not that line. Re-run the nonce suite and report WHICH node ids
         fail and the colour — report no count you were given. Restore the
         worktree.
     (b) Run this control at C5. In `packages/orchestration/command_audit.py`
         delete the two lines `    "accepted",` and `    "replayed",` from
         `OUTCOMES`. The reviewer measured that two-line sequence AS C5 LANDS
         IT at exactly 1 occurrence, both readings agreeing. Re-run
         `tests/orchestration/test_command_audit.py` and report which node id
         fails and the colour.
     Both controls exist because a suite that cannot go red proves nothing when
     it is green.
 G12 RANGE: the range from the round base to C6 lists EXACTLY the nine declared
     paths other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and holds 0 paths beginning `apps/`, `docs/`,
     `tests/ui_server/` or `tests/cli/` and 0 equal to
     `packages/orchestration/ui_server.py`. Each commit has ONE parent;
     `git show --numstat` and `git diff --numstat` AGREE on every cell; every
     cell equals the `+/-` column of the handback's `## Commits` table (§3 item
     28) — compare them cell by cell and say so. Report each pre-handback
     commit's insertions against the 500 cap of AGENTS.md DECISION F104 D1; the
     handback commit's own numbers belong in the round report, not here (§3
     item 14). `^<<<SLICE ` and `^<<<END ` read 0 lines in ALL SIX committed
     targets. `git ls-files .remedy-wt` reads 0. Classify THIS ROUND's reflog
     rows by the operation before the first `:` and report `amend`, `rebase`
     and `cherry` each reading 0; assert no total over the whole reflog
     (finding R-0601).
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status table with exactly one
     row for each of C0a, C0b, C1, C2, C3, C4, C5, C6 and C7, the round base
     SHA, one line per gate with the transcripts in the round report rather
     than in the file (finding R-0582), and the Fortschritt line verbatim.
     Report its `wc -l` against the 100 lines a bundle of more than five
     commits allows.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C7.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R15
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R15 lands the two package-level prerequisites of the dispatch and changes the
door not at all. The nonce store refuses an oversize record AT PUBLICATION,
which pays R-0637, and `command_audit.OUTCOMES` gains the `accepted` and
`replayed` tokens the door will write next round. The 501 seam still stands.

## Next Steps
1. `job.stop` dispatches to `safe_points.request_stop`, writing `accepted` and
   publishing the nonce record; the replay audit moves to `replayed`, which
   pays R-0636. `tests/ui_server/test_command_channel.py` migrates its seam
   pins in that same round. `decision.resolve` keeps answering 501.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure. DECISION F009 D17 carries the ordering.

## Risks
- Splitting by command means the door briefly dispatches one exposed id and
  refuses the other with 501. That is honest — `not_implemented` is what the
  audit records for a command this door has not yet dispatched — but the tests
  must assert it deliberately rather than inherit it.
- `accepted` and `replayed` enter the vocabulary a round before any caller
  writes them. `tests/ui_server/test_command_channel.py` still asserts the door
  writes no `accepted`, which stays true and is what keeps the gap honest.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R15

<<<SLICE LEDGER15
Gate: R15 — the R14 entry. R14 PASSED. The round wrote no production code, which is what it existed for, and every value it reported reproduced under the reviewer's own re-execution off disk rather than being read back out of the handback. TRANSPORT HELD: `.agent/authored/f009-r14.md` at `6d1df108` and `.agent/last_block.md` at `17f7a75b` are both sha256 654dfd57dbf72a9dae005417f1594ac9e4136af4cd9acec2df30d7295b143abb over 21051 bytes and 208 lines, equal as bytes and equal to the digest the round declared. THE SLICES ARE THE REVIEWER'S OWN ORDERED EXTRACTION out of the committed C0a blob: exactly PLANF009R14 `d22036cc…` 2550 B 43 L, LEDGER14 `82e6f1c0…` 5086 B 1 L and DECISION16 `9f8e2c4c…` 3607 B 13 L, aggregating to 11243 bytes over 57 lines. `.agent/plan.md` at `130c2ef3` is BYTE-EQUAL to PLANF009R14 at 43 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` reading 1 each and `F009` the first `\bF\d{3}\b` match. BOTH APPENDS HOLD UNDER BOTH READERS WITH THE REVIEWER'S OWN NEGATIVE CONTROLS: at `dd6cdfe8` the live-review base blob is a byte-exact prefix and the remainder is a newline plus LEDGER14, sha256 `1a542238…` over 5087 bytes and 2 lines, the file going 458487 to 463574 bytes and 1084 to 1086 lines; at `5a8fb3b0` the decisions base blob is a byte-exact prefix and the remainder is a newline plus DECISION16, sha256 `eeb7a60c…` over 3608 bytes and 14 lines, the file going 442327 to 445935 bytes and 6797 to 6811 lines; the paragraph reader counted N as 1 and 7 respectively and matched the appended units in order, and a single flipped printable byte in the FIRST appended paragraph of each was REJECTED by both readers while both accepted the true file. THE SETS HELD line-anchored at the round base and at C2: `^- R-\d+ — ` 203 and 203 with every id DISTINCT at each, `^Done: R-\d+ — ` 2 at both, `^Landed: ` 0 at both, `^Gate: R\d+ — ` 13 and 14 over that many DISTINCT keys, `^Gate: R14 — ` 0 and 1, max id R-0637, and 201 open by DECISION F009 D10's rule. THE DECISIONS FILE HELD: `^## DECISION F009 D\d+ — ` 15 and 16 with every number DISTINCT, `^## DECISION F009 D16 — ` 0 and 1, and the `^## DECISION ` total 100 and 101. THE HEADER MATCHES THE SHAPE IT JOINS: of the 14 `Gate: ` lines at C2, 13 read `Gate: R<n> — the R<n-1> entry.` and the one that does not is `Gate: R1 — the F008 R36 entry.`, which records the previous feature's closing verdict and has no R0 to name — so the ledger gained no duplicate key (§3 item 26). THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 507 passed, the same two numbers the handback reported and neither of them predicted. THE RANGE HELD, walked by the reviewer: six single-parent commits over exactly the five declared paths plus the handback's own, the set difference empty in both directions and 0 paths under `packages/`, `apps/`, `tests/` or `docs/`, which is the no-production-code constraint as a measurement; insertions 208, 121, 19, 2 and 14 for the five pre-handback commits, every one under the 500 cap; `^<<<SLICE ` and `^<<<END ` reading 0 in all three committed targets; `git ls-files .remedy-wt` 0; and one worktree, the primary checkout alone. THE VERDICT TEXT IT CARRIED IS ITSELF TRUE, which a shape gate cannot reach and the reviewer therefore measured: LEDGER14's R13 claims reproduce — `.agent/authored/f009-r13.md` at `97f364be` and `.agent/last_block.md` at `19aec738` are both sha256 23b45930601cfdfe083f267acb946475c378f41c24331daa7ca4aaa380a63ed8 over 23444 bytes and 351 lines, its nine slices aggregate to 11031 bytes over 149 lines, `.agent/plan.md` at `f9c51774` is byte-equal to PLANF009R13 at 41 lines, `packages/orchestration/flight_plan.py` at `c204f0b5` is sha256 2298635f1e4151f8d9712786b7d5224223bc642f8cb3c95d6f123cb858a1730d, R13's per-commit insertions are 351, 286, 17, 2, 49 and 34, and its handback is 82 lines. DECISION F009 D16'S OWN MEASUREMENT IS TRUE TOO: `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` at `1e7539be` holds exactly `job.stop` and `decision.resolve`, and `resolve_flight_plan_approval` is defined in `packages/orchestration/flight_plan.py` at `c204f0b5`. NO FINDING is registered against R14.
<<<END LEDGER15

<<<SLICE DECISION17
## DECISION F009 D17 — D16's first round splits in two, and the audit vocabulary lands a round before its writer (2026-08-22)

Measured at `de1e5c00` by the reviewer, before this round was delegated: retiring the 501 seam for `job.stop` alone moves far more than the door. `tests/ui_server/test_command_channel.py` mentions the literal `501` on 21 lines, and its `_post_command` helper submits `job.stop` by default — `test_the_seam_is_audited_as_not_implemented` asserts exactly that — so roughly seventeen pinned sites change status the moment that one id dispatches, including `test_every_exposed_command_reaches_the_seam`, which loops over both exposed ids and must split because after that round one of them dispatches and the other still answers 501. Two further pins sit outside that file: `tests/orchestration/test_command_audit.py` fixes `OUTCOMES` as an exact tuple and separately asserts `"accepted" not in OUTCOMES`.

CHOSEN: DECISION F009 D16's FIRST round becomes two, so D16's four become five and nothing else in its ordering changes. Round one — this one — lands only what the dispatch DEPENDS on, with no door edit at all: the nonce store's publication bound, which pays R-0637, and the `accepted` and `replayed` tokens in `command_audit.OUTCOMES` with the pin that fixes them. Round two edits `packages/orchestration/ui_server.py`, migrates the seam pins in `tests/ui_server/test_command_channel.py` and pays R-0636. Rounds three, four and five are D16's second, third and fourth unchanged.

WHY, measured rather than estimated: DECISION F085 D6 caps a step block at 490 lines TOTAL. The dispatch, the publication call site, the two finding fixes and roughly seventeen test-pin migrations do not fit in one, and D16 itself rules that a block which does not fit is not delivered — it becomes a declared deviation on a round that did nothing wrong. The cut also keeps D16's own criterion intact: each round is independently testable end to end. This one ships two package functions with their own tests and leaves the door provably unchanged, which is a stronger property than a half-wired dispatch, not a weaker one.

WHY THE VOCABULARY MOVES EARLY, and why that is not a claim about behaviour. `accepted` and `replayed` enter the closed set here while NO caller writes either, and the door's own guard — `tests/ui_server/test_command_channel.py` asserting that no record the door wrote carries `accepted` — stays TRUE and unedited, which is what keeps the gap visible rather than papered over. The reviewer ran that file against this change in a disposable worktree at the round base and it passed unmodified. Landing the vocabulary here buys round two a change set of one production file and one test file.

WHY R-0637 IS PAID HERE THOUGH ITS OWN FIX CLAUSE SAYS OTHERWISE. That clause reads "owed by the round that retires the seam, in the same commit that adds the publish call site". Paying it one round EARLIER is strictly stronger and not a deviation from its intent: the bound is in force BEFORE any door path can reach publication, so the window in which an unreplayable record could be written is never opened rather than merely closed on arrival. R-0636 does NOT move, because its fix genuinely depends on the door caller it names.

ALTERNATIVES: (a) keep D16's four rounds and let the first exceed the block cap — rejected on the cap, which is a measurement and not a preference. (b) split by LAYER instead, landing a dispatch module first — rejected for the same reason D16 rejected it: DECISION F009 D5 rules that the handler imports the effect functions directly and that the import guard asserts exactly that set. (c) migrate the seam pins in THIS round and dispatch in the next — rejected because a test pinning a status the door does not yet return is a test asserting a falsehood, and the suite would have to be red between the two rounds.

REVERSE by collapsing rounds one and two back into a single block, which is possible only if DECISION F085 D6's cap changes; the effect mapping comes from D5 and the round ordering from D16, and neither is altered here.
<<<END DECISION17

<<<SLICE NONCE_CONST_FROM
#: A record this large is a bug in the caller, not a response. Matches the door's own
#: request ceiling, so nothing that fits through the door fails to fit in the store.
MAX_NONCE_RECORD_BYTES = 64 * 1024
<<<END NONCE_CONST_FROM

<<<SLICE NONCE_CONST_TO
#: A record this large is a bug in the caller, not a response. It bounds the RESPONSE this
#: store holds — a body the door composed — and not the request the client sent, which is a
#: different quantity that merely shares the door's ceiling (finding R-0637).
#: `publish_nonce_result` refuses an oversize record instead of writing one, because
#: `_read_record` refuses it at every later lookup and it could never be replayed.
MAX_NONCE_RECORD_BYTES = 64 * 1024
<<<END NONCE_CONST_TO

<<<SLICE NONCE_DOC_FROM
    status it was returned with, because a replay has to reproduce both. `None` means
    nothing is in force: an unusable nonce, a job id that is not one, or a control directory
    that could not be reached.
<<<END NONCE_DOC_FROM

<<<SLICE NONCE_DOC_TO
    status it was returned with, because a replay has to reproduce both. `None` means
    nothing is in force: an unusable nonce, a job id that is not one, a record larger than
    `MAX_NONCE_RECORD_BYTES`, or a control directory that could not be reached.
<<<END NONCE_DOC_TO

<<<SLICE NONCE_PUB_FROM
    record = {"status": int(status), "body": body}
    dir_fd = _open_nonce_dir_fd(jid, control_root_path, create=True)
    if dir_fd is None:
        return None
    try:
        published = _fs.write_file_atomically(
            dir_fd, _record_name(nonce), _record_bytes(record),
            create_only=True, file_mode=NONCE_FILE_MODE,
            error_cls=safe_points.StopControlError, noun="command nonce record")
<<<END NONCE_PUB_FROM

<<<SLICE NONCE_PUB_TO
    record = {"status": int(status), "body": body}
    # Finding R-0637: the bound is enforced HERE, where the record is written, and not in
    # `_read_record` alone. An oversize record is refused by every later lookup, so
    # publishing one leaves a nonce that can never be replayed and a client whose retry
    # silently re-executes the command instead of being answered. Refusing at publication
    # returns None, which is what every other unusable input to this function returns.
    raw = _record_bytes(record)
    if len(raw) > MAX_NONCE_RECORD_BYTES:
        return None
    dir_fd = _open_nonce_dir_fd(jid, control_root_path, create=True)
    if dir_fd is None:
        return None
    try:
        published = _fs.write_file_atomically(
            dir_fd, _record_name(nonce), raw,
            create_only=True, file_mode=NONCE_FILE_MODE,
            error_cls=safe_points.StopControlError, noun="command nonce record")
<<<END NONCE_PUB_TO

<<<SLICE NONCE_TESTIMPORT_FROM
from packages.orchestration.command_nonce import (
    NONCE_DIRNAME,
<<<END NONCE_TESTIMPORT_FROM

<<<SLICE NONCE_TESTIMPORT_TO
from packages.orchestration.command_nonce import (
    MAX_NONCE_RECORD_BYTES,
    NONCE_DIRNAME,
<<<END NONCE_TESTIMPORT_TO

<<<SLICE NONCE_TESTAPPEND


# -- the publication bound (finding R-0637) --------------------------------------------


def test_a_record_over_the_bound_is_refused_at_publication(control: Path) -> None:
    """The write side had no negative control at all: a record that can never be replayed
    must never be written. `_read_record` refuses anything above the bound, so publishing
    one would turn idempotency OFF for that nonce with no error anywhere."""
    oversize = {"filler": "x" * (MAX_NONCE_RECORD_BYTES + 1)}
    assert publish_nonce_result(
        JOB, NONCE, oversize, status=200, control_root_path=control) is None
    assert lookup_nonce_result(JOB, NONCE, control_root_path=control) is None
    assert not record_path(control).exists()


def test_a_record_at_the_bound_still_publishes(control: Path) -> None:
    """The refusal is an upper bound and not an off-by-one: a record whose serialised form
    is exactly `MAX_NONCE_RECORD_BYTES` long publishes and reads back. The padding is
    solved for with the serialiser production itself uses, so this arithmetic cannot drift
    away from `_record_bytes`."""
    def sized(filler: int) -> int:
        return len(_fs.json_bytes({"status": 200, "body": {"filler": "x" * filler}},
                                  indent=None, sort_keys=False))

    pad = MAX_NONCE_RECORD_BYTES - sized(0)
    assert sized(pad) == MAX_NONCE_RECORD_BYTES
    body = {"filler": "x" * pad}
    published = publish_nonce_result(
        JOB, NONCE, body, status=200, control_root_path=control)
    assert published == {"status": 200, "body": body}
    assert record_path(control).stat().st_size == MAX_NONCE_RECORD_BYTES


def test_the_bound_refuses_before_the_store_is_created(control: Path) -> None:
    """An oversize record must not leave the nonce directory behind as litter: the refusal
    happens before `_open_nonce_dir_fd` is reached, which is why it is ordered that way."""
    oversize = {"filler": "x" * (MAX_NONCE_RECORD_BYTES + 1)}
    assert publish_nonce_result(
        JOB, NONCE, oversize, status=200, control_root_path=control) is None
    assert not nonce_dir(control).exists()
<<<END NONCE_TESTAPPEND

<<<SLICE AUDIT_OUTCOMES_FROM
#: DECISION F009 D14's closed vocabulary. Each token names the CHECK that refused, never
#: the client's message, so a wording change cannot drift the vocabulary. `accepted` is
#: reserved for the round that retires the 501 seam: nothing is accepted while that stands.
OUTCOMES = (
    "rejected_token",
    "rejected_csrf",
    "rejected_job",
    "rejected_shape",
    "rejected_command",
    "rejected_rate",
    "not_implemented",
)
<<<END AUDIT_OUTCOMES_FROM

<<<SLICE AUDIT_OUTCOMES_TO
#: DECISION F009 D14's closed vocabulary. Each token names the CHECK that refused, never
#: the client's message, so a wording change cannot drift the vocabulary. `accepted` and
#: `replayed` are the two NO caller writes yet: DECISION F009 D17 lands the vocabulary one
#: round ahead of the dispatch that writes them, so the round retiring the 501 seam changes
#: the door alone. `replayed` is deliberately distinct from `accepted` (finding R-0636): a
#: replay REPEATS an acceptance rather than being one, and T5_F035 and T9_F167 both read
#: this file to count what the door did, so one token for both would make them
#: indistinguishable to the two features that care.
OUTCOMES = (
    "rejected_token",
    "rejected_csrf",
    "rejected_job",
    "rejected_shape",
    "rejected_command",
    "rejected_rate",
    "not_implemented",
    "accepted",
    "replayed",
)
<<<END AUDIT_OUTCOMES_TO

<<<SLICE AUDIT_TEST_FROM
def test_the_outcome_vocabulary_is_the_closed_set_d14_ruled() -> None:
    """`accepted` is deliberately ABSENT: nothing is accepted while the 501 seam stands."""
    assert OUTCOMES == (
        "rejected_token",
        "rejected_csrf",
        "rejected_job",
        "rejected_shape",
        "rejected_command",
        "rejected_rate",
        "not_implemented",
    )
    assert "accepted" not in OUTCOMES
    assert len(set(OUTCOMES)) == len(OUTCOMES)
<<<END AUDIT_TEST_FROM

<<<SLICE AUDIT_TEST_TO
def test_the_outcome_vocabulary_is_the_closed_set_d14_ruled() -> None:
    """The closed set, in order. `accepted` and `replayed` are DECISION F009 D17's pair."""
    assert OUTCOMES == (
        "rejected_token",
        "rejected_csrf",
        "rejected_job",
        "rejected_shape",
        "rejected_command",
        "rejected_rate",
        "not_implemented",
        "accepted",
        "replayed",
    )
    assert "accepted" in OUTCOMES
    assert "replayed" in OUTCOMES, "a replay is not the acceptance it repeats (R-0636)"
    assert len(set(OUTCOMES)) == len(OUTCOMES)
<<<END AUDIT_TEST_TO
