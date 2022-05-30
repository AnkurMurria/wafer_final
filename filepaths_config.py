class filepaths:
    def __init__(self, operation='Train'):
        self.error_log = 'logs/errorlog.txt'
        self.info_log = 'logs/infolog.txt'
        

        
        self.model_Folder = 'models/'

        if operation == 'Train':
            self.schema = 'schemas/schema_training.json'
            self.training_folder = 'Training_Batch_Files/'
            self.approved_folder = 'ValidatedFiles/ApprovedFiles/'
            self.rejected_folder = 'ValidatedFiles/RejectedFiles/'
            self.dbName = "train"
            self.dbFolder = "Databases/"
            self.FinalCSVFolder = 'FinalCSV/'
            self.FinalCSVFile = 'InputFile.csv'
        else:
            self.schema = 'schemas/schema_prediction.json'
            self.training_folder = 'Prediction_Batch_files/'
            self.approved_folder = 'ValidatedFiles_prediction/ApprovedFiles/'
            self.rejected_folder = 'ValidatedFiles_prediction/RejectedFiles/'
            self.dbName = "predict"
            self.dbFolder = "Databases_predict/"
            self.FinalCSVFolder = 'PredictCSV/'
            self.FinalCSVFile = 'InputFile_predict.csv'
