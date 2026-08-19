# Step 5 — The Reconstruction Test

**Goal:** prove — or disprove — that you can explain a past agent action after the fact. This is the test an auditor, a regulator, or your own post-mortem will run for you eventually. Better to run it yourself first.

## Setup

Pick ONE consequential action an agent actually took in the last 30 days. Not a hypothetical. Choose from your highest-severity gap-register rows if you have them: a record mutation, an external send, a routing decision, a refund.

Set a 60-minute timer. Use only what's already logged — no asking the person who built the workflow to explain from memory. (Memory is not a record.)

## The three questions

### 1. What did it know?
Reconstruct the inputs at action time: the record state, the enrichment data, the trigger payload. Not what the data looks like *now* — what it looked like *then*.
- Pass: you can produce the input state with timestamps.
- Fail: you can only see current state, or the inputs weren't captured.

### 2. Why did it act?
What was the logic or objective at the moment of action — the branch it took, the prompt it ran, the rule version in force *that day*?
- Pass: you can point to the exact logic version and the condition that fired.
- Fail: the workflow has been edited since and history isn't versioned, or the LLM prompt/response wasn't logged.

### 3. Who authorized it?
Under what standing authority did it run — and can you name the human accountable for that grant?
- Pass: a named person, a documented grant, bounds the action respected.
- Fail: "it was set up by someone on the ops team in 2024."

## Scoring

| Result | Meaning |
|--------|---------|
| 3/3 | You can defend this action to anyone. Rare. |
| 2/3 | Partial reconstruction — you'd survive an internal review, not an external one. |
| 0–1/3 | The action is unexplainable. If it had gone wrong, you could not distinguish a model failure from a policy failure from an authorization failure. |

## The point

Run it on three actions across different agents. If your median is under 2/3, your stack has an accountability gap that no amount of smarter models fixes — because the missing piece isn't intelligence. It's the record of context, reasoning, and authority at decision time.

Found that gap and can't close it with process alone? That's exactly the research the maintainer is doing — see README.
