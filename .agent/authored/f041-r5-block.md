STEP F041 R5 — T003's RESULTS PANEL: book round 4 and record D5, then the pure rules, the preview send, the two read doors, the panel with its README, screenshot lightbox and app card, its entry and mount, and a headless render

GOAL
Round 4 passed at `3c923d23`; the session handoff at `d735c058` carries its gate entry. Book it
and record DECISION F041 D5 in one commit, then land D5: the part of F041 a person sees. A
`Results` button opens a panel holding the app card (start, stop, and a link only while the app
answers), the job's README as the server's sanitized fragment, and a screenshot grid whose
pictures open in a lightbox. No route, event name, command or server module changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code, its tests, the render harness and the mutation tool yourself against S1 to S7.
Only the `.agent/` records and the assumption log's line travel as payloads. Read DECISION F041
D5 in records.diff before you write code. Before you write anything, read whole:
`apps/ui/src/api/pauseSend.ts` and `pauseSend.test.ts`, `decisionAnswer.ts`, `decisionSend.ts`,
`decisionNonce.ts`, `steeringSend.ts`'s `describeChatSendResult`, `ownership.ts`'s
`ownershipViewPath`, and in `remedyApi.ts` `fetchJson` and the tour door's section;
`components/tour/TourOverlay.tsx` and its CSS module; `components/story/StoryPanel.tsx` and its
CSS module; `components/graph/usePageVisible.ts`; `components/panels/RightLivePanel.tsx`;
`components/shell/RemedyShell.tsx`; `apps/ui/src/styles/tokens.css`;
`docs/ui/design_reference/assumption_log.md`; `tests/ui_contracts/test_story_panel_contract.py`,
`test_main_layout_guard.py`, `test_raw_colour_ratchet.py` and `test_pause_controls_contract.py`;
`artifacts_view` and `read_artifact_file` in `packages/orchestration/artifact_preview.py`,
`preview_view` in `packages/orchestration/preview_control.py`, and `_dispatch_job_preview` in
`packages/orchestration/ui_server.py`; and the five `.agent/authored/f039-r5-render_*` files.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r5-payloads/`, `.remedy-wt/f041-r5/`, `.remedy-wt/f041-r5-dry/`  READ-ONLY:
                                  the reviewer's payloads, block, scripts and tree.
  `.remedy-wt/f041-r5-worker/`    YOURS for logs, scripts and screenshots; create it if absent.
  `.remedy-wt/f041-render-run/` is the render harness's own work dir. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe.
Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx: run the primary's own binaries under `apps/ui/node_modules/.bin/`.
Stop a process only by its own recorded pid, never with `pkill -f`. Never `git reset` a commit.
Every comment and docstring you write names a command only as a whole real command, never with a
placeholder in place of a word (`tests/cli/test_advertised_commands.py` refuses such a line).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f041-artifact-preview`, and `git log --oneline -1` must read `d735c0587`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f041-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 28 | 10389 | a59a03bc914e2d552d3040364ab4b0b84da9b77bfceedc7149d6bed0ad6abdff |
| plan.md | 28 | 975 | 46db78d7fe1e8af3fdca6528929b695b46b0cbbd51cb6e5ecf612279e0b67b81 |
| assumption_line.md | 1 | 1051 | 27e6b13c17b7990c07054ded3ae957f339f8947cbb6bde47d4a8dcd98a463dd8 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `d735c0587`. It appends round 4's gate entry to
`.agent/live_review.md` and DECISION F041 D5 to `.agent/decisions.md`. `assumption_line.md` is
appended byte for byte to the end of `docs/ui/design_reference/assumption_log.md`, whose last
byte is already a newline.

THE SPECIFICATION. Every colour, shadow, radius and layer comes from a `--remedy-*` token that
`apps/ui/src/styles/tokens.css` defines: no raw colour in any file this round adds or edits.
S1 THE PURE RULES, a NEW FILE `apps/ui/src/api/artifactPreview.ts`, with no `window.`,
   `document.`, `fetch(`, `Date`, `Math.random` or React in it. Types: `ArtifactRoot` is
   `"workspace" | "evidence"`; `ReadmeArtifact {root; path; html; truncated: boolean; sourceBytes:
   number}`; `ImageArtifact {root; path; bytes: number; contentType: string}`; `ArtifactsView
   {readme: ReadmeArtifact | null; images: ImageArtifact[]; error: string}`; `PREVIEW_STATES`,
   the tuple `stopped`, `starting`, `probing`, `live`, `failed`, `not_applicable`, and
   `PreviewState` from it; `PreviewView {state; url; port: number; reason; updatedAt}`;
   `ArtifactRequest {jobId; token; baseUrl?}`.
   `decodeArtifactsView(payload: unknown)` answers the camel-cased view of the server's
   `{readme, images, error}`, or null when ANY key is out of shape: `readme` null or an object
   whose `root` is a root, `path` and `html` strings, `truncated` a boolean and `source_bytes` a
   finite number; `images` an array whose every entry has a root, string `path`, finite `bytes`
   and string `content_type`; `error` a string. `decodePreviewView(payload)` likewise for
   `{state, url, port, reason, updated_at}`, `state` one of `PREVIEW_STATES`.
   Paths, each with `ownershipViewPath`'s base rule and every value through `encodeURIComponent`:
   `artifactsViewPath(r)` is `<base>/api/jobs/<job>/artifacts?token=<token>`;
   `previewViewPath(r)` is `<base>/api/jobs/<job>/preview?token=<token>`;
   `artifactFilePath(r, root, path)` is
   `<base>/api/jobs/<job>/artifacts/file?root=<root>&path=<path>&token=<token>`.
   `readmeCockpitHtml(html, images, r)`: each match of `/<img src="([^"]*)" alt="([^"]*)">/g`
   — the one image shape the server's renderer and sanitizer emit — whose source, with `&lt;`,
   `&gt;`, `&quot;` and `&#x27;` decoded and then `&amp;`, and one leading `./` removed, equals
   the `path` of an entry of `images`, becomes `<img src="U" alt="A" loading="lazy">`, where A
   is the matched alt text unchanged and U is `artifactFilePath(r, "evidence", path)` with every
   `&` written `&amp;` and every `"` written `&quot;`; any other match becomes A alone. Then
   every remaining `/<img\b[^>]*>/g` is removed. Nothing else in the html changes.
   `captureCaption(path)`: the last `/` segment without its last `.suffix`, each run of `_`, `-`
   and white space made one space, trimmed; the whole last segment when that is empty.
   `lightboxIndexAfter(index, count, key)`: `ArrowRight` answers `Math.min(index + 1, count - 1)`,
   `ArrowLeft` answers `Math.max(index - 1, 0)`, any other key answers `index`.
   `PREVIEW_POLL_FAST_MS = 2000`, `PREVIEW_POLL_SLOW_MS = 15000`, and `previewPollDelayMs(view:
   PreviewView | null)` answers the fast delay while `starting` or `probing`, else the slow one.
   `PreviewCard {line; detail; action: "start" | "stop" | null; actionLabel; link: string | null}`
   and `previewCardView(view: PreviewView | null)`, a fresh object per call, by state:
     null            line PREVIEW_UNREADABLE_LINE, detail "", action null, actionLabel "", link null
     stopped         "The app is not running.", the reason, "start", "Start app", null
     starting        "Starting the app…", "", "stop", "Stop app", null
     probing         "The app started. Checking that it answers…", "", "stop", "Stop app", null
     live            `Live on port <port>.`, "", "stop", "Stop app", the url when it matches
                     `/^https?:\/\//i`, else null
     failed          "The app could not be shown.", the reason, "start", "Try again", null
     not_applicable  "This project has no app to run.", the reason, null, "", null
   Constants, exported, the panel's only words for these states: ARTIFACTS_LOADING_LINE
   "Reading this job's results…", ARTIFACTS_UNREADABLE_LINE "This job's results could not be
   read.", README_UNREADABLE_LINE "The README could not be read.", README_ABSENT_LINE "This job
   has no README.", README_TRUNCATED_LINE "The README is long, so only its beginning is shown.",
   CAPTURES_ABSENT_LINE "No screenshots were captured.", PREVIEW_LOADING_LINE "Reading the app's
   state…", PREVIEW_UNREADABLE_LINE "The app's state could not be read.". Each `…` is U+2026.
S2 THE SEND, a NEW FILE `apps/ui/src/api/previewSend.ts`, built as `pauseSend.ts` is and
   composing its `submitPauseSendRequest` and `PauseSendDeps` rather than copying them:
   `JOB_PREVIEW_START_COMMAND_ID = "job.preview-start"`, `JOB_PREVIEW_STOP_COMMAND_ID =
   "job.preview-stop"`, `PreviewCommand`; `buildPreviewSendRequest(target, command, clientNonce)`,
   null for an empty job id, an empty token or a nonce `isUsableCommandNonce` refuses, else
   `pauseSend.ts`'s path, method and three headers with the body `{command, client_nonce, args:
   {}}`; `describePreviewSendResult(command, result)`: unreachable is `describeChatSendResult`'s
   own; a refusal takes that function's tone for its status with "This request could not be read,
   so the app was neither started nor stopped." (400), "This dashboard was not allowed to start or
   stop the app. Open the dashboard again from a fresh link." (403), "Too many requests arrived at
   once. Wait a moment, then try again." (429), "The job could not record this request. Try again
   in a moment." (500), else "The job refused this request, so nothing was recorded."; an
   acceptance whose body's `outcome` is `accepted` is tone ok with "Starting the app. The link
   appears once the app answers." for start and "Stopping the app." for stop, and any other body
   is tone warn with "The job answered, but not in a way this page understands.";
   `sendPreviewCommand(target, command, deps = {})` mints, builds, races the submit against the
   20-second deadline and never throws, answering tone warn "This action cannot be sent as the
   page stands." when no nonce or no request comes out.
S3 THE READS, in `apps/ui/src/api/remedyApi.ts`, a section directly after the tour door's, shaped
   exactly as it: `ArtifactsFetcher`, `loadArtifactsView(request, fetchPayload = fetchJson)`,
   `PreviewFetcher`, `loadPreviewView(request, fetchPayload = fetchJson)`, each through S1's path
   and decoder, answering null on a throw or a refused payload. Nothing else in the file changes.
S4 THE PANEL, NEW FILES under `apps/ui/src/components/artifacts/`, none calling `fetch(`:
   `AppPreviewCard.tsx` `({jobId, serverToken})`: `visible = usePageVisible()`, state `view`
   (`undefined` before the first answer), `tick`, `sending` and `message`. ONE effect, whose
   dependency list is exactly `[jobId, serverToken, visible, tick]`, returns at once while hidden,
   else calls `loadPreviewView`, and unless cancelled stores the answer and sets ONE
   `window.setTimeout` of `previewPollDelayMs(answer)` that increments `tick`; its cleanup marks
   it cancelled and calls `window.clearTimeout`. It renders `<section data-ui="app-preview-card"
   aria-label="App preview" data-state={the state, or "unknown"}>`: PREVIEW_LOADING_LINE before
   the first answer, else `previewCardView`'s line, its detail when not empty, an `<a
   data-ui="app-preview-link" href target="_blank" rel="noopener noreferrer">Open app</a>` only
   when its link is not null, a button with its action label when its action is not null,
   disabled while sending, whose click awaits `sendPreviewCommand` with the matching id, stores
   the sentence and increments `tick`; and `<p aria-live="polite">` with the sentence.
   `ArtifactLightbox.tsx` `({images, index, request, onIndex, onClose})`, portaled to
   `document.body`: `<div data-ui="artifact-lightbox-backdrop">` whose click closes, and `<section
   role="dialog" aria-modal="true" aria-label="Screenshot" data-ui="artifact-lightbox">` with the
   picture from `artifactFilePath(request, "evidence", path)` whose alt is its caption, `<p
   data-ui="artifact-lightbox-caption">` reading `<index + 1> of <count> · <caption>`, and the
   buttons `Previous` and `Next`, disabled at their ends, and `Close`, which takes focus on mount.
   A window keydown listener, removed on unmount: Escape closes; ArrowLeft and ArrowRight prevent
   their default and call `onIndex(lightboxIndexAfter(...))`. Its CSS module takes the tour
   overlay's backdrop and centred card rules; the picture fits `max-height: calc(100vh - 220px)`.
   `ArtifactsPanel.tsx` `({jobId, serverToken, onClose})`, portaled to `document.body`: `<section
   role="region" aria-label="Results" data-ui="artifacts-panel">` holding a heading `Results`, a
   `Close results` button, the `AppPreviewCard`, then ARTIFACTS_LOADING_LINE until
   `loadArtifactsView` answers (one effect per job and token, with the `cancelled` guard) and
   ARTIFACTS_UNREADABLE_LINE when it answers null; else a `README` heading with
   README_UNREADABLE_LINE when the view's error is not empty, README_ABSENT_LINE when it has no
   README, or `<article data-ui="artifacts-readme" dangerouslySetInnerHTML={{ __html:
   readmeCockpitHtml(...) }} />` — THE ONE SUCH SITE IN `apps/ui/src` — followed, when truncated,
   by README_TRUNCATED_LINE and `<a data-ui="artifacts-readme-full" target="_blank"
   rel="noopener noreferrer">Open the full README</a>` to `artifactFilePath` of the README's own
   root and path; then a `Screenshots` heading with CAPTURES_ABSENT_LINE, or `<ul
   data-ui="artifacts-captures">` of one `<li>` per image: a button labelled `Open screenshot
   <caption>` around its thumbnail (`loading="lazy"`, empty alt) that opens the lightbox at its
   index, and the caption beside it. A window keydown listener closes the panel on Escape only
   while no lightbox is open. `ArtifactsPanel.module.css` docks the panel `position: fixed` at
   `top: 88px`, `right: calc(var(--remedy-right-width) + 16px)`, `width: min(440px, calc(100vw -
   48px))`, `max-height: calc(100vh - 120px)` scrolling, `z-index: var(--remedy-z-overlay)`, on
   `--remedy-glass-bg-strong`, `--remedy-glass-border`, `--remedy-radius-lg` and
   `--remedy-shadow-card`, text `--remedy-ink`, quiet lines `--remedy-muted`, code in
   `--remedy-font-mono`, links `--remedy-blue`, the grid three columns of 4:3 thumbnails; the app
   card uses the same module.
S5 THE ENTRY. `RightLivePanel` gains `onOpenResults?: () => void` and, directly after the Story
   button, `{onOpenResults && (<button type="button" className={styles.advancedToggle}
   onClick={onOpenResults}>Results</button>)}` under a comment naming DECISION F041 D5.
   `RemedyShell` gains `resultsOpen` state under such a comment, passes `onOpenResults={() =>
   setResultsOpen(true)}` directly after `onOpenStory`, and mounts `{resultsOpen &&
   (<ArtifactsPanel jobId={dashboard.jobId} serverToken={serverToken} onClose={() =>
   setResultsOpen(false)} />)}` directly after the story's mount, outside `<main>`. Nothing else
   in either file changes. `assumption_line.md` is appended to the assumption log.
S6 THE TESTS. NEW FILES `artifactPreview.test.ts` and `previewSend.test.ts` beside their modules.
   Every decoder, card and request case is asserted as ONE whole-shape literal with `toEqual`,
   never key by key: a valid payload of each view; each key of each shape out of shape in turn,
   answering null; the three paths with a job id holding a space and a token holding `&`;
   `readmeCockpitHtml` over a capture image, a `./captures/` image, an image outside `captures/`,
   a capture not listed, an alt text holding `&quot;`, a stray `<img>` of another shape and the
   text around them, each as its whole output; `captureCaption`, `lightboxIndexAfter` at both
   ends, `previewPollDelayMs` for every state and null; `previewCardView` for every state and
   null, and a live view whose url is `javascript:alert(1)`; the two doors with a fake fetcher
   (the path asked, the decoded answer, a throw, a refused payload); every status and outcome of
   `describePreviewSendResult` for both commands; and `sendPreviewCommand` with fakes for no
   nonce, a refused build, an answer and a deadline that wins. A NEW FILE
   `tests/ui_contracts/test_artifact_preview.py`, reading through `strip_ts_comments`:
   `dangerouslySetInnerHTML` occurs exactly once over every `.ts` and `.tsx` under `apps/ui/src`,
   in `ArtifactsPanel.tsx`, on a line holding `readmeCockpitHtml(`; no component of the directory
   holds `fetch(`; the panel holds `createPortal(`, `document.body`, `role="region"` and
   `data-ui="artifacts-panel"`; the lightbox `createPortal(`, `role="dialog"`, `aria-modal="true"`
   and `data-ui="artifact-lightbox"`; the card exactly one `window.setTimeout(`, a
   `window.clearTimeout(`, `usePageVisible()`, `sendPreviewCommand(` and the dependency list
   `[jobId, serverToken, visible, tick]`; `previewSend.ts`'s two ids equal
   `JOB_PREVIEW_START_COMMAND_ID` and `JOB_PREVIEW_STOP_COMMAND_ID` read from `ui_server.py`; both
   CSS modules name `var(--remedy-z-overlay)` and hold no raw colour; no purity word of S1 occurs
   in `artifactPreview.ts`; the shell's `</main>` precedes `<ArtifactsPanel` and it passes
   `onOpenResults={() => setResultsOpen(true)}`; and `RightLivePanel.tsx` holds S5's button.
S7 THE RENDER, five NEW files `.agent/authored/f041-r5-render_measure.py`, `_index.html`,
   `_main.tsx`, `_vite.config.mjs` and `_drive.mjs`, adapted from F039 round 5's with the work
   dir `.remedy-wt/f041-render-run`, CDP port 9368, server port 8998, and the screenshot under
   your own directory. `main.tsx` installs, before it mounts, a `window.fetch` stand-in that
   records every call on `window` and answers: the artifacts view with a README whose html is
   `<h1>Fixture app</h1><p>Before <img src="captures/one.png" alt="first shot"> after <img
   src="docs/elsewhere.png" alt="elsewhere shot"></p>`, truncated, and the images
   `captures/one.png`, `captures/two.png` and `captures/three.png`; the preview view, `stopped`
   until a start is posted, then `starting`, `probing` and `live` at
   `http://127.0.0.1:5173/` port 5173 on the next three reads, and `stopped` after a stop is
   posted; every command with 200 and `{command, outcome: "accepted", state}`; a `preview=failed`
   query parameter makes it answer `failed` with the reason `started but health check failed:
   connection refused`, and `preview=na` `not_applicable`. It mounts the real `ArtifactsPanel`
   for job `render-job` and token `render-token`, recording its close. `measure.py` puts one real
   PNG under `dist/` at `api/jobs/render-job/artifacts/file`, so every capture address loads it.
   `drive.mjs` prints one PASS or FAIL line per check at 1280 by 800: C-a the panel is a child of
   `document.body`, its z-index is 80 and its box lies inside the viewport; C-b the README shows
   `Fixture app`, holds exactly one image whose address holds `path=captures%2Fone.png` and
   `token=render-token` and whose `naturalWidth` is above 0, shows `elsewhere shot` as text, no
   resource entry names `elsewhere.png`, and the full README link holds `path=README.md`; C-c the
   grid holds three buttons captioned `one`, `two` and `three`, the second opens the dialog
   reading `2 of 3 · two` with focus on `Close`, ArrowRight reads `3 of 3 · three` twice over,
   ArrowLeft `2 of 3 · two`, and Escape removes the dialog while the panel stays; C-d the card
   reads `The app is not running.` with `Start app` and no link, a click posts
   `job.preview-start` with `args` `{}` and the CSRF header, and the card reaches `Live on port
   5173.` within 15 seconds with the link to `http://127.0.0.1:5173/`, while a sample every 50 ms
   finds no link before the card's `data-state` reads `live`; C-e `Stop app` posts
   `job.preview-stop` and the card returns to `The app is not running.` with no link; C-f the
   failed page shows the reason and `Try again`; C-g the not-applicable page shows `This project
   has no app to run.` and no button in the card; C-h Escape removes the panel and records the
   close, the count of preview reads then stays unchanged over a 3-second idle wait, and no console
   error was logged in the whole run. It screenshots after C-b and prints `RENDER: <n> of 8
   checks pass`. Its whole output is saved as `.agent/authored/f041-r5-render.txt`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6, C7, C8, C9 and C10, in this order.
C1a — `.agent/authored/f041-r5-block.md` := this block, and `.agent/authored/f041-r5-plan.md` and
  `.agent/authored/f041-r5-assumption_line.md` := the payloads, by `shutil.copyfile`. Subject:
  `F041 R5 C1a: copy round 5 block and payloads into .agent/authored/`. Its insertions are this
  block's line count plus 29.
C1b — `.agent/authored/f041-r5-records.diff` := records.diff. Subject: `F041 R5 C1b: copy round 5
  records diff into .agent/authored/`. Expected insertions: 28.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F041 R5 C2: book
  round 4, record D5`. Expected by `git show --numstat`: 10/0 .agent/decisions.md, 2/0 .agent/live_review.md, 7/7 .agent/plan.md.
C3 — S1, S3 and `artifactPreview.test.ts`. Subject: `F041 R5 C3: decide what the results panel
  shows and read its two views`.
C4 — S2 and `previewSend.test.ts`. Subject: `F041 R5 C4: send the preview pair through the door`.
C5 — S4. Subject: `F041 R5 C5: show the README, the screenshots and the app card in a panel`.
C6 — S5. Subject: `F041 R5 C6: open the results panel from the right panel`.
C7 — the contract test. Subject: `F041 R5 C7: pin the results panel's seams`.
C8 — S7's five files and `.agent/authored/f041-r5-render.txt`. Subject: `F041 R5 C8: render the
  results panel headless and record its checks`.
C9 — your mutation tool as `.agent/authored/f041-r5-mutations.py`. Subject: `F041 R5 C9: add the
  round 5 mutation tool`.
C10 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F041 R5 C10:
  rewrite handoff for round 5`. Then `git push origin feature/f041-artifact-preview` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects (C3a, C3b and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f041-r5-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the four new files under
   `apps/ui/src/api/`, `apps/ui/src/api/remedyApi.ts`, the new files under
   `apps/ui/src/components/artifacts/`, `RightLivePanel.tsx`, `RemedyShell.tsx`,
   `docs/ui/design_reference/assumption_log.md`, `tests/ui_contracts/test_artifact_preview.py`
   and `.agent/handoff.md`. Report the list `git diff --name-only d735c0587` measures after C10.
   Do NOT touch anything else, in particular `packages/`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C10, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`, no `git reset`. Leave every worktree listed at
   your step 4, its branch, and every stash alone; the one G5 adds is removed as its last action.
6. DO NOT run the full suite: it belongs to F041's closure (amend0917 rule 1). Run no self-use
   job, no command that calls a provider, and never a real preview or `remedy runtime serve`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C10 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f041-r5-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f041-r5/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it, and show that the assumption log at C6 equals its
 bytes at `d735c0587` followed by `assumption_line.md`'s. One reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 named, equals the reviewer's reading, printed from its dry tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2467439 | f5e1d5e444f22d5fad3961127efc4895322a885fbf9b650ae21243b5c305eabb |
 | .agent/live_review.md | C2 | 304029 | 2b53622128fab38cf5c5044e92a446c8aa6e6eba5eefbdc095c8c0ea539d8bb9 |
 | .agent/plan.md | C2 | 975 | 46db78d7fe1e8af3fdca6528929b695b46b0cbbd51cb6e5ecf612279e0b67b81 |
 | docs/ui/design_reference/assumption_log.md | C6 | 28366 | fb2b87f1ed3d85524d82252465acaf2b5812d4f37eb4d484fe908bf7a87df12f |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at
 `d735c0587` and at C2 (the reviewer read `[]` at both), and `git diff --name-only <C1b> <C2>`,
 which must name exactly the three `.agent/` paths of the table.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_artifact_preview.py
 .agent/authored/f041-r5-render_measure.py .agent/authored/f041-r5-mutations.py` at C9, with its
 real exit code. Then report, quoted from the commits, the whole of `artifactPreview.ts`, the card's
 effect and click handler, the lightbox's keydown listener, the panel's README block, and the
 changed lines of `remedyApi.ts`, `RightLivePanel.tsx` and `RemedyShell.tsx`.

G4 THE TESTS AND THE RENDER — in the primary checkout at C9, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_preview_commands.py tests/ui_server/test_artifacts_route.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
bash -c 'apps/ui/node_modules/.bin/vitest run --root apps/ui 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran both in the primary checkout at `d735c0587`: the first without
 `test_dashboard_contract.py` read `1447 passed, 4 skipped` and that file alone `64 passed`, and
 the second read `91 passed | 1 skipped` test files and `1831 passed | 5 skipped` tests, all at
 real exit code 0. The four skips are the D3 quarantine nodes of `test_graph_architecture.py` and
 `test_ux_quality.py`, and yours must be exactly those four. Report the whole tail of each, every
 `SKIPPED` line, and the node count of `tests/ui_contracts/test_artifact_preview.py` by
 `--collect-only -q`: the first run's passed count must equal 1447 plus 64 plus that node count, the
 vitest test count must exceed 1831 by the tests your two new files hold. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0. Then
 `python3 .agent/authored/f041-r5-render_measure.py /home/decodeux/Repos/remedy`, whose whole
 output C8 saves: it must print `RENDER: 8 of 8 checks pass` and exit 0, and afterwards
 `.remedy-wt/f041-render-run` must be gone and `git status --porcelain` empty. Report the
 screenshot's path and size.

G5 THE RED PROOFS — your tool `.agent/authored/f041-r5-mutations.py` takes a worktree path, edits
 the named file INSIDE it (asserting the FROM text occurs exactly once there), runs
 `apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 /home/decodeux/Repos/remedy/apps/ui/vitest.config.ts` scoped to the two new test files, or
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_artifact_preview.py` with the
 worktree as the working directory, restores the bytes, and prints one line per mutation with the
 runner's exit code and failed count, unmutated controls of both runners first and last,
 `restored byte-identical: True` after each, and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
 <bool>`. A collection or import error is a broken edit, not a reading; repair the edit.
  m1 `readmeCockpitHtml` leaves an image outside `captures/` in place;
  m2 `readmeCockpitHtml` drops the token from the rewritten address;
  m3 `previewCardView` offers the link while probing;
  m4 `previewCardView` offers a link to any address while live;
  m5 `decodePreviewView` accepts a state outside `PREVIEW_STATES`;
  m6 `lightboxIndexAfter` wraps from the last picture to the first;
  m7 `previewPollDelayMs` answers the slow delay while starting;
  m8 `buildPreviewSendRequest` leaves out the CSRF header;
  m9 `loadPreviewView` lets a failed read throw;
  m10 the panel renders in place, without `createPortal`;
  m11 the lightbox writes its caption through `dangerouslySetInnerHTML`;
  m12 the card's effect cleanup no longer clears its timeout;
  m13 the Results button is removed from `RightLivePanel.tsx`.
 Run it on `git worktree add --detach .remedy-wt/f041-r5-mut <C9>` and report its whole output.
 THEN THE RENDER'S OWN RED PROBE: first link `<worktree>/apps/ui/node_modules` to the primary's
 `apps/ui/node_modules` with `os.symlink` (gitignored, gone with the worktree), because the
 worktree's own sources resolve `react` from their own ancestors and not from the harness's work
 dir; run the harness once UNMUTATED on the worktree, which must print 8 of 8; then apply m3 alone,
 run `python3 .agent/authored/f041-r5-render_measure.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r5-mut`,
 report both whole outputs, the second of which must show C-d FAIL and a non-zero exit, and
 restore the file byte-identically. EVERY mutation and the probe must be red; a green one is reported as
 green, and you then add the test or check that catches it before C10 and re-run. Then
 `git worktree remove --force .remedy-wt/f041-r5-mut`, `git worktree prune`, and report
 `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C10, in your reply since C10 cannot hold them: `git status --porcelain`,
 empty; `git log --oneline -n 12`, C10 to C1a and `d735c0587` in order (more if a commit was
 split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C9 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 2 of feature F041, round 5, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 5,
then the result tour's preview anchor and the end-to-end run on a fixture app, then the closure.
State the open-findings count, 0, and the operator-questions count, 1.
