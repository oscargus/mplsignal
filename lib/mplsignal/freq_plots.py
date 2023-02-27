"""
Functions for plotting transfer functions.
"""

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "freqz",
    "freqz_tf",
    "freqz_zpk",
    "freqz_fir",
]
import matplotlib.pyplot as plt
import numpy as np

from mplsignal import _api, _utils
from mplsignal.ticker import (
    DegreeFormatter,
    DegreeLocator,
    PiFormatter,
    PiLocator,
    SampleFrequencyFormatter,
)


def freqz(
    num=None,
    den=None,
    zeros=None,
    poles=None,
    gain=1,
    w=None,
    freq_unit='rad',
    phase_unit='rad',
    ax=None,
    style='stacked',
    magnitude_scale='log',
    frequency_scale='linear',
    whole=False,
    include_nyquist=False,
    fs=2 * np.pi,
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
    w : int or array-like, optional
        If a single integer, compute at that many frequency points in the
        range :math:`[0, \\pi]`, default: 512.
        If array-like, frequencies to determine transfer function at.
    freq_unit : {'rad', 'deg', 'norm', 'fs', 'normfs'}, default: 'rad'
        Unit for frequency axes.
    phase_unit : {'rad', 'deg'}, default: 'rad'
        Unit for phase.
    ax : :class:`~matplotlib.axes.Axes` or iterable of :class:`~matplotlib.axes.Axes`,\
 optional
        Axes or iterable of Axes to plot in. If None, create required Axes.
    style : {'stacked', 'twin', 'magnitude', 'phase', 'group_delay', \
'tristacked'}, default: 'stacked'
        Plotting style.
    magnitude_scale : {'linear', 'log'}, default: 'log'
        Whether magnitude is plotted in linear or logarithmic (dB) scale.
    frequency_scale : {'linear', 'log'}, default: 'linear'
        Whether frequency is plotted in linear or logarithmic scale.
    whole : bool, optional
        Plot from 0 to :math:`2\\pi` if True. Otherwise, plot from 0 to
        :math:`\\pi`.
    include_nyquist : bool, optional
        If *whole* is False and *w* is an integer, setting *include_nyquist*
        to True will include the last frequency (Nyquist frequency) and is
        otherwise ignored.
    fs : float, optional
        Sample frequency.
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

    _api.check_in_iterable(('rad', 'deg', 'norm', 'fs', 'normfs'), freq_unit=freq_unit)
    _api.check_in_iterable(('rad', 'deg'), phase_unit=phase_unit)
    _api.check_in_iterable(
        ('stacked', 'twin', 'magnitude', 'phase', 'group_delay', 'tristacked'),
        style=style,
    )
    _api.check_in_iterable(('linear', 'log'), magnitude_scale=magnitude_scale)
    _api.check_in_iterable(('linear', 'log'), frequency_scale=frequency_scale)

    if not np.iterable(ax) and ax is not None:
        ax = [ax]

    if w is None:
        w = 512

    if isinstance(w, int):
        if frequency_scale == 'linear':
            w = np.linspace(
                0, 2 * np.pi if whole else np.pi, w, endpoint=include_nyquist
            )
        else:
            w = np.logspace(
                1e-5,
                2 * np.pi if whole else np.pi,
                w,
                endpoint=include_nyquist,
            )
        if kwargs.get('xmax', None) is None and not include_nyquist:
            kwargs['xmax'] = 2 * np.pi if whole else np.pi

    if num is not None and den is not None:
        h = _utils.freqz_tf(num, den, w)

    if zeros is not None and poles is not None and gain is not None:
        h = _utils.freqz_zpk(zeros, poles, gain, w)

    return _plot_h(
        w,
        h,
        ax=ax,
        style=style,
        freq_unit=freq_unit,
        phase_unit=phase_unit,
        magnitude_scale=magnitude_scale,
        frequency_scale=frequency_scale,
        fs=fs,
        **kwargs,
    )


def _plot_h(
    w,
    h,
    fs=None,
    ax=None,
    style='stacked',
    freq_unit='rad',
    phase_unit='rad',
    magnitude_scale='log',
    frequency_scale='linear',
    **kwargs,
):
    """
    Work horse for the `freq*` functions.

    Parameters
    ----------
    w
    h
    fs
    ax
    style
    freq_unit
    phase_unit
    magnitude_scale
    frequency_scale
    **kwargs
    """
    minx = kwargs.pop('xmin', w.min())
    maxx = kwargs.pop('xmax', w.max())
    maglabel = kwargs.get(
        'maglabel',
        'Magnitude, dB' if magnitude_scale == 'log' else "Magnitude",
    )
    phaselabel = kwargs.get('phaselabel', 'Phase, %s' % (phase_unit))
    freqlabel = kwargs.get('freqlabel', _get_freq_unit_text(freq_unit))

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
            raise ValueError("Must have at least two axes for 'stacked' or 'twin'.")
        _mag_plot_z(
            ax[0],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            xlabel=(freqlabel if style == 'twin' else None),
            ylabel=maglabel,
            frequency_scale=frequency_scale,
            magnitude_scale=magnitude_scale,
            **kwargs,
        )

        _phase_plot_z(
            ax[1],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            phase_unit=phase_unit,
            ylabel=phaselabel,
            xlabel=(freqlabel if style == 'stacked' else None),
            fs=fs,
            frequency_scale=frequency_scale,
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
            magnitude_scale=magnitude_scale,
            frequency_scale=frequency_scale,
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
            frequency_scale=frequency_scale,
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
            freq_unit=freq_unit,
            phase_unit=phase_unit,
            ylabel=phaselabel,
            xlabel=freqlabel,
            frequency_scale=frequency_scale,
            fs=fs,
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
            magnitude_scale=magnitude_scale,
            frequency_scale=frequency_scale,
            **kwargs,
        )
        _phase_plot_z(
            ax[1],
            w,
            h,
            xmin=minx,
            xmax=maxx,
            phase_unit=phase_unit,
            ylabel=phaselabel,
            xlabel=None,
            frequency_scale=frequency_scale,
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
            frequency_scale=frequency_scale,
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
    freq_unit=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    magnitude_scale='log',
    frequency_scale='linear',
    fs=1,
    **kwargs,
):
    """Plot magnitude response."""
    magnitude = np.abs(h)
    if magnitude_scale == 'log':
        magnitude = 20 * np.log10(np.abs(h))
    wscale = _get_freq_scale(freq_unit, fs)
    w = wscale * w
    ax.plot(w, magnitude, **kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if xlocator is None:
        xlocator = _set_freq_formatter(freq_unit, ax.xaxis)
    if xlocator is not None:
        ax.xaxis.set_major_locator(xlocator)

    if ylocator is not None:
        ax.yaxis.set_major_locator(ylocator)

    if frequency_scale == 'log':
        ax.set_xscale('log')

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
    freq_unit=None,
    phase_unit=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    frequency_scale='linear',
    fs=1,
    **kwargs,
):
    """Plot phase response."""
    phase = np.unwrap(np.angle(h))
    if phase_unit == 'deg':
        phase = 180 / np.pi * phase
    wscale = _get_freq_scale(freq_unit, fs)
    w = wscale * w
    ax.plot(w, phase, **kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if xlocator is None:
        xlocator = _set_freq_formatter(freq_unit, ax.xaxis)
    if xlocator is not None:
        ax.xaxis.set_major_locator(xlocator)

    if ylocator is None:
        ylocator = _set_phase_formatter(phase_unit, ax.yaxis)
    if ylocator is not None:
        ax.yaxis.set_major_locator(ylocator)

    if frequency_scale == 'log':
        ax.set_xscale('log')

    if xmin is None:
        xmin = w.min()
    if xmax is None:
        xmax = w.max()
    ax.set_xlim(wscale * xmin, wscale * xmax)


def _group_delay_plot_z(
    ax,
    w,
    h,
    xmin=None,
    xmax=None,
    freq_unit=None,
    xlabel=None,
    ylabel=None,
    xlocator=None,
    ylocator=None,
    frequency_scale='linear',
    fs=1,
    **kwargs,
):
    """Plot group delay."""
    gd, w = _utils.group_delay_from_h(w, h)
    wscale = _get_freq_scale(freq_unit, fs)
    w = wscale * w

    ax.plot(w, gd, **kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if xlocator is None:
        xlocator = _set_freq_formatter(freq_unit, ax.xaxis)
    if xlocator is not None:
        ax.xaxis.set_major_locator(xlocator)

    if ylocator is not None:
        ax.yaxis.set_major_locator(ylocator)

    if frequency_scale == 'log':
        ax.set_xscale('log')

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
        Additional arguments passed to :func:`freqz`.

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
        Additional arguments  passed to :func:`freqz`.

    Returns
    -------
    None.
    """
    return freqz(num=num, den=np.array([1.0]), **kwargs)


def freqz_zpk(zeros, poles, gain=1, **kwargs):
    """
    Plot the frequency response of a discrete-time system represented using
    zeros, poles and gain.

    Parameters
    ----------
    zeros : array-like
        Zeros of system.
    poles : array-like
        Poles of system.
    gain : float
        Gain of system.
    **kwargs
        Additional arguments passed to :func:`freqz`.

    Returns
    -------
    None.
    """
    return freqz(zeros=zeros, poles=poles, gain=gain, **kwargs)


def _get_freq_scale(freq_unit, fs):
    """Return scale factor based on named option."""
    if freq_unit == 'deg':
        return 180 / np.pi
    if freq_unit in ('norm', 'normfs'):
        return 1 / (2 * np.pi)
    if freq_unit == 'fs':
        if fs is None:
            raise ValueError("Cannot use freq_unit = 'fs' without providing fs")
        return fs / (2 * np.pi)
    return 1


def _set_freq_formatter(freq_unit, axis):
    """Set major formatter for frequency based on named option."""
    if freq_unit == 'deg':
        axis.set_major_formatter(DegreeFormatter())
        return DegreeLocator()
    if freq_unit in ('fs', 'norm'):
        return None
    if freq_unit == 'normfs':
        axis.set_major_formatter(SampleFrequencyFormatter(fs=2 * np.pi))
        return None
    axis.set_major_formatter(PiFormatter())
    return PiLocator()


def _get_freq_unit_text(freq_unit):
    """Return frequency axis label based on named option."""
    if freq_unit == 'deg':
        return "Frequency, deg/sample"
    if freq_unit in ('norm', 'normfs'):
        return 'Normalized frequency'
    if freq_unit == 'fs':
        return "Frequency, Hz"
    return "Frequency, rad/sample"


def _set_phase_formatter(phase_unit, axis):
    """Set major formatter for phase based on unit."""
    if phase_unit == 'deg':
        axis.set_major_formatter(DegreeFormatter())
        return DegreeLocator()
    axis.set_major_formatter(PiFormatter())
    return PiLocator()
