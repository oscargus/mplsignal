#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

from matplotlib.ticker import Formatter, Locator, MaxNLocator
import math


class PiLocator(Locator):
    def __init__(self, nbins=None, **kwargs):
        steps = kwargs.pop('steps', [1, 2, 5])
        self._locator = MaxNLocator(nbins, steps=steps, **kwargs)

    def tick_values(self, vmin, vmax):
        """
        Return the values of the located ticks given **vmin** and **vmax**.
        """
        # Use MaxNLocator and scale by pi
        return math.pi * (self._locator.tick_values(vmin / math.pi, vmax / math.pi))

    def __call__(self):
        """Return the locations of the ticks."""
        # note: some locators return data limits, other return view limits,
        # hence there is no *one* interface to call self.tick_values.
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)


class PiFormatter(Formatter):
    """
    Create a string based on a tick value and location.
    """

    # some classes want to see all the locs to help format
    # individual ones
    locs = []

    def __init__(self, digits=3, **kwargs):
        self._digits = digits
        super().__init__(**kwargs)

    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x* at position pos.
        ``pos=None`` indicates an unspecified location.
        """
        if x == 0.0:
            return "$0$"
        pimult = x / math.pi
        if abs(pimult - 1.0) < 1e-9:
            return r"$\pi$"
        if abs(pimult + 1.0) < 1e-9:
            return r"$-\pi$"
        pimult = round(pimult, self._digits)
        return fr"${pimult}\pi$"
