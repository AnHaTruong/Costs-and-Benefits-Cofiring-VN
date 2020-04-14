"""Three pieces of code scraped from the net showing how to plot a tornado diagram in Python."""

#%%
# Marijn van Vliet
# Posted on Stackoverflow Aug 21 '15 at 10:24
# https://stackoverflow.com/questions/32132773/a-tornado-chart-and-p10-p90-in-python-matplotlib

import pytest

import numpy as np
from matplotlib import pyplot as plt

pytest.skip("Skipping tornadoplot_sample module.", allow_module_level=True)


###############################################################################
# The data (change all of this to your actual data, this is just a mockup)
variables = [
    "apple",
    "juice",
    "orange",
    "peach",
    "gum",
    "stones",
    "bags",
    "lamps",
]

base = 3000

lows = np.array(
    [
        base - 246 / 2,
        base - 1633 / 2,
        base - 500 / 2,
        base - 150 / 2,
        base - 35 / 2,
        base - 36 / 2,
        base - 43 / 2,
        base - 37 / 2,
    ]
)

values = np.array([246, 1633, 500, 150, 35, 36, 43, 37])

###############################################################################
# The actual drawing part

# The y position for each variable
ys = range(len(values))[::-1]  # top to bottom

# Plot the bars, one by one
for y, low, value in zip(ys, lows, values):
    # The width of the 'low' and 'high' pieces
    low_width = base - low
    high_width = low + value - base

    # Each bar is a "broken" horizontal bar chart
    plt.broken_barh(
        [(low, low_width), (base, high_width)],
        (y - 0.4, 0.8),
        facecolors=["white", "white"],  # Try different colors if you like
        edgecolors=["black", "black"],
        linewidth=1,
    )

    # Display the value as text. It should be positioned in the center of
    # the 'high' bar, except if there isn't any room there, then it should be
    # next to bar instead.
    x = base + high_width / 2
    if x <= base + 50:
        x = base + high_width + 50
    plt.text(x, y, str(value), va="center", ha="center")

# Draw a vertical line down the middle
plt.axvline(base, color="black")

# Position the x-axis on the top, hide all the other spines (=axis lines)
axes = plt.gca()  # (gca = get current axes)
axes.spines["left"].set_visible(False)
axes.spines["right"].set_visible(False)
axes.spines["bottom"].set_visible(False)
axes.xaxis.set_ticks_position("top")

# Make the y-axis display the variables
plt.yticks(ys, variables)

# Set the portion of the x- and y-axes to show
plt.xlim(base - 1000, base + 1000)
plt.ylim(-1, len(variables))


#%%

# This one by Tony Yu
# posted on matplotlib mailing list Jun 22, 2012
# http://matplotlib.1069221.n5.nabble.com/tornado-chart-td26614.html

# tornado chart example
import numpy as np
import matplotlib.pyplot as plt


people = ("Tom", "Dick", "Harry", "Slim", "Jim")
num_people = len(people)

time_spent = np.random.uniform(low=5, high=100, size=num_people)
proficiency = np.abs(time_spent / 12.0 + np.random.normal(size=num_people))
pos = np.arange(num_people) + 0.5  # bars centered on the y axis

fig, (ax_left, ax_right) = plt.subplots(ncols=2)
ax_left.barh(pos, time_spent, align="center", facecolor="cornflowerblue")
ax_left.set_yticks([])
ax_left.set_xlabel("Hours spent")
ax_left.invert_xaxis()

ax_right.barh(pos, proficiency, align="center", facecolor="lemonchiffon")
ax_right.set_yticks(pos)
# x moves tick labels relative to left edge of axes in axes units
ax_right.set_yticklabels(people, ha="center", x=-0.08)
ax_right.set_xlabel("Proficiency")

plt.suptitle("Learning Python")

plt.show()


#%%

# John Hunter - 4

# tornado chart example; inspired by
# http://www.nytimes.com/imagepages/2007/07/29/health/29cancer.graph.web.html
# and sample code from Tony Yu
import numpy as np
import matplotlib.pyplot as plt

cancers = [
    "Kidney cancer",
    "Bladder cancer",
    "Esophageal cancer",
    "Ovarian cancer",
    "Liver cancer",
    "Non-Hodgkin's\nlymphoma",
    "Leukemia",
    "Prostate cancer",
    "Pancreatic cancer",
    "Breast cancer",
    "Colorectal cancer",
    "Lung cancer",
]

num_cancers = len(cancers)

# generate some random data for the graphs (TODO; put real data here)
new_cases_men = np.random.uniform(low=20e3, high=200e3, size=num_cancers)

new_cases_women = np.random.uniform(low=20e3, high=200e3, size=num_cancers)
deaths_women = np.random.rand(num_cancers) * new_cases_women
deaths_men = np.random.rand(num_cancers) * new_cases_men

# force these values where the labels happen to make sure they are
# positioned nicely
new_cases_men[-1] = 120e3
new_cases_men[-2] = 55e3
deaths_men[-1] = 80e3

# bars centered on the y axis
pos = np.arange(num_cancers) + 0.5

# make the left and right axes for women and men
fig = plt.figure(facecolor="white", edgecolor="none")
ax_women = fig.add_axes([0.05, 0.1, 0.35, 0.8])
ax_men = fig.add_axes([0.6, 0.1, 0.35, 0.8])

ax_men.set_xticks(np.arange(50e3, 201e3, 50e3))
ax_women.set_xticks(np.arange(50e3, 201e3, 50e3))

# turn off the axes spines except on the inside y-axis
# for loc, spine in ax_women.spines.iteritems():
for loc, spine in ax_women.spines.items():
    if loc != "right":
        spine.set_color("none")  # don't draw spine

# for loc, spine in ax_men.spines.iteritems():
for loc, spine in ax_men.spines.items():
    if loc != "left":
        spine.set_color("none")  # don't draw spine

# just tick on the top
ax_women.xaxis.set_ticks_position("top")
ax_men.xaxis.set_ticks_position("top")

# make the women's graphs
ax_women.barh(
    pos, new_cases_women, align="center", facecolor="#DBE3C2", edgecolor="None"
)
ax_women.barh(
    pos, deaths_women, align="center", facecolor="#7E895F", height=0.5, edgecolor="None"
)
ax_women.set_yticks([])
ax_women.invert_xaxis()

# make the men's graphs
ax_men.barh(pos, new_cases_men, align="center", facecolor="#D8E2E1", edgecolor="None")
ax_men.barh(
    pos, deaths_men, align="center", facecolor="#6D7D72", height=0.5, edgecolor="None"
)
ax_men.set_yticks([])

# we want the cancer labels to be centered in the fig coord system and
# centered w/ respect to the bars so we use a custom transform
import matplotlib.transforms as transforms

transform = transforms.blended_transform_factory(fig.transFigure, ax_men.transData)
for i, label in enumerate(cancers):
    ax_men.text(0.5, i + 0.5, label, ha="center", va="center", transform=transform)

# the axes titles are in axes coords, so x=0, y=1.025 is on the left
# side of the axes, just above, x=1.0, y=1.025 is the right side of the
# axes, just above
ax_men.set_title("MEN", x=0.0, y=1.025, fontsize=12)
ax_women.set_title("WOMEN", x=1.0, y=1.025, fontsize=12)


# the fig suptile is in fig coords, so 0.98 is the far right; we right align the text
fig.suptitle("July 29, 2007", x=0.98, ha="right")

# now add the annotations
ax_men.annotate(
    "New Cases",
    xy=(0.95 * new_cases_men[-1], num_cancers - 0.5),
    xycoords="data",
    xytext=(20, 0),
    textcoords="offset points",
    size=12,
    va="center",
    arrowprops=dict(arrowstyle="->"),
)

# a curved arrow for the deaths annotation
ax_men.annotate(
    "Deaths",
    xy=(0.95 * deaths_men[-1], num_cancers - 0.5),
    xycoords="data",
    xytext=(40, -20),
    textcoords="offset points",
    size=12,
    va="center",
    arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=3"),
)

plt.show()
