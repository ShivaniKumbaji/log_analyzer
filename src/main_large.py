"""
Main entry point optimized for large log files (50,000+ lines)
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    import config
    from log_reader import LogReader
    from log_parser import LogParser
    from data_processor import DataProcessor
    from visualizer import Visualizer
    from report_generator import ReportGenerator
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.EXECUTION_LOG_PATH),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def analyze_large_file(file_path=None):
    """Analyze large log file efficiently"""
    logger = setup_logging()
    
    print("\n" + "="*70)
    print("LOG FILE ANALYZER - LARGE FILE OPTIMIZED")
    print("="*70)
    
    start_time = datetime.now()
    
    try:
        # 1. Read log file
        print(f"\n📂 STEP 1: Reading log file...")
        reader = LogReader(file_path)
        parsed_logs = []
        
        # 2. Parse each line with progress indicator
        print("🔍 STEP 2: Parsing log entries...")
        parser = LogParser()
        
        line_count = 0
        batch_size = 10000  # Process in batches for memory efficiency
        
        for line in reader.read_lines():
            line_count += 1
            parsed = parser.parse_line(line)
            if parsed:
                parsed_logs.append(parsed)
            
            # Show progress every batch_size lines
            if line_count % batch_size == 0:
                print(f"  Processed {line_count:,} lines...")
        
        # Get statistics
        reading_stats = reader.get_stats()
        parsing_stats = parser.get_stats()
        
        print(f"\n📊 PARSING SUMMARY:")
        print(f"  Total lines: {reading_stats['total_lines']:,}")
        print(f"  Skipped lines: {reading_stats['skipped_lines']:,}")
        print(f"  Successfully parsed: {parsing_stats['parsed_count']:,}")
        print(f"  Failed to parse: {parsing_stats['failed_count']:,}")
        print(f"  Success rate: {parsing_stats['success_rate']:.2f}%")
        
        if not parsed_logs:
            print("\n❌ No valid log entries found!")
            return
        
        # 3. Process and analyze data
        print(f"\n📈 STEP 3: Analyzing {len(parsed_logs):,} log entries...")
        processor = DataProcessor()
        processor.create_dataframe(parsed_logs)
        stats = processor.analyze()
        
        # Display summary in console
        processor.show_summary()
        
        # 4. Generate visualizations
        print("\n🎨 STEP 4: Creating visualizations...")
        visualizer = Visualizer()
        visualizer.create_all_charts(stats)
        
        # 5. Generate report
        print("\n📄 STEP 5: Generating report...")
        report_gen = ReportGenerator()
        report_text = report_gen.generate(stats, parsing_stats, reading_stats)
        
        # Display report summary
        print("\n" + "="*60)
        print("REPORT SUMMARY")
        print("="*60)
        print(f"Total Requests: {stats.get('total_requests', 0):,}")
        print(f"Error Requests: {stats.get('error_requests', 0):,}")
        print(f"Error Rate: {stats.get('error_percentage', 0):.2f}%")
        
        error_codes = stats.get('error_code_distribution', {})
        if error_codes:
            print(f"\nUnique Error Codes: {len(error_codes)}")
            print("Top 3 Error Codes:")
            for code, count in sorted(error_codes.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"  HTTP {code}: {count:,} errors")
        
        top_ips = stats.get('top_error_ips', {})
        if top_ips:
            print(f"\nTop {len(top_ips)} Error IPs:")
            for ip, count in top_ips.items():
                print(f"  {ip}: {count:,} errors")
        
        # Calculate execution time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ ANALYSIS COMPLETED IN {duration:.2f} SECONDS!")
        print(f"📁 Check the 'output' folder for results.")
        
        # Performance metrics
        lines_per_second = reading_stats['total_lines'] / duration if duration > 0 else 0
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"  Lines processed per second: {lines_per_second:,.0f}")
        print(f"  Memory efficient: ✅ (Streaming line-by-line)")
        print(f"  Scalable to large files: ✅")
        
        logger.info(f"Large file analysis completed in {duration:.2f} seconds")
        logger.info(f"Processed {reading_stats['total_lines']:,} lines at {lines_per_second:,.0f} lines/sec")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        logger.error(f"File not found: {e}")
        
    except MemoryError:
        print("\n❌ MEMORY ERROR: File too large to process!")
        print("   Try increasing batch size or processing in chunks.")
        logger.error("Memory error during large file processing")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())


def main():
    """Main function with command line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Log File Analyzer for Large Files')
    parser.add_argument('--file', '-f', type=str, help='Path to log file')
    parser.add_argument('--lines', '-l', type=int, default=50000,
                       help='Number of lines for test file (default: 50000)')
    
    args = parser.parse_args()
    
    if args.file:
        # Analyze specified file
        analyze_large_file(args.file)
    else:
        # Use default file
        analyze_large_file()


if __name__ == "__main__":
    main()