STEP T001a/1 — F109 Semantic dedupe (round 1, session 1)

Goal: claim F109 in the roadmap ledger, discharge the one open closure
candidate F108 left behind, and land T001a — the PURE per-session
sent-hash index and its unit tests.

SCOPE RULE, quoted verbatim in every F109 order per the feature file's
Orchestrator brief: RESUMED SESSION ONLY, PROVEN SENDS ONLY.

Base commit: 5e18a8536afa086b591b5a2e13009d68d6227432 (tip of `main`,
pull request 231 merged). Open PR Gate: `gh pr list --state open` returns
the empty list at that commit, so no merge is owed and none is permitted
this round.

Branch to create, from `main` at the base commit above:
feature/f109-semantic-dedupe

Bundle (one commit per item, in this order):
  C0a. Save this entire step block verbatim to `.agent/authored/f109-r1.md`.
  C0b. Mirror it byte-for-byte to `.agent/last_block.md`.
  C1.  `.agent/plan.md` <- SLICE PLAN, whole-file replacement. This is the
       FIRST substantive commit of the round because the round touches the
       finding ledger (docs/agents/planner_reviewer_prompt.md §3 item 23).
  C2.  `docs/roadmap/STATUS.md` <- the STATUSFROM/STATUSTO pair, AND
       `.agent/context.md` <- SLICE CONTEXT, whole-file replacement. One
       commit: the claim and the context that describes it are one act.
  C3.  `.agent/live_review.md` <- SLICE RECORD, appended, AND
       `.agent/candidates.md` <- SLICE CANDIDATES, whole-file replacement.
       One commit: registering the candidate and emptying the carrier it
       came from are one act, and the closure protocol requires both in
       the same round.
  C4.  NEW FILE `packages/orchestration/session_sent_index.py`, written to
       SPEC M below. No other file is touched by this commit.
  C5.  NEW FILE `tests/orchestration/test_semantic_dedupe.py`, written to
       SPEC T below. No other file is touched by this commit.
  C6.  `.agent/handoff.md` <- rewritten per AGENTS.md `### handoff.md`,
       reporting the REAL results of gates G1 through G8, every one of
       which runs at C5 or earlier.
  Then: `git push -u origin feature/f109-semantic-dedupe`. The push happens
  AFTER C6, so the handback does NOT quote its result; the reviewer
  measures the remote tip itself.

Exact change set for this round. These paths and NO others:
  `.agent/authored/f109-r1.md`   new
  `.agent/last_block.md`          rewritten
  `.agent/plan.md`                rewritten
  `docs/roadmap/STATUS.md`        one line rewritten
  `.agent/context.md`             rewritten
  `.agent/live_review.md`         one paragraph appended
  `.agent/candidates.md`          rewritten
  `packages/orchestration/session_sent_index.py`   new
  `tests/orchestration/test_semantic_dedupe.py`    new
  `.agent/handoff.md`             rewritten

Constraints:
  1. Apply every SLICE byte-for-byte. If a slice looks wrong, apply it
     anyway and DECLARE the problem in the handback's deviations. Never
     silently repair a slice; never edit one to fit.
  2. Touch no path outside the change set above. No "while I'm here" edits.
  3. The pair in C2 was tested mechanically before emission. Its reading:
     TO contains FROM: false. It is therefore a REWRITE, and its proof is
     the FROM-0x / TO-1x count in `docs/roadmap/STATUS.md` after C2.
  4. SLICE RECORD is APPENDED, never inserted and never overwriting.
     `.agent/live_review.md` at the base commit ends WITHOUT a trailing
     newline — its last three bytes are `EN.` — so the append is exactly
     the two bytes `\n\n` followed by the slice's bytes, and the file
     still ends without a trailing newline afterwards.
  5. Production code is described by SPEC, not sliced: you AUTHOR the
     Python in C4 and C5 to the specification below. Naming, docstrings
     and structure are yours to write; every behaviour named in the SPEC
     is mandatory and nothing beyond it may be added.
  6. No round of F109 gates on `ruff`: this session's reviewer cannot
     execute it and a gate whose result rests on your word alone is not
     evidence. Follow the repository's ruff configuration by construction
     instead — line length 120, and imports grouped stdlib, then
     third-party, then first-party (`packages.…`), matching the layout of
     `packages/orchestration/prompt_segments.py`.
  7. Destructive verification (G6) runs ONLY inside a disposable
     `git worktree`, which is DISCARDED afterwards rather than reverted.
     The primary checkout is never mutated, so `git status --porcelain` is
     empty at every commit and at the end of the round.
  8. Every commit's insertion count stays under 500 (AGENTS.md DECISION
     F104 D1 — the `+` column only).
  9. Three PROPERTY GUARDS already sweep every `*.py` under
     `packages/orchestration/`, so the new module in C4 must satisfy all
     three by construction. The reviewer read them at the base commit and
     names them here so they cannot surprise the round:
     `test_no_shell_true_in_orchestration` (AST: no `shell=True`),
     `test_no_0000_in_production` (no `0.0.0.0`) and
     `test_no_bad_permit_order_in_production` (no `allow repo_test_run`,
     `allow repo_generated_write` or `allow workspace_write`), all in
     `tests/orchestration/test_test_runner.py`. SPEC M's module is a pure
     data structure and satisfies all three trivially; this constraint
     exists so a later edit does not quietly break one. None of the three
     is a closed-set or count guard, so ADDING a module to that directory
     is safe — the reviewer checked for that class specifically.

SPEC M — `packages/orchestration/session_sent_index.py`, new module.

  PURPOSE. Remember which prompt segments have PROVABLY been delivered to
  a given provider session, so that a later call which RESUMES that same
  session can skip resending them. This module is the bookkeeping half of
  F109 and nothing else.

  PURITY, and it is load-bearing. The module reads no file, writes no
  file, touches no network, calls no provider and imports nothing from
  `packages.orchestration` except type hints it genuinely needs. It is a
  data structure with rules. Persisting the index into the job's evidence
  is T001b and is deliberately absent here; say so in the module docstring
  where a reader would search for it, per AGENTS.md "Deliberate absences
  are documented where a reader would search for them".

  The module docstring also states the scope rule verbatim: RESUMED
  SESSION ONLY, PROVEN SENDS ONLY.

  PUBLIC API. Exactly these names, and no others:

    `SessionSentIndexError(Exception)` — the one error type of the module.

    `SessionSentIndex` — the index. Construct with no arguments to an
    empty index. Methods:

      `record_call(session_id, manifest_rows, *, ok)` -> int
        Record the segment hashes of ONE finalized call. `manifest_rows`
        is the sequence of mappings that
        `ComposedPrompt.manifest_as_dicts()` returns — each row carries a
        `"sha256"` key whose value is the hex digest of that segment's
        text. Returns the number of hashes this call added that the
        session did not already hold.
        RECORDS NOTHING AT ALL, and returns 0, when `ok` is False: a call
        that did not succeed did not reach the session, and an index that
        guesses otherwise is the exact dishonesty this feature forbids.
        RECORDS NOTHING AT ALL, and returns 0, when `session_id` is not a
        non-empty string after stripping: a call with no session has no
        session to remember, and an empty key would become a bucket every
        sessionless call shares — a cross-session leak by construction.
        Neither of those two cases is an error; both are ordinary and
        both are silent.
        RAISES `SessionSentIndexError` when a row is not a mapping, when
        it has no `"sha256"` key, or when that value is not a non-empty
        string. A malformed manifest is a programming error, not a
        routine condition, and it must not degrade into a silently
        smaller index.

      `sent_hashes(session_id)` -> frozenset[str]
        Every hash proven sent to that session. An unknown or empty
        session id yields the EMPTY frozenset, never an error and never
        another session's set.

      `was_sent(session_id, sha256)` -> bool
        True only when that exact session already holds that exact hash.

      `invalidate_session(session_id)` -> None
        Drop that session's set entirely. This is the resume-fallback
        safety valve: once a resume attempt has fallen back to full
        context, nothing about what the model still holds is proven any
        more. An unknown session id is a silent no-op, NOT an error — a
        fallback can fire before any call to that session ever succeeded.

      `session_ids()` -> tuple[str, ...]
        Every session id the index holds, SORTED, so evidence written
        from this index is deterministic rather than dict-ordered.

      `as_evidence_dicts()` -> list[dict]
        JSON-ready rows, one per session, sorted by session id:
        `{"session_id": <str>, "sent_sha256": [<hashes, sorted>]}`.
        Sorting both levels is what makes two runs with the same sends
        produce byte-identical evidence.

    `session_sent_index_from_evidence(rows)` -> SessionSentIndex
      Rebuild an index from what `as_evidence_dicts()` produced. Raises
      `SessionSentIndexError` on a row that is not a mapping, a row whose
      `"session_id"` is not a non-empty string, or a `"sent_sha256"` value
      that is not a sequence of non-empty strings. This is the restart
      honesty seam: an index rebuilt after a process restart contains
      exactly what the evidence proves and never more.

SPEC T — `tests/orchestration/test_semantic_dedupe.py`, new test file.

  Hermetic and pure: no `tmp_path`, no network, no provider, no sleep.
  Group the tests in classes by behaviour. Every test name says what it
  asserts. These cases are mandatory:

   1. A successful call records every hash in its manifest for its
      session. Build the manifest for this ONE test through the REAL
      producer — register segments on a `PromptSegmentRegistry` from
      `packages.orchestration.prompt_segments`, compose them with
      `compose_prompt_segments`, and feed `manifest_as_dicts()` — so the
      module is pinned against the manifest shape that actually ships
      rather than against a hand-made dictionary.
   2. A call with `ok=False` records NOTHING, and the session's set stays
      empty. This is the restart-honesty case: an unproven send is absent.
   3. A call whose `session_id` is the empty string, and a call whose
      `session_id` is whitespace only, each record NOTHING.
   4. Two different session ids keep DISJOINT sets: a hash recorded for
      session A is not `was_sent` for session B, even when both calls
      carried the identical segment text. This is the negative test the
      feature's Acceptance section requires — dedupe never crosses
      session ids.
   5. `invalidate_session` clears exactly the named session and leaves
      every other session's set untouched.
   6. `invalidate_session` on a session id the index has never seen is a
      no-op and raises nothing.
   7. Recording the same manifest twice is idempotent: the set is
      unchanged and the second `record_call` returns 0.
   8. An evidence round trip preserves every session and every hash:
      `session_sent_index_from_evidence(index.as_evidence_dicts())`
      yields the same `session_ids()` and the same `sent_hashes()` for
      each, and `as_evidence_dicts()` of the rebuilt index equals that of
      the original.
   9. `as_evidence_dicts()` is deterministic: two indexes built by
      recording the same sessions in OPPOSITE order produce equal output.
  10. `record_call` raises `SessionSentIndexError` for a manifest row
      with no `"sha256"` key, and for one whose `"sha256"` is the empty
      string.
  11. `session_sent_index_from_evidence` raises `SessionSentIndexError`
      for a row with no `"session_id"`, and for a `"sent_sha256"` that is
      not a sequence of non-empty strings.
  12. `was_sent` is False for a session the index has never seen.

Done when — GATES. Run every one of them and record its REAL exit code and
output. "Green" as a word is a finding. Gates G1 through G8 all run at C5
or earlier, so C6 can quote every one of them. Report ONE LINE PER GATE in
the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r1.md .agent/last_block.md`
     — the two digests must be equal to each other AND equal to
     `SHA256_OF_THIS_BLOCK` as stated by the reviewer in the delegation
     wrapper. Report the digest. Runs at C0b.

  G2 THE PLAN. At C1: `.agent/plan.md` is byte-equal to SLICE PLAN
     (compare with `cmp` against a scratch copy of the slice under
     `.remedy-wt/`, never a retype); `wc -l` is strictly under 50;
     `grep -c '^## Goal$'` is 1 and `grep -c '^## Next Steps$'` is 1.

  G3 THE CLAIM AND THE CONTEXT. At C2, in `docs/roadmap/STATUS.md`:
     `grep -c '^- \[~\] F109 — Semantic dedupe$'` is 1;
     `grep -c '^- \[ \] F109'` is 0;
     `grep -c '^- \[x\] F'` is UNCHANGED from its value at the base
     commit — measure it at the base FIRST and report both numbers;
     `grep -c '^- \[~\] F'` over the whole file is 1, which is what
     `tests/docs/test_docs_consistency.py` line 328 caps.
     And `.agent/context.md` is byte-equal to SLICE CONTEXT by `cmp`.

  G4 THE LEDGER APPEND. At C3, over `.agent/live_review.md`:
     (a) BYTE ARITHMETIC. Its size must be exactly 2015028 + 2 + S, where
         2015028 is the base size and S is the byte length of SLICE
         RECORD as saved to scratch. Report all three numbers. The base
         sha256 is c3fa642ece4f90819e2ec7c73e29bc1d574dcf160e726e660e3ab05a937d588e.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER. Split the whole file on
         blank lines into units. COUNT the paragraphs in SLICE RECORD
         yourself — call that N, do not take a number from this block —
         and assert the LAST N units of the file equal those N
         paragraphs, in order.
     (c) NEGATIVE CONTROL. On a SCRATCH COPY under `.remedy-wt/`, flip one
         byte inside the FIRST appended paragraph and confirm that reader
         (b) REJECTS the mutated copy. The tracked file is never mutated;
         report that its sha256 is identical before and after the control.
     (d) COUNTS. `grep -c '^- R-[0-9]\{4\} — '` goes from 329 to 330 and
         `grep -c '^- R-0769 — '` is exactly 1;
         `grep -c '^Done: R-[0-9]\{4\} — '` is UNCHANGED at 62.

  G5 THE CANDIDATES CARRIER. At C3: `.agent/candidates.md` is byte-equal
     to SLICE CANDIDATES by `cmp`; `grep -c 'R-0769'` is 1;
     `grep -c '^## Open candidates$'` is 0 — the section that held the
     open entry is gone, which is what "empties the file" means here.

  G6 THE COLOUR OF THE NEW CODE. Inside a DISPOSABLE `git worktree` added
     at the round's C5 commit, never in the primary checkout:
     (a) CONTROL FIRST. Run
         `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`
         UNMUTATED. Record the real exit code and the passed count. A
         colour with no baseline is not evidence.
     (b) MUTATION A. In `session_sent_index.py`, make `record_call` ignore
         its `ok` argument and record regardless. Re-run the same command.
         It MUST fail, and the failing test must be the `ok=False` case of
         SPEC T item 2. Report the exit code and the failing test names.
     (c) MUTATION B. Restore, then make `record_call` accept an empty
         `session_id` as an ordinary key. Re-run. It MUST fail on the
         SPEC T item 3 cases. Report the exit code and failing names.
     Purge `__pycache__` before each run and use `python3 -B`, so no
     stale bytecode can mask a mutation. Then
     `git worktree remove --force` the worktree and `git worktree prune`;
     report `git worktree list` afterwards.

  G7 THE SUITES. At C5, run these SEVEN commands SERIALLY — never two
     pytest processes alive at once — and report each one's real exit code
     and count. The base counts, measured by the reviewer at the base
     commit, are given so any drift is visible immediately:
       `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
          new this round; report the count, there is no base
       `python3 -m pytest tests/docs/ -q`                    base 295
       `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`
                                                             base  30
       `python3 -m pytest tests/ui_server/ -q`               base 515
       `python3 -m pytest tests/orchestration/test_test_runner.py -q`
                                                             base  52
       `python3 -m pytest tests/regression/test_resource_safety.py -q`
                                                             base  21
       `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`
                                                             base  16
     Then the canary, which every handback runs:
       `python3 -m pytest tests/cli/test_golden_path.py -q`  base  42

  G8 THE TREE. At C5: `git status --porcelain` is EMPTY. `git ls-files
     .remedy-wt` returns nothing. Report the insertion count of each
     commit from C0a through C5 — six numbers, each under 500. The C6
     handback commit's own insertion count is NOT reported here and is not
     owed: it cannot exist while the text stating it is being written.

Handback: rewrite `.agent/handoff.md` per AGENTS.md `### handoff.md`. It
carries the feature and round, the SESSION NUMBER — which is 1 — the
branch, the commit SHAs, a changed-files table, ONE LINE PER GATE with its
real result, the open-findings count, the deviations, and the next
expected action. It has no length cap. An item-status table covering C0a
through C6 is mandatory: every item appears exactly once, with status
`done`, `skipped` or `deviated`, and a reason for the latter two.

SLICE PLAN — whole-file replacement of `.agent/plan.md`.
<<<SLICE PLAN
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 1 — claim F109 in the roadmap ledger, discharge the one closure
candidate F108 left open, and land T001a: the PURE per-session sent-hash
index `packages/orchestration/session_sent_index.py` with its unit tests
in `tests/orchestration/test_semantic_dedupe.py`. The module records,
queries, invalidates and serialises; it reads no file and calls no
provider.

## Next Steps

- T001b: persist the index into the job's evidence at the
  `on_call_finalized` seam, and invalidate a session's set whenever a
  resume attempt falls back to full context.
- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- The index must never key on an empty session id: that key would become
  a bucket every sessionless call shares, which is the cross-session leak
  the feature exists to prevent. T001a pins it with a test.
- `R-0769` is registered this round, not fixed: its repair edits
  `README.md` and a docs test, neither of which F109 owns.
SLICE PLAN>>>

SLICE CONTEXT — whole-file replacement of `.agent/context.md`.
<<<SLICE CONTEXT
# Context — F109 Semantic dedupe

## Active Branch
feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432`.

## Scope
F109 (Tier 3, depends on F105 and F106 — both done): within a RESUMED
session, segments whose hash already went to that exact session are
replaced by short reference markers, and only there. The scope rule binds
every round: resumed session only, proven sends only. Task slicing: T001
the sent-index (record at finalization, persist, invalidate on fallback)
plus unit tests; T002 the composition hook, the markers and the scope
guards plus fake-provider chain tests; T003 the measurement fixture, the
disable flag and the docs.

## Do not touch
Cross-session caching, provider-side cache mechanics, and prompt CONTENT —
all explicitly out of scope per `docs/roadmap/features/T3_F109.md` Do not
touch. Segment ranks and composition ORDER stay exactly as F105 set them:
dedupe replaces a segment's text, never its position, because the ordering
is what the provider cache hits.

## Assumptions
- F105 owns `packages/orchestration/prompt_segments.py` and already hashes
  every composed segment into a manifest row, so F109 is bookkeeping over
  those hashes and introduces no second hashing scheme.
- F106 owns the provider resume surface — `supports_resume`,
  `resume_used`, `resume_session_ref` — and F109 reads that session
  reference without widening it.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- No round of F109 gates on `ruff`: this session's reviewer cannot execute
  it, so such a gate would rest on the worker's word alone. The new files
  follow the repository's ruff configuration by construction instead.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for this round lives in the `## Current Step`
section of `.agent/plan.md`. This file deliberately does not restate it.
SLICE CONTEXT>>>

THE PAIR for `docs/roadmap/STATUS.md`. Containment test, run mechanically
before emission: TO contains FROM: false. Shape: REWRITE. Proof: FROM 0x
and TO 1x in the file after C2.
<<<STATUSFROM
- [ ] F109 — Semantic dedupe
STATUSFROM>>>
<<<STATUSTO
- [~] F109 — Semantic dedupe
STATUSTO>>>

SLICE CANDIDATES — whole-file replacement of `.agent/candidates.md`.
<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY — no candidate is open.

The entry F108's closure round recorded on 2026-09-02 — `README.md` carries
F106's capability paragraph twice, the second copy misplaced under "Accepted
in Tier 5 so far" — was registered in F109 round 1 as finding `R-0769` in
`.agent/live_review.md`; the reason, the measurement and the routing are on
that record. The entry recorded after F106's closure (job/mission
resume-from-persisted-state, DECISION F106 D2) was registered in F108 round 1
as finding `R-0762` on the same record.
SLICE CANDIDATES>>>

SLICE RECORD — appended to `.agent/live_review.md`, preceded by exactly two
newline bytes. One paragraph.
<<<SLICE RECORD
- R-0769 — Low, THE ROOT README CARRIES F106'S CAPABILITY PARAGRAPH TWICE AND THE SECOND COPY SITS UNDER THE WRONG TIER. Raised by the reviewer's closure review of F108, carried in `.agent/candidates.md` as a closure candidate per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings", and registered here because this is F109's first reviewed round. Measured by the reviewer at `5e18a8536afa086b591b5a2e13009d68d6227432`: `grep -n "F106 session resume" README.md` returns exactly two lines, 65 and 136. Line 65 opens the paragraph beneath the heading `Accepted in Tier 3 so far:` at line 64 and is correct, because F106 is a Tier 3 feature and `docs/roadmap/STATUS.md` carries its accepted line in the Tier 3 block. Line 136 opens a SECOND, differently worded paragraph beneath the heading `Accepted in Tier 5 so far:` at line 77, where no Tier 3 feature belongs. The two are not copies of one text: the first reads "repair rounds resume the original provider session and send only the findings delta, with an honest automatic fallback to full context and resume_used recorded in the call evidence", while the second reads "a repair round resumes the prior round's own provider session — gated on the provider honestly advertising support and a captured prior session id, never guessed — and sends only a hunk-selected findings delta in place of the full diff, with an honest, automatic fallback to full context the instant a resume attempt errors; the reduction is measured against a fixture repair chain, not assumed". A reader who finds one therefore has no signal that the other exists, and the tier F106 was accepted in is stated twice and contradictorily. THIS IS NOT R-0570, AND THE DISTINCTION WAS MEASURED RATHER THAN ASSUMED, per docs/agents/planner_reviewer_prompt.md §3 item 30, which requires the open set to be searched for the DEFECT before an id is minted. R-0570 is OPEN over the same file and names the same blind test — `test_the_readme_reports_the_accepted_foundation_and_no_later_feature` in `tests/docs/test_docs_consistency.py` iterates the ids the README LISTS and asserts each one is accepted in the ledger — but the defect R-0570 registers is an OMISSION, a list short of the ledger, and the fix its own text prescribes is to add the missing ids and pin the ledger-to-list direction. Neither half of that fix reaches this instance: F106 IS accepted, so the list-to-ledger direction passes, and the correct Tier 3 entry EXISTS, so a ledger-to-list completeness pin passes too, and the misplaced duplicate survives both. Two ids for one defect is the cost item 30 warns of, and a fix that silently misses a live instance is the cost on the other side; this paragraph is the record of which was chosen and why. Low, because nothing false is asserted about what Remedy can do — both paragraphs describe F106 accurately — and the whole cost is that the Tier 5 list claims a feature that is not a Tier 5 feature. The fix deletes the paragraph at `README.md` line 136, or merges its wording into the line 65 entry, and pins tier placement in `tests/docs/test_docs_consistency.py`; neither is a file F109 owns, and AGENTS.md forbids mixing an unrelated fix into a feature branch, so it routes to the same paydown branch as R-0570. OPEN.
SLICE RECORD>>>
