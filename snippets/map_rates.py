import numpy as np

smooth = np.genfromtxt("../data_output/hmtk_bsb2013_pp_decluster_woo1996.csv", delimiter=",",skip_header=True)
smooth = np.genfromtxt("../data_output/hmtk_bsb2013_decluster_frankel1995.csv", delimiter=",",skip_header=True)
#smooth = np.genfromtxt("../data_output/hmtk_bsb2013_pp_decluster_woo1996.csv", delimiter=",",skip_header=True)


o = np.array(smooth)

x = o[:, 0]
y = o[:, 1]
r = o[:, 4]
#r = o[:, 2] / (res**2)
#r = np.array([ np.log10(r) if  r >= 1 else 0 for r in r ])
#r = np.array([ np.log10(r) if  r >= 1 else 0 for r in r ])

#print np.sqrt(len(x))

from map import rate_map

#print len(x), len(y), len(r), sqrt()
#m = rate_map(x, y, r, "a-value [Woo1996]  $h(m) = %.2f e^{(%.2f m)}$ km"%(model.c, model.d), 
m = rate_map(x, y, r, "a-value [Frankel1995]", 
             (50,50), origin='lower')
m.show()


