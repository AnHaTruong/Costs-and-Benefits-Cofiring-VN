
# Economic of co-firing in two power plants in Vietnam
#
# Pollutant emitter
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
import pandas as pd


class Fuel:
    def __init__(self,
                 name,
                 heat_value,
                 price,
                 transport_distance,
                 ef_transport
                 ):
        self.name = name
        self.heat_value = heat_value
        self.price = price
        self.price.display_unit = 'USD/t'
        self.transport_distance = transport_distance
        self.ef_transport = ef_transport

    def cost_per_GJ(self):
        cost = self.price / self.heat_value
        cost.display_unit = 'USD / GJ'
        return cost


class Emitter:
    """A system which emits pollutants.
       Refer to emission_factor for the allowable keys in "quantities" and "controls"
       Emissions are proportional to a quantity of fuel used (or to an activity level).
       Multiple fuels can be used.
       Each pollutant can be reduced by a given percentage (default: 0, no filter).

       Simple example:

       from parameters import emission_factor
       import numpy as np
       print(Emitter({'Straw': np.array([0., 1000., 1000.])}, emission_factor))

                     CO2                NOx             PM10                SO2
Straw  [0.0, 1003.86, 1003.86]  [0.0, 2.28, 2.28]  [0.0, 9.1, 9.1]  [0.0, 0.18, 0.18]
Total  [0.0, 1003.86, 1003.86]  [0.0, 2.28, 2.28]  [0.0, 9.1, 9.1]  [0.0, 0.18, 0.18]

       Real example:
       from parameters import emission_factor, MongDuong1Cofire

       MD_stack = Emitter({'6b_coal': MongDuong1Cofire.coal_used,
                                 'Straw': MongDuong1Cofire.biomass_used
                                 },
                                emission_factor,
                                {'CO2': 0.0, 'SO2': 0.982, 'NOx': 0.0, 'PM10': 0.996}
                                )

       print(MD_stack, "\n")
       print(MD_stack.emissions()['Total'], "\n")
       print(MD_stack.emissions()['Total']['CO2'], "\n")
       """
    def __init__(self,
                 quantities,   # A dictionary of (fuel: emissions_time_series)
                 emission_factor,
                 controls={'CO2': 0, 'SO2': 0, 'NOx': 0, 'PM10': 0}):
        # assert all(isinstance(v, np.ndarray) for v in quantities.values())
        self.quantities = quantities
        self.controled_emission_factor = pd.Series({
            fuel: pd.Series(emission_factor[fuel]) * (1 - pd.Series(controls))
            for fuel in emission_factor})

    def __str__(self):
        return self.emissions().transpose().to_string()

    def emissions_fuel(self, fuel, v_quantity):
        return {pollutant: v_quantity * self.controled_emission_factor[fuel][pollutant]
                for pollutant in self.controled_emission_factor[fuel].keys()
                }

    def emissions(self):
        df = pd.DataFrame({
            fuel: self.emissions_fuel(fuel, self.quantities[fuel])
            for fuel in self.quantities.keys()})
        df['Total'] = df.sum(axis=1)
#        return df
        return df.applymap(lambda v: v[1])   # Return a scalar (during regression testing)
