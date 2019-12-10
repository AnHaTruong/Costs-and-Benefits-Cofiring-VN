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
"""Plot the social cost-benefit analysis figure."""

import matplotlib.pyplot as plt

# pylint: disable=wrong-import-order
from manuscript1.parameters import MongDuong1System, NinhBinhSystem, depreciation_period
from natu.units import kUSD

#%%


def plot_cba(system, axes):
    """Plot to compare costs and benefits of cofiring."""
    extra_om = (
        system.cofiring_plant.operating_expenses_detail().loc["O&M, coal"]
        + system.cofiring_plant.operating_expenses_detail().loc["O&M, biomass"]
        - system.plant.operating_expenses_detail().loc["Operation & Maintenance"])

    cost = [system.farmer.operating_expenses()[1] / kUSD,
            system.reseller.operating_expenses()[1] / kUSD,
            system.cofiring_plant.amortization(depreciation_period)[1] / kUSD,
            extra_om[1] / kUSD]

    cumul = [0, cost[0], cost[0] + cost[1], cost[0] + cost[1] + cost[2]]
    axes.bar(x=[0, 0, 0, 0],
             height=cost,
             width=0.1,
             bottom=cumul,
             edgecolor="black")

    fuel_saved = (
        system.plant.operating_expenses_detail().loc["Fuel cost, coal"]
        - system.cofiring_plant.operating_expenses_detail().loc["Fuel cost, coal"])

    benefit = [fuel_saved[1] / kUSD,
               524,
               12549,
               496,
               137]
    cumul = [0,
             benefit[0],
             benefit[0] + benefit[1],
             benefit[0] + benefit[1] + benefit[2],
             benefit[0] + benefit[1] + benefit[2] + benefit[3]]

    axes.bar(x=[0.5, 0.5, 0.5, 0.5, 0.5],
             height=benefit,
             width=0.1,
             bottom=cumul,
             edgecolor="black")

    axes.set_xlim(left=-0.1, right=0.9)
    axes.tick_params(axis='x', length=0)
    axes.set_xticks([0, 0.5])
    axes.set_xticklabels(["Cost", "Benefit"])

    axes.set_ylabel('kUSD/y')

    axes.set_title(system.plant.name)


# noinspection PyTypeChecker
FIGURE, AXESS = plt.subplots(nrows=1, ncols=2, figsize=[12, 6])
plot_cba(MongDuong1System, AXESS[0])
plot_cba(NinhBinhSystem, AXESS[1])
FIGURE.tight_layout()

#plt.savefig('figure_cba.svg')
