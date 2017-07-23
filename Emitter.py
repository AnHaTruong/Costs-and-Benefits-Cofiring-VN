# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Emitter: this class represents a system which emits pollutants."""

import pandas as pd


# pylint: disable=too-few-public-methods
class Emitter:
    """A system which emits pollutants.

       Multiple activities and multiple pollutants.
       Each pollutant can be reduced by a given percentage (default: 0, no filter),
           the reduction is end-of-pipe, common to all activities
       Emissions are proportional to an activity level,
           for example a quantity of fuel burned, or a distance traveled by a given mode
       Polymorphic signature: activity level can be a scalar or an array representing a time series

       The emission_factor table is a dictionary of dictionaries:
           emission_factor[activity][pollutant]

       Simple example:

       from parameters import emission_factor
       import numpy as np
       print(Emitter({'Straw': np.array([0., 1000., 1000.])}, emission_factor))

                     CO2                NOx             PM10                SO2
Straw  [0.0, 1003.86, 1003.86]  [0.0, 2.28, 2.28]  [0.0, 9.1, 9.1]  [0.0, 0.18, 0.18]
Total  [0.0, 1003.86, 1003.86]  [0.0, 2.28, 2.28]  [0.0, 9.1, 9.1]  [0.0, 0.18, 0.18]

       Real example:

       from parameters import emission_factor, MongDuong1System

       emitter = Emitter({'6b_coal': MongDuong1System.cofiring_plant.coal_used,
                          'Straw': MongDuong1System.cofiring_plant.biomass_used
                          },
                         emission_factor,
                         {'CO2': 0.0, 'SO2': 0.982, 'NOx': 0.0, 'PM10': 0.996}
                         )

       print(emitter, "\n")
       print(emitter.emissions()['Total'], "\n")
       print(emitter.emissions()['Total']['CO2'], "\n")
       """
    def __init__(self,
                 activity_level,   # A dictionary of {activity: level, ...}
                 emission_factor,
                 emission_control=None):
        assert set(activity_level.keys()).issubset(emission_factor.keys())
        self.levels = activity_level
        self.activities = activity_level.keys()
        self.emission_factor = emission_factor
        self.emission_control = emission_control

        self.pollutants = emission_factor[list(activity_level)[0]].keys()

        if emission_control is None:
            emission_control = {'CO2': 0, 'SO2': 0, 'NOx': 0, 'PM10': 0}
        self.controled_emission_factor = pd.Series({
            activity: pd.Series(emission_factor[activity]) * (1 - pd.Series(emission_control))
            for activity in emission_factor})

    def __str__(self):
        return self.emissions().transpose().to_string()

    def emissions(self):
        df = pd.DataFrame({
            activity: {
                pollutant:
                    self.levels[activity] * self.controled_emission_factor[activity][pollutant]
                for pollutant in self.pollutants}
            for activity in self.activities})
        df['Total'] = df.sum(axis=1)
        return df
