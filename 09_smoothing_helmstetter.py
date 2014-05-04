'''
Test suite for smoothed seismicity class
'''
import os
import numpy as np

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser
from hmtk.seismicity.smoothing.helmstetter2012 import smoothing


from hmtk.seismicity.smoothing import utils
from hmtk.seismicity.smoothing.smoothed_seismicity import (
    SmoothedSeismicity, _get_adjustment, Grid)

from hmtk.seismicity.smoothing.kernels.isotropic_gaussian import \
    IsotropicGaussian

BASE_PATH = 'data_input/'
OUTPUT_FILE = 'hmtk_bsb2013_helmstetter2012.csv'
#TEST_CATALOGUE = 'hmtk_bsb2013_decluster.csv'
TEST_CATALOGUE = 'hmtk_bsb2013.csv'

#TAIWAN
BASE_PATH = 'data_input/'
OUTPUT_FILE = 'hmtk_taiwan_helmstetter2012.csv'
TEST_CATALOGUE = 'hmtk_taiwan.csv'

calculate_completeness = False


_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)

# catalogue
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()
print catalogue.get_number_events()

print min(catalogue.data['year']), max(catalogue.data['year'])


# Time-varying completeness

comp_table = np.array([[1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0]])

# comp_table = np.array([[1990., 3.0],
#                        [1980., 3.5],
#                        [1970., 4.5],
#                        [1960., 5.0],
#                        [1900., 6.5],
#                        [1800., 7.0]])

comp_table = np.array([[2000., 2.5],
                       [1990., 3.0],
                       [1980., 3.5],
                       [1970., 4.5],
                       [1960., 5.0],
                       [1900., 6.5],
                       [1800., 7.0]])

comp_table = np.array([[ 2005, 2.5],
                        [ 2002,3. ],
                        [ 2000,3.5],
                        [ 1998,4. ],
                        [ 1997,4.5],
                        [ 1997,5. ],
                        [ 1992,5.5],
                        [ 1992,6. ],
                        [ 1988,6.5],
                        [ 1988,7. ]])

if calculate_completeness:
    from hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971
    stepp = Stepp1971()
    
    completeness_config = {'magnitude_bin': 0.5,
                           'time_bin': 5,
                           'increment_lock': True}
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
    create_stepp_plot(stepp, "data_output/stepp_plot_taiwan_01.png")
    



res, spc = 0.5, 100
#res, spc = 1, 50
#res, spc = 0.1, 500

#[xmin, xmax, spcx, ymin, ymax, spcy, zmin, zmax, spcz]
_l = [ 118.5,  124,  res,  20.0,   26.5,  res,    0,   300,   300]
nx = round((_l[1] - _l[0]) / _l[2],0)
ny = round((_l[4] - _l[3]) / _l[5],0)
grid_shape = (nx, ny)
# create grid specifications
grid_limits = utils.Grid.make_from_list(_l)
    
    #[ -80,  -30,  res,  -37,   13,  res,    0,   30,   30])
    #[ 118.5,  124,  res,  20.0,   26.5,  res,    0,   300,   300])


# configure 
config = {'grid_limits' : grid_limits, 
          'completeness_table' : comp_table,
          'b_value' : 1.0, 
          'stationary_time_step_in_days': 365,
          'catalogue_year_start': 1986,
          'catalogue_year_divisor': 2011,
          'target_minimum_magnitude': 4.5,
          'add_before_learning_on_target': True,
          'log': True,
          'plot_bandwidth': False,
          'plot_rate_timeseries': False,
          'plot_stationary_rate': False,
          'plot_target_events_count': False,
      }

# and create smoothing class 
s = smoothing(catalogue = catalogue, 
              config = config)

#     s.plot_catalogue(s.learning_catalogue, title="Learning Catalogue [1960-2000]")
#     s.plot_catalogue(s.target_catalogue, title="Target Catalogue U \ ]1960-2000[")

#     res =  s.optimize_seismicity_model()
#     print res

#s.plot_stationary_rate = True
x, y, r = s.stationary_rate_model(s.r, s.t, r_min=1.0e-4, k=5, a=100, 
                                  normalized=False,
                                  )
# # area normalization...
# r = r / (res**2)
m_min = min(s.learning_catalogue.data['magnitude'])
a = np.log10(r * m_min) + config['b_value']*m_min
#a = np.array([ a if  a >= 0 else 0 for a in a ])

print len(s.learning_catalogue.data['magnitude'])

_x = s.learning_catalogue.data['longitude']
_y = s.learning_catalogue.data['latitude']
_h = s.learning_catalogue.data['h']
_d = s.learning_catalogue.data['d']
_w = s.learning_catalogue.data['w']
_m = s.learning_catalogue.data['magnitude']

# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# 
# plt.close('all')
# f = plt.figure()
# 
# gs1 = gridspec.GridSpec(3, 1)
# 
# ax1 = f.add_subplot(gs1[0])
# ax2 = f.add_subplot(gs1[1])
# ax3 = f.add_subplot(gs1[2])
# 
# #print _w
# alpha = 0.5*np.ones(_w.shape)
# z = np.zeros(_w.shape)
# #print alpha
# color = np.column_stack((_w/255., z, 1 - _w/255., alpha))
# #exit()
# 
# ax1.hist(_h)
# ax1.set_title("Distances on 'Time'")
# ax1.set_xlabel("days")
# 
# ax2.hist(_d)
# ax2.set_title("Distances on 'Space'")
# ax2.set_xlabel("km")
#  
# ax3.hist(_w, bins=30)
# ax3.set_title("Completeness Weights")
# ax3.set_xlabel("weight")
#  
# gs1.tight_layout(f)
#  
# plt.show()
# 
# plt.close('all')
# f = plt.figure()
# ax = f.add_axes([0.1,0.1,0.8,0.8])
# ax.set_title("DistanceTime Bandwidth Distribution")
# ax.set_xlabel("distances [km]")
# ax.set_ylabel("times [days]")
# 
# 
# plt.scatter(_d, _h, s=np.exp(_m), cmap=plt.cm.RdYlGn,
#                  marker='o', facecolors='none', edgecolors=color, #alpha=0.3,
#                  )
# #plt.colorbar(cs)
# plt.show()


from map import rate_map
m = rate_map(x, y, r, "alpha [Helmstetter2012]", 
             (nx,ny), s.learning_catalogue, origin='lower')
m.show()


# m.m.scatter(_x, _y, s=_h, 
#             marker='o', facecolors='none', edgecolors='k', alpha=0.1
#             )
# m.m.scatter(_x, _y, s=_d, 
#             marker='o', facecolors='none', edgecolors='b', alpha=0.1
#             )

m = rate_map(x, y, a, "a-value [Helmstetter2012]", 
             (nx,ny), s.learning_catalogue, origin='lower')
m.show()

#print output_data
# export results
#model.write_to_csv(OUTPUT_FILE)
