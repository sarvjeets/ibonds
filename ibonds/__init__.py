from datetime import date, datetime, timedelta
from pathlib import Path

import requests
import yaml


class InterestRates:
    """Class to represent historic interest rates for I Bonds."""
    FILE_PATH = 'interest_rates.yaml'

    @classmethod
    def latest_rates_data(cls):
        """Download the latest interest rates data from this project'ss github
        repo."""
        r = requests.get('https://raw.githubusercontent.com/sarvjeets/'
                         'ibonds/main/ibonds/interest_rates.yaml')
        r.raise_for_status()
        return r.text

    def __init__(self, interest_rate_data=None):
        """
            Args:
                interest_rate_data: A string containing the contents of the
                interest rate file. Useful for testing or providing your
                own interest rates to this class.
        """
        if not interest_rate_data:
            f = Path(__file__).resolve().parent / InterestRates.FILE_PATH
            interest_rate_data = f.read_text()
        self.interest_rates = yaml.safe_load(interest_rate_data)

    @classmethod
    def previous_rate_date(cls, d):
        """Given a date d, returns the previous date when interest rates were
        changed.

        Args:
            d: A datetime.date object.
        """
        assert d >= date(1998, 9, 1)

        if d < date(1998, 11, 1):
            return date(1998, 9, 1)

        month = d.month
        if month >= 1 and month <= 4:
            return date(d.year - 1, 11, 1)
        if month >= 5 and month <= 10:
            return date(d.year, 5, 1)
        # month = 11 or 12
        return date(d.year, 11, 1)

    def latest_date(self):
        return max(self.interest_rates.keys())

    def is_current(self, within_days=1, today=date.today()):
        """Returns where the interest rates are current.

        Args:
            within_days: The interest rates are considered current if it is
            within within_days interval.
            today: A datetime.date object representing current date. Exposed
            here for testing.
        """
        last_date = today - timedelta(days=within_days)
        return self.previous_rate_date(last_date) in self.interest_rates

    def fixed_rate(self, d):
        """Get fixed ratei (in %) as of date d. Returns None if interest
        rate is not present in interest rates file/date provided to this
        class.
        """
        pre_date = self.previous_rate_date(d)
        if pre_date not in self.interest_rates:
            return None
        return self.interest_rates.get(self.previous_rate_date(d))[0]

    def inflation_rate(self, d):
        """Get inflation rate (in %) as of date d. Returns None if interest
        rate is not present in interest rates file/date provided to this
        class.
        """
        pre_date = self.previous_rate_date(d)
        if pre_date not in self.interest_rates:
            return None
        return self.interest_rates[self.previous_rate_date(d)][1]

    def composite_rate(self, fixed_rate, d):
        """Return the composite rate for I bond with fixed_rate on date d."""
        inflation_rate = self.inflation_rate(d)

        if not inflation_rate:
            return None

        f = fixed_rate / 100.0
        i = inflation_rate / 100.0
        r = (f + (2 * i) + (f * i)) * 100.0
        if r > 0:
            return round(r, 2)
        return 0.0  # Composite rate can't be below zero.


class _YearMonth:
    """Internal class to help with I bond value calculations."""
    def __init__(self, year, month):
        self.month = month
        self.year = year

    def __sub__(self, other):
        """Returns the number of months in self - other."""
        return (self.year - other.year) * 12 + (self.month - other.month)

    def __add__(self, months):
        """Adds months to self."""
        new_val = _YearMonth(self.year, self.month)
        new_val.month += months
        new_val.year += (new_val.month - 1) // 12
        new_val.month = ((new_val.month - 1) % 12) + 1
        return new_val

    def date(self):
        """Converts self to a date object."""
        return date(self.year, self.month, 1)


class IBond:
    """Class representing an I Bond."""
    def __init__(self, issue_date, denom, interest_rates=InterestRates()):
        """
        Args:
            issue_date: Issue date of an I Bond in MM/YYYY format.
            demon: Denomination of the I Bond.
            interest_rates: An initialized object of type InterestRates.
        """
        self.issue_date = datetime.strptime(issue_date, '%m/%Y').date()
        assert self.issue_date >= date(1998, 9, 1)
        self.denom = denom
        self.interest_rates = interest_rates

    def fixed_rate(self):
        """Returns fixed rate (in %) of this I Bond."""
        rate = self.interest_rates.fixed_rate(self.issue_date)
        assert rate is not None, ('Cannot find fixed rate for I Bond with '
                                  f'issue date {self.issue_date}')
        return rate

    def composite_rate(self, d=date.today()):
        """Returns composite rate (in %) of this I Bond on date d. Returns None
        if interest rate is not present in interest rates provided to this
        class.
        """
        current_month = _YearMonth(d.year, d.month)
        age_months = (current_month - _YearMonth(self.issue_date.year,
                                                 self.issue_date.month))
        rate_change_month = current_month + (- (age_months % 6))
        return self.interest_rates.composite_rate(self.fixed_rate(),
                                                  rate_change_month.date())

    def value(self, d=date.today()):
        """Returns value of this I Bond on date d."""
        assert (d - self.issue_date) >= timedelta(days=0), (
            f'Cannot compute value on {d} which is before the issue date '
            f'{self.issue_date}')

        # All bond values are multiple of $25 bond.
        value_25 = 25.0
        value_on = _YearMonth(self.issue_date.year, self.issue_date.month)
        months_left = _YearMonth(d.year, d.month) - value_on
        months_left = min(months_left, 12 * 30)  # No interest after 30 yrs.

        if months_left < 12 * 5:   # 5 year penalty
            months_left -= 3
            if months_left < 0:
                months_left = 0

        # Rate changes every 6 months. Interest accrues monthly and compounds
        # semiannually.
        while months_left >= 6:
            r = self.composite_rate(value_on.date())
            value_25 = round(value_25 * (1 + r / 200.0), 2)
            value_on = value_on + 6
            months_left -= 6

        if months_left > 0:
            # Make the last adjustment.
            r = self.composite_rate(value_on.date())
            value_25 = round(value_25 * (1 + r / 200.0) ** (months_left / 6.0),
                             2)

        return value_25 * (self.denom / 25.0)
