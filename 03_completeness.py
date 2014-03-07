
# In[ ]:

# Python utilities
import numpy as np
import matplotlib.pyplot as plt

# Import HMTK I/O Tools
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter

# HMTK Completeness Tools
from hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971

print 'Import OK'


# In[ ]:

# Read catalogue
ifile = 'data_input/hmtk_bsb2013.csv'
parser = CsvCatalogueParser(ifile)
catalogue = parser.read_file()
print 'Catalogue contains %s events' % catalogue.get_number_events()

# Sort catalogue chronologically
catalogue.sort_catalogue_chronologically()
print 'Catalogue sorted chronologically!'


# In[ ]:

stepp = Stepp1971()

completeness_config = {'magnitude_bin': 1,
                       'time_bin': 5,
                       'increment_lock': False}
print completeness_config

# Run analysis
print 'Running Stepp (1971) completeness analysis:'
completeness_table = stepp.completeness(catalogue, completeness_config)
print completeness_table
print 'done!'

# Print the output completeness table
#for row in completeness_table:
#    print '%8.1f  %8.2f' %(row[0], row[1])


# In[ ]:

from hmtk.plotting.seismicity.completeness.plot_stepp_1972 import create_stepp_plot
create_stepp_plot(stepp, "data_output/stepp_plot_catalogue_bsb2013.png")


# In[ ]:



