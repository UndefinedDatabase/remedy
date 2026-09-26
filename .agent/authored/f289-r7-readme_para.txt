F289 self-use sources (when Remedy looks for work to do on itself at the end of a
feature and its list of open review findings is empty, it now has two more places to
look: it checks the README, the documentation index, the user guides and the command
list against what the code really ships, for example a guide the index does not
list, a command a guide never mentions, or a setting name that does not exist, and
it reads the warnings `remedy doctor core` prints, of which a retired built-in model
is the kind it can repair itself; each problem it finds becomes a small job with
that one repair as its only task, and the job changes nothing by itself: it stops at
the normal approval step and a reviewer decides what lands; the first such job, run
at this feature's own close, added a missing user guide to the documentation index).
