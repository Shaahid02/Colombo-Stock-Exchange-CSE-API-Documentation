# CSE API Documentation & Python Client

This repository contains a comprehensive Python client for the Colombo Stock Exchange (CSE) API, along with documentation and examples.

## 📁 Files Overview

- **`app.py`** - Main CSE API client class with all endpoint methods
- **`cse_api_examples.py`** - Comprehensive examples and demonstrations
- **`quick_test.py`** - Quick test script to verify API functionality
- **`index.html`** - Web-based API documentation
- **`api_endpoint_urls.txt`** - List of all available API endpoints

## 🚀 Quick Start

```python
from app import CSE_API

# Initialize the API client
cse = CSE_API()

# Get market status
status = cse.get_market_status()
print(status['data'])

# Get company information
company = cse.get_company_info("LOLC.N0000")
print(company['data'])
```

## 📊 Available API Endpoints

### Stock Information APIs

| Method                              | Endpoint           | Parameters          | Description                              |
| ----------------------------------- | ------------------ | ------------------- | ---------------------------------------- |
| `get_company_info(symbol)`          | companyInfoSummery | symbol (required)   | Detailed info of a single stock/security |
| `get_trade_summary()`               | tradeSummary       | None                | Summary of trades for all securities     |
| `get_today_share_price()`           | todaySharePrice    | None                | Today's share price data                 |
| `get_top_gainers()`                 | topGainers         | None                | List of top gaining stocks               |
| `get_top_losers()`                  | topLooses          | None                | List of top losing stocks                |
| `get_most_active_trades()`          | mostActiveTrades   | None                | Most active trades by volume             |
| `get_detailed_trades(symbol)`       | detailedTrades     | symbol (optional)   | Detailed trades information              |
| `get_companies_by_alphabet(letter)` | alphabetical       | alphabet (required) | Companies starting with specific letter  |
| `get_all_companies()`               | alphabetical (A-Z) | None                | All registered companies (iterates A-Z)  |

### Market Data APIs

| Method                       | Endpoint           | Parameters | Description                               |
| ---------------------------- | ------------------ | ---------- | ----------------------------------------- |
| `get_market_status()`        | marketStatus       | None       | Market open/close status                  |
| `get_market_summary()`       | marketSummery      | None       | Market summary data                       |
| `get_daily_market_summary()` | dailyMarketSummery | None       | Daily market summary with historical data |

### Index Data APIs

| Method                   | Endpoint   | Parameters        | Description                 |
| ------------------------ | ---------- | ----------------- | --------------------------- |
| `get_aspi_data()`        | aspiData   | None              | All Share Price Index data  |
| `get_snp_data()`         | snpData    | None              | S&P Sri Lanka 20 Index data |
| `get_chart_data(symbol)` | chartData  | symbol (required) | Chart data for stocks       |
| `get_all_sectors()`      | allSectors | None              | All sector data             |

### Announcement APIs

| Method                               | Endpoint                                  | Parameters | Description                            |
| ------------------------------------ | ----------------------------------------- | ---------- | -------------------------------------- |
| `get_new_listings_announcements()`   | getNewListingsRelatedNoticesAnnouncements | None       | New listings and related announcements |
| `get_buy_in_board_announcements()`   | getBuyInBoardAnnouncements                | None       | Buy-in board announcements             |
| `get_approved_announcements()`       | approvedAnnouncement                      | None       | Approved announcements                 |
| `get_covid_announcements()`          | getCOVIDAnnouncements                     | None       | COVID-related announcements            |
| `get_financial_announcements()`      | getFinancialAnnouncement                  | None       | Financial announcements                |
| `get_circular_announcements()`       | circularAnnouncement                      | None       | Circular announcements                 |
| `get_directive_announcements()`      | directiveAnnouncement                     | None       | Directive announcements                |
| `get_non_compliance_announcements()` | getNonComplianceAnnouncements             | None       | Non-compliance announcements           |

## 💡 Usage Examples

### Basic Usage

```python
from app import CSE_API

cse = CSE_API()

# Get market dashboard
def market_dashboard():
    # Market status
    status = cse.get_market_status()
    print(f"Market Status: {status['data']['status']}")

    # ASPI Index
    aspi = cse.get_aspi_data()
    print(f"ASPI: {aspi['data']['value']} ({aspi['data']['change']:+.2f})")

    # Top gainers
    gainers = cse.get_top_gainers()
    print("Top Gainers:")
    for stock in gainers['data'][:5]:
        print(f"  {stock['symbol']}: +{stock['changePercentage']:.2f}%")
```

### Stock Analysis

```python
def analyze_stock(symbol):
    cse = CSE_API()

    # Company information
    info = cse.get_company_info(symbol)
    if info['success']:
        company_name = info['data']['reqSymbolInfo']['name']
        print(f"Company: {company_name}")

    # Detailed trades
    trades = cse.get_detailed_trades(symbol)
    if trades['success']:
        for trade in trades['data']['reqDetailTrades']:
            if trade['symbol'] == symbol:
                print(f"Price: {trade['price']}")
                print(f"Change: {trade['change']} ({trade['changePercentage']:.2f}%)")
                print(f"Volume: {trade['qty']}")

# Usage
analyze_stock("LOLC.N0000")
```

### Getting All Companies

````python
def get_companies_by_letter():
    cse = CSE_API()

    # Get companies starting with 'A'
    result = cse.get_companies_by_alphabet('A')
    if result['success']:
        companies = result['data']['reqAlphabetical']
        for company in companies[:5]:  # Show first 5
            print(f"{company['name']} ({company['symbol']}) - ${company['price']}")

def get_all_registered_companies():
    cse = CSE_API()

    # This will fetch ALL companies (A-Z) - takes 2-3 minutes
    result = cse.get_all_companies()
    if result['success']:
        print(f"Total companies: {result['total_companies']}")

        # Save to file
        with open('all_companies.json', 'w') as f:
            json.dump(result['data'], f, indent=2)

        return result['data']

# Usage
get_companies_by_letter()
all_companies = get_all_registered_companies()
```### Error Handling

All API methods return a dictionary with the following structure:

```python
{
    'success': True/False,
    'status_code': 200,  # HTTP status code
    'data': {...},       # API response data (if success=True)
    'error': "..."       # Error message (if success=False)
}
````

Example with error handling:

```python
response = cse.get_company_info("INVALID.SYMBOL")
if response['success']:
    print("Data:", response['data'])
else:
    print(f"Error: {response['error']}")
    print(f"Status Code: {response['status_code']}")
```

## 🧪 Running Tests

### Quick Test

```bash
python quick_test.py
```

### Comprehensive Test

```bash
python cse_api_examples.py
```

### Interactive Examples

```bash
python cse_api_examples.py
# Choose from:
# 1. Market Dashboard
# 2. Specific Stock Analysis
# 3. Comprehensive API Test
```

## 📋 API Response Examples

### Company Information

```json
{
  "reqSymbolInfo": {
    "symbol": "LOLC.N0000",
    "name": "L O L C HOLDINGS PLC",
    "sector": "Diversified Financials",
    "currentPrice": 285.0
  },
  "reqLogo": {
    "path": "upload_logo/378_1601611239.jpeg"
  }
}
```

### Market Status

```json
{
  "status": "Market Closed"
}
```

### Top Gainers

```json
[
  {
    "symbol": "HEXP.N0000",
    "changePercentage": 15.86,
    "price": 12.5,
    "change": 1.7
  }
]
```

### Market Summary

```json
{
  "tradeVolume": 3263762020.0,
  "shareVolume": 115084307,
  "marketCap": 6940225783432.0
}
```

### Companies by Alphabet

```json
{
  "reqAlphabetical": [
    {
      "id": 188,
      "name": "BAIRAHA FARMS PLC",
      "symbol": "BFL.N0000",
      "lastTradedTime": 1756109291425,
      "price": 211.0,
      "turnover": 596200.25,
      "sharevolume": 2849,
      "tradevolume": 29,
      "percentageChange": 0.7159904534606205,
      "change": 1.5
    }
  ]
}
```

}

```

## 🔧 Technical Details

### Base URL

```

https://www.cse.lk/api/

````

### Request Method

All endpoints use **POST** requests with `application/x-www-form-urlencoded` content type.

### Headers

```python
{
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
````

### Rate Limiting

The API doesn't specify rate limits, but it's recommended to:

- Add delays between requests
- Implement retry logic for failed requests
- Cache responses when appropriate

## 🛠️ Dependencies

```bash
pip install requests
```

## 📝 Notes

1. **Symbol Format**: Stock symbols typically end with `.N0000` or `.X0000`
2. **Chart Data**: May return HTTP 400 for some symbols
3. **Market Hours**: Some data may be limited during market closed hours
4. **Response Format**: All responses are in JSON format

## 🤝 Contributing

Feel free to contribute by:

- Adding new endpoint methods
- Improving error handling
- Adding more examples
- Updating documentation

## ⚠️ Disclaimer

This is an unofficial API client. The CSE API is provided by the Colombo Stock Exchange and may change without notice. Always verify data accuracy for trading decisions.

## 📞 Support

For API-related questions, contact the Colombo Stock Exchange directly. For client library issues, please create an issue in this repository.
