from openquake.nrmllib import models
from openquake.hazardlib import geo

from hmtk.sources import source_model, point_source
from hmtk.sources.point_source import mtkPointSource

import glob
import numpy as np

m0=2.5
sources = []
smooth = np.genfromtxt("../hmtk_bsb2013_decluster_smoothing_data.csv", delimiter=",",skip_header=True)
for i, line in enumerate(smooth):
    #print line
    p = mtkPointSource(identifier = i,
        name = "%s"%i,
        trt='Stable Continental Crust',
        geometry = geo.point.Point(line[0], line[1]),
        upper_depth = 0.,
        lower_depth = 30.,
        mag_scale_rel="WC1994", # default
        rupt_aspect_ratio=1.0,
        mfd=models.TGRMFD(min_mag=m0, 
                          max_mag=7.0,
                          a_val=float(line[4]), 
                          b_val=1.0),
        nodal_plane_dist=None,
        hypo_depth_dist=None)
 
    sources.append(p)
 
s = source_model.mtkSourceModel(identifier="02", 
                                name = "PSHAB-Smoothed (decluster)", 
                                sources = sources)
 
s.serialise_to_nrml(filename = "source_model_pshab_decluster_smoothed.xml", 
                    use_defaults = True)
