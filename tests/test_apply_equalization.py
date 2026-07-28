from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import freefield.freefield as ff


class DummySound:
    def __init__(self, level):
        self.level = level


def test_apply_equalization_applies_level_to_copy(monkeypatch):
    # Arrange
    original_signal = DummySound(level=40)
    speaker = SimpleNamespace(level=65, filter=None)

    sound_constructor = Mock(return_value=original_signal)
    pick_speakers_mock = Mock(return_value=[speaker])

    monkeypatch.setattr(ff.slab, "Sound", sound_constructor)
    monkeypatch.setattr(ff, "pick_speakers", pick_speakers_mock)

    # Act
    result = ff.apply_equalization(
        signal=original_signal,
        speaker=2,
        level=True,
        frequency=False,
    )

    # Assert
    sound_constructor.assert_called_once_with(original_signal)
    pick_speakers_mock.assert_called_once_with(2)

    assert result is not original_signal
    assert result.level == 65
    assert original_signal.level == 40


def test_apply_equalization_raises_error_when_level_is_missing(monkeypatch):
    # Arrange
    original_signal = DummySound(level=40)
    speaker = SimpleNamespace(level=None, filter=None)

    monkeypatch.setattr(
        ff.slab,
        "Sound",
        Mock(return_value=original_signal),
    )
    monkeypatch.setattr(
        ff,
        "pick_speakers",
        Mock(return_value=[speaker]),
    )

    # Act and Assert
    with pytest.raises(
        ValueError,
        match="speaker not level-equalized",
    ):
        ff.apply_equalization(
            signal=original_signal,
            speaker=2,
            level=True,
            frequency=False,
        )

    assert original_signal.level == 40


def test_apply_equalization_applies_frequency_filter(monkeypatch):
    # Arrange
    original_signal = DummySound(level=40)
    filtered_signal = DummySound(level=40)

    frequency_filter = Mock()
    frequency_filter.apply.return_value = filtered_signal

    speaker = SimpleNamespace(
        level=None,
        filter=frequency_filter,
    )

    monkeypatch.setattr(
        ff.slab,
        "Sound",
        Mock(return_value=original_signal),
    )
    monkeypatch.setattr(
        ff,
        "pick_speakers",
        Mock(return_value=[speaker]),
    )

    # Act
    result = ff.apply_equalization(
        signal=original_signal,
        speaker=2,
        level=False,
        frequency=True,
    )

    # Assert
    frequency_filter.apply.assert_called_once()

    signal_passed_to_filter = frequency_filter.apply.call_args.args[0]

    assert signal_passed_to_filter is not original_signal
    assert result is filtered_signal
    assert original_signal.level == 40


def test_apply_equalization_raises_error_when_filter_is_missing(monkeypatch):
    # Arrange
    original_signal = DummySound(level=40)
    speaker = SimpleNamespace(level=None, filter=None)

    frequency_filter = Mock()

    monkeypatch.setattr(
        ff.slab,
        "Sound",
        Mock(return_value=original_signal),
    )
    monkeypatch.setattr(
        ff,
        "pick_speakers",
        Mock(return_value=[speaker]),
    )

    # Act and Assert
    with pytest.raises(
        ValueError,
        match="speaker not frequency-equalized",
    ):
        ff.apply_equalization(
            signal=original_signal,
            speaker=2,
            level=False,
            frequency=True,
        )

    frequency_filter.apply.assert_not_called()
    assert original_signal.level == 40


def test_apply_equalization_returns_copy_when_corrections_are_disabled(
    monkeypatch,
):
    # Arrange
    original_signal = DummySound(level=40)
    speaker = SimpleNamespace(level=None, filter=None)

    monkeypatch.setattr(
        ff.slab,
        "Sound",
        Mock(return_value=original_signal),
    )
    monkeypatch.setattr(
        ff,
        "pick_speakers",
        Mock(return_value=[speaker]),
    )

    # Act
    result = ff.apply_equalization(
        signal=original_signal,
        speaker=2,
        level=False,
        frequency=False,
    )

    # Assert
    assert result is not original_signal
    assert result.level == 40
    assert original_signal.level == 40


def test_apply_equalization_applies_level_before_frequency_filter(monkeypatch):
    # Arrange
    original_signal = DummySound(level=40)
    filtered_signal = DummySound(level=65)

    def apply_filter(signal):
        assert signal is not original_signal
        assert signal.level == 65
        return filtered_signal

    frequency_filter = Mock()
    frequency_filter.apply.side_effect = apply_filter

    speaker = SimpleNamespace(
        level=65,
        filter=frequency_filter,
    )

    monkeypatch.setattr(
        ff.slab,
        "Sound",
        Mock(return_value=original_signal),
    )
    monkeypatch.setattr(
        ff,
        "pick_speakers",
        Mock(return_value=[speaker]),
    )

    # Act
    result = ff.apply_equalization(
        signal=original_signal,
        speaker=2,
        level=True,
        frequency=True,
    )

    # Assert
    frequency_filter.apply.assert_called_once()

    assert result is filtered_signal
    assert result.level == 65
    assert original_signal.level == 40