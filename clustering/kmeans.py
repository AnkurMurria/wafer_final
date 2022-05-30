from logs.logger import Custom_Logger
from filepaths_config import filepaths
from fileio.fileio import model_io

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator

class KMeans_Cluster:
    def __init__(self):
        self.logger = Custom_Logger()
        self.filepaths = filepaths()
    
    def elbow_plot(self, data):
        try:
            wcss = []
            for i in range (1, 11):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger.log_data("info", "Elbow Plot Done")
            return self.kn.knee
        except Exception as e:
            self.logger.log_data("error", "Elbow Plot Failed")
            raise e
    
    def create_clusters(self, data, number_of_clusters):
        try:
            self.data = data
            self.kmeans = KMeans(n_clusters = number_of_clusters, init = 'k-means++', random_state=42)
            self.y_means = self.kmeans.fit_predict(data)
            
            self.file_op = model_io()
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans') # saving the KMeans model to directory
            
            self.data['Cluster']=self.y_means  # create a new column in dataset for storing the cluster information                                                                                    
                                                # passing 'Model' as the functions need three parameters
            
            self.logger.log_data("info", "Cluster Created")
            return self.data
        except Exception as e:
            self.logger.log_data("error", "Cluster Failed")
            raise e
        
        