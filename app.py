"""
Flask Web Interface for Log File Analyzer
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
import threading
import json
import time

# Add src to path for analyzer imports
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# Import analyzer modules
try:
    from log_reader import LogReader
    from log_parser import LogParser
    from data_processor import DataProcessor
    from visualizer import Visualizer
    from report_generator import ReportGenerator
    print("✅ Analyzer modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Create mock functions for testing
    def mock_analyze(file_path):
        return {
            'status': 'error',
            'message': 'Analyzer modules not loaded properly'
        }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = project_root / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['OUTPUT_FOLDER'] = project_root / 'output'

# Create folders if they don't exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
    folder.mkdir(exist_ok=True)

def analyze_log_file(file_path):
    """Analyze log file and return results"""
    try:
        print(f"📂 Analyzing file: {file_path}")
        
        # Initialize analyzer components
        reader = LogReader(file_path)
        parser = LogParser()
        
        # Parse log file
        parsed_logs = []
        line_count = 0
        
        print("🔍 Parsing log entries...")
        for line in reader.read_lines():
            line_count += 1
            parsed = parser.parse_line(line)
            if parsed:
                parsed_logs.append(parsed)
            
            # Show progress every 5000 lines
            if line_count % 5000 == 0:
                print(f"  Processed {line_count:,} lines...")
        
        # Get statistics
        reading_stats = reader.get_stats()
        parsing_stats = parser.get_stats()
        
        if not parsed_logs:
            return {
                'status': 'error',
                'message': 'No valid log entries found'
            }
        
        # Process and analyze data
        print("📈 Processing data...")
        processor = DataProcessor()
        processor.create_dataframe(parsed_logs)
        stats = processor.analyze()
        
        # Generate visualizations
        print("🎨 Creating visualizations...")
        visualizer = Visualizer()
        
        # Save charts with unique names
        timestamp = int(time.time())
        error_chart = app.config['OUTPUT_FOLDER'] / f'error_distribution_{timestamp}.png'
        ip_chart = app.config['OUTPUT_FOLDER'] / f'top_ips_{timestamp}.png'
        
        visualizer.output_path = error_chart
        visualizer.plot_error_distribution(stats)
        
        visualizer.output_path = ip_chart
        visualizer.plot_top_ips(stats)
        
        # Generate report
        print("📄 Generating report...")
        report_gen = ReportGenerator()
        report_file = app.config['OUTPUT_FOLDER'] / f'summary_report_{timestamp}.txt'
        report_gen.output_path = report_file
        report_text = report_gen.generate(stats, parsing_stats, reading_stats)
        
        # Prepare response data
        result = {
            'status': 'success',
            'file_name': Path(file_path).name,
            'file_size': os.path.getsize(file_path),
            'total_lines': reading_stats['total_lines'],
            'parsed_lines': parsing_stats['parsed_count'],
            'failed_lines': parsing_stats['failed_count'],
            'success_rate': parsing_stats['success_rate'],
            'total_requests': stats.get('total_requests', 0),
            'error_requests': stats.get('error_requests', 0),
            'success_requests': stats.get('success_requests', 0),
            'error_percentage': stats.get('error_percentage', 0),
            'unique_ips': stats.get('unique_ips', 0),
            'unique_error_ips': stats.get('unique_error_ips', 0),
            'error_codes': stats.get('error_code_distribution', {}),
            'top_ips': stats.get('top_error_ips', {}),
            'request_types': stats.get('request_type_distribution', {}),
            'charts': {
                'error_distribution': f'/download/{error_chart.name}',
                'top_ips': f'/download/{ip_chart.name}'
            },
            'report': f'/download/{report_file.name}',
            'timestamp': timestamp
        }
        
        print(f"✅ Analysis completed successfully")
        return result
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'message': str(e)
        }

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    if 'log_file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})
    
    file = request.files['log_file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})
    
    if file:
        # Save uploaded file
        filename = file.filename
        file_path = app.config['UPLOAD_FOLDER'] / filename
        file.save(file_path)
        
        # Analyze the file
        result = analyze_log_file(str(file_path))
        
        # Add file info to result
        result['uploaded_file'] = filename
        
        return jsonify(result)

@app.route('/analyze/default')
def analyze_default():
    """Analyze the default large log file"""
    default_file = project_root / 'data' / 'large_server_logs.txt'
    
    if not default_file.exists():
        return jsonify({
            'status': 'error',
            'message': 'Default log file not found'
        })
    
    result = analyze_log_file(str(default_file))
    result['file_name'] = 'large_server_logs.txt'
    
    return jsonify(result)

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated files"""
    file_path = app.config['OUTPUT_FOLDER'] / filename
    
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/status')
def status():
    """Check server status"""
    return jsonify({
        'status': 'running',
        'analyzer': 'ready',
        'max_file_size': '100MB'
    })

if __name__ == '__main__':
    print("="*60)
    print("LOG FILE ANALYZER WEB INTERFACE")
    print("="*60)
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"📊 Output folder: {app.config['OUTPUT_FOLDER']}")
    print(f"🌐 Server starting on http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)