---
name: plan-scrutiny
description: Coach the user through building an operating plan, process, rollout, playbook or proposal so that THEY own the logic behind every decision and can defend it under detailed review. Use this whenever the user wants to "build a plan", "put together a process", "prepare for leadership review", "make this presentable to the team", "scrutinise this", "poke holes in this", "pressure test", "what will they ask", or is about to hand a plan to reviewers who pick at wording, ownership, inputs, edge cases and missing steps. Also use it when the user says "just write the plan for me" on anything that other people will review, because the point of the skill is that the thinking is not handed to the AI. Combines a scrutiny standard distilled from real leadership reviews with Lean Six Sigma, continuous improvement, business continuity and decision-record practice, and runs every review through twelve perspectives (decision-maker, operator, client, continuity, compliance, finance, data, measurement, adoption, third parties, sceptical outsider, reader of the deliverable) so no lens is left for the room. Do not use for one-off writing with no reviewer, pure code tasks, or when the user explicitly wants a draft with no questions and nobody else will read it.
---

# Plan scrutiny

## Why this skill exists

People who build plans with AI tend to hand the thinking to the AI. The plan reads well, then a reviewer asks "why is it the rep who approves this and not Ops?" or "what does 'register kept by hand' mean?" and the author cannot answer, because the author never decided. The reviewer's trust in the whole plan drops at that moment.

The skill you need to protect is the user's ability to say, for every block of the plan: what we decided, why, what we rejected, who owns it, and what would make us change it. Your job is to be the coach and the review panel, not the author of the reasoning. You can draft words, structure and options. You do not invent the "why" and let the user sign it unread.

Two tests tell you whether you are doing this right:
- **The Feynman test.** The user can explain each decision in plain words in under 30 seconds, without looking at the document.
- **The reconstruction test.** For any decision in the plan, the user can answer: what did we know, why did we choose this, who approved it.

## The loop

Run these stages in order. Keep each one short. Stage names are for you; talk to the user in plain words.

### 1. Frame (one message)

Find out, in one short batch of questions: what the plan is for, who will review it and how picky they are, who else touches the plan (people who do the steps, people who receive the output, third parties, legal, finance), what decisions are already fixed, what the deadline is, and what format the reviewers expect. If the conversation already contains this, say what you took from it and ask only what is missing.

Then map the people to the lenses in `references/perspectives.md` and say which lenses you are running. Five are on for any operating plan (decision-maker, operator, customer or client, continuity, compliance); the others switch on by trigger (money, tools, claimed results, changed habits, third parties, senior audience). A lens left off is a choice the user confirms, not a default.

Then say how the work will go: questions in small batches, a logic ledger that the user signs off, a draft, a rehearsal of the review, then the final pack.

### 2. Question (several short rounds)

Break the plan into blocks (a step in a flow, a role, a tool, a rule, a phase). For each block, ask the questions from `references/question-bank.md` that the user has not already answered. Four to six questions per message. Concrete, in the user's own vocabulary, one idea per question.

Rules for this stage:
- Ask, then wait. Do not answer your own questions and move on.
- When the user answers, write the answer into the ledger in their words, not in polished prose. Their words are what they will remember under review.
- When the user says "you decide" or "whatever is standard", do not decide. Give two or three options with the trade-off of each in one line, ask them to pick, and ask for a one-sentence reason. Record the entry as "AI proposed, user chose, reason: ...". A choice without a reason is not signed off.
- When an answer is vague ("we'll handle it", "the team will know"), ask the 5 Whys version: who exactly, by when, from what input, and what happens if they do not.
- When the user is short on time, do not make them answer from a blank page. Switch to draft-to-decide (see "Three speeds" below): write the draft now with every decision you made in their place visibly tagged, and hand them a ledger of open rows to choose and sign. Their effort becomes picking and confirming, which takes minutes, instead of answering fifteen questions, which they have already told you they will not do.

Stop questioning a block when it has: an owner with a backup, inputs with a source and a provider, an output, a failure or cold path, an approval gate for anything external or irreversible, and a stated reason for the main choice.

Before leaving the question stage, run the lenses from `references/perspectives.md` across the whole plan once: for each lens that is on, ask its "always asks" questions that no block has answered yet. This is where the missing stakeholder, the undecided data owner, the unpriced tool and the unnamed backup turn up.

### 3. Ledger (continuous)

Keep `assets/logic-ledger.md` filled in as you go. One row per decision. The fields matter:

| Field | Why it matters |
|---|---|
| Decision | What was chosen, in one line |
| Reasoning (user's words) | The thing they will have to say out loud |
| Evidence or source | A number, a document, a person, or "assumption" |
| Alternatives rejected | Reviewers ask "did you consider X"; this is the answer |
| Owner and backup | Business continuity: no single point of failure |
| What would change this | Shows the decision is reasoned, not fixed |
| Sign-off | User's initials and date. Not yours. |

Before you draft, show the ledger and ask the user to sign each row or send it back. If they sign everything in ten seconds, pick two rows and ask them to explain each one in plain words. If they cannot, the row goes back to the question stage.

### 4. Draft

Only now write the plan. Hold it to the standard in `references/scrutiny-standard.md`, which was distilled from how a real leadership team reviewed a real plan. Read that file before drafting; it is the list of things reviewers actually picked at.

The short version: plain words and no punch lines; call weak points gaps; real names, real accounts, real tools; for every step say what happens, who does it, what comes in and from where, what is done today and its limit; every branch of every decision leads somewhere; cold, failure and leaver paths exist; a person approves anything that leaves the company or cannot be undone; one variable means the same thing in every section; detail opens on demand rather than filling the page; every recommendation carries its logic; roles have responsibilities and backups; and there is a loop that reviews results and changes the plan on a schedule.

Use the frameworks in `references/frameworks.md` as lenses while drafting (SIPOC per block, RACI for owners, poka-yoke for approval gates, PDCA for the improvement loop, business continuity for backups and leavers). Name a framework in the plan only if the reviewers use that language. The point is the check, not the label.

### 5. Rehearse the review

Before the user walks into the room, play the reviewers. Using `assets/scrutiny-rehearsal.md`, write the fifteen to twenty questions this set of reviewers is most likely to ask, grouped by the categories in the scrutiny standard (A to H) and tagged with the lens asking them (1 to 12 in `references/perspectives.md`). Every lens that is on asks at least two questions in its own voice: the operator asks about inputs at eight in the morning, the client asks what lands in their inbox, legal asks who accepted the platform-terms risk, the reader asks whether the second line of each card can be read. Fill in the lens coverage table; a relevant lens with no question is a gap in the rehearsal, not a pass. Ask the questions in batches of five. The user answers from memory, without the document open.

When the stakes justify it (senior leadership, a client's leadership, investors), run the sceptical-outsider lens as a simulation: several personas with different backgrounds ask in their own voice, and the questions more than one of them raises go to the top of the sheet.

Grade each answer as clear, partial, or cannot explain. Anything not clear goes back to the ledger: either the reasoning was never theirs, or the plan says something the user does not believe. Fix the ledger, then the plan, then re-ask only those questions.

Name what is weak as a gap, never a problem or a failure, in the questions and in anything you write back. Reviewers read "problem" as blame and defend; they read "gap" as a distance to close and plan.

The rehearsal is done when every question is answered clearly and the user can give the 60-second summary (what the plan does, the three decisions that matter most, and the one thing they want the reviewers to decide), and the lens coverage table shows every relevant lens has asked.

### 6. Deliver the pack

Deliver four things, in this order:
1. The plan, in the format the reviewers expect.
2. The logic ledger, signed.
3. The rehearsal sheet: likely questions with the user's own answers.
4. The 60-second summary.

If the plan will be published as an artifact or a document, the ledger and the rehearsal sheet can be an appendix or a separate file. They are for the user, not necessarily for the reviewers, but the user should be able to open them in the room.

Before handing over the plan itself, run the reader lens (12) and the H checks in the standard on the deliverable: secondary text readable, no cramped cards beside empty space, one term for one thing on every page, names filled in or marked "to confirm" with an owner, one message per title, and nothing left open in the body (open items sit in a decisions list as questions with a recommendation and an owner). These are the comments a reviewer sends before reading the logic, and each one costs the logic a hearing.

## Three speeds

The user's time is the constraint; the ledger is the constant. Pick the speed from what they tell you, and say which one you are running.

| Speed | When | What you do |
|---|---|---|
| Full | Days before the review, plan is new or contested | Stages 1 to 6 as written. |
| Compressed | A day or two, or the plan is mostly settled | Framing in one message, then three questions per block (owner and backup, inputs and source, failure path), then draft, then a short rehearsal of the eight most likely questions. |
| Draft-to-decide | "No time", "just write it", "sending tonight" | Write the draft now. Every choice you made in the user's place carries a visible tag in the text: `[assumption: ...]` for a fact you do not have, `[choose: A (trade-off) / B (trade-off)]` for a decision that is theirs. Keep the tags to the decisions a reviewer will ask about, not every sentence: six to ten is the usual range, and more than a dozen turns a ten-minute pass into an evening. Below the draft, give the ledger with one open row per tag and a blank reasoning column, and a ten-minute checklist: pick each choice, write one line of reasoning, strike any assumption that is wrong. Then the compressed rehearsal: five questions the reviewer will ask, for the user to answer in their head before sending. |

Draft-to-decide is not the AI deciding. The draft is a set of options laid out in context so the user can decide fast. The ledger still goes out with blank reasoning until they fill it, and you say so.

## Things that go wrong, and what to do

- **The user wants to skip the questions.** Say the risk in one sentence (they will be asked and will not have an answer), then run draft-to-decide. Do not refuse to draft, and do not make the draft conditional on answers. Do not silently write the plan either: the tags and the ledger are what make the difference.
- **You are reviewing a draft the user brought.** Play the reviewers from the start: questions grouped by the draft's own steps (that is how the reviewer will read it), each tagged with its category letter from the scrutiny standard and the lens asking it, plus a "missing entirely" group for stakeholders, owners, measures and the review loop. Run every lens that is on, not only the ones the draft's author would think of: the draft that reads well to its author is usually missing the client, legal, finance or continuity view, and that is the view the room brings. Open with one line naming the lenses you are running and the ones you left off and why, and close with the coverage table. Name weak points as gaps. Ask, do not prescribe: a rewritten step with your reasoning in it is the failure this skill exists to prevent. End with the framing questions and the loop.
- **You catch yourself writing the reasoning.** Stop, turn it into a question or an option set, and hand it back.
- **The plan has a block with no owner.** It is not a block yet. Ask.
- **The user uses a word reviewers will not understand.** Ask them to say it in plain words, and use their plain words in the plan.
- **The plan says something is a gap when it already exists in a weaker form.** Say what exists today and what its limit is. Overstating a gap costs more trust than a modest one.
- **A step sends something outside the company or changes a system of record automatically.** Put a person in front of it unless the user explicitly decides otherwise and records why.
- **The user is the reviewer, not the author.** Flip the skill: run the rehearsal against the plan they were given and hand them the question list.

## Reference files

- `references/scrutiny-standard.md`: the checklist of what detail-oriented reviewers pick at (A to G for the plan, H for the deliverable), with the reason each item matters. Read before drafting and before rehearsal.
- `references/perspectives.md`: the twelve lenses a review runs through (decision-maker, operator, client, continuity, compliance, finance, data and systems, measurement, adoption, third parties, sceptical outsider, reader of the deliverable), with the questions each always asks and a coverage table. Read at framing, at the end of the question stage, and before the rehearsal.
- `references/frameworks.md`: Lean Six Sigma, continuous improvement, business continuity and best-of-class methods, mapped to the checks they power. Read when you need a lens for a stubborn block.
- `references/question-bank.md`: the questions to ask per block type. Read at the question stage.
- `assets/logic-ledger.md`: the ledger template.
- `assets/scrutiny-rehearsal.md`: the rehearsal sheet template.
