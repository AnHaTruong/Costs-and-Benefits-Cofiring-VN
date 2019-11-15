# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Plot the economics feasibility diagram.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017-2019
"""
import matplotlib.pyplot as plt

from model.utils import USD, MUSD, t, isclose
from model.feasibility import farmer_gain, farmer_wta, plant_gain, plant_wtp

from manuscript1.parameters import MongDuong1System, NinhBinhSystem
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period


#%%

# pylint: disable=invalid-name, too-many-locals
def plot_feasibility(system, ax):
    """Plot to determine if cofiring is economically feasible."""
    x0 = 0
    x1 = farmer_wta(system) / (USD / t)
    x2 = plant_wtp(system, discount_rate, tax_rate, depreciation_period) / (USD / t)
    assert not isclose(x1, x2), "WTA == WTP, aborting plot."
    x3 = x2 + (x2 - x1) / 2
    x4 = (x1 + x2) / 2

    y0farmer = farmer_gain(system, x0 * USD / t) / MUSD
    y1farmer = farmer_gain(system, x1 * USD / t) / MUSD
    y3farmer = farmer_gain(system, x3 * USD / t) / MUSD
    assert abs(y1farmer) < 0.001, "Farmer gain at WTA not zero, aborting plot."

    y0plant = plant_gain(system, x0 * USD / t, discount_rate, tax_rate, depreciation_period) / MUSD
    y2plant = plant_gain(system, x2 * USD / t, discount_rate, tax_rate, depreciation_period) / MUSD
    y3plant = plant_gain(system, x3 * USD / t, discount_rate, tax_rate, depreciation_period) / MUSD
    assert abs(y2plant) < 0.001, "Plant gain at WTP not zero, aborting plot."

    transport_cost = system.transport_cost_per_t[1] / (USD / t)
    x5 = x4 - transport_cost / 2
    x6 = x4 + transport_cost / 2
    y5 = y6 = 0.01

    ax.plot([x0, x3], [y0farmer, y3farmer], 'g-')
    ax.plot(x1, y1farmer, 'go')
    ax.plot(x0, y0farmer, 'gs')
    ax.plot([x0, x3], [y0plant, y3plant], 'r-')
    ax.plot(x2, y2plant, 'ro')
    ax.plot([x5, x6], [y5, y6], 'bo-', linewidth=10)
    ax.legend(["Farmer's gain",
               "WTA",
               "Cost to collect",
               "Plant's gain",
               "WTP",
               "Transport cost"])

    ax.set_ylim([y3plant / 2, y0plant / 3])
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('Straw price (USD/t)')
    ax.set_ylabel('Cofiring benefit (MUSD)')

    ax.set_title(system.plant.parameter.name)


# noinspection PyTypeChecker
figure, axes = plt.subplots(nrows=1, ncols=2, figsize=[12, 6])
plot_feasibility(MongDuong1System, axes[0])
plot_feasibility(NinhBinhSystem, axes[1])
figure.tight_layout()

plt.savefig("figure_economics.svg")
