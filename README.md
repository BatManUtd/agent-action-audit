# Agent Action Audit

**Your AI agents have API keys. Do they have authority?**

We run AI agentic workflows inside B2B GTM stacks for a living — n8n, Make, Zapier, custom LLM builds wired into HubSpot, Salesforce, Clay, Outreach. Same finding on nearly every engagement:

Teams can list what their agents **can** do. Nobody has written down what they're **allowed** to do.

The gap between those two lists is your risk surface.

## What this is

The audit we run before we automate anything. Five documents, three templates, one afternoon. Free.

| Step | File | Output |
|------|------|--------|
| 1 | [`audit/01-agent-inventory.md`](audit/01-agent-inventory.md) | Every agent and automation touching your systems |
| 2 | [`audit/02-capability-map.md`](audit/02-capability-map.md) | What each one CAN do (scopes, tokens, tool access) |
| 3 | [`audit/03-authority-map.md`](audit/03-authority-map.md) | What each one is ALLOWED to do (usually: undefined) |
| 4 | [`audit/04-gap-register.md`](audit/04-gap-register.md) | Capability minus authority = your exposure, ranked |
| 5 | [`audit/05-reconstruction-test.md`](audit/05-reconstruction-test.md) | The uncomfortable one. See below. |

Templates in [`templates/`](templates/): a minimal agent decision log, an approval matrix your automations can actually read, and the post-incident question set.

A worked example from a real (anonymized) engagement in [`examples/revops-stack-audit.md`](examples/revops-stack-audit.md).

## The reconstruction test

Pick any consequential action an agent took last month. A record it changed, a sequence it fired, a lead it routed, an enrichment it wrote. Now answer three questions:

1. **What did it know** at the moment it acted?
2. **Why did it act** — what was it optimizing for?
3. **Who approved it** — or under what standing authority did it run?

Most teams can't answer one of the three. That's not a tooling criticism. It's the finding.

## Who this is for

RevOps, marketing ops, and platform teams at B2B companies that have wired AI agents or automation into systems of record. If an automation in your stack can mutate CRM data, send external messages, or move money — this audit is for you.

## What this is not

Not a product. Not a framework requiring software. Not a compliance certification. It's the working checklist of an agency that builds these systems and got uncomfortable with what we found in our own work.

## Contributing

PRs welcome. Most valuable contribution: your gap-register findings, anonymized. The pattern library gets better with every stack that runs the audit.

---

Built from real engagements by [Opsmarshal](https://www.opsmarshal.com) — RevOps + AI agentic workflows for B2B companies.
Maintained by [Ananda Narasimhan](https://www.linkedin.com/in/simhan911). Researching the recommendation→execution gap in enterprise AI — if your agents are stuck in read-only mode, [I want to hear about it](https://www.linkedin.com/in/simhan911).

License: MIT

## Skills

| Skill | What it does |
|-------|--------------|
| [`skills/plan-scrutiny`](skills/plan-scrutiny/SKILL.md) | A plan-building coach for Claude. It makes the author answer for every decision (owner, inputs, failure path, approval gate, rejected alternative) in a signed logic ledger, drafts to a scrutiny standard distilled from real leadership reviews, then rehearses the review. Built because people who build plans with AI hand it the thinking and cannot defend the result. |
