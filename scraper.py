import json
import re
import urllib.request

# All 11 GICS Sectors
SECTORS = {
    "Technology": "https://stockanalysis.com/stocks/industry/technology/",
    "Healthcare": "https://stockanalysis.com/stocks/industry/healthcare/",
    "Financials": "https://stockanalysis.com/stocks/industry/financial-services/",
    "Consumer Discretionary": "https://stockanalysis.com/stocks/industry/consumer-discretionary/",
    "Communication Services": "https://stockanalysis.com/stocks/industry/communication-services/",
    "Industrials": "https://stockanalysis.com/stocks/industry/industrials/",
    "Consumer Staples": "https://stockanalysis.com/stocks/industry/consumer-staples/",
    "Energy": "https://stockanalysis.com/stocks/industry/energy/",
    "Utilities": "https://stockanalysis.com/stocks/industry/utilities/",
    "Real Estate": "https://stockanalysis.com/stocks/industry/real-estate/",
    "Basic Materials": "https://stockanalysis.com/stocks/industry/basic-materials/",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. Get List of 40 Tickers
tickers_to_scrape = []

for sector_name, url in SECTORS.items():
    rank_limit = 10 if sector_name == "Technology" else 3
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)
            rank = 1
            for row in rows:
                if rank > rank_limit:
                    break
                symbol_match = re.search(
                    r'/stocks/([a-z0-9\.\-]+)/"', row, re.IGNORECASE
                )
                if symbol_match:
                    symbol = symbol_match.group(1).upper()
                    tickers_to_scrape.append(
                        {"symbol": symbol, "sector": sector_name}
                    )
                    rank += 1
    except Exception as e:
        print(f"Error fetching top list for {sector_name}: {e}")

print(f"Found {len(tickers_to_scrape)} tickers across 11 sectors.")

# 2. Scrape Revenue and EPS Forecasts for each Ticker
forecast_dataset = []


def clean_num(val):
    """Clean numeric strings like '426.9B', '10.10', '97.7%'."""
    if not val or "Pro" in val or "-" in val:
        return None
    val_clean = val.replace("$", "").replace("%", "").strip()
    multiplier = 1.0
    if val_clean.endswith("B"):
        multiplier = 1e9
        val_clean = val_clean[:-1]
    elif val_clean.endswith("M"):
        multiplier = 1e6
        val_clean = val_clean[:-1]
    elif val_clean.endswith("K"):
        multiplier = 1e3
        val_clean = val_clean[:-1]
    try:
        return float(val_clean) * multiplier
    except ValueError:
        return None


for item in tickers_to_scrape:
    symbol = item["symbol"]
    forecast_url = f"https://stockanalysis.com/stocks/{symbol.lower()}/forecast/"
    req = urllib.request.Request(forecast_url, headers=headers)

    print(f"Fetching forecast for {symbol}...")
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")

            # Parse Table Headers (Years)
            years = re.findall(
                r"<th[^>]*>\s*(20\d\d)\s*</th>", html, re.IGNORECASE
            )
            # Remove duplicates preserving order
            years = list(dict.fromkeys(years))

            # Parse Table Rows
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)
            for row in rows:
                cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
                if not cells:
                    continue

                # Strip HTML tags from cell strings
                clean_cells = [
                    re.sub(r"<[^>]+>", "", c).strip() for c in cells
                ]
                row_label = clean_cells[0]

                # Map relevant metrics
                if any(
                    k in row_label.lower()
                    for k in ["revenue", "eps", "growth", "high", "avg", "low"]
                ):
                    for idx, year in enumerate(years):
                        if idx + 1 < len(clean_cells):
                            raw_val = clean_cells[idx + 1]
                            parsed_val = clean_num(raw_val)
                            forecast_dataset.append(
                                {
                                    "Symbol": symbol,
                                    "Sector": item["sector"],
                                    "Metric": row_label,
                                    "Year": year,
                                    "Value": parsed_val,
                                    "RawValue": raw_val,
                                }
                            )
    except Exception as e:
        print(f"Error fetching forecast for {symbol}: {e}")

# Save JSON file output
with open("portfolio_forecasts.json", "w", encoding="utf-8") as f:
    json.dump(forecast_dataset, f, indent=2)

print("Saved portfolio_forecasts.json successfully.")
