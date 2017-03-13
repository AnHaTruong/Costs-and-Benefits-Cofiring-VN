# Economic of co-firing in two power plants in Vietnam
#
# Coal saved & fuel cost saving
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

"""Calculation of the amount of coal saved and fuel cost saving due to biomass co-firing
"""


from parameters import biomass_ratio
from biomassrequired import gross_heat_input


def coal_saved(plant):
    """ amount of coal saved with biomass co-firing
    Does not work for a CofiringPlant

    """
    mass = gross_heat_input(plant) * biomass_ratio / plant.coal.heat_value
    mass.display_unit = 't/y'
    return mass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
