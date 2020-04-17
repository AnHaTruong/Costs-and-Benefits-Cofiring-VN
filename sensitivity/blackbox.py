# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# blackbox
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Represents the model as a blackbox function for sensitivity analysis.

Sensitivity analysis is based on the representation  Y = f(X1, ..., Xn).
    Xi are the uncertain parameters. Each has an uncertainty range and a baseline value.
    Y is the model result, allowed to be vector here, we do multi objective analysis.
"""
from pandas import Series

from model.utils import npv, display_as

from model.system import System, Price

from manuscript1.parameters import (
    plant_parameter_MD1,
    cofire_MD1,
    supply_chain_MD1,
    plant_parameter_NB,
    cofire_NB,
    supply_chain_NB,
    farm_parameter,
    transport_parameter,
    mining_parameter,
    emission_factor,
)

#%%


def as_model_parameters(x):
    """Bundle the flat dict of parameters x into data structures used by the model.

    Naming convention: underscore prefix to denote the parameter modified.
    """
    _price = Price(
        biomass_plantgate=x["biomass_plantgate"],
        biomass_fieldside=x["biomass_fieldside"],
        coal=x["coal_price"],
        electricity=x["electricity_price"],
    )
    _external_cost = Series(
        {
            "CO2": x["external_cost_CO2"],
            "SO2": x["external_cost_SO2"],
            "PM10": x["external_cost_PM10"],
            "NOx": x["external_cost_NOx"],
        }
    )
    _farm_parameter = farm_parameter._replace(open_burn_rate=x["open_burn_rate"])
    _discount_rate = x["discount_rate"]
    return _price, _external_cost, _farm_parameter, _discount_rate


def cofire_patched(cofiring_parameter, x):
    """Return a copy of cofiring_parameter, with the cofiring ratio modified as per x."""
    _cofire = cofiring_parameter._replace(cofire_rate=x["cofire_rate"])
    return _cofire


def f_MD1(x):
    """Return the business value and the externalities of cofiring, as a pair of USD quantities.

    Mong Duong 1 case.
    """
    _price_MD1, _external_cost, _farm_parameter, _discount_rate = as_model_parameters(x)
    _cofire = cofire_patched(cofire_MD1, x)

    MD1SystemVariant = System(
        plant_parameter_MD1,
        _cofire,
        supply_chain_MD1,
        _price_MD1,
        _farm_parameter,
        transport_parameter,
        mining_parameter,
        emission_factor,
    )
    business_value = MD1SystemVariant.table_business_value(_discount_rate)[-1]
    display_as(business_value, "MUSD")

    benefits_table = MD1SystemVariant.emissions_reduction_benefit(_external_cost).loc[
        "Value"
    ]
    external_value = npv(_discount_rate, benefits_table.sum())
    display_as(external_value, "MUSD")
    return business_value, external_value


def f_NB(x):
    """Return the business value and the externalities of cofiring, as a pair of USD quantities.

    Ninh Binh case
    """
    _price_NB, _external_cost, _farm_parameter, _discount_rate = as_model_parameters(x)
    _cofire = cofire_patched(cofire_NB, x)

    NBSystemVariant = System(
        plant_parameter_NB,
        _cofire,
        supply_chain_NB,
        _price_NB,
        _farm_parameter,
        transport_parameter,
        mining_parameter,
        emission_factor,
    )
    business_value = NBSystemVariant.table_business_value(_discount_rate)[-1]
    display_as(business_value, "MUSD")

    benefits_table = NBSystemVariant.emissions_reduction_benefit(_external_cost).loc[
        "Value"
    ]
    external_value = npv(_discount_rate, benefits_table.sum())
    display_as(external_value, "MUSD")
    return business_value, external_value
