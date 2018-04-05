#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

import pytest
from datetime import datetime

from landsat_downloader.finder import LandsatFinder

PATH_ROW_LIST = [(222,63), (222, 64)]
START_DATE = datetime(2018, 1, 1)
END_DATE = datetime(2018, 2, 1)

def test_landsat_finder_errors():
    try:
        LandsatFinder.search_scenes_metadata(
            path_row_list=None,
            start_date=START_DATE, 
            end_date=END_DATE)
    except ValueError as exc:
        assert(str(exc) == "[Error on Search Scenes Metadata] Expected value is: [(path, row), (path, row)...]")
        

def test_landsat_finder():
    scenes = LandsatFinder.search_scenes_metadata(
        path_row_list=PATH_ROW_LIST, 
        start_date=START_DATE, 
        end_date=END_DATE)
    assert(len(scenes) == 4)

    for scene in scenes:
        assert(scene.get("path") == 222)
        assert(scene.get("row") == 63 or scene.get("row") == 64)
