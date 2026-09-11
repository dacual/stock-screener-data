import json
import re
import urllib.request

# All 11 GICS Sectors mapped to StockAnalysis URLs
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

all_sector_data = []

for sector_name, url in SECTORS.items():
    # Set limit: Top 10 for Tech, Top 3 for all other sectors
    rank_limit = 10 if sector_name == "Technology" else 3
    print(f"Scraping top {rank_limit} for sector: {sector_name}...")

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")

            # Extract table rows
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)

            rank = 1
            for row in rows:
                if rank > rank_limit:
                    break

                # Extract Ticker/Symbol
                symbol_match = re.search(
                    r'/stocks/([a-z0-9\.\-]+)/"', row, re.IGNORECASE
                )
                if symbol_match:
                    symbol = symbol_match.group(1).upper()

                    # Extract Company Name
                    name_match = re.search(r'title="([^"]+)"', row)
                    company_name = (
                        name_match.group(1) if name_match else symbol
                    )

                    all_sector_data.append(
                        {
                            "Sector": sector_name,
                            "Rank": rank,
                            "Symbol": symbol,
                            "Company Name": company_name,
                        }
                    )
                    rank += 1
    except Exception as e:
        print(f"Error scraping {sector_name}: {e}")

# Save JSON file output
with open("sector_top3.json", "w", encoding="utf-8") as f:
    json.dump(all_sector_data, f, indent=2)

print(
    f"Successfully generated sector_top3.json with {len(all_sector_data)} total records."
)
