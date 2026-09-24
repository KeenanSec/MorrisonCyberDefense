# Data Processing & Business Associate Agreement (DPA / BAA)
## Morrison Cyber Defense LLC

**Document Reference:** `MCD-DPA-BAA-[Year]`  
**Attached to & Incorporating:** Master Services Agreement ("MSA") between Morrison Cyber Defense LLC ("Processor" / "Business Associate") and `[Client Legal Entity Name]` ("Controller" / "Covered Entity")  
**Effective Date:** `[Effective Date]`  
**Applicable Legal Frameworks:**  
* Texas Data Privacy and Security Act (TDPSA - Tex. Bus. & Com. Code § 541)  
* Texas Identity Theft Enforcement and Protection Act (Tex. Bus. & Com. Code § 521)  
* Health Insurance Portability and Accountability Act of 1996 (HIPAA) & HITECH Act (45 C.F.R. Parts 160 and 164)  

---

### 1. Purpose & Scope of Data Processing

1.1 **Context:** In performing cybersecurity assessments, Microsoft 365 configuration hardening, and continuous threat monitoring under the Master Services Agreement ("MSA") and applicable Statements of Work ("SOW"), Contractor may temporarily access, process, or view data that contains:
* **Personally Identifiable Information (PII):** Employee names, corporate email addresses, phone numbers, and authentication logs; and/or
* **Protected Health Information (PHI) / ePHI:** Patient medical records, billing records, or health plan identifiers (if Client operates as a Covered Entity or Hybrid Entity under HIPAA).

1.2 **Role Delineation:**
* Under Texas Data Privacy law (TDPSA), Client is the **Data Controller** and Contractor is the **Data Processor**.
* Under HIPAA/HITECH regulations, Client is the **Covered Entity** (or Business Associate) and Contractor acts as a **Business Associate** (or Subcontractor Business Associate).

---

### 2. Permitted Uses & Disclosures of Data

2.1 **Strict Service Limitation:** Contractor shall process Client Personal Data and PHI solely for the following explicit purposes:
* Executing diagnostic technical audits and verifying security baseline compliance (CISA ScubaGear, CIS Benchmarks).
* Configuring security guardrails (Conditional Access, MFA, DLP rules, SPF/DKIM/DMARC).
* Ingesting endpoint and cloud identity threat telemetry into Huntress MDR for threat detection and host isolation.
* Generating executive risk reports and cyber insurance underwriting attestations.

2.2 **Prohibition on Data Monetization:** Contractor shall never sell, rent, monetize, train machine learning models on, or disclose Client Personal Data or PHI to any unauthorized third party.

---

### 3. Technical & Organizational Safeguards (TOMs)

Contractor implements and maintains rigorous physical, technical, and administrative safeguards designed to protect Client data against unauthorized access, loss, or alteration:

| Security Domain | Operational Control Enforced by Contractor |
| :--- | :--- |
| **Authentication & Access** | Phishing-resistant FIDO2 hardware keys (YubiKeys) mandated on all administrative consoles. Zero shared credentials. |
| **Data in Transit** | Minimum TLS 1.3 enforced for all web, API, and cloud telemetry transmission. |
| **Data at Rest** | AES-256 full disk encryption (BitLocker) enabled on all founder administrative laptops and cloud repositories. |
| **Multi-Tenant Isolation** | Client documentation and secrets stored in dedicated, cryptographically isolated vaults (Hudu / Bitwarden Teams). |
| **Endpoint Hardening** | 24/7 Huntress Managed EDR, real-time Defender antivirus, and automated daily patch management on admin devices. |
| **Out-of-Band Comms** | Encrypted channels (Signal, Proton Mail) isolated from standard tenant infrastructure during security incidents. |

---

### 4. Approved Technical Subprocessors

4.1 **Authorized Subprocessors:** Client grants general written authorization for Contractor to utilize the following pre-vetted infrastructure and security subprocessors to deliver the Services:

| Subprocessor Name | Role in Service Delivery | Data Processed / Stored | Security & Compliance Certification |
| :--- | :--- | :--- | :--- |
| **Microsoft Corporation** | Cloud Tenant & Identity Platform (Entra ID, Intune, M365) | User directories, sign-in logs, email headers | SOC 1/2/3, ISO 27001, HIPAA BAA |
| **Huntress Labs Inc.** | 24/7 Managed EDR, Managed Defender, M365 MDR | Process hashes, endpoint metadata, M365 sign-in telemetry | SOC 2 Type II, HIPAA Compliant |
| **Sherweb Inc.** | Microsoft Cloud Solutions Provider (CSP) Distributor | Tenant licensing and provisioning records | SOC 2 Type II, ISO 27001 |
| **Cloudflare Inc.** | Authoritative DNS, DNSSEC, and Edge Defense | DNS queries, public web traffic routing | SOC 2 Type II, PCI-DSS Level 1 |

4.2 **Subprocessor Due Diligence:** Contractor covenants that each subprocessor is bound by written contractual terms requiring data privacy and security protections no less stringent than those set forth in this Agreement.

---

### 5. Security Incident & Breach Notification SLA

5.1 **Notification Timeline:** Contractor shall notify Client in writing without unreasonable delay, and in no event later than **twenty-four (24) hours**, after becoming aware of and confirming any Security Incident or Breach of Unsecured PHI affecting Client’s data within Contractor’s direct custody.

5.2 **Notification Contents:** To the extent reasonably available at the time of notification, Contractor’s report shall include:
* The identification of each individual whose information was impacted;
* A brief description of what occurred, including the date of the incident and date of discovery;
* The types of data or PHI involved; and
* The immediate mitigation, isolation, and remediation steps taken by Contractor.

5.3 **Regulatory Reporting Coordination:** Client maintains sole legal authority and responsibility for reporting breaches to affected individuals, the Texas Attorney General (pursuant to Tex. Bus. & Com. Code § 521.053 for breaches affecting 250+ Texas residents), and the U.S. Department of Health and Human Services (HHS OCR). Contractor shall provide reasonable technical assistance to support Client’s regulatory filings.

---

### 6. HIPAA Business Associate Agreement (BAA) Specific Covenants

To the extent Contractor processes Protected Health Information (PHI) on behalf of Client:
* **Minimum Necessary Standard:** Contractor shall request, use, and disclose only the minimum necessary PHI required to accomplish the cybersecurity purpose.
* **Individual Rights:** Contractor shall assist Client in responding to individual requests for inspection, amendment, or accounting of disclosures of PHI in Contractor’s possession within ten (10) business days of written notice.
* **Audit of Books and Records:** Contractor shall make its internal practices, books, and records relating to the use and disclosure of PHI available to the Secretary of Health and Human Services upon lawful request for purposes of determining compliance with HIPAA.

---

### 7. Data Retention & Cryptographic Disposal

7.1 **Retention Limitation:** Contractor shall retain Client Personal Data and telemetry only for as long as necessary to fulfill the services specified in the applicable SOW, or as required by applicable Texas statute of limitations.

7.2 **Return or Destruction:** Upon termination of the Master Services Agreement, Contractor shall, at Client’s election:
* Securely transfer all Client data and audit evidence to Client in an industry-standard encrypted format; and/or
* Cryptographically wipe and securely destroy all Client data residing on Contractor’s local systems and cloud storage in accordance with NIST SP 800-88 Rev. 1 (Guidelines for Media Sanitization).

---

### 8. Governing Law & Execution

This Data Processing & Business Associate Agreement shall be governed by and construed in accordance with the laws of the State of Texas and applicable federal privacy statutes.

**FOR CLIENT (Controller / Covered Entity):**  
`[Client Legal Entity Name]`  
Signature: `________________________________________________`  
Printed Name: `________________________________________`  
Title: `_______________________________________________`  
Date: `________________________`  

**FOR SERVICE PROVIDER (Processor / Business Associate):**  
Morrison Cyber Defense LLC  
Signature: `________________________________________________`  
Printed Name: Senior Partner  
Title: Principal Cybersecurity Architect  
Date: `________________________`
