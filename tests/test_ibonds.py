import unittest
from datetime import date

from ibonds import InterestRates

INTEREST_RATE_DATA = """2021-05-01:
- 0.00
- 1.77
2021-11-01:
- 0.00
- 3.56
2022-05-01:
- 0.00
- 4.81
2022-11-01:
- 0.40
- 3.24
"""


class IBondsTest(unittest.TestCase):
    def test_something(self):
        interest_rates = InterestRates(INTEREST_RATE_DATA)
        self.assertEqual(date(2022, 11, 1), interest_rates.get_latest_date())

    def test_previous_rate_date(self):
        i = InterestRates()
        self.assertEqual(i.get_previous_rate_date(date(1998, 10, 1)),
                         date(1998, 9, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 1, 10)),
                         date(1999, 11, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 2, 1)),
                         date(1999, 11, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 3, 1)),
                         date(1999, 11, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 4, 1)),
                         date(1999, 11, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 5, 1)),
                         date(2000, 5, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 6, 1)),
                         date(2000, 5, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 7, 1)),
                         date(2000, 5, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 8, 1)),
                         date(2000, 5, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 9, 1)),
                         date(2000, 5, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 10, 1)),
                         date(2000, 5, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 11, 1)),
                         date(2000, 11, 1))
        self.assertEqual(i.get_previous_rate_date(date(2000, 12, 1)),
                         date(2000, 11, 1))

    def test_is_current(self):
        i = InterestRates(INTEREST_RATE_DATA)  # Latest date: 2022-11-01

        self.assertTrue(i.is_current(within_days=0, today=date(2022, 12, 1)))
        self.assertTrue(i.is_current(within_days=1, today=date(2023, 5, 1)))
        self.assertTrue(i.is_current(within_days=2, today=date(2023, 5, 2)))
        self.assertFalse(i.is_current(within_days=1, today=date(2023, 5, 2)))
        self.assertFalse(i.is_current(within_days=60, today=date(2023, 11, 1)))

    def test_get_rates(self):
        i = InterestRates(INTEREST_RATE_DATA)
        self.assertEquals(0.4, i.get_fixed_rate(date(2023, 4, 7)))
        self.assertEquals(3.24, i.get_inflation_rate(date(2023, 4, 7)))
        self.assertEquals(6.89, i.get_composite_rate(0.4, date(2023, 4, 7)))
