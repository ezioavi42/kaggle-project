

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
    def __init__(self, kNN = 5, fall_back = LinearRegression(), knn_agg = np.mean ):
        self.K = kNN
        self.knn_agg = knn_agg
        self.fall_back = fall_back
        
        
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
        
    def predict(self, exdata_array ):
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
        for i in range(n):
	    location = exlocation_data.values[i,:]
            if pandas.isnull( location ).sum() > 0:
                #missing data, use fall_back
		missing_location+=1
                prediction[i] = self.fall_back.predict( exdata[i,:] )
            else:
		
                nn_responses = self.response_.ix[census_utilities.find_geo_NN( location[0], location[1], self.location_data_, self.K )]
        	print nn_responses.std()	
		if nn_responses.std() > 5: #arbitrary
			prediction[i] = self.fall_back.predict( exdata[i,:] )
		else:
			knn_+=1
			prediction[i] = self.knn_agg( nn_responses)
	
	print "Prediction complete, using %d geo-nn. There were %d missing locations, accounting for %f of the response. %f responses were generated by geo-knn."%(self.K, missing_location, float(missing_location)/n, float(knn_)/n)
        return prediction
            
        
                
        
