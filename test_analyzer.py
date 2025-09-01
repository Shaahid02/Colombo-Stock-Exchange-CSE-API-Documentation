"""
Quick test of the investment analyzer
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from company_analyzer import CSE_InvestmentAnalyzer

def quick_test():
    """Test the analyzer with a few companies"""
    print("🧪 Quick test of CSE Investment Analyzer")
    print("="*50)
    
    analyzer = CSE_InvestmentAnalyzer()
    
    if not analyzer.company_data:
        print("❌ No company data available")
        return
    
    print(f"📊 Found {len(analyzer.company_data)} companies")
    
    # Test with first 3 companies
    print("\nTesting with first 3 companies...")
    analyzer.analyze_companies(limit=3, delay=0.5)
    
    if analyzer.analysis_results:
        print(f"\n✅ Successfully analyzed {len(analyzer.analysis_results)} companies")
        
        # Show sample data
        for i, company in enumerate(analyzer.analysis_results[:2], 1):
            print(f"\n{i}. {company.get('symbol')} - {company.get('name')}")
            print(f"   Price: LKR {company.get('last_traded_price', 0)}")
            print(f"   Change: {company.get('change_percentage', 0):+.2f}%")
            print(f"   Market Cap: LKR {company.get('market_cap', 0):,.0f}")
            print(f"   Risk Category: {company.get('risk_category', 'N/A')}")
            
        # Test analysis generation
        print(f"\n📈 Generating investment analysis...")
        analysis = analyzer.generate_investment_analysis()
        
        summary = analysis.get('summary', {})
        print(f"   Total companies: {summary.get('total_companies', 0)}")
        print(f"   Active companies: {summary.get('active_companies', 0)}")
        
        market = analysis.get('market_overview', {})
        if market:
            print(f"   Average price: LKR {market.get('price_ranges', {}).get('average_price', 0):,.2f}")
    else:
        print("❌ No data analyzed")

if __name__ == "__main__":
    quick_test()
