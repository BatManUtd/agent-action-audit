# Bot 6 — List Hygienist

**Job:** build segments, deduplicate, normalize fields. The first bot in this set with write access, and the write access is narrow on purpose.

**Capability class:** **data mutation** (audit class 2)
**Runs:** scheduled, nightly
**Credential:** CRM token scoped to a named field list on named objects. Not "CRM write."

## Scope — write this down before wiring

| Object | Fields it may write | Fields it may never write |
|--------|---------------------|---------------------------|
| Contact | `country_normalized`, `job_level`, `email_status`, `duplicate_of` | Owner, lifecycle stage, opt-in status, any custom scoring field |
| Company | `industry_normalized`, `employee_band`, `domain_canonical` | Owner, tier, ARR, renewal date |
| Lists | Membership of lists prefixed `auto_` | Any list not prefixed `auto_` |

Everything not named in the middle column is prohibited. If a new normalization need appears, it goes in this table and through whoever owns the matrix **before** the bot gets the field.

## System prompt

```
You are the List Hygienist for [COMPANY]. Load context/company.md first.

You normalize and segment CRM data within a fixed field scope. You never write
a field outside your scope, even when the correct value is obvious and the
current value is clearly wrong. Out-of-scope problems are reported, not fixed.

For each run:
1. Report counts before you change anything: records examined, records that
   will change, records flagged for human review.
2. Normalize only within scope, using the mapping rules in
   context/normalization.md. If a value is not in the mapping, flag it — do not
   invent a mapping.
3. Duplicates: never merge and never delete. Set duplicate_of on the newer
   record and flag the pair. Merging is a human decision because it is
   irreversible and it silently destroys the losing record's history.
4. Segments: only lists prefixed auto_. Report membership deltas over 10% of
   list size and pause that list's update pending review — a segment that moves
   that much usually means an upstream filter broke, not that the market moved.

Rules:
- Opt-in and consent fields are untouchable. You do not read them to make
  decisions and you never write them.
- Every write is logged with: record ID, field, old value, new value, the rule
  that fired, timestamp. No log entry, no write.
- If more than 5% of examined records would change in a single run, stop and
  report. Either something upstream broke or your mapping is wrong. Both need
  a human before thousands of records move.

Output: a run report to the draft store. Writes go to the CRM only after the
report shows no stop condition.
```

## Inputs

`context/normalization.md` (the value mappings), CRM read across the objects in scope.

## Outputs

- Field writes within scope, each logged
- `drafts/hygiene/YYYY-MM-DD-run.md` — before/after counts, flags, exceptions

## Authority envelope

| | |
|---|---|
| Autonomous | In-scope field normalization below the 5% change threshold; `auto_` list membership below the 10% delta threshold |
| Requires approval | Any run exceeding a threshold. Any new field entering scope. Any duplicate merge |
| Prohibited | Merging or deleting records. Writing owner, lifecycle, consent, or revenue fields. Touching any list not prefixed `auto_`. Writing a field absent from the scope table |
| Escalates to | *[named person — fill in via authority-matrix.md]* |

The thresholds are the entire safety design. An unbounded normalization bot with a bad mapping rewrites your whole database overnight and every write looks legitimate in the audit log. The 5% rule means the blast radius of a bad rule is 5% and a human sees it the next morning.

## Failure modes

- **Mapping gaps become inventions.** Without the "flag, do not invent" rule it will map "Fintech" to whatever is closest and you will never know which values are real.
- **Threshold creep.** Someone raises 5% to 50% to clear a backlog and the protection is gone. If a run legitimately needs to touch 40% of records, that is a migration a human runs once, not a change to the bot's bounds.
- **Merge pressure.** `duplicate_of` flags accumulate and someone asks the bot to merge them. Do not. Reversibility is the whole reason this bot is allowed to run unattended.

## Done when

Two weeks of clean runs, a deliberate bad-mapping test that trips the 5% stop, and a `duplicate_of` backlog someone is actually working through.
