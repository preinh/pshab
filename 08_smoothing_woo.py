'''
Test suite for smoothed seismicity class
'''
import os
import numpy as np

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser

#from hmtk.seismicity.catalogue import Catalogue

from hmtk.seismicity.smoothing import utils
from hmtk.seismicity.smoothing.smoothed_seismicity_woo \
    import SmoothedSeismicityWoo

from hmtk.seismicity.smoothing.kernels.woo_1996 import \
    IsotropicGaussianWoo

BASE_PATH = 'data_input/'
OUTPUT_FILE = 'data_output/hmtk_bsb2013_decluster_woo_rates.csv'
TEST_CATALOGUE = 'hmtk_bsb2013_decluster.csv'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
#print catalogue.get_number_events()
#print np.min(catalogue.data['magnitude'])

# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
grid_limits = utils.Grid.make_from_list([ -80, -30, 1, -37, 14, 1, 0, 30, 10])

model = SmoothedSeismicityWoo(grid_limits, bvalue=1.0)

# Time-varying completeness
comp_table = np.array([[1990., 3.0],
                       [1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0],
                       [1900., 6.5],
                       [1800., 7.0]])

#config
#config = {'Length_Limit': 3., 'BandWidth': 100., 'increment': True, 'MagnitudeBinSize': 0.5 }

config = {'min_magnitude': 3.0 , 
          'magnitude_bin': 0.5, 
          'use3d': False,
          'bandwidth_h_limit': 3,
          }

#smoothing
output_data = model.run_analysis(catalogue,
                                 config,
                                 completeness_table=comp_table,
                                 smoothing_kernel = IsotropicGaussianWoo())
# export results
model.write_to_csv(OUTPUT_FILE)

#print model.grid
#print model.catalogue
#print model.beta
#print model.data
#print model.kernel
#print output_data

exit()
