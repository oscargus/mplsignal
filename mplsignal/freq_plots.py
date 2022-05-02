#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "freqz",
    "freqz_tf",
    "freqz_fir",
]
import numpy as np
import matplotlib.pyplot as plt
from mplsignal import _utils
from mplsignal.ticker import PiFormatter, PiLocator


def freqz(
    num=None,
    den=None,
    zeros=None,
    poles=None,
    gain=1,
    w=None,
    freq_units='rad',
    phase_units='rad',
    ax=None,
    style=None,
    **kwargs,
):
    r"""
    Plot the frequency response of a discrete-time system.

    Parameters
    ----------
    num : array-like, optional
        Numerator of transfer function.
    den : array-like, optional
        Denominator of transfer function.
    zeros : array-like, optional
        Zeros of transfer function.
    poles : array-like, optional
        Poles of transfer function.
    gain : float, optional
        The gain of pole-zero-based transfer function.
    w : integer or array-like, optional
        If a single integer, compute at that many frequency points in the
        range :math:`[0, \pi]`. Default: 512.
        If array-like, frequencies to determine transfer function at.
    freq_units : {'rad', 'deg', 'norm'}. Default: 'rad'
        Units for frequency axes--.
    phase_units : {'rad', 'deg'}. Default: 'rad'
        Units for frequency axes.
    ax : `Axes`, optional
        Axes to plot in.
    style : {'stacked', 'twin', 'magnitude', 'phase'}
        Plotting style.
    **kwargs
        Additional arguments.

    Returns
    -------
    None.

    """
    # if Axes not provided

    if num is None and zeros is None:
        raise ValueError("At least one of 'num' and 'zeros' must be provided.")

    if num is not None and zeros is not None:
        raise ValueError("At most one of 'num' and 'zeros' must be provided.")

    if den is None and poles is None:
        raise ValueError("At least one of 'den' and 'poles' must be provided.")

    if den is not None and poles is not None:
        raise ValueError("At most one of 'den' and 'poles' must be provided.")

    if w is None:
        w = 512

    if style is None:
        style = 'stacked'

    if isinstance(w, int):
        w = np.linspace(0, np.pi, w)

    if num is not None and den is not None:
        _, h = _utils.freqz_tf(num, den, w)

    if zeros is not None and poles is not None and gain is not None:
        _, h = _utils.freqz_zpk(zeros, poles, gain, w)

    return _plot_h(w, h, ax=ax, style=style, **kwargs)


def _plot_h(w, h, ax=None, style='stacked', **kwargs):
    if style != 'phase':
        magnitude = 20 * np.log10(np.abs(h))
    if style != 'magnitude':
        phase = np.unwrap(np.angle(h))
    minx = w.min()
    maxx = w.max()
    maglabel = kwargs.get('maglabel', 'Magnitude, dB')
    phaselabel = kwargs.get('phaselabel', 'Phase, rad')
    freqlabel = kwargs.get('freqlabel', 'Frequency, rad')
    if style in ('stacked', 'twin'):
        if ax is None:
            fig = plt.gcf()
            if len(fig.axes) == 0:
                if style == 'stacked':
                    fig, ax = plt.subplots(2, 1)
                else:
                    ax = plt.gca()
                    _ = ax.twinx()
                    ax = fig.axes
            else:
                ax = fig.axes
        else:
            fig = ax[0].figure
        if len(ax) != 2:
            raise ValueError("Must have exactly two axes for 'stacked' or 'twin'.")
        _mag_plot_z(
            ax[0], w, magnitude, xmin=minx, xmax=maxx, ylabel=maglabel, **kwargs
        )

        _phase_plot_z(
            ax[1],
            w,
            phase,
            xmin=minx,
            xmax=maxx,
            ylabel=phaselabel,
            xlabel=freqlabel,
            **kwargs,
        )
        return fig
    if style == 'magnitude':
        if ax is None:
            ax = plt.gca()
        _mag_plot_z(
            ax,
            w,
            magnitude,
            xmin=minx,
            xmax=maxx,
            ylabel=maglabel,
            xlabel=freqlabel,
            **kwargs,
        )
        return ax.figure
    if style == 'phase':
        if ax is None:
            ax = plt.gca()
        _phase_plot_z(
            ax,
            w,
            phase,
            xmin=minx,
            xmax=maxx,
            ylabel=phaselabel,
            xlabel=freqlabel,
            **kwargs,
        )
        return ax.figure
    raise ValueError(f"Unknown style: {style!r}")


def _mag_plot_z(
    ax,
    w,
    magnitude,
    xmin=None,
    xmax=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    **kwargs,
):
    "Plot magnitude response"
    ax.plot(w, magnitude, **kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if xlocator is None:
        ax.xaxis.set_major_formatter(PiFormatter())
        xlocator = PiLocator()
    if xlocator is not None:
        ax.xaxis.set_major_locator(xlocator)

    if ylocator is not None:
        ax.yaxis.set_major_locator(ylocator)

    if xmin is None:
        xmin = w.min()
    if xmax is None:
        xmax = w.max()
    ax.set_xlim(xmin, xmax)


def _phase_plot_z(
    ax,
    w,
    phase,
    xmin=None,
    xmax=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    **kwargs,
):
    "Plot phase response"
    ax.plot(w, phase, **kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if xlocator is None:
        ax.xaxis.set_major_formatter(PiFormatter())
        xlocator = PiLocator()
    if xlocator is not None:
        ax.xaxis.set_major_locator(xlocator)

    if ylocator is None:
        ax.yaxis.set_major_formatter(PiFormatter())
        ylocator = PiLocator()
    ax.yaxis.set_major_locator(ylocator)

    if xmin is None:
        xmin = w.min()
    if xmax is None:
        xmax = w.max()
    ax.set_xlim(xmin, xmax)


def freqz_tf(num, den, **kwargs):
    """
    Plot the frequency response of a discrete-time system represented using a
    transfer function.

    Parameters
    ----------
    num : array-like
        Numerator of transfer function.
    den : array-like
        Denominator of transfer function.
    **kwargs
        Additional arguments.

    Returns
    -------
    None.

    """
    return freqz(num=num, den=den, **kwargs)


def freqz_fir(num, **kwargs):
    """
    Plot the frequency response of a discrete-time FIR filter.

    Parameters
    ----------
    num : array-like
        Numerator of transfer function.
    **kwargs
        Additional arguments.

    Returns
    -------
    None.

    """
    return freqz(num=num, den=np.array([1.0]), **kwargs)
