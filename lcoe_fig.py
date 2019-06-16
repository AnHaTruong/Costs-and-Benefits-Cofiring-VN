# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Instantiate technology data in Vietnam Technology Catalogue (Jakob Lundsager et al. 2019)
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Plot LCOE figure as calculated using Vietnam Technology Catalogue parameters."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# pylint: disable=wrong-import-order
from model.utils import USD
from natu.units import MWh
from natu.numpy import npv
from param_tech_catalogue import discount_rate, tax_rate
from param_tech_catalogue import Coal_Supercritical, CCGT, Solar_PV, Wind_Onshore, Wind_Offshore
from parameters import depreciation_period

# %% Creat a graph
unit = USD / MWh
lcoe_arg = [discount_rate, tax_rate, depreciation_period]


def create_LCOE_df(plant, base_price, upper_price, lower_price):
    """Group elements of LCOE for convention power plant in to a dataframe."""
    lcoe_base = []
    lcoe_upper = []
    lcoe_lower = []
    lcoe_capital = []
    lcoe_fuel = []
    lcoe_OM = []
    for year in ['2020', '2030', '2050', 'Lower20', 'Upper20', 'Lower50', 'Upper50']:
        lcoe_base.append(plant[year][base_price].lcoe(*lcoe_arg) / unit)
        lcoe_upper.append(plant[year][upper_price].lcoe(*lcoe_arg) / unit)
        lcoe_lower.append(plant[year][lower_price].lcoe(*lcoe_arg) / unit)
        lcoe_capital.append(plant[year][base_price].capital /
                            npv(discount_rate, plant[year][base_price].power_generation) / unit)
        lcoe_fuel.append(npv(discount_rate, plant[year][base_price].fuel_cost()) /
                         npv(discount_rate, plant[year][base_price].power_generation) / unit)
        lcoe_OM.append(npv(discount_rate, plant[year][base_price].operation_maintenance_cost()) /
                       npv(discount_rate, plant[year][base_price].power_generation) / unit)

    lcoe = pd.DataFrame({'lcoe': np.array(lcoe_base),
                         'lcoe capital': np.array(lcoe_capital),
                         'lcoe fuel': np.array(lcoe_fuel),
                         'lcoe OM': np.array(lcoe_OM),
                         'upper error': np.array(lcoe_upper) - np.array(lcoe_base),
                         'lower error': np.array(lcoe_base) - np.array(lcoe_lower)})
    lcoe.index = (['2020', '2030', '2050', 'Lower20', 'Upper20', 'Lower50', 'Upper50'])
    return lcoe


lcoe_coal_SC = create_LCOE_df(Coal_Supercritical, '6b_coal', 'coal_upper', 'coal_lower')
lcoe_CCGT = create_LCOE_df(CCGT, 'natural_gas', 'gas_upper', 'gas_lower')


def create_RELCOE_df(plant):
    """Group elements of LCOE for renewable power plant in to a dataframe."""
    lcoe_RE = []
    lcoe_capital = []
    lcoe_fuel = []
    lcoe_OM = []
    for year in ['2020', '2030', '2050', 'Lower20', 'Upper20', 'Lower50', 'Upper50']:
        lcoe_RE.append(plant[year].lcoe(*lcoe_arg) / unit)
        lcoe_capital.append(plant[year].capital /
                            npv(discount_rate, plant[year].power_generation) / unit)
        lcoe_fuel.append(npv(discount_rate, plant[year].fuel_cost()) /
                         npv(discount_rate, plant[year].power_generation) / unit)
        lcoe_OM.append(npv(discount_rate, plant[year].operation_maintenance_cost()) /
                       npv(discount_rate, plant[year].power_generation) / unit)

    lcoe = pd.DataFrame({'lcoe': np.array(lcoe_RE),
                         'lcoe capital': np.array(lcoe_capital),
                         'lcoe fuel': np.array(lcoe_fuel),
                         'lcoe OM': np.array(lcoe_OM)})
    lcoe.index = (['2020', '2030', '2050', 'Lower20', 'Upper20', 'Lower50', 'Upper50'])
    return lcoe


lcoe_PV = create_RELCOE_df(Solar_PV)
lcoe_wind_onshore = create_RELCOE_df(Wind_Onshore)
lcoe_wind_offshore = create_RELCOE_df(Wind_Offshore)

n = 3
ind = np.arange(n)
width = 0.1
ind1 = ind + 0.15
ind2 = ind + 0.3
ind3 = ind + 0.45
inda = np.array([0, 0.15, 0.3])
color1 = ['salmon', 'mistyrose', 'darkred']
color2 = ['#4572a7', '#89a54e', '#4198af']
index1 = [ind, ind1, ind2, ind3]
index2 = [inda, inda + 0.5, inda + 1, inda + 1.5]
xlabel = ['Coal', 'Coal', 'Coal',
          'Gas', 'Gas', 'Gas',
          'Solar PV', 'Solar PV', 'Solar PV',
          'Wind onshore', 'Wind onshore', 'Wind onshore']


def plot_lcoe(x, plant, color):
    """Plot a stack bar for LCOE of convention power plant with error bar."""
    plt.bar(x, plant['lcoe capital'], width, color=color[0], edgecolor='none')
    plt.bar(x, plant['lcoe OM'], width, bottom=plant['lcoe capital'],
            color=color[1], edgecolor='none')
    plt.bar(x, plant['lcoe fuel'], width,
            bottom=plant['lcoe capital'] + plant['lcoe OM'],
            color=color[2], edgecolor='none',
            yerr=[plant['lower error'], plant['upper error']], ecolor='r')


def plot_lcoe_re(x, plant, color):
    """Plot a stack bar for LCOE of renewable power plant (no error bar)."""
    plt.bar(x, plant['lcoe capital'], width, color=color[0], edgecolor='none')
    plt.bar(x, plant['lcoe OM'], width, bottom=plant['lcoe capital'],
            color=color[1], edgecolor='none')
    plt.bar(x, plant['lcoe fuel'], width,
            bottom=plant['lcoe capital'] + plant['lcoe OM'],
            color=color[2], edgecolor='none')


def plot_lcoe_figure(index, ff_scenarios, re_scenarios, color, text):
    """Plot LCOE of 5 different technologies grouped in 3 scenarios.

    Argument scenarios is a list of 3 elements. I.e. ['2020', '2030', '2050'].
    """
    plt.figure(figsize=(9, 6))
    plt.ylim(0, 140)
    plt.ylabel('2017 USD/MWh', rotation='vertical')
    plot_lcoe(index[0], lcoe_coal_SC.loc[ff_scenarios, :], color)
    plot_lcoe(index[1], lcoe_CCGT.loc[ff_scenarios, :], color)
    plot_lcoe_re(index[2], lcoe_PV.loc[re_scenarios, :], color)
    plot_lcoe_re(index[3], lcoe_wind_onshore.loc[re_scenarios, :], color)

    plt.xticks(np.concatenate(index), (xlabel), rotation=45)
    legend_capital = mpatches.Patch(color=color[0], label='Capital cost')
    legend_OM = mpatches.Patch(color=color[1], label='O&M cost')
    legend_fuel = mpatches.Patch(color=color[2], label='Fuel cost')
    plt.legend(loc='center right', handles=[legend_capital, legend_OM, legend_fuel],
               prop={'size': 9})
    plt.text(0.3, 130, text[0])
    plt.text(1.2, 130, text[1])
    plt.text(2.2, 130, text[2])
    plt.tight_layout()


plot_lcoe_figure(index1, ['2020', '2030', '2050'], ['2020', '2030', '2050'], color1,
                 ['2020', '2030', '2050'])
plt.title('LCOE comparion among generation technologies')
plt.savefig('LCOE1.png')
plt.clf()

plot_lcoe_figure(index2, ['2020', '2030', '2050'], ['2020', '2030', '2050'], color2,
                 [' ', ' ', ' '])
plt.title('Recreation of EOR19 LCOE graph')
plt.savefig('LCOE1a.png')
plt.clf()

plot_lcoe_figure(index1, ['2020', 'Lower20', 'Upper20'], ['2020', 'Upper20', 'Lower20'], color1,
                 ['Base', 'maxFF, minRE', 'minFF, maxRE'])
plt.title('LCOE comparison in 2020 with worst case and best case scenarios for RE')
plt.savefig('LCOE2.png')
plt.clf()

plot_lcoe_figure(index1, ['2050', 'Lower50', 'Upper50'], ['2020', 'Upper50', 'Lower50'], color1,
                 ['Base', 'maxFF, minRE', 'minFF, maxRE'])
plt.title('LCOE comparison in 2050 with worst case and best case scenarios for RE')
plt.savefig('LCOE3.png')
plt.clf()
