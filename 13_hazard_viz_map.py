# -*- coding: utf-8 -*-

import numpy as np
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser

catalogue_file = "data_input/hmtk_bsb2013_pp_decluster.csv"

#from hmtk.seismicity.catalogue import Catalogue

# catalogue
parser = CsvCatalogueParser(catalogue_file)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()



method = "frankel1995"
method = "woo1996"
#method = "helmstetter2012"
#method = "oq-dourado2014_b2"

filename = "data_output/poe_0.1_smooth_decluster_%s.csv"%(method)
filename = "data_output/poe_0.1_%s.csv"%(method)
#filename = "data_output/poe_0.1_smooth_decluster_%s_cum.csv"%(method)
filename = "data_output/bsb2013_helmstetter2012.csv"


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

# d2 = np.genfromtxt(fname=filename2, 
#                  #comments='#',
#                   delimiter=',', 
#                   skiprows = 2, 
#                   #skip_header = 1, 
#                   #skip_footer, 
#                   #converters, missing, missing_values, filling_values, usecols, names, 
#                   #excludelist, deletechars, replace_space, autostrip, 
#                   #case_sensitive, defaultfmt, unpack, usemask, loose, invalid_raise,
#                   )
#  
# x2 = d2[:,0]
# y2 = d2[:,1]
# h2 = d2[:,2]

#print len(x), np.sqrt(len(x))

from map import hazard_map
title = "PGA (poe 10%, 50 years) [ helmstetter2012 ]"

# m = hazard_map(x, y, h2-h, title, 
#                (50, 50), origin='lower')
m = hazard_map(x, y, h, title,
               (50, 50), origin='lower',
#               (100, 100), origin='lower',
               catalogue=catalogue)
m.show()
