# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# tornado plot
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Create a tornado plot.

A tornado plot is a kind of horizontal bar graph.
It is often used to display results of sensitivity analysis one at a time.

This file builds upon Marijn van Vliet's post on Stackoverflow Aug 21 '15 at 10:24
https://stackoverflow.com/questions/32132773/a-tornado-chart-and-p10-p90-in-python-matplotlib
"""

from pandas import DataFrame
from matplotlib import pyplot as plt

from model.utils import MUSD
from sensitivity.uncertainty import uncertainty_MD1, uncertainty_NB
from sensitivity.one_at_a_time import one_at_a_time
from sensitivity.blackbox import f_MD1, f_NB


def plot_tornado(axes, data, ys, stack_label):
    """Plot the horizontal bars for one objective."""

    #%% Convert to floats

    base = data.iloc[0, 1] / MUSD
    lows = data.iloc[:, 0].to_numpy() / MUSD
    highs = data.iloc[:, 2].to_numpy() / MUSD

    thickness = 0.8

    # Plot the bars, one by one
    for y, low, high in zip(ys, lows, highs):
        axes.broken_barh(
            [(low, base - low), (base, high - base)],
            (y - thickness / 2, thickness),
            facecolors=["#FFFFFF00", "mistyrose"],
            edgecolors=["black", "darkred"],
            linewidth=1,
        )
    axes.text(base, ys[-1] + 1, stack_label, va="top", ha="center")


def plot_sensitivity(uncertainty, model, plant_name, axes):
    """Plot the sensitivity analysis, tornado diagram, two objectives."""

    runs = one_at_a_time(uncertainty, model)

    stack_order = [
        "tax_rate",
        # "open_burn_rate",
        "biomass_plantgate",
        "biomass_fieldside",
        "electricity_price",
        "external_cost_NOx",
        "external_cost_SO2",
        "coal_price",
        "external_cost_CO2",
        "discount_rate",
        "external_cost_PM2.5",
        #        "external_cost_PM10",
        "cofire_rate",
    ]

    ys = range(len(stack_order))
    data = DataFrame(runs["business_value"]).reindex(stack_order)
    plot_tornado(axes, data, ys, "Business value")

    data = DataFrame(runs["external_value"]).reindex(stack_order)
    plot_tornado(axes, data, ys, "External value")

    # Plot the parameters name
    data["Maximum"] = data.max(axis=1)
    maximum = data["Maximum"].max()
    data["Minimum"] = data.min(axis=1)
    right = maximum / MUSD
    ylabel_position = right * 1.05

    for y, label in zip(ys, stack_order):
        axes.text(ylabel_position, y, label, va="center", ha="left")

    axes.axvline(0, color="grey")  # Draw a vertical line down at zero

    axes.spines["left"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.spines["top"].set_visible(False)
    axes.spines["bottom"].set_visible(True)

    axes.set_yticks(ys)
    axes.set_yticklabels([])
    axes.tick_params(axis="y", length=0)

    axes.text(
        ylabel_position,
        len(stack_order),
        plant_name,
        va="center",
        ha="left",
        style="italic",
    )
    axes.text(right * 1.03, -1.05, "MUSD", va="top", ha="left")


# noinspection PyTypeChecker
figure, axes_list = plt.subplots(nrows=2, ncols=1, figsize=[12, 9])
plot_sensitivity(uncertainty_MD1, f_MD1, "Mong Duong 1", axes_list[0])
plot_sensitivity(uncertainty_NB, f_NB, "Ninh Binh", axes_list[1])
plt.subplots_adjust(right=0.8)

plt.savefig("figure_sensitivity.pdf")
