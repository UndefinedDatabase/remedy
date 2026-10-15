# A job's story: playing it in the cockpit and sharing it as one file (v1)

When a job finishes, Remedy can tell what happened in it as a short story. The story is split into
chapters, one for each phase the job went through, such as the plan, the build, the review and the
finish. Inside each chapter, small cards say what happened at the moments that mattered, such
as a decision, a failed test or a repair, with the reviewer's verdict and the cost so far. You can
play the story in the cockpit, which is Remedy's browser view of a job, and you can save it as one
HTML file that anyone can open in a browser without Remedy.

Every sentence in a story comes from Remedy's own fixed wording for events and from a small table of
chapter titles. Nothing in a story is written by a model, and a job that failed is told as it
happened, failures included.

## Playing the story in the cockpit

Open the job in the cockpit and press the Story button in the right-hand panel. A card opens over
the lower left of the graph. It shows where you are in the story, one button per chapter, the card
for the current moment, and the buttons Previous chapter, Play, Next chapter and Close story.

The story moves the cockpit's own timeline, the bar of phases under the graph, so the graph and the
bar always show the moment the card is telling. Play steps through the job one recorded event at a
time and waits a little longer before each new chapter. The space bar starts and pauses the story,
and the Escape key closes it. If your computer asks for reduced motion, Play jumps from chapter to
chapter instead.

While a job is still running, its story ends where its record ends, and the card says so.

Two settings change the pace. `story.step_ms` is the wait between two events, 420 milliseconds by
default, and `story.chapter_pause_ms` is the extra wait before a new chapter, 1600 milliseconds by
default. Set them in your project's `remedy.toml`:

```toml
[remedy.story]
step_ms = 300
chapter_pause_ms = 1200
```

or with the environment variables `REMEDY_STORY_STEP_MS` and `REMEDY_STORY_CHAPTER_PAUSE_MS`. The browser keeps a value from 50 to
10000 milliseconds and uses the default for anything else. The cockpit reads them when it starts.

## Saving the story as one file

```bash
remedy job story <job id> --export story.html
```

This writes `story.html`, one file that holds everything the story needs: the story player, its
styles, and the job's task list and recorded events. Open the file in any browser, straight from
your disk. It makes no network request at all and needs no Remedy, so you can send it to someone
by mail or put it anywhere. The file plays the same way as the cockpit's story: the chapter
buttons, Play and Pause, the space bar, and the timeline, which you can drag or move with the arrow
keys once you have clicked it. It has no Close button, because there is nothing to close it back
to.

The file holds the job's task list, its recorded events as the cockpit shows them, and who did what
in the job. It does not hold the job's evidence files, such as test logs or changes to code; those
stay in Remedy. Secrets that the cockpit hides are hidden in the file too, because the file is
built from exactly what the cockpit shows.

The file carries no font of its own. It uses the same list of fonts as the cockpit, so it shows in
whichever of those fonts the reader's computer has. The design rules for Remedy's look forbid fonts
written into a page's styles, and the cockpit itself loads no font file yet, so the file does the
same.

### How large a story may be

A story file may be at most 5,000,000 bytes (about 5 MB) by default. A story that would be larger
is refused as a whole, and nothing is written: Remedy never cuts a story short to make it fit. Change
the limit with `export_max_bytes` under the same `[remedy.story]` table of `remedy.toml`, or with
the environment variable
`REMEDY_STORY_EXPORT_MAX_BYTES`. The story of the demo job, two tasks planned and run on Remedy's
fake providers, is about 272,000 bytes.

### When saving does not work

| What you see | What it means | Exit code |
|---|---|---|
| The record of the job cannot be read | The job id names no job Remedy knows | 3 |
| The story player is not built | Build the browser view once with `cd apps/ui && npm install && npm run build` | 3 |
| The story is over the budget | Raise `story.export_max_bytes`, or share the story in the cockpit | 1 |
| The story could not be written | The folder you named does not exist, or you may not write there | 1 |

Add `--json` for a machine-readable answer that names the file, its size in bytes and the budget.

## How Remedy checks that the file needs no network

A test in Remedy's suite, `tests/ui_server/test_story_export_file_live.py`, runs the demo job on
the fake providers, saves its story, opens the file in headless Chrome, which is Chrome without a
window, and records every request the page makes while the story plays and for two seconds after.
It passes only when the one request is the file itself. It also plays the story: it checks the three chapters of the demo, moves the timeline with
the arrow key, jumps to a chapter, and starts and pauses the story with the space bar. On top of
that, the file tells the browser to refuse any request it might try, so a later change that adds
one is blocked and shows up in that test.
