"""
Test the company name search functionality
"""
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.download_financial_reports import CSE_ReportDownloader

def test_company_search():
    """Test searching by company name"""
    downloader = CSE_ReportDownloader()
    
    # Test with LOLC
    company_search = "LOLC"
    from_date = "2024-06-01"
    to_date = "2025-08-26"
    
    print("🧪 Testing download by company name search")
    print(f"Company search: {company_search}")
    print(f"Date range: {from_date} to {to_date}")
    print("-" * 50)
    
    # This should find LOLC FINANCE PLC and download its reports
    results = downloader.download_reports_by_company_name(company_search, from_date, to_date)
    
    print(f"\n✅ Test completed!")
    print(f"Found {len(results)} announcements")
    if results:
        successful = [r for r in results if r.get('success', False)]
        print(f"Successfully downloaded {len(successful)} files")

if __name__ == "__main__":
    test_company_search()
