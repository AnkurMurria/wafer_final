from logs.logger import Custom_Logger
from filepaths_config import filepaths

import pandas as pd

class LoadData:
    def __init__(self, operation='Train'):
        self.logger = Custom_Logger()
        self.filepaths = filepaths(operation)
    
    def fetch_csv(self):
        try:
            data = pd.read_csv(self.filepaths.FinalCSVFolder+self.filepaths.FinalCSVFile)
            self.logger.log_data("info", "Loaded Data")
            return data
        except Exception as e:
            self.logger.log_data("error", "Data Load Failed")
            raise e
            

