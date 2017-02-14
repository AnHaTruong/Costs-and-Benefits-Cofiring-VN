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
from natu.units import kW, MJ, kg, t, d, MW, ha, g    # Reexported
import natu.numpy as np

# Semantic overloading: we reuse the "amount" dimension to mean "value"
from natu.core import ScalarUnit
from natu import units


VND = ScalarUnit(1, 'N', 'mol', prefixable=True)
units.VND = VND

USD = ScalarUnit(22270, 'N', 'mol', prefixable=True)
units.USD = USD

time_step = 1 * y
time_horizon = 20

v_zeros = np.zeros(time_horizon + 1, dtype=np.float64)
v_ones = np.ones(time_horizon + 1, dtype=np.float64)
v_after_invest = np.ones(time_horizon + 1, dtype=np.float64)
v_after_invest[0] = 0

h_per_yr = 8760 * hr

zero_USD = 0 * USD
zero_VND = 0 * VND
zero_km = 0 * km


def print_with_unit(func, unit):
    """ Display the desired unit on Tables"""
    value = func
    value.display_unit = unit
    return value
