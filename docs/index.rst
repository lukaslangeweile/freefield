Freefield: A Toolbox for Conducting Psychoacoustic Experiments
##############################################################

Freefield is an intuitive tool to design and conduct psychoacoustic experiments with Tucker-Davis Technologies (TDT) Hardware in Python.

Initially tailored specifically to only be applied in the anechoic experiment chamber at the University of Leipzig (the freefield laboratory),
it has been further developed to be more dynamically applicable. Now it allows you to easliy create your own unique experiment setups and let freefield handle essential operations like
writing to and reading from buffers, recording signals or loudspoeaker equalization for you.


.. _Installation:

Installation
============

The installation consists of two parts - the Python dependencies and the drivers for the hardware in the experimental setup.
The latter is only relevant if you actually use the devices and is not required if you merely want to play around with the code.

Python dependencies
-------------------
We recommend using Anaconda for the installation. If you are new to Python, take a look at the `install guide <https://www.anaconda.com/docs/getting-started/installation>`_ for Anaconda.

Once you installed Anaconda, create a new environment with the correct Python version (name it "freefield" for example):

.. code-block:: bash

    conda create --name freefield python=3.8

.. Note::
    To use all the functionalities of freefield, Python 3.8 is required. However, if you do not plan to use head pose estimation you also can use more recent versions.

Activate the environment and install pip, which is necessary to install other Python packages:

.. code-block:: bash

    conda activate freefield
    conda install pip

Now install the remaining python packages:

.. code-block:: bash

    pip install opencv-contrib-python numpy setuptools pandas matplotlib pillow h5py h5netcdf scipy slab metawear

Finally, you have to obtain the freefield package from github:

.. code-block:: bash

    pip install git+https://github.com/pfriedrich-hub/freefield.git


If you are only interested in playing around with the code, this is already sufficient and you can head
to the Getting started section. However, if you want to use the experimental setup (only possible on a Windows machine),
continue with the hardware drivers section.

Hardware drivers
----------------

.. Note::
    Unfortunately, communication with TDT devices relies on the pywin32 package, which is only available for Windows.
    You can still use freefield on Mac OS or Linux to your experiment code, but connection to the actual processors will be simulated via a dummy.

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
