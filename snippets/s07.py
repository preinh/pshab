from openquake.nrmllib import models
from openquake.hazardlib import geo

from hmtk.sources import source_model, point_source
from hmtk.sources.point_source import mtkPointSource

from decimal import Decimal

p = mtkPointSource(identifier = '001',
    name = 'A Point Source',
    trt='Stable Continental Crust',
    geometry = geo.point.Point(10., 10.),
    upper_depth = 0.,
    lower_depth = 30.,
    mag_scale_rel="WC1994", # default
    rupt_aspect_ratio=1.0,
    mfd=models.TGRMFD(a_val=3., b_val=1.0, min_mag=2.5, max_mag=7.0),
    nodal_plane_dist=None,
    hypo_depth_dist=None)


s = source_model.mtkSourceModel(identifier="09", 
                                name = "nick smoothed", 
                                sources = [p])

s.serialise_to_nrml(filename = "smoothed_model.xml", 
                    use_defaults = True)



# 
# # Define a complete source
# area_geom = polygon.Polygon([point.Point(10., 10.),
#                              point.Point(12., 10.),
#                              point.Point(12., 8.),
#                              point.Point(10., 8.)])
# 
# 
# 
# 
# area_source = mtkAreaSource('001',
#     'Area Source',
#     trt='Active Shallow Crust',
#     geometry = area_geom,
#     upper_depth = 0.,
#     lower_depth = 20.,
#     mag_scale_rel=None,
#     rupt_aspect_ratio=1.0,
#     mfd=models.TGRMFD(a_val=3., b_val=1.0, min_mag=5.0, max_mag=8.0),
#     nodal_plane_dist=None,
#     hypo_depth_dist=None)

# expected_source = models.AreaSource(
#     '001',
#     'A Point Source',
#     geometry=models.AreaGeometry(area_geom.wkt, 0., 20.),
#     mag_scale_rel='WC1994',
#     rupt_aspect_ratio=1.0,
#     mfd=models.TGRMFD(a_val=3., b_val=1.0, min_mag=5.0, max_mag=8.0),
#     nodal_plane_dist=None,
#     hypo_depth_dist=None)
# test_source = self.area_source.create_oqnrml_source(use_defaults=True)
# self.assertTrue(isinstance(test_source, models.AreaSource))
# self.assertEqual(test_source.id, expected_source.id)
# self.assertEqual(test_source.name, expected_source.name)
# self.assertAlmostEqual(test_source.mfd.b_val,
#                        expected_source.mfd.b_val)




#         simple_polygon = polygon.Polygon([point.Point(2.0, 3.0),
#                                           point.Point(3.0, 3.0),
#                                           point.Point(3.0, 2.0),
#                                           point.Point(2.0, 2.0)])
#         self.area_source.create_geometry(simple_polygon, 0., 30.)
#         self.area_source.select_catalogue(selector0, 0.)
