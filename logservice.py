import os
from datetime import datetime

class LogService:
    def __init__(self, prefix="session"):
        log_dir = "logs"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = os.path.join(log_dir, f"{prefix}_{timestamp}.log")

        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
                print(f"[LogService] Created log directory: {log_dir}")
            except Exception as e:
                print(f"[LogService] ERROR: Could not create log directory: {e}")

        self.file = open(self.filename, "a", encoding="utf-8")
        self.write("Logger Initialized", type="INFO")

    def write(self, message, type="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{type.upper()}] {message}\n"
        
        print(line, end='') 

        self.file.write(line)
        self.file.flush()

    def close(self):
        self.write("Logger closed", type="INFO")
        self.file.close()