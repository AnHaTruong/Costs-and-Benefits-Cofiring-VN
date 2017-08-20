# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Class for business analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Provide financial project management accounting."""

import pandas as pd
import natu.numpy as np
from init import TIMEHORIZON, ZEROS, USD, after_invest, display_as


class Investment:
    """Financial project accounting: NPV after revenue, operating expenses, amortization and taxes.

    The capital investment is made in period 0,
    revenue, operating expenses and taxes occur in subsequent periods
    Taxes account for linear amortization of the capital starting period 1
    No salvage value

    Virtual class: descendent class should redefine  operating_expense()  to
        return a vector of quantities of size TIMEHORIZON+1
        which has the display unit set to kUSD

    The  revenue  must be set after the investment is initialized
        This is so because the code that set the revenue can also
        set it as an expense to another object.

    >>> from init import ZEROS
    >>> i = Investment("test", 1000*USD)
    >>> i.revenue = ZEROS * USD
    >>> i.net_present_value(0, 0, 10)
    -1 kUSD
    """

    def __init__(self, name, capital=0 * USD):
        self.capital = display_as(capital, 'kUSD')
        self.name = name
        self._revenue = None

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
        v_invest = 1 - after_invest(1)
        return display_as(v_invest * self.capital / sum(v_invest), 'kUSD')

    @staticmethod
    def operating_expenses():
        return display_as(ZEROS * USD, 'kUSD')

    def amortization(self, depreciation_period):
        """Return vector of linear amortization amounts."""
        assert isinstance(depreciation_period, int), "Depreciation period not an integer"
        assert 0 < depreciation_period < TIMEHORIZON - 1, "Depreciation not in {1..timehorizon-2}"
        v_cost = ZEROS.copy() * USD
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.capital / float(depreciation_period)
        return display_as(v_cost, 'kUSD')

    def earning_before_tax(self, depreciation_period):
        earning = (self.revenue
                   - self.operating_expenses()
                   - self.amortization(depreciation_period))
        return display_as(earning, 'kUSD')

    def income_tax(self, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        tax = tax_rate * self.earning_before_tax(depreciation_period)
        return display_as(tax, 'kUSD')

    def cash_out(self, tax_rate, depreciation_period):
        flow = (self.investment()
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
