from datetime import datetime
from filepaths_config import filepaths

class Custom_Logger:
    def __init__(self):
        self.logpath = filepaths()

    def log_data(self, logtype, message):
        try:
            if logtype =="error":
                path = self.logpath.error_log
            else:
                path = self.logpath.info_log
            
            self.now = datetime.now()
            self.date = self.now.date()
            self.current_time = self.now.strftime("%H:%M:%S.%f")[:-3]
            file = open(path, 'a+')
            file.write(str(self.date) + " " + str(self.current_time) + " -- " + message + "\n")
            file.close()
    
        except Exception as e:
            print("Exception in logger", e)

#import traceback
#def foo(): 
#    stack = traceback.extract_stack()
#    print(stack[-2].filename)