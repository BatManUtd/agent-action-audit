# Step 3 — Authority Map

**Goal:** for each agent, document what it is ALLOWED to do — by whom, up to what threshold, under what conditions.

This is the step that exposes the gap. Capability lives in config; authority usually lives nowhere. If your delegation-of-authority policy exists, it's a PDF written for humans. Your automations have never read it.

## Questions per agent

For each agent ID and each capability class it holds:

1. **Is this action class explicitly authorized for this agent?** (Written anywhere — policy, runbook, ticket, Slack decision. "It's always done this" is not authorization.)
2. **Who granted the authority, and do they still hold the right to grant it?**
3. **What are the bounds?** Amount thresholds, record types, audiences, time windows, environments.
4. **What requires a human?** Which specific conditions escalate — and to a named person, not a channel.
5. **What is expressly prohibited?** If the prohibition list is empty, nobody has thought about it.

## Authority table

| Agent ID | Capability class | Authorized? (Y/N/UNDOCUMENTED) | Granted by | Bounds | Escalation condition | Escalates to (named) | Prohibited actions |
|----------|-----------------|-------------------------------|-----------|--------|---------------------|---------------------|--------------------|
| A-01 | | | | | | | |

## What good looks like

"A-07 (refund bot) may issue refunds ≤ $200 on orders < 30 days old, max 3/customer/quarter; anything above routes to CS lead (J. Park); prohibited from touching enterprise-tier accounts."

One sentence. Bounds, escalation, named human, prohibition. If you can't write that sentence for an agent, the agent is operating on undocumented authority.

## Done when

Every agent × capability class cell reads Y, N, or UNDOCUMENTED. The UNDOCUMENTED count is your second headline metric — in our engagements it typically covers **the majority of write-capable automations.**
