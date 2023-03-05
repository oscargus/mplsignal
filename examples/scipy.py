"""
---------------------
``scipyplot`` example
---------------------

This example illustrates how the :mod:`mplsignal.scipyplot` module provides functions
to be used for the *plot* argument to, e.g., :func:`scipy.signal.freqz`.
"""

import matplotlib.pyplot as plt
from mplsignal.scipyplot import freqz
from scipy import signal

b, a = signal.ellip(7, 1, 60, 0.4)
h, w = signal.freqz(b, a, plot=freqz)
plt.show()

# %%
# There are other functions with different plot formats

from mplsignal.scipyplot import freqz_twin

plt.figure()
h, w = signal.freqz(b, a, plot=freqz_twin)
