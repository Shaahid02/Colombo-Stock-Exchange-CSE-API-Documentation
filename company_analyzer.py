"""
CSE Investment Analysis Tool
Analyzes all companies from data.json using the companyInfoSummery API
Provides investment-focused insights and analysis
"""

import json
import os
import sys
from datetime import datetime
import pandas as pd
import time
from typing import Dict, List, Any, Optional
import numpy as np

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import CSE_API

class CSE_InvestmentAnalyzer:
    def __init__(self):
        self.cse_api = CSE_API()
        self.company_data = self.load_company_data()
        self.analysis_results = []
        self.failed_requests = []
        
    def load_company_data(self):
        """Load company data from data.json"""
        try:
            with open('company_data/data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Error: company_data/data.json not found")
            return []
        except Exception as e:
            print(f"❌ Error loading company data: {e}")
            return []
    
    def get_company_summary(self, symbol: str) -> Dict[str, Any]:
        """Get company info summary for a specific symbol"""
        try:
            result = self.cse_api.get_company_info(symbol)
            if result['success']:
                return {
                    'success': True,
                    'data': result['data']
                }
            else:
                return {
                    'success': False,
                    'error': result['error']
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def calculate_investment_metrics(self, symbol_info: Dict, beta_info: Dict) -> Dict[str, Any]:
        """Calculate key investment metrics"""
        metrics = {}
        
        # Basic price metrics
        last_price = symbol_info.get('lastTradedPrice', 0)
        prev_close = symbol_info.get('previousClose', 0)
        
        if last_price and prev_close:
            metrics['price_change_pct'] = ((last_price - prev_close) / prev_close) * 100
        
        # Volatility indicators (using historical high/low data)
        ytd_high = symbol_info.get('ytdHiPrice', 0)
        ytd_low = symbol_info.get('ytdLowPrice', 0)
        p12_high = symbol_info.get('p12HiPrice', 0)
        p12_low = symbol_info.get('p12LowPrice', 0)
        
        if ytd_high and ytd_low and ytd_high != ytd_low:
            metrics['ytd_volatility'] = ((ytd_high - ytd_low) / ytd_low) * 100
            if last_price:
                metrics['position_in_ytd_range'] = ((last_price - ytd_low) / (ytd_high - ytd_low)) * 100
        
        if p12_high and p12_low and p12_high != p12_low:
            metrics['p12_volatility'] = ((p12_high - p12_low) / p12_low) * 100
            if last_price:
                metrics['position_in_p12_range'] = ((last_price - p12_low) / (p12_high - p12_low)) * 100
        
        # Value metrics
        market_cap = symbol_info.get('marketCap', 0)
        quantity_issued = symbol_info.get('quantityIssued', 0)
        
        if market_cap and quantity_issued:
            metrics['book_value_per_share'] = market_cap / quantity_issued
        
        # Liquidity metrics
        ytd_volume = symbol_info.get('ytdShareVolume', 0)
        ytd_turnover = symbol_info.get('ytdTurnover', 0)
        
        if ytd_volume and ytd_turnover:
            metrics['avg_price_ytd'] = ytd_turnover / ytd_volume
            if last_price and metrics['avg_price_ytd']:
                metrics['price_vs_ytd_avg'] = ((last_price - metrics['avg_price_ytd']) / metrics['avg_price_ytd']) * 100
        
        # Risk metrics
        beta_asi = beta_info.get('triASIBetaValue')
        beta_spsl = beta_info.get('betaValueSPSL')
        
        if beta_asi:
            if beta_asi > 1.5:
                metrics['risk_category'] = 'High Risk'
            elif beta_asi > 1.0:
                metrics['risk_category'] = 'Medium Risk'
            elif beta_asi > 0.5:
                metrics['risk_category'] = 'Low Risk'
            else:
                metrics['risk_category'] = 'Very Low Risk'
        
        return metrics
    
    def extract_comprehensive_data(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive data for investment analysis"""
        try:
            symbol_info = company_data.get('reqSymbolInfo', {})
            beta_info = company_data.get('reqSymbolBetaInfo', {})
            logo_info = company_data.get('reqLogo', {})
            
            # Calculate investment metrics
            investment_metrics = self.calculate_investment_metrics(symbol_info, beta_info)
            
            base_data = {
                # Basic Company Info
                'security_id': symbol_info.get('id'),
                'symbol': symbol_info.get('symbol'),
                'name': symbol_info.get('name'),
                'isin': symbol_info.get('isin'),
                'issue_date': symbol_info.get('issueDate'),
                'par_value': symbol_info.get('parValue'),
                
                # Current Price Data
                'last_traded_price': symbol_info.get('lastTradedPrice'),
                'previous_close': symbol_info.get('previousClose'),
                'change': symbol_info.get('change'),
                'change_percentage': symbol_info.get('changePercentage'),
                'today_high': symbol_info.get('hiTrade'),
                'today_low': symbol_info.get('lowTrade'),
                
                # Historical Price Ranges
                'ytd_high': symbol_info.get('ytdHiPrice'),
                'ytd_low': symbol_info.get('ytdLowPrice'),
                'p12_high': symbol_info.get('p12HiPrice'),
                'p12_low': symbol_info.get('p12LowPrice'),
                'all_time_high': symbol_info.get('allHiPrice'),
                'all_time_low': symbol_info.get('allLowPrice'),
                
                # Volume and Turnover Data
                'quantity_issued': symbol_info.get('quantityIssued'),
                'today_volume': symbol_info.get('tdyShareVolume'),
                'today_turnover': symbol_info.get('tdyTurnover'),
                'ytd_volume': symbol_info.get('ytdShareVolume'),
                'ytd_turnover': symbol_info.get('ytdTurnover'),
                'p12_volume': symbol_info.get('p12ShareVolume'),
                
                # Market Data
                'market_cap': symbol_info.get('marketCap'),
                'market_cap_percentage': symbol_info.get('marketCapPercentage'),
                'foreign_holdings': symbol_info.get('foreignHoldings'),
                'foreign_percentage': symbol_info.get('foreignPercentage'),
                
                # Beta and Risk Metrics
                'tri_asi_beta': beta_info.get('triASIBetaValue'),
                'spsl_beta': beta_info.get('betaValueSPSL'),
                'beta_period': beta_info.get('triASIBetaPeriod'),
                'beta_quarter': beta_info.get('quarter'),
                
                # Additional Info
                'has_logo': logo_info is not None and logo_info.get('path') is not None,
                'logo_path': logo_info.get('path') if logo_info else None,
                
                # Timestamp
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            # Merge with calculated investment metrics
            base_data.update(investment_metrics)
            
            return base_data
            
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return {}
    
    def analyze_companies(self, limit: Optional[int] = None, delay: float = 1.0):
        """Analyze companies for investment insights"""
        if not self.company_data:
            print("❌ No company data available")
            return
        
        companies_to_analyze = self.company_data[:limit] if limit else self.company_data
        total_companies = len(companies_to_analyze)
        
        print(f"🚀 Starting investment analysis of {total_companies} companies...")
        print(f"⏱️  Delay between requests: {delay} seconds")
        print("="*80)
        
        for i, company in enumerate(companies_to_analyze, 1):
            symbol = company.get('symbol')
            name = company.get('name', 'Unknown')
            
            print(f"\n[{i}/{total_companies}] {symbol} - {name}")
            
            # Get company summary
            result = self.get_company_summary(symbol)
            
            if result['success']:
                # Extract comprehensive data
                company_analysis = self.extract_comprehensive_data(result['data'])
                company_analysis['source_data'] = company  # Include original data
                
                self.analysis_results.append(company_analysis)
                
                # Display key investment metrics
                price = company_analysis.get('last_traded_price', 'N/A')
                change_pct = company_analysis.get('change_percentage', 0)
                market_cap = company_analysis.get('market_cap', 0)
                risk_cat = company_analysis.get('risk_category', 'Unknown')
                ytd_pos = company_analysis.get('position_in_ytd_range', 0)
                
                print(f"  💰 Price: {price} ({change_pct:+.2f}%)")
                print(f"  📊 Market Cap: LKR {market_cap:,.0f}" if market_cap else "  📊 Market Cap: N/A")
                print(f"  ⚖️  Risk: {risk_cat}")
                print(f"  📈 YTD Range Position: {ytd_pos:.1f}%" if ytd_pos else "")
                print("  ✅ Success")
                
            else:
                error = result.get('error', 'Unknown error')
                self.failed_requests.append({
                    'symbol': symbol,
                    'name': name,
                    'error': error
                })
                print(f"  ❌ Failed: {error}")
            
            # Delay between requests
            if i < total_companies:
                time.sleep(delay)
        
        print(f"\n🎉 Analysis completed!")
        print(f"✅ Successful: {len(self.analysis_results)}")
        print(f"❌ Failed: {len(self.failed_requests)}")
    
    def generate_investment_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive investment analysis"""
        if not self.analysis_results:
            return {"error": "No data to analyze"}
        
        df = pd.DataFrame(self.analysis_results)
        
        # Filter companies with valid price data
        df_active = df[(df['last_traded_price'].notna()) & (df['last_traded_price'] > 0)]
        
        analysis = {
            'summary': {
                'total_companies': len(df),
                'active_companies': len(df_active),
                'inactive_companies': len(df) - len(df_active),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            
            'market_overview': self._analyze_market_overview(df_active),
            'valuation_analysis': self._analyze_valuations(df_active),
            'risk_analysis': self._analyze_risk_profile(df_active),
            'performance_analysis': self._analyze_performance(df_active),
            'liquidity_analysis': self._analyze_liquidity(df_active),
            'investment_opportunities': self._identify_opportunities(df_active)
        }
        
        return analysis
    
    def _analyze_market_overview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze overall market conditions"""
        if df.empty:
            return {}
        
        total_market_cap = df['market_cap'].sum()
        
        return {
            'total_market_capitalization': total_market_cap,
            'average_market_cap': df['market_cap'].mean(),
            'median_market_cap': df['market_cap'].median(),
            'market_cap_distribution': {
                'large_cap': len(df[df['market_cap'] > df['market_cap'].quantile(0.9)]),
                'mid_cap': len(df[(df['market_cap'] > df['market_cap'].quantile(0.3)) & 
                                 (df['market_cap'] <= df['market_cap'].quantile(0.9))]),
                'small_cap': len(df[df['market_cap'] <= df['market_cap'].quantile(0.3)])
            },
            'price_ranges': {
                'average_price': df['last_traded_price'].mean(),
                'median_price': df['last_traded_price'].median(),
                'highest_price': df['last_traded_price'].max(),
                'lowest_price': df['last_traded_price'].min()
            }
        }
    
    def _analyze_valuations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze company valuations"""
        if df.empty:
            return {}
        
        # Price position analysis
        df_with_ytd = df[df['position_in_ytd_range'].notna()]
        
        valuation_metrics = {}
        
        if not df_with_ytd.empty:
            valuation_metrics = {
                'ytd_position_analysis': {
                    'near_highs': len(df_with_ytd[df_with_ytd['position_in_ytd_range'] > 80]),
                    'mid_range': len(df_with_ytd[(df_with_ytd['position_in_ytd_range'] >= 20) & 
                                                 (df_with_ytd['position_in_ytd_range'] <= 80)]),
                    'near_lows': len(df_with_ytd[df_with_ytd['position_in_ytd_range'] < 20]),
                    'average_position': df_with_ytd['position_in_ytd_range'].mean()
                },
                'volatility_analysis': {
                    'high_volatility': len(df[df['ytd_volatility'] > 100]) if 'ytd_volatility' in df.columns else 0,
                    'medium_volatility': len(df[(df['ytd_volatility'] >= 50) & (df['ytd_volatility'] <= 100)]) if 'ytd_volatility' in df.columns else 0,
                    'low_volatility': len(df[df['ytd_volatility'] < 50]) if 'ytd_volatility' in df.columns else 0
                }
            }
        
        return valuation_metrics
    
    def _analyze_risk_profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze risk profiles of companies"""
        if df.empty:
            return {}
        
        df_with_beta = df[df['tri_asi_beta'].notna()]
        
        if df_with_beta.empty:
            return {'note': 'No beta data available'}
        
        return {
            'beta_distribution': {
                'high_risk': len(df_with_beta[df_with_beta['tri_asi_beta'] > 1.5]),
                'medium_risk': len(df_with_beta[(df_with_beta['tri_asi_beta'] > 1.0) & (df_with_beta['tri_asi_beta'] <= 1.5)]),
                'low_risk': len(df_with_beta[(df_with_beta['tri_asi_beta'] > 0.5) & (df_with_beta['tri_asi_beta'] <= 1.0)]),
                'very_low_risk': len(df_with_beta[df_with_beta['tri_asi_beta'] <= 0.5])
            },
            'beta_statistics': {
                'average_beta': df_with_beta['tri_asi_beta'].mean(),
                'median_beta': df_with_beta['tri_asi_beta'].median(),
                'highest_beta': df_with_beta['tri_asi_beta'].max(),
                'lowest_beta': df_with_beta['tri_asi_beta'].min()
            }
        }
    
    def _analyze_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance metrics"""
        if df.empty:
            return {}
        
        df_with_change = df[df['change_percentage'].notna()]
        
        return {
            'daily_performance': {
                'gainers': len(df_with_change[df_with_change['change_percentage'] > 0]),
                'losers': len(df_with_change[df_with_change['change_percentage'] < 0]),
                'unchanged': len(df_with_change[df_with_change['change_percentage'] == 0]),
                'average_change': df_with_change['change_percentage'].mean(),
                'best_performer': df_with_change['change_percentage'].max(),
                'worst_performer': df_with_change['change_percentage'].min()
            }
        }
    
    def _analyze_liquidity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze liquidity metrics"""
        if df.empty:
            return {}
        
        df_with_volume = df[df['today_volume'].notna() & (df['today_volume'] > 0)]
        
        if df_with_volume.empty:
            return {'note': 'No volume data available'}
        
        return {
            'volume_analysis': {
                'total_volume_today': df_with_volume['today_volume'].sum(),
                'average_volume': df_with_volume['today_volume'].mean(),
                'high_volume_stocks': len(df_with_volume[df_with_volume['today_volume'] > df_with_volume['today_volume'].quantile(0.8)]),
                'low_volume_stocks': len(df_with_volume[df_with_volume['today_volume'] < df_with_volume['today_volume'].quantile(0.2)])
            },
            'turnover_analysis': {
                'total_turnover_today': df_with_volume['today_turnover'].sum() if 'today_turnover' in df_with_volume.columns else 0,
                'companies_with_turnover': len(df_with_volume[df_with_volume['today_turnover'].notna() & (df_with_volume['today_turnover'] > 0)]) if 'today_turnover' in df_with_volume.columns else 0
            }
        }
    
    def _identify_opportunities(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify potential investment opportunities"""
        if df.empty:
            return {}
        
        opportunities = {}
        
        # Value opportunities (near YTD lows)
        df_with_ytd = df[df['position_in_ytd_range'].notna()]
        if not df_with_ytd.empty:
            value_opportunities = df_with_ytd[df_with_ytd['position_in_ytd_range'] < 25].copy()
            value_opportunities = value_opportunities.sort_values('position_in_ytd_range')
            
            opportunities['value_opportunities'] = value_opportunities[
                ['symbol', 'name', 'last_traded_price', 'position_in_ytd_range', 'market_cap']
            ].head(10).to_dict('records')
        
        # Growth opportunities (strong recent performance with good volume)
        df_growth = df[(df['change_percentage'] > 5) & (df['today_volume'].notna()) & (df['today_volume'] > 0)]
        if not df_growth.empty:
            growth_opportunities = df_growth.sort_values('change_percentage', ascending=False)
            
            opportunities['growth_opportunities'] = growth_opportunities[
                ['symbol', 'name', 'last_traded_price', 'change_percentage', 'today_volume']
            ].head(10).to_dict('records')
        
        # Low risk, stable opportunities
        df_stable = df[(df['tri_asi_beta'].notna()) & (df['tri_asi_beta'] < 1.0) & (df['market_cap'] > df['market_cap'].median())]
        if not df_stable.empty:
            stable_opportunities = df_stable.sort_values('tri_asi_beta')
            
            opportunities['stable_opportunities'] = stable_opportunities[
                ['symbol', 'name', 'last_traded_price', 'tri_asi_beta', 'market_cap']
            ].head(10).to_dict('records')
        
        return opportunities
    
    def get_investment_recommendations(self, investment_style: str = 'balanced') -> Dict[str, List]:
        """Get personalized investment recommendations based on style"""
        if not self.analysis_results:
            return {}
        
        df = pd.DataFrame(self.analysis_results)
        df_active = df[(df['last_traded_price'].notna()) & (df['last_traded_price'] > 0)]
        
        recommendations = {}
        
        if investment_style.lower() == 'conservative':
            # Low beta, stable companies, good market cap
            conservative = df_active[
                (df_active['tri_asi_beta'].notna()) & 
                (df_active['tri_asi_beta'] < 1.0) &
                (df_active['market_cap'] > df_active['market_cap'].median())
            ].sort_values('tri_asi_beta').head(10)
            
            recommendations['conservative'] = conservative[
                ['symbol', 'name', 'last_traded_price', 'tri_asi_beta', 'market_cap', 'risk_category']
            ].to_dict('records')
        
        elif investment_style.lower() == 'aggressive':
            # High beta, high growth potential
            aggressive = df_active[
                (df_active['tri_asi_beta'].notna()) & 
                (df_active['tri_asi_beta'] > 1.2)
            ].sort_values('change_percentage', ascending=False).head(10)
            
            recommendations['aggressive'] = aggressive[
                ['symbol', 'name', 'last_traded_price', 'tri_asi_beta', 'change_percentage', 'risk_category']
            ].to_dict('records')
        
        elif investment_style.lower() == 'value':
            # Near YTD lows, good fundamentals
            value = df_active[
                (df_active['position_in_ytd_range'].notna()) & 
                (df_active['position_in_ytd_range'] < 30) &
                (df_active['market_cap'] > 0)
            ].sort_values('position_in_ytd_range').head(10)
            
            recommendations['value'] = value[
                ['symbol', 'name', 'last_traded_price', 'position_in_ytd_range', 'ytd_high', 'ytd_low']
            ].to_dict('records')
        
        else:  # balanced
            # Mix of different risk levels and opportunities
            balanced = df_active[
                (df_active['tri_asi_beta'].notna()) & 
                (df_active['tri_asi_beta'] >= 0.5) & 
                (df_active['tri_asi_beta'] <= 1.5)
            ].sort_values('market_cap', ascending=False).head(10)
            
            recommendations['balanced'] = balanced[
                ['symbol', 'name', 'last_traded_price', 'tri_asi_beta', 'market_cap', 'change_percentage']
            ].to_dict('records')
        
        return recommendations
    
    def save_analysis(self, filename: str = None):
        """Save comprehensive analysis to files"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'investment_analysis_{timestamp}'

        # Ensure analysis directory exists
        os.makedirs('analysis', exist_ok=True)
        
        # Save raw data
        with open(f'analysis/{filename}_raw_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False, default=str)
        
        # Save investment analysis
        analysis = self.generate_investment_analysis()
        with open(f'analysis/{filename}_investment_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        # Save recommendations for different investment styles
        for style in ['conservative', 'aggressive', 'value', 'balanced']:
            recommendations = self.get_investment_recommendations(style)
            if recommendations:
                with open(f'reports/{filename}_{style}_recommendations.json', 'w', encoding='utf-8') as f:
                    json.dump(recommendations, f, indent=2, ensure_ascii=False, default=str)
        
        # Save failed requests
        if self.failed_requests:
            with open(f'analysis/{filename}_failed_requests.json', 'w', encoding='utf-8') as f:
                json.dump(self.failed_requests, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analysis saved:")
        print(f"  📊 Raw data: analysis/{filename}_raw_data.json")
        print(f"  📈 Investment analysis: analysis/{filename}_investment_analysis.json")
        print(f"  🎯 Recommendations: analysis/{filename}_[style]_recommendations.json")
        if self.failed_requests:
            print(f"  ❌ Failed requests: analysis/{filename}_failed_requests.json")

    def print_investment_summary(self):
        """Print comprehensive investment analysis summary"""
        analysis = self.generate_investment_analysis()
        
        print("\n" + "="*80)
        print("📊 INVESTMENT ANALYSIS SUMMARY")
        print("="*80)
        
        # Market Overview
        summary = analysis.get('summary', {})
        market = analysis.get('market_overview', {})
        
        print(f"\n🌐 Market Overview:")
        print(f"  Companies analyzed: {summary.get('total_companies', 0)}")
        print(f"  Active companies: {summary.get('active_companies', 0)}")
        print(f"  Total market cap: LKR {market.get('total_market_capitalization', 0):,.0f}")
        print(f"  Average price: LKR {market.get('price_ranges', {}).get('average_price', 0):,.2f}")
        
        # Risk Analysis
        risk = analysis.get('risk_analysis', {})
        beta_dist = risk.get('beta_distribution', {})
        
        if beta_dist:
            print(f"\n⚖️  Risk Distribution:")
            print(f"  High Risk (β>1.5): {beta_dist.get('high_risk', 0)} companies")
            print(f"  Medium Risk (1.0<β≤1.5): {beta_dist.get('medium_risk', 0)} companies")
            print(f"  Low Risk (0.5<β≤1.0): {beta_dist.get('low_risk', 0)} companies")
            print(f"  Very Low Risk (β≤0.5): {beta_dist.get('very_low_risk', 0)} companies")
        
        # Performance
        perf = analysis.get('performance_analysis', {}).get('daily_performance', {})
        if perf:
            print(f"\n📈 Today's Performance:")
            print(f"  Gainers: {perf.get('gainers', 0)}")
            print(f"  Losers: {perf.get('losers', 0)}")
            print(f"  Best performer: +{perf.get('best_performer', 0):.2f}%")
            print(f"  Worst performer: {perf.get('worst_performer', 0):.2f}%")
            print(f"  Market average: {perf.get('average_change', 0):+.2f}%")
        
        # Investment Opportunities
        opportunities = analysis.get('investment_opportunities', {})
        
        if opportunities.get('value_opportunities'):
            print(f"\n💎 Top Value Opportunities (Near YTD Lows):")
            for i, stock in enumerate(opportunities['value_opportunities'][:5], 1):
                print(f"  {i}. {stock['symbol']} - {stock['position_in_ytd_range']:.1f}% of YTD range")
        
        if opportunities.get('growth_opportunities'):
            print(f"\n🚀 Top Growth Opportunities (Strong Recent Performance):")
            for i, stock in enumerate(opportunities['growth_opportunities'][:5], 1):
                print(f"  {i}. {stock['symbol']} - +{stock['change_percentage']:.2f}%")
        
        if opportunities.get('stable_opportunities'):
            print(f"\n🛡️  Top Stable Opportunities (Low Risk):")
            for i, stock in enumerate(opportunities['stable_opportunities'][:5], 1):
                print(f"  {i}. {stock['symbol']} - β={stock['tri_asi_beta']:.3f}")

def main():
    """Main function with investment-focused menu"""
    print("CSE Investment Analysis Tool")
    print("="*50)
    print("1. Quick analysis (first 20 companies)")
    print("2. Sector analysis (first 100 companies)")
    print("3. Full market analysis (ALL companies)")
    print("4. Custom analysis")
    print("5. Get investment recommendations")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    analyzer = CSE_InvestmentAnalyzer()
    
    if not analyzer.company_data:
        print("❌ No company data available. Exiting.")
        return
    
    print(f"\n📊 Found {len(analyzer.company_data)} companies in data.json")
    
    if choice == "1":
        print("🧪 Quick analysis of first 20 companies...")
        analyzer.analyze_companies(limit=20, delay=0.8)
    elif choice == "2":
        print("📈 Sector analysis of first 100 companies...")
        analyzer.analyze_companies(limit=100, delay=1.0)
    elif choice == "3":
        print("⚠️  This will analyze ALL companies and may take 1-2 hours.")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            analyzer.analyze_companies(delay=1.5)
        else:
            print("Analysis cancelled.")
            return
    elif choice == "4":
        limit = input("Enter number of companies to analyze (or 'all'): ").strip()
        delay = input("Enter delay between requests in seconds (default 1.0): ").strip()
        
        limit = None if limit.lower() == 'all' else int(limit) if limit.isdigit() else 20
        delay = float(delay) if delay.replace('.', '').isdigit() else 1.0
        
        print(f"📊 Custom analysis: {limit or 'all'} companies with {delay}s delay...")
        analyzer.analyze_companies(limit=limit, delay=delay)
    elif choice == "5":
        print("🎯 Investment Recommendations")
        print("Choose your investment style:")
        print("1. Conservative (Low risk, stable)")
        print("2. Aggressive (High risk, high reward)")
        print("3. Value (Undervalued opportunities)")
        print("4. Balanced (Mixed approach)")
        
        style_choice = input("Enter style (1-4): ").strip()
        styles = {'1': 'conservative', '2': 'aggressive', '3': 'value', '4': 'balanced'}
        
        if style_choice in styles:
            # First need to analyze some companies
            print(f"Analyzing companies for {styles[style_choice]} recommendations...")
            analyzer.analyze_companies(limit=100, delay=1.0)
            
            recommendations = analyzer.get_investment_recommendations(styles[style_choice])
            
            print(f"\n🎯 {styles[style_choice].title()} Investment Recommendations:")
            for category, stocks in recommendations.items():
                print(f"\n{category.title()}:")
                for i, stock in enumerate(stocks[:10], 1):
                    print(f"  {i}. {stock.get('symbol')} - {stock.get('name')}")
                    print(f"     Price: LKR {stock.get('last_traded_price', 0):.2f}")
                    if 'tri_asi_beta' in stock:
                        print(f"     Risk: β={stock.get('tri_asi_beta', 0):.3f}")
        else:
            print("Invalid choice.")
            return
    else:
        print("Invalid choice.")
        return
    
    if len(analyzer.analysis_results) > 0:
        # Show investment summary
        analyzer.print_investment_summary()
        
        # Save results
        save = input("\n💾 Save analysis to files? (y/N): ").strip().lower()
        if save in ['y', 'yes']:
            analyzer.save_analysis()
            
            # Offer to generate recommendations
            rec = input("📋 Generate investment recommendations? (y/N): ").strip().lower()
            if rec in ['y', 'yes']:
                print("\nGenerating recommendations for all investment styles...")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                for style in ['conservative', 'aggressive', 'value', 'balanced']:
                    recs = analyzer.get_investment_recommendations(style)
                    if recs:
                        print(f"  ✅ {style.title()} recommendations generated")

if __name__ == "__main__":
    main()
