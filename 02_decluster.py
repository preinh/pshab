
# In[ ]:

# Python utilities
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


# In[ ]:

ifile = 'data_input/hmtk_bsb2013.csv'
parser = CsvCatalogueParser(ifile)
catalogue = parser.read_file()
print 'Catalogue contains %s events' % catalogue.get_number_events()

# Sort catalogue chronologically
catalogue.sort_catalogue_chronologically()
print 'Catalogue sorted chronologically!'


# In[ ]:

# Set up the declustering algorithm
# Step 1 - set-up the tool
gardner_knopoff = GardnerKnopoffType1()


# In[ ]:

declust_config = {'time_distance_window': GardnerKnopoffWindow(),
                  'fs_time_prop': 1.0}
print declust_config


# In[ ]:

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


# In[ ]:

output_file = 'data_output/bsb2013_catalogue_declustered_v1.csv'
writer = CsvCatalogueWriter(output_file)
writer.write_file(catalogue)

