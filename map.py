# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from matplotlib.mlab import griddata

#plt.xkcd()

class rate_map(object):
    def __init__(self, x, y, rate, title, (nx,ny), catalogue=None, origin='upper'):
        
        # define region and resolution
        x0, xf, nx = -80, -30, nx
        y0, yf, ny = -37, 13, ny
    
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
        
        self.m.drawcoastlines(linewidth=1)
        self.m.drawcountries(linewidth=1)
        self.m.drawstates(linewidth=0.5)
        self.m.drawmeridians(np.arange(x0, xf, 10))
        self.m.drawparallels(np.arange(y0, yf, 10))

        lon, lat = self.m(x, y)

        levels = np.linspace(min(rate), max(rate), 10)
        
        lat = np.reshape(lat, (nx, ny))
        lon = np.reshape(lon, (nx, ny))
        rate = np.reshape(rate, (nx, ny))


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

        cs = self.m.imshow(rate, 
                           plt.cm.RdYlGn_r,
#                           plt.cm.Spectral_r,
                           origin=origin,
                           )
        self.ax.set_xlabel("longitude")
        self.ax.set_ylabel("latitude")
        
        plt.colorbar(cs, 
                     #extend='both',
                     )
        
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
        
        # define region and resolution
        x0, xf, nx = -80, -30, nx
        y0, yf, ny = -37, 13, ny
    
#         x0, xf, nx = 118.5, 124, nx
#         y0, yf, ny = 20, 26.5, ny
    
    
        self.catalogue = catalogue
    
        self.f = plt.figure()
        self.ax = self.f.add_axes([0.1,0.1,0.8,0.8])
        self.ax.set_title(title)
        self.ax.set_xlabel("longitude")
        self.ax.set_ylabel("latitude")
        
        self.m = Basemap(projection='cyl', 
                    llcrnrlon = x0,
                    llcrnrlat = y0,
                    urcrnrlon = xf,
                    urcrnrlat = yf,
                    suppress_ticks=False,
                    resolution='i', 
                    area_thresh=1000.,
                    ax = self.ax)
        
        self.m.drawcoastlines(linewidth=1)
        self.m.drawcountries(linewidth=1)
        self.m.drawstates(linewidth=0.5)
        self.m.drawmeridians(np.arange(x0, xf, 10))
        self.m.drawparallels(np.arange(y0, yf, 10))

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
                           cmap=plt.cm.hot_r,
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

        plt.colorbar(cs, 
                     #extend='both',
                     )
        
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