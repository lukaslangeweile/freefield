import matplotlib.pyplot as plt
import numpy as np
import freefield
from freefield.setups import SETUPS, Setup


def plot_setup(setup, close_threshold=0.20, label_offset=0.07):
    """
    Plot all loudspeakers of a setup in 3D.

    Speaker indices are displayed next to their positions. If speakers are
    spatially close to each other, the vertical text offset alternates to
    reduce overlap.

    Arguments:
        setup (str | Setup): Setup whose loudspeakers should be plotted.
        close_threshold (float): Distance in meters below which two speakers
            are considered close.
        label_offset (float): Vertical offset of speaker index labels in meters.

    Returns:
        tuple: Matplotlib figure and axes objects.
    """

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

    # Load speaker table
    speakers = freefield.read_speaker_table(setup)

    azi = np.array([speaker.azimuth for speaker in speakers])
    ele = np.array([speaker.elevation for speaker in speakers])
    dis = np.array([speaker.distance for speaker in speakers])
    idx = np.array([speaker.index for speaker in speakers])

    # Convert spherical coordinates to Cartesian coordinates
    azi = np.deg2rad(azi)
    ele = np.deg2rad(ele - 90)

    x = dis * np.sin(ele) * np.cos(azi)
    y = dis * np.sin(ele) * np.sin(azi)
    z = dis * np.cos(ele)

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    fig.set_size_inches(15, 15)

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

    # Plot speakers and listener
    scatter = ax.scatter(x, y, z, c="b", marker=".")
    ax.scatter(0, 0, 0, c="r", marker="o")

    # Keep track of the offset used for every label
    label_offsets = np.full(len(speakers), label_offset, dtype=float)

    for i in range(len(speakers)):
        offset_correction = 0
        if i > 0:
            # Distances to all speakers whose labels have already been placed
            distances = np.sqrt(
                (x[i] - x[:i]) ** 2
                + (y[i] - y[:i]) ** 2
                + (z[i] - z[:i]) ** 2
            )

            close_speakers = np.where(distances <= close_threshold)[0]

            if len(close_speakers) > 0:
                # Find the closest already labelled speaker
                closest = close_speakers[np.argmin(distances[close_speakers])]

                # Put this label on the opposite side
                label_offsets[i] = -label_offsets[closest]

            if label_offsets[i] < 0:
                offset_correction = -0.07

        ax.text(
            x[i],
            y[i],
            z[i] + label_offsets[i] + offset_correction,
            str(idx[i]),
        )

    return fig, ax, scatter

def update_setup_plot(fig, scatter, speakers, active=None, done=None):
    """
    Update speaker colors in a setup plot.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure containing the setup plot.

    scatter : matplotlib.collections.PathCollection
        Scatter object containing the speaker markers.

    speakers : list[Speaker]
        Speakers shown in the scatter plot. Their order must correspond
        to the order of points in `scatter`.

    active : Speaker | None
        Speaker currently being checked.

    done : list[Speaker] | None
        Speakers that have already been confirmed.
    """

    if done is None:
        done = []
    done_indices = {speaker.index for speaker in done}
    active_index = active.index if active is not None else None

    colors = []


    for speaker in speakers:
        if speaker.index == active_index:
            # currently tested speaker
            colors.append("tab:orange")
        elif speaker.index in done_indices:
            # successfully checked speaker
            colors.append("tab:green")
        else:
            # not tested yet
            colors.append("lightgray")

    scatter.set_color(colors)

    # redraw plot
    fig.canvas.draw_idle()
    fig.canvas.flush_events()


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

    scatter = ax.scatter(x, y, z, c="b", marker=".")
    ax.scatter(0, 0, 0, c="r", marker="o")

    return fig, ax, scatter


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
