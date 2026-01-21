"""
SINGLE FILE LOG ANALYZER - Everything in one file
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from collections import Counter

print("\n" + "="*60)
print("SINGLE FILE LOG ANALYZER")
print("="*60)

# Configuration
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "server_logs.txt"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_FILE = OUTPUT_DIR / "summary_report.txt"
CHART_FILE = OUTPUT_DIR / "error_distribution.png"
LOG_FILE = BASE_DIR / "logs" / "execution.log"

# Create directories
for dir_path in [OUTPUT_DIR, BASE_DIR / "logs"]:
    dir_path.mkdir(exist_ok=True)

# Log pattern
LOG_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),'
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}),'
    r'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH),'
    r'(\d+)$'
)

def validate_ip(ip):
    """Check if IP address is valid"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            num = int(part)
            if not 0 <= num <= 255:
                return False
        except ValueError:
            return False
    return True

def parse_log_line(line):
    """Parse a single log line"""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    
    timestamp_str, ip, request_type, error_code_str = match.groups()
    
    if not validate_ip(ip):
        return None
    
    try:
        error_code = int(error_code_str)
        is_error = 400 <= error_code < 600
    except ValueError:
        return None
    
    return {
        'timestamp': timestamp_str,
        'ip_address': ip,
        'request_type': request_type,
        'error_code': error_code,
        'is_error': is_error
    }

def main():
    """Main analysis function"""
    start_time = datetime.now()
    
    print(f"\n📂 Reading file: {DATA_FILE}")
    
    if not DATA_FILE.exists():
        print(f"❌ File not found: {DATA_FILE}")
        return
    
    # Read and parse file
    parsed_logs = []
    total_lines = 0
    failed_lines = 0
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            
            if not line:
                continue
                
            parsed = parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)
            else:
                failed_lines += 1
    
    print(f"✅ Read {total_lines} lines")
    print(f"✅ Successfully parsed: {len(parsed_logs)}")
    print(f"❌ Failed to parse: {failed_lines}")
    
    if not parsed_logs:
        print("❌ No valid log entries found!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(parsed_logs)
    
    # Analyze
    total_requests = len(df)
    error_df = df[df['is_error']]
    error_count = len(error_df)
    
    # Error code distribution
    error_codes = error_df['error_code'].value_counts().to_dict()
    
    # Top IPs with errors
    top_ips = error_df['ip_address'].value_counts().head(5).to_dict()
    
    # Show results
    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    print(f"Total Requests: {total_requests}")
    print(f"Error Requests: {error_count}")
    print(f"Success Requests: {total_requests - error_count}")
    print(f"Error Rate: {(error_count/total_requests*100):.2f}%")
    
    if error_codes:
        print("\nError Code Distribution:")
        for code, count in sorted(error_codes.items()):
            print(f"  HTTP {code}: {count} errors")
    
    if top_ips:
        print("\nTop IPs with Errors:")
        for ip, count in top_ips.items():
            print(f"  {ip}: {count} errors")
    
    # Create chart
    print("\n🎨 Creating chart...")
    if error_codes:
        plt.figure(figsize=(10, 6))
        plt.bar(list(error_codes.keys()), list(error_codes.values()), color='red')
        plt.title('HTTP Error Code Distribution')
        plt.xlabel('Error Code')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(CHART_FILE, dpi=150)
        plt.close()
        print(f"✅ Chart saved: {CHART_FILE}")
    
    # Generate report
    print("\n📄 Generating report...")
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write("LOG ANALYSIS REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Lines Read: {total_lines}\n")
        f.write(f"Successfully Parsed: {len(parsed_logs)}\n")
        f.write(f"Failed to Parse: {failed_lines}\n\n")
        f.write(f"Total Requests: {total_requests}\n")
        f.write(f"Error Requests: {error_count}\n")
        f.write(f"Error Rate: {(error_count/total_requests*100):.2f}%\n\n")
        
        if error_codes:
            f.write("Error Code Distribution:\n")
            for code, count in sorted(error_codes.items()):
                f.write(f"  HTTP {code}: {count} errors\n")
            f.write("\n")
        
        if top_ips:
            f.write("Top IPs with Errors:\n")
            for ip, count in top_ips.items():
                f.write(f"  {ip}: {count} errors\n")
    
    print(f"✅ Report saved: {REPORT_FILE}")
    
    # Completion
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n✅ Analysis completed in {duration:.2f} seconds!")
    print(f"📁 Check the 'output' folder for results.")

if __name__ == "__main__":
    main()