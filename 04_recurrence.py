
# In[ ]:

# Import required modules
import numpy as np
import matplotlib.pyplot as plt

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter

# HMTK Completeness Tools
from hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971

# Import Recurrence Tools
from hmtk.seismicity.occurrence.b_maximum_likelihood import BMaxLikelihood
from hmtk.seismicity.occurrence.kijko_smit import KijkoSmit
from hmtk.seismicity.occurrence.weichert import Weichert

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

stepp = Stepp1971()

completeness_config = {'magnitude_bin': 1,
                       'time_bin': 5,
                       'increment_lock': False}
print completeness_config

# Run analysis
print 'Running Stepp (1971) completeness analysis:'
completeness_table = stepp.completeness(catalogue, completeness_config)
print completeness_table
print 'done!'


# In[ ]:

from hmtk.plotting.seismicity.catalogue_plots import (plot_observed_recurrence, 
                                                      get_completeness_adjusted_table,
                                                      _get_catalogue_bin_limits)

magnitude_bin = 0.1
end_year = 2010

earthquake_count = get_completeness_adjusted_table(catalogue, 
                                                   completeness_table, 
                                                   magnitude_bin, 
                                                   catalogue.end_year)
#print 'Magnitude  N(OBS)     N(CUM)   Log10(Nc)'
#for row in earthquake_count:
#    print '%6.2f %10.3f %10.3f %10.3f' %(row[0], row[1], row[2], row[3]) 

plot_observed_recurrence(catalogue, completeness, magnitude_bin, catalogue.end_year)


# In[ ]:

# Set up the configuration parameters
recurrence_config = {'reference_magnitude': None,
                     'magnitude_interval': 0.5,
                     'Average Type': 'Weighted'}

bml_recurrence = BMaxLikelihood()

bval, sigmab, rate, sigma_rate = bml_recurrence.calculate(catalogue, 
                                                          recurrence_config, 
                                                          completeness_table)

print 'B-value = %9.4f +/- %9.4f' %(bval, sigmab)
print 'Rate (M >= 4.0) = %9.4f +/- %9.4f' %(rate, sigma_rate)


# In[ ]:

# Set up the configuration parameters
bks_recurrence = KijkoSmit()

bval, sigmab, rate, sigma_rate = bks_recurrence.calculate(catalogue, 
                                                          recurrence_config, 
                                                          completeness_table)

print 'B-value = %9.4f +/- %9.4f' % (bval, sigmab)
print 'Rate (M >= 4.0) = %9.4f +/- %9.4f' % (rate, sigma_rate)


# In[ ]:

# Set up the configuration parameters
bwc_recurrence = Weichert()

bval, sigmab, rate, sigma_rate = bwc_recurrence.calculate(catalogue, 
                                                          recurrence_config, 
                                                          completeness_table)

print 'B-value = %9.4f +/- %9.4f' %(bval, sigmab)
print 'Rate (M >= 4.0) = %9.4f +/- %9.4f' %(rate, sigma_rate)


# In[ ]:



