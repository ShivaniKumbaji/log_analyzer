"""
Module for generating text reports
"""

import logging
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

# Import config
try:
    from .config import SUMMARY_REPORT_PATH
except ImportError:
    # Fallback
    SUMMARY_REPORT_PATH = Path("output") / "summary_report.txt"

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates text reports from analysis"""
    
    def __init__(self, output_path: str = None):
        """
        Initialize ReportGenerator
        
        Args:
            output_path: Where to save report (optional)
        """
        if output_path:
            self.output_path = Path(output_path)
        else:
            self.output_path = SUMMARY_REPORT_PATH
        
        # Create output directory if it doesn't exist
        self.output_path.parent.mkdir(exist_ok=True)
    
    def generate(self, stats: Dict[str, Any], 
                parsing_stats: Dict[str, Any],
                reading_stats: Dict[str, Any]) -> str:
        """
        Generate text report
        
        Args:
            stats: Analysis statistics
            parsing_stats: Parsing statistics
            reading_stats: Reading statistics
            
        Returns:
            Report as string
        """
        print("📋 Generating report...")
        
        lines = []
        
        # Header
        lines.append("="*60)
        lines.append("LOG FILE ANALYSIS REPORT")
        lines.append("="*60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # File Statistics
        lines.append("FILE STATISTICS")
        lines.append("-"*40)
        lines.append(f"Total Lines Read: {reading_stats.get('total_lines', 0)}")
        lines.append(f"Valid Lines: {reading_stats.get('valid_lines', 0)}")
        lines.append(f"Skipped Lines: {reading_stats.get('skipped_lines', 0)}")
        lines.append(f"Successfully Parsed: {parsing_stats.get('parsed_count', 0)}")
        lines.append(f"Failed to Parse: {parsing_stats.get('failed_count', 0)}")
        lines.append(f"Success Rate: {parsing_stats.get('success_rate', 0)}%")
        lines.append("")
        
        # Analysis Summary
        lines.append("ANALYSIS SUMMARY")
        lines.append("-"*40)
        lines.append(f"Total Requests: {stats.get('total_requests', 0)}")
        lines.append(f"Error Requests: {stats.get('error_requests', 0)}")
        lines.append(f"Success Requests: {stats.get('success_requests', 0)}")
        lines.append(f"Error Rate: {stats.get('error_percentage', 0):.2f}%")
        lines.append(f"Unique IP Addresses: {stats.get('unique_ips', 0)}")
        lines.append(f"Unique IPs with Errors: {stats.get('unique_error_ips', 0)}")
        lines.append("")
        
        # Error Codes
        error_dist = stats.get('error_code_distribution', {})
        if error_dist:
            lines.append("ERROR CODE DISTRIBUTION")
            lines.append("-"*40)
            for code, count in sorted(error_dist.items()):
                lines.append(f"HTTP {code}: {count} errors")
            lines.append("")
        
        # Top IPs
        top_ips = stats.get('top_error_ips', {})
        if top_ips:
            lines.append("TOP IP ADDRESSES WITH ERRORS")
            lines.append("-"*40)
            for ip, count in top_ips.items():
                lines.append(f"{ip}: {count} errors")
            lines.append("")
        
        # Request Types
        req_dist = stats.get('request_type_distribution', {})
        if req_dist:
            lines.append("REQUEST TYPE DISTRIBUTION")
            lines.append("-"*40)
            for req_type, count in req_dist.items():
                lines.append(f"{req_type}: {count} requests")
        
        # Footer
        lines.append("")
        lines.append("="*60)
        lines.append("END OF REPORT")
        lines.append("="*60)
        
        # Convert to string
        report_text = "\n".join(lines)
        
        # Save to file
        self._save_report(report_text)
        
        return report_text
    
    def _save_report(self, report_text: str) -> None:
        """Save report to file"""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"✅ Report saved to: {self.output_path}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def display_report(self, report_text: str) -> None:
        """Display report in console"""
        print("\n" + "="*60)
        print("REPORT")
        print("="*60)
        print(report_text)