import pandas as pd

df = pd.read_csv("data/raw_companies.csv", encoding="utf-8")

# --- 1. pe_backed ---
# Rule: if source starts with "pe_portfolio_", the company is on a PE firm's
# portfolio page — so it IS PE-backed. Otherwise, check notes for deal language.
def derive_pe_backed(row):
    if str(row["source"]).startswith("pe_portfolio_"):
        return "yes"
    notes_lower = str(row.get("notes", "")).lower()
    if row["source"] == "deal_press_release" and any(
        kw in notes_lower for kw in ["acquired", "investment", "majority", "stake"]
    ):
        return "yes"
    return "unknown"

df["pe_backed"] = df.apply(derive_pe_backed, axis=1)

# --- 2. acquisition ---
# Rule: notes mention acquisition / carve-out / add-on / buy-and-build.
def derive_acquisition(row):
    notes_lower = str(row.get("notes", "")).lower()
    if any(kw in notes_lower for kw in ["acqui", "add-on", "carve-out", "buy-and-build"]):
        return "yes"
    return "unknown"

df["acquisition"] = df.apply(derive_acquisition, axis=1)

# --- 3. erp_hiring ---
# Rule: source == "job_board_erp" OR notes mention ERP / SAP / DATEV / Dynamics.
def derive_erp_hiring(row):
    notes_lower = str(row.get("notes", "")).lower()
    if row["source"] == "job_board_erp":
        return "yes"
    if any(kw in notes_lower for kw in ["erp", "sap", "datev", "dynamics"]):
        return "yes"
    return "unknown"

df["erp_hiring"] = df.apply(derive_erp_hiring, axis=1)

# --- 4. multi_entity ---
# Rule: notes mention "multi-entity", "subsidiary", "group", "sites", "locations".
def derive_multi_entity(row):
    notes_lower = str(row.get("notes", "")).lower()
    if any(kw in notes_lower for kw in ["multi-entity", "subsidiary", "group", "sites", "locations"]):
        return "yes"
    return "unknown"

df["multi_entity"] = df.apply(derive_multi_entity, axis=1)

# --- Save ---
df.to_csv("data/enriched_companies.csv", index=False, encoding="utf-8")

print(f"Enriched {len(df)} rows")
print("\n=== pe_backed ===")
print(df["pe_backed"].value_counts())
print("\n=== acquisition ===")
print(df["acquisition"].value_counts())
print("\n=== erp_hiring ===")
print(df["erp_hiring"].value_counts())
print("\n=== multi_entity ===")
print(df["multi_entity"].value_counts())