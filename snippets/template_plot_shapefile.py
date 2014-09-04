import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from shapely.geometry import MultiPolygon, shape
from descartes import PolygonPatch
import fiona
 

# We can extract the London Borough boundaries by filtering on the AREA_CODE key
# Get maps from EDINA http://digimap.edina.ac.uk/digimap/home
# mp = MultiPolygon([shape(pol['geometry']) \
#                    for pol in fiona.open('./politic_brazil_states/politic_brazil_states.shp') \
#                    if  pol['geometry']['type'] == 'Polygon'])


p = []
mp = [] 
for pol in fiona.open('./politic_brazil_states/politic_brazil_states.shp'):
    print pol['geometry']['type']
    if pol['geometry']['type'] == 'Polygon':
        p.append(shape(pol['geometry']))
    elif pol['geometry']['type'] == 'MultiPolygon':
        mp.append(shape(pol['geometry']))



# We can now do GIS-ish operations on each borough polygon!
# we could randomize this by dumping the polygons into a list and shuffling it
# or we could define a random colour using fc=np.random.rand(3,)
# available colour maps are here: http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
cm = plt.get_cmap('RdBu')
num_colours = len(mp)

fig = plt.figure()
ax = fig.add_subplot(111)

minx, miny, maxx, maxy = mp.bounds
w, h = maxx - minx, maxy - miny

ax.set_xlim(minx - 0.2 * w, maxx + 0.2 * w)
ax.set_ylim(miny - 0.2 * h, maxy + 0.2 * h)
ax.set_aspect(1)
 
patches = []
for idx, p in enumerate(mp):
    colour = cm(1. * idx / num_colours)
    patches.append(PolygonPatch(p, fc=colour, ec='#555555', lw=0.2, alpha=1., zorder=1))

ax.add_collection(PatchCollection(patches, match_original=True))

ax.set_xticks([])
ax.set_yticks([])

plt.title("Shapefile polygons rendered using Shapely")
plt.tight_layout()
#plt.savefig('data/london_from_shp.png', alpha=True, dpi=300)
plt.show()