"""
Proper launcher for Log File Analyzer
"""

import os
import sys
from pathlib import Path

def main():
    """Launch the log analyzer"""
    print("\n" + "="*60)
    print("LOG FILE ANALYZER LAUNCHER")
    print("="*60)
    
    # Get paths
    project_root = Path(__file__).parent
    src_dir = project_root / "src"
    
    # Check if we can run the analyzer
    requirements = [
        (src_dir / "main.py", "main.py"),
        (project_root / "data" / "server_logs.txt", "data file"),
        (src_dir / "__init__.py", "__init__.py")
    ]
    
    print("\nChecking requirements...")
    all_ok = True
    for path, name in requirements:
        if path.exists():
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: NOT FOUND at {path}")
            all_ok = False
    
    if not all_ok:
        print("\n❌ Some requirements are missing. Please check above.")
        return
    
    # Change to src directory and run
    print(f"\nChanging to: {src_dir}")
    original_dir = os.getcwd()
    os.chdir(src_dir)
    
    try:
        # Import and run main
        print("\n" + "="*60)
        print("STARTING LOG ANALYZER...")
        print("="*60)
        
        # Clear any cached modules
        if 'main' in sys.modules:
            del sys.modules['main']
        
        # Run the main module
        exec(open("main.py").read())
        
    except Exception as e:
        print(f"\n❌ Error running analyzer: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Return to original directory
        os.chdir(original_dir)
        print(f"\nReturned to: {original_dir}")
    
    print("\n" + "="*60)
    print("LAUNCHER COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()