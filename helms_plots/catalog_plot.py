import numpy as np
import matplotlib.pyplot as plt 
plt.xkcd()

from hmtk.plotting.mapping import HMTKBaseMap

dpi = 90

map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
basemap1 = HMTKBaseMap(map_config, '\gls{bsb2013} helmstetter2012 catalogues', dpi=dpi)



X = np.genfromtxt('cat', skip_header=True)

x = X[:,1]
y = X[:,2]
z = X[:,3]
#print min(z), max(z)
basemap1.add_size_scaled_points(y, x, z, alpha=0.3, 
                                colour='k', smin=0.5, sscale=2, 
                                facecolor='none', overlay=True,
                                label='learning')

Y = np.genfromtxt('TARG', skip_header=True)

#print Y[:10]

x = Y[:,1]
y = Y[:,2]
z = Y[:,3]

basemap1.add_size_scaled_points(x, y, z, 
                                alpha=0.6, edgecolor='r', 
                                smin=1, sscale=2, facecolor='none',
                                label='target', overlay=True)

plt.legend(fontsize='small')
plt.show()
#print X[:10]

