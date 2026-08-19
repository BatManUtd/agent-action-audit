# Approval Matrix Template

The delegation-of-authority table your automations can actually read. One row per action class. Keep it in version control; every edit gets a commit message naming who approved the change.

| Action class | Autonomous below | Requires approval above | Approver (named) | Backup approver | Prohibited entirely | Expiry / review date |
|--------------|------------------|------------------------|------------------|-----------------|---------------------|----------------------|
| Refund / credit | $200, <30d order age | $200 | | | Enterprise-tier accounts | |
| CRM record mutation | Field updates on non-customer records | Owner reassignment, stage changes, deletes | | | Bulk deletes without backup | |
| External email send | Sequences to opted-in prospects | New audience segments, >500 recipients | | | Customers in open support escalations | |
| Spend / commitment | $0 (none autonomous) | Any | | | | |
| Access change | Nothing autonomous | Any | | | Production credentials | |

## Rules

- Approver is a person, not a role or channel. Roles go stale; channels diffuse accountability.
- Every threshold needs a unit and a window ("3 per customer per quarter", not "a few").
- An empty Prohibited column means nobody has thought about it. Fill it or say why.
- Review dates are mandatory. Unreviewed authority is undocumented authority with better formatting.
