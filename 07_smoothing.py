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
OUTPUT_FILE = 'hmtk_bsb2013_smoothing_data.csv'
TEST_CATALOGUE = 'hmtk_bsb2013.csv'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
grid_limits = Grid.make_from_list([ -80, -30, 1, -37, 14, 1, 0, 30, 10])
model = SmoothedSeismicity(grid_limits, bvalue=1.0)

# Time-varying completeness
comp_table = np.array([[1990., 2.0],
                       [1980., 3.0],
                       [1960., 4.0],
                       [1950., 5.0],
                       [1910., 6.5]])

#config
config = {'Length_Limit': 3., 'BandWidth': 100., 'increment': 1.0}

#smoothing
output_data = model.run_analysis(catalogue,
                                 config,
                                 completeness_table=comp_table,
                                 smoothing_kernel = IsotropicGaussian())
print output_data
# export results
model.write_to_csv(OUTPUT_FILE)
