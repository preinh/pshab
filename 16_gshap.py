import pickle
import numpy as np
import scipy.interpolate
import csv



# catalogue
import os
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser
BASE_PATH = 'data_input/'
TEST_CATALOGUE = 'hmtk_bsb2013_pp_decluster.csv'
_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()
catalogue.sort_catalogue_chronologically()



import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from matplotlib.mlab import griddata

plt.xkcd()


def read_data(file, extension=".csv"):
    
    try:
        data = pickle.load(open(file + ".pkl", 'rb'))
    except:
        data = np.genfromtxt(file + extension)
        
        #clean data
        
        bad_data = data.len()        
        #filter data
        x = data[:,0]
        y = data[:,1]
        z = data[:,2]

        valid_lons = np.logical_and(x >= x0, x <= xf)
        valid_lats = np.logical_and(y >= y0, y <= yf)
        valid_vals = np.logical_not(np.isnan(z))
        bbox = np.logical_and(valid_lons, valid_lats)
        
        valid_data = np.logical_and(bbox, valid_vals)
        
        data = data[data]
        print 'bad_data: '%( bad_data - data.len()  )
        
        #print 'File %s written' % output_file_name
        f=open(file + ".pkl",'wb')
        pickle.dump(data, f)
        f.close()

    return data

def map(data, config):
        x0, xf = config['min_lon'], config['max_lon']
        y0, yf = config['min_lat'], config['max_lat']

    
        f = plt.figure()
        ax = f.add_axes([0.1,0.1,0.8,0.8])
        ax.set_title("PGA (poe 10%, 50 years) [ gshap ]")
        
        m = Basemap(projection='cyl', 
                    llcrnrlon = x0,
                    llcrnrlat = y0,
                    urcrnrlon = xf,
                    urcrnrlat = yf,
                    suppress_ticks=False,
                    resolution='i', 
                    area_thresh=1000.,
                    ax = ax)
        
        m.drawcoastlines(linewidth=1, color='0.3')
        m.drawcountries(linewidth=1, color='0.3')
        m.drawstates(linewidth=0.5, color='0.3')
        m.drawmeridians(np.arange(x0, xf, 10), linewidth=0)
        m.drawparallels(np.arange(y0, yf, 10), linewidth=0)

        x = data[:,0]
        y = data[:,1]
        z = data[:,2]/10.

        lon, lat = m(x, y)

        levels = np.linspace(min(z), max(z), 10)
        

        # Set up a regular grid of interpolation points
        xi, yi = np.linspace(x0, xf, 50), np.linspace(y0, yf, 50)
        xi, yi = np.meshgrid(xi, yi)
        
        
        # Interpolate
        #rbf = scipy.interpolate.RectBivariateSpline(x, y, z, function='linear')
        zi = scipy.interpolate.griddata(points=zip(x, y), values=z, xi=(xi,yi), method='linear')


        cs = m.imshow(zi, plt.cm.hot_r, 
                    vmin=0, vmax=0.16, origin='lower',
                    extent=[x.min(), x.max(), y.min(), y.max()],
                    label="pga [g]")


        _cb = plt.colorbar(cs, extend='max')
        _cb.ax.tick_params(labelsize='small')
        _cb.set_label("PGA [g]", fontsize='small')

 
#         cs = self.m.contourf(lon, lat, rate, levels,
#                              cmap = plt.cm.RdYlGn_r,
#                              latlon=True,
#                              #extend='both'
#                              )
#        print lon, lat, z
        
#         cs = m.scatter(lon, lat, color=z,
#                           marker='o',
#                           #cmap=plt.cm.RdYlGn_r,
#                           linewidth=0,
#                           alpha = 0.8,
#                         )
#         cs = m.pcolormesh(lon, lat, z,
#                           shading='flat',
#                           cmap=plt.cm.RdYlGn_r,
#                           latlon=True,
#                         )

#         cs = m.imshow(x, 
#                plt.cm.RdYlGn_r,
# #              plt.cm.Spectral_r,
# #               origin='lower',
#                            )
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        
#        plt.colorbar(cs, 
                     #extend='both',
 #                    )
#        plt.colorbar()
        x = catalogue.data['longitude']
        y = catalogue.data['latitude']
        mag = catalogue.data['magnitude']
         
        m.scatter(x, y, s=np.exp(mag), 
                       marker='o', facecolors='none', edgecolors='k', alpha=0.1
                       )

        fig_name = "/Users/pirchiner/Desktop/gshap.png"
        plt.savefig(fig_name, dpi=150, format='png')
        plt.show()
        
        


if __name__ == '__main__':


    
    # Configure the limits of the map and the coastline resolution
    config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
    #map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}
    #map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}
    
#     image_file = '/Users/pirchiner/Downloads/GSHPUB/GSHPUB.tif'
#     image = plt.imread(image_file)
#     plt.imshow(image)
#     plt.colorbar()
#     plt.show()    
#     exit()

    
    gshapfile ="/Users/pirchiner/Downloads/GSHPUB"

    try:
        data = pickle.load(open(gshapfile + ".pkl", 'rb'))
    except:
        data = np.genfromtxt(gshapfile + ".DAT")
        bad_data = len(data)        
        #filter data
        x = data[:,0]
        y = data[:,1]
        z = data[:,2]

        valid_lons = np.logical_and(x >= config['min_lon'], x <= config['max_lon'])
        valid_lats = np.logical_and(y >= config['min_lat'], y <= config['max_lat'])
        valid_vals = np.logical_not(np.isnan(z))
        bbox = np.logical_and(valid_lons, valid_lats)
        
        valid_data = np.logical_and(bbox, valid_vals)
        
        data = data[valid_data]
        print 'bad_data: %d'%( bad_data - len(data)  )
        
        #print 'File %s written' % output_file_name
        f=open(gshapfile + ".pkl",'wb')
        pickle.dump(data, f)
        f.close()
    

    map(data, config)






