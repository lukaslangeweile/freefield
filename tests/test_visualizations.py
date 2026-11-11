import numpy as np
import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock

import freefield.visualizations as visualizations


@pytest.fixture
def mock_axes(monkeypatch):
    """Replace the matplotlib 3D axes with a mock."""
    figure = MagicMock()
    ax = figure.add_subplot.return_value

    monkeypatch.setattr(
        visualizations.plt,
        "figure",
        MagicMock(return_value=figure),
    )

    return ax


def test_plot_sources_creates_3d_axes(monkeypatch):
    """plot_sources should create a figure and 3D axes."""
    figure = MagicMock()
    mock_figure = MagicMock(return_value=figure)

    monkeypatch.setattr(
        visualizations.plt,
        "figure",
        mock_figure,
    )
    result = visualizations.plot_sources(
        azimuth=np.array([0]),
        elevation=np.array([0]),
    )

    mock_figure.assert_called_once_with()
    figure.add_subplot.assert_called_once_with(222, projection="3d")
    ax = figure.add_subplot.return_value
    assert result == (figure, ax, ax.scatter.return_value)


@pytest.mark.parametrize(
    "azimuth,elevation,expected_x,expected_y,expected_z",
    [
        (
            np.array([0]),
            np.array([0]),
            np.array([-1.4]),
            np.array([0.0]),
            np.array([0.0]),
        ),
        (
            np.array([90]),
            np.array([0]),
            np.array([0.0]),
            np.array([-1.4]),
            np.array([0.0]),
        ),
        (
            np.array([0]),
            np.array([90]),
            np.array([0.0]),
            np.array([0.0]),
            np.array([1.4]),
        ),
    ],
)
def test_plot_sources_calculates_expected_coordinates(
    mock_axes,
    azimuth,
    elevation,
    expected_x,
    expected_y,
    expected_z,
):
    """Source positions should be converted to the expected Cartesian coordinates."""
    visualizations.plot_sources(
        azimuth=azimuth,
        elevation=elevation,
    )

    source_call = mock_axes.scatter.call_args_list[0]

    x, y, z = source_call.args

    np.testing.assert_allclose(x, expected_x, atol=1e-10)
    np.testing.assert_allclose(y, expected_y, atol=1e-10)
    np.testing.assert_allclose(z, expected_z, atol=1e-10)


def test_plot_sources_uses_custom_scalar_distance(mock_axes):
    """A scalar distance should be applied to all sources."""
    azimuth = np.array([0, 90])
    elevation = np.array([0, 0])
    distance = 2.0

    visualizations.plot_sources(
        azimuth=azimuth,
        elevation=elevation,
        distance=distance,
    )

    source_call = mock_axes.scatter.call_args_list[0]
    x, y, z = source_call.args

    np.testing.assert_allclose(
        x,
        np.array([-2.0, 0.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        y,
        np.array([0.0, -2.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        z,
        np.array([0.0, 0.0]),
        atol=1e-10,
    )


def test_plot_sources_accepts_distance_array(mock_axes):
    """Individual distances should be applied to the corresponding sources."""
    azimuth = np.array([0, 90])
    elevation = np.array([0, 0])
    distance = np.array([1.0, 2.0])

    visualizations.plot_sources(
        azimuth=azimuth,
        elevation=elevation,
        distance=distance,
    )

    source_call = mock_axes.scatter.call_args_list[0]
    x, y, z = source_call.args

    np.testing.assert_allclose(
        x,
        np.array([-1.0, 0.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        y,
        np.array([0.0, -2.0]),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        z,
        np.array([0.0, 0.0]),
        atol=1e-10,
    )


def test_plot_sources_plots_all_sources(mock_axes):
    """All supplied source positions should be passed to scatter."""
    azimuth = np.array([-90, 0, 90])
    elevation = np.array([0, 0, 0])

    visualizations.plot_sources(
        azimuth=azimuth,
        elevation=elevation,
    )

    source_call = mock_axes.scatter.call_args_list[0]

    x, y, z = source_call.args

    assert len(x) == 3
    assert len(y) == 3
    assert len(z) == 3


def test_plot_sources_plots_sources_with_expected_style(mock_axes):
    """Sources should be plotted as blue points."""
    visualizations.plot_sources(
        azimuth=np.array([0]),
        elevation=np.array([0]),
    )

    source_call = mock_axes.scatter.call_args_list[0]

    assert source_call.kwargs == {
        "c": "b",
        "marker": ".",
    }


def test_plot_sources_plots_listener_at_origin(mock_axes):
    """The listener should be plotted as a red circle at the origin."""
    visualizations.plot_sources(
        azimuth=np.array([0]),
        elevation=np.array([0]),
    )

    assert mock_axes.scatter.call_count == 2

    listener_call = mock_axes.scatter.call_args_list[1]

    assert listener_call.args == (0, 0, 0)
    assert listener_call.kwargs == {
        "c": "r",
        "marker": "o",
    }


@pytest.fixture
def speakers():
    """Known positions with distinct distances and nonconsecutive indices."""
    return [
        SimpleNamespace(index=7, azimuth=0, elevation=0, distance=1.0),
        SimpleNamespace(index=2, azimuth=90, elevation=0, distance=2.0),
        SimpleNamespace(index=11, azimuth=0, elevation=90, distance=3.0),
    ]


@pytest.fixture
def speaker_table(monkeypatch, speakers):
    read_table = MagicMock(return_value=speakers)
    monkeypatch.setattr(visualizations.freefield, "read_speaker_table", read_table)
    return read_table


@pytest.mark.parametrize("name", list(visualizations.SETUPS))
@pytest.mark.parametrize("uppercase", [False, True])
def test_plot_setup_resolves_names(mock_axes, speaker_table, name, uppercase):
    visualizations.plot_setup(name.upper() if uppercase else name)

    speaker_table.assert_called_once_with(visualizations.SETUPS[name])


def test_plot_setup_accepts_custom_setup(mock_axes, speaker_table):
    setup = visualizations.Setup(
        name="custom",
        speaker_table="custom_speakers.txt",
        calibration_file="custom_calibration.pkl",
        playback_processors=("RX81",),
        recording_processor=None,
    )

    visualizations.plot_setup(setup)

    speaker_table.assert_called_once_with(setup)


@pytest.mark.parametrize(
    "setup,error,message",
    [
        ("unknown_setup", ValueError, "Unknown setup"),
        (None, TypeError, "must be a string or Setup object"),
        (42, TypeError, "must be a string or Setup object"),
        ([], TypeError, "must be a string or Setup object"),
    ],
)
def test_plot_setup_rejects_invalid_setup(
    mock_axes, speaker_table, setup, error, message
):
    with pytest.raises(error, match=message):
        visualizations.plot_setup(setup)

    speaker_table.assert_not_called()
    visualizations.plt.figure.assert_not_called()


def test_plot_setup_returns_plot_objects(mock_axes, speaker_table):
    result = visualizations.plot_setup("dome")

    figure = visualizations.plt.figure.return_value
    figure.add_subplot.assert_called_once_with(111, projection="3d")
    assert result == (figure, mock_axes, mock_axes.scatter.return_value)


def test_plot_setup_plots_speaker_coordinates_and_listener(mock_axes, speaker_table):
    visualizations.plot_setup("dome")

    assert mock_axes.scatter.call_count == 2
    sources, listener = mock_axes.scatter.call_args_list
    np.testing.assert_allclose(
        sources.args,
        [[-1, 0, 0], [0, -2, 0], [0, 0, 3]],
        atol=1e-10,
    )
    assert sources.kwargs == {"c": "b", "marker": "."}
    assert listener.args == (0, 0, 0)
    assert listener.kwargs == {"c": "r", "marker": "o"}


@pytest.mark.parametrize("plot", ["sources", "setup"])
def test_plots_use_equal_axis_ranges(mock_axes, speaker_table, plot):
    """The longest spatial extent sets the range of every axis."""
    if plot == "sources":
        visualizations.plot_sources(
            azimuth=np.array([0, 90, 0]),
            elevation=np.array([0, 0, 90]),
            distance=np.array([1.0, 2.0, 3.0]),
        )
    else:
        visualizations.plot_setup("dome")

    np.testing.assert_allclose(mock_axes.set_xlim.call_args.args, [-2.0, 1.0])
    np.testing.assert_allclose(mock_axes.set_ylim.call_args.args, [-2.5, 0.5])
    np.testing.assert_allclose(mock_axes.set_zlim.call_args.args, [0.0, 3.0])
    mock_axes.set_box_aspect.assert_called_once_with((1, 1, 1))


@pytest.mark.parametrize("label_offset", [0.07, 0.15])
def test_plot_setup_labels_speaker_indices(
    mock_axes, speaker_table, speakers, label_offset
):
    visualizations.plot_setup("dome", label_offset=label_offset)

    assert mock_axes.text.call_count == len(speakers)
    positions = [(-1, 0, 0), (0, -2, 0), (0, 0, 3)]
    for call, speaker, (x, y, z) in zip(
        mock_axes.text.call_args_list, speakers, positions
    ):
        np.testing.assert_allclose(call.args[:3], [x, y, z + label_offset], atol=1e-10)
        assert call.args[3] == str(speaker.index)


@pytest.mark.parametrize(
    "close_threshold,expected_sides",
    [
        (0.01, [1, 1, 1, 1]),
        (0.125, [1, -1, 1, 1]),
        (0.20, [1, -1, 1, 1]),
    ],
)
def test_plot_setup_alternates_labels_near_closest_speaker(
    mock_axes, speaker_table, close_threshold, expected_sides
):
    """Nearby labels alternate, including at the distance threshold."""
    nearby = [
        SimpleNamespace(index=i, azimuth=0, elevation=0, distance=distance)
        for i, distance in enumerate([1.0, 1.125, 1.15625, 2.0])
    ]
    speaker_table.return_value = nearby

    visualizations.plot_setup("dome", close_threshold=close_threshold)

    assert mock_axes.text.call_count == len(nearby)
    for call, side in zip(mock_axes.text.call_args_list, expected_sides):
        assert np.sign(call.args[2]) == side


@pytest.mark.parametrize(
    "active_index,done_indices,expected_colors",
    [
        (None, None, ["lightgray", "lightgray", "lightgray"]),
        (None, [], ["lightgray", "lightgray", "lightgray"]),
        (2, [], ["lightgray", "tab:orange", "lightgray"]),
        (None, [11, 7], ["tab:green", "lightgray", "tab:green"]),
        (2, [7, 2], ["tab:green", "tab:orange", "lightgray"]),
        (99, [99], ["lightgray", "lightgray", "lightgray"]),
    ],
)
def test_update_setup_plot_colors_by_speaker_index(
    speakers, active_index, done_indices, expected_colors
):
    """Status uses indices, preserves plot order, and gives active priority."""
    figure = MagicMock()
    scatter = MagicMock()
    active = SimpleNamespace(index=active_index) if active_index is not None else None
    done = (
        [SimpleNamespace(index=index) for index in done_indices]
        if done_indices is not None else None
    )

    visualizations.update_setup_plot(figure, scatter, speakers, active=active, done=done)

    scatter.set_color.assert_called_once_with(expected_colors)
    figure.canvas.draw_idle.assert_called_once_with()
    figure.canvas.flush_events.assert_called_once_with()


def test_update_setup_plot_resets_previous_status(speakers):
    figure = MagicMock()
    scatter = MagicMock()
    done = [speakers[0]]

    visualizations.update_setup_plot(figure, scatter, speakers, active=speakers[1], done=done)
    visualizations.update_setup_plot(figure, scatter, speakers)

    assert scatter.set_color.call_args.args == (["lightgray"] * 3,)
    assert done == [speakers[0]]


@pytest.mark.parametrize("plot", ["sources", "setup"])
def test_plots_render_with_matplotlib(monkeypatch, speaker_table, plot):
    """Exercise real 3D plotting without opening a window or requiring hardware."""
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    figure = Figure()
    FigureCanvasAgg(figure)
    monkeypatch.setattr(visualizations.plt, "figure", lambda: figure)

    if plot == "sources":
        result = visualizations.plot_sources(
            np.array([0, 90, 0]), np.array([0, 0, 90])
        )
    else:
        result = visualizations.plot_setup("dome")

    fig, axes, scatter = result
    assert fig is figure
    assert axes.name == "3d"
    assert scatter in axes.collections
    assert len(axes.collections) == 2
    figure.canvas.draw()


