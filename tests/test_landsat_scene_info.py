#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

from datetime import datetime

from landsat_downloader.scene_info import SceneInfo, Identifier, Product


def test_scene_info_product_rt():
    scene_id = "LC82240692018037LGN00"
    scene_t2 = "LC08_L1GT_224069_20180206_20180221_01_T2"
    scene_rt = "LC08_L1GT_224069_20180206_20180206_01_RT"

    scene_info = SceneInfo(scene_id=scene_id, product_id=scene_t2)
    product = scene_info.make_rt_product_id(scene_t2)
    assert(product == scene_rt)

    product = scene_info.make_rt_product_id()
    assert(product == scene_rt)


def test_scene_info_product():
    scene = "LC82240682018069LGN00"
    scene_t2 = "LC08_L1GT_224068_20180310_20180320_01_T2"
    scene_rt = "LC08_L1GT_224068_20180310_20180310_01_RT"

    scene_info = SceneInfo(scene_id=scene, product_id=scene_t2)
    assert(scene_info.id_info.path == 224)
    assert(scene_info.id_info.row == 68)
    assert(scene_info.id_info.year == 2018)
    assert(scene_info.id_info.gsi == "LGN")
    assert(scene_info.id_info.version == "00")
    assert(scene_info.id_info.acq_date == datetime(2018, 3, 10).date())

    assert(scene_info.product_id != "{}.TIF".format(scene_t2))
    assert(scene_info.make_rt_product_id(scene_t2) != scene_t2)
    assert(scene_info.make_rt_product_id(scene_t2) == scene_rt)


def test_scene_info_julian_2_date():
    scene = "LC82240682018069LGN00"
    
    scene_info = Identifier(scene_id=scene)
    date = scene_info.julian_2_date("2015070")
    assert(date == datetime(2015, 3, 11).date())

    date = scene_info.julian_2_date("2018069")
    assert(date == datetime(2018, 3, 10).date())

    date = scene_info.julian_2_date("2018001")
    assert(date == datetime(2018, 1, 1).date())


# Add with api info
# def test_scene_info_product_loop():
#     scene = "LC82240682018069LGN0"
#     scene_rt = "LC08_L1GT_224068_20180310_20180310_01_RT"
#     for i in range(2, 5):
#         s = "{}{}".format(scene, i)
#         scene_info = SceneInfo(scene_id=s, product_id=scene_rt)
#         assert(scene_info.scene_id == "LC82240682018069LGN00")
