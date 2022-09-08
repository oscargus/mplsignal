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
from mplsignal import _utils, _api
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
    style='stacked',
    magnitude_scale='log',
    **kwargs,
):
    """
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
        range :math:`[0, \\pi]`. Default: 512.
        If array-like, frequencies to determine transfer function at.
    freq_units : {'rad', 'deg', 'norm', 'fs'}. Default: 'rad'
        Units for frequency axes.
    phase_units : {'rad', 'deg'}. Default: 'rad'
        Units for phase.
    ax : :class:`~matplotlib.axes.Axes` or iterable of \
:class:`~matplotlib.axes.Axes`, optional
        Axes or iterable of Axes to plot in. If None, create required Axes.
    style : {'stacked', 'twin', 'magnitude', 'phase', 'group_delay', \
'tristacked'}. Default: 'stacked'
        Plotting style.
    magnitude_scale : {'linear', 'log'}. Default: 'log'
        Whether magnitude is plotted in linear or logarithmig (dB) scale.
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

    _api.check_in_iterable(('rad', 'deg', 'norm', 'fs'), freq_units=freq_units)
    _api.check_in_iterable(('rad', 'deg'), phase_units=phase_units)
    _api.check_in_iterable(
        ('stacked', 'twin', 'magnitude', 'phase', 'group_delay', 'tristacked'),
        style=style,
    )
    _api.check_in_iterable(('linear', 'log'), magnitude_scale=magnitude_scale)

    if not np.iterable(ax) and ax is not None:
        ax = [ax]

    if w is None:
        w = 512

    if isinstance(w, int):
        w = np.linspace(0, np.pi, w)

    if num is not None and den is not None:
        h = _utils.freqz_tf(num, den, w)

    if zeros is not None and poles is not None and gain is not None:
        h = _utils.freqz_zpk(zeros, poles, gain, w)

    return _plot_h(
        w,
        h,
        ax=ax,
        style=style,
        freq_units=freq_units,
        phase_units=phase_units,
        magnitude_scale=magnitude_scale,
        **kwargs,
    )


def _plot_h(
    w,
    h,
    ax=None,
    style='stacked',
    freq_units='rad',
    phase_units='rad',
    magnitude_scale='log',
    **kwargs,
):
    minx = w.min()
    maxx = w.max()
    maglabel = kwargs.get('maglabel', 'Magnitude, dB')
    phaselabel = kwargs.get('phaselabel', 'Phase, rad')
    freqlabel = kwargs.get('freqlabel', 'Frequency, rad')
    group_delay_label = kwargs.get('gdlabel', 'Group delay, samples')
    if style in ('stacked', 'twin'):
        if ax is None:
            fig = plt.gcf()
            if len(fig.axes) == 0:
                if style == 'stacked':
                    ax = fig.subplots(2, 1)
                else:
                    ax = plt.gca()
                    _ = ax.twinx()
                    ax = fig.axes
            else:
                ax = fig.axes
        else:
            if style == 'twin':
                _ = ax[0].twinx()
                ax = ax[0].figure.axes
            fig = ax[0].figure
        if len(ax) < 2:
            raise ValueError(
                "Must have at least two axes for 'stacked' or 'twin'."
            )
        _mag_plot_z(
            ax[0],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            xlabel=(freqlabel if style == 'twin' else None),
            ylabel=maglabel,
            **kwargs,
        )

        _phase_plot_z(
            ax[1],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            ylabel=phaselabel,
            xlabel=(freqlabel if style == 'stacked' else None),
            **kwargs,
        )
        return fig
    if style == 'magnitude':
        if ax is None:
            ax = [plt.gca()]
        _mag_plot_z(
            ax[0],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            ylabel=maglabel,
            xlabel=freqlabel,
            **kwargs,
        )
        return ax[0].figure
    if style == 'group_delay':
        if ax is None:
            ax = [plt.gca()]
        _group_delay_plot_z(
            ax[0],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            ylabel=group_delay_label,
            xlabel=freqlabel,
            **kwargs,
        )
        return ax[0].figure
    if style == 'phase':
        if ax is None:
            ax = [plt.gca()]
        _phase_plot_z(
            ax[0],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            ylabel=phaselabel,
            xlabel=freqlabel,
            **kwargs,
        )
        return ax[0].figure
    if style == 'tristacked':
        if ax is None:
            fig = plt.gcf()
            if len(fig.axes) == 0:
                ax = fig.subplots(3, 1)
            else:
                ax = fig.axes
        else:
            fig = ax[0].figure
        if len(ax) < 3:
            raise ValueError("Must have at least three axes for 'tristacked'.")
        _mag_plot_z(
            ax[0],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            xlabel=None,
            ylabel=maglabel,
            **kwargs,
        )
        _phase_plot_z(
            ax[1],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            ylabel=phaselabel,
            xlabel=None,
            **kwargs,
        )
        _group_delay_plot_z(
            ax[2],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            ylabel=group_delay_label,
            xlabel=freqlabel,
            **kwargs,
        )
        return fig
    raise ValueError(f"Unknown style: {style!r}")


def _mag_plot_z(
    ax,
    w,
    h,
    xmin=None,
    xmax=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    **kwargs,
):
    "Plot magnitude response"
    magnitude = 20 * np.log10(np.abs(h))
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
    h,
    xmin=None,
    xmax=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    **kwargs,
):
    "Plot phase response"
    phase = np.unwrap(np.angle(h))
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
    if ylocator is not None:
        ax.yaxis.set_major_locator(ylocator)

    if xmin is None:
        xmin = w.min()
    if xmax is None:
        xmax = w.max()
    ax.set_xlim(xmin, xmax)


def _group_delay_plot_z(
    ax,
    w,
    h,
    xmin=None,
    xmax=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    **kwargs,
):
    "Plot group delay"
    gd, w = _utils.group_delay_from_h(w, h)
    ax.plot(w, gd, **kwargs)

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
