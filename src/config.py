"""
Configuration settings for the Log Analyzer
"""

import os
from pathlib import Path

# Get the project root directory (log_analyzer folder)
BASE_DIR = Path(__file__).parent.parent

# Define paths
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, LOG_DIR]:
    directory.mkdir(exist_ok=True)

# File paths
DEFAULT_INPUT_FILE = DATA_DIR / "large_server_logs.txt"
SUMMARY_REPORT_PATH = OUTPUT_DIR / "summary_report.txt"
VISUALIZATION_PATH = OUTPUT_DIR / "error_distribution.png"
EXECUTION_LOG_PATH = LOG_DIR / "execution.log"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Analysis settings
TOP_IP_COUNT = 5  # Show top 5 IPs with most errors

# Print paths for debugging
if __name__ == "__main__":
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"DEFAULT_INPUT_FILE: {DEFAULT_INPUT_FILE}")
    print(f"File exists: {DEFAULT_INPUT_FILE.exists()}")