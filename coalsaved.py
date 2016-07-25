# Economic of co-firing in two power plants in Vietnam
#
# Coal saved & fuel cost saving
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Calculation of the amount of coal saved and fuel cost saving due to biomass co-firing
    
"""

from parameters import biomass_ratio
from biomassrequired import gross_heat_input


def coal_saved(plant):
    """ amount of coal save with biomass co-firing
    """
    return gross_heat_input(plant) * biomass_ratio / plant.coal_heat_value


   
