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
from job import number_of_truck_trips, transport_time, benefit_bm_transport
from job import om_work, cofiring_work, benefit_om, total_job_benefit
from parameters import FTE

print('')

row = '{:40}' + '{:25.1f}'


def print_job(plant, cofiringplant):

    row1 = benefit_bm_collection(cofiringplant)
    row2 = benefit_bm_transport(cofiringplant)
    row3 = benefit_om(plant)
    row4 = total_job_benefit(plant, cofiringplant)
    row5 = number_of_truck_trips(cofiringplant)
    row6 = transport_time(cofiringplant)

    row1.display_unit = 'USD'
    row2.display_unit = 'USD'
    row3.display_unit = 'USD'
    row4.display_unit = 'USD'
    row6.display_unit = 'hr'

    print(row.format('Transportation time', row6))

    print(row.format('Truck trips', row5))

    print(row.format('Work for biomass collection',
                     bm_collection_work(cofiringplant)
                     )
          )

    print(row.format('Work for biomass transportation',
                     bm_transport_work(cofiringplant)
                     )
          )

    print(row.format('Work for O&M', om_work(plant)))

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

    print(row.format('Job benefit from biomass collection', row1))

    print(row.format('Job benefit from biomass transportation', row2))

    print(row.format('Job benefit from co-firing O&M', row3))

    print(row.format('Total job benefit from co-firing', row4))


print('')
print('Benefit from job creation Mong Duong 1')
print('')
print_job(MongDuong1, MongDuong1Cofire)

print('')
print('Benefit from job creation Ninh Binh')
print('')
print_job(NinhBinh, NinhBinhCofire)
