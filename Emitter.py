# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
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
       >>> a = Activity('Combustion', 1000, {'CO2': 1, 'PM10': 0.0091})
       >>> b = Activity('Transport', 300, {'CO2': 1, 'PM10': 0.02})
       >>> print(Emitter(a, b))
                      CO2  PM10
       Combustion  1000.0   9.1
       Transport    300.0   6.0
       Total       1300.0  15.1

       Each pollutant can be reduced by a given fraction (default: 0, no filter),
           the reduction is end-of-pipe, common to all activities

       >>> print(Emitter(a, b, emission_control={'PM10': 0.9}))
                      CO2  PM10
       Combustion  1000.0  0.91
       Transport    300.0  0.60
       Total       1300.0  1.51

       Polymorphic: activity level can be a scalar or an array representing a time series

       >>> import numpy as np
       >>> c = Activity('Combustion', np.array([1000, 110, 0]), {'CO2': 1, 'PM10': 0.0091})
       >>> print(Emitter(c))
                              CO2               PM10
       Combustion  [1000, 110, 0]  [9.1, 1.001, 0.0]
       Total       [1000, 110, 0]  [9.1, 1.001, 0.0]

       Mutable: activities can be changed after the initialization

       >>> e = Emitter()
       >>> e.activities = [a]
       >>> print(e)
                      CO2  PM10
       Combustion  1000.0   9.1
       Total       1000.0   9.1
       """

    def __init__(self,
                 *activities,
                 emission_control=None):
        self.activities = activities
        self.emission_control = emission_control

    def __str__(self):
        return self.emissions().transpose().to_string()

    def emissions(self):
        self.pollutants = self.activities[0].emission_factor.keys()

        self.control = {key: 1 for key in self.pollutants}

        if self.emission_control:
            for pollutant, fraction in self.emission_control.items():
                self.control[pollutant] = 1 - fraction
        df = pd.DataFrame({
            activity.name: {
                pollutant:
                    activity.level * activity.emission_factor[pollutant] * self.control[pollutant]
                for pollutant in self.pollutants}
            for activity in self.activities})
        df['Total'] = df.sum(axis=1)
        return df
