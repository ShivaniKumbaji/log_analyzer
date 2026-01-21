"""
Module for creating visualizations
"""

import matplotlib.pyplot as plt
import logging
from typing import Dict, Any
from pathlib import Path

# Import config
try:
    from .config import VISUALIZATION_PATH
except ImportError:
    # Fallback
    VISUALIZATION_PATH = Path("output") / "error_distribution.png"

logger = logging.getLogger(__name__)


class Visualizer:
    """Creates charts from analysis data"""
    
    def __init__(self, output_path: str = None):
        """
        Initialize Visualizer
        
        Args:
            output_path: Where to save the chart (optional)
        """
        if output_path:
            self.output_path = Path(output_path)
        else:
            self.output_path = VISUALIZATION_PATH
        
        # Create output directory if it doesn't exist
        self.output_path.parent.mkdir(exist_ok=True)
        
    def plot_error_distribution(self, stats: Dict[str, Any]) -> bool:
        """
        Create bar chart of error codes
        
        Args:
            stats: Analysis statistics
            
        Returns:
            True if successful, False otherwise
        """
        try:
            error_dist = stats.get('error_code_distribution', {})
            
            if not error_dist:
                print("⚠️ No error data to visualize")
                return False
            
            print("📊 Creating visualization...")
            
            # Prepare data
            error_codes = list(error_dist.keys())
            counts = list(error_dist.values())
            
            # Create figure
            plt.figure(figsize=(10, 6))
            
            # Create bar chart
            bars = plt.bar(error_codes, counts, color='red', alpha=0.7)
            
            # Add labels on bars
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, height,
                        f'{count}', ha='center', va='bottom')
            
            # Customize chart
            plt.title('HTTP Error Code Distribution', fontweight='bold')
            plt.xlabel('HTTP Error Code')
            plt.ylabel('Number of Errors')
            plt.grid(axis='y', alpha=0.3)
            
            # Save the figure
            plt.tight_layout()
            plt.savefig(self.output_path, dpi=150)
            plt.close()
            
            print(f"✅ Chart saved to: {self.output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating chart: {e}")
            return False
    
    def plot_top_ips(self, stats: Dict[str, Any]) -> bool:
        """
        Create horizontal bar chart for top IPs
        
        Args:
            stats: Analysis statistics
            
        Returns:
            True if successful
        """
        try:
            top_ips = stats.get('top_error_ips', {})
            
            if not top_ips:
                return False
            
            # Prepare data
            ips = list(top_ips.keys())
            counts = list(top_ips.values())
            
            # Create figure
            plt.figure(figsize=(10, 5))
            
            # Create horizontal bar chart
            bars = plt.barh(ips, counts, color='orange', alpha=0.7)
            
            # Add labels
            for bar, count in zip(bars, counts):
                plt.text(count, bar.get_y() + bar.get_height()/2,
                        f' {count}', va='center')
            
            # Customize
            plt.title('Top IP Addresses with Errors', fontweight='bold')
            plt.xlabel('Number of Errors')
            plt.tight_layout()
            
            # Save
            ip_chart_path = self.output_path.parent / 'top_ips.png'
            plt.savefig(ip_chart_path, dpi=150)
            plt.close()
            
            print(f"✅ IP chart saved to: {ip_chart_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Could not create IP chart: {e}")
            return False
    
    def create_all_charts(self, stats: Dict[str, Any]) -> None:
        """Create all available charts"""
        self.plot_error_distribution(stats)
        self.plot_top_ips(stats)