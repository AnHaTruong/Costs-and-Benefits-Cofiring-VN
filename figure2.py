# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Plot the air pollutants emissions and CO2 emissions figure."""

import matplotlib.pyplot as plt
import numpy as np

from parameters import MongDuong1System, NinhBinhSystem
from natu.units import kt, Mt, y


#%%

def plot_data(system):
    """Return CO2 and other air pollutants emissions for one site."""
    baseline = system.emissions_baseline(total=True) * y
    cofiring = system.emissions_cofiring(total=True) * y

    CO2stack = np.array([baseline.at['Total_plant', 'CO2'],
                         cofiring.at['Total_plant', 'CO2']]) / Mt

    CO2trans = np.array([baseline.at['Total_transport', 'CO2'],
                         cofiring.at['Total_transport', 'CO2']]) / Mt

    CO2field = np.array([baseline.at['Total_field', 'CO2'],
                         cofiring.at['Total_field', 'CO2']]) / Mt

    polstack = np.array([baseline.at['Total_plant', 'SO2'],
                         cofiring.at['Total_plant', 'SO2'],
                         baseline.at['Total_plant', 'PM10'],
                         cofiring.at['Total_plant', 'PM10'],
                         baseline.at['Total_plant', 'NOx'],
                         cofiring.at['Total_plant', 'NOx']
                         ]) / kt

    poltrans = np.array([baseline.at['Total_transport', 'SO2'],
                         cofiring.at['Total_transport', 'SO2'],
                         baseline.at['Total_transport', 'PM10'],
                         cofiring.at['Total_transport', 'PM10'],
                         baseline.at['Total_transport', 'NOx'],
                         cofiring.at['Total_transport', 'NOx']
                         ]) / kt

    polfield = np.array([baseline.at['Total_field', 'SO2'],
                         cofiring.at['Total_field', 'SO2'],
                         baseline.at['Total_field', 'PM10'],
                         cofiring.at['Total_field', 'PM10'],
                         baseline.at['Total_field', 'NOx'],
                         cofiring.at['Total_field', 'NOx']
                         ]) / kt

    return CO2stack, CO2trans, CO2field, polstack, poltrans, polfield


#%%


def plot_emissions(system, axes):
    """Plot to compare atmospheric pollution with and without cofiring."""
    CO2stack, CO2trans, CO2field, polstack, poltrans, polfield = plot_data(system)
    ind = [0, 0.5]
    width = 0.48
    index = [2, 2.5, 3.5, 4, 5, 5.5]

    ax1 = axes
    ax2 = ax1.twiny()

    ax1.barh(ind, CO2stack, width, color='darkred', edgecolor='none', label='Plant emissions')
    ax1.barh(ind, CO2trans, width, color='mistyrose', edgecolor='none',
             left=CO2stack, label='Transport emissions')
    ax1.barh(ind, CO2field, width, color='salmon', edgecolor='none',
             left=(CO2stack + CO2trans), label='Field emissions')

    ax2.barh(index, polstack, width, color='darkred', edgecolor='none')
    ax2.barh(index, poltrans, width, color='mistyrose', edgecolor='none', left=polstack)
    ax2.barh(index, polfield, width, color='salmon', edgecolor='none', left=(polstack + poltrans))

    ax1.set_xlabel('CO2 emission (Mt/y)')
    ax2.set_xlabel('Air pollutant Emission (kt/y)')

    plt.yticks(np.concatenate((ind, index), axis=0), ('CO2 Baseline', 'CO2 Cofire',
                                                      'SO2 Baseline', 'SO2 Cofire',
                                                      'PM10 Baseline', 'PM10 Cofire',
                                                      'NOx Baseline', 'NOx Cofire')
               )
    ax1.tick_params(axis='y', length=0)
    ax2.tick_params(axis='y', length=0)
    ax1.legend(bbox_to_anchor=(0.98, 0.8),
               prop={'size': 9},
               title=system.plant.name + ' Emissions',
               frameon=False)


# noinspection PyTypeChecker
FIGURE, AXESS = plt.subplots(nrows=1, ncols=2, figsize=[12, 6])
plot_emissions(MongDuong1System, AXESS[0])
plot_emissions(NinhBinhSystem, AXESS[1])
FIGURE.tight_layout()

plt.savefig('figure2.png')
