===============================
CTData EdSight Scraping Tool
===============================

.. role:: bash(code)
   :language: bash

.. image:: https://img.shields.io/pypi/v/ctdata_edsight_scraping_tool.svg
        :target: https://pypi.python.org/pypi/ctdata_edsight_scraping_tool

.. image:: https://img.shields.io/travis/scuerda/ctdata_edsight_scraping_tool.svg
        :target: https://travis-ci.org/scuerda/ctdata_edsight_scraping_tool

.. image:: https://readthedocs.org/projects/ctdata-edsight-scraping-tool/badge/?version=latest
        :target: https://ctdata-edsight-scraping-tool.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/scuerda/ctdata_edsight_scraping_tool/shield.svg
     :target: https://pyup.io/repos/github/scuerda/ctdata_edsight_scraping_tool/
     :alt: Updates


Click based CLI for scraping CTSDE EdSight


* Free software: GPL v3.0


Features
--------

* Command line tool for exploring CT SDE's EdSight database
* Option to download all datasets as a batch operation

How to use
----------

There are a few utility commands to help identify which datasets you might want and what variables they make available.

To see a list of datasets, issue the following command :bash:`edsight datasets`.
To see variables associated with a dataset, issue the following command :bash:`edsight info -d DATASET`.

There are a few assumptions made regarding downloading.

1. You're using this because you want to download a complete dataset.
2. You might want the data at either the district or school level.

Consequentially, the download commands are fairly minimal in terms of options. All variable combinations for a given
geography will be downloaded and file names will reflect the variables contained within. Also, state values are
downloaded and included when fetching either the district or school files. This results in some duplication if you want
both, but we felt it was more appropriate to always include the state data.

If you want just one dataset, use :bash:`edsight fetch`.

You'll need to provide the dataset and a target directory for where the data should be saved.
For example. :bash:`edsight fetch -d 'Chronic Absenteeism' -g District -o ./tmp` will download District-level
Chronic Absenteeism and save the files in the /tmp directory. The default is to fetch the district data, so you actually
can get away with just :bash:`edsight fetch -d 'Chronic Absenteeism' -o ./tmp` and only use the `-g` flag when you want
school data. NOTE: The `-g/--geography` flag will be depricated in an upcoming release and will be replaced with a
`-s/--school` flag to simply this specification.

If you want the whole EdSight catalog, use :bash:`edsight fetch_catalog -o TARGET_DIR`.

This will trigger a lengthy download process, so make sure this is what you want to do. Subdirectories will automatically
be created for each dataset geography.



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

