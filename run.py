"""
Runner script - Run from main project folder
"""

import os
import sys
from pathlib import Path

print("="*60)
print("LOG FILE ANALYZER - RUNNER")
print("="*60)

# Get the project root
project_root = Path(__file__).parent
src_dir = project_root / "src"
main_file = src_dir / "main.py"

print(f"Project root: {project_root}")
print(f"Source directory: {src_dir}")
print(f"Main file: {main_file}")

# Check if main.py exists
if not main_file.exists():
    print(f"\n❌ ERROR: main.py not found at {main_file}")
    print("Files in src directory:")
    for f in os.listdir(src_dir):
        print(f"  - {f}")
    sys.exit(1)

# Change to src directory to run main.py
original_dir = os.getcwd()
try:
    os.chdir(src_dir)
    print(f"\nChanged to directory: {src_dir}")
    print(f"Current directory: {os.getcwd()}")
    
    # Add current directory to Python path
    sys.path.insert(0, str(src_dir))
    
    # Now run main.py as a script
    print("\n" + "="*60)
    print("RUNNING LOG ANALYZER...")
    print("="*60)
    
    # Execute main.py as a script
    with open("main.py", "r", encoding="utf-8") as f:
        exec(f.read())
    
    print("\n" + "="*60)
    print("RUNNER COMPLETED")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Change back to original directory
    os.chdir(original_dir)
    print(f"\nChanged back to: {original_dir}")