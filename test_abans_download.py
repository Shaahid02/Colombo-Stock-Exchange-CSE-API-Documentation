"""
Test download_financial_reports tool for Abans Electrical
Date range: 2024-01-01 to 2025-08-26
"""

from tools.download_financial_reports import CSE_ReportDownloader
from datetime import datetime

def test_abans_financial_reports():
    """Test downloading financial reports for Abans Electrical"""
    
    print("🔍 Testing Financial Reports Download for Abans Electrical")
    print("=" * 60)
    
    # Initialize the downloader
    downloader = CSE_ReportDownloader()
    
    # Test date range
    start_date = "2024-01-01"
    end_date = "2025-08-26"
    
    print(f"\n📅 Date range: {start_date} to {end_date}")
    
    # Search for Abans Electrical company data
    print("\n📊 Searching for Abans Electrical company data...")
    
    try:
        # First, let's find the security ID for Abans Electrical
        security_id = downloader.find_security_id("ABANS ELECTRICALS")
        
        if security_id:
            print(f"✅ Found security ID: {security_id}")
            
            # Get company info
            company_info = downloader.get_company_info(security_id)
            if company_info:
                print(f"🏢 Company: {company_info.get('name', 'N/A')}")
                print(f"📈 Symbol: {company_info.get('symbol', 'N/A')}")
            
            # Create download folder
            download_folder = downloader.create_download_folder("abans_electrical_reports")
            print(f"📁 Download folder: {download_folder}")
            
            # Download reports using the security ID method
            print(f"\n📥 Downloading financial reports for security ID: {security_id}")
            print("⏳ This may take a few minutes...")
            
            download_count = downloader.download_reports_by_security_id(
                security_id=security_id,
                from_date=start_date,
                to_date=end_date
            )
            
            print(f"✅ Download completed! {download_count} reports processed")
            
        else:
            # Try alternative approach with company name
            print("� Security ID not found, trying with company name...")
            
            download_count = downloader.download_reports_by_company_name(
                company_name_or_symbol="ABANS ELECTRICALS",
                from_date=start_date,
                to_date=end_date
            )
            
            print(f"✅ Download completed! {download_count} reports processed")
            
    except Exception as e:
        print(f"❌ Error during download test: {e}")
        print(f"� Error details: {type(e).__name__}")
        
        # Try a more basic test
        print("\n🔄 Trying basic functionality test...")
        try:
            # Test if we can at least load company data
            company_data = downloader.load_company_data()
            print(f"✅ Company data loaded: {len(company_data) if company_data else 0} companies")
            
            # Look for Abans companies manually
            abans_companies = []
            if company_data:
                for company in company_data:
                    name = company.get('name', '').upper()
                    symbol = company.get('symbol', '').upper()
                    if 'ABANS' in name or 'ABAN' in symbol:
                        abans_companies.append(company)
                        
                if abans_companies:
                    print(f"✅ Found {len(abans_companies)} Abans companies in data:")
                    for company in abans_companies:
                        print(f"   📈 {company.get('symbol', 'N/A')} - {company.get('name', 'N/A')}")
                else:
                    print("⚠️ No Abans companies found in loaded data")
                    
        except Exception as inner_e:
            print(f"❌ Basic test also failed: {inner_e}")

if __name__ == "__main__":
    test_abans_financial_reports()
