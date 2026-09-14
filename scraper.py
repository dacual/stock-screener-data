import json

# 1. 40-Stock Universe Baseline (10 Tech + 3 per remaining 10 GICS sectors)
UNIVERSE = [
    # Technology (10 Tickers)
    {"Sector": "Technology", "Rank": 1, "Symbol": "NVDA", "Company Name": "NVIDIA Corporation"},
    {"Sector": "Technology", "Rank": 2, "Symbol": "AAPL", "Company Name": "Apple Inc."},
    {"Sector": "Technology", "Rank": 3, "Symbol": "MSFT", "Company Name": "Microsoft Corporation"},
    {"Sector": "Technology", "Rank": 4, "Symbol": "TSM", "Company Name": "Taiwan Semiconductor Manufacturing"},
    {"Sector": "Technology", "Rank": 5, "Symbol": "AVGO", "Company Name": "Broadcom Inc."},
    {"Sector": "Technology", "Rank": 6, "Symbol": "MU", "Company Name": "Micron Technology, Inc."},
    {"Sector": "Technology", "Rank": 7, "Symbol": "SKHY", "Company Name": "SK hynix Inc."},
    {"Sector": "Technology", "Rank": 8, "Symbol": "AMD", "Company Name": "Advanced Micro Devices, Inc."},
    {"Sector": "Technology", "Rank": 9, "Symbol": "ASML", "Company Name": "ASML Holding N.V."},
    {"Sector": "Technology", "Rank": 10, "Symbol": "INTC", "Company Name": "Intel Corporation"},

    # Healthcare (3 Tickers)
    {"Sector": "Healthcare", "Rank": 1, "Symbol": "LLY", "Company Name": "Eli Lilly and Company"},
    {"Sector": "Healthcare", "Rank": 2, "Symbol": "UNH", "Company Name": "UnitedHealth Group Incorporated"},
    {"Sector": "Healthcare", "Rank": 3, "Symbol": "JNJ", "Company Name": "Johnson & Johnson"},

    # Financials (3 Tickers)
    {"Sector": "Financials", "Rank": 1, "Symbol": "JPM", "Company Name": "JPMorgan Chase & Co."},
    {"Sector": "Financials", "Rank": 2, "Symbol": "BAC", "Company Name": "Bank of America Corporation"},
    {"Sector": "Financials", "Rank": 3, "Symbol": "WFC", "Company Name": "Wells Fargo & Company"},

    # Consumer Discretionary (3 Tickers)
    {"Sector": "Consumer Discretionary", "Rank": 1, "Symbol": "AMZN", "Company Name": "Amazon.com, Inc."},
    {"Sector": "Consumer Discretionary", "Rank": 2, "Symbol": "TSLA", "Company Name": "Tesla, Inc."},
    {"Sector": "Consumer Discretionary", "Rank": 3, "Symbol": "HD", "Company Name": "The Home Depot, Inc."},

    # Communication Services (3 Tickers)
    {"Sector": "Communication Services", "Rank": 1, "Symbol": "GOOGL", "Company Name": "Alphabet Inc."},
    {"Sector": "Communication Services", "Rank": 2, "Symbol": "META", "Company Name": "Meta Platforms, Inc."},
    {"Sector": "Communication Services", "Rank": 3, "Symbol": "NFLX", "Company Name": "Netflix, Inc."},

    # Industrials (3 Tickers)
    {"Sector": "Industrials", "Rank": 1, "Symbol": "GE", "Company Name": "General Electric Company"},
    {"Sector": "Industrials", "Rank": 2, "Symbol": "CAT", "Company Name": "Caterpillar Inc."},
    {"Sector": "Industrials", "Rank": 3, "Symbol": "RTX", "Company Name": "RTX Corporation"},

    # Consumer Staples (3 Tickers)
    {"Sector": "Consumer Staples", "Rank": 1, "Symbol": "PG", "Company Name": "The Procter & Gamble Company"},
    {"Sector": "Consumer Staples", "Rank": 2, "Symbol": "COST", "Company Name": "Costco Wholesale Corporation"},
    {"Sector": "Consumer Staples", "Rank": 3, "Symbol": "WMT", "Company Name": "Walmart Inc."},

    # Energy (3 Tickers)
    {"Sector": "Energy", "Rank": 1, "Symbol": "XOM", "Company Name": "Exxon Mobil Corporation"},
    {"Sector": "Energy", "Rank": 2, "Symbol": "CVX", "Company Name": "Chevron Corporation"},
    {"Sector": "Energy", "Rank": 3, "Symbol": "COP", "Company Name": "ConocoPhillips"},

    # Utilities (3 Tickers)
    {"Sector": "Utilities", "Rank": 1, "Symbol": "NEE", "Company Name": "NextEra Energy, Inc."},
    {"Sector": "Utilities", "Rank": 2, "Symbol": "SO", "Company Name": "The Southern Company"},
    {"Sector": "Utilities", "Rank": 3, "Symbol": "DUK", "Company Name": "Duke Energy Corporation"},

    # Real Estate (3 Tickers)
    {"Sector": "Real Estate", "Rank": 1, "Symbol": "PLD", "Company Name": "Prologis, Inc."},
    {"Sector": "Real Estate", "Rank": 2, "Symbol": "AMT", "Company Name": "American Tower Corporation"},
    {"Sector": "Real Estate", "Rank": 3, "Symbol": "EQIX", "Company Name": "Equinix, Inc."},

    # Basic Materials (3 Tickers)
    {"Sector": "Basic Materials", "Rank": 1, "Symbol": "LIN", "Company Name": "Linde plc"},
    {"Sector": "Basic Materials", "Rank": 2, "Symbol": "SHW", "Company Name": "The Sherwin-Williams Company"},
    {"Sector": "Basic Materials", "Rank": 3, "Symbol": "FCX", "Company Name": "Freeport-McMoRan Inc."}
]

# Write sector summary file
with open("sector_top3.json", "w", encoding="utf-8") as f:
    json.dump(UNIVERSE, f, indent=2)

# Generate forecast structure dataset
forecast_dataset = []
for item in UNIVERSE:
    sym = item["Symbol"]
    forecast_dataset.extend([
        {"Symbol": sym, "Sector": item["Sector"], "Metric": "Revenue High", "Year": "2026", "Value": 100.0, "RawValue": "100.0B"},
        {"Symbol": sym, "Sector": item["Sector"], "Metric": "Revenue Avg", "Year": "2026", "Value": 90.0, "RawValue": "90.0B"},
        {"Symbol": sym, "Sector": item["Sector"], "Metric": "Revenue Low", "Year": "2026", "Value": 80.0, "RawValue": "80.0B"},
        {"Symbol": sym, "Sector": item["Sector"], "Metric": "Revenue High", "Year": "2027", "Value": 120.0, "RawValue": "120.0B"},
        {"Symbol": sym, "Sector": item["Sector"], "Metric": "Revenue Avg", "Year": "2027", "Value": 110.0, "RawValue": "110.0B"},
        {"Symbol": sym, "Sector": item["Sector"], "Metric": "Revenue Low", "Year": "2027", "Value": 100.0, "RawValue": "100.0B"}
    ])

with open("portfolio_forecasts.json", "w", encoding="utf-8") as f:
    json.dump(forecast_dataset, f, indent=2)

print(f"Generated sector_top3.json with {len(UNIVERSE)} tickers.")
print(f"Generated portfolio_forecasts.json with {len(forecast_dataset)} records.")
