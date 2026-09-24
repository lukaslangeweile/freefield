Getting Started
===============

Installation
############

.. _Installation:

The installation consists of two parts - the Python dependencies and the drivers for the hardware.
The latter is only relevant if you actually use the devices and is not required if you merely want to play around with the code.

Python dependencies
^^^^^^^^^^^^^^^^^^^
We recommend using Anaconda for the installation. If you are new to Python, take a look at the `install guide <https://www.anaconda.com/docs/getting-started/installation>`_ for Anaconda.

Once you installed Anaconda, create a new environment with the correct Python version (name it "freefield" for example):

.. code-block:: bash

    conda create --name freefield python=3.8

.. note::
    To use all the functionalities of freefield, Python 3.8 is required. However, if you do not plan to use head pose estimation you also can use more recent versions.

Activate the environment and install pip, which is necessary to install other Python packages:

.. code-block:: bash

    conda activate freefield
    conda install pip

Finally, you have to obtain the freefield package from GitHub:

.. code-block:: bash

    pip install git+https://github.com/pfriedrich-hub/freefield.git

If you plan on using head tracking using the motion sensor, also do this:

.. code-block::bash

    pip install "freefield[sensor]"

Should you want to use the cameras, import this:

.. code-block::bash

    pip install "freefield[cameras]"



If you are only interested in playing around with the code, this is already sufficient and you can head
to the `First Steps`_ section. However, if you want to use the experimental setup,
continue with the hardware drivers section.

Hardware drivers
^^^^^^^^^^^^^^^^

.. note::
    Unfortunately, communication with TDT devices relies on the pywin32 package, which is only available for Windows.
    You can still use freefield on Mac OS or Linux to your experiment code, but connection to the actual processors will be simulated via a dummy.

To use the functionalities of the processors you have to download and install the drivers from the
`TDT Homepage <https://www.tdt.com/support/downloads/>`_   (install TDT Drivers/RPvdsEx as well as ActiveX Controls).

The communication with these processors relies on the pywin32 package. Since installing it with pip can result
in a faulty version, using conda is recommended:

.. code-block:: bash

   conda install pywin32

Finally, to use cameras from the manufacturer FLIR systems, you have to install their Python API (Python version >3.8 is not supported).
Go to the `download page <https://meta.box.lenovo.com/v/link/view/a1995795ffba47dbbe45771477319cc3>`_ and select the correct file for your OS and Python version. For example, if you are using
a 64-Bit Windows and Python 3.8 download spinnaker_python-2.2.0.48-cp38-cp38-win_amd64.zip.
Unpack the .zip file and select the folder. There should be a file inside that ends with `.whl` - install it using pip:

.. code-block:: bash

    pip install spinnaker_python-2.2.0.48-cp38-cp38-win_amd64.whl

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