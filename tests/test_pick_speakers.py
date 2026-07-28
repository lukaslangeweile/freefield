import freefield.freefield as ff
import pytest
import numpy as np


@pytest.fixture
def speaker_setup(monkeypatch):
    # create Speakers
    speaker_index_2 = ff.Speaker(
        index=2,
        analog_channel=0,
        analog_proc="RX8",
        digital_proc="RX8",
        azimuth=30,
        elevation=12.5,
        distance=1.4,
        digital_channel=0,
    )

    speaker_index_3 = ff.Speaker(
        index=3,
        analog_channel=0,
        analog_proc="RX8",
        digital_proc="RX8",
        azimuth=20,
        elevation=12.5,
        distance=1.4,
        digital_channel=0,
    )

    speaker_index_4 = ff.Speaker(
        index=4,
        analog_channel=0,
        analog_proc="RX8",
        digital_proc="RX8",
        azimuth=35,
        elevation=12.5,
        distance=1.4,
        digital_channel=0,
    )

    speakers_by_index = {
        2: speaker_index_2,
        3: speaker_index_3,
        4: speaker_index_4,
    }

    # patch SPEAKERS
    monkeypatch.setattr(
        ff,
        "SPEAKERS",
        list(speakers_by_index.values()),
    )
    # return
    return speakers_by_index


def test_pick_speakers_returns_speaker_for_existing_index(speaker_setup):
    # Diagnose der Testvoraussetzungen
    assert [speaker.index for speaker in ff.SPEAKERS] == [2, 3, 4]
    assert ff.SPEAKERS[0] is speaker_setup[2]

    # Act
    result = ff.pick_speakers(2)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] is speaker_setup[2]

def test_pick_speakers_returns_empty_list_for_non_existing_index(speaker_setup):
    # Act
    result = ff.pick_speakers(99)

    # Assert
    assert result == []

def test_pick_speakers_returns_speakers_for_existing_indices(speaker_setup):
    # Act
    result = ff.pick_speakers([4, 2])

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] is speaker_setup[2]
    assert result[1] is speaker_setup[4]

def test_pick_speakers_returns_each_speaker_only_once_for_duplicate_indices(speaker_setup):
    # Act
    result = ff.pick_speakers([2, 2])

    # Assert
    assert result == [speaker_setup[2]]

def test_pick_speakers_returns_speaker_for_existing_coordinates(speaker_setup):
    # Act
    result = ff.pick_speakers((30, 12.5, 1.4))

    # Assert
    assert result == [speaker_setup[2]]

def test_pick_speakers_returns_empty_list_for_non_existing_coordinates(speaker_setup):
    # Act
    result = ff.pick_speakers((90, 17.5, 0.4))

    # Assert
    assert result == []

def test_pick_speakers_returns_speakers_for_coordinate_list(speaker_setup):
    # Arrange
    coordinates = [
        (35, 12.5, 1.4),
        (30, 12.5, 1.4),
    ]

    # Act
    result = ff.pick_speakers(coordinates)

    # Assert
    assert len(result) == 2
    assert result[0] is speaker_setup[2]
    assert result[1] is speaker_setup[4]


def test_pick_speakers_returns_single_speaker_object(speaker_setup):
    # Arrange
    selected_speaker = speaker_setup[3]

    # Act
    result = ff.pick_speakers(selected_speaker)

    # Assert
    assert len(result) == 1
    assert result[0] is selected_speaker


def test_pick_speakers_returns_list_of_speaker_objects(speaker_setup):
    # Arrange
    selected_speakers = [
        speaker_setup[4],
        speaker_setup[2],
    ]

    # Act
    result = ff.pick_speakers(selected_speakers)

    # Assert
    assert len(result) == 2
    assert result[0] is speaker_setup[4]
    assert result[1] is speaker_setup[2]


@pytest.mark.parametrize(
    "numpy_index",
    [
        np.int32(3),
        np.int64(3),
    ],
)
def test_pick_speakers_accepts_numpy_integer_index(
    speaker_setup,
    numpy_index,
):
    # Act
    result = ff.pick_speakers(numpy_index)

    # Assert
    assert len(result) == 1
    assert result[0] is speaker_setup[3]


def test_pick_speakers_accepts_numpy_array_of_indices(speaker_setup):
    # Arrange
    indices = np.array([4, 2], dtype=np.int64)

    # Act
    result = ff.pick_speakers(indices)

    # Assert
    assert len(result) == 2
    assert result[0] is speaker_setup[2]
    assert result[1] is speaker_setup[4]


def test_pick_speakers_returns_empty_list_for_empty_selection(speaker_setup):
    # Act
    result = ff.pick_speakers([])

    # Assert
    assert result == []