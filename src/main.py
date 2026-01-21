"""
Main entry point for Log File Analyzer
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

# Now import our modules
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
    print("Current directory:", os.getcwd())
    print("Files in src directory:", os.listdir('.'))
    sys.exit(1)


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.EXECUTION_LOG_PATH),
            logging.StreamHandler()  # Also print to console
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Main function"""
    print("\n" + "="*60)
    print("LOG FILE ANALYZER")
    print("="*60)
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Log Analyzer")
    
    start_time = datetime.now()
    
    try:
        # 1. Read log file
        print("\n📂 STEP 1: Reading log file...")
        reader = LogReader()
        parsed_logs = []
        
        # 2. Parse each line
        print("🔍 STEP 2: Parsing log entries...")
        parser = LogParser()
        
        for line in reader.read_lines():
            parsed = parser.parse_line(line)
            if parsed:
                parsed_logs.append(parsed)
        
        # Get statistics
        reading_stats = reader.get_stats()
        parsing_stats = parser.get_stats()
        
        print(f"\n📊 Parsing Results:")
        print(f"  Total lines: {reading_stats['total_lines']}")
        print(f"  Skipped lines: {reading_stats['skipped_lines']}")
        print(f"  Successfully parsed: {parsing_stats['parsed_count']}")
        print(f"  Failed to parse: {parsing_stats['failed_count']}")
        print(f"  Success rate: {parsing_stats['success_rate']}%")
        
        # 3. Process and analyze data
        print("\n📈 STEP 3: Analyzing data...")
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
        
        # Display report in console
        report_gen.display_report(report_text)
        
        # Calculate execution time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Analysis completed in {duration:.2f} seconds!")
        print(f"📁 Check the 'output' folder for results.")
        
        logger.info(f"Analysis completed successfully in {duration:.2f} seconds")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("Please make sure 'data/server_logs.txt' exists.")
        logger.error(f"File not found: {e}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()