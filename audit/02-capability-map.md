# Step 2 — Capability Map

**Goal:** for each agent in the inventory, document what it CAN do — not what it's supposed to do. Capability is defined by credentials, not intentions.

## Method

For each agent ID from Step 1, pull the actual scopes:

- **API keys/tokens:** what scopes were granted? (Most integrations were authorized with full-access scopes because that was the fastest way to make the error go away.)
- **OAuth grants:** read or read/write? Which objects?
- **Platform permissions:** the user/service account the automation runs as — what role does it hold? (Automations running as an admin user inherit admin capability. This is the most common finding.)
- **Tool access (LLM agents):** which tools can it call? Can any tool chain to a write action?

## Capability table

| Agent ID | System | Runs as | Granted scope | Can create | Can modify | Can delete | Can send external | Can move money |
|----------|--------|---------|---------------|-----------|-----------|-----------|-------------------|----------------|
| A-01 | | | | ☐ | ☐ | ☐ | ☐ | ☐ |

## The five capability classes that matter

1. **External communication** — can send email/messages/posts visible outside the company
2. **Data mutation** — can create, modify, or delete records in a system of record
3. **Resource commitment** — can spend, credit, refund, or commit money
4. **Access change** — can grant, modify, or revoke access/credentials
5. **Production action** — can deploy, restart, configure, or modify live systems

Tag every agent with its classes. An enrichment bot that "only updates fields" is class 2. A sequencer is classes 1 and 2.

## Done when

Every agent has verified (not assumed) scopes and capability-class tags. Rule of thumb from our engagements: **assume every scope is broader than the owner remembers.** Verify against the platform, not the person.
