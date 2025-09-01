"""
Enhanced Investment Analyzer with Dividend Tracking
Integrates company analysis with corporate announcements and dividend data
"""
import json
import pandas as pd
import numpy as np
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import CSE_API

class EnhancedInvestmentAnalyzer:
    """
    Enhanced investment analyzer with dividend tracking and corporate announcements
    """
    
    def __init__(self, data_file: str = None):
        self.api = CSE_API()
        if data_file is None:
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_file = os.path.join(parent_dir, "company_data/data.json")
        self.company_data = self._load_company_data(data_file)
        self.announcement_categories = self._load_announcement_categories()
        self.analysis_results = []
        self.dividend_data = []
        
    def _load_company_data(self, data_file: str) -> List[Dict]:
        """Load company data from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Company data file not found: {data_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing company data: {e}")
            return []
    
    def _load_announcement_categories(self) -> Dict:
        """Load announcement categories from JSON file"""
        try:
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            categories_file = os.path.join(parent_dir, "company_data/announcement_categories.json")
            with open(categories_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Announcement categories file not found. Run fetch_categories.py first.")
            return {"categories": []}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing announcement categories: {e}")
            return {"categories": []}
    
    def get_dividend_categories(self) -> List[Dict]:
        """Get all dividend-related announcement categories"""
        categories = self.announcement_categories.get('categories', [])
        return [cat for cat in categories if 'DIVIDEND' in cat.get('categoryName', '').upper()]
    
    def fetch_recent_dividends(self, days_back: int = 90) -> List[Dict]:
        """
        Fetch recent dividend announcements
        
        Args:
            days_back: Number of days to look back for dividends
            
        Returns:
            List of dividend announcements
        """
        print(f"💰 Fetching dividend announcements from last {days_back} days...")
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        dividend_categories = self.get_dividend_categories()
        all_dividends = []
        
        for category in dividend_categories:
            category_name = category.get('categoryName', '')
            print(f"   📋 Searching {category_name}...")
            
            result = self.api.get_approved_announcements(
                announcement_type=category_name,
                from_date=start_date,
                to_date=end_date,
                announcement_categories=category_name
            )
            
            if result['success'] and 'approvedAnnouncements' in result['data']:
                announcements = result['data']['approvedAnnouncements']
                all_dividends.extend(announcements)
                print(f"   ✅ Found {len(announcements)} {category_name.lower()} announcements")
            else:
                print(f"   ⚠️  No {category_name.lower()} announcements found")
            
            time.sleep(0.3)  # Rate limiting
        
        print(f"\n🎉 Total dividend announcements found: {len(all_dividends)}")
        self.dividend_data = all_dividends
        return all_dividends
    
    def get_dividend_details(self, announcement_id: int) -> Optional[Dict]:
        """
        Get detailed dividend information by announcement ID
        
        Args:
            announcement_id: The announcement ID to fetch details for
            
        Returns:
            Detailed dividend information or None if failed
        """
        result = self.api.get_announcement_by_id(announcement_id)
        
        if result['success']:
            return result['data']
        else:
            print(f"❌ Failed to get dividend details for ID {announcement_id}: {result.get('error')}")
            return None
    
    def analyze_companies_with_dividends(self, limit: Optional[int] = None, delay: float = 1.0):
        """
        Analyze companies with enhanced dividend information
        
        Args:
            limit: Maximum number of companies to analyze (None for all)
            delay: Delay between API requests in seconds
        """
        if not self.company_data:
            print("❌ No company data available")
            return
        
        companies_to_analyze = self.company_data[:limit] if limit else self.company_data
        
        print(f"🚀 Starting enhanced analysis of {len(companies_to_analyze)} companies...")
        print(f"⏱️  Delay between requests: {delay} seconds")
        print("="*80)
        
        successful = 0
        failed = 0
        
        for i, company in enumerate(companies_to_analyze, 1):
            symbol = company.get('symbol', 'N/A')
            print(f"\n[{i}/{len(companies_to_analyze)}] {symbol}")
            
            # Get basic company info
            company_result = self.api.get_company_info(symbol)
            
            if company_result['success']:
                company_info = company_result['data']
                
                # Extract key metrics
                last_price = company_info.get('lastTradedPrice', 0)
                change_pct = company_info.get('changePercentage', 0)
                market_cap = company_info.get('marketCap', 0)
                
                # Calculate risk category
                risk_category = self._calculate_risk_category(company_info)
                
                # Check for recent dividends for this company
                company_dividends = [div for div in self.dividend_data 
                                   if symbol.split('.')[0] in div.get('company', '').upper()]
                
                # Compile enhanced analysis
                enhanced_data = {
                    'symbol': symbol,
                    'name': company_info.get('name', 'N/A'),
                    'last_traded_price': last_price,
                    'change_percentage': change_pct,
                    'market_cap': market_cap,
                    'risk_category': risk_category,
                    'ytd_high': company_info.get('high52Week', 0),
                    'ytd_low': company_info.get('low52Week', 0),
                    'volume': company_info.get('volume', 0),
                    'turnover': company_info.get('turnover', 0),
                    'recent_dividends': len(company_dividends),
                    'dividend_announcements': company_dividends[:3],  # Last 3 dividends
                    'last_dividend_date': company_dividends[0].get('dateOfAnnouncement') if company_dividends else None,
                    'analysis_date': datetime.now().isoformat()
                }
                
                self.analysis_results.append(enhanced_data)
                
                # Display progress
                dividend_info = f" | 💰 {len(company_dividends)} recent dividends" if company_dividends else ""
                print(f"  💰 Price: {last_price} ({change_pct:+.2f}%)")
                print(f"  📊 Market Cap: LKR {market_cap:,.0f}")
                print(f"  ⚖️  Risk: {risk_category}{dividend_info}")
                print(f"  ✅ Success")
                
                successful += 1
            else:
                print(f"  ❌ Failed: {company_result.get('error', 'Unknown error')}")
                failed += 1
            
            time.sleep(delay)
        
        print(f"\n🎉 Enhanced analysis completed!")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
    
    def _calculate_risk_category(self, company_info: Dict) -> str:
        """Calculate risk category based on price volatility and market metrics"""
        try:
            current_price = float(company_info.get('lastTradedPrice', 0))
            high_52week = float(company_info.get('high52Week', 0))
            low_52week = float(company_info.get('low52Week', 0))
            
            if high_52week > 0 and low_52week > 0:
                volatility = (high_52week - low_52week) / low_52week
                
                if volatility < 0.2:
                    return "Very Low Risk"
                elif volatility < 0.5:
                    return "Low Risk"
                elif volatility < 1.0:
                    return "Medium Risk"
                elif volatility < 2.0:
                    return "High Risk"
                else:
                    return "Very High Risk"
            
            return "Risk Unknown"
        except (ValueError, TypeError):
            return "Risk Unknown"
    
    def generate_dividend_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive dividend analysis report
        
        Returns:
            Dict containing dividend insights and recommendations
        """
        if not self.analysis_results:
            return {"error": "No analysis data available"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(self.analysis_results)
        
        # Dividend analysis
        dividend_companies = df[df['recent_dividends'] > 0].copy()
        non_dividend_companies = df[df['recent_dividends'] == 0].copy()
        
        dividend_analysis = {
            "summary": {
                "total_companies_analyzed": len(df),
                "companies_with_dividends": len(dividend_companies),
                "companies_without_dividends": len(non_dividend_companies),
                "dividend_percentage": len(dividend_companies) / len(df) * 100 if len(df) > 0 else 0
            },
            "dividend_insights": {
                "top_dividend_payers": dividend_companies.nlargest(10, 'recent_dividends')[
                    ['symbol', 'name', 'last_traded_price', 'recent_dividends', 'last_dividend_date']
                ].to_dict('records') if not dividend_companies.empty else [],
                
                "dividend_by_risk": dividend_companies.groupby('risk_category')['recent_dividends'].agg([
                    'count', 'mean', 'sum'
                ]).to_dict() if not dividend_companies.empty else {},
                
                "high_value_dividend_stocks": dividend_companies[
                    (dividend_companies['recent_dividends'] > 0) & 
                    (dividend_companies['market_cap'] > dividend_companies['market_cap'].median())
                ][['symbol', 'name', 'last_traded_price', 'market_cap', 'recent_dividends']].to_dict('records') if not dividend_companies.empty else []
            },
            "investment_recommendations": {
                "dividend_aristocrats": self._find_dividend_aristocrats(dividend_companies),
                "value_dividend_plays": self._find_value_dividend_plays(dividend_companies),
                "growth_with_dividends": self._find_growth_dividend_stocks(dividend_companies)
            }
        }
        
        return dividend_analysis
    
    def _find_dividend_aristocrats(self, dividend_df: pd.DataFrame) -> List[Dict]:
        """Find consistent dividend paying companies"""
        if dividend_df.empty:
            return []
        
        # Companies with multiple recent dividends and low risk
        aristocrats = dividend_df[
            (dividend_df['recent_dividends'] >= 2) & 
            (dividend_df['risk_category'].isin(['Very Low Risk', 'Low Risk']))
        ].nlargest(5, 'recent_dividends')
        
        return aristocrats[['symbol', 'name', 'last_traded_price', 'risk_category', 'recent_dividends']].to_dict('records')
    
    def _find_value_dividend_plays(self, dividend_df: pd.DataFrame) -> List[Dict]:
        """Find undervalued companies with dividends"""
        if dividend_df.empty:
            return []
        
        # Companies with dividends and prices closer to 52-week lows
        dividend_df = dividend_df.copy()
        dividend_df['price_position'] = (
            (dividend_df['last_traded_price'] - dividend_df['ytd_low']) / 
            (dividend_df['ytd_high'] - dividend_df['ytd_low'])
        ).fillna(0.5)
        
        value_plays = dividend_df[
            (dividend_df['recent_dividends'] > 0) & 
            (dividend_df['price_position'] < 0.4)  # Price in lower 40% of range
        ].nsmallest(5, 'price_position')
        
        return value_plays[['symbol', 'name', 'last_traded_price', 'recent_dividends', 'price_position']].to_dict('records')
    
    def _find_growth_dividend_stocks(self, dividend_df: pd.DataFrame) -> List[Dict]:
        """Find growing companies that also pay dividends"""
        if dividend_df.empty:
            return []
        
        # Companies with positive momentum and dividends
        growth_dividend = dividend_df[
            (dividend_df['recent_dividends'] > 0) & 
            (dividend_df['change_percentage'] > 0)
        ].nlargest(5, 'change_percentage')
        
        return growth_dividend[['symbol', 'name', 'last_traded_price', 'change_percentage', 'recent_dividends']].to_dict('records')
    
    def save_enhanced_analysis(self, filename: Optional[str] = None):
        """Save enhanced analysis results to files"""
        if not self.analysis_results:
            print("❌ No analysis results to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate dividend report
        dividend_report = self.generate_dividend_report()
        
        # Save to JSON
        json_filename = filename or f"enhanced_investment_analysis_{timestamp}.json"
        json_path = os.path.join(reports_dir, json_filename)
        
        full_report = {
            "analysis_metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_companies": len(self.analysis_results),
                "dividend_announcements_analyzed": len(self.dividend_data)
            },
            "company_analysis": self.analysis_results,
            "dividend_report": dividend_report
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)
        print(f"💾 Enhanced analysis saved to: {json_path}")
        
        # Save to Excel
        excel_filename = json_filename.replace('.json', '.xlsx')
        excel_path = os.path.join(reports_dir, excel_filename)
        
        # Create multiple sheets
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Main analysis
            df_main = pd.DataFrame(self.analysis_results)
            df_main.to_excel(writer, sheet_name='Company Analysis', index=False)
            
            # Dividend companies
            dividend_companies = df_main[df_main['recent_dividends'] > 0]
            if not dividend_companies.empty:
                dividend_companies.to_excel(writer, sheet_name='Dividend Companies', index=False)
            
            # Top recommendations
            recommendations = dividend_report.get('investment_recommendations', {})
            for rec_type, rec_data in recommendations.items():
                if rec_data:
                    df_rec = pd.DataFrame(rec_data)
                    sheet_name = rec_type.replace('_', ' ').title()[:31]  # Excel sheet name limit
                    df_rec.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"📊 Excel report saved to: {excel_path}")
        
        return {
            "json_file": json_path,
            "excel_file": excel_path,
            "summary": dividend_report['summary']
        }

def main():
    """Main execution function"""
    print("🎯 Enhanced CSE Investment Analyzer with Dividend Tracking")
    print("="*70)
    
    # Initialize analyzer
    analyzer = EnhancedInvestmentAnalyzer()
    
    if not analyzer.company_data:
        print("❌ No company data available. Make sure data.json exists.")
        return
    
    print(f"📊 Loaded {len(analyzer.company_data)} companies")
    print(f"📋 Loaded {len(analyzer.announcement_categories.get('categories', []))} announcement categories")
    
    # Fetch recent dividends first
    analyzer.fetch_recent_dividends(days_back=90)
    
    # Analyze companies (limit to 50 for demo, remove limit for full analysis)
    print(f"\n🔍 Analyzing companies with dividend data...")
    analyzer.analyze_companies_with_dividends(limit=50, delay=0.8)
    
    if analyzer.analysis_results:
        # Generate and display summary
        dividend_report = analyzer.generate_dividend_report()
        summary = dividend_report.get('summary', {})
        
        print(f"\n📈 ANALYSIS SUMMARY")
        print(f"="*40)
        print(f"Total companies analyzed: {summary.get('total_companies_analyzed', 0)}")
        print(f"Companies with recent dividends: {summary.get('companies_with_dividends', 0)}")
        print(f"Dividend percentage: {summary.get('dividend_percentage', 0):.1f}%")
        
        # Show top dividend recommendations
        recommendations = dividend_report.get('investment_recommendations', {})
        
        if recommendations.get('dividend_aristocrats'):
            print(f"\n👑 TOP DIVIDEND ARISTOCRATS:")
            for i, stock in enumerate(recommendations['dividend_aristocrats'][:3], 1):
                print(f"   {i}. {stock['symbol']} - {stock['name']}")
                print(f"      Price: LKR {stock['last_traded_price']} | Risk: {stock['risk_category']}")
                print(f"      Recent Dividends: {stock['recent_dividends']}")
        
        if recommendations.get('value_dividend_plays'):
            print(f"\n💎 VALUE DIVIDEND OPPORTUNITIES:")
            for i, stock in enumerate(recommendations['value_dividend_plays'][:3], 1):
                print(f"   {i}. {stock['symbol']} - {stock['name']}")
                print(f"      Price: LKR {stock['last_traded_price']} | Position: {stock['price_position']:.1%}")
                print(f"      Recent Dividends: {stock['recent_dividends']}")
        
        # Save results
        print(f"\n💾 Saving enhanced analysis...")
        save_result = analyzer.save_enhanced_analysis()
        
        if save_result:
            print(f"✅ Reports saved successfully!")
            print(f"   📄 JSON: {save_result['json_file']}")
            print(f"   📊 Excel: {save_result['excel_file']}")
    else:
        print("❌ No analysis results generated")

if __name__ == "__main__":
    main()
