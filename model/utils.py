# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Common init file for all modules in the directory.

For 10x acceleration, add these three lines BEFORE imporing this module:
    # pylint: disable=wrong-import-position
    from natu import config
    config.use_quantities = False

Besides that, no module should import objects from natu.

It¨ is in the manual, but worth reminding:
Units thread into arrays from the right but not from the left
  array([1, 2]) * m  -->  array([1 m, 2 m], dtype=object)
  m * array([1, 2])   --> [1  2] m
 So when multiplying a vector by a quantity, put the vector left
"""

from numpy import asarray, arange

from natu import config

from natu.numpy import array, unique
from natu.numpy import ones, zeros, concatenate, cumsum, roll, sum as np_sum
from natu.math import fsum, sqrt, pi
from natu.units import t, hr, d, y
from natu.units import m, km, ha, g, kg, MJ, GJ, TJ, kWh, MWh, kW, MW
from natu import units
from natu.core import ScalarUnit

# Quiet pylint "unused-import" warning , they are for re-export.
_ = m, km, ha, g, kg, d, MJ, GJ, TJ, kWh, MWh, kW, MW
_ = arange, ones, zeros, concatenate, np_sum, cumsum, roll
_ = fsum, sqrt, pi

use_floats = not config.use_quantities

# Define kt and Mt units
# The t unit is not prefixable in natu.py , and making it so may have side effects.
if use_floats:
    kt = 1e6
    Mt = 1e9
else:
    kt = ScalarUnit(1e6, "M", "kg")
    units.kt = kt

    Mt = ScalarUnit(1e9, "M", "kg")
    units.Mt = Mt

# Semantic overloading: we reuse the "amount" dimension to mean "value"

if use_floats:
    USD = 1
    VND = USD / 22270
else:
    VND = ScalarUnit(1 / 22270, "N", "mol", prefixable=True)
    units.VND = VND

    USD = ScalarUnit(1, "N", "mol", prefixable=True)
    units.USD = USD

kUSD = 1000 * USD
MUSD = 1000 * kUSD


# Full Time Equivalent, a work time unit amounting to "1 job".
FTE = 1560 * hr
units.FTE = FTE


TIME_HORIZON = 20

ONES = ones(TIME_HORIZON + 1)


def npv(values, rate, length=TIME_HORIZON):
    """Net present value of an array-like cash flow.

    Includes investment in period 0 and the subsequent 'length' values.
    Cut and pasted here to avoid warnings because numpy moved it to numpy-financial.
    """
    assert length <= len(values), "NPV called with time horizon larger than array"
    assert length in (10, 20), "Catch off by one error in testing phase"
    mask = [1] + [1] * length + [0] * (len(values) - length - 1)
    values = asarray(values) * mask
    return (values / (1 + rate) ** arange(0, len(values))).sum(axis=0)


def after_invest(qty, time_horizon=TIME_HORIZON):
    """Construct a time serie from a quantity.

    Used to vectorize calculations involving qty.
    Assumes invest completes in the first year.
    Return  natu.numpy.array([0 * qty, qty, ..., qty]) so that the 0 has correct unit.

    >>> import pytest
    >>> if use_floats:
    ...     pytest.skip('after_invest doctests uses quantities.')
    >>> after_invest(3 * t, 20)
    array([0 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t,
           3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t, 3 t], dtype=object)
    """
    assert not hasattr(qty, "__iter__"), "Vectorize only scalar arguments."
    data_type = float if use_floats else object
    return array([0 * qty] + [qty] * time_horizon, dtype=data_type)


def year_1(df):
    """Replace the vector [a, b, b, b, .., b] by the quantity  b per year, in a dataframe.

    Object  y  denotes the unit symbol for "year".
    This assumes that investment occured in period 0, then steady state from period 1 onwards.
    """

    def projector(vector):
        scalar = vector[1]
        assert list(vector)[1:] == [scalar] * (len(vector) - 1)
        return scalar / y

    return df.applymap(projector).T


def summarize(sequence, discount_rate):
    """Summarize a sequence, verify it is a steady state.

    Return first element, second element, and NPV of everything.
    """
    is_constant = len(unique(sequence[1:])) == 1
    assert is_constant, "Error: expecting everything constant after first year."
    return sequence[0], sequence[1], npv(sequence, discount_rate)


def display_as(qty, unit):
    """Set the display_unit of qty or of qty's items to 'unit' and return qty.

    This function is more robust than using  qty.display_unit =  in the code directly,
    because when  use_quantities = False  it is transparent instead of producing an error

    >>> import pytest
    >>> if use_floats:
    ...     pytest.skip('This doctests uses units.')
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
    if not use_floats:
        if hasattr(qty, "__iter__"):
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

    This version works with natu quantities.
    The versions in standard library math or even in natu.math package do not (bug in natu ?)
    Absolute tolerance can be ommited, but if provided must have the correct dimension
    >>> isclose(0 * VND, 0 * USD)
    True
    >>> isclose(.1 * t+ .1 * t + .1 * t, .3 * t, abs_tol = 0 * t)
    True
    """
    return abs(qty_a - qty_b) <= max(rel_tol * max(abs(qty_a), abs(qty_b)), abs_tol)


def isclose_all(qty_a, qty_b, rel_tol=1e-09, abs_tol=0.0):
    """Compare two lists of numbers or quantities for almost-equality according to PEP 485.

    It needs the corectly dimensioned abs_tol:
    >>> isclose_all([1 * t, 2 * t], [3/3 * t, 2*t], abs_tol = 0 *t)
    True
    """
    return all(isclose(a, b, rel_tol, abs_tol) for a, b in zip(qty_a, qty_b))


def safe_divide(costs, masses):
    """Divide two vectors elementwise, producing NaN instead of error when the divisor is zero.

    >>> import pytest
    >>> if use_floats:
    ...     pytest.skip('This doctests uses units.')
    >>> import natu.numpy as np
    >>> costs = array([100 * USD, 200 * USD])
    >>> masses = array([0 * t, 10 * t])

    >>> safe_divide(costs, masses)
    array([nan USD/t, 20 USD/t], dtype=object)

    >>> costs / masses
    Traceback (most recent call last):
     ...
    ZeroDivisionError: float division by zero
    """
    result = costs.copy()
    for i, mass in enumerate(masses):
        # More pythonic, but pytest gives a warning
        # try:
        #     result[i] /= mass
        # except ZeroDivisionError:
        #     result[i] = display_as(float('NaN') * USD / t, 'USD/t')
        if use_floats:
            if mass != 0:
                result[i] /= mass
            else:
                result[i] = display_as(float("NaN") * USD / t, "USD/t")
        else:
            if mass.__nonzero__():
                result[i] /= mass
            else:
                result[i] = display_as(float("NaN") * USD / t, "USD/t")

    return display_as(result, "USD/t")


def solve_linear(f, x0, x1):
    """Solve equation f(x) == 0, where f is linear, given two points x0 and x1.

    The solution of  a x + b == 0  is  x = - b / a
    This is trivial, but the function is useful when  f  is a black box.
    If f is not linear, computes where the secant at x0 and x1 intersects the horizontal axis.

    >>> solve_linear(lambda x: 2 * x + 4, 0, 1)
    -2.0
    """
    assert not isclose(x1, x0), "Starting points are too close."
    y0 = f(x0)  # y0 = a x0 + b
    y1 = f(x1)  # y1 = a x1 + b
    a = (y1 - y0) / (x1 - x0)
    b = y0 - a * x0
    return -b / a
