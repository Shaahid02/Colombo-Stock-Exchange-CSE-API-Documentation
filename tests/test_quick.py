"""
Quick test for a specific company's financial reports
"""
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_financial_reports import CSE_ReportDownloader

def quick_test():
    """Quick test with ABANS ELECTRICALS PLC"""
    downloader = CSE_ReportDownloader()
    
    # Test with ABANS ELECTRICALS PLC (Security ID: 642)
    # Using a recent date range
    security_id = 642
    from_date = "2024-01-01"  # Using 2024 as it might have more data
    to_date = "2025-08-26"
    
    print("🧪 Quick test for ABANS ELECTRICALS PLC")
    print(f"Security ID: {security_id}")
    print(f"Date range: {from_date} to {to_date}")
    print("-" * 50)
    
    results = downloader.download_reports_by_security_id(security_id, from_date, to_date)
    
    print(f"\n✅ Test completed!")
    print(f"Found {len(results)} announcements")
    if results:
        successful = [r for r in results if r.get('success', False)]
        print(f"Successfully downloaded {len(successful)} files")

if __name__ == "__main__":
    quick_test()
