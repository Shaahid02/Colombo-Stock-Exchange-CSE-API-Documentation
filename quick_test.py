"""
Quick Test Script for CSE API
Tests basic functionality of key endpoints
"""

from app import CSE_API

def quick_test():
    """Quick test of CSE API functionality"""
    cse = CSE_API()
    
    print("🧪 Quick CSE API Test")
    print("="*30)
    
    # Test 1: Market Status (should always work)
    print("\n1. Testing Market Status...")
    status = cse.get_market_status()
    if status['success']:
        print(f"   ✅ Success: {status['data']}")
    else:
        print(f"   ❌ Failed: {status['error']}")
    
    # Test 2: Company Info
    print("\n2. Testing Company Info (LOLC)...")
    company = cse.get_company_info("LOLC.N0000")
    if company['success']:
        if 'reqSymbolInfo' in company['data']:
            name = company['data']['reqSymbolInfo'].get('name', 'Unknown')
            print(f"   ✅ Success: {name}")
        else:
            print(f"   ✅ Response received but no symbol info")
    else:
        print(f"   ❌ Failed: {company['error']}")
    
    # Test 3: Market Summary
    print("\n3. Testing Market Summary...")
    summary = cse.get_market_summary()
    if summary['success']:
        trade_vol = summary['data'].get('tradeVolume', 0)
        print(f"   ✅ Success: Trade Volume = {trade_vol:,.0f}")
    else:
        print(f"   ❌ Failed: {summary['error']}")
    
    # Test 4: ASPI Data
    print("\n4. Testing ASPI Data...")
    aspi = cse.get_aspi_data()
    if aspi['success']:
        value = aspi['data'].get('value', 0)
        change = aspi['data'].get('change', 0)
        print(f"   ✅ Success: ASPI = {value:,.2f} ({change:+.2f})")
    else:
        print(f"   ❌ Failed: {aspi['error']}")
    
    print("\n🎉 Quick test complete!")

if __name__ == "__main__":
    quick_test()
