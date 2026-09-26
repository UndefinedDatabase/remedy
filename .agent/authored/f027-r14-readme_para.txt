F027 task veto (you can now stop one task of a job for good, with a reason, while
the rest of the job goes on: from the command line with `remedy job veto-task`,
naming the job, the task and your reason, or from the task's detail panel in the
browser, which offers a "Veto task" form only for a task that can still be vetoed;
the reason is required and is kept word for word; the vetoed task is struck through
on the graph, every task that depended on it is shown faded and will not run, and
hovering over one of them or opening its detail panel tells you why; tasks that do
not depend on it run as usual, and a job whose remaining work was all vetoed stops
as blocked and names what was vetoed; each veto puts a question in the decision
inbox with two answers, to plan the left-over work again as a new job or to accept
the smaller result, and nothing happens until you answer; after you answer, starting
the job again with `remedy job run` and the job's id finishes it, and a new job made
for the left-over work waits for you to plan it; the job's report shows who vetoed
each task and the reason; a veto cannot be undone, because planning the work again
is the way back).
