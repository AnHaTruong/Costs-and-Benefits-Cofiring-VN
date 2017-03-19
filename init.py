# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#


from natu.units import hr, y
import natu.numpy as np
# RTFM:  Units thread into arrays from the right but not from the left
#  np.array([1, 2]) * m  -->  array([1 m, 2 m], dtype=object)
#  m * np.array([1, 2])   --> [1  2] m
# So when multiplying a vector by a quantity, put the vector left

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


def display_as(v, unit):
    """Sets the display_unit of every element of the vector to 'unit'.
       Returns the vector
    """
    for element in v:
        element.display_unit = unit
    return v


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Compare two floats for almost-equality according to PEP 485"""
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def zero_to_NaN(vector):
    """A copy of the vector, with  0 * unit  replaced by  NaN * unit"""
    return [element if element else element * float('nan') for element in vector]
