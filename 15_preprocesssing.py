# -*- coding: utf-8 -*-

### 
###    Imports 
###

# Python Numerical and Plotting Libraries
import pickle
import numpy as np
import matplotlib.pyplot as plt
plt.xkcd()

# HMTK Catalogue Import/Export Libraries
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter

# HMTK Mapping Tools
from hmtk.plotting.mapping import HMTKBaseMap

# HMTK Catalogue Plotting Tools
from hmtk.plotting.seismicity.catalogue_plots import (plot_depth_histogram,
                                                      plot_magnitude_time_scatter,
                                                      plot_magnitude_time_density,
                                                      plot_magnitude_depth_density,
                                                      plot_weekday_histogram,
                                                      plot_hour_histogram,
                                                      plot_rate,
                                                      plot_observed_recurrence)


# HMTK Declustering Tools
from hmtk.seismicity.declusterer.dec_afteran import Afteran
from hmtk.seismicity.declusterer.dec_gardner_knopoff import GardnerKnopoffType1
from hmtk.seismicity.declusterer.distance_time_windows import GardnerKnopoffWindow, GruenthalWindow, UhrhammerWindow


# HMTK Completeness Tools
from hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971
from hmtk.plotting.seismicity.completeness.plot_stepp_1972 import create_stepp_plot



def read_catalog(input_catalogue_file, m_min=3.0):
    
    
    ### 
    ###    Catalogue cache or read/cache
    ###
    
    try:
        print '--Reading Catalog'
        print input_catalogue_file
        catalogue = pickle.load(open(input_catalogue_file + ".pkl", 'rb'))
        print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
        print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)
    except:
        print '--Reading Catalog'
        parser = CsvCatalogueParser(input_catalogue_file + ".csv")
        catalogue = parser.read_file()

        print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
        print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)
    
        # Sort catalogue chronologically
        catalogue.sort_catalogue_chronologically()
        print 'Catalogue sorted chronologically!'
    
        print '--Removing nan magnitudes'
        valid_magnitudes = np.logical_not(np.isnan(catalogue.data['magnitude']))
        catalogue.select_catalogue_events(valid_magnitudes)
        print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
        print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)

        print '--Removing magnitudes < %f'%m_min
        valid_magnitudes = catalogue.data['magnitude'] >= m_min
        catalogue.select_catalogue_events(valid_magnitudes)
        print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
        print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)
         
        print '--Removing nan depths'
        valid_depths = np.logical_not(np.isnan(catalogue.data['depth']))
        catalogue.select_catalogue_events(valid_depths)
        print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
        print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)
         
        print '--Removing 0 days'
        valid_months = catalogue.data['day'] != 0
        catalogue.select_catalogue_events(valid_months)
        print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
        print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)
        
        # Cache
        # Set-up the file writer
        print '--Caching'
        output_file_name = input_catalogue_file + '.csv'
        #writer = CsvCatalogueWriter(output_file_name)
        #writer.write_file(catalogue)
        #exit()
         
        #print 'File %s written' % output_file_name
        f=open(input_catalogue_file + ".pkl",'wb')
        pickle.dump(catalogue, f)
        f.close()

    return catalogue


def decluster_catalogue(catalogue, config):
    
    
    ### 
    ###    Catalogue cache or read/cache
    ###

    # Set up the declustering algorithm
    # Step 1 - set-up the tool
    if config['decluster_method'] == 'afteran':
        decluster_method = Afteran()
    elif config['decluster_method'] == 'gardner_knopoff':
        decluster_method = GardnerKnopoffType1()
    else:
        print "invalid decluster_method configuration: use [afteran|gardner_knopoff]"    
        return None 
    
    
    print 'Running declustering ...'
    cluster_vector, flag_vector = decluster_method.decluster(catalogue, config)
    print 'done!'
    print '%s clusters found' % np.max(cluster_vector)
    print '%s Non-poissionian events identified' % np.sum(flag_vector != 0)

    
    if config['plot']:
        ### 
        ###    Map Config 
        ###
        
        map_dpi = 90 
        add_geology = True
        add_sourcemodel = True
        savefig=False
        
        #map_title = 'Brazilian Seismic Zones'
        map_title = 'Clusters'
        #map_title = 'ISC-GEM Catalogue'
        #map_title = 'South-American Lithology'
        
        
        # Configure the limits of the map and the coastline resolution
        map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
        #map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}
        #map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}
        
        basemap = HMTKBaseMap(map_config, map_title, dpi=map_dpi)       
        #basemap.add_catalogue(catalogue, linewidth=0.2, alpha=0.1, overlay=True)
    
        idx = cluster_vector != 0
        x = catalogue.data['longitude'][idx]
        y = catalogue.data['latitude'][idx]
        c = cluster_vector[idx]
        
        basemap.add_colour_scaled_points(x, y, c, 
                                         overlay=True,
                                         shape='s', alpha=0.5, size=100, 
                                         linewidth=0.5, facecolor='none', 
                                         cmap=plt.cm.get_cmap('Paired'),
                                         )
    
        plt.show()

        if config['figname']:
            basemap.savemap(config['figname'])

    
    print 'Original catalogue had %s events' % catalogue.get_number_events()
    catalogue.select_catalogue_events(flag_vector == 0)
    print 'Purged catalogue now contains %s events' % catalogue.get_number_events()

    if config['filename']:
        writer = CsvCatalogueWriter(config['filename'])
        writer.write_file(catalogue)
    
    return catalogue







# quality control
    # day_of_week plot
    # hour_of_day plot
    # seismic_rate plot
    # cumulative number of eq
    # depth histogram

# decluster catalog
    # save decluster catalog

# completeness catalog
    # magnitude density plot
    # save complete catalog

# max_magnitude
    





if __name__ == '__main__':

    ### 
    ###    Model Config 
    ###
    

 
    model_name = 'hmtk_sa3'
    #model_name = 'hmtk_bsb2013'

    
    ### 
    ###    Map Config 
    ###
    
    dpi = 150 
    add_geology = True
    add_sourcemodel = True
    savefig=False
    
    plot_quality = False
    plot_density = False

    plot_stepp = False
    
    declustered = True
    if declustered:
        model_name += '_pp_decluster'

    print model_name
    input_catalogue_file = 'data_input/' + model_name

    output_base='/Users/pirchiner/dev/pshab/data_output/'+model_name
    output_base='/Users/pirchiner/Desktop/'+model_name
    

    ### 
    ###    Catalogue 
    ###
    
    print input_catalogue_file
    # read catalog
    catalogue = read_catalog(input_catalogue_file)

    valid_months = catalogue.data['day'] != 0
    catalogue.select_catalogue_events(valid_months)

    valid_years = catalogue.data['year'] >= 1900
    catalogue.select_catalogue_events(valid_years)


    if plot_quality:
        # quality control
    
        # seismic_rate plot
        plot_rate(catalogue, color='#5fbdce', filename=output_base+"_rate.png", linewidth=2)
        # seismic_cumulative rate plot
        plot_rate(catalogue, cumulative=True, color='#5fbdce', filename=output_base+"_cum.png", linewidth=2)
        # depth histogram
        plot_depth_histogram(catalogue, 30, normalisation=True, filename=output_base+"_depth.png", color='#5fbdce', alpha=0.6)    
        # day_of_week plot
        plot_weekday_histogram(catalogue, color='#5fbdce', alpha=0.6, filename=output_base+"_weekday.png")    
        # hour_of_day plot
        plot_hour_histogram(catalogue, color='#5fbdce', alpha=0.6, filename=output_base+"_hour.png")    
        # seismic_rate plot
        # cumulative number of eq



    if not declustered:
        # decluster catalog
            # plot decluster
            # save decluster catalog
        config = {
                  'decluster_method': 'gardner_knopoff', # afteran | gardner_knopoff
                  #'time_distance_window': GardnerKnopoffWindow(),
                  'time_distance_window': GruenthalWindow(),
                  #'time_distance_window': UhrhammerWindow(),
                  # afteran
                  'time_window': 60.,
                  # gardner_knopoff
                  'fs_time_prop': 1.0,
                  # write declustered
                  'filename': None,
                  #'filename': output_base+"_pp_decluster.csv",
                  # plot cluster
                  'plot':False,
                  'figname': output_base+"_pp_decluster.png",
                  }
        declustered_catalogue = decluster_catalogue(catalogue, config)
        plot_rate(catalogue, cumulative=True, color='#F0E797', new_figure=True, overlay=True, linewidth=1.5, label="Gardner-Knopoff/Gruenthal", alpha=0.8)


        catalogue = read_catalog(input_catalogue_file)
        valid_months = catalogue.data['day'] != 0
        catalogue.select_catalogue_events(valid_months)
        valid_years = catalogue.data['year'] >= 1900
        catalogue.select_catalogue_events(valid_years)
        config = {
                  'decluster_method': 'gardner_knopoff', # afteran | gardner_knopoff
                  'time_distance_window': GardnerKnopoffWindow(),
                  #'time_distance_window': GruenthalWindow(),
                  #'time_distance_window': UhrhammerWindow(),
                  # afteran
                  'time_window': 60.,
                  # gardner_knopoff
                  'fs_time_prop': 1.0,
                  # write declustered
                  'filename': None,
                  #'filename': output_base+"_pp_decluster.csv",
                  # plot cluster
                  'plot':False,
                  'figname': output_base+"_pp_decluster.png",
                  }
        declustered_catalogue = decluster_catalogue(catalogue, config)
        plot_rate(catalogue, cumulative=True, color='#FF9D84', new_figure=False, overlay=True, linewidth=1.5, label="Gardner-Knopoff/Gardner-Knopoff", alpha=0.8)

        
        catalogue = read_catalog(input_catalogue_file)
        valid_months = catalogue.data['day'] != 0
        catalogue.select_catalogue_events(valid_months)
        valid_years = catalogue.data['year'] >= 1900
        catalogue.select_catalogue_events(valid_years)
        config = {
                  'decluster_method': 'gardner_knopoff', # afteran | gardner_knopoff
                  #'time_distance_window': GardnerKnopoffWindow(),
                  #'time_distance_window': GruenthalWindow(),
                  'time_distance_window': UhrhammerWindow(),
                  # afteran
                  'time_window': 60.,
                  # gardner_knopoff
                  'fs_time_prop': 1.0,
                  # write declustered
                  'filename': None,
                  #'filename': output_base+"_pp_decluster.csv",
                  # plot cluster
                  'plot':False,
                  'figname': output_base+"_pp_decluster.png",
                  }
        declustered_catalogue = decluster_catalogue(catalogue, config)
        plot_rate(catalogue, cumulative=True, color='#FF5460', new_figure=False, overlay=True, linewidth=1.5, label="Gardner-Knopoff/Uhrhammer", alpha=0.8)

        
        
        catalogue = read_catalog(input_catalogue_file)
        valid_months = catalogue.data['day'] != 0
        catalogue.select_catalogue_events(valid_months)
        valid_years = catalogue.data['year'] >= 1900
        catalogue.select_catalogue_events(valid_years)
        config = {
                  'decluster_method': 'afteran', # afteran | gardner_knopoff
                  #'time_distance_window': GardnerKnopoffWindow(),
                  'time_distance_window': GruenthalWindow(),
                  #'time_distance_window': UhrhammerWindow(),
                  # afteran
                  'time_window': 60.,
                  # gardner_knopoff
                  'fs_time_prop': 1.0,
                  # write declustered
                  'filename': None,
                  #'filename': output_base+"_pp_decluster.csv",
                  # plot cluster
                  'plot':False,
                  'figname': output_base+"_pp_decluster.png",
                  }
        declustered_catalogue = decluster_catalogue(catalogue, config)
        plot_rate(declustered_catalogue, cumulative=True, color='#75B08A', new_figure=False, overlay=True, linewidth=1.5, label="Afteran/Gruenthal", alpha=0.8)

        catalogue = read_catalog(input_catalogue_file)
        valid_months = catalogue.data['day'] != 0
        catalogue.select_catalogue_events(valid_months)
        valid_years = catalogue.data['year'] >= 1900
        catalogue.select_catalogue_events(valid_years)
        
        plot_rate(catalogue, cumulative=True, color='#22475E', new_figure=False, overlay=True, linewidth=1.5, label="Original", alpha=0.8)
        plt.legend(loc="upper left", fontsize='small')
        plt.show()

    # seismic_rate plot
    #plot_rate(catalogue, color='#5fbdce', filename=output_base+"_rate.png", linewidth=2)
    # seismic_cumulative rate plot
    #plot_rate(catalogue, cumulative=True, color='#5fbdce', filename=output_base+"_cum.png", linewidth=2)

    #catalogue = 

# completeness catalog
    if plot_density:
        # magnitude density plot
        plot_magnitude_time_density(catalogue, mag_int=0.5, time_int=1.0, 
                                    filename=output_base+"_time_density.png", figsize=(18,6))


    if plot_stepp:
        # completeness analysis
        stepp = Stepp1971()
        
        completeness_config = {'magnitude_bin': 0.5,
                               'time_bin': 2.5,
                               'increment_lock': True}
        print completeness_config
        
        # Run analysis
        print 'Running Stepp (1971) completeness analysis:'
        print np.min(catalogue.data['magnitude'])
        completeness_table = stepp.completeness(catalogue, completeness_config)
        print completeness_table
        print 'done!'
        
        # Print the output completeness table
        #for row in completeness_table:
        #    print '%8.1f  %8.2f' %(row[0], row[1])
        
        
        #In[ ]:
        
        create_stepp_plot(stepp, #filename=output_base+"_stepp.png",
                          figsize=(10, 8), dpi=dpi,
                          legendoffset=(1.2,1),
                          show=True,
                          )
        
    
    if model_name == 'hmtk_sa3':
        ct = np.array([  [ 1986,      3. ]
                         [ 1986,      3.5]
                         [ 1986,      4. ]
                         [ 1960,      4.5]
                         [ 1958,      5. ]
                         [ 1958,      5.5]
                         [ 1927,      6. ]
                         [ 1898,      6.5]
                         [ 1885,      7. ]
                         [ 1885,      7.5]
                         [ 1885,      8. ]])
    else:
        ct = np.array([[ 1980, 3. ],
                       [ 1975, 3.5],
                       [ 1975, 4. ]
                       [ 1965, 4.5],
                       [ 1965, 5. ]
                       [ 1860, 5.5],
                       [ 1860, 6. ]])
    
    
    





    
    # stepp plot
    # save complete catalog
    

# max_magnitude
    