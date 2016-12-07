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



from parameters import biomass_ratio, coal_import_price
from biomassrequired import gross_heat_input


def coal_saved(plant):
    """ amount of coal saved with biomass co-firing

    >>> from parameters import *
    >>> print_with_unit(coal_saved, MongDuong1, 't/y')
    155987 t/y
    >>> print_with_unit(coal_saved, NinhBinh, 't/y')
    28974.7 t/y
    """
    return gross_heat_input(plant) * biomass_ratio / plant.coal_heat_value
    
    
def coal_import_saving(plant):
    """ Return the maximum benefit for trade balance from the amount of 
        avoided coal import (equivalence to coal saved per year) from co-firing
        assuming that same amount of coal will be imported if there is no co-firing
    >>> from parameters import *   
    >>> print_with_unit(coal_import_saving, MongDuong1, 'kUSD/y')
    11387 kUSD/y
    >>> print_with_unit(coal_import_saving, NinhBinh, 'kUSD/y')
    2115.15 kUSD/y
    """
    return coal_saved(plant) * coal_import_price

def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
