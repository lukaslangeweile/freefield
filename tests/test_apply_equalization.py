import numpy as np
import pytest
import slab

import freefield.freefield as ff


@pytest.fixture
def speaker_setup(monkeypatch):
    speaker = ff.Speaker(
        index=2,
        analog_channel=0,
        analog_proc="RX8",
        digital_proc="RX8",
        azimuth=30,
        elevation=12.5,
        distance=1.4,
        digital_channel=0,
    )

    monkeypatch.setattr(ff, "SPEAKERS", [speaker])

    return speaker


def test_apply_equalization_applies_level_to_copy(speaker_setup):
    # Arrange
    signal = slab.Sound.whitenoise(
        duration=0.01,
        samplerate=48828,
    )
    signal.level = 40
    speaker_setup.level = 65

    # Act
    result = ff.apply_equalization(
        signal=signal,
        speaker=speaker_setup,
        level=True,
        frequency=False,
    )

    # Assert
    assert isinstance(result, slab.Sound)
    assert result is not signal
    assert result.level == pytest.approx(65)
    assert signal.level == pytest.approx(40)


def test_apply_equalization_raises_error_when_level_is_missing(
    speaker_setup,
):
    # Arrange
    signal = slab.Sound.whitenoise(
        duration=0.01,
        samplerate=48828,
    )
    speaker_setup.level = None

    # Act and Assert
    with pytest.raises(
        ValueError,
        match="speaker not level-equalized",
    ):
        ff.apply_equalization(
            signal=signal,
            speaker=speaker_setup,
            level=True,
            frequency=False,
        )


def test_apply_equalization_applies_real_frequency_filter(
    speaker_setup,
):
    # Arrange
    samplerate = 48828
    signal_data = np.array(
        [1.0, -0.5, 0.25, -0.125],
        dtype=float,
    )
    signal = slab.Sound(
        signal_data,
        samplerate=samplerate,
    )

    speaker_setup.filter = slab.Filter(
        data=np.array([0.5]),
        samplerate=samplerate,
        fir="IR",
    )

    original_data = signal.data.copy()

    # Act
    result = ff.apply_equalization(
        signal=signal,
        speaker=speaker_setup,
        level=False,
        frequency=True,
    )

    # Assert
    assert isinstance(result, slab.Sound)
    assert result is not signal
    assert result.samplerate == samplerate

    np.testing.assert_allclose(
        result.data,
        original_data * 0.5,
    )
    np.testing.assert_allclose(
        signal.data,
        original_data,
    )


def test_apply_equalization_raises_error_when_filter_is_missing(
    speaker_setup,
):
    # Arrange
    signal = slab.Sound.whitenoise(
        duration=0.01,
        samplerate=48828,
    )
    speaker_setup.filter = None

    # Act and Assert
    with pytest.raises(
        ValueError,
        match="speaker not frequency-equalized",
    ):
        ff.apply_equalization(
            signal=signal,
            speaker=speaker_setup,
            level=False,
            frequency=True,
        )


def test_apply_equalization_returns_copy_when_corrections_are_disabled(
    speaker_setup,
):
    # Arrange
    signal = slab.Sound.whitenoise(
        duration=0.01,
        samplerate=48828,
    )
    original_data = signal.data.copy()

    # Act
    result = ff.apply_equalization(
        signal=signal,
        speaker=speaker_setup,
        level=False,
        frequency=False,
    )

    # Assert
    assert isinstance(result, slab.Sound)
    assert result is not signal

    np.testing.assert_allclose(
        result.data,
        original_data,
    )
    np.testing.assert_allclose(
        signal.data,
        original_data,
    )


def test_apply_equalization_applies_level_and_frequency_filter(
    speaker_setup,
):
    # Arrange
    samplerate = 48828
    signal = slab.Sound.whitenoise(
        duration=0.01,
        samplerate=samplerate,
    )
    signal.level = 40

    speaker_setup.level = 65
    speaker_setup.filter = slab.Filter(
        data=np.array([0.5]),
        samplerate=samplerate,
        fir="IR",
    )

    # Act
    result = ff.apply_equalization(
        signal=signal,
        speaker=speaker_setup,
        level=True,
        frequency=True,
    )

    # Assert
    assert isinstance(result, slab.Sound)
    assert result is not signal
    assert signal.level == pytest.approx(40)
    expected_level = 65 + 20 * np.log10(0.5)
    assert result.level == pytest.approx(expected_level)