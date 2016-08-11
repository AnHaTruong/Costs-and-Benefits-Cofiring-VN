print("Testing python package  natu ")

print("Offset units: what is 0 degC + 100 K")
from natu.units import degC, K
print("Should print 100.0 degC")
print(0*degC + 100*K)

print("Multiply by adding logarithms: what is (10/dB + 10/dB)*dB")
from natu.units import dB
print("Should print 100.0")
print((10/dB + 10/dB)*dB )

print("Prefixes: what is km/m")
from natu.units import km, m
print("Should print 1000")
print(km/m)

print("Coherent relations: what is 1*kg*m**2/s**2")
from natu.units import kg, m, s
print("Should print 1.0 J")
print(1*kg*m**2/s**2)

print("Constant: speed of light")
from natu.groups.constants import c
print("Should be 299792458.0 m/s")
print(c)

from natu.units import m
print(m)

l = 0.0254*m
print(l)

l.display_unit = 'inch'
print(l)

from natu.units import inch
print(l/inch)

print(km)

print("Temperatures are absolute, what is 25°C + 25°C")
print("Should be 323.15°C")
print(25*degC + 25*degC)
print("In Kelvins:")
print(25*degC / K)
print((25*degC + 25*degC)/K)

### New units
from natu.core import ScalarUnit
from natu.units import ns
shake = ScalarUnit.from_quantity(10*ns, 'shake')

from natu import units
units.shake = shake

time = 500*ns
time.display_unit = 'shake'
print(time)


### Define a new dimension : value
### Define two units : VND and USD
### Both are scalar, with a fixed ratio

print("")
print("-------------------")

from natu.units import km, ha
from natu.units import g, kg, t
from natu.units import hr, d, y
from natu.units import MJ, kWh, MWh, GWh
from natu.units import kW, MW

print(km.dimension)
print(ha.dimension)
print(kg.dimension)
print(hr.dimension)
print(MJ.dimension)
print(MW.dimension)

print("Dimensions not used in the model: angle A, current I, amount N, temperature Theta")

print("Let's semanticaly overload. We reuse the amount dimension to mean value")
from natu.core import ScalarUnit
VND = ScalarUnit(1, 'N', 'mol', prefixable=True)
USD = ScalarUnit(22000, 'N', 'mol', prefixable=True)

print(VND)
print(USD)

from natu import units
units.VND = VND
units.USD = USD

price = 100000*VND

print(price)

price.display_unit = 'VND'
print(price)

price.display_unit = 'USD'
print(price)