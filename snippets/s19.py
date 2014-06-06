from mpl_toolkits.basemap import Basemap, pyproj
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

serverurl='http://motherlode.ucar.edu:8080/thredds/wms/fmrc/NCEP/NAM/CONUS_12km/NCEP-NAM-CONUS_12km-noaaport_best.ncd?'

wms_cprm = "http://onegeology.cprm.gov.br/cgi-bin/BRA_GSB_EN_Bedrock_Geology/wms?"
wms_oneg = "http://mapdmzrec.brgm.fr/cgi-bin/mapserv54?map=/carto/ogg/mapFiles/CGMW_Bedrock_and_Structural_Geology.map&"

wmsl_oneg = {'server_url': wms_oneg,
                  'layers': ['World_CGMW_50M_Geology'],
                  }


wmsl_br_blt = {'server_url': wms_cprm,
                'layers': ['BRA_GSB_EN_1M_BLT'],
                'styles': ['default'],
              }

wmsl_br_ba = {'server_url': wms_cprm,
                'layers': ['BRA_GSB_EN_1M_BA'],
                'styles': ['default'],
              }
# SA
lon_min = -90; lon_max = -30.0
lat_min = -60; lat_max =  30.0

# BR
lon_min = -80; lon_max = -30.0
lat_min = -37; lat_max =  13.0

m = Basemap(llcrnrlon=lon_min, urcrnrlat=lat_max,
            urcrnrlon=lon_max, llcrnrlat=lat_min,resolution='i',epsg=4326)

m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)


m.wmsimage(wmsl_oneg['server_url'], xpixels=500,verbose=True,
           layers=wmsl_oneg['layers'],
           format='image/png',
           transparent=True,
           alpha=0.5,
           )


m.wmsimage(wmsl_br_blt['server_url'], xpixels=500,verbose=True,
           layers=wmsl_br_blt['layers'],
           format='image/png',
           transparent=True,
           alpha=0.5,
           )


#f = plt.figure()

plt.show()

