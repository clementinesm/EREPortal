import queries
import pandas as pd

default_buyback_rate = 10.5
default_consumption_rate = 10.5
default_tdsp_rate = 5.0
red_alpha = 0.5
green_alpha = 0.75

def swap_dateorder(date):
    '''
    :param date: string of format yyyy-mm or mm-yyyy
    :return: converts from one format to the other
    '''
    return str(date.split('-')[1]) + '-' + str(date.split('-')[0])

def getdata(flowdates, systemsize, selected_TDSPs, selected_premises, esiid=None):
    if esiid:
        noesiid = (esiid == 'none') | (esiid == '')
    else:
        noesiid = True
    if noesiid:
        querygen = queries.monthlygen(flowdates=flowdates,
                                      TDSP=selected_TDSPs,
                                      premisetype=selected_premises,
                                      systemsize=systemsize,
                                      compact=True)
    else:
        querygen = queries.monthlygen(flowdates=flowdates,
                                      TDSP=selected_TDSPs,
                                      premisetype=selected_premises,
                                      systemsize=systemsize,
                                      accounts = [esiid],
                                      compact=True)
    df = queries.data_query(querygen)
    return df

def get_fill_line_alpha(revenue, energycost, tdspcost, solarpayments, grossmargin):
    fillcolor = []
    fillalpha = []
    linecolor = []
    if revenue > 0:
        fillcolor.append('green')
        fillalpha.append(green_alpha)
        linecolor.append('green')
    else:
        fillcolor.append('red')
        fillalpha.append(red_alpha)
        linecolor.append('red')
    if energycost > 0:
        fillcolor.append('green')
        fillalpha.append(green_alpha)
        linecolor.append('green')
    else:
        fillcolor.append('red')
        fillalpha.append(red_alpha)
        linecolor.append('red')
    if tdspcost > 0:
        fillcolor.append('green')
        fillalpha.append(green_alpha)
        linecolor.append('green')
    else:
        fillcolor.append('red')
        fillalpha.append(red_alpha)
        linecolor.append('red')
    if solarpayments > 0:
        fillcolor.append('green')
        fillalpha.append(green_alpha)
        linecolor.append('green')
    else:
        fillcolor.append('red')
        fillalpha.append(red_alpha)
        linecolor.append('red')
    if grossmargin > 0:
        fillcolor.append('green')
        fillalpha.append(green_alpha)
        linecolor.append('green')
    else:
        fillcolor.append('red')
        fillalpha.append(red_alpha)
        linecolor.append('red')
    return fillcolor, fillalpha, linecolor
