"""
Quick test to verify the updated API integration works correctly
"""
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_financial_reports import CSE_ReportDownloader

def test_updated_api():
    """Test the updated API integration"""
    
    print("🧪 Testing Updated API Integration")
    print("="*50)
    
    downloader = CSE_ReportDownloader()
    
    # Test 1: Date range only (should work with nullable company_ids)
    print("\n📅 Test 1: Date range only (all companies)")
    print("-" * 50)
    
    from_date = "2025-06-26"
    to_date = "2025-08-26"
    
    try:
        print(f"Calling API with dates: {from_date} to {to_date}, no company ID")
        result = downloader.cse_api.get_financial_announcements_filtered(from_date, to_date)
        
        if result['success']:
            announcements = result['data']['reqFinancialAnnouncemnets']
            print(f"✅ Success: Found {len(announcements)} announcements")
        else:
            print(f"❌ Failed: {result['error']}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Date range with specific company ID
    print("\n🎯 Test 2: Date range with company ID")
    print("-" * 50)
    
    company_id = "642"  # ABANS ELECTRICALS PLC
    
    try:
        print(f"Calling API with dates: {from_date} to {to_date}, company ID: {company_id}")
        result = downloader.cse_api.get_financial_announcements_filtered(from_date, to_date, company_id)
        
        if result['success']:
            announcements = result['data']['reqFinancialAnnouncemnets']
            print(f"✅ Success: Found {len(announcements)} announcements for company {company_id}")
            
            # Show company names in results
            if announcements:
                companies = set([ann['name'] for ann in announcements])
                print(f"   Companies in results: {list(companies)}")
        else:
            print(f"❌ Failed: {result['error']}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Full download with date range only
    print("\n📥 Test 3: Download by date range (no company filter)")
    print("-" * 50)
    
    try:
        print("Testing full download functionality...")
        results = downloader.download_reports_by_date_range(from_date, to_date)
        print(f"✅ Download test completed: {len(results)} download attempts")
        
        successful = [r for r in results if r.get('success', False)]
        print(f"   Successful downloads: {len(successful)}")
    except Exception as e:
        print(f"❌ Exception in download test: {e}")
    
    print(f"\n🎉 API integration tests completed!")

if __name__ == "__main__":
    test_updated_api()
