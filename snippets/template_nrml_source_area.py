from hmtk.sources import source_model, area_source

from openquake.nrmllib import models
from openquake.hazardlib import geo

from decimal import Decimal

a = area_source.mtkAreaSource(identifier = "01", 
                  name = "area source name", 
                  trt = "stable crust", 
                  geometry = geo.Polygon([geo.Point(-58.73, -10.33),
                                          geo.Point(-58.74, -13.54),
                                          geo.Point(-55.94, -13.59), 
                                          geo.Point(-56.58, -10.31),
                                          geo.Point(-58.73, -10.33)]), 
                  upper_depth = "0", 
                  lower_depth = "30", 
                  mag_scale_rel = "WC1994", # default 
                  rupt_aspect_ratio = 1, 
                  mfd = models.TGRMFD(min_mag=3.0,
                                      max_mag=7.0, 
                                      b_val=0.847, 
                                      a_val=0.737), 
                  nodal_plane_dist = models.NodalPlane(Decimal('1.0'), 
                                                       strike=0., 
                                                       dip=90.,
                                                       rake=0.), 
                  hypo_depth_dist = None)

#a.create_oqnrml_source

s = source_model.mtkSourceModel(identifier="09", 
                                        name = "sources model name", 
                                        sources = [a])

s.serialise_to_nrml(filename = "s03.xml", 
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
