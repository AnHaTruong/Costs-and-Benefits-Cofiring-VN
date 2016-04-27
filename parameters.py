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

h_per_yr = 8760 * ureg.hour # Number of hour per yr
biomass_heat_value = 11.7 * ureg.MJ / ureg.kg
biomass_ratio = 0.05    # Percent of energy that comes from biomass
                        # energy meaning both heat and electricity produced

winder_capacity = 6.57 * ureg.t / ureg.day
work_hour_day = 8 * ureg.hour / ureg.day
FTE = 1560 * ureg.hour / ureg.year  # number of working hour for a FTE job                                   # a full time equivalence job
truck_velocity = 45 * ureg.km / ureg.hour
truck_load = 20 * ureg.t
OM_hour_MWh = 0.12 * ureg.hour / ureg.MWh # working hour for OM per MWh                                                   # O&M of co-firing per MWh
time_step = 1 * ureg.year
time_horizon = 20
discount_rate = 0.087771 * time_step / ureg.year
tax_rate = 0.25  # Corporate tax in Vietnam
electricity_tariff = 1158.1 * ureg.VND / ureg.kWh
biomass_fix_cost = 37.26 * ureg.USD / ureg.t

# wage per hour is calculated from base salary defined in gorvenmental regulations
wage_bm_collect = 1.11 * ureg.USD / ureg.hour
wage_bm_transport = 1.11 * ureg.USD / ureg.hour
wage_operation_maintenance = 1.67 * ureg.USD / ureg.hour
winder_rental_cost = 40 * ureg.USD / ureg.ha

ef_so2_biomass = 0.18 * ureg.g / ureg.kg
ef_pm10_biomass = 9.1 * ureg.g / ureg.kg
ef_nox_biomass = 2.28 * ureg.g / ureg.kg

health_damage_so2 = 3767 * ureg.USD / ureg.t
health_damage_pm10 = 5883 * ureg.USD / ureg.t
health_damage_nox = 286 * ureg.USD / ureg.t

zero_kwh = 0 * ureg.kWh
zero_USD = 0 * ureg.USD
zero_VND = 0 * ureg.VND


class PowerPlant:
    pass

MongDuong1 = PowerPlant()

MongDuong1.commissioning = 2015 * ureg.year
MongDuong1.boiler_technology = 'CFB'
MongDuong1.capacity = 1080 * ureg.MW
MongDuong1.generation = 6500 * ureg.GWh / ureg.year
MongDuong1.coal_heat_value = 19.4 * ureg.MJ / ureg.kg
MongDuong1.base_coal_consumption = 2.75 * ureg.Mt / ureg.year
MongDuong1.base_plant_efficiency = 38.84 / 100
MongDuong1.base_boiler_efficiency = 87.03 / 100

MongDuong1.capital_cost = 50 * ureg.USD / ureg.kW
MongDuong1.coal_price = 52.69 * ureg.USD / ureg.t
MongDuong1.fix_om_cost = 32.24 * ureg.USD / ureg.kW / ureg.year
MongDuong1.variable_om_cost = 0.006 * ureg.USD / ureg.kWh
# Computed separately. Assumes 5% co-firing
MongDuong1.biomass_required = 259107.274137779 * ureg.t / ureg.year
MongDuong1.biomass_unit_cost = 41.311153541657 * ureg.USD / ureg.t
MongDuong1.heat_rate = 9.32786896004 * ureg.MJ / ureg.kWh
MongDuong1.capacity_factor = 0.68704549298157
MongDuong1.collection_radius = 70.7431601125762 * ureg.km
MongDuong1.coal_saved = 155986.88053583 * ureg.t / ureg.year
MongDuong1.coal_transport_distance = 0 * ureg.km
MongDuong1.coal_heat_value = 19.43468 * ureg.MJ / ureg.kg
MongDuong1.biomass_yeild = 5.605 * ureg.t / ureg.ha / ureg.year
# rice cultivation area needed to supply straw for co-firing in the plant
MongDuong1.rice_cultivation_area = 46228 * ureg.ha

MongDuong1.ef_coal_combust = 0.0966 * ureg.kg / ureg.MJ
MongDuong1.ef_coal_transport = 0 * ureg.kg / ureg.t / ureg.km
MongDuong1.ef_biomass_combust = 0.0858 * ureg.kg / ureg.MJ
MongDuong1.ef_biomass_transport = 0.062 * ureg.kg / ureg.t / ureg.km

MongDuong1.esp_efficiency = 0.996
MongDuong1.desulfur_efficiency = 0.982
MongDuong1.ef_so2_coal = 11.5 * ureg.kg / ureg.t
MongDuong1.ef_pm10_coal = 43.8 * ureg.kg / ureg.t
MongDuong1.ef_nox_coal = 18 * ureg.kg / ureg.t

NinhBinh = PowerPlant()

NinhBinh.commissioning = 1974
NinhBinh.boiler_technology = 'PC'
NinhBinh.capacity = 100 * ureg.MW
NinhBinh.generation = 750 * ureg.GWh / ureg.year
NinhBinh.coal_heat_value = 25.3 * ureg.MJ / ureg.kg
NinhBinh.base_coal_consumption = 0.42 * ureg.Mt / ureg.year
NinhBinh.base_plant_efficiency = 21.77 / 100
NinhBinh.base_boiler_efficiency = 81.61 / 100


NinhBinh.capital_cost = 100 * ureg.USD / ureg.kW
NinhBinh.coal_price = 83.83 * ureg.USD / ureg.t
NinhBinh.fix_om_cost = 32.24 * ureg.USD / ureg.kW / ureg.year
NinhBinh.variable_om_cost = 0.006 * ureg.USD / ureg.kWh
# Computed separately. Assumes 5% co-firing
NinhBinh.biomass_required = 53362.0062849769 * ureg.t / ureg.year
NinhBinh.biomass_unit_cost = 38.154337591058 * ureg.USD / ureg.t
NinhBinh.heat_rate = 16.6489459609128 * ureg.MJ / ureg.kWh
NinhBinh.capacity_factor = 0.85616438356164
NinhBinh.collection_radius = 15.7274063201183 * ureg.km
NinhBinh.coal_saved = 24664.423049406 * ureg.t / ureg.year
NinhBinh.coal_transport_distance = 200 * ureg.km
NinhBinh.coal_heat_value = 25.3132 * ureg.MJ / ureg.kg
NinhBinh.biomass_yeild = 5.7 * ureg.t / ureg.ha / ureg.year
# rice cultivation area needed to supply straw for co-firing in the plant
NinhBinh.rice_cultivation_area = 9362 * ureg.ha

NinhBinh.ef_coal_combust = 0.0966 * ureg.kg / ureg.MJ
NinhBinh.ef_coal_transport = 0.031 * ureg.kg / ureg.t / ureg.km
NinhBinh.ef_biomass_combust = 0.0858 * ureg.kg / ureg.MJ
NinhBinh.ef_biomass_transport = 0.062 * ureg.kg / ureg.t / ureg.km

NinhBinh.esp_efficiency = 0.992
NinhBinh.desulfur_efficiency = 0
NinhBinh.ef_so2_coal = 11.5 * ureg.kg / ureg.t
NinhBinh.ef_pm10_coal = 26.1 * ureg.kg / ureg.t
NinhBinh.ef_nox_coal = 18 * ureg.kg / ureg.t
