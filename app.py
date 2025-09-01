import requests
import json
from typing import Optional, Dict, Any, List

class CSE_API:
    """
    Colombo Stock Exchange API Client
    All endpoints use POST requests with application/x-www-form-urlencoded data
    """
    
    def __init__(self):
        self.base_url = "https://www.cse.lk/api/"
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _make_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request to the CSE API"""
        try:
            response = requests.post(
                self.base_url + endpoint,
                data=data or {},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Failed to decode JSON response: {str(e)}',
                'status_code': response.status_code if 'response' in locals() else None
            }
    
    # Stock Information APIs
    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get detailed information of a single stock/security by symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'LOLC.N0000')
        
        Returns:
            Dict containing company info including logo and symbol information
        """
        return self._make_request("companyInfoSummery", {"symbol": symbol})
    
    def get_trade_summary(self) -> Dict[str, Any]:
        """
        Get summary of trades for all securities
        
        Returns:
            Dict containing trade summary for all securities
        """
        return self._make_request("tradeSummary")
    
    def get_today_share_price(self) -> Dict[str, Any]:
        """
        Get today's share price data for all stocks
        
        Returns:
            List of today's share prices for all securities
        """
        return self._make_request("todaySharePrice")
    
    def get_top_gainers(self) -> Dict[str, Any]:
        """
        Get list of top gaining stocks
        
        Returns:
            List of stocks with highest percentage gains
        """
        return self._make_request("topGainers")
    
    def get_top_losers(self) -> Dict[str, Any]:
        """
        Get list of top losing stocks
        
        Returns:
            List of stocks with highest percentage losses
        """
        return self._make_request("topLooses")
    
    def get_most_active_trades(self) -> Dict[str, Any]:
        """
        Get most active trades by volume
        
        Returns:
            List of most actively traded stocks
        """
        return self._make_request("mostActiveTrades")
    
    def get_detailed_trades(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed trades information
        
        Args:
            symbol (str, optional): Stock symbol to filter trades
        
        Returns:
            Dict containing detailed trade information
        """
        data = {"symbol": symbol} if symbol else {}
        return self._make_request("detailedTrades", data)
    
    def get_companies_by_alphabet(self, alphabet: str) -> Dict[str, Any]:
        """
        Get companies starting with a specific alphabet
        
        Args:
            alphabet (str): Single letter (A-Z) to filter companies
        
        Returns:
            Dict containing companies starting with the specified letter
        """
        return self._make_request("alphabetical", {"alphabet": alphabet.upper()})
    
    def get_all_companies(self) -> Dict[str, Any]:
        """
        Get all registered companies by iterating through all alphabets
        
        Returns:
            Dict containing all companies from A-Z, with success status and combined data
        """
        import string
        all_companies = []
        failed_requests = []
        
        print("Fetching all companies from A-Z...")
        
        for letter in string.ascii_uppercase:
            print(f"Fetching companies starting with '{letter}'...")
            response = self.get_companies_by_alphabet(letter)
            
            if response['success']:
                data = response['data']
                companies = []
                
                # Handle the reqAlphabetical response structure
                if isinstance(data, dict) and 'reqAlphabetical' in data:
                    companies = data['reqAlphabetical']
                elif isinstance(data, list):
                    companies = data
                
                if companies:
                    all_companies.extend(companies)
                    print(f"  Found {len(companies)} companies starting with '{letter}'")
                else:
                    print(f"  No companies found for '{letter}'")
            else:
                failed_requests.append({
                    'letter': letter,
                    'error': response['error']
                })
                print(f"  Failed to fetch companies for '{letter}': {response['error']}")
        
        print(f"\nCompleted! Total companies found: {len(all_companies)}")

        active_companies = [ c for c in all_companies if c.get('lastTradedTime') is not None ]

        print(f"Active companies (last traded time > 0): {len(active_companies)}")

        if failed_requests:
            print(f"Failed requests for letters: {[req['letter'] for req in failed_requests]}")
        
        return {
            'success': True,
            'total_companies': len(all_companies),
            'active_companies': len(active_companies),
            'data': [all_companies, active_companies],
            'failed_requests': failed_requests,
            'status_code': 200
        }
    
    # Market Data APIs
    def get_market_status(self) -> Dict[str, Any]:
        """
        Get current market open/close status
        
        Returns:
            Dict containing market status information
        """
        return self._make_request("marketStatus")
    
    def get_market_summary(self) -> Dict[str, Any]:
        """
        Get market summary data
        
        Returns:
            Dict containing comprehensive market statistics
        """
        return self._make_request("marketSummery")
    
    def get_daily_market_summary(self) -> Dict[str, Any]:
        """
        Get daily market summary with historical data
        
        Returns:
            List containing daily market statistics
        """
        return self._make_request("dailyMarketSummery")
    
    # Index Data APIs
    def get_aspi_data(self) -> Dict[str, Any]:
        """
        Get All Share Price Index (ASPI) data
        
        Returns:
            Dict containing ASPI value and change information
        """
        return self._make_request("aspiData")
    
    def get_snp_data(self) -> Dict[str, Any]:
        """
        Get S&P Sri Lanka 20 Index data
        
        Returns:
            Dict containing S&P index value and change information
        """
        return self._make_request("snpData")
    
    def get_chart_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get chart data for stocks
        Note: May return HTTP 400 for some symbols
        
        Args:
            symbol (str): Stock symbol
        
        Returns:
            Dict containing chart data for the specified symbol
        """
        return self._make_request("chartData", {"symbol": symbol})
    
    def get_all_sectors(self) -> Dict[str, Any]:
        """
        Get all sector data
        
        Returns:
            List containing all sector indices information
        """
        return self._make_request("allSectors")
    
    # Announcement APIs
    def get_new_listings_announcements(self) -> Dict[str, Any]:
        """
        Get new listings and related announcements
        
        Returns:
            Dict containing new listing related announcements
        """
        return self._make_request("getNewListingsRelatedNoticesAnnouncements")
    
    def get_buy_in_board_announcements(self) -> Dict[str, Any]:
        """
        Get buy-in board announcements
        
        Returns:
            Dict containing buy-in board announcements
        """
        return self._make_request("getBuyInBoardAnnouncements")
    
    def get_approved_announcements(self) -> Dict[str, Any]:
        """
        Get approved announcements
        
        Returns:
            Dict containing approved announcements
        """
        return self._make_request("approvedAnnouncement")
    
    def get_covid_announcements(self) -> Dict[str, Any]:
        """
        Get COVID-related announcements
        
        Returns:
            Dict containing COVID-related announcements
        """
        return self._make_request("getCOVIDAnnouncements")
    
    def get_financial_announcements(self) -> Dict[str, Any]:
        """
        Get financial announcements
        
        Returns:
            Dict containing financial announcements
        """
        return self._make_request("getFinancialAnnouncement")
    
    def get_financial_announcements_filtered(self, from_date: str, to_date: str, company_ids: Optional[str] = None) -> Dict[str, Any]:
        """
        Get financial announcements filtered by date range, optionally filtered by company security ID
        
        Args:
            from_date (str): Start date in YYYY-MM-DD format (e.g., '2025-01-01')
            to_date (str): End date in YYYY-MM-DD format (e.g., '2025-08-26')
            company_ids (str, optional): Company security ID (e.g., '642'). If None, fetches for all companies
        
        Returns:
            Dict containing filtered financial announcements
        """
        form_data = {
            'fromDate': from_date,
            'toDate': to_date
        }
        
        # Only add company_ids to form data if it's provided
        if company_ids is not None:
            form_data['companyIds'] = company_ids
        
        return self._make_request("getFinancialAnnouncement", data=form_data)
    
    def get_circular_announcements(self) -> Dict[str, Any]:
        """
        Get circular announcements
        
        Returns:
            Dict containing circular announcements
        """
        return self._make_request("circularAnnouncement")
    
    def get_directive_announcements(self) -> Dict[str, Any]:
        """
        Get directive announcements
        
        Returns:
            Dict containing directive announcements
        """
        return self._make_request("directiveAnnouncement")
    
    def get_non_compliance_announcements(self) -> Dict[str, Any]:
        """
        Get non-compliance announcements
        
        Returns:
            Dict containing non-compliance announcements
        """
        return self._make_request("getNonComplianceAnnouncements")


def demo_api_calls():
    """Demonstrate usage of various CSE API endpoints"""
    cse = CSE_API()
    
    print("=== CSE API Demo ===\n")
    
    # 1. Get company information
    print("1. Company Information (LOLC):")
    company_info = cse.get_company_info("LOLC.N0000")
    if company_info['success']:
        data = company_info['data']
        if 'reqSymbolInfo' in data:
            print(f"   Company: {data['reqSymbolInfo'].get('name', 'N/A')}")
            print(f"   Symbol: {data['reqSymbolInfo'].get('symbol', 'N/A')}")
    else:
        print(f"   Error: {company_info['error']}")
    print()
    
    # 2. Market status
    print("2. Market Status:")
    market_status = cse.get_market_status()
    if market_status['success']:
        print(f"   Status: {market_status['data'].get('status', 'N/A')}")
    else:
        print(f"   Error: {market_status['error']}")
    print()
    
    # 3. Top gainers
    print("3. Top Gainers (first 3):")
    gainers = cse.get_top_gainers()
    if gainers['success'] and isinstance(gainers['data'], list):
        for i, stock in enumerate(gainers['data'][:3]):
            print(f"   {i+1}. {stock.get('symbol', 'N/A')}: +{stock.get('changePercentage', 0):.2f}%")
    else:
        print(f"   Error: {gainers.get('error', 'No data')}")
    print()
    
    # 4. Market summary
    print("4. Market Summary:")
    summary = cse.get_market_summary()
    if summary['success']:
        data = summary['data']
        print(f"   Trade Volume: {data.get('tradeVolume', 0):,.0f}")
        print(f"   Share Volume: {data.get('shareVolume', 0):,.0f}")
    else:
        print(f"   Error: {summary['error']}")
    print()
    
    # 5. ASPI Data
    print("5. ASPI Index:")
    aspi = cse.get_aspi_data()
    if aspi['success']:
        data = aspi['data']
        print(f"   Value: {data.get('value', 0):,.2f}")
        print(f"   Change: {data.get('change', 0):+.2f}")
    else:
        print(f"   Error: {aspi['error']}")
    print()
    
    # 6. Companies by alphabet (sample)
    print("6. Companies Starting with 'A' (sample):")
    companies_a = cse.get_companies_by_alphabet("A")
    if companies_a['success']:
        data = companies_a['data']
        companies = []
        
        # Handle the reqAlphabetical response structure
        if isinstance(data, dict) and 'reqAlphabetical' in data:
            companies = data['reqAlphabetical']
        elif isinstance(data, list):
            companies = data
        
        if companies:
            print(f"   Found {len(companies)} companies starting with 'A'")
            for i, company in enumerate(companies[:3]):
                if isinstance(company, dict):
                    name = company.get('name', 'N/A')
                    symbol = company.get('symbol', 'N/A')
                    price = company.get('price', 'N/A')
                    print(f"   {i+1}. {name} ({symbol}) - Price: {price}")
        else:
            print("   No companies found starting with 'A'")
    else:
        print(f"   Error: {companies_a['error']}")


def get_all_companies_demo():
    """Demo function specifically for getting all companies"""
    cse = CSE_API()
    
    print("=== Getting All Registered Companies ===\n")
    print("This will fetch companies from A-Z. This may take a few minutes...\n")
    
    # Get all companies
    result = cse.get_all_companies()
    
    if result['success']:
        print(f"\n✅ Successfully retrieved {result['total_companies']} companies!")
        
        if result['failed_requests']:
            print(f"⚠️  Some requests failed for letters: {[req['letter'] for req in result['failed_requests']]}")
        
        # Show sample companies
        print(f"\n📊 Sample companies (first 10):")
        for i, company in enumerate(result['data'][:10]):
            if isinstance(company, dict):
                name = company.get('name', company.get('companyName', 'N/A'))
                symbol = company.get('symbol', company.get('stockSymbol', 'N/A'))
                print(f"   {i+1}. {name} ({symbol})")
        
        if len(result['data']) > 10:
            print(f"   ... and {len(result['data']) - 10} more companies")
            
        return result['data']
    else:
        print(f"❌ Failed to get companies: {result.get('error', 'Unknown error')}")
        return None


if __name__ == "__main__":
    print("CSE API Client")
    print("==============")
    print("1. Run basic API demo")
    print("2. Get all registered companies (A-Z)")
    print("3. Get companies by specific alphabet")
    
    choice = input("\nEnter your choice (1-3) or press Enter for demo: ").strip()
    
    if choice == "2":
        get_all_companies_demo()
    elif choice == "3":
        letter = input("Enter alphabet (A-Z): ").strip().upper()
        if letter and len(letter) == 1 and letter.isalpha():
            cse = CSE_API()
            result = cse.get_companies_by_alphabet(letter)
            if result['success']:
                data = result['data']
                companies = []
                
                # Handle the reqAlphabetical response structure
                if isinstance(data, dict) and 'reqAlphabetical' in data:
                    companies = data['reqAlphabetical']
                elif isinstance(data, list):
                    companies = data
                
                if companies:
                    print(f"\n✅ Found {len(companies)} companies starting with '{letter}':")
                    for i, company in enumerate(companies[:10]):
                        if isinstance(company, dict):
                            name = company.get('name', 'N/A')
                            symbol = company.get('symbol', 'N/A')
                            price = company.get('price', 'N/A')
                            print(f"   {i+1}. {name} ({symbol}) - Price: {price}")
                    if len(companies) > 10:
                        print(f"   ... and {len(companies) - 10} more")
                else:
                    print(f"No companies found starting with '{letter}'")
            else:
                print(f"❌ Error: {result['error']}")
        else:
            print("Invalid alphabet. Please enter a single letter A-Z.")
    else:
        demo_api_calls()