from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import freefield
from freefield.setups import SETUPS, Setup
import slab

def plot_setup(setup):

    # Check input

    if isinstance(setup, str):
        setup_name = setup.lower()

        try:
            setup = SETUPS[setup_name]
        except KeyError:
            raise ValueError(
                f"Unknown setup {setup!r}. "
                f"Available setups are: {', '.join(SETUPS)}"
            )

    elif isinstance(setup, Setup):
        setup = setup


    else:
        raise TypeError(
            f"Argument 'setup' must be a string or Setup object, "
            f"got {type(setup).__name__} instead."
        )

    # Load speakertable
    speakers = freefield.read_speaker_table(setup)

    azi = np.array([speaker.azimuth for speaker in speakers])
    ele = np.array([speaker.elevation for speaker in speakers])
    dis = np.array([speaker.distance for speaker in speakers])
    idx = np.array([speaker.index for speaker in speakers])


    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    fig.set_size_inches(15, 15)

    azi = np.deg2rad(azi)
    ele = np.deg2rad(ele - 90)

    x = dis * np.sin(ele) * np.cos(azi)
    y = dis * np.sin(ele) * np.sin(azi)
    z = dis * np.cos(ele)

    # Use the same scale for all axes
    max_range = max(
        np.ptp(x),
        np.ptp(y),
        np.ptp(z),
    )

    x_mid = (np.max(x) + np.min(x)) / 2
    y_mid = (np.max(y) + np.min(y)) / 2
    z_mid = (np.max(z) + np.min(z)) / 2

    ax.set_xlim(x_mid - max_range / 2, x_mid + max_range / 2)
    ax.set_ylim(y_mid - max_range / 2, y_mid + max_range / 2)
    ax.set_zlim(z_mid - max_range / 2, z_mid + max_range / 2)

    ax.set_box_aspect((1, 1, 1))

    ax.scatter(x, y, z, c="b", marker=".")
    ax.scatter(0, 0, 0, c="r", marker="o")
    for i in range(len(speakers)):
        ax.text(x[i], y[i], z[i] + 0.15, str(idx[i]))

    return fig, ax

def plot_sources(azimuth, elevation, distance=1.4):
    """Display sources in a 3D plot.

    Arguments:
        azimuth (np.ndarray): Azimuth of the sources in degrees.
            Must have the same length as elevation.
        elevation (np.ndarray): Elevation of the sources in degrees.
            Must have the same length as azimuth.
        distance (float | np.ndarray): Distance of the sources to the listener.
            Can either be an array with the same length as azimuth and elevation,
            or a single float if all sources have the same distance.
    """
    fig = plt.figure()
    ax = fig.add_subplot(222, projection="3d")

    azimuth = np.deg2rad(azimuth)
    elevation = np.deg2rad(elevation - 90)

    x = distance * np.sin(elevation) * np.cos(azimuth)
    y = distance * np.sin(elevation) * np.sin(azimuth)
    z = distance * np.cos(elevation)

    # Use the same scale for all axes
    max_range = max(
        np.ptp(x),
        np.ptp(y),
        np.ptp(z),
    )

    x_mid = (np.max(x) + np.min(x)) / 2
    y_mid = (np.max(y) + np.min(y)) / 2
    z_mid = (np.max(z) + np.min(z)) / 2

    ax.set_xlim(x_mid - max_range / 2, x_mid + max_range / 2)
    ax.set_ylim(y_mid - max_range / 2, y_mid + max_range / 2)
    ax.set_zlim(z_mid - max_range / 2, z_mid + max_range / 2)

    ax.set_box_aspect((1, 1, 1))

    ax.scatter(x, y, z, c="b", marker=".")
    ax.scatter(0, 0, 0, c="r", marker="o")


    return fig, ax


if __name__ == '__main__':
    speakers = freefield.read_speaker_table()
    azi = np.array([speaker.azimuth for speaker in speakers])
    ele = np.array([speaker.elevation for speaker in speakers])
    dis = np.array([speaker.distance for speaker in speakers])
    plot_sources(azi, ele)

# def _plot_equalization(target, signal, filt, speaker_nr, low_cutoff=50,
#                        high_cutoff=20000, bandwidth=1/8):
#     """
#     Make a plot to show the effect of the equalizing FIR-filter on the
#     signal in the time and frequency domain. The plot is saved to the log
#     folder (existing plots are overwritten)
#     """
#     row = speaker_from_number(speaker_nr)  # get the speaker
#     signal_filt = filt.apply(signal)  # apply the filter to the signal
#     fig, ax = plt.subplots(2, 2, figsize=(16., 8.))
#     fig.suptitle("Equalization Speaker Nr. %s at Azimuth: %s and "
#                  "Elevation: %s" % (speaker_nr, row[2], row[3]))
#     ax[0, 0].set(title="Power per ERB-Subband", ylabel="A")
#     ax[0, 1].set(title="Time Series", ylabel="Amplitude in Volts")
#     ax[1, 0].set(title="Equalization Filter Transfer Function",
#                  xlabel="Frequency in Hz", ylabel="Amplitude in dB")
#     ax[1, 1].set(title="Filter Impulse Response",
#                  xlabel="Time in ms", ylabel="Amplitude")
#     # get level per subband for target, signal and filtered signal
#     fbank = slab.Filter.cos_filterbank(
#         1000, bandwidth, low_cutoff, high_cutoff, signal.samplerate)
#     center_freqs, _, _ = slab.Filter._center_freqs(low_cutoff, high_cutoff, bandwidth)
#     center_freqs = slab.Filter._erb2freq(center_freqs)
#     for data, name, color in zip([target, signal, signal_filt],
#                                  ["target", "signal", "filtered"],
#                                  ["red", "blue", "green"]):
#         levels = fbank.apply(data).level
#         ax[0, 0].plot(center_freqs, levels, label=name, color=color)
#         ax[0, 1].plot(data.times*1000, data.data, alpha=0.5, color=color)
#     ax[0, 0].legend()
#     w, h = filt.tf(plot=False)
#     ax[1, 0].semilogx(w, h, c="black")
#     ax[1, 1].plot(filt.times, filt.data, c="black")
#     fig.savefig(_location.parent/Path("log/speaker_%s_equalization.pdf"
#                                       % (speaker_nr)), dpi=800)
#     plt.close()
