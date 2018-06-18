============
landsat_downloader
============

.. image:: https://img.shields.io/pypi/v/landsat_downloader.svg
        :target: https://pypi.python.org/pypi/landsat_downloader

.. image:: https://img.shields.io/travis/dagnaldo/landsat_downloader.svg
        :target: https://travis-ci.org/dagnaldo/landsat_downloader

.. image:: https://readthedocs.org/projects/landsat-downloader/badge/?version=latest
        :target: https://landsat-downloader.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


A python package used for download landsat images from EarthExplorer

* Free software: GNU General Public License v3
* Documentation: https://landsat-downloader.readthedocs.io.

Features:
--------

* Find scenes:
	.. code-block:: python
   
		from datetime import datetime, timedelta

		from landsat_downloader.finder import *

		today = datetime.now()
		last_30 = datetime.now() - timedelta(days=30)
		pr_list = [(224, 68), (224, 69)]

		scenes = LandsatFinder.search_scenes_metadata(
			path_row_list=pr_list, 
			start_date=last_30, 
			end_date=today)

* Download scenes:
	.. code-block:: python
    
		from datetime import datetime, timedelta
		from landsat_downloader.downloader import *
		
		scene_id = "LC80020652018130LGN00"
		product_id = "LC08_L1TP_002065_20180510_20180517_01_T1"
		landsat.download_scenes(scenes_list=[scene], bands=[4, "BQA"])
		LandsatDownloader.download_scene(bands=["B6"], scene_id=scene_id, product_id=product_id)

* TODO

- Create CLI;

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
