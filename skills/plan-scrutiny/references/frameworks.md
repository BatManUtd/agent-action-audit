# Frameworks as lenses

These methods are here for the checks they give you, not for their names. Name a framework in the plan only if the reviewers speak that language. Each entry says what the method is in one line, which check in the scrutiny standard it powers, and the question it gives you to ask the user.

## Lean Six Sigma

**SIPOC (Supplier, Input, Process, Output, Customer).** One row per step. Powers C1. Ask: for this step, who supplies what, what does the step do, what comes out, who receives it? A step that cannot fill the row is not understood yet.

**DMAIC (Define, Measure, Analyse, Improve, Control).** The spine of any improvement plan. Powers B2, G1. Ask: what is the measured baseline today (Measure), what causes the gap (Analyse), what changes (Improve), and what keeps it from sliding back (Control)? Most AI-written plans skip Measure and Control.

**5 Whys.** Ask why five times to get from the symptom to the cause. Powers F1. Use it on every gap: "replies are slow" → why → "nobody is alerted" → why → "the alert rule does not exist" → the fix is the rule, not a reminder to be faster.

**RACI (Responsible, Accountable, Consulted, Informed).** One accountable person per block, never two. Powers D1, D2. Ask: who does the work, who answers for it, who must be asked first, who is told after? If "accountable" has two names, ask which one the reviewer should call.

**Poka-yoke (mistake-proofing).** Design so the wrong thing cannot happen rather than hoping it will not. Powers E1. Ask: what would make this mistake impossible, not just unlikely? A draft that cannot be sent without a click is poka-yoke; a reminder to be careful is not.

**Waste (the seven wastes, applied to office work).** Waiting, handoffs, rework, over-processing, unused talent, excess motion, overproduction. Powers C4. Ask: where does this plan make someone wait, re-enter data, or do a step nobody reads?

**Value stream map.** The flow with time and handoffs marked. Powers E3. Ask: how long does each step wait before the next person touches it?

## Continuous improvement

**PDCA (Plan, Do, Check, Act) / Kaizen.** Small changes on a fixed cadence. Powers G1. Ask: what is the cadence, who runs it, what input does it read (a scorecard, a log), and what is the one change per cycle? A review with no input and no decision is a meeting, not a loop.

**A3 thinking (Toyota).** The whole problem, analysis, countermeasure and follow-up on one page. Powers C4, F1. Ask: can the plan's logic fit on one page a reviewer reads in two minutes, with the detail behind it?

**Retrospective rules.** What worked, what did not, what we change, who owns the change by when. Powers G2. Ask: where is the feedback written down, and who turns it into a change?

## Business continuity

**Single point of failure.** Any step that stops when one person, tool or account stops. Powers C3, D1. Ask: if this person is out for two weeks, what happens on day one? If the answer is "it waits", name a backup.

**Leaver and joiner process.** What happens in the first 48 hours when someone leaves or joins. Powers C3. Ask: what is in the leaver checklist, who runs it, what is the handover artefact?

**Recovery objectives.** How long can this be down, and how much can be lost. Powers C3. Ask: if the tool is suspended for a week, what do we lose and what do we do by hand?

**Dependency register.** Every external tool, access, contract or person the plan depends on. Powers B1, D3. Ask: what access does this need, who grants it, and what is plan B if it is refused?

## Best of class methods

**Pre-mortem (Klein).** Assume the plan failed six months from now; write the story of why. Powers C2, C3, F3. Ask the user to tell the failure story first, then check the plan covers each cause.

**Decision records (ADR style).** Context, decision, alternatives, consequences, status. Powers F1, F2, F3. This is what the logic ledger is.

**Six-pager and FAQ (Amazon).** Narrative plus the questions a reader will ask, answered in advance. Powers the rehearsal. Ask: what are the ten questions the sharpest reader asks, and are they answered in the document?

**Checklists (Gawande).** Short, pause-point checklists at the moments where things go wrong. Powers E1. Ask: where are the pause points, and what is checked at each?

**Steel-manning.** State the strongest case for the rejected alternative before dismissing it. Powers F2. Ask: what is the best argument for doing it the other way?

**Feynman technique.** Explain it in plain words to someone outside the team; where you stumble is where you do not understand it. Powers A2 and the whole skill. Ask the user to explain a block to an imaginary new hire in three sentences.

**Red team.** Someone whose job is to break the plan. Powers the rehearsal. You play this role in stage 5.

**OKR-style measures.** Each outcome with a number and a date. Powers B2, G1. Ask: how will we know in 30 days whether this worked?

## Choosing a lens

| Symptom in the plan | Lens |
|---|---|
| Step has no inputs or outputs | SIPOC |
| Gap stated as a symptom | 5 Whys |
| Two people "own" a block | RACI |
| Automated external action | Poka-yoke, checklists |
| Only the happy path | Pre-mortem, single point of failure |
| No review cadence | PDCA |
| Decision with no reason | Decision record, steel-man |
| Reviewer will not understand a term | Feynman |
| Plan too dense on first read | A3, waste |
