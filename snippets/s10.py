import numpy as np
from scipy import spatial, optimize

#from sklearn import neighbors as nn

from matplotlib import pylab as pl

k = 8
a = 20

_x = np.linspace(0, 100, 50)
_y = np.linspace(0, 100, 50)

xx, yy = np.meshgrid(_x, _y)

X = np.array(zip(xx.ravel(), yy.ravel()))

def knn(X, k, pos):
#     knn = nn.NearestNeighbors(n_neighbors=k, 
#                               metric='euclidean').fit(X)
#     #print knn.kneighbors(X, k, return_distance=True)
#     _d, _i = knn.kneighbors([0,0], k, return_distance=True)

    tree = spatial.KDTree(X)
    _d, _i = tree.query([0,0], k)
#    print np.ndarray(_d[0])
#    print np.array(_i[0])
    #print _d[0], _i[0], X[_i[0]]
#    print _d, _i, X[_i]

    
#     pl.scatter(xx.ravel(), yy.ravel())
#     pl.scatter(X[_i, 0], X[_i, 1], 100, 'y', 's', alpha=0.5)
#     pl.xlim(xmin=0)
#     pl.ylim(ymin=0)
#     
#     pl.show()

    return max(  np.abs(X[_i, pos])  )

#exit()


def f(x, a, k):
    return x[0] + a*x[1]

def time_constraint(x, *kargs, **kwargs):
    return x[0] - knn(X, k, pos=0)

def space_constraint(x, *kargs, **kwargs):
    return x[1] - knn(X, k, pos=1)


x0 = np.array([1, 1])

hi, di = optimize.fmin_slsqp(   f, 
                                x0, 
                                args=(a, k),
                                ieqcons=[time_constraint, 
                                         space_constraint],
                                full_output=False)
print hi, di

    
pl.scatter(xx.ravel(), yy.ravel(), c='y', marker='x')
#pl.scatter(X[_i, 0], X[_i, 1], 100, 'y', 's', alpha=0.5)
pl.xlim(xmin=0)
pl.ylim(ymin=0)

pl.axhline(di)
pl.axvline(hi)

pl.show()

