from openquake.nrmllib import models
from openquake.hazardlib import geo

from hmtk.sources import source_model, point_source
from hmtk.sources.point_source import mtkPointSource


# catalogue
import os
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser
BASE_PATH = 'data_input/'
TEST_CATALOGUE = 'hmtk_bsb2013_pp_decluster.csv'
_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()
catalogue.sort_catalogue_chronologically()



import glob
import numpy as np

#n=50
n=150
m_min, m_max = 3.5, 7.0
o = []
sources = []
#filename = "/Users/pirchiner/dev/helmstetter/output/conan/rates_2_280.csv"

#smooth = np.genfromtxt("data_output/bsb2013_helmstetter2012.csv", delimiter=",",skip_header=False)
smooth = np.genfromtxt("data_output/bsb2013_helmstetter2012.csv", delimiter=",",skip_header=False)
for i, line in enumerate(smooth):
    #print line
    if str(line[2]) != "nan":
        
        _a = np.log10(float(line[2])*m_min) + 1.*m_min
        #_a = float(line[2])
    #_a = np.log10(sum(r[5])*m_min) + b_value*m_min
    #_a = sum(r[5])
        l = [line[0], line[1], _a ]
        o.append(l)
    #print l

        p = mtkPointSource(identifier = i,
            name = "%s"%i,
            trt='Stable Continental Crust',
            geometry = geo.point.Point(line[0], line[1]),
            upper_depth = 0.,
            lower_depth = 20.,
            mag_scale_rel="WC1994", # default
            rupt_aspect_ratio=1.0,
            mfd=models.TGRMFD(min_mag=m_min, 
                              max_mag=m_max,
                              a_val= _a , 
                              b_val=1.0),
            nodal_plane_dist=None,
            hypo_depth_dist=None)
      
        sources.append(p)
  
s = source_model.mtkSourceModel(identifier="04", 
                                name = "PSHAB-Smoothed Helmstetter2012", 
                                sources = sources)
  
s.serialise_to_nrml(filename = "helmstetter2012/source_model_pshab_helmstetter2012.xml", 
                    use_defaults = True)
        
        

o = np.array(o)

x = o[:, 0]
y = o[:, 1]
r = o[:, 2]
       
from map import rate_map

#print len(x), len(y), len(r), sqrt()
m = rate_map(x, y, r, "a-value [Helmstetter2012]", 
             (n,n), catalogue=catalogue, origin='lower')
m.show()

       
