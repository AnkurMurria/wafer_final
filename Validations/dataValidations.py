import json
import shutil
import os
import re
import pandas as pd
from os import listdir
from logs.logger import Custom_Logger
from filepaths_config import filepaths

class data_Validator:
    def __init__(self, path, operation='Train'):
        self.logger = Custom_Logger()
        self.filepaths = filepaths(operation)



    def schemainformation(self):
        try:
            with open(self.filepaths.schema) as file:
                json_schema = json.load(file)
                file.close()
            
            FileName = json_schema['SampleFileName']
            LengthOfDateStampInFile = json_schema['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = json_schema['LengthOfTimeStampInFile']
            column_names = json_schema['ColName']
            NumberofColumns = json_schema['NumberofColumns']

            self.logger.log_data("info", "loaded the schema")
            
            return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns
        except Exception as e:
            self.logger.log_data("error","Error loading schema information")
            raise e

    

    def fileNameRegex(self):
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex



    def deleteFolder(self, folderpath):
        try:
            if os.path.isdir(folderpath):
                shutil.rmtree(folderpath)
            
            self.logger.log_data("info", "Deleted folder")
        except Exception as e:
            self.logger.log_data("error", "folder deletion failed")
            raise e



    def createFolder(self, folderpath):
        try:
            if not os.path.isdir(folderpath):
                os.makedirs(folderpath)
                    
            self.logger.log_data("info", "created folder")
        except Exception as e:
            self.logger.log_data("error", "folder creation failed")
            raise e
    


    def validateFileNames(self,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        try:
            regex = self.fileNameRegex()
            filelist = listdir(self.filepaths.training_folder)
            
            self.deleteFolder(self.filepaths.approved_folder)
            self.deleteFolder(self.filepaths.rejected_folder)
            self.createFolder(self.filepaths.approved_folder)
            self.createFolder(self.filepaths.rejected_folder)
            for filename in filelist:
                if(re.match(regex, filename)):
                    split_removecsv = re.split(".csv", filename)
                    split_datetime = re.split("_", split_removecsv[0])
                    if len(split_datetime[1]) == LengthOfDateStampInFile:
                        if len(split_datetime[2]) == LengthOfTimeStampInFile:
                            shutil.copy(self.filepaths.training_folder+filename,self.filepaths.approved_folder)
                        else:
                            shutil.copy(self.filepaths.training_folder+filename,self.filepaths.rejected_folder)
                    else:
                        shutil.copy(self.filepaths.training_folder+filename,self.filepaths.rejected_folder)
                else:
                    shutil.copy(self.filepaths.training_folder+filename,self.filepaths.rejected_folder)
            self.logger.log_data("info","validated file names")
        except Exception as e:
            self.logger.log_data("error","file names validation failed")
            raise e
            
        
    def validateNumberOfColumns(self, NumberofColumns):
        try:
            filelist = listdir(self.filepaths.approved_folder)
            NumberofColumns = NumberofColumns
            
            for filename in filelist:
                csv = pd.read_csv(self.filepaths.approved_folder + filename)
                if csv.shape[1] == NumberofColumns:
                    pass
                else:
                    shutil.move(self.filepaths.approved_folder + filename,self.filepaths.rejected_folder)
            
            self.logger.log_data("info","validated Number of columns")
        except Exception as e:
            self.logger.log_data("error","Number of columns validation failed")
            raise e
                
    def ValidateBlankColumns(self):
        try:
            filelist = listdir(self.filepaths.approved_folder)
            
            for filename in filelist:
                csv = pd.read_csv(self.filepaths.approved_folder + filename)
                file_moved = 0
                for column in csv:
                    if(csv[column].count() == 0):
                        file_moved = 1
                        shutil.move(self.filepaths.approved_folder + filename,self.filepaths.rejected_folder)
                        break
                
                if file_moved == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(self.filepaths.approved_folder + filename, index=None, header=True)

            self.logger.log_data("info","validated blank columns")
        except Exception as e:
            self.logger.log_data("error","blank column validation failed")
            raise e
                
            
        
