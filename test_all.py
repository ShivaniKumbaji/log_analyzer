"""
Test script to verify everything works
"""

import os
import sys
from pathlib import Path

print("="*60)
print("COMPREHENSIVE TEST")
print("="*60)

# 1. Check Python and packages
print("\n1. CHECKING PYTHON AND PACKAGES")
print("-"*40)

try:
    import pandas as pd
    print(f"✅ pandas {pd.__version__}")
except ImportError:
    print("❌ pandas not installed")

try:
    import matplotlib
    print(f"✅ matplotlib {matplotlib.__version__}")
except ImportError:
    print("❌ matplotlib not installed")

# 2. Check folder structure
print("\n2. CHECKING FOLDER STRUCTURE")
print("-"*40)

folders = ['data', 'src', 'logs', 'output', 'tests']
for folder in folders:
    if os.path.exists(folder):
        print(f"✅ {folder}/")
        if folder == 'data':
            files = os.listdir(folder)
            print(f"   Files: {files}")
    else:
        print(f"❌ {folder}/")

# 3. Check data file
print("\n3. CHECKING DATA FILE")
print("-"*40)

data_file = Path("data") / "server_logs.txt"
if data_file.exists():
    print(f"✅ {data_file}")
    with open(data_file, 'r') as f:
        lines = f.readlines()
        print(f"   Lines: {len(lines)}")
        print("   First 3 lines:")
        for i, line in enumerate(lines[:3]):
            print(f"   {i+1}. {line.strip()}")
else:
    print(f"❌ {data_file} not found")

# 4. Check src files
print("\n4. CHECKING SOURCE FILES")
print("-"*40)

src_files = ['config.py', 'log_reader.py', 'log_parser.py', 
             'data_processor.py', 'visualizer.py', 
             'report_generator.py', 'main.py']

for file in src_files:
    file_path = Path("src") / file
    if file_path.exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")

# 5. Test imports
print("\n5. TESTING IMPORTS")
print("-"*40)

# Change to src directory to test imports
original_dir = os.getcwd()
os.chdir("src")

try:
    import config
    print("✅ config.py")
except ImportError as e:
    print(f"❌ config.py: {e}")

try:
    from log_reader import LogReader
    print("✅ LogReader")
except ImportError as e:
    print(f"❌ LogReader: {e}")

try:
    from log_parser import LogParser
    print("✅ LogParser")
except ImportError as e:
    print(f"❌ LogParser: {e}")

# Change back
os.chdir(original_dir)

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)