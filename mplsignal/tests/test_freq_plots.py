#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


import pytest
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from mplsignal import freqz


def test_freqz():
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den)
    assert len(fig.axes) == 2


def test_freqz_twin():
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='twin')
    assert len(fig.axes) == 2


def test_freqz_magnitude():
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='magnitude')
    # assert len(fig.axes) == 1


def test_freqz_phase():
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='phase')
    # assert len(fig.axes) == 1


@pytest.mark.parametrize(
    'kwargs,error,msg',
    [
        ({'den': [1, 1]}, ValueError, "At least one of 'num'"),
        ({'num': [1, 1]}, ValueError, "At least one of 'den'"),
        ({'poles': [1, 1]}, ValueError, "At least one of 'num'"),
        ({'zeros': [1, 1]}, ValueError, "At least one of 'den'"),
        (
            {'den': [1, 1], 'num': [1, 1], 'poles': [-0.5, 0.5]},
            ValueError,
            "At most one of 'den'",
        ),
        ({'num': [1, 1], 'zeros': [-0.5, 0.5]}, ValueError, "At most one of 'num'"),
        (
            {'den': [1, 1], 'num': [1, 1], 'style': "foo"},
            ValueError,
            "'foo' is not a valid value",
        ),
    ],
)
def test_freqz_errors(kwargs, error, msg):
    plt.figure()
    with pytest.raises(error, match=msg):
        freqz(**kwargs)


@image_comparison(['freqz_default.png'], style='mpl20')
def test_freqz_default_image():
    fig, axes = plt.subplots(2, 1)
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, ax=axes)


@image_comparison(['freqz_magnitude.png'], style='mpl20')
def test_freqz_magnitude_image():
    fig, ax = plt.subplots()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, style='magnitude', ax=ax)


@image_comparison(['freqz_twin.png'], style='mpl20')
def test_freqz_twin_image():
    fig, ax = plt.subplots()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, style='twin', ax=ax)
    plt.tight_layout()


@image_comparison(['freqz_phase.png'], style='mpl20')
def test_freqz_phase_image():
    fig, ax = plt.subplots()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, style='phase', ax=ax)


@image_comparison(['freqz_group_delay.png'], style='mpl20')
def test_freqz_group_delay_image():
    fig, ax = plt.subplots()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, style='group_delay', ax=ax)


@image_comparison(['freqz_tristacked.png'], style='mpl20')
def test_freqz_tristacked_image():
    fig, ax = plt.subplots(3, 1)
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, style='tristacked', ax=ax)
    plt.tight_layout()
