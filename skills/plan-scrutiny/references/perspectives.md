# Perspectives: the lenses a review runs through

A plan is read by several kinds of people, and each kind picks at a different thing. A rehearsal that only asks the author's own kind of question leaves the other kinds for the room. This file lists the perspectives, what each one looks for, the questions it always asks, and what a clear answer sounds like. Use it in the Frame stage (to map the stakeholders to lenses), in the Question stage (to find the blocks nobody has asked about), in the Rehearsal (every relevant lens asks at least two questions) and when reviewing a draft someone else wrote.

The categories in `scrutiny-standard.md` (A to G, and H for the deliverable) say *what kind of flaw* a reviewer finds. The perspectives here say *who is looking*. Cross them: a rehearsal sheet is complete when every relevant lens has asked, and every category has been touched.

## How to choose the lenses

Five lenses are on by default for any operating plan. The rest switch on when the plan has the trigger named in the table. Say which lenses you are running and why; a lens left out is a decision the user signs, not a default.

| Lens | Default | Switch on when |
|---|---|---|
| 1 Decision-maker | on | always |
| 2 Operator | on | always |
| 3 Customer or client | on | anyone outside the team receives an output |
| 4 Continuity | on | always |
| 5 Compliance, legal and platform terms | on | personal data, contracts, third-party platforms, regulated activity |
| 6 Finance and commercial | | the plan costs money, prices a service or changes margin |
| 7 Data and systems | | a tool, record or integration is introduced or changed |
| 8 Measurement | | the plan claims a result |
| 9 Change and adoption | | people have to work differently from today |
| 10 Third parties | | partners, vendors, contractors or agency staff do steps in the flow |
| 11 Sceptical outsider | | the plan goes to senior leadership, investors or a client's leadership |
| 12 Reader of the deliverable | | the plan is delivered as a page, deck or document (that is, always at delivery) |

## The lenses

### 1. Decision-maker (leadership, the sponsor)

Looks for: what they are being asked to approve, what it costs, what the risk is, and whether the person in front of them owns the logic. Reads the first screen and the decisions list; skims the rest.

Always asks:
- What exactly do you want me to approve today, and what can wait?
- What does this cost, in money and in people's time, and against what baseline?
- What is the one thing that goes wrong, and who answers for it?
- Why this and not the obvious alternative?

Clear answer: one line per decision, with an owner, a cost or "to set by [who] by [when]", and the rejected alternative named.

Gap it found in the field: a deck that listed open questions with no recommendation. The room spent its time on the questions instead of the plan.

### 2. Operator (the person who does the step every day)

Looks for: whether the step can actually be run at eight in the morning with the inputs that exist, how long it takes, what they click, what they do when the input does not arrive.

Always asks:
- Where do I get the input, and what do I do if it is late or wrong?
- How long does this take me, and what do I stop doing to make room?
- Who do I ask when it breaks?
- Which part is the tool, and which part is me?

Clear answer: a SIPOC row per step and a named person for "when it breaks".

Gap it found in the field: two people with the same responsibilities on one account, and a lead with no stated backup, so the plan depended on one inbox.

### 3. Customer or client (whoever receives the output)

Looks for: what they see, what they get, what they are asked to sign off, who contacts them, what data of theirs is used, and whether anything reaches them without a person checking it.

Always asks:
- What arrives in my inbox, from whom, and did a person read it first?
- What am I expected to approve or provide, and by when?
- Who do I call when it goes wrong?
- Whose data is this, and where does it live?

Clear answer: every client-facing output has a sender, an approver, a channel and a response standard; data ownership is a decision in the ledger, not an assumption.

Gap it found in the field: client-side feedback collectors were missing from the plan until a reviewer named them; a handover email could have gone out automatically.

### 4. Continuity (what happens when a person, tool or account stops)

Looks for: single points of failure, leaver and joiner paths, what the plan does by hand when the tool is down, and where the history lives.

Always asks:
- If this person leaves on Friday, what happens on Monday?
- If the tool suspends the account for a week, what do we lose?
- Where is the record, and can the backup open it?
- Who has agreed to be the backup, and do they know the steps?

Clear answer: a backup by name per block, a 48-hour leaver checklist with an owner, and a record outside any one person's account.

Gap it found in the field: conversation history sat in the sender's own account; a team of three had no named backup.

### 5. Compliance, legal and platform terms

Looks for: personal data and lawful basis, opt-out handling, who owns the data, contracts with third parties, the terms of any platform the plan automates against, disclosure (is the sender who they say they are), and who reviews all of this.

Always asks:
- What personal data moves, under what basis, and who can see it?
- How does someone opt out, and how fast does every system honour it?
- Does this break the terms of the platform we run on, and who has accepted that risk by name?
- Who reviews this before launch, and is that written down?

Clear answer: an opt-out rule with a time limit and an owner; a named leader for platform-terms risk; a named reviewer for data protection; no invented identities.

Gap it found in the field: made-up sender profiles still in use; no named owner for the platform-terms risk; data ownership between agency and client undecided.

### 6. Finance and commercial

Looks for: cost per month, cost per account, what is priced to the client, margin, what the baseline is, and when the spend is reviewed.

Always asks:
- What does this cost per month, all in, and who approved it?
- What is the price to the client, and what margin does that leave?
- What is the baseline we are improving from?
- When do we stop spending if it does not work?

Clear answer: a cost line per tool and per person-hour where it matters, a baseline date, and a stop rule.

### 7. Data and systems

Looks for: the system of record, integrations, access, vendor dependence, what is synced and what is re-typed, and what happens when a vendor changes its terms or product.

Always asks:
- Which system is the source of truth, and which ones copy from it?
- What is entered twice today, and who reconciles it?
- Who administers each tool, and who has access?
- What is plan B if this vendor is gone in six months?

Clear answer: one record of truth named, each integration with an owner, a fallback for each critical tool.

### 8. Measurement

Looks for: what is measured today, what will be measured, baseline, target, who reads the number, and what decision the number changes.

Always asks:
- What is the number today?
- What number at day 30, 60, 90, and who set it?
- Who looks at it, how often, and what do they change when it is wrong?
- What does this number not tell us?

Clear answer: a short KPI tree with a "today" state per measure, a baseline owner and date, and a review cadence that produces one change per cycle. "Not measured today" is an acceptable answer; an invented number is not.

### 9. Change and adoption

Looks for: who has to change a habit, what they lose, what training exists, who will resist and why, what the first week looks like.

Always asks:
- Whose day changes, and have they seen this?
- What do they stop doing, and what do they do instead?
- What is the training, and who gives it?
- What tells us in week two that people have not adopted it?

Clear answer: a per-role "today versus new way" line, an onboarding checklist, and an adoption signal in the measures.

### 10. Third parties (partners, vendors, contractors, agency staff)

Looks for: who employs the people in the flow, who owns the accounts they use, what the contract says, what happens when the party changes or leaves.

Always asks:
- Who employs this person, and whose account do they use?
- What does the contract say about the data and the accounts when they leave?
- Who manages them day to day, and who do they escalate to?
- What is the notice period, and is it longer than the leaver checklist?

Clear answer: employer and account ownership stated per person; an open item marked "to decide" with an owner where it is not.

Gap it found in the field: it was undecided who employed the agency's inside sales people and who owned the accounts they sent from.

### 11. Sceptical outsider (a senior founder, an investor, a client's leadership)

Looks for: whether the fundamentals hold without the vocabulary. Would they buy this? What is the simplest version? What is the author not saying?

Always asks:
- Say it in one sentence to someone who has never heard of the tool.
- What is the simplest version that gets most of the result?
- What are you not telling me?
- What would you do with half the budget?

Clear answer: the 60-second summary works without the document, and the author can name the version they would run with half the resources.

Run this lens as a simulation when the stakes justify it: several personas with different backgrounds asking in their own voice, then a tally of which questions came up from more than one of them. Those are the questions the room will ask.

### 12. Reader of the deliverable (the page, the deck, the document)

Looks for: can it be read. Contrast, text size, density, terminology, whether a term on slide 3 matches slide 11, whether the names are filled in, whether the title of each slide says one thing.

Always asks:
- Can I read the second line inside each box from the back of the room?
- Does this card or table have more in it than I can take in?
- Is the same thing called the same thing everywhere?
- Which names are still "to confirm", and who confirms them by when?

Clear answer: the H checks in `scrutiny-standard.md` pass. Nine comments on a single deck in one sitting, all about readability and terminology, is what this lens prevents.

## Coverage check

Before the rehearsal is called done, fill this in. A relevant lens with no question is a gap in the rehearsal, and it goes into the sheet before the user walks in.

| Lens | Relevant? | Questions asked | Weakest answer | Ledger row |
|---|---|---|---|---|
| 1 Decision-maker | | | | |
| 2 Operator | | | | |
| 3 Customer or client | | | | |
| 4 Continuity | | | | |
| 5 Compliance, legal, platform terms | | | | |
| 6 Finance and commercial | | | | |
| 7 Data and systems | | | | |
| 8 Measurement | | | | |
| 9 Change and adoption | | | | |
| 10 Third parties | | | | |
| 11 Sceptical outsider | | | | |
| 12 Reader of the deliverable | | | | |
