F029 subtree rerun (you can now say "do that part again": choose a task in the middle of a
job that has finished, stopped, paused or been blocked, and Remedy puts back every file that task and the
tasks depending on it changed, exactly as the files were before the task ran, and proves it
by comparing git's fingerprints of the files, while the work of every other task stays; when
another task also changed one of those files, the rerun is refused and the files are named;
before anything changes it estimates what running those tasks again will cost and asks you
when that is above the limit you set or cannot be estimated; you may name a different model
for the rerun, and the job's records and its final report say so; in the browser the Rerun
button of a run's detail panel does this, and on the command line `remedy job rerun-subtree`;
`remedy job run` then runs the tasks again, and every earlier attempt stays visible: the
graph marks such a task "attempt 2", the task's detail panel lists each attempt with how it
ended, and a rerun inside a mission is noted in the mission's dossier).
