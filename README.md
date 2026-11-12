![Package](https://github.com/OleBialas/freefield/workflows/Python%20package/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/soundlab/badge/?version=latest)](https://free-field.readthedocs.io/en/latest/?badge=latest)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/OleBialas/freefield/graphs/commit-activity)
![PyPI license](https://img.shields.io/badge/license-MIT-brightgreen)
[![DOI](https://zenodo.org/badge/195776894.svg)](https://zenodo.org/badge/latestdoi/195776894)


The code in this package was written to conduct experiments using a psychoacoustics setup which consists of 48 loudspeakers and 4 cameras in a hemi-anaechoic room. The loudspeakers are driven by two digital signal processors
from Tucker-Davis Technologies (TDT). While large parts of this package are tailored to one specific experimental
setup, some elements (e.g. handling TDT device, head pose estimation) might have broader applicability.

## Installation

Use a dedicated Python environment. The Linux CI runs the test suite on Python
3.8 and 3.12. The example below uses Python 3.12. For a FLIR setup, choose a
Python version supported by the Spinnaker SDK and Python wheel you plan to use.

```bash
conda create --name freefield python=3.12 pip
conda activate freefield
```

Clone or download the Freefield version you want to install. From the root of
that checkout, run the command for your setup. Pip installs the Python
dependencies declared by Freefield.

| Use case | Install command |
| --- | --- |
| Freefield with the base dependencies | `python -m pip install .` |
| Webcam or camera-based head pose estimation | `python -m pip install ".[camera]"` |
| Motion sensor | `python -m pip install ".[sensor]"` |
| Camera and motion sensor | `python -m pip install ".[camera,sensor]"` |

For a FLIR camera, install the camera extra and follow the FLIR steps below.

### TDT processors

On Windows, install the TDT drivers, RPvdsEx, and ActiveX Controls from
[TDT Downloads](https://www.tdt.com/support/downloads/). In the active
Freefield environment, install the Python bindings for ActiveX.

```bash
conda install pywin32
```

On macOS and Linux, Freefield simulates the TDT processor connection.

### FLIR cameras

1. Install the [Teledyne Spinnaker SDK](https://www.teledynevisionsolutions.com/products/spinnaker-sdk)
   for your operating system.
2. Obtain the Python wheel for the **same SDK version**, matching your Python
   version and system architecture. For example, a wheel tagged
   `cp312-cp312-win_amd64` targets 64-bit CPython 3.12 on Windows. See the
   [Spinnaker Python installation guide](https://softwareservices.flir.com/Spinnaker/4.4/getting-started/python.html)
   for the compatibility table for SDK 4.4.
3. In the active Freefield environment, install the downloaded wheel. Replace the
   example path with the path to your wheel.

   ```bash
   python -m pip install "path/to/spinnaker_python-4.4.0.249-cp312-cp312-win_amd64.whl"
   python -c "import PySpin; print(PySpin.System)"
   ```

The Spinnaker wheel provides the `PySpin` import used by Freefield. The
[`pyspin` project on PyPI](https://pypi.org/project/pyspin/) is a terminal
spinner.

### Verify the installation

Run these commands from outside the checkout to check the installed package.

```bash
python -m pip check
python -c "import freefield; print(freefield.__version__); print(len(freefield.read_speaker_table('dome')))"
```

If you installed the camera extra, check its imports as well.

```bash
python -c "import cv2; from headpose import PoseEstimator; print(cv2.__version__)"
```

Continue with the [first steps](docs/getting_started.rst#first-steps) to
initialize a setup and play a sound.
