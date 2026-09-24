# Readiness assessment

## What is actually present

- A business plan, service prices, role split, sales scripts, and lead lists.
- Seven CSV files totaling **5,893 rows**. Their headers contain company names, addresses, industry data, and sales hooks. They have **no phone, email, or named decision-maker fields**. Row count is not proof of unique, currently operating, qualified prospects.
- Assessment, hardening, and authorization templates. These are drafts with example content, not completed client deliverables.
- A research scraper and the new local organizational harness. Neither proves security assessment tooling is deployed or tested.

Evidence: [lead directory](../market-intelligence/leads/), [services](../business-plan/04_services_and_pricing_architecture.md), [governance](../business-plan/03_governance_and_wgu_operations.md), [sales scripts](../sales-and-gtm/02_cold_outreach_scripts.md), [deliverables](../deliverables-and-templates/README.md).

## Main gaps and when they matter

| Gap | Repository finding | Required next action | Stage |
|---|---|---|---|
| Callable prospects | Names/addresses exist; phone and buyer contacts do not | Verify 20 relevant businesses, public business lines, contact role, and source date | Before prospecting batch |
| One initial customer and service | Seven verticals and several technically different offers | Approve one profile and one narrow assessment | Before pitching |
| Honest message | Existing scripts imply customer history and guaranteed outcomes | Use the new scripts; review every exported pitch | Before pitching |
| Business identity | README says LLC; launch checklist still lists formation as open | Confirm actual legal/trading identity; use only accurate titles and suffixes | Before representations/contracts |
| Reliable contact and scheduling | Domain/email and virtual line are described | Test inbound/outbound email, callback, voicemail, calendar invitation, and who answers | Before calling |
| Outreach applicability | No documented campaign review found | Confirm relevant calling rules and suppression process for the actual channels and recipients | Before outbound campaign |
| Credibility packet | Bios contain claims; no demonstrated assessment artifact found | Verify bios and create a labeled lab-based sample with actual evidence | Before detailed sales review |
| Final commercial offer | Prices exist; no evidence of cost/capacity validation | Estimate work, review time, direct costs, and approve a fixed scope/price | Before quote |
| Executable agreement | RoE exists; no complete reviewed MSA/SOW found in file inventory | Prepare an agreement covering business terms and align SOW/RoE | Before signing |
| Banking/payment/tax | Payment vendors and terms are discussed, not verified | Confirm business payment route, invoice, bookkeeping, and service tax treatment | Before collecting money |
| Insurance | Coverage appears as a launch task | Confirm coverage appropriate to the actual services and contract obligations | Before client work; before binding promises of coverage |
| Delivery proof | Checklists exist; no completed assessment rehearsal found | Run one authorized lab assessment end to end, including review and time measurement | Before promising delivery dates |
| Secure collaboration | Harness records are local and gitignored | Decide shared access/storage, backups, vault, and retention ownership | Before handling client data |
| Provider relationships | Vendor names/prices appear in plans | Verify contracts, access, licensing, escalation, and costs before including a provider in an offer | Only if selling that service |
| Support/capacity | Hours, ten-day turnarounds, and response promises are written | Confirm both founders' availability, maximum concurrent jobs, and absence coverage | Before promising service levels |

“Not found” means not demonstrated in this repository, not that you have never done it. No formation search, mailbox test, insurance verification, or client account inspection was performed.

## Claims to retire before using old material

| Existing wording or conflict | Location | Practical correction |
|---|---|---|
| “100% compliant,” passing every audit, preventing coverage denial | sales-and-gtm/02_cold_outreach_scripts.md | Offer documented observations and prioritized actions; do not promise a regulator's or insurer's decision |
| “Most ... we work with” | Same sales scripts | Only state actual customer experience; otherwise describe the service without implying clients |
| 80%+ close rate, insurance invalidation, “completely free” assessment | business-plan/04_services_and_pricing_architecture.md | Remove unsupported statistics and coverage conclusions; any credit needs explicit, approved commercial terms |
| 90%+ threats eliminated / 85% exploit vectors remediated | Existing hardening and assessment templates | Report observed changes and remaining limitations without invented percentages |
| Five endpoints in offer versus 10–25 in authorization template | Services document versus RoE | Use identical asset limits across quote, SOW, and authorization |
| “Complete immunity” and categorical liability protection | Governance document | Treat as drafting objectives for counsel, not enforceable protection already obtained |
| Vendor SOC coverage and low per-user costs stated as operational facts | README and tooling plan | Confirm current provider agreement, scope, configuration, pricing, and escalation before sale |

This kit supersedes older scripts for launch preparation. Historical documents remain unchanged and are not approved client copy.

## What can wait

A paid CRM, bulk lead enrichment, automated outreach, custom dashboard expansion, full rebrand, multiple vertical campaigns, elaborate recurring reports, and a complete managed-security stack can wait until demand justifies them. A short incident contact sheet is useful immediately; building an incident-response service is a separate business decision.
