# Worked Example — RevOps Stack Audit (anonymized)

Series B B2B SaaS, ~180 employees. HubSpot + Salesforce sync, Clay enrichment, Outreach sequencing, n8n for glue, one custom LLM agent for inbound routing. Audit ran in one afternoon plus a half-day of scope verification.

## Headline numbers

- **Agents found:** 23 (team estimated "maybe 10")
- **Orphaned (no claimable owner):** 6
- **Write-capable:** 17
- **Write-capable with UNDOCUMENTED authority:** 14 of 17
- **Reconstruction test (3 actions):** scores 1/3, 1/3, 2/3

## Selected gap-register rows

| Gap | Finding | Severity | Fix applied |
|-----|---------|----------|-------------|
| G-02 | Clay enrichment token had full CRM write scope; workflow only needed 4 fields on Company objects | 4 | Scoped token; 20-minute fix |
| G-05 | n8n "temporary" workflow from a former employee could modify deal stages; no owner, no trigger documentation | 5 | Killed |
| G-09 | Outreach sequence auto-enrolled from a list refreshed by a broken filter — capability to email churned customers | 4 | Threshold + human gate on new-segment enrollment |
| G-11 | LLM router ran as an admin service account; could reassign any lead including named accounts | 4 | Dedicated service identity, object-scoped |
| G-14 | Refund automation respected a $250 limit that existed only in the builder's memory; policy PDF said $100 | 3 | Approval matrix committed to repo; workflow reads it |

## What the team said

The line that stuck, from their ops lead after the reconstruction test: "We could rebuild the workflow in an hour. We couldn't explain last Tuesday in a week."

## Pattern notes (across engagements)

- The most dangerous automations are rarely the newest. They're the oldest — pre-AI Zaps with accumulated scope and departed owners.
- Fixing credentials closes more gaps than writing policy. Do both, credentials first.
- Nobody fails the reconstruction test on purpose. The logs teams keep answer "did it run," never "what did it know, why, and on whose authority."
