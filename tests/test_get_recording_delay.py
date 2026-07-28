import freefield.freefield as ff

def test_get_recording_delay_returns_sound_travel_time_without_processors():
    # Arrange
    distance = 343
    sample_rate = 1000

    # Act
    result = ff.get_recording_delay(
        distance=distance,
        sample_rate=sample_rate,
    )

    # Assert
    assert result == 1000