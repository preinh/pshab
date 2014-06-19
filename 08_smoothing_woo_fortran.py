'''
Test suite for smoothed seismicity class
'''
import os
import csv
import numpy as np

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser

#from hmtk.seismicity.catalogue import Catalogue

from hmtk.seismicity.smoothing import utils
from hmtk.seismicity.smoothing.smoothed_seismicity_woo \
    import SmoothedSeismicityWoo

from hmtk.seismicity.smoothing.kernels.woo_1996 import \
    IsotropicGaussianWoo

BASE_PATH = 'data_input/'
OUTPUT_FILE = 'data_output/hmtk_bsb2013_pp_decluster_woo_rates.csv'
TEST_CATALOGUE = 'hmtk_bsb2013_pp_decluster.csv'

rate_file = '/Users/pirchiner/dev/codigo_woo/pshab/woo_smoothing_data_inf.dat'

_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
#print catalogue.get_number_events()
#print np.min(catalogue.data['magnitude'])


#res, spc = 0.5, 100
res, spc = 1, 50
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


data = np.genfromtxt(rate_file)

x0,xf,dx = min(data[:,0]), max(data[:,0]), 1
y0,yf,dy = min(data[:,1]), max(data[:,1]), 1
m0,mf,dm = min(data[:,2]), max(data[:,2]), 0.5

fid = open(OUTPUT_FILE, 'wt')
header_info = ['Longitude', 'Latitude', 'Smoothed Rate']
writer = csv.DictWriter(fid, fieldnames=header_info)
headers = dict((name0, name0) for name0 in header_info)
# Write to file
writer.writerow(headers)

x,y,r = [],[],[]
for i in np.arange(x0,xf+dx,dx):
    for j in np.arange(y0,yf+dy,dy):
        idx = np.logical_and(data[:,0] == i, data[:,1] == j)
        cum_rate = np.sum(data[idx,3])
        a_value = np.log(cum_rate*3.0) + 1*3.0
        x.append(i)
        y.append(j)
        r.append(a_value)
        #print i, j, a_value

        row_dict = {'Longitude': '%.5f' % i,
                    'Latitude': '%.5f' % j,
                    'Smoothed Rate': '%.5e' % a_value,
                    }
        writer.writerow(row_dict)
fid.close()

x = np.array(x)
y = np.array(y)
r = np.array(r)


# 
# x = o[:, 0]
# y = o[:, 1]
# r = o[:, 2]
#r = o[:, 2] / (res**2)
#r = np.array([ np.log10(r) if  r >= 1 else 0 for r in r ])
#r = np.array([ np.log10(r) if  r >= 1 else 0 for r in r ])

#print np.sqrt(len(x))

from map import rate_map

#print len(x), len(y), len(r), sqrt()
#print model.c, model.d
#m = rate_map(x, y, r, "a-value [Woo1996]  $h(m) = %.2f e^{(%.2f m)}$ km"%(model.c, model.d), 
m = rate_map(x, y, r, "a-value [woo1996]", 
             (nx,ny), catalogue=catalogue, origin='lower')
m.show()





# export results
#model.write_to_csv(OUTPUT_FILE)
#model.write_rates(OUTPUT_FILE)

#print model.grid
#print model.catalogue
#print model.beta
#print model.data
#print model.kernel
#print output_data

