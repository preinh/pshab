# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt

from hmtk.plotting.mapping import HMTKBaseMap
from hmtk.parsers.source_model.nrml04_parser import nrmlSourceModelParser

# <codecell>


# Import an Area Source Model
area_source_file = './s03.xml'
parser = nrmlSourceModelParser(area_source_file)
area_model = parser.read_file()

# <codecell>

# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}

# Create a hmtk basemap
basemap1 = HMTKBaseMap(map_config, 'Source Models')
# Add fault sources
#basemap1.add_source_model(fault_model, overlay=True)
# Add area sources
basemap1.add_source_model(area_model, area_border='b-')

# <codecell>

# Load in the catalogue
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser

input_file = '../data_input/hmtk_bsb2013.csv'
parser = CsvCatalogueParser(input_file)
catalogue = parser.read_file()
print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)

# <codecell>

area_model.sources[0].catalogue = 'data_input/hmtk_bsb2013.csv'
#area_model.sources[0].catalogue = catalogue

# <codecell>

from hmtk.seismicity.selector import CatalogueSelector
# Create an instance of the selector class
selector = CatalogueSelector(catalogue, create_copy=True)

# <codecell>

for source in area_model.sources:
    # Selects the earthquakes within each polygon
    source.select_catalogue(selector)
    print 'Source Number %s - %s contains %8.0f events' %(source.id, source.name, source.catalogue.get_number_events())

# <codecell>


# Example - show earthquakes in the Gulf of Corinth zone
map_config_goc = {'min_lon': 21.0, 'max_lon': 25.0, 'min_lat': 37.0, 'max_lat': 39.0, 'resolution':'h'}
# Configure the limits of the map and the coastline resolution
map_config_goc = {'min_lon': -58.9, 'max_lon': -55.5, 'min_lat': -13.8, 'max_lat': -10.0, 'resolution':'l'}


basemap2 = HMTKBaseMap(map_config_goc, 'MatoGrosso')
basemap2.add_catalogue(area_model.sources[0].catalogue, overlay=True)
basemap2.add_source_model(area_model, area_border='k-')


# <codecell>


