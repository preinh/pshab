# -*- coding: utf-8 -*-

import numpy as np


method = "frankel1995"
#method = "woo1996"
method = "helmstetter2012"
#method = "oq-dourado2014"

filename = "dourado_reproduction/final_result_dourado/brasil_8sources1_475_0.csv"
#filename = "data_output/poe_0.1_%s.csv"%(method)


d = np.genfromtxt(fname=filename, 
                 #comments='#',
                  delimiter=',', 
                  skiprows = 1, 
                  #skip_header = 1, 
                  #skip_footer, 
                  #converters, missing, missing_values, filling_values, usecols, names, 
                  #excludelist, deletechars, replace_space, autostrip, 
                  #case_sensitive, defaultfmt, unpack, usemask, loose, invalid_raise,
                  )

x = d[:,0]
y = d[:,1]
h = d[:,2]

# gal (cm/s^2) -> g (10 m/s^2) <==> h *= 1e-3
h = h*1.e-3

#print len(x), np.sqrt(len(x))

from map import hazard_map

m = hazard_map(x, y, h, "PGA (g) poe 10%, 50 years [dourado2014] CRISIS2007", 
               (50, 50), origin='lower')
m.show()
