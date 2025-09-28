# I Bonds

This is a python library that calculates the current value of a
[Series I Savings Bond](https://www.treasurydirect.gov/savings-bonds/i-bonds/).
The historic rates are supplied via a data file which is updated every time
a new rate is released by [Treasury Direct](https://www.treasurydirect.gov/).

## Installation

This project can be installed via [pip](https://pip.pypa.io/en/stable/).
To install the library, run:

```
pip install ibonds
```

## Example code
```python
from ibonds import IBond

ibond = IBond('01/2010', 10_000)  # $10,000 I-Bond bought in Jan 2010
print(f'Fixed Rate: {ibond.fixed_rate()}')
print(f'Current Composie Rate: {ibond.composite_rate()}')
print(f'Current value: {ibond.value()}')

from datetime import date  # For historic rates and values.

d = date(2020, 1, 1)  # Jan 1, 2020
print(f'Composie Rate on Jan 1, 2020: {ibond.composite_rate(d)}')
print(f'Value on Jan 1, 2020: {ibond.value(d)}')
```

If you are interested in tracking more than one I Bond, and would prefer
a command line interface, please check out
[lakshmi](https://github.com/sarvjeets/lakshmi). If you like a spreadsheet
instead, [eyebonds.info](https://eyebonds.info/) is a great resource.

## Acknowledgements
I would like to acknowledge [eyebonds.info](https://eyebonds.info/) and
[Bogleheads](https://www.bogleheads.org) websites which I used to understand
I Bond interest rate calculations.

## Disclaimer

This library has no link to official Treasury Direct website. No claim is
made for any accuracy of data that you generate using this code. Although
I have tried my best to implement the formula presented in Tresury Direct,
the values returned by this module might be incorrect. When in doubt, go to
the official Treasury Direct website to verify any and all information.
