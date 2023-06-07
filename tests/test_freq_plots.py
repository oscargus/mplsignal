#!/usr/bin/env python

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from mplsignal import freqz, freqz_fir, freqz_tf, freqz_zpk


def test_freqz():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den)
    assert len(fig.axes) == 2


def test_freqz_twin():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='twin')
    assert len(fig.axes) == 2


def test_freqz_magnitude():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='magnitude')
    assert len(fig.axes) == 1


def test_freqz_phase():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='phase')
    assert len(fig.axes) == 1


def test_freqz_tristacked():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig = freqz(num=num, den=den, style='tristacked')
    assert len(fig.axes) == 3


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
        (
            {'num': [1, 1], 'zeros': [-0.5, 0.5]},
            ValueError,
            "At most one of 'num'",
        ),
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


@image_comparison(['freqz_freq_units.png'], style='mpl20')
def test_freqz_freq_units_image():
    fig, axes = plt.subplots(5, 1, figsize=(3, 10))
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    for i, freq_unit in enumerate(('rad', 'deg', 'norm', 'normfs', 'fs')):
        freqz(
            num=num,
            den=den,
            style='phase',
            freq_unit=freq_unit,
            ax=axes[i],
            fs=1e6,
        )
    plt.tight_layout()


@image_comparison(['freqz_freq_units_magnitude.png'], style='mpl20')
def test_freqz_freq_units_magnitude_image():
    fig, axes = plt.subplots(5, 1, figsize=(3, 10), layout='compressed')
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    for i, freq_unit in enumerate(('rad', 'deg', 'norm', 'normfs', 'fs')):
        freqz(
            num=num,
            den=den,
            style='magnitude',
            freq_unit=freq_unit,
            ax=axes[i],
            fs=1e3,
        )


@image_comparison(['freqz_freq_units_group_delay.png'], style='mpl20')
def test_freqz_freq_units_group_delay_image():
    fig, axes = plt.subplots(5, 1, figsize=(3, 10), layout='compressed')
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    for i, freq_unit in enumerate(('rad', 'deg', 'norm', 'normfs', 'fs')):
        freqz(
            num=num,
            den=den,
            style='group_delay',
            freq_unit=freq_unit,
            ax=axes[i],
            fs=1e3,
        )


@image_comparison(['freqz_phase_units.png'], style='mpl20')
def test_freqz_phase_units_image():
    fig, axes = plt.subplots(2, 1, figsize=(3, 6))
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    for i, phase_unit in enumerate(('rad', 'deg')):
        freqz(
            num=num,
            den=den,
            style='phase',
            phase_unit=phase_unit,
            ax=axes[i],
        )
    plt.tight_layout()


@image_comparison(['freqz_magnitude_scale.png'], style='mpl20')
def test_freqz_magnitude_scale_image():
    fig, axes = plt.subplots(2, 1, figsize=(3, 6))
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    for i, magnitude_scale in enumerate(('log', 'linear')):
        freqz(
            num=num,
            den=den,
            style='magnitude',
            magnitude_scale=magnitude_scale,
            ax=axes[i],
        )
    plt.tight_layout()


@image_comparison(['freqz_freq_units_log.png'], style='mpl20')
def test_freqz_freq_units_log_image():
    fig, axes = plt.subplots(5, 1, figsize=(3, 10))
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    for i, freq_unit in enumerate(('rad', 'deg', 'norm', 'normfs', 'fs')):
        freqz(
            num=num,
            den=den,
            style='magnitude',
            freq_unit=freq_unit,
            ax=axes[i],
            frequency_scale='log',
            fs=1e6,
        )
    plt.tight_layout()


@check_figures_equal(extensions=['png'])
def test_adding_axes_stacked(fig_test, fig_ref):
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig_test.subplots(2, 1)
    # Hack so that gcf() returns fig_test
    fn = plt.gcf
    plt.gcf = lambda: fig_test
    freqz(num=num, den=den)
    # Restore
    plt.gcf = fn

    ax = fig_ref.subplots(2, 1)
    freqz(num=num, den=den, ax=ax)


@check_figures_equal(extensions=['png'])
def test_adding_axes_tristacked(fig_test, fig_ref):
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    fig_test.subplots(3, 1)
    # Hack so that gcf() returns fig_test
    fn = plt.gcf
    plt.gcf = lambda: fig_test
    freqz(num=num, den=den, style='tristacked')
    # Restore
    plt.gcf = fn

    ax = fig_ref.subplots(3, 1)
    freqz(num=num, den=den, ax=ax, style='tristacked')


def test_incorrect_axes():
    _, ax = plt.subplots()
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    with pytest.raises(
        ValueError, match="Must have at least two axes for 'stacked' or 'twin'."
    ):
        freqz(num=num, den=den, style='stacked')

    with pytest.raises(
        ValueError, match="Must have at least two axes for 'stacked' or 'twin'."
    ):
        freqz(num=num, den=den, style='twin')

    _, ax = plt.subplots(2, 1)
    with pytest.raises(
        ValueError, match="Must have at least three axes for 'tristacked'."
    ):
        freqz(num=num, den=den, style='tristacked')


@image_comparison(['freqz_partial_freq_range.png'], style='mpl20')
def test_freqz_partial_freq_range():
    fig, axes = plt.subplots(3, 1, figsize=(3, 6), layout='constrained')
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    w = np.linspace(0, 0.3, 1000)
    freqz(num=num, den=den, w=w, ax=axes, style='tristacked')


@image_comparison(['freqz_whole_freq_range.png'], style='mpl20')
def test_freqz_whole_freq_range():
    fig, ax = plt.subplots(2, 1)
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    freqz(num=num, den=den, ax=ax, whole=True)


@image_comparison(['freqz_roots.png'], style='mpl20')
def test_freqz_roots():
    fig, ax = plt.subplots(2, 1)
    z = np.roots([1, 2, 1])
    p = np.roots([1, -1.2, 0.5])
    freqz(zeros=z, poles=p, ax=ax)


@check_figures_equal(extensions=["png"])
def test_freqz_zpk(fig_test, fig_ref):
    z = np.roots([1, 2, 1])
    p = np.roots([1, -1.2, 0.5])
    ax_ref = fig_ref.subplots(2, 1)
    freqz(poles=p, zeros=z, gain=1e-2, ax=ax_ref)

    ax_test = fig_test.subplots(2, 1)
    freqz_zpk(z, p, 1e-2, ax=ax_test)


@check_figures_equal(extensions=["png"])
def test_freqz_fir(fig_test, fig_ref):
    h = [1, 2, 1]
    ax_ref = fig_ref.subplots(2, 1)
    freqz(num=h, den=1, ax=ax_ref)

    ax_test = fig_test.subplots(2, 1)
    freqz_fir(h, ax=ax_test)


@check_figures_equal(extensions=["png"])
def test_freqz_tf(fig_test, fig_ref):
    num = [1, 2, 1]
    den = [1, -1.2, 0.5]
    ax_ref = fig_ref.subplots(2, 1)
    freqz(num=num, den=den, ax=ax_ref)

    ax_test = fig_test.subplots(2, 1)
    freqz_tf(num, den, ax=ax_test)
