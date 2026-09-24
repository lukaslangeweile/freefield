from setuptools import setup, find_packages
import re

with open('README.md') as f:
    readme = f.read()

# extract version
with open('freefield/__init__.py') as file:
    for line in file.readlines():
        m = re.match("__version__ *= *['\"](.*)['\"]", line)
        if m:
            version = m.group(1)

CAMERA_REQUIRES = [
    "opencv-python",
    "headpose",
    "pillow",
    "PySpin"
]

SENSOR_REQUIRES = [
    "metawear",
]



setup(name='freefield',
      version=version,
      description='Toolbox for Psychoacoustic Experiments.',
      long_description=readme,
      long_description_content_type='text/markdown',
      url='https://github.com/pfriedrich-hub/freefield.git',
      authors='Ole Bialas, Paul Friedrich, Lukas Lange',
      author_email='bialas@cbs.mpg.de',
      license='MIT',
      python_requires='>=3.6',
      install_requires=['numpy',
                        'setuptools',
                        'pandas',
                        'matplotlib',
                        'scipy',
                        'slab'],
      extras_require={
          "camera": CAMERA_REQUIRES,
          "sensor": SENSOR_REQUIRES,
          "headpose": CAMERA_REQUIRES + SENSOR_REQUIRES,
      },
      packages=find_packages(),
      package_data={'freefield': ['data/tables/*', 'data/sounds/*', 'data/sounds/USOs/*',
                                  'data/sounds/tts-numbers_n13_resamp_48828/*', 'data/sounds/numbers_0-99_tts/*'
                                  'data/rcx/*', 'data/models/*',
                                  'data/models/pose_model/*',
                                  'data/models/pose_model/variables/*',
                                  'old_tests/*', 'old_tests/images/*']},
      include_package_data=True,
      zip_safe=False)

# add pypi.org/classifiers
