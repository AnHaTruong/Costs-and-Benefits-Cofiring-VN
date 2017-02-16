# Economic of co-firing in two power plants in Vietnam
#
# Class for business analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_horizon, v_zeros, USD, as_kUSD
import natu.numpy as np
import pandas as pd


class Investment:
    """An investment of capital paid in period 0,
        There are income, operating expenses and taxes in subsequent periods
        Taxes account for linear amortization of the capital starting period 1
        No salvage value
       Virtual class,
        descendent class should redefine  income()  and  operating_expense()
        These functions should return a vector of numbers like v_zeros
    """
    def __init__(self, capital=0*USD):
        self.capital = capital
        self.capital.display_unit = 'kUSD'
        self.investment = as_kUSD(v_zeros.copy()*USD)
        self.investment[0] = capital

    def income(self):
        return as_kUSD(v_zeros * USD)

    def operating_expenses(self):
        return as_kUSD(v_zeros * USD)

    def amortization(self, depreciation_period):
        assert type(depreciation_period) is int, "Depreciation period not an integer"
        assert 0 < depreciation_period < time_horizon - 1, "Depreciation not in {1..timehorizon-1}"
        v_cost = v_zeros.copy()*USD
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.capital / float(depreciation_period)
        return as_kUSD(v_cost)

    def earning_before_tax(self, depreciation_period):
        return as_kUSD(self.income() -
                       self.operating_expenses() -
                       self.amortization(depreciation_period)
                       )

    def income_tax(self, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        return as_kUSD(tax_rate * self.earning_before_tax(depreciation_period))

    def net_cash_flow(self, tax_rate, depreciation_period):
        return as_kUSD(self.income() -
                       self.investment -
                       self.operating_expenses() -
                       self.income_tax(tax_rate, depreciation_period)
                       )

    def net_present_value(self, discount_rate, tax_rate, depreciation_period):
        assert 0 <= discount_rate < 1, "Discount rate not in [0, 1["
        return np.npv(discount_rate, self.net_cash_flow(tax_rate, depreciation_period))

    def internal_rate_of_return(self):
        pass

    def payback_period(self):
        pass

    def table(self, tax_rate, depreciation_period):
        t = np.array([self.investment,
                      self.income(),
                      self.operating_expenses(),
                      self.amortization(depreciation_period),
                      self.earning_before_tax(depreciation_period),
                      self.income_tax(tax_rate, depreciation_period),
                      self.net_cash_flow(tax_rate, depreciation_period)
                      ]
                     )
        return t

    def pretty_table(self, tax_rate, depreciation_period):
        t = self.table(tax_rate, depreciation_period)
        t = np.transpose(t)
        labels = ["Investment",
                  "Income",
                  "Op. Expense",
                  "Amortization",
                  "Earn. B. Tax",
                  "Income tax",
                  "Net cashflow"
                  ]
        t = pd.DataFrame(t, columns=labels)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 150)
        print(t)
        return t
