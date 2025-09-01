"""
Dedicated Dividend Tracking Tool for CSE
Monitors dividend announcements, tracks payment schedules, and provides dividend insights
"""
import json
import pandas as pd
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import CSE_API

class DividendTracker:
    """
    Comprehensive dividend tracking and analysis tool
    """
    
    def __init__(self):
        self.api = CSE_API()
        self.announcement_categories = self._load_announcement_categories()
        self.dividend_data = []
        self.detailed_dividends = []
        
    def _load_announcement_categories(self) -> Dict:
        """Load announcement categories from JSON file"""
        try:
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            categories_path = os.path.join(parent_dir, "company_data/announcement_categories.json")
            with open(categories_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Run fetch_categories.py first to download announcement categories")
            return {"categories": []}
    
    def get_dividend_categories(self) -> List[Dict]:
        """Get all dividend-related categories"""
        categories = self.announcement_categories.get('categories', [])
        return [cat for cat in categories if 'DIVIDEND' in cat.get('categoryName', '').upper()]
    
    def fetch_all_dividends(self, days_back: int = 180) -> List[Dict]:
        """
        Fetch all dividend announcements from specified period
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of all dividend announcements
        """
        print(f"💰 Fetching ALL dividend announcements from last {days_back} days...")
        print("="*60)
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        dividend_categories = self.get_dividend_categories()
        all_dividends = []
        
        for category in dividend_categories:
            category_name = category.get('categoryName', '')
            print(f"\n📋 Fetching: {category_name}")
            
            result = self.api.get_approved_announcements(
                announcement_type=category_name,
                from_date=start_date,
                to_date=end_date,
                announcement_categories=category_name
            )
            
            if result['success'] and 'approvedAnnouncements' in result['data']:
                announcements = result['data']['approvedAnnouncements']
                all_dividends.extend(announcements)
                print(f"   ✅ Found {len(announcements)} announcements")
                
                # Show recent examples
                for ann in announcements[:3]:
                    company = ann.get('company', 'N/A')
                    date = ann.get('dateOfAnnouncement', 'N/A')
                    print(f"      - {company} ({date})")
                    
                if len(announcements) > 3:
                    print(f"      ... and {len(announcements) - 3} more")
            else:
                print(f"   ⚠️  No announcements found")
            
            time.sleep(0.5)  # Rate limiting
        
        self.dividend_data = all_dividends
        print(f"\n🎉 Total dividend announcements collected: {len(all_dividends)}")
        return all_dividends
    
    def fetch_dividend_details(self, max_details: int = 20) -> List[Dict]:
        """
        Fetch detailed information for recent dividend announcements
        
        Args:
            max_details: Maximum number of dividend details to fetch
            
        Returns:
            List of detailed dividend information
        """
        if not self.dividend_data:
            print("❌ No dividend data available. Run fetch_all_dividends() first.")
            return []
        
        print(f"\n🔍 Fetching detailed information for {min(max_details, len(self.dividend_data))} dividends...")
        
        detailed_dividends = []
        
        # Sort by date and get most recent
        sorted_dividends = sorted(
            self.dividend_data, 
            key=lambda x: x.get('createdDate', 0), 
            reverse=True
        )
        
        for i, dividend in enumerate(sorted_dividends[:max_details], 1):
            announcement_id = dividend.get('announcementId')
            company = dividend.get('company', 'N/A')
            
            print(f"   [{i}/{min(max_details, len(self.dividend_data))}] {company}")
            
            if announcement_id:
                details = self.api.get_announcement_by_id(announcement_id)
                
                if details['success'] and 'reqBaseAnnouncement' in details['data']:
                    base_info = details['data']['reqBaseAnnouncement']
                    docs = details['data'].get('reqAnnouncementDocs', [])
                    
                    enhanced_dividend = {
                        'announcement_id': announcement_id,
                        'company_name': base_info.get('companyName', 'N/A'),
                        'symbol': base_info.get('symbol', 'N/A'),
                        'dividend_per_share': base_info.get('votingDivPerShare', 0),
                        'financial_year': base_info.get('financialYear', 'N/A'),
                        'announcement_date': base_info.get('dateOfAnnouncement', 'N/A'),
                        'ex_dividend_date': base_info.get('xd', 'N/A'),
                        'payment_date': base_info.get('payment', 'N/A'),
                        'agm_date': base_info.get('agm', 'N/A'),
                        'record_date': base_info.get('recordDate'),
                        'remarks': base_info.get('remarks', 'N/A'),
                        'documents_count': len(docs),
                        'documents': docs
                    }
                    
                    detailed_dividends.append(enhanced_dividend)
                    
                    # Show key info
                    div_amount = enhanced_dividend['dividend_per_share']
                    ex_date = enhanced_dividend['ex_dividend_date']
                    payment_date = enhanced_dividend['payment_date']
                    print(f"      💰 LKR {div_amount}/share | Ex: {ex_date} | Pay: {payment_date}")
                else:
                    print(f"      ❌ Failed to get details")
            
            time.sleep(0.4)  # Rate limiting
        
        self.detailed_dividends = detailed_dividends
        print(f"\n✅ Fetched details for {len(detailed_dividends)} dividends")
        return detailed_dividends
    
    def generate_dividend_calendar(self) -> pd.DataFrame:
        """
        Generate upcoming dividend calendar
        
        Returns:
            DataFrame with upcoming dividend events
        """
        if not self.detailed_dividends:
            print("❌ No detailed dividend data. Run fetch_dividend_details() first.")
            return pd.DataFrame()
        
        calendar_data = []
        current_date = datetime.now()
        
        for dividend in self.detailed_dividends:
            # Parse dates
            try:
                ex_date_str = dividend.get('ex_dividend_date', '')
                payment_date_str = dividend.get('payment_date', '')
                agm_date_str = dividend.get('agm_date', '')
                
                # Add events to calendar
                if ex_date_str and ex_date_str != 'N/A':
                    calendar_data.append({
                        'date': ex_date_str,
                        'event_type': 'Ex-Dividend',
                        'company': dividend['company_name'],
                        'symbol': dividend['symbol'],
                        'amount': dividend['dividend_per_share'],
                        'details': f"LKR {dividend['dividend_per_share']}/share"
                    })
                
                if payment_date_str and payment_date_str != 'N/A':
                    calendar_data.append({
                        'date': payment_date_str,
                        'event_type': 'Dividend Payment',
                        'company': dividend['company_name'],
                        'symbol': dividend['symbol'],
                        'amount': dividend['dividend_per_share'],
                        'details': f"LKR {dividend['dividend_per_share']}/share payment"
                    })
                
                if agm_date_str and agm_date_str != 'N/A':
                    calendar_data.append({
                        'date': agm_date_str,
                        'event_type': 'AGM',
                        'company': dividend['company_name'],
                        'symbol': dividend['symbol'],
                        'amount': 0,
                        'details': 'Annual General Meeting'
                    })
            except Exception as e:
                continue
        
        if calendar_data:
            df_calendar = pd.DataFrame(calendar_data)
            # Sort by date
            df_calendar = df_calendar.sort_values('date')
            return df_calendar
        else:
            return pd.DataFrame()
    
    def analyze_dividend_trends(self) -> Dict[str, Any]:
        """
        Analyze dividend trends and patterns
        
        Returns:
            Dict containing dividend trend analysis
        """
        if not self.detailed_dividends:
            return {"error": "No detailed dividend data available"}
        
        df = pd.DataFrame(self.detailed_dividends)
        
        # Dividend amount analysis
        dividend_amounts = df['dividend_per_share'].astype(float)
        dividend_amounts = dividend_amounts[dividend_amounts > 0]  # Remove zeros
        
        trend_analysis = {
            "dividend_statistics": {
                "total_dividends_analyzed": len(df),
                "average_dividend": dividend_amounts.mean() if not dividend_amounts.empty else 0,
                "median_dividend": dividend_amounts.median() if not dividend_amounts.empty else 0,
                "min_dividend": dividend_amounts.min() if not dividend_amounts.empty else 0,
                "max_dividend": dividend_amounts.max() if not dividend_amounts.empty else 0,
                "std_deviation": dividend_amounts.std() if not dividend_amounts.empty else 0
            },
            "top_dividend_payers": df.nlargest(10, 'dividend_per_share')[
                ['company_name', 'symbol', 'dividend_per_share', 'ex_dividend_date', 'payment_date']
            ].to_dict('records') if not df.empty else [],
            
            "upcoming_payments": self._get_upcoming_payments(df),
            "recent_announcements": df.nlargest(10, 'announcement_id')[
                ['company_name', 'symbol', 'dividend_per_share', 'announcement_date']
            ].to_dict('records') if not df.empty else []
        }
        
        return trend_analysis
    
    def _get_upcoming_payments(self, df: pd.DataFrame) -> List[Dict]:
        """Get upcoming dividend payments"""
        upcoming = []
        current_date = datetime.now()
        
        for _, row in df.iterrows():
            try:
                payment_date_str = row.get('payment_date', '')
                if payment_date_str and payment_date_str != 'N/A':
                    # Simple date comparison (assuming DD MMM YYYY format)
                    upcoming.append({
                        'company_name': row['company_name'],
                        'symbol': row['symbol'],
                        'dividend_per_share': row['dividend_per_share'],
                        'payment_date': payment_date_str,
                        'ex_dividend_date': row.get('ex_dividend_date', 'N/A')
                    })
            except:
                continue
        
        # Sort by payment date (simple string sort for now)
        return sorted(upcoming, key=lambda x: x['payment_date'])[:10]
    
    def save_dividend_tracking_report(self):
        """Save comprehensive dividend tracking report"""
        if not self.detailed_dividends:
            print("❌ No dividend data to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(parent_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate trend analysis
        trends = self.analyze_dividend_trends()
        
        # Generate calendar
        calendar_df = self.generate_dividend_calendar()
        
        # Prepare full report
        full_report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_dividends": len(self.detailed_dividends),
                "analysis_period_days": 180
            },
            "dividend_trends": trends,
            "detailed_dividends": self.detailed_dividends,
            "calendar_events": calendar_df.to_dict('records') if not calendar_df.empty else []
        }
        
        # Save JSON report
        json_filename = f"dividend_tracking_report_{timestamp}.json"
        json_path = os.path.join(reports_dir, json_filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Dividend report saved to: {json_path}")
        
        # Save Excel report
        excel_filename = f"dividend_tracking_report_{timestamp}.xlsx"
        excel_path = os.path.join(reports_dir, excel_filename)
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Detailed dividends
            df_dividends = pd.DataFrame(self.detailed_dividends)
            df_dividends.to_excel(writer, sheet_name='All Dividends', index=False)
            
            # Calendar
            if not calendar_df.empty:
                calendar_df.to_excel(writer, sheet_name='Dividend Calendar', index=False)
            
            # Top payers
            if trends.get('top_dividend_payers'):
                df_top = pd.DataFrame(trends['top_dividend_payers'])
                df_top.to_excel(writer, sheet_name='Top Dividend Payers', index=False)
            
            # Upcoming payments
            if trends.get('upcoming_payments'):
                df_upcoming = pd.DataFrame(trends['upcoming_payments'])
                df_upcoming.to_excel(writer, sheet_name='Upcoming Payments', index=False)
        
        print(f"📊 Excel report saved to: {excel_path}")
        
        return {
            "json_file": json_path,
            "excel_file": excel_path,
            "summary": trends.get('dividend_statistics', {})
        }
    
    def show_dividend_summary(self):
        """Display a summary of dividend analysis"""
        if not self.detailed_dividends:
            print("❌ No dividend data available")
            return
        
        trends = self.analyze_dividend_trends()
        stats = trends.get('dividend_statistics', {})
        
        print(f"\n📊 DIVIDEND ANALYSIS SUMMARY")
        print(f"="*50)
        print(f"Total dividends analyzed: {stats.get('total_dividends_analyzed', 0)}")
        print(f"Average dividend: LKR {stats.get('average_dividend', 0):.2f}")
        print(f"Highest dividend: LKR {stats.get('max_dividend', 0):.2f}")
        print(f"Lowest dividend: LKR {stats.get('min_dividend', 0):.2f}")
        
        # Top dividend payers
        top_payers = trends.get('top_dividend_payers', [])
        if top_payers:
            print(f"\n👑 TOP 5 DIVIDEND PAYERS:")
            for i, payer in enumerate(top_payers[:5], 1):
                print(f"   {i}. {payer['symbol']} - {payer['company_name']}")
                print(f"      💰 LKR {payer['dividend_per_share']}/share")
                print(f"      📅 Ex-Date: {payer['ex_dividend_date']} | Payment: {payer['payment_date']}")
        
        # Upcoming payments
        upcoming = trends.get('upcoming_payments', [])
        if upcoming:
            print(f"\n📅 UPCOMING DIVIDEND PAYMENTS:")
            for i, payment in enumerate(upcoming[:5], 1):
                print(f"   {i}. {payment['symbol']} - {payment['company_name']}")
                print(f"      💰 LKR {payment['dividend_per_share']}/share on {payment['payment_date']}")

def main():
    """Main dividend tracking execution"""
    print("💰 CSE Dividend Tracking Tool")
    print("="*40)
    
    tracker = DividendTracker()
    
    # Check if categories are loaded
    dividend_cats = tracker.get_dividend_categories()
    if not dividend_cats:
        print("❌ No dividend categories available. Run fetch_categories.py first.")
        return
    
    print(f"📋 Found {len(dividend_cats)} dividend categories:")
    for cat in dividend_cats:
        print(f"   - {cat.get('categoryName')}")
    
    # Fetch all dividend announcements
    print(f"\n🔍 Starting dividend data collection...")
    tracker.fetch_all_dividends(days_back=120)  # Last 4 months
    
    if tracker.dividend_data:
        # Fetch detailed information for recent dividends
        tracker.fetch_dividend_details(max_details=15)
        
        # Show summary
        tracker.show_dividend_summary()
        
        # Save comprehensive report
        print(f"\n💾 Saving dividend tracking report...")
        save_result = tracker.save_dividend_tracking_report()
        
        if save_result:
            print(f"✅ Dividend tracking report saved!")
            print(f"   📄 JSON: {save_result['json_file']}")
            print(f"   📊 Excel: {save_result['excel_file']}")
            
            summary = save_result.get('summary', {})
            print(f"\n🎯 KEY INSIGHTS:")
            print(f"   Average dividend: LKR {summary.get('average_dividend', 0):.2f}")
            print(f"   Highest dividend: LKR {summary.get('max_dividend', 0):.2f}")
            print(f"   Total companies tracked: {summary.get('total_dividends_analyzed', 0)}")
    else:
        print("❌ No dividend data collected")

if __name__ == "__main__":
    main()
