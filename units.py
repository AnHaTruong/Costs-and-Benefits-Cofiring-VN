# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#


from natu.units import km, hr, y
import natu.numpy as np

# Semantic overloading: we reuse the "amount" dimension to mean "value"
from natu.core import ScalarUnit
from natu import units

VND = ScalarUnit(1, 'N', 'mol', prefixable=True)
units.VND = VND

USD = ScalarUnit(22270, 'N', 'mol', prefixable=True)
units.USD = USD


h_per_yr = 8760 * hr
time_step = 1 * y
time_horizon = 20

v_zeros = np.zeros(time_horizon + 1, dtype=np.float64)
v_ones = np.ones(time_horizon + 1, dtype=np.float64)
v_after_invest = np.ones(time_horizon + 1, dtype=np.float64)
v_after_invest[0] = 0

zero_USD = 0 * USD
zero_VND = 0 * VND
zero_km = 0 * km


def display_as(v, unit):
    """Sets the display_unit of every element of the vector to 'unit'.
       Returns the vector
    """
    for i in range(time_horizon+1):
        v[i].display_unit = unit
    return v


# TODO: all functions should set the display_unit of their result
# to make this function unnecessary
def print_with_unit(func, unit):
    """ Display the desired unit on Tables"""
    value = func
    value.display_unit = unit
    return value


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):   # From PEP 485
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
