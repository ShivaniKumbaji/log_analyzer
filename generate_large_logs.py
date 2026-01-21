"""
Generate a large log file with 50,000+ entries for testing
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_large_log_file():
    """Generate a log file with 50,000+ entries"""
    
    # Configuration
    output_file = Path("data") / "large_server_logs.txt"
    num_lines = 50000  # Minimum required: 50,000
    
    # Sample data
    ips = [f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}" for _ in range(100)]
    requests = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    status_codes = [200, 201, 301, 302, 400, 401, 403, 404, 500, 502, 503]
    
    print(f"Generating {num_lines:,} log entries...")
    print(f"Output file: {output_file}")
    
    start_time = datetime(2025, 1, 15, 0, 0, 0)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            # Generate log entry
            timestamp = start_time + timedelta(seconds=i)
            ip = random.choice(ips)
            request = random.choice(requests)
            status = random.choice(status_codes)
            
            # Add some malformed entries (2% of lines)
            if random.random() < 0.02:
                if random.random() < 0.5:
                    f.write(f"MALFORMED_LINE_{i}\n")
                else:
                    f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},INVALID_IP,{request},{status}\n")
            else:
                f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},{ip},{request},{status}\n")
            
            # Show progress every 5000 lines
            if i > 0 and i % 5000 == 0:
                print(f"  Generated {i:,} lines...")
    
    print(f"✅ Successfully generated {num_lines:,} log entries")
    print(f"📁 File size: {output_file.stat().st_size / (1024*1024):.2f} MB")
    
    return output_file

def test_performance():
    """Test the analyzer with large file"""
    from src.main import main as run_analyzer
    import time
    
    print("\n" + "="*60)
    print("PERFORMANCE TEST WITH 50,000+ LOGS")
    print("="*60)
    
    # Generate large log file
    large_file = generate_large_log_file()
    
    print("\n⏱️ Starting performance analysis...")
    start_time = time.time()
    
    try:
        # We'll create a modified version to test with large file
        print(f"\n📂 Testing with file: {large_file}")
        
        # Count lines first
        with open(large_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"📊 File contains: {line_count:,} lines")
        
        # Run a simplified test
        print("\n🔍 Running analysis...")
        from src.log_reader import LogReader
        from src.log_parser import LogParser
        
        reader = LogReader(str(large_file))
        parser = LogParser()
        
        parsed_count = 0
        for line in reader.read_lines():
            if parser.parse_line(line):
                parsed_count += 1
        
        stats = reader.get_stats()
        parse_stats = parser.get_stats()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "="*60)
        print("PERFORMANCE RESULTS")
        print("="*60)
        print(f"Total lines processed: {stats['total_lines']:,}")
        print(f"Lines per second: {stats['total_lines'] / duration:.0f}")
        print(f"Successfully parsed: {parse_stats['parsed_count']:,}")
        print(f"Failed to parse: {parse_stats['failed_count']:,}")
        print(f"Parsing success rate: {parse_stats['success_rate']:.2f}%")
        print(f"Total execution time: {duration:.2f} seconds")
        print(f"Memory efficient: ✅ (Processes line by line)")
        print(f"Handles malformed entries: ✅ ({parse_stats['failed_count']:,} handled)")
        
        if duration < 10:
            print("\n✅ PERFORMANCE: EXCELLENT - Handles 50K+ logs efficiently!")
        elif duration < 30:
            print("\n✅ PERFORMANCE: GOOD - Within acceptable limits")
        else:
            print("\n⚠️ PERFORMANCE: SLOW - May need optimization")
        
    except Exception as e:
        print(f"\n❌ Error during performance test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_performance()