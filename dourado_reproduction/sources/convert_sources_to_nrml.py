from hmtk.sources import source_model, area_source

from openquake.nrmllib import models
from openquake.hazardlib import geo

#from decimal import Decimal
import glob
import numpy as np

sources = []
for i, f_geom in enumerate(glob.glob("*.eq.src")):
    
    region = f_geom.split(".")[:-2][0]
    print region
    f = open("%s.eq.rates"%region, 'r')
    m_min, m_max = f.readline().strip().split(" ")
    print "m====>", m_min, m_max
    b, b_sigma = f.readline().strip().split(" ")
    print "b====>", b, b_sigma
    l, l_sigma = f.readline().strip().split(" ")
    print "a====>", l, l_sigma

    mfd = models.TGRMFD(min_mag = m_min,
                        max_mag = m_max, 
                        b_val = float(b), 
                        a_val = np.log10(float(l)*float(m_min)) + float(b)*float(m_min))

    points=[]
    for g in open(f_geom, 'r').readlines():
        c = g.strip().split(" ")
        points.append(geo.Point(float(c[1]), float(c[0])))
    points.append(points[0])
    print points
    geom = geo.Polygon(points)
    print geom
    
    a = area_source.mtkAreaSource(identifier = i, 
                  name = region, 
                  trt = "Stable Continental Crust", 
                  geometry = geom, 
                  upper_depth = "0", 
                  lower_depth = "40", 
                  mag_scale_rel = "WC1994", # default 
                  rupt_aspect_ratio = 1, 
                  mfd = mfd, 
                  nodal_plane_dist = None, 
                  hypo_depth_dist = None)

    sources.append(a)
    
    f.close()

s = source_model.mtkSourceModel(identifier="01", 
                                name = "PSHAB", 
                                sources = sources)

s.serialise_to_nrml(filename = "areas_pshab_dourado.xml", 
                    use_defaults = True)

