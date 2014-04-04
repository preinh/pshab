
# In[ ]:

# Python Numerical and Plotting Libraries
import numpy as np
import matplotlib.pyplot as plt

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


# In[ ]:

input_catalogue_file = 'data_input/hmtk_chile.csv'
#input_catalogue_file = 'data_input/hmtk_sa.csv'

parser = CsvCatalogueParser(input_catalogue_file)
catalogue = parser.read_file()
print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)


# In[ ]:

# Sort catalogue chronologically
catalogue.sort_catalogue_chronologically()
print 'Catalogue sorted chronologically!'


# In[ ]:

# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}

map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}

# Create a hmtk basemap
basemap1 = HMTKBaseMap(map_config, 'Earthquake Catalogue')
# Add a catalogue
#basemap1.add_catalogue(catalogue)

valid_magnitudes = catalogue.data['magnitude'] <> np.nan
catalogue.select_catalogue_events(valid_magnitudes)
valid_magnitudes = catalogue.data['magnitude'] >= 2.0
catalogue.select_catalogue_events(valid_magnitudes)
print catalogue.data['magnitude']

valid_depths = catalogue.data['depth'] <> np.nan
catalogue.select_catalogue_events(valid_depths)
# In[ ]:

# Limit the catalogue to the time period 1960 - 2012
valid_time = np.logical_and(catalogue.data['year'] >= 1960,
                            catalogue.data['year'] <= 2014)
catalogue.select_catalogue_events(valid_time)
#plot_magnitude_time_density(catalogue, 0.5, 2.0)
print 'Catalogue now contains %s events' % catalogue.get_number_events()


# In[ ]:

# Show distribution of magnitudes with time
#plot_magnitude_time_scatter(catalogue, fmt_string='.')


# In[ ]:

# Plot the magnitude-time density
magnitude_bin = 0.2
time_bin = 5.0 # in Decimal Years
plot_magnitude_time_density(catalogue, magnitude_bin, time_bin)


# In[ ]:

# Depth histogram
#plot_depth_histogram(catalogue, 10.)


# In[ ]:

# Time-varying completeness
completeness = np.array([[1980., 3.0],
                         [1985., 4.0],
                         [1964., 5.0],
                         [1910., 6.5],
                         [1900., 9.0]])
plot_observed_recurrence(catalogue, completeness, 0.2, catalogue.end_year)


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



