"""
Test the get_all_companies function with just first 5 letters
"""
import os
from app import CSE_API
import json

def test_get_companies_subset():
    """Test getting companies for first 5 letters (A-E)"""
    cse = CSE_API()
    
    print("🧪 Testing get_all_companies with first 5 letters (A-E)")
    print("="*60)
    
    import string
    all_companies = []
    failed_requests = []
    
    for letter in list(string.ascii_uppercase)[:26]:  #  26 letters A-Z
        print(f"Fetching companies starting with '{letter}'...")
        response = cse.get_companies_by_alphabet(letter)
        
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
                print(f"  ✅ Found {len(companies)} companies starting with '{letter}'")
            else:
                print(f"  No companies found for '{letter}'")
        else:
            failed_requests.append({
                'letter': letter,
                'error': response['error']
            })
            print(f"  ❌ Failed to fetch companies for '{letter}': {response['error']}")
    
    print(f"\n🎉 Total companies found (A-E): {len(all_companies)}")
    
    if all_companies:
        print(f"\n📊 Sample companies (first 20):")
        for i, company in enumerate(all_companies[:20]):
            if isinstance(company, dict):
                name = company.get('name', 'N/A')
                symbol = company.get('symbol', 'N/A')
                price = company.get('price', 0)
                change_pct = company.get('percentageChange', 0)
                print(f"   {i+1:2d}. {name[:40]:<40} ({symbol}) - ${price:>6} ({change_pct:+5.2f}%)")
        
        # Show statistics
        active_companies = [c for c in all_companies if c.get('price', 0) > 0]
        print(f"\n📈 Statistics:")
        print(f"   Total companies: {len(all_companies)}")
        print(f"   Active companies (price > 0): {len(active_companies)}")
        print(f"   Inactive companies: {len(all_companies) - len(active_companies)}")
        
        if active_companies:
            prices = [c['price'] for c in active_companies if isinstance(c.get('price'), (int, float)) and c['price'] > 0]
            if prices:
                avg_price = sum(prices) / len(prices)
                max_price = max(prices)
                min_price = min(prices)
                print(f"   Average price: ${avg_price:.2f}")
                print(f"   Highest price: ${max_price:.2f}")
                print(f"   Lowest price: ${min_price:.2f}")

    return [all_companies, active_companies]

if __name__ == "__main__":
    companies = test_get_companies_subset()
    all_companies, active_companies = companies
    if active_companies:
        # Ask if user wants to save to file
        print(f"\n💾 Save {len(active_companies)} active companies to JSON file? (y/n): ", end="")
        try:
            save = input().strip().lower()
            if save in ['y', 'yes']:
                os.makedirs("training_data", exist_ok=True)
                filename = "training_data/cse_companies_A_to_E.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(active_companies, f, indent=2, ensure_ascii=False)
                print(f"✅ Active companies saved to: {filename}")
        except:
            print("\nSkipping file save.")
    
    print("\n🎉 Test completed!")
