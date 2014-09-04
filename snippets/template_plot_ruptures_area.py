
# <codecell>

import numpy as np
import matplotlib.pyplot as plt

from hmtk.plotting.mapping import HMTKBaseMap
from hmtk.parsers.source_model.nrml04_parser import nrmlSourceModelParser

from openquake.hazardlib.source import AreaSource
 


# <codecell>


# Import an Area Source Model
area_source_file = './s03.xml'
parser = nrmlSourceModelParser(area_source_file)
area_model = parser.read_file()
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

print area_model

from openquake.hazardlib.source import PointSource, AreaSource, SimpleFaultSource, ComplexFaultSource, CharacteristicFaultSource
from openquake.hazardlib.mfd import TruncatedGRMFD, EvenlyDiscretizedMFD
from openquake.hazardlib.scalerel import WC1994
from openquake.hazardlib.geo import Point, NodalPlane, Polygon, Line, ComplexFaultSurface
from openquake.hazardlib.geo.surface import PlanarSurface
from openquake.hazardlib.pmf import PMF
from openquake.hazardlib.tom import PoissonTOM

import numpy
from matplotlib import pyplot
from matplotlib import collections
from mpl_toolkits.basemap import Basemap

def get_map_projection(src):
    """
    Return map projection specific to source.
    """
    # extract rupture enclosing polygon (considering a buffer of 10 km)
    rup_poly = src.get_rupture_enclosing_polygon(10.)
    min_lon = numpy.min(rup_poly.lons)
    max_lon = numpy.max(rup_poly.lons)
    min_lat = numpy.min(rup_poly.lats)
    max_lat = numpy.max(rup_poly.lats)
    
    # create map projection
    m = Basemap(projection='merc', llcrnrlat=min_lat, urcrnrlat=max_lat,
                llcrnrlon=min_lon, urcrnrlon=max_lon, resolution='l')

    return min_lon, max_lon, min_lat, max_lat, m
    
def get_planar_surface_boundary(surf):
    """
    Return coordinates of planar surface boundary
    """
    boundary_lons = numpy.array(
        [surf.top_left.longitude, surf.top_right.longitude,
         surf.bottom_right.longitude, surf.bottom_left.longitude, surf.top_left.longitude]
    )
    boundary_lats = numpy.array(
        [surf.top_left.latitude, surf.top_right.latitude,
         surf.bottom_right.latitude, surf.bottom_left.latitude, surf.top_left.latitude]
    )
    
    return boundary_lons, boundary_lats

    
def get_mesh_boundary(mesh):
    """
    Return coordinates of mesh boundary
    """
    boundary_lons = numpy.concatenate((mesh.lons[0, :], mesh.lons[1:, -1], mesh.lons[-1,:-1][::-1], mesh.lons[:-1, 0][::-1]))
    boundary_lats = numpy.concatenate((mesh.lats[0, :], mesh.lats[1:, -1], mesh.lats[-1,:-1][::-1], mesh.lats[:-1, 0][::-1]))
    
    return boundary_lons, boundary_lats

# define area source
src = AreaSource(
    source_id='1',
    name='area',
    tectonic_region_type='Active Shallow Crust',
    mfd=TruncatedGRMFD(min_mag=5., max_mag=6.5, bin_width=0.2, a_val=3.45, b_val=0.98),
    rupture_mesh_spacing=2.,
    magnitude_scaling_relationship=WC1994(),
    rupture_aspect_ratio=1.,
    temporal_occurrence_model=PoissonTOM(50.),
    upper_seismogenic_depth=2.,
    lower_seismogenic_depth=12.,
    nodal_plane_distribution=PMF([(1, NodalPlane(strike=45, dip=30, rake=0))]),
    hypocenter_distribution=PMF([(1, 7.)]),
    polygon=Polygon([Point(133.5, -22.5), Point(133.5, -23.0), Point(130.75, -23.75), Point(130.75, -24.5),
                     Point(133.5, -26.0), Point(133.5, -27.0), Point(130.75, -27.0), Point(128.977, -25.065),
                     Point(128.425, -23.436), Point(126.082, -23.233), Point(125.669, -22.351), Point(125.4, -20.5),
                     Point(125.75, -20.25), Point(126.7, -21.25), Point(128.5, -21.25), Point(129.25, -20.6),
                     Point(130.0, -20.6), Point(130.9, -22.25), Point(133.0, -22.0), Point(133.5, -22.5)]),
    area_discretization=20.
)


src = area_model

# loop over ruptures, extract rupture surface boundary and magnitude
min_lon, max_lon, min_lat, max_lat, m = get_map_projection(src)

boundaries = []
mags = []
for rup in src.iter_ruptures():
    surf = rup.surface
    mag = rup.mag

    boundary_lons, boundary_lats = get_planar_surface_boundary(surf)
    xx, yy = m(boundary_lons, boundary_lats)
    boundaries.append([(x, y) for x, y in zip(xx, yy)])
    mags.append(mag)


# plot ruptures. Color proportional to magnitude
fig1 = pyplot.figure()

m.drawparallels(numpy.arange(min_lat, max_lat, 5.), labels=[True, False, False, True])
m.drawmeridians(numpy.arange(min_lon, max_lon, 5.), labels=[True, False, False, True])
m.drawcoastlines()
m.drawcountries()

# plot area source boundary
x, y = m(src.polygon.lons, src.polygon.lats)
m.plot(x, y, linewidth=2, color='black')

bounds = collections.LineCollection(boundaries)
bounds.set_array(numpy.array(mags))
pyplot.gca().add_collection(bounds)

cb = pyplot.colorbar(bounds, orientation='horizontal')
cb.set_label('Magnitude')
pyplot.title('Area Source Ruptures', fontsize=20)

pyplot.show()

