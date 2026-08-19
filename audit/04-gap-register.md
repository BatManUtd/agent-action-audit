# Step 4 — Gap Register

**Goal:** capability minus authority = exposure. Rank it, own it, close it.

## Building the register

A gap exists wherever Step 2 says an agent CAN do something and Step 3 says the authority is UNDOCUMENTED, exceeded, or explicitly absent.

| Gap ID | Agent | Capability without authority | Worst plausible action | Reversible? | Blast radius | Severity (1–5) | Owner | Fix |
|--------|-------|------------------------------|------------------------|-------------|--------------|----------------|-------|-----|
| G-01 | | | | | | | | |

## Scoring severity

Score on worst *plausible* action, not average behavior. The enrichment bot that CAN overwrite every account owner field scores on "reassigns the entire book of business," not "fixed a typo."

- **Reversibility dominates.** Irreversible + external (sent emails, deleted records without backup, money moved) = automatic 4+.
- **Blast radius:** one record, one segment, one system, or everything the credential reaches.
- **Detection lag:** would you know in minutes, days, or at the QBR?

## Standard fixes (cheapest first)

1. **Narrow the credential.** Most gaps close by replacing a full-scope token with a scoped one. No process change.
2. **Add a threshold + named approver** for actions above a bound (templates/approval-matrix.md).
3. **Log the decision** at action time (templates/agent-decision-log.csv) — doesn't prevent, but makes reconstruction possible.
4. **Split the workflow:** autonomous below the line, human-gated above it.
5. **Kill it.** Orphaned automations with write access and no owner don't get fixed. They get turned off.

## Done when

Every gap has a severity, an owner, and a fix with a date. Track one number over time: **count of write-capable agents operating on undocumented authority.** Getting it to zero is the audit's definition of done.
