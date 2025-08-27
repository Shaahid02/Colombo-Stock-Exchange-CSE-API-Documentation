"""
Test script for the updated download functionality
"""
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_financial_reports import CSE_ReportDownloader

def test_updated_functionality():
    """Test all the updated download functionality"""
    
    print("🧪 Testing Updated CSE Report Downloader")
    print("="*50)
    
    downloader = CSE_ReportDownloader()
    
    # Test 1: Download by date range only (all companies) - limited for testing
    print("\n📅 Test 1: Download by date range only (all companies)")
    print("-" * 60)
    
    from_date = "2025-08-25"
    to_date = "2025-08-26"
    
    print(f"Testing date range download: {from_date} to {to_date}")
    result1 = downloader.download_reports_by_date_range(from_date, to_date)
    print(f"✅ Test 1: Found {len(result1)} reports")
    
    # Test 2: Download by date range with specific security ID
    print(f"\n🎯 Test 2: Download by date range with Security ID")
    print("-" * 60)
    
    security_id = "642"  # ABANS ELECTRICALS PLC
    print(f"Testing filtered download for Security ID {security_id}")
    result2 = downloader.download_reports_by_date_range(from_date, to_date, security_id)
    print(f"✅ Test 2: Found {len(result2)} reports for Security ID {security_id}")
    
    # Test 3: Download by company name
    print(f"\n🏢 Test 3: Download by company name")
    print("-" * 60)
    
    company_name = "ABANS"
    print(f"Testing company name search: {company_name}")
    result3 = downloader.download_reports_by_company_name(company_name, from_date, to_date)
    print(f"✅ Test 3: Found {len(result3)} reports for company {company_name}")
    
    # Test 4: Verify folder structure
    print(f"\n📁 Test 4: Verify folder structure")
    print("-" * 60)
    
    if os.path.exists("reports"):
        print("📂 Current reports folder structure:")
        for root, dirs, files in os.walk("reports"):
            level = root.replace("reports", "").count(os.sep)
            indent = " " * 2 * level
            folder_name = os.path.basename(root) or "reports"
            print(f"{indent}📁 {folder_name}/")
            subindent = " " * 2 * (level + 1)
            pdf_count = sum(1 for f in files if f.endswith('.pdf'))
            json_count = sum(1 for f in files if f.endswith('.json'))
            if pdf_count > 0:
                print(f"{subindent}📄 {pdf_count} PDF files")
            if json_count > 0:
                print(f"{subindent}📋 {json_count} JSON log files")
    else:
        print("❌ Reports folder not found")
    
    # Test 5: Show deprecated method warnings
    print(f"\n⚠️  Test 5: Test deprecated methods")
    print("-" * 60)
    
    print("Testing deprecated download_reports_by_security_id():")
    downloader.download_reports_by_security_id("642", from_date, to_date)
    
    print("\nTesting deprecated download_reports_by_time_range():")
    downloader.download_reports_by_time_range(from_date, to_date)
    
    print(f"\n🎉 All tests completed!")
    print("="*50)
    
    return {
        'date_range_all': len(result1),
        'date_range_filtered': len(result2),
        'company_name': len(result3)
    }

if __name__ == "__main__":
    results = test_updated_functionality()
    print(f"\n📊 Test Results Summary:")
    for test_name, count in results.items():
        print(f"   {test_name}: {count} reports")