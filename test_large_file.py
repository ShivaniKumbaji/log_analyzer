"""
Test the analyzer with large log files
"""

import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

print("="*70)
print("LARGE FILE ANALYZER TEST")
print("="*70)

# Test with the large file we already generated
large_file = Path("data") / "large_server_logs.txt"

if not large_file.exists():
    print(f"\n❌ Large test file not found: {large_file}")
    print("Run: python generate_large_logs.py first")
    sys.exit(1)

print(f"\n📂 Testing with file: {large_file}")
print(f"📊 File size: {large_file.stat().st_size / (1024*1024):.2f} MB")

# Count lines
with open(large_file, 'r', encoding='utf-8') as f:
    line_count = sum(1 for _ in f)
print(f"📈 Total lines: {line_count:,}")

print("\n🚀 Starting analysis...")

# Import and run
try:
    # Change to src directory
    import os
    original_dir = os.getcwd()
    os.chdir(src_dir)
    
    # Import main module
    import main as analyzer
    
    print("\n" + "="*70)
    print("ANALYSIS STARTED")
    print("="*70)
    
    # The main module will run when imported
    # (since main.py has code that runs when __name__ == "__main__")
    
    os.chdir(original_dir)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()