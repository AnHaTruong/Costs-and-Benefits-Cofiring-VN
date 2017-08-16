# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Common init file for all modules in the directory.

This file should be imported before any "import natu ..."
otherwise use_quantities does not work

It is in the manual, but worth reminding:
Units thread into arrays from the right but not from the left
  np.array([1, 2]) * m  -->  array([1 m, 2 m], dtype=object)
  m * np.array([1, 2])   --> [1  2] m
 So when multiplying a vector by a quantity, put the vector left
"""

from natu import config
# config.use_quantities = False

import natu.numpy as np
from natu.numpy import array
from natu.units import hr, t
from natu import units
from natu.core import ScalarUnit

# Semantic overloading: we reuse the "amount" dimension to mean "value"

if config.use_quantities:
    VND = ScalarUnit(1 / 22270, 'N', 'mol', prefixable=True)
    units.VND = VND

    USD = ScalarUnit(1, 'N', 'mol', prefixable=True)
    units.USD = USD
else:
    USD = 1
    VND = USD / 22270

kUSD = 1000 * USD
MUSD = 1000 * kUSD

# Full Time Equivalent, a work time unit amounting to "1 job".
FTE = 1560 * hr
units.FTE = FTE

TIMEHORIZON = 20   # years

ZEROS = np.zeros(TIMEHORIZON + 1)
ONES = np.ones(TIMEHORIZON + 1)


def after_invest(qty):
    """Construct a time serie from a quantity.

    Used to vectorize calculations involving qty.
    Return  natu.numpy.array([0, qty, ..., qty]).
    The dtype=object might be a performance cost when "use_quantities = False" (untested).
    """
    assert not hasattr(qty, '__iter__'), "Vectorize only scalar arguments."
    return array([0 * qty] + [qty] * TIMEHORIZON, dtype=object)


def display_as(qty, unit):
    """Set the display_unit of qty or of qty's items to 'unit' and return qty.

    This function is more robust than using  qty.display_unit =  in the code directly,
    because when  use_quantities = False  it is transparent instead of producing an error

    >>> display_as(2 * hr, 's')
    7200 s

    Polymorphic: qty can be a quantity or a vector of quantities

    >>> from natu.units import y
    >>> v = [48 * hr, 1 * y]
    >>> v
    [48 hr, 1 y]
    >>> display_as(v, 'd')
    [2 d, 365.25 d]
    """
    if config.use_quantities:
        if hasattr(qty, '__iter__'):
            for element in qty:
                element.display_unit = unit
        else:
            qty.display_unit = unit
    return qty


def isclose(qty_a, qty_b, rel_tol=1e-09, abs_tol=0.0):
    """Compare two numbers or quantities for almost-equality according to PEP 485.

    >>> .1 + .1 + .1 == .3
    False

    >>> isclose(.1 + .1 + .1, .3)
    True

    This version works with natu quantities
    The versions in standard library math or even in natu.math package do not (bug in natu ?)
    >>> isclose(0 * VND, 0 * USD)
    True
    """
    return abs(qty_a - qty_b) <= max(rel_tol * max(abs(qty_a), abs(qty_b)), abs_tol)


def safe_divide(costs, masses):
    """Divide two vectors elementwise, producing NaN instead of error when the divisor is zero."""
    result = costs.copy()
    for i, mass in enumerate(masses):
        if mass.__nonzero__():
            result[i] /= mass
        else:
            result[i] = display_as(float('NaN') * USD / t, 'USD/t')
    return display_as(result, 'USD/t')
