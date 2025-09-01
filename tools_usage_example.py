"""
Example Usage of CSE Tools Package

This file demonstrates how to use the tools after moving them to the tools/ package.
"""

# Import from the tools package
from tools.company_analyzer import CSE_InvestmentAnalyzer
from tools.download_financial_reports import CSE_ReportDownloader
from tools.enhanced_analyzer import EnhancedInvestmentAnalyzer
from tools.dividend_tracker import DividendTracker
from tools.fetch_categories import fetch_and_store_categories
from tools.get_all_companies import main as get_all_companies

# Alternative: Import everything at once
# from tools import CSE_InvestmentAnalyzer, CSE_ReportDownloader, EnhancedInvestmentAnalyzer, DividendTracker

def example_usage():
    """Demonstrate basic usage of the tools"""
    
    print("🚀 CSE Tools Package Examples")
    print("=" * 50)
    
    # Example 1: Initialize Company Analyzer
    print("\n1. Company Analyzer:")
    analyzer = CSE_InvestmentAnalyzer()
    print(f"   ✅ Loaded {len(analyzer.company_data)} companies")
    
    # Example 2: Initialize Report Downloader
    print("\n2. Report Downloader:")
    downloader = CSE_ReportDownloader()
    print("   ✅ Report downloader initialized")
    
    # Example 3: Initialize Enhanced Analyzer
    print("\n3. Enhanced Analyzer:")
    enhanced = EnhancedInvestmentAnalyzer()
    print(f"   ✅ Enhanced analyzer initialized with {len(enhanced.company_data)} companies")
    
    # Example 4: Initialize Dividend Tracker
    print("\n4. Dividend Tracker:")
    dividend_tracker = DividendTracker()
    print("   ✅ Dividend tracker initialized")
    
    print("\n✅ All tools imported and initialized successfully!")
    print("\n📝 Usage Notes:")
    print("   - All tools maintain their original functionality")
    print("   - File paths are automatically adjusted for the new structure") 
    print("   - Import using: from tools.<module> import <class>")
    print("   - Or import all: from tools import <class1>, <class2>, ...")

if __name__ == "__main__":
    example_usage()
