# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Input parameters of the model"""

from pint import UnitRegistry
ureg = UnitRegistry()

ureg.load_definitions('./unitdef.py')

h_per_yr = 8760 * ureg.hour # Number of hour per year
biomass_heat_value = 11.7 * ureg.megajoule / ureg.kilogram
biomass_ratio = 0.05    # Percent of energy that comes from biomass
                        # energy meaning both heat and electricity produced

winder_capacity = 6.57 * ureg.tonne / ureg.day
work_hour_day = 8 * ureg.hour / ureg.day
FTE = 1560 * ureg.hour / ureg.year
truck_velocity = 45 * ureg.kilometer
truck_load = 20 * ureg.tonne
OM_hour_MW = 0.12 * ureg.hour / ureg.megawatt
time_step = 1 * ureg.year
time_horizon = 20
discount_rate = 0.087771 * time_step / ureg.year
tax_rate = 0.25  # Corporate tax in Vietnam
electricity_tariff = 1158.1 * ureg.VND / ureg.kilowatthour

zero_kwh = 0 * ureg.kilowatthour
zero_USD = 0 * ureg.USD
zero_VND = 0 * ureg.VND


class PowerPlant:
    pass

MongDuong1 = PowerPlant()

MongDuong1.commissioning = 2015 * ureg.year
MongDuong1.boiler_technology = 'CFB'
MongDuong1.capacity = 1080 * ureg.megawatt
MongDuong1.generation = 6500 * ureg.gigawatthour / ureg.year
MongDuong1.coal_heat_value = 19.4 * ureg.megajoule / ureg.kilogram
MongDuong1.base_coal_consumption = 2.75 * ureg.megatonne / ureg.year
MongDuong1.base_plant_efficiency = 38.84 / 100
MongDuong1.base_boiler_efficiency = 87.03 / 100

MongDuong1.capital_cost = 50 * ureg.USD / ureg.kilowatt
MongDuong1.coal_price = 52.69 * ureg.USD / ureg.tonne
MongDuong1.fix_om_cost = 32.24 * ureg.USD / ureg.kilowatt / ureg.year
MongDuong1.variable_om_cost = 0.006 * ureg.USD / ureg.kilowatthour
# Computed separately. Assumes 5% co-firing
MongDuong1.biomass_required = 259107.274137779 * ureg.tonne / ureg.year
MongDuong1.biomass_unit_cost = 41.311153541657 * ureg.USD / ureg.tonne
MongDuong1.heat_rate = 9.32786896004 * ureg.megajoule / ureg.kilowatthour
MongDuong1.capacity_factor = 0.68704549298157
MongDuong1.collection_radius = 70.7431601125762 * ureg.kilometer
MongDuong1.coal_saved = 155986.88053583 * ureg.tonne / ureg.year
MongDuong1.coal_transport_distance = 0 * ureg.kilometer
MongDuong1.coal_heat_value = 19.43468 * ureg.megajoule / ureg.kilogram

MongDuong1.ef_coal_combust = 0.0966 * ureg.kilogram / ureg.megajoule
MongDuong1.ef_coal_transport = 0 * ureg.kilogram / ureg.tonne / ureg.kilometer
MongDuong1.ef_biomass_combust = 0.0858 * ureg.kilogram / ureg.megajoule
MongDuong1.ef_biomass_transport = 0.062 * ureg.kilogram / ureg.tonne / ureg.kilometer


NinhBinh = PowerPlant()

NinhBinh.commissioning = 1974
NinhBinh.boiler_technology = 'PC'
NinhBinh.capacity = 100 * ureg.megawatt
NinhBinh.generation = 750 * ureg.gigawatthour / ureg.year
NinhBinh.coal_heat_value = 25.3 * ureg.megajoule / ureg.kilogram
NinhBinh.base_coal_consumption = 0.42 * ureg.megatonne / ureg.year
NinhBinh.base_plant_efficiency = 21.77 / 100
NinhBinh.base_boiler_efficiency = 81.61 / 100


NinhBinh.capital_cost = 100 * ureg.USD / ureg.kilowatt
NinhBinh.coal_price = 83.83 * ureg.USD / ureg.tonne
NinhBinh.fix_om_cost = 32.24 * ureg.USD / ureg.kilowatt / ureg.year
NinhBinh.variable_om_cost = 0.006 * ureg.USD / ureg.kilowatthour
# Computed separately. Assumes 5% co-firing
NinhBinh.biomass_required = 53362.0062849769 * ureg.tonne / ureg.year
NinhBinh.biomass_unit_cost = 38.154337591058 * ureg.USD / ureg.tonne
NinhBinh.heat_rate = 16.6489459609128 * ureg.megajoule / ureg.kilowatthour
NinhBinh.capacity_factor = 0.85616438356164
NinhBinh.collection_radius = 15.7274063201183 * ureg.kilometer
NinhBinh.coal_saved = 24664.423049406 * ureg.tonne / ureg.year
NinhBinh.coal_transport_distance = 200 * ureg.kilometer
NinhBinh.coal_heat_value = 25.3132 * ureg.megajoule / ureg.kilogram

NinhBinh.ef_coal_combust = 0.0966 * ureg.kilogram / ureg.megajoule
NinhBinh.ef_coal_transport = 0.031 * ureg.kilogram / ureg.tonne / ureg.kilometer
NinhBinh.ef_biomass_combust = 0.0858 * ureg.kilogram / ureg.megajoule
NinhBinh.ef_biomass_transport = 0.062 * ureg.kilogram / ureg.tonne / ureg.kilometer
