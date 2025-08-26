"""
Get All Registered Companies from CSE API
This script fetches all registered companies by iterating through alphabets A-Z
"""

from app import CSE_API
import json
import csv
from datetime import datetime

def save_companies_to_files(companies_data):
    """Save companies data to JSON and CSV files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save to JSON
    json_filename = f"cse_all_companies_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(companies_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to JSON: {json_filename}")
    
    # Save to CSV
    csv_filename = f"cse_all_companies_{timestamp}.csv"
    if companies_data:
        # Get all possible keys from all companies
        all_keys = set()
        for company in companies_data:
            if isinstance(company, dict):
                all_keys.update(company.keys())
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(all_keys))
            writer.writeheader()
            for company in companies_data:
                if isinstance(company, dict):
                    writer.writerow(company)
        print(f"💾 Saved to CSV: {csv_filename}")
    
    return json_filename, csv_filename

def analyze_companies_data(companies_data):
    """Analyze the companies data and show statistics"""
    if not companies_data:
        print("❌ No companies data to analyze")
        return
    
    print(f"\n📊 COMPANIES DATA ANALYSIS")
    print(f"="*40)
    print(f"Total Companies: {len(companies_data)}")
    
    # Count by first letter
    letter_count = {}
    sectors = set()
    
    for company in companies_data:
        if isinstance(company, dict):
            # Count by first letter of company name
            name = company.get('name', company.get('companyName', ''))
            if name:
                first_letter = name[0].upper()
                letter_count[first_letter] = letter_count.get(first_letter, 0) + 1
            
            # Collect sectors if available
            sector = company.get('sector', company.get('sectorName', ''))
            if sector:
                sectors.add(sector)
    
    # Show distribution by alphabet
    print(f"\n📈 Companies by First Letter:")
    for letter in sorted(letter_count.keys()):
        print(f"   {letter}: {letter_count[letter]} companies")
    
    # Show sectors if available
    if sectors:
        print(f"\n🏢 Sectors Found: {len(sectors)}")
        for sector in sorted(sectors)[:10]:  # Show first 10 sectors
            print(f"   - {sector}")
        if len(sectors) > 10:
            print(f"   ... and {len(sectors) - 10} more sectors")
    
    # Sample companies
    print(f"\n📝 Sample Companies (first 15):")
    for i, company in enumerate(companies_data[:15]):
        if isinstance(company, dict):
            name = company.get('name', 'N/A')
            symbol = company.get('symbol', 'N/A')
            price = company.get('price', 0)
            change_pct = company.get('percentageChange', 0)
            print(f"   {i+1:2d}. {name} ({symbol}) - ${price} ({change_pct:+.2f}%)")

def main():
    """Main function to get all companies and save them"""
    print("🏢 CSE All Companies Fetcher")
    print("="*40)
    print("This will fetch ALL registered companies from the CSE API")
    print("The process may take 2-3 minutes as it queries A-Z alphabetically")
    
    proceed = input("\nProceed? (y/N): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    # Initialize API client
    cse = CSE_API()
    
    # Get all companies
    print(f"\n🚀 Starting to fetch companies...")
    result = cse.get_all_companies()
    
    if not result['success']:
        print(f"❌ Failed to get companies: {result.get('error', 'Unknown error')}")
        return
    
    companies_data = result['data']
    print(f"\n✅ Successfully retrieved {len(companies_data)} companies!")
    
    if result['failed_requests']:
        print(f"⚠️  Note: Some requests failed for letters: {[req['letter'] for req in result['failed_requests']]}")
    
    # Analyze the data
    analyze_companies_data(companies_data)
    
    # Ask if user wants to save to files
    save_files = input(f"\n💾 Save {len(companies_data)} companies to JSON/CSV files? (Y/n): ").strip().lower()
    if save_files not in ['n', 'no']:
        json_file, csv_file = save_companies_to_files(companies_data)
        print(f"\n✅ Files saved successfully!")
        print(f"   📄 JSON: {json_file}")
        print(f"   📊 CSV:  {csv_file}")
    
    return companies_data

def test_single_alphabet():
    """Test getting companies for a single alphabet"""
    cse = CSE_API()
    
    letter = input("Enter alphabet to test (A-Z): ").strip().upper()
    if not letter or len(letter) != 1 or not letter.isalpha():
        print("Invalid input. Please enter a single letter A-Z.")
        return
    
    print(f"\n🧪 Testing companies for letter '{letter}'...")
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
            print(f"✅ Found {len(companies)} companies starting with '{letter}'")
            
            print(f"\n📝 Companies starting with '{letter}':")
            for i, company in enumerate(companies):
                if isinstance(company, dict):
                    name = company.get('name', 'N/A')
                    symbol = company.get('symbol', 'N/A')
                    price = company.get('price', 0)
                    change_pct = company.get('percentageChange', 0)
                    print(f"   {i+1:2d}. {name} ({symbol}) - ${price} ({change_pct:+.2f}%)")
            
            # Show raw data structure for first company
            print(f"\n🔍 Sample company data structure:")
            print(json.dumps(companies[0], indent=2))
        else:
            print(f"No companies found starting with '{letter}'")
    else:
        print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    print("CSE Companies Fetcher")
    print("="*25)
    print("1. Get ALL companies (A-Z)")
    print("2. Test single alphabet")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "2":
        test_single_alphabet()
    else:
        main()
