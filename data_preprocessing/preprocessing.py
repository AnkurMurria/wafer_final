from logs.logger import Custom_Logger
from filepaths_config import filepaths

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class preprocessing:
    def __init__(self):
        self.logger = Custom_Logger()
        self.filepaths = filepaths()
    

    def remove_columns(self, data, columns):
        try:
            data = data.drop(labels=columns, axis = 1)
            self.logger.log_data("info", "Dropped Columns")
            return data
        except Exception as e:
            self.logger.log_data("error", "Column Drop Failed")
            raise e


        
    def getLabelsFeatures(self, data, labels):
        try:
            X = data.drop(labels=labels, axis = 1)
            Y = data[labels]
            self.logger.log_data("info", "separated labels and features")
            return X,Y
        except Exception as e:
            self.logger.log_data("error", "label separation failed")
            raise e

        
    def checkNulls(self, data):
        try:
            is_null = False
            nulls = data.isna().sum()
            for nullcount in nulls:
                if nullcount > 0:
                    is_null = True
                    break
            
            self.logger.log_data("info", "Null check completed")
            return is_null

        except Exception as e:
            self.logger.log_data("error", "Null check failed")
            raise e
    
    def impute_nulls(self, data):
        try:
            self.data = data
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            self.new_data=pd.DataFrame(data=self.new_array, columns=self.data.columns)
            
            self.logger.log_data("info", "Null's imputed")
            return self.new_data
        except Exception as e:
            self.logger.log_data("error", "Null imputation failed")
            raise e
        
    def getDummyColums(self, data):
        try:
            self.data = data
            self.columns = data.columns
            self.description = data.describe()
            self.columns_to_drop = []
            
            for i in self.columns:
                if self.description[i]['std'] == 0:
                    self.columns_to_drop.append(i)
            
            self.logger.log_data("info", "getDummyColums")
            return self.columns_to_drop
        
        except Exception as e:
            self.logger.log_data("info", "getDummyColums failed")
            raise e
        
        