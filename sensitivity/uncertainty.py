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

from model.utils import VND, kWh, t, display_as

from manuscript1.parameters import (
    coal_import_price,
    discount_rate,
    external_cost,
    external_cost_low,
    external_cost_high,
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
bounds["discount_rate"] = [0.05, discount_rate, discount_rate, 0.15]

bounds["tax_rate"] = [0.1, tax_rate, tax_rate, 0.3]

# Low bound: Minimum observed in Vietnam, 2014-01 lowest grade coal. (MOIT)
bounds["coal_price"] = [
    1060000 * VND / t,
    price_MD1.coal,
    price_NB.coal,
    coal_import_price,
]

# Low bound: 2015-01 system average power purchase price of EVN (MOIT web)
# High bound: # About 8.5 UScents, plausible upper bound on wholesale power price.
bounds["electricity_price"] = [
    1137.48 * VND / kWh,
    price_MD1.electricity,
    price_NB.electricity,
    2000 * VND / kWh,
]

# Low bound: # Status quo according to UNDP (2018) table 16
# High bound: Upper case in UNDP (201*)
bounds["external_cost_CO2"] = [
    external_cost_low["CO2"],
    external_cost["CO2"],
    external_cost["CO2"],
    external_cost_high["CO2"],
]

bounds["external_cost_SO2"] = [
    external_cost_low["SO2"],
    external_cost["SO2"],
    external_cost["SO2"],
    external_cost_high["SO2"],
]

bounds["external_cost_PM10"] = [
    external_cost_low["PM10"],
    external_cost["PM10"],
    external_cost["PM10"],
    external_cost_high["PM10"],
]

bounds["external_cost_PM2.5"] = [
    external_cost_low["PM2.5"],
    external_cost["PM2.5"],
    external_cost["PM2.5"],
    external_cost_high["PM2.5"],
]

bounds["external_cost_NOx"] = [
    external_cost_low["NOx"],
    external_cost["NOx"],
    external_cost["NOx"],
    external_cost_high["NOx"],
]

bounds["open_burn_rate"] = [
    0.4,
    farm_parameter.open_burn_rate,
    farm_parameter.open_burn_rate,
    0.8,
]

bounds["biomass_plantgate"] = [
    min(price_MD1.biomass_plantgate, price_NB.biomass_plantgate) * 0.8,
    price_MD1.biomass_plantgate,
    price_NB.biomass_plantgate,
    max(price_MD1.biomass_plantgate, price_NB.biomass_plantgate) * 1.2,
]

bounds["biomass_fieldside"] = [
    min(price_MD1.biomass_fieldside, price_NB.biomass_fieldside) * 0.8,
    price_MD1.biomass_fieldside,
    price_NB.biomass_fieldside,
    max(price_MD1.biomass_fieldside, price_NB.biomass_fieldside) * 1.2,
]

bounds["cofire_rate"] = [0.03, 0.05, 0.05, 0.1]

display_as(bounds["coal_price"], "USD/t")
display_as(bounds["electricity_price"], "VND/kWh")
display_as(bounds["external_cost_CO2"], "USD/t")
display_as(bounds["external_cost_SO2"], "USD/t")
display_as(bounds["external_cost_PM2.5"], "USD/t")
display_as(bounds["external_cost_NOx"], "USD/t")
display_as(bounds["biomass_plantgate"], "USD/t")
display_as(bounds["biomass_fieldside"], "USD/t")


# Sanity check
def is_between(a, b, c: float):
    """Check that bounds indeed bracket the central value."""
    return (a <= b <= c) or (a >= b >= c)


for key, value in bounds.items():
    assert is_between(
        value[0], value[1], value[3]
    ), f"Baseline not beween uncertainty bounds for MD1 uncertainty for {key} parameter: {value}."
    assert is_between(
        value[0], value[2], value[3]
    ), f"Baseline not beween uncertainty bounds for NB uncertainty for {key} parameter: {value}."

uncertainty = DataFrame.from_dict(
    bounds,
    orient="index",
    columns=["Low bound", "Baseline_MD1", "Baseline_NB", "High bound"],
)

uncertainty_MD1 = uncertainty[["Low bound", "Baseline_MD1", "High bound"]]
uncertainty_MD1 = uncertainty_MD1.rename(columns={"Baseline_MD1": "Baseline"})

uncertainty_NB = uncertainty[["Low bound", "Baseline_NB", "High bound"]]
uncertainty_NB = uncertainty_NB.rename(columns={"Baseline_NB": "Baseline"})
