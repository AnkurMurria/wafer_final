from logs.logger import Custom_Logger

from Validations.dataValidations import data_Validator
from Transformation.dataTransformation import dataTransform
from dbOperations.db import db

class validations:
    def __init__(self, operation='Train'):
        self.logger = Custom_Logger()
        self.operation = operation


    def validate_model(self):
        try:
            validation=data_Validator("test", self.operation)
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns = validation.schemainformation()

            validation.validateFileNames(LengthOfDateStampInFile, LengthOfTimeStampInFile)
            validation.validateNumberOfColumns(NumberofColumns)
            validation.ValidateBlankColumns()

            transform = dataTransform(self.operation)
            transform.replaceMissingWithNull()

            dbops = db(self.operation)
            dbops.createTable(column_names)
            dbops.insertIntoTable()
            dbops.tableToCSV()
        
            self.logger.log_data("info", "Created new csv")
        except Exception as e:
            self.logger.log_data("error", "Error Validating data")
            raise e