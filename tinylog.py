import sys
import utime

class TinyLog:
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4
    
    # Map log levels to their single-character representation
    _LEVEL_CHARS = {
        DEBUG: 'D',
        INFO: 'I',
        WARN: 'W',
        ERROR: 'E',
        CRITICAL: 'C'
    }

    def __init__(self, log_level: int):
        self.log_level = log_level
    
    def _log(self, level: int, message: str):
        if level >= self.log_level:
            timestamp = utime.time()
            level_char = self._LEVEL_CHARS.get(level, '?')
            print(f'[{level_char}][{timestamp}]: {message}')
            
    def debug(self, message: str):
        self._log(self.DEBUG, message)
        
    def info(self, message: str):
        self._log(self.INFO, message)
        
    def warn(self, message: str):
        self._log(self.WARN, message)
        
    def error(self, message: str):
        self._log(self.ERROR, message)
        
    def critical(self, message: str):
        self._log(self.CRITICAL, message)