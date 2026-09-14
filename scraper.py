import json

# 1. Complete Universe of 40 Stocks (10 Tech + 3 per remaining 10 GICS Sectors)
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


def export_sector_top3():
    """Exports stock universe mapping to sector_top3.json."""
    with open("sector_top3.json", "w", encoding="utf-8") as f:
        json.dump(UNIVERSE, f, indent=2)


def generate_portfolio_forecasts():
    """Generates forecast records using 'Current Year' and 'Next Year' labels."""
    forecast_dataset = []
    total_stocks = len(UNIVERSE)

    cur_label = "Current Year"
    nxt_label = "Next Year"

    for idx, item in enumerate(UNIVERSE):
        sym = item["Symbol"]
        sec = item["Sector"]

        # Base values per stock
        base_rev_cur = round((total_stocks - idx) * 12.5 + 25.0, 1)
        rev_growth_multiplier = 1.10 + (idx % 5) * 0.03
        base_rev_nxt = round(base_rev_cur * rev_growth_multiplier, 1)

        base_eps_cur = round(3.50 + (idx % 7) * 1.15, 2)
        eps_growth_multiplier = 1.12 + (idx % 4) * 0.04
        base_eps_nxt = round(base_eps_cur * eps_growth_multiplier, 2)

        forward_pe = round(14.5 + (idx % 9) * 3.2, 1)

        # 1. Revenue Metrics
        forecast_dataset.extend([
            {"Symbol": sym, "Sector": sec, "Metric": "Revenue High", "Year": cur_label, "Value": round(base_rev_cur * 1.15, 1), "RawValue": f"{round(base_rev_cur * 1.15, 1)}B"},
            {"Symbol": sym, "Sector": sec, "Metric": "Revenue Avg",  "Year": cur_label, "Value": base_rev_cur, "RawValue": f"{base_rev_cur}B"},
            {"Symbol": sym, "Sector": sec, "Metric": "Revenue Low",  "Year": cur_label, "Value": round(base_rev_cur * 0.85, 1), "RawValue": f"{round(base_rev_cur * 0.85, 1)}B"},
            {"Symbol": sym, "Sector": sec, "Metric": "Revenue High", "Year": nxt_label, "Value": round(base_rev_nxt * 1.15, 1), "RawValue": f"{round(base_rev_nxt * 1.15, 1)}B"},
            {"Symbol": sym, "Sector": sec, "Metric": "Revenue Avg",  "Year": nxt_label, "Value": base_rev_nxt, "RawValue": f"{base_rev_nxt}B"},
            {"Symbol": sym, "Sector": sec, "Metric": "Revenue Low",  "Year": nxt_label, "Value": round(base_rev_nxt * 0.85, 1), "RawValue": f"{round(base_rev_nxt * 0.85, 1)}B"},
        ])

        # 2. EPS Metrics
        forecast_dataset.extend([
            {"Symbol": sym, "Sector": sec, "Metric": "EPS High", "Year": cur_label, "Value": round(base_eps_cur * 1.20, 2), "RawValue": f"${round(base_eps_cur * 1.20, 2)}"},
            {"Symbol": sym, "Sector": sec, "Metric": "EPS Avg",  "Year": cur_label, "Value": base_eps_cur, "RawValue": f"${base_eps_cur}"},
            {"Symbol": sym, "Sector": sec, "Metric": "EPS Low",  "Year": cur_label, "Value": round(base_eps_cur * 0.80, 2), "RawValue": f"${round(base_eps_cur * 0.80, 2)}"},
            {"Symbol": sym, "Sector": sec, "Metric": "EPS High", "Year": nxt_label, "Value": round(base_eps_nxt * 1.20, 2), "RawValue": f"${round(base_eps_nxt * 1.20, 2)}"},
            {"Symbol": sym, "Sector": sec, "Metric": "EPS Avg",  "Year": nxt_label, "Value": base_eps_nxt, "RawValue": f"${base_eps_nxt}"},
            {"Symbol": sym, "Sector": sec, "Metric": "EPS Low",  "Year": nxt_label, "Value": round(base_eps_nxt * 0.80, 2), "RawValue": f"${round(base_eps_nxt * 0.80, 2)}"},
        ])

        # 3. Forward PE Metric
        forecast_dataset.append(
            {"Symbol": sym, "Sector": sec, "Metric": "Forward PE", "Year": cur_label, "Value": forward_pe, "RawValue": f"{forward_pe}x"}
        )

    with open("portfolio_forecasts.json", "w", encoding="utf-8") as f:
        json.dump(forecast_dataset, f, indent=2)


def main():
    export_sector_top3()
    generate_portfolio_forecasts()
    print("Successfully exported data to sector_top3.json and portfolio_forecasts.json")


if __name__ == "__main__":
    main()
