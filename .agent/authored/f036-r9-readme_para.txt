F036 guided result tour (you can now ask a finished job "what did I get?" and be walked
through the answer in at most eight short stops: how the run ended, what changed in each part
of the code, the command that runs it, and whether its Definition of Done passed, each stop
tied to a real place in the job, such as a task, a changed file, a file of its evidence or a
command it ran; the Tour button in the browser steps through the stops, and its "Show me"
opens the task or the changed file a stop names; `remedy job show --tour` prints the same
stops; every job gets a tour built from its own records when its run ends, and a tour written
by the summary model, checked so that it claims nothing the records do not say, only when you
switch on the `tour.model_written` setting).
