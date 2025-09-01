"""
Summary of CSE Investment Tools Created
Shows overview of available tools and recent analysis results
"""
import json
import os
from datetime import datetime

def show_tools_summary():
    """Display summary of all available CSE investment tools"""
    print("🎯 CSE Investment Tools - Complete Overview")
    print("="*60)
    
    tools = [
        {
            "name": "📊 Enhanced Investment Analyzer",
            "file": "enhanced_analyzer.py",
            "description": "Combines company analysis with dividend tracking for comprehensive investment insights"
        },
        {
            "name": "💰 Dividend Tracker", 
            "file": "dividend_tracker.py",
            "description": "Dedicated tool for tracking dividend announcements, payments, and calendar"
        },
        {
            "name": "🏢 Company Analyzer",
            "file": "company_analyzer.py", 
            "description": "Original investment analyzer with risk assessment and market metrics"
        },
        {
            "name": "📥 Download Manager",
            "file": "download_financial_reports.py",
            "description": "Downloads financial reports with flexible filtering options"
        },
        {
            "name": "🔧 CSE API Client",
            "file": "app.py",
            "description": "Complete API client with all CSE endpoints including new announcement APIs"
        }
    ]
    
    print("📱 AVAILABLE TOOLS:")
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool['name']}")
        print(f"   📂 File: {tool['file']}")
        print(f"   📝 {tool['description']}")
    
    # Show new API endpoints
    print(f"\n🆕 NEW API ENDPOINTS ADDED:")
    endpoints = [
        "🏢 Corporate Announcement Categories - Get all announcement types",
        "📋 Approved Announcements - Search announcements by type and date",
        "🔍 Announcement Details - Get detailed dividend/AGM information"
    ]
    
    for endpoint in endpoints:
        print(f"   {endpoint}")

def show_recent_analysis():
    """Show summary of recent analysis results"""
    print(f"\n📈 RECENT ANALYSIS RESULTS")
    print("="*40)
    
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        print("❌ No reports directory found")
        return
    
    # Find recent reports
    json_files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
    recent_files = sorted(json_files, reverse=True)[:3]
    
    for i, filename in enumerate(recent_files, 1):
        file_path = os.path.join(reports_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'dividend_tracking' in filename:
                print(f"\n{i}. 💰 Dividend Report: {filename}")
                metadata = data.get('report_metadata', {})
                trends = data.get('dividend_trends', {})
                stats = trends.get('dividend_statistics', {})
                
                print(f"   📅 Generated: {metadata.get('generated_at', 'N/A')[:16]}")
                print(f"   💵 Total dividends: {stats.get('total_dividends_analyzed', 0)}")
                print(f"   💰 Avg dividend: LKR {stats.get('average_dividend', 0):.2f}")
                print(f"   🏆 Highest: LKR {stats.get('max_dividend', 0):.2f}")
                
            elif 'enhanced_investment' in filename:
                print(f"\n{i}. 📊 Enhanced Investment Report: {filename}")
                metadata = data.get('analysis_metadata', {})
                dividend_report = data.get('dividend_report', {})
                summary = dividend_report.get('summary', {})
                
                print(f"   📅 Generated: {metadata.get('generated_at', 'N/A')[:16]}")
                print(f"   🏢 Companies analyzed: {summary.get('total_companies_analyzed', 0)}")
                print(f"   💰 With dividends: {summary.get('companies_with_dividends', 0)}")
                print(f"   📊 Dividend %: {summary.get('dividend_percentage', 0):.1f}%")
            
            else:
                print(f"\n{i}. 📄 Report: {filename}")
                
        except Exception as e:
            print(f"\n{i}. ❌ Error reading {filename}: {e}")

def show_data_files():
    """Show available data files"""
    print(f"\n📂 DATA FILES")
    print("="*25)
    
    company_data_dir = "company_data"
    if os.path.exists(company_data_dir):
        files = os.listdir(company_data_dir)
        for file in files:
            file_path = os.path.join(company_data_dir, file)
            if file.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if file == 'announcement_categories.json':
                        categories_count = len(data.get('categories', []))
                        print(f"📋 {file} - {categories_count} announcement categories")
                    elif file == 'data.json':
                        companies_count = len(data) if isinstance(data, list) else 'Unknown'
                        print(f"🏢 {file} - {companies_count} companies")
                    else:
                        print(f"📄 {file}")
                except:
                    print(f"📄 {file} (could not read)")
    else:
        print("❌ No company_data directory found")

def show_usage_guide():
    """Show quick usage guide"""
    print(f"\n🚀 QUICK USAGE GUIDE")
    print("="*30)
    print("""
💡 For Investment Analysis:
   python enhanced_analyzer.py     # Complete analysis with dividends
   python company_analyzer.py      # Basic company analysis
   
💰 For Dividend Tracking:
   python dividend_tracker.py      # Track all dividend announcements
   
📥 For Data Downloads:
   python download_financial_reports.py  # Download financial reports
   
🧪 For Testing:
   python test_new_endpoints.py    # Test the new API endpoints
   cd tests && python run_tests.py # Run all unit tests
   
📋 For Data Updates:
   python fetch_categories.py      # Update announcement categories
   python get_all_companies.py     # Update company list
    """)

def main():
    """Main summary display"""
    show_tools_summary()
    show_recent_analysis()
    show_data_files()
    show_usage_guide()
    
    print(f"\n🎉 CSE Investment Suite Ready!")
    print(f"All tools are configured and tested. Happy investing! 📈")

if __name__ == "__main__":
    main()
