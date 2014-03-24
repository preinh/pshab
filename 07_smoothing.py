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
OUTPUT_FILE = 'hmtk_bsb2013_decluster_smooth_data.csv'
TEST_CATALOGUE = 'hmtk_bsb2013_decluster.csv'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
print catalogue.get_number_events()

# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
grid_limits = Grid.make_from_list([ -80, -30, 1, -37, 14, 1, 0, 30, 10])
model = SmoothedSeismicity(grid_limits, bvalue=1.0)

# Time-varying completeness
comp_table = np.array([[1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0]])

#config
config = {'Length_Limit': 3., 'BandWidth': 100., 'increment': 1.0}

#smoothing
output_data = model.run_analysis(catalogue,
                                 config,
                                 completeness_table=comp_table,
                                 smoothing_kernel = IsotropicGaussian())
#print output_data
# export results
model.write_to_csv(OUTPUT_FILE)
