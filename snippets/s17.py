# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pylab as plt


# HMTK Catalogue Import/Export Libraries
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter


input_catalogue_file = '../data_input/hmtk_chile.csv'
#input_catalogue_file = 'data_input/hmtk_sa.csv'

parser = CsvCatalogueParser(input_catalogue_file)
catalogue = parser.read_file()
print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year, catalogue.end_year)
valid_magnitudes = catalogue.data['magnitude'] <> np.nan
catalogue.select_catalogue_events(valid_magnitudes)
valid_magnitudes = catalogue.data['magnitude'] >= 2.0
catalogue.select_catalogue_events(valid_magnitudes)
print catalogue.data['magnitude']





def gr(m, a, b=1):
    return 10**(a) - 10**(b*m)


def F_gr(m, b=1, m_min=2.0):
    return 10**(-b*(m - m_min))


def f_gr(m, b=1, m_min=2.0):
    _r = 10**(-b*(m - m_min))
#     _i = m < m_min
#     _r[_i] = 1.2e-7
    return _r


def F_bgr(m, b=1, m_min=2.0, m_max=5.0):
    _r = (1 - 10**(-b*(m - m_min))) / (1 - 10**(-b*(m_max - m_min)))
    return _r

def f_bgr(m, b=1, m_min=2.0, m_max=5.0):
    _r = (b*np.log(10))*10**(-b*(m - m_min)) / (1 - 10**(-b*(m_max - m_min)))
    return _r


def F_tapgr(m, b=1, m_min=2.0, m_max=5.0):
    beta = b*np.log(10.)
    _r = 1 - (m_min / m )**beta * np.exp((m_min - m) / m_max)
    return _r

def F_trugr(m, b=1, m_min=2.0, m_max=5.0):
    beta = b*np.log(10.)
    _r = (1 - np.exp(-beta*(m - m_min))) / ( 1 - np.exp(-beta*(m_max - m_min)))
    return _r


def F_kagan(m, b=1, m_min=2.0, m_max=8.0):
    _r = 10**(-b*(m - m_min)) * np.exp( 10**(1.5*(m_min - m_max)) - 10**(1.5*(m - m_max)))
    #print _r
    _i = np.logical_or((m < m_min), (m > m_max + .3))
    _r[_i] = 1e-7
    #print _r
    return _r


def dtgr(m, b=1, m_min=3, m_max=7.7):
    beta = b*np.log(10.)
    n = np.exp((-beta*(m - m_min)))
    d = 1 - np.exp((-beta*(m_max - m_min)))
    _r = n / d
    #print _r
    _i = np.logical_or((m < m_min), (m > m_max + .3))
    _r[_i] = 1e-7
    #print _r
    return _r


def tgr(m, b=1, m_min=3, m_max=7.7):
    beta = b*np.log(10.)
    n = np.exp((-beta*(m)))
    d = 1 - np.exp((-beta*(m_max)))
    _r = n / d
    #print _r
    #_i = np.logical_or())
    _r[m > (m_max + .3)] = 1e-10
    #print _r
    return _r



def tapered_pareto(m, a, b=1, m_min=2.0, m_max=7.):
    beta = b*np.log(10.)
    a_m_min = a
    e = np.exp( -beta*(m_max - m_min) )
    _r = ( a_m_min * np.exp(-beta*(m - m_min)) - e ) / (1 - e)

    _i = np.logical_or((m < m_min), (m > m_max))
    _r[_i] = 1e-7

    return _r 


# def truncated_pareto(M, a, b=1, m_min=2.0, m_max=7.):
#     beta = b*np.log(10.)
#     a_m_min = a
#     e = np.exp( -beta*(m_max - m_min) )
#     _r = ( a_m_min * np.exp(-beta*(M - m_min)) - e ) / (1 - e)
#     return _r




def truncated_pareto(m, a, b=1., m_min=2., m_max=7.):
    _r = 10**(-b * (m - m_min))
    _i = np.logical_or((m < m_min), (m > m_max + 1))
    _r[_i] = 1e-7
    return _r 
    

def bgr(m, a, b=1., m_min=2., m_max=8):
    _r = 10**(a - b * (m - m_min)) - 10**(a - b *(m_max - m_min))
    _i = np.logical_or((m < m_min), (m > m_max + 1))
    _r[_i] = 1e-1
    return _r

def pareto(m, a, b=1, m_min=2.0):
    beta = b*np.log(10.)
    a_m_min = a
    _r = a_m_min * np.exp(-beta*(m - m_min))
    _i = (m < m_min)
    _r[_i] = 1e-7
    return _r


# 
# def truncated_pareto(M, a, b=1, m_min=2.0, m_max=5.):
#     beta = b*np.log(10.)
#     a_m_min = a
#     e = np.exp( -beta*(m_max - m_min) )
#     
#     return ( a_m_min * np.exp(-beta*(M - m_min)) - e ) / (1 - e)



if __name__ == "__main__":
    m = np.linspace(2.5, 8.5, 150)

#    plt.xkcd()
    f = plt.figure()
    
#    ax1 = f.add_subplot(2,1,1)
    f.patch.set_facecolor("white")

    a = 1000.

    #plt.semilogy(m, gr_mfd(m, 3.0))
#    ax1.semilogy(m, F_gr(m.copy()), label="F-GR")
#     ax1.semilogy(m, gr(m, a), label="GR")
#     ax1.semilogy(m, F_bgr(m), label="F-bGR")
#     ax1.semilogy(m, F_tapgr(m), label="F-tapGR")
#     ax1.semilogy(m, F_trugr(m), label="F-trubGR")

#     ax1.set_xlabel(r'Magnitude $m$')
#     ax1.set_ylabel(r"Frequency $ \log{(N > m)} $")
#     ax1.set_title(r"Magnitude Frequency Distribution")
#     ax1.legend()


    ax2 = f.add_subplot(1,1,1)
#    ax2.semilogy(m, gr(m, a), label="f-GR")
    ax2.semilogy(m, 1e6*f_gr(m),"-" , lw=4.0, alpha=0.3, label="Gutemberg-Richter")
#  #   ax2.semilogy(m, f_bgr(m), label="f-bGR")
# #     ax2.semilogy(m, F_gr(m), label="F-GR")
#    ax2.semilogy(m, 1e6*pareto(m, 1),"." , alpha=0.3, label="Pareto")
# #     ax2.semilogy(m, truncated_pareto(m, 1), label="trun_P")
# #     ax2.semilogy(m, tapered_pareto(m, 1), label="tap-P")
    ax2.semilogy(m, bgr(m, 6),'.', alpha=0.5, label="Bounded GR")
#     ax2.semilogy(m, 1e8*tgr(m),'-.',lw=2.0 ,alpha=0.7, label="Truncated GR")
#     ax2.semilogy(m, 1e5*dtgr(m),'-',lw=2.0,  alpha=0.5, label="Double Truncated GR")
    ax2.semilogy(m, 1e6*F_kagan(m), '.' , alpha=0.5,  label="Kagan (Tapered Pareto)")
#    ax2.semilogy(m, gr(m, a), label="gr")
    
#    print catalogue.data['magnitude']
    ax2.hist(catalogue.data['magnitude'], bins=10, histtype='step',  label="subset from Chilean's catalog")

    
#    ax2.set_ylim(1e-6, 1e2)
    ax2.set_xlim(2.8, 8.3)

    ax2.set_xlabel(r'Magnitude $m$')
    ax2.set_ylabel(r"Frequency $ \log{(N)} $")
    ax2.set_title(r"Earthquakes Magnitude Frequency Distribution")
    ax2.legend()

    plt.show()
    