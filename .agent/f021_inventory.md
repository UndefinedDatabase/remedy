# F021 Inventory — the ground the live activity feed builds on

Measured at round base `5179725f` on branch `feature/f021-live-activity-feed`.
Every claim below is a reading taken from the SOURCE named beside it, at the
symbol named beside it. Nothing here is copied from the feature file, from the
step block, or from another `.agent/` document. Where a search returned nothing,
the section says ABSENT and names where it looked, because text search cannot
find code that does not exist (AGENTS.md, Code Discoverability Conventions).

Set sizes were re-derived by AST rather than by grep, with the scripts left
under `.remedy-wt/f021r2/` (`kind_sets.py`, `actor_map.py`, `event_labels.py`);
grep was only ever the candidate list.

---

## (a) The subscription

**Which module opens the connection.** `apps/ui/src/api/brainStreamDeps.ts`,
symbol `browserBrainStreamEnv`, is the only place a real stream is constructed:
its `makeSource` closure reads `globals.EventSource` and returns
`new Source(url)`. The URL is built one layer down in the same file by
`createBrainStreamHostDeps.openSource`, as a template literal over the path
`/api/jobs/<job>/events/stream` with a `cursor` query parameter. The socket is
OWNED by
`createBrainStreamHost` in `apps/ui/src/api/brainStreamHost.ts`, whose local
`source` variable holds it and whose `drop()` closes and forgets it; `connect`
calls `drop()` before opening, so one host never holds two sockets at once.

**What is exported and what a consumer receives.**
`apps/ui/src/api/useBrainStream.ts` exports exactly one symbol,
`useBrainStream(jobId, makeDeps)`. Its return type is `BrainStreamView`,
declared in `apps/ui/src/api/brainStreamRunner.ts`, and that interface has three
fields and no more: `status: BrainStreamStatus | null`, `lastSeq: number | null`
and `gapDetected: boolean`. A consumer therefore receives a transport summary,
never the events. The composition itself is
`createBrainStreamSession` in `apps/ui/src/api/brainStreamSession.ts`, whose
`BrainStreamSession` interface does expose a store pair — `subscribe(listener)`
and `view()` — plus `start()` and `close()`.

**One connection per mount, or per consumer.** Per CONSUMER. The construct is in
`useBrainStream`:

    const session = useMemo(() => createBrainStreamSession(latestMakeDeps.current(jobId)), [jobId]);

followed by an effect whose body is `session.start()` with a `session.close()`
cleanup. `useMemo` and `useEffect` are per component INSTANCE, so a second
component calling the hook builds a second session and `start()` opens a second
EventSource. The `makeDeps` argument is deliberately read through
`latestMakeDeps` — a `useRef` — and is NOT in the memo's dependency list; the
comment above the hook states the reason as avoiding a teardown and a fresh
EventSource on every parent render, so the guard that exists today is against
re-renders of ONE consumer, not against a second consumer.

**Can a second consumer attach without opening one? NOT TODAY, and the missing
piece is not the store.** Three readings:

1. There is exactly ONE call site of the hook in the whole app:
   `apps/ui/src/components/shell/RemedyShell.tsx`, `RemedyShell`, line reading
   `useBrainStream(dashboard.jobId, (jobId) => …)`. Its result is bound to
   `stream` and the only field ever read from it is `stream.status`, handed to
   `RightLivePanel` as `streamStatus`.
2. There is no shared holder to attach to. A repo-wide search of
   `apps/ui/src/**` for `createContext` and `useContext` returns exactly one
   provider, `ReducedMotionContext` in
   `apps/ui/src/components/shell/ReducedMotionProvider.tsx`. No stream context,
   no module-level singleton session, and `useBrainStream` returns the VIEW
   rather than the session, so the `subscribe` that
   `BrainStreamSession` exports is unreachable from outside the hook. ABSENT.
3. Even with a shared session, a feed would receive nothing (see (b)).

The cheapest shape that satisfies "one subscription, client-side fan-out" is
therefore: keep the single `useBrainStream` call in `RemedyShell`, widen
`BrainStreamView`, and prop-drill — `RemedyShell` already prop-drills
`stream.status` to `RightLivePanel`.

---

## (b) The event envelope

**The wire shape has one writer.** `packages/orchestration/ui_server.py`,
function `_safe_event_summary(seq, event)`, returns a dict with exactly FOUR
keys and nothing else:

    {"seq": seq, "event": …, "timestamp": …, "outcome": …}

Its docstring names itself the one writer for both transports, and both call
sites confirm it: `_build_events_since_json` maps it over the ledger slice for
`/events-since`, and `iter_sse_frames` wraps each one in `sse_event_frame`,
which emits `id: <seq>\ndata: <json>\n\n`.

- **Monotonic `seq`: YES.** In `iter_sse_frames` the value passed is the loop
  variable of `range(cursor, len(events))` over the ledger, and
  `_build_events_since_json` passes `start + offset`. It is the ledger's own
  index, not a per-response counter.
- **Kind discriminator: YES, but as a bare string.** The `event` key is
  `event.get("event", "")` — the run-log event name, defaulting to the empty
  string when absent.
- **Anything a row could resolve to a graph node: NO. ABSENT, and it is a
  deliberate-looking drop.** `packages/orchestration/run_log.py`, dataclass
  `RunEvent`, carries `task_id`, `artifact_id`, `provider`, `role`, `model`,
  `message` and a `metadata` dict alongside `event`, `job_id`, `run_id`,
  `timestamp` and `outcome`. `_safe_event_summary` selects three of those and
  drops `task_id` and `metadata`. The JobPlan branch loses it the same way:
  `ui_server._load_job_plan_events` builds `metadata["task_id"]` from the trace
  event, and `_safe_event_summary` then discards `metadata` wholesale. So no
  transport currently delivers a task id to the client.

**The client shape.** `apps/ui/src/api/brainStream.ts`, interface
`BrainStreamFrame`, is `{ seq: number; event: unknown }`. The payload is typed
`unknown` and is never narrowed anywhere: `brainStreamHost.receive` parses the
JSON, requires only a numeric `seq`, and calls `tell({ seq, event: payload })`.
`brainStream.receiveBrainFrame` then reads `frame.seq` and nothing else, and
`brainStreamRunner.publish` builds its view from `state.status`,
`state.lastSeq` and `state.gapDetected`. The event body is therefore DISCARDED
by the current client — no module retains it, which a search of
`apps/ui/src/api/brainStream*.ts` for `.event` confirms (the single non-test hit
is `EventsSincePayload.events` in `brainStreamDeps.framesOf`).

Consequence for T002/T003: a feed needs BOTH a retained payload on the client
AND a task id added to `_safe_event_summary` — and the second is a change to
`packages/`, which the feature file's own scope excludes. This is the sharpest
finding of the round.

---

## (c) The event kinds

**There is NO single authoritative list. Stated plainly, because T001's
coverage test is specified against one.**

The kinds that reach a feed are the `event` field of the run log. Its type is
declared in `packages/orchestration/run_log.py` as `RunEvent.event: str` — a
free string with no `Enum`, no `Literal` union and no validation on the write
path: `RunLogWriter.log(event: str, …)` forwards whatever it is given, and
`RunLogWriter.append` writes the line unchecked. `timeline.append_run_event` is
the same, keyword `event: str`.

Four DEFINED sets exist near this seam. Measured by AST from their modules:

| Symbol | File | Keys |
|---|---|---|
| `NARRATED_EVENTS` | `packages/orchestration/teacher_narration.py` | 11 |
| `EVENT_METADATA_SCHEMAS` | `packages/orchestration/event_schemas.py` | 7 |
| `TRACE_EVENT_KINDS` | `packages/orchestration/agent_run_trace.py` | 16 |
| `_STREAM_EVENT_KINDS` | `packages/orchestration/agent_run_trace.py` | 6 |

They are PAIRWISE DISJOINT — all six intersections are empty — and their union
is 40 names. They are also not all the same ledger: `TRACE_EVENT_KINDS` and
`_STREAM_EVENT_KINDS` describe `agent_run_trace.jsonl` under job evidence, while
the SSE stream reads `<data_root>/runs/<job_id>/*.jsonl` through
`ui_server._load_events` → `timeline.load_run_events`.

Against the emitters: an AST sweep of `packages/**/*.py` for run-log emission
(`<writer>.log(…)` and `append_run_event(event=…)`) finds 35 call sites, of
which 25 pass a string LITERAL — 23 distinct names — and **10 compute the name
at runtime**. Of those 23 literal names, exactly ONE (`token_policy_applied`)
appears in any of the four defined sets; 22 appear in none. So even an
exhaustive literal grep could not enumerate the vocabulary, because ten writers
never spell it.

**On the client side: ABSENT.** Searched `apps/ui/src/api/` for a kind union.
`brainStreamDriver.ts` exports `BrainStreamEvent`, a six-member union
(`opened`, `frame`, `closed`, `unsupported`, `snapshot`, `timer`) — those are
TRANSPORT events, not domain kinds, and the domain kind stays `unknown` inside
`BrainStreamFrame`. The two domain unions in `apps/ui/src/api/types.ts` are
`RemedyTimelineEventKind` (`llm_action | test | review`, 3) and
`RemedyActivityItem["kind"]` (`build | review | user | system | test`, 5); both
belong to the REST dashboard payload, neither is keyed on a run-log event name.

**A humanization catalog ALREADY EXISTS on both sides, and neither covers the
stream.**

- Client: `EVENT_LABELS` in `apps/ui/src/api/remedyApi.ts` — 11 entries mapping
  an event name to `{actor, kind, label}`, read at exactly one place,
  `EVENT_LABELS[a.event_kind]` inside `normalizeDashboardPayload`, with an
  inline fallback object for an unknown kind. It is NOT exported (module-private
  `const`) and the string `EVENT_LABELS` does not appear in
  `apps/ui/src/api/remedyApi.test.ts`, so it has no coverage test today. Its
  keys are keyed on the dashboard payload's `event_kind`, not on the stream
  envelope's `event`; 3 of its 11 keys also appear in `TRACE_EVENT_KINDS`, 0 in
  `NARRATED_EVENTS`, and 8 appear in no defined set at all.
- Server: `NARRATED_EVENTS` in `packages/orchestration/teacher_narration.py`,
  with `UNRECOGNISED_TEMPLATE` as its honest fallback and `narrate_run_event`
  applying it when a name is missing, is not a string, or is absent from the
  dict.
- `ui_server._load_job_plan_events` holds a third one, the local `_ACTOR_MAP`,
  whose key set measures EQUAL to `TRACE_EVENT_KINDS` in both directions (16
  and 16, both differences empty).

A fourth catalog would be the fourth spelling of one concept. Whether T001
extends `EVENT_LABELS` (and exports it) or opens a new module is a DECISION for
R3, and its coverage test cannot be "every kind in the authoritative list"
because no such list exists — it can only be "every kind in the catalog's own
enumeration, plus an honest fallback for everything else", which is the shape
`narrate_run_event` already uses.

---

## (d) The graph's focus surface

**What identifies a node.** Two different strings, and they can differ.

- `apps/ui/src/components/graph/forceBrainTypes.ts`, interface
  `ForceBrainNode`: `id: string` is REQUIRED, `nodeId?: string` is OPTIONAL.
- The graph that actually renders in the shell is NOT the force graph:
  `apps/ui/src/components/graph/BrainGraphStage.tsx` renders
  `apps/ui/src/components/graph/BrainGraphCanvas.tsx`, an SVG graph whose
  exported `BrainGraphCanvas` is the live renderer. Its `buildDisplayModel`
  pushes task nodes as
  `{ id: t.id, … }` — the TASK id from `dashboard.tasks` — and prompt satellite
  nodes as `{ id: p.id, taskId: p.taskId, … }`.
- `apps/ui/src/api/remedyApi.ts` builds each task with
  `id: scrubUiText(t.id || …)` and `nodeId: String(t.related_node_id || t.id || …)`.
  When the payload carries `related_node_id`, `nodeId !== id`.

**Does a focus/select/highlight entry point exist? A CALLBACK does; an
IMPERATIVE one is ABSENT.**

- The callback is the prop `onSelectNode: (nodeId: string | null) => void`. It
  originates as `setSelectedNodeId` in `apps/ui/src/RemedyApp.tsx` (state
  `const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)`)
  and is prop-drilled through `RemedyShell` → `BrainGraphStage` →
  `BrainGraphCanvas`, and separately `RemedyShell` → `RightLivePanel`.
- `RightLivePanel` ALREADY receives `onSelectNode` and already passes it to one
  sibling of the feed: `TaskChecklistCard`, whose row handler is
  `onClick={() => { if (row.nodeId) onSelectNode(row.nodeId); }}`. It does NOT
  pass it to `ActivityFeedCard`, which today receives only `activity`. So the
  wiring a feed row needs is one prop on one existing component.
- Highlight is a comparison, not an API: in `BrainGraphCanvas` the select ring
  renders under `selectedNodeId === n.id`.
- ABSENT: no exported function named focus/select/centre/highlight anywhere in
  `apps/ui/src/components/graph/`. The only imperative camera calls are
  `fg.zoom(…)` and `fg.centerAt(0, 0, …)` inside a mount-time `useEffect` in
  `ForceBrainGraph.tsx`, against a `graphRef` that is local to that component
  and never lifted. Nothing pans or zooms to a node.

**A hazard the jump feature must resolve, measured rather than inferred.**
`TaskChecklistCard` emits `row.nodeId` while `BrainGraphCanvas` builds task
nodes with `id: t.id` and rings on `selectedNodeId === n.id`. `RemedyShell`
absorbs the mismatch for the POPOVER only, with
`dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId)`,
accepting either spelling. The graph's own ring has no such fallback. A feed row
that jumps must pick the id the graph compares against, or the same divergence
lands in F021.

**What would have to be added** for a real jump: (1) an id on the stream
envelope that resolves to a task — see (b); (2) `onSelectNode` passed to
`ActivityFeedCard`; (3) if "focus" means moving the camera and not only ringing
the node, an imperative surface on the graph, which does not exist in any form
today. `apps/ui/src/components/graph/ForceBrainGraph.tsx` is imported by nothing
— searched `apps/ui/src/**` for an import of that module and found 0; the only
importers of `apps/ui/src/components/graph/buildForceBrainModel.ts` are that
same unrendered component and
`apps/ui/src/components/graph/buildForceBrainModel.test.ts` — so building the
camera API on the force graph would be building it on dead render code.

---

## (e) The test convention

**Runner.** vitest. `apps/ui/package.json`, `scripts.test:unit`, is
`vitest run`. Configuration is `apps/ui/vitest.config.ts`, whose whole `test`
block is two settings: `environment: "node"` and
`include: ["src/**/*.test.ts"]`.

Two consequences, both load-bearing for T001:

- `environment: "node"` means NO DOM and no React rendering. Every rule of the
  stream client lives in plain modules for exactly this reason — the header
  comment of `apps/ui/src/api/useBrainStream.ts` says the React half is
  "deliberately the ONLY part of it that is React at all".
- The include glob is `*.test.ts`, so a `.test.tsx` file WOULD NOT BE COLLECTED.
  A component test is not expressible under this config; a catalog test is.

**File-naming pattern and location.** Test beside source, same stem plus
`.test.ts` — the AGENTS.md `test_x.py ↔ x.py` rule in its TypeScript spelling.
Ten such files exist under `apps/ui/src/`: six `brainStream*.test.ts` and
`remedyApi.test.ts` in `apps/ui/src/api/`, `cockpitLogic.test.ts` at the src
root, `components/graph/buildForceBrainModel.test.ts`, and
`components/prompt/promptTraceLens.test.ts`.

**Style, read from the two files named in the order.**
`apps/ui/src/api/brainStreamSession.test.ts` imports `describe, it, expect` from
`"vitest"`, declares a `class FakeSource implements BrainStreamSource` whose
listeners fire only when the test says so, and builds a `harness(options)`
factory that injects all four deps and RECORDS scheduler calls instead of
firing them. `apps/ui/src/components/graph/buildForceBrainModel.test.ts` has no
fakes at all: a `dashboardWithTasks(n)` helper feeds real fixtures through
`normalizeDashboardPayload` and each `it` asserts one invariant over the
returned model. A pure catalog module fits the second style exactly.

**The command that runs them.**

    npm run test:unit --prefix apps/ui        # or: npx vitest run, cwd apps/ui

Measured this round in the primary checkout: `npx vitest run` with cwd
`apps/ui` exits 0 with **10 test files and 152 tests passed** in 370 ms.

**How pytest reaches it.** `tests/orchestration/test_test_runner.py`, class
`TestVitestFrontendTestFoundation`, method `test_vitest_passes`, runs
`["npx", "vitest", "run"]` with `cwd=apps/ui` and asserts `returncode == 0`,
under a `timeout=30`. The same class also pins `apps/ui/vitest.config.ts`, the
`test:unit` script, and the existence of `apps/ui/src/api/remedyApi.test.ts`.
That is the ONLY route: searching `.github/` and `scripts/` for `vitest` or
`test:unit` returns 0 hits, and this repository has no `Makefile` at its root
(`ls Makefile` fails) — `.github/workflows/ci.yml` runs
`npm ci --prefix apps/ui` but never a frontend test command. ABSENT as a CI
step; present only as a pytest child.

Note for T001's cost: adding test files grows the run that must finish inside
that hard 30-second timeout.

**The other convention.** `tests/ui_contracts/` (11 python files) asserts
SOURCE TEXT rather than behaviour — e.g.
`tests/ui_contracts/test_brain_stream_hook.py` asserts
`"export function useBrainStream(" in code`, and
`tests/ui_contracts/test_remedy_shell_stream.py` asserts
`"useBrainStream(dashboard.jobId," in code`. Both of those pin the exact
call-site strings quoted in (a), so any change to how the shell subscribes must
update them in the same commit.
