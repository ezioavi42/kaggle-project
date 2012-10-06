#quadratic variable selection


from itertools import combinations

run data_explorying.py


vdata = data.values
ix = []
n,d = vdata.shape

#there are d*(d-1)/2 different combinations.

qdata = np.zeros( (n, d*(d-1)/2 ) )

for col_pos, i,j in enumerate( combinations( range(d), 2) ):
    qdata[:, col_pos] = vdata[:,i]*v[:,j]
    ix.append( (i,j) )
    

    
lr = sklm.Lasso( alpha = .001, normalize = True)
lr.fit( qdata, response)

print "Percent of variables selected: %.2f"%( float(np.nonzero( lr.coef_ ).shape[0])/(d*(d-1)/2)
print "indexes:"
print np.nonzero( lr.coef_ )
