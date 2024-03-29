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

from manuscript1.parameters import (
    MongDuong1System,
    NinhBinhSystem,
    depreciation_period,
    external_cost,
)

from model.utils import kUSD, array, cumsum, roll

#%%


# pylint: disable=too-many-locals
def plot_cba(system, axes):
    """Plot to compare costs and benefits of cofiring."""
    axes.set_title(system.plant.name)
    axes.set_ylabel("kUSD/y")

    axes.set_xlim(left=-0.4, right=1.25)
    axes.tick_params(axis="x", length=0)
    axes.set_xticks([0.3, 0.7])
    axes.set_xticklabels(["Costs", "Benefits"])

    #%% Benefits

    fuel_saved = (
        system.plant.operating_expenses_detail().loc["Fuel cost, main fuel"]
        - system.cofiring_plant.operating_expenses_detail().loc["Fuel cost, main fuel"]
    )

    emission_reduction_value = system.emissions_reduction_benefit(external_cost).loc[
        "Value"
    ]
    benefit_year1 = emission_reduction_value.apply(lambda sequence: sequence[1] / kUSD)
    benefit_year1 = benefit_year1.drop("PM10")

    benefits = array([fuel_saved[1] / kUSD] + list(benefit_year1))

    top_benefits = cumsum(benefits)
    bottom_benefits = roll(top_benefits, 1)
    bottom_benefits[0] = 0
    mid_benefits = bottom_benefits + benefits / 2

    axes.bar(
        x=[0.7] * 5,
        height=benefits,
        width=0.1,
        bottom=bottom_benefits,
        edgecolor="black",
    )

    voffset_unit = top_benefits[-1] / 100

    def legend_benefit(text, row, ypos):
        axes.annotate(
            text + str(int(benefits[row])) + " k$/y",
            xy=(0.75, mid_benefits[row]),
            xytext=(0.90, ypos),
            arrowprops=dict(arrowstyle="-"),
            horizontalalignment="left",
            verticalalignment="center",
        )

    legend_benefit("Saved coal\n", 0, mid_benefits[0])
    texts = benefit_year1.keys()
    legend_benefit(texts[0] + "\n", 1, mid_benefits[1] - 5 * voffset_unit)
    legend_benefit(texts[1] + "\n", 2, mid_benefits[2] + 5 * voffset_unit)
    legend_benefit(texts[2] + "\n", 3, mid_benefits[3])
    legend_benefit(texts[3] + "\n", 4, mid_benefits[4])

    #%% Costs

    extra_om = (
        system.cofiring_plant.operating_expenses_detail().loc["O&M, main fuel"]
        + system.cofiring_plant.operating_expenses_detail().loc["O&M, cofuel"]
        - system.plant.operating_expenses_detail().loc["Operation & Maintenance"]
    )

    costs = array(
        [
            system.farmer.operating_expenses()[1] / kUSD,
            system.reseller.operating_expenses()[1] / kUSD,
            system.cofiring_plant.amortization(depreciation_period)[1] / kUSD,
            extra_om[1] / kUSD,
        ]
    )

    top_costs = cumsum(costs)
    bottom_costs = roll(top_costs, 1)
    bottom_costs[0] = 0
    mid_costs = bottom_costs + costs / 2

    axes.bar(
        x=[0.3] * 4, height=costs, width=0.1, bottom=bottom_costs, edgecolor="black"
    )

    def legend_cost(text, row):
        axes.annotate(
            text + str(int(costs[row])) + " k$/y",
            xy=(0.25, mid_costs[row]),
            xytext=(0.1, mid_costs[0] + row * voffset_unit * 5),
            arrowprops=dict(arrowstyle="-"),
            horizontalalignment="right",
            verticalalignment="center",
        )

    legend_cost("Collect ", 0)
    legend_cost("Transport ", 1)
    legend_cost("Invest ", 2)
    legend_cost("Operate ", 3)

    #%% Business value

    business_value = benefits[0] - top_costs[-1]

    axes.bar(
        x=[0.5],
        width=0.1,
        height=business_value,
        bottom=top_costs[-1],
        edgecolor="black",
    )

    axes.hlines(
        y=[top_costs[-1], benefits[0]],
        xmin=[0.35, 0.55],
        xmax=[0.45, 0.65],
        linestyles="dashed",
    )

    axes.annotate(
        "Business value\n" + str(int(business_value)) + " k$/y",
        xy=(0.45, top_costs[-1] + business_value * 0.75),
        xytext=(0.30, top_costs[-1] + business_value),
        arrowprops=dict(arrowstyle="-"),
        horizontalalignment="right",
        verticalalignment="bottom",
    )

    #%% Externalities

    externalities = top_benefits[-1] - benefits[0]

    axes.bar(
        x=[0.5], width=0.1, height=externalities, bottom=benefits[0], edgecolor="black"
    )

    axes.hlines(y=top_benefits[-1], xmin=0.55, xmax=0.65, linestyles="dashed")

    axes.annotate(
        "Externality \n" + str(int(externalities)) + " k$/y",
        xy=(0.45, benefits[0] + externalities * 0.25),
        xytext=(0.25, benefits[0] + externalities * 0.35),
        arrowprops=dict(arrowstyle="-"),
        horizontalalignment="right",
        verticalalignment="bottom",
    )

    # End of plot definition


# noinspection PyTypeChecker
FIGURE, AXESS = plt.subplots(nrows=1, ncols=2, figsize=[12, 6])
plot_cba(MongDuong1System, AXESS[0])
plot_cba(NinhBinhSystem, AXESS[1])
FIGURE.tight_layout()

plt.savefig("figure_cba.pdf")
