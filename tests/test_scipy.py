import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import image_comparison
from mplsignal.scipyplot import (
    freqz,
    freqz_magnitude,
    freqz_phase,
    freqz_tristacked,
    freqz_twin,
)


@image_comparison(['scipy_freqz.png'], style='mpl20')
def test_freqz():
    scipy = pytest.importorskip('scipy')
    plt.figure()
    h = scipy.signal.remez(11, [0, 0.1, 0.3, 0.5], [1, 0])
    scipy.signal.freqz(h, plot=freqz)


@image_comparison(['scipy_freqz_twin.png'], style='mpl20')
def test_freqz_twin():
    scipy = pytest.importorskip('scipy')
    plt.figure()
    h = scipy.signal.remez(11, [0, 0.1, 0.3, 0.5], [1, 0])
    scipy.signal.freqz(h, plot=freqz_twin)


@image_comparison(['scipy_freqz_phase.png'], style='mpl20')
def test_freqz_phase():
    scipy = pytest.importorskip('scipy')
    plt.figure()
    h = scipy.signal.remez(11, [0, 0.1, 0.3, 0.5], [1, 0])
    scipy.signal.freqz(h, plot=freqz_phase)


@image_comparison(['scipy_freqz_magnitude.png'], style='mpl20')
def test_freqz_magnitude():
    scipy = pytest.importorskip('scipy')
    plt.figure()
    h = scipy.signal.remez(11, [0, 0.1, 0.3, 0.5], [1, 0])
    scipy.signal.freqz(h, plot=freqz_magnitude)


@image_comparison(['scipy_freqz_tristacked.png'], style='mpl20')
def test_freqz_tristacked():
    scipy = pytest.importorskip('scipy')
    plt.figure()
    b, a = scipy.signal.ellip(5, 0.1, 40, 0.2)
    scipy.signal.freqz(b, a, plot=freqz_tristacked)
