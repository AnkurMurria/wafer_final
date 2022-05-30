from data_loader.data_loader import LoadData
from data_preprocessing.preprocessing import preprocessing
from fileio.fileio import model_io
import pandas 

from logs.logger import Custom_Logger

class prediction:
    def __init__(self):
        self.logger = Custom_Logger()
        self.operation = 'Predict'

    def predict_values(self):
        loader = LoadData(self.operation)
        data = loader.fetch_csv()

        preprocessor = preprocessing()

        check_nulls = preprocessor.checkNulls(data)
        if check_nulls:
            data = preprocessor.impute_nulls(data)
            
        #data = data.fillna(0) #temporary change

        dummycolumns = preprocessor.getDummyColums(data)

        data = preprocessor.remove_columns(data, dummycolumns)

        file_loader  = model_io()

        kmeans=file_loader.load_model('KMeans')

        clusters=kmeans.predict(data.drop(['Wafer'],axis=1))#drops the first column for cluster prediction
        data['clusters']=clusters
        clusters=data['clusters'].unique()

        #clear the csv before insertion
        csvtoclear = "Prediction_Output_File/Predictions.csv"
        f = open(csvtoclear, "w+")
        f.close()

        for i in clusters:
            cluster_data= data[data['clusters']==i]
            wafer_names = list(cluster_data['Wafer'])
            cluster_data=data.drop(labels=['Wafer'],axis=1)
            cluster_data = cluster_data.drop(['clusters'],axis=1)
            model_name = file_loader.find_correct_model_file(i)
            model = file_loader.load_model(model_name)
            result=list(model.predict(cluster_data))
            result = pandas.DataFrame(list(zip(wafer_names,result)),columns=['Wafer','Prediction'])
            path="Prediction_Output_File/Predictions.csv"
            result.to_csv("Prediction_Output_File/Predictions.csv",header=True,mode='a+') #appends result to prediction file
        
        self.logger.log_data("info", "Prediction Done")

        return path, result.head().to_json(orient="records")