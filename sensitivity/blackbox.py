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
from pandas import Series, DataFrame

from model.utils import npv, VND, kWh, display_as

from model.system import System, Price
from manuscript1.parameters import (
    discount_rate,
    external_cost,
    tax_rate,
    plant_parameter_MD1,
    cofire_MD1,
    supply_chain_MD1,
    price_MD1,
    plant_parameter_NB,
    cofire_NB,
    supply_chain_NB,
    price_NB,
    farm_parameter,
    transport_parameter,
    mining_parameter,
    emission_factor,
)

#%%

# We use an average coal price as baseline to run the sensitivity test. Fixme?
uncertainty = DataFrame(
    index=[
        "discount_rate",
        "tax_rate",
        "coal_price",
        "electricity_price",
        "external_cost_CO2",
        "external_cost_SO2",
        "external_cost_PM10",
        "external_cost_NOx",
    ],
    columns=["Low bound", "Baseline", "High bound"],
    data=[
        [0.03, discount_rate, 0.15],
        [0, tax_rate, 0.4],
        [
            price_MD1.coal * 0.75,
            (price_MD1.coal + price_NB.coal) / 2,
            price_NB.coal * 1.25,
        ],
        [1000 * VND / kWh, price_MD1.electricity, 1500 * VND / kWh],
        [external_cost["CO2"] * 0.1, external_cost["CO2"], external_cost["CO2"] * 30],
        [external_cost["SO2"] * 0.2, external_cost["SO2"], external_cost["SO2"] * 2],
        [external_cost["PM10"] * 0.2, external_cost["PM10"], external_cost["PM10"] * 2],
        [external_cost["NOx"] * 0.2, external_cost["NOx"], external_cost["NOx"] * 2],
    ],
)

display_as(uncertainty.loc["coal_price"], "USD/t")
display_as(uncertainty.loc["electricity_price"], "USD/kWh")
display_as(uncertainty.loc["external_cost_CO2"], "USD/t")
display_as(uncertainty.loc["external_cost_SO2"], "USD/t")
display_as(uncertainty.loc["external_cost_PM10"], "USD/t")
display_as(uncertainty.loc["external_cost_NOx"], "USD/t")

#%%


def f_MD1(x):
    """Return the business value and the externalities of cofiring, as a pair of USD quantities.

    The argument x must be a Series homogenous with uncertainty.index
    Mong Duong 1 case.
    """
    assert all(
        x.index == uncertainty.index
    ), "Model argument mismatch uncertainty.index."
    price_MD1_local = Price(
        biomass_plantgate=price_MD1.biomass_plantgate,
        biomass_fieldside=price_MD1.biomass_fieldside,
        coal=x["coal_price"],
        electricity=x["electricity_price"],
    )

    external_cost_variant = Series(
        {
            "CO2": x["external_cost_CO2"],
            "SO2": x["external_cost_SO2"],
            "PM10": x["external_cost_PM10"],
            "NOx": x["external_cost_NOx"],
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
    business_value = MD1SystemVariant.table_business_value(x["discount_rate"])[-1]
    display_as(business_value, "MUSD")

    benefits_table = MD1SystemVariant.emissions_reduction_benefit(
        external_cost_variant
    ).loc["Value"]
    external_value = npv(x["discount_rate"], benefits_table.sum())
    display_as(external_value, "MUSD")
    return business_value, external_value


def f_NB(x):
    """Return the business value and the externalities of cofiring, as a pair of USD quantities.

    The argument x must be a Series homogenous with uncertainty.index
    Ninh Binh case
    """
    assert all(
        x.index == uncertainty.index
    ), "Model argument mismatch uncertainty.index."
    price_NB_local = Price(
        biomass_plantgate=price_NB.biomass_plantgate,
        biomass_fieldside=price_NB.biomass_fieldside,
        coal=x["coal_price"],
        electricity=x["electricity_price"],
    )

    external_cost_variant = Series(
        {
            "CO2": x["external_cost_CO2"],
            "SO2": x["external_cost_SO2"],
            "PM10": x["external_cost_PM10"],
            "NOx": x["external_cost_NOx"],
        }
    )

    NBSystemVariant = System(
        plant_parameter_NB,
        cofire_NB,
        supply_chain_NB,
        price_NB_local,
        farm_parameter,
        transport_parameter,
        mining_parameter,
        emission_factor,
    )
    business_value = NBSystemVariant.table_business_value(x["discount_rate"])[-1]
    display_as(business_value, "MUSD")

    benefits_table = NBSystemVariant.emissions_reduction_benefit(
        external_cost_variant
    ).loc["Value"]
    external_value = npv(x["discount_rate"], benefits_table.sum())
    display_as(external_value, "MUSD")
    return business_value, external_value
