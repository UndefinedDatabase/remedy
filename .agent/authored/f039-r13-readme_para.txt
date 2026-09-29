F039 story mode (a finished job can now be told as a short story: its chapters are the phases it
went through, such as the plan, the build, the review and the finish, and small cards say what
happened at the moments that mattered, a decision, a failed test or a repair, with the reviewer's
verdict, who acted and the cost so far, every word taken from Remedy's own fixed wording and never
from a model; the Story button in the cockpit opens it over the graph, where Play walks the
timeline one event at a time with a pause before each chapter; the command
`remedy job story <job id> --export <file>` saves it as one HTML file that plays in any browser
straight from your disk, with no network and no Remedy, and refuses a story larger than the
`story.export_max_bytes` setting rather than cutting it; a test opens such a file in headless
Chrome and passes only when the page makes no request but the file itself).
