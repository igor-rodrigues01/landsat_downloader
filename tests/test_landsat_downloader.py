#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `landsat_downloader` package."""

import pytest
import os

from click.testing import CliRunner

from landsat_downloader import cli

from landsat_downloader.downloader import LandsatDownloader


def test_downloader_bands_creation():
    downloader = LandsatDownloader()

    bands = downloader._create_bands_names(bands=[4,5,6])
    assert(bands==["B4", "B5", "B6"])

    bands = downloader._create_bands_names(bands=[4, 'BQA'])
    assert(bands==["B4", "BQA"])

    bands = downloader._create_bands_names(bands=[i for i in range(1,10)])
    assert(bands==["B{}".format(i) for i in range(1,10)])

def test_downloader_bands_exception():
    downloader = LandsatDownloader()
    
    try:
        bands = downloader._create_bands_names(bands=False)
    except ValueError as exc:
        assert(str(exc)=="[Error on Bands] Expected value is: [1,2,3,4,5...]")

def test_download_bands():
    imgs = LandsatDownloader.download_scenes(bands=["BQA"],
        scene_id_list=['LC82240692018037LGN00'])
    assert(len(imgs)==2)
    assert(imgs[0]['type']=='BQA')
    assert(imgs[0]['name']=='LC08_L1GT_224069_20180206_20180206_01_RT_BQA.TIF')
    
    assert(imgs[1]['type']=='MTL')
    assert(imgs[1]['name']=='LC08_L1GT_224069_20180206_20180206_01_RT_MTL.txt')
    
    os.remove(imgs[0]['path'])
    os.remove(imgs[1]['path'])

def test_download_without_metadata():
    imgs = LandsatDownloader.download_scenes(bands=["BQA"],
        scene_id_list=['LC82240692018037LGN00'], metadata=False)
    assert(len(imgs)==1)
    assert(imgs[0]['type']=='BQA')
    assert(imgs[0]['name']=='LC08_L1GT_224069_20180206_20180206_01_RT_BQA.TIF')

    # Test if files exists
    imgs = LandsatDownloader.download_scenes(bands=["BQA"],
        scene_id_list=['LC82240692018037LGN00'], metadata=False)    
    assert(len(imgs)==1)
    assert(imgs[0]['type']=='BQA')
    assert(imgs[0]['name']=='LC08_L1GT_224069_20180206_20180206_01_RT_BQA.TIF')
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
        imgs = LandsatDownloader.download_scenes(
            bands=11
        )
    except ValueError as exc:
        assert(isinstance(exc, ValueError))


def test_download_scene_with_scene_product():
    try:
        imgs = LandsatDownloader.download_scenes(
            bands=['BQA'],
            product_id_list=['LC08_L1GT_224068_20180310_20180320_01_T2'],
            scene_id_list=['LC82240692018037LGN00']
        )
    except ValueError as exc:
        assert(isinstance(exc, ValueError))


def test_download_scene_without_scene():
    imgs = LandsatDownloader.download_scenes(
        bands=['BQA'], product_id_list=['LC08_L1GT_224068_20180310_20180320_01_T2']
    )
    assert(imgs)
    os.remove(imgs[0]['path'])


def test_download_scene_without_product():
    imgs = LandsatDownloader.download_scenes(
        bands=['BQA'],
        scene_id_list=['LC82240692018037LGN00']
    )
    assert(imgs)
    os.remove(imgs[0]['path'])
