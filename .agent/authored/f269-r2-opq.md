
### Q4 — manual achieve ignores the contract (2026-09-18, F269, round 2)

What needs deciding: a mission now carries a contract, a list of acceptance criteria that each have a check. When the automatic run tries to declare a mission achieved while a blocking criterion is not yet met, it is refused and told which criteria are open. The manual command a person types to mark a mission achieved is not refused in that case. It prints which blocking criteria are still unmet and then marks the mission achieved anyway, because that command has always been described as the operator's own explicit judgement.

Why it matters: if the manual command also refused, a person could never close a mission whose contract they consider wrong or no longer relevant without first changing the contract. If it does not refuse, a mission can be marked achieved with a criterion unmet, although the command says so plainly.

My recommendation: keep the manual command as the operator's override, with the unmet criteria printed every time, and let only the automatic run be held by the contract.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.
