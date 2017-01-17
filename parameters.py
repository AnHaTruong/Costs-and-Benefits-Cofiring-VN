# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

from natu.units import km, ha
from natu.units import g, kg, t
from natu.units import hr, d, y
from natu.units import MJ
from natu.units import kW, MW, GW

### Semantic overloading
### We reuse the "amount" dimension to mean "value"
from natu.units import mol
from natu.core import ScalarUnit
from natu import units
VND = ScalarUnit(1, 'N', 'mol', prefixable=True)
units.VND = VND

USD = ScalarUnit(22270, 'N', 'mol', prefixable=True)
units.USD = USD

"""Input parameters of the model"""

h_per_yr = 8760 * hr # Number of hour per year
biomass_heat_value = 11.7 * MJ / kg
biomass_ratio = 0.05   # Percent of energy that comes from biomass
                        # energy meaning both heat and electricity produced
straw_collection_fraction = 0.82
straw_selling_proportion = 0.79
RPR_straw = 1.0
straw_burn_rate = 0.9 # Percentage of straw burned infield after harvest
winder_capacity = 6.57 * t / d
work_hour_day = 8 * hr / d
FTE = 1560 * hr / y  # number of working hour for a FTE job # a full time equivalence job
truck_velocity = 45 * km / hr
truck_load = 20 * t
OM_hour_MWh = 0.12 * hr / MW / hr # working hour for OM per MWh    # O&M of co-firing per MWh
time_step = 1 * y
time_horizon = 20
discount_rate = 0.087771 * time_step / y
depreciation_period = 10
tax_rate = 0.25  # Corporate tax in Vietnam
biomass_fix_cost = 37.26 * USD / t
transport_tariff = 2000 * VND/t/km # vantaiduongviet.com
tortuosity_factor = 1.5
# wage per hour is calculated from base salary defined in gorvenmental regulations
wage_bm_collect = 1.11 * USD / hr
wage_bm_transport = 1.11 * USD / hr
wage_operation_maintenance = 1.67 * USD / hr
winder_rental_cost = 40 * USD / ha

ef_so2_biomass = 0.18 * g / kg
ef_pm10_biomass = 9.1 * g / kg
ef_nox_biomass = 2.28 * g / kg
carbon_price = 1 * USD / t
coal_import_price = 73 * USD / t

health_damage_so2 = 3767 * USD / t
health_damage_pm10 = 5883 * USD / t
health_damage_nox = 286 * USD / t

zero_kwh = 0 * kW*hr
zero_USD = 0 * USD
zero_VND = 0 * VND
zero_km = 0 * km

class PowerPlant:
    pass

MongDuong1 = PowerPlant()

MongDuong1.commissioning = 2015 * y
MongDuong1.boiler_technology = 'CFB'
MongDuong1.capacity = 1080 * MW
# MongDuong1.generation = 6500 * GW * hr / y
MongDuong1.capacity_factor = 0.60
# MongDuong1.base_coal_consumption = 2751600 * t / y
MongDuong1.base_plant_efficiency = 38.84 / 100
MongDuong1.base_boiler_efficiency = 87.03 / 100

MongDuong1.capital_cost = 50 * USD / kW
MongDuong1.coal_price = 1131400 * VND / t
MongDuong1.fix_om_cost = 32.24 * USD / kW / y
MongDuong1.variable_om_cost = 0.006 * USD / (kW*hr)
MongDuong1.fix_om_coal = 29.31 * USD / kW / y
MongDuong1.variable_om_coal = 0.0048 * USD / (kW*hr)
MongDuong1.coal_transport_distance = 0 * km
MongDuong1.coal_heat_value = 19.43468 * MJ / kg
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

NinhBinh = PowerPlant()

NinhBinh.commissioning = 1974
NinhBinh.boiler_technology = 'PC'
NinhBinh.capacity = 100 * MW
# NinhBinh.generation = 560 * GW * hr / y
NinhBinh.capacity_factor = 0.64
# NinhBinh.base_coal_consumption = 420000 * t / y
NinhBinh.base_plant_efficiency = 21.77 / 100
NinhBinh.base_boiler_efficiency = 81.61 / 100

NinhBinh.capital_cost = 100 * USD / kW
NinhBinh.coal_price = 1825730 * VND / t
NinhBinh.fix_om_cost = 32.24 * USD / kW / y
NinhBinh.variable_om_cost = 0.006 * USD / (kW*hr)
NinhBinh.fix_om_coal = 29.31 * USD / kW / y
NinhBinh.variable_om_coal = 0.0048 * USD / (kW*hr)
NinhBinh.electricity_tariff = 1665.6 * VND / (kW * hr)

NinhBinh.coal_transport_distance = 200 * km
NinhBinh.coal_heat_value = 21.5476 * MJ / kg
NinhBinh.biomass_yield = 5.7 * t / ha / y
NinhBinh.bm_density = 68.67 * t / (km**2) / y

NinhBinh.ef_coal_combust = 0.0966 * kg / MJ
NinhBinh.ef_coal_transport = 0.071 * kg / t / km # coal transported by barge
NinhBinh.ef_biomass_combust = 0.0858 * kg / MJ
NinhBinh.ef_biomass_transport = 0.110 * kg / t / km # biomass transported by truck

NinhBinh.esp_efficiency = 0.992
NinhBinh.desulfur_efficiency = 0
NinhBinh.ef_so2_coal = 11.5 * kg / t
NinhBinh.ef_pm10_coal = 26.1 * kg / t
NinhBinh.ef_nox_coal = 18 * kg / t


