# Economic of co-firing in two power plants in Vietnam
#
# Pollutant emitter
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
import pandas as pd


class Emitter:
    """A system which emits pollutants.
       Refer to emission_factor for the allowable keys in "quantities" and "controls"
       Emissions are proportional to a quantity of fuel used (or to an activity level).
       Multiple fuels can be used.
       Each pollutant can be reduced by a given percentage (default: 0, no filter).

       Simplest example:
       from parameters import emission_factor
       print(Emitter({'Straw': 1000}, emission_factor))

                  CO2   NOx  PM10   SO2
       Straw  1003.86  2.28   9.1  0.18
       Total  1003.86  2.28   9.1  0.18

       Real example:
       from parameters import emission_factor, MongDuong1
       MD_plant_stack = Emitter({'6b_coal': MongDuong1.coal_used[1], 'Straw': 0*t/y},
                                emission_factor,
                                {'CO2': 0.0, 'SO2': 0.982, 'NOx': 0.0, 'PM10': 0.996}
                                )

       print(MD_plant_stack, "\n")
       print(MD_plant_stack.emissions['Total'], "\n")
       print(MD_plant_stack.emissions['Total']['CO2'], "\n")

       """
    def __init__(self, quantities, emission_factors, controls={'CO2': 0, 'SO2': 0, 'NOx': 0, 'PM10': 0}):
        self.controls = pd.Series(controls)
        self.quantities = pd.Series(quantities)
        self.emissions = pd.DataFrame(
            {fuel: (pd.Series(emission_factors[fuel]) *
                    (1 - self.controls) *
                    self.quantities[fuel]
                    )
             for fuel in quantities.keys()
             })
        self.emissions['Total'] = self.emissions.sum(axis=1)

    def __str__(self):
        return self.emissions.transpose().to_string()
