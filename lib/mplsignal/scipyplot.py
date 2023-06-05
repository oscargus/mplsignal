#!/usr/bin/env python

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.
"""
The module contains utility functions to easily interact with SciPy.

The SciPy functions :func:`scipy.signal.freqs` and  :func:`scipy.signal.freqz` have a
*plot* argument to provide a plotting callback function. The functions provided in this
module is aimed to be used as such a callback. The focus is to make a plot that can be
used to see the results clearly and quickly. For publication quality plots, the
functions in :mod:`~mplsignal.freq_plots` are generally preferred.
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
    freqz_magnitude, freqz_phase, freqz_tristacked, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz)
    """
    fig = _plot_h(w, h)
    fig.set_layout_engine("constrained")


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
    freqz, freqz_magnitude, freqz_phase, freqz_tristacked

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_twin)
    """
    fig = _plot_h(w, h, style='twin')
    fig.set_layout_engine("constrained")
    fig.legend(ncols=2, loc='upper center')


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
    freqz, freqz_phase, freqz_tristacked, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_magnitude)
    """
    fig = _plot_h(w, h, style='magnitude')
    fig.set_layout_engine("constrained")


def freqz_phase(w, h):
    """
    Utility function to easily plot the result from :func:`scipy.signal.freqz`.

    Only the phase is plotted.

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
    freqz, freqz_magnitude, freqz_tristacked, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_phase)
    """
    fig = _plot_h(w, h, style='phase')
    fig.set_layout_engine("constrained")


def freqz_tristacked(w, h):
    """
    Utility function to easily plot the result from :func:`scipy.signal.freqz`.

    The magnitude, phase, and group delay responses are plotted in three different
    subplots.

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
    freqz, freqz_magnitude, freqz_phase, freqz_twin

    Examples
    --------
    >>> from scipy import signal
    ... from mplsignal import scipyplot
    ...
    ... signal.freqz([1, 1, 1, 1], plot=scipyplot.freqz_tristacked)
    """
    fig = _plot_h(w, h, style='tristacked')
    fig.set_layout_engine("constrained")
