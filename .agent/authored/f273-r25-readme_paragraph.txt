F273 findings paydown v1 (the open findings that describe a real defect were
repaired as their own text specifies, from 130 open at the claim to 14 at the
close, each of those carried by name to the next paydown: the suite runs on an
isolated data root and fails when the configured one changes; the token
ledger keeps one row per provider call; the integrity gate and the review
package read the ledger through its one canonical reader; CI fails on any ruff
finding and adds Python 3.12 to its matrix; and the modules, commands and
cockpit sections nothing wrote to were deleted),
