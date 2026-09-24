# Master Services Agreement (MSA)
## Morrison Cyber Defense LLC

**THIS MASTER SERVICES AGREEMENT** (the "Agreement" or "MSA") is entered into as of `[Effective Date]` (the "Effective Date"), by and between:

**SERVICE PROVIDER:**  
**Morrison Cyber Defense LLC**, a Texas limited liability company with principal offices in Greater Houston, Harris County, Texas ("Contractor", "Provider", or "MCD").  
Email: `security@morrisoncyber.org` | Web: `https://morrisoncyber.org`  

**AND**

**CLIENT:**  
**`[Client Legal Entity Name]`**, a `[State of Incorporation / Formation, e.g., Texas]` `[Entity Type, e.g., Corporation / LLC]` ("Client"), with its principal office located at `[Client Physical Address]`.  
Primary Contact: `[Contact Name, Title, Direct Email, Direct Phone]`.

---

### Recitals

WHEREAS, Contractor provides specialized commercial cybersecurity advisory services, Microsoft 365 cloud hardening, cyber insurance underwriting readiness audits, and managed endpoint detection and response oversight; and

WHEREAS, Client desires to engage Contractor from time to time to perform cybersecurity assessments, configuration hardening sprints, and/or ongoing security stewardship services as set forth in one or more mutually executed Statements of Work ("SOW"), and Contractor agrees to perform such services subject to the terms and conditions of this Agreement;

NOW, THEREFORE, in consideration of the mutual covenants herein contained and other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree as follows:

---

### 1. Scope of Services & Statements of Work

1.1 **Statements of Work:** Contractor shall provide services ("Services") and deliverables ("Deliverables") to Client in accordance with one or more written Statements of Work ("SOW") executed by authorized representatives of both parties. Each SOW shall reference this MSA and describe the specific scope of services, asset limits, deliverable milestones, pricing, and project schedule.

1.2 **Order of Precedence:** In the event of an irreconcilable conflict between the terms of this MSA and any SOW or exhibit, the terms of this MSA shall govern and control, unless the SOW explicitly identifies the specific section of this MSA it intends to supersede.

1.3 **Independent Contractor Status:** Contractor is an independent contractor. Neither party is an agent, employee, partner, or joint venturer of the other. Contractor maintains full control over the manner, means, and personnel used to perform the Services.

---

### 2. Fees, Invoicing & Payment Terms

2.1 **Project Fees & Retainers:**
* **Fixed-Fee Projects (Diagnostic Audits & Hardening Sprints):** Client shall pay fifty percent (50%) of the fixed project fee upon mutual execution of the SOW as a non-refundable commencement deposit, and the remaining fifty percent (50%) upon delivery of the final assessment report or completion of the sprint sign-off milestone.
* **Monthly Stewardship Retainers:** Recurring retainer fees are due and payable in advance on the first (1st) day of each calendar month via automated clearing house (ACH) electronic transfer or pre-authorized credit card. 

2.2 **Strict Zero Net-30 Policy:** Contractor operates on a strict zero Net-30 commercial receivables policy. All project milestones require verified payment prior to release of production deliverables, and all monthly monitoring services require automated ACH clearance. 

2.3 **Late Payments & Suspension:** Any invoice unpaid after five (5) business days past due shall accrue interest at the lesser of one and one-half percent (1.5%) per month or the maximum rate permitted by Texas law. Contractor reserves the right to immediately suspend access to managed monitoring telemetry (Huntress MDR), active project sprints, or client portal access if any invoice remains unpaid after seven (7) days written notice.

2.4 **Taxes:** All fees are exclusive of applicable federal, state, or municipal sales, excise, or value-added taxes, which shall be the sole responsibility of Client (excluding taxes based upon Contractor's net corporate income).

---

### 3. Client Duties & Technical Prerequisites

3.1 **Access & Permissions:** Client shall grant Contractor necessary administrative access (least-privilege Global Reader / Security Reader roles for audits; temporary delegated administrative credentials for configuration sprints) to target cloud tenants, endpoint management portals, and network infrastructure.

3.2 **Authorized Representative:** Client shall designate a primary technical liaison with full authority to grant system access, approve configuration changes, and receive confidential security briefings.

3.3 **Pre-Testing Authorization (RoE):** Prior to initiating any technical diagnostic scanning or tenant inspection, Client must execute Contractor's standard Security Assessment Authorization & Rules of Engagement ("RoE"), confirming Client’s legal authority over all in-scope systems under the Computer Fraud and Abuse Act (18 U.S.C. § 1030) and Texas Penal Code § 33.02.

---

### 4. Non-Negotiable Contractual Shields & Liability Allocations

The parties expressly agree that the following five (5) liability allocation provisions are fundamental elements of the basis of the bargain between Contractor and Client:

#### 4.1 Limitation of Liability & Damages Cap
TO THE MAXIMUM EXTENT PERMITTED UNDER APPLICABLE TEXAS LAW:  
(A) IN NO EVENT SHALL MORRISON CYBER DEFENSE LLC, ITS CO-FOUNDERS, MEMBERS, OR EMPLOYEES BE LIABLE TO CLIENT OR ANY THIRD PARTY FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL, SPECIAL, PUNITIVE, OR EXEMPLARY DAMAGES (INCLUDING LOSS OF PROFITS, LOSS OF DATA, BUSINESS INTERRUPTION, LOSS OF GOODWILL, RANSOM OR EXTORTION PAYMENTS, OR REGULATORY FINES), REGARDLESS OF THE THEORY OF LIABILITY (WHETHER IN CONTRACT, TORT, STRICT LIABILITY, OR OTHERWISE).  

(B) THE TOTAL AGGREGATE LIABILITY OF MORRISON CYBER DEFENSE LLC ARISING OUT OF OR RELATING TO THIS AGREEMENT, THE SERVICES, OR ANY DELIVERABLE SHALL UNDER NO CIRCUMSTANCES EXCEED THE TOTAL FEES ACTUALLY PAID BY CLIENT TO MORRISON CYBER DEFENSE LLC UNDER THE SPECIFIC STATEMENT OF WORK (SOW) GIVING RISE TO THE CLAIM DURING THE THREE (3) MONTHS IMMEDIATELY PRECEDING THE OCCURRENCE OF THE EVENT GIVING RISE TO LIABILITY.

#### 4.2 Third-Party Platform & Software Disclaimer
Client acknowledges that Contractor utilizes, configures, and interacts with third-party software and cloud infrastructure platforms, including Microsoft 365, Microsoft Azure, Microsoft Entra ID, Microsoft Intune, Microsoft Defender, Huntress MDR, CIPP.app, and third-party security telemetry agents. Contractor does not develop, warrant, or insure third-party code.  

CONTRACTOR SHALL HAVE NO LIABILITY ARISING FROM:  
(I) PLATFORM OUTAGES, ZERO-DAY VULNERABILITIES, OR DATA LOSS CAUSED BY MICROSOFT OR OTHER THIRD-PARTY PROVIDERS;  
(II) COMPATIBILITY ISSUES, DRIVER CRASHES, OR CORRUPTIONS CAUSED BY SOFTWARE VENDOR PATCHES OR MICROSOFT UPDATES; OR  
(III) AUTOMATED ACTIONS TAKEN BY THIRD-PARTY THREAT DETECTION SOFTWARE (INCLUDING HOST NETWORK ISOLATION OR USER SESSION TERMINATION BY HUNTRESS MDR).

#### 4.3 No Warranty of System Infiltration Immunity
Client expressly acknowledges that cybersecurity is an ongoing discipline of risk reduction, defense-in-depth, and attack surface minimization, not absolute risk elimination. Contractor does NOT guarantee, warrant, or represent that:  
(A) Client’s systems, networks, endpoints, or cloud tenants will be 100% impenetrable or unhackable;  
(B) All existing or future vulnerabilities, advanced persistent threats (APTs), zero-day exploits, backdoors, or malicious actors will be detected, prevented, or neutralized; or  
(C) Client will never suffer a ransomware encryption event, data breach, business email compromise (BEC), or wire transfer redirection.  

Contractor’s services represent diagnostic and configuration efforts aligned with industry frameworks (NIST CSF 2.0, CIS Baselines, CISA CPGs). Client remains solely responsible for its own business risk decisions, multi-person financial dual-custody verification controls, and employee conduct.

#### 4.4 Discovery of Pre-Existing Compromise
If Contractor discovers evidence of an active, ongoing, or pre-existing security compromise, unauthorized intrusion, lateral movement, or active data exfiltration during any assessment or sprint:  
(A) Contractor’s scheduled diagnostic scope shall immediately pause;  
(B) Contractor shall notify Client’s emergency contact within sixty (60) minutes of verified discovery;  
(C) Standard SOWs do not include certified digital forensic investigations, evidence chain-of-custody handling, or incident response crisis management. Emergency containment assistance shall be provided solely upon mutual execution of an Emergency Incident Triage Addendum at Contractor's prevailing emergency rate ($250.00/hour).

#### 4.5 Client Responsibility for Data & Backups
Client warrants and covenants that, prior to the commencement of any configuration, hardening, policy deployment, or testing activities by Contractor, Client has performed and validated complete, restorable, and disconnected (offline or immutable) backups of all critical business data, databases, mailboxes, and operational systems.  

Contractor shall have zero liability for data loss, corrupted databases, or system restoration costs resulting from pre-existing environment defects, hardware failures, or unexpected third-party software behavior during configuration.

---

### 5. Confidentiality & Proprietary Data

5.1 **Confidential Information:** "Confidential Information" means all non-public information disclosed by one party ("Disclosing Party") to the other party ("Receiving Party"), including but not limited to business plans, financial records, client lists, network architectures, vulnerability findings, IP addresses, credential hashes, and security assessment reports.

5.2 **Protection Standards:** The Receiving Party agrees to protect Confidential Information with the same degree of care it uses for its own confidential materials (and never less than a reasonable standard of care under the Texas Uniform Trade Secrets Act). Confidential Information shall not be disclosed to any third party without prior written consent, except to employees, contractors (e.g., Huntress Labs for telemetry), and legal counsel who need to know such information for the purposes of this Agreement.

5.3 **Contractor Proprietary Property:** Contractor retains all right, title, and interest in and to its pre-existing materials, proprietary assessment scripts, audit templates, automated CIPP deployment recipes, benchmark frameworks, and general methodologies. Upon full payment of all applicable fees, Client is granted a perpetual, non-exclusive, internal license to utilize the specific final written reports and hardening documentation generated for Client.

---

### 6. Term, Termination & Suspension

6.1 **Term:** This Agreement commences on the Effective Date and continues for twelve (12) months. It shall automatically renew for successive one (1) year periods unless either party provides written notice of non-renewal at least thirty (30) days prior to the expiration of the then-current term.

6.2 **Termination for Convenience:** Either party may terminate a month-to-month Recurring Retainer SOW for convenience upon thirty (30) days prior written notice. Fixed-fee diagnostic audits and hardening sprints cannot be canceled for convenience once technical work has commenced.

6.3 **Termination for Cause:** Either party may terminate this Agreement immediately if the other party:
* Materially breaches this Agreement or an SOW and fails to cure such breach within fifteen (15) days after receiving written notice;
* Files for bankruptcy, insolvency, or enters into liquidation; or
* Violates Section 3.3 (Rules of Engagement / CFAA authorization) or Section 5 (Confidentiality).

6.4 **Post-Termination Obligations:** Upon termination, Client shall promptly pay Contractor for all services performed and approved expenses incurred up to the effective date of termination. Contractor shall promptly revoke all administrative credentials and securely return or destroy Client confidential data.

---

### 7. Governing Law, Jurisdiction & Dispute Resolution

7.1 **Texas Governing Law:** This Agreement, and all claims or causes of action arising out of or relating to this Agreement, shall be governed by and construed in accordance with the laws of the State of Texas, without regard to its conflict of laws principles.

7.2 **Mandatory Mediation & Arbitration:** In the event of any controversy, claim, or dispute arising out of or relating to this Agreement:
* The parties shall first submit the matter to good-faith mediation before a certified mediator in Houston, Harris County, Texas.
* If the dispute is not resolved within forty-five (45) days of initiating mediation, it shall be resolved by final and binding arbitration administered by the American Arbitration Association (AAA) under its Commercial Arbitration Rules, held in Houston, Harris County, Texas, before a single arbitrator with at least ten (10) years of commercial technology litigation experience.
* The prevailing party in any arbitration or legal proceeding shall be entitled to recover reasonable attorneys' fees and costs.

7.3 **Waiver of Jury Trial:** TO THE MAXIMUM EXTENT PERMITTED UNDER APPLICABLE LAW, EACH PARTY HEREBY IRREVOCABLY WAIVES ALL RIGHTS TO A TRIAL BY JURY IN ANY ACTION, PROCEEDING, OR COUNTERCLAIM ARISING OUT OF OR RELATING TO THIS AGREEMENT.

---

### 8. General Provisions

8.1 **Severability:** If any provision of this Agreement is held to be invalid or unenforceable, such provision shall be severed and the remaining provisions shall remain in full force and effect.

8.2 **Notices:** All notices must be in writing and delivered via email with delivery confirmation, or certified mail to the addresses listed in the preamble.

8.3 **Counterparts & E-Signatures:** This Agreement may be executed in counterparts, each of which shall be deemed an original. Delivery of an executed signature page by electronic signature (e.g., DocuSign, PandaDoc) or PDF email shall be legally binding and effective.

---

### 9. Execution & Acceptance

IN WITNESS WHEREOF, the parties hereto have caused this Master Services Agreement to be executed by their duly authorized representatives as of the Effective Date.

**FOR CLIENT:**  
**`[Client Legal Entity Name]`**  

By: `________________________________________________`  
Printed Name: `________________________________________`  
Title: `_______________________________________________`  
Date: `________________________`  

**FOR SERVICE PROVIDER:**  
**Morrison Cyber Defense LLC**  

By: `________________________________________________`  
Printed Name: Senior Partner  
Title: Principal Cybersecurity Architect  
Date: `________________________`
