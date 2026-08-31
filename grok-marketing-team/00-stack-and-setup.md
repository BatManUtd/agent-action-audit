# Setup — Stack, Keys, Context

One afternoon, assuming you already have a CRM and somewhere to put drafts. Budget three hours: one on the context file, one on wiring, one on the approval matrix and the Publisher.

## What you need

| Thing | Why | Notes |
|-------|-----|-------|
| xAI API key | Runs all eight bots | One key per bot, not one key for all eight. See below. |
| A context file | The eight bots share one source of truth | `context/company.md` — the single highest-leverage file here |
| An orchestrator | Moves output between bots | n8n, Make, Zapier, a Python script, or a human. All fine. |
| A draft store | Where bots 1–7 write | Notion, Google Docs, a git repo, an S3 bucket |
| An approval queue | Where the Publisher waits | Slack channel with a button, a Linear ticket, an email to a named person |

**Model IDs change.** Check the current xAI model list rather than copying an ID from a doc — including this one. The specs here assume a current frontier Grok model with tool-calling; anything in that class works. Reasoning-heavy roles (Signal Scout, Campaign Analyst) benefit from the larger model, drafting roles do not.

## One key per bot

The single cheapest thing you can do for auditability, and almost nobody does it.

```
XAI_KEY_SCOUT=...        # bot 1
XAI_KEY_EDITOR=...       # bot 2
XAI_KEY_DRAFT=...        # bot 3
...
XAI_KEY_PUBLISHER=...    # bot 8 — the one that matters
```

Eight keys cost the same as one. What you buy is attribution: when the usage graph spikes or a bad draft ships, you know which bot did it without reading logs. When you retire a role, you revoke a key instead of untangling a shared credential. This is [Step 2](../audit/02-capability-map.md) of the audit, applied before there is anything to audit.

The same logic governs the **downstream** credentials, and here it is not optional:

- Bots 1–5 and 7 get **read-only** tokens to every system they touch. Not read/write with a promise to behave. Read-only at the token.
- Bot 6 gets a token scoped to the specific objects and fields it normalizes. Not "CRM write."
- Bot 8 gets the only send/publish credential in the system.

If your platform cannot issue a read-only token for something a bot needs to read, that is a finding. Write it down and move on; do not paper over it by granting write.

## The context file

Every bot loads `context/company.md` before its own system prompt. Get this right and mediocre prompts produce decent output. Get it wrong and excellent prompts produce confident nonsense.

```markdown
# Company Context

## What we sell
[One paragraph. Concrete. What the buyer gets, not what the category is called.]

## Who buys it
[Titles, company shape, the trigger that makes them start looking.]

## Who does not buy it
[Explicit. This section does more work than the one above.]

## How we talk
[Voice rules. Banned words. Two examples of on-brand copy, one of off-brand.]

## Claims we can make
[Numbers we can cite, with sources. Anything not on this list is unsupported.]

## Claims we cannot make
[Competitor comparisons, compliance language, performance guarantees, customer names not cleared for use.]

## Current priorities
[The 2–3 campaigns or themes in flight. Update this weekly or the bots drift.]
```

The "claims we cannot make" section is the one that prevents an incident. A drafting bot with no prohibition list will invent a customer logo, a percentage, and a SOC 2 date in the same paragraph, and it will all read beautifully.

## Wiring

```
                    context/company.md
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   [1 Scout]           [3 Draft Engine]    [7 Analyst]
        │                   │                   │
        │            [2 Positioning Editor]     │
        │                   │                   │
        │        ┌──────────┴──────────┐        │
        │   [4 Repurposer]      [5 Sequence]    │
        │        │                     │        │
   [6 Hygienist] └──────────┬──────────┘        │
        │                   │                   │
        └───────────► DRAFT STORE ◄─────────────┘
                            │
                    ┌───────┴───────┐
                    │ HUMAN APPROVAL│  ← named person, per authority-matrix.md
                    └───────┬───────┘
                            │
                      [8 Publisher] ──► outside world
```

Two rules the diagram encodes:

1. **Nothing reaches the Publisher without passing the Positioning Editor.** Bot 2 is not a quality nicety, it is a gate. It is also the cheapest bot to run and the one most teams skip.
2. **The human approval step is not inside a bot.** It is a state transition the Publisher waits on. A bot that approves its own output is a bot with undocumented authority wearing a costume.

## Cost

Eight bots on a mid-size B2B content cadence — a few long-form assets, daily social, two active sequences, a weekly readout — lands in the low tens of dollars per month in API spend. The Draft Engine and Repurposer dominate. The Analyst is cheap and runs weekly.

The cost that matters is not tokens. It is the hour a week someone spends in the approval queue. Budget it explicitly or the queue becomes a rubber stamp, which is the same as having no gate.

## Before you wire bot 8

Fill in [`authority-matrix.md`](authority-matrix.md) with real names. Not roles. Not `#marketing-ops`. Names.

Then run one test: have the Publisher attempt an action that should be prohibited and confirm it refuses and logs the refusal. An untested gate is a gate you are assuming works.
