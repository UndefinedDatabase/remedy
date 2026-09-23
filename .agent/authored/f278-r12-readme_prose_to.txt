rather than against prose),
F278 durable writes & loud failures (every file the tool keeps is now written the
same safe way — into a temporary file beside it, flushed to disk, renamed into
place, and the folder flushed too — and every private copy of that routine is
deleted, with a test that refuses a new one; and no failure is swallowed in
silence any more: the lint rule against catching every error is on, each of the
290 places that still must do so says why, the raw stream record names the step
that failed, and four places that hid a failure behind a success now report it).