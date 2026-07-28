import pickle

import pytest

import freefield.freefield as ff


@pytest.fixture
def speaker_setup(monkeypatch):
    speaker_2 = ff.Speaker(
        index=2,
        analog_channel=0,
        analog_proc="RX8",
        digital_proc="RX8",
        azimuth=30,
        elevation=12.5,
        distance=1.4,
        digital_channel=0,
    )

    speaker_3 = ff.Speaker(
        index=3,
        analog_channel=1,
        analog_proc="RX8",
        digital_proc="RX8",
        azimuth=-30,
        elevation=12.5,
        distance=1.4,
        digital_channel=1,
    )

    speaker_2.level = None
    speaker_2.filter = None
    speaker_3.level = None
    speaker_3.filter = None

    monkeypatch.setattr(
        ff,
        "SPEAKERS",
        [speaker_2, speaker_3],
    )

    return {
        2: speaker_2,
        3: speaker_3,
    }


def test_load_equalization_assigns_level_and_filter(
    tmp_path,
    speaker_setup,
):
    # Arrange
    equalization_file = tmp_path / "equalization.pkl"

    equalization = {
        2: {
            "level": 62.5,
            "filter": "filter-for-speaker-2",
        },
        3: {
            "level": 64.0,
            "filter": "filter-for-speaker-3",
        },
    }

    with open(equalization_file, "wb") as file:
        pickle.dump(equalization, file)

    # Act
    ff.load_equalization(file=equalization_file)

    # Assert
    assert speaker_setup[2].level == 62.5
    assert speaker_setup[2].filter == "filter-for-speaker-2"

    assert speaker_setup[3].level == 64.0
    assert speaker_setup[3].filter == "filter-for-speaker-3"

def test_load_equalization_ignores_level_if_false(
        tmp_path,
        speaker_setup,
):
    # Arrange
    equalization_file = tmp_path / "equalization.pkl"

    equalization = {
        2: {
            "level": 62.5,
            "filter": "filter-for-speaker-2",
        },
        3: {
            "level": 64.0,
            "filter": "filter-for-speaker-3",
        },
    }

    with open(equalization_file, "wb") as file:
        pickle.dump(equalization, file)

    # Act
    ff.load_equalization(file=equalization_file, level=False)

    # Assert
    assert speaker_setup[2].level is None
    assert speaker_setup[2].filter == "filter-for-speaker-2"

    assert speaker_setup[3].level is None
    assert speaker_setup[3].filter == "filter-for-speaker-3"

def test_load_equalization_ignores_filter_if_false(
        tmp_path,
        speaker_setup,
):
    # Arrange
    equalization_file = tmp_path / "equalization.pkl"

    equalization = {
        2: {
            "level": 62.5,
            "filter": "filter-for-speaker-2",
        },
        3: {
            "level": 64.0,
            "filter": "filter-for-speaker-3",
        },
    }

    with open(equalization_file, "wb") as file:
        pickle.dump(equalization, file)

    # Act
    ff.load_equalization(file=equalization_file, frequency=False)

    # Assert
    assert speaker_setup[2].level == 62.5
    assert speaker_setup[2].filter is None

    assert speaker_setup[3].level == 64.0
    assert speaker_setup[3].filter is None

def test_load_equalization_uses_default_file(
        tmp_path,
        speaker_setup,
        monkeypatch,
):
    # Arrange
    setup = "test_setup"

    monkeypatch.setattr(ff, "DIR", tmp_path)
    monkeypatch.setattr(ff, "SETUP", setup)

    data_directory = tmp_path / "data"
    data_directory.mkdir()

    equalization_file = data_directory / f"calibration_{setup}.pkl"

    equalization = {
        2: {
            "level": 62.5,
            "filter": "filter-for-speaker-2",
        },
        3: {
            "level": 64.0,
            "filter": "filter-for-speaker-3",
        },
    }

    with open(equalization_file, "wb") as file:
        pickle.dump(equalization, file)

    # Act: bewusst kein file-Argument übergeben
    ff.load_equalization()

    # Assert
    assert speaker_setup[2].level == 62.5
    assert speaker_setup[2].filter == "filter-for-speaker-2"

    assert speaker_setup[3].level == 64.0
    assert speaker_setup[3].filter == "filter-for-speaker-3"