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

from job import bm_collection_work, bm_transport_work, benefit_bm_collection
from job import number_of_truck, transport_time, benefit_bm_transport
from job import om_work, cofiring_work, benefit_om, total_job_benefit
from parameters import FTE, h_per_yr

print('')

row = '{:40}' + '{:25.1f}'

def print_job(plant):
    
    col1 = benefit_bm_collection(plant)
    col2 = benefit_bm_transport(plant)
    col3 = benefit_om(plant)
    col4 = total_job_benefit(plant)
    
    col1.display_unit = 'USD/y'
    col2.display_unit = 'USD/y'
    col3.display_unit = 'USD/y'
    col4.display_unit = 'USD/y'
    
    print(row.format('transportation time', transport_time(plant)))
         
    print(row.format('number of truck', number_of_truck(plant)))         
  
    print(row.format('total hour for biomass collection',
                     bm_collection_work(plant) * h_per_yr
                    )
         )

    print(row.format('total hour for biomass transportation',
                     bm_transport_work(plant) * h_per_yr
                    )
         )

    print(row.format('total hour for O&M', om_work(plant) * h_per_yr))
      
    print(row.format('FTE job from biomass collection',
                     bm_collection_work(plant) / FTE
                    )
         )
      
    print(row.format('FTE job from biomass transportation',
                     bm_transport_work(plant) / FTE
                    )
         )

    print(row.format('FTE job from co-firing O&M', om_work(plant) / FTE))
                  
    print(row.format('Total FTE job', cofiring_work(plant) / FTE))
                  
    print(row.format('Job benefit from biomass collection', col1))
   
    print(row.format('Job benefit from biomass transportation', col2))
    
    print(row.format('Job benefit from co-firing O&M', col3))

    print(row.format('Total job benefit from co-firing', col4))


print('')
print('Benefit from job creation Mong Duong 1')
print('')
print_job(MongDuong1)

print('')
print('Benefit from job creation Ninh Binh')
print('')
print_job(NinhBinh)
