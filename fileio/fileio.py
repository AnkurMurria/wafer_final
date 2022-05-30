from fileinput import filename
from logs.logger import Custom_Logger
from filepaths_config import filepaths

import pickle
import os
import shutil


class model_io:

    def __init__(self):
        self.logger = Custom_Logger()
        self.filepaths = filepaths()

    def save_model(self, model, filename):
        try:
            path = os.path.join(self.filepaths.model_Folder, filename)
            if os.path.isdir(path):
                shutil.rmtree(self.filepaths.model_Folder)
                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(path + '/' + filename+'.sav', 'wb') as f:
                pickle.dump(model, f)

            self.logger.log_data("info", "Saved Model")
            return 'success'
        except Exception as e:
            self.logger.log_data("error", "Unable to save model")
            raise e


    def load_model(self,filename):
        try:
            with open(self.filepaths.model_Folder + filename + '/' + filename + '.sav',
                      'rb') as f:
                self.logger.log_data("info", "Model loaded")
                return pickle.load(f)
            
        except Exception as e:
            self.logger.log_data("error", "Model load failed")
            raise e

    def find_correct_model_file(self,cluster_number):
        try:
            self.cluster_number= cluster_number
            self.folder_name=self.filepaths.model_Folder
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if (self.file.index(str( self.cluster_number))!=-1):
                        self.model_name=self.file
                except:
                    continue

            
            self.model_name=self.model_name.split('.')[0]
            self.logger.log_data("info", "Model name found")
            return self.model_name
        except Exception as e:
            self.logger.log_data("info", "Model not found")
            raise e