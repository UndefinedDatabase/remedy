# A project's missions in the cockpit: orders, their jobs, and the repositories they reached (v1)

Remedy keeps one lasting mission for each repository it works on. Every order you give for that
repository is filed in the mission as one more batch of work, and every job the order starts is
linked to it. An order you give for several repositories at once is filed in each repository's own
mission, and Remedy remembers that those batches belong to the same order.

The cockpit, which is Remedy's browser view of a job, shows these missions in its missions panel.

## Opening the panel

Open a job in the cockpit and press the Missions button in the right-hand panel. A panel opens over
the graph. It shows one card for each mission of the project the cockpit is showing, the newest
first. A card names what the mission is for and how many orders and jobs it holds. The Escape key
or the Close missions button closes the panel.

## Reading a mission's orders

Press a card to open it. Remedy then reads that mission's newest 25 orders, the newest first, and
says how many older ones it is not showing. Each order shows:

- its title, which is the first line of the order you wrote;
- how many model calls its jobs in this project made, and how many tokens they read and wrote;
- how far it reached, for example "3 jobs in 2 projects";
- one small button, called a chip, for each job of the order.

The panel never shows a cost in money. It counts model calls and tokens, which is what Remedy
measures for each call.

## Following an order into another repository

Each chip names the project and the folder of the repository its job works in, the job's title and
its state. When an order reached several repositories, its chips include the jobs in the other
repositories too, in the order the jobs were started. The chip of the job you are looking at is
outlined.

Press a chip to open that job in its own project's cockpit. The address in your browser changes to
that project and that job, so the browser's Back button returns you to where you were. A chip shows
only references and titles: to see a job's evidence, open its cockpit through its chip.

A chip whose job Remedy no longer holds, or cannot read, is shown greyed out and cannot be pressed.

## Where this is built

The panel and its two reading routes are described in
[operator-cockpit-v1.md](../system/operator-cockpit-v1.md), in the section on a project's missions.
