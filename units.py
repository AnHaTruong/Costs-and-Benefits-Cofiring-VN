# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

from natu.units import km, ha
from natu.units import g, kg, t
from natu.units import hr, d, y
from natu.units import MJ
from natu.units import kW, MW, GW

### Semantic overloading
### We reuse the "amount" dimension to mean "value"
from natu.units import mol
from natu.core import ScalarUnit
from natu import units
VND = ScalarUnit(1, 'N', 'mol', prefixable=True)
units.VND = VND

USD = ScalarUnit(22270, 'N', 'mol', prefixable=True)
units.USD = USD
time_step = 1 * y
time_horizon = 20
h_per_yr = 8760 * hr  # Number of hour per year

zero_kwh = 0 * kW*hr
zero_USD = 0 * USD
zero_VND = 0 * VND
zero_km = 0 * km
