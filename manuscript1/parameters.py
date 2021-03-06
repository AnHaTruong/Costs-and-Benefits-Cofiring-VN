# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Define the model's input parameters.

All numeric values should be defined in this module,
except those defined in the parameters_supplychain module
"""


from pandas import Series

from model.utils import USD, VND
from model.utils import MJ, kg, t, d, hr, km, MW, ha, kW, y, kWh, MWh, g
from model.system import System, Price
from model.powerplant import Fuel, PlantParameter
from model.cofiringplant import CofiringParameter
from model.farmer import FarmerParameter
from model.reseller import ResellerParameter
from model.system import MiningParameter

from manuscript1.parameters_supplychain import supply_chain_MD1, supply_chain_NB


discount_rate = 0.1  # As per MOIT circular on coal plants tariff calculation.
depreciation_period = 10
tax_rate = 0.20  # Corporate tax in Vietnam

coal_import_price = 112 * USD / t

# CO2 6 USD/t fromcentral case in UNDP (2018) Opportunities for carbon pricing in VN.
external_cost_SKC = Series(
    {  # Sakulniyomporn, Kubaha, and Chullabodhi (2011) RSER 15
        "CO2": 6 * USD / t,
        "SO2": 3767 * USD / t,
        "PM10": 5883 * USD / t,
        "NOx": 286 * USD / t,
    }
)

external_cost_ZWY = Series(
    {  # Zhang Q, Weili T, Yumei W, et al. (2007) Energy Policy 35
        "CO2": 6 * USD / t,
        "SO2": 3680 * USD / t,
        "PM10": 2625 * USD / t,
        "NOx": 2438 * USD / t,
    }
)

external_cost_HAS = Series(
    {  # Hainoun A, Almoustafa A, Seif Aldin M. (2010) Energy 35
        "CO2": 6 * USD / t,
        "SO2": 1134 * USD / t,
        "PM10": 2496 * USD / t,
        "NOx": 1398 * USD / t,
    }
)

external_cost = (external_cost_SKC + external_cost_ZWY + external_cost_HAS) / 3

mining_parameter = MiningParameter(
    productivity_surface=8.04 * t / hr,  # www.eia.g
    productivity_underground=2.5 * t / hr,  # ww.eia.gov
    # Decision 1768/QD-TKV dated 28/9/2018
    wage_mining=5.59 * USD / hr,
)
coal_6b = Fuel(
    name="6b_coal",
    heat_value=19.43468 * MJ / kg,  # numerical value also used in emission_factor
    transport_distance=0 * km,
    transport_mean="conveyor_belt",
)

coal_4b = Fuel(
    name="4b_coal",
    heat_value=21.5476 * MJ / kg,  # numerical value also used in emission_factor
    transport_distance=200 * km,
    transport_mean="barge_transport",
)

straw = Fuel(
    name="straw_boiler",
    heat_value=11.7 * MJ / kg,  # numerical value also used in emission_factor
    transport_distance="Endogenous",
    transport_mean="road_transport",
)

_diesel_heat_value = 45.5 * MJ / kg  # ACEA

emission_factor = dict()

emission_factor[None] = {
    "CO2": 0 * kg / t,
    "SO2": 0 * kg / t,
    "NOx": 0 * kg / t,
    "PM10": 0 * kg / t,
}

emission_factor["6b_coal"] = {
    "CO2": 0.0966 * kg / MJ * coal_6b.heat_value,  # IPCC 2006
    "SO2": 11.5 * kg / t,  # Eastern Research Group (2011)
    "NOx": 18 * kg / t,  # idem
    "PM10": 43.8 * kg / t,
}  # idem

emission_factor["4b_coal"] = {
    "CO2": 0.0966 * kg / MJ * coal_4b.heat_value,  # IPCC 2006
    "SO2": emission_factor["6b_coal"]["SO2"],
    "NOx": emission_factor["6b_coal"]["NOx"],
    "PM10": 26.1 * kg / t,
}

emission_factor["diesel"] = {
    "CO2": 0.0705 * kg / MJ * _diesel_heat_value,  # EPA AP-42, VolI, 3,3
    "SO2": 0.0004 * kg / MJ * _diesel_heat_value,  # EPA AP-42, VolI, 3,3
    "NOx": 0.0018 * kg / MJ * _diesel_heat_value,  # EPA AP-42, VolI, 3,3
    "PM10": 0.00014 * kg / MJ * _diesel_heat_value,
}  # EPA AP-42, VolI, 3,3

emission_factor["conveyor_belt"] = {
    "CO2": 0 * kg / t / km,
    "SO2": 0 * kg / t / km,
    "NOx": 0 * kg / t / km,
    "PM10": 0 * kg / t / km,
}

emission_factor["road_transport"] = {
    "CO2": 0.110 * kg / t / km,  # Binh & Tuan (2016)
    "SO2": 0.003
    * g
    / (20 * t)
    / km,  # http://naei.defra.gov.uk/data/ef-transport, year 2014
    "NOx": 2.68 * g / (20 * t) / km,  # idem
    "PM10": 0.04 * g / (20 * t) / km,
}  # idem

emission_factor["barge_transport"] = {
    "CO2": 0.071 * kg / t / km,  # Binh & Tuan (2016)
    "SO2": 2 * g / kg * (8 * g / t / km),  # Van Dingenen et al. (2016)
    "NOx": 50.75 * g / kg * (8 * g / t / km),  # idem
    "PM10": 3.19 * g / kg * (8 * g / t / km),
}  # idem

emission_factor["straw_open"] = {
    "CO2": 1177 * kg / t,  # (Kim Oanh & 2011) for open burning
    "SO2": 0.51 * kg / t,  # (Kim Oanh & 2015) for open burning
    "NOx": 0.49 * kg / t,  # (Kim Oanh & 2011) for open burning
    "PM10": 9.4 * kg / t,
}  # (Kim Oanh & 2011) for open burning

emission_factor["straw_boiler"] = {
    "CO2": 1674 * kg / t,  # (Cao & 2008) from experiments
    "SO2": 0.18 * kg / t,  # idem
    "NOx": 3.43 * kg / t,  # idem
    "PM10": 6.28 * kg / t,
}  # idem

# hourly wage calculated from base salary defined in governmental regulations
farm_parameter = FarmerParameter(
    winder_rental_cost=40 * USD / ha,  # per period
    winder_haul=6.57 * t / d,
    work_hour_day=8 * hr / d,
    wage_bm_collect=3.7 * USD / hr,  # Tran Dang (2019)
    fuel_cost_per_hour=0.5 * USD / hr,
    open_burn_rate=0.6,
    fuel_use=4.16 * kg / d,
    # Thang T.C. et al. (2014), Policies and measures for improve the efficiency of value chain:
    # the cases of rice and pork in Vietnam, Hanoi, Vietnam.
    profit=2 * 527 * USD / ha,
)

transport_parameter = ResellerParameter(
    barge_fuel_consumption=8 * g / t / km,  # Van Dingenen & 2016
    truck_loading_time=2.7 / 60 * hr / t,  # Ovaskainen & Lundberg (2016)
    wage_bm_loading=1.11 * USD / hr,
    truck_load=20 * t,  # Also used in road_transport.emission_factor
    truck_velocity=45 * km / hr,
    fuel_cost_per_hour_driving=7.15 * USD / hr,
    fuel_cost_per_hour_loading=0 * USD / hr,
    rental_cost_per_hour=9.62 * USD / hr,
    wage_bm_transport=2.13 * USD / hr,  # http://vietnamsalary.careerbuilder.vn
)

plant_parameter_MD1 = PlantParameter(
    name="Mong Duong 1",
    capacity=1080 * MW,
    commissioning=2015,
    boiler_technology="CFB",
    capacity_factor=0.60,
    boiler_efficiency_new=87.03 / 100,
    plant_efficiency=38.84 / 100,
    fix_om_main=29.31 * USD / kW / y,
    variable_om_main=0.0048 * USD / kWh,
    emission_control={"CO2": 0.0, "SO2": 0.982, "NOx": 0.0, "PM10": 0.996},
    fuel=coal_6b,
)

cofire_MD1 = CofiringParameter(
    investment_cost=50 * USD / kW,
    fix_om_cost=32.24 * USD / kW / y,
    variable_om_cost=0.006 * USD / kWh,
    OM_hour_MWh=0.12 * hr / MWh,  # working hour for OM per MWh
    wage_operation_maintenance=2.7 * USD / hr,  # A 2015 job opening
    cofire_rate=0.05,
    cofuel=straw,
    # Tillman (2000) r mass ratio
    boiler_efficiency_loss=lambda r: 0.0044 * r ** 2 + 0.0055 * r,
)

price_MD1 = Price(
    biomass_plantgate=22 * USD / t,
    biomass_fieldside=16 * USD / t,
    coal=1131400 * VND / t,
    electricity=1239.17 * VND / kWh,
)

MongDuong1System = System(
    plant_parameter_MD1,
    cofire_MD1,
    supply_chain_MD1,
    price_MD1,
    farm_parameter,
    transport_parameter,
    mining_parameter,
    emission_factor,
)

plant_parameter_NB = PlantParameter(
    name="Ninh Binh",
    capacity=100 * MW,
    commissioning=1974,
    boiler_technology="PC",
    capacity_factor=0.64,
    plant_efficiency=21.77 / 100,
    boiler_efficiency_new=81.61 / 100,
    fix_om_main=plant_parameter_MD1.fix_om_main,
    variable_om_main=plant_parameter_MD1.variable_om_main,
    emission_control={"CO2": 0.0, "SO2": 0.0, "NOx": 0.0, "PM10": 0.992},
    fuel=coal_4b,
)

cofire_NB = cofire_MD1._replace(investment_cost=100 * USD / kW)

price_NB = Price(
    biomass_plantgate=32 * USD / t,
    biomass_fieldside=19 * USD / t,
    coal=1825730 * VND / t,  # Includes transport
    electricity=1665.6 * VND / kWh,
)

NinhBinhSystem = System(
    plant_parameter_NB,
    cofire_NB,
    supply_chain_NB,
    price_NB,
    farm_parameter,
    transport_parameter,
    mining_parameter,
    emission_factor,
)
