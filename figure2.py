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
""" Draw Figure 2 CO2 and air pollutant emission
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_pdf import PdfPages
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from natu.units import t


def plot_emissions(plant, cofiringplant):
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
    
    CO2field = np.array([cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0]).at['CO2', 'Total'][1],
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1]).at['CO2', 'Total'][1]]
                        ) / Mt

    polstack = np.array([plant.stack.emissions().at['SO2', 'Total'][1],
                         cofiringplant.stack.emissions().at['SO2', 'Total'][1],
                         plant.stack.emissions().at['PM10', 'Total'][1],
                         cofiringplant.stack.emissions().at['PM10', 'Total'][1],
                         plant.stack.emissions().at['NOx', 'Total'][1],
                         cofiringplant.stack.emissions().at['NOx', 'Total'][1]
                         ]) / kt

    poltrans = np.array([plant.coal_transporter().emissions().at['SO2', 'Total'][1],
                         (cofiringplant.coal_transporter().emissions().at['SO2', 'Total'][1]
                          + cofiringplant.straw_supply.transport_emissions().at['SO2', 'Total'][1]),
                         plant.coal_transporter().emissions().at['PM10', 'Total'][1],
                         (cofiringplant.coal_transporter().emissions().at['PM10', 'Total'][1]
                          + cofiringplant.straw_supply.transport_emissions().at['PM10', 'Total'][1]),
                         plant.coal_transporter().emissions().at['NOx', 'Total'][1],
                         (cofiringplant.coal_transporter().emissions().at['NOx', 'Total'][1]
                          + cofiringplant.straw_supply.transport_emissions().at['NOx', 'Total'][1])
                         ]) / kt

    polfield = np.array([cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0]).at['SO2', 'Total'][1],
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1]).at['SO2', 'Total'][1],
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0]).at['PM10', 'Total'][1],
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1]).at['PM10', 'Total'][1],
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0]).at['NOx', 'Total'][1],
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1]).at['NOx', 'Total'][1]
                         ]) / kt

    ind = [0, 0.5]
    width = 0.48
    index = [2, 2.5, 3.5, 4, 5, 5.5]

    fig, ax1 = plt.subplots()
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
    ax1.legend(bbox_to_anchor=(0.98, 0.8), prop={'size': 9}, title=plant.name + ' Emissions',
               frameon=False)

#with PdfPages('figure2.pdf') as pdf:
#    plt.figure(1)
#    plot_emissions(MongDuong1, MongDuong1Cofire)
#    plt.text(63, 5.8, 'Emission from Mong Duong 1', horizontalalignment='center',
#             rotation='vertical', fontsize=14)
#    pdf.savefig()
#    plt.close()
#
#    plt.figure(2)
#    plot_emissions(NinhBinh, NinhBinhCofire)
#    plt.text(9.5, 5.3, 'Emission from Ninh Binh', horizontalalignment='center',
#             rotation='vertical', fontsize=14)
#    pdf.savefig()
#    plt.close()


plot_emissions(MongDuong1, MongDuong1Cofire)
plt.tight_layout()
plt.savefig('MD1emission.png')
plot_emissions(NinhBinh, NinhBinhCofire)
plt.tight_layout()
plt.savefig('NBemission.png')
