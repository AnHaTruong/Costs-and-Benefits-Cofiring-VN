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

We start coding as a specific. Will make abstract/reusable when it works.
"""

from matplotlib import pyplot as plt

from model.utils import MUSD
from sensitivity.one_at_a_time import result_business_value as data

#%%

data["Maximum"] = data.max(axis=1)
maximum = data["Maximum"].max()
data["Minimum"] = data.min(axis=1)
data["Width"] = (data["Low bound"] - data["High bound"]).apply(abs)

data.sort_values(by=["Width"], inplace=True)

#%% Convert to floats

variables = data.index.tolist()
base = data.iloc[0, 1] / MUSD
lows = data.iloc[:, 0].to_numpy() / MUSD
highs = data.iloc[:, 2].to_numpy() / MUSD

right = maximum / MUSD

#%% The actual drawing part

thickness = 0.8
ylabel_position = right * 1.05

# The y position for each variable
ys = range(len(variables))

# Plot the bars, one by one
for y, low, high, label in zip(ys, lows, highs, variables):
    # Each bar is a "broken" horizontal bar chart
    plt.broken_barh(
        [(low, base - low), (base, high - base)],
        (y - thickness / 2, thickness),
        facecolors=["grey", "white"],
        edgecolors=["grey", "grey"],
        linewidth=1,
    )
    plt.text(ylabel_position, y, label, va="center", ha="left")

plt.axvline(0, color="grey")  # Draw a vertical line down at zero

# Position the x-axis on the top, hide all the other spines (=axis lines)
axes = plt.gca()  # (gca = get current axes)
axes.spines["left"].set_visible(False)
axes.spines["right"].set_visible(False)
axes.spines["top"].set_visible(False)
axes.spines["bottom"].set_visible(True)

axes.set_xlabel("Business value (MUSD)")

axes.set_yticks(ys)
axes.set_yticklabels([])
axes.tick_params(axis="y", length=0)

axes.set_title("Sensitivity analysis of biomass cofiring, Mong Duong plant")
