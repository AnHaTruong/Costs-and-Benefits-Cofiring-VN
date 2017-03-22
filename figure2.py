# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Draw Figure 2 SO2 emission reduction and its benefit to public health
"""

import matplotlib.pyplot as plt
import numpy as np

from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from natu.units import t


value1 = ([MongDuong1Cofire.straw_supply.field_emission(MongDuong1Cofire.biomass_used[0])['Total']['SO2']/t,
           MongDuong1Cofire.straw_supply.field_emission(MongDuong1Cofire.biomass_used)['Total']['SO2']/t,
           MongDuong1.stack.emissions()['Total']['SO2'] / t,
           MongDuong1Cofire.stack.emissions()['Total']['SO2'] /t
           ])

print(value1)

value2 = ([NinhBinhCofire.straw_supply.field_emission(NinhBinhCofire.biomass_used[0])['Total']['SO2']/t,
           NinhBinhCofire.straw_supply.field_emission(NinhBinhCofire.biomass_used)['Total']['SO2']/t,
           NinhBinh.stack.emissions()['Total']['SO2'] / t,
           NinhBinhCofire.stack.emissions()['Total']['SO2'] / t
           ])
print(value2)

value3 = ([MongDuong1Cofire.straw_supply.field_emission(MongDuong1Cofire.biomass_used[0])['Total']['PM10']/t,
           MongDuong1Cofire.straw_supply.field_emission(MongDuong1Cofire.biomass_used)['Total']['PM10']/t,
           MongDuong1.stack.emissions()['Total']['PM10'] / t,
           MongDuong1Cofire.stack.emissions()['Total']['PM10'] / t
           ])
print(value3)

value4 = ([NinhBinhCofire.straw_supply.field_emission(NinhBinhCofire.biomass_used[0])['Total']['PM10']/t,
           NinhBinhCofire.straw_supply.field_emission(NinhBinhCofire.biomass_used)['Total']['PM10']/t,
           NinhBinh.stack.emissions()['Total']['PM10'] / t,
           NinhBinhCofire.stack.emissions()['Total']['PM10'] / t
           ])
print(value4)

value5 = ([MongDuong1Cofire.straw_supply.field_emission(MongDuong1Cofire.biomass_used[0])['Total']['NOx']/t,
           MongDuong1Cofire.straw_supply.field_emission(MongDuong1Cofire.biomass_used)['Total']['NOx']/t,
           MongDuong1.stack.emissions()['Total']['NOx'] / t,
           MongDuong1Cofire.stack.emissions()['Total']['NOx'] / t
           ])
print(value5)

value6 = ([NinhBinhCofire.straw_supply.field_emission(NinhBinhCofire.biomass_used[0])['Total']['NOx']/t,
           NinhBinhCofire.straw_supply.field_emission(NinhBinhCofire.biomass_used)['Total']['NOx']/t,
           NinhBinh.stack.emissions()['Total']['NOx'] / t,
           NinhBinhCofire.stack.emissions()['Total']['NOx'] / t
           ])
print(value6)

bw = 0.3
index = np.arange(4)
plt.axis([0, 4, 0, 600])
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])

plt.figure(1)
plt.title('SO2 emissions-Mong Duong 1')
plt.axis([0, 4, 0, 600])
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])
plt.ylabel('t/y')
plt.bar(index, value1, bw, color='b')

plt.figure(2)
plt.axis([0, 4, 0, 5000])
plt.title('SO2 emissions-Ninh Binh')
plt.ylabel('t/y')
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])
plt.bar(index, value2, bw, color='r')

plt.figure(3)
plt.title('PM10 emissions-Mong Duong 1')
plt.axis([0, 4, 0, 17000])
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])
plt.ylabel('t/y')
plt.bar(index, value3, bw, color='b')

plt.figure(4)
plt.axis([0, 4, 0, 4000])
plt.title('PM10 emissions-Ninh Binh')
plt.ylabel('t/y')
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])
plt.bar(index, value4, bw, color='r')

plt.figure(5)
plt.title('NOx emissions-Mong Duong 1')
plt.axis([0, 4, 0, 49000])
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])
plt.ylabel('t/y')
plt.bar(index, value5, bw, color='b')

plt.figure(6)
plt.axis([0, 4, 0, 8000])
plt.title('NOx emissions-Ninh Binh')
plt.ylabel('t/y')
plt.xticks(index, ['Field base', 'Field co-fire', 'Plant base', 'Plant co-fire'])
plt.bar(index, value6, bw, color='r')

plt.show()
