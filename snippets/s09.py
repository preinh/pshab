from openquake.nrmllib import models
from openquake.hazardlib import geo

from hmtk.sources import source_model, point_source
from hmtk.sources.point_source import mtkPointSource

import csv

import glob
import numpy as np

m0=3.0
sources = []
filename = "../data_output/hmtk_bsb2013_decluster_woo_rates.csv"

r = [l for l in csv.reader(open(filename), delimiter=',', quotechar='"')]
#smooth = np.genfromtxt("../data_output/hmtk_bsb2013_decluster_woo_rates.csv", delimiter=",",skip_header=True)
for i, line in enumerate(r[1:]):
    rates = line[5].split(" ")
    #print rates
    
    p = mtkPointSource(identifier = i,
        name = "%s"%i,
        trt='Stable Continental Crust',
        geometry = geo.point.Point(float(line[0]), float(line[1])),
        upper_depth = 0.,
        lower_depth = 30.,
        mag_scale_rel="WC1994", # default
        rupt_aspect_ratio=1.0,
        mfd=models.IncrementalMFD(min_mag=float(line[3]), 
                                  bin_width=float(line[4]),
                                  occur_rates=rates),
        nodal_plane_dist=None,
        hypo_depth_dist=None)
    #print p
 
    sources.append(p)
 
s = source_model.mtkSourceModel(identifier="03", 
                                name = "PSHAB-Woo (decluster)", 
                                sources = sources)
 
s.serialise_to_nrml(filename = "../woo/source_model_pshab_decluster_woo.xml", 
                    use_defaults = True)
