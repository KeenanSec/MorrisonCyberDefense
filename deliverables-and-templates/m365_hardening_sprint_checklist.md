# Morrison Cyber Defense LLC
## Microsoft 365 Security Hardening Sprint: Implementation Checklist & Sign-Off

**Client Organization:** `[Client Business Name]`  
**M365 Tenant ID:** `[Tenant GUID / Domain]`  
**Sprint Lead:** Principal Cybersecurity Architect (Senior Partner)  
**Execution Analyst:** Keenan Morrison (Associate Cybersecurity Analyst)  
**Target Completion:** `[Target Date - 10 Business Days]`  

---

## 1. Executive Sprint Overview

The **Microsoft 365 Security Hardening Sprint** is an intensive, 10-day hands-on remediation service designed to eliminate 90%+ of common cyber threat vectors across cloud identity, email, and endpoint environments.

### Target Benchmark:
* **Baseline Microsoft Secure Score:** `[e.g., 28.4%]`
* **Post-Hardening Target Secure Score:** `[Target: 70%+ / 75%+]`
* **Zero Disruption Protocol:** All Conditional Access policies tested in **Report-Only** mode for 48 hours prior to live enforcement.

---

## 2. Phase-by-Phase Technical Checklist

### Phase 1: Identity & Access Management (Entra ID)
| Item | Task Description | Lead Role | Status |
| :--- | :--- | :--- | :--- |
| **1.1** | **Global Admin Audit:** Reduce Global Administrator accounts to 2–4 maximum. Strip GA rights from regular day-to-day user accounts. | Principal | `[ ] Completed` |
| **1.2** | **Emergency "Break-Glass" Accounts:** Create two cloud-only emergency accounts with 32+ character random passwords, FIDO2 hardware keys, and exclusion from CA policies. Stored in physical safe. | Principal | `[ ] Completed` |
| **1.3** | **Enforce Phishing-Resistant MFA:** Deploy Conditional Access requiring Microsoft Authenticator with number matching across all active users. | Keenan | `[ ] Completed` |
| **1.4** | **Block Legacy Basic Authentication:** Create Conditional Access policy blocking legacy mail protocols (POP3, IMAP, Authenticated SMTP). | Keenan | `[ ] Completed` |
| **1.5** | **Geographic / Risky Sign-In Blocks:** Block sign-in attempts from unauthorized foreign jurisdictions (outside US/Canada or designated operational countries). | Keenan | `[ ] Completed` |
| **1.6** | **Self-Service Password Reset (SSPR):** Configure SSPR with combined registration for security info. | Keenan | `[ ] Completed` |

### Phase 2: Exchange Online & Email Defense
| Item | Task Description | Lead Role | Status |
| :--- | :--- | :--- | :--- |
| **2.1** | **SPF Record Verification:** Validate DNS TXT record for SPF; ensure `-all` (hard-fail) enforcement. | Keenan | `[ ] Completed` |
| **2.2** | **DKIM Key Generation & Enablement:** Generate dual 2048-bit DKIM keys in Exchange admin and verify DNS CNAME publication. | Keenan | `[ ] Completed` |
| **2.3** | **DMARC Deployment:** Implement DMARC policy (starting at `p=quarantine; pct=100` or `p=reject`) with daily aggregate reporting. | Principal | `[ ] Completed` |
| **2.4** | **External Email Warning Banners:** Configure mail flow transport rule applying standard warning banner to all incoming external messages. | Keenan | `[ ] Completed` |
| **2.5** | **Disable External Auto-Forwarding:** Enforce remote domain restrictions blocking automatic external email forwarding (anti-exfiltration). | Keenan | `[ ] Completed` |
| **2.6** | **Anti-Phishing & Impersonation Protection:** Configure Defender for Office 365 anti-phishing policies with targeted user impersonation protection for executives and finance personnel. | Principal | `[ ] Completed` |

### Phase 3: Endpoint Hardening & Intune Compliance
| Item | Task Description | Lead Role | Status |
| :--- | :--- | :--- | :--- |
| **3.1** | **Intune Compliance Baseline:** Deploy compliance policies requiring BitLocker disk encryption, minimum OS build, and active antivirus. | Keenan | `[ ] Completed` |
| **3.2** | **Attack Surface Reduction (ASR) Rules:** Deploy standard ASR rules in audit/block mode (blocking executable content from email client and Office macros). | Principal | `[ ] Completed` |
| **3.3** | **Defender for Business Onboarding:** Verify EDR onboarding status across 100% of managed Windows/macOS devices. | Keenan | `[ ] Completed` |
| **3.4** | **Tamper Protection:** Enable tenant-wide Defender Tamper Protection preventing local malware or users from disabling security controls. | Keenan | `[ ] Completed` |

### Phase 4: Logging, Alerting & Audit Trails
| Item | Task Description | Lead Role | Status |
| :--- | :--- | :--- | :--- |
| **4.1** | **Unified Audit Logging:** Confirm Purview Unified Audit Log (UAL) is explicitly enabled with 180-day minimum retention. | Keenan | `[ ] Completed` |
| **4.2** | **Suspicious Forwarding & Rule Alerts:** Configure alert policies triggering immediate notification upon creation of inbox forwarding or deletion rules. | Keenan | `[ ] Completed` |
| **4.3** | **Break-Glass Monitoring:** Configure Entra ID alert forwarding or webhook notification whenever an emergency break-glass account logs in. | Principal | `[ ] Completed` |

---

## 3. Post-Hardening Validation & Before/After Scorecard

```
+---------------------------------------------------------------------------------+
| Metric                              | Before Sprint       | After Sprint         |
+-------------------------------------+---------------------+---------------------+
| Microsoft Secure Score              | [   .  %]           | [   .  %]           |
| Accounts without MFA                | [      ]            | 0                   |
| Legacy Basic Auth Protocols Enabled | [      ]            | 0                   |
| SPF / DKIM / DMARC Status           | Missing / Failing   | 100% Validated      |
| Endpoint EDR Onboarding Rate        | [   .  %]           | 100% Managed        |
| External Auto-Forwarding Permitted  | YES (At Risk)       | BLOCKED             |
+---------------------------------------------------------------------------------+
```

---

## 4. Delivery & Operational Hand-Off Sign-Off

All checklist items marked above have been physically executed and audited. Configuration evidence and tenant export logs are archived in the client repository.

**Execution & Evidence Collection:**  
Keenan Morrison, Associate Cybersecurity Analyst  
Signature: `______________________________________` Date: `____________`

**Senior Architectural Review & Final Acceptance:**  
Senior Partner, Principal Cybersecurity Architect  
Morrison Cyber Defense LLC  
Signature: `______________________________________` Date: `____________`
