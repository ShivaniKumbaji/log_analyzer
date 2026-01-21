"""
Module for reading log files
"""

import logging
from pathlib import Path

# Import config using absolute path
try:
    # Try relative import first
    from .config import DEFAULT_INPUT_FILE
except ImportError:
    # Fall back to absolute import
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from config import DEFAULT_INPUT_FILE

logger = logging.getLogger(__name__)


class LogReader:
    """Reads log files line by line"""
    
    def __init__(self, file_path: str = None):
        """
        Initialize LogReader
        
        Args:
            file_path: Path to log file (optional)
        """
        if file_path:
            self.file_path = Path(file_path)
        else:
            self.file_path = DEFAULT_INPUT_FILE
            
        self.skipped_lines = 0
        self.total_lines = 0
        
    def validate_file(self) -> bool:
        """Check if file exists and is readable"""
        if not self.file_path.exists():
            print(f"❌ ERROR: File not found: {self.file_path}")
            return False
        
        if self.file_path.stat().st_size == 0:
            print(f"⚠️ WARNING: File is empty: {self.file_path}")
            return False
            
        print(f"✅ File validated: {self.file_path}")
        return True
    
    def read_lines(self):
        """
        Read file line by line
        
        Yields:
            Each line from the file
        """
        if not self.validate_file():
            return []
        
        print(f"📖 Reading file: {self.file_path}")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    self.total_lines += 1
                    line = line.strip()
                    
                    if not line:  # Skip empty lines
                        self.skipped_lines += 1
                        continue
                        
                    yield line
                    
            print(f"✅ Finished reading. Total lines: {self.total_lines}")
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            yield from []  # Return empty generator
    
    def get_stats(self) -> dict:
        """Get reading statistics"""
        return {
            'total_lines': self.total_lines,
            'skipped_lines': self.skipped_lines,
            'valid_lines': self.total_lines - self.skipped_lines
        }