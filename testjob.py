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

from job import bm_collection_work, bm_transport_work
from job import bm_transport_work, number_of_truck, transport_time 
from job import om_work, cofiring_work
from parameters import FTE

print('')
head = '{:38}' + '{:18}' + '{:15}'
row = '{:35}' + '{:15.5f}'*2

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
                  bm_collection_work(MongDuong1),
                  bm_collection_work(NinhBinh)
                  )
      )

print (row.format('total hour for biomass transportation',
                  bm_transport_work(MongDuong1),
                  bm_transport_work(NinhBinh)
                  )
      )

print (row.format('total hour for O&M',
                  om_work(MongDuong1),
                  om_work(NinhBinh)
                  )
      )
      
print (row.format('FTE job from biomass collection',
                  bm_collection_work(MongDuong1) / FTE,
                  bm_collection_work(NinhBinh) / FTE
                  )
      )
      
print (row.format('FTE job from biomass transportation',
                  bm_transport_work(MongDuong1) / FTE,
                  bm_transport_work(NinhBinh) / FTE
                  )
      )

print (row.format('FTE job from co-firing O&M',
                  om_work(MongDuong1) / FTE,
                  om_work(NinhBinh) / FTE
                  )
      )

print (row.format('Total FTE job',
                  cofiring_work(MongDuong1) / FTE,
                  cofiring_work(NinhBinh) / FTE
                  )
      )
