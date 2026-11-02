import pandas as pd

df = pd.read_csv("data/cleaned_companies.csv", encoding="utf-8")

def score_row(row):
    s = 0
    if row["pe_backed"] == "yes":     s += 3
    if row["acquisition"] == "yes":   s += 2
    if row["erp_hiring"] == "yes":    s += 2
    if row["multi_entity"] == "yes":  s += 1
    return s

df["icp_score"] = df.apply(score_row, axis=1)
df = df.sort_values("icp_score", ascending=False).reset_index(drop=True)
df["rank"] = df.index + 1

df.to_csv("data/scored_companies.csv", index=False, encoding="utf-8")

# --- summary ---
print(f"Scored {len(df)} companies")
print(f"Score distribution:")
print(df["icp_score"].value_counts().sort_index(ascending=False).to_string())
print(f"\nTop 10 accounts:")
print(df[["rank", "company_name", "icp_score", "pe_backed", "acquisition", "erp_hiring", "multi_entity"]].head(10).to_string(index=False))