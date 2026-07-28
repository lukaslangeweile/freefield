import freefield.freefield as ff
import pytest
import numpy as np

import numpy as np

import freefield.freefield as ff


def test_read_speaker_table_assigns_columns_correctly(monkeypatch):
    # Arrange
    table = np.array(
        [
            ["0", "22", "RX82", "-52.5", "25", "1.4", "", ""],
            ["1", "23", "RX82", "52.5", "25", "1.6", "7", "RX81"],
        ],
        dtype=str,
    )

    monkeypatch.setattr(
        ff.np,
        "loadtxt",
        lambda *args, **kwargs: table,
    )

    # Act
    result = ff.read_speaker_table()

    # Assert
    assert len(result) == 2

    speaker_0 = result[0]
    assert speaker_0.index == 0
    assert speaker_0.analog_channel == 22
    assert speaker_0.analog_proc == "RX82"
    assert speaker_0.azimuth == -52.5
    assert speaker_0.elevation == 25.0
    assert speaker_0.distance == 1.4
    assert speaker_0.digital_channel is None
    assert speaker_0.digital_proc is None

    speaker_1 = result[1]
    assert speaker_1.index == 1
    assert speaker_1.analog_channel == 23
    assert speaker_1.analog_proc == "RX82"
    assert speaker_1.azimuth == 52.5
    assert speaker_1.elevation == 25.0
    assert speaker_1.distance == 1.6
    assert speaker_1.digital_channel == 7.0
    assert speaker_1.digital_proc == "RX81"