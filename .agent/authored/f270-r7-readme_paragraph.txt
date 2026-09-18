F270 history apply (every applied task of a job lands as one commit on its
`remedy/job-<job id>` branch; `remedy job apply <job> --approve
--commit-with-history` merges those commits onto the operator's branch with
`--no-ff` and refuses a dirty tree, a conflict or a staging job, changing
nothing; `--commit "<message>"` and `--commit-auto` land one commit of the
copied files, and `--push` pushes it once, never forced, to the branch's
upstream while no blocking criterion is unmet; `remedy do` passes the flags
through, chains its jobs under a commit flag and pushes the mission once; and
without one of those flags Remedy commits nothing on the operator's branch).
