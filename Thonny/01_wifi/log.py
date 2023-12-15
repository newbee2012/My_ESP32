import config
class Log:
    def __init__(self, level="INFO"):
        self.level = level.upper()
        
    def debug(self, str):
        if self.level == "DEBUG":
            print(str)
            
    def info(self, str):
        if self.level == "DEBUG" or self.level == "INFO":
            print(str)
        
    def error(self, str):
        print(str)

logger = Log(config.log_level)