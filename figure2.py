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
""" Plots the air pollutants emissions and CO2 emissions figure
"""

import matplotlib.pyplot as plt
import numpy as np

from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from natu.units import t   # pylint: disable=E0611


def plot_emissions(plant, cofiringplant, axes):
    """Plots the air pollutants emissions and CO2 emissions figure for one site"""
    kt = 1000 * t
    Mt = 1000000 * t

    CO2stack = np.array([plant.stack.emissions().at['CO2', 'Total'][1],
                         cofiringplant.stack.emissions().at['CO2', 'Total'][1]
                         ]) / Mt

    CO2trans = np.array([plant.coal_transporter().emissions().at['CO2', 'Total'][1],
                         (cofiringplant.coal_transporter().emissions().at['CO2', 'Total'][1]
                          + cofiringplant.straw_supply.transport_emissions().at['CO2', 'Total'][1]
                          )
                         ]) / Mt

    field_emis_before = cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])
    field_emis_after = cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])
    CO2field = np.array([field_emis_before.at['CO2', 'Total'][1],
                         field_emis_after.at['CO2', 'Total'][1]]
                        ) / Mt

    polstack = np.array([plant.stack.emissions().at['SO2', 'Total'][1],
                         cofiringplant.stack.emissions().at['SO2', 'Total'][1],
                         plant.stack.emissions().at['PM10', 'Total'][1],
                         cofiringplant.stack.emissions().at['PM10', 'Total'][1],
                         plant.stack.emissions().at['NOx', 'Total'][1],
                         cofiringplant.stack.emissions().at['NOx', 'Total'][1]
                         ]) / kt

    coal_transport_emis_before = plant.coal_transporter().emissions()
    coal_transport_emis_after = cofiringplant.coal_transporter().emissions()
    straw_transport_emis = cofiringplant.straw_supply.transport_emissions()
    poltrans = np.array([coal_transport_emis_before.at['SO2', 'Total'][1],
                         (coal_transport_emis_after.at['SO2', 'Total'][1]
                          + straw_transport_emis.at['SO2', 'Total'][1]),
                         coal_transport_emis_before.at['PM10', 'Total'][1],
                         (coal_transport_emis_after.at['PM10', 'Total'][1]
                          + straw_transport_emis.at['PM10', 'Total'][1]),
                         coal_transport_emis_before.at['NOx', 'Total'][1],
                         (coal_transport_emis_after.at['NOx', 'Total'][1]
                          + straw_transport_emis.at['NOx', 'Total'][1])
                         ]) / kt

    polfield = np.array([field_emis_before.at['SO2', 'Total'][1],
                         field_emis_after.at['SO2', 'Total'][1],
                         field_emis_before.at['PM10', 'Total'][1],
                         field_emis_after.at['PM10', 'Total'][1],
                         field_emis_before.at['NOx', 'Total'][1],
                         field_emis_after.at['NOx', 'Total'][1]
                         ]) / kt

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
               title=plant.name + ' Emissions',
               frameon=False)


FIGURE, AXESS = plt.subplots(nrows=1, ncols=2, figsize=[12, 6])
plot_emissions(MongDuong1, MongDuong1Cofire, AXESS[0])
plot_emissions(NinhBinh, NinhBinhCofire, AXESS[1])
FIGURE.tight_layout()

plt.savefig('figure2.png')
