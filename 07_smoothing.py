'''
Test suite for smoothed seismicity class
'''
import os
import numpy as np
from math import fabs

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser

from hmtk.seismicity.catalogue import Catalogue

from hmtk.seismicity.smoothing import utils
from hmtk.seismicity.smoothing.smoothed_seismicity import (
    SmoothedSeismicity, _get_adjustment, Grid)

from hmtk.seismicity.smoothing.kernels.isotropic_gaussian import \
    IsotropicGaussian

BASE_PATH = 'data_input/'
OUTPUT_FILE = 'data_output/hmtk_bsb2013_decluster_frankel1995.csv'
TEST_CATALOGUE = 'hmtk_bsb2013_decluster.csv'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
print catalogue.get_number_events()

res, spc = 0.5, 100
#res, spc = 1, 50
#res, spc = 0.2, 250


# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
grid_limits = Grid.make_from_list([ -80, -30, res, -37, 13, res, 0, 30, 30])
model = SmoothedSeismicity(grid_limits, bvalue=1.0)

# Time-varying completeness
comp_table = np.array([[1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0]])

#config
config = {'Length_Limit': 3., 'BandWidth': 150., 'increment': 1.0}

#smoothing
o = model.run_analysis(catalogue,
                         config,
                         completeness_table=comp_table,
                         smoothing_kernel = IsotropicGaussian(),
                         #increment = False,
                         )

x = o[:, 0]
y = o[:, 1]
r = o[:, 4] / (res**2)
r = np.array([ np.log10(r) if  r > 0 else np.NaN for r in r ])
#r = np.log10(r)

#print np.sqrt(len(x))

from map import rate_map
m = rate_map(x, y, r, "a-value [Frankel1995] h=%d km"%config['BandWidth'], 
             spc, catalogue)
m.show()

#print output_data
# export results
model.write_to_csv(OUTPUT_FILE)
