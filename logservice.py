import os
from datetime import datetime

class LogService:
    def __init__(self, prefix="session"):
        self.prefix = prefix
        self.write("Logger Initialized", type="INFO")

    def write(self, message, type="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{type.upper()}] {message}\n"
        print(line, end='') 

    def close(self):
        self.write("Logger closed", type="INFO")