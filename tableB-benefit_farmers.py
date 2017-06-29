# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

from init import display_as

from parameters import MongDuong1Cofire, NinhBinhCofire
from parameters import winder_rental_cost, straw
from parameters import work_hour_day, winder_haul, wage_bm_collect, truck_load, wage_bm_loading
from parameters import truck_velocity, wage_bm_transport, truck_loading_time

display_as(winder_rental_cost, 'USD/ha')


def print_income(supply_chain):
    area = supply_chain.farm_area()[1]
    revenue = supply_chain.cost(straw.price)[1]
    collect_cost = supply_chain.farm_wages(work_hour_day,
                                           winder_haul,
                                           wage_bm_collect)[1]
    loading_cost = supply_chain.loading_wages(truck_loading_time,
                                              wage_bm_loading)[1]
    transport_cost = supply_chain.transport_wages(truck_load,
                                                  truck_velocity,
                                                  wage_bm_transport)[1]
    winder_cost = winder_rental_cost * area

    total = supply_chain.farm_profit(straw.price,
                                     work_hour_day,
                                     winder_haul,
                                     wage_bm_collect,
                                     truck_loading_time,
                                     wage_bm_loading,
                                     truck_load,
                                     truck_velocity,
                                     wage_bm_transport,
                                     winder_rental_cost)[1]

    row = '{:20}' + '{:10.2f}' + '{:10.0f}'
    print(total)
    print('{:27}{:15}{:4}{:5.0f}'.format('', 'Per ha', 'For', area))
    print(row.format('Straw sales revenue', display_as(revenue / area, 'USD/ha'), revenue))
    print(row.format('- Collection cost', display_as(collect_cost / area, 'USD/ha'), collect_cost))
    print(row.format('- Hauling cost', display_as(loading_cost / area, 'USD/ha'), loading_cost))
    print(row.format('- Transport cost',
                     display_as(transport_cost / area, 'USD/ha'),
                     transport_cost))
    print(row.format('- Winder rental', winder_cost / area, display_as(winder_cost, 'kUSD')))
    print(row.format('= Net income', display_as(total / area, 'USD/ha'), total))
    print()

print('Extra net income for farmers around Mong Duong 1')
print_income(MongDuong1Cofire.straw_supply)

print('Extra net income for farmers around Ninh Binh')
print_income(NinhBinhCofire.straw_supply)
