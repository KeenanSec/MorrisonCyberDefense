# Morrison Cyber Defense LLC
## Security Assessment Authorization & Rules of Engagement (RoE)

**Client Organization:** `[Client Company Legal Name]`  
**Client Primary Contact:** `[Name, Title, Email, Direct Phone]`  
**Practice:** Morrison Cyber Defense LLC (Houston, TX)  
**Engagement Lead / Principal Architect:** Senior Partner, Morrison Cyber Defense LLC  
**Associate Technical Analyst:** Keenan Morrison  
**Effective Dates:** `[Start Date]` through `[End Date]`  

---

### 1. Scope of Authorization & Authority to Test

The undersigned executive of **`[Client Company Legal Name]`** ("Client") hereby grants explicit written authorization to **Morrison Cyber Defense LLC** ("MCD") to perform authorized security baseline assessments, external posture scans, and Microsoft 365 configuration audits in accordance with the terms below.

Client certifies that it owns or has full lawful authorization from the equipment/service owners to permit MCD to assess the target systems, domains, IP addresses, and cloud tenants listed in Section 2.

> [!IMPORTANT]
> **Legal Protection & Compliance with Computer Fraud and Abuse Act (18 U.S.C. § 1030) and Texas Penal Code § 33.02:**  
> MCD personnel will only access systems within the authorized scope during the approved testing window. Testing activities are non-destructive and strictly diagnostic.

---

### 2. In-Scope Targets

| Target Type | In-Scope Identifier / Range | Description |
| :--- | :--- | :--- |
| **Public FQDNs / Domains** | `[e.g., examplecompany.com, portal.examplecompany.com]` | External web & DNS surface |
| **External IPv4 Addresses** | `[e.g., 203.0.113.10 – 203.0.113.14]` | Perimeter firewall / VPN gateway |
| **Cloud Tenant (M365)** | `[e.g., examplecompany.onmicrosoft.com]` | Entra ID, Exchange, Defender, Intune |
| **Internal Sample Hosts** | Up to `[10-25]` representative workstations / servers | Local configuration & EDR verification |

#### Explicit Out-of-Scope Systems (Do NOT Touch)
* Production ICS/SCADA/OT networks, PLCs, RTUs, and HMIs (unless governed by separate OT Appendix).
* Third-party SaaS providers not under direct administrative control of Client.
* Disruption of voice/VoIP, physical life safety, or emergency dispatch systems.

---

### 3. Permitted Techniques vs. Prohibited Actions

#### Permitted Diagnostic Techniques:
* Port identification, service banner inspection, and protocol analysis.
* Read-only Microsoft 365 tenant audits using least-privilege Global Reader / Security Reader roles.
* Authenticated endpoint configuration checks (CIS Benchmarks, patch levels, BitLocker, EDR presence).
* Passive DNS, certificate transparency, and credential exposure search on public databases.
* Synthetic phishing simulation (only if explicitly opted into in SOW).

#### Prohibited Actions (Zero Tolerance):
* **No Denial of Service (DoS/DDoS):** No stress testing or bandwidth exhaustion.
* **No Exploitation or Data Exfiltration:** Proof-of-vulnerability stops at identification; no production exploitation.
* **No Unauthorized Account Creation:** No persistent administrative backdoors or persistence hooks.
* **No Ransomware / Destruction:** No destructive payload delivery or file alteration.

---

### 4. Schedule & Testing Window

* **Assessment Hours:** Standard Business Hours (`8:00 AM – 5:00 PM CT`) or After Hours (`6:00 PM – 11:00 PM CT`), as designated: `[Select Window]`.
* **Points of Contact for Operational Deconfliction:**
  * **Client Emergency Contact:** `[Name, Mobile 24/7]`
  * **MCD Principal Architect:** `[Principal Phone 24/7]`
  * **MCD Technical Lead:** Keenan Morrison `[Phone]`

---

### 5. Critical Finding Escalation Protocol

If MCD identifies an active ongoing compromise, critical zero-day vulnerability, or exposed administrative credentials during the audit:
1. **Immediate Halt:** MCD will freeze testing on that specific asset immediately.
2. **Direct Phone Notification:** MCD will call the Client Primary Contact within **60 minutes**.
3. **Written Briefing:** MCD will provide an encrypted summary of the critical exposure within **4 hours**.

---

### 6. Signatures & Execution

By signing below, the parties agree to all terms, targets, and restrictions established in this Rules of Engagement document.

**For Client Organization:**  
Name: `____________________________________`  
Title: `____________________________________`  
Signature: `_________________________________` Date: `___________`

**For Morrison Cyber Defense LLC:**  
Name: Senior Partner, Principal Cybersecurity Architect  
Signature: `_________________________________` Date: `___________`
