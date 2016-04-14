# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Tests for the calculation of number of job created from co-firing in job.py
"""

from parameters import MongDuong1, NinhBinh

from job import FTE_bm_collection, hour_bm_collection, FTE_bm_transport
from job import hour_bm_transport, number_of_truck, transport_time 
from job import FTE_OM, hour_om, total_FTE

print('')
head = '{:38}' + '{:18}' + '{:15}'
row = '{:35}' + '{:15.2f}'*2

print (head.format(' ', 'Mong Duong 1', 'Ninh Binh'))

print (row.format('transportation time',
                  transport_time(MongDuong1),
                  transport_time(NinhBinh)
                  )
      )

print (row.format('number of truck',
                  number_of_truck(MongDuong1),
                  number_of_truck(NinhBinh)
                  )
      )

print (row.format('total hour for biomass collection',
                  hour_bm_collection(MongDuong1),
                  hour_bm_collection(NinhBinh)
                  )
      )

print (row.format('total hour for biomass transportation',
                  hour_bm_transport(MongDuong1),
                  hour_bm_transport(NinhBinh)
                  )
      )

print (row.format('total hour for O&M',
                  hour_om(MongDuong1),
                  hour_om(NinhBinh)
                  )
      )
      
print (row.format('FTE job from biomass collection',
                  FTE_bm_collection(MongDuong1),
                  FTE_bm_collection(NinhBinh)
                  )
      )
      
print (row.format('FTE job from biomass transportation',
                  FTE_bm_transport(MongDuong1),
                  FTE_bm_transport(NinhBinh)
                  )
      )

print (row.format('FTE job from co-firing O&M',
                  FTE_OM(MongDuong1),
                  FTE_OM(NinhBinh)
                  )
      )

print (row.format('Total FTE job',
                  total_FTE(MongDuong1),
                  total_FTE(NinhBinh)
                  )
      )
