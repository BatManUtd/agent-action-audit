# Post-Incident Question Set (Agent Actions)

Run within 48 hours of any agent action that caused harm, near-miss, or surprise. Answers go in the incident record verbatim — including "unknown."

## Reconstruction
1. What exact action executed, and in which system?
2. What did the agent know at action time? (Input state with timestamps, not current state.)
3. What logic/prompt/rule version was in force at that moment?
4. What was it optimizing for, and did that conflict with any stated policy?

## Authority
5. Under what authority did it run? (Grant, grantor, bounds.)
6. Did the action stay inside the bounds? If bounds were undefined — say so.
7. Should it have escalated? To whom? Why didn't it?

## Failure classification
8. Was this a model failure (wrong reasoning), a context failure (wrong/missing data), a policy failure (rule wrong or absent), or an authorization failure (rule right, authority wrong)?
9. Could the same class of failure fire in other automations sharing the credential, logic, or data source?

## Closure
10. What one change makes this class of action reconstructable next time — and who owns shipping it by when?

If questions 2, 3, or 5 come back "unknown," the incident finding is not the bad action. It's the missing record.
