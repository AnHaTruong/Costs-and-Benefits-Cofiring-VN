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
from health import *
import numpy as np

from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from natu.units import t, y


value1 = ([so2_emission_field_base(MongDuong1) / t * y,
           so2_emission_field_cofire(MongDuong1, MongDuong1Cofire) / t * y,
           so2_emission_plant_base(MongDuong1) / t * y,
           so2_emission_plant_cofire(MongDuong1, MongDuong1Cofire) / t * y
          ])

print(value1)

value2 = ([so2_emission_field_base(NinhBinh) / t * y,
           so2_emission_field_cofire(NinhBinh, NinhBinhCofire) / t * y,
           so2_emission_plant_base(NinhBinh) / t * y,
           so2_emission_plant_cofire(NinhBinh, NinhBinhCofire) / t * y
          ])
print(value2)

value3 = ([pm10_emission_field_base(MongDuong1) / t * y,
           pm10_emission_field_cofire(MongDuong1, MongDuong1Cofire) / t * y,
           pm10_emission_plant_base(MongDuong1) / t * y,
           pm10_emission_plant_cofire(MongDuong1, MongDuong1Cofire) / t * y
          ])
print(value3)

value4 = ([pm10_emission_field_base(NinhBinh) / t * y,
           pm10_emission_field_cofire(NinhBinh, NinhBinhCofire) / t * y,
           pm10_emission_plant_base(NinhBinh) / t * y,
           pm10_emission_plant_cofire(NinhBinh, NinhBinhCofire) / t * y
          ])
print(value4)

value5 = ([nox_emission_field_base(MongDuong1) / t * y,
           nox_emission_field_cofire(MongDuong1, MongDuong1Cofire) / t * y,
           nox_emission_plant_base(MongDuong1) / t * y,
           nox_emission_plant_cofire(MongDuong1, MongDuong1Cofire) / t * y
          ])
print(value5)

value6 = ([nox_emission_field_base(NinhBinh) / t * y,
           nox_emission_field_cofire(NinhBinh, NinhBinhCofire) / t * y,
           nox_emission_plant_base(NinhBinh) / t * y,
           nox_emission_plant_cofire(NinhBinh, NinhBinhCofire) / t * y
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
