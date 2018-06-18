#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

import pytest

from landsat_downloader.downloader import LandsatDownloader
from landsat_downloader.exceptions import (
    DownloaderErrors,
)


SCENE_ID_01 = 'LC82210712017013LGN01'
SCENE_ID_00 = 'LC82210712017013LGN00'
PRODUCT_ID_T2 = 'LC08_L1TP_221071_20170113_20170311_01_T1'
# PRODUCT_ID_RT = 'LC08_L1TP_221071_20170113_20170113_01_RT'


def test_download():
    imgs = LandsatDownloader.download_scene(
        bands=['BQA'],
        scene_id=SCENE_ID_00,
        product_id=PRODUCT_ID_T2)
    assert(len(imgs) == 2)
    assert('BQA' in [i['type'] for i in imgs])
    assert('MTL' in [i['type'] for i in imgs])
    imgs = LandsatDownloader.download_scene(
        bands=['BQA'],
        scene_id=SCENE_ID_00,
        metadata=False,
        product_id=PRODUCT_ID_T2)
    assert(len(imgs) == 1)
    assert('BQA' in [i['type'] for i in imgs])

# def test_error():
#     with pytest.raises(DownloaderErrors):
#         LandsatDownloader.download_scene(
#             bands=['BQA'], scene_id=SCENE_ID_01.replace('LGN01', 'LGN03'))


def test_with_wrong_scene_id():
    imgs = LandsatDownloader.download_scene(
        bands=['BQA'],
        scene_id=SCENE_ID_01,
        product_id=PRODUCT_ID_T2)
    assert(len(imgs) == 2)
    assert('BQA' in [i['type'] for i in imgs])
    assert('MTL' in [i['type'] for i in imgs])

    imgs = LandsatDownloader.download_scene(
        bands=['BQA'],
        scene_id=SCENE_ID_01,
        product_id=PRODUCT_ID_T2,
        metadata=False)
    assert(len(imgs) == 1)
    assert('BQA' in [i['type'] for i in imgs])
