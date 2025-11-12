import uuid
import json
from typing import List
import datetime

class LoggerLineType:
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"

class LoggerLine:
    def __init__(self, type: LoggerLineType, message: str):
        self.type = type
        self.message = message
    
    def __str__(self):
        return f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{self.type}]: {self.message}"

    __repr__ = __str__

class SpecialLogger:
    def __init__(self):
        self.filename = f"logs_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.logs: List[LoggerLine] = []

    def info(self, message: str):
        self.logs.append(LoggerLine(LoggerLineType.INFO, message))
        self.save()

    def warning(self, message: str):
        self.logs.append(LoggerLine(LoggerLineType.WARNING, message))
        self.save()
    
    def error(self, message: str):
        self.logs.append(LoggerLine(LoggerLineType.ERROR, message))
        self.save()

    def save(self):
        with open(self.filename + ".log", "w") as f:
            for log_line in self.logs:
                f.write(str(log_line) + "\n")
    
    def save_json(self, object):
        with open(self.filename + ".json", "w") as f:
            f.write(json.dumps(object))

loggy = SpecialLogger()