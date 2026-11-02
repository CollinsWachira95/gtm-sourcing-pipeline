import pandas as pd

df = pd.read_csv("data/raw_companies.csv", encoding="utf-8")

print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

print("\n=== VALIDATION ===")

missing_url = df["source_url"].isna() | (df["source_url"].astype(str).str.strip() == "")
print(f"Rows missing source_url: {missing_url.sum()}")
if missing_url.sum() > 0:
    print("  Every row must have a URL you actually visited.")
    print(df[missing_url][["company_name", "source"]].to_string())

missing_name = df["company_name"].isna() | (df["company_name"].astype(str).str.strip() == "")
print(f"Rows missing company_name: {missing_name.sum()}")

print("\n=== ROWS PER SOURCE ===")
print(df["source"].value_counts())

normalized = df["company_name"].astype(str).str.strip().str.lower()
dupes = normalized[normalized.duplicated(keep=False)]
if len(dupes) > 0:
    print("\n=== POSSIBLE DUPLICATES ===")
    print(df[normalized.isin(dupes)][["company_name", "source"]].to_string())
else:
    print("\nNo duplicate names detected.")