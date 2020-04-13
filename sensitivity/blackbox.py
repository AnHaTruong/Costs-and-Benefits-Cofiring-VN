# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# blackbox
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Represents the model as a blackbox, for sensitivity analysis.

Sensitivity analysis is based on the representation  Y = f(X1, ..., Xn).
Y must be a scalar, unitless. For our biomass model can be business_value or the external benefits.
The Xi are the uncertain parameters.
"""
from pandas import Series

from model.utils import npv, USD, VND, kWh, display_as

from model.system import System, Price
from manuscript1.parameters import (
    MongDuong1System,
    discount_rate,
    external_cost,
    tax_rate,
    plant_parameter_MD1,
    cofire_MD1,
    supply_chain_MD1,
    price_MD1,
    farm_parameter,
    transport_parameter,
    mining_parameter,
    emission_factor,
)

#%% The toy version

toy_uncertainty = {
    "num_vars": 2,
    "names": ["discount_rate", "tax_rate"],
    "bounds": [[0.03, 0.15], [0, 0.4]],  # Discount rate  # Tax rate
}


# We know the tax rate does not matter, but we want to check that the sensitivity computes to 0
# pylint: disable=unused-argument
def toy_business_value(discount_rate, tax_rate):
    """Return the business value of cofiring in USD, as a float."""
    return MongDuong1System.table_business_value(discount_rate)[-1] / USD


#%% The real one

uncertainty = {
    "num_vars": 8,
    "names": [
        "discount_rate",
        "tax_rate",
        "coal_price",
        "electricity_price",
        "external_cost_CO2",
        "external_cost_SO2",
        "external_cost_PM10",
        "external_cost_NOx",
    ],
    "lomidhi": [
        [0.03, discount_rate, 0.15],
        [0, tax_rate, 0.4],
        [price_MD1.coal * 0.75, price_MD1.coal, price_MD1.coal * 1.25],
        [1000 * VND / kWh, price_MD1.electricity, 1500 * VND / kWh],
        [external_cost["CO2"] * 0.1, external_cost["CO2"], external_cost["CO2"] * 30],
        [external_cost["SO2"] * 0.2, external_cost["SO2"], external_cost["SO2"] * 2],
        [external_cost["PM10"] * 0.2, external_cost["PM10"], external_cost["PM10"] * 2],
        [external_cost["NOx"] * 0.2, external_cost["NOx"], external_cost["NOx"] * 2],
    ],
}

display_as(uncertainty["lomidhi"][2], "USD/t")
display_as(uncertainty["lomidhi"][3], "VND/kWh")
display_as(uncertainty["lomidhi"][4], "USD/t")
display_as(uncertainty["lomidhi"][5], "USD/t")
display_as(uncertainty["lomidhi"][6], "USD/t")
display_as(uncertainty["lomidhi"][7], "USD/t")

#%%


def business_value(
    discount_rate,
    tax_rate,
    coal_price,
    electricity_price,
    external_cost_CO2,
    external_cost_SO2,
    external_cost_PM10,
    external_cost_NOx,
):
    """Return the business value of cofiring in USD, as a float."""
    price_MD1_local = Price(
        biomass_plantgate=price_MD1.biomass_plantgate,
        biomass_fieldside=price_MD1.biomass_fieldside,
        coal=coal_price,
        electricity=electricity_price,
    )

    MD1SystemVariant = System(
        plant_parameter_MD1,
        cofire_MD1,
        supply_chain_MD1,
        price_MD1_local,
        farm_parameter,
        transport_parameter,
        mining_parameter,
        emission_factor,
    )
    result = MD1SystemVariant.table_business_value(discount_rate)[-1] / USD
    return result


def multi_objectives(
    discount_rate,
    tax_rate,
    coal_price,
    electricity_price,
    external_cost_CO2,
    external_cost_SO2,
    external_cost_PM10,
    external_cost_NOx,
):
    """Return the business value and the externalities of cofiring in USD, as a pair of floats."""
    price_MD1_local = Price(
        biomass_plantgate=price_MD1.biomass_plantgate,
        biomass_fieldside=price_MD1.biomass_fieldside,
        coal=coal_price,
        electricity=electricity_price,
    )

    external_cost_variant = Series(
        {
            "CO2": external_cost_CO2,
            "SO2": external_cost_SO2,
            "PM10": external_cost_PM10,
            "NOx": external_cost_NOx,
        }
    )

    MD1SystemVariant = System(
        plant_parameter_MD1,
        cofire_MD1,
        supply_chain_MD1,
        price_MD1_local,
        farm_parameter,
        transport_parameter,
        mining_parameter,
        emission_factor,
    )
    business_value = MD1SystemVariant.table_business_value(discount_rate)[-1] / USD

    benefits_table = MD1SystemVariant.emissions_reduction_benefit(
        external_cost_variant
    ).loc["Value"]
    external_value = npv(discount_rate, benefits_table.sum()) / USD
    return business_value, external_value
