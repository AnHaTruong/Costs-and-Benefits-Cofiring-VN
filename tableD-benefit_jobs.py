# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print table D for job created from co-firing in job.py
"""

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire

from job import bm_collection_work, bm_transport_work, benefit_bm_collection
from job import number_of_truck, transport_time, benefit_bm_transport
from job import om_work, cofiring_work, benefit_om, total_job_benefit
from parameters import FTE
from init import h_per_yr

print('')

row = '{:40}' + '{:25.1f}'


def print_job(plant, cofiringplant):

    col1 = benefit_bm_collection(cofiringplant)
    col2 = benefit_bm_transport(cofiringplant)
    col3 = benefit_om(plant)
    col4 = total_job_benefit(plant, cofiringplant)
    col5 = number_of_truck(cofiringplant)
    col6 = transport_time(cofiringplant)

    col1.display_unit = 'USD/y'
    col2.display_unit = 'USD/y'
    col3.display_unit = 'USD/y'
    col4.display_unit = 'USD/y'
    col5.display_unit = '1/y'
    col6.display_unit = 'hr'

    print(row.format('transportation time', col6))

    print(row.format('number of truck', col5))

    print(row.format('total hour for biomass collection',
                     bm_collection_work(cofiringplant) * h_per_yr
                     )
          )

    print(row.format('total hour for biomass transportation',
                     bm_transport_work(cofiringplant) * h_per_yr
                     )
          )

    print(row.format('total hour for O&M', om_work(plant) * h_per_yr))

    print(row.format('FTE job from biomass collection',
                     bm_collection_work(cofiringplant) / FTE
                     )
          )

    print(row.format('FTE job from biomass transportation',
                     bm_transport_work(cofiringplant) / FTE
                     )
          )

    print(row.format('FTE job from co-firing O&M', om_work(plant) / FTE))

    print(row.format('Total FTE job', cofiring_work(plant, cofiringplant) / FTE))

    print(row.format('Job benefit from biomass collection', col1))

    print(row.format('Job benefit from biomass transportation', col2))

    print(row.format('Job benefit from co-firing O&M', col3))

    print(row.format('Total job benefit from co-firing', col4))


print('')
print('Benefit from job creation Mong Duong 1')
print('')
print_job(MongDuong1, MongDuong1Cofire)

print('')
print('Benefit from job creation Ninh Binh')
print('')
print_job(NinhBinh, NinhBinhCofire)
