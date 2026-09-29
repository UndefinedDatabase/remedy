## F039 — Story/replay mode

A finished job can now be told as a short story, played in the cockpit or handed to someone as one
HTML file that plays anywhere without Remedy.

### What it does

- **Chapters.** A story's chapters are the phases the phase bar reads over the whole event ledger,
  titled from one fixed table (The plan, The build, The review, The finish and so on); a phase with
  many key events splits into parts. A title names the phase, never its outcome, so a failing run is
  never titled as a good one (DECISION F039 D1).
- **Narration cards.** Each cluster of key events (decisions, failures, heals, stops) becomes a card:
  the humanize catalog's line for each event, the reviewer's verdict for a review round, the
  ownership ledger's sentence when exactly one actor matches, and the cost so far. No sentence comes
  from a model (D3).
- **Autoplay.** Play walks the timeline one ledger event at a time, pausing before each new chapter;
  under reduced motion it jumps chapter to chapter. The pace comes from `story.step_ms` and
  `story.chapter_pause_ms` (D4, D5).
- **In the cockpit.** The Story button in the right panel opens a docked card that drives the
  timeline's own scrub, so the graph and the phase bar always show the moment being told (D6).
- **Export.** `remedy job story <job id> --export <file>` writes one page that inlines the story
  player (built a second time by the UI build as one script and one style sheet) and the job's story
  data, under a content security policy that allows no request. It refuses a player that is not
  built and a file larger than `story.export_max_bytes` (5,000,000 bytes by default), and never cuts
  a story (D7, D8).

### Fixed along the way

- **R-1102 (High):** the cockpit replaced every minted task id with `task-<n>`, so a finished
  `remedy do` job never reached Finalized on the phase bar. The dashboard mapping now keeps a task's
  own id.
- **R-1101:** the story panel's autoplay stalled while its host re-rendered; its one timer now
  re-arms only on play, position and reduced motion.
- **R-1103:** the zero-network test stopped reading the browser's events at its last check; it now
  reads for two more seconds.

### Proof

- `tests/ui_server/test_story_export_file_live.py` runs the demo job on the fake providers, exports
  its story, and drives headless Chrome over `--remote-debugging-pipe`: three golden chapters, the
  slider's arrow key, a chapter jump, Space for Play and Pause, and no request but the file itself.
- The feature's one full suite: `20611 passed, 20 skipped` at exit 0
  (`.agent/authored/f039-closure-suite.txt`).
- Evidence job `f039r12e1001`; review package
  `remedy-review-20260929-031523-READY_FOR_REVIEW.zip`, SHA-256
  `e9097684c735ec44a6b33f4bc409de252280e7294e3d2d142b4197684f9dee7d`, accepted head
  `da3d5430681239aff3419da447abbb75f2105112`.
- Self-use item `SU-035` ran to its approval gate on `claude-cli` and was not applied; the check that
  generated it reads a file name as a config key, which is R-1104 (Low), carried to F286.

Guide: `docs/guides/story-user-guide-v1.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
