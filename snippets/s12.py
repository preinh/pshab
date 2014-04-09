from openquake.nrmllib import models
from openquake.hazardlib import geo

from hmtk.sources import source_model, point_source
from hmtk.sources.point_source import mtkPointSource

import csv

import glob
import numpy as np

m0=2.0
sources = []
filename = "../data_output/stationary_rate_bsb2013.csv"

r = [l for l in csv.reader(open(filename), delimiter=',', quotechar='"')]
#smooth = np.genfromtxt("../data_output/hmtk_bsb2013_decluster_woo_rates.csv", delimiter=",",skip_header=True)
for i, line in enumerate(r[1:]):
    rate = line[2].strip
    #print rates
    
    p = mtkPointSource(identifier = i,
        name = "%s"%i,
        trt='Stable Continental Crust',
        geometry = geo.point.Point(float(line[0]), float(line[1])),
        upper_depth = 0.,
        lower_depth = 30.,
        mag_scale_rel="WC1994", # default
        rupt_aspect_ratio=1.0,
        mfd=models.TGRMFD(min_mag=m0, 
                          max_mag=7.0,
                          a_val=float(line[2]), 
                          b_val=1.0),
        nodal_plane_dist=None,
        hypo_depth_dist=None)
    #print p
 
    sources.append(p)
 
s = source_model.mtkSourceModel(identifier="04", 
                                name = "PSHAB-Helmstetter2012", 
                                sources = sources)
 
s.serialise_to_nrml(filename = "../helmstetter2012/source_model_pshab_helmstetter2012.xml", 
                    use_defaults = True)
