"""
--------------------------
``freqz`` *style* examples
--------------------------

There are a number of different styles available when using
:func:`~mplsignal.freq_plots.freqz` and related methods.

The currently available styles are:

    * ``'stacked'`` - Magnitude and phase in two separate subplots (default)
    * ``'twin'`` - Magnitude and phase in same plot
    * ``'magnitude'`` - Magnitude
    * ``'phase'`` - Phase
    * ``'group_delay'`` - Group delay
    * ``'tristacked'`` - Magnitude, phase, and group delay in three separate subplots
"""

import matplotlib.pyplot as plt
from scipy import signal

from mplsignal import freqz

b, a = signal.ellip(7, 1, 60, 0.4)

for style in ('stacked', 'twin', 'magnitude', 'phase', 'group_delay', 'tristacked'):
    plt.figure()
    fig = freqz(num=b, den=a, style=style)
    fig.suptitle(f"style={style!r}")
    fig.show()
