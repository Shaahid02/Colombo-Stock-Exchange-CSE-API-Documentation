"""
Test script for the new CSE API endpoints:
- Corporate Announcement Categories
- Approved Announcements  
- Announcement Details by ID
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import CSE_API

def test_new_endpoints():
    """Test the three new API endpoints"""
    print("🧪 Testing New CSE API Endpoints")
    print("="*50)
    
    cse = CSE_API()
    
    # 1. Test Corporate Announcement Categories
    print("\n1️⃣  Testing Corporate Announcement Categories...")
    categories_result = cse.get_corporate_announcement_categories()
    
    if categories_result['success']:
        categories = categories_result['data']
        print(f"✅ Found {len(categories)} announcement categories")
        
        # Show first 5 categories
        print("\n📋 First 5 categories:")
        for i, category in enumerate(categories[:5], 1):
            print(f"   {i}. {category.get('categoryName')} (ID: {category.get('id')})")
            
        # Find dividend-related categories
        dividend_categories = [cat for cat in categories 
                             if 'DIVIDEND' in cat.get('categoryName', '').upper()]
        print(f"\n💰 Found {len(dividend_categories)} dividend-related categories:")
        for cat in dividend_categories:
            print(f"   - {cat.get('categoryName')} (ID: {cat.get('id')})")
    else:
        print(f"❌ Failed: {categories_result.get('error')}")
    
    # 2. Test Approved Announcements
    print("\n\n2️⃣  Testing Approved Announcements...")
    
    # Use recent date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"📅 Searching from {start_date} to {end_date}")
    
    announcements_result = cse.get_approved_announcements(
        announcement_type="CASH DIVIDEND",
        from_date=start_date,
        to_date=end_date,
        announcement_categories="CASH DIVIDEND"
    )
    
    if announcements_result['success']:
        data = announcements_result['data']
        
        if isinstance(data, dict) and 'approvedAnnouncements' in data:
            announcements = data['approvedAnnouncements']
            print(f"✅ Found {len(announcements)} cash dividend announcements")
            
            if announcements:
                print("\n💵 Recent cash dividend announcements:")
                for i, announcement in enumerate(announcements[:5], 1):
                    company = announcement.get('company', 'N/A')
                    date = announcement.get('dateOfAnnouncement', 'N/A')
                    ann_id = announcement.get('announcementId', 'N/A')
                    print(f"   {i}. {company} - {date} (ID: {ann_id})")
                    
                # Test announcement details for first announcement
                if announcements:
                    first_announcement_id = announcements[0].get('announcementId')
                    if first_announcement_id:
                        print(f"\n\n3️⃣  Testing Announcement Details (ID: {first_announcement_id})...")
                        details_result = cse.get_announcement_by_id(first_announcement_id)
                        
                        if details_result['success']:
                            details = details_result['data']
                            
                            if 'reqBaseAnnouncement' in details:
                                base_info = details['reqBaseAnnouncement']
                                print(f"✅ Got detailed announcement info:")
                                print(f"   Company: {base_info.get('companyName', 'N/A')}")
                                print(f"   Symbol: {base_info.get('symbol', 'N/A')}")
                                print(f"   Dividend per Share: LKR {base_info.get('votingDivPerShare', 0)}")
                                print(f"   Financial Year: {base_info.get('financialYear', 'N/A')}")
                                print(f"   Ex-Dividend Date: {base_info.get('xd', 'N/A')}")
                                print(f"   Payment Date: {base_info.get('payment', 'N/A')}")
                                print(f"   AGM Date: {base_info.get('agm', 'N/A')}")
                                
                                # Show documents if any
                                if 'reqAnnouncementDocs' in details:
                                    docs = details['reqAnnouncementDocs']
                                    print(f"\n📄 {len(docs)} document(s) attached:")
                                    for doc in docs:
                                        filename = doc.get('fileOriginalName', 'N/A')
                                        size_kb = doc.get('fileSize', 0) / 1024
                                        print(f"   - {filename} ({size_kb:.1f} KB)")
                            else:
                                print("📋 Raw announcement details:", details)
                        else:
                            print(f"❌ Failed to get announcement details: {details_result.get('error')}")
            else:
                print("📭 No cash dividend announcements found in the date range")
        else:
            print("📋 Raw announcements data:", data)
    else:
        print(f"❌ Failed: {announcements_result.get('error')}")
    
    print("\n🎉 New API endpoints testing completed!")

def show_usage_examples():
    """Show how to use the new endpoints"""
    print("\n" + "="*60)
    print("📚 USAGE EXAMPLES")
    print("="*60)
    
    print("""
🔹 Corporate Announcement Categories:
   categories = cse.get_corporate_announcement_categories()
   
🔹 Approved Announcements:
   announcements = cse.get_approved_announcements(
       announcement_type="CASH DIVIDEND",
       from_date="2025-08-01", 
       to_date="2025-08-31",
       announcement_categories="CASH DIVIDEND"
   )
   
🔹 Announcement Details:
   details = cse.get_announcement_by_id(32886)
   
💡 Common announcement types:
   - CASH DIVIDEND
   - BONUS ISSUE
   - RIGHTS ISSUE
   - ANNUAL GENERAL MEETING
   - INTERIM FINANCIAL STATEMENTS
    """)

if __name__ == "__main__":
    test_new_endpoints()
    show_usage_examples()
