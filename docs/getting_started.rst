Getting Started
===============

.. _installation:

Installation
############

Freefield requires Python 3.8 or later. The Linux CI covers Python 3.8 and 3.12.
For FLIR cameras, choose a Python version supported by the Spinnaker SDK and its
Python wheel for your operating system and architecture.

Python environment
^^^^^^^^^^^^^^^^^^

Create and activate a separate environment. This example uses Conda with
Python 3.12.

.. code-block:: bash

    conda create --name freefield python=3.12 pip
    conda activate freefield

Python package
^^^^^^^^^^^^^^

Clone or download the Freefield version you want to use and run the appropriate
command from the root of that checkout. Pip installs the Python dependencies
for the selected configuration.

.. list-table::
   :header-rows: 1

   * - Use case
     - Command
   * - Base installation
     - ``python -m pip install .``
   * - Webcam or camera-based head pose estimation
     - ``python -m pip install ".[camera]"``
   * - Motion sensor
     - ``python -m pip install ".[sensor]"``
   * - Camera and motion sensor
     - ``python -m pip install ".[camera,sensor]"``

The camera extra includes OpenCV, Pillow, and the ``headpose`` package, which
uses PyTorch and Torchvision. For a FLIR camera, install the camera extra and
the matching Spinnaker SDK and Python wheel.

TDT processors
^^^^^^^^^^^^^^

On Windows, install the TDT drivers, RPvdsEx, and ActiveX Controls from
`TDT Downloads <https://www.tdt.com/support/downloads/>`_. Then install the
Python bindings for ActiveX in your Freefield environment.

.. code-block:: bash

    conda install pywin32

On macOS and Linux, Freefield simulates the TDT processor connection.

FLIR cameras
^^^^^^^^^^^^

Install the `Teledyne Spinnaker SDK <https://www.teledynevisionsolutions.com/products/spinnaker-sdk>`_
and obtain the Python wheel for the **same SDK version**. Select the wheel for
your CPython version, operating system, and architecture. A wheel tagged
``cp312-cp312-win_amd64`` targets 64-bit CPython 3.12 on Windows. Consult the
`Spinnaker Python installation guide <https://softwareservices.flir.com/Spinnaker/4.4/getting-started/python.html>`_
for SDK 4.4, or use the guide for your installed SDK version.

Install the downloaded wheel in the active Freefield environment. Replace the
example path with your wheel's path.

.. code-block:: bash

    python -m pip install "path/to/spinnaker_python-4.4.0.249-cp312-cp312-win_amd64.whl"
    python -c "import PySpin; print(PySpin.System)"

The Spinnaker wheel provides the ``PySpin`` import. The
`pyspin project on PyPI <https://pypi.org/project/pyspin/>`_ is a terminal spinner.

Verify the installation
^^^^^^^^^^^^^^^^^^^^^^^

From outside the checkout, run the following commands to check the installed
package and its loudspeaker table.

.. code-block:: bash

    python -m pip check
    python -c "import freefield; print(freefield.__version__); print(len(freefield.read_speaker_table('dome')))"

If you installed the camera extra, check its imports as well.

.. code-block:: bash

    python -c "import cv2; from headpose import PoseEstimator; print(cv2.__version__)"

For a FLIR installation, also check that the camera can acquire an image and
that Freefield can estimate head pose on the lab computer.

First Steps
###########

Once the installation is complete, start by importing and initializing freefield. Initialization selects the experimental setup and prepares the corresponding hardware configuration for use::

    import freefield

    # Initialize a setup using one of its default processor configurations.
    freefield.initialize(
        setup="dome",
        default="loctest_freefield",
    )

The setup argument specifies the experimental environment you want to use. For the predefined setups and available default modes, see :doc:`setups`.

Inspecting the Speakers
^^^^^^^^^^^^^^^^^^^^^^^

After initialization, you can access the loudspeakers defined for the current setup. Each loudspeaker is represented by a :class:`Speaker` object containing information such as its index, spatial position, and processor connection::

    speakers = freefield.read_speaker_table()

    print(speakers[0])

You can select individual loudspeakers by their index using :func:`freefield.pick_speakers`::

    speaker = freefield.pick_speakers(10)[0]

Loudspeakers can also be selected based on their spatial position. For example, to select the loudspeaker located directly in front of the listener at ear level::

    speaker = freefield.pick_speakers(
        (0, 0, 1.4)
    )[0]

Here, the tuple specifies azimuth, elevation, and distance.

Playing a Sound
^^^^^^^^^^^^^^^

Freefield handles communication with the playback processors, while the actual sound can be generated using any suitable Python package. The following example uses `slab <https://slab.readthedocs.io/en/latest/>`_ to create a short pink-noise stimulus::

    import slab

    stimulus = slab.Sound.pinknoise(duration=0.5)

Before playback, the processor needs to know the length of the playback buffer::

    freefield.write(
        tag="playbuflen",
        value=stimulus.n_samples,
        processors=["RX81", "RX82"],
    )

The stimulus can then be assigned to the selected loudspeaker and played::

    freefield.set_signal_and_speaker(
        signal=stimulus.data.flatten(),
        speaker=speaker,
    )

    freefield.play()

From here, the same basic operations can be combined into complete experimental procedures. See :doc:`worked_examples` for examples of a sound-localization experiment and a Minimum Audible Angle experiment.

Ending a Session
^^^^^^^^^^^^^^^^

When you are finished using the setup, stop the initialized devices with::

    freefield.halt()