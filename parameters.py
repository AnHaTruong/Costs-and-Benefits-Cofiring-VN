# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#


from units import MJ, kg, t, d, hr, km, MW, USD, VND, ha, g, kW, y, time_step
from PowerPlant import PowerPlant


"""Input parameters of the model"""

discount_rate = 0.087771 * time_step / y
depreciation_period = 10
tax_rate = 0.25  # Corporate tax in Vietnam

biomass_heat_value = 11.7 * MJ / kg
biomass_ratio = 0.05             # As percent of energy coming from biomass

straw_collection_fraction = 0.5  # Refer to (Leinonen and Nguyen 2013)
straw_selling_proportion = 0.79  # Refer to (Leinonen and Nguyen 2013)
residue_to_product_ratio_straw = 1.0
straw_burn_rate = 0.9  # Percentage of straw burned infield after harvest
winder_capacity = 6.57 * t / d
work_hour_day = 8 * hr / d
FTE = 1560 * hr / y  # number of working hour for a FTE job # a full time equivalence job
truck_velocity = 45 * km / hr
truck_load = 20 * t
OM_hour_MWh = 0.12 * hr / MW / hr  # working hour for OM per MWh    # O&M of co-firing per MWh

biomass_fix_cost = 37.26 * USD / t
transport_tariff = 2000 * VND / t / km  # vantaiduongviet.com
tortuosity_factor = 1.5
# wage per hour is calculated from base salary defined in governmental regulations
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


MongDuong1 = PowerPlant(capacity=1080 * MW,
                        capacity_factor=0.60,
                        commissioning=2015,
                        boiler_technology='CFB',
                        coal_heat_value=19.43468 * MJ / kg,
                        plant_efficiency=38.84 / 100,
                        boiler_efficiency=87.03 / 100,
                        electricity_tariff=1239.17 * VND / (kW*hr),
                        coal_price=1131400 * VND / t,
                        fix_om_coal=29.31 * USD / kW / y,
                        variable_om_coal=0.0048 * USD / (kW*hr),
                        ef_coal_combust=0.0966 * kg / MJ,
                        ef_coal_transport=0 * kg / t / km,
                        coal_transport_distance=0 * km,
                        esp_efficiency=0.996,
                        desulfur_efficiency=0.982,
                        ef_so2_coal=11.5 * kg / t,
                        ef_pm10_coal=43.8 * kg / t,
                        ef_nox_coal=18 * kg / t,
                        )

MongDuong1.capital_cost = 50 * USD / kW
MongDuong1.fix_om_cost = 32.24 * USD / kW / y
MongDuong1.variable_om_cost = 0.006 * USD / (kW*hr)
MongDuong1.ef_biomass_combust = 0.0858 * kg / MJ
MongDuong1.ef_biomass_transport = 0.110 * kg / t / km  # biomass transported by truck


NinhBinh = PowerPlant(capacity=100 * MW,
                      capacity_factor=0.64,
                      commissioning=1974,
                      boiler_technology='PC',
                      coal_heat_value=21.5476 * MJ / kg,
                      plant_efficiency=21.77 / 100,
                      boiler_efficiency=81.61 / 100,
                      electricity_tariff=1665.6 * VND / (kW * hr),
                      coal_price=1825730 * VND / t,
                      fix_om_coal=29.31 * USD / kW / y,
                      variable_om_coal=0.0048 * USD / (kW*hr),
                      coal_transport_distance=200 * km,
                      ef_coal_combust=0.0966 * kg / MJ,
                      ef_coal_transport=0.071 * kg / t / km,  # coal transported by barge
                      esp_efficiency=0.992,
                      desulfur_efficiency=0,
                      ef_so2_coal=11.5 * kg / t,
                      ef_pm10_coal=26.1 * kg / t,
                      ef_nox_coal=18 * kg / t
                      )

NinhBinh.capital_cost = 100 * USD / kW
NinhBinh.fix_om_cost = 32.24 * USD / kW / y
NinhBinh.variable_om_cost = 0.006 * USD / (kW*hr)
NinhBinh.ef_biomass_combust = 0.0858 * kg / MJ
NinhBinh.ef_biomass_transport = 0.110 * kg / t / km  # biomass transported by truck
