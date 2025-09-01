import pandas as pd
import re

# Load CSV
df = pd.read_csv("training_data/daily_market_capitalization(1).csv", dtype=str)

date_col = "date_scraped"  # adjust if needed

# Step 1: Detect ambiguous dates (both <=12)
def is_ambiguous(date_str):
    if not isinstance(date_str, str):
        return False
    match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_str.strip())
    if not match:
        return False
    d1, d2, _ = map(int, match.groups())
    return d1 <= 12 and d2 <= 12

df["ambiguous"] = df[date_col].apply(is_ambiguous)

# Step 2: Parse everything as dd/mm/yyyy (since we know sequence starts April 10)
df["resolved_date"] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")

# Step 3: Build correction log for ambiguous ones
corrections = []
for idx, row in df[df["ambiguous"]].iterrows():
    us_fmt = pd.to_datetime(row[date_col], dayfirst=False, errors="coerce")
    intl_fmt = pd.to_datetime(row[date_col], dayfirst=True, errors="coerce")
    corrections.append({
        "original": row[date_col],
        "us_format": us_fmt.strftime("%d/%m/%Y") if pd.notna(us_fmt) else None,
        "intl_format": intl_fmt.strftime("%d/%m/%Y") if pd.notna(intl_fmt) else None,
        "chosen": intl_fmt.strftime("%d/%m/%Y") if pd.notna(intl_fmt) else None
    })

# Step 4: Format final column as dd/mm/yyyy
df[date_col] = df["resolved_date"].dt.strftime("%d/%m/%Y")

# Step 5: Save outputs
df.to_csv("training_data/normalized_dates.csv", index=False)
if corrections:
    pd.DataFrame(corrections).to_csv("training_data/auto_corrected_dates.csv", index=False)

print("✅ All dates normalized to dd/mm/yyyy (assumed ascending from 10 April → 26 August).")
print(" - Cleaned file: training_data/normalized_dates.csv")
print(" - Ambiguous log: training_data/auto_corrected_dates.csv")
