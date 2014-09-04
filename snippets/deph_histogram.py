
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
###    Catalogue 
###


#input_catalogue_file = 'data_input/hmtk_bsb2013.csv'
input_catalogue_file = 'data_input/hmtk_sa3.csv'

input_catalogue_file = '../data_input/hmtk_sa3'
input_catalogue_file = '../data_input/hmtk_bsb2013'




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
    output_file_name = input_catalogue_file + ".csv"
    writer = CsvCatalogueWriter(output_file_name)
    # Write the catalogue to file
    writer.write_file(catalogue)
    #exit()
    
    print 'File %s written' % output_file_name
    f=open(input_catalogue_file + ".pkl",'wb')
    pickle.dump(catalogue, f)
    f.close()






X = catalogue.data['depth']



print max(X), min(X)
# X = np.random.random(50)
# print max(X), min(X)
# for i,x in enumerate(X):
#     print i, x
b = np.linspace(min(X), max(X), 8)
 
#f = plt.figure(num, figsize, dpi, facecolor, edgecolor, frameon, FigureClass)
 
n, bins, patches = plt.hist(X, bins=b, 
                            orientation='horizontal', 
                            #log=False,
                            #bottom=True, 
                            #normed=True,
                            histtype='bar',
                            color='#5fbdce',
                            alpha=0.6)
   
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
  
# majorLocator   = MultipleLocator(2e4)
# majorFormatter = FormatStrFormatter('%g')
# minorLocator   = MultipleLocator(1e4)
#  
# plt.gca().xaxis.set_major_locator(majorLocator)
# plt.gca().xaxis.set_major_formatter(majorFormatter)
# plt.gca().xaxis.set_minor_locator(minorLocator)
#plt.boxplot(X)
plt.gca().invert_yaxis()
plt.xlabel("# earthquakes")
plt.ylabel("depth [km]")
plt.title("Depth Distribution - \gls{bsb2013}.08")
#plt.title("Depth Distribution - ISC-GEM")
 
#plt.savefig("/Users/pirchiner/Desktop/teste.png", format='png')
#plt.show()
#plot_depth_histogram(catalogue, 50.0)
exit()
