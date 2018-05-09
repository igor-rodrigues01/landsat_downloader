#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

from datetime import datetime

from landsat_downloader.scene_info import SceneInfo


def test_scene_info_product_rt():
    scene = "LC08_L1GT_224069_20180206_20180301_01_T1"
    scene_rt = "LC08_L1GT_224069_20180206_20180206_01_RT"

    scene_info = SceneInfo(product_id=scene)
    product = scene_info.make_rt_product_id(scene)

    assert(product == scene_rt)


def test_scene_info_product():
    scene = "LC82240682018069LGN00"
    scene_t2 = "LC08_L1GT_224068_20180310_20180320_01_T2"
    scene_rt = "LC08_L1GT_224068_20180310_20180310_01_RT"

    scene_info = SceneInfo(scene_id=scene)
    info = scene_info.get_info_from_scene_id(scene)
    assert(info.get('path') == 224)
    assert(info.get('row') == 68)
    assert(info.get('year') == 2018)
    assert(info.get('gsi') == "LGN")
    assert(info.get('version') == "00")
    assert(info.get('acq_date') == datetime(2018, 3, 10).date())

    assert(scene_info.product_id != "{}.TIF".format(scene_t2))
    assert(scene_info.product_id == scene_t2)
    assert(scene_info.make_rt_product_id(scene_t2) != scene_t2)
    assert(scene_info.make_rt_product_id(scene_t2) == scene_rt)


def test_scene_info_julian_2_date():
    scene = "LC82240682018069LGN00"
    scene_info = SceneInfo(scene_id=scene)
    date = scene_info.julian_2_date("2015070")
    assert(date == datetime(2015, 3, 11).date())

    date = scene_info.julian_2_date("2018069")
    assert(date == datetime(2018, 3, 10).date())
