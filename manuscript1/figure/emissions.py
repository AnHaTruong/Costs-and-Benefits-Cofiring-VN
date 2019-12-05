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
import matplotlib.patches as mpatches

# pylint: disable=wrong-import-order
from manuscript1.parameters import MongDuong1System, NinhBinhSystem
from natu.units import kt, Mt, y
from natu.numpy import array, concatenate

#%%


def plot_emissions(system, axes):
    """Plot to compare atmospheric pollution with and without cofiring."""
    baseline = system.emissions_baseline() * y
    cofiring = system.emissions_cofiring() * y

    def emis(segment, pollutant='CO2', unit=Mt):
        return array([baseline.at['Total_' + segment, pollutant],
                      cofiring.at['Total_' + segment, pollutant]]) / unit

    def emis3(segment):
        return concatenate(
            [emis(segment, 'SO2', kt), emis(segment, 'PM10', kt), emis(segment, 'NOx', kt)])

    def barhstack(axes, bottom, width, height=0.48, xlabel=None):
        """Plot a horizontal stacked bar, width is a sequence of three horizontal dimensions."""
        axes.barh(bottom, width[0], height, color='darkred', edgecolor='none')
        axes.barh(bottom, width[1], height, width[0], color='mistyrose', edgecolor='none')
        axes.barh(bottom, width[2], height, width[0] + width[1], color='salmon', edgecolor='none')
        axes.tick_params(axis='y', length=0)
        axes.set_xlabel(xlabel)

    bot1 = [0, 0.5]
    bot2 = [2, 2.5, 3.5, 4, 5, 5.5]

    barhstack(axes,
              bot1,
              [emis('plant'), emis('transport'), emis('field')],
              xlabel='CO2 emission (Mt/y)')

    barhstack(axes.twiny(),
              bot2,
              [emis3('plant'), emis3('transport'), emis3('field')],
              xlabel='Air pollutant Emission (kt/y)')

    plt.yticks(concatenate(
        (bot1, bot2)),
        ('CO2 Baseline', 'CO2 Cofire', 'SO2 Baseline', 'SO2 Cofire',
         'PM10 Baseline', 'PM10 Cofire', 'NOx Baseline', 'NOx Cofire'))

    legend_plant = mpatches.Patch(color='darkred', label='Plant emissions')
    legend_transport = mpatches.Patch(color='mistyrose', label='Transport emissions')
    legend_field = mpatches.Patch(color='salmon', label='Field emissions')
    axes.legend(handles=[legend_plant, legend_transport, legend_field],
                bbox_to_anchor=(0.98, 0.8),
                prop={'size': 9},
                title=system.plant.name + ' Emissions',
                frameon=False)


# noinspection PyTypeChecker
FIGURE, AXESS = plt.subplots(nrows=1, ncols=2, figsize=[12, 6])
plot_emissions(MongDuong1System, AXESS[0])
plot_emissions(NinhBinhSystem, AXESS[1])
FIGURE.tight_layout()

plt.savefig('figure_emissions.svg')
