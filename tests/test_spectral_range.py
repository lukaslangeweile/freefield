import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import freefield.freefield as ff


class DummySignal:
    def __init__(self):
        self.n_channels = 3
        self.samplerate = 48828

    def channel(self, index):
        return index


class DummyFilteredSignal:
    def __init__(self, level):
        self.level = np.asarray(level, dtype=float)


class DummyFilterBank:
    def __init__(self):
        self.n_channels = 4

        self.channel_levels = {
            0: [10, 20, 30, 40],
            1: [13, 18, 35, 40],
            2: [11, 25, 32, 38],
        }

    def apply(self, channel):
        return DummyFilteredSignal(
            level=self.channel_levels[channel],
        )


def prepare_spectral_range(monkeypatch):
    filter_bank = DummyFilterBank()
    received_filterbank_arguments = {}

    def create_filterbank(**kwargs):
        received_filterbank_arguments.update(kwargs)
        return filter_bank

    def create_center_frequencies(
            low_cutoff,
            high_cutoff,
            bandwidth,
    ):
        return (
            np.array([1, 2, 3, 4], dtype=float),
            None,
            None,
        )

    def convert_erb_to_frequency(center_frequencies):
        return np.array(
            [100, 500, 1000, 5000],
            dtype=float,
        )

    monkeypatch.setattr(
        ff.slab.Filter,
        "cos_filterbank",
        create_filterbank,
    )
    monkeypatch.setattr(
        ff.slab.Filter,
        "_center_freqs",
        create_center_frequencies,
    )
    monkeypatch.setattr(
        ff.slab.Filter,
        "_erb2freq",
        convert_erb_to_frequency,
    )

    return received_filterbank_arguments


def test_spectral_range_returns_level_range_for_each_frequency_band(
        monkeypatch,
):
    # Arrange
    signal = DummySignal()
    received_arguments = prepare_spectral_range(monkeypatch)

    # Act
    result = ff.spectral_range(
        signal=signal,
        bandwidth=0.2,
        low_cutoff=100,
        high_cutoff=5000,
        plot=False,
    )

    # Assert
    expected = np.array(
        [3, 7, 5, 2],
        dtype=float,
    )

    np.testing.assert_allclose(result, expected)

    assert received_arguments == {
        "length": 1000,
        "bandwidth": 0.2,
        "low_cutoff": 100,
        "high_cutoff": 5000,
        "samplerate": 48828,
    }


def test_spectral_range_plots_on_given_axes(monkeypatch):
    # Arrange
    signal = DummySignal()
    prepare_spectral_range(monkeypatch)

    figure, axes = plt.subplots()

    try:
        # Act
        result = ff.spectral_range(
            signal=signal,
            bandwidth=0.2,
            low_cutoff=100,
            high_cutoff=5000,
            thresh=3,
            plot=axes,
            log=True,
        )

        # Assert: numerisches Ergebnis bleibt unverändert
        np.testing.assert_allclose(
            result,
            np.array([3, 7, 5, 2], dtype=float),
        )

        # Maximum und Minimum werden als zwei Linien dargestellt
        assert len(axes.lines) == 2

        max_line, min_line = axes.lines

        np.testing.assert_allclose(
            max_line.get_xdata(),
            [100, 500, 1000, 5000],
        )
        np.testing.assert_allclose(
            max_line.get_ydata(),
            [13, 25, 35, 40],
        )
        np.testing.assert_allclose(
            min_line.get_ydata(),
            [10, 18, 30, 38],
        )

        assert max_line.get_color() == "black"
        assert min_line.get_color() == "black"
        assert max_line.get_linestyle() == "--"
        assert min_line.get_linestyle() == "--"

        # semilogx() muss eine logarithmische x-Achse erzeugen
        assert axes.get_xscale() == "log"

        # Differenzen über 3 liegen in Band 2 und 3:
        # [3, 7, 5, 2] > 3
        assert len(axes.collections) == 2

        for collection in axes.collections:
            red, green, blue, alpha = collection.get_facecolor()[0]

            assert red == 1
            assert green == 0
            assert blue == 0
            assert alpha == 0.6

    finally:
        plt.close(figure)