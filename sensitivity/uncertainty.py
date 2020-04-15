# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# uncertainty
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Parameters for the sensitivity analysis.

Each uncertain parameter has a baseline value and an uncertainty range.
"""
from pandas import DataFrame

from model.utils import VND, USD, kWh, t, display_as

from manuscript1.parameters import (
    coal_import_price,
    discount_rate,
    external_cost,
    external_cost_SKC,
    external_cost_ZWY,
    external_cost_HAS,
    farm_parameter,
    price_MD1,
    price_NB,
    tax_rate,
)

#%%

# There should be baseline_MD1 and baseline_NB to ensure coherence

bounds = {}

# Low bound: GDP growth rate was >5% since 1980 except 85 and 86.
# High bound: # Typical private sector
bounds["discount_rate"] = [0.05, discount_rate, 0.15]

bounds["tax_rate"] = [0.1, tax_rate, 0.3]

# Low bound: Minimum observed in Vietnam, 2014-01 lowest grade coal. (MOIT)
bounds["coal_price"] = [1060000 * VND / t, price_NB.coal, coal_import_price]

# Low bound: 2015-01 system average power purchase price of EVN (MOIT web)
# High bound: # About 8.5 UScents, plausible upper bound on wholesale power price.
bounds["electricity_price"] = [
    1137.48 * VND / kWh,
    price_NB.electricity,
    2000 * VND / kWh,
]

# Low bound: # Status quo according to UNDP (2018) table 16
# High bound: Upper case in UNDP (201*)
bounds["external_cost_CO2"] = [0.2 * USD / t, external_cost["CO2"], 15 * USD / t]

bounds["external_cost_SO2"] = [
    min(external_cost_SKC["SO2"], external_cost_ZWY["SO2"], external_cost_HAS["SO2"])
    * 0.8,
    external_cost["SO2"],
    max(external_cost_SKC["SO2"], external_cost_ZWY["SO2"], external_cost_HAS["SO2"])
    * 1.2,
]

bounds["external_cost_PM10"] = [
    min(external_cost_SKC["PM10"], external_cost_ZWY["PM10"], external_cost_HAS["PM10"])
    * 0.8,
    external_cost["PM10"],
    max(external_cost_SKC["PM10"], external_cost_ZWY["PM10"], external_cost_HAS["PM10"])
    * 1.2,
]

bounds["external_cost_NOx"] = [
    min(external_cost_SKC["NOx"], external_cost_ZWY["NOx"], external_cost_HAS["NOx"])
    * 0.8,
    external_cost["NOx"],
    max(external_cost_SKC["NOx"], external_cost_ZWY["NOx"], external_cost_HAS["NOx"])
    * 1.2,
]

bounds["straw_burn_rate"] = [0.3, farm_parameter.straw_burn_rate, 0.9]

bounds["biomass_plantgate"] = [
    min(price_MD1.biomass_plantgate, price_NB.biomass_plantgate) * 0.8,
    (price_MD1.biomass_plantgate + price_NB.biomass_plantgate) / 2,
    max(price_MD1.biomass_plantgate, price_NB.biomass_plantgate) * 1.2,
]

bounds["biomass_fieldside"] = [
    min(price_MD1.biomass_fieldside, price_NB.biomass_fieldside) * 0.8,
    (price_MD1.biomass_fieldside + price_NB.biomass_fieldside) / 2,
    max(price_MD1.biomass_fieldside, price_NB.biomass_fieldside) * 1.2,
]

display_as(bounds["coal_price"], "USD/t")
display_as(bounds["electricity_price"], "VND/kWh")
display_as(bounds["external_cost_CO2"], "USD/t")
display_as(bounds["external_cost_SO2"], "USD/t")
display_as(bounds["external_cost_PM10"], "USD/t")
display_as(bounds["external_cost_NOx"], "USD/t")
display_as(bounds["biomass_plantgate"], "USD/t")
display_as(bounds["biomass_fieldside"], "USD/t")

# assert bounds bracket the baseline(s)

uncertainty = DataFrame.from_dict(
    bounds, orient="index", columns=["Low bound", "Baseline", "High bound"]
)
