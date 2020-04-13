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

import pandas as pd

from model.utils import display_as, USD
from sensitivity.blackbox import uncertainty, multi_objectives, business_value as f


#%% Display the parameters

df = pd.DataFrame(
    data=uncertainty["lomidhi"],
    index=uncertainty["names"],
    columns=["Low bound", "Reference", "High bound"],
)

result_business_value = pd.DataFrame().reindex_like(df)
result_business_value2 = pd.DataFrame().reindex_like(df)
result_external_value = pd.DataFrame().reindex_like(df)

#%% The runs

n_params = uncertainty["num_vars"]
range_vars = range(n_params)


def parameters(levels):
    """Return the list of parameters choosen by the index.

    Denoting the model as y=f(x1, x2, .., xn), this function returns  [x1, ..., xn].
    Denoting the levels as [i1, .., in],
    the value ik = 0, 1 or 2 selects if xi should have its low/reference/high level.
    """
    return [uncertainty["lomidhi"][k][levels[k]] for k in range_vars]


# Central case is in-loop, not optimal doing 3 N runs instead of 2 N + 1.
for var in range_vars:
    for col in [0, 1, 2]:
        index = [1] * n_params
        index[var] = col
        x = parameters(index)
        y = f(*x)
        result_business_value.iloc[var, col] = display_as(y * USD, "MUSD")


# Central case is in-loop, not optimal doing 3 N runs instead of 2 N + 1.
for var in range_vars:
    for col in [0, 1, 2]:
        index = [1] * n_params
        index[var] = col
        x = parameters(index)
        y1, y2 = multi_objectives(*x)
        result_business_value2.iloc[var, col] = display_as(y1 * USD, "MUSD")
        result_external_value.iloc[var, col] = display_as(y2 * USD, "MUSD")


#%% Tabulate

print("Sensitivity analysis, one parameter at a time")
print()
print("Parameters values for the sensitivity analysis.")
print(df)
print()
print("Result: business value.")
print(result_business_value)
print()
print("Result: business value.")
print(result_business_value2)
print()
print("Result: external value.")
print(result_external_value)
