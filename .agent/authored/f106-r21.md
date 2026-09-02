── STEP CLOSURE-REGISTERFINDING/1 — F106 ────────────────────────────────
Goal: Register round 20's real discovery — `create_provider()` has no
`"ollama"` branch, so the resolved product-default provider can never
reach a real call through the ping-pong job path — as finding R-0761
(Medium) in `.agent/live_review.md`, discharging closure precondition 6's
requirement that every string `describe_self_use_run_defects` surfaced be
registered before F106 closes.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r21.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 21 (PLAN21 below)
  C2  — append R-0761 (one paragraph) to .agent/live_review.md
  C3  — rewrite .agent/handoff.md for round 21 handback

Change: exactly the .agent/** paths of C0a/C0b, .agent/plan.md,
.agent/live_review.md and .agent/handoff.md. No path under packages/,
apps/, tests/, docs/, scripts/ — this round registers a finding about
production code, it does not fix it.

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile, never
   cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN21 is a REWRITE of .agent/plan.md, applied via shutil.copyfile
   from .remedy-wt/f106-r21-plan.md (38 lines, < 50, holds `## Goal`/
   `## Next Steps`, sha256
   88950ca67241acbb0f1c835c7bac82ea56e872edf0ffa9608bf4dadf0bcc6052, 1948
   bytes).
3. C2 — a ONE-PARAGRAPH append to .agent/live_review.md, never retyped,
   applied via shutil.copyfile from .remedy-wt/f106-r21-finding.txt (5025
   bytes, sha256
   d4e3403b5ef11e11293aa49df9b28fda9ac49d7f03e2e1295c36057e4d7a7bf5, zero
   internal newlines, no trailing newline). Re-measure the file's own base
   length before
   appending: at this round's base the file is 1899768 bytes and does NOT
   end in a trailing newline (confirmed unchanged since round 19 — round
   20 touched no ledger path), so the separator is "\n\n" (this file's own
   convention). Expected total: base + 2 + 5025 = 1904795 bytes, sha256
   a26a404d25da52bb2df11e7709cb6206757361046014e5c79f56c8f6e67730cc. (If
   your own measured total differs from this arithmetic, recompute the sum
   yourself rather than trusting either number blindly, and state which
   number you land on and why.)
4. C3 — .agent/handoff.md rewrite per AGENTS.md's handoff contract: state,
   SESSION 6, branch, commit SHAs, a changed-files table, this round's
   real gates (below), open-findings count (322 registered — up from 321
   — 60 resolved, 21 decisions), and next expected action: closure
   precondition 6 is MET (R-0761 registered, documented OPEN per
   precondition 1's Medium/Low-risk allowance); the eventual closure
   verdict is PASS WITH RISKS, not PASS, because of R-0761. Name that the
   closure commit still owes TWO things: DECISION F106 D2's
   `.agent/candidates.md` entry, and setting
   `scripts/self_use_queue.json`'s SU-003 `consumed_by` to `F106`.

Done when (run every command yourself; record REAL exit codes, never the
word "green"):
G1 TRANSPORT — .agent/authored/f106-r21.md and .agent/last_block.md both
   sha256-equal to this block as saved (single digest comparison).
G2 THE PLAN — .agent/plan.md sha256
   88950ca67241acbb0f1c835c7bac82ea56e872edf0ffa9608bf4dadf0bcc6052, 38
   lines (`wc -l`), holds `## Goal` and `## Next Steps`.
G3 THE LEDGER APPEND — .agent/live_review.md's real post-commit bytes and
   sha256 (compute and report; constraint 3 gives the expected arithmetic
   but you verify it, not assume it); the file's last `\n\n`-delimited
   unit is byte-equal to the R-0761 source text; negative control — flip
   one byte inside a SCRATCH copy of that text and confirm the flipped
   copy no longer byte-equals the file's own last unit (never mutate the
   tracked file itself).
G4 THE LEDGER COUNTS — over .agent/live_review.md at HEAD:
   `grep -cE '^- R-[0-9]{4} — '` reads 322 (up from 321 — exactly `R-0761`
   added, confirmed by `grep -c '^- R-0761 — '` reading exactly 1);
   `grep -cE '^Done: R-[0-9]{4} — '` reads 60 (unmoved); `grep -cE
   '^DECISION F[0-9]+ D[0-9]+ — '` reads 21 (unmoved).
G5 THE CODE CITATION HOLDS — re-grep, at this round's own HEAD, that
   `packages/orchestration/pingpong_provider.py:1591` is still
   `def create_provider(name: str, *, model: str = "") -> PingPongProvider:`
   and line 1599 still raises the quoted `RuntimeError` naming exactly
   `fake, claude, claude-cli` — this round touches no production file, so
   these must be byte-identical to round 20's own citations; report the
   real current line numbers and text, do not assume they held.
G6 THE TREE — `git status --porcelain` empty; every commit's insertions
   under 500 (C0a/C0b exempt as verbatim `.agent/**` state-file saves);
   canary (`pytest tests/cli/test_golden_path.py -q`) REAL exit 0; HEAD
   pushed and equal to `origin/feature/f106-session-resume`.

Handback: completion report + rewrite .agent/handoff.md (C3 above). State
the real numbers for every gate above, not the word "green". Name every
deviation, however small.
─────────────────────────────────────────────────────────────────────────
