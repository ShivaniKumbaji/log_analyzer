"""
Module for processing and analyzing log data
"""

import pandas as pd
import logging
from typing import List, Dict, Any

# Import config
try:
    from .config import TOP_IP_COUNT
except ImportError:
    # Fallback
    TOP_IP_COUNT = 5

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes parsed log data"""
    
    def __init__(self):
        self.df = pd.DataFrame()  # Empty DataFrame
        self.stats = {}
    
    def create_dataframe(self, parsed_logs: List[Dict[str, Any]]) -> None:
        """
        Create DataFrame from parsed logs
        
        Args:
            parsed_logs: List of parsed log dictionaries
        """
        if not parsed_logs:
            print("⚠️ No logs to process")
            return
        
        # Create DataFrame
        self.df = pd.DataFrame(parsed_logs)
        print(f"✅ Created DataFrame with {len(self.df)} rows")
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the log data
        
        Returns:
            Dictionary with analysis results
        """
        if self.df.empty:
            print("⚠️ DataFrame is empty")
            return {}
        
        print("🔍 Analyzing data...")
        
        try:
            # Basic counts
            total_requests = len(self.df)
            
            # Filter error requests (HTTP 4xx and 5xx)
            error_df = self.df[self.df['is_error']]
            error_count = len(error_df)
            
            # Error code distribution
            error_code_counts = error_df['error_code'].value_counts().to_dict()
            
            # Top IPs with errors
            top_ips = error_df['ip_address'].value_counts().head(TOP_IP_COUNT).to_dict()
            
            # Request type distribution
            request_counts = self.df['request_type'].value_counts().to_dict()
            
            # Error by request type
            error_by_request = error_df['request_type'].value_counts().to_dict()
            
            # Compile results
            self.stats = {
                'total_requests': total_requests,
                'error_requests': error_count,
                'success_requests': total_requests - error_count,
                'error_percentage': (error_count / total_requests * 100) if total_requests > 0 else 0,
                'error_code_distribution': error_code_counts,
                'top_error_ips': top_ips,
                'request_type_distribution': request_counts,
                'error_by_request': error_by_request,
                'unique_ips': self.df['ip_address'].nunique(),
                'unique_error_ips': error_df['ip_address'].nunique() if not error_df.empty else 0
            }
            
            print("✅ Analysis complete!")
            return self.stats
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return {}
    
    def show_summary(self):
        """Display summary in console"""
        if not self.stats:
            print("No analysis results available")
            return
        
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"Total Requests: {self.stats['total_requests']}")
        print(f"Error Requests: {self.stats['error_requests']}")
        print(f"Success Requests: {self.stats['success_requests']}")
        print(f"Error Rate: {self.stats['error_percentage']:.2f}%")
        print(f"Unique IPs: {self.stats['unique_ips']}")
        print(f"Unique IPs with Errors: {self.stats['unique_error_ips']}")
        
        if self.stats['error_code_distribution']:
            print("\nError Code Distribution:")
            for code, count in self.stats['error_code_distribution'].items():
                print(f"  HTTP {code}: {count} errors")
        
        if self.stats['top_error_ips']:
            print("\nTop IPs with Errors:")
            for ip, count in self.stats['top_error_ips'].items():
                print(f"  {ip}: {count} errors")
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the DataFrame"""
        return self.df
    
    def get_stats(self) -> Dict[str, Any]:
        """Get analysis statistics"""
        return self.stats