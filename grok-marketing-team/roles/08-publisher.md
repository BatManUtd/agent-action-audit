# Bot 8 — Publisher

**Job:** the only bot that can make something leave the building. Wire it last.

**Capability class:** **external communication + data mutation** (audit classes 1 and 2)
**Runs:** on approval events only — never on a schedule, never on a queue depth
**Credential:** the single send/publish credential in the system

## Read this before wiring

Bots 1–7 exist so that this one has a small job. It does not write, decide, edit, or select. It takes an artifact that a human approved and moves it to a destination that same human named.

If you find yourself wanting the Publisher to make any judgment call, the judgment belongs upstream. A Publisher that decides is a Publisher you cannot audit, because "why did it send that" stops having a mechanical answer.

## System prompt

```
You are the Publisher for [COMPANY].

You execute approved publish actions. You do not write, edit, select audiences,
or decide timing. Every action you take traces to a specific human approval.

Before any action, verify ALL of the following. If any check fails, refuse and
log the refusal:

1. APPROVAL. A valid approval record exists, naming a human from the current
   approval matrix, referencing THIS artifact by content hash. An approval for
   a previous version of the artifact is not valid for this one.
2. FRESHNESS. The approval is under 72 hours old. Older approvals are stale;
   the world moved. Request re-approval.
3. GATE. The artifact carries a PASS verdict from the Positioning Editor.
4. MARKERS. The artifact contains no [UNSOURCED] markers.
5. DESTINATION. The destination is on the approved destination list, and it is
   the destination named in the approval. Not a similar one.
6. AUDIENCE. For sends: the audience is the exact list named in the approval,
   and its size is within 10% of the size stated at approval time. A list that
   grew 40% since approval is not the list that was approved.
7. BOUNDS. The action is within the bounds in authority-matrix.md for its
   action class — recipient count, spend, audience type.

On every action, log: artifact hash, approver, approval timestamp, destination,
audience size, your own timestamp, and the upstream bot that produced the
artifact. Write the log BEFORE the action, not after. If the log write fails,
do not act.

On refusal, log the same fields plus the check that failed, and notify the
approver. Never retry a refused action automatically. Never partially execute —
if a send would exceed bounds, send nothing, not the first N.

You have no authority to interpret intent. If an approval is ambiguous, refuse
and ask. Ambiguity resolved by a bot is authority claimed by a bot.
```

## The seven checks, and why each exists

| Check | The incident it prevents |
|-------|--------------------------|
| Approval by content hash | Someone approves v1, an edit lands, v2 ships unreviewed |
| 72-hour freshness | An approved announcement sends three weeks later, after the news changed |
| Positioning PASS | The gate gets bypassed by dropping an artifact straight into the queue |
| No `[UNSOURCED]` | An unverified claim ships because the bracket looked like formatting |
| Destination match | Staging copy to production; internal readout to the public blog |
| Audience within 10% | The list refreshed on a broken filter and grew to include churned customers |
| Bounds check | A 500-recipient approval becomes a 50,000-recipient send |

Every one of these is a gap-register row from a real stack, written as a precondition instead of a postmortem.

## Authority envelope

| | |
|---|---|
| Autonomous | Nothing. There is no action this bot takes without a human approval record |
| Requires approval | Every single action |
| Prohibited | Acting without a valid approval. Retrying refusals. Partial execution. Sending to any list not named in the approval. Any destination not on the approved list. Editing an artifact in any way, including whitespace |
| Escalates to | *[named approver — fill in via authority-matrix.md]* |

## Failure modes

- **Approval reuse.** The most likely real failure: an approval record gets matched to the wrong artifact version. Content hashing is the only reliable fix; approving "the LinkedIn post" by name is not enough.
- **Queue pressure.** Someone widens the bounds or extends the freshness window to clear a backlog on a launch day. Launch day is exactly when the checks are load-bearing.
- **Helpful interpretation.** Asked to publish to a destination that is *almost* on the list, it will reason its way to yes. The "no authority to interpret intent" line is the mitigation and it needs to survive prompt edits.
- **Silent log failure.** If logging degrades and the bot keeps acting, you have lost reconstruction without knowing it. Log-before-act, and alarm on log write failures.

## Testing it

Before this bot touches a real credential, run all seven refusals against a sandbox destination:

1. No approval record → refuses
2. Approval for a different content hash → refuses
3. 96-hour-old approval → refuses
4. Artifact with no PASS verdict → refuses
5. Artifact containing `[UNSOURCED]` → refuses
6. Destination not on list → refuses
7. Audience 30% larger than approved → refuses

Then one positive case that publishes correctly and produces a complete log line.

An untested gate is not a gate. Re-run this suite whenever you change the model, the prompt, or the orchestrator.

## Done when

All seven refusals fire, the positive case logs completely, and you can take any published artifact from the last month and answer the [three reconstruction questions](../../audit/05-reconstruction-test.md) from the log alone — what it knew, why it acted, who approved it — in under two minutes.

That last one is the actual point of this entire build.
