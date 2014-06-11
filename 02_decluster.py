
# Python utilities
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Import HMTK I/O Tools
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter


# HMTK Declustering Tools
from hmtk.seismicity.declusterer.dec_afteran import Afteran
from hmtk.seismicity.declusterer.dec_gardner_knopoff import GardnerKnopoffType1
from hmtk.seismicity.declusterer.distance_time_windows import GardnerKnopoffWindow, GruenthalWindow, UhrhammerWindow

# HMTK Completeness Tools
from hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971

print 'Import OK'


write_output = False
output_file = 'data_output/bsb2013_catalogue_declustered_v1.csv'

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




# Set up the declustering algorithm
# Step 1 - set-up the tool
gardner_knopoff = GardnerKnopoffType1()


declust_config = {'time_distance_window': GardnerKnopoffWindow(),
                  'fs_time_prop': 1.0}
print declust_config


print 'Running declustering ...'
vcl, flag_vector = gardner_knopoff.decluster(catalogue, declust_config)
print 'done!'
print '%s clusters found' % np.max(vcl)
print '%s Non-poissionian events identified' % np.sum(flag_vector != 0)





# In[ ]:

# Setup the algorithm
afteran = Afteran()
declust_config = {'time_distance_window': GardnerKnopoffWindow(),
                  'time_window': 60.}
print 'Running Afteran ...'
# Run Afteran
vcl2, flag_vector2 = afteran.decluster(catalogue, declust_config)
print 'done!'
print '%s clusters found' % np.max(vcl2)
print '%s Non-poissionian events identified' % np.sum(flag_vector2 != 0)



# In[ ]:

catalogue.select_catalogue_events(flag_vector == 0)
print 'Purged catalogue now contains %s events' % catalogue.get_number_events()

if write_output:
    
    writer = CsvCatalogueWriter(output_file)
    writer.write_file(catalogue)

