# -*- coding: utf-8 -*-

### 
###    Imports 
###

import pickle

# Python Numerical and Plotting Libraries
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
add_geology = True
add_sourcemodel = True
savefig=False

plot_mag_time_count = False

#map_title = 'Brazilian Seismic Zones'
map_title = '\gls{bsb2013}.08 Catalogue and Seismic Zoning'
#map_title = 'ISC-GEM Catalogue'
#map_title = 'South-American Lithology'


### 
###    Catalogue 
###

input_catalogue_file = 'data_input/hmtk_sa3'
#input_catalogue_file = 'data_input/hmtk_bsb2013'

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
    #basemap1.add_source_model(source_model, overlay=True)    
    
if plot_mag_time_count:
    filename = "/Users/pirchiner/Desktop/tmp_plot.png"
    # Limit the catalogue to the time period 1960 - 2012
    valid_time = np.logical_and(catalogue.data['year'] >= 1960,
                                catalogue.data['year'] <= 2014)
    catalogue.select_catalogue_events(valid_time)
    plot_magnitude_time_density(catalogue, 0.5, 1.0, filename=filename, figsize=(18,6))
    print 'Catalogue now contains %s events' % catalogue.get_number_events()


# Show distribution of magnitudes with time
#plot_magnitude_time_scatter(catalogue, fmt_string='o', alpha=0.3, linewidth=0.0)




# Depth histogram
# plot_depth_histogram(catalogue, 10.)

filename = "/Users/pirchiner/Desktop/tmp_plot.png"

# Time-varying completeness
completeness = np.array([[1980., 3.0],
                         [1985., 4.0],
                         [1964., 5.0],
                         [1910., 6.5],
                         [1900., 9.0]])
plot_observed_recurrence(catalogue, completeness, 0.2, 
                         catalogue.end_year, 
                         title="Recurrence [Rate / Time]",
                         overlay=True,
                         markersize=10,
                         color=['#FEF2D8','#F18C79'],
                         #linewidth=3,
                         alpha=0.6,
                         )







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



filename = "/Users/pirchiner/Desktop/tmp_plot.png"

# Time-varying completeness
completeness = np.array([[1980., 3.0],
                         [1985., 4.0],
                         [1964., 5.0],
                         [1910., 6.5],
                         [1900., 9.0]])
plot_observed_recurrence(catalogue, completeness, 0.2, 
                         catalogue.end_year, 
                         title="Recurrence [Rate / Time]",
                         filename=filename,
                         overlay=True,      
                         color=['#036F73','#84CDC2'],
                         markersize=10,
                         #linewidth=3,
                         alpha=0.6)


plt.show()
exit()
    












plt.show()

exit()


# In[ ]:

# Limit the catalogue to depths less than 50 km
#valid_depth = catalogue.data['depth'] <= 50.
#catalogue.select_catalogue_events(valid_depth)
plot_depth_histogram(catalogue, 2.0)

exit()
# In[ ]:

# Set-up the file writer
output_file_name = 'data_output/basic_demo_catalogue_1.csv'
writer = CsvCatalogueWriter(output_file_name)

# Write the catalogue to file
writer.write_file(catalogue)

print 'File %s written' % output_file_name


# In[ ]:

completeness = np.array([[1985., 4.0],
                         [1964., 5.0],
                         [1910., 6.5]])
# Set-up the exporter
output_file_name = 'data_output/basic_demo_catalogue_complete_1.csv'
writer = CsvCatalogueWriter(output_file_name)

# Write the catalogue to file, purging events from the incomplete period
writer.write_file(catalogue, magnitude_table=completeness)

print 'File %s written' % output_file_name


# In[ ]:



