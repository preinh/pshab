# -*- coding: utf-8 -*-

### 
###    Imports 
###

# Python Numerical and Plotting Libraries
import pickle
import numpy as np
import matplotlib.pyplot as plt
plt.xkcd()

# HMTK Catalogue Import/Export Libraries
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter

# HMTK Plotting Tools
from hmtk.plotting.seismicity.catalogue_plots import (plot_depth_histogram,
                                                      plot_magnitude_time_scatter,
                                                      plot_magnitude_time_density,
                                                      plot_magnitude_depth_density,
                                                      plot_observed_recurrence)
from hmtk.plotting.mapping import HMTKBaseMap
print 'Imports OK!'


### 
###    Map Config 
###

map_dpi = 90 
add_geology = False
add_sourcemodel = True
savefig=False

#map_title = 'Brazilian Seismic Zones'
map_title = 'Seismic Zoning [ dourado2014 ]'
#map_title = 'ISC-GEM Catalogue'
#map_title = 'South-American Lithology'


# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
#map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}
#map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}


# #central
# map_config = {'min_lon': -60.0, 'max_lon': -46.0, 'min_lat': -24.0, 'max_lat': 6.0, 'resolution':'l'}
# #SE
# map_config = {'min_lon': -52.0, 'max_lon': -36.0, 'min_lat': -32.5, 'max_lat': -13.0, 'resolution':'l'}
# #MT
# map_config = {'min_lon': -60.0, 'max_lon': -55.0, 'min_lat': -15.0, 'max_lat': -10.0, 'resolution':'l'}
# #AM
# map_config = {'min_lon': -65.0, 'max_lon': -55.0, 'min_lat': -07.0, 'max_lat': 4.0, 'resolution':'l'}
# #NE
# map_config = {'min_lon': -43.0, 'max_lon': -33.0, 'min_lat': -15, 'max_lat': -1.5, 'resolution':'l'}
# #AC
# map_config = {'min_lon': -75.0, 'max_lon': -68.0, 'min_lat': -13.0, 'max_lat': -4.0, 'resolution':'l'}



### 
###    Catalogue 
###

#input_catalogue_file = 'data_input/hmtk_sa3'
input_catalogue_file = 'data_input/hmtk_bsb2013'

### 
###    Catalogue cache or read/cache
###

try:
    catalogue = pickle.load(open(input_catalogue_file + ".pkl", 'rb'))
except:

    parser = CsvCatalogueParser(input_catalogue_file + ".csv")
    catalogue = parser.read_file()
    print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
    print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)

    # Sort catalogue chronologically
    catalogue.sort_catalogue_chronologically()
    print 'Catalogue sorted chronologically!'

    valid_magnitudes = np.logical_not(np.isnan(catalogue.data['magnitude']))
    catalogue.select_catalogue_events(valid_magnitudes)
    valid_magnitudes = catalogue.data['magnitude'] >= 3.0
    catalogue.select_catalogue_events(valid_magnitudes)
    #print catalogue.data['magnitude']
     
    valid_depths = np.logical_not(np.isnan(catalogue.data['depth']))
    catalogue.select_catalogue_events(valid_depths)
     
    # Set-up the file writer
    output_file_name = 'data_input/hmtk_sa3.csv'
    writer = CsvCatalogueWriter(output_file_name)
    # Write the catalogue to file
    writer.write_file(catalogue)
    #exit()
    
    print 'File %s written' % output_file_name
    f=open(input_catalogue_file + ".pkl",'wb')
    pickle.dump(catalogue, f)
    f.close()




### 
###    Mapa
###
# Create a hmtk basemap
basemap1 = HMTKBaseMap(map_config, map_title, dpi=map_dpi)

### 
###    Geologia
###
if add_geology:
    wms_cprm = "http://onegeology.cprm.gov.br/cgi-bin/BRA_GSB_EN_Bedrock_Geology/wms?"
    wms_oneg = "http://mapdmzrec.brgm.fr/cgi-bin/mapserv54?map=/carto/ogg/mapFiles/CGMW_Bedrock_and_Structural_Geology.map&"
    
    wmsl_oneg = {'server_url': wms_oneg,
                  'layers': ['World_CGMW_50M_Geology'],
                  }
    
    wmsl_br_blt = {'server_url': wms_cprm,
                    'layers': ['BRA_GSB_EN_1M_BLT'],
                    'styles': ['default'],
                  }
    
    wmsl_br_ba = {'server_url': wms_cprm,
                    'layers': ['BRA_GSB_EN_1M_BA'],
                    'styles': ['default'],
                  }
    
    o = basemap1.m.wmsimage(wmsl_oneg['server_url'], 
               xpixels=1000,verbose=True,
               layers=wmsl_oneg['layers'],
               format='png',
               transparent=True,
               )
    o.set_alpha(0.3)
    
    # legendUrl="http://mapdmzrec.brgm.fr/cgi-bin/mapserv54?map=/carto/ogg/mapFiles/CGMW_Bedrock_and_Structural_Geology.map&version=1.1.1&service=WMS&request=GetLegendGraphic&layer=Eurasia_CGMW_12500K_GeologicalUnits&format=image/png&STYLE=default"
    # 
    # import os
    # import urllib2
    # 
    # from IPython.core.display import Image
    # from matplotlib._png import read_png
    # from matplotlib.offsetbox import AnnotationBbox, OffsetImage
    # 
    # def saveLayerAsImage(layer, inname):
    #     out = open(inname, 'wb')
    #     out.write(layer.read())
    #     out.close()
    # 
    # 
    # #Annotating the map with the legend
    # #Save the legend as image
    # legend = urllib2.urlopen(legendUrl)
    # saveLayerAsImage(legend, 'legend_temp.png')
    # 
    # arr = read_png('legend_temp.png')
    # imagebox = OffsetImage(arr, zoom=0.9)
    # 
    # #read the image as an array
    # # arr = read_png('legend_temp.png')
    # xy =[ -35, -47 ]
    # 
    # #Gets the current axis
    # ax = plt.gca()
    # 
    # #Creates the annotation
    # ab = AnnotationBbox(imagebox, xy,
    #                     xybox=(0.,0),
    #                     xycoords='data',
    #                     boxcoords="offset points",
    #                     pad=0.)
    # 
    # #Adds the legend image as an AnnotationBbox to the map
    # ax.add_artist(ab)
    
    
    
    o = basemap1.m.wmsimage(wmsl_br_ba['server_url'], 
                xpixels=500,verbose=True,
                layers=wmsl_br_ba['layers'],
                format='png',
                )
    o.set_alpha(0.4)
    
    # basemap1.m.wmsimage(wmsl_br_blt['server_url'], 
    #            xpixels=1000,verbose=True,
    #            layers=wmsl_br_blt['layers'],
    #            format='png',
    #            transparent=True,
    #            alpha=0.2,
    #            )
    
    


    

### 
###    Source Model
###


if add_sourcemodel:
    from hmtk.parsers.source_model.nrml04_parser import nrmlSourceModelParser
    
    source_model_file = "/Users/pirchiner/dev/pshab/dourado_reproduction/source_model.xml"
    
    # read source model file
    parser = nrmlSourceModelParser(source_model_file)
    source_model = parser.read_file(2.0)
    
    # add source model
    #basemap1.add_source_model(source_model, area_border, border_width, point_marker, point_size, overlay)    
    basemap1.add_source_model(source_model, overlay=True)    
    

### 
###    Catálogo
###

x = catalogue.data['longitude']
y = catalogue.data['latitude']
z = catalogue.data['depth']

_idx = np.argsort(z)
catalogue.select_catalogue_events(_idx)
basemap1.add_catalogue(catalogue, alpha=0.1)

#basemap1.add_colour_scaled_points(x, y, np.log(z+1), overlay=True)


if savefig: basemap1.savemap("/Users/pirchiner/Desktop/teste.png")
plt.show()
#exit()


# Limit the catalogue to the time period 1960 - 2012
#valid_time = np.logical_and(catalogue.data['year'] >= 1960,
#                            catalogue.data['year'] <= 2014)
#catalogue.select_catalogue_events(valid_time)

