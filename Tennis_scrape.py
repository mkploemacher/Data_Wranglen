import os
import requests
import pandas as pd
import tabula

# 1. Download the PDF if not already on disk
pdf_url = (
    "https://photoresources.wtatennis.com/wta/document/"
    "2020/11/16/98dcd689-f10e-4a15-a169-4f4974f9a3dc/PRIZE-MONEY-2020.pdf"
)
pdf_path = "/Users/Maartenkiko/Desktop/Tennis/Prize_money_WTA/prize_money_2020.pdf"

if not os.path.exists(pdf_path):
    print(f"Downloading PDF from {pdf_url} …")
    resp = requests.get(pdf_url)
    resp.raise_for_status()
    with open(pdf_path, "wb") as f:
        f.write(resp.content)
    print("Download complete.")

# 2. Extract all tables from every page
print("Extracting tables with tabula…")
tables = tabula.read_pdf(
    pdf_path,
    pages="all",
    multiple_tables=True,
    lattice=True,       # better when tables have explicit cell borders
    pandas_options={"dtype": str}
)

# 3. Concatenate into one DataFrame
print(f"Found {len(tables)} tables; concatenating…")
df = pd.concat(tables, ignore_index=True)

# 4. Basic cleanup
#    - Drop rows or columns that are completely empty
#    - Rename columns to meaningful names
df.dropna(how="all", axis=1, inplace=True)
df.dropna(how="all", axis=0, inplace=True)

# Typical columns in the WTA PDF are:
# ['Rank', 'Player', 'Nat', 'PrizeMoney (USD)', 'OtherEventEarnings', ...]
# Adjust to your actual column layout after inspecting df.columns
df.columns = [
    "Standing",
    "Name",
    "Nat",
    "Total",
    # …add or trim as you see fit
][: len(df.columns)]

# 5. Convert PrizeMoney to numeric
df["Total"] = (
    df["Total"]
    .str.replace(",", "")
    .astype(float)
)

# 6. Save to CSV
out_csv = "WTA_prize_money_2020.csv"
df.to_csv(out_csv, index=False)
print(f"Exported cleaned data to {out_csv}.")
