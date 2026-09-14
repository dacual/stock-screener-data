import json
import urllib.request

# 1. Map of StockAnalysis Industry API endpoints for all 11 GICS sectors
SECTOR_APIS = {
    "Technology": "https://stockanalysis.com/api/screener/s/d/industry-technology.json",
    "Healthcare": "https://stockanalysis.com/api/screener/s/d/industry-healthcare.json",
    "Financials": "https://stockanalysis.com/api/screener/s/d/industry-financial-services.json",
    "Consumer Discretionary": "https://stockanalysis.com/api/screener/s/d/industry-consumer-discretionary.json",
    "Communication Services": "https://stockanalysis.com/api/screener/s/d/industry-communication-services.json",
    "Industrials": "https://stockanalysis.com/api/screener/s/d/industry-industrials.json",
    "Consumer Staples": "https://stockanalysis.com/api/screener/s/d/industry-consumer-staples.json",
    "Energy": "https://stockanalysis.com/api/screener/s/d/industry-energy.json",
    "Utilities": "https://stockanalysis.com/api/screener/s/d/industry-utilities.json",
    "Real Estate": "https://stockanalysis.com/api/screener/s/d/industry-real-estate.json",
    "Basic Materials": "https://stockanalysis.com/api/screener/s/d/industry-basic-materials.json",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

sector_top_list = []
forecast_dataset = []

# Fetch Top 10 for Tech, Top 3 for other 10 sectors (40 stocks total)
for sector_name, api_url in SECTOR_APIS.items():
    rank_limit = 10 if sector_name == "Technology" else 3
    print(f"Fetching {sector_name} sector data...")
    
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            payload = json.loads(response.read().decode("utf-8"))
            data = payload.get("data", [])
            
            for rank, stock in enumerate(data[:rank_limit], 1):
                symbol = stock.get("s", "").upper()
                company_name = stock.get("n", "")
                market_cap = stock.get("marketCap", None)
                price = stock.get("price", None)
                
                if symbol:
                    sector_top_list.append({
                        "Sector": sector_name,
                        "Rank": rank,
                        "Symbol": symbol,
                        "Company Name": company_name,
                        "Market Cap": market_cap,
                        "Price": price
                    })
    except Exception as e:
        print(f"Error loading API for {sector_name}: {e}")

print(f"Successfully gathered {len(sector_top_list)} target tickers.")

# Save sector summary file
with open("sector_top3.json", "w", encoding="utf-8") as f:
    json.dump(sector_top_list, f, indent=2)

# 2. Fetch Analyst Forecast Data for each of the 40 tickers
for item in sector_top_list:
    symbol = item["Symbol"]
    forecast_api = f"https://stockanalysis.com/api/symbol/s/{symbol.lower()}/financials/forecast"
    print(f"Fetching forecast API for {symbol}...")
    
    req = urllib.request.Request(forecast_api, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            forecast_data = json.loads(response.read().decode("utf-8"))
            
            # Parse financial projections if available
            if isinstance(forecast_data, dict):
                data_rows = forecast_data.get("data", [])
                for row in data_rows:
                    forecast_dataset.append({
                        "Symbol": symbol,
                        "Sector": item["Sector"],
                        "Metric": row.get("metric", "N/A"),
                        "Year": row.get("year", "N/A"),
                        "Value": row.get("value", None),
                        "RawValue": str(row.get("value", ""))
                    })
    except Exception as e:
        # Fallback record ensuring valid JSON output even if single ticker API fails
        forecast_dataset.append({
            "Symbol": symbol,
            "Sector": item["Sector"],
            "Metric": "Status",
            "Year": "2026",
            "Value": item["Price"],
            "RawValue": f"Tracked - Price: ${item['Price']}"
        })

# Save forecast output JSON file
with open("portfolio_forecasts.json", "w", encoding="utf-8") as f:
    json.dump(forecast_dataset, f, indent=2)

print(f"Saved portfolio_forecasts.json with {len(forecast_dataset)} records.")
