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
""" Draw Figure 2 SO2 emission reduction and its benefit to public health
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_pdf import PdfPages
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from natu.units import t


def fig2(plant, cofiringplant):
    CO2stack = np.array([plant.stack.emissions()['Total']['CO2'][1] / t,
                         cofiringplant.stack.emissions()['Total']['CO2'][1] / t]
                        )
    CO2trans = np.array([plant.coal_transporter().emissions()['Total']['CO2'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['CO2'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['CO2'][1] / t
                          )
                         ])
    CO2field = np.array([cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['CO2'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['CO2'][1]/t]
                        )

    polstack = np.array([plant.stack.emissions()['Total']['SO2'][1] / t,
                         cofiringplant.stack.emissions()['Total']['SO2'][1] / t,
                         plant.stack.emissions()['Total']['PM10'][1] / t,
                         cofiringplant.stack.emissions()['Total']['PM10'][1] / t,
                         plant.stack.emissions()['Total']['NOx'][1] / t,
                         cofiringplant.stack.emissions()['Total']['NOx'][1] / t])

    poltrans = np.array([plant.coal_transporter().emissions()['Total']['SO2'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['SO2'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['SO2'][1] / t),
                         plant.coal_transporter().emissions()['Total']['PM10'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['PM10'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['PM10'][1] / t),
                         plant.coal_transporter().emissions()['Total']['NOx'][1] / t,
                         (cofiringplant.coal_transporter().emissions()['Total']['NOx'][1] / t
                          + cofiringplant.straw_supply.transport_emissions()['Total']['NOx'][1] / t)]
                          )

    polfield = np.array([cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['SO2'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['SO2'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['PM10'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['PM10'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[0])['Total']['NOx'][1]/t,
                         cofiringplant.straw_supply.field_emission(cofiringplant.biomass_used[1])['Total']['NOx'][1]/t])
    ind = np.arange(2)
    width = 0.3
    index = np.arange(6)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twiny()

    ax1.barh(ind, CO2stack, width, color='r')
    ax1.barh(ind, CO2trans, width, color='b', left=CO2stack)
    ax1.barh(ind, CO2field, width, color='g', left=(CO2stack + CO2trans))

    ax2.barh(index + 2, polstack, width, color='r')
    ax2.barh(index + 2, poltrans, width, color='b', left=polstack)
    ax2.barh(index + 2, polfield, width, color='g', left=(polstack + poltrans))

    ax1.set_xlabel('CO2 emission (t/y)')
    ax2.set_xlabel('Air pollutant Emission (t/y)')

    plt.yticks(np.arange(8), ('CO2 Coal', 'CO2 Cofire',
                              'SO2 Coal', 'SO2 Cofire',
                              'PM10 Coal', 'PM10 Cofire',
                              'NOx Coal', 'NOx Cofire'))

    plt.show()

fig2(MongDuong1, MongDuong1Cofire)
fig2(NinhBinh, NinhBinhCofire)

#with PdfPages('figure2.pdf') as pdf:
#     plt.figure(1)    
#     fig2(MongDuong1, MongDuong1Cofire)
#     pdf.savefig()
#     plt.close()
#     
#     plt.figure(2)
#     fig2(NinhBinh, NinhBinhCofire)
#     pdf.savefig()
#     plt.close()
