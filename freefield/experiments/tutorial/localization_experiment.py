import freefield
import slab
import time

freefield.initialize(setup="dome", default="loctest_freefield", sensor_tracking=True)

speaker_indices = [1, 2, 3, 4, 5, 6, 7] #TODO: select indices for azimuthal speakers
speakers = freefield.pick_speakers(speaker_indices)
n_reps = 4
seq = slab.Trialsequence(speakers, n_reps, kind="non_repeating")

freefield.play_start_sound()

for speaker in seq:
    time.sleep(0.2)
    sound = slab.Sound.pinknoise(duration=0.5)
    freefield.write(tag="playbuflen", value=sound.n_samples, processors=["RX81", "RX82"])
    freefield.set_signal_and_speaker(signal=sound.data.flatten(), speaker=speaker)
    freefield.play()
    freefield.wait_for_button(proc="RP2", tag="response")
    pose = freefield.get_head_pose(method="sensor", convention="psychoacoustics")
    seq.add_response(pose)