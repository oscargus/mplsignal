[![Build status](https://github.com/oscargus/mplsignal/workflows/Tests/badge.svg)](https://github.com/oscargus/mplsignal/actions?query=workflow%3ATests)
[![License](https://img.shields.io/github/license/oscargus/mplsignal)](https://github.com/oscargus/mplsignal/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mplsignal)](https://pypi.org/project/mplsignal/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/oscargus/mplsignal)](https://github.com/oscargus/mplsignal/releases)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/oscargus/mplsignal/latest)](https://github.com/oscargus/mplsignal/compare/v0.1.1...HEAD)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mplsignal)](https://pypi.org/project/mplsignal/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/mplsignal)](https://pypi.org/project/mplsignal/)
![GitHub top language](https://img.shields.io/github/languages/top/oscargus/mplsignal)

# mplsignal

Matplotlib extension for signal processing

Documentation can be found [here](https://mplsignal.readthedocs.io/).

mplsignal currently consists of four main parts:

   * `plane_plots`: various `splane` and `zplane` for plotting pole-zero diagrams
   * `freq_plots`: various `freqs` and `freqz` methods for plotting magnitude and phase responses of transfer functions
   * `ticker`: tickers and formatters suitable for `freqs`/`freqz`-plots
   * `scipyplot`: convenience functions that can be directly fed to `scipy.signal.freqs` and ` scipy.signal.freqz`

## Dependencies
mplsignal is only useful if you also have [Matplotlib](https://matplotlib.org/) installed.
In addition, it relies on [adjustText](https://adjusttext.readthedocs.io/) to position the multiplicity
numbers next to poles and zeros.

If [SciPy](https://scipy.org/) is installed, mplsignal will use some functions to compute frequency responses etc,
but mplsignal also has its own functions for this.

## Installation

You can install using `pip`:

```bash
pip install mplsignal
```

## Development Installation

```bash
pip install -e ".[dev]"
```

## Related work

In the meantime between starting working on mplsignal and finally getting around to make it public,
[zplane](https://pypi.org/project/zplane/) was released. This can do most things that mplsignal can do and a few more.
However, the configurability is larger for mplsignal and the tickers and locators are unique features.
