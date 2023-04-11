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
