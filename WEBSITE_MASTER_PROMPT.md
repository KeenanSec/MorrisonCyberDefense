# MISSION: BUILD THE OFFICIAL B2B WEBSITE FOR MORRISON CYBER DEFENSE LLC

You are an expert full-stack developer and B2B conversion designer. Your job is to analyze the top Y Combinator B2B security and infrastructure websites (e.g., Stripe, Cloudflare, Vanta, Huntress, GitLab, Algolia) and use their architectural patterns, typography, and trust mechanics to build a production-grade, authoritative website for **Morrison Cyber Defense LLC**.

---

## 1. DESIGN MANDATE: HIGH-TRUST, ANTI-SLOP, ANTI-WORDPRESS

### What to NEVER Do:
* **No "Vibe-Coded" Slop:** No chaotic neon purple gradients, no meaningless floating 3D glass spheres, no hand-waving "AI-powered next-gen synergy" buzzword soup, and no non-functional fake widgets. Enterprise buyers and insurance underwriters bounce immediately from sites that look like high school crypto projects.
* **No "Shitty WordPress" Bloat:** No clunky page-builder DOM nesting (Elementor/Divi), no 15MB asset loads, no cheesy stock photos of padlocks or hackers in black hoodies, and no generic marketing agency filler.

### What Elite YC B2B Sites Actually Do (The Benchmark):
* **Crisp Visual Hierarchy:** Dark slate/navy foundations (`#070A11`, `#0B1120`, `#111A2E`) with subtle 1px border lines (`#1E293B`, `#334155`). High-contrast, WCAG AAA text legibility (`#F8FAFC`, `#94A3B8`).
* **Authoritative Typography:** Humanist sans-serif (`Plus Jakarta Sans` or `Inter`) paired with a monospace font (`JetBrains Mono`) for technical parameters, terminal badges, and checklist task codes.
* **Radical Transparency:** Clear, upfront pricing, exact sprint timelines (10 business days), concrete frameworks (NIST CSF 2.0, Microsoft Secure Score, Entra ID, DMARC `p=reject`), and zero hidden fees.
* **High-Craft Performance:** Pure semantic HTML5, modern modular CSS (custom properties), and dependency-free Vanilla ES6 JS that loads in under 300ms.

---

## 2. CLIENT CONTEXT & ASSET INGESTION

Extract and incorporate the verified operational data from the firm's business plan and repository:

1. **Entity & Identity:**
   * **Company Name:** Morrison Cyber Defense LLC (Texas Member-Managed LLC)
   * **Headquarters:** Greater Houston Metropolitan Area, Texas
   * **Domain & Contact:** `https://morrisoncyber.org` | `security@morrisoncyber.org`
   * **Logo:** Embed the official brand emblem (`assets/MorrisonCyberDefenseLogo.jpg` or `assets/logo.jpg`) in the navigation bar, hero card, and footer.

2. **Beachhead Target Market:**
   * Greater Houston commercial construction contractors (AGC), maritime & logistics operators along Port Houston / Houston Ship Channel, and industrial energy service firms (10–100 seats).
   * Primary business trigger: Imminent cyber insurance policy renewals (Travelers, Chubb, Coalition) demanding proof of strict MFA, DMARC, and immutable cloud backups, combined with surging wire fraud / Business Email Compromise (BEC) risks targeting contractor progress draws.

3. **Leadership Credentials (Purdue Family Business Model):**
   * **Senior Partner (Father / Co-Founder):** Principal Cybersecurity Architect. 20+ years in enterprise architecture, Microsoft Entra ID engineering, industrial operational resilience (ICS/OT), and executive board risk reviews.
   * **Keenan Morrison (Son / Co-Founder):** Lead Technical Systems Auditor. B.S. Cybersecurity student at Western Governors University (WGU); CompTIA Security+, Network+, and A+ certified; SkillsUSA Cybersecurity State Finalist. Leads hands-on tenant discovery, CIPP automated baseline audits, and remediation validation.

4. **Productized Service Tiers & Pricing:**
   * **Step 1: Diagnostic M365 Baseline Review ($2,500 Fixed / 10-Day Turnaround):** 100% read-only diagnostic review of Microsoft 365 cloud identity, MFA enforcement, email transport, and underwriter compliance.
   * **The Conversion Bridge (100% Roll-In Credit Guarantee):** 100% of the $2,500 diagnostic fee is credited directly toward follow-on remediation or monthly retainers, eliminating sales friction.
   * **Step 2: M365 Defense Sprint ($3,800–$5,500 Starting):** Active 10-day hands-on remediation hardening Entra ID, Intune, Defender for Business, and strict DMARC (`p=reject`).
   * **Step 3: Monthly Stewardship ($1,750/mo for 10–25 seats):** Continuous multi-tenant governance backed by **Huntress 24/7 human MDR SOC threat isolation**, CIPP drift management, and quarterly executive underwriter attestations.

5. **Operational Guardrails & Legal Standards:**
   * **100% Read-Only Diagnostics:** Zero modifications to live client environments during audits.
   * **48-Hour Report-Only Testing:** All Entra Conditional Access policies must sit in Report-Only mode for 48 hours to prevent legitimate workflow lockouts.
   * **Legal Compliance:** Strict adherence to the Computer Fraud and Abuse Act (CFAA) and Texas Penal Code § 33.02.
   * **Dual Sign-Off:** Execution by Lead Auditor with final architectural sign-off by Senior Partner.

---

## 3. REQUIRED SITE SECTIONS & INTERACTIVE UTILITIES

1. **Sticky Header:**
   * Brand emblem, company name, location tag (`HOUSTON, TX • CLOUD DEFENSE & ADVISORY`).
   * Navigation links: Services, Sprint Checklist, Value Matrix, Pricing, ROI Calculator, Insurance Quiz, Guardrails, Leadership, and "Book Assessment" CTA button.

2. **Hero Section:**
   * Direct headline: *Enterprise-Grade Microsoft 365 Cloud Defense & Cyber Insurance Readiness.*
   * Subtitle articulating the Houston commercial contractor focus, ransomware/wire fraud mitigation, and Huntress 24/7 MDR threat isolation.
   * Prominent brand profile card displaying the logo, Texas LLC credentials, and key operating metrics (10-day turnaround, 100% roll-in credit, 24/7 human isolation).
   * Trust badge bar: Huntress Partner SOC, CompTIA Security+/Network+/A+, WGU Cybersecurity, 10-Day SLA.

3. **Market Reality Section ("The Three Threats"):**
   * *The Insurance Renewal Crunch:* Carriers rejecting policies over missing MFA, unconfigured DMARC, or lack of EDR.
   * *Wire Fraud & Invoice Diversion:* How compromised mailboxes lead to six-figure intercepted contractor draws.
   * *The General MSP Gap:* Why standard IT helpdesks fail at deep Microsoft Entra identity architecture.

4. **Productized Pricing & Offer Structure:**
   * Three distinct cards for Step 1 ($2,500 Diagnostic), Step 2 ($3,800+ Sprint), and Step 3 ($1,750/mo Stewardship).
   * Prominent visual treatment of the **100% Fee Roll-In Credit Bridge**.

5. **Interactive 5-Phase M365 Hardening Sprint Checklist Explorer:**
   A tabbed technical component allowing prospects to inspect the actual implementation protocol:
   * **Phase 1: Identity & Entra ID:** GA reduction to 2–4, break-glass FIDO2 emergency accounts, number-matching MFA via Conditional Access, legacy auth protocol blocks, geographic sign-in restrictions, SSPR.
   * **Phase 2: Email & Domain Defense:** SPF hard-fail (`-all`), dual 2048-bit DKIM keys, strict DMARC (`p=reject`), external sender warning banners, external auto-forwarding killswitch, executive anti-impersonation rules.
   * **Phase 3: Endpoints & Intune:** Intune compliance baselines, BitLocker encryption, Defender for Business EDR onboarding, Defender Tamper Protection.
   * **Phase 4: Audit Logs & Purview:** 180-day Unified Audit Log retention, suspicious forwarding alert rules, break-glass webhook alarms.
   * **Phase 5: Before vs. After Scorecard:** Visualizing the baseline vs. hardened state (Microsoft Secure Score 28% -> 76%+, 0 unmanaged MFA accounts, DMARC enforced).
   * *Functionality:* Live interactive checkboxes that recalculate an on-page "Sprint Implementation Progress" meter.

6. **Value Comparison Matrix:**
   A clean comparison table comparing **Morrison Cyber Defense** vs. **General IT MSPs** vs. **Big 4 / National Cyber Firms** across Core Focus, Pricing Transparency, 24/7 Human Isolation, Turnaround Time, Senior Architect Access, and Local Houston Response.

7. **Interactive Cyber Exposure & Insurance ROI Calculator:**
   A dynamic seat slider (10 to 150 seats) computing estimated BEC risk exposure mitigated, annual insurance premium savings, turnaround time (10 days), and net diagnostic cost ($0 with roll-in credit).

8. **Interactive 60-Second Cyber Insurance Readiness Check:**
   A 5-question multi-step readiness evaluator assessing MFA enforcement, DMARC spoofing defense, 24/7 EDR/MDR, Global Admin hygiene, and cloud backups, generating an instant percentage score and tailored underwriter guidance.

9. **Operational Guardrails & Leadership Bios:**
   Clear cards for the 4 operational guardrails and detailed bios highlighting the Senior Partner's 20+ years enterprise architecture and Keenan Morrison's CompTIA and WGU credentials.

10. **Direct Scoping Intake Form & Institutional Footer:**
    A validated intake form (Name, Company, Business Email, Seat Count, Urgency) with a 4-hour SLA notice, complete with copyright, Texas LLC registration, and statutory legal notices.

---

## 4. OUTPUT REQUIREMENTS

Generate clean, valid, production-ready code with complete separation of concerns:
* `index.html`: Fully semantic HTML5 with complete text content (no `Lorem Ipsum`), accessible ARIA attributes, and SVG icons.
* `styles.css`: CSS3 custom properties design system, responsive grid/flexbox layouts, clean component styling, and zero external framework dependencies.
* `app.js`: Vanilla ES6 JavaScript handling navigation, checklist tabs and progress updates, ROI slider math, quiz logic, and form feedback.
