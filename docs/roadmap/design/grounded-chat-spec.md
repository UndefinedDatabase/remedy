# Grounded Chat & Intent Dispatch — Design Spec (target, F038)

> Roadmap design annex. This describes TARGET design for F038 (Tier 5) and its
> CLI-first delivery path; it is not yet built. Binding Done criteria live in
> ROADMAP.md F038; this spec details the how. PART J stands: the cockpit is
> the control stand — chat is one input inside it, never a second product
> surface and never a second write path.

## 1. Purpose

One conversational entry point that (a) answers questions with project or node
context, every claim cited from real evidence, and (b) turns free-text intent
into existing, audited operator actions via confirmable action cards. Works
with local models (Ollama/vLLM) and external providers alike.

## 2. Read path (grounded Q&A)

Two scopes, both answer ONLY from a defined evidence set; uncited claims
render marked "unsupported"; a canary test asking about absent facts must get
"not in evidence".

- **Project scope** — evidence set (all existing today):
  project brain output (`project_brain.py` aggregate: blockers, patterns,
  focus, next step), progress ledger, decision queue state, roadmap position
  (STATUS.md next-open parse), latest job reports/review bundles.
  When F071 (mission dossier) and F103 (token ledger views) land, they JOIN
  this set — no redesign, the composer takes evidence providers as a list.
- **Node scope** — that node's evidence only: prompt trace, verdicts, diff,
  run log (existing explain_run direction).

Answers carry citation chips [1][2] anchoring into the underlying artifacts
(cockpit: EvidencePanel anchors; CLI: artifact paths).

## 3. Write path (intent dispatch)

Free text → schema-enforced parse (F005 pattern, pydantic in
`packages/orchestration/schemas/`) into EXACTLY ONE existing verb:

| Intent | Verb (existing/planned owner) |
|---|---|
| submit a job | `remedy do "…"` intake (do_cmd / F013) |
| steer a running task | steering inbox (F030) |
| answer/approve a decision | decision queue (`decision_queue.py` / F031-F032) |
| pause/resume | pause verbs (F025) |
| status question | NOT a verb — routed to the read path |

Parse result renders as an **action card**: verb + parsed args + cost/scope
hints. Nothing executes unconfirmed. Confirmation dispatches through the
normal channel (CLI call path today; the F009 single write channel once it
exists), so the action is indistinguishable in audit/feed from the same action
taken via UI or CLI. Unparseable intent → honest "no matching action" plus
the verb list; never a guess, never a silent fallback to Q&A.

## 4. Delivery: CLI-first, cockpit second (Part B conformity)

- **Stage 1 (`remedy chat`, CLI):** REPL + one-shot (`remedy chat "question"`).
  Modules: `chat_evidence.py` (composer over evidence providers),
  `chat_answer.py` (grounded answer + citations), `chat_intent.py`
  (schema parse → ActionCard), all in `packages/orchestration/` —
  UI-independent by construction (library principle, architecture.md).
- **Stage 2 (cockpit):** chat surface in the UI, chips anchor into the
  EvidencePanel; endpoints follow the existing pattern
  (`/api/projects/{pid}/chat`, `/api/projects/{pid}/chat/intent`);
  dispatch goes through the F009 write channel. Design reference binding
  per A8 (docs/ui/design_reference/).

## 5. Model routing & tokens

Chat answer and intent parse are cheap/mid classes per F110
(`docs/agents/model_routing_policy.md`), local-capable via the existing
provider pattern (role env vars, F113 later). No top-tier calls from the chat
path. Evidence composition is deterministic code, not LLM calls (token
thrift, P4); the LLM sees a compact composed context, capped per F112 once it
exists (interim hard cap: ≤4000 tokens composed evidence).

## 6. Honesty & safety invariants

1. Chat never mutates anything directly; dispatch only via confirmed,
   existing verbs.
2. Every factual claim in an answer is cited or marked "unsupported".
3. Canary suite: absent-fact questions answer "not in evidence".
4. An unconfirmed action card provably executes nothing.
5. No project-scope answer from sources outside the defined evidence set
   (in particular: no raw source-code ingestion — project-brain boundary
   stays intact).
6. Redaction: composed evidence passes the existing redaction patterns
   before any provider call.

## 7. Test plan (summary; details in T5_F038.md acceptance)

Fixture set ≥10 intents (job submission, steering, decision answer,
pause/resume, 2 unparseable); citation anchor resolution both scopes; canary
both scopes; audit-equivalence check (chat-dispatched action == CLI action in
evidence); token cap test on composed evidence; local-model smoke (Ollama
endpoint) for answer + parse.
