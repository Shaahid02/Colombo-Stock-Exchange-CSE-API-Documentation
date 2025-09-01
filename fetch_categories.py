"""
Script to fetch and store CSE announcement categories
"""
import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import CSE_API

def fetch_and_store_categories():
    """Fetch announcement categories and store them in JSON file"""
    print("📋 Fetching CSE Announcement Categories...")
    
    cse = CSE_API()
    result = cse.get_corporate_announcement_categories()
    
    if result['success']:
        categories = result['data']
        print(f"✅ Successfully fetched {len(categories)} categories")
        
        # Prepare data for storage
        categories_data = {
            "metadata": {
                "fetch_date": datetime.now().isoformat(),
                "total_categories": len(categories),
                "source": "CSE API - corporateAnnouncementCategory"
            },
            "categories": categories
        }
        
        # Create company_data directory if it doesn't exist
        data_dir = "company_data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Save to JSON file
        file_path = os.path.join(data_dir, "announcement_categories.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(categories_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved categories to: {file_path}")
        
        # Show summary of categories by type
        print("\n📊 Category Summary:")
        
        # Group categories by common keywords
        dividend_cats = [cat for cat in categories if 'DIVIDEND' in cat.get('categoryName', '').upper()]
        meeting_cats = [cat for cat in categories if 'MEETING' in cat.get('categoryName', '').upper()]
        financial_cats = [cat for cat in categories if any(word in cat.get('categoryName', '').upper() 
                          for word in ['FINANCIAL', 'INTERIM', 'ANNUAL'])]
        appointment_cats = [cat for cat in categories if 'APPOINTMENT' in cat.get('categoryName', '').upper()]
        
        print(f"   💰 Dividend-related: {len(dividend_cats)} categories")
        print(f"   🏢 Meeting-related: {len(meeting_cats)} categories")
        print(f"   📈 Financial-related: {len(financial_cats)} categories")
        print(f"   👥 Appointment-related: {len(appointment_cats)} categories")
        
        # Show all dividend categories
        if dividend_cats:
            print(f"\n💰 Dividend Categories:")
            for cat in dividend_cats:
                print(f"   - {cat.get('categoryName')} (ID: {cat.get('id')})")
        
        return categories_data
    else:
        print(f"❌ Failed to fetch categories: {result.get('error')}")
        return None

if __name__ == "__main__":
    fetch_and_store_categories()
