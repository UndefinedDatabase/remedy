# F037 Source Inventory — measured at `9dde5495`, round R1

Every answer below is this worker's own measurement, taken on the F037 branch at
the round base. Commands are quoted with their real output; code facts carry
`path:line`. Where a thing could not be measured it says so instead of guessing.

## Q1 — The unified-diff parsers that already exist

`packages/orchestration/review_scope.py` holds the repository's one hunk-header
reader. Its module docstring states the design constraint that produced it:
"No AST parsing (simple regex on the diff)" (`review_scope.py:11`).

- `_parse_diff(diff_text: str) -> dict[str, dict[str, Any]]` — `review_scope.py:73`.
  Returns `{path: {"ranges": [[s, e], ...], "added_lines": [...],
  "import_change": bool, "new_file": bool, "lines": [...]}}` (`review_scope.py:76-82`).
  `ranges` are NEW-file line numbers; `lines` is that file's raw diff lines
  verbatim from its `---`/`+++` pair onward.
- `parse_diff_line_ranges(diff_text: str) -> dict[str, list[list[int]]]` —
  `review_scope.py:139`. Returns `{path: [[start, end], ...]}` in NEW-file line
  numbers only; it is `_parse_diff` with every other key dropped
  (`review_scope.py:146`). Its docstring calls itself "The single shared reading
  of unified-diff hunk headers" (`review_scope.py:142-144`).
- `split_diff_by_path(diff_text: str) -> dict[str, str]` — `review_scope.py:151`.
  Returns `{path: diff_section}`, each value the file's `lines` joined with
  newlines (`review_scope.py:165`). Explicitly documented to DROP any preamble
  before the first `---` — `diff --git`, `index` (`review_scope.py:161-163`).

What each DISCARDS of what F037's contract v1 needs
(`docs/roadmap/features/T5_F037.md:40-43` names `path, old_path?, status, stats,
hunks:[{id, header, lines:[{kind, old_ln?, new_ln?, content, intraline}]}]`):

| Contract need | `_parse_diff` | `parse_diff_line_ranges` | `split_diff_by_path` |
|---|---|---|---|
| per-line kind `ctx`/`add`/`del` | not structured — only `+` bodies land in `added_lines` (`review_scope.py:127-128`); `-` and context lines survive only inside the raw `lines` list | discarded | discarded (raw text only) |
| new line numbers | per-HUNK range only, never per line (`review_scope.py:120-125`) | same | discarded |
| old line numbers | discarded — `_HUNK_RE` matches `-\d+(?:,\d+)?` WITHOUT a capture group (`review_scope.py:51`) | discarded | discarded |
| hunk header text | discarded from the structure; present only as a raw element of `lines` | discarded | present only as raw text |
| rename headers / `old_path` | discarded — the entry is keyed by the `+++` path and `pending_old_path` is used only when the new path is `/dev/null` (`review_scope.py:97-99`) | discarded | discarded |
| binary markers | never seen — a `Binary files … differ` stanza has no `---`/`+++` pair, so the file never enters `files` at all | never seen | never seen |
| stats `{+,-}` | derivable from `added_lines` for `+` only; `-` is never collected (`review_scope.py:131-133`) | discarded | discarded |
| intraline spans | not computed anywhere | not computed | not computed |

Measured empirically, not only read (both probes run in-process against the real
module at the round base):

    binary diff parsed files: []
    rename diff keys: ['new.py']
    rename entry: ranges [[3, 5]]  added_lines ['added', 'more']  new_file False
    lines kept: ['--- a/old.py', '+++ b/new.py', '@@ -3,2 +3,3 @@ inside a function',
                 ' ctx', '-gone', '+added', '+more']
    parse_diff_line_ranges: {'new.py': [[3, 5]]}

So a binary file is INVISIBLE to the existing reader and a rename loses its old
path, keeping only the new one.

`rg -ln 'unified|@@' packages/ --type py` returned 22 modules. Of those, the ones
that really read unified-diff SYNTAX (the rest only mention the word in a prompt
string, a format label, a docstring or a `difflib` call):

- `packages/orchestration/review_scope.py` — hunk headers and `+`/`-` body lines;
  the only structured reader (`review_scope.py:51`, `:73`).
- `packages/orchestration/source_apply.py` — applies hunks; its own hunk regex
  `^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@` at `source_apply.py:463`, and it
  stops at a file-boundary line at `source_apply.py:489`.
- `packages/orchestration/structured_patch.py` — detects a diff
  (`structured_patch.py:216`) and cuts it into per-file `UnifiedDiff` records
  (`structured_patch.py:220-262`); classifies a body line only as
  `@@`/`+`/`-`/space (`structured_patch.py:241`).
- `packages/orchestration/diff_repair_response.py` — its own hunk-header regex at
  `diff_repair_response.py:182`; the module states it holds NO parser and takes
  touched paths elsewhere (`diff_repair_response.py:14`).
- `packages/orchestration/provider_trust.py` — a MULTILINE `^@@ ` counter for
  hunk counting (`provider_trust.py:377`) and a shape sniffer
  (`provider_trust.py:490`).
- `packages/orchestration/final_verifier.py` — extracts file paths from diff
  headers only (`final_verifier.py:105`).
- `packages/orchestration/local_model_advisor.py` — a marker tuple used to detect
  diff-looking text, not to parse it (`local_model_advisor.py:256`).
- `packages/orchestration/pingpong_loop.py` — a PRODUCER, not a reader:
  `difflib.unified_diff` at `pingpong_loop.py:1800`.
- `packages/orchestration/job_evidence.py` — also a producer:
  `difflib.unified_diff` at `job_evidence.py:1242`.
- `packages/orchestration/diff_repair.py` and
  `packages/orchestration/diff_repair_apply.py` — both state IN SOURCE that they
  deliberately hold no parser and reuse `review_scope`
  (`diff_repair.py:8-13`, `diff_repair_apply.py:16`).

ANSWER, one sentence: F037's JSON contract v1 CANNOT be produced by extending an
existing reader without changing that reader's contract — `_parse_diff` throws
away old line numbers at the regex level, never records a per-line kind, never
sees a binary file and never carries an old path — so T001 needs a NEW module,
and the existing `parse_diff_line_ranges` seam should stay exactly as it is
because `diff_repair` and `source_apply` are pinned to its current shape.

## Q2 — The file-status vocabulary

Every `STATUS_*` constant in `packages/orchestration/review_subject.py`:

| Constant | Value | Line |
|---|---|---|
| `STATUS_ADDED` | `added` | 72 |
| `STATUS_MODIFIED` | `modified` | 73 |
| `STATUS_DELETED` | `deleted` | 74 |
| `STATUS_RENAMED` | `renamed` | 75 |
| `STATUS_COPIED` | `copied` | 76 |
| `STATUS_TYPE_CHANGED` | `type_changed` | 77 |
| `STATUS_DIRTY` | `dirty` | 78 |

The whole of `_GIT_STATUS_MAP`, `review_subject.py:80-86`:

    _GIT_STATUS_MAP = {          # :80
        "A": STATUS_ADDED,       # :81
        "M": STATUS_MODIFIED,    # :82
        "D": STATUS_DELETED,     # :83
        "R": STATUS_RENAMED,     # :84
        "C": STATUS_COPIED,      # :85
        "T": STATUS_TYPE_CHANGED,# :86
    }

Read at `review_subject.py:319`. The accepted set is
`_VALID_STATUSES` at `review_subject.py:597-598`, holding all seven constants.

Against F037's `modified|added|deleted|renamed|binary`
(`docs/roadmap/features/T5_F037.md:40-41`):

- EXIST already: `modified`, `added`, `deleted`, `renamed` — four of five.
- DOES NOT EXIST: `binary`. No `STATUS_BINARY` is defined anywhere in
  `review_subject.py`.
- The contract OMITS three constants the module carries: `copied`,
  `type_changed`, `dirty`.

A separate, adjacent vocabulary exists that the contract does not name at all:
`KIND_REGULAR`, `KIND_SYMLINK`, `KIND_DELETED`, `KIND_DIRECTORY`, `KIND_SPECIAL`
(`review_subject.py:61-65`), with `VALID_FILE_KINDS` at `review_subject.py:66-67`
and a git-mode map at `review_subject.py:267-277`. "Binary" is NOT one of them
either — the axis this module models is file KIND (symlink, submodule, device),
not text-versus-binary.

What this repository does with a binary file in a diff today, cited:

- `packages/orchestration/diff_repair.py:62-77` — `_read_source_lines` returns
  the reason string `"binary"` when the file holds a NUL byte (`:68-69`) or fails
  a UTF-8 decode (`:71-73`). That path reads the SOURCE FILE from disk, not the
  diff, and its output is an omission reason, not a file status
  (`diff_repair.py:23` lists it beside `missing`, `no_ranges`, `out_of_bounds`,
  `budget`).
- `packages/orchestration/provider_trust.py:627-629` — the only place that reads
  a binary marker OUT OF DIFF TEXT: `"GIT binary patch" in raw_patch` or
  `^Binary files ` MULTILINE, raising `BINARY_FILE_CHANGE`
  (`provider_trust.py:97`) at severity BLOCKER. It REJECTS; it does not classify.
- `packages/orchestration/source_apply.py:379` — refuses to write binary content
  (`binary content not allowed`).
- `packages/orchestration/pingpong_loop.py:1769-1770` — the diff PRODUCER
  substitutes the literal placeholder text `[binary file]` for a binary path's
  body, by EXTENSION allow-list (`_BINARY_EXTENSIONS`, `pingpong_loop.py:1736`),
  and `packages/orchestration/pingpong_promote.py:76-79` returns the label
  `binary_file` from the same extension test.

So: nothing in this repository today maps a binary file to a review file STATUS.
Binary is currently a rejection reason, an omission reason, or a rendered
placeholder — three different vocabularies, none of them `review_subject`'s.

## Q3 — Where a diff comes from at runtime

PRODUCERS of unified-diff TEXT:

- `packages/orchestration/pingpong_loop.py:1749-1800` — `difflib.unified_diff`
  over original-versus-staging, capped, excluding secrets and binaries
  (`pingpong_loop.py:1751`, `:1769-1770`).
- `packages/orchestration/job_evidence.py:1242-1249` — `difflib.unified_diff`
  inside the evidence writer.
- `packages/orchestration/repair_attest.py:107` — builds "the exact `safe.diff`
  content: tracked diff + untracked headers", hashing the emitted bytes
  (`repair_attest.py:599`).

PERSISTED PATHS (all under a job's evidence directory):

| Path | Written by | Scope |
|---|---|---|
| `task_runs/<task_id>/safe.diff` | `pingpong_evidence.py:487` (`_write("safe.diff", …)`), `repair_attest.py:629-631`, `manual_attestation.py:96` | per TASK |
| `workspace.diff` | `job_evidence.py:194` and `job_evidence.py:197` | per JOB |

READERS: `review_scope.py:425` (`run_dir / "safe.diff"`),
`final_verifier.py:162` and `:166` (both `safe.diff` and `workspace.diff`),
`change_provenance_gate.py:211` and `:244`, `missing_tests_gate.py:136`.

PER ATTEMPT? No. Measured:

- `packages/orchestration/repair_loop_v2.py` — the module that owns repair
  ATTEMPTS — contains no diff artifact at all; it names diffs only to FORBID
  them in its records: `repair_loop_v2.py:24` ("no raw stdout/stderr / full logs
  / raw candidates / diffs / secrets") and `repair_loop_v2.py:595` ("Never raw
  logs/diffs/candidates"). `"diff --git"` is in its `_RAW_MARKERS` rejection
  tuple at `repair_loop_v2.py:45`.
- `packages/orchestration/repair_loop.py:601` states the same exclusion for the
  v1 record.
- `packages/orchestration/self_dogfood_execution.py` persists an attempt under
  `_attempt_dir(attempt_id)/attempt.json` (`:333-334`, `:363-366`) and a request
  text (`_store_request`, `:582`); no diff file.
- The nearest thing to a per-attempt diff is `patch_intent_diff_preview` in
  artifact metadata (`apps/cli/commands/job.py:608`, read at
  `apps/cli/commands/patch.py:54`), and `packages/orchestration/patch_intent.py:324`
  says in so many words: "diff_preview: human-readable preview block — NOT a real
  patch; read-only." It is also on the forbidden-raw-field list
  (`redaction_patterns.py:26`, `event_ledger.py:27`, `event_schemas.py:62`) and
  is stripped from review bundles at `review_bundle.py:1147`.

CONSEQUENCE for the feature file's endpoint, which takes an attempt parameter
(`docs/roadmap/features/T5_F037.md:32-33`, `:61-62`, `:77-78`): there is TODAY no
per-attempt diff to serve. A diff exists per task run and per job only. T001 must
either serve the per-task `safe.diff` and treat the attempt parameter as a future
axis, or a new per-attempt artifact must be produced first.

## Q4 — The server route table

`packages/orchestration/ui_server.py`, class `_RemedyHandler`. `do_GET` at
`ui_server.py:3389`, `do_POST` at `ui_server.py:3555`.

| Request path | Line | Match shape |
|---|---|---|
| `/` | 3395 | `path == "/"` |
| `/assets/…` | 3400 | `path.startswith("/assets/")` |
| `/api/state` | 3411 | `path == "/api/state"` |
| `/api/jobs/<job_id>/<endpoint>` | 3422 | `len(parts) == 5` + dict lookup |
| `/api/jobs/<job_id>/events-since` | 3451 | `endpoint == "events-since"` |
| `/api/jobs/<job_id>/events/stream` | 3457 | `len(parts) == 6` + parts compare |
| `/api/layers` | 3484 | `path == "/api/layers"` |
| `/api/jobs/<job_id>/nodes/<node_id>/detail` | 3489 | `len(parts) == 7` + parts compare |
| `/api/jobs/<job_id>/nodes/<node_id>/human-detail` | 3501 | `len(parts) == 7` + parts compare |
| `/api/jobs/<job_id>/nodes/<node_id>/debug-detail` | 3513 | `len(parts) == 7` + parts compare |
| everything else → 404 | 3524 | fallthrough |
| POST `/api/jobs/<job_id>/commands` | 3562 | `len(parts) == 5` + `parts[4] == "commands"` |

The `<endpoint>` dict is a literal inside `do_GET` at `ui_server.py:3429-3444`
and holds 14 keys: `dashboard`, `brain`, `brain-view-model`, `live-state`,
`task-progress`, `decisions`, `next-action`, `guide`, `events`, `readiness`,
`context-budget`, `story`, `checklist`, `diagnostics`.

EXACT CODE SHAPE by which a route is added: there is no router object and no
decorator. A route is a new `if` inside `do_GET` — either a literal comparison
(`if path == "/api/layers":` → `self._send_json(200, _build_layers_json())`,
`ui_server.py:3484-3486`) or, for a parameterised path, a `parts`-length plus
positional-element test (`ui_server.py:3489-3498`). The cheapest addition is a
new key in the handlers dict at `ui_server.py:3429`, which needs a
`_build_*_json(job)` function and nothing else.

`rg -ln 'ui_server' tests/` returned 51 paths. The ones that would turn red on a
new endpoint:

- `tests/ui_server/test_command_channel.py:1233` —
  `LITERAL_GET_ROUTES = frozenset({"/", "/api/state", "/api/layers"})`, asserted
  by EXACT SET EQUALITY at `tests/ui_server/test_command_channel.py:1306`. A new
  LITERAL GET route fails here. Its endpoint keys are derived by an AST walk over
  `do_GET` (`:1236-1278`) rather than transcribed, so a new DICT endpoint passes
  the equality but must appear in `_walkable_paths` (`:1280-1296`) or
  `:1311-1313` fails.
- `tests/ui_server/test_command_channel.py:1316-1331` —
  `test_every_route_the_server_serves_refuses_post_put_and_delete` walks every
  path from `_walkable_paths()` with POST/PUT/DELETE and asserts every answer is
  405 (`:1327-1329`) AND that the walk length equals `len(_walkable_paths()) * 3`
  (`:1331`). A new endpoint that answers a mutating verb fails here.
- `tests/ui_server/test_command_channel.py:1343-1351` — an unknown path is 405
  for every mutating method.
- `tests/ui_server/test_live_state.py:280-341` and `:415-421` — one
  endpoint-exists test per endpoint (`events`, `brain`, `guide`, `readiness`,
  `context-budget`, `brain-view-model`, node `detail`, `live-state`,
  `events-since`). These pin presence, not the set, so a new route does not
  redden them.
- Whole-file readers of `ui_server.py` that could be reached by a new endpoint's
  code: `tests/ui_server/test_live_state.py:454`, `:562`, `:568`, `:573`;
  `tests/ui_contracts/test_responsive.py:846`;
  `tests/ui_contracts/test_timeline_guard.py:25`;
  `tests/ui_contracts/test_humanize_catalog.py:29` and `:152`;
  `tests/orchestration/test_autonomy.py:253` and `:798`;
  `tests/orchestration/test_memory_events.py:92` and `:96`;
  `tests/regression/test_named_bugs.py:451`, `:553`, `:560`;
  `tests/ui_contracts/test_ux_quality.py:450-456` (`shell=True` must not appear).

MEASURED GAP, stated rather than guessed: I found NO test that counts lines,
functions or routes over the whole of `ui_server.py`. The nearest thing is the
AST walk above, which counts nothing and derives instead. Also noted: the
docstring at `tests/ui_server/test_command_channel.py:1240` says "thirteen job
endpoints" while the dict at `ui_server.py:3429-3444` holds fourteen. That is a
stale docstring, not an assertion, so nothing is red — reported because a reader
of that guard would otherwise trust the number.

## Q5 — The attempt identifier

| Notion | Module | Id field | Type |
|---|---|---|---|
| `list_repair_attempts(repair_id, job_id="", data_dir=None) -> list[dict]` | `packages/orchestration/repair_loop_v2.py:387`, called from `ui_server.py:612` via the import at `ui_server.py:603` | `attempt_id`, defined at `repair_loop_v2.py:188`, minted as `f"rat-{uuid4().hex[:10]}"` at `repair_loop_v2.py:379-380` and used as the record filename at `:383`; the record also carries `repair_id` (`:206`) | `str` |
| `repair_attempts_v1` job metadata | read at `ui_server.py:809`; the key constant `_ATTEMPTS_KEY = "repair_attempts_v1"` lives at `packages/orchestration/repair_loop.py:693`; also read at `review_bundle.py:761` | the DICT KEY itself is the identity — `ui_server.py:817-818` iterates `attempts.values()` and never reads an id field; the only id inside a value is `repair_intent_id` (`ui_server.py:825-826`) | `dict[str, dict]`; the inner id is `str` |
| `self_dogfood_execution.list_attempts(data_dir=None) -> list[dict]` | `packages/orchestration/self_dogfood_execution.py:378`, called from `ui_server.py:1326` | `attempt_id` on `SelfImprovementAttempt` (`self_dogfood_execution.py:177-178`), serialized at `:202`, used as the directory name at `_attempt_dir` (`:333-334`) | `str` |

ANSWER, one sentence: NO single canonical attempt id exists across the three —
two of them use a field named `attempt_id` but mint it in different namespaces
(`rat-…` under a job-and-repair directory versus a bare id under a data-root
attempts directory) and the third has no id field at all, only a metadata dict
key — so F037's endpoint parameter must NAME which of the three it means before
T001 can route on it.

## Q6 — The client entry point

`docs/ui/design_reference/component_spec.md:103-115` names the component
(`:103-104`) and its entry point: "entry = button in DetailPopover emitting
`onOpenDiff(taskId)` (no-op today; roadmap F037 lineage)" (`:114-115`).
Measured against the source:

    rg -n 'onOpenDiff|DiffViewer' apps/ui/src/
    (no output)

REAL COUNT: 0 hits. Neither identifier exists anywhere under `apps/ui/src/`.
The design reference names an entry point that has not been built.

What `apps/ui/src/components/detail/DetailPopover.tsx` takes TODAY, at
`DetailPopover.tsx:62`, as an inline destructured object type — there is no
named Props interface:

    { dashboard: RemedyDashboard;
      selectedNode: RemedyGraphNode;
      selectedPromptId?: string | null;
      onClose: () => void }

Four props. No `onOpenDiff`, no `taskId`.

The test file that pins that component: THERE IS NONE. Measured two ways —
`rg -ln 'DetailPopover' apps/ui/` returns exactly two files,
`apps/ui/src/components/shell/RemedyShell.tsx` (the only caller) and the
component itself; and a walk of `apps/ui` for `*.test.*` / `*.spec.*` outside
`node_modules` and `dist` returns 31 files, none of which names DetailPopover
and none of which lives under `components/detail/`. So adding a prop to this
component turns no vitest file red, and T002 will be adding the first test that
covers it.

## Q7 — The fetch seam and the bundle budget

`apps/ui/src/api/remedyApi.ts`:

- The function that performs a GET: `fetchJson<T>(path)` at `remedyApi.ts:25-29`.
  It is `async`, module-private (NOT exported), and calls
  `fetch(path, { method: "GET", credentials: "same-origin" })`.
- ERROR CONVENTION: a non-`ok` response THROWS —
  `throw new Error(\`Request failed ${r.status}: ${path}\`)` (`remedyApi.ts:27`).
  It never returns an error value.
- DEGRADED CONVENTION: every caller wraps the throw in a bare `try`/`catch` and
  pushes the endpoint NAME onto `failedEndpoints` — `remedyApi.ts:616-620`
  (dashboard), `:629-633` (brain-view-model), `:639-644` (decisions). A failed
  PRIMARY returns `normalizeApiFailure(jobId, failedEndpoints)`
  (`remedyApi.ts:317`, called at `:624`), which sets
  `apiHealth: { degraded: true, failedEndpoints }` (`remedyApi.ts:349`). A failed
  SECONDARY leaves the dashboard rendered and only records the name
  (`remedyApi.ts:649-654`), with `degraded` true only when `dashboard` is among
  the failures (`:651`). The healthy default is at `remedyApi.ts:184`.
- HOW A CALLER REACHES IT: not directly. `fetchJson` is private; the single
  public door is `loadRemedyDashboard(o: ApiClientOptions)` at
  `remedyApi.ts:608`, which builds `${base}/api/jobs/${o.jobId}/<endpoint>?${q}`
  with `q = token=${encodeURIComponent(o.token)}` (`remedyApi.ts:609-610`).
  A new F037 read endpoint therefore needs either a second exported loader beside
  `loadRemedyDashboard` or a widening of it.

BUNDLE / ASSET BUDGET: `rg -ln 'bundle|dist|asset' tests/` returned 130 files, so
the sweep alone proves nothing. I therefore searched every `.py` under `tests/`
for a line mentioning `dist` or `assets` TOGETHER with a size, byte, budget,
ceiling or limit token. Five lines matched and NONE is a size budget —
`test_ci_stage_selection.py:31` ("distinguishes"),
`test_context_compiler.py:687` ("distant"), `test_test_run_runtime.py:213`
("distinctive"), `test_version_report.py:26` (`distribution`), and
`test_cost_metric_render.py:146` (an assets-spec line reference).

STATED PLAINLY: NO bundle-size or asset-size budget exists in `tests/` at
`9dde5495`. There is also none in the build config — `apps/ui/vite.config.ts` is
19 lines and sets only `outDir`, `emptyOutDir`, `sourcemap: false` and
`rollupOptions.input` (`vite.config.ts:8-15`); no `chunkSizeWarningLimit`, no
manual chunks. So the "bundle-budget discipline from the perf feature"
that `docs/roadmap/features/T5_F037.md:37` leans on does NOT yet exist as an
enforced ceiling, and T003 would be creating it rather than satisfying it.

## Q8 — The guards a new module must satisfy

`rg -ln 'review_scope|review_subject' tests/` returned 55 paths, but MOST match
only the artifact filename `review_scope_packet.json`, not the module. Narrowing
to real importers (`rg -n 'from packages.orchestration.review_scope|…review_subject' tests/`),
the equality guards that a new parser or a widened vocabulary would turn red:

- `tests/orchestration/test_review_scope.py:7-14` — the exact import set from
  `review_scope`: `SCHEMA_VERSION`, `build_review_scope_packet`,
  `parse_diff_line_ranges`, `render_scope_markdown`, `split_diff_by_path`,
  `write_review_scope_packet`. Renaming or removing any is an ImportError at
  collection.
- `tests/orchestration/test_review_scope.py:51` — `pkt["schema_version"] ==
  SCHEMA_VERSION`. `SCHEMA_VERSION` is `"1.0.0"` at `review_scope.py:22`; the
  test reads the constant, so a bump does not redden it, but any packet that
  omits the field does.
- `tests/orchestration/test_review_scope.py:53` — `pkt["changed_files"] == [...]`,
  an EXACT LIST.
- `tests/orchestration/test_review_scope.py:54` —
  `pkt["changed_line_ranges"][path] == [[46, 48]]`, an EXACT range list. This is
  the guard that pins `_parse_diff`'s NEW-file-number semantics.
- `tests/orchestration/test_review_scope.py:57-58` — `pkt["test_results"] == {…}`,
  an EXACT DICT of four keys.
- `tests/orchestration/test_review_scope.py:273-282` —
  `test_only_allowed_risk_tags_emitted` asserts `set(tags) <= _ALLOWED_RISK_TAGS`
  for every file. That set is HAND-WRITTEN IN THE TEST at
  `tests/orchestration/test_review_scope.py:225`, not imported from the module,
  so it is a transcription that drifts silently downward; it is a subset test, so
  a NEW tag fails it.
- `tests/orchestration/test_review_scope.py:388-389` — the written-artifact map
  is pinned by exact key, `task_runs/T001/review_scope_packet.{json,md}`.
- `tests/orchestration/test_review_subject_strict_schema.py:37`, `:73`, `:91` —
  `validate_review_file_schema(...) == []` and
  `validate_review_subject_schema(...) == []`, EXACT EMPTY problem lists. The
  validator reads `_VALID_STATUSES` (`review_subject.py:597-598`), so adding a
  `binary` status without adding it there produces a non-empty list and fails.
- `tests/orchestration/test_review_subject_recursive_schema.py:50`, `:101`,
  `:115`, `:129` — the same `== []` shape for the commit and subject validators,
  including base-mode/base-kind pairings.
- `tests/orchestration/test_review_subject_coherence.py:78`, `:82`, `:86` — the
  coherence checker's `== []`, exercising the status-versus-kind rules at
  `review_subject.py:741-781`.
- `tests/orchestration/test_review_schema_versions.py:28` —
  `validate_content_proof_schema(_proof(schema_version="1.1.0")) == []`.
- `tests/orchestration/test_manual_completion_bundle.py:265-267` — three EXACT
  COUNTS over a whole artifact: `len(...["changed_files"]) == 9`, `== 2`, `== 3`.
  A parser that resolves paths differently changes these numbers.
- `tests/orchestration/test_final_verifier.py:73` and `:252` —
  `report["changed_line_ranges"] == {...}`, EXACT dicts including the union case.

MEASURED GAP, stated rather than guessed: `rg -n 'VALID_STATUSES|_GIT_STATUS_MAP|
VALID_FILE_KINDS|STATUS_COPIED|STATUS_TYPE_CHANGED' tests/` returned NO OUTPUT.
No test names the status vocabulary directly. The vocabulary is therefore guarded
only INDIRECTLY, through the `== []` validator assertions above, which means
adding `binary` to `_VALID_STATUSES` would turn nothing red by itself — the
danger is the reverse one, that a `binary` status invented in a NEW module and
never added to `_VALID_STATUSES` would be rejected by
`validate_review_file_schema` the first time the two vocabularies meet.
