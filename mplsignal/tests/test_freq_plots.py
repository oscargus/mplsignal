#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


import pytest
import matplotlib.pyplot as plt
from mplsignal import freqz


def test_freqz():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den)
    assert len(fig.axes) == 2


def test_freqz_twin():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den, style='twin')
    assert len(fig.axes) == 2


def test_freqz_magnitude():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den, style='magnitude')
    assert len(fig.axes) == 1


def test_freqz_phase():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den, style='phase')
    assert len(fig.axes) == 1


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
        ({'den': [1, 1], 'num': [1, 1], 'style': "foo"}, ValueError, "Unknown style"),
    ],
)
def test_freqz_errors(kwargs, error, msg):
    plt.figure()
    with pytest.raises(error, match=msg):
        freqz(**kwargs)
