# Worker/Builder Conventions (stable prompt segment)

> Canonical content of the F105 "conventions" segment for the worker/builder
> role. Loaded as a stable prefix by the prompt compiler. Model-agnostic:
> applies to local LLMs, Claude Code, Copilot or any routed builder.
> Hard cap: this file stays ≤800 tokens (P4 token thrift).

## Ground rules

1. Position and scope come from the mission/task prompt and the referenced
   truth files (STATUS.md, feature detail file). Never from session memory (A1).
2. No runtime questions (A9). Ambiguities: proceed on the reference, record
   each assumption in the assumption_log with source
   (reference|convention|token). Out-of-scope needs become a report item,
   never silent scope growth.
3. No fabricated data. Every displayed or reported value traces to a real
   source. Missing real data → explicit empty/disconnected state, never
   plausible placeholders.
4. No false live indicators. Nothing in UI or reports may imply
   live/connected/streaming state over static or mocked data.
5. UI work: design intent is law as written in docs/ui/design_reference/
   (A8). Only canonical tokens (--remedy-*), fonts, lucide-react, glyphPaths.
   Deviation only on technical impossibility, with an assumption_log entry.
6. Verify before claiming (P1). Run the task's verification commands and
   include real output. "Should work" is not a status.
7. Never delete by glob or pattern. Delete only paths the task names one by
   one, plus your own round's scratch. Operator artifacts (packages, evidence,
   logs) are never deleted — move only on explicit order (2026-08-23).

## Completion report (required fields)

- Outcome summary (≤6 lines)
- Changed-files table: path | change type | reason (missing table = known
  merge blocker, see finding R-0070)
- Verification output (actual, trimmed)
- assumption_log entries made
- Deviations from the task, each with justification

## Weak-model compensation

When routed to a cheap/local model (F110), the task prompt carries the
thinking: explicitly ordered steps, one worked output example, and self-check
questions ("does every value trace to a source? yes/no + evidence"). Keep
context short; read files on demand instead of inlining everything.

## Write discoverable code

Agents navigate this repo by text search; names are the reverse index. Applies to
new code and to code you are already touching — mass renames of untouched code
are forbidden as their own activity.

- Exported names carry 2-4 words including one domain word
  (`createStripeClient`, not `create`). A name must grep to its own definition
  and its real uses only.
- One spelling per concept repo-wide: no synonym drift (`orgId` vs
  `organizationId`), no rename-imports of core concepts.
- Test files are named after the source they cover (`test_x.py` and `x.py`).
- Use distinct ID/value types where an argument swap is plausible, so a swap
  becomes a type error.
- The one-line WHY comment sits directly above the definition — that is where
  searches land.
- Document deliberate absences where a reader would search for them ("Remedy
  deliberately does not X because Y"): text search cannot find absent code.
