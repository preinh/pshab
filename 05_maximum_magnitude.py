
# In[ ]:

# Import required modules
import numpy as np
import matplotlib.pyplot as plt

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter

# Import Mmax Tools
from hmtk.seismicity.max_magnitude.kijko_nonparametric_gaussian import KijkoNonParametricGaussian
from hmtk.seismicity.max_magnitude.kijko_sellevol_bayes import KijkoSellevolBayes
from hmtk.seismicity.max_magnitude.kijko_sellevol_fixed_b import KijkoSellevolFixedb
from hmtk.seismicity.max_magnitude.cumulative_moment_release import CumulativeMoment

print 'Import OK!'


# In[ ]:

input_file = 'data_input/hmtk_bsb2013.csv'

parser = CsvCatalogueParser(input_file)
catalogue = parser.read_file()
print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)

# Sort catalogue chronologically
catalogue.sort_catalogue_chronologically()
print 'Catalogue sorted chronologically!'

# Plot magnitude time density
from hmtk.plotting.seismicity.catalogue_plots import plot_magnitude_time_density
magnitude_bin = 0.2
time_bin = 10.0
plot_magnitude_time_density(catalogue, magnitude_bin, time_bin)


# In[ ]:

mmax_config = {'b-value': 1.0,
               'input_mmin': 4.5,
               'input_mmax': None,
               'input_mmax_uncertainty': 0.5}

mmax_ks = KijkoSellevolFixedb()

mmax, mmax_sigma = mmax_ks.get_mmax(catalogue, mmax_config)

print 'Mmax = %8.3f +/- %8.3f' %(mmax, mmax_sigma)


# In[ ]:

mmax_config = {'b-value': 1.0,
               'sigma-b': 0.05,
               'input_mmin': 4.5,
               'input_mmax': None,
               'input_mmax_uncertainty': 0.5}

mmax_ksb = KijkoSellevolBayes()

mmax, mmax_sigma = mmax_ksb.get_mmax(catalogue, mmax_config)

print 'Mmax = %8.3f +/- %8.3f' %(mmax, mmax_sigma)


# In[ ]:

mmax_config = {'number_earthquakes': 100, # Selects the N largest earthquakes in the catalogue for analysis
               'input_mmax': None,
               'input_mmax_uncertainty': 0.5}

mmax_knpg = KijkoNonParametricGaussian()
mmax, mmax_sigma = mmax_knpg.get_mmax(catalogue, mmax_config)
print 'Mmax = %8.3f +/- %8.3f' %(mmax, mmax_sigma)


# In[ ]:

mmax_config = {'number_bootstraps': 1000} # Number of samples for the uncertainty analyis

mmax_cum_mo = CumulativeMoment()
mmax, mmax_sigma = mmax_cum_mo.get_mmax(catalogue, mmax_config)
print 'Mmax = %8.3f +/- %8.3f' %(mmax, mmax_sigma)

