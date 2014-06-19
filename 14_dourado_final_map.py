# -*- coding: utf-8 -*-





# catalogue
import os
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser
BASE_PATH = 'data_input/'
TEST_CATALOGUE = 'hmtk_bsb2013_pp_decluster.csv'
_CATALOGUE = os.path.join(BASE_PATH,TEST_CATALOGUE)
parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()
catalogue.sort_catalogue_chronologically()




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

m = hazard_map(x, y, h, "PGA (poe 10%, 50 years) [ dourado2014, crisis2007 ]", 
               (50, 50), catalogue=catalogue, origin='lower')


from hmtk.parsers.source_model.nrml04_parser import nrmlSourceModelParser

source_model_file = "/Users/pirchiner/dev/pshab/dourado_reproduction/source_model.xml"

# read source model file
parser = nrmlSourceModelParser(source_model_file)
source_model = parser.read_file(2.0)

# add source model
#basemap1.add_source_model(source_model, area_border, border_width, point_marker, point_size, overlay)    
m.basemap.add_source_model(source_model, border_width=0.5, overlay=True)    
    


m.show()
