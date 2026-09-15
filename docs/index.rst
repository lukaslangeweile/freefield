Freefield: A Toolbox for Conducting Psychoacoustic Experiments
##############################################################

Freefield is the software we are using to run psychoacoustical experiments (mostly concerning spatial hearing) at the
university of Leipzig. The name is a term from the field of acoustics and describes a situation where no sound reflections occur.
While the code is tailored to our experimental setup, it can be dynamically adapted to a more broader use.

The Setup
---------
Our main setup consists of an arc and a dome shaped array of 48 loudspeakers in a anechoic chamber. The loudspeakers are driven
by two RX8 real time processors from Tucker Davis Technologies (TDT).

Over the course, many lab members felt the need to conduct experiments outside of this main lab due to various reasons, which led
us to adjust the libraries internal logic to allow for the implementation of self-designed, custom setups.


.. _Installation:

Installation
------------

The installation consists of two parts - the Python dependencies and the drivers for the hardware in the experimental setup.
The latter is only relevant if you actually use the devices and is not required if you merely want to play around with the code.

Python dependencies
...................

You will need Python version 3.8 since this is required by tensorflow which is necessary for head pose estimation. If you are new to Python, take a look at the installation guide for the Anaconda distribution.

Once you installed Anaconda, create a new environment with the correct Python version (name it "freefield" for example):

.. code-block:: bash

    conda create --name freefield python=3.12

Activate the environment and install pip, which is necessary to install other Python packages:

.. code-block:: bash

    conda activate freefield
    conda install pip

Now install the remaining python packages:

.. code-block:: bash

    pip install opencv-contrib-python numpy setuptools pandas matplotlib pillow h5py h5netcdf scipy slab metawear

Finally, you have to obtain the freefield package as from github:

.. code-block:: bash

    pip install git+https://github.com/pfriedrich-hub/freefield.git


If you are only interested in playing around with the code, this is already sufficient and you can head
to the getting started section. However, if you want to use the experimental setup (only possible on a Windows machine)
there is more work to be done.

Hardware drivers
................


To use the functionalities of the processors you have to download and install the drivers from the
`TDT Hompage <https://www.tdt.com/support/downloads/>`_   (install TDT Drivers/RPvdsEx as well as ActiveX Controls).

The communication with these processors relies on the pywin32 package. Since installing it with pip can result
in a faulty version, using conda is preferred :\
`conda install pywin32`

Finally, to use cameras from the manufacturer FLIR systems, you have to install their Python API (Python version >3.8 is not supported).
Go to the `download page <https://meta.box.lenovo.com/v/link/view/a1995795ffba47dbbe45771477319cc3>`_ and select the correct file for your OS and Python version. For example, if you are using
a 64-Bit Windows and Python 3.8 download spinnaker_python-2.2.0.48-cp38-cp38-win_amd64.zip.
Unpack the .zip file and select the folder. There should be a file inside that ends with .whl - install it using pip:\
`pip install spinnaker_python-2.2.0.48-cp38-cp38-win_amd64.whl`

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started
   setups
   initialize
   hardware
   worked_examples
   reference
