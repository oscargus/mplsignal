[![Build status](https://github.com/oscargus/mplsignal/workflows/Tests/badge.svg)](https://github.com/oscargus/mplsignal/actions?query=workflow%3ATests)
[![License](https://img.shields.io/github/license/oscargus/mplsignal)](https://github.com/oscargus/mplsignal/blob/main/LICENSE)
# mplsignal

Matplotlib extension for signal processing

Documentation can be found [here](https://mplsignal.readthedocs.io/).

mplsignal currently consists of four main parts:

   * `plane_plots`: various `splane` and `zplane` for plotting pole-zero diagrams
   * `freq_plots`: various `freqs` and `freqz` methods for plotting magnitude and phase responses of transfer functions
   * `ticker`: tickers and formatters suitable for `freqs`/`freqz`-plots
   * `scipyplot`: convenience functions that can be directly fed to `scipy.signal.freqs` and ` scipy.signal.freqz`

## Installation

You can install using `pip`:

```bash
pip install mplsignal
```

## Development Installation


```bash
pip install -e ".[dev]"
```
