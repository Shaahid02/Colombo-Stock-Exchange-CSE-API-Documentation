"""
CSE Financial Reports Downloader
Downloads PDF reports from CSE financial announcements API
"""

import os
import requests
from urllib.parse import urljoin
from app import CSE_API
import time
from datetime import datetime
import json

class CSE_ReportDownloader:
    def __init__(self):
        self.cse_api = CSE_API()
        self.base_download_url = "https://cdn.cse.lk/"  # CDN URL for file downloads
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.company_data = self.load_company_data()
        
    def load_company_data(self):
        """Load company data from data.json to get security IDs"""
        try:
            with open('company_data/data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Warning: company_data/data.json not found. Security ID lookup will not be available.")
            return []
        except Exception as e:
            print(f"⚠️  Warning: Error loading company data: {e}")
            return []
    
    def find_security_id(self, symbol_or_name):
        """
        Find security ID by company symbol or name
        
        Args:
            symbol_or_name (str): Company symbol (e.g., 'ABAN.N0000') or name (e.g., 'ABANS ELECTRICALS')
        
        Returns:
            int or None: Security ID if found, None otherwise
        """
        if not self.company_data:
            return None
            
        search_term = symbol_or_name.upper()
        
        for company in self.company_data:
            if (search_term in company['symbol'].upper() or 
                search_term in company['name'].upper()):
                return company['securityId']
        
        return None
    
    def get_company_info(self, security_id):
        """
        Get company information by security ID
        
        Args:
            security_id (int): Company security ID
        
        Returns:
            dict or None: Company information if found
        """
        if not self.company_data:
            return None
            
        for company in self.company_data:
            if company['securityId'] == security_id:
                return company
        
        return None
        
    def create_download_folder(self, folder_name="cse_financial_reports"):
        """Create a folder for downloaded reports in the reports directory"""
        # Ensure reports directory exists
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            print(f"📁 Created reports directory: {reports_dir}")
        
        # Create the specific folder inside reports
        full_folder_path = os.path.join(reports_dir, folder_name)
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)
            print(f"📁 Created download folder: {full_folder_path}")
        return full_folder_path
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def download_file(self, file_path, company_name, symbol, file_text, download_folder):
        """Download a single PDF file"""
        try:
            # Construct full URL
            full_url = urljoin(self.base_download_url, file_path)
            
            # Create safe filename
            safe_company_name = self.sanitize_filename(company_name)
            safe_file_text = self.sanitize_filename(file_text)
            
            # Extract file extension from path
            file_extension = os.path.splitext(file_path)[1] or '.pdf'
            
            # Create filename: CompanyName_Symbol_ReportType_timestamp.pdf
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_company_name}_{symbol}_{safe_file_text}_{timestamp}{file_extension}"
            
            # Full local path
            local_path = os.path.join(download_folder, filename)
            
            print(f"📥 Downloading: {company_name} ({symbol})")
            print(f"    Report: {file_text}")
            print(f"    URL: {full_url}")
            
            # Download the file
            response = requests.get(full_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Save to file
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"    ✅ Downloaded: {filename} ({file_size:,} bytes)")
            
            return {
                'success': True,
                'filename': filename,
                'local_path': local_path,
                'file_size': file_size,
                'url': full_url
            }
            
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Download failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'url': full_url if 'full_url' in locals() else 'Unknown'
            }
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_financial_reports(self, limit=None, company_filter=None):
        """
        Download all financial reports
        
        Args:
            limit (int): Maximum number of files to download (None for all)
            company_filter (str): Only download reports from companies containing this text
        """
        print("🚀 Starting Financial Reports Download")
        print("="*50)
        
        # Get financial announcements
        print("📡 Fetching financial announcements...")
        result = self.cse_api.get_financial_announcements()
        
        if not result['success']:
            print(f"❌ Failed to fetch announcements: {result['error']}")
            return []
        
        announcements = result['data']['reqFinancialAnnouncemnets']
        print(f"📄 Found {len(announcements)} financial announcements")
        
        # Apply filters
        if company_filter:
            announcements = [a for a in announcements if company_filter.lower() in a['name'].lower()]
            print(f"🔍 Filtered to {len(announcements)} announcements containing '{company_filter}'")
        
        if limit:
            announcements = announcements[:limit]
            print(f"📊 Limited to first {len(announcements)} announcements")
        
        # Create download folder
        folder_name = "all_reports" + (f"_filtered_{company_filter}" if company_filter else "")
        download_folder = self.create_download_folder(folder_name)
        
        # Download files
        download_results = []
        successful_downloads = 0
        failed_downloads = 0
        
        for i, announcement in enumerate(announcements, 1):
            print(f"\n[{i}/{len(announcements)}] " + "="*40)
            
            result = self.download_file(
                file_path=announcement['path'],
                company_name=announcement['name'],
                symbol=announcement['symbol'],
                file_text=announcement['fileText'],
                download_folder=download_folder
            )
            
            result.update({
                'announcement_id': announcement['id'],
                'company_name': announcement['name'],
                'symbol': announcement['symbol'],
                'file_text': announcement['fileText'],
                'uploaded_date': announcement['uploadedDate']
            })
            
            download_results.append(result)
            
            if result['success']:
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Small delay to be respectful to the server
            time.sleep(1)
        
        # Summary
        print(f"\n🎉 Download Summary")
        print("="*30)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        print(f"📁 Files saved to: {os.path.abspath(download_folder)}")
        
        # Save download log in reports directory
        log_filename = os.path.join("reports", f"download_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_filename, 'w', encoding='utf-8') as f:
            json.dump(download_results, f, indent=2, ensure_ascii=False)
        print(f"📋 Download log saved: {log_filename}")
        
        return download_results
    
    def download_specific_reports(self, symbols_list):
        """
        Download reports for specific company symbols
        
        Args:
            symbols_list (list): List of company symbols (e.g., ['LOLC', 'CSLK'])
        """
        print(f"🎯 Downloading reports for specific symbols: {symbols_list}")
        
        result = self.cse_api.get_financial_announcements()
        if not result['success']:
            print(f"❌ Failed to fetch announcements: {result['error']}")
            return []
        
        announcements = result['data']['reqFinancialAnnouncemnets']
        
        # Filter by symbols
        filtered_announcements = [
            a for a in announcements 
            if any(symbol.upper() in a['symbol'].upper() for symbol in symbols_list)
        ]
        
        print(f"📄 Found {len(filtered_announcements)} reports for specified symbols")
        
        if not filtered_announcements:
            print("❌ No reports found for the specified symbols")
            return []
        
        # Create download folder with symbol names
        folder_name = f"specific_companies_{'_'.join(symbols_list)}"
        download_folder = self.create_download_folder(folder_name)
        
        # Download files
        download_results = []
        for i, announcement in enumerate(filtered_announcements, 1):
            print(f"\n[{i}/{len(filtered_announcements)}] " + "="*40)
            
            result = self.download_file(
                file_path=announcement['path'],
                company_name=announcement['name'],
                symbol=announcement['symbol'],
                file_text=announcement['fileText'],
                download_folder=download_folder
            )
            
            download_results.append(result)
            time.sleep(1)
        
        return download_results

    def download_reports_by_date_range(self, from_date, to_date, security_id=None):
        """
        Download reports for a specific date range, optionally filtered by company security ID
        
        Args:
            from_date (str): Start date in YYYY-MM-DD format (e.g., '2025-01-01')
            to_date (str): End date in YYYY-MM-DD format (e.g., '2025-08-26')
            security_id (str or int, optional): Company security ID to filter by (e.g., '642' or 642)
        
        Returns:
            list: Download results
        """
        print(f"🔍 Downloading reports for date range: {from_date} to {to_date}")
        
        company_info = None
        if security_id:
            security_id = str(security_id)  # Ensure it's a string for the API
            print(f"🎯 Filtering by Security ID: {security_id}")
            
            # Get company info for better logging
            company_info = self.get_company_info(int(security_id))
            if company_info:
                print(f"🏢 Company: {company_info['name']} ({company_info['symbol']})")
        else:
            print("🌐 Fetching reports for ALL companies in the date range")
        
        # Fetch filtered financial announcements
        print("📡 Fetching financial announcements...")
        
        # Use the updated API method - it now handles both filtered and unfiltered requests
        result = self.cse_api.get_financial_announcements_filtered(from_date, to_date, security_id)
        
        if not result['success']:
            print(f"❌ Failed to fetch announcements: {result['error']}")
            return []
        
        announcements = result['data']['reqFinancialAnnouncemnets']
        
        print(f"📄 Found {len(announcements)} financial announcements")
        
        if not announcements:
            print("❌ No announcements found for the specified criteria")
            return []
        
        # Create download folder name
        if company_info:
            folder_name = f"{company_info['symbol'].split('.')[0]}_{from_date}_to_{to_date}"
        elif security_id:
            folder_name = f"secID_{security_id}_{from_date}_to_{to_date}"
        else:
            folder_name = f"all_companies_{from_date}_to_{to_date}"
        
        download_folder = self.create_download_folder(folder_name)
        
        # Download files
        download_results = []
        successful_downloads = 0
        failed_downloads = 0
        
        for i, announcement in enumerate(announcements, 1):
            print(f"\n[{i}/{len(announcements)}] " + "="*40)
            
            result = self.download_file(
                file_path=announcement['path'],
                company_name=announcement['name'],
                symbol=announcement['symbol'],
                file_text=announcement['fileText'],
                download_folder=download_folder
            )
            
            result.update({
                'announcement_id': announcement['id'],
                'company_name': announcement['name'],
                'symbol': announcement['symbol'],
                'file_text': announcement['fileText'],
                'uploaded_date': announcement['uploadedDate'],
                'manual_date': announcement.get('manualDate'),
                'security_id': security_id if security_id else 'all',
                'date_range': f"{from_date} to {to_date}"
            })
            
            download_results.append(result)
            
            if result['success']:
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Small delay to be respectful to the server
            time.sleep(1)
        
        # Summary
        print(f"\n🎉 Download Summary")
        print("="*30)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        print(f"📁 Files saved to: {os.path.abspath(download_folder)}")
        
        # Save download log in reports directory
        log_filename = os.path.join("reports", f"download_log_{folder_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_filename, 'w', encoding='utf-8') as f:
            json.dump(download_results, f, indent=2, ensure_ascii=False)
        print(f"📋 Download log saved: {log_filename}")
        
        return download_results
    
    # Deprecated methods - kept for backward compatibility
    def download_reports_by_security_id(self, security_id, from_date, to_date):
        """
        DEPRECATED: Use download_reports_by_date_range() instead
        Download reports for a specific company by security ID and date range
        """
        print("⚠️  This method is deprecated. Using download_reports_by_date_range() instead...")
        return self.download_reports_by_date_range(from_date, to_date, security_id)
    
    def download_reports_by_company_name(self, company_name_or_symbol, from_date, to_date):
        """
        Download reports for a company by name/symbol and date range
        
        Args:
            company_name_or_symbol (str): Company name or symbol to search for
            from_date (str): Start date in YYYY-MM-DD format
            to_date (str): End date in YYYY-MM-DD format
        
        Returns:
            list: Download results
        """
        # Find security ID
        security_id = self.find_security_id(company_name_or_symbol)
        
        if security_id is None:
            print(f"❌ Could not find security ID for: {company_name_or_symbol}")
            print("💡 Available companies:")
            
            # Show some matching companies
            search_term = company_name_or_symbol.upper()
            matches = [c for c in self.company_data 
                      if search_term in c['name'].upper() or search_term in c['symbol'].upper()]
            
            for match in matches[:10]:  # Show first 10 matches
                print(f"   🏢 {match['name']} ({match['symbol']}) - Security ID: {match['securityId']}")
            
            if len(matches) > 10:
                print(f"   ... and {len(matches) - 10} more matches")
            
            return []
        
        print(f"🔍 Found Security ID {security_id} for: {company_name_or_symbol}")
        return self.download_reports_by_date_range(from_date, to_date, security_id)

    def download_reports_by_time_range(self, from_date, to_date):
        """
        DEPRECATED: Use download_reports_by_date_range() instead  
        Download reports for a specific time range
        """
        print("⚠️  This method is deprecated. Using download_reports_by_date_range() instead...")
        return self.download_reports_by_date_range(from_date, to_date)

def main():
    """Main function with interactive menu"""
    downloader = CSE_ReportDownloader()
    
    print("CSE Financial Reports Downloader")
    print("="*35)
    print("1. Download ALL financial reports")
    print("2. Download first 10 reports (test)")
    print("3. Download reports for specific companies")
    print("4. Download reports containing keyword")
    print("5. Download reports by date range (all companies)")
    print("6. Download reports by date range and company (Security ID)")
    print("7. Download reports by company name/symbol and date range")
    print("8. List available financial reports (No download)")

    choice = input("\nEnter your choice (1-8): ").strip()
    
    if choice == "1":
        print("⚠️  This will download ALL financial reports. This may take a while and use significant storage.")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            downloader.download_financial_reports()
        else:
            print("Download cancelled.")
    
    elif choice == "2":
        print("📥 Downloading first 10 reports as a test...")
        downloader.download_financial_reports(limit=10)
    
    elif choice == "3":
        symbols = input("Enter company symbols (comma-separated, e.g., LOLC,CSLK,TAP): ").strip()
        if symbols:
            symbols_list = [s.strip() for s in symbols.split(',')]
            downloader.download_specific_reports(symbols_list)
        else:
            print("No symbols provided.")
    
    elif choice == "4":
        keyword = input("Enter keyword to search in company names: ").strip()
        if keyword:
            limit_str = input("Limit number of downloads (press Enter for no limit): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            downloader.download_financial_reports(limit=limit, company_filter=keyword)
        else:
            print("No keyword provided.")
    
    elif choice == "5":
        from_date = input("Enter from date (YYYY-MM-DD, e.g., 2025-01-01): ").strip()
        to_date = input("Enter to date (YYYY-MM-DD, e.g., 2025-08-26): ").strip()
        
        if from_date and to_date:
            try:
                # Validate date format
                datetime.strptime(from_date, '%Y-%m-%d')
                datetime.strptime(to_date, '%Y-%m-%d')
                downloader.download_reports_by_date_range(from_date, to_date)
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD format.")
        else:
            print("❌ Both from date and to date are required.")
    
    elif choice == "6":
        from_date = input("Enter from date (YYYY-MM-DD, e.g., 2025-01-01): ").strip()
        to_date = input("Enter to date (YYYY-MM-DD, e.g., 2025-08-26): ").strip()
        security_id = input("Enter Security ID (e.g., 642): ").strip()
        
        if from_date and to_date and security_id:
            try:
                # Validate date format
                datetime.strptime(from_date, '%Y-%m-%d')
                datetime.strptime(to_date, '%Y-%m-%d')
                downloader.download_reports_by_date_range(from_date, to_date, security_id)
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD format.")
        else:
            print("❌ All fields (from date, to date, Security ID) are required.")
    
    elif choice == "7":
        company_name = input("Enter company name or symbol (e.g., 'ABANS' or 'LOLC'): ").strip()
        from_date = input("Enter from date (YYYY-MM-DD, e.g., 2025-01-01): ").strip()
        to_date = input("Enter to date (YYYY-MM-DD, e.g., 2025-08-26): ").strip()
        
        if company_name and from_date and to_date:
            try:
                # Validate date format
                datetime.strptime(from_date, '%Y-%m-%d')
                datetime.strptime(to_date, '%Y-%m-%d')
                downloader.download_reports_by_company_name(company_name, from_date, to_date)
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD format.")
        else:
            print("❌ All fields (company name, from date, to date) are required.")
    
    elif choice == "8":
        print("📄 Fetching available reports...")
        cse = CSE_API()
        result = cse.get_financial_announcements()
        if result['success']:
            announcements = result['data']['reqFinancialAnnouncemnets']
            print(f"\n📊 Available Financial Reports ({len(announcements)} total):")
            print("-" * 80)
            for i, ann in enumerate(announcements[:20], 1):  # Show first 20
                print(f"{i:2d}. {ann['name']} ({ann['symbol']})")
                print(f"    📄 {ann['fileText']}")
                print(f"    📅 {ann['uploadedDate']}")
                print()
            if len(announcements) > 20:
                print(f"... and {len(announcements) - 20} more reports")
        else:
            print(f"❌ Failed to fetch reports: {result['error']}")
    
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()