```bash
remedy init                                         # register this repository (once)
remedy doctor core                                  # check local health
remedy do "Write a CONTRIBUTING.md" --plan-only     # plan an example order, run nothing
remedy do "Write a CONTRIBUTING.md"                 # plan and run it; stops before apply
remedy job list                                     # the jobs it planned and ran
```
