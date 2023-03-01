"""
---------------------------------------
``freqz`` frequency unit format example
---------------------------------------

This example illustrates the effect of the *freq_units* argument of
:func:`~mplsignal.freq_plots.freqz` and related methods.

Here, :func:`~mplsignal.freq_plots.freqz_fir` is used as we deal with an FIR filter.
"""

import matplotlib.pyplot as plt
from scipy.signal import remez

from mplsignal.freq_plots import freqz_fir

fig, ax = plt.subplots(5, 1, figsize=(6.4, 10), layout='compressed')

h = remez(31, [0, 0.2, 0.25, 0.5], [1, 0])

for i, freq_unit in enumerate(('rad', 'deg', 'norm', 'fs', 'normfs')):
    freqz_fir(h, freq_unit=freq_unit, style='magnitude', ax=ax[i], fs=1000)

fig.show()

# %%
# It is also possible to get rational multiples of :math:`\pi` by using
# :class:`~mplsignal.ticker.PiRationalFormatter` as formatter. In the phase plot,
# *pi_always_in_numerator* is set to False to illustrate the difference.

from mplsignal.ticker import PiRationalFormatter

fig, ax = plt.subplots(2, 1, layout='compressed')
freqz_fir(h, ax=ax)
ax[0].xaxis.set_major_formatter(PiRationalFormatter())
ax[1].xaxis.set_major_formatter(PiRationalFormatter(pi_always_in_numerator=False))

fig.show()
