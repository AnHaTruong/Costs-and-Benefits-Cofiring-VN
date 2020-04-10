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
from sensitivity.blackbox import uncertainty, business_value as f


#%% Display the parameters

df = pd.DataFrame(
    data=uncertainty["lomidhi"],
    index=uncertainty["names"],
    columns=["Low bound", "Reference", "High bound"],
)

result = pd.DataFrame().reindex_like(df)

#%% The runs

range_vars = range(uncertainty["num_vars"])


def parameters(index):
    """Return the list of parameters choosen by the index.

    Denoting the model as y=f(x1, x2, .., xn), this function returns  [x1, ..., xn].
    Denoting the index as [i1, .., in],
    the value ik = 0, 1 or 2 selects if xi should have its low/reference/high value.
    """
    return [uncertainty["lomidhi"][k][index[k]] for k in range_vars]


# Central case is in-loop, not optimal doing 3 N runs instead of 2 N + 1.
for var in range_vars:
    for col in [0, 1, 2]:
        index = [1, 1, 1, 1]
        index[var] = col
        x = parameters(index)
        y = f(*x)
        result.iloc[var, col] = display_as(y * USD, "MUSD")


#%% Tabulate

print("Sensitivity analysis, one parameter at a time")
print()
print("Parameters values for the sensitivity analysis.")
print(df)
print()
print("Result: business value.")
print(result)
