#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.
"""
The module contains utility functions to easily interact with SciPy.

The SciPy functions :func:`scipy.signal.freqs` and  :func:`scipy.signal.freqz`
have a `plot` argument to provide a plotting callback function.
The functions provided in this module is aimed to be used as such a callback.
"""
from .freq_plots import _plot_h


def freqz(w, h):
    """
    Utility function to easily plot the result from :func:`scipy.signal.freqz`.

    The magnitude and phase responses are plotted in two different subplots.

    Parameters
    ----------
    w : array-like
        Frequency points.
    h : array-like
        Transfer function evaluated at *w*.

    Returns
    -------
    None.

    See Also
    --------
    freqz_magnitude, freqz_phase, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz)
    """
    _plot_h(w, h)


def freqz_twin(w, h):
    """
    Utility function to easily plot the result from :func:`scipy.signal.freqz`.

    The magnitude and phase responses are plotted in the same plot using
    different y-axes.

    Parameters
    ----------
    w : array-like
        Frequency points.
    h : array-like
        Transfer function evaluated at *w*.

    Returns
    -------
    None.

    See Also
    --------
    freqz, freqz_magnitude, freqz_phase

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_twin)
    """
    _plot_h(w, h, style='twin')


def freqz_magnitude(w, h):
    """
    Utility function to easily plot the result from :func:`scipy.signal.freqz`.

    Only the magnitude is plotted.

    Parameters
    ----------
    w : array-like
        Frequency points.
    h : array-like
        Transfer function evaluated at *w*.

    Returns
    -------
    None.

    See Also
    --------
    freqz, freqz_phase, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_magnitude)
    """
    _plot_h(w, h, style='magnitude')


def freqz_phase(w, h):
    """
    Utility function to easily plot the result from :func:`scipy.signal.freqz`.

    Only the magnitude is plotted.

    Parameters
    ----------
    w : array-like
        Frequency points.
    h : array-like
        Transfer function evaluated at *w*.

    Returns
    -------
    None.

    See Also
    --------
    freqz, freqz_magnitude, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_phase)
    """
    _plot_h(w, h, style='phase')
