

import pandas
import numpy as np
from sklearn.linear_model import LinearRegression

import census_utilities

class GeoNN( object ):
    """
    This class implements a geoNN algo that finds the k nearest geographic neighbours. Sometimes that information is not available,
    so we must rely on a different, fall_back, algo. The fallback algo must have .fit and .predict methods.
    
    methods:
     fit(location_data, data, response): fits the data, returns an instance of the model. Ideally all pandas dataframes
     
     
     predict(location_data, data ): returns the predicted response variables, ideally pandas dataframes.

     """
    def __init__(self, kNN = 5, fall_back = LinearRegression(), knn_agg = np.mean, stdThreshHold = 5 ):
        self.K = kNN
        self.knn_agg = knn_agg
        self.fall_back = fall_back
	self.stdThreshHold = stdThreshHold
        
        
    def fit(self, data_array, response):
        """
        To inline this with other sklearn models, exdata_array must be a array of the form:
            [ exlocation_data, exdata ]
        
        Ideally both pandas dataframes.
        """
        
        location_data = data_array[0]
        data = data_array[1]
        
        self.data_ = data
        self.location_data_ = location_data
        self.response_ = response
        
        self.fall_back.fit( data, response )
        
        return self
        
    def predict(self, exdata_array, response = None ):
        """
        To inline this with other sklearn models, exdata_array must be a array of the form:
            [ exlocation_data, exdata ]
        
        Ideally both pandas dataframes.
        """
        exlocation_data = exdata_array[0]
        exdata = exdata_array[1].values
        
        
        if exlocation_data.shape[0] != exdata.shape[0]:
            raise Exception("length of first argument does not equal length of second argument.")
        
        n = exlocation_data.shape[0]
        
        prediction = np.empty( n )
	
        missing_location = 0    
        knn_ = 0
        sum_knn_ = 0
        sum_fallback_ = 0
        for i in range(n):
            location = exlocation_data.values[i,:]
            if pandas.isnull( location ).sum() > 0:
                #missing data, use fall_back
                missing_location+=1
                prediction[i] = self.fall_back.predict( exdata[i,:] )
            else:
        
                nn_responses = self.response_.ix[census_utilities.find_geo_NN( location[0], location[1], self.location_data_, self.K )]

                if nn_responses.std() > self.stdThreshHold: #arbitrary
                    prediction[i] = self.fall_back.predict( exdata[i,:] )
                    sum_fallback_ += abs( response[i] - prediction[i] )

                else:
                    knn_+=1
                    prediction[i] = self.knn_agg( nn_responses)
                    
                    sum_knn_ += abs( response[i] - prediction[i] )
	
        print "Prediction complete, using %d geo-nn, and agg function %s. "%(self.K, self.knn_agg)
        print "%f responses were generated by geo-knn, with an MAE accuracy of %f"%( float(knn_)/n, sum_knn_/knn_)
        print "Fallback had an MAE accuracy of %f"%( sum_fallback_/(1+n-knn_))
        return prediction
                
        

class GeoNNFinder( object ):
    """
    This class implements a way to find the nearest geographic neighbours.
    
    GeoNNFinder( location_data)
        location_data: a pandas 2d array of location and longtitude
        
    methods:
        
        find( lat, long, k)
     
     

     """
    def __init__(self, location_data ):
        self.location_data_ = location_data
        
    
    def find(self, lat, long, k):
        
        return census_utilities.find_geo_NN( lat, long, self.location_data_, k )

       
        
