"""
Module for parsing log entries
"""

import re
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class LogParser:
    """Parses log lines and extracts fields"""
    
    def __init__(self):
        # Regex pattern for log format: timestamp,ip,request,error_code
        self.pattern = re.compile(
            r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),'
            r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}),'
            r'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH),'
            r'(\d+)$'
        )
        
        # Valid request types
        self.valid_requests = {'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'}
        
        # Statistics
        self.parsed_count = 0
        self.failed_count = 0
    
    def parse_line(self, log_line: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single log line
        
        Args:
            log_line: Raw log line string
            
        Returns:
            Dictionary with parsed fields or None if invalid
        """
        try:
            # Try to match the pattern
            match = self.pattern.match(log_line)
            
            if not match:
                self.failed_count += 1
                return None
            
            timestamp_str, ip, request_type, error_code_str = match.groups()
            
            # Validate IP address
            if not self._is_valid_ip(ip):
                self.failed_count += 1
                return None
            
            # Validate request type
            if request_type not in self.valid_requests:
                request_type = 'UNKNOWN'
            
            # Parse error code
            try:
                error_code = int(error_code_str)
                is_error = 400 <= error_code < 600  # HTTP error codes are 400-599
            except ValueError:
                error_code = 0
                is_error = False
            
            # Parse timestamp
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp = None
            
            self.parsed_count += 1
            
            return {
                'timestamp': timestamp,
                'ip_address': ip,
                'request_type': request_type,
                'error_code': error_code,
                'is_error': is_error,
                'raw_line': log_line
            }
            
        except Exception as e:
            self.failed_count += 1
            return None
    
    def _is_valid_ip(self, ip: str) -> bool:
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
    
    def get_stats(self) -> dict:
        """Get parsing statistics"""
        total = self.parsed_count + self.failed_count
        success_rate = (self.parsed_count / total * 100) if total > 0 else 0
        
        return {
            'parsed_count': self.parsed_count,
            'failed_count': self.failed_count,
            'success_rate': round(success_rate, 2)
        }