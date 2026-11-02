import pandas as pd

df = pd.read_csv("data/scored_companies.csv", encoding="utf-8")
top10 = df.head(10).copy()

drafts = []
for _, row in top10.iterrows():
    # Build the signal context from the row's verified facts
    signals = []
    if row["pe_backed"] == "yes":
        signals.append("PE-backed (a PE owner is likely pushing consolidated reporting)")
    if row["acquisition"] == "yes":
        signals.append("recent acquisition (integrating the new entity creates reporting pain)")
    if row["erp_hiring"] == "yes":
        signals.append("hiring for ERP roles (finance-system migration is in progress)")
    if row["multi_entity"] == "yes":
        signals.append("multi-entity (consolidation across subsidiaries is a current pain)")

    # This is the prompt you'd paste into ChatGPT / Claude / an API
    prompt = f"""You are drafting a first-touch email to a German CFO.

Company: {row['company_name']}
City: {row['city'] if pd.notna(row['city']) else 'Germany'}
Signals we identified: {'; '.join(signals)}
Product: ARC Intelligence — an AI-native Finance OS that connects ERP systems
and consolidates finance data for Mittelstand CFOs.

Write 3–4 sentences maximum. Direct, respectful, not salesy. Reference the
signal as the hook. Close with a specific question (not "let me know if you're
interested"). Do not invent facts about the company.
"""
    drafts.append({
        "rank": row["rank"],
        "company_name": row["company_name"],
        "icp_score": row["icp_score"],
        "signals": "; ".join(signals),
        "prompt": prompt,
        "draft": "",  # <-- paste LLM output here
    })

# Save prompts + (eventually) drafts
out = pd.DataFrame(drafts)
out.to_csv("data/outreach_prompts.csv", index=False, encoding="utf-8")
print(f"Generated {len(out)} prompts → data/outreach_prompts.csv")
print("\nNext step: paste each prompt into an LLM, copy the draft back into")
print("data/outreach_prompts.csv, and save as data/outreach_drafts.md")