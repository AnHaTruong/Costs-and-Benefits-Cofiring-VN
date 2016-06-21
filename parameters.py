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

USD = ScalarUnit(21473, 'N', 'mol', prefixable=True)
units.USD = USD

"""Input parameters of the model"""

h_per_yr = 8760 * hr # Number of hour per year
biomass_heat_value = 11.7 * MJ / kg
biomass_ratio = 0.05    # Percent of energy that comes from biomass
                        # energy meaning both heat and electricity produced

winder_capacity = 6.57 * t / d
work_hour_day = 8 * hr / d
FTE = 1560 * hr / y  # number of working hour for a FTE job # a full time equivalence job
truck_velocity = 45 * km / hr
truck_load = 20 * t
OM_hour_MWh = 0.12 * hr / MW / hr # working hour for OM per MWh    # O&M of co-firing per MWh
time_step = 1 * y
time_horizon = 20
discount_rate = 0.087771 * time_step / y
tax_rate = 0.25  # Corporate tax in Vietnam
electricity_tariff = 1158.1 * VND / (kW * hr)
biomass_fix_cost = 37.26 * USD / t

# wage per hour is calculated from base salary defined in gorvenmental regulations
wage_bm_collect = 1.11 * USD / hr
wage_bm_transport = 1.11 * USD / hr
wage_operation_maintenance = 1.67 * USD / hr
winder_rental_cost = 40 * USD / ha

ef_so2_biomass = 0.18 * g / kg
ef_pm10_biomass = 9.1 * g / kg
ef_nox_biomass = 2.28 * g / kg

health_damage_so2 = 3767 * USD / t
health_damage_pm10 = 5883 * USD / t
health_damage_nox = 286 * USD / t

zero_kwh = 0 * kW*hr
zero_USD = 0 * USD
zero_VND = 0 * VND


class PowerPlant:
    pass

MongDuong1 = PowerPlant()

MongDuong1.commissioning = 2015 * y
MongDuong1.boiler_technology = 'CFB'
MongDuong1.capacity = 1080 * MW
MongDuong1.generation = 6500 * GW * hr / y
MongDuong1.coal_heat_value = 19.4 * MJ / kg
MongDuong1.base_coal_consumption = 2751600 * t / y
MongDuong1.base_plant_efficiency = 38.84 / 100
MongDuong1.base_boiler_efficiency = 87.03 / 100

MongDuong1.capital_cost = 50 * USD / kW
MongDuong1.coal_price = 52.69 * USD / t
MongDuong1.fix_om_cost = 32.24 * USD / kW / y
MongDuong1.variable_om_cost = 0.006 * USD / (kW*hr)
# Computed separately. Assumes 5% co-firing
MongDuong1.biomass_required = 259107.274137779 * t / y
MongDuong1.biomass_unit_cost = 41.311153541657 * USD / t
MongDuong1.heat_rate = 9.32786896004 * MJ / (kW*hr)
MongDuong1.capacity_factor = 0.68704549298157
MongDuong1.collection_radius = 70.7431601125762 * km
MongDuong1.coal_saved = 155986.88053583 * t / y
MongDuong1.coal_transport_distance = 0 * km
MongDuong1.coal_heat_value = 19.43468 * MJ / kg
MongDuong1.biomass_yeild = 5.605 * t / ha / y
# rice cultivation area needed to supply straw for co-firing in the plant
MongDuong1.rice_cultivation_area = 46228 * ha

MongDuong1.ef_coal_combust = 0.0966 * kg / MJ
MongDuong1.ef_coal_transport = 0 * kg / t / km
MongDuong1.ef_biomass_combust = 0.0858 * kg / MJ
MongDuong1.ef_biomass_transport = 0.062 * kg / t / km

MongDuong1.esp_efficiency = 0.996
MongDuong1.desulfur_efficiency = 0.982
MongDuong1.ef_so2_coal = 11.5 * kg / t
MongDuong1.ef_pm10_coal = 43.8 * kg / t
MongDuong1.ef_nox_coal = 18 * kg / t

NinhBinh = PowerPlant()

NinhBinh.commissioning = 1974
NinhBinh.boiler_technology = 'PC'
NinhBinh.capacity = 100 * MW
NinhBinh.generation = 750 * GW * hr / y
NinhBinh.coal_heat_value = 25.3 * MJ / kg
NinhBinh.base_coal_consumption = 420000 * t / y
NinhBinh.base_plant_efficiency = 21.77 / 100
NinhBinh.base_boiler_efficiency = 81.61 / 100


NinhBinh.capital_cost = 100 * USD / kW
NinhBinh.coal_price = 83.83 * USD / t
NinhBinh.fix_om_cost = 32.24 * USD / kW / y
NinhBinh.variable_om_cost = 0.006 * USD / (kW*hr)
# Computed separately. Assumes 5% co-firing
NinhBinh.biomass_required = 53362.0062849769 * t / y
NinhBinh.biomass_unit_cost = 38.154337591058 * USD / t
NinhBinh.heat_rate = 16.6489459609128 * MJ / (kW*hr)
NinhBinh.capacity_factor = 0.85616438356164
NinhBinh.collection_radius = 15.7274063201183 * km
NinhBinh.coal_saved = 24664.423049406 * t / y
NinhBinh.coal_transport_distance = 200 * km
NinhBinh.coal_heat_value = 25.3132 * MJ / kg
NinhBinh.biomass_yeild = 5.7 * t / ha / y
# rice cultivation area needed to supply straw for co-firing in the plant
NinhBinh.rice_cultivation_area = 9362 * ha

NinhBinh.ef_coal_combust = 0.0966 * kg / MJ
NinhBinh.ef_coal_transport = 0.031 * kg / t / km
NinhBinh.ef_biomass_combust = 0.0858 * kg / MJ
NinhBinh.ef_biomass_transport = 0.062 * kg / t / km

NinhBinh.esp_efficiency = 0.992
NinhBinh.desulfur_efficiency = 0
NinhBinh.ef_so2_coal = 11.5 * kg / t
NinhBinh.ef_pm10_coal = 26.1 * kg / t
NinhBinh.ef_nox_coal = 18 * kg / t
