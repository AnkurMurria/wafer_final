import sqlite3
from os import listdir
import csv
from logs.logger import Custom_Logger
from filepaths_config import filepaths
import os

class db:
    def __init__(self, operation='Train'):
        self.logger = Custom_Logger()
        self.filepaths = filepaths(operation)

    def connect(self):
        try:
            conn = sqlite3.connect(self.filepaths.dbFolder+self.filepaths.dbName+'.db')
            self.logger.log_data("info", "Connected to db")
            return conn
        except Exception as e:
            self.logger.log_data("error", "db Connection failed")
            raise e



    def createTable(self, columnNames):
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.execute("DELETE FROM Good_Raw_Data")
                conn.commit()
                conn.close()
            else:
                for columnName, dataType in columnNames.items():
                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=columnName,dataType=dataType))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=columnName, dataType=dataType))
                conn.close()
            
            self.logger.log_data("info", "Created table")
        except Exception as e:
            self.logger.log_data("error", "Table Creation failed")
            conn.close()
            raise e



    def insertIntoTable(self):
        try:
            conn = self.connect()
            filePath = self.filepaths.approved_folder
            files = listdir(filePath)
            
            for file in files:
                with open(filePath+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                            conn.commit()
            
            conn.close()

            self.logger.log_data("info", "Inserted data into table")
        except Exception as e:
            self.logger.log_data("error", "Table Insertion failed")
            conn.close()
            raise e
        
    

    def tableToCSV(self):
        try:
            conn = self.connect()
            self.fileFromDb = self.filepaths.FinalCSVFolder
            self.fileName = self.filepaths.FinalCSVFile
            
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlSelect)
            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]
            
            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)
            
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)
            
            conn.close()

            self.logger.log_data("info", "Created CSV")

        except Exception as e:
            self.logger.log_data("error", "CSV Creation failed")
            conn.close()
            raise e
        
        
        