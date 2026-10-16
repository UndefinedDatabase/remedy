# What the cockpit's words mean: explanations, the Terms list and the welcome tour (v1)

The cockpit is Remedy's browser view of a job. Many of its words have a precise meaning, such as
Open, Proof, Scrubbed or Partially applied. Every one of those words now carries a short
explanation, and the cockpit can walk a first-time visitor through its main parts.

## An explanation for every underlined word

A word with a dotted underline explains itself. Rest the pointer on it for a moment, or move to it
with the Tab key, and a small card opens beside it with the word's name and one or two sentences
about what it means for this job. The Escape key closes the card, and so does moving away.

Some cards also show the figures behind the word. The Tokens and Cost tiles at the top show their
breakdown under the explanation: the tokens each role used, and the cost against the job's budget
with a line saying whether the figures are actual or estimated. A tilde before the cost means the
price is estimated.

A word inside a button, such as the state of a task in the task list, opens its card when the
pointer rests on it, but the Tab key moves past it, because the button itself is what the keyboard
reaches there. The Terms list below holds the same explanation for the keyboard.

## The Terms list

Press the question mark key anywhere in the cockpit, except while you are typing into a field, or
press the Terms button in the right-hand panel. A panel opens with every word the cockpit
explains, each with the place it appears, such as the metrics bar, the timeline or the task list,
and its explanation. Type into its search field to keep only the words whose name or explanation
contains what you typed. The Escape key or the Close terms button closes it.

## The welcome tour

The first time a browser opens the cockpit, a short tour of six steps starts by itself. Each step
darkens the page except for the part it talks about, when that part is on the page: the graph,
the timeline, the panel that shows what is happening now, the decision inbox, the note field and
the Terms button. Previous and Next move between the steps, as do the arrow keys.

Skip tour, Finish, Close tour and the Escape key all end the tour, and ending it in any of these
ways means it does not start by itself again in that browser. To see it again, open the Terms
list and press Take the tour. The browser keeps this one fact under the name
`remedy:first-run-tour`; clearing the site's stored data for the cockpit brings the tour back on
the next visit.

## Where the explanations come from

Each explanation names the place in Remedy's own documentation or code that defines its word, and
a test checks that the definition still says what the explanation relies on. When a definition
changes, that test fails until the explanation is brought up to date, so the cockpit does not go on
explaining a word the old way. A word whose feature Remedy has not built yet has no explanation
until that feature exists.
