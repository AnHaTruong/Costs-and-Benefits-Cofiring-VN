# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from unitsdef import *

class PowerPlant:

    def __init__(self, capacity, capacity_factor, commissioning,
                 boiler_technology, coal_heat_value, base_plant_efficiency):
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.power_generation = capacity * capacity_factor * time_step
        self.elec_sale = self.power_generation
        self.coal_heat_value = coal_heat_value
        self.base_plant_efficiency = base_plant_efficiency
        self.base_coal_consumption = capacity * capacity_factor / base_plant_efficiency / coal_heat_value


MongDuong1 = PowerPlant(capacity=1080 * MW,
                        capacity_factor=0.60,
                        commissioning = 2015 * y,
                        boiler_technology = 'CFB',
                        coal_heat_value = 19.43468 * MJ / kg,
                        base_plant_efficiency = 38.84 / 100)

MongDuong1.base_boiler_efficiency = 87.03 / 100

MongDuong1.capital_cost = 50 * USD / kW
MongDuong1.coal_price = 1131400 * VND / t
MongDuong1.fix_om_cost = 32.24 * USD / kW / y
MongDuong1.variable_om_cost = 0.006 * USD / (kW*hr)
MongDuong1.fix_om_coal = 29.31 * USD / kW / y
MongDuong1.variable_om_coal = 0.0048 * USD / (kW*hr)
MongDuong1.coal_transport_distance = 0 * km
MongDuong1.biomass_yield = 5.605 * t / ha / y
MongDuong1.electricity_tariff = 1239.17 * VND / (kW*hr)

MongDuong1.small_radius = 50 * km # Distance from the plant to the boder of Quang Ninh with adjacent provinces
MongDuong1.bm_density_1 = 5.49 * t / (km**2) / y # Straw density in Quang Ninh
MongDuong1.bm_density_2 = 60.38 * t / (km**2) / y # Straw density in adjacent provinces

MongDuong1.ef_coal_combust = 0.0966 * kg / MJ
MongDuong1.ef_coal_transport = 0 * kg / t / km # asumming conveyor transport emission factor = 0
MongDuong1.ef_biomass_combust = 0.0858 * kg / MJ
MongDuong1.ef_biomass_transport = 0.110 * kg / t / km # biomass transported by truck

MongDuong1.esp_efficiency = 0.996
MongDuong1.desulfur_efficiency = 0.982
MongDuong1.ef_so2_coal = 11.5 * kg / t
MongDuong1.ef_pm10_coal = 43.8 * kg / t
MongDuong1.ef_nox_coal = 18 * kg / t

NinhBinh = PowerPlant(capacity=100 * MW,
                      capacity_factor=0.64,
                      commissioning=1974,
                      boiler_technology='PC',
                      coal_heat_value = 21.5476 * MJ / kg,
                      base_plant_efficiency = 21.77 / 100)

NinhBinh.base_boiler_efficiency = 81.61 / 100

NinhBinh.capital_cost = 100 * USD / kW
NinhBinh.coal_price = 1825730 * VND / t
NinhBinh.fix_om_cost = 32.24 * USD / kW / y
NinhBinh.variable_om_cost = 0.006 * USD / (kW*hr)
NinhBinh.fix_om_coal = 29.31 * USD / kW / y
NinhBinh.variable_om_coal = 0.0048 * USD / (kW*hr)
NinhBinh.electricity_tariff = 1665.6 * VND / (kW * hr)

NinhBinh.coal_transport_distance = 200 * km
NinhBinh.biomass_yield = 5.7 * t / ha / y
#NinhBinh.bm_density = 68.67 * t / (km**2) / y

NinhBinh.ef_coal_combust = 0.0966 * kg / MJ
NinhBinh.ef_coal_transport = 0.071 * kg / t / km # coal transported by barge
NinhBinh.ef_biomass_combust = 0.0858 * kg / MJ
NinhBinh.ef_biomass_transport = 0.110 * kg / t / km # biomass transported by truck

NinhBinh.esp_efficiency = 0.992
NinhBinh.desulfur_efficiency = 0
NinhBinh.ef_so2_coal = 11.5 * kg / t
NinhBinh.ef_pm10_coal = 26.1 * kg / t
NinhBinh.ef_nox_coal = 18 * kg / t