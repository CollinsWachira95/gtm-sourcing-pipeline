# GTM Sourcing & Enrichment Pipeline

A self-initiated data pipeline built to demonstrate GTM engineering skills: sourcing at scale, data cleaning, signal-based scoring, LLM-assisted outreach, and CRM orchestration.

## The Problem
ARC Intelligence sells an AI-native Finance OS to German Mittelstand CFOs. The GTM team needs a repeatable way to identify companies with complex finance/reporting structures (multi-entity, PE-backed), find out why they need help *now* (ERP migrations, acquisitions), and reach them with relevant, personalized messages.

This project builds a miniature version of that machine. 

## The Pipeline
1. **Source:** Collect verified companies from public sources.
2. **Enrich:** Add `pe_backed`, `acquisition`, `erp_hiring`, and `multi_entity` signals based on public evidence.
3. **Clean:** Normalize names, flag ICP-fit issues, and quarantine unverified rows to prevent scoring bad data.
4. **Score:** Rank companies based on a self-defined ICP weighting.
5. **Draft:** Generate AI-assisted outreach for the top-ranked accounts.
6. **Orchestrate:** Push to HubSpot and visualize pipeline health in Looker Studio.

## ICP Definition
**Target:** German Mittelstand companies (50–500 employees) that are multi-entity.
**Signals (in priority order):**
1. **PE-backed** (Fit) — A PE owner pushes consolidated reporting. 
2. **Recent acquisition** (Timing) — Integrating a new entity creates immediate consolidation pain.
3. **Hiring ERP roles** (Timing) — A finance-system migration means data is in flux.
4. **Multi-entity** (Fit) — Structural complexity across subsidiaries.

**Philosophy:** *Fit over timing.* A company with the right structure has the pain ARC solves; timing decides when to call.

## Results & Data Quality
*Note: Full details are in `data_quality_report.md`.*
- **Sourced:** 45 verified companies across 7 source types.
- **Quarantined:** 18 rows (flagged `verify_*`) because they lacked verified ownership or ICP-fit data. They were quarantined, not deleted, to maintain an audit trail.
- **Excluded:** 1 row (a current ARC customer) marked `excluded_customer`.
- **Scored:** 26 fully verified companies.

### The Scoring Finding (Why 22 companies tied)
Weights: PE (+3), Acquisition (+2), ERP Hiring (+2), Multi-entity (+1). Max score: 8.
The scoring revealed a critical data finding: **22 of the 26 verified companies scored exactly 3.** Because PE-backed is weighted heavily and most verified companies lacked secondary timing signals (like verified acquisitions), they clustered into a massive tie. 

**Why this matters:** A forced ranking (1 to 26) would have created a fake "Top 10" that was actually just random noise among the tied companies. We documented the tie honestly rather than faking a ranking.

## LLM Outreach & Hallucination Findings
We generated programmatic prompts for the Top 10 companies and used an LLM to draft personalized first-touch emails.
- **The Finding:** 5 out of 10 drafts contained at least one hallucinated fact (e.g., inventing the wrong PE owner, a fake acquisition target, or an incorrect date).
- **The Fix:** Drafts were **not sent**. They were stored in `data/ranked_outreach_drafts.csv` with a `draft_review` column. This demonstrates why a human-in-the-loop review gate is mandatory before automating outbound.

## HubSpot & Dashboard
* **HubSpot:** All 26 scored companies were imported. A custom `ICP Score` property allows BDRs to filter the top accounts and see the source traceability.
* **Dashboard:** The Looker Studio dashboard visualizes the score distribution, highlighting the 22-company tie at score 3 as an honest reflection of the data.

<img width="604" height="384" alt="ScreenShot Tool -20261102194934" src="https://github.com/user-attachments/assets/1b2c6f1f-1ae3-423b-adc4-cbf777c16711" />
<img width="1920" height="869" alt="ScreenShot Tool -20261102192351" src="https://github.com/user-attachments/assets/ce5cbcc5-193c-45f1-9669-488bee529f21" />


## Tech Stack
Python (pandas), SQLite (for data quality checks), HubSpot (CRM), Looker Studio, LLM (drafting).

## How to Run
```bash
python src/01_source.py
python src/02_enrich.py
python src/03_clean.py
python src/04_score.py
python src/05_outreach_draft.py


---

### 🖼️ One last thing to add: Screenshots

At the bottom of the README (right before Tech Stack), you need to insert the images you took.

```markdown
## Dashboard
![Pipeline Dashboard](docs/dashboard_screenshot.png)

## HubSpot CRM
![HubSpot Import](docs/hubspot_screenshot.png)
