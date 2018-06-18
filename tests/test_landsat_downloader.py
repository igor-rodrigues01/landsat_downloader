#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

import os
import pytest

from landsat_downloader.downloader import LandsatDownloader


SCENE_ID_22468 = 'LC82240682018069LGN00'
PRODUCT_ID_22468_T2 = 'LC08_L1GT_224068_20180310_20180320_01_T2'
PRODUCT_ID_22468_RT = 'LC08_L1GT_224068_20180310_20180310_01_RT'


SCENE_ID_22469 = 'LC82240692018053LGN00'
PRODUCT_ID_22469_T2 = 'LC08_L1GT_224069_20180222_20180308_01_T2'
PRODUCT_ID_22469_RT = 'LC08_L1GT_224069_20180222_20180222_01_RT'


def test_bands_creation():
    downloader = LandsatDownloader()

    bands = downloader._create_bands_names(bands=[4, 5, 6])
    assert(bands == ["B4", "B5", "B6"])

    bands = downloader._create_bands_names(bands=[4, 'BQA'])
    assert(bands == ["B4", "BQA"])

    bands = downloader._create_bands_names(bands=[i for i in range(1, 10)])
    assert(bands == ["B{}".format(i) for i in range(1, 10)])


def test_bands_exception():
    downloader = LandsatDownloader()

    MSG = "[Error on Bands] Expected value is: [1,2,3,4,5...]"
    try:
        downloader._create_bands_names(bands=False)
    except ValueError as exc:
        assert(str(exc) == MSG)


def test_download_bands():
    imgs = LandsatDownloader.download_scene(
        bands=["BQA"], scene_id=SCENE_ID_22469, product_id=PRODUCT_ID_22469_T2)
    assert(len(imgs) == 2)
    assert(imgs[0]['type'] == 'BQA')
    assert(imgs[0]['name'] ==
           '{}_BQA.TIF'.format(PRODUCT_ID_22469_RT))

    assert(imgs[1]['type'] == 'MTL')
    assert(imgs[1]['name'] == '{}_MTL.txt'.format(PRODUCT_ID_22469_RT))

    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])


def test_download_without_metadata():
    imgs = LandsatDownloader.download_scene(
        bands=["BQA"],
        scene_id=SCENE_ID_22469,
        product_id=PRODUCT_ID_22469_T2,
        metadata=False
    )
    assert(len(imgs) == 1)
    assert(imgs[0]['type'] == 'BQA')
    assert(imgs[0]['name'] == '{}_BQA.TIF'.format(PRODUCT_ID_22469_RT))

    # Test if files exists
    imgs = LandsatDownloader.download_scene(
        bands=["BQA"], 
        scene_id=SCENE_ID_22469,
        product_id=PRODUCT_ID_22469_T2,
        metadata=False)
    assert(len(imgs) == 1)
    assert(imgs[0]['type'] == 'BQA')
    assert(imgs[0]['name'] == '{}_BQA.TIF'.format(PRODUCT_ID_22469_RT))
    os.remove(imgs[0]['path'])


def test_download_scene_without_scene_product():
    with pytest.raises(ValueError):
        LandsatDownloader.download_scene(bands=11)


def test_download_scene_with_scene_product():
    with pytest.raises(ValueError):
        LandsatDownloader.download_scene(
            bands=['BQA'],
            scene_id=SCENE_ID_22469
        )


def test_download_scene_with_null_list():
    with pytest.raises(ValueError):
        LandsatDownloader.download_scene(bands=[])


def test_download_scene_with_scen_id_list():
    imgs = LandsatDownloader.download_scene(
        bands=['BQA'], 
        scene_id=SCENE_ID_22469,
        product_id=PRODUCT_ID_22469_RT)
    assert("{}_BQA.TIF".format(PRODUCT_ID_22469_RT)
           in [i['name'] for i in imgs])
    assert('BQA' in [i['type'] for i in imgs])
    assert('MTL' in [i['type'] for i in imgs])
    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])


def test_download_scene_without_product_T2():
    imgs = LandsatDownloader.download_scene(
        bands=['BQA'], 
        scene_id=SCENE_ID_22468,
        product_id=PRODUCT_ID_22468_T2
    )
    product_id = "{}_BQA.TIF".format(PRODUCT_ID_22468_RT)
    assert(product_id in [i['name'] for i in imgs])
    assert('BQA' in [i['type'] for i in imgs])
    assert('MTL' in [i['type'] for i in imgs])
    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])


def test_download_scene_without_product_T1():
    imgs = LandsatDownloader.download_scene(
        bands=['BQA'], 
        scene_id=SCENE_ID_22469, 
        product_id=PRODUCT_ID_22469_T2
    )
    assert("{}_BQA.TIF".format(PRODUCT_ID_22469_RT)
           in [i['name'] for i in imgs])
    assert('BQA' in [i['type'] for i in imgs])
    assert('MTL' in [i['type'] for i in imgs])
    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])
