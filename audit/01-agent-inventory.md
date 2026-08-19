# Step 1 — Agent Inventory

**Goal:** one list of every non-human actor that can touch your systems. Agents, automations, workflows, scheduled scripts, AI features inside SaaS tools.

Most teams find 2–3x more than they expected. Count anything that acts without a human clicking at the moment of action.

## Where to look

- Automation platforms: n8n, Make, Zapier, Workato, Tray
- CRM-native: HubSpot workflows, Salesforce Flow, Process Builder leftovers
- AI features inside tools: auto-enrichment (Clay, Apollo), AI sequencing (Outreach/Salesloft), AI routing, AI summaries that write back
- Custom: cron jobs, serverless functions, LLM agents with tool access, MCP-connected assistants
- Shadow: personal Zapier accounts, browser extensions with write access, "temporary" scripts older than 90 days

## Inventory table

| ID | Name | Platform | Owner (human) | Systems it touches | Trigger | Last reviewed |
|----|------|----------|---------------|--------------------|---------|---------------|
| A-01 | | | | | | |

## Rules

- **Every row needs a named human owner.** "The ops team" is not an owner. If nobody claims it, that's a finding — tag it `ORPHANED`.
- **Systems it touches** means write access, not just read. Reading is a privacy question; writing is an authority question.
- If you can't determine what triggers it, tag `UNKNOWN_TRIGGER`. Unknown triggers on write-capable automations go straight to the gap register.

## Done when

Every non-human actor has a row, an owner, and a trigger. Expect 2–3 hours for a typical Series B stack. The number of `ORPHANED` tags is your first headline metric.
