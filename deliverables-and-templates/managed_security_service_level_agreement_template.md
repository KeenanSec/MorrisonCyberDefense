# Managed Security Service Level Agreement (SLA)
## Morrison Cyber Defense LLC

**SLA Reference:** `MCD-SLA-RETAINER-[Year]`  
**Governing Agreement:** Master Services Agreement ("MSA") between Morrison Cyber Defense LLC ("Provider") and `[Client Legal Entity Name]` ("Client")  
**Effective Date:** `[Retainer Start Date]`  
**Service Tier:** Tier 3 — Monthly Continuous Security Stewardship Retainer  
**Monthly Fee:** `$1,750.00 – $2,500.00 / month` *(as designated in the applicable Retainer Schedule)*  

---

### 1. Dual-Tier Operational Delivery Model

To ensure enterprise-grade protection without founder burnout, Contractor provides a structured, dual-tier operational delivery model:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: 24/7/365 CONTINUOUS THREAT MONITORING & RAPID CONTAINMENT       │
│ • Powered by: Huntress Labs Managed SOC (Nocturnal & Holiday Coverage) │
│ • Scope: Automated Host Isolation, Process Telemetry, Ransomware Kill  │
│ • Availability: 24 Hours a Day, 7 Days a Week, 365 Days a Year         │
└────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │ (Escalations & Incident Triage)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 2: DAYTIME STRATEGIC ADVISORY, DRIFT & TENANT STEWARDSHIP        │
│ • Powered by: Morrison Cyber Defense LLC (Keenan Morrison & Principal)│
│ • Scope: M365 Baseline Audits, Conditional Access Drift, CIPP Admin    │
│ • Availability: Monday – Friday, 8:00 AM – 5:00 PM Central Time (CT)   │
└────────────────────────────────────────────────────────────────────────┘
```

1.1 **Tier 1 (24/7/365 Huntress MDR SOC):** Continuous background endpoint and identity telemetry collection. In the event of active malicious execution (e.g., ransomware payload launch, suspicious PowerShell spawning, credential dumping), the Huntress human SOC analyst team executes rapid automated or analyst-driven host isolation immediately at machine speed, halting lateral movement across the network.

1.2 **Tier 2 (Daytime Practice Advisory & Stewardship):** Morrison Cyber Defense co-founders oversee routine operational security, monitor policy drift across Microsoft 365, evaluate monthly CIPP telemetry, push tenant configuration updates, and conduct quarterly executive risk briefings during standard Texas business hours.

---

### 2. Incident Classification & Service Level Commitments

Contractor categorizes all security events, support inquiries, and alert notifications into four (4) severity levels, with specific response time objectives:

| Severity Level | Definition & Criteria | SOC / Huntress Response | MCD Advisory Response | Ongoing Status Update Frequency |
| :--- | :--- | :--- | :--- | :--- |
| **Severity 1 (Critical)** | Active ransomware outbreak, verified active credential intrusion, unauthorized administrative tenant takeover, or massive data exfiltration event. | **< 15 Minutes** (Host isolation initiated) | **< 60 Minutes** (Direct executive call) | Every 2 Hours until contained |
| **Severity 2 (High)** | Confirmed business email compromise (BEC) attempt, single compromised user mailbox, unmitigated critical vulnerability (CVSS > 9.0) with active exploit. | **< 30 Minutes** (Session revoked / alert) | **< 2 Business Hours** | Every 4 Business Hours |
| **Severity 3 (Medium)** | Configuration drift detected (e.g., non-compliant device, disabled MFA policy), new administrative user provisioning review, routine suspicious email submission. | Next scheduled analysis cycle | **< 4 Business Hours** | Daily until resolved |
| **Severity 4 (Low / Info)** | General security advisory questions, scheduled quarterly review requests, routine user add/remove notifications, compliance documentation requests. | Standard operational logging | **< 8 Business Hours** | Upon completion |

> [!NOTE]
> **Business Hours Definition:** Standard Business Hours are defined as **8:00 AM to 5:00 PM Central Time (CT)**, Monday through Friday, excluding federally recognized bank holidays and Texas state holidays. Severity 1 events receive automated 24/7/365 SOC isolation coverage regardless of the hour.

---

### 3. Service Scope & Monthly Inclusions

Under the Tier 3 Monthly Stewardship Retainer, Contractor provides the following continuous technical deliverables:

* **Endpoint Detection & Response (EDR):** Licensing, deployment, telemetry ingestion, and continuous agent health monitoring for up to twenty-five (25) endpoints via Huntress Managed EDR.
* **Managed Antivirus (Defender Orchestration):** Centralized policy orchestration, definition update enforcement, and threat telemetry monitoring for Windows Defender.
* **Microsoft 365 Identity & Cloud Defense:** Continuous Huntress MDR monitoring for Entra ID (impossible travel detection, suspicious inbox forwarding rules, token theft alerts).
* **Continuous Configuration Drift Auditing:** Monthly automated baseline verification using CIPP.app to detect unauthorized permission grants, disabled MFA, or policy degradation.
* **Vulnerability & Patch Governance:** Monthly review of Windows OS patch compliance and software vulnerability telemetry across covered endpoints.
* **Employee Security Awareness & Phishing Simulation:** Automated bi-monthly phishing simulations and training compliance tracking for covered user accounts.
* **Quarterly Executive Cyber Briefing:** 30-minute quarterly virtual risk review with Client executive leadership, delivering an updated NIST CSF 2.0 posture scorecard.

---

### 4. Explicit Exclusions & Demarcation of Boundaries

To prevent misunderstanding and operational friction, the following activities are expressly **EXCLUDED** from this Managed Security SLA:

* **General IT Helpdesk & Desktop Support:** Printer configuration, monitor cabling, localized software bugs (e.g., Excel macro errors), Wi-Fi speed troubleshooting, and physical hardware repair are the exclusive responsibility of Client or its general IT provider.
* **On-Site Physical Server & Hardware Repair:** Contractor provides cloud-centric and remote endpoint security oversight; physical server swapping or rack-and-stack labor is excluded.
* **Disaster Recovery Data Restoration Labor:** While Contractor monitors backup status and verifies policy compliance, full-environment bare-metal server data restoration labor following physical disaster is billable under separate project rates.
* **Certified Digital Forensics & Court Testimony:** Formal litigation support, chain-of-custody evidentiary processing, and expert witness testimony are not included and require dedicated breach counsel engagement.

---

### 5. Client Obligations & System Access

5.1 **Designated Point of Contact:** Client shall maintain an updated list of primary and secondary operational points of contact, including after-hours mobile phone numbers for emergency escalation.

5.2 **Agent Connectivity:** Client must ensure that covered workstations connect to the Internet at least once every fourteen (14) days to maintain telemetry synchronization and policy enforcement.

5.3 **Cooperation During Containment:** Client acknowledges that when Huntress SOC initiates automated host isolation to contain active malware, the affected endpoint will be disconnected from the local network and internet (except for secure communication with the Huntress management server). Client agrees not to manually circumvent or tamper with host isolation without explicit instructions from Contractor.

---

### 6. Billing, Terms & Cancellation

6.1 **Automated Monthly Billing:** Monthly retainer fees are billed on the first (1st) business day of each month via pre-authorized ACH direct debit.

6.2 **Term & 30-Day Cancellation:** The monthly stewardship retainer operates on a month-to-month basis following the initial ninety (90) day baseline stabilization period. Either party may cancel the retainer for convenience by providing thirty (30) days advance written notice.

6.3 **Offboarding Protocol:** Upon notice of termination, Contractor shall provide Client with an orderly 30-day offboarding schedule, transfer telemetry agent uninstallers, revoke delegated administrative access, and deliver a final offboarding summary.

---

### 7. Signatures & Acceptance

IN WITNESS WHEREOF, the parties accept and agree to the service levels, response commitments, and boundaries outlined in this Managed Security Service Level Agreement.

**FOR CLIENT:**  
`[Client Legal Entity Name]`  
Signature: `________________________________________________`  
Printed Name: `________________________________________`  
Title: `_______________________________________________`  
Date: `________________________`  

**FOR SERVICE PROVIDER:**  
Morrison Cyber Defense LLC  
Signature: `________________________________________________`  
Printed Name: Senior Partner  
Title: Principal Cybersecurity Architect  
Date: `________________________`
