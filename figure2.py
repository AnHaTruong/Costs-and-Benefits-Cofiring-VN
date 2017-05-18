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
    CO2stack = np.array([plant.stack.emissions()['Total']['CO2'][1] / t,
                         cofiringplant.stack.emissions()['Total']['CO2'][1] / t
                         ]) / 1000
    CO2trans = np.array([plant.coal_transporter().emissions()['Total']['CO2'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['CO2'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['CO2'][1] / t
                          )
                         ])/1000
    CO2field = np.array([cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['CO2'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['CO2'][1]/t]
                        )/1000

    polstack = np.array([plant.stack.emissions()['Total']['SO2'][1] / t,
                         cofiringplant.stack.emissions()['Total']['SO2'][1] / t,
                         plant.stack.emissions()['Total']['PM10'][1] / t,
                         cofiringplant.stack.emissions()['Total']['PM10'][1] / t,
                         plant.stack.emissions()['Total']['NOx'][1] / t,
                         cofiringplant.stack.emissions()['Total']['NOx'][1] / t]) / 1000

    poltrans = np.array([plant.coal_transporter().emissions()['Total']['SO2'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['SO2'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['SO2'][1] / t),
                         plant.coal_transporter().emissions()['Total']['PM10'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['PM10'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['PM10'][1] / t),
                         plant.coal_transporter().emissions()['Total']['NOx'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['NOx'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['NOx'][1] / t)]
                          ) / 1000

    polfield = np.array([cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['SO2'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['SO2'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['PM10'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['PM10'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['NOx'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['NOx'][1]/t])/1000

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

    ax1.set_xlabel('CO2 emission (kt/y)')
    ax2.set_xlabel('Air pollutant Emission (kt/y)')

    plt.yticks(np.concatenate((ind, index), axis=0), ('CO2 Baseline', 'CO2 Cofire',
                                                      'SO2 Baseline', 'SO2 Cofire',
                                                      'PM10 Baseline', 'PM10 Cofire',
                                                      'NOx Baseline', 'NOx Cofire')
               )
    ax1.legend(bbox_to_anchor=(0.98, 0.8), prop={'size': 9})

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
plt.text(63, 5.8, 'Emission from Mong Duong 1', horizontalalignment='center',
         rotation='vertical', fontsize=14)
plt.tight_layout()
plt.savefig('MD1emission.png')
plot_emissions(NinhBinh, NinhBinhCofire)
plt.text(9.5, 5.3, 'Emission from Ninh Binh', horizontalalignment='center',
         rotation='vertical', fontsize=14)
plt.tight_layout()
plt.savefig('NBemission.png')

