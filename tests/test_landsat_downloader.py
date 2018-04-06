#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

import os

from click.testing import CliRunner

from landsat_downloader import cli

from landsat_downloader.downloader import LandsatDownloader


SCENE_ID = 'LC82240692018037LGN00'
PRODUCT_ID_T2 = 'LC08_L1GT_224068_20180310_20180320_01_T2'
PRODUCT_ID_RT = 'LC08_L1GT_224069_20180206_20180206_01_RT'


def test_downloader_bands_creation():
    downloader = LandsatDownloader()

    bands = downloader._create_bands_names(bands=[4, 5, 6])
    assert(bands == ["B4", "B5", "B6"])

    bands = downloader._create_bands_names(bands=[4, 'BQA'])
    assert(bands == ["B4", "BQA"])

    bands = downloader._create_bands_names(bands=[i for i in range(1, 10)])
    assert(bands == ["B{}".format(i) for i in range(1, 10)])


def test_downloader_bands_exception():
    downloader = LandsatDownloader()

    MSG = "[Error on Bands] Expected value is: [1,2,3,4,5...]"
    try:
        downloader._create_bands_names(bands=False)
    except ValueError as exc:
        assert(str(exc) == MSG)


def test_download_bands():
    imgs = LandsatDownloader.download_scenes(
        bands=["BQA"], scene_id_list=[SCENE_ID])
    assert(len(imgs) == 2)
    assert(imgs[0]['type'] == 'BQA')
    assert(imgs[0]['name'] ==
           '{}_BQA.TIF'.format(PRODUCT_ID_RT))

    assert(imgs[1]['type'] == 'MTL')
    assert(imgs[1]['name'] == '{}_MTL.txt'.format(PRODUCT_ID_RT))

    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])


def test_download_without_metadata():
    imgs = LandsatDownloader.download_scenes(
        bands=["BQA"],
        scene_id_list=[SCENE_ID],
        metadata=False
        )
    assert(len(imgs) == 1)
    assert(imgs[0]['type'] == 'BQA')
    assert(imgs[0]['name'] == '{}_BQA.TIF'.format(PRODUCT_ID_RT))

    # Test if files exists
    imgs = LandsatDownloader.download_scenes(
        bands=["BQA"], scene_id_list=[SCENE_ID], metadata=False)
    assert(len(imgs) == 1)
    assert(imgs[0]['type'] == 'BQA')
    assert(imgs[0]['name'] == '{}_BQA.TIF'.format(PRODUCT_ID_RT))
    os.remove(imgs[0]['path'])


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'landsat_downloader.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_download_scene_without_scene_product():
    try:
        LandsatDownloader.download_scenes(bands=11)
    except ValueError as exc:
        assert(isinstance(exc, ValueError))


def test_download_scene_with_scene_product():
    try:
        LandsatDownloader.download_scenes(
            bands=['BQA'],
            product_id_list=[PRODUCT_ID_T2],
            scene_id_list=[SCENE_ID]
        )
    except ValueError as exc:
        assert(isinstance(exc, ValueError))


def test_download_scene_without_scene():
    imgs = LandsatDownloader.download_scenes(
        bands=['BQA'], product_id_list=[PRODUCT_ID_T2]
    )
    assert(imgs)
    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])


def test_download_scene_without_product():
    imgs = LandsatDownloader.download_scenes(
        bands=['BQA'], scene_id_list=[SCENE_ID])
    assert(imgs)
    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])
