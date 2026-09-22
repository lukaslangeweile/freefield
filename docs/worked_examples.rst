Worked Examples
###############
Here you can get an impression of typical workflows with the freefield library. The code presented uses the
`slab library <https://slab.readthedocs.io/en/latest/>`_ to create Sound objects, whose data is passed over to the freefield functions.
We also use it here to create trial sequences.

Localisation Test
-----------------
Runs a Localisation Test for speakers across the azimuth of the dome setup. ::

    import time
    import freefield
    import slab


    # Initialize the free-field setup.
    # Sensor tracking is used to record the perceived sound direction.
    freefield.initialize(
        setup="dome",
        default="loctest_freefield",
        sensor_tracking=True,
    )

    # Select loudspeakers located in the horizontal plane.
    speaker_indices = [1, 2, 3, 4, 5, 6, 7]

    # Create a randomized trial sequence.
    n_reps = 4
    sequence = slab.Trialsequence(
        conditions=speaker_indices,
        n_reps=n_reps,
        kind="non_repeating",
    )

    # Use the same broadband stimulus for every trial.
    stimulus = slab.Sound.pinknoise(duration=0.5)

    # The buffer length is identical for every trial and only needs to be set once.
    freefield.write(
        tag="playbuflen",
        value=stimulus.n_samples,
        processors=["RX81", "RX82"],
    )

    freefield.play_start_sound()

    for speaker_index in sequence:

        # The participant presses the button when the head is returned to center position
        freefield.wait_for_button(
            proc="RP2",
            tag="response",
        )

        speaker = freefield.pick_speakers(speaker_index)[0]

        # Present the stimulus from the target loudspeaker.
        freefield.set_signal_and_speaker(
            signal=stimulus.data.flatten(),
            speaker=speaker,
        )
        freefield.play()

        # The participant turns their head towards the perceived sound location
        # and presses the response button.
        freefield.wait_for_button(
            proc="RP2",
            tag="response",
        )

        response = freefield.get_head_pose(
            method="sensor",
            convention="psychoacoustics",
        )

        sequence.add_response(response)

Minimum Audible Angle (MMA) Experiment
--------------------------------------
Determines the Minimum Audible Angle, i.e. the just noticable difference in sound presentation angle, for the azimuth with
the arc setup::

    import random
    import time
    import freefield
    import slab


    # Initialize the loudspeaker array and response button.
    freefield.initialize(
        setup="arc",
        device=[
            ["RX81", "RX8", "play_buf.rcx"],
            ["RX82", "RX8", "play_buf.rcx"],
            ["RP2", "RP2", "button.rcx"],
        ],
    )

    # Experimental parameters.
    reference_azimuth = 0
    speaker_spacing = 4.28
    elevation = 0
    distance = 1.4
    isi = 0.3

    # Use the same stimulus in every interval.
    stimulus = slab.Sound.pinknoise(duration=0.2)

    freefield.write(
        tag="playbuflen",
        value=stimulus.n_samples,
        processors=["RX81", "RX82"],
    )

    # Find the loudspeaker at the reference position.
    reference_speaker = freefield.pick_speakers(
        (reference_azimuth, elevation, distance)
    )[0]

    # The staircase controls the angular separation between
    # the reference and deviant loudspeaker.
    staircase = slab.Staircase(
        start_val=7 * speaker_spacing,
        n_reversals=10,
        step_sizes=[
            2 * speaker_spacing,
            speaker_spacing,
        ],
        n_up=1,
        n_down=2,
        min_val=speaker_spacing,
        max_val=7 * speaker_spacing,
    )

    for separation in staircase:

        # Randomly place the deviant to the left or right
        # of the reference position.
        direction = random.choice([-1, 1])

        deviant_azimuth = (
            reference_azimuth
            + direction * separation
        )

        deviant_speaker = freefield.pick_speakers(
            (deviant_azimuth, elevation, distance)
        )[0]

        # Randomly select which of the three intervals contains the deviant.
        target_interval = random.randrange(3)

        trial_speakers = [
            reference_speaker,
            reference_speaker,
            reference_speaker,
        ]

        trial_speakers[target_interval] = deviant_speaker

        # Present the three intervals.
        for speaker in trial_speakers:

            freefield.set_signal_and_speaker(
                signal=stimulus.data.flatten(),
                speaker=speaker,
            )

            freefield.play()

            time.sleep(isi)

        # Ask the participant which interval contained the deviant.
        freefield.wait_for_button(
            proc="RP2",
            tag="response",
        )

        response = freefield.read(
            tag="response",
            processor="RP2",
        )

        # This assumes that the response buttons are encoded as 1, 2, and 3.
        correct_response = target_interval + 1

        correct = response == correct_response

        staircase.add_response(correct)

    print(
        f"Estimated MAA: {staircase.threshold():.2f} degrees"
    )
