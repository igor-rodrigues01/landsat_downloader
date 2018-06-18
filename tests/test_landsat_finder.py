#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

from datetime import datetime

from landsat_downloader.finder import LandsatFinder

PATH_ROW_LIST = [(222, 63), (222, 64)]
START_DATE = datetime(2018, 1, 1)
END_DATE = datetime(2018, 2, 1)


# API
# def test_landsat_finder_errors():
#     try:
#         LandsatFinder.search_scenes_metadata(
#             path_row_list=None,
#             start_date=START_DATE,
#             end_date=END_DATE)
#     except ValueError as exc:
#         _error = "[Error on Search Scenes Metadata]"
#         _msg = "Expected value is: [(path, row), (path, row)...]"

#         assert(str(exc) == "{} {}".format(_error, _msg))


# def test_landsat_finder():
#     scenes = LandsatFinder.search_scenes_metadata(
#         path_row_list=PATH_ROW_LIST,
#         start_date=START_DATE,
#         end_date=END_DATE)
#     assert(len(scenes) == 4)

#     for scene in scenes:
#         assert(scene.get("path") == 222)
#         assert(scene.get("row") == 63 or scene.get("row") == 64)
