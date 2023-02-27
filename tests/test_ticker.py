#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


import math

import numpy as np

from mplsignal.ticker import PiFormatter, PiLocator


def test_pilocator():
    locator = PiLocator()
    np.testing.assert_allclose(
        locator.tick_values(0, math.pi),
        np.array([0.0, 0.628319, 1.256637, 1.884956, 2.513274, 3.141593]),
        rtol=1e-6,
        atol=1e-6,
    )


def test_pilocator_adjust_locations():
    locator = PiLocator(5)
    np.testing.assert_allclose(
        locator.tick_values(0, math.pi),
        np.array([0.0, 0.62831853, 1.25663706, 1.88495559, 2.51327412, 3.14159265]),
    )


def test_piformatter():
    formatter = PiFormatter()
    assert formatter(math.pi) == r'$\pi$'
    assert formatter(-math.pi) == r'$-\pi$'
    assert formatter(2 * math.pi) == r'$2\pi$'
    assert formatter(0.2 * math.pi) == r'$0.2\pi$'
    assert formatter(0.25 * math.pi) == r'$0.25\pi$'
    assert formatter(0) == r'$0$'
    assert formatter(0.202 * math.pi) == r'$0.202\pi$'
    assert formatter(0.20234 * math.pi) == r'$0.202\pi$'


def test_piformatter_adjust_digits():
    formatter = PiFormatter(digits=4)
    assert formatter(math.pi) == r'$\pi$'
    assert formatter(-math.pi) == r'$-\pi$'
    assert formatter(2 * math.pi) == r'$2\pi$'
    assert formatter(0.2 * math.pi) == r'$0.2\pi$'
    assert formatter(0.25 * math.pi) == r'$0.25\pi$'
    assert formatter(0) == r'$0$'
    assert formatter(0.202 * math.pi) == r'$0.202\pi$'
    assert formatter(0.20234 * math.pi) == r'$0.2023\pi$'

    formatter = PiFormatter(digits=2)
    assert formatter(math.pi) == r'$\pi$'
    assert formatter(-math.pi) == r'$-\pi$'
    assert formatter(2 * math.pi) == r'$2\pi$'
    assert formatter(0.2 * math.pi) == r'$0.2\pi$'
    assert formatter(0.25 * math.pi) == r'$0.25\pi$'
    assert formatter(0) == r'$0$'
    assert formatter(0.202 * math.pi) == r'$0.2\pi$'
    assert formatter(0.20234 * math.pi) == r'$0.2\pi$'
