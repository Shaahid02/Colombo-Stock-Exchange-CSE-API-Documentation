"""
Comprehensive CSE API Examples
This file demonstrates how to use all available CSE API endpoints
"""

from app import CSE_API
import json
import time

def print_json_response(title: str, response: dict, max_items: int = 3):
    """Helper function to print API responses in a formatted way"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    
    if not response['success']:
        print(f"❌ Error: {response['error']}")
        if response.get('status_code'):
            print(f"   Status Code: {response['status_code']}")
        return
    
    print(f"✅ Status Code: {response['status_code']}")
    
    data = response['data']
    if isinstance(data, list) and len(data) > max_items:
        print(f"📊 Showing first {max_items} of {len(data)} items:")
        print(json.dumps(data[:max_items], indent=2, default=str))
        print(f"... and {len(data) - max_items} more items")
    else:
        print("📊 Response:")
        print(json.dumps(data, indent=2, default=str))

def comprehensive_api_test():
    """Test all CSE API endpoints"""
    cse = CSE_API()
    
    print("🚀 Starting Comprehensive CSE API Test")
    print("This will test all available endpoints...")
    
    # 1. Stock Information APIs
    print_json_response(
        "1. Company Information (LOLC)", 
        cse.get_company_info("LOLC.N0000")
    )
    
    print_json_response(
        "2. Trade Summary", 
        cse.get_trade_summary(),
        max_items=5
    )
    
    print_json_response(
        "3. Today's Share Prices", 
        cse.get_today_share_price(),
        max_items=5
    )
    
    print_json_response(
        "4. Top Gainers", 
        cse.get_top_gainers(),
        max_items=5
    )
    
    print_json_response(
        "5. Top Losers", 
        cse.get_top_losers(),
        max_items=5
    )
    
    print_json_response(
        "6. Most Active Trades", 
        cse.get_most_active_trades(),
        max_items=5
    )
    
    print_json_response(
        "7. Detailed Trades (All)", 
        cse.get_detailed_trades(),
        max_items=5
    )
    
    print_json_response(
        "8. Detailed Trades (LOLC)", 
        cse.get_detailed_trades("LOLC.N0000")
    )
    
    # 2. Market Data APIs
    print_json_response(
        "9. Market Status", 
        cse.get_market_status()
    )
    
    print_json_response(
        "10. Market Summary", 
        cse.get_market_summary()
    )
    
    print_json_response(
        "11. Daily Market Summary", 
        cse.get_daily_market_summary(),
        max_items=2
    )
    
    # 3. Index Data APIs
    print_json_response(
        "12. ASPI Data", 
        cse.get_aspi_data()
    )
    
    print_json_response(
        "13. S&P Sri Lanka 20 Index Data", 
        cse.get_snp_data()
    )
    
    print_json_response(
        "14. Chart Data (LOLC)", 
        cse.get_chart_data("LOLC.N0000")
    )
    
    print_json_response(
        "15. All Sectors", 
        cse.get_all_sectors(),
        max_items=5
    )
    
    # 4. Announcement APIs
    print_json_response(
        "16. New Listings Announcements", 
        cse.get_new_listings_announcements(),
        max_items=3
    )
    
    print_json_response(
        "17. Buy-in Board Announcements", 
        cse.get_buy_in_board_announcements(),
        max_items=3
    )
    
    print_json_response(
        "18. Approved Announcements", 
        cse.get_approved_announcements(),
        max_items=3
    )
    
    print_json_response(
        "19. COVID Announcements", 
        cse.get_covid_announcements(),
        max_items=3
    )
    
    print_json_response(
        "20. Financial Announcements", 
        cse.get_financial_announcements(),
        max_items=3
    )
    
    print_json_response(
        "21. Circular Announcements", 
        cse.get_circular_announcements(),
        max_items=3
    )
    
    print_json_response(
        "22. Directive Announcements", 
        cse.get_directive_announcements(),
        max_items=3
    )
    
    print_json_response(
        "23. Non-Compliance Announcements", 
        cse.get_non_compliance_announcements(),
        max_items=3
    )
    
    print(f"\n{'='*50}")
    print("🎉 API Test Complete!")
    print("All 22 CSE API endpoints have been tested.")

def specific_stock_analysis(symbol: str):
    """Analyze a specific stock using multiple endpoints"""
    cse = CSE_API()
    
    print(f"\n🔍 Analyzing Stock: {symbol}")
    print("="*60)
    
    # Get company info
    company_info = cse.get_company_info(symbol)
    if company_info['success'] and 'reqSymbolInfo' in company_info['data']:
        info = company_info['data']['reqSymbolInfo']
        print(f"📈 Company: {info.get('name', 'N/A')}")
        print(f"🏷️  Symbol: {info.get('symbol', 'N/A')}")
    
    # Get detailed trades for this stock
    trades = cse.get_detailed_trades(symbol)
    if trades['success'] and 'reqDetailTrades' in trades['data']:
        for trade in trades['data']['reqDetailTrades']:
            if trade.get('symbol') == symbol:
                print(f"💰 Current Price: {trade.get('price', 'N/A')}")
                print(f"📊 Change: {trade.get('change', 'N/A')} ({trade.get('changePercentage', 0):.2f}%)")
                print(f"📦 Volume: {trade.get('qty', 'N/A')}")
                print(f"🔄 Trades: {trade.get('trades', 'N/A')}")
                break
    
    # Get chart data
    chart_data = cse.get_chart_data(symbol)
    if chart_data['success']:
        print("📈 Chart data available")
    else:
        print(f"📈 Chart data: {chart_data.get('error', 'Not available')}")

def market_dashboard():
    """Create a simple market dashboard"""
    cse = CSE_API()
    
    print("\n📊 CSE MARKET DASHBOARD")
    print("="*40)
    
    # Market Status
    status = cse.get_market_status()
    if status['success']:
        print(f"🏢 Market Status: {status['data'].get('status', 'N/A')}")
    
    # Market Summary
    summary = cse.get_market_summary()
    if summary['success']:
        data = summary['data']
        print(f"💵 Trade Volume: {data.get('tradeVolume', 0):,.0f}")
        print(f"📈 Share Volume: {data.get('shareVolume', 0):,.0f}")
    
    # Indices
    aspi = cse.get_aspi_data()
    if aspi['success']:
        data = aspi['data']
        print(f"📊 ASPI: {data.get('value', 0):,.2f} ({data.get('change', 0):+.2f})")
    
    snp = cse.get_snp_data()
    if snp['success']:
        data = snp['data']
        print(f"📊 S&P SL20: {data.get('value', 0):,.2f} ({data.get('change', 0):+.2f})")
    
    # Top Movers
    print("\n🚀 TOP GAINERS:")
    gainers = cse.get_top_gainers()
    if gainers['success'] and isinstance(gainers['data'], list):
        for i, stock in enumerate(gainers['data'][:3]):
            print(f"   {i+1}. {stock.get('symbol', 'N/A')}: +{stock.get('changePercentage', 0):.2f}%")
    
    print("\n📉 TOP LOSERS:")
    losers = cse.get_top_losers()
    if losers['success'] and isinstance(losers['data'], list):
        for i, stock in enumerate(losers['data'][:3]):
            print(f"   {i+1}. {stock.get('symbol', 'N/A')}: {stock.get('changePercentage', 0):.2f}%")

if __name__ == "__main__":
    # Choose what to run
    print("CSE API Examples")
    print("================")
    print("1. Market Dashboard")
    print("2. Specific Stock Analysis")
    print("3. Comprehensive API Test (all endpoints)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        market_dashboard()
    elif choice == "2":
        symbol = input("Enter stock symbol (e.g., LOLC.N0000): ").strip()
        if symbol:
            specific_stock_analysis(symbol)
        else:
            print("No symbol provided")
    elif choice == "3":
        comprehensive_api_test()
    else:
        print("Invalid choice. Running market dashboard...")
        market_dashboard()
