# Morrison Cyber Defense operating harness

A shared home for company projects, repeatable procedures, and reusable templates. Start with the weekly company workflow and create a project for each real initiative or client engagement. Procedures and blank templates are versioned; actual working records default to the gitignored `local/` directory.

## Start here

From the repository root, using Python 3.10 or later on Linux:

```bash
python3 harness/mcd.py init
python3 harness/mcd.py new company-launch --name "Company launch" --owner Keenan
python3 harness/mcd.py task "Review launch priorities with Dad" --project company-launch --owner Keenan --due 2026-09-30
python3 harness/mcd.py dashboard
```

Use dates that match your actual commitments. To create a client workspace:

```bash
python3 harness/mcd.py new example-client --name "Example Client" --owner Principal --kind client
python3 harness/mcd.py task "Confirm scope and authorization" --project example-client --owner Principal --due 2026-09-30
python3 harness/mcd.py status T0001 doing --project example-client
```

Task IDs are local to their project; omit `--project` for company-wide tasks. Set a task to `todo`, `doing`, `blocked`, or `done`. Use `--note` on `status` to record a blocker or completion reference. Edit project status in `project.json`; suggested values are planning, active, blocked, complete, and archived.

`--workspace /path/to/workspace` before the command selects another location. Keep alternative workspaces outside version control and apply your own access controls. The CLI uses a local advisory lock and rejects concurrent commands with a retry message. Coordinate manual spreadsheet/text-editor changes separately; those editors do not honor the CLI lock. Network filesystem locking is not supported. It does not synchronize across computers or provide authentication, encryption, notifications, or enforced approvals. Back up working data separately and test recovery.

## Procedures

| Procedure | When to use it |
|---|---|
| [Prospecting](workflows/01-prospecting.md) | Research, qualification, outreach drafts, and follow-ups |
| [Onboarding](workflows/02-onboarding.md) | Scope, contacts, authorization, and kickoff |
| [Assessment](workflows/03-assessment.md) | Evidence collection, findings, and reporting |
| [Delivery](workflows/04-delivery.md) | Reviewed changes, validation, and handoff |
| [Stewardship](workflows/05-stewardship.md) | Monthly client service reviews |
| [Incidents](workflows/06-incidents.md) | Intake, responder handoff, and action logging |
| [Company operations](workflows/07-company-operations.md) | Weekly planning, finances, obligations, and renewals |
| [Quality and data](workflows/08-quality-and-data.md) | Review, storage, delivery, and retention |
| [Offboarding](workflows/09-offboarding.md) | Acceptance, transition, and access removal |

## Working records

`init` creates company tasks, a prospect pipeline, business obligations register, metrics register, and decision log. Edit CSV registers in a spreadsheet or text editor, preserving headers. Use ISO dates (`YYYY-MM-DD`). Spreadsheet cells imported from outside sources should be treated as untrusted text, not formulas.

For pipeline records use unique IDs, verified source references, an owner, a next action, and a due date. Suggested stages: research, qualified, discovery, proposal, won, lost, do-not-contact. Check the do-not-contact field before preparing outreach. Lead lists are source material; copy only selected, verified prospects into the pipeline. Outreach is manual; no messages are sent by the CLI.

Internal projects get a project brief, tasks, and decisions. Client projects additionally get scope, approval log, evidence index, findings, changes, assessment report, monthly review, incident record, and closeout template. Use stable IDs such as E001, F001, and C001 and cross-reference them. Blank records and newly generated files do not indicate completed work or authorization.

Store raw client evidence and secrets in approved restricted systems; reference their locations here. Gitignore prevents ordinary staging, not access or disclosure. Review files before sharing or committing.

## Existing company references

- [Business plan](../business-plan/README.md): strategy and pricing assumptions to confirm.
- [Sales playbook](../sales-and-gtm/README.md): source material for drafts.
- [Lead lists](../market-intelligence/leads/): research candidates.
- [Scraper](../market-intelligence/scraper/README.md): separate research tool; not run by this harness.
- [Existing deliverables](../deliverables-and-templates/README.md): reference structures; examples and technical recommendations need review before use.
- [Infrastructure](../infrastructure/README.md): internal technical reference.

The harness does not run security tools, change client systems, send messages, or certify compliance. Client reports start blank so example findings and projected results cannot be mistaken for observed facts. Technical procedures must be checked against current authoritative documentation when used.

## Maintenance

Review procedures after each engagement and record process changes in version control. At the weekly founders meeting, review overdue tasks, active projects, prospect next actions, business obligations, and decisions. Every action should have one owner and a clear completion criterion.

Run checks from the repository root:

```bash
python3 -m unittest discover -s harness/tests -v
```

## Data integrity

Task writes validate exact CSV headers, row widths, unique IDs, dates, owners, and statuses before replacing the file atomically. UTF-8 BOMs and quoted multiline notes are supported. Invalid files are reported without being overwritten; restore or correct them explicitly. Symlinks in workspace paths and working files are rejected. Project creation publishes a complete directory only after its templates are ready. These controls do not replace backups or operating-system access permissions.

## Import prospect candidates

The scraper's offline `pipeline-leads` command produces exactly the pipeline register schema. Preview and import from the repository root:

```bash
python3 harness/mcd.py import-leads harness/local/contractor-clinic-candidates.csv --dry-run
python3 harness/mcd.py import-leads harness/local/contractor-clinic-candidates.csv
```

Optionally add `--owner Keenan` to assign newly imported rows. Existing rows are never updated by import: IDs and organization/location matches are skipped, and an existing organization opt-out suppresses additional locations of that organization. Reimporting the same candidate file is a no-op. Duplicate IDs or malformed headers/rows/dates cause an error before any write. Import and task operations use the same lock and atomic replacement logic.

Pipeline rows require a unique nonempty ID, organization, and one of the documented stages. Use `true`, `false`, or blank for `do_not_contact`; dates in `verified_at` and `due` must be blank or `YYYY-MM-DD`. Candidate imports leave verification dates and contacts unfilled. A registry address in `contact_reference` is a location reference, not a researched phone number or email. Research candidates before outreach.

See the [scraper normalization instructions](../market-intelligence/scraper/README.md#harness-pipeline-export-offline) for filtering and deduplication limits. Keep populated candidate exports under `harness/local/` or another restricted, unversioned workspace.
