# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.
"""
This module contains Matplotlib :class:`~matplotlib.tickers.Ticker` and
:class:`~matplotlib.tickers.Locator` classes suitable for signal processing
plots.
"""
import math

from matplotlib.ticker import Formatter, Locator, MaxNLocator


def _is_close_to_int(x):
    return math.isclose(x, round(x))


class FactorLocator(Locator):
    def __init__(self, factor=1.0, nbins=None, **kwargs):
        steps = kwargs.pop('steps', [1, 2, 3, 4, 5, 6, 8, 10])
        if nbins is None:
            nbins = 'auto'
        self._factor = factor
        self._locator = MaxNLocator(nbins, steps=steps, **kwargs)

    def tick_values(self, vmin, vmax):
        """
        Return the values of the located ticks given **vmin** and **vmax**.
        """
        # Use MaxNLocator and scale by factor
        return self._factor * (
            self._locator.tick_values(vmin / self._factor, vmax / self._factor)
        )

    def __call__(self):
        """Return the locations of the ticks."""
        # note: some locators return data limits, other return view limits,
        # hence there is no *one* interface to call self.tick_values.
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)


class PiLocator(FactorLocator):
    """Locator for finding multiples of :math:`\\pi`."""

    def __init__(self, nbins=None, **kwargs):
        super().__init__(factor=math.pi, nbins=nbins, **kwargs)


class SampleFrequencyLocator(FactorLocator):
    """Locator for finding multiples of sample frequency."""

    def __init__(self, nbins=None, fs=1.0, **kwargs):
        super().__init__(factor=fs / (2 * math.pi), nbins=nbins, **kwargs)


class DegreeLocator(MaxNLocator):
    """Locator for finding multiples that are nice when using degrees."""

    def __init__(self, nbins=None, **kwargs):
        steps = kwargs.pop('steps', [1, 1.5, 2, 3, 5, 6, 10])
        if nbins is None:
            nbins = 'auto'
        super().__init__(nbins, steps=steps, **kwargs)


class FactorFormatter(Formatter):
    """
    Create a string based on a tick value and location.
    """

    # some classes want to see all the locs to help format
    # individual ones
    locs = []

    def __init__(self, digits=3, factor=1.0, name="constant", **kwargs):
        self._digits = digits
        self._factor = factor
        self._name = name
        super().__init__(**kwargs)

    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x* at position pos.
        ``pos=None`` indicates an unspecified location.
        """
        if x == 0.0:
            return "$0$"
        factormult = x / self._factor
        if abs(factormult - 1.0) < 1e-9:
            return fr"${self._name}$"
        if abs(factormult + 1.0) < 1e-9:
            return fr"$-{self._name}$"
        factormult = round(factormult, self._digits)
        if _is_close_to_int(factormult):
            factormult = round(factormult)
        return fr"${factormult}{self._name}$"


class PiFormatter(FactorFormatter):
    r"""
    Create a string with multiple of :math:`\pi`.
    """

    def __init__(self, digits=3, **kwargs):
        super().__init__(digits=digits, factor=math.pi, name=r"\pi", **kwargs)


class SampleFrequencyFormatter(FactorFormatter):
    r"""
    Create a string with multiple of sample frequency, :math:`f_s`.
    """

    def __init__(self, digits=3, fs=1.0, **kwargs):
        """ """
        super().__init__(
            digits=digits, factor=fs / (2 * math.pi), name=r"f_s", **kwargs
        )


class DegreeFormatter(FactorFormatter):
    r"""
    Create a string with a trailing :math:`^{\circ}`.
    """

    def __init__(self, digits=3, **kwargs):
        super().__init__(digits=digits, factor=1, name=r"^{\circ}", **kwargs)
