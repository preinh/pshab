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
#OUTPUT_FILE = 'data_output/hmtk_bsb2013_decluster_frankel1995.csv'
OUTPUT_FILE = '/Users/pirchiner/dev/pshab/data_output/hmtk_sa3_decluster_frankel1995.csv'

#model_name = 'hmtk_bsb2013'
model_name = 'hmtk_sa3'
#TEST_CATALOGUE = 'hmtk_bsb2013_pp_decluster.csv'
TEST_CATALOGUE = 'hmtk_sa3_pp_decluster.csv'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
#print catalogue.get_number_events()

#res, spc = 0.5, 100
res, spc = 1, 50
#res, spc = 0.2, 250


# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}
#_l = [ 118.5,  124,  res,  20.0,   26.5,  res,    0,   300,   300]
_l = [ -95.,  -25,  res,  -65,   25,  res,    0,   800,   800]
#_l = [ -80,  -30,  res,  -37,   13,  res,    0,   30,   30]
grid_limits = Grid.make_from_list(_l)

nx = round((_l[1] - _l[0]) / _l[2],0)
ny = round((_l[4] - _l[3]) / _l[5],0)
grid_shape = (nx, ny)
print grid_shape
model = SmoothedSeismicity(grid_limits, bvalue=1.0)

# Time-varying completeness
comp_table = np.array([[1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0]])





if model_name == 'hmtk_sa3':
    comp_table = np.array([  [ 1986,      3. ],
                     [ 1986,      3.5],
                     [ 1986,      4. ],
                     [ 1960,      4.5],
                     [ 1958,      5. ],
                     [ 1958,      5.5],
                     [ 1927,      6. ],
                     [ 1898,      6.5],
                     [ 1885,      7. ],
                     [ 1885,      7.5],
                     [ 1885,      8. ]])
else:
    comp_table = np.array([[ 1980, 3. ],
                   [ 1975, 3.5],
                   [ 1975, 4. ],
                   [ 1965, 4.5],
                   [ 1965, 5. ],
                   [ 1860, 5.5],
                   [ 1860, 6. ]])

    

#config
config = {'Length_Limit': 3., 'BandWidth': 150., 'increment': True, 'magnitude_increment': 0.5}
#smoothing
o = model.run_analysis(  catalogue,
                         config,
                         completeness_table=comp_table,
                         smoothing_kernel = IsotropicGaussian(),
                         #increment = False,
                         )

x = o[:, 0]
y = o[:, 1]
r = o[:, 4]  #/ (res**2)

r = np.array([ np.log10(r) if  r > 0 else np.NaN for r in r ])
#r = np.log10(r)
r[r < 0] = 0.
#r = 

#print np.sqrt(len(x))

from map import rate_map
m = rate_map(x, y, r, "a-value [Frankel1995]", 
            (nx,ny), catalogue=None, origin='lower')
m.show()

#print output_data
# export results
model.write_to_csv(OUTPUT_FILE)
