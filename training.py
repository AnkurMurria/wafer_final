from logs.logger import Custom_Logger

from cgi import test
from data_loader.data_loader import LoadData
from data_preprocessing.preprocessing import preprocessing
from clustering.kmeans import KMeans_Cluster
from model_search import Model_Finder
from fileio.fileio import model_io

from sklearn.model_selection import train_test_split

import pandas as pd

class training:
    def __init__(self):
        self.logger = Custom_Logger()

    def train_model(self):
        try:
            loader = LoadData()
            data = loader.fetch_csv()

            preprocessor = preprocessing()
            data = preprocessor.remove_columns(data, ['Wafer'])

            X, Y = preprocessor.getLabelsFeatures(data, labels='Output')

            check_nulls = preprocessor.checkNulls(X)
            if check_nulls:
                X = preprocessor.impute_nulls(X)
            
            #X = X.fillna(0) #temporary change
            
            dummycolumns = preprocessor.getDummyColums(X)

            X = preprocessor.remove_columns(X, dummycolumns)
            
            kmeans = KMeans_Cluster()
            number_of_clusters = kmeans.elbow_plot(X)

            X = kmeans.create_clusters(X, number_of_clusters)

            X['Labels'] = Y

            #X.to_csv("aftercluster.csv")

            unique_clusters = X['Cluster'].unique()
            
            for cluster in unique_clusters:
                cluster_data = X[X['Cluster']==cluster]

                X_cluster = cluster_data.drop(['Labels','Cluster'], axis = 1)
                Y_cluster = cluster_data['Labels']

                x_train, x_test, y_train, y_test = train_test_split(X_cluster, Y_cluster, test_size = 0.3, random_state=42)

                model_search = Model_Finder()

                model_name, model, random_forest_score, xgboost_score = model_search.get_best_model(x_train, y_train, x_test, y_test)

                save_model  = model_io()
                result = save_model.save_model(model, model_name + str(cluster))
                self.logger.log_data("info", "Model {} Created. Random forest score = {} , xgb score = {}".format(cluster, random_forest_score, xgboost_score))
            
            self.logger.log_data("info", "Models Created")
        
        except Exception as e:
            self.logger.log_data("error", "Model Creation Failed")
            raise e




