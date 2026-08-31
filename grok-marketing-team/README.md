# The Grok Bot Marketing Team

**Eight roles. One afternoon. Every one of them shipped with an authority envelope.**

This is the companion build to the [Agent Action Audit](../README.md). The audit asks what your agents are *allowed* to do. This is what it looks like when you answer that question **before** you wire anything up.

A marketing team of eight Grok-powered bots. Seven of them cannot touch the outside world. One can, and it is gated.

## The roles

| # | Role | Does | Capability class | External send? |
|---|------|------|------------------|----------------|
| 1 | [Signal Scout](roles/01-signal-scout.md) | Finds accounts and triggers worth acting on | Read-only | No |
| 2 | [Positioning Editor](roles/02-positioning-editor.md) | Guards the narrative; rejects off-message drafts | Read-only | No |
| 3 | [Draft Engine](roles/03-draft-engine.md) | Long-form drafting — posts, newsletters, pages | Read-only | No |
| 4 | [Repurposer](roles/04-repurposer.md) | One asset → channel-native variants | Read-only | No |
| 5 | [Sequence Writer](roles/05-sequence-writer.md) | Outbound and lifecycle email copy | Read-only | No |
| 6 | [List Hygienist](roles/06-list-hygienist.md) | Segment building, dedupe, field normalization | Data mutation (bounded) | No |
| 7 | [Campaign Analyst](roles/07-campaign-analyst.md) | Pulls performance, writes the weekly readout | Read-only | No |
| 8 | [Publisher](roles/08-publisher.md) | The only bot that can send or post | External comms + mutation | **Yes — gated** |

Start here: [`00-stack-and-setup.md`](00-stack-and-setup.md). Then the [authority matrix](authority-matrix.md), which is the file that actually matters.

## The one design decision

Seven of these bots produce artifacts. Exactly one of them can make an artifact leave the building.

That is the whole architecture. It is not a safety feature bolted on afterward — it is the reason the thing is auditable at all. When every bot can send, your authority surface is eight bots wide and you will never map it. When one bot can send, you have a single chokepoint, a single approval queue, and a single log to read after something goes wrong.

The cost is one extra hop. The benefit is that the [reconstruction test](../audit/05-reconstruction-test.md) is passable by construction: the Publisher logs what it received, who approved it, and which upstream bot produced it, every time.

Most "AI marketing team" builds give all eight bots an API key with send scope because that was the fastest path to a demo. Then they fail step 3 of the audit on all eight rows.

## What this is not

Not a product, not a framework, not something you install. Eight prompt specs, a shared context file, an approval matrix, and a wiring diagram. Bring your own orchestrator — n8n, Make, a cron job, or a person copy-pasting on a Tuesday. All four work.

It is also not autonomous. It is a **drafting** team with a human at the publish gate. If you were looking for the version that runs your marketing while you sleep, that version fails the audit and you should not ship it.

## Setup order

1. `00-stack-and-setup.md` — keys, context file, orchestrator, cost
2. `roles/01` through `roles/07` — the drafting bots, in any order
3. `authority-matrix.md` — fill in your named approvers before step 4
4. `roles/08-publisher.md` — wire this **last**, after the matrix has real names in it

Wiring the Publisher before the matrix is how teams end up with an unbounded send capability and a promise to document it later. The promise is never kept.

---

Built by [Opsmarshal](https://www.opsmarshal.com) — RevOps + AI agentic workflows for B2B companies.
