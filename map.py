# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from matplotlib.mlab import griddata

from hmtk.plotting.mapping import HMTKBaseMap

plt.xkcd()

class rate_map(object):
    def __init__(self, x, y, rate, title, (nx,ny), catalogue=None, origin='upper'):
        
        # Configure the limits of the map and the coastline resolution
        map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
        #map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}
 
         
         
        # define region and resolution
        x0, xf, nx = map_config['min_lon'], map_config['max_lon'], nx
        y0, yf, ny = map_config['min_lat'], map_config['max_lat'], ny
    

        # define region and resolution
#         x0, xf, nx = -80, -30, nx
#         y0, yf, ny = -37, 13, ny
    
#         x0, xf, nx = 118.5, 124, nx
#         y0, yf, ny = 20, 26.5, ny
    
        self.catalogue = catalogue
    
        self.f = plt.figure()
        self.ax = self.f.add_axes([0.1,0.1,0.8,0.8])
        self.ax.set_title(title)
        
        self.m = Basemap(projection='cyl', 
                    llcrnrlon = x0,
                    llcrnrlat = y0,
                    urcrnrlon = xf,
                    urcrnrlat = yf,
                    suppress_ticks=False,
                    resolution='i', 
                    area_thresh=1000.,
                    ax = self.ax)
        
        self.m.drawcoastlines(linewidth=1, color='0.3')
        self.m.drawcountries(linewidth=1, color='0.3')
        self.m.drawstates(linewidth=0.5, color='0.3')
        self.m.drawmeridians(np.arange(x0, xf, 10), linewidth=0)
        self.m.drawparallels(np.arange(y0, yf, 10), linewidth=0)

        lon, lat = self.m(x, y)

        levels = np.linspace(min(rate), max(rate), 10)
        
#         lat = np.reshape(lat, (nx, ny))
#         lon = np.reshape(lon, (nx, ny))
#         rate = np.reshape(rate, (nx, ny))


#         cs = self.m.contourf(lon, lat, rate, levels,
#                              cmap = plt.cm.RdYlGn_r,
#                              latlon=True,
#                              #extend='both'
#                              )
        
#         cs = self.m.pcolormesh(lon, lat, rate,
#                           shading='flat',
#                           cmap=plt.cm.RdYlGn_r,
#                           latlon=True
#                         )
        extent = (x0, xf, y0, yf)
        
        xx = np.linspace(x0,xf,nx) 
        yy = np.linspace(y0,yf,ny)
        xs,ys = np.meshgrid(xx,yy)
        
        resampled = griddata(lon, lat, rate, xs, ys)
        
        cs = self.m.imshow(resampled, 
                           extent=extent, 
                           cmap=plt.cm.RdYlGn_r,
#                           plt.cm.Spectral_r,
                           origin=origin,
                           vmin=-3, vmax=3,
                           )
        self.ax.set_xlabel("longitude")
        self.ax.set_ylabel("latitude")
        
        _cb = plt.colorbar(cs, 
                     #extend='both',
                     )

        _cb.ax.tick_params(labelsize='small')
        _cb.set_label('a-value', fontsize='small')


        
        if self.catalogue:
            x = self.catalogue.data['longitude']
            y = self.catalogue.data['latitude']
            mag = self.catalogue.data['magnitude']
            
            self.m.scatter(x, y, s=np.exp(mag), 
                           marker='o', facecolors='none', edgecolors='k', alpha=0.1
                           )

    def show(self):
        plt.show()
        
        
        
        
class hazard_map(object):
    def __init__(self, x, y, rate, title, (nx, ny), catalogue=None, origin='upper'):
        
  
        
        map_title = title
        
        
        # Configure the limits of the map and the coastline resolution
        map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}

        
        
        # define region and resolution
        x0, xf, nx = map_config['min_lon'], map_config['max_lon'], nx
        y0, yf, ny = map_config['min_lat'], map_config['max_lat'], ny
    
#         x0, xf, nx = 118.5, 124, nx
#         y0, yf, ny = 20, 26.5, ny
    
    
        self.catalogue = catalogue
    
#         self.f = plt.figure()
#         self.ax = self.f.add_axes([0.1,0.1,0.8,0.8])
#         self.ax.set_title(title)
#         self.ax.set_xlabel("longitude")
#         self.ax.set_ylabel("latitude")
        
        self.basemap = HMTKBaseMap(map_config, map_title, dpi=90)
        #self.m = self.basemap.m
        _ax = plt.gca()
        _ax.set_title(title)
        _ax.set_xlabel("longitude", labelpad=25)
        _ax.set_ylabel("latitude", labelpad=25)


#         self.m = Basemap(projection='cyl', 
#                     llcrnrlon = x0,
#                     llcrnrlat = y0,
#                     urcrnrlon = xf,
#                     urcrnrlat = yf,
#                     suppress_ticks=False,
#                     resolution='i', 
#                     area_thresh=1000.,
#                     ax = self.ax)
        
#         self.m.drawcoastlines(linewidth=1)
#         self.m.drawcountries(linewidth=1)
#         self.m.drawstates(linewidth=0.5)
#         self.m.drawmeridians(np.arange(x0, xf, 10), linewidth=0)
#         self.m.drawparallels(np.arange(y0, yf, 10), linewidth=0)

        lon, lat = self.basemap.m(x, y)

        levels = np.linspace(min(rate), max(rate), 10)
        
#         lat = np.reshape(lat, (nx, ny))
#         lon = np.reshape(lon, (nx, ny))
#         rate = np.reshape(rate, (nx, ny))


#         cs = self.m.contourf(lon, lat, rate, levels,
#                              cmap = plt.cm.RdYlGn_r,
#                              latlon=True,
#                              #extend='both'
#                              )
        
#         cs = self.m.pcolormesh(lon, lat, rate,
#                           shading='flat',
#                           cmap=plt.cm.RdYlGn_r,
#                           latlon=True
#                         )

        extent = (x0, xf, y0, yf)
        
        xx = np.linspace(x0,xf,nx) 
        yy = np.linspace(y0,yf,ny)
        xs,ys = np.meshgrid(xx,yy)
        
        resampled = griddata(lon, lat, rate, xs, ys)
        
        cs = self.basemap.m.imshow(resampled, 
                           extent=extent,
                           cmap=plt.cm.hot_r,
                           vmin=0, vmax=0.2,
                           )
        #plt.plot(xs0, ys0, "r.")
        #plt.plot(xs, ys, "b.")
#         plt.title("imshow for irregularly spaced data using griddata")
#         plt.show()
    


#         cs = self.m.imshow(rate, 
#                            plt.cm.RdYlGn_r,
#                            origin=origin,
#                            )

#         cs = self.m.scatter(lon, lat, c=rate, 
#                            cmap=plt.cm.RdYlGn_r,
#                            #origin=origin,
#                            )

        _cb = plt.colorbar(cs, 
                     extend='max',
                     )
        _cb.ax.tick_params(labelsize='small')
        _cb.set_label('PGA [g]', fontsize='small')
#         if self.catalogue:
#             x = self.catalogue.data['longitude']
#             y = self.catalogue.data['latitude']
#             mag = self.catalogue.data['magnitude']
#             
#             self.m.scatter(x, y, s=np.exp(mag), 
#                            marker='o', facecolors='none', edgecolors='k', alpha=0.1
#                            )

    def show(self):
        plt.show()        