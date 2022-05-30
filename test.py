#from ast import Load
#from logs.logger import Custom_Logger
from Validations.dataValidations import data_Validator
from Transformation.dataTransformation import dataTransform
from dbOperations.db import db

#obj = Custom_Logger()
#obj.log_data("info", "info message 5")


#obj=data_Validator("test")
#LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns = obj.schemainformation()
#print("LengthOfDateStampInFile", LengthOfDateStampInFile)
#print("LengthOfTimeStampInFile", LengthOfTimeStampInFile)
#print("column_names", LengthOfDateStampInFile)
#print("NumberofColumns", NumberofColumns)

#obj.createFolder("sample/sam/s1")

#obj.validateFileNames(LengthOfDateStampInFile, LengthOfTimeStampInFile)
#obj.validateNumberOfColumns(NumberofColumns)
#obj.ValidateBlankColumns()

#obj2 = dataTransform()
#obj2.replaceMissingWithNull()

#obj3 = db()
#obj3.createTable(column_names)
#obj3.insertIntoTable()
#bj3.tableToCSV()

from data_loader.data_loader import LoadData

obj = LoadData()
data = obj.fetch_csv()
print(data)