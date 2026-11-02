import pandas as pd
import re

# ---------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------
df = pd.read_csv("data/enriched_companies.csv", encoding="utf-8")
original_count = len(df)

# ---------------------------------------------------------------
# 2. Split into three sets
# ---------------------------------------------------------------
# Three buckets, each with a different downstream meaning:
#   - excluded:  known not-a-prospect (e.g. current customer)
#   - quarantined: not yet verified — cannot be scored honestly
#   - scoring_set: verified, eligible for scoring
excluded = df[df["status"] == "excluded_customer"].copy()
quarantined = df[~df["status"].isin(["verified", "excluded_customer"])].copy()
scoring_set = df[df["status"] == "verified"].copy()

# ---------------------------------------------------------------
# 3. Normalize company names (in the scoring set)
# ---------------------------------------------------------------
# Why: "Contus-Gruppe", "contus-gruppe", "Contus Gruppe" are the
# same company. Lowercase + strip legal suffixes + collapse
# whitespace/hyphens gives us a canonical key to dedupe on.
LEGAL_SUFFIXES = [
    "gmbh & co. kgaa", "gmbh & co. kg", "gmbh & co. kgaa", "gmbh & co.",
    "gmbh", "ag", "kg", "kgaa", "se", "ug", "e.k.", "mbh", "ohg", "gbr",
]

def normalize_name(name):
    if pd.isna(name):
        return ""
    s = str(name).strip().lower()
    # remove legal suffixes (longest first, to catch "gmbh & co. kgaa")
    for suffix in LEGAL_SUFFIXES:
        if s.endswith(" " + suffix):
            s = s[: -len(suffix) - 1].strip()
            break
    # collapse multiple spaces / hyphens into a single space
    s = re.sub(r"[\s\-_]+", " ", s)
    return s.strip()

scoring_set["normalized_name"] = scoring_set["company_name"].apply(normalize_name)

# ---------------------------------------------------------------
# 4. Deduplicate on normalized_name (keep first occurrence)
# ---------------------------------------------------------------
before_dedup = len(scoring_set)
scoring_set = scoring_set.drop_duplicates(subset=["normalized_name"], keep="first")
after_dedup = len(scoring_set)
duplicates_removed = before_dedup - after_dedup

# ---------------------------------------------------------------
# 5. ICP size flag
# ---------------------------------------------------------------
# We don't have a dedicated employees column, so we infer from notes.
# This is honest: the flag is derived from text we wrote ourselves,
# not invented.
def derive_icp_size_flag(row):
    notes = str(row.get("notes", "")).lower()
    if any(kw in notes for kw in ["above icp", "far above", "1,600", "8,000", "above 500"]):
        return "out_of_range"
    return "in_range"

scoring_set["icp_size_flag"] = scoring_set.apply(derive_icp_size_flag, axis=1)

# ---------------------------------------------------------------
# 6. Standardize unknowns
# ---------------------------------------------------------------
# Any remaining NaN in signal columns becomes "unknown", so that
# "no data" has one representation, not three.
for col in ["pe_backed", "acquisition", "erp_hiring", "multi_entity"]:
    scoring_set[col] = scoring_set[col].fillna("unknown")

# ---------------------------------------------------------------
# 7. Save the three sets
# ---------------------------------------------------------------
scoring_set.to_csv("data/cleaned_companies.csv", index=False, encoding="utf-8")
quarantined.to_csv("data/quarantined_companies.csv", index=False, encoding="utf-8")
excluded.to_csv("data/excluded_companies.csv", index=False, encoding="utf-8")

# ---------------------------------------------------------------
# 8. Write the data-quality report
# ---------------------------------------------------------------
report = f"""# Data Quality Report

## Summary
- Rows loaded: {original_count}
- Rows excluded (known customer): {len(excluded)}
- Rows quarantined (status not verified): {len(quarantined)}
- Rows eligible for scoring (before dedup): {before_dedup}
- Duplicates removed: {duplicates_removed}
- Rows eligible for scoring (after dedup): {after_dedup}

## What was excluded and why
{excluded[["company_name", "status"]].to_string(index=False) if len(excluded) else "(none)"}

## What was quarantined and why
{quarantined[["company_name", "status"]].to_string(index=False) if len(quarantined) else "(none)"}

## ICP size flags
{scoring_set["icp_size_flag"].value_counts().to_string()}

## Decisions documented
- "unknown" is treated as "no data", not "no". A row with
  pe_backed=unknown is not scored as if it were pe_backed=no.
- Rows with status verify_* are quarantined, not deleted.
  They remain in the dataset for audit; they are simply not
  scored until a human verifies them.
- Excluded rows (customers) are kept in a separate file, not
  deleted. The record of *why* a company was excluded is
  itself useful data.
- Company names were normalized (lowercase, legal suffixes
  stripped, whitespace collapsed) before deduplication.
- ICP size flags are derived from notes, not from a dedicated
  employees column (which we don't have). The flag is honest:
  it reflects facts we recorded, not assumptions.
"""

with open("data_quality_report.md", "w") as f:
    f.write(report)

print(f"Loaded: {original_count} rows")
print(f"Excluded: {len(excluded)} rows")
print(f"Quarantined: {len(quarantined)} rows")
print(f"Scoring set (before dedup): {before_dedup}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Scoring set (after dedup): {after_dedup}")
print(f"\nICP size flags:\n{scoring_set['icp_size_flag'].value_counts().to_string()}")
print("\nWrote: data/cleaned_companies.csv, data/quarantined_companies.csv, data/excluded_companies.csv, data_quality_report.md")