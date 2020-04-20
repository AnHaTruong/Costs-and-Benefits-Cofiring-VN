# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# table_sensitivityanalysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Print the results of the sensitivity analysis."""

from pandas import DataFrame

from sensitivity.one_at_a_time import sensitivity_runs_MD1, sensitivity_runs_NB


def table_sensitivity(run, name):
    """Return the two sensitivity analysis result tables, as a string."""
    contents = [
        f"Results of the sensitivity analysis for {name} case.",
        "",
        "Result: business value.",
        DataFrame(run["business_value"]).to_string(),
        "",
        "Result: external value.",
        DataFrame(run["external_value"]).to_string(),
        "",
    ]
    return "\n".join(contents)


print(table_sensitivity(sensitivity_runs_MD1, "Mong Duong 1"))
print(table_sensitivity(sensitivity_runs_NB, "Ninh Binh"))
