from datetime import date, timedelta
from pathlib import Path

import yaml


class InterestRates:
    FILE_PATH = 'interest_rates.yaml'

    """Class to represent historic interest rates for I Bonds."""
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

    def get_previous_rate_date(self, d):
        """Given a date d, returns the previous date when interest rates were
        changed.

        Args:
            d: A datetime.date object.
        """
        if d < date(1998, 11, 1):
            return date(1998, 9, 1)

        month = d.month
        if month >= 1 and month <= 4:
            return date(d.year - 1, 11, 1)
        if month >= 5 and month <= 10:
            return date(d.year, 5, 1)

        # month = 11 or 12
        return date(d.year, 11, 1)

    def get_latest_date(self):
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
        return self.get_previous_rate_date(last_date) in self.interest_rates


class IBonds:
    """Class representing an I Bond."""
    def __init__(self, issue_date, denom):
        """
        Args:
            issue_date: Issue date of an I Bond in MM/YYYY format.
            demon: Denomination of the I Bond.
        """
        pass
