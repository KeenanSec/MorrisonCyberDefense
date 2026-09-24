# Incident Response Scope Limitation Addendum & Emergency Triage Authorization
## Morrison Cyber Defense LLC

**Addendum Reference:** `MCD-ADDENDUM-IR-[ClientCode]`  
**Attached to & Incorporating:** Master Services Agreement ("MSA") and Statement of Work ("SOW") between Morrison Cyber Defense LLC ("MCD") and `[Client Legal Entity Name]` ("Client")  
**Emergency Hotline / Primary Escalation:** Senior Partner (Principal Architect) | Keenan Morrison (Lead Technical Systems Auditor)  
**Emergency Rate:** `$250.00 / hour` (4-Hour Minimum Advance Retainer)  

---

### 1. Purpose & Critical Legal Demarcation

This Addendum establishes clear legal boundaries between **preventative diagnostic/hardening services** and **active crisis incident response**, protecting both Client and Contractor from unrealistic operational expectations and potential liability pitfalls during a cybersecurity emergency.

> [!CAUTION]
> **Essential Scope Distinction:**  
> Morrison Cyber Defense LLC is a specialized **cybersecurity risk reduction, hardening, and managed security advisory firm**. MCD is **NOT** a certified Digital Forensics and Incident Response (DFIR) investigation firm, nor a provider of legal counsel. Routine advisory engagements, baseline audits, and monthly retainers do **NOT** include litigation-grade forensic data acquisition, law enforcement chain-of-custody preservation, or full breach remediation.

---

### 2. Protocol Upon Discovery of Pre-Existing or Active Compromise

In accordance with Section 4.4 of the Master Services Agreement, if Contractor discovers evidence of an active compromise, persistent threat actor, unauthorized access token, or active data exfiltration during any diagnostic audit, hardening sprint, or routine maintenance:

```
┌────────────────────────────────────────────────────────────────────────┐
│ STEP 1: IMMEDIATE ISOLATION & TESTING HALT                              │
│ • Contractor immediately pauses scheduled diagnostic or audit testing  │
│ • Prevents accidental destruction of forensic volatile memory/evidence  │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STEP 2: 60-MINUTE EXECUTIVE NOTIFICATION                                │
│ • Direct emergency phone call to Client Primary Contact within 60 mins │
│ • Transmission of encrypted preliminary findings summary               │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STEP 3: CYBER INSURANCE & LEGAL BREACH COUNSEL ENGAGEMENT              │
│ • Client immediately contacts Cyber Insurance Claims Carrier           │
│ • Engagement of specialized privacy attorney (Breach Coach) to        │
│   establish attorney-client privilege over forensic investigations     │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STEP 4: EMERGENCY TRIAGE SCOPE AUTHORIZATION (OPTIONAL)                 │
│ • Execution of Section 4 below at $250.00/hour for emergency support   │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 3. Demarcation: Huntress 24/7 SOC vs. Morrison Cyber Defense

For clients subscribed to Tier 3 Monthly Stewardship, the division of incident response responsibility is strictly defined as follows:

| Role / Action | Huntress 24/7 Managed SOC | Morrison Cyber Defense LLC | Client & Breach Counsel |
| :--- | :--- | :--- | :--- |
| **Nocturnal Threat Detection** | Primary 24/7/365 Monitor | Secondary Reviewer (Daytime) | Internal Awareness |
| **Active Malicious Host Isolation** | Direct automated / analyst isolation | Validates isolation state | Provides local host context |
| **Malware Process Termination** | Direct remediation action | Reviews alert & impact | Approves reboot / restore |
| **Compromised M365 Account Lock** | Alerts / suggests revocation | Revokes tokens & resets pass | Approves credential resets |
| **Business Strategy & Coordination** | Telemetry provider | Advisory Lead & Liaison | Final Decision Maker |
| **Forensic Evidence Chain-of-Custody** | Excluded | Excluded | Dedicated DFIR Firm |
| **Breach Notification & Legal Notice** | Excluded | Excluded | Client Legal Counsel |

---

### 4. Emergency Incident Triage Authorization (Work Authorization)

Should Client request technical assistance from MCD during an active incident or post-compromise crisis, Client authorizes MCD to perform emergency triage services subject to the following terms:

4.1 **Authorized Emergency Scope:**
* Assisting internal IT or external forensic vendors with administrative access to Microsoft 365 logs (Unified Audit Log, Sign-in Logs).
* Executing immediate mass password resets, session token revocations, and Conditional Access lockdown policies.
* Isolating suspect endpoints via Huntress EDR console.
* Serving as technical liaison between Client management, cyber insurance adjusters, and outside forensic investigators.

4.2 **Emergency Billing Terms:**
* All emergency incident triage services are billed at Contractor’s prevailing emergency rate of **$250.00 per hour**, billed in fifteen (15) minute increments.
* **Emergency Retainer:** Prior to the commencement of emergency response work, Client shall remit an immediate emergency deposit of **$1,000.00** (representing four (4) hours of work) via credit card or wire transfer.
* Unused portions of the emergency deposit shall be refunded upon formal incident closeout.

4.3 **Forensic Limitation & Evidence Disclaimer:** Contractor will take reasonable precautions to preserve system logs. However, Contractor makes no warranty that actions taken to stop an active intrusion will preserve evidentiary forensic admissibility in a court of law. Client assumes all risk of evidence spoliation resulting from emergency containment actions requested by Client.

---

### 5. Cyber Insurance Carrier Notification Mandate

Client acknowledges that commercial cyber liability insurance policies typically require **immediate notice** to the insurance carrier prior to hiring forensic investigators or incurring incident response costs. Failure to timely notify the carrier may result in forfeiture of policy coverage. Client agrees that it is Client’s sole responsibility to initiate notice to its insurer.

---

### 6. Signatures & Standing Authorization

The undersigned authorized executive accepts this Incident Response Scope Limitation Addendum and agrees to the emergency triage rates and protocols specified herein.

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
