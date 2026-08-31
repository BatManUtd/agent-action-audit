# Authority Matrix — Grok Marketing Team

The delegation-of-authority table for the eight bots. Fill in the names before you wire bot 8. Keep it in version control; every edit gets a commit message naming who approved the change.

This is the [approval matrix template](../templates/approval-matrix.md) applied to a real build. It is the file that turns eight prompt specs into a system you can defend.

## Agent inventory

| ID | Bot | Runs as (service identity) | Credential scope | Capability classes | Owner (named) |
|----|-----|---------------------------|------------------|--------------------|---------------|
| M-01 | Signal Scout | `svc-grok-scout` | Read-only: CRM, enrichment, search | none | |
| M-02 | Positioning Editor | `svc-grok-editor` | Read-only: draft store | none | |
| M-03 | Draft Engine | `svc-grok-draft` | Read-only: draft store, search | none | |
| M-04 | Repurposer | `svc-grok-repurpose` | Read-only: draft store | none | |
| M-05 | Sequence Writer | `svc-grok-sequence` | Read-only: CRM, sequencer | none | |
| M-06 | List Hygienist | `svc-grok-hygiene` | Scoped write: named fields only | 2 (data mutation) | |
| M-07 | Campaign Analyst | `svc-grok-analyst` | Read-only: analytics, CRM, ads, email | none | |
| M-08 | Publisher | `svc-grok-publisher` | Send/publish — the only one | 1, 2 (external comms, mutation) | |

Capability classes are from [Step 2 of the audit](../audit/02-capability-map.md). Six of eight bots hold none. That is the design working.

## Authority by action class

| Action class | Autonomous below | Requires approval above | Approver (named) | Backup approver | Prohibited entirely | Review date |
|--------------|------------------|------------------------|------------------|-----------------|---------------------|-------------|
| Draft production | All drafting to the draft store | — | n/a | n/a | Publishing from any drafting bot | |
| Positioning verdict | PASS / REVISE / BLOCK | — | n/a | n/a | Bot overriding its own BLOCK | |
| CRM field normalization | In-scope fields, <5% of records per run | 5% of records, or any new field in scope | | | Owner, lifecycle, consent, revenue fields | |
| Segment membership | `auto_`-prefixed lists, <10% delta | 10% delta, or any non-`auto_` list | | | Lists tied to consent or billing | |
| Record merge / delete | Nothing autonomous | Any | | | Deletion without backup | |
| External publish (owned channels) | Nothing autonomous | Any | | | Destinations not on the approved list | |
| External send (email) | Nothing autonomous | Any | | | Churned customers; contacts in open support escalations; any list not named in the approval | |
| Paid spend | $0 — no bot may commit spend | Any | | | All bots. Spend is not delegated to this system at all | |
| Access change | Nothing autonomous | Any | | | All bots. No bot may modify credentials or scopes, including its own | |

## Approved destinations

Bot 8 may publish only to destinations on this list. Adding one is a matrix change with a named approver, not a config tweak.

| Destination | Type | Max audience per action | Approver |
|-------------|------|------------------------|----------|
| Company blog | Owned publish | n/a | |
| LinkedIn company page | Owned social | n/a | |
| X company account | Owned social | n/a | |
| Newsletter — subscribers | Email send | | |
| Outbound sequence — named list | Email send | | |

## Rules

- **Approver is a person, not a role or a channel.** `#marketing-ops` is not an approver. Roles go stale, channels diffuse accountability, and neither can be named in a postmortem.
- **Every threshold needs a unit and a window.** "Under 500 recipients per send, max 3 sends per list per week" — not "reasonable volume."
- **An empty Prohibited cell means nobody has thought about it.** Fill it or write down why it is genuinely empty.
- **Review dates are mandatory.** Unreviewed authority is undocumented authority with better formatting.
- **Bounds live here, not in prompts.** A prompt is a request. The credential scope and the orchestrator's gate are the enforcement. If the only thing stopping a bot from sending is a sentence in its system prompt telling it not to, it is not stopped — [Step 3](../audit/03-authority-map.md) counts that as undocumented authority, correctly.

## Metrics to track

The three numbers from the audit, applied to this build:

| Metric | Target | Why |
|--------|--------|-----|
| Write-capable bots on undocumented authority | 0 | The audit's definition of done |
| Publisher refusals per month | > 0 | Zero refusals means the checks are not binding, or nobody is testing them |
| Median reconstruction score on published actions | 3/3 | Achievable by construction here — the Publisher's log answers all three questions |

A reconstruction score below 3/3 on this build means the Publisher's logging has degraded, since the log was designed to answer all three. Treat it as an incident, not a metric miss.

## Change log

Every edit to this file gets a row. This table is the record of who granted what authority and when — which is exactly the record [Step 3](../audit/03-authority-map.md) finds missing in most stacks.

| Date | Change | Requested by | Approved by |
|------|--------|--------------|-------------|
| | Initial matrix | | |
