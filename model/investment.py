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

from abc import abstractmethod

from pandas import Series, DataFrame
from natu.numpy import zeros, npv
from model.utils import USD, after_invest, display_as, isclose


class Investment:
    """Financial project accounting: NPV after revenue, operating expenses, amortization and taxes.

    The investment is made in period 0,
    revenue, operating expenses and taxes occur in subsequent periods
    Taxes account for linear amortization of the amount invested starting period 1
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
    >>> i.revenue = zeros(21) * USD
    >>> i.net_present_value(0, 0, 10)
    -1 kUSD
    """

    def __init__(self, name, time_horizon, amount_invested=0 * USD):
        self.amount_invested = display_as(amount_invested, 'kUSD')
        self.name = name
        self.time_horizon = time_horizon
        self._revenue = None
        self.merchandise = display_as(zeros(self.time_horizon + 1) * USD, 'kUSD')
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
        return display_as(v_invest * self.amount_invested / sum(v_invest), 'kUSD')

    def operating_expenses(self):
        return display_as(zeros(self.time_horizon + 1) * USD, 'kUSD')

    def amortization(self, depreciation_period):
        """Return vector of linear amortization amounts."""
        if not self.amount_invested:
            return display_as(zeros(self.time_horizon + 1) * USD, 'kUSD')
        assert isinstance(depreciation_period, int), "Depreciation period not an integer"
        assert depreciation_period > 0, "Depreciation period negative"
        assert depreciation_period < self.time_horizon - 1, "Depreciation >= timehorizon - 2 year"
        v_cost = zeros(self.time_horizon + 1).copy() * USD
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.amount_invested / float(depreciation_period)
        return display_as(v_cost, 'kUSD')

    def earning_before_tax(self, depreciation_period=None):
        """Return  EBT time series."""
        ebt = (self.revenue
               - self.merchandise
               - self.operating_expenses()
               - self.amortization(depreciation_period))
        return display_as(ebt, 'kUSD')

    def income_tax(self, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        tax = tax_rate * self.earning_before_tax(depreciation_period)
        return display_as(tax, 'kUSD')

    def earning_after_tax(self, tax_rate, depreciation_period=None):
        """Return  EAT  time series."""
        eat = (self.earning_before_tax(depreciation_period)
               - self.income_tax(tax_rate, depreciation_period))
        return display_as(eat, 'kUSD')

    def cash_out(self, tax_rate, depreciation_period):
        """Return cash out time series."""
        flow = (self.investment()
                + self.merchandise
                + self.operating_expenses()
                + self.income_tax(tax_rate, depreciation_period))
        return display_as(flow, 'kUSD')

    def net_cash_flow(self, tax_rate, depreciation_period):
        flow = (self.revenue
                - self.cash_out(tax_rate, depreciation_period))
        return display_as(flow, 'kUSD')

    def result_economic(self, tax_rate, depreciation_period):
        """Return a DataFrame with the annual economic accounts, by year.

        Amortize the investment over N periods.
        """
        data = [
            self.revenue,
            self.amortization(depreciation_period),
            self.merchandise,
            self.operating_expenses(),
            self.earning_before_tax(depreciation_period),
            self.income_tax(tax_rate, depreciation_period),
            self.earning_after_tax(tax_rate, depreciation_period)]
        index = [
            "Revenue (kUSD)",
            "- Expense, Amortization",
            "- Expense, Merchandise",
            "- Expense, Operating",
            "= Earnings Before Tax",
            "- Income tax " + str(round(100 * tax_rate)) + '%',
            "= Earnings after tax"]
        return DataFrame(data, index=index)

    def result_cash(self, tax_rate, depreciation_period):
        """Return a DataFrame detailing the cash flow annual result, by year.

        Assume investment is paid in full in year 0.
        """
        data = [
            self.revenue,
            self.investment(),
            self.merchandise,
            self.operating_expenses(),
            self.income_tax(tax_rate, depreciation_period),
            self.net_cash_flow(tax_rate, depreciation_period)]
        index = [
            "Revenue (kUSD)",
            "- Expense, Investment",
            "- Expense, Merchandise",
            "- Expense, Operating",
            "- Expense, Income tax",
            "= Net cashflow"]
        return DataFrame(data, index=index)

    def business_data(self, tax_rate, depreciation_period):
        """Return a sequence of  DataFrames  detailing the business data, by year.

        The first dataframe is the economic result, it amortizes the investment over N periods.
        The second dataframe is the cash flow result, assumes investment is paid in full in year 0.
        The third dataframe is the detail of operating expenses: fuel, labor, tools.
        """
        return (self.result_economic(tax_rate, depreciation_period),
                self.result_cash(tax_rate, depreciation_period),
                self.operating_expenses_detail())

    def npv_cash(self, discount_rate, tax_rate, depreciation_period, label=""):
        """Return a Series. Cash flow statement, net present value."""
        cash_result = self.result_cash(tax_rate, depreciation_period)
        data = cash_result.apply((lambda x: npv(discount_rate, x)), axis=1)
        table = Series(data)
        assert isclose(
            self.net_present_value(discount_rate, tax_rate, depreciation_period),
            data.loc['= Net cashflow'])
        table.name = self.name if label == "" else label
        return table

    def npv_opex(self, discount_rate, label=""):
        """Return a Series. Operating expenses statement, net present value."""
        opex = self.operating_expenses_detail()
        data = opex.apply((lambda x: npv(discount_rate, x)), axis=1)
        table = Series(data)
        table.name = self.name if label == "" else label
        return table

    def net_present_value(self, discount_rate, tax_rate=0, depreciation_period=1):
        assert 0 <= discount_rate < 1, "Discount rate not in [0, 1["
        value = npv(discount_rate,
                    self.net_cash_flow(tax_rate, depreciation_period))
        return display_as(value, 'kUSD')

    def internal_rate_of_return(self):
        pass

    def payback_period(self):
        pass

    @abstractmethod
    def operating_expenses_detail(self):
        """Return a dataframe detailing the operating expenses (rows) by year (columns).

        This is a virtual method since each child class has different kind of OPEX.
        Declared abstract so that PyLint does not complain about 'lack of self use'.
        Return an empty DataFrame because PyLint typecheck when we use apply() in npv_opex method.
        """
        return DataFrame()
