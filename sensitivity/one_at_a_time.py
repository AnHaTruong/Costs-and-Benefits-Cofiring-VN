# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# sensitivity_one_at_a_time
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Perform a sensitivity analysis, one parameter at a time.

For each parameter, we run the model using the low, central and high value;
keeping other parameters at their central value.
Sensitivity analysis starts with this method because it is the simplest and clearest.
  It requires 2N+1 model runs, where N is the number of parameters explored.
  Results can be represented clearly on a Tornado diagram.
  It does not show interactions between input variables.
  It does not explore the full input space.
For deeper analysis, the SALib package implements more complex methods.
"""

from pandas import DataFrame


def one_at_a_time(parameter_space, model):
    """Run the model 2N+1 times, to perform the one-at-a-time sensitivity analysis.

    Return results in a pair of dict of dict,
    because trying to store natu quantities in a DataFrame give cryptic errors.
    """
    result = {
        "business_value": parameter_space.to_dict(),
        "external_value": parameter_space.to_dict(),
    }

    baseline_x = parameter_space["Baseline"]
    baseline_business_value, baseline_external_value = model(baseline_x)

    for parameter in parameter_space.index:
        result["business_value"]["Baseline"][parameter] = baseline_business_value
        result["external_value"]["Baseline"][parameter] = baseline_external_value
        for bound in ["Low bound", "High bound"]:
            x = baseline_x.copy()
            x[parameter] = parameter_space.loc[parameter, bound]
            y1, y2 = model(x)
            result["business_value"][bound][parameter] = y1
            result["external_value"][bound][parameter] = y2
    return result


def table_sensitivity(uncertainty, model, name):
    """Return the two sensitivity analysis result tables, as a string."""
    run = one_at_a_time(uncertainty, model)
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
