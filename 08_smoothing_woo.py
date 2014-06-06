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
OUTPUT_FILE = 'data_output/hmtk_bsb2013_decluster_woo1996.csv'
TEST_CATALOGUE = 'hmtk_bsb2013_decluster.csv'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
#print catalogue.get_number_events()
#print np.min(catalogue.data['magnitude'])


res, spc = 0.5, 100
#res, spc = 1, 50
#res, spc = 2, 25
#res, spc = 0.25, 200


# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
#_l = [ 118.5,  124,  res,  20.0,   26.5,  res,    0,   300,   300]
_l = [ -80,  -30,  res,  -37,   13,  res,    0,   30,   30]
#grid_limits = Grid.make_from_list(_l)

nx = round((_l[1] - _l[0]) / _l[2],0)
ny = round((_l[4] - _l[3]) / _l[5],0)
grid_shape = (nx, ny)



b_value = 1.0

# model
#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, spcz]
grid_limits = utils.Grid.make_from_list([ -80, -30, res, -37, 13, res, 0, 30, 30])

model = SmoothedSeismicityWoo(grid_limits, bvalue=b_value)

# Time-varying completeness
comp_table = np.array([[1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0]])

comp_table = np.array([[1990., 3.0],
                       [1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0],
                       [1900., 6.5],
                       [1800., 7.0]])

# comp_table = np.array([[2000., 2.5],
#                        [1990., 3.0],
#                        [1980., 3.5],
#                        [1970., 4.5],
#                        [1960., 5.0],
#                        [1900., 6.5],
#                        [1800., 7.0]])

#config
#config = {'Length_Limit': 3., 'BandWidth': 100., 'increment': True, 'MagnitudeBinSize': 0.5 }

config = {'min_magnitude': 3.0 , 
          'magnitude_bin': 0.5, 
          'use3d': False,
          'bandwidth_h_limit': 3,
          }

#smoothing
woo = model.run_analysis(catalogue,
                     config,
                     completeness_table=comp_table,
                     smoothing_kernel = IsotropicGaussianWoo())

m_min = config['min_magnitude']
#m_min = 3.0
o = []
for r in woo:
    _a = np.log10(sum(r[5])*m_min) + b_value*m_min
    #_a = sum(r[5])
    l = [r[0], r[1], _a ]
    #print l
    o.append(l)

o = np.array(o)

x = o[:, 0]
y = o[:, 1]
r = o[:, 2]
#r = o[:, 2] / (res**2)
#r = np.array([ np.log10(r) if  r >= 1 else 0 for r in r ])
#r = np.array([ np.log10(r) if  r >= 1 else 0 for r in r ])

print np.sqrt(len(x))

from map import rate_map

#print len(x), len(y), len(r), sqrt()

m = rate_map(x, y, r, "a-value [Woo1996]  h(m) = %.2fe**(%.2f*m) km"%(model.c, model.d), 
             (nx,ny), catalogue=catalogue, origin='lower')
m.show()


# export results
#model.write_to_csv(OUTPUT_FILE)
model.write_rates(OUTPUT_FILE)

#print model.grid
#print model.catalogue
#print model.beta
#print model.data
#print model.kernel
#print output_data

