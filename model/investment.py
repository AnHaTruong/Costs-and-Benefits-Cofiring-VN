# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Class for business analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Provide financial project management accounting."""

import pandas as pd
import natu.numpy as np
from model.utils import USD, kUSD, after_invest, display_as, isclose


class Investment:
    """Financial project accounting: NPV after revenue, operating expenses, amortization and taxes.

    The capital investment is made in period 0,
    revenue, operating expenses and taxes occur in subsequent periods
    Taxes account for linear amortization of the capital starting period 1
    No salvage value

    Virtual class: descendent class should redefine  operating_expense()  to
        return a vector of quantities of size time_horizon+1
        which has the display unit set to kUSD

    The  revenue  must be set after the investment is initialized.
        This is so because the code that set the revenue can also
        set it as an expense to another object.

    >>> i = Investment('test', 20)
    >>> i.revenue()
    Traceback (most recent call last):
        ...
    AttributeError: Accessing  Investment.revenue  value before it is set

    >>> i.revenue = after_invest(3000 * USD, 20)
    >>> # set the costs of whoever is paying the 3000 USD per year
    >>> i.revenue
    array([0 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD,
           3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD,
           3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD, 3 kUSD], dtype=object)

    >>> i = Investment("test", 20, 1000*USD)
    >>> i.revenue = np.zeros(21) * USD
    >>> i.net_present_value(0, 0, 10)
    -1 kUSD
    """

    def __init__(self, name, time_horizon, capital=0 * USD):
        self.capital = display_as(capital, 'kUSD')
        self.name = name
        self.time_horizon = time_horizon
        self._revenue = None
        self.costs_of_goods_sold = display_as(np.zeros(self.time_horizon + 1) * USD, 'kUSD')
        self.expenses = []
        self.expenses_index = []

    @property
    def revenue(self):
        if self._revenue is None:
            raise AttributeError('Accessing  Investment.revenue  value before it is set')
        return display_as(self._revenue, 'kUSD')

    @revenue.setter
    def revenue(self, value):
        self._revenue = value

    def investment(self):
        """Multi year investment possible.

        But code outside this module assume it occurs only in  year 0.
        """
        v_invest = 1 - after_invest(1, self.time_horizon)
        return display_as(v_invest * self.capital / sum(v_invest), 'kUSD')

    def operating_expenses(self):
        return display_as(np.zeros(self.time_horizon + 1) * USD, 'kUSD')

    def amortization(self, depreciation_period):
        """Return vector of linear amortization amounts."""
        if not self.capital:
            return display_as(np.zeros(self.time_horizon + 1) * USD, 'kUSD')
        assert isinstance(depreciation_period, int), "Depreciation period not an integer"
        assert depreciation_period > 0, "Depreciation period negative"
        assert depreciation_period < self.time_horizon - 1, "Depreciation >= timehorizon - 2 year"
        v_cost = np.zeros(self.time_horizon + 1).copy() * USD
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.capital / float(depreciation_period)
        return display_as(v_cost, 'kUSD')

    def earning_before_tax(self, depreciation_period=None):
        """Return  EBT vector."""
        earning = (self.revenue
                   - self.costs_of_goods_sold
                   - self.operating_expenses()
                   - self.amortization(depreciation_period))
        return display_as(earning, 'kUSD')

    def income_tax(self, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        tax = tax_rate * self.earning_before_tax(depreciation_period)
        return display_as(tax, 'kUSD')

    def cash_out(self, tax_rate, depreciation_period):
        """Return cash out vector."""
        flow = (self.investment()
                + self.costs_of_goods_sold
                + self.operating_expenses()
                + self.income_tax(tax_rate, depreciation_period))
        return display_as(flow, 'kUSD')

    def net_cash_flow(self, tax_rate, depreciation_period):
        flow = (self.revenue
                - self.cash_out(tax_rate, depreciation_period))
        return display_as(flow, 'kUSD')

    def net_present_value(self, discount_rate, tax_rate=0, depreciation_period=1):
        assert 0 <= discount_rate < 1, "Discount rate not in [0, 1["
        value = np.npv(discount_rate,
                       self.net_cash_flow(tax_rate, depreciation_period))
        return display_as(value, 'kUSD')

    def internal_rate_of_return(self):
        pass

    def payback_period(self):
        pass

    def table(self, tax_rate=0.25, depreciation_period=10):
        """Tabulate the characteristics of the investment, returning an np.array."""
        result = np.array([self.revenue,
                          self.investment(),
                          self.amortization(depreciation_period),
                          self.costs_of_goods_sold,
                          self.operating_expenses(),
                          self.earning_before_tax(depreciation_period),
                          self.income_tax(tax_rate, depreciation_period),
                          self.cash_out(tax_rate, depreciation_period),
                          self.net_cash_flow(tax_rate, depreciation_period)])
        return result

    def pretty_table(self, discount_rate, tax_rate, depreciation_period):
        """Tabulate the characteristics of the investment, returning a multiline string."""
        lines = [self.name]
        lines.append("NPV  = " + str(self.net_present_value(discount_rate,
                                                            tax_rate,
                                                            depreciation_period)))
        table = self.table(tax_rate, depreciation_period)
        table = np.transpose(table)
        labels = ["Revenue",
                  "Investment",
                  "Amortization",
                  "Cost of goods",
                  "Op. Expense",
                  "Earn. B. Tax",
                  "Income tax",
                  "Cash out",
                  "Net cashflow"
                  ]
        result = pd.DataFrame(table, columns=labels)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 150)
        lines.append(str(result))
        return '\n'.join(lines)

    def earning_before_tax_detail(self):
        """Tabulate the earning before taxes (there are no interests)."""
        sales = pd.Series([self.revenue[1]], ['Sales revenue'])
        cash_flows = sales.append(- pd.Series(self.expenses, self.expenses_index))
        df = pd.DataFrame(data=[cash_flows / kUSD], index=["kUSD"])
        df["= Earning Before Tax"] = df.sum(axis=1)

        a = self.earning_before_tax()[1] / kUSD
        b = df.loc["kUSD", "= Earning Before Tax"]
        assert isclose(a, b), "Inconsistent EBT estimates"

        return df.T
