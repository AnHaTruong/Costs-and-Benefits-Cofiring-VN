# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

from units import USD, VND, time_step
from natu.units import MJ, kg, t, d, hr, km, MW, ha, g, kW, y, kWh
from PowerPlant import PowerPlant, CoalSupply


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

MDcoal = CoalSupply(heat_value=19.43468 * MJ / kg,
                    price=1131400 * VND / t,
                    transport_distance=0 * km,
                    ef_combust=0.0966 * kg / MJ,
                    ef_transport=0 * kg / t / km,
                    ef_so2=11.5 * kg / t,
                    ef_pm10=43.8 * kg / t,
                    ef_nox=18 * kg / t
                    )

MongDuong1 = PowerPlant(capacity=1080 * MW,
                        capacity_factor=0.60,
                        commissioning=2015,
                        boiler_technology='CFB',
                        plant_efficiency=38.84 / 100,
                        boiler_efficiency=87.03 / 100,
                        electricity_tariff=1239.17 * VND / kWh,
                        fix_om_coal=29.31 * USD / kW / y,
                        variable_om_coal=0.0048 * USD / kWh,
                        esp_efficiency=0.996,
                        desulfur_efficiency=0.982,
                        coal=MDcoal
                        )

MongDuong1.capital_cost = 50 * USD / kW
MongDuong1.fix_om_cost = 32.24 * USD / kW / y
MongDuong1.variable_om_cost = 0.006 * USD / (kW*hr)
MongDuong1.ef_biomass_combust = 0.0858 * kg / MJ
MongDuong1.ef_biomass_transport = 0.110 * kg / t / km  # biomass transported by truck

NBcoal = CoalSupply(heat_value=21.5476 * MJ / kg,
                    price=1825730 * VND / t,
                    transport_distance=200 * km,
                    ef_combust=0.0966 * kg / MJ,
                    ef_transport=0.071 * kg / t / km,  # coal transported by barge
                    ef_so2=11.5 * kg / t,
                    ef_pm10=26.1 * kg / t,
                    ef_nox=18 * kg / t
                    )

NinhBinh = PowerPlant(capacity=100 * MW,
                      capacity_factor=0.64,
                      commissioning=1974,
                      boiler_technology='PC',
                      plant_efficiency=21.77 / 100,
                      boiler_efficiency=81.61 / 100,
                      electricity_tariff=1665.6 * VND / kWh,
                      fix_om_coal=29.31 * USD / kW / y,
                      variable_om_coal=0.0048 * USD / kWh,
                      esp_efficiency=0.992,
                      desulfur_efficiency=0,
                      coal=NBcoal
                      )

NinhBinh.capital_cost = 100 * USD / kW
NinhBinh.fix_om_cost = 32.24 * USD / kW / y
NinhBinh.variable_om_cost = 0.006 * USD / (kW*hr)
NinhBinh.ef_biomass_combust = 0.0858 * kg / MJ
NinhBinh.ef_biomass_transport = 0.110 * kg / t / km  # biomass transported by truck
