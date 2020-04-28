# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Print the tables for manuscript 'Costs and benefits of co-firing'.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017-2019
"""

from pandas import DataFrame, concat

from manuscript1.parameters import MongDuong1System, NinhBinhSystem
from model.fuelpowerplant import Fuel


def dict_to_df(stem, dictionary):
    """Cast a dictionary into DataFrame, stemming the keys."""
    stemmed_keys = [stem + "_" + key for key in dictionary.keys()]
    data = dictionary.values()
    return DataFrame(data, index=stemmed_keys)


def fuel_to_df(stem, fuel):
    """Cast a Fuel namedtuple into DataFrame, stemming the keys."""
    return dict_to_df(stem, fuel._asdict())


def scalar_to_df(index, value):
    """Cast a scalar into a DataFrame."""
    if index == "boiler_efficiency_loss":
        value = "0.0044 r^2 + 0.0055 r"
    return DataFrame([value], index=[index])


def flatten(serie):
    """Flatten a parameter table so that the dictionary and namedtuples get one line per value."""
    df = DataFrame()
    for index, value in serie.iteritems():
        if isinstance(value, dict):
            df = df.append(dict_to_df(index, value))
        else:
            if isinstance(value, Fuel):
                df = df.append(fuel_to_df(index, value))
            else:
                df = df.append(scalar_to_df(index, value))
    return df


tableMD1 = flatten(MongDuong1System.parameters_table())
tableNB = flatten(NinhBinhSystem.parameters_table())

table = concat([tableMD1, tableNB], axis=1)
table.columns = table.loc["name"]
table = table.drop("name")

print(table)
