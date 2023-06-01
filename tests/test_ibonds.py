import unittest
from datetime import date

from ibonds import IBond, InterestRates, _YearMonth

INTEREST_RATE_DATA = """
2020-11-01:
- 0.00
- 0.84
2021-05-01:
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
        self.assertEqual(date(2022, 11, 1), interest_rates.latest_date())

    def test_previous_rate_date(self):
        self.assertEqual(InterestRates.previous_rate_date(date(1998, 10, 1)),
                         date(1998, 9, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 1, 10)),
                         date(1999, 11, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 2, 1)),
                         date(1999, 11, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 3, 1)),
                         date(1999, 11, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 4, 1)),
                         date(1999, 11, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 5, 1)),
                         date(2000, 5, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 6, 1)),
                         date(2000, 5, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 7, 1)),
                         date(2000, 5, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 8, 1)),
                         date(2000, 5, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 9, 1)),
                         date(2000, 5, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 10, 1)),
                         date(2000, 5, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 11, 1)),
                         date(2000, 11, 1))
        self.assertEqual(InterestRates.previous_rate_date(date(2000, 12, 1)),
                         date(2000, 11, 1))

    def test_is_current(self):
        i = InterestRates(INTEREST_RATE_DATA)  # Latest date: 2022-11-01

        self.assertTrue(i.is_current(within_days=0, today=date(2022, 12, 1)))
        self.assertTrue(i.is_current(within_days=1, today=date(2023, 5, 1)))
        self.assertTrue(i.is_current(within_days=2, today=date(2023, 5, 2)))
        self.assertFalse(i.is_current(within_days=1, today=date(2023, 5, 2)))
        self.assertFalse(i.is_current(within_days=60, today=date(2023, 11, 1)))

    def test_rates(self):
        i = InterestRates()
        self.assertEqual(0.4, i.fixed_rate(date(2023, 4, 7)))
        self.assertEqual(3.24, i.inflation_rate(date(2023, 4, 7)))
        self.assertEqual(6.89, i.composite_rate(0.4, date(2023, 4, 7)))

    def test_rates_missing(self):
        i = InterestRates(INTEREST_RATE_DATA)
        self.assertIsNone(i.fixed_rate(date(2025, 1, 1)))
        self.assertIsNone(i.inflation_rate(date(2025, 1, 1)))
        self.assertIsNone(i.composite_rate(0, date(2025, 1, 1)))

    def test_ibond_init(self):
        i = InterestRates()
        IBond('05/2021', 10000, i)
        with self.assertRaises(AssertionError):
            IBond('01/1990', 25, i)

    def test_fixed_rate(self):
        ib = IBond('04/2023', 25)
        self.assertEqual(0.4, ib.fixed_rate())

    def test_composite_rate(self):
        ib = IBond('04/2023', 25)
        self.assertEqual(6.89, ib.composite_rate(date(2023, 4, 7)))

    def test_yearmonth(self):
        self.assertEqual(2, _YearMonth(2023, 5) - _YearMonth(2023, 3))
        self.assertEqual(1, _YearMonth(2023, 1) - _YearMonth(2022, 12))
        self.assertEqual(12 * 5, _YearMonth(2023, 1) - _YearMonth(2018, 1))
        self.assertEqual(-11, _YearMonth(2023, 1) - _YearMonth(2023, 12))

        d = _YearMonth(2022, 1) + 11
        self.assertEqual(date(2022, 12, 1), d.date())

        d = _YearMonth(2022, 12) + 1
        self.assertEqual(date(2023, 1, 1), d.date())

        d = _YearMonth(2022, 11) + 6
        self.assertEqual(date(2023, 5, 1), d.date())

    def test_ibond_composite_rate(self):
        i = InterestRates(INTEREST_RATE_DATA)
        ib = IBond('01/2021', 100, i)
        self.assertEqual(6.48, ib.composite_rate(date(2023, 5, 1)))
        self.assertIsNone(ib.composite_rate(date(2023, 7, 1)))

    def test_value_with_bad_date(self):
        with self.assertRaisesRegex(
            AssertionError, 'Cannot compute value on 2023-03-12 which is '
                            'before the issue date 2023-04-01'):
            IBond('04/2023', 25, InterestRates()).value(date(2023, 3, 12))

    def test_value(self):
        ib = IBond('01/2022', 1000)
        self.assertEqual(1000, ib.value(date(2022, 1, 1)))
        self.assertEqual(1000, ib.value(date(2022, 2, 2)))
        self.assertEqual(1085.60, ib.value(date(2023, 4, 1)))

        ib = IBond('04/2018', 1000)
        self.assertEqual(1184.80, ib.value(date(2023, 4, 1)))
        self.assertEqual(1223.60, ib.value(date(2023, 10, 1)))

        ib = IBond('09/1998', 10000)
        self.assertEqual(43240, ib.value(date(2023, 9, 1)))
