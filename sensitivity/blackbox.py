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

from model.utils import npv, VND, USD, kWh, t, display_as

from model.system import System, Price
from manuscript1.parameters import (
    discount_rate,
    external_cost,
    external_cost_SKC,
    external_cost_ZWY,
    external_cost_HAS,
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
    coal_import_price,
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
        # Biomass prices
        # Straw burn rate  0.3 - 0.6 - 0.9
    ],
    columns=["Low bound", "Baseline", "High bound"],
    data=[
        [
            0.05,  # GDP growth rate was >5% since 1980 except 85 and 86.
            discount_rate,
            0.15,  # Typical private sector
        ],
        [0.1, tax_rate, 0.3],
        [
            1060000
            * VND
            / t,  # Minimum observed in Vietnam, 2014-01 lowest grade coal. (MOIT)
            price_NB.coal,
            coal_import_price,
        ],
        [
            1137.48
            * VND
            / kWh,  # 2015-01 system average power purchase price of EVN (MOIT web)
            price_NB.electricity,
            2000
            * VND
            / kWh,  # About 8.5 UScents, plausible upper bound on wholesale power price.
        ],
        [
            0.2 * USD / t,  # Status quo according to UNDP (2018) table 16
            external_cost["CO2"],
            15 * USD / t,  # Upper case in UNDP (201*)
        ],
        [
            min(
                external_cost_SKC["SO2"],
                external_cost_ZWY["SO2"],
                external_cost_HAS["SO2"],
            )
            * 0.8,
            external_cost["SO2"],
            max(
                external_cost_SKC["SO2"],
                external_cost_ZWY["SO2"],
                external_cost_HAS["SO2"],
            )
            * 1.2,
        ],
        [
            min(
                external_cost_SKC["PM10"],
                external_cost_ZWY["PM10"],
                external_cost_HAS["PM10"],
            )
            * 0.8,
            external_cost["PM10"],
            max(
                external_cost_SKC["PM10"],
                external_cost_ZWY["PM10"],
                external_cost_HAS["PM10"],
            )
            * 1.2,
        ],
        [
            min(
                external_cost_SKC["NOx"],
                external_cost_ZWY["NOx"],
                external_cost_HAS["NOx"],
            )
            * 0.8,
            external_cost["NOx"],
            max(
                external_cost_SKC["NOx"],
                external_cost_ZWY["NOx"],
                external_cost_HAS["NOx"],
            )
            * 1.2,
        ],
    ],
)

display_as(uncertainty.loc["coal_price"], "USD/t")
display_as(uncertainty.loc["electricity_price"], "VND/kWh")
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
