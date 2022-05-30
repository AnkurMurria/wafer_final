from logs.logger import Custom_Logger
from filepaths_config import filepaths
import pandas as pd
from os import listdir

class dataTransform:
    def __init__(self, operation='Train'):
        self.logger = Custom_Logger()
        self.filepaths = filepaths(operation)
    
    def replaceMissingWithNull(self):
        try:
            filelist = listdir(self.filepaths.approved_folder)
            path = self.filepaths.approved_folder
            
            for filename in filelist:
                fileContent = pd.read_csv(path + filename)
                fileContent.fillna('NULL', inplace=True)
                fileContent['Wafer'] = fileContent['Wafer'].str[6:]
                fileContent.to_csv(self.filepaths.approved_folder + filename, index = None, header=True)
            
            self.logger.log_data("info", "Replaced missing values with NULL")
        except Exception as e:
            self.logger.log_data("error", "Replace missing values with NULL failed")
            raise e