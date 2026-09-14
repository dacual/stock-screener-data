from datetime import datetime
import json
import os
import numpy as np
import pandas as pd


def fetch_raw_data(source_path="data.json") -> pd.DataFrame:
  """Loads raw stock analysis data from a JSON file or API response."""
  if os.path.exists(source_path):
    with open(source_path, "r", encoding="utf-8") as f:
      data = json.load(f)
    return pd.DataFrame(data)
  else:
    # Fallback dummy data if file does not exist yet
    return pd.DataFrame([
        {"Ticker": "AAPL", "Metric": "Revenue", "2026": 412000000000, "2027": 455000000000},
        {"Ticker": "NVDA", "Metric": "Revenue", "2026": 128000000000, "2027": 165000000000},
    ])


def standardize_year_columns(df: pd.DataFrame) -> pd.DataFrame:
  """Dynamically maps current and next year column headers to 'Current Year' and

  'Next Year', and computes YoY growth cleanly without hardcoded years.
  """
  df = df.copy()

  # 1. Resolve current calendar year dynamically
  now = datetime.now()
  cur_year = str(now.year)  # Dynamically resolves to "2026"
  nxt_year = str(now.year + 1)  # Dynamically resolves to "2027"

  # 2. Rename year columns safely
  rename_dict = {}
  if cur_year in df.columns:
    rename_dict[cur_year] = "Current Year"
  if nxt_year in df.columns:
    rename_dict[nxt_year] = "Next Year"

  df.rename(columns=rename_dict, inplace=True)

  # 3. Calculate % Growth and formatting
  if "Current Year" in df.columns and "Next Year" in df.columns:
    df["Current Year"] = pd.to_numeric(df["Current Year"], errors="coerce")
    df["Next Year"] = pd.to_numeric(df["Next Year"], errors="coerce")

    # YoY Growth Formula: ((Next Year - Current Year) / |Current Year|) * 100
    df["YoY Growth %"] = np.where(
        (df["Current Year"].notna()) & (df["Current Year"] != 0),
        (
            (df["Next Year"] - df["Current Year"])
            / df["Current Year"].abs()
        )
        * 100,
        np.nan,
    )

    # Add green/red emoji display column
    def format_icon(val):
      if pd.isna(val):
        return "N/A"
      icon = "🟢" if val > 0 else ("🔴" if val < 0 else "⚪")
      return f"{icon} {val:+.2f}%"

    df["YoY Growth Display"] = df["YoY Growth %"].apply(format_icon)

  return df


def save_processed_data(
    df: pd.DataFrame, json_path="output.json", excel_path="output.xlsx"
):
  """Saves the transformed DataFrame into output formats."""
  # Export clean JSON
  df.to_json(json_path, orient="records", indent=2)

  # Export clean Excel sheet
  df.to_excel(excel_path, index=False)
  print(f"Successfully exported data to {json_path} and {excel_path}")


def main():
  # Step 1: Fetch raw data
  raw_df = fetch_raw_data()

  # Step 2: Transform year headers & calculate growth
  processed_df = standardize_year_columns(raw_df)

  # Step 3: Export output files
  save_processed_data(processed_df)


if __name__ == "__main__":
  main()
