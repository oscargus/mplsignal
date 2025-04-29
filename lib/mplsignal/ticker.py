# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.
"""
This module contains Matplotlib :class:`~matplotlib.tickers.Ticker` and
:class:`~matplotlib.tickers.Locator` classes suitable for signal processing
plots.
"""
import math
from fractions import Fraction
from typing import Optional

from matplotlib.ticker import Formatter, Locator, MaxNLocator


def _is_close_to_int(x):
    """Return True if *x* is close to an integer."""
    return math.isclose(x, round(x))


class FactorLocator(Locator):
    """
    Locator for finding multiples of *factor*.

    Wraps a :class:`~matplotlib.tickers.MaxNLocator`.

    Parameters
    ----------
    factor : float, default: 1.0
        The factor to extract.
    nbins : int, optional
        Number of bins to aim for, see :class:`~matplotlib.tickers.MaxNLocator`.
    **kwargs
        Additional arguments passed to :class:`~matplotlib.tickers.MaxNLocator`.
    """

    def __init__(self, factor: float = 1.0, nbins: Optional[int] = None, **kwargs):
        """
        Locator for finding multiples of *factor*.
        """
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
    """
    Locator for finding multiples of :math:`\\pi`.

    Parameters
    ----------
    nbins : int, optional
        Number of bins to aim for, see :class:`~matplotlib.tickers.MaxNLocator`.
    """

    def __init__(self, nbins: Optional[int] = None, **kwargs):
        super().__init__(factor=math.pi, nbins=nbins, **kwargs)


class SampleFrequencyLocator(FactorLocator):
    """Locator for finding multiples of sample frequency."""

    def __init__(self, nbins: Optional[int] = None, fs: float = 1.0, **kwargs):
        super().__init__(factor=fs / (2 * math.pi), nbins=nbins, **kwargs)


class DegreeLocator(MaxNLocator):
    """
    Locator for finding multiples that are nice when using degrees.

    Parameters
    ----------
    nbins : int, optional
        Number of bins to aim for, see :class:`~matplotlib.tickers.MaxNLocator`.
    """

    def __init__(self, nbins: Optional[int] = None, **kwargs):
        steps = kwargs.pop('steps', [1, 1.5, 2, 3, 5, 6, 10])
        if nbins is None:
            nbins = 'auto'
        super().__init__(nbins, steps=steps, **kwargs)


class FactorFormatter(Formatter):
    """
    Create a string based on a tick value and location as a multiple of *factor*.

    Parameters
    ----------
    digits : int, default: 3
        Number of digits to round fractional numbers to.
    factor : float, default: 1.0
        The factor.
    name : str, optional
        The name of the factor.
    name_on_all_numbers : bool, default False
        If True, *name* is added to all numbers, even 0, if False, *name* is not added
        to 0.
    **kwargs
        Additional arguments passed to :class:`~matplotlib.tickers.Formatter`.
    """

    # some classes want to see all the locs to help format
    # individual ones
    locs = []

    def __init__(
        self,
        digits: int = 3,
        factor: float = 1.0,
        name: str = "constant",
        name_on_all_numbers: bool = False,
        **kwargs,
    ):
        self._digits = digits
        self._factor = factor
        self._name = name
        self._name_on_all_numbers = name_on_all_numbers
        super().__init__(**kwargs)

    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x* at position pos.
        ``pos=None`` indicates an unspecified location.
        """
        if x == 0.0:
            if self._name_on_all_numbers:
                return f"$0{self._name}$"
            else:
                return "$0$"
        factor_mult = x / self._factor
        if not self._name_on_all_numbers:
            if abs(factor_mult - 1.0) < 1e-9:
                return f"${self._name}$"
            if abs(factor_mult + 1.0) < 1e-9:
                return f"$-{self._name}$"
        factor_mult = round(factor_mult, self._digits)
        if _is_close_to_int(factor_mult):
            factor_mult = round(factor_mult)
        return f"${factor_mult}{self._name}$"


class PiFormatter(FactorFormatter):
    r"""
    Create a string with multiple of :math:`\pi`.

    Parameters
    ----------
    digits : int, default: 3
        Number of digits to round fractional numbers to.
    **kwargs
        Additional arguments passed to :class:`FactorFormatter`.
        Cannot include *factor* and *name*.
    """

    def __init__(self, digits: int = 3, **kwargs):
        super().__init__(digits=digits, factor=math.pi, name=r"\pi", **kwargs)


class SampleFrequencyFormatter(FactorFormatter):
    r"""
    Create a string with multiple of sample frequency, :math:`f_s`.

    Parameters
    ----------
    digits : int, default: 3
        Number of digits to round fractional numbers to.
    fs : float, default: 1.0
        The sample frequency in Hz.
    **kwargs
        Additional arguments passed to :class:`FactorFormatter`.
        Cannot include *factor* and *name*.
    """

    def __init__(self, digits: int = 3, fs: float = 1.0, **kwargs):
        super().__init__(
            digits=digits, factor=fs / (2 * math.pi), name=r"f_s", **kwargs
        )


class DegreeFormatter(FactorFormatter):
    r"""
    Create a string with a trailing :math:`^{\circ}`.

    Parameters
    ----------
    digits : int, default: 3
        Number of digits to round fractional numbers to.
    fs : float, default: 1.0
        The sample frequency in Hz.
    **kwargs
        Additional arguments passed to :class:`FactorFormatter`.
        Cannot include *factor*, *name*, and *only_name_when_one*.
    """

    def __init__(self, digits: int = 3, **kwargs):
        super().__init__(
            digits=digits,
            factor=1,
            name=r"^{\circ}",
            name_on_all_numbers=True,
            **kwargs,
        )


class PiRationalFormatter(Formatter):
    r"""
    Create a string with rational multiple of :math:`\pi`.

    Parameters
    ----------
    digits : int, default: 3
        Number of digits to round fractional numbers to.
    pi_always_in_numerator: bool, default: True
        If True, the strings will look like :math:`\frac{2\pi}{5}`, if False,
        like :math:`\frac{2}{5}\pi`
    **kwargs
        Additional arguments passed to :class:`~matplotlib.tickers.Formatter`.
    """

    # some classes want to see all the locs to help format
    # individual ones
    locs = []

    def __init__(self, digits: int = 3, pi_always_in_numerator: bool = True, **kwargs):
        self._digits = digits
        self._pi_always_in_numerator = pi_always_in_numerator
        super().__init__(**kwargs)

    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x* at position pos.
        ``pos=None`` indicates an unspecified location.
        """
        if abs(x) < 1e-9:
            return "$0$"
        factor_mult = x / math.pi
        if abs(factor_mult - 1.0) < 1e-9:
            return r"$\pi$"
        if abs(factor_mult + 1.0) < 1e-9:
            return r"$-\pi$"
        sign = "-" if factor_mult < 0 else ""
        factor_mult = abs(factor_mult)
        factor_mult = Fraction(round(factor_mult, self._digits)).limit_denominator()
        if factor_mult.denominator == 1:
            return fr"${sign}{factor_mult.numerator}\pi$"
        if self._pi_always_in_numerator:
            if factor_mult.numerator == 1:
                return fr"${sign}\frac{{\pi}}{{{factor_mult.denominator}}}$"
            den = factor_mult.denominator
            return fr"${sign}\frac{{{factor_mult.numerator}\pi}}{{{den}}}$"
        return (
            fr"${sign}\frac{{{factor_mult.numerator}}}{{{factor_mult.denominator}}}\pi$"
        )
