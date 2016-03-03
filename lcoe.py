# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity(LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""LCOE assessment of a co-firing project"""

from parameters import cap_rec_factor
from parameters import biomass_heat_value, h_per_yr
from parameters import NinhBinh, MongDuong1


def bm_unit_cost_mj(plant):
    """calculate the biomass unit cost per 1 MJ of heat"""
    return plant.biomass_unit_cost /biomass_heat_value 


def lcoe(plant):
    """calcuate the levelized cost of electricity for co-firing project"""
    return (plant.capital_cost * cap_rec_factor + plant.fix_om_cost)\
           / h_per_yr / plant.capacity_factor \
           + bm_unit_cost_mj(plant) * plant.heat_rate \
           + plant.variable_om_cost\

print("capacity recovery factor", cap_rec_factor)

print("Biomass unit cost per MJ Mong Duong1 = ", bm_unit_cost_mj(MongDuong1))

print("Levelized cost of electricity Mong Duong1 = ", lcoe(MongDuong1), "USD/kWh")

print("Biomass unit cost per MJ Ninh Binh = ", bm_unit_cost_mj(NinhBinh))

print("Levelized cost of electricity Ninh Binh = ", lcoe(NinhBinh), "USD/kWh")

print(MongDuong1.biomass_unit_cost)
print(NinhBinh.biomass_unit_cost)
print(biomass_heat_value)
