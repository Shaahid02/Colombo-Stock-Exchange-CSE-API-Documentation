"""
Test script for filtered financial report downloads
"""
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_financial_reports import CSE_ReportDownloader

def test_security_id_download():
    """Test downloading by security ID and date range"""
    downloader = CSE_ReportDownloader()
    
    # Example: ABANS ELECTRICALS PLC with security ID 642
    security_id = 642
    from_date = "2025-01-01"
    to_date = "2025-08-26"
    
    print("🧪 Testing download by Security ID")
    print(f"Security ID: {security_id}")
    print(f"Date range: {from_date} to {to_date}")
    print("-" * 50)
    
    results = downloader.download_reports_by_security_id(security_id, from_date, to_date)
    
    print(f"\n✅ Test completed. Downloaded {len([r for r in results if r['success']])} files")
    return results

def test_company_name_download():
    """Test downloading by company name/symbol and date range"""
    downloader = CSE_ReportDownloader()
    
    # Example: Search for ABANS
    company_search = "ABANS"
    from_date = "2025-01-01"
    to_date = "2025-08-26"
    
    print("\n🧪 Testing download by Company Name")
    print(f"Company search: {company_search}")
    print(f"Date range: {from_date} to {to_date}")
    print("-" * 50)
    
    results = downloader.download_reports_by_company_name(company_search, from_date, to_date)
    
    print(f"\n✅ Test completed. Downloaded {len([r for r in results if r['success']])} files")
    return results

def test_lookup_functions():
    """Test the security ID lookup functions"""
    downloader = CSE_ReportDownloader()
    
    print("\n🧪 Testing Security ID lookup functions")
    print("-" * 50)
    
    # Test finding security ID
    test_searches = ["ABANS", "LOLC", "CSLK", "ACCESS ENGINEERING"]
    
    for search in test_searches:
        security_id = downloader.find_security_id(search)
        print(f"🔍 '{search}' -> Security ID: {security_id}")
        
        if security_id:
            company_info = downloader.get_company_info(security_id)
            if company_info:
                print(f"    🏢 {company_info['name']} ({company_info['symbol']})")
    
    print("\n📊 Company data loaded:", len(downloader.company_data), "companies")

if __name__ == "__main__":
    print("CSE Filtered Downloads Test")
    print("="*40)
    
    # Test lookup functions first
    test_lookup_functions()
    
    # Test security ID download (comment out if you don't want to download)
    # test_security_id_download()
    
    # Test company name download (comment out if you don't want to download)
    # test_company_name_download()
    
    print("\n🎉 All tests completed!")
