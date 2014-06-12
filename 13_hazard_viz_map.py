# -*- coding: utf-8 -*-

import numpy as np


#method = "frankel1995"
method = "woo1996"
#method = "helmstetter2012"
#method = "oq-dourado2014_b2"

#filename = "data_output/poe_0.1_smooth_decluster_%s.csv"%(method)
filename = "data_output/poe_0.1_%s.csv"%(method)


d = np.genfromtxt(fname=filename, 
                 #comments='#',
                  delimiter=',', 
                  skiprows = 2, 
                  #skip_header = 1, 
                  #skip_footer, 
                  #converters, missing, missing_values, filling_values, usecols, names, 
                  #excludelist, deletechars, replace_space, autostrip, 
                  #case_sensitive, defaultfmt, unpack, usemask, loose, invalid_raise,
                  )

x = d[:,0]
y = d[:,1]
h = d[:,2]

#print len(x), np.sqrt(len(x))

from map import hazard_map
title = "PGA (poe 10%%, 50 years) [ %s ]"%method

m = hazard_map(x, y, h, title, 
               (50, 50), origin='lower')
m.show()
