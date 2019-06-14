# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Emitter: this class represents a system which emits pollutants."""
from collections import namedtuple

import pandas as pd

Activity = namedtuple('Activity', 'name, level, emission_factor')


# pylint: disable=too-few-public-methods
class Emitter:
    """A system which emits pollutants.

    Multiple activities and multiple pollutants.
    Emissions are proportional to an activity level,
    for example a quantity of fuel burned, or a distance traveled by a given mode

    Example:
    >>> pd.options.display.float_format = '{:,.1f}'.format
    >>> a = Activity('Combustion', 1000, {'CO2': 1, 'PM10': 0.0091})
    >>> b = Activity('Transport', 300, {'CO2': 1, 'PM10': 0.02})
    >>> print(Emitter(a, b))
                   CO2  PM10
    Combustion 1,000.0   9.1
    Transport    300.0   6.0
    Total      1,300.0  15.1

    Each pollutant can be reduced by a given fraction (default: 0, no filter),
    the reduction is end-of-pipe, common to all activities

    >>> print(Emitter(a, b, emission_control={'PM10': 0.9}))
                   CO2  PM10
    Combustion 1,000.0   0.9
    Transport    300.0   0.6
    Total      1,300.0   1.5

    Polymorphic: activity level can be a scalar or an array representing a time series

    >>> import numpy as np
    >>> c = Activity('Combustion', np.array([1000, 110, 0]), {'CO2': 1, 'PM10': 0.001})
    >>> print(Emitter(c))
                           CO2              PM10
    Combustion  [1000, 110, 0]  [1.0, 0.11, 0.0]
    Total       [1000, 110, 0]  [1.0, 0.11, 0.0]

    Mutable: activities can be changed after the initialization

    >>> e = Emitter()
    >>> e.activities = [a]
    >>> print(e)
                   CO2  PM10
    Combustion 1,000.0   9.1
    Total      1,000.0   9.1
    """

    def __init__(self, *activities, emission_control=None):
        """Initialize with zero or more activities and optional emission control.

        *activities: each must be an Activity namedtuple
        emission_control: a dictionary of str: float, where str is the pollutant name
            and the float between 0 and 1 is the filter efficiency
        """
        self.activities = activities
        self.emission_control = emission_control

    def __str__(self):
        """Return the table of emissions.

        Pollutants are in columns, activities are in row.
        """
        return self.emissions(total=True).transpose().to_string()

    def emissions(self, total=False):
        """Return a dataframe of emissions, including a total across all activities."""
        pollutants = self.activities[0].emission_factor.keys()

        control = {pollutant: 1 for pollutant in pollutants}

        if self.emission_control:
            for pollutant, fraction in self.emission_control.items():
                control[pollutant] = 1 - fraction
        result = pd.DataFrame({
            activity.name: {
                pollutant:
                    activity.level * activity.emission_factor[pollutant] * control[pollutant]
                for pollutant in pollutants}
            for activity in self.activities})
        if total:
            result['Total'] = result.sum(axis=1)  # Should return this directly
        return result
