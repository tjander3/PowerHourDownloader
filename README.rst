===================
PowerHourDownloader
===================


.. image:: https://img.shields.io/pypi/v/powerhourdownloader.svg
        :target: https://pypi.python.org/pypi/powerhourdownloader

.. image:: https://img.shields.io/travis/tjander3/powerhourdownloader.svg
        :target: https://travis-ci.com/tjander3/powerhourdownloader

.. image:: https://readthedocs.org/projects/powerhourdownloader/badge/?version=latest
        :target: https://powerhourdownloader.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/tjander3/powerhourdownloader/shield.svg
     :target: https://pyup.io/repos/github/tjander3/powerhourdownloader/
     :alt: Updates



Python project to download powerhours in one mp4


* Free software: MIT license
* Documentation: https://powerhourdownloader.readthedocs.io.


Python environment
--------

Create a virtual env: `python<version> -m venv <virtual-environment-name>`

Activate environment: `. ./env/Scripts/activate`

Install packages in environment: `python -m pip install -r requirements_dev.txt`


Building
--------

To build this for release we use pyinstaller

to build on windows do the following:

- Verify you can run flask web app locally with your current python environment
- Build with pyinstaller from webapp directory: `pyinstaller --paths C:\Users\tjand\git\PowerHourDownloader -w -F
 --add-data "templates;templates" .\hello_world.py`




Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
