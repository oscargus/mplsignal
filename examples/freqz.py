"""
-----------------
``freqz`` Example
-----------------

A short example showcasing how to use :func:`~mplsignal.freq_plots.freqz`.
"""

from mplsignal import freqz

num = [1 / 3, 1 / 3, 1 / 3]
den = [1, -1.2, -0.5]
fig = freqz(num=num, den=den)
fig.show()
